# ABOUTME: CompEquIss predictor - calculates composite equity issuance
# ABOUTME: Run: python3 pyCode/Predictors/CompEquIss.py

"""
CompEquIss Predictor

Composite equity issuance calculation.

Inputs:
- SignalMasterTable.parquet (permno, time_avail_m, ret, mve_c)

Outputs:
- CompEquIss.csv (permno, yyyymm, CompEquIss)

This predictor calculates:
1. Cumulative index starting at 1, compounded with returns
2. Buy-and-hold return over 60 months
3. Composite equity issuance = log(mve_c/l60.mve_c) - buy_and_hold_return
"""

import pandas as pd
import numpy as np
import sys
import os

# Add utils directory to path for imports
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'utils'))
from savepredictor import save_predictor

def main():
    print("Starting CompEquIss predictor...")
    
    # DATA LOAD
    print("Loading SignalMasterTable...")
    df = pd.read_parquet('../pyData/Intermediate/SignalMasterTable.parquet', 
                        columns=['permno', 'time_avail_m', 'ret', 'mve_c'])
    
    print(f"Loaded {len(df):,} SignalMasterTable observations")
    
    # SIGNAL CONSTRUCTION
    print("Constructing CompEquIss signal...")
    
    # Sort by permno and time_avail_m
    df = df.sort_values(['permno', 'time_avail_m'])
    
    # Create cumulative index starting at 1, compounded with returns
    # tempIdx = 1 if _n == 1
    # tempIdx = (1 + ret) * l.tempIdx if _n > 1
    df['tempIdx'] = np.nan
    df.loc[df.groupby('permno').cumcount() == 0, 'tempIdx'] = 1
    
    # Create lagged tempIdx
    df['l_tempIdx'] = df.groupby('permno')['tempIdx'].shift(1)
    
    # Calculate tempIdx for subsequent observations
    mask = df.groupby('permno').cumcount() > 0
    df.loc[mask, 'tempIdx'] = (1 + df.loc[mask, 'ret']) * df.loc[mask, 'l_tempIdx']
    
    # Forward fill tempIdx within each permno
    df['tempIdx'] = df.groupby('permno')['tempIdx'].ffill()
    
    # Create 60-month lags
    df['l60_tempIdx'] = df.groupby('permno')['tempIdx'].shift(60)
    df['l60_mve_c'] = df.groupby('permno')['mve_c'].shift(60)
    
    # Calculate buy-and-hold return over 60 months
    # tempBH = (tempIdx - l60.tempIdx) / l60.tempIdx
    df['tempBH'] = np.where(
        df['l60_tempIdx'] == 0,
        np.nan,
        np.where(
            (df['tempIdx'] - df['l60_tempIdx']).isna() & df['l60_tempIdx'].isna(),
            1.0,
            (df['tempIdx'] - df['l60_tempIdx']) / df['l60_tempIdx']
        )
    )
    
    # Calculate composite equity issuance
    # CompEquIss = log(mve_c/l60.mve_c) - tempBH
    df['log_mve_ratio'] = np.where(
        df['l60_mve_c'] == 0,
        np.nan,
        np.where(
            (df['mve_c'] / df['l60_mve_c']).isna() & df['l60_mve_c'].isna(),
            1.0,
            np.log(df['mve_c'] / df['l60_mve_c'])
        )
    )
    
    df['CompEquIss'] = df['log_mve_ratio'] - df['tempBH']
    
    print(f"Generated CompEquIss values for {df['CompEquIss'].notna().sum():,} observations")
    
    # Clean up temporary columns
    df = df.drop(columns=['tempIdx', 'l_tempIdx', 'l60_tempIdx', 'l60_mve_c', 'tempBH', 'log_mve_ratio'])
    
    # SAVE
    print("Saving predictor...")
    save_predictor(df, 'CompEquIss')
    
    print("CompEquIss predictor completed successfully!")

if __name__ == "__main__":
    main()