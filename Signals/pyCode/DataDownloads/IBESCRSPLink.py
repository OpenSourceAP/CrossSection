# ABOUTME: Downloads and standardizes the CRSP-IBES link directly from WRDS.
# ABOUTME: Produces a monthly permno/ticker mapping with match scores for downstream predictors.
"""
Inputs:
- Env vars `WRDS_USERNAME` and `WRDS_PASSWORD` for database access
- wrdsapps_link_crsp_ibes.ibcrsphist (historical ticker/PERMNO intervals)
- Full CRSP stock-month calendar (permno, time_avail_m); in debug mode,
  OPENAP_CRSP_CALENDAR must point to a separate full keys-only extract from msf_v2

Outputs:
- OPENAP_DATA_ROOT/Intermediate/IBESCRSPLinkingTable.parquet

How to run:
- From repository root: `OPENAP_DATA_ROOT=Signals/pyData-v2 OPENAP_CRSP_CALENDAR=Signals/pyData-v2/Inputs/CRSP_stock_month_calendar.parquet /opt/venv/projects/openap/bin/python3 Signals/pyCode/DataDownloads/IBESCRSPLink.py`
- For Stage 1, set DEBUG_MODE=True in memory; the link uses the full calendar.
"""

import os
import sys
from typing import List

import pandas as pd
from dotenv import load_dotenv

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from utils.debug_mode import log_selection  # noqa: E402
from utils.wrds_connection import get_wrds_engine, release_wrds_engine
from utils.download_paths import intermediate_path, crsp_calendar_path
from config import DEBUG_MODE


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
    log_selection("IBESCRSPLink")
    load_dotenv()

    print("Processing CRSP-IBES linking data...")

    # Validate the complete calendar before issuing any database query.
    calendar_path = crsp_calendar_path()
    crsp_monthly = pd.read_parquet(calendar_path, columns=["permno", "time_avail_m"])
    crsp_monthly["time_avail_m"] = pd.to_datetime(crsp_monthly["time_avail_m"])
    keys = ["permno", "time_avail_m"]
    if crsp_monthly.empty or crsp_monthly[keys].isna().any().any() or crsp_monthly.duplicated(keys).any():
        raise ValueError("The CRSP calendar is empty or has null/duplicate security-month keys.")
    if DEBUG_MODE and (
        crsp_monthly.time_avail_m.min() > pd.Timestamp("1976-01-01")
        or crsp_monthly.time_avail_m.max() < pd.Timestamp("2024-12-01")
    ):
        raise ValueError("Debug IBES requires a full CRSP stock-month calendar, not the 1981 monthly debug output.")
    print(f"Full CRSP calendar: {len(crsp_monthly):,} distinct stock-months, "
          f"{crsp_monthly.time_avail_m.min():%Y-%m} to {crsp_monthly.time_avail_m.max():%Y-%m}")

    username = os.getenv("WRDS_USERNAME")
    password = os.getenv("WRDS_PASSWORD")
    if not username or not password:
        raise RuntimeError("WRDS credentials not found in environment variables.")

    print("Querying IBES-CRSP link from WRDS database...")
    engine = get_wrds_engine()

    query = """
        SELECT ticker, permno, sdate, edate, score
        FROM wrdsapps_link_crsp_ibes.ibcrsphist
        WHERE permno IS NOT NULL
    """

    try:
        iblink_raw = pd.read_sql_query(query, engine)
    finally:
        release_wrds_engine(engine)
    print(f"Loaded {len(iblink_raw):,} IBES-CRSP linking records from WRDS")

    # Convert start/end dates to monthly timestamps
    iclink = iblink_raw.copy()
    iclink["sdate_m"] = pd.to_datetime(iclink["sdate"]).dt.to_period("M").dt.to_timestamp()
    iclink["edate_m"] = (
        pd.to_datetime(iclink["edate"]).dt.to_period("M") - 1
    ).dt.to_timestamp()
    iclink = iclink.drop(columns=["sdate", "edate"])

    # Each link can cover many months and a PERMNO can have several link
    # intervals. Calendar keys are unique; this expansion is intentional.
    merged = iclink.merge(crsp_monthly, on="permno", how="inner")
    merged = merged.query("ticker.notna()").copy()
    merged = merged[
        (merged["time_avail_m"].notna())
        & (merged["time_avail_m"] >= merged["sdate_m"])
        & (merged["time_avail_m"] <= merged["edate_m"])
    ]

    print(f"Joined IBES-CRSP link with CRSP monthly data: {len(merged):,} rows")

    # Keep the lowest score per stock-month; ties go to the first IBES ticker.
    overlapping = merged.duplicated(keys, keep=False)
    overlap_groups = merged.loc[overlapping, keys].drop_duplicates().shape[0]
    print(f"Overlapping link candidates: {overlapping.sum():,} rows across "
          f"{overlap_groups:,} stock-months")
    merged = (
        merged.sort_values(["permno", "time_avail_m", "score", "ticker"])
        .groupby(["permno", "time_avail_m"], as_index=False)
        .first()
    )
    print(f"Resolved {overlapping.sum() - overlap_groups:,} extra link candidates; "
          f"{len(merged):,} unique stock-months")

    merged = merged.rename(columns={"ticker": "tickerIBES"})

    desired_columns = ["tickerIBES", "permno", "time_avail_m", "score"]
    final_data = enforce_column_schema(merged, desired_columns)

    output_path = intermediate_path("IBESCRSPLinkingTable.parquet")
    final_data.to_parquet(output_path, index=False)

    print(f"IBES-CRSP Linking Table saved with {len(final_data):,} records")
    print(f"Unique permnos: {final_data['permno'].nunique()}")
    print(f"Unique IBES tickers: {final_data['tickerIBES'].nunique()}")

    print("\nSample data:")
    print(final_data.head())


if __name__ == "__main__":
    main()
