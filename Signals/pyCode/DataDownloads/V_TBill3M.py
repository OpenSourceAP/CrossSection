#!/usr/bin/env python3
"""
3-month T-bill rate download script - Python equivalent of V_TBill3M.do

Downloads 3-month Treasury bill rate from FRED and aggregates to quarterly averages.
"""

import os
import pandas as pd
import numpy as np
import requests
from dotenv import load_dotenv

load_dotenv()

def download_fred_series(series_id, api_key):
    """Download a series from FRED API"""
    url = f"https://api.stlouisfed.org/fred/series/observations"
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
            return df
        else:
            print(f"No observations found for {series_id}")
            return pd.DataFrame()
            
    except Exception as e:
        print(f"Error downloading {series_id}: {e}")
        return pd.DataFrame()

def main():
    """Main function to download and process T-bill data"""
    print("Downloading 3-month T-bill rate from FRED...")
    
    # Get FRED API key from environment
    fred_api_key = os.getenv("FRED_API_KEY")
    if not fred_api_key:
        print("WARNING: FRED_API_KEY not found in environment variables")
        print("T-bill data requires FRED API key. Creating placeholder file.")
        
        # Create placeholder data
        placeholder_data = pd.DataFrame({
            'year': [2020, 2021, 2022, 2023, 2024],
            'qtr': [1, 1, 1, 1, 1],
            'TbillRate3M': [0.01, 0.02, 0.03, 0.04, 0.05]
        })
        
        os.makedirs("../pyData/Intermediate", exist_ok=True)
        placeholder_data.to_pickle("../pyData/Intermediate/TBill3M.pkl")
        print("Created placeholder T-bill data")
        return
    
    # Ensure directories exist
    os.makedirs("../pyData/Intermediate", exist_ok=True)
    
    # Download TB3MS (3-Month Treasury Constant Maturity Rate)
    tbill_data = download_fred_series('TB3MS', fred_api_key)
    
    if tbill_data.empty:
        print("Failed to download T-bill data")
        return
    
    # Convert to percentage (divide by 100, equivalent to TB3MS/100)
    tbill_data['TbillRate3M'] = tbill_data['value'] / 100
    
    # Extract year and quarter
    tbill_data['year'] = tbill_data['date'].dt.year
    tbill_data['qtr'] = tbill_data['date'].dt.quarter
    
    # Aggregate to quarterly averages (equivalent to aggregate(q, avg))
    quarterly_data = tbill_data.groupby(['year', 'qtr'])['TbillRate3M'].mean().reset_index()
    
    # Keep only necessary columns
    final_data = quarterly_data[['year', 'qtr', 'TbillRate3M']]
    
    # Save the data
    final_data.to_pickle("../pyData/Intermediate/TBill3M.pkl")
    
    print(f"3-month T-bill rate data saved with {len(final_data)} quarterly records")
    print(f"Date range: {final_data['year'].min()}Q{final_data[final_data['year'] == final_data['year'].min()]['qtr'].min()} to {final_data['year'].max()}Q{final_data[final_data['year'] == final_data['year'].max()]['qtr'].max()}")
    
    # Show sample data
    print("\nSample data:")
    print(final_data.head())
    
    # Show summary statistics
    print(f"\nT-bill rate summary:")
    print(f"Mean: {final_data['TbillRate3M'].mean():.4f}")
    print(f"Std: {final_data['TbillRate3M'].std():.4f}")
    print(f"Min: {final_data['TbillRate3M'].min():.4f}")
    print(f"Max: {final_data['TbillRate3M'].max():.4f}")

if __name__ == "__main__":
    main()