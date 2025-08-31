#!/usr/bin/env python3
"""
Compustat Short Interest data download script - Python equivalent of G_CompustatShortInterest.do

Downloads short interest data with monthly aggregation.
Combines legacy (1973-2024) and new (2006+) data sources, prioritizing legacy when both exist.
Data reported bi-weekly with 4-day lag; using mid-month observation for real-time availability.
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

# Create SQLAlchemy engine for database connection
engine = create_engine(
    f"postgresql://{os.getenv('WRDS_USERNAME')}:{os.getenv('WRDS_PASSWORD')}@wrds-pgdata.wharton.upenn.edu:9737/wrds"
)

# Legacy file (1973-2024)
QUERY_LEGACY = """
SELECT a.gvkey, a.iid, a.shortint, a.shortintadj, a.datadate
FROM comp.sec_shortint_legacy as a
"""

# Add row limit for debugging if configured
if MAX_ROWS_DL > 0:
    QUERY_LEGACY += f" LIMIT {MAX_ROWS_DL}"
    print(f"DEBUG MODE: Limiting to {MAX_ROWS_DL} rows", flush=True)

si_legacy = pd.read_sql_query(QUERY_LEGACY, engine)
print(f"Downloaded {len(si_legacy)} legacy short interest records")

# Create monthly time variable
si_legacy['datadate'] = pd.to_datetime(si_legacy['datadate'])
# Convert to monthly periods and then to timestamps for DTA compatibility
si_legacy['time_avail_m'] = si_legacy['datadate'].dt.to_period('M').dt.to_timestamp()

# Collapse to monthly data using first non-missing values
# (equivalent to gcollapse (firstnm) shortint shortintadj, by(gvkey time_avail_m))
# Using mid-month observation for real-time availability
def first_non_missing(series):
    """Return first non-missing value"""
    non_missing = series.dropna()
    return non_missing.iloc[0] if len(non_missing) > 0 else None

monthly_si_legacy = si_legacy.groupby(['gvkey', 'time_avail_m']).agg({
    'shortint': first_non_missing,
    'shortintadj': first_non_missing
}).reset_index()

# Add legacy flag
monthly_si_legacy['legacyFile'] = 1
print(f"After monthly aggregation: {len(monthly_si_legacy)} legacy records")

# New file (2006-)
QUERY_NEW = """
SELECT a.gvkey, a.iid, a.shortint, a.shortintadj, a.datadate
FROM comp.sec_shortint as a
"""

# Add row limit for debugging if configured
if MAX_ROWS_DL > 0:
    QUERY_NEW += f" LIMIT {MAX_ROWS_DL}"

si_new = pd.read_sql_query(QUERY_NEW, engine)
engine.dispose()
print(f"Downloaded {len(si_new)} new short interest records")

# Create monthly time variable
si_new['datadate'] = pd.to_datetime(si_new['datadate'])
si_new['time_avail_m'] = si_new['datadate'].dt.to_period('M').dt.to_timestamp()

# Collapse to monthly data
monthly_si_new = si_new.groupby(['gvkey', 'time_avail_m']).agg({
    'shortint': first_non_missing,
    'shortintadj': first_non_missing
}).reset_index()

print(f"After monthly aggregation: {len(monthly_si_new)} new records")

# Combine
monthly_si = pd.concat([monthly_si_legacy, monthly_si_new], ignore_index=True)
print(f"After combining: {len(monthly_si)} total records")

# Keep legacy data if two observations for same firm in same month
# Count observations per gvkey-time_avail_m
monthly_si['nobs'] = monthly_si.groupby(['gvkey', 'time_avail_m'])['gvkey'].transform('count')

# Drop non-legacy observations when duplicates exist
monthly_si = monthly_si[~((monthly_si['nobs'] > 1) & (monthly_si['legacyFile'] != 1))]

# Drop temporary columns
monthly_si = monthly_si.drop(columns=['nobs', 'legacyFile'])

# Check whether no repeated observations
duplicates = monthly_si.duplicated(subset=['gvkey', 'time_avail_m'], keep=False)
assert not duplicates.any(), f"Found {duplicates.sum()} duplicate gvkey-time_avail_m combinations"

# Wrap up - scale values by 10^6 for consistency with shares outstanding
monthly_si['shortint'] = monthly_si['shortint'] / 1e6
monthly_si['shortintadj'] = monthly_si['shortintadj'] / 1e6

# Convert gvkey to numeric
monthly_si['gvkey'] = pd.to_numeric(monthly_si['gvkey'], errors='coerce')

# Apply column standardization with data type enforcement
monthly_si = standardize_columns(monthly_si, "monthlyShortInterest")

# Ensure directories exist
os.makedirs("../pyData/Intermediate", exist_ok=True)

# Save the data
monthly_si.to_parquet("../pyData/Intermediate/monthlyShortInterest.parquet")

print(f"Monthly Short Interest data saved with {len(monthly_si)} records")

# Show summary statistics
print(f"Date range: {monthly_si['time_avail_m'].min()} to {monthly_si['time_avail_m'].max()}")
print(f"Unique companies: {monthly_si['gvkey'].nunique()}")

print("\nSample data:")
print(monthly_si.head())

# Show missing data summary
print("\nMissing data:")
print(f"shortint: {monthly_si['shortint'].isna().sum()} missing")
print(f"shortintadj: {monthly_si['shortintadj'].isna().sum()} missing")