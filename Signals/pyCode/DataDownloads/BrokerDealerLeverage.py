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

How to run: from Signals/pyCode, run python3 DataDownloads/BrokerDealerLeverage.py

Use the project Python environment at /opt/venv/projects/openap.
"""

import os
import pandas as pd
import numpy as np
import requests
from dotenv import load_dotenv
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from utils.debug_mode import log_selection

log_selection("BrokerDealerLeverage")
load_dotenv()


def download_fred_series(series_id, api_key, start_date='1900-01-01'):
    """Provide dated numeric balance-sheet observations, excluding missing source values."""
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

api_key = os.getenv('FRED_API_KEY')

# Obtain broker-dealer balance sheets for the quarterly leverage measure.
print("Downloading FRED series...")

assets_data = download_fred_series('BOGZ1FL664090005Q', api_key)
assets_data = assets_data.rename(columns={'value': 'assets'})

liab_data = download_fred_series('BOGZ1FL664190005Q', api_key)
liab_data = liab_data.rename(columns={'value': 'liab'})

equity_data = download_fred_series('BOGZ1FL665080003Q', api_key)
equity_data = equity_data.rename(columns={'value': 'equity'})

# Align balance-sheet components by date while retaining their full combined history.
data = assets_data.merge(liab_data, on='date', how='outer')
data = data.merge(equity_data, on='date', how='outer')

# Identify calendar quarters for the seasonal adjustment.
data['qtr'] = data['date'].dt.quarter
data['year'] = data['date'].dt.year

# Measure leverage as total assets relative to equity.
data['lev'] = data['assets'] / data['equity']

# Start the leverage history in 1968, the baseline year for the seasonal adjustment.
data = data[data['year'] >= 1968].copy()

data = data.sort_values('date').reset_index(drop=True)

# Measure leverage growth relative to the preceding observation.
data['levfacnsa'] = np.log(data['lev']) - np.log(data['lev'].shift(1))

# Estimate the historical seasonal pattern separately for each calendar quarter.
data['tempMean'] = 0.0

for qtr in [1, 2, 3, 4]:
    qtr_mask = (data['qtr'] == qtr)
    qtr_data = data[qtr_mask].copy().sort_values('year').reset_index(drop=True)

    qtr_data['cumsum'] = qtr_data['levfacnsa'].cumsum()
    qtr_data['count'] = range(1, len(qtr_data) + 1)

    # Estimate the seasonal mean from this calendar quarter's history.
    qtr_data['tempMean'] = qtr_data['cumsum'] / qtr_data['count']

    # Preserve the Q1 baseline convention, which excludes one observation from the count.
    if qtr == 1:
        mask_adj = qtr_data['count'] > 1
        qtr_data.loc[mask_adj, 'tempMean'] = qtr_data.loc[mask_adj, 'cumsum'] / (qtr_data.loc[mask_adj, 'count'] - 1)

    # Leave the 1968 baseline unadjusted.
    qtr_data.loc[qtr_data['year'] == 1968, 'tempMean'] = 0.0

    data.loc[qtr_mask, 'tempMean'] = qtr_data['tempMean'].values

# Remove the seasonal pattern using only estimates from earlier years.
data['levfac'] = data['levfacnsa']

for qtr in [1, 2, 3, 4]:
    qtr_mask = (data['qtr'] == qtr)
    qtr_indices = data[qtr_mask].sort_values('year').index

    tempMean_lagged = data.loc[qtr_indices, 'tempMean'].shift(1)

    data.loc[qtr_indices, 'levfac'] = (
        data.loc[qtr_indices, 'levfacnsa'] - tempMean_lagged
    )

    # Keep the first observation unadjusted when no earlier seasonal estimate exists.
    first_idx = qtr_indices[0]
    data.loc[first_idx, 'levfac'] = data.loc[first_idx, 'levfacnsa']

    # Retain the original Q1 1969 convention: report the unadjusted change.
    if qtr == 1:
        q1_1969_mask = (data['year'] == 1969) & (data['qtr'] == 1)
        if q1_1969_mask.any():
            q1_1969_idx = data[q1_1969_mask].index[0]
            data.loc[q1_1969_idx, 'levfac'] = data.loc[q1_1969_idx, 'levfacnsa']

# Provide one leverage-growth factor per calendar quarter.
output_data = data[['qtr', 'year', 'levfac']].copy()
output_data = output_data.sort_values(['year', 'qtr'])

# Preserve quarters with missing factors rather than shortening the time series.

print(f"Processed {len(output_data)} quarterly observations")

# Save the quarterly leverage factor for downstream signals.
output_file = "../pyData/Intermediate/brokerLev.parquet"
output_data.to_parquet(output_file, index=False)

print(f"Saved {len(output_data)} records to {output_file}")
print("Broker-dealer leverage processing completed successfully.")
