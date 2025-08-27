# ABOUTME: Translates EarningsConsistency.do from Stata to Python
# ABOUTME: Calculates earnings consistency measure based on standardized earnings changes

# How to run: python3 EarningsConsistency.py
# Inputs: ../pyData/Intermediate/m_aCompustat.parquet
# Outputs: ../pyData/Predictors/EarningsConsistency.csv

import pandas as pd
import numpy as np

# set path for utils
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from utils.savepredictor import save_predictor
from utils.stata_replication import stata_multi_lag

# DATA LOAD
df = pd.read_parquet('../pyData/Intermediate/m_aCompustat.parquet', 
                     columns=['permno', 'time_avail_m', 'epspx'])

# SIGNAL CONSTRUCTION
# Sort data (equivalent to xtset permno time_avail_m)
df = df.sort_values(['permno', 'time_avail_m'])

# Create 12-month and 24-month lags of epspx using multi_lag
df = stata_multi_lag(df, 'permno', 'time_avail_m', 'epspx', [12, 24], prefix='l', fill_gaps=True)

# Calculate temp variable: (epspx - l12.epspx)/(.5*(abs(l12.epspx) + abs(l24.epspx)))
# Handle division by zero and missing lagged values like Stata (set to missing)
denominator = 0.5 * (abs(df['l12_epspx']) + abs(df['l24_epspx']))
# If any required values are missing, result should be missing (like Stata)
missing_condition = df['epspx'].isna() | df['l12_epspx'].isna() | df['l24_epspx'].isna()
df['temp'] = np.where(
    missing_condition | (denominator == 0), 
    np.nan, 
    (df['epspx'] - df['l12_epspx']) / denominator
)

# Create lagged versions of temp for 12, 24, 36, 48 months using multi_lag
df = stata_multi_lag(df, 'permno', 'time_avail_m', 'temp', [12, 24, 36, 48], prefix='temp', fill_gaps=True)

# Calculate EarningsConsistency as row mean of temp variables
temp_cols = ['temp', 'temp12_temp', 'temp24_temp', 'temp36_temp', 'temp48_temp']
df['EarningsConsistency'] = df[temp_cols].mean(axis=1)

# Create 12-month lag of temp for filtering (already created by multi_lag as temp12_temp)
df['l12_temp'] = df['temp12_temp']

# Apply filters: set EarningsConsistency to missing if:
# 1. abs(epspx/l12.epspx) > 6 OR
# 2. (temp > 0 & l12.temp < 0 & !mi(temp)) OR (temp < 0 & l12.temp > 0 & !mi(temp))
# Handle division by zero in filter condition
epspx_ratio = np.where(df['l12_epspx'] == 0, np.nan, abs(df['epspx'] / df['l12_epspx']))
filter_condition = (
    (epspx_ratio > 6) |
    ((df['temp'] > 0) & (df['l12_temp'] < 0) & df['temp'].notna()) |
    ((df['temp'] < 0) & (df['l12_temp'] > 0) & df['temp'].notna())
)

df.loc[filter_condition, 'EarningsConsistency'] = np.nan

# save predictor
save_predictor(df, 'EarningsConsistency')