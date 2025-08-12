# ABOUTME: Translates MomOffSeason predictor from Stata to Python
# ABOUTME: Creates off-season long-term reversal by removing seasonal components

"""
MomOffSeason Predictor Translation

This script translates the Stata predictor MomOffSeason.do to Python.
The predictor calculates off-season momentum by subtracting seasonal returns
from 48-month rolling momentum.

Usage:
    python3 Predictors/MomOffSeason.py
    
Input:
    - pyData/Intermediate/SignalMasterTable.parquet (columns: permno, time_avail_m, ret)
    
Output:
    - pyData/Predictors/MomOffSeason.csv (columns: permno, yyyymm, MomOffSeason)
"""

import pandas as pd
import numpy as np
import sys
import os

# Add parent directory to path for any shared utilities
sys.path.append('..')

def main():
    print("Starting MomOffSeason predictor translation...")
    
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
    
    # Create seasonal lag variables (equivalent to: foreach n of numlist 23(12)59)
    # This creates lags for seasonal returns: 23, 35, 47, 59 months
    lag_periods = list(range(23, 60, 12))  # 23, 35, 47, 59
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
    
    # Calculate momentum base using 48-month rolling window
    print("Creating momentum base with 48-month rolling window...")
    
    # Create retLagTemp = l12.ret (12-month lagged returns)
    print("Creating retLagTemp (lag 12 months)...")
    df['lag_time_12'] = df['time_avail_m'] - pd.DateOffset(months=12)
    lag_data_12 = df[['permno', 'time_avail_m', 'ret']].copy()
    lag_data_12.columns = ['permno', 'lag_time_12', 'retLagTemp']
    df = df.merge(lag_data_12, on=['permno', 'lag_time_12'], how='left')
    df = df.drop('lag_time_12', axis=1)
    
    # Create 48-month rolling sum and count of retLagTemp (equivalent to asrol)
    print("Calculating 48-month rolling sum and count...")
    df = df.sort_values(['permno', 'time_avail_m'])
    
    # Use position-based rolling as approximation (since data is monthly, 48 positions ≈ 48 months)
    # This matches the approach used in working predictors
    df['retLagTemp_sum48'] = df.groupby('permno')['retLagTemp'].transform(
        lambda x: x.rolling(window=48, min_periods=1).sum()
    )
    
    df['retLagTemp_count48'] = df.groupby('permno')['retLagTemp'].transform(
        lambda x: x.notna().rolling(window=48, min_periods=1).sum()
    )
    
    print("Calculated 48-month rolling momentum base")
    
    # Calculate final predictor (equivalent to: gen MomOffSeason = (retLagTemp_sum48 - retTemp1)/(retLagTemp_count48 - retTemp2))
    df['MomOffSeason'] = (df['retLagTemp_sum48'] - df['retTemp1']) / (df['retLagTemp_count48'] - df['retTemp2'])
    # Handle division by zero - when denominator is 0, result should be NaN
    df.loc[(df['retLagTemp_count48'] - df['retTemp2']) == 0, 'MomOffSeason'] = np.nan
    print("Calculated MomOffSeason predictor")
    
    # Create yyyymm column from time_avail_m 
    # Convert datetime to yyyymm integer format (e.g. 199112 for Dec 1991)
    df['yyyymm'] = (df['time_avail_m'].dt.year * 100 + df['time_avail_m'].dt.month).astype(int)
    
    # SAVE - Keep only required output columns
    output_df = df[['permno', 'yyyymm', 'MomOffSeason']].copy()
    
    # Drop rows where predictor is missing (following Stata convention)
    output_df = output_df.dropna(subset=['MomOffSeason'])
    
    # Save to CSV
    output_path = '../pyData/Predictors/MomOffSeason.csv'
    output_df.to_csv(output_path, index=False)
    print(f"Saved {len(output_df)} observations to {output_path}")
    
    print("MomOffSeason predictor translation completed successfully!")

if __name__ == "__main__":
    main()