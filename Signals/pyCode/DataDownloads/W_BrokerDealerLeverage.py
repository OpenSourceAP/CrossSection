# ABOUTME: Downloads broker-dealer financial data from FRED and computes seasonally adjusted leverage factor
# ABOUTME: Processes quarterly assets, liabilities, and equity data to calculate broker-dealer leverage ratios
"""
Inputs:
- FRED series BOGZ1FL664090005Q (assets)
- FRED series BOGZ1FL664190005Q (liabilities)
- FRED series BOGZ1FL665080003Q (equity)
- FRED_API_KEY environment variable

Outputs:
- ../pyData/Intermediate/brokerLev.parquet

How to run: python3 W_BrokerDealerLeverage.py
"""

import os
import pandas as pd
import numpy as np
import requests
from dotenv import load_dotenv
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from config import MAX_ROWS_DL

load_dotenv()


def download_fred_series(series_id, api_key, start_date='1900-01-01'):
    url = "https://api.stlouisfed.org/fred/series/observations"
    params = {
        'series_id': series_id,
        'api_key': api_key,
        'file_type': 'json',
        'observation_start': start_date,
        'sort_order': 'asc'
    }

    response = requests.get(url, params=params, timeout=30)
    response.raise_for_status()

    data = response.json()
    df = pd.DataFrame(data['observations'])
    df['date'] = pd.to_datetime(df['date'])
    df['value'] = pd.to_numeric(df['value'], errors='coerce')
    df = df.dropna(subset=['value'])

    print(f"Downloaded {len(df)} observations for {series_id}")
    return df[['date', 'value']]


print("Processing broker-dealer leverage data...")

# Get FRED API key from environment variable
api_key = os.getenv('FRED_API_KEY')

# Download three quarterly FRED series: assets, liabilities, equity
print("Downloading FRED series...")

# Download broker-dealer assets
assets_data = download_fred_series('BOGZ1FL664090005Q', api_key)
assets_data = assets_data.rename(columns={'value': 'assets'})

# Download broker-dealer liabilities
liab_data = download_fred_series('BOGZ1FL664190005Q', api_key)
liab_data = liab_data.rename(columns={'value': 'liab'})

# Download broker-dealer equity
equity_data = download_fred_series('BOGZ1FL665080003Q', api_key)
equity_data = equity_data.rename(columns={'value': 'equity'})

# Merge all three series on date
data = assets_data.merge(liab_data, on='date', how='outer')
data = data.merge(equity_data, on='date', how='outer')

# Extract quarter and year from date
data['qtr'] = data['date'].dt.quarter
data['year'] = data['date'].dt.year

# Calculate leverage ratio (assets/equity)
data['lev'] = data['assets'] / data['equity']

# Keep only data from 1968 onwards
data = data[data['year'] >= 1968].copy()

# Sort chronologically
data = data.sort_values('date').reset_index(drop=True)

# Calculate quarter-over-quarter log leverage change
data['levfacnsa'] = np.log(data['lev']) - np.log(data['lev'].shift(1))

# Calculate seasonal adjustment factors by quarter using cumulative means
data['tempMean'] = 0.0

for qtr in [1, 2, 3, 4]:
    qtr_mask = (data['qtr'] == qtr)
    qtr_data = data[qtr_mask].copy().sort_values('year').reset_index(drop=True)

    # Calculate cumulative sum and observation count within quarter
    qtr_data['cumsum'] = qtr_data['levfacnsa'].cumsum()
    qtr_data['count'] = range(1, len(qtr_data) + 1)

    # Calculate running mean of leverage changes within quarter
    qtr_data['tempMean'] = qtr_data['cumsum'] / qtr_data['count']

    # Special Q1 adjustment: use n-1 denominator for running mean
    if qtr == 1:
        mask_adj = qtr_data['count'] > 1
        qtr_data.loc[mask_adj, 'tempMean'] = qtr_data.loc[mask_adj, 'cumsum'] / (qtr_data.loc[mask_adj, 'count'] - 1)

    # No seasonal adjustment for base year 1968
    qtr_data.loc[qtr_data['year'] == 1968, 'tempMean'] = 0.0

    # Apply calculated seasonal factors to main dataset
    data.loc[qtr_mask, 'tempMean'] = qtr_data['tempMean'].values

# Apply seasonal adjustment by subtracting lagged seasonal factor
data['levfac'] = data['levfacnsa']  # Initialize with unadjusted values

for qtr in [1, 2, 3, 4]:
    qtr_mask = (data['qtr'] == qtr)
    qtr_indices = data[qtr_mask].sort_values('year').index

    # Lag seasonal factors by one period within each quarter
    tempMean_lagged = data.loc[qtr_indices, 'tempMean'].shift(1)

    # Subtract lagged seasonal factor from raw leverage change
    data.loc[qtr_indices, 'levfac'] = (
        data.loc[qtr_indices, 'levfacnsa'] - tempMean_lagged
    )

    # No adjustment for first observation in each quarter
    first_idx = qtr_indices[0]
    data.loc[first_idx, 'levfac'] = data.loc[first_idx, 'levfacnsa']

    # Q1 1969 special case: seasonal adjustment undefined, keep raw value
    if qtr == 1:
        q1_1969_mask = (data['year'] == 1969) & (data['qtr'] == 1)
        if q1_1969_mask.any():
            q1_1969_idx = data[q1_1969_mask].index[0]
            data.loc[q1_1969_idx, 'levfac'] = data.loc[q1_1969_idx, 'levfacnsa']

# Select output columns matching Stata script
output_data = data[['qtr', 'year', 'levfac']].copy()
output_data = output_data.sort_values(['year', 'qtr'])

# Retain all observations including those with missing leverage factors

print(f"Processed {len(output_data)} quarterly observations")

# Save processed data to parquet file
output_file = "../pyData/Intermediate/brokerLev.parquet"
output_data.to_parquet(output_file, index=False)

print(f"Saved {len(output_data)} records to {output_file}")
print("Broker-dealer leverage processing completed successfully.")