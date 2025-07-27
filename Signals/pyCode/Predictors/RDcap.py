# ABOUTME: Translates RDcap.do to create R&D capital to assets predictor for small firms
# ABOUTME: Run from pyCode/ directory: python3 Predictors/RDcap.py

# Run from pyCode/ directory
# Inputs: m_aCompustat.parquet, SignalMasterTable.parquet
# Output: ../pyData/Predictors/RDcap.csv

import pandas as pd
import numpy as np

# DATA LOAD
df = pd.read_parquet('../pyData/Intermediate/m_aCompustat.parquet')
df = df[['permno', 'time_avail_m', 'at', 'xrd']].copy()

# Drop duplicates
df = df.drop_duplicates(subset=['permno', 'time_avail_m'])

# Merge with SignalMasterTable
smt = pd.read_parquet('../pyData/Intermediate/SignalMasterTable.parquet')
df = df.merge(smt[['permno', 'time_avail_m', 'mve_c']], on=['permno', 'time_avail_m'], how='inner')

# Sort for lag operations
df = df.sort_values(['permno', 'time_avail_m'])

# SIGNAL CONSTRUCTION
# Extract year for filtering
df['year'] = df['time_avail_m'].dt.year

# Handle missing xrd values
df['tempXRD'] = df['xrd'].fillna(0)

# Calculate lags of tempXRD
df['tempXRD_lag12'] = df.groupby('permno')['tempXRD'].shift(12)
df['tempXRD_lag24'] = df.groupby('permno')['tempXRD'].shift(24)
df['tempXRD_lag36'] = df.groupby('permno')['tempXRD'].shift(36)
df['tempXRD_lag48'] = df.groupby('permno')['tempXRD'].shift(48)

# Calculate R&D capital (weighted sum of current and lagged R&D)
df['RDcap'] = (df['tempXRD'] + 
               0.8 * df['tempXRD_lag12'] + 
               0.6 * df['tempXRD_lag24'] + 
               0.4 * df['tempXRD_lag36'] + 
               0.2 * df['tempXRD_lag48']) / df['at']

# Exclude observations before 1980
df.loc[df['year'] < 1980, 'RDcap'] = np.nan

# Create size tertiles and keep only smallest firms (as in original paper)
df['tempsizeq'] = df.groupby('time_avail_m')['mve_c'].transform(lambda x: pd.qcut(x, 3, labels=False, duplicates='drop') + 1)
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