# ABOUTME: Downloads and processes Compustat short interest data, combining legacy and new sources
# ABOUTME: Joins with CCMLinkingTable to add permno and aggregates to monthly permno-level data
"""
Inputs:
- comp.sec_shortint_legacy (1973-2024)
- comp.sec_shortint (2006+)
- ../pyData/Intermediate/CCMLinkingTable.parquet

Outputs:
- ../pyData/Intermediate/monthlyShortInterest.parquet

How to run: python3 G_CompustatShortInterest.py
"""

import os
from sqlalchemy import create_engine
import pandas as pd
from dotenv import load_dotenv
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from config import MAX_ROWS_DL
from utils.column_standardizer_yaml import standardize_columns

load_dotenv()

# Database connection setup
engine = create_engine(
    f"postgresql://{os.getenv('WRDS_USERNAME')}:{os.getenv('WRDS_PASSWORD')}@wrds-pgdata.wharton.upenn.edu:9737/wrds"
)

# Download legacy short interest data (1973-2024)
QUERY_LEGACY = """
SELECT a.gvkey, a.iid, a.shortint, a.shortintadj, a.datadate
FROM comp.sec_shortint_legacy as a
"""

if MAX_ROWS_DL > 0:
    QUERY_LEGACY += f" LIMIT {MAX_ROWS_DL}"
    print(f"DEBUG MODE: Limiting to {MAX_ROWS_DL} rows", flush=True)

si_legacy = pd.read_sql_query(QUERY_LEGACY, engine)
print(f"Downloaded {len(si_legacy)} legacy short interest records")

# Create monthly time variable for legacy data
si_legacy['datadate'] = pd.to_datetime(si_legacy['datadate'])
si_legacy['time_avail_m'] = si_legacy['datadate'].dt.to_period('M').dt.to_timestamp()

# Aggregate legacy data to monthly level using first non-missing values
def first_non_missing(series):
    non_missing = series.dropna()
    return non_missing.iloc[0] if len(non_missing) > 0 else None

monthly_si_legacy = si_legacy.groupby(['gvkey', 'time_avail_m']).agg({
    'shortint': first_non_missing,
    'shortintadj': first_non_missing
}).reset_index()

monthly_si_legacy['legacyFile'] = 1
print(f"After monthly aggregation: {len(monthly_si_legacy)} legacy records")

# Download new short interest data (2006+)
QUERY_NEW = """
SELECT a.gvkey, a.iid, a.shortint, a.shortintadj, a.datadate
FROM comp.sec_shortint as a
"""

if MAX_ROWS_DL > 0:
    QUERY_NEW += f" LIMIT {MAX_ROWS_DL}"

si_new = pd.read_sql_query(QUERY_NEW, engine)
engine.dispose()
print(f"Downloaded {len(si_new)} new short interest records")

# Create monthly time variable for new data
si_new['datadate'] = pd.to_datetime(si_new['datadate'])
si_new['time_avail_m'] = si_new['datadate'].dt.to_period('M').dt.to_timestamp()

# Aggregate new data to monthly level
monthly_si_new = si_new.groupby(['gvkey', 'time_avail_m']).agg({
    'shortint': first_non_missing,
    'shortintadj': first_non_missing
}).reset_index()

print(f"After monthly aggregation: {len(monthly_si_new)} new records")

# Combine legacy and new data
monthly_si = pd.concat([monthly_si_legacy, monthly_si_new], ignore_index=True)
print(f"After combining: {len(monthly_si)} total records")

# Prioritize legacy data when both sources have data for same firm-month
monthly_si['nobs'] = monthly_si.groupby(['gvkey', 'time_avail_m'])['gvkey'].transform('count')
monthly_si = monthly_si[~((monthly_si['nobs'] > 1) & (monthly_si['legacyFile'] != 1))]
monthly_si = monthly_si.drop(columns=['nobs', 'legacyFile'])

# Verify no duplicate observations remain
duplicates = monthly_si.duplicated(subset=['gvkey', 'time_avail_m'], keep=False)
assert not duplicates.any(), f"Found {duplicates.sum()} duplicate gvkey-time_avail_m combinations"

# Scale values and finalize data
monthly_si['shortint'] = monthly_si['shortint'] / 1e6
monthly_si['shortintadj'] = monthly_si['shortintadj'] / 1e6
monthly_si['gvkey'] = pd.to_numeric(monthly_si['gvkey'], errors='coerce')

# Apply column standardization
monthly_si = standardize_columns(monthly_si, "monthlyShortInterest")

# Save final data
os.makedirs("../pyData/Intermediate", exist_ok=True)
monthly_si.to_parquet("../pyData/Intermediate/monthlyShortInterest.parquet")

print(f"Monthly Short Interest data saved with {len(monthly_si)} records")
print(f"Date range: {monthly_si['time_avail_m'].min()} to {monthly_si['time_avail_m'].max()}")
print(f"Unique companies: {monthly_si['gvkey'].nunique()}")

print("\nSample data:")
print(monthly_si.head())

print("\nMissing data:")
print(f"shortint: {monthly_si['shortint'].isna().sum()} missing")
print(f"shortintadj: {monthly_si['shortintadj'].isna().sum()} missing")