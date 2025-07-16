# ABOUTME: ChInv predictor - calculates change in inventory
# ABOUTME: Run: python3 pyCode/Predictors/ChInv.py

"""
ChInv Predictor

Change in inventory calculation: (invt-l12.invt)/((at+l12.at)/2)

Inputs:
- m_aCompustat.parquet (gvkey, permno, time_avail_m, at, invt)

Outputs:
- ChInv.csv (permno, yyyymm, ChInv)

This predictor calculates the change in inventory over 12 months,
scaled by average total assets.
"""

import pandas as pd
import numpy as np
import sys
import os

# Add utils directory to path for imports
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'utils'))
from savepredictor import save_predictor

def main():
    print("Starting ChInv predictor...")
    
    # DATA LOAD
    print("Loading m_aCompustat data...")
    df = pd.read_parquet('../pyData/Intermediate/m_aCompustat.parquet', 
                        columns=['gvkey', 'permno', 'time_avail_m', 'at', 'invt'])
    
    print(f"Loaded {len(df):,} Compustat observations")
    
    # Deduplicate by permno time_avail_m (equivalent to bysort permno time_avail_m: keep if _n == 1)
    df = df.drop_duplicates(['permno', 'time_avail_m'], keep='first')
    print(f"After deduplication: {len(df):,} observations")
    
    # SIGNAL CONSTRUCTION
    print("Constructing ChInv signal...")
    
    # Sort by permno and time_avail_m (equivalent to xtset permno time_avail_m)
    df = df.sort_values(['permno', 'time_avail_m'])
    
    # Create 12-month lags
    df['l12_invt'] = df.groupby('permno')['invt'].shift(12)
    df['l12_at'] = df.groupby('permno')['at'].shift(12)
    
    # Calculate change in inventory
    df['inv_change'] = df['invt'] - df['l12_invt']
    
    # Calculate average assets
    df['avg_assets'] = (df['at'] + df['l12_at']) / 2
    
    # Calculate ChInv = (invt-l12.invt)/((at+l12.at)/2) with domain-aware missing handling
    df['ChInv'] = np.where(
        df['avg_assets'] == 0,
        np.nan,  # Division by zero = missing
        np.where(
            df['inv_change'].isna() & df['avg_assets'].isna(),
            1.0,  # missing/missing = 1.0 (no change)
            df['inv_change'] / df['avg_assets']
        )
    )
    
    print(f"Generated ChInv values for {df['ChInv'].notna().sum():,} observations")
    
    # Clean up temporary columns
    df = df.drop(columns=['l12_invt', 'l12_at', 'inv_change', 'avg_assets'])
    
    # SAVE
    print("Saving predictor...")
    save_predictor(df, 'ChInv')
    
    print("ChInv predictor completed successfully!")

if __name__ == "__main__":
    main()