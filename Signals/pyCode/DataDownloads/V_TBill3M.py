#!/usr/bin/env python3
"""
3-month T-bill rate download script - Python equivalent of V_TBill3M.do

Downloads 3-month Treasury bill rate from FRED and aggregates to quarterly
averages.
"""

import os
import pandas as pd
import requests
from dotenv import load_dotenv

load_dotenv()


def download_fred_series(series_id, api_key, start_date='1900-01-01'):
    """Download a series from FRED API.
    
    Args:
        series_id: FRED series identifier
        api_key: FRED API key
        start_date: Start date for data retrieval
        
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

    try:
        response = requests.get(url, params=params, timeout=30)
        response.raise_for_status()
        data = response.json()

        if 'observations' in data:
            df = pd.DataFrame(data['observations'])
            df['date'] = pd.to_datetime(df['date'])
            df['value'] = pd.to_numeric(df['value'], errors='coerce')
            df = df[['date', 'value']].dropna()
            return df
        else:
            print(f"No observations found for {series_id}")
            return pd.DataFrame()

    except requests.exceptions.RequestException as e:
        print(f"Error downloading {series_id}: {e}")
        return pd.DataFrame()


def main():
    """Main function to download and process T-bill data"""
    print("Downloading 3-month T-bill rate from FRED...")

    # Get FRED API key from environment
    fred_api_key = os.getenv("FRED_KEY")
    if not fred_api_key:
        print("ERROR: FRED_KEY not found in environment variables")
        print("Please set FRED_KEY in your .env file")
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
    print(f"Date range: {tbill_data['date'].min()} to {tbill_data['date'].max()}")

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

    # Reorder columns to match Stata: TbillRate3M, qtr, year
    final_data = quarterly_data[['TbillRate3M', 'qtr', 'year']]

    print(f"Created {len(final_data)} quarterly records")

    # Save the data
    final_data.to_parquet("../pyData/Intermediate/TBill3M.parquet")

    print(
        f"3-month T-bill rate data saved with {len(final_data)} "
        "quarterly records"
    )
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