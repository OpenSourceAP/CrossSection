# ABOUTME: Translates Mom12mOffSeason predictor from Stata to Python
# ABOUTME: Creates 12-month momentum excluding focal (most recent) return

"""
Mom12mOffSeason Predictor Translation

This script translates the Stata predictor Mom12mOffSeason.do to Python.
Calculates 10-month rolling mean excluding the focal (most recent) return.

Usage:
    python3 Predictors/Mom12mOffSeason.py
    
Input:
    - pyData/Intermediate/SignalMasterTable.parquet (columns: permno, time_avail_m, ret)
    
Output:
    - pyData/Predictors/Mom12mOffSeason.csv (columns: permno, yyyymm, Mom12mOffSeason)
"""

import pandas as pd
import numpy as np
import os

def main():
    print("Starting Mom12mOffSeason predictor translation...")
    
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

    
    # Calculate 10-month calendar-based rolling statistics
    # Need to exclude focal (current) observation from the rolling calculation
    print("Computing 10-month calendar-based rolling statistics excluding focal return...")
    
    # Import relativedelta for calendar-based calculations
    from dateutil.relativedelta import relativedelta
    
    # Implement true calendar-based rolling to exactly match Stata asrol
    # This will be slow but is necessary for correct results
    print("Computing true calendar-based rolling statistics (this may take several minutes)...")
    
    # Convert to yyyymm integer for efficient calendar arithmetic
    df['yyyymm'] = df['time_avail_m'].dt.year * 100 + df['time_avail_m'].dt.month
    
    def calculate_calendar_rolling_fast(group):
        group = group.sort_values('yyyymm').reset_index(drop=True)
        n_obs = len(group)
        mom_values = np.full(n_obs, np.nan)
        
        # Pre-compute all yyyymm values for efficient comparison
        yyyymm_values = group['yyyymm'].values
        ret_values = group['ret'].values
        
        for i in range(n_obs):
            current_yyyymm = yyyymm_values[i]
            
            # Calculate 10-month calendar window start (9 months back)
            current_year = current_yyyymm // 100
            current_month = current_yyyymm % 100
            
            start_month = current_month - 9
            start_year = current_year
            while start_month <= 0:
                start_month += 12
                start_year -= 1
            
            window_start_yyyymm = start_year * 100 + start_month
            
            # Find observations in calendar window, excluding focal
            window_mask = (
                (yyyymm_values >= window_start_yyyymm) & 
                (yyyymm_values <= current_yyyymm) &
                (yyyymm_values != current_yyyymm)
            )
            
            # Calculate mean if minimum 6 observations
            window_returns = ret_values[window_mask]
            if len(window_returns) >= 6:
                mom_values[i] = np.mean(window_returns)
        
        group['Mom12mOffSeason'] = mom_values
        return group[['permno', 'time_avail_m', 'ret', 'Mom12mOffSeason']]
    
    print("Processing groups (this will take time for large dataset)...")
    df = df.groupby('permno', group_keys=False).apply(calculate_calendar_rolling_fast)

    
    # Keep only observations with valid Mom12mOffSeason values
    df_final = df.dropna(subset=['Mom12mOffSeason']).copy()
    print(f"Generated {len(df_final)} valid Mom12mOffSeason observations")

    # SAVE
    print("Preparing output...")
    
    # Convert time_avail_m to yyyymm format (equivalent to Stata date conversion)
    df_final['yyyymm'] = df_final['time_avail_m'].dt.year * 100 + df_final['time_avail_m'].dt.month
    
    # Keep only required columns and ensure correct order
    df_output = df_final[['permno', 'yyyymm', 'Mom12mOffSeason']].copy()
    
    # Convert to integers for consistency
    df_output['permno'] = df_output['permno'].astype('int64')
    df_output['yyyymm'] = df_output['yyyymm'].astype('int64')

    
    # Save to CSV
    output_path = '../pyData/Predictors/Mom12mOffSeason.csv'
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    df_output.to_csv(output_path, index=False)
    
    print(f"Mom12mOffSeason predictor saved to {output_path}")
    print(f"Output shape: {df_output.shape}")
    print("Summary statistics:")
    print(f"  Mean: {df_output['Mom12mOffSeason'].mean():.6f}")
    print(f"  Std: {df_output['Mom12mOffSeason'].std():.6f}")
    print(f"  Min: {df_output['Mom12mOffSeason'].min():.6f}")
    print(f"  Max: {df_output['Mom12mOffSeason'].max():.6f}")
    
if __name__ == '__main__':
    main()