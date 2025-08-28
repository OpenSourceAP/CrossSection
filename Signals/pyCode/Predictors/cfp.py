# ABOUTME: cfp predictor - calculates cash flow to price ratio
# ABOUTME: Run: python3 pyCode/Predictors/cfp.py

"""
cfp Predictor

Cash flow to price ratio calculation with accrual adjustment.
Uses either calculated cash flow (ib - accrual_level) or direct operating cash flow (oancf).

Inputs:
- m_aCompustat.parquet (gvkey, permno, time_avail_m, act, che, lct, dlc, txp, dp, ib, oancf)
- SignalMasterTable.parquet (permno, time_avail_m, mve_c)

Outputs:
- cfp.csv (permno, yyyymm, cfp)

This predictor calculates cash flow to price ratio using either:
1. Calculated cash flow: (ib - accrual_level) / mve_c
2. Direct operating cash flow: oancf / mve_c (if oancf is available)

Where accrual_level is calculated using 12-month changes in working capital components.
"""

import pandas as pd
import numpy as np
import sys
import os

# Add utils directory to path for imports
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from utils.save_standardized import save_predictor

def main():
    print("Starting cfp predictor...")
    
    # DATA LOAD
    print("Loading m_aCompustat data...")
    compustat_df = pd.read_parquet('../pyData/Intermediate/m_aCompustat.parquet', 
                                 columns=['gvkey', 'permno', 'time_avail_m', 'act', 'che', 
                                         'lct', 'dlc', 'txp', 'dp', 'ib', 'oancf'])
    
    print(f"Loaded {len(compustat_df):,} Compustat observations")
    
    # Deduplicate by permno time_avail_m (equivalent to bysort permno time_avail_m: keep if _n == 1)
    compustat_df = compustat_df.drop_duplicates(['permno', 'time_avail_m'], keep='first')
    print(f"After deduplication: {len(compustat_df):,} observations")
    
    # Load SignalMasterTable
    print("Loading SignalMasterTable...")
    signal_master = pd.read_parquet('../pyData/Intermediate/SignalMasterTable.parquet', 
                                   columns=['permno', 'time_avail_m', 'mve_c'])
    
    print(f"Loaded SignalMasterTable: {len(signal_master):,} observations")
    
    # Merge with SignalMasterTable (equivalent to merge 1:1 permno time_avail_m using SignalMasterTable, keep(using match))
    print("Merging with SignalMasterTable...")
    df = pd.merge(signal_master, compustat_df[['permno', 'time_avail_m', 'act', 'che', 
                                              'lct', 'dlc', 'txp', 'dp', 'ib', 'oancf']], 
                  on=['permno', 'time_avail_m'], how='inner')
    
    print(f"After merge: {len(df):,} observations")
    
    # SIGNAL CONSTRUCTION
    print("Constructing cfp signal...")
    
    # Sort by permno and time_avail_m (equivalent to xtset permno time_avail_m)
    df = df.sort_values(['permno', 'time_avail_m'])
    
    # Create 12-month lags for accrual calculation (calendar-based, not position-based)
    lag_cols = ['act', 'che', 'lct', 'dlc', 'txp']
    for col in lag_cols:
        # Create 12-month lag using calendar months, not position-based shift
        df[f'lag_time'] = df['time_avail_m'] - pd.DateOffset(months=12)
        lag_data = df[['permno', 'time_avail_m', col]].copy()
        lag_data = lag_data.rename(columns={'time_avail_m': 'lag_time', col: f'l12_{col}'})
        df = pd.merge(df, lag_data, on=['permno', 'lag_time'], how='left')
        df = df.drop('lag_time', axis=1)
    
    # Calculate accrual_level
    # accrual_level = (act-l12.act - (che-l12.che)) - ((lct-l12.lct)-(dlc-l12.dlc)-(txp-l12.txp)-dp)
    df['accrual_level'] = (
        (df['act'] - df['l12_act']) - (df['che'] - df['l12_che'])
    ) - (
        (df['lct'] - df['l12_lct']) - (df['dlc'] - df['l12_dlc']) - (df['txp'] - df['l12_txp']) - df['dp']
    )
    
    # Calculate initial cfp = (ib - accrual_level) / mve_c
    df['calculated_cf'] = df['ib'] - df['accrual_level']
    
    # Calculate cfp with domain-aware missing value handling
    # Following missing/missing = 1.0 pattern for division operations
    df['cfp'] = np.where(
        df['mve_c'] == 0,
        np.nan,  # Division by zero = missing
        np.where(
            df['calculated_cf'].isna() & df['mve_c'].isna(),
            1.0,  # missing/missing = 1.0 (no change)
            df['calculated_cf'] / df['mve_c']
        )
    )
    
    # Replace with oancf/mve_c if oancf is available (equivalent to replace cfp = oancf/mve_c if oancf !=.)
    mask_oancf_available = df['oancf'].notna()
    df.loc[mask_oancf_available, 'cfp'] = np.where(
        df.loc[mask_oancf_available, 'mve_c'] == 0,
        np.nan,
        np.where(
            df.loc[mask_oancf_available, 'oancf'].isna() & df.loc[mask_oancf_available, 'mve_c'].isna(),
            1.0,
            df.loc[mask_oancf_available, 'oancf'] / df.loc[mask_oancf_available, 'mve_c']
        )
    )
    
    print(f"Generated cfp values for {df['cfp'].notna().sum():,} observations")
    print(f"Used oancf for {mask_oancf_available.sum():,} observations")
    
    # Clean up temporary columns
    lag_cols_to_drop = [f'l12_{col}' for col in lag_cols]
    df = df.drop(columns=lag_cols_to_drop + ['accrual_level', 'calculated_cf'])
    
    # SAVE
    print("Saving predictor...")
    save_predictor(df, 'cfp')
    
    print("cfp predictor completed successfully!")

if __name__ == "__main__":
    main()