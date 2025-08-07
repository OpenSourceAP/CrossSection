# ABOUTME: CredRatDG predictor - calculates credit rating downgrade signal
# ABOUTME: Run: python3 pyCode/Predictors/CredRatDG.py

"""
CredRatDG Predictor

Credit rating downgrade signal using both Compustat and CIQ data.

Inputs:
- m_SP_creditratings.parquet (gvkey, time_avail_m, credrat)
- m_CIQ_creditratings.parquet (gvkey, time_avail_m, ratingaction)
- SignalMasterTable.parquet (gvkey, permno, time_avail_m)

Outputs:
- CredRatDG.csv (permno, yyyymm, CredRatDG)

This predictor calculates:
1. Credit rating downgrade from Compustat (credrat < l.credrat)
2. Credit rating downgrade from CIQ (ratingaction == "Downgrade")
3. Signal = 1 if any downgrade in current or previous 5 months
4. Excludes data before 1979
"""

import pandas as pd
import numpy as np
import sys
import os

# Add utils directory to path for imports
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'utils'))
from savepredictor import save_predictor

def main():
    print("Starting CredRatDG predictor...")
    
    # Process Compustat SP ratings data
    print("Loading m_SP_creditratings data...")
    comp_df = pd.read_parquet('../pyData/Intermediate/m_SP_creditratings.parquet', 
                             columns=['gvkey', 'time_avail_m', 'credrat'])
    
    print(f"Loaded {len(comp_df):,} Compustat ratings observations")
    
    # Sort by gvkey and time_avail_m
    comp_df = comp_df.sort_values(['gvkey', 'time_avail_m'])
    
    # Create lag of credrat
    comp_df['l_credrat'] = comp_df.groupby('gvkey')['credrat'].shift(1)
    
    # Generate downgrade signal: credrat_dwn = 1 if credrat - l.credrat < 0
    comp_df['credrat_dwn'] = np.where(
        comp_df['credrat'] - comp_df['l_credrat'] < 0, 
        1, 
        np.nan
    )
    
    # Set first observation per gvkey to missing
    comp_df.loc[comp_df.groupby('gvkey').cumcount() == 0, 'credrat_dwn'] = np.nan
    
    # Keep only required columns
    comp_df = comp_df[['gvkey', 'time_avail_m', 'credrat_dwn']].copy()
    
    print(f"Generated {comp_df['credrat_dwn'].notna().sum():,} Compustat downgrade signals")
    
    # Process CIQ SP ratings data
    print("Loading m_CIQ_creditratings data...")
    ciq_raw = pd.read_parquet('../pyData/Intermediate/m_CIQ_creditratings.parquet', 
                             columns=['gvkey', 'ratingdate', 'anydowngrade'])
    
    print(f"Loaded {len(ciq_raw):,} CIQ ratings observations")
    
    # Keep only downgrades and non-missing gvkey
    ciq_raw = ciq_raw[ciq_raw['gvkey'].notna() & (ciq_raw['anydowngrade'] == 1)]
    
    print(f"Filtered to {len(ciq_raw):,} CIQ downgrade observations")
    
    # Expand each rating to be valid for 12 months after ratingdate
    from dateutil.relativedelta import relativedelta
    expanded_records = []
    
    for _, row in ciq_raw.iterrows():
        base_date = pd.to_datetime(row['ratingdate'])
        for months_offset in range(12):
            time_avail_m = (base_date + relativedelta(months=months_offset)).replace(day=1)
            expanded_records.append({
                'gvkey': float(row['gvkey']),  # Ensure gvkey is float to match SignalMasterTable
                'time_avail_m': time_avail_m,
                'ciq_dg': 1
            })
    
    ciq_df = pd.DataFrame(expanded_records)
    
    # Handle duplicates within month by looking for any downgrades
    ciq_df = ciq_df.groupby(['gvkey', 'time_avail_m'])['ciq_dg'].max().reset_index()
    
    print(f"Generated {len(ciq_df):,} CIQ downgrade signals")
    
    # Load SignalMasterTable
    print("Loading SignalMasterTable...")
    signal_master = pd.read_parquet('../pyData/Intermediate/SignalMasterTable.parquet', 
                                   columns=['gvkey', 'permno', 'time_avail_m'])
    
    # Drop observations with missing gvkey
    signal_master = signal_master[signal_master['gvkey'].notna()]
    
    print(f"Loaded {len(signal_master):,} SignalMasterTable observations")
    
    # Merge data
    print("Merging data...")
    df = pd.merge(signal_master, comp_df, on=['gvkey', 'time_avail_m'], how='left')
    df = pd.merge(df, ciq_df, on=['gvkey', 'time_avail_m'], how='left')
    
    # Use CIQ if Compustat data is missing
    df['credrat_dwn'] = df['credrat_dwn'].fillna(df['ciq_dg'])
    
    print(f"After merging: {len(df):,} observations")
    
    # SIGNAL CONSTRUCTION
    print("Constructing CredRatDG signal...")
    
    # Sort by permno and time_avail_m
    df = df.sort_values(['permno', 'time_avail_m'])
    
    # Create lags for credrat_dwn
    for i in range(1, 6):
        df[f'l{i}_credrat_dwn'] = df.groupby('permno')['credrat_dwn'].shift(i)
    
    # Generate CredRatDG signal
    # CredRatDG = 1 if (credrat_dwn == 1 | l.credrat_dwn == 1 | l2.credrat_dwn == 1 | l3.credrat_dwn == 1 | l4.credrat_dwn == 1 | l5.credrat_dwn == 1)
    df['CredRatDG'] = 0
    
    # Check for any downgrade in current or previous 5 months
    downgrade_mask = (
        (df['credrat_dwn'] == 1) |
        (df['l1_credrat_dwn'] == 1) |
        (df['l2_credrat_dwn'] == 1) |
        (df['l3_credrat_dwn'] == 1) |
        (df['l4_credrat_dwn'] == 1) |
        (df['l5_credrat_dwn'] == 1)
    )
    
    df.loc[downgrade_mask, 'CredRatDG'] = 1
    
    # Exclude data before 1979
    # gen year = yofd(dofm(time_avail_m))
    # replace CredRatDG = . if year < 1979
    df['year'] = df['time_avail_m'].dt.year
    df.loc[df['year'] < 1979, 'CredRatDG'] = np.nan
    
    print(f"Generated CredRatDG values for {df['CredRatDG'].notna().sum():,} observations")
    
    # Clean up temporary columns
    lag_cols = [f'l{i}_credrat_dwn' for i in range(1, 6)]
    df = df.drop(columns=['credrat_dwn', 'ciq_dg', 'year'] + lag_cols)
    
    # SAVE
    print("Saving predictor...")
    save_predictor(df, 'CredRatDG')
    
    print("CredRatDG predictor completed successfully!")

if __name__ == "__main__":
    main()