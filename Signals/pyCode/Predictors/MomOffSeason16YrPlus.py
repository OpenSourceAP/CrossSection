# ABOUTME: Translates MomOffSeason16YrPlus predictor from Stata to Python
# ABOUTME: Creates off-season long-term reversal for years 16-20 by removing seasonal components

"""
MomOffSeason16YrPlus Predictor Translation

This script translates the Stata predictor MomOffSeason16YrPlus.do to Python.
The predictor calculates off-season momentum for years 16-20 by subtracting seasonal returns
from 60-month rolling momentum, with a minimum requirement of 36 observations.

Usage:
    python3 Predictors/MomOffSeason16YrPlus.py
    
Input:
    - pyData/Intermediate/SignalMasterTable.parquet (columns: permno, time_avail_m, ret)
    
Output:
    - pyData/Predictors/MomOffSeason16YrPlus.csv (columns: permno, yyyymm, MomOffSeason16YrPlus)
"""

import pandas as pd
import numpy as np
import sys
import os

# Add parent directory to path for any shared utilities
sys.path.append('..')
from utils.asrol import asrol

def main():
    print("Starting MomOffSeason16YrPlus predictor translation...")
    
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
    
    # Create seasonal lag variables (equivalent to: foreach n of numlist 191(12)239)
    # This creates lags for seasonal returns from years 16-20: 191, 203, 215, 227, 239 months
    lag_periods = list(range(191, 240, 12))  # 191, 203, 215, 227, 239
    print(f"Creating seasonal lags for periods: {lag_periods}")
    
    # Create time-based lag variables (equivalent to: gen temp`n' = l`n'.ret)
    # Stata lags are time-based, not position-based
    print("Creating time-based seasonal lags...")
    
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
    
    # Calculate seasonal row total (equivalent to: egen retTemp1 = rowtotal(temp*), missing)
    # The 'missing' option means if all values are missing, return missing (not 0)
    df['retTemp1'] = df[temp_vars].sum(axis=1)
    # Handle case where all values are NaN - should return NaN, not 0
    all_missing = df[temp_vars].isna().all(axis=1)
    df.loc[all_missing, 'retTemp1'] = np.nan
    print("Calculated retTemp1 (seasonal row total)")
    
    # Calculate count of non-missing seasonal values (equivalent to: egen retTemp2 = rownonmiss(temp*))
    df['retTemp2'] = df[temp_vars].notna().sum(axis=1)
    print("Calculated retTemp2 (seasonal row non-missing count)")
    
    # Calculate momentum base using 60-month rolling window
    print("Creating momentum base with 60-month rolling window...")
    
    # Create retLagTemp = l180.ret (180-month lagged returns, i.e., 15 years ago)
    print("Creating retLagTemp (lag 180 months)...")
    df['lag_time_180'] = df['time_avail_m'] - pd.DateOffset(months=180)
    lag_data_180 = df[['permno', 'time_avail_m', 'ret']].copy()
    lag_data_180.columns = ['permno', 'lag_time_180', 'retLagTemp']
    df = df.merge(lag_data_180, on=['permno', 'lag_time_180'], how='left')
    df = df.drop('lag_time_180', axis=1)
    
    # Create 60-month rolling sum and count of retLagTemp (equivalent to asrol)
    # Note: This variant requires minimum 36 observations (vs 1 in other variants)
    print("Calculating 60-month rolling sum and count (minimum 36 observations)...")
    df = df.sort_values(['permno', 'time_avail_m'])
    
    # Use asrol for 60-month rolling sum and count with minimum 36 periods
    df = asrol(df, 'permno', 'time_avail_m', 'retLagTemp', 60, stat='sum', new_col_name='sum60_retLagTemp', min_periods=36)
    df = asrol(df, 'permno', 'time_avail_m', 'retLagTemp', 60, stat='count', new_col_name='count60_retLagTemp', min_periods=36)
    
    print("Calculated 60-month rolling momentum base")
    
    # Calculate final predictor (equivalent to: gen MomOffSeason16YrPlus = (sum60_retLagTemp - retTemp1)/(count60_retLagTemp - retTemp2))
    df['MomOffSeason16YrPlus'] = (df['sum60_retLagTemp'] - df['retTemp1']) / (df['count60_retLagTemp'] - df['retTemp2'])
    # Handle division by zero - when denominator is 0, result should be NaN
    df.loc[(df['count60_retLagTemp'] - df['retTemp2']) == 0, 'MomOffSeason16YrPlus'] = np.nan
    print("Calculated MomOffSeason16YrPlus predictor")
    
    # Create yyyymm column from time_avail_m 
    # Convert datetime to yyyymm integer format (e.g. 199112 for Dec 1991)
    df['yyyymm'] = (df['time_avail_m'].dt.year * 100 + df['time_avail_m'].dt.month).astype(int)
    
    # SAVE - Keep only required output columns
    output_df = df[['permno', 'yyyymm', 'MomOffSeason16YrPlus']].copy()
    
    # Drop rows where predictor is missing (following Stata convention)
    output_df = output_df.dropna(subset=['MomOffSeason16YrPlus'])
    
    # Save to CSV
    output_path = '../pyData/Predictors/MomOffSeason16YrPlus.csv'
    output_df.to_csv(output_path, index=False)
    print(f"Saved {len(output_df)} observations to {output_path}")
    
    print("MomOffSeason16YrPlus predictor translation completed successfully!")

if __name__ == "__main__":
    main()