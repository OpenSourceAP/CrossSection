#!/usr/bin/env python3
"""
VIX data download script - Python equivalent of T_VIX.do

Downloads VIX data using FRED API.
Note: Uses VXOCLS (VXO) and VIXCLS (VIX) to create continuous series.
"""

import os
import time
import pandas as pd
import numpy as np
import requests
from dotenv import load_dotenv

load_dotenv()


def download_fred_series(series_id, api_key, max_retries=3, retry_delay=1):
    """Download a series from FRED API with retry logic.

    Args:
        series_id: FRED series identifier
        api_key: FRED API key
        max_retries: Maximum number of retry attempts
        retry_delay: Initial delay between retries (seconds)

    Returns:
        pandas.DataFrame: DataFrame with date and series_id columns
    """
    url = "https://api.stlouisfed.org/fred/series/observations"
    params = {
        'series_id': series_id,
        'api_key': api_key,
        'file_type': 'json',
        'observation_start': '1900-01-01'
    }

    for attempt in range(max_retries + 1):
        try:
            print(f"Downloading {series_id} (attempt {attempt + 1}...)")
            response = requests.get(url, params=params, timeout=30)
            response.raise_for_status()
            data = response.json()

            # Check for API errors in response
            if 'error_code' in data:
                raise requests.exceptions.RequestException(
                    f"FRED API error {data['error_code']}: "
                    f"{data.get('error_message', 'Unknown error')}"
                )

            if 'observations' in data:
                df = pd.DataFrame(data['observations'])
                if len(df) == 0:
                    print(f"Warning: No observations found for {series_id}")
                    return pd.DataFrame()

                df['date'] = pd.to_datetime(df['date'])
                df['value'] = pd.to_numeric(df['value'], errors='coerce')
                df = df[['date', 'value']].dropna()
                df.columns = ['date', series_id]
                print(f"Successfully downloaded {len(df)} observations")
                return df
            else:
                print(f"No observations found for {series_id}")
                return pd.DataFrame()

        except requests.exceptions.Timeout:
            print(f"Timeout downloading {series_id} (attempt {attempt + 1})")
        except requests.exceptions.ConnectionError:
            print(f"Connection error downloading {series_id} "
                  f"(attempt {attempt + 1})")
        except requests.exceptions.RequestException as e:
            print(f"Request error downloading {series_id}: {e}")
            if "API key" in str(e) or "error_code" in str(e):
                # Don't retry on API key errors
                break
        except Exception as e:
            print(f"Unexpected error downloading {series_id}: {e}")

        if attempt < max_retries:
            delay = retry_delay * (2 ** attempt)  # Exponential backoff
            print(f"Retrying in {delay} seconds...")
            time.sleep(delay)

    print(f"Failed to download {series_id} after {max_retries + 1} attempts")
    return pd.DataFrame()


def main():
    """Main function to download and process VIX data"""
    print("Downloading VIX data from FRED...")

    # Get FRED API key from environment
    fred_api_key = os.getenv("FRED_API_KEY")
    if not fred_api_key:
        print("ERROR: FRED_API_KEY not found in environment variables")
        print("Please set FRED_API_KEY in your .env file")
        print("You can get a free API key from: "
              "https://fred.stlouisfed.org/docs/api/api_key.html")
        return

    # Ensure directories exist
    os.makedirs("../pyData/Intermediate", exist_ok=True)

    # Download both VIX series
    # VXO (older series)
    vxocls_data = download_fred_series('VXOCLS', fred_api_key)
    # VIX (current series)
    vixcls_data = download_fred_series('VIXCLS', fred_api_key)

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
    # Use VXOCLS primarily, but use VIXCLS for dates >= Sept 23, 2021
    # when VXOCLS is missing
    cutoff_date = pd.to_datetime('2021-09-23')

    vix_data['vix'] = vix_data['VXOCLS']

    # Fill with VIXCLS for missing VXOCLS values after cutoff date
    post_cutoff = vix_data['date'] >= cutoff_date
    missing_vxo = vix_data['VXOCLS'].isna()
    fill_mask = post_cutoff & missing_vxo

    vix_data.loc[fill_mask, 'vix'] = vix_data.loc[fill_mask, 'VIXCLS']

    # Calculate daily change in VIX
    # (equivalent to gen dVIX = vix - l.vix)
    vix_data['dVIX'] = vix_data['vix'].diff()

    # Keep only necessary columns and rename date
    final_data = vix_data[['date', 'vix', 'dVIX']].copy()
    final_data = final_data.rename(columns={'date': 'time_d'})

    # Remove rows with missing VIX data
    final_data = final_data.dropna(subset=['vix'])

    # Save the data
    final_data.to_parquet("../pyData/Intermediate/d_vix.parquet")

    print(f"VIX data saved with {len(final_data)} records")
    date_min = final_data['time_d'].min().strftime('%Y-%m-%d')
    date_max = final_data['time_d'].max().strftime('%Y-%m-%d')
    print(f"Date range: {date_min} to {date_max}")

    # Show sample data
    print("\nSample data:")
    print(final_data.head())

    # Show summary statistics
    print("\nVIX summary:")
    print(f"Mean: {final_data['vix'].mean():.2f}")
    print(f"Std: {final_data['vix'].std():.2f}")
    print(f"Min: {final_data['vix'].min():.2f}")
    print(f"Max: {final_data['vix'].max():.2f}")


if __name__ == "__main__":
    main()
