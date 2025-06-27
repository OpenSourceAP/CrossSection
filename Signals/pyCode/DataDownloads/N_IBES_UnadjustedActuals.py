#!/usr/bin/env python3
"""
IBES Unadjusted Actuals data download script - Python equivalent of N_IBES_UnadjustedActuals.do

Downloads IBES actual earnings data (unadjusted) and fills time series gaps.
"""

import os
import psycopg2
import pandas as pd
import numpy as np
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

# Download everything (newer approach as noted in comments)
QUERY = """
SELECT a.*
FROM ibes.actpsumu_epsus as a
WHERE a.measure = 'EPS'
"""

# Add row limit for debugging if configured
if MAX_ROWS_DL > 0:
    QUERY += f" LIMIT {MAX_ROWS_DL}"
    print(f"DEBUG MODE: Limiting to {MAX_ROWS_DL} rows", flush=True)

actuals_data = pd.read_sql_query(QUERY, conn)
conn.close()

print(f"Downloaded {len(actuals_data)} IBES actual earnings records")

# Ensure directories exist
os.makedirs("../pyData/Intermediate", exist_ok=True)

# Rename shout to shoutIBESUnadj
if 'shout' in actuals_data.columns:
    actuals_data = actuals_data.rename(columns={'shout': 'shoutIBESUnadj'})

# Set up monthly time (equivalent to gen time_avail_m = mofd(statpers))
actuals_data['statpers'] = pd.to_datetime(actuals_data['statpers'])
# Keep as datetime64[ns] instead of Period to maintain type compatibility with DTA format
actuals_data['time_avail_m'] = actuals_data['statpers'].dt.to_period('M').dt.to_timestamp()
# Ensure it's properly datetime64[ns] format to match Stata expectations
actuals_data['time_avail_m'] = pd.to_datetime(actuals_data['time_avail_m'])

# Keep only one observation per ticker/time_avail_m
# (equivalent to egen id = group(ticker); bys id time_av: keep if _n == 1)
initial_count = len(actuals_data)
actuals_data = actuals_data.drop_duplicates(['ticker', 'time_avail_m'], keep='first')
print(f"After removing within-month duplicates: {len(actuals_data)} records")

# Fill time series gaps (equivalent to xtset id time_av; tsfill)
print("Filling time series gaps...")

# Get unique tickers
tickers = actuals_data['ticker'].unique()
filled_data = []

for ticker in tickers:
    ticker_data = actuals_data[actuals_data['ticker'] == ticker].copy()
    ticker_data = ticker_data.sort_values('time_avail_m')

    if len(ticker_data) > 1:
        # Create full time range for this ticker using datetime to avoid period conversion
        min_time = ticker_data['time_avail_m'].min()
        max_time = ticker_data['time_avail_m'].max()
        full_time_range = pd.date_range(start=min_time, end=max_time, freq='MS')

        # Reindex to fill gaps
        ticker_data = ticker_data.set_index('time_avail_m').reindex(full_time_range)
        ticker_data.index.name = 'time_avail_m'
        ticker_data = ticker_data.reset_index()

        # Forward fill specified variables (equivalent to Stata's replace logic)
        fill_vars = ['int0a', 'fy0a', 'shoutIBESUnadj', 'ticker']
        for var in fill_vars:
            if var in ticker_data.columns:
                ticker_data[var] = ticker_data[var].ffill()

    filled_data.append(ticker_data)

# Combine all tickers
if filled_data:
    actuals_data = pd.concat(filled_data, ignore_index=True)
    print(f"After filling time series gaps: {len(actuals_data)} records")

# Drop statpers (we have time_avail_m now)
if 'statpers' in actuals_data.columns:
    actuals_data = actuals_data.drop('statpers', axis=1)

# Rename ticker to tickerIBES for consistency
actuals_data = actuals_data.rename(columns={'ticker': 'tickerIBES'})

# Ensure tickerIBES is object type to match Stata expectations
actuals_data['tickerIBES'] = actuals_data['tickerIBES'].astype(str)

# Ensure time_avail_m is properly datetime64[ns] format after time series operations
actuals_data['time_avail_m'] = pd.to_datetime(actuals_data['time_avail_m'])

# Convert missing values to match Stata format
# String columns: None → empty string
string_columns = ['curr_price', 'measure', 'cusip', 'cname', 'curcode', 'oftic']
for col in string_columns:
    if col in actuals_data.columns:
        actuals_data[col] = actuals_data[col].fillna('')

# Date columns: None → pd.NaT (ensure proper datetime type)
date_columns = ['prdays', 'fy0edats', 'int0dats']
for col in date_columns:
    if col in actuals_data.columns:
        actuals_data[col] = pd.to_datetime(actuals_data[col])

# Save the data
actuals_data.to_parquet("../pyData/Intermediate/IBES_UnadjustedActuals.parquet")

print(f"IBES Unadjusted Actuals data saved with {len(actuals_data)} records")

# Show date range and sample data
print(f"Date range: {actuals_data['time_avail_m'].min()} to {actuals_data['time_avail_m'].max()}")
print(f"Unique tickers: {actuals_data['tickerIBES'].nunique()}")

print("\nSample data:")
print(actuals_data[['tickerIBES', 'time_avail_m', 'int0a', 'fy0a']].head())
