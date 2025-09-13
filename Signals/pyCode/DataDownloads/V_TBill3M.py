# ABOUTME: Downloads 3-month T-bill rate from FRED and aggregates to quarterly averages
# ABOUTME: Creates year-quarter-level dataset with TbillRate3M variable for downstream analysis
"""
Inputs:
- FRED API TB3MS series (monthly 3-month Treasury bill rates)
- FRED_API_KEY environment variable

Outputs:
- ../pyData/Intermediate/TBill3M.parquet

How to run: python V_TBill3M.py
"""

import os
import pandas as pd
import numpy as np
import requests
from dotenv import load_dotenv
import sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from utils.column_standardizer_yaml import standardize_columns

load_dotenv()


def download_fred_tb3ms(api_key):
    print("Downloading TB3MS from FRED...")

    url = "https://api.stlouisfed.org/fred/series/observations"
    params = {
        'series_id': 'TB3MS',
        'api_key': api_key,
        'file_type': 'json',
        'observation_start': '1900-01-01'
    }

    response = requests.get(url, params=params, timeout=30)
    response.raise_for_status()
    data = response.json()

    if 'observations' not in data:
        raise ValueError("No observations found in FRED response")

    df = pd.DataFrame(data['observations'])
    df['date'] = pd.to_datetime(df['date'])
    df['TB3MS'] = pd.to_numeric(df['value'], errors='coerce')
    df = df[['date', 'TB3MS']].dropna()

    print(f"Downloaded {len(df)} monthly observations")
    return df


def main():
    print("Processing 3-month T-bill rate...")
    
    # Get FRED API key from environment
    fred_api_key = os.getenv("FRED_API_KEY")
    if not fred_api_key:
        print("ERROR: FRED_API_KEY not found in environment variables")
        return
    
    # Create output directory if needed
    os.makedirs("../pyData/Intermediate", exist_ok=True)
    
    # Download monthly T-bill data from FRED
    monthly_data = download_fred_tb3ms(fred_api_key)
    
    # Prepare data for quarterly aggregation
    monthly_data = monthly_data.set_index('date')
    

    # Aggregate monthly data to quarterly averages
    quarterly_data = monthly_data.resample('QE').mean()
    quarterly_data = quarterly_data.dropna().reset_index()

    print(f"Aggregated to {len(quarterly_data)} quarterly observations")

    # Convert T-bill rate from percentage to decimal
    quarterly_data['TbillRate3M'] = quarterly_data['TB3MS'] / 100.0
    
    # Extract quarter from date
    quarterly_data['qtr'] = quarterly_data['date'].dt.quarter

    # Extract year from date
    quarterly_data['year'] = quarterly_data['date'].dt.year

    # Keep only required columns
    final_data = quarterly_data[['year', 'qtr', 'TbillRate3M']].copy()

    # Display summary information
    print(f"Final dataset: {len(final_data)} quarterly records")
    date_range_start = (
        f"{final_data['year'].min()}Q"
        f"{final_data[final_data['year'] == final_data['year'].min()]['qtr'].min()}"
    )
    date_range_end = (
        f"{final_data['year'].max()}Q"
        f"{final_data[final_data['year'] == final_data['year'].max()]['qtr'].max()}"
    )
    print(f"Date range: {date_range_start} to {date_range_end}")

    # Apply standardization and save to parquet
    final_data = standardize_columns(final_data, 'TBill3M')
    final_data.to_parquet("../pyData/Intermediate/TBill3M.parquet", index=False)

    print("3-month T-bill rate data saved successfully")

    # Display sample data and summary statistics
    print("\nSample data:")
    print(final_data.head())

    print("\nT-bill rate summary:")
    print(f"Mean: {final_data['TbillRate3M'].mean():.6f}")
    print(f"Std: {final_data['TbillRate3M'].std():.6f}")
    print(f"Min: {final_data['TbillRate3M'].min():.6f}")
    print(f"Max: {final_data['TbillRate3M'].max():.6f}")


if __name__ == "__main__":
    main()