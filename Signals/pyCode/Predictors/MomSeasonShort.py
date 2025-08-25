# ABOUTME: Return seasonality last year predictor translation from Stata
# ABOUTME: Calculates MomSeasonShort as 11-month lagged return

# Run from pyCode/ directory
# Inputs: SignalMasterTable.parquet
# Output: ../pyData/Predictors/MomSeasonShort.csv

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
# Replace missing returns with 0 (equivalent to Stata: replace ret = 0 if mi(ret))
df['ret'] = df['ret'].fillna(0)

# Generate MomSeasonShort = l11.ret (11-month lag of ret)
# Use stata_multi_lag to create 11-month lag efficiently
print("Creating 11-month lag using stata_multi_lag...")
df = stata_multi_lag(df, 'permno', 'time_avail_m', 'ret', [11])

# Assign MomSeasonShort from the calendar-based lag
df['MomSeasonShort'] = df['ret_lag11']

# Keep only necessary columns for output
df_final = df[['permno', 'time_avail_m', 'MomSeasonShort']].copy()
df_final = df_final.dropna(subset=['MomSeasonShort'])

# Convert time_avail_m to yyyymm format like other predictors
df_final['yyyymm'] = df_final['time_avail_m'].dt.year * 100 + df_final['time_avail_m'].dt.month

# Convert to integers for consistency with other predictors
df_final['permno'] = df_final['permno'].astype('int64')
df_final['yyyymm'] = df_final['yyyymm'].astype('int64')

# Keep only required columns and set index
df_final = df_final[['permno', 'yyyymm', 'MomSeasonShort']].copy()
df_final = df_final.set_index(['permno', 'yyyymm'])

# SAVE
df_final.to_csv('../pyData/Predictors/MomSeasonShort.csv')

print("MomSeasonShort predictor saved successfully")
print(f"Output shape: {df_final.shape}")