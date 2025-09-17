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
from utils.save_standardized import save_predictor

print("Starting MomOffSeason06YrPlus.py...")

# DATA LOAD
print("Loading data...")
df = pd.read_parquet('../pyData/Intermediate/SignalMasterTable.parquet')
df = df[['permno', 'time_avail_m', 'ret']].copy()

# SIGNAL CONSTRUCTION
# Replace missing returns with 0
df['ret'] = df['ret'].fillna(0)

# Years 6-10 before predicted month = months 61-120 before time_predict_m
# time_predict_m = time_avail_m + 1 month (the month we're predicting)
# So we need lags 60-119 from time_avail_m

# Exclude same calendar month as predicted month (lags 71, 83, 95, 107, 119)
same_month_lags = [71, 83, 95, 107, 119]
off_season_lags = [lag for lag in range(60, 120) if lag not in same_month_lags]

print(f"Creating {len(off_season_lags)} off-season lag variables...")
df = stata_multi_lag(df, 'permno', 'time_avail_m', 'ret', off_season_lags)

# Average returns from years 6-10, excluding same calendar month
lag_cols = [f'ret_lag{n}' for n in off_season_lags]
df['MomOffSeason06YrPlus'] = df[lag_cols].mean(axis=1)

# Force to NA if all lag values are missing
all_missing = df[lag_cols].isna().all(axis=1)
df.loc[all_missing, 'MomOffSeason06YrPlus'] = np.nan

# SAVE
print(f"Calculated MomOffSeason06YrPlus for {df['MomOffSeason06YrPlus'].notna().sum()} observations")

save_predictor(df, 'MomOffSeason06YrPlus')
print("MomOffSeason06YrPlus.py completed successfully")