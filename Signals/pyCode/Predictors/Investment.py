# ABOUTME: Translates Investment.do to create investment predictor
# ABOUTME: Run from pyCode/ directory: python3 Predictors/Investment.py

# Run from pyCode/ directory
# Inputs: m_aCompustat.parquet
# Output: ../pyData/Predictors/Investment.csv

import pandas as pd
import numpy as np
import sys
import os

# Add the parent directory to sys.path to import utils
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils.data_utils import asrol

# DATA LOAD
df = pd.read_parquet('../pyData/Intermediate/m_aCompustat.parquet')
df = df[['gvkey', 'permno', 'time_avail_m', 'capx', 'revt']].copy()

# CHECKPOINT 1: Initial data load
print(f"Initial observations: {len(df)}")
test_permnos = [10006, 10051, 11406, 12473]
test_date = pd.Timestamp('2007-04-01')
test_obs = df[(df['permno'].isin(test_permnos)) & (df['time_avail_m'] == test_date)]
print("CHECKPOINT 1 - Test observations:")
print(test_obs[['permno', 'time_avail_m', 'capx', 'revt']])

# Drop duplicates
df = df.drop_duplicates(subset=['permno', 'time_avail_m'])

# CHECKPOINT 2: After removing duplicates
print(f"After duplicate removal: {len(df)}")
test_obs = df[(df['permno'].isin(test_permnos)) & (df['time_avail_m'] == test_date)]
print("CHECKPOINT 2 - Test observations:")
print(test_obs[['permno', 'time_avail_m', 'capx', 'revt']])

# Sort for time series operations
df = df.sort_values(['permno', 'time_avail_m'])

# SIGNAL CONSTRUCTION
# Calculate investment ratio
df['Investment'] = df['capx'] / df['revt']

# CHECKPOINT 3: After creating Investment ratio
investment_count = df['Investment'].notna().sum()
print(f"Non-missing Investment after creation: {investment_count}")
test_obs = df[(df['permno'].isin(test_permnos)) & (df['time_avail_m'] == test_date)]
print("CHECKPOINT 3 - Test observations:")
print(test_obs[['permno', 'time_avail_m', 'Investment', 'capx', 'revt']])

# Calculate rolling mean over 36 months (minimum 24)
df = asrol(df, 'permno', 'time_avail_m', 'Investment', 36, stat='mean', new_col_name='tempMean', min_periods=24)

# CHECKPOINT 4: After rolling mean calculation
tempmean_count = df['tempMean'].notna().sum()
print(f"Non-missing tempMean after asrol: {tempmean_count}")
test_obs = df[(df['permno'].isin(test_permnos)) & (df['time_avail_m'] == test_date)]
print("CHECKPOINT 4 - Test observations:")
print(test_obs[['permno', 'time_avail_m', 'Investment', 'tempMean']])

# Normalize by rolling mean
df['Investment'] = df['Investment'] / df['tempMean']

# CHECKPOINT 5: After normalizing by rolling mean
investment_count = df['Investment'].notna().sum()
print(f"Non-missing Investment after normalization: {investment_count}")
test_obs = df[(df['permno'].isin(test_permnos)) & (df['time_avail_m'] == test_date)]
print("CHECKPOINT 5 - Test observations:")
print(test_obs[['permno', 'time_avail_m', 'Investment', 'tempMean']])

# Set to missing if revenue less than 10 million
df.loc[df['revt'] < 10, 'Investment'] = np.nan

# CHECKPOINT 6: After revenue filter
investment_count = df['Investment'].notna().sum()
print(f"Non-missing Investment after revenue filter: {investment_count}")
test_obs = df[(df['permno'].isin(test_permnos)) & (df['time_avail_m'] == test_date)]
print("CHECKPOINT 6 - Test observations:")
print(test_obs[['permno', 'time_avail_m', 'Investment', 'revt']])

# Keep only necessary columns for output
df_final = df[['permno', 'time_avail_m', 'Investment']].copy()

# CHECKPOINT 7: Before final dropna
print(f"Observations before final dropna: {len(df_final)}")
test_obs = df_final[(df_final['permno'].isin(test_permnos)) & (df_final['time_avail_m'] == test_date)]
print("CHECKPOINT 7 - Test observations before dropna:")
print(test_obs[['permno', 'time_avail_m', 'Investment']])

df_final = df_final.dropna(subset=['Investment'])

# CHECKPOINT 8: After final dropna
print(f"Final observations after dropna: {len(df_final)}")
test_obs = df_final[(df_final['permno'].isin(test_permnos)) & (df_final['time_avail_m'] == test_date)]
print("CHECKPOINT 8 - Final test observations:")
print(test_obs[['permno', 'time_avail_m', 'Investment']])

# Convert time_avail_m to yyyymm format like other predictors
df_final['yyyymm'] = df_final['time_avail_m'].dt.year * 100 + df_final['time_avail_m'].dt.month

# Convert to integers for consistency with other predictors
df_final['permno'] = df_final['permno'].astype('int64')
df_final['yyyymm'] = df_final['yyyymm'].astype('int64')

# Keep only required columns and set index
df_final = df_final[['permno', 'yyyymm', 'Investment']].copy()
df_final = df_final.set_index(['permno', 'yyyymm'])

# CHECKPOINT 9: Final output format
print(f"Final output observations: {len(df_final)}")
test_obs_final = df_final.reset_index()[(df_final.reset_index()['permno'].isin(test_permnos)) & (df_final.reset_index()['yyyymm'] == 200704)]
print("CHECKPOINT 9 - Final output format for test observations:")
print(test_obs_final[['permno', 'yyyymm', 'Investment']])

# SAVE
df_final.to_csv('../pyData/Predictors/Investment.csv')

print("Investment predictor saved successfully")