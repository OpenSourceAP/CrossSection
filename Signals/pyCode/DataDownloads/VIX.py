# ABOUTME: Downloads VIX volatility index data from FRED API using both VXO and VIX series
# ABOUTME: Creates continuous VIX series and calculates daily VIX changes for market volatility analysis
"""
Inputs:
- FRED API series: VXOCLS (VXO - older volatility series)
- FRED API series: VIXCLS (VIX - current volatility series)

Outputs:
- ../pyData/Intermediate/d_vix.parquet

How to run: python3 VIX.py
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


def download_fred_series(series_id, api_key):
    # Set up FRED API request parameters
    url = "https://api.stlouisfed.org/fred/series/observations"
    params = {
        'series_id': series_id,
        'api_key': api_key,
        'file_type': 'json',
        'observation_start': '1900-01-01'
    }

    print(f"Downloading {series_id}...")
    response = requests.get(url, params=params, timeout=30)
    response.raise_for_status()
    data = response.json()

    # Process successful response
    df = pd.DataFrame(data['observations'])

    # Clean and format the data
    df['date'] = pd.to_datetime(df['date'])
    df['value'] = pd.to_numeric(df['value'], errors='coerce')
    df = df[['date', 'value']]
    df.columns = ['date', series_id]
    print(f"Successfully downloaded {len(df)} observations")
    return df


print("Downloading VIX data from FRED...")

# Get FRED API key from environment
fred_api_key = os.getenv("FRED_API_KEY")

# Download both VIX series
vxocls_data = download_fred_series('VXOCLS', fred_api_key)  # VXO (older series)
vixcls_data = download_fred_series('VIXCLS', fred_api_key)  # VIX (current series)

# Merge the two series
vix_data = pd.merge(vxocls_data, vixcls_data, on='date', how='outer')
vix_data = vix_data.sort_values('date').reset_index(drop=True)

# Create combined VIX series (equivalent to Stata logic)
cutoff_date = pd.to_datetime('2021-09-23')
vix_data['vix'] = vix_data['VXOCLS']

# Fill with VIXCLS for missing VXOCLS values after cutoff date
post_cutoff = vix_data['date'] >= cutoff_date
missing_vxo = vix_data['VXOCLS'].isna()
fill_mask = post_cutoff & missing_vxo
vix_data.loc[fill_mask, 'vix'] = vix_data.loc[fill_mask, 'VIXCLS']

# Keep only necessary columns and rename date first
final_data = vix_data[['date', 'vix']].copy()
final_data = final_data.rename(columns={'date': 'time_d'})

# Apply precision control to match Stata format
final_data['vix'] = final_data['vix'].astype('float32')

# Calculate daily change in VIX (equivalent to gen dVIX = vix - l.vix)
final_data['dVIX'] = final_data['vix'].diff().astype('float32')

# Apply row limit for debugging if configured
if MAX_ROWS_DL > 0:
    final_data = final_data.head(MAX_ROWS_DL)
    print(f"DEBUG MODE: Limited to {MAX_ROWS_DL} rows")

# Save the data
final_data.to_parquet("../pyData/Intermediate/d_vix.parquet")

# Print summary information
print(f"VIX data saved with {len(final_data)} records")
date_min = final_data['time_d'].min().strftime('%Y-%m-%d')
date_max = final_data['time_d'].max().strftime('%Y-%m-%d')
print(f"Date range: {date_min} to {date_max}")

print("\nSample data:")
print(final_data.head())

print("\nVIX summary:")
print(f"Total records: {len(final_data)}")
print(f"Missing VIX values: {final_data['vix'].isna().sum()}")
print(f"Missing dVIX values: {final_data['dVIX'].isna().sum()}")
print(f"Mean: {final_data['vix'].mean():.2f}")
print(f"Std: {final_data['vix'].std():.2f}")
print(f"Min: {final_data['vix'].min():.2f}")
print(f"Max: {final_data['vix'].max():.2f}")
