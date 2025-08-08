# ABOUTME: Return seasonality last year predictor translation from Stata
# ABOUTME: Calculates MomSeasonShort as 11-month lagged return

# Run from pyCode/ directory
# Inputs: SignalMasterTable.parquet
# Output: ../pyData/Predictors/MomSeasonShort.csv

import pandas as pd
import numpy as np

# DATA LOAD
df = pd.read_parquet('../pyData/Intermediate/SignalMasterTable.parquet')
df = df[['permno', 'time_avail_m', 'ret']].copy()

# Sort for lag operations
df = df.sort_values(['permno', 'time_avail_m'])

# SIGNAL CONSTRUCTION
# Replace missing returns with 0 (equivalent to Stata: replace ret = 0 if mi(ret))
df['ret'] = df['ret'].fillna(0)

# Generate MomSeasonShort = l11.ret (11-month lag of ret)
# Use calendar-based lag (11 months back) instead of positional lag
# This matches Stata's l11. operator which uses calendar-based lags
df['time_lag11'] = pd.to_datetime(df['time_avail_m']) - pd.DateOffset(months=11)

# Create lag data for merging  
lag_data = df[['permno', 'time_avail_m', 'ret']].copy()
lag_data['time_avail_m'] = pd.to_datetime(lag_data['time_avail_m'])
lag_data.columns = ['permno', 'time_lag11', 'ret_lag11']

# Convert time_lag11 to datetime for consistent merging
df['time_lag11'] = pd.to_datetime(df['time_lag11'])

# Merge to get lagged values
df = df.merge(lag_data, on=['permno', 'time_lag11'], how='left')

# Assign MomSeasonShort from the calendar-based lag
df['MomSeasonShort'] = df['ret_lag11']

# Keep only necessary columns for output
df_final = df[['permno', 'time_avail_m', 'MomSeasonShort']].copy()
df_final = df_final.dropna(subset=['MomSeasonShort'])

# Convert time_avail_m to yyyymm format like other predictors
df_final['yyyymm'] = df_final['time_avail_m'].dt.year * 100 + df_final['time_avail_m'].dt.month

# Convert to integers for consistency with other predictors
df_final['permno'] = df_final['permno'].astype('int64')
df_final['yyyymm'] = df_final['yyyymm'].astype('int64')

# Keep only required columns and set index
df_final = df_final[['permno', 'yyyymm', 'MomSeasonShort']].copy()
df_final = df_final.set_index(['permno', 'yyyymm'])

# SAVE
df_final.to_csv('../pyData/Predictors/MomSeasonShort.csv')

print("MomSeasonShort predictor saved successfully")
print(f"Output shape: {df_final.shape}")