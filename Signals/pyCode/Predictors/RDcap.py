# ABOUTME: Translates RDcap.do to create R&D capital to assets predictor for small firms
# ABOUTME: Run from pyCode/ directory: python3 Predictors/RDcap.py

# Run from pyCode/ directory
# Inputs: m_aCompustat.parquet, SignalMasterTable.parquet
# Output: ../pyData/Predictors/RDcap.csv

import pandas as pd
import numpy as np
import sys
sys.path.append('.')
from utils.stata_fastxtile import fastxtile

# DATA LOAD
df = pd.read_parquet('../pyData/Intermediate/m_aCompustat.parquet')
df = df[['permno', 'time_avail_m', 'at', 'xrd']].copy()

# Drop duplicates
df = df.drop_duplicates(subset=['permno', 'time_avail_m'])

# Merge with SignalMasterTable (keep master match like Stata)
smt = pd.read_parquet('../pyData/Intermediate/SignalMasterTable.parquet')
df = df.merge(smt[['permno', 'time_avail_m', 'mve_c']], on=['permno', 'time_avail_m'], how='left')

# Sort for lag operations
df = df.sort_values(['permno', 'time_avail_m'])

# SIGNAL CONSTRUCTION
# Extract year for filtering
df['year'] = df['time_avail_m'].dt.year

# Handle missing xrd values
df['tempXRD'] = df['xrd'].fillna(0)

# Calculate calendar-based lags of tempXRD (matching Stata's l12., l24., etc.)
df_tempxrd = df[['permno', 'time_avail_m', 'tempXRD']].copy()

# Calculate lag times
df['time_lag12'] = df['time_avail_m'] - pd.DateOffset(months=12)
df['time_lag24'] = df['time_avail_m'] - pd.DateOffset(months=24)
df['time_lag36'] = df['time_avail_m'] - pd.DateOffset(months=36)
df['time_lag48'] = df['time_avail_m'] - pd.DateOffset(months=48)

# Merge to get lagged values
df = df.merge(df_tempxrd.rename(columns={'time_avail_m': 'time_lag12', 'tempXRD': 'tempXRD_lag12'}),
              on=['permno', 'time_lag12'], how='left')
df = df.merge(df_tempxrd.rename(columns={'time_avail_m': 'time_lag24', 'tempXRD': 'tempXRD_lag24'}),
              on=['permno', 'time_lag24'], how='left')
df = df.merge(df_tempxrd.rename(columns={'time_avail_m': 'time_lag36', 'tempXRD': 'tempXRD_lag36'}),
              on=['permno', 'time_lag36'], how='left')
df = df.merge(df_tempxrd.rename(columns={'time_avail_m': 'time_lag48', 'tempXRD': 'tempXRD_lag48'}),
              on=['permno', 'time_lag48'], how='left')

# Clean up temporary columns
df = df.drop(['time_lag12', 'time_lag24', 'time_lag36', 'time_lag48'], axis=1)

# Fill missing lagged values with 0 (like Stata arithmetic)
df['tempXRD_lag12'] = df['tempXRD_lag12'].fillna(0)
df['tempXRD_lag24'] = df['tempXRD_lag24'].fillna(0)
df['tempXRD_lag36'] = df['tempXRD_lag36'].fillna(0)
df['tempXRD_lag48'] = df['tempXRD_lag48'].fillna(0)

# Calculate R&D capital (weighted sum of current and lagged R&D)
df['RDcap'] = (df['tempXRD'] + 
               0.8 * df['tempXRD_lag12'] + 
               0.6 * df['tempXRD_lag24'] + 
               0.4 * df['tempXRD_lag36'] + 
               0.2 * df['tempXRD_lag48']) / df['at']

# Exclude observations before 1980
df.loc[df['year'] < 1980, 'RDcap'] = np.nan

# Create size tertiles using fastxtile helper
df['tempsizeq'] = fastxtile(df, 'mve_c', by='time_avail_m', n=3)
df.loc[df['tempsizeq'] >= 2, 'RDcap'] = np.nan

# Keep only necessary columns for output
df_final = df[['permno', 'time_avail_m', 'RDcap']].copy()
df_final = df_final.dropna(subset=['RDcap'])

# Convert time_avail_m to yyyymm format like other predictors
df_final['yyyymm'] = df_final['time_avail_m'].dt.year * 100 + df_final['time_avail_m'].dt.month

# Convert to integers for consistency with other predictors
df_final['permno'] = df_final['permno'].astype('int64')
df_final['yyyymm'] = df_final['yyyymm'].astype('int64')

# Keep only required columns and set index
df_final = df_final[['permno', 'yyyymm', 'RDcap']].copy()
df_final = df_final.set_index(['permno', 'yyyymm'])

# SAVE
df_final.to_csv('../pyData/Predictors/RDcap.csv')

print("RDcap predictor saved successfully")