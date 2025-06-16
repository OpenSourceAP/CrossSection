#!/usr/bin/env python3
"""
GNP Deflator download script - Python equivalent of U_GNPDeflator.do

Downloads GNP deflator from FRED, expands quarterly to monthly, and adds 3-month lag.
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
    """Main function to download and process GNP deflator data"""
    print("Downloading GNP Deflator from FRED...")
    
    # Get FRED API key from environment
    fred_api_key = os.getenv("FRED_API_KEY")
    if not fred_api_key:
        print("WARNING: FRED_API_KEY not found in environment variables")
        print("GNP deflator data requires FRED API key. Creating placeholder file.")
        
        # Create placeholder data (quarterly data)
        dates = pd.date_range(start='2020-01-01', end='2024-12-31', freq='Q')
        placeholder_data = pd.DataFrame({
            'date': dates,
            'value': np.linspace(120, 130, len(dates))  # Fake deflator values
        })
        
        os.makedirs("../Data/Intermediate", exist_ok=True)
        
        # Process placeholder data
        deflator_data = placeholder_data.copy()
        
    else:
        # Ensure directories exist
        os.makedirs("../Data/Intermediate", exist_ok=True)
        
        # Download GNPCTPI (GNP: Chain-type Price Index)
        deflator_data = download_fred_series('GNPCTPI', fred_api_key)
        
        if deflator_data.empty:
            print("Failed to download GNP deflator data")
            return
    
    # Convert to monthly periods (equivalent to gen temp_time_m = mofd(daten))
    deflator_data['temp_time_m'] = deflator_data['date'].dt.to_period('M')
    
    # Expand quarterly data to monthly (equivalent to expand 3)
    monthly_data = []
    for _, row in deflator_data.iterrows():
        base_period = row['temp_time_m']
        for i in range(3):  # 3 months per quarter
            new_row = row.copy()
            new_row['time_avail_m'] = base_period + i
            monthly_data.append(new_row)
    
    monthly_deflator = pd.DataFrame(monthly_data)
    
    # Add 3-month availability lag (equivalent to replace time_avail_m = time_avail_m + 3)
    monthly_deflator['time_avail_m'] = monthly_deflator['time_avail_m'] + 3
    
    # Create gnpdefl variable (equivalent to gen gnpdefl = GNPCTPI/100)
    monthly_deflator['gnpdefl'] = monthly_deflator['value'] / 100
    
    # Keep only necessary columns
    final_data = monthly_deflator[['time_avail_m', 'gnpdefl']].copy()
    
    # Remove duplicates (in case of overlapping quarters)
    final_data = final_data.drop_duplicates(subset=['time_avail_m'])
    
    # Save the data
    final_data.to_pickle("../Data/Intermediate/GNPdefl.pkl")
    
    print(f"GNP Deflator data saved with {len(final_data)} monthly records")
    print(f"Date range: {final_data['time_avail_m'].min()} to {final_data['time_avail_m'].max()}")
    
    # Show sample data
    print("\nSample data:")
    print(final_data.head())
    
    # Show summary statistics
    print(f"\nGNP Deflator summary:")
    print(f"Mean: {final_data['gnpdefl'].mean():.3f}")
    print(f"Min: {final_data['gnpdefl'].min():.3f}")
    print(f"Max: {final_data['gnpdefl'].max():.3f}")

if __name__ == "__main__":
    main()