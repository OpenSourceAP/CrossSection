# ABOUTME: Calculates off-season long-term reversal following Heston and Sadka 2008 Table 2 Years 2-5 Nonannual
# ABOUTME: Run from pyCode/ directory: python3 Predictors/MomOffSeason.py

# Run from pyCode/ directory
# Inputs: SignalMasterTable.parquet
# Output: ../pyData/Predictors/MomOffSeason.csv

import pandas as pd
import numpy as np
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from utils.stata_replication import stata_multi_lag
from utils.asrol import asrol
from utils.save_standardized import save_predictor

print("Starting MomOffSeason.py...")

# DATA LOAD
print("Loading SignalMasterTable...")
df = pd.read_parquet('../pyData/Intermediate/SignalMasterTable.parquet')
df = df[['permno', 'time_avail_m', 'ret']].copy()
print(f"Loaded data: {df.shape[0]} rows")

# SIGNAL CONSTRUCTION
print("Filling missing returns with 0...")
# Replace missing returns with 0
df['ret'] = df['ret'].fillna(0)

# Create lag variables for returns at specific intervals (23, 35, 47, 59 months)
print("Creating lag variables for returns (23, 35, 47, 59 months)...")
lag_periods = [23, 35, 47, 59]
df = stata_multi_lag(df, 'permno', 'time_avail_m', 'ret', lag_periods)

# Calculate sum of lagged returns
lag_cols = [f'ret_lag{n}' for n in lag_periods]
df['retTemp1'] = df[lag_cols].sum(axis=1)
# Handle case where all values are NaN - should return NaN, not 0
all_missing = df[lag_cols].isna().all(axis=1)
df.loc[all_missing, 'retTemp1'] = np.nan

# Count number of non-missing lagged return values
df['retTemp2'] = df[lag_cols].notna().sum(axis=1)

# Create 12-month lagged return for rolling calculations
df = stata_multi_lag(df, 'permno', 'time_avail_m', 'ret', [12])

# Calculate 48-month rolling sum of 12-month lagged returns
df = asrol(df, 'permno', 'time_avail_m', '1mo', 48, 'ret_lag12', 'sum', 'retLagTemp_sum48', min_samples=1)

# Calculate 48-month rolling count of 12-month lagged returns
df = asrol(df, 'permno', 'time_avail_m', '1mo', 48, 'ret_lag12', 'count', 'retLagTemp_count48', min_samples=1)

print("Calculating MomOffSeason signal...")
# Calculate off-season momentum as difference in average returns
df['MomOffSeason'] = (df['retLagTemp_sum48'] - df['retTemp1']) / (df['retLagTemp_count48'] - df['retTemp2'])
print(f"Calculated MomOffSeason for {df['MomOffSeason'].notna().sum()} observations")

# SAVE
save_predictor(df, 'MomOffSeason')
print("MomOffSeason.py completed successfully")