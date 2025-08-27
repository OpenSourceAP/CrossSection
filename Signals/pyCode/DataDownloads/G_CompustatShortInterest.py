#%%

# debug
import os
os.chdir(os.path.join(os.path.dirname(__file__), '..'))
print(os.getcwd())

"""
Compustat Short Interest data download script - Python equivalent of G_CompustatShortInterest.do
(https://github.com/OpenSourceAP/CrossSection/blob/master/Signals/Code/DataDownloads/G_CompustatShortInterest.do)

Downloads short interest data with monthly aggregation.
Data reported bi-weekly with 4-day lag; using mid-month observation for real-time availability.

from Stata:
* In 2025, S&P replaced the short interest data (starting in 1973) with a different
* data source that only starts in 2006. We combine both files and keep the legacy
* data when both are available for consistency with previous publications

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

#%%

# Create SQLAlchemy engine for database connection
engine = create_engine(
    f"postgresql://{os.getenv('WRDS_USERNAME')}:{os.getenv('WRDS_PASSWORD')}@wrds-pgdata.wharton.upenn.edu:9737/wrds"
)

# download legacy short interest file (ends in 2024)
QUERY = """
SELECT a.gvkey, a.iid, a.shortint, a.shortintadj, a.datadate
FROM comp.sec_shortint as a
"""

si_legacy = pd.read_sql_query(QUERY, engine)

# download standard short interest file (standard as of 2025)
QUERY = """
SELECT a.gvkey, a.iid, a.shortint, a.shortintadj, a.datadate
FROM comp.sec_shortint as a
"""

si_standard = pd.read_sql_query(QUERY, engine)

engine.dispose()

#%%

# == Combine and clean ==

si_legacy['legacy'] = 1
si_standard['legacy'] = 0

# Combine both datasets, keeping legacy data when both are available for a (gvkey, iid, datadate)
# 1. Concatenate, then sort so legacy comes first, then drop duplicates keeping the first (legacy preferred)
si = pd.concat([si_legacy, si_standard], ignore_index=True)
si = si.sort_values(['gvkey', 'iid', 'datadate', 'legacy'], ascending=[True, True, True, False])

#%%

temp = si.copy()
temp['n'] = temp.groupby(['gvkey', 'datadate','legacy'])['shortint'].transform('count')

temp.query('n > 1').sort_values(['gvkey', 'datadate', 'legacy']).head(10)






#%%
print(f"Downloaded {len(si_data)} short interest records")

# Ensure directories exist
os.makedirs("../pyData/Intermediate", exist_ok=True)

# Create monthly time variable
si_data['datadate'] = pd.to_datetime(si_data['datadate'])
# Convert to monthly periods and then to timestamps for DTA compatibility
si_data['time_avail_m'] = si_data['datadate'].dt.to_period('M').dt.to_timestamp()

# Collapse to monthly data using first non-missing values
# (equivalent to gcollapse (firstnm) shortint shortintadj, by(gvkey time_avail_m))
# Using mid-month observation for real-time availability
def first_non_missing(series):
    """Return first non-missing value"""
    non_missing = series.dropna()
    return non_missing.iloc[0] if len(non_missing) > 0 else None

monthly_si = si_data.groupby(['gvkey', 'time_avail_m']).agg({
    'shortint': first_non_missing,
    'shortintadj': first_non_missing
}).reset_index()

print(f"After monthly aggregation: {len(monthly_si)} records")

# Convert gvkey to numeric
monthly_si['gvkey'] = pd.to_numeric(monthly_si['gvkey'], errors='coerce')

# Apply column standardization with data type enforcement
monthly_si = standardize_columns(monthly_si, "monthlyShortInterest")

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
