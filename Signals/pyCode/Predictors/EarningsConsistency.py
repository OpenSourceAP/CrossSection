# ABOUTME: Translates EarningsConsistency.do from Stata to Python
# ABOUTME: Calculates earnings consistency measure based on standardized earnings changes

# How to run: python3 EarningsConsistency.py
# Inputs: ../pyData/Intermediate/m_aCompustat.parquet
# Outputs: ../pyData/Predictors/EarningsConsistency.csv

import pandas as pd
import numpy as np

# DATA LOAD
df = pd.read_parquet('../pyData/Intermediate/m_aCompustat.parquet', 
                     columns=['permno', 'time_avail_m', 'epspx'])

# SIGNAL CONSTRUCTION
# Sort data (equivalent to xtset permno time_avail_m)
df = df.sort_values(['permno', 'time_avail_m'])

# Create 12-month and 24-month lags of epspx using merge-based calendar approach
def create_calendar_lag_merge(df, column, lag_months):
    """Create calendar-based lag using merge approach (faster)"""
    df_copy = df[['permno', 'time_avail_m', column]].copy()
    df_copy['lag_time'] = df_copy['time_avail_m'] + pd.DateOffset(months=lag_months)
    df_copy = df_copy.rename(columns={column: f'lag{lag_months}_{column}'})
    
    result = df.merge(df_copy[['permno', 'lag_time', f'lag{lag_months}_{column}']], 
                     left_on=['permno', 'time_avail_m'], 
                     right_on=['permno', 'lag_time'], 
                     how='left')
    return result[f'lag{lag_months}_{column}']

df['l12_epspx'] = create_calendar_lag_merge(df, 'epspx', 12)
df['l24_epspx'] = create_calendar_lag_merge(df, 'epspx', 24)

# Calculate temp variable: (epspx - l12.epspx)/(.5*(abs(l12.epspx) + abs(l24.epspx)))
# Handle division by zero like Stata (set to missing)
denominator = 0.5 * (abs(df['l12_epspx']) + abs(df['l24_epspx']))
df['temp'] = np.where(denominator == 0, np.nan, (df['epspx'] - df['l12_epspx']) / denominator)

# Create lagged versions of temp for 12, 24, 36, 48 months using calendar-based approach
for n in [12, 24, 36, 48]:
    df[f'temp{n}'] = create_calendar_lag_merge(df, 'temp', n)

# Calculate EarningsConsistency as row mean of temp variables
temp_cols = ['temp', 'temp12', 'temp24', 'temp36', 'temp48']
df['EarningsConsistency'] = df[temp_cols].mean(axis=1)

# Create 12-month lag of temp for filtering using calendar-based approach
df['l12_temp'] = create_calendar_lag_merge(df, 'temp', 12)

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

# Create yyyymm variable
df['yyyymm'] = (df['time_avail_m'].dt.year * 100 + df['time_avail_m'].dt.month).astype(int)

# Keep only required columns and remove missing values
result = df[['permno', 'yyyymm', 'EarningsConsistency']].dropna()

# Save the predictor
result.to_csv('../pyData/Predictors/EarningsConsistency.csv', index=False)