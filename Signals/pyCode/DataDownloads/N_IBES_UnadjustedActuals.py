# ABOUTME: Downloads IBES unadjusted actual earnings data and fills time series gaps
# ABOUTME: Creates monthly time series with forward-filled variables for each ticker
"""
Inputs:
- ibes.actpsumu_epsus (IBES unadjusted actuals database)

Outputs:
- ../pyData/Intermediate/IBES_UnadjustedActuals.parquet

How to run: python3 N_IBES_UnadjustedActuals.py
"""

import os
from sqlalchemy import create_engine
import pandas as pd
import numpy as np
from dotenv import load_dotenv
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from config import MAX_ROWS_DL
from utils.column_standardizer_yaml import standardize_columns

load_dotenv()

# Create database connection
engine = create_engine(
    f"postgresql://{os.getenv('WRDS_USERNAME')}:{os.getenv('WRDS_PASSWORD')}@wrds-pgdata.wharton.upenn.edu:9737/wrds"
)

# Download IBES actual earnings data (EPS measure only)
QUERY = """
SELECT a.*
FROM ibes.actpsumu_epsus as a
WHERE a.measure = 'EPS'
"""

# Apply debug row limit if configured
if MAX_ROWS_DL > 0:
    QUERY += f" LIMIT {MAX_ROWS_DL}"
    print(f"DEBUG MODE: Limiting to {MAX_ROWS_DL} rows", flush=True)

actuals_data = pd.read_sql_query(QUERY, engine)
engine.dispose()

print(f"Downloaded {len(actuals_data)} IBES actual earnings records")

# Create output directory
os.makedirs("../pyData/Intermediate", exist_ok=True)

# Rename shout column to distinguish from adjusted version
if 'shout' in actuals_data.columns:
    actuals_data = actuals_data.rename(columns={'shout': 'shoutIBESUnadj'})

# Convert statement period to monthly time variable
actuals_data['statpers'] = pd.to_datetime(actuals_data['statpers'])
actuals_data['time_avail_m'] = actuals_data['statpers'].dt.to_period('M').dt.to_timestamp()
actuals_data['time_avail_m'] = pd.to_datetime(actuals_data['time_avail_m'])

# Remove duplicate ticker-month observations
initial_count = len(actuals_data)
actuals_data = actuals_data.drop_duplicates(['ticker', 'time_avail_m'], keep='first')
print(f"After removing within-month duplicates: {len(actuals_data)} records")

# Fill monthly time series gaps for each ticker
print("Filling time series gaps...")

def fill_ticker_gaps(group):
    group = group.sort_values('time_avail_m')
    
    if len(group) <= 1:
        return group
    
    # Create full monthly time range for this ticker
    min_time = group['time_avail_m'].min()
    max_time = group['time_avail_m'].max()
    full_time_range = pd.date_range(start=min_time, end=max_time, freq='MS')
    
    # Reindex to create missing months
    group = group.set_index('time_avail_m').reindex(full_time_range)
    group.index.name = 'time_avail_m'
    group = group.reset_index()
    
    # Forward fill key variables into missing months
    fill_vars = ['int0a', 'fy0a', 'shoutIBESUnadj', 'ticker']
    for var in fill_vars:
        if var in group.columns:
            group[var] = group[var].ffill()
    
    return group

# Apply gap filling to each ticker
actuals_data = actuals_data.groupby('ticker').apply(fill_ticker_gaps).reset_index(drop=True)
print(f"After filling time series gaps: {len(actuals_data)} records")

# Remove original statement period column
if 'statpers' in actuals_data.columns:
    actuals_data = actuals_data.drop('statpers', axis=1)

# Standardize ticker column name
actuals_data = actuals_data.rename(columns={'ticker': 'tickerIBES'})

# Ensure ticker column is string type
actuals_data['tickerIBES'] = actuals_data['tickerIBES'].astype(str)

# Ensure time column remains datetime format
actuals_data['time_avail_m'] = pd.to_datetime(actuals_data['time_avail_m'])

# Handle missing values in string columns
string_columns = ['curr_price', 'measure', 'cusip', 'cname', 'curcode', 'oftic']
for col in string_columns:
    if col in actuals_data.columns:
        actuals_data[col] = actuals_data[col].fillna('')

# Handle missing values in date columns
date_columns = ['prdays', 'fy0edats', 'int0dats']
for col in date_columns:
    if col in actuals_data.columns:
        actuals_data[col] = pd.to_datetime(actuals_data[col])

# Apply column standardization and save data
actuals_data = standardize_columns(actuals_data, 'IBES_UnadjustedActuals')
actuals_data.to_parquet("../pyData/Intermediate/IBES_UnadjustedActuals.parquet")

print(f"IBES Unadjusted Actuals data saved with {len(actuals_data)} records")

# Display summary statistics
print(f"Date range: {actuals_data['time_avail_m'].min()} to {actuals_data['time_avail_m'].max()}")
print(f"Unique tickers: {actuals_data['tickerIBES'].nunique()}")

print("\nSample data:")
print(actuals_data[['tickerIBES', 'time_avail_m', 'int0a', 'fy0a']].head())
