# ABOUTME: Translates MRreversal.do to create momentum-reversal predictor
# ABOUTME: Run from pyCode/ directory: python3 Predictors/MRreversal.py

# Run from pyCode/ directory
# Inputs: SignalMasterTable.parquet
# Output: ../pyData/Predictors/MRreversal.csv

import pandas as pd
import numpy as np

# DATA LOAD
df = pd.read_parquet('../pyData/Intermediate/SignalMasterTable.parquet')
df = df[['permno', 'time_avail_m', 'ret']].copy()

# Sort for lag operations
df = df.sort_values(['permno', 'time_avail_m'])

# SIGNAL CONSTRUCTION
# Replace missing returns with 0
df['ret'] = df['ret'].fillna(0)

# CHECKPOINT 1: After ret cleanup, before lag calculation
print("CHECKPOINT 1: After ret cleanup, before lag calculation")
debug_obs1 = df[(df['permno'] == 15017) & (df['time_avail_m'] == pd.Period('2018-06', freq='M'))]
if not debug_obs1.empty:
    print("permno=15017, time_avail_m=2018-06:")
    print(debug_obs1[['permno', 'time_avail_m', 'ret']].to_string())
debug_obs2 = df[(df['permno'] == 91201) & (df['time_avail_m'] == pd.Period('2019-10', freq='M'))]
if not debug_obs2.empty:
    print("permno=91201, time_avail_m=2019-10:")
    print(debug_obs2[['permno', 'time_avail_m', 'ret']].to_string())

# Calculate lags for months 13-18 using calendar-based approach (matching Stata's l13.ret etc.)
# Use merge operations to efficiently create calendar-based lags
for lag in [13, 14, 15, 16, 17, 18]:
    # Create a copy for the lag data with shifted dates
    lag_df = df[['permno', 'time_avail_m', 'ret']].copy()
    lag_df['time_avail_m'] = lag_df['time_avail_m'] + pd.DateOffset(months=lag)
    lag_df = lag_df.rename(columns={'ret': f'ret_lag{lag}'})
    
    # Merge to get the lagged values
    df = df.merge(lag_df[['permno', 'time_avail_m', f'ret_lag{lag}']], 
                  on=['permno', 'time_avail_m'], how='left')
    
    # Fill missing lags with 0 (consistent with Stata behavior for missing)
    df[f'ret_lag{lag}'] = df[f'ret_lag{lag}'].fillna(0)

# Calculate momentum-reversal (geometric return over months 13-18)
df['MRreversal'] = ((1 + df['ret_lag13']) * 
                    (1 + df['ret_lag14']) * 
                    (1 + df['ret_lag15']) * 
                    (1 + df['ret_lag16']) * 
                    (1 + df['ret_lag17']) * 
                    (1 + df['ret_lag18'])) - 1

# CHECKPOINT 2: After MRreversal calculation
print("\nCHECKPOINT 2: After MRreversal calculation")
debug_obs1 = df[(df['permno'] == 15017) & (df['time_avail_m'] == pd.Period('2018-06', freq='M'))]
if not debug_obs1.empty:
    print("permno=15017, time_avail_m=2018-06:")
    print(debug_obs1[['permno', 'time_avail_m', 'ret', 'ret_lag13', 'ret_lag14', 'ret_lag15', 'ret_lag16', 'ret_lag17', 'ret_lag18', 'MRreversal']].to_string())
debug_obs2 = df[(df['permno'] == 91201) & (df['time_avail_m'] == pd.Period('2019-10', freq='M'))]
if not debug_obs2.empty:
    print("permno=91201, time_avail_m=2019-10:")
    print(debug_obs2[['permno', 'time_avail_m', 'ret', 'ret_lag13', 'ret_lag14', 'ret_lag15', 'ret_lag16', 'ret_lag17', 'ret_lag18', 'MRreversal']].to_string())

# Keep only necessary columns for output
df_final = df[['permno', 'time_avail_m', 'MRreversal']].copy()
df_final = df_final.dropna(subset=['MRreversal'])

# Convert time_avail_m to yyyymm format like other predictors
df_final['yyyymm'] = df_final['time_avail_m'].dt.year * 100 + df_final['time_avail_m'].dt.month

# Convert to integers for consistency with other predictors
df_final['permno'] = df_final['permno'].astype('int64')
df_final['yyyymm'] = df_final['yyyymm'].astype('int64')

# Keep only required columns and set index
df_final = df_final[['permno', 'yyyymm', 'MRreversal']].copy()
df_final = df_final.set_index(['permno', 'yyyymm'])

# CHECKPOINT 3: Before save
print("\nCHECKPOINT 3: Before save")
debug_obs1 = df_final[(df_final.index.get_level_values('permno') == 15017) & (df_final.index.get_level_values('yyyymm') == 201806)]
if not debug_obs1.empty:
    print("permno=15017, yyyymm=201806:")
    print(debug_obs1.to_string())
debug_obs2 = df_final[(df_final.index.get_level_values('permno') == 91201) & (df_final.index.get_level_values('yyyymm') == 201910)]
if not debug_obs2.empty:
    print("permno=91201, yyyymm=201910:")
    print(debug_obs2.to_string())

# SAVE
df_final.to_csv('../pyData/Predictors/MRreversal.csv')

print("MRreversal predictor saved successfully")