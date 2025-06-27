#!/usr/bin/env python3
"""
IBES EPS Adjusted data download script - Python equivalent of L2_IBES_EPS_Adj.do

Downloads IBES EPS estimates (adjusted for splits) with actuals joined.
"""

import os
import psycopg2
import pandas as pd
from dotenv import load_dotenv
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from config import MAX_ROWS_DL

load_dotenv()

conn = psycopg2.connect(
    host="wrds-pgdata.wharton.upenn.edu",
    port=9737,
    database="wrds",
    user=os.getenv("WRDS_USERNAME"),
    password=os.getenv("WRDS_PASSWORD")
)

QUERY = """
SELECT a.fpi, a.ticker, a.statpers, a.fpedats, a.anndats_act
    , a.meanest, a.actual, a.medest, a.stdev, a.numest
    , b.prdays, b.price, b.shout
FROM ibes.statsum_epsus as a left join ibes.actpsum_epsus as b
on a.ticker = b.ticker and a.statpers = b.statpers
"""

# Add row limit for debugging if configured
if MAX_ROWS_DL > 0:
    QUERY += f" LIMIT {MAX_ROWS_DL}"
    print(f"DEBUG MODE: Limiting to {MAX_ROWS_DL} rows", flush=True)

ibes_adj = pd.read_sql_query(QUERY, conn)
conn.close()

print(f"Downloaded {len(ibes_adj)} IBES EPS adjusted records")

# Ensure directories exist
os.makedirs("../pyData/Intermediate", exist_ok=True)

# Set up linking variables
ibes_adj['statpers'] = pd.to_datetime(ibes_adj['statpers'])
# Keep as datetime64[ns] instead of Period to maintain type compatibility with DTA format
ibes_adj['time_avail_m'] = ibes_adj['statpers'].dt.to_period('M').dt.to_timestamp()
# Ensure it's properly datetime64[ns] format to match Stata expectations
ibes_adj['time_avail_m'] = pd.to_datetime(ibes_adj['time_avail_m'])

# Convert date columns to datetime to match Stata format (NaT for missing values)
ibes_adj['fpedats'] = pd.to_datetime(ibes_adj['fpedats'])
ibes_adj['anndats_act'] = pd.to_datetime(ibes_adj['anndats_act'])
ibes_adj['prdays'] = pd.to_datetime(ibes_adj['prdays'])

# Rename ticker to tickerIBES
ibes_adj = ibes_adj.rename(columns={'ticker': 'tickerIBES'})

# Keep last obs each month - first remove rows with missing meanest
initial_count = len(ibes_adj)
ibes_adj = ibes_adj.dropna(subset=['meanest'])
print(f"Removed {initial_count - len(ibes_adj)} records with missing meanest")

# Sort and keep last observation for each tickerIBES/fpi/time_avail_m combination
ibes_adj = ibes_adj.sort_values(['tickerIBES', 'fpi', 'time_avail_m', 'statpers'])
ibes_adj = ibes_adj.drop_duplicates(['tickerIBES', 'fpi', 'time_avail_m'], keep='last')

print(f"After keeping last obs per month: {len(ibes_adj)} records")

# Save the data
ibes_adj.to_parquet("../pyData/Intermediate/IBES_EPS_Adj.parquet", index=False)

print(f"IBES EPS Adjusted data saved with {len(ibes_adj)} records")
print(f"Date range: {ibes_adj['time_avail_m'].min()} to {ibes_adj['time_avail_m'].max()}")

print("\nSample data:")
print(ibes_adj.head())
