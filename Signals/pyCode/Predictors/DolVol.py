# ABOUTME: Translates DolVol.do to create dollar volume predictor
# ABOUTME: Run from pyCode/ directory: python3 Predictors/DolVol.py

# Run from pyCode/ directory
# Inputs: monthlyCRSP.parquet
# Output: ../pyData/Predictors/DolVol.csv

import pandas as pd
import numpy as np

# DATA LOAD
df = pd.read_parquet('../pyData/Intermediate/monthlyCRSP.parquet')
df = df[['permno', 'time_avail_m', 'vol', 'prc']].copy()

# Sort for lag operations
df = df.sort_values(['permno', 'time_avail_m'])

# SIGNAL CONSTRUCTION
# Calculate 2-month lags
df['vol_lag2'] = df.groupby('permno')['vol'].shift(2)
df['prc_lag2'] = df.groupby('permno')['prc'].shift(2)

# Calculate dollar volume with log transformation
df['DolVol'] = np.log(df['vol_lag2'] * np.abs(df['prc_lag2']))

# Keep only necessary columns for output
df_final = df[['permno', 'time_avail_m', 'DolVol']].copy()
df_final = df_final.dropna(subset=['DolVol'])

# Convert time_avail_m to yyyymm format like other predictors
df_final['yyyymm'] = df_final['time_avail_m'].dt.year * 100 + df_final['time_avail_m'].dt.month

# Convert to integers for consistency with other predictors
df_final['permno'] = df_final['permno'].astype('int64')
df_final['yyyymm'] = df_final['yyyymm'].astype('int64')

# Keep only required columns and set index
df_final = df_final[['permno', 'yyyymm', 'DolVol']].copy()
df_final = df_final.set_index(['permno', 'yyyymm'])

# SAVE
df_final.to_csv('../pyData/Predictors/DolVol.csv')

print("DolVol predictor saved successfully")