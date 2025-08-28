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
from utils.asrol import asrol_fast

# DATA LOAD
df = pd.read_parquet('../pyData/Intermediate/m_aCompustat.parquet')
df = df[['gvkey', 'permno', 'time_avail_m', 'capx', 'revt']].copy()


# Drop duplicates
df = df.drop_duplicates(subset=['permno', 'time_avail_m'])


# Sort for time series operations
df = df.sort_values(['permno', 'time_avail_m'])

# SIGNAL CONSTRUCTION
# Calculate investment ratio
df['Investment'] = df['capx'] / df['revt']


# Calculate rolling mean over 36 months (minimum 24)
df = asrol_fast(df, 'permno', 'time_avail_m', 'Investment', 36, stat='mean', new_col_name='tempMean', min_periods=24)


# Normalize by rolling mean
df['Investment'] = df['Investment'] / df['tempMean']


# Set to missing if revenue less than 10 million
df.loc[df['revt'] < 10, 'Investment'] = np.nan


# Keep only necessary columns for output
df_final = df[['permno', 'time_avail_m', 'Investment']].copy()


df_final = df_final.dropna(subset=['Investment'])


# Convert time_avail_m to yyyymm format like other predictors
df_final['yyyymm'] = df_final['time_avail_m'].dt.year * 100 + df_final['time_avail_m'].dt.month

# Convert to integers for consistency with other predictors
df_final['permno'] = df_final['permno'].astype('int64')
df_final['yyyymm'] = df_final['yyyymm'].astype('int64')

# Keep only required columns and set index
df_final = df_final[['permno', 'yyyymm', 'Investment']].copy()
df_final = df_final.set_index(['permno', 'yyyymm'])


# SAVE
df_final.to_csv('../pyData/Predictors/Investment.csv')

print("Investment predictor saved successfully")