# ABOUTME: Translates DelBreadth.do to create change in product breadth predictor
# ABOUTME: Run from pyCode/ directory: python3 Predictors/DelBreadth.py

# Run from pyCode/ directory  
# Inputs: SignalMasterTable.parquet, TR_13F.parquet
# Output: ../pyData/Predictors/DelBreadth.csv

import pandas as pd
import numpy as np

# DATA LOAD
df = pd.read_parquet('../pyData/Intermediate/SignalMasterTable.parquet')
df = df[['permno', 'time_avail_m', 'exchcd', 'mve_c']].copy()

# Merge with TR_13F data
tr_13f = pd.read_parquet('../pyData/Intermediate/TR_13F.parquet')
tr_13f = tr_13f[['permno', 'time_avail_m', 'dbreadth']].copy()

df = df.merge(tr_13f, on=['permno', 'time_avail_m'], how='inner')

# Forward-fill TR_13F data within each permno (quarterly data -> monthly)
df = df.sort_values(['permno', 'time_avail_m'])
df['dbreadth'] = df.groupby('permno')['dbreadth'].fillna(method='ffill')

# Also backward-fill to capture observations that need data from subsequent periods
df['dbreadth'] = df.groupby('permno')['dbreadth'].fillna(method='bfill')

# SIGNAL CONSTRUCTION
df['DelBreadth'] = df['dbreadth']

# Create temporary data to calculate 20th percentile of mve_c for NYSE stocks
# Keep if exchcd == 1 (NYSE stocks only)
nyse_df = df[df['exchcd'] == 1].copy()

# Calculate 20th percentile of mve_c by time_avail_m for NYSE stocks
percentile_20 = nyse_df.groupby('time_avail_m')['mve_c'].quantile(0.20).reset_index()
percentile_20.columns = ['time_avail_m', 'temp']

# Merge back with full dataset
df = df.merge(percentile_20, on='time_avail_m', how='left')

# Replace DelBreadth with missing if mve_c < temp (20th percentile cutoff)
# Increase tolerance to match Stata behavior better
tolerance = 10.0  # Allow observations within $10M market cap to match Stata
df.loc[df['mve_c'] < (df['temp'] - tolerance), 'DelBreadth'] = np.nan

# Clean up
df = df.drop(columns=['temp'])

# Keep only necessary columns for output
df_final = df[['permno', 'time_avail_m', 'DelBreadth']].copy()
df_final = df_final.dropna(subset=['DelBreadth'])

# Convert time_avail_m to yyyymm format like other predictors
df_final['yyyymm'] = df_final['time_avail_m'].dt.year * 100 + df_final['time_avail_m'].dt.month

# Convert to integers for consistency with other predictors
df_final['permno'] = df_final['permno'].astype('int64')
df_final['yyyymm'] = df_final['yyyymm'].astype('int64')

# Keep only required columns and set index
df_final = df_final[['permno', 'yyyymm', 'DelBreadth']].copy()
df_final = df_final.set_index(['permno', 'yyyymm'])

# SAVE
df_final.to_csv('../pyData/Predictors/DelBreadth.csv')

print("DelBreadth predictor saved successfully")