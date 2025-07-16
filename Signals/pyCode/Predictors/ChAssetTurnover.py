# ABOUTME: ChAssetTurnover predictor - calculates change in asset turnover
# ABOUTME: Run: python3 pyCode/Predictors/ChAssetTurnover.py

"""
ChAssetTurnover Predictor

Change in asset turnover calculation.

Inputs:
- m_aCompustat.parquet (gvkey, permno, time_avail_m, rect, invt, aco, ppent, intan, ap, lco, lo, sale)

Outputs:
- ChAssetTurnover.csv (permno, yyyymm, ChAssetTurnover)

This predictor calculates:
1. Asset turnover = sale / average net assets over 12 months
2. Change in asset turnover = current - 12-month lag

Where net assets = rect + invt + aco + ppent + intan - ap - lco - lo
"""

import pandas as pd
import numpy as np
import sys
import os

# Add utils directory to path for imports
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'utils'))
from savepredictor import save_predictor

def main():
    print("Starting ChAssetTurnover predictor...")
    
    # DATA LOAD
    print("Loading m_aCompustat data...")
    df = pd.read_parquet('../pyData/Intermediate/m_aCompustat.parquet', 
                        columns=['gvkey', 'permno', 'time_avail_m', 'rect', 'invt', 'aco', 
                                'ppent', 'intan', 'ap', 'lco', 'lo', 'sale'])
    
    print(f"Loaded {len(df):,} Compustat observations")
    
    # Deduplicate by permno time_avail_m (equivalent to bysort permno time_avail_m: keep if _n == 1)
    df = df.drop_duplicates(['permno', 'time_avail_m'], keep='first')
    print(f"After deduplication: {len(df):,} observations")
    
    # SIGNAL CONSTRUCTION
    print("Constructing ChAssetTurnover signal...")
    
    # Sort by permno and time_avail_m (equivalent to xtset permno time_avail_m)
    df = df.sort_values(['permno', 'time_avail_m'])
    
    # Calculate net assets (temp = rect + invt + aco + ppent + intan - ap - lco - lo)
    df['temp'] = (df['rect'] + df['invt'] + df['aco'] + df['ppent'] + df['intan'] - 
                  df['ap'] - df['lco'] - df['lo'])
    
    # Create 12-month lag of net assets
    df['l12_temp'] = df.groupby('permno')['temp'].shift(12)
    
    # Calculate asset turnover = sale/((temp + l12.temp)/2)
    df['avg_net_assets'] = (df['temp'] + df['l12_temp']) / 2
    
    # Calculate AssetTurnover with domain-aware missing value handling
    df['AssetTurnover'] = np.where(
        df['avg_net_assets'] == 0,
        np.nan,  # Division by zero = missing
        np.where(
            df['sale'].isna() & df['avg_net_assets'].isna(),
            1.0,  # missing/missing = 1.0 (no change)
            df['sale'] / df['avg_net_assets']
        )
    )
    
    # Replace negative asset turnover with missing (equivalent to replace AssetTurnover = . if AssetTurnover < 0)
    df.loc[df['AssetTurnover'] < 0, 'AssetTurnover'] = np.nan
    
    # Create 12-month lag of AssetTurnover
    df['l12_AssetTurnover'] = df.groupby('permno')['AssetTurnover'].shift(12)
    
    # Calculate change in asset turnover
    df['ChAssetTurnover'] = df['AssetTurnover'] - df['l12_AssetTurnover']
    
    print(f"Generated ChAssetTurnover values for {df['ChAssetTurnover'].notna().sum():,} observations")
    
    # Clean up temporary columns
    df = df.drop(columns=['temp', 'l12_temp', 'avg_net_assets', 'AssetTurnover', 'l12_AssetTurnover'])
    
    # SAVE
    print("Saving predictor...")
    save_predictor(df, 'ChAssetTurnover')
    
    print("ChAssetTurnover predictor completed successfully!")

if __name__ == "__main__":
    main()