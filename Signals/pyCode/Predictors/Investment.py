# ABOUTME: Investment following Titman, Wei and Xie 2004, Table 1B Average
# ABOUTME: Ratio of capital investment to revenue divided by firm-specific 36-month rolling mean
"""
Usage:
    python3 Predictors/Investment.py

Inputs:
    - m_aCompustat.parquet: Monthly Compustat data with columns [permno, capx, revt]

Outputs:
    - Investment.csv: CSV file with columns [permno, yyyymm, Investment]
    - Investment = (capx/revt) / 36-month rolling mean, exclude if revt < $10m
"""

# Run from pyCode/ directory
# Inputs: m_aCompustat.parquet
# Output: ../pyData/Predictors/Investment.csv

import pandas as pd
import numpy as np
import sys
import os

# Add the parent directory to sys.path to import utils
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils.asrol import asrol

# DATA LOAD
df = pd.read_parquet('../pyData/Intermediate/m_aCompustat.parquet')
df = df[['gvkey', 'permno', 'time_avail_m', 'capx', 'revt']].copy()


# Drop duplicates
df = df.drop_duplicates(subset=['permno', 'time_avail_m'])


# Sort for time series operations
df = df.sort_values(['permno', 'time_avail_m'])

# SIGNAL CONSTRUCTION
# Calculate investment ratio as capital expenditure divided by revenue
df['Investment'] = df['capx'] / df['revt']

# Calculate 36-month rolling historical average of investment ratio (minimum 24 observations required)
df = asrol(df, 'permno', 'time_avail_m', '1mo', 36, 'Investment', 'mean', 'tempMean', min_samples=24)

# Normalize current investment ratio by its historical average to capture relative investment intensity
df['Investment'] = df['Investment'] / df['tempMean']

# Exclude firms with revenue below $10 million to focus on established companies
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