# ABOUTME: Translates realestate.do to create real estate holdings predictor
# ABOUTME: Run from pyCode/ directory: python3 Predictors/realestate.py

# Run from pyCode/ directory
# Inputs: m_aCompustat.parquet, SignalMasterTable.parquet
# Output: ../pyData/Predictors/realestate.csv

import pandas as pd
import numpy as np

# DATA LOAD
df = pd.read_parquet('../pyData/Intermediate/m_aCompustat.parquet')
df = df[['permno', 'time_avail_m', 'ppenb', 'ppenls', 'fatb', 'fatl', 'ppegt', 'ppent', 'at']].copy()

# Merge with SignalMasterTable
smt = pd.read_parquet('../pyData/Intermediate/SignalMasterTable.parquet')
df = df.merge(smt[['permno', 'time_avail_m', 'sicCRSP']], on=['permno', 'time_avail_m'], how='inner')

# Sample selection
df['sicCRSP'] = df['sicCRSP'].astype(str)
df['sic2D'] = df['sicCRSP'].str[:2]

# Count observations by industry-time and keep only industries with >= 5 observations
df['tempN'] = df.groupby(['sic2D', 'time_avail_m'])['at'].transform('count')
df = df[df['tempN'] >= 5].copy()

# Drop observations with missing key variables
df = df.dropna(subset=['at'])
df = df[(df['ppent'].notna()) | (df['ppegt'].notna())].copy()

# SIGNAL CONSTRUCTION
# Calculate real estate ratios using old and new methods
df['re_old'] = (df['ppenb'] + df['ppenls']) / df['ppent']
df['re_new'] = (df['fatb'] + df['fatl']) / df['ppegt']

# CHECKPOINT 1
bad_obs_1 = (df['permno'] == 10018) & (df['time_avail_m'].dt.year == 1987) & (df['time_avail_m'].dt.month == 4)
bad_obs_2 = (df['permno'] == 10018) & (df['time_avail_m'].dt.year == 1987) & (df['time_avail_m'].dt.month == 5)
bad_obs_3 = (df['permno'] == 10083) & (df['time_avail_m'].dt.year == 1986) & (df['time_avail_m'].dt.month == 12)
print("CHECKPOINT 1")
if bad_obs_1.any():
    print(df[bad_obs_1][['permno', 'time_avail_m', 're_old', 're_new']])
if bad_obs_2.any():
    print(df[bad_obs_2][['permno', 'time_avail_m', 're_old', 're_new']])
if bad_obs_3.any():
    print(df[bad_obs_3][['permno', 'time_avail_m', 're_old', 're_new']])

# Use new method, fallback to old method if new is missing
df['re'] = df['re_new']
df.loc[df['re_new'].isna(), 're'] = df['re_old']

# Convert infinite values to NaN to match Stata's behavior (division by zero)
df['re'] = df['re'].replace([np.inf, -np.inf], np.nan)

# CHECKPOINT 2
print("CHECKPOINT 2")
if bad_obs_1.any():
    print(df[bad_obs_1][['permno', 'time_avail_m', 're', 're_old', 're_new']])
if bad_obs_2.any():
    print(df[bad_obs_2][['permno', 'time_avail_m', 're', 're_old', 're_new']])
if bad_obs_3.any():
    print(df[bad_obs_3][['permno', 'time_avail_m', 're', 're_old', 're_new']])

# Extract year and decade
df['year'] = df['time_avail_m'].dt.year
df['decade'] = (df['year'] // 10) * 10

# Industry adjustment - subtract industry mean
df['tempMean'] = df.groupby(['sic2D', 'time_avail_m'])['re'].transform('mean')

# CHECKPOINT 3
print("CHECKPOINT 3")
if bad_obs_1.any():
    print(df[bad_obs_1][['permno', 'time_avail_m', 're', 'tempMean', 'sic2D']])
if bad_obs_2.any():
    print(df[bad_obs_2][['permno', 'time_avail_m', 're', 'tempMean', 'sic2D']])
if bad_obs_3.any():
    print(df[bad_obs_3][['permno', 'time_avail_m', 're', 'tempMean', 'sic2D']])

df['realestate'] = df['re'] - df['tempMean']

# CHECKPOINT 4
print("CHECKPOINT 4")
if bad_obs_1.any():
    print(df[bad_obs_1][['permno', 'time_avail_m', 'realestate', 're', 'tempMean']])
if bad_obs_2.any():
    print(df[bad_obs_2][['permno', 'time_avail_m', 'realestate', 're', 'tempMean']])
if bad_obs_3.any():
    print(df[bad_obs_3][['permno', 'time_avail_m', 'realestate', 're', 'tempMean']])

# Keep only necessary columns for output
df_final = df[['permno', 'time_avail_m', 'realestate']].copy()
df_final = df_final.dropna(subset=['realestate'])

# Convert time_avail_m to yyyymm format like other predictors
df_final['yyyymm'] = df_final['time_avail_m'].dt.year * 100 + df_final['time_avail_m'].dt.month

# Convert to integers for consistency with other predictors
df_final['permno'] = df_final['permno'].astype('int64')
df_final['yyyymm'] = df_final['yyyymm'].astype('int64')

# Keep only required columns and set index
df_final = df_final[['permno', 'yyyymm', 'realestate']].copy()
df_final = df_final.set_index(['permno', 'yyyymm'])

# SAVE
df_final.to_csv('../pyData/Predictors/realestate.csv')

print("realestate predictor saved successfully")