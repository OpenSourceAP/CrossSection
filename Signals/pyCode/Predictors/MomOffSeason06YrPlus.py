# ABOUTME: Translates MomOffSeason06YrPlus predictor from Stata to Python
# ABOUTME: Creates off-season long-term reversal for years 6-10 by removing seasonal components

"""
MomOffSeason06YrPlus Predictor Translation

This script translates the Stata predictor MomOffSeason06YrPlus.do to Python.
The predictor calculates off-season momentum for years 6-10 by subtracting seasonal returns
from 60-month rolling momentum.

Usage:
    python3 Predictors/MomOffSeason06YrPlus.py
    
Input:
    - pyData/Intermediate/SignalMasterTable.parquet (columns: permno, time_avail_m, ret)
    
Output:
    - pyData/Predictors/MomOffSeason06YrPlus.csv (columns: permno, yyyymm, MomOffSeason06YrPlus)
"""

import pandas as pd
import numpy as np
import sys
import os

# Add parent directory to path for any shared utilities
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from utils.stata_asreg_asrol import asrol
from utils.stata_replication import stata_multi_lag

def main():
    print("Starting MomOffSeason06YrPlus predictor translation...")
    
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
    
    
    # Create seasonal lag variables using stata_multi_lag for calendar validation
    # This creates lags for seasonal returns from 6+ years ago: 71, 83, 95, 107, 119 months
    lag_periods = [71, 83, 95, 107, 119]
    print(f"Creating seasonal lags for periods: {lag_periods}")
    
    # Use stata_multi_lag for calendar-validated seasonal lags
    df = stata_multi_lag(df, 'permno', 'time_avail_m', 'ret', lag_periods)
    
    # Rename lag columns to match original temp variable names
    for n in lag_periods:
        df[f'temp{n}'] = df[f'ret_lag{n}']
    
    
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
    
    # Create retLagTemp = l60.ret using stata_multi_lag
    print("Creating retLagTemp (lag 60 months)...")
    df = stata_multi_lag(df, 'permno', 'time_avail_m', 'ret', [60])
    df['retLagTemp'] = df['ret_lag60']
    
    # Create 60-month rolling sum and count of retLagTemp using calendar-based approach
    print("Calculating 60-month calendar-based rolling sum and count...")
    df = df.sort_values(['permno', 'time_avail_m'])
    
    # Convert to yyyymm integer for efficient calendar arithmetic
    df['yyyymm'] = df['time_avail_m'].dt.year * 100 + df['time_avail_m'].dt.month
    
    def calculate_calendar_rolling_60m(group):
        group = group.sort_values('yyyymm').reset_index(drop=True)
        n_obs = len(group)
        sum_values = np.full(n_obs, np.nan)
        count_values = np.full(n_obs, np.nan)
        
        # Pre-compute all yyyymm values for efficient comparison
        yyyymm_values = group['yyyymm'].values
        retLagTemp_values = group['retLagTemp'].values
        
        for i in range(n_obs):
            current_yyyymm = yyyymm_values[i]
            
            # Calculate 60-month calendar window start (59 months back, including current)
            current_year = current_yyyymm // 100
            current_month = current_yyyymm % 100
            
            start_month = current_month - 59
            start_year = current_year
            while start_month <= 0:
                start_month += 12
                start_year -= 1
            
            window_start_yyyymm = start_year * 100 + start_month
            
            # Find observations in 60-month calendar window (including focal)
            window_mask = (
                (yyyymm_values >= window_start_yyyymm) & 
                (yyyymm_values <= current_yyyymm)
            )
            
            # Calculate sum and count (including NaN handling like Stata minimum(1))
            window_values = retLagTemp_values[window_mask]
            non_missing_values = window_values[~pd.isna(window_values)]
            
            if len(non_missing_values) >= 1:  # minimum(1) like in Stata
                sum_values[i] = np.sum(non_missing_values)
                count_values[i] = len(non_missing_values)
        
        group['retLagTemp_sum60'] = sum_values
        group['retLagTemp_count60'] = count_values
        return group
    
    print("Processing groups for calendar-based rolling (this may take time)...")
    df = df.groupby('permno', group_keys=False).apply(calculate_calendar_rolling_60m)
    
    print("Calculated 60-month rolling momentum base")
    
    
    # Calculate final predictor (equivalent to: gen MomOffSeason06YrPlus = (retLagTemp_sum60 - retTemp1)/(retLagTemp_count60 - retTemp2))
    df['MomOffSeason06YrPlus'] = (df['retLagTemp_sum60'] - df['retTemp1']) / (df['retLagTemp_count60'] - df['retTemp2'])
    # Handle division by zero - when denominator is 0, result should be NaN
    df.loc[(df['retLagTemp_count60'] - df['retTemp2']) == 0, 'MomOffSeason06YrPlus'] = np.nan
    print("Calculated MomOffSeason06YrPlus predictor")
    
    
    # yyyymm column already created in the rolling function above
    
    # SAVE - Keep only required output columns
    output_df = df[['permno', 'yyyymm', 'MomOffSeason06YrPlus']].copy()
    
    # Drop rows where predictor is missing (following Stata convention)
    output_df = output_df.dropna(subset=['MomOffSeason06YrPlus'])
    
    # Save to CSV
    output_path = '../pyData/Predictors/MomOffSeason06YrPlus.csv'
    output_df.to_csv(output_path, index=False)
    print(f"Saved {len(output_df)} observations to {output_path}")
    
    print("MomOffSeason06YrPlus predictor translation completed successfully!")

if __name__ == "__main__":
    main()