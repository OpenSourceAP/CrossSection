#!/usr/bin/env python3
"""
VIX data download script - Python equivalent of T_VIX.do

Downloads VIX data using FRED API.
Note: Uses VXOCLS (VXO) and VIXCLS (VIX) to create continuous series.
"""

import os
import pandas as pd
import numpy as np
from datetime import datetime
import requests
from dotenv import load_dotenv

load_dotenv()

def download_fred_series(series_id, api_key):
    """Download a series from FRED API"""
    url = "https://api.stlouisfed.org/fred/series/observations"
    params = {
        'series_id': series_id,
        'api_key': api_key,
        'file_type': 'json',
        'observation_start': '1900-01-01'
    }

    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        data = response.json()

        if 'observations' in data:
            df = pd.DataFrame(data['observations'])
            df['date'] = pd.to_datetime(df['date'])
            df['value'] = pd.to_numeric(df['value'], errors='coerce')
            df = df[['date', 'value']].dropna()
            df.columns = ['date', series_id]
            return df
        else:
            print("No observations found for {series_id}")
            return pd.DataFrame()

    except Exception as e:
        print("Error downloading {series_id}: {e}")
        return pd.DataFrame()

def main():
    """Main function to download and process VIX data"""
    print("Downloading VIX data from FRED...")

    # Get FRED API key from environment
    fred_api_key = os.getenv("FRED_API_KEY")
    if not fred_api_key:
        print("ERROR: FRED_API_KEY not found in environment variables")
        print("Please set FRED_API_KEY in your .env file")
        print("You can get a free API key from: https://fred.stlouisfed.org/docs/api/api_key.html")
        return

    # Ensure directories exist
    os.makedirs("../pyData/Intermediate", exist_ok=True)

    # Download both VIX series
    vxocls_data = download_fred_series('VXOCLS', fred_api_key)  # VXO (older series)
    vixcls_data = download_fred_series('VIXCLS', fred_api_key)  # VIX (current series)

    if vxocls_data.empty and vixcls_data.empty:
        print("Failed to download any VIX data")
        return

    # Merge the two series
    if not vxocls_data.empty and not vixcls_data.empty:
        vix_data = pd.merge(vxocls_data, vixcls_data, on='date', how='outer')
    elif not vxocls_data.empty:
        vix_data = vxocls_data.copy()
        vix_data['VIXCLS'] = np.nan
    else:
        vix_data = vixcls_data.copy()
        vix_data['VXOCLS'] = np.nan

    vix_data = vix_data.sort_values('date').reset_index(drop=True)

    # Create combined VIX series (equivalent to Stata logic)
    # Use VXOCLS primarily, but use VIXCLS for dates >= Sept 23, 2021 when VXOCLS is missing
    cutoff_date = pd.to_datetime('2021-09-23')

    vix_data['vix'] = vix_data['VXOCLS']

    # Fill with VIXCLS for missing VXOCLS values after cutoff date
    post_cutoff = vix_data['date'] >= cutoff_date
    missing_vxo = vix_data['VXOCLS'].isna()
    fill_mask = post_cutoff & missing_vxo

    vix_data.loc[fill_mask, 'vix'] = vix_data.loc[fill_mask, 'VIXCLS']

    # Calculate daily change in VIX (equivalent to gen dVIX = vix - l.vix)
    vix_data['dVIX'] = vix_data['vix'].diff()

    # Keep only necessary columns and rename date
    final_data = vix_data[['date', 'vix', 'dVIX']].copy()
    final_data = final_data.rename(columns={'date': 'time_d'})

    # Remove rows with missing VIX data
    final_data = final_data.dropna(subset=['vix'])

    # Save the data
    final_data.to_pickle("../pyData/Intermediate/d_vix.pkl")

    print("VIX data saved with {len(final_data)} records")
    print("Date range: {final_data['time_d'].min().strftime('%Y-%m-%d')} to {final_data['time_d'].max().strftime('%Y-%m-%d')}")

    # Show sample data
    print("\nSample data:")
    print(final_data.head())

    # Show summary statistics
    print("\nVIX summary:")
    print("Mean: {final_data['vix'].mean():.2f}")
    print("Std: {final_data['vix'].std():.2f}")
    print("Min: {final_data['vix'].min():.2f}")
    print("Max: {final_data['vix'].max():.2f}")

if __name__ == "__main__":
    main()
