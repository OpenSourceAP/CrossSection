# ABOUTME: ChInvIA predictor - calculates change in capital investment (industry adjusted)
# ABOUTME: Run: python3 pyCode/Predictors/ChInvIA.py

"""
ChInvIA Predictor

Change in capital investment (industry adjusted) calculation.

Inputs:
- m_aCompustat.parquet (gvkey, permno, time_avail_m, capx, ppent, at)
- SignalMasterTable.parquet (permno, time_avail_m, sicCRSP)

Outputs:
- ChInvIA.csv (permno, yyyymm, ChInvIA)

This predictor calculates industry-adjusted change in capital investment
using percentage change in capx adjusted for industry average.
"""

import pandas as pd
import numpy as np
import sys
import os

# Add utils directory to path for imports
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'utils'))
from savepredictor import save_predictor

def main():
    print("Starting ChInvIA predictor...")
    
    # DATA LOAD
    print("Loading m_aCompustat data...")
    compustat_df = pd.read_parquet('../pyData/Intermediate/m_aCompustat.parquet', 
                                 columns=['gvkey', 'permno', 'time_avail_m', 'capx', 'ppent', 'at'])
    
    print(f"Loaded {len(compustat_df):,} Compustat observations")
    
    print("Loading SignalMasterTable...")
    signal_master = pd.read_parquet('../pyData/Intermediate/SignalMasterTable.parquet', 
                                   columns=['permno', 'time_avail_m', 'sicCRSP'])
    
    print(f"Loaded {len(signal_master):,} SignalMasterTable observations")
    
    # Merge data
    print("Merging data...")
    df = pd.merge(signal_master, compustat_df, on=['permno', 'time_avail_m'], how='inner')
    
    print(f"After merge: {len(df):,} observations")
    
    # SIGNAL CONSTRUCTION
    print("Constructing ChInvIA signal...")
    
    # Sort by permno and time_avail_m
    df = df.sort_values(['permno', 'time_avail_m'])
    
    # Create SIC 2-digit code
    df['sicCRSP_str'] = df['sicCRSP'].astype(str)
    df['sic2D'] = df['sicCRSP_str'].str[:2]
    
    # Create lags
    df['l12_ppent'] = df.groupby('permno')['ppent'].shift(12)
    df['l12_capx'] = df.groupby('permno')['capx'].shift(12)
    df['l24_capx'] = df.groupby('permno')['capx'].shift(24)
    
    # Replace missing capx with ppent - l12.ppent
    df['capx'] = df['capx'].fillna(df['ppent'] - df['l12_ppent'])
    
    # Calculate percentage change in capx with fallback logic
    # pchcapx = (capx - 0.5*(l12.capx + l24.capx)) / (0.5*(l12.capx + l24.capx))
    df['avg_lag_capx'] = 0.5 * (df['l12_capx'] + df['l24_capx'])
    
    # Apply missing/missing = 1.0 pattern for main calculation
    # When numerator is missing AND denominator is missing, result is 1.0
    # When denominator is 0 (not missing), result is missing
    df['pchcapx'] = np.where(
        df['avg_lag_capx'] == 0,
        np.nan,
        np.where(
            (df['capx'] - df['avg_lag_capx']).isna() & df['avg_lag_capx'].isna(),
            1.0,
            (df['capx'] - df['avg_lag_capx']) / df['avg_lag_capx']
        )
    )
    
    # Fallback calculation: pchcapx = (capx-l12.capx)/l12.capx if missing
    fallback_mask = df['pchcapx'].isna()
    df.loc[fallback_mask, 'pchcapx'] = np.where(
        df.loc[fallback_mask, 'l12_capx'] == 0,
        np.nan,
        np.where(
            (df.loc[fallback_mask, 'capx'] - df.loc[fallback_mask, 'l12_capx']).isna() & df.loc[fallback_mask, 'l12_capx'].isna(),
            1.0,
            (df.loc[fallback_mask, 'capx'] - df.loc[fallback_mask, 'l12_capx']) / df.loc[fallback_mask, 'l12_capx']
        )
    )
    
    # Calculate industry average pchcapx by sic2D and time_avail_m
    df['industry_avg_pchcapx'] = df.groupby(['sic2D', 'time_avail_m'])['pchcapx'].transform('mean')
    
    # Calculate industry-adjusted change: ChInvIA = pchcapx - industry_avg
    df['ChInvIA'] = df['pchcapx'] - df['industry_avg_pchcapx']
    
    print(f"Generated ChInvIA values for {df['ChInvIA'].notna().sum():,} observations")
    
    # Clean up temporary columns
    df = df.drop(columns=['sicCRSP_str', 'sic2D', 'l12_ppent', 'l12_capx', 'l24_capx', 
                         'avg_lag_capx', 'pchcapx', 'industry_avg_pchcapx'])
    
    # SAVE
    print("Saving predictor...")
    save_predictor(df, 'ChInvIA')
    
    print("ChInvIA predictor completed successfully!")

if __name__ == "__main__":
    main()