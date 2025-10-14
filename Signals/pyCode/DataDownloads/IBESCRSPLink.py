# ABOUTME: Downloads and standardizes the CRSP-IBES link directly from WRDS.
# ABOUTME: Produces a monthly permno/ticker mapping with match scores for downstream predictors.
"""
Inputs:
- Env vars `WRDS_USERNAME` and `WRDS_PASSWORD` for database access
- ../pyData/Intermediate/monthlyCRSP.parquet (columns: permno, time_avail_m)

Outputs:
- ../pyData/Intermediate/IBESCRSPLinkingTable.parquet

How to run:
- From Signals/pyCode/: `python3 DataDownloads/CRSPIBESLink.py`
- Example (debug mode with MAX_ROWS_DL=100): `MAX_ROWS_DL=100 python3 DataDownloads/CRSPIBESLink.py`
"""

import os
import sys
from typing import List

import pandas as pd
from dotenv import load_dotenv
from sqlalchemy import create_engine

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from config import MAX_ROWS_DL  # noqa: E402


def enforce_column_schema(df: pd.DataFrame, columns: List[str]) -> pd.DataFrame:
    """Return a copy of df with the desired columns and pandas dtypes."""
    df_out = df.copy()

    # Keep only requested columns in the specified order
    df_out = df_out.reindex(columns=columns)

    # Apply dtypes / cleanup to match historical expectations
    if "tickerIBES" in df_out.columns:
        df_out["tickerIBES"] = df_out["tickerIBES"].fillna("").astype(str)

    if "permno" in df_out.columns:
        df_out["permno"] = pd.to_numeric(df_out["permno"], errors="coerce").astype("Int32")

    if "time_avail_m" in df_out.columns:
        df_out["time_avail_m"] = pd.to_datetime(df_out["time_avail_m"], errors="coerce")

    if "score" in df_out.columns:
        df_out["score"] = pd.to_numeric(df_out["score"], errors="coerce").astype("Int32")

    return df_out


def main() -> None:
    load_dotenv()

    print("Processing CRSP-IBES linking data...")

    # Ensure output directory exists
    os.makedirs("../pyData/Intermediate", exist_ok=True)

    username = os.getenv("WRDS_USERNAME")
    password = os.getenv("WRDS_PASSWORD")
    if not username or not password:
        raise RuntimeError("WRDS credentials not found in environment variables.")

    print("Querying IBES-CRSP link from WRDS database...")
    engine = create_engine(
        f"postgresql://{username}:{password}@wrds-pgdata.wharton.upenn.edu:9737/wrds"
    )

    query = """
        SELECT ticker, permno, ncusip, sdate, edate, score
        FROM wrdsapps.ibcrsphist AS a
        WHERE permno IS NOT NULL
    """

    iblink_raw = pd.read_sql_query(query, engine)
    print(f"Loaded {len(iblink_raw):,} IBES-CRSP linking records from WRDS")

    engine.dispose()

    # Convert start/end dates to monthly timestamps
    iclink = iblink_raw.copy()
    iclink["sdate_m"] = pd.to_datetime(iclink["sdate"]).dt.to_period("M").dt.to_timestamp()
    iclink["edate_m"] = (
        pd.to_datetime(iclink["edate"]).dt.to_period("M") - 1
    ).dt.to_timestamp()
    iclink = iclink.drop(columns=["sdate", "edate"])

    # Load CRSP monthly calendar to align date ranges
    crsp_monthly = pd.read_parquet(
        "../pyData/Intermediate/monthlyCRSP.parquet",
        columns=["permno", "time_avail_m"],
    )

    merged = iclink.merge(crsp_monthly, on="permno", how="outer")
    merged = merged.query("ticker.notna()").copy()
    merged = merged[
        (merged["time_avail_m"].notna())
        & (merged["time_avail_m"] >= merged["sdate_m"])
        & (merged["time_avail_m"] <= merged["edate_m"])
    ]

    print(f"Joined IBES-CRSP link with CRSP monthly data: {len(merged):,} rows")

    # De-duplicate by keeping the lowest score within each permno-month
    merged = (
        merged.sort_values(["permno", "time_avail_m", "score"], ascending=[True, True, True])
        .groupby(["permno", "time_avail_m"], as_index=False)
        .first()
    )
    print(f"Removed duplicates by score: {len(merged):,} rows")

    merged = merged.rename(columns={"ticker": "tickerIBES"})

    desired_columns = ["tickerIBES", "permno", "time_avail_m", "score"]
    final_data = enforce_column_schema(merged, desired_columns)

    if MAX_ROWS_DL > 0:
        final_data = final_data.head(MAX_ROWS_DL)
        print(f"DEBUG MODE: Limited to {MAX_ROWS_DL} rows")

    output_path = "../pyData/Intermediate/IBESCRSPLinkingTable.parquet"
    final_data.to_parquet(output_path, index=False)

    print(f"IBES-CRSP Linking Table saved with {len(final_data):,} records")
    print(f"Unique permnos: {final_data['permno'].nunique()}")
    print(f"Unique IBES tickers: {final_data['tickerIBES'].nunique()}")

    print("\nSample data:")
    print(final_data.head())


if __name__ == "__main__":
    main()
