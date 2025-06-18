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

actuals_data = pd.read_sql_query(QUERY, conn)
conn.close()

print("Downloaded {len(actuals_data)} IBES actual earnings records")

# Ensure directories exist
os.makedirs("../pyData/Intermediate", exist_ok=True)

# Rename shout to shoutIBESUnadj
if 'shout' in actuals_data.columns:
    actuals_data = actuals_data.rename(columns={'shout': 'shoutIBESUnadj'})

# Set up monthly time (equivalent to gen time_avail_m = mofd(statpers))
actuals_data['statpers'] = pd.to_datetime(actuals_data['statpers'])
actuals_data['time_avail_m'] = actuals_data['statpers'].dt.to_period('M')

# Keep only one observation per ticker/time_avail_m
# (equivalent to egen id = group(ticker); bys id time_av: keep if _n == 1)
initial_count = len(actuals_data)
actuals_data = actuals_data.drop_duplicates(['ticker', 'time_avail_m'], keep='first')
print("After removing within-month duplicates: {len(actuals_data)} records")

# Fill time series gaps (equivalent to xtset id time_av; tsfill)
print("Filling time series gaps...")

# Get unique tickers
tickers = actuals_data['ticker'].unique()
filled_data = []

for ticker in tickers:
    ticker_data = actuals_data[actuals_data['ticker'] == ticker].copy()
    ticker_data = ticker_data.sort_values('time_avail_m')

    if len(ticker_data) > 1:
        # Create full time range for this ticker
        min_time = ticker_data['time_avail_m'].min()
        max_time = ticker_data['time_avail_m'].max()
        full_time_range = pd.period_range(start=min_time, end=max_time, freq='M')

        # Reindex to fill gaps
        ticker_data = ticker_data.set_index('time_avail_m').reindex(full_time_range)
        ticker_data.index.name = 'time_avail_m'
        ticker_data = ticker_data.reset_index()

        # Forward fill specified variables (equivalent to Stata's replace logic)
        fill_vars = ['int0a', 'fy0a', 'shoutIBESUnadj', 'ticker']
        for var in fill_vars:
            if var in ticker_data.columns:
                ticker_data[var] = ticker_data[var].fillna(method='ffill')

    filled_data.append(ticker_data)

# Combine all tickers
if filled_data:
    actuals_data = pd.concat(filled_data, ignore_index=True)
    print("After filling time series gaps: {len(actuals_data)} records")

# Drop statpers (we have time_avail_m now)
if 'statpers' in actuals_data.columns:
    actuals_data = actuals_data.drop('statpers', axis=1)

# Rename ticker to tickerIBES for consistency
actuals_data = actuals_data.rename(columns={'ticker': 'tickerIBES'})

# Save the data
actuals_data.to_pickle("../pyData/Intermediate/IBES_UnadjustedActuals.pkl")

print("IBES Unadjusted Actuals data saved with {len(actuals_data)} records")

# Show date range and sample data
print("Date range: {actuals_data['time_avail_m'].min()} to {actuals_data['time_avail_m'].max()}")
print("Unique tickers: {actuals_data['tickerIBES'].nunique()}")

print("\nSample data:")
print(actuals_data[['tickerIBES', 'time_avail_m', 'int0a', 'fy0a']].head())
