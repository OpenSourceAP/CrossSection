# ABOUTME: BMdec predictor - calculates book-to-market using December market equity
# ABOUTME: Run: python3 pyCode/Predictors/BMdec.py

"""
BMdec Predictor

Book-to-market ratio using December market equity from prior year.

Inputs:
- m_aCompustat.parquet (permno, time_avail_m, txditc, seq, ceq, at, lt, pstk, pstkrv, pstkl)
- monthlyCRSP.parquet (permno, time_avail_m, prc, shrout)

Outputs:
- BMdec.csv (permno, yyyymm, BMdec)

This predictor calculates book-to-market ratio using book equity divided by
December market equity from the appropriate prior period (12 or 17 months ago
depending on the current month).
"""

import pandas as pd
import numpy as np
import sys
import os

# Add utils directory to path for imports
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'utils'))
from savepredictor import save_predictor

def main():
    print("Starting BMdec predictor...")
    
    # DATA LOAD
    print("Loading m_aCompustat data...")
    compustat_df = pd.read_parquet('../pyData/Intermediate/m_aCompustat.parquet', 
                                 columns=['permno', 'time_avail_m', 'txditc', 'seq', 'ceq', 
                                         'at', 'lt', 'pstk', 'pstkrv', 'pstkl'])
    
    print(f"Loaded {len(compustat_df):,} Compustat observations")
    
    # Deduplicate by permno time_avail_m (equivalent to bysort permno time_avail_m: keep if _n == 1)
    compustat_df = compustat_df.drop_duplicates(['permno', 'time_avail_m'], keep='first')
    print(f"After deduplication: {len(compustat_df):,} observations")
    
    print("Loading monthlyCRSP data...")
    crsp_df = pd.read_parquet('../pyData/Intermediate/monthlyCRSP.parquet', 
                             columns=['permno', 'time_avail_m', 'prc', 'shrout'])
    
    print(f"Loaded {len(crsp_df):,} CRSP observations")
    
    # Merge 1:1 permno time_avail_m (equivalent to merge 1:1 permno time_avail_m using monthlyCRSP, nogenerate keep(match))
    print("Merging Compustat and CRSP data...")
    df = pd.merge(compustat_df, crsp_df, on=['permno', 'time_avail_m'], how='inner')
    print(f"After merge: {len(df):,} observations")
    
    # SIGNAL CONSTRUCTION
    print("Constructing BMdec signal...")
    
    # Sort by permno and time_avail_m (equivalent to xtset permno time_avail_m)
    df = df.sort_values(['permno', 'time_avail_m'])
    
    # Extract month and year information
    df['month'] = df['time_avail_m'].dt.month
    df['year'] = df['time_avail_m'].dt.year
    
    # Calculate market equity for December only (equivalent to gen tempME = abs(prc)*shrout if month(dofm(time_avail_m)) == 12)
    df['tempME'] = np.where(df['month'] == 12, abs(df['prc']) * df['shrout'], np.nan)
    
    # Calculate December market equity by permno-year (equivalent to egen tempDecME = min(tempME), by(permno tempYear))
    # Note: using min() on a series with mostly NaN values returns the non-NaN value, which is what we want
    df['tempDecME'] = df.groupby(['permno', 'year'])['tempME'].transform('min')
    
    # Compute book equity following Stata logic
    # Step 1: Handle txditc (replace missing with 0)
    df['txditc'] = df['txditc'].fillna(0)
    
    # Step 2: Compute preferred stock (tempPS)
    df['tempPS'] = df['pstk'].copy()
    df['tempPS'] = df['tempPS'].fillna(df['pstkrv'])
    df['tempPS'] = df['tempPS'].fillna(df['pstkl'])
    
    # Step 3: Compute shareholders equity (tempSE)
    df['tempSE'] = df['seq'].copy()
    # If seq is missing, use ceq + tempPS
    mask_seq_missing = df['tempSE'].isna()
    df.loc[mask_seq_missing, 'tempSE'] = df.loc[mask_seq_missing, 'ceq'] + df.loc[mask_seq_missing, 'tempPS']
    # If still missing, use at - lt
    mask_still_missing = df['tempSE'].isna()
    df.loc[mask_still_missing, 'tempSE'] = df.loc[mask_still_missing, 'at'] - df.loc[mask_still_missing, 'lt']
    
    # Step 4: Compute book equity
    df['tempBE'] = df['tempSE'] + df['txditc'] - df['tempPS']
    
    # Create calendar-based lags for tempDecME (to match Stata l12/l17 behavior)
    # Stata's l12.var looks for value from 12 months ago in calendar time, not 12 positions back
    
    # Create lag dates for each observation
    df['lag12_date'] = df['time_avail_m'] - pd.DateOffset(months=12)
    df['lag17_date'] = df['time_avail_m'] - pd.DateOffset(months=17)
    
    # Create a lookup table for tempDecME values by permno and date
    lookup_df = df[['permno', 'time_avail_m', 'tempDecME']].copy()
    
    # Merge for 12-month lag
    lag12_merge = df[['permno', 'lag12_date']].merge(
        lookup_df, 
        left_on=['permno', 'lag12_date'], 
        right_on=['permno', 'time_avail_m'], 
        how='left',
        suffixes=('', '_lag12')
    )
    df['l12_tempDecME'] = lag12_merge['tempDecME']
    
    # Merge for 17-month lag
    lag17_merge = df[['permno', 'lag17_date']].merge(
        lookup_df,
        left_on=['permno', 'lag17_date'],
        right_on=['permno', 'time_avail_m'],
        how='left', 
        suffixes=('', '_lag17')
    )
    df['l17_tempDecME'] = lag17_merge['tempDecME']
    
    # Clean up temporary columns
    df = df.drop(columns=['lag12_date', 'lag17_date'])
    
    # Calculate BMdec based on month with domain-aware missing value handling
    # Following missing/missing = 1.0 pattern for division operations
    
    # For months >= 6: use l12.tempDecME
    # For months < 6: use l17.tempDecME
    
    # First calculate both potential ratios with missing/missing = 1.0 pattern
    df['bm_with_l12'] = np.where(
        df['l12_tempDecME'] == 0,
        np.nan,  # Division by zero = missing
        np.where(
            df['tempBE'].isna() & df['l12_tempDecME'].isna(),
            1.0,  # missing/missing = 1.0 (no change)
            df['tempBE'] / df['l12_tempDecME']
        )
    )
    
    df['bm_with_l17'] = np.where(
        df['l17_tempDecME'] == 0,
        np.nan,  # Division by zero = missing
        np.where(
            df['tempBE'].isna() & df['l17_tempDecME'].isna(),
            1.0,  # missing/missing = 1.0 (no change)
            df['tempBE'] / df['l17_tempDecME']
        )
    )
    
    # Now assign based on month
    df['BMdec'] = np.where(df['month'] >= 6, df['bm_with_l12'], df['bm_with_l17'])
    
    print(f"Generated BMdec values for {df['BMdec'].notna().sum():,} observations")
    
    # Clean up temporary columns (equivalent to drop temp*)
    temp_cols = [col for col in df.columns if col.startswith('temp') or col.startswith('bm_with')]
    df = df.drop(columns=temp_cols + ['month', 'year'])
    
    # SAVE
    print("Saving predictor...")
    save_predictor(df, 'BMdec')
    
    print("BMdec predictor completed successfully!")

if __name__ == "__main__":
    main()