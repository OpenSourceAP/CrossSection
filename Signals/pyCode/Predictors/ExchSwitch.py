# ABOUTME: Translates ExchSwitch.do to create exchange switching indicator
# ABOUTME: Run from pyCode/ directory: python3 Predictors/ExchSwitch.py

# Run from pyCode/ directory
# Inputs: SignalMasterTable.parquet
# Output: ../pyData/Predictors/ExchSwitch.csv

import pandas as pd
import numpy as np

# DATA LOAD
df = pd.read_parquet('../pyData/Intermediate/SignalMasterTable.parquet')
df = df[['gvkey', 'permno', 'time_avail_m', 'exchcd']].copy()

# Sort for lag operations
df = df.sort_values(['permno', 'time_avail_m'])

# SIGNAL CONSTRUCTION
# Create lags for 12 months
for i in range(1, 13):
    df[f'exchcd_lag{i}'] = df.groupby('permno')['exchcd'].shift(i)

# Create exchange switch indicator
# NYSE (1) <- AMEX (2) or NASDAQ (3) in past 12 months
# OR AMEX (2) <- NASDAQ (3) in past 12 months

# Check if any of the 12 lags equal 2 or 3
amex_nasdaq_lags = [df[f'exchcd_lag{i}'].isin([2, 3]) for i in range(1, 13)]
any_amex_nasdaq = pd.concat(amex_nasdaq_lags, axis=1).any(axis=1)

# Check if any of the 12 lags equal 3  
nasdaq_lags = [df[f'exchcd_lag{i}'] == 3 for i in range(1, 13)]
any_nasdaq = pd.concat(nasdaq_lags, axis=1).any(axis=1)

# Exchange switch conditions
condition1 = (df['exchcd'] == 1) & any_amex_nasdaq  # NYSE from AMEX/NASDAQ
condition2 = (df['exchcd'] == 2) & any_nasdaq       # AMEX from NASDAQ

df['ExchSwitch'] = (condition1 | condition2).astype(int)

# Keep only necessary columns for output
df_final = df[['permno', 'time_avail_m', 'ExchSwitch']].copy()

# Convert time_avail_m to yyyymm format like other predictors
df_final['yyyymm'] = df_final['time_avail_m'].dt.year * 100 + df_final['time_avail_m'].dt.month

# Convert to integers for consistency with other predictors
df_final['permno'] = df_final['permno'].astype('int64')
df_final['yyyymm'] = df_final['yyyymm'].astype('int64')

# Keep only required columns and set index
df_final = df_final[['permno', 'yyyymm', 'ExchSwitch']].copy()
df_final = df_final.set_index(['permno', 'yyyymm'])

# SAVE
df_final.to_csv('../pyData/Predictors/ExchSwitch.csv')

print("ExchSwitch predictor saved successfully")