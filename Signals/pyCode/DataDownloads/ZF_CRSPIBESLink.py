#!/usr/bin/env python3
"""
CRSP-IBES Linking data script - Python equivalent of ZF_CRSPIBESLink.do

Queries IBES-CRSP linking table directly from WRDS database.
"""

import os
import pandas as pd
from dotenv import load_dotenv
from sqlalchemy import create_engine
import sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from config import MAX_ROWS_DL
from utils.column_standardizer_yaml import standardize_columns

load_dotenv()

print("Processing CRSP-IBES linking data...")

# Ensure directories exist
os.makedirs("../pyData/Intermediate", exist_ok=True)

# Query WRDS database
print("Querying IBES-CRSP link from WRDS database...")

engine = create_engine(
    f"postgresql://{os.getenv('WRDS_USERNAME')}:{os.getenv('WRDS_PASSWORD')}@wrds-pgdata.wharton.upenn.edu:9737/wrds"
)

QUERY = """
SELECT ticker, permno, ncusip, sdate, edate, score
FROM wrdsapps.ibcrsphist as a
WHERE permno is not null
"""

iblink_raw = pd.read_sql_query(QUERY, engine)
print(f"Loaded {len(iblink_raw)} IBES-CRSP linking records from WRDS")

engine.dispose()

# Convert dates to monthly format
iclink = iblink_raw.copy()
iclink['sdate_m'] = pd.to_datetime(iclink['sdate']).dt.to_period('M').dt.to_timestamp()
iclink['edate_m'] = (
    pd.to_datetime(iclink['edate']).dt.to_period('M') - 1
).dt.to_timestamp()
iclink.drop(columns=['sdate', 'edate'], inplace=True)

# Load CRSP monthly data for date filtering
crspm = pd.read_parquet("../pyData/Intermediate/monthlyCRSP.parquet", columns=['permno', 'time_avail_m'])

# Join with CRSP data and filter by valid date ranges
df0 = iclink.merge(crspm, on=['permno'], how='outer').query(
    "ticker.notna()"
).query(
    "time_avail_m >= sdate_m & time_avail_m <= edate_m"
)

print(f'Joined IBES-CRSP link with CRSP monthly data: {len(df0)} rows')

# Remove duplicates - keep the lowest score
df = df0.sort_values(['permno', 'time_avail_m', 'score']).groupby(['permno', 'time_avail_m']).first().reset_index()
print(f'Removed duplicates by score: {len(df)} rows')

# Rename columns to match expected output
df = df.rename(columns={'ticker': 'tickerIBES'})

# Save the data
final_data = standardize_columns(df, 'IBESCRSPLinkingTable')
final_data.to_parquet("../pyData/Intermediate/IBESCRSPLinkingTable.parquet", index=False)

print(f"IBES-CRSP Linking Table saved with {len(final_data)} records")

# Show summary statistics
if 'permno' in final_data.columns:
    print(f"Unique permnos: {final_data['permno'].nunique()}")

if 'tickerIBES' in final_data.columns:
    print(f"Unique IBES tickers: {final_data['tickerIBES'].nunique()}")

print("\nSample data:")
print(final_data.head())