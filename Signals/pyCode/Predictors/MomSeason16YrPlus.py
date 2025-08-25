# ABOUTME: Return Seasonality (16-20 years) predictor translation from Stata
# ABOUTME: Calculates seasonal momentum by averaging returns from lags 191, 203, 215, 227, 239 months

import pandas as pd
import numpy as np
import sys
import os

# Add parent directory to path for any shared utilities
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from utils.stata_replication import stata_multi_lag

# DATA LOAD
df = pd.read_parquet('../pyData/Intermediate/SignalMasterTable.parquet')
df = df[['permno', 'time_avail_m', 'ret']].copy()

# Sort data for lag operations
df = df.sort_values(['permno', 'time_avail_m'])

# SIGNAL CONSTRUCTION
# Replace missing returns with 0 (equivalent to Stata: replace ret = 0 if mi(ret))
df['ret'] = df['ret'].fillna(0)

# Create time-based lags for months 191(12)240 (191, 203, 215, 227, 239)
# This matches Stata's numlist pattern 191(12)240 which generates 191, 191+12=203, 191+24=215, 191+36=227, 191+48=239
# Use stata_multi_lag to create multiple lags efficiently
lag_periods = [191, 203, 215, 227, 239]
print(f"Creating time-based lags for periods: {lag_periods}")
print("Using stata_multi_lag...")
df = stata_multi_lag(df, 'permno', 'time_avail_m', 'ret', lag_periods)

# Get list of temp columns
temp_cols = [f'ret_lag{n}' for n in lag_periods]

# Calculate row total and row non-missing count (equivalent to Stata egen commands)
# egen retTemp1 = rowtotal(temp*), missing
df['retTemp1'] = df[temp_cols].sum(axis=1, skipna=True)

# egen retTemp2 = rownonmiss(temp*)  
df['retTemp2'] = df[temp_cols].notna().sum(axis=1)

# Generate MomSeason16YrPlus = retTemp1/retTemp2
df['MomSeason16YrPlus'] = df['retTemp1'] / df['retTemp2']

# Set to NaN where retTemp2 is 0 to handle division by zero
df.loc[df['retTemp2'] == 0, 'MomSeason16YrPlus'] = np.nan

# SAVE
# Clean up - drop rows where MomSeason16YrPlus is missing (equivalent to Stata: drop if MomSeason16YrPlus == .)
df_clean = df.dropna(subset=['MomSeason16YrPlus']).copy()

# Convert time_avail_m to yyyymm format (equivalent to Stata date conversion)
df_clean['yyyymm'] = pd.to_datetime(df_clean['time_avail_m']).dt.year * 100 + pd.to_datetime(df_clean['time_avail_m']).dt.month

# Keep only required columns and ensure correct order
df_output = df_clean[['permno', 'yyyymm', 'MomSeason16YrPlus']].copy()

# Save to CSV
output_path = '../pyData/Predictors/MomSeason16YrPlus.csv'
os.makedirs(os.path.dirname(output_path), exist_ok=True)
df_output.to_csv(output_path, index=False)

print(f"MomSeason16YrPlus predictor saved to {output_path}")
print(f"Output shape: {df_output.shape}")
print("First few rows:")
print(df_output.head())