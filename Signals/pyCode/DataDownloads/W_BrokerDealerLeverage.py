#!/usr/bin/env python3
"""
Broker-Dealer Leverage processing - Python equivalent of W_BrokerDealerLeverage.do

Downloads broker-dealer financial data from FRED and computes seasonally adjusted
leverage factor.
"""

import os
import pandas as pd
import numpy as np
import requests
from dotenv import load_dotenv

load_dotenv()


def download_fred_series(series_id, api_key, start_date='1900-01-01',
                         max_retries=3, retry_delay=1):
    """Download a series from FRED API with retry logic."""
    import time
    
    url = "https://api.stlouisfed.org/fred/series/observations"
    params = {
        'series_id': series_id,
        'api_key': api_key,
        'file_type': 'json',
        'observation_start': start_date,
        'sort_order': 'asc'
    }
    
    for attempt in range(max_retries):
        try:
            response = requests.get(url, params=params, timeout=30)
            response.raise_for_status()
            
            data = response.json()
            if 'observations' not in data:
                raise ValueError(f"No observations found for series {series_id}")
            
            df = pd.DataFrame(data['observations'])
            df['date'] = pd.to_datetime(df['date'])
            df['value'] = pd.to_numeric(df['value'], errors='coerce')
            df = df.dropna(subset=['value'])
            
            print(f"Downloaded {len(df)} observations for {series_id}")
            return df[['date', 'value']]
            
        except Exception as e:
            print(f"Attempt {attempt + 1} failed for {series_id}: {e}")
            if attempt < max_retries - 1:
                time.sleep(retry_delay * (2 ** attempt))
            else:
                raise


def main():
    """Process broker-dealer leverage data."""
    print("Processing broker-dealer leverage data...")
    
    # Get FRED API key
    api_key = os.getenv('FRED_API_KEY')
    if not api_key:
        raise ValueError("FRED_API_KEY environment variable not set")
    
    # Download the three FRED series
    print("Downloading FRED series...")
    
    # Assets: BOGZ1FL664090005Q
    assets_data = download_fred_series('BOGZ1FL664090005Q', api_key)
    assets_data = assets_data.rename(columns={'value': 'assets'})
    
    # Liabilities: BOGZ1FL664190005Q
    liab_data = download_fred_series('BOGZ1FL664190005Q', api_key)
    liab_data = liab_data.rename(columns={'value': 'liab'})
    
    # Equity: BOGZ1FL665080003Q
    equity_data = download_fred_series('BOGZ1FL665080003Q', api_key)
    equity_data = equity_data.rename(columns={'value': 'equity'})
    
    # Merge all series
    data = assets_data.merge(liab_data, on='date', how='outer')
    data = data.merge(equity_data, on='date', how='outer')
    
    # Create quarter and year variables
    data['qtr'] = data['date'].dt.quarter
    data['year'] = data['date'].dt.year
    
    # Calculate leverage
    data['lev'] = data['assets'] / data['equity']
    
    # Drop data before 1968
    data = data[data['year'] >= 1968].copy()
    
    # Sort by date
    data = data.sort_values('date').reset_index(drop=True)
    
    # Compute log leverage change
    data['levfacnsa'] = np.log(data['lev']) - np.log(data['lev'].shift(1))
    
    # Compute seasonal adjustment using Stata's cumulative sum logic
    # bys qtr (year): gen tempMean = sum(levfacnsa)/_n
    data['tempMean'] = 0.0
    
    for qtr in [1, 2, 3, 4]:
        qtr_mask = (data['qtr'] == qtr)
        qtr_data = data[qtr_mask].copy().sort_values('year').reset_index(drop=True)
        
        # Calculate cumulative sum and running count
        qtr_data['cumsum'] = qtr_data['levfacnsa'].cumsum()
        qtr_data['count'] = range(1, len(qtr_data) + 1)
        
        # Standard case: tempMean = cumsum / count
        qtr_data['tempMean'] = qtr_data['cumsum'] / qtr_data['count']
        
        # Special case for Q1: use (count-1) instead of count when count > 1
        if qtr == 1:
            mask_adj = qtr_data['count'] > 1
            qtr_data.loc[mask_adj, 'tempMean'] = qtr_data.loc[mask_adj, 'cumsum'] / (qtr_data.loc[mask_adj, 'count'] - 1)
        
        # Set to 0 for 1968 (first year)
        qtr_data.loc[qtr_data['year'] == 1968, 'tempMean'] = 0.0
        
        # Update main dataframe
        data.loc[qtr_mask, 'tempMean'] = qtr_data['tempMean'].values
    
    # Compute seasonally adjusted leverage factor
    # Replicate Stata logic: by qtr: gen levfac = levfacnsa - tempMean[_n-1]
    data['levfac'] = data['levfacnsa']  # Default value
    
    for qtr in [1, 2, 3, 4]:
        qtr_mask = (data['qtr'] == qtr)
        qtr_indices = data[qtr_mask].sort_values('year').index
        
        # Create tempMean lagged by 1 position within quarter
        tempMean_lagged = data.loc[qtr_indices, 'tempMean'].shift(1)
        
        # Apply seasonal adjustment: levfac = levfacnsa - tempMean[_n-1]
        data.loc[qtr_indices, 'levfac'] = (
            data.loc[qtr_indices, 'levfacnsa'] - tempMean_lagged
        )
        
        # First observation in each quarter keeps original value (_n==1)
        first_idx = qtr_indices[0]
        data.loc[first_idx, 'levfac'] = data.loc[first_idx, 'levfacnsa']
        
        # Special case for Q1 1969
        if qtr == 1:
            q1_1969_mask = (data['year'] == 1969) & (data['qtr'] == 1)
            if q1_1969_mask.any():
                q1_1969_idx = data[q1_1969_mask].index[0]
                data.loc[q1_1969_idx, 'levfac'] = data.loc[q1_1969_idx, 'levfacnsa']
    
    # Keep only required columns (match Stata output column order)
    output_data = data[['qtr', 'year', 'levfac']].copy()
    output_data = output_data.sort_values(['year', 'qtr'])
    
    # Keep all observations including missing levfac (matching Stata behavior)
    
    print(f"Processed {len(output_data)} quarterly observations")
    
    # Save to parquet
    output_file = "../pyData/Intermediate/brokerLev.parquet"
    os.makedirs(os.path.dirname(output_file), exist_ok=True)
    output_data.to_parquet(output_file, index=False)
    
    print(f"Saved {len(output_data)} records to {output_file}")
    print("Broker-dealer leverage processing completed successfully.")


if __name__ == "__main__":
    main()