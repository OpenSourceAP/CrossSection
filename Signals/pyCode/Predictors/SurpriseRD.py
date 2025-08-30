# ABOUTME: SurpriseRD.py - calculates unexpected R&D increase predictor
# ABOUTME: Unexpected R&D increase - binary indicator for firms with surprising increases in R&D spending
# ABOUTME: Reference: Eberhart, Maxwell and Siddique 2004, Table 5A EW

# Run from pyCode/ directory
# Inputs: m_aCompustat.parquet
# Output: ../pyData/Predictors/SurpriseRD.csv

import pandas as pd
import numpy as np

# DATA LOAD
df = pd.read_parquet('../pyData/Intermediate/m_aCompustat.parquet')
df = df[['gvkey', 'permno', 'time_avail_m', 'xrd', 'revt', 'at']].copy()

# Drop duplicates
df = df.drop_duplicates(subset=['permno', 'time_avail_m'])

# Sort for lag operations
df = df.sort_values(['permno', 'time_avail_m'])

# SIGNAL CONSTRUCTION
# Calculate 12-month lags
df['xrd_lag12'] = df.groupby('permno')['xrd'].shift(12)
df['at_lag12'] = df.groupby('permno')['at'].shift(12)

# R&D surprise conditions
condition1 = (df['xrd'] / df['revt'] > 0)
condition2 = (df['xrd'] / df['at'] > 0) 
condition3 = (df['xrd'] / df['xrd_lag12'] > 1.05)
condition4 = ((df['xrd'] / df['at']) / (df['xrd_lag12'] / df['at_lag12']) > 1.05)
condition5 = (~df['xrd'].isna())
condition6 = (~df['xrd_lag12'].isna())

# Create SurpriseRD indicator
df['SurpriseRD'] = np.nan
df.loc[condition1 & condition2 & condition3 & condition4 & condition5 & condition6, 'SurpriseRD'] = 1

# Set to 0 if conditions not met but both xrd and lagged xrd are not missing
df.loc[df['SurpriseRD'].isna() & condition5 & condition6, 'SurpriseRD'] = 0

# Keep only necessary columns for output
df_final = df[['permno', 'time_avail_m', 'SurpriseRD']].copy()
df_final = df_final.dropna(subset=['SurpriseRD'])

# Convert time_avail_m to yyyymm format like other predictors
df_final['yyyymm'] = df_final['time_avail_m'].dt.year * 100 + df_final['time_avail_m'].dt.month

# Convert to integers for consistency with other predictors
df_final['permno'] = df_final['permno'].astype('int64')
df_final['yyyymm'] = df_final['yyyymm'].astype('int64')

# Keep only required columns and set index
df_final = df_final[['permno', 'yyyymm', 'SurpriseRD']].copy()
df_final = df_final.set_index(['permno', 'yyyymm'])

# SAVE
df_final.to_csv('../pyData/Predictors/SurpriseRD.csv')

print("SurpriseRD predictor saved successfully")