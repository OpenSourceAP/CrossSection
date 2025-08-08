# ABOUTME: Translates MomSeason06YrPlus predictor from Stata to Python
# ABOUTME: Creates seasonal momentum predictor using 6-10 year past returns

"""
MomSeason06YrPlus Predictor Translation

This script translates the Stata predictor MomSeason06YrPlus.do to Python.
The predictor calculates seasonal momentum using returns from 6-10 years ago
in the same calendar months.

Usage:
    python3 Predictors/MomSeason06YrPlus.py
    
Input:
    - pyData/Intermediate/SignalMasterTable.parquet (columns: permno, time_avail_m, ret)
    
Output:
    - pyData/Predictors/MomSeason06YrPlus.csv (columns: permno, yyyymm, MomSeason06YrPlus)
"""

import pandas as pd
import numpy as np
import sys
import os

# Add parent directory to path for any shared utilities
sys.path.append('..')

def main():
    print("Starting MomSeason06YrPlus predictor translation...")
    
    # DATA LOAD
    print("Loading SignalMasterTable...")
    df = pd.read_parquet('../pyData/Intermediate/SignalMasterTable.parquet')
    
    # Keep only required columns: permno, time_avail_m, ret
    df = df[['permno', 'time_avail_m', 'ret']].copy()
    print(f"Loaded {len(df)} observations")
    
    # Sort data by permno and time_avail_m (equivalent to xtset)
    df = df.sort_values(['permno', 'time_avail_m'])
    print("Data sorted by permno and time_avail_m")
    
    # SIGNAL CONSTRUCTION
    print("Starting signal construction...")
    
    # Replace missing returns with 0 (equivalent to: replace ret = 0 if mi(ret))
    df['ret'] = df['ret'].fillna(0)
    print("Replaced missing returns with 0")
    
    # Create temporary variables for lags 71, 83, 95, 107, 119 months
    # foreach n of numlist 71(12)120 creates: 71, 83, 95, 107, 119
    # This creates lags for seasonal returns from 6+ years ago
    lag_periods = list(range(71, 121, 12))  # 71, 83, 95, 107, 119
    print(f"Creating lags for periods: {lag_periods}")
    
    # Create time-based lag variables (equivalent to: gen temp`n' = l`n'.ret)
    # Stata lags are time-based, not position-based
    print("Creating time-based lags...")
    
    for n in lag_periods:
        print(f"Creating temp{n} (lag {n} months)...")
        # Create a lagged time column
        df[f'lag_time_{n}'] = df['time_avail_m'] - pd.DateOffset(months=n)
        
        # Create a helper dataframe for the lag merge
        lag_data = df[['permno', 'time_avail_m', 'ret']].copy()
        lag_data.columns = ['permno', f'lag_time_{n}', f'temp{n}']
        
        # Merge to get the lagged values
        df = df.merge(lag_data, on=['permno', f'lag_time_{n}'], how='left')
        
        # Clean up the temporary time column
        df = df.drop(f'lag_time_{n}', axis=1)
    
    # Create list of temporary variable names for row operations
    temp_vars = [f'temp{n}' for n in lag_periods]
    
    # Calculate row total (equivalent to: egen retTemp1 = rowtotal(temp*), missing)
    # The 'missing' option means if all values are missing, return missing (not 0)
    df['retTemp1'] = df[temp_vars].sum(axis=1)
    # Handle case where all values are NaN - should return NaN, not 0
    all_missing = df[temp_vars].isna().all(axis=1)
    df.loc[all_missing, 'retTemp1'] = np.nan
    print("Calculated retTemp1 (row total)")
    
    # Calculate count of non-missing values (equivalent to: egen retTemp2 = rownonmiss(temp*))
    df['retTemp2'] = df[temp_vars].notna().sum(axis=1)
    print("Calculated retTemp2 (row non-missing count)")
    
    # Calculate final predictor (equivalent to: gen MomSeason06YrPlus = retTemp1/retTemp2)
    df['MomSeason06YrPlus'] = df['retTemp1'] / df['retTemp2']
    # Handle division by zero - when retTemp2 is 0, result should be NaN
    df.loc[df['retTemp2'] == 0, 'MomSeason06YrPlus'] = np.nan
    print("Calculated MomSeason06YrPlus predictor")
    
    # Create yyyymm column from time_avail_m 
    # Convert datetime to yyyymm integer format (e.g. 199112 for Dec 1991)
    df['yyyymm'] = (df['time_avail_m'].dt.year * 100 + df['time_avail_m'].dt.month).astype(int)
    
    # SAVE - Keep only required output columns
    output_df = df[['permno', 'yyyymm', 'MomSeason06YrPlus']].copy()
    
    # Drop rows where predictor is missing (following Stata convention)
    output_df = output_df.dropna(subset=['MomSeason06YrPlus'])
    
    # Save to CSV
    output_path = '../pyData/Predictors/MomSeason06YrPlus.csv'
    output_df.to_csv(output_path, index=False)
    print(f"Saved {len(output_df)} observations to {output_path}")
    
    print("MomSeason06YrPlus predictor translation completed successfully!")

if __name__ == "__main__":
    main()