#!/usr/bin/env python3
"""
3-month T-bill rate download script - Python equivalent of V_TBill3M.do

Downloads 3-month Treasury bill rate from FRED and aggregates to quarterly
averages.
"""

import os
import time
import pandas as pd
import requests
from dotenv import load_dotenv

load_dotenv()


def download_fred_series(series_id, api_key, start_date='1900-01-01',
                         max_retries=3, retry_delay=1):
    """Download a series from FRED API with retry logic.

    Args:
        series_id: FRED series identifier
        api_key: FRED API key
        start_date: Start date for data retrieval
        max_retries: Maximum number of retry attempts
        retry_delay: Initial delay between retries (seconds)

    Returns:
        pandas.DataFrame: DataFrame with date and value columns
    """
    url = "https://api.stlouisfed.org/fred/series/observations"
    params = {
        'series_id': series_id,
        'api_key': api_key,
        'file_type': 'json',
        'observation_start': start_date
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
    """Main function to download and process T-bill data"""
    print("Downloading 3-month T-bill rate from FRED...")

    # Get FRED API key from environment
    fred_api_key = os.getenv("FRED_API_KEY")
    if not fred_api_key:
        print("ERROR: FRED_API_KEY not found in environment variables")
        print("Please set FRED_API_KEY in your .env file")
        return

    # Ensure directories exist
    os.makedirs("../pyData/Intermediate", exist_ok=True)

    # Download TB3MS (3-Month Treasury Constant Maturity Rate)
    print("Downloading TB3MS series from FRED...")
    tbill_data = download_fred_series('TB3MS', fred_api_key)

    if tbill_data.empty:
        print("Failed to download T-bill data")
        return

    print(f"Downloaded {len(tbill_data)} monthly observations")
    date_min = tbill_data['date'].min()
    date_max = tbill_data['date'].max()
    print(f"Date range: {date_min} to {date_max}")

    # Convert to percentage (divide by 100, equivalent to TB3MS/100)
    tbill_data['TbillRate3M'] = tbill_data['value'] / 100

    # Extract year and quarter
    tbill_data['year'] = tbill_data['date'].dt.year
    tbill_data['qtr'] = tbill_data['date'].dt.quarter

    # Aggregate to quarterly averages (equivalent to aggregate(q, avg))
    print("Aggregating to quarterly averages...")
    quarterly_data = (
        tbill_data.groupby(['year', 'qtr'])['TbillRate3M']
        .mean().reset_index()
    )

    # Convert to float32 to match Stata precision (compress command)
    quarterly_data['TbillRate3M'] = quarterly_data['TbillRate3M'].astype('float32')

    # Reorder columns to match Stata: TbillRate3M, qtr, year
    final_data = quarterly_data[['TbillRate3M', 'qtr', 'year']]

    print(f"Created {len(final_data)} quarterly records")

    # Save the data
    final_data.to_parquet("../pyData/Intermediate/TBill3M.parquet")

    print(f"3-month T-bill rate data saved with {len(final_data)} "
          "quarterly records")
    min_year = final_data['year'].min()
    max_year = final_data['year'].max()
    min_qtr = (
        final_data[final_data['year'] == min_year]['qtr'].min()
    )
    max_qtr = (
        final_data[final_data['year'] == max_year]['qtr'].max()
    )
    print(f"Date range: {min_year}Q{min_qtr} to {max_year}Q{max_qtr}")

    # Show sample data
    print("\nSample data:")
    print(final_data.head())

    # Show summary statistics
    print("\nT-bill rate summary:")
    print(f"Mean: {final_data['TbillRate3M'].mean():.4f}")
    print(f"Std: {final_data['TbillRate3M'].std():.4f}")
    print(f"Min: {final_data['TbillRate3M'].min():.4f}")
    print(f"Max: {final_data['TbillRate3M'].max():.4f}")


if __name__ == "__main__":
    main()
