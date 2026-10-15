# ABOUTME: Downloads and processes Compustat short interest data, prioritizing the legacy feed when overlaps occur
# ABOUTME: Mirrors the Stata implementation (G_CompustatShortInterest.do) without relying on the CCM linking table
"""
Inputs:
- comp.sec_shortint_legacy (1973-2024)
- comp.sec_shortint (2006+)

Outputs:
- ../pyData/Intermediate/monthlyShortInterest.parquet

How to run: from Signals/pyCode, run python3 DataDownloads/CompustatShortInterest.py

Use the project Python environment at /opt/venv/projects/openap.
"""

import os
import sys
from typing import Literal

import pandas as pd
from sqlalchemy import create_engine
from dotenv import load_dotenv

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from config import DEBUG_MODE
from utils.debug_mode import get_debug_row_limit

DEBUG_ROWS = get_debug_row_limit("CompustatShortInterest")

load_dotenv()

engine = create_engine(
    f"postgresql://{os.getenv('WRDS_USERNAME')}:{os.getenv('WRDS_PASSWORD')}@wrds-pgdata.wharton.upenn.edu:9737/wrds"
)


def _build_query(source: Literal["legacy", "new"]) -> str:
    table = "comp.sec_shortint_legacy" if source == "legacy" else "comp.sec_shortint"
    query = f"""
SELECT a.gvkey, a.iid, a.shortint, a.shortintadj, a.datadate
FROM {table} as a
"""
    if DEBUG_MODE:
        query += f" LIMIT {DEBUG_ROWS}"
    return query


def _collapse_monthly(df: pd.DataFrame) -> pd.DataFrame:
    """Keep each measure's earliest nonmissing value per company-month."""

    if df.empty:
        return df.assign(time_avail_m=pd.NaT)

    df = df.copy()
    df["datadate"] = pd.to_datetime(df["datadate"])
    df["time_avail_m"] = df["datadate"].dt.to_period("M").dt.to_timestamp()
    df = df.sort_values(["gvkey", "time_avail_m", "datadate"])

    def first_non_missing(series: pd.Series) -> float | None:
        non_missing = series.dropna()
        return non_missing.iloc[0] if not non_missing.empty else None

    company_month_groups = df.groupby(["gvkey", "time_avail_m"], as_index=False)
    grouped = company_month_groups.agg(
        shortint=("shortint", first_non_missing),
        shortintadj=("shortintadj", first_non_missing),
    )
    return grouped


# Build monthly short-interest measures from the preferred legacy history.
query_legacy = _build_query("legacy")
if DEBUG_MODE:
    print(f"DEBUG MODE: Limiting to {DEBUG_ROWS} rows", flush=True)

print(f"Downloading legacy short interest data...", flush=True)
si_legacy = pd.read_sql_query(query_legacy, engine)
print(f"Downloaded {len(si_legacy)} legacy short interest records")

monthly_si_legacy = _collapse_monthly(si_legacy)
monthly_si_legacy["legacyFile"] = 1
print(f"After monthly aggregation: {len(monthly_si_legacy)} legacy records")

# Add the newer feed to extend coverage where the legacy history is absent.
query_new = _build_query("new")
print(f"Downloading new short interest data...", flush=True)
si_new = pd.read_sql_query(query_new, engine)
engine.dispose()
print(f"Downloaded {len(si_new)} new short interest records")

monthly_si_new = _collapse_monthly(si_new)
print(f"After monthly aggregation: {len(monthly_si_new)} new records")

monthly_si = pd.concat([monthly_si_legacy, monthly_si_new], ignore_index=True)
print(f"After combining: {len(monthly_si)} total records")

# Retain the legacy measure whenever both feeds cover the same company-month.
monthly_si['nobs'] = monthly_si.groupby(['gvkey', 'time_avail_m'])['gvkey'].transform('count')
is_superseded_new_record = (monthly_si['nobs'] > 1) & (monthly_si['legacyFile'] != 1)
monthly_si = monthly_si[~is_superseded_new_record]
monthly_si = monthly_si.drop(columns=['nobs', 'legacyFile'])

# Report any repeated company-months remaining after source selection.
duplicates = monthly_si.duplicated(subset=['gvkey', 'time_avail_m'], keep=False)
print(f"Duplicate check: {duplicates.sum()} duplicate gvkey-time_avail_m combinations")

# Express short-interest amounts in millions of shares and standardize company identifiers.
monthly_si['shortint'] = monthly_si['shortint'] / 1e6
monthly_si['shortintadj'] = monthly_si['shortintadj'] / 1e6
monthly_si['gvkey'] = pd.to_numeric(monthly_si['gvkey'], errors='coerce')

# Save the combined monthly short-interest history for downstream signals.
monthly_si.to_parquet("../pyData/Intermediate/monthlyShortInterest.parquet")

print(f"Monthly Short Interest data saved with {len(monthly_si)} records")
print(f"Date range: {monthly_si['time_avail_m'].min()} to {monthly_si['time_avail_m'].max()}")
print(f"Unique companies: {monthly_si['gvkey'].nunique()}")

print("\nSample data:")
print(monthly_si.head())

print("\nMissing data:")
print(f"shortint: {monthly_si['shortint'].isna().sum()} missing")
print(f"shortintadj: {monthly_si['shortintadj'].isna().sum()} missing")
