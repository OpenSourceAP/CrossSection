"""
ABOUTME: Downloads and processes Compustat short interest data, combining legacy and new sources
ABOUTME: Joins with CCMLinkingTable to add permno and aggregates to monthly permno-level data

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
si_legacy['time_avail_m'] = si_legacy['datadate'].dt.to_period('M').dt.to_timestamp()

# Sort and collapse to monthly data keeping datadate
# (equivalent to gcollapse (firstnm) shortint shortintadj datadate, by(gvkey iid time_avail_m))
si_legacy = si_legacy.sort_values(['gvkey', 'iid', 'time_avail_m', 'datadate'])

def first_non_missing(series):
    """Return first non-missing value"""
    non_missing = series.dropna()
    return non_missing.iloc[0] if len(non_missing) > 0 else None

monthly_si_legacy = si_legacy.groupby(['gvkey', 'iid', 'time_avail_m']).agg({
    'shortint': first_non_missing,
    'shortintadj': first_non_missing,
    'datadate': 'first'  # Keep first datadate for link validity check
}).reset_index()

print(f"After monthly aggregation: {len(monthly_si_legacy)} legacy records")

# Add permno - rename iid to liid for join
monthly_si_legacy['liid'] = monthly_si_legacy['iid']
linking_table = pd.read_parquet("../pyData/Intermediate/CCMLinkingTable.parquet")

# Join with linking table
monthly_si_legacy = monthly_si_legacy.merge(
    linking_table[['gvkey', 'liid', 'permno', 'timeLinkStart_d', 'timeLinkEnd_d']],
    on=['gvkey', 'liid'],
    how='inner'
)

# Use only if data date is within the validity period of the link
# Handle NaT (missing) end dates as "valid forever"
monthly_si_legacy['temp'] = (
    (monthly_si_legacy['timeLinkStart_d'] <= monthly_si_legacy['datadate']) & 
    ((monthly_si_legacy['datadate'] <= monthly_si_legacy['timeLinkEnd_d']) | 
     monthly_si_legacy['timeLinkEnd_d'].isna())
)
print(f"Legacy link validity check: {monthly_si_legacy['temp'].value_counts().to_dict()}")
monthly_si_legacy = monthly_si_legacy[monthly_si_legacy['temp'] == True]
monthly_si_legacy = monthly_si_legacy.drop(columns=['temp', 'timeLinkStart_d', 'timeLinkEnd_d', 'liid'])

# Handle edge cases where permno-(gvkey-iid) link shifts within months
monthly_si_legacy['tmp'] = monthly_si_legacy.groupby(['permno', 'time_avail_m'])['permno'].transform('count')
print(f"Legacy edge cases (permno shifts within month): {(monthly_si_legacy['tmp'] == 2).sum()}")

# Sort and keep mid-month observation when duplicates exist
monthly_si_legacy = monthly_si_legacy.sort_values(['permno', 'time_avail_m', 'datadate'])
monthly_si_legacy['row_num'] = monthly_si_legacy.groupby(['permno', 'time_avail_m']).cumcount() + 1
monthly_si_legacy = monthly_si_legacy[~((monthly_si_legacy['tmp'] == 2) & (monthly_si_legacy['row_num'] == 2))]
monthly_si_legacy = monthly_si_legacy.drop(columns=['tmp', 'datadate', 'row_num', 'iid'])

# Add legacy flag
monthly_si_legacy['legacyFile'] = 1

# Save temporary legacy file for later combination
temp_legacy = monthly_si_legacy.copy()

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

# Sort and collapse to monthly data keeping datadate
si_new = si_new.sort_values(['gvkey', 'iid', 'time_avail_m', 'datadate'])

monthly_si_new = si_new.groupby(['gvkey', 'iid', 'time_avail_m']).agg({
    'shortint': first_non_missing,
    'shortintadj': first_non_missing,
    'datadate': 'first'
}).reset_index()

print(f"After monthly aggregation: {len(monthly_si_new)} new records")

# Add permno
monthly_si_new['liid'] = monthly_si_new['iid']
monthly_si_new = monthly_si_new.merge(
    linking_table[['gvkey', 'liid', 'permno', 'timeLinkStart_d', 'timeLinkEnd_d']],
    on=['gvkey', 'liid'],
    how='inner'
)

# Use only if data date is within the validity period of the link
# Handle NaT (missing) end dates as "valid forever"
monthly_si_new['temp'] = (
    (monthly_si_new['timeLinkStart_d'] <= monthly_si_new['datadate']) & 
    ((monthly_si_new['datadate'] <= monthly_si_new['timeLinkEnd_d']) | 
     monthly_si_new['timeLinkEnd_d'].isna())
)
print(f"New link validity check: {monthly_si_new['temp'].value_counts().to_dict()}")
monthly_si_new = monthly_si_new[monthly_si_new['temp'] == True]
monthly_si_new = monthly_si_new.drop(columns=['temp', 'timeLinkStart_d', 'timeLinkEnd_d', 'liid'])

# Handle edge cases where permno-(gvkey-iid) link shifts within months
monthly_si_new['tmp'] = monthly_si_new.groupby(['permno', 'time_avail_m'])['permno'].transform('count')
print(f"New edge cases (permno shifts within month): {(monthly_si_new['tmp'] == 2).sum()}")

# Sort and keep mid-month observation when duplicates exist
monthly_si_new = monthly_si_new.sort_values(['permno', 'time_avail_m', 'datadate'])
monthly_si_new['row_num'] = monthly_si_new.groupby(['permno', 'time_avail_m']).cumcount() + 1
monthly_si_new = monthly_si_new[~((monthly_si_new['tmp'] == 2) & (monthly_si_new['row_num'] == 2))]
monthly_si_new = monthly_si_new.drop(columns=['tmp', 'datadate', 'row_num', 'iid'])

# Combine
monthly_si = pd.concat([temp_legacy, monthly_si_new], ignore_index=True)
print(f"After combining: {len(monthly_si)} total records")

# Keep legacy data if two observations for same firm in same month
# Count observations per gvkey-permno-iid-time_avail_m (note: iid already dropped)
monthly_si['nobs'] = monthly_si.groupby(['gvkey', 'permno', 'time_avail_m'])['gvkey'].transform('count')

# Drop non-legacy observations when duplicates exist
monthly_si = monthly_si[~((monthly_si['nobs'] > 1) & (monthly_si['legacyFile'] != 1))]
monthly_si = monthly_si.drop(columns=['nobs', 'legacyFile'])

# There are 16 observations where the same permno shows up with different short interest in the same month
# I drop those observations
monthly_si['tmp'] = monthly_si.groupby(['permno', 'time_avail_m'])['permno'].transform('count')
print(f"Duplicate permno-time_avail_m observations: {(monthly_si['tmp'] == 2).sum()}")
monthly_si = monthly_si[monthly_si['tmp'] != 2]
monthly_si = monthly_si.drop(columns=['tmp'])

# Check whether no repeated observations
duplicates_gvkey = monthly_si.duplicated(subset=['gvkey', 'permno', 'time_avail_m'], keep=False)
assert not duplicates_gvkey.any(), f"Found {duplicates_gvkey.sum()} duplicate gvkey-permno-time_avail_m combinations"

duplicates_permno = monthly_si.duplicated(subset=['permno', 'time_avail_m'], keep=False)
assert not duplicates_permno.any(), f"Found {duplicates_permno.sum()} duplicate permno-time_avail_m combinations"

# Wrap up - scale values by 10^6 for consistency with shares outstanding
monthly_si['shortint'] = monthly_si['shortint'] / 1e6
monthly_si['shortintadj'] = monthly_si['shortintadj'] / 1e6

# Apply column standardization with data type enforcement
# Note: The YAML expects gvkey and time_avail_m, shortint, shortintadj only
# So we need to drop permno before standardization or update the YAML
monthly_si_for_save = standardize_columns(monthly_si, "monthlyShortInterest")

# Ensure directories exist
os.makedirs("../pyData/Intermediate", exist_ok=True)

# Save the data
monthly_si_for_save.to_parquet("../pyData/Intermediate/monthlyShortInterest.parquet")

print(f"Monthly Short Interest data saved with {len(monthly_si_for_save)} records")

# Show summary statistics
print(f"Date range: {monthly_si_for_save['time_avail_m'].min()} to {monthly_si_for_save['time_avail_m'].max()}")
print(f"Unique companies: {monthly_si_for_save['gvkey'].nunique()}")

print("\nSample data:")
print(monthly_si_for_save.head())

# Show missing data summary
print("\nMissing data:")
print(f"shortint: {monthly_si_for_save['shortint'].isna().sum()} missing")
print(f"shortintadj: {monthly_si_for_save['shortintadj'].isna().sum()} missing")