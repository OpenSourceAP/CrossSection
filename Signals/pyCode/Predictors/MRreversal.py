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

# Calculate lags for months 13-18
df['ret_lag13'] = df.groupby('permno')['ret'].shift(13).fillna(0)
df['ret_lag14'] = df.groupby('permno')['ret'].shift(14).fillna(0)
df['ret_lag15'] = df.groupby('permno')['ret'].shift(15).fillna(0)
df['ret_lag16'] = df.groupby('permno')['ret'].shift(16).fillna(0)
df['ret_lag17'] = df.groupby('permno')['ret'].shift(17).fillna(0)
df['ret_lag18'] = df.groupby('permno')['ret'].shift(18).fillna(0)

# Calculate momentum-reversal (geometric return over months 13-18)
df['MRreversal'] = ((1 + df['ret_lag13']) * 
                    (1 + df['ret_lag14']) * 
                    (1 + df['ret_lag15']) * 
                    (1 + df['ret_lag16']) * 
                    (1 + df['ret_lag17']) * 
                    (1 + df['ret_lag18'])) - 1

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

# SAVE
df_final.to_csv('../pyData/Predictors/MRreversal.csv')

print("MRreversal predictor saved successfully")