# ABOUTME: Downloads and processes Compustat short interest data, prioritizing the legacy feed when overlaps occur
# ABOUTME: Mirrors the Stata implementation (G_CompustatShortInterest.do) without relying on the CCM linking table
"""
Inputs:
- comp.sec_shortint_legacy (1973-2024)
- comp.sec_shortint (2006+)

Outputs:
- ../pyData/Intermediate/monthlyShortInterest.parquet

How to run: python3 CompustatShortInterest.py
"""

import os
import sys
from typing import Literal

import pandas as pd
from sqlalchemy import create_engine
from dotenv import load_dotenv

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from config import MAX_ROWS_DL

load_dotenv()

# Database connection setup
engine = create_engine(
    f"postgresql://{os.getenv('WRDS_USERNAME')}:{os.getenv('WRDS_PASSWORD')}@wrds-pgdata.wharton.upenn.edu:9737/wrds"
)

def _build_query(source: Literal["legacy", "new"]) -> str:
    table = "comp.sec_shortint_legacy" if source == "legacy" else "comp.sec_shortint"
    query = f"""
SELECT a.gvkey, a.iid, a.shortint, a.shortintadj, a.datadate
FROM {table} as a
"""
    if MAX_ROWS_DL > 0:
        query += f" LIMIT {MAX_ROWS_DL}"
    return query


def _collapse_monthly(df: pd.DataFrame) -> pd.DataFrame:
    """Replicate Stata gcollapse (firstnm) by gvkey and month."""

    if df.empty:
        return df.assign(time_avail_m=pd.NaT)

    df = df.copy()
    df["datadate"] = pd.to_datetime(df["datadate"])
    df["time_avail_m"] = df["datadate"].dt.to_period("M").dt.to_timestamp()
    df = df.sort_values(["gvkey", "time_avail_m", "datadate"])

    def first_non_missing(series: pd.Series) -> float | None:
        non_missing = series.dropna()
        return non_missing.iloc[0] if not non_missing.empty else None

    grouped = df.groupby(["gvkey", "time_avail_m"], as_index=False).agg(
        shortint=("shortint", first_non_missing),
        shortintadj=("shortintadj", first_non_missing),
    )
    return grouped


# Download and process legacy short interest data (1973-2024)
query_legacy = _build_query("legacy")
if MAX_ROWS_DL > 0:
    print(f"DEBUG MODE: Limiting to {MAX_ROWS_DL} rows", flush=True)

print(f"Downloading legacy short interest data...", flush=True)
si_legacy = pd.read_sql_query(query_legacy, engine)
print(f"Downloaded {len(si_legacy)} legacy short interest records")

monthly_si_legacy = _collapse_monthly(si_legacy)
monthly_si_legacy["legacyFile"] = 1
print(f"After monthly aggregation: {len(monthly_si_legacy)} legacy records")

# Download and process new short interest data (2006+)
query_new = _build_query("new")
print(f"Downloading new short interest data...", flush=True)
si_new = pd.read_sql_query(query_new, engine)
engine.dispose()
print(f"Downloaded {len(si_new)} new short interest records")

monthly_si_new = _collapse_monthly(si_new)
print(f"After monthly aggregation: {len(monthly_si_new)} new records")

# Combine legacy and new data at the gvkey-month level
monthly_si = pd.concat([monthly_si_legacy, monthly_si_new], ignore_index=True)
print(f"After combining: {len(monthly_si)} total records")

# Prioritize legacy data when both sources have data for same firm-month
monthly_si['nobs'] = monthly_si.groupby(['gvkey', 'time_avail_m'])['gvkey'].transform('count')
monthly_si = monthly_si[~((monthly_si['nobs'] > 1) & (monthly_si['legacyFile'] != 1))]
monthly_si = monthly_si.drop(columns=['nobs', 'legacyFile'])

# Verify no duplicate observations remain
duplicates = monthly_si.duplicated(subset=['gvkey', 'time_avail_m'], keep=False)
print(f"Duplicate check: {duplicates.sum()} duplicate gvkey-time_avail_m combinations")

# Scale values and finalize data
monthly_si['shortint'] = monthly_si['shortint'] / 1e6
monthly_si['shortintadj'] = monthly_si['shortintadj'] / 1e6
monthly_si['gvkey'] = pd.to_numeric(monthly_si['gvkey'], errors='coerce')

# Save final data
monthly_si.to_parquet("../pyData/Intermediate/monthlyShortInterest.parquet")

print(f"Monthly Short Interest data saved with {len(monthly_si)} records")
print(f"Date range: {monthly_si['time_avail_m'].min()} to {monthly_si['time_avail_m'].max()}")
print(f"Unique companies: {monthly_si['gvkey'].nunique()}")

print("\nSample data:")
print(monthly_si.head())

print("\nMissing data:")
print(f"shortint: {monthly_si['shortint'].isna().sum()} missing")
print(f"shortintadj: {monthly_si['shortintadj'].isna().sum()} missing")
