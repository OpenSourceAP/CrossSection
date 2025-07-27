# ABOUTME: Translates Mom6m.do to create six-month momentum predictor
# ABOUTME: Run from pyCode/ directory: python3 Predictors/Mom6m.py

# Run from pyCode/ directory
# Inputs: SignalMasterTable.parquet
# Output: ../pyData/Predictors/Mom6m.csv

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

# Calculate lags
df['ret_lag1'] = df.groupby('permno')['ret'].shift(1)
df['ret_lag2'] = df.groupby('permno')['ret'].shift(2)
df['ret_lag3'] = df.groupby('permno')['ret'].shift(3)
df['ret_lag4'] = df.groupby('permno')['ret'].shift(4)
df['ret_lag5'] = df.groupby('permno')['ret'].shift(5)

# Calculate 6-month momentum (geometric return)
df['Mom6m'] = ((1 + df['ret_lag1']) * 
               (1 + df['ret_lag2']) * 
               (1 + df['ret_lag3']) * 
               (1 + df['ret_lag4']) * 
               (1 + df['ret_lag5'])) - 1

# Keep only necessary columns for output
df_final = df[['permno', 'time_avail_m', 'Mom6m']].copy()
df_final = df_final.dropna(subset=['Mom6m'])

# Convert time_avail_m to yyyymm format like other predictors
df_final['yyyymm'] = df_final['time_avail_m'].dt.year * 100 + df_final['time_avail_m'].dt.month

# Convert to integers for consistency with other predictors
df_final['permno'] = df_final['permno'].astype('int64')
df_final['yyyymm'] = df_final['yyyymm'].astype('int64')

# Keep only required columns and set index
df_final = df_final[['permno', 'yyyymm', 'Mom6m']].copy()
df_final = df_final.set_index(['permno', 'yyyymm'])

# SAVE
df_final.to_csv('../pyData/Predictors/Mom6m.csv')

print("Mom6m predictor saved successfully")