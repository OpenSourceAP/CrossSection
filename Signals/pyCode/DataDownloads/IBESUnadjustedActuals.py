# ABOUTME: Downloads IBES unadjusted actual earnings data and fills time series gaps
# ABOUTME: Creates monthly time series with forward-filled variables for each ticker
"""
Inputs:
- ibes.actpsumu_epsus (IBES unadjusted actuals database)

Outputs:
- ../pyData/Intermediate/IBES_UnadjustedActuals.parquet

How to run: from Signals/pyCode, run python3 DataDownloads/IBESUnadjustedActuals.py

Use the project Python environment at /opt/venv/projects/openap.
"""

import os
from sqlalchemy import create_engine
import pandas as pd
import numpy as np
from dotenv import load_dotenv
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from config import DEBUG_MODE
from utils.debug_mode import get_debug_row_limit

DEBUG_ROWS = get_debug_row_limit("IBESUnadjustedActuals")

load_dotenv()

engine = create_engine(
    f"postgresql://{os.getenv('WRDS_USERNAME')}:{os.getenv('WRDS_PASSWORD')}@wrds-pgdata.wharton.upenn.edu:9737/wrds"
)

# Obtain unadjusted actual EPS and shares for earnings-related signals.
QUERY = """
SELECT a.*
FROM ibes.actpsumu_epsus as a
WHERE a.measure = 'EPS'
"""

# Apply debug row limit if configured
if DEBUG_MODE:
    QUERY += f" LIMIT {DEBUG_ROWS}"
    print(f"DEBUG MODE: Limiting to {DEBUG_ROWS} rows", flush=True)

actuals_data = pd.read_sql_query(QUERY, engine)
engine.dispose()

print(f"Downloaded {len(actuals_data)} IBES actual earnings records")

# Distinguish unadjusted IBES shares from split-adjusted shares in other datasets.
actuals_data = actuals_data.rename(columns={'shout': 'shoutIBESUnadj'})

# Align actuals with their observation month for monthly analyst-data joins.
actuals_data['statpers'] = pd.to_datetime(actuals_data['statpers'])
actuals_data['time_avail_m'] = actuals_data['statpers'].dt.to_period('M').dt.to_timestamp()
actuals_data['time_avail_m'] = pd.to_datetime(actuals_data['time_avail_m'])

# Retain the first source observation when a ticker has multiple records in a month.
initial_count = len(actuals_data)
actuals_data = actuals_data.drop_duplicates(['ticker', 'time_avail_m'], keep='first')
print(f"After removing within-month duplicates: {len(actuals_data)} records")

# Carry available actuals into gaps within each ticker's observed monthly history.
print("Filling time series gaps...")


def fill_ticker_gaps(group):
    """Carry reported earnings and shares into gaps within a ticker's observed history."""
    group = group.sort_values('time_avail_m')

    if len(group) <= 1:
        return group

    # Include months between the first and last observations, without extending coverage beyond them.
    min_time = group['time_avail_m'].min()
    max_time = group['time_avail_m'].max()
    full_time_range = pd.date_range(start=min_time, end=max_time, freq='MS')

    group = group.set_index('time_avail_m').reindex(full_time_range)
    group.index.name = 'time_avail_m'
    group = group.reset_index()

    # Carry forward the reported interim/annual earnings and shares until the next observation.
    fill_vars = ['int0a', 'fy0a', 'shoutIBESUnadj', 'ticker']
    for var in fill_vars:
        group[var] = group[var].ffill()

    return group


ticker_groups = actuals_data.groupby('ticker')
actuals_data = ticker_groups.apply(fill_ticker_gaps)
del ticker_groups
actuals_data = actuals_data.reset_index(drop=True)
print(f"After filling time series gaps: {len(actuals_data)} records")

actuals_data = actuals_data.drop('statpers', axis=1)

# Keep the monthly linking fields compatible with other IBES datasets.
actuals_data = actuals_data.rename(columns={'ticker': 'tickerIBES'})

actuals_data['tickerIBES'] = actuals_data['tickerIBES'].astype(str)

actuals_data['time_avail_m'] = pd.to_datetime(actuals_data['time_avail_m'])

# Represent absent text descriptors consistently as empty text, including in added months.
string_columns = ['curr_price', 'measure', 'cusip', 'cname', 'curcode', 'oftic']
for col in string_columns:
    actuals_data[col] = actuals_data[col].fillna('')

# Preserve missing price and period-end dates in months added by gap filling.
date_columns = ['prdays', 'fy0edats', 'int0dats']
for col in date_columns:
    actuals_data[col] = pd.to_datetime(actuals_data[col])

# Save the monthly unadjusted-actuals history for downstream signals.
actuals_data.to_parquet("../pyData/Intermediate/IBES_UnadjustedActuals.parquet")

print(f"IBES Unadjusted Actuals data saved with {len(actuals_data)} records")

print(f"Date range: {actuals_data['time_avail_m'].min()} to {actuals_data['time_avail_m'].max()}")
print(f"Unique tickers: {actuals_data['tickerIBES'].nunique()}")

print("\nSample data:")
print(actuals_data[['tickerIBES', 'time_avail_m', 'int0a', 'fy0a']].head())
