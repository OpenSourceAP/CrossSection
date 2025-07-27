# ABOUTME: Translates Mom12m.do to create twelve-month momentum predictor
# ABOUTME: Run from pyCode/ directory: python3 Predictors/Mom12m.py

# Run from pyCode/ directory
# Inputs: SignalMasterTable.parquet
# Output: ../pyData/Predictors/Mom12m.csv

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

# Calculate lags for 11 months (excluding current month)
ret_lags = []
for i in range(1, 12):
    lag_col = f'ret_lag{i}'
    df[lag_col] = df.groupby('permno')['ret'].shift(i)
    ret_lags.append(f'(1 + df["{lag_col}"])')

# Calculate 12-month momentum (geometric return over 11 months)
momentum_formula = ' * '.join(ret_lags)
df['Mom12m'] = eval(momentum_formula) - 1

# Keep only necessary columns for output
df_final = df[['permno', 'time_avail_m', 'Mom12m']].copy()
df_final = df_final.dropna(subset=['Mom12m'])

# Convert time_avail_m to yyyymm format like other predictors
df_final['yyyymm'] = df_final['time_avail_m'].dt.year * 100 + df_final['time_avail_m'].dt.month

# Convert to integers for consistency with other predictors
df_final['permno'] = df_final['permno'].astype('int64')
df_final['yyyymm'] = df_final['yyyymm'].astype('int64')

# Keep only required columns and set index
df_final = df_final[['permno', 'yyyymm', 'Mom12m']].copy()
df_final = df_final.set_index(['permno', 'yyyymm'])

# SAVE
df_final.to_csv('../pyData/Predictors/Mom12m.csv')

print("Mom12m predictor saved successfully")