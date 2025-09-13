# ABOUTME: Downloads OptionMetrics-CRSP linking data and creates monthly permno-secid mapping
# ABOUTME: Processes link dates, joins with CRSP monthly data, and deduplicates by score
"""
Inputs:
- wrdsapps_link_crsp_optionm.opcrsphist (WRDS database)
- ../pyData/Intermediate/monthlyCRSP.parquet

Outputs:
- ../pyData/Intermediate/OPTIONMETRICSCRSPLinkingTable.parquet

How to run: python3 OptionMetricsCRSPLink.py
"""

import os
import pandas as pd
from pathlib import Path
from dotenv import load_dotenv
from sqlalchemy import create_engine
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from utils.column_standardizer_yaml import standardize_columns

load_dotenv()


# Load OptionMetrics linking data from WRDS database
print("Processing CRSP-OptionMetrics data...")

engine = create_engine(
    f"postgresql://{os.getenv('WRDS_USERNAME')}:{os.getenv('WRDS_PASSWORD')}@wrds-pgdata.wharton.upenn.edu:9737/wrds"
)

# Query WRDS database for OptionMetrics linking data
QUERY = """
SELECT secid, sdate, edate, permno, score
FROM wrdsapps_link_crsp_optionm.opcrsphist as a
WHERE permno is not null
"""

# Read linking data from WRDS
omlink0 = pd.read_sql_query(QUERY, engine)
print(f"Loaded {len(omlink0)} OptionMetrics linking records from WRDS")

engine.dispose()

# Load CRSP monthly data for time_avail_m dates
crspm = pd.read_parquet("../pyData/Intermediate/monthlyCRSP.parquet", columns=['permno', 'time_avail_m'])

# Convert daily link dates to monthly periods
omlink = omlink0.copy()

# Convert start date to first day of same month
omlink['sdate_m'] = pd.to_datetime(omlink['sdate']).dt.to_period('M').dt.to_timestamp()

# Convert end date to previous month (since monthly dates assume end of month)
omlink["edate_m"] = (
    pd.to_datetime(omlink["edate"]).dt.to_period("M") - 1
).dt.to_timestamp()

omlink.drop(columns=['sdate', 'edate'], inplace=True)

# Join OptionMetrics linking data with CRSP monthly data
# Full outer join on permno, filter for valid links and date ranges
df0 = omlink.merge(crspm, on=['permno'], how='outer').query(
    "secid.notna()"  # Keep only records with valid OptionMetrics secid
).query(
    "time_avail_m >= sdate_m & time_avail_m <= edate_m"  # Keep only valid date ranges
)

print(f'joined om-crsp link, crspm, and option volume data: {len(df0)} rows')

# Remove duplicates by keeping best score for each permno-month
# Lower score indicates better match quality
df = df0.sort_values(['permno','time_avail_m','score']).groupby(['permno','time_avail_m']).first().reset_index()

print(f'removed duplicates by score: {len(df)} rows')

# Standardize column names and types

df = standardize_columns(df, "OPTIONMETRICSCRSPLinkingTable")

# Save final linking table
df.to_parquet("../pyData/Intermediate/OPTIONMETRICSCRSPLinkingTable.parquet", index=False)

print(f"OptionMetrics linking data saved with {len(df)} records")
print(f"Head: {df.head()}")