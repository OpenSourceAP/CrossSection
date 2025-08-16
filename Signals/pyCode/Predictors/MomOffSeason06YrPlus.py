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
from utils.asrol import asrol

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
    
    # CHECKPOINT 1: After ret replacement
    print("CHECKPOINT 1: After ret replacement")
    bad_obs_1 = df[(df['permno'] == 83382) & (df['time_avail_m'] == pd.Period('2005-10', freq='M'))]
    bad_obs_2 = df[(df['permno'] == 33268) & (df['time_avail_m'] == pd.Period('1983-11', freq='M'))]
    if not bad_obs_1.empty:
        print(f"permno=83382, time_avail_m=2005-10: ret={bad_obs_1['ret'].iloc[0]}")
    if not bad_obs_2.empty:
        print(f"permno=33268, time_avail_m=1983-11: ret={bad_obs_2['ret'].iloc[0]}")
    
    # Create seasonal lag variables (equivalent to: foreach n of numlist 71(12)119)
    # This creates lags for seasonal returns from 6+ years ago: 71, 83, 95, 107, 119 months
    lag_periods = list(range(71, 120, 12))  # 71, 83, 95, 107, 119
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
    
    # CHECKPOINT 2: After seasonal lag creation
    print("CHECKPOINT 2: After seasonal lag creation")
    temp_vars = [f'temp{n}' for n in lag_periods]
    bad_obs_1 = df[(df['permno'] == 83382) & (df['time_avail_m'] == pd.Period('2005-10', freq='M'))]
    bad_obs_2 = df[(df['permno'] == 33268) & (df['time_avail_m'] == pd.Period('1983-11', freq='M'))]
    if not bad_obs_1.empty:
        temp_vals_1 = [str(bad_obs_1[var].iloc[0]) if var in bad_obs_1.columns else 'NaN' for var in temp_vars]
        print(f"permno=83382, time_avail_m=2005-10: temp71={temp_vals_1[0]}, temp83={temp_vals_1[1]}, temp95={temp_vals_1[2]}, temp107={temp_vals_1[3]}, temp119={temp_vals_1[4]}")
    if not bad_obs_2.empty:
        temp_vals_2 = [str(bad_obs_2[var].iloc[0]) if var in bad_obs_2.columns else 'NaN' for var in temp_vars]
        print(f"permno=33268, time_avail_m=1983-11: temp71={temp_vals_2[0]}, temp83={temp_vals_2[1]}, temp95={temp_vals_2[2]}, temp107={temp_vals_2[3]}, temp119={temp_vals_2[4]}")
    
    # Create list of temporary variable names for row operations
    
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
    
    # CHECKPOINT 3: After seasonal aggregation
    print("CHECKPOINT 3: After seasonal aggregation")
    bad_obs_1 = df[(df['permno'] == 83382) & (df['time_avail_m'] == pd.Period('2005-10', freq='M'))]
    bad_obs_2 = df[(df['permno'] == 33268) & (df['time_avail_m'] == pd.Period('1983-11', freq='M'))]
    if not bad_obs_1.empty:
        print(f"permno=83382, time_avail_m=2005-10: retTemp1={bad_obs_1['retTemp1'].iloc[0]}, retTemp2={bad_obs_1['retTemp2'].iloc[0]}")
    if not bad_obs_2.empty:
        print(f"permno=33268, time_avail_m=1983-11: retTemp1={bad_obs_2['retTemp1'].iloc[0]}, retTemp2={bad_obs_2['retTemp2'].iloc[0]}")
    
    # Calculate momentum base using 60-month rolling window
    print("Creating momentum base with 60-month rolling window...")
    
    # Create retLagTemp = l60.ret (60-month lagged returns)
    print("Creating retLagTemp (lag 60 months)...")
    df['lag_time_60'] = df['time_avail_m'] - pd.DateOffset(months=60)
    lag_data_60 = df[['permno', 'time_avail_m', 'ret']].copy()
    lag_data_60.columns = ['permno', 'lag_time_60', 'retLagTemp']
    df = df.merge(lag_data_60, on=['permno', 'lag_time_60'], how='left')
    df = df.drop('lag_time_60', axis=1)
    
    # Create 60-month rolling sum and count of retLagTemp (equivalent to asrol)
    print("Calculating 60-month rolling sum and count...")
    df = df.sort_values(['permno', 'time_avail_m'])
    
    # Use asrol for 60-month rolling sum and count
    df = asrol(df, 'permno', 'time_avail_m', 'retLagTemp', 60, stat='sum', new_col_name='retLagTemp_sum60', min_periods=1)
    df = asrol(df, 'permno', 'time_avail_m', 'retLagTemp', 60, stat='count', new_col_name='retLagTemp_count60', min_periods=1)
    
    print("Calculated 60-month rolling momentum base")
    
    # CHECKPOINT 4: After rolling momentum calculation
    print("CHECKPOINT 4: After rolling momentum calculation")
    bad_obs_1 = df[(df['permno'] == 83382) & (df['time_avail_m'] == pd.Period('2005-10', freq='M'))]
    bad_obs_2 = df[(df['permno'] == 33268) & (df['time_avail_m'] == pd.Period('1983-11', freq='M'))]
    if not bad_obs_1.empty:
        print(f"permno=83382, time_avail_m=2005-10: retLagTemp={bad_obs_1['retLagTemp'].iloc[0]}, retLagTemp_sum60={bad_obs_1['retLagTemp_sum60'].iloc[0]}, retLagTemp_count60={bad_obs_1['retLagTemp_count60'].iloc[0]}")
    if not bad_obs_2.empty:
        print(f"permno=33268, time_avail_m=1983-11: retLagTemp={bad_obs_2['retLagTemp'].iloc[0]}, retLagTemp_sum60={bad_obs_2['retLagTemp_sum60'].iloc[0]}, retLagTemp_count60={bad_obs_2['retLagTemp_count60'].iloc[0]}")
    
    # Calculate final predictor (equivalent to: gen MomOffSeason06YrPlus = (retLagTemp_sum60 - retTemp1)/(retLagTemp_count60 - retTemp2))
    df['MomOffSeason06YrPlus'] = (df['retLagTemp_sum60'] - df['retTemp1']) / (df['retLagTemp_count60'] - df['retTemp2'])
    # Handle division by zero - when denominator is 0, result should be NaN
    df.loc[(df['retLagTemp_count60'] - df['retTemp2']) == 0, 'MomOffSeason06YrPlus'] = np.nan
    print("Calculated MomOffSeason06YrPlus predictor")
    
    # CHECKPOINT 5: After final calculation
    print("CHECKPOINT 5: After final calculation")
    bad_obs_1 = df[(df['permno'] == 83382) & (df['time_avail_m'] == pd.Period('2005-10', freq='M'))]
    bad_obs_2 = df[(df['permno'] == 33268) & (df['time_avail_m'] == pd.Period('1983-11', freq='M'))]
    if not bad_obs_1.empty:
        print(f"permno=83382, time_avail_m=2005-10: MomOffSeason06YrPlus={bad_obs_1['MomOffSeason06YrPlus'].iloc[0]}, retLagTemp_sum60={bad_obs_1['retLagTemp_sum60'].iloc[0]}, retTemp1={bad_obs_1['retTemp1'].iloc[0]}, retLagTemp_count60={bad_obs_1['retLagTemp_count60'].iloc[0]}, retTemp2={bad_obs_1['retTemp2'].iloc[0]}")
    if not bad_obs_2.empty:
        print(f"permno=33268, time_avail_m=1983-11: MomOffSeason06YrPlus={bad_obs_2['MomOffSeason06YrPlus'].iloc[0]}, retLagTemp_sum60={bad_obs_2['retLagTemp_sum60'].iloc[0]}, retTemp1={bad_obs_2['retTemp1'].iloc[0]}, retLagTemp_count60={bad_obs_2['retLagTemp_count60'].iloc[0]}, retTemp2={bad_obs_2['retTemp2'].iloc[0]}")
    
    # Create yyyymm column from time_avail_m 
    # Convert datetime to yyyymm integer format (e.g. 199112 for Dec 1991)
    df['yyyymm'] = (df['time_avail_m'].dt.year * 100 + df['time_avail_m'].dt.month).astype(int)
    
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