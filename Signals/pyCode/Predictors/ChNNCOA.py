# ABOUTME: ChNNCOA predictor - calculates change in net noncurrent operating assets
# ABOUTME: Run: python3 pyCode/Predictors/ChNNCOA.py

"""
ChNNCOA Predictor

Change in net noncurrent operating assets calculation.

Inputs:
- m_aCompustat.parquet (gvkey, permno, time_avail_m, at, act, ivao, lt, dlc, dltt)

Outputs:
- ChNNCOA.csv (permno, yyyymm, ChNNCOA)

This predictor calculates:
1. Net noncurrent operating assets: ((at - act - ivao) - (lt - dlc - dltt)) / at
2. Change over 12 months: current_ratio - l12.current_ratio
"""

import pandas as pd
import numpy as np
import sys
import os

# Add utils directory to path for imports
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'utils'))
from savepredictor import save_predictor

def main():
    print("Starting ChNNCOA predictor...")
    
    # DATA LOAD
    print("Loading m_aCompustat data...")
    df = pd.read_parquet('../pyData/Intermediate/m_aCompustat.parquet', 
                        columns=['gvkey', 'permno', 'time_avail_m', 'at', 'act', 'ivao', 'lt', 'dlc', 'dltt'])
    
    print(f"Loaded {len(df):,} Compustat observations")
    
    # SIGNAL CONSTRUCTION
    print("Constructing ChNNCOA signal...")
    
    # Deduplicate by permno time_avail_m
    df = df.drop_duplicates(['permno', 'time_avail_m'], keep='first')
    print(f"After deduplication: {len(df):,} observations")
    
    # Sort by permno and time_avail_m
    df = df.sort_values(['permno', 'time_avail_m'])
    
    # Calculate net noncurrent operating assets ratio
    # temp = ((at - act - ivao) - (lt - dlc - dltt)) / at
    df['temp'] = np.where(
        df['at'] == 0,
        np.nan,
        np.where(
            ((df['at'] - df['act'] - df['ivao']) - (df['lt'] - df['dlc'] - df['dltt'])).isna() & df['at'].isna(),
            1.0,
            ((df['at'] - df['act'] - df['ivao']) - (df['lt'] - df['dlc'] - df['dltt'])) / df['at']
        )
    )
    
    # Create 12-month lag
    df['l12_temp'] = df.groupby('permno')['temp'].shift(12)
    
    # Calculate change over 12 months
    df['ChNNCOA'] = df['temp'] - df['l12_temp']
    
    print(f"Generated ChNNCOA values for {df['ChNNCOA'].notna().sum():,} observations")
    
    # Clean up temporary columns
    df = df.drop(columns=['temp', 'l12_temp'])
    
    # SAVE
    print("Saving predictor...")
    save_predictor(df, 'ChNNCOA')
    
    print("ChNNCOA predictor completed successfully!")

if __name__ == "__main__":
    main()