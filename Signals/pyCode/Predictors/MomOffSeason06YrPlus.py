# ABOUTME: Calculates off-season momentum (years 6-10) following Heston and Sadka 2008 Table 2 Years 6-10 Nonannual
# ABOUTME: Run from pyCode/ directory: python3 Predictors/MomOffSeason06YrPlus.py

# Run from pyCode/ directory
# Inputs: SignalMasterTable.parquet
# Output: ../pyData/Predictors/MomOffSeason06YrPlus.csv

import pandas as pd
import numpy as np
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from utils.stata_replication import stata_multi_lag
from utils.asrol import asrol
from utils.save_standardized import save_predictor

print("Starting MomOffSeason06YrPlus.py...")

# DATA LOAD
print("Loading data...")
df = pd.read_parquet('../pyData/Intermediate/SignalMasterTable.parquet')
df = df[['permno', 'time_avail_m', 'ret']].copy()

# SIGNAL CONSTRUCTION
# Replace missing returns with 0
df['ret'] = df['ret'].fillna(0)

# Create lag variables for returns in years 6-10 (71, 83, 95, 107, 119 months)
lag_periods = list(range(71, 120, 12))  # 71, 83, 95, 107, 119
df = stata_multi_lag(df, 'permno', 'time_avail_m', 'ret', lag_periods)

# Calculate sum of lagged returns
lag_cols = [f'ret_lag{n}' for n in lag_periods]
df['retTemp1'] = df[lag_cols].sum(axis=1)
# Handle case where all values are NaN - should return NaN, not 0
all_missing = df[lag_cols].isna().all(axis=1)
df.loc[all_missing, 'retTemp1'] = np.nan

# Count number of non-missing lagged return values
df['retTemp2'] = df[lag_cols].notna().sum(axis=1)

# Create 60-month lagged return for rolling calculations
df = stata_multi_lag(df, 'permno', 'time_avail_m', 'ret', [60])

# Calculate 60-month rolling sum of 60-month lagged returns
df = asrol(df, 'permno', 'time_avail_m', '1mo', 60, 'ret_lag60', 'sum', 'retLagTemp_sum60', min_samples=1)

# Calculate 60-month rolling count of 60-month lagged returns
df = asrol(df, 'permno', 'time_avail_m', '1mo', 60, 'ret_lag60', 'count', 'retLagTemp_count60', min_samples=1)

# Calculate off-season momentum for years 6-10 as difference in average returns
df['MomOffSeason06YrPlus'] = (df['retLagTemp_sum60'] - df['retTemp1']) / (df['retLagTemp_count60'] - df['retTemp2'])

# SAVE
print(f"Calculated MomOffSeason06YrPlus for {df['MomOffSeason06YrPlus'].notna().sum()} observations")

save_predictor(df, 'MomOffSeason06YrPlus')
print("MomOffSeason06YrPlus.py completed successfully")