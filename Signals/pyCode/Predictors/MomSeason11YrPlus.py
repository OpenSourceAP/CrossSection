# ABOUTME: Translates MomSeason11YrPlus.do to create seasonal return momentum predictor for years 11-15
# ABOUTME: Run from pyCode/ directory: python3 Predictors/MomSeason11YrPlus.py

# Run from pyCode/ directory
# Inputs: SignalMasterTable.parquet
# Output: ../pyData/Predictors/MomSeason11YrPlus.csv

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

# Sort for lag operations
df = df.sort_values(['permno', 'time_avail_m'])

# SIGNAL CONSTRUCTION
# Replace missing returns with 0
df['ret'] = df['ret'].fillna(0)

# Generate calendar-based lags for seasonal returns (131, 143, 155, 167, 179 months)
# Following Stata: foreach n of numlist 131(12)180 { gen temp`n' = l`n'.ret }
lag_periods = list(range(131, 180, 12))  # 131, 143, 155, 167, 179
print(f"Creating calendar-based lags for periods: {lag_periods}")
print("Using stata_multi_lag...")
df = stata_multi_lag(df, 'permno', 'time_avail_m', 'ret', lag_periods)

# Calculate rowtotal and rownonmiss
# Following Stata: egen retTemp1 = rowtotal(temp*), missing
temp_cols = [f'ret_lag{n}' for n in lag_periods]
df['retTemp1'] = df[temp_cols].sum(axis=1, skipna=True)

# Following Stata: egen retTemp2 = rownonmiss(temp*)
df['retTemp2'] = df[temp_cols].notna().sum(axis=1)

# Calculate MomSeason11YrPlus
# Following Stata: gen MomSeason11YrPlus = retTemp1/retTemp2
# Handle division by zero (when retTemp2 = 0, result should be NaN)
df['MomSeason11YrPlus'] = np.where(df['retTemp2'] > 0, df['retTemp1'] / df['retTemp2'], np.nan)

# Keep only necessary columns for output
df_final = df[['permno', 'time_avail_m', 'MomSeason11YrPlus']].copy()
df_final = df_final.dropna(subset=['MomSeason11YrPlus'])

# Convert time_avail_m to yyyymm format like other predictors
df_final['yyyymm'] = df_final['time_avail_m'].dt.year * 100 + df_final['time_avail_m'].dt.month

# Convert to integers for consistency with other predictors
df_final['permno'] = df_final['permno'].astype('int64')
df_final['yyyymm'] = df_final['yyyymm'].astype('int64')

# Keep only required columns and set index
df_final = df_final[['permno', 'yyyymm', 'MomSeason11YrPlus']].copy()
df_final = df_final.set_index(['permno', 'yyyymm'])

# SAVE
df_final.to_csv('../pyData/Predictors/MomSeason11YrPlus.csv')

print("MomSeason11YrPlus predictor saved successfully")