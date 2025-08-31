# ABOUTME: Calculates off-season momentum (years 11-15) following Heston and Sadka 2008 Table 2 Years 11-15 Nonannual
# ABOUTME: Run from pyCode/ directory: python3 Predictors/MomOffSeason11YrPlus.py

# Run from pyCode/ directory
# Inputs: SignalMasterTable.parquet
# Output: ../pyData/Predictors/MomOffSeason11YrPlus.csv

import pandas as pd
import numpy as np
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from utils.stata_replication import stata_multi_lag
from utils.asrol import asrol
from utils.save_standardized import save_predictor

print("Starting MomOffSeason11YrPlus.py...")

# DATA LOAD
print("Loading data...")
df = pd.read_parquet('../pyData/Intermediate/SignalMasterTable.parquet')
df = df[['permno', 'time_avail_m', 'ret']].copy()

# SIGNAL CONSTRUCTION
# Update 0 if mi(ret)
df['ret'] = df['ret'].fillna(0)

# foreach n of numlist 131(12)179 { Generate l`n'.ret }
# This creates lags for periods: 131, 143, 155, 167, 179 months
lag_periods = list(range(131, 180, 12))  # 131, 143, 155, 167, 179
df = stata_multi_lag(df, 'permno', 'time_avail_m', 'ret', lag_periods)

# eGenerate rowtotal(temp*), missing
lag_cols = [f'ret_lag{n}' for n in lag_periods]
df['retTemp1'] = df[lag_cols].sum(axis=1)
# Handle case where all values are NaN - should return NaN, not 0
all_missing = df[lag_cols].isna().all(axis=1)
df.loc[all_missing, 'retTemp1'] = np.nan

# eGenerate rownonmiss(temp*)
df['retTemp2'] = df[lag_cols].notna().sum(axis=1)

# Generate l120.ret
df = stata_multi_lag(df, 'permno', 'time_avail_m', 'ret', [120])

# asrol retLagTemp, by(permno) window(time_avail_m 60) stat(sum) minimum(1) gen(retLagTemp_sum60)
df = asrol(df, 'permno', 'time_avail_m', '1mo', 60, 'ret_lag120', 'sum', 'retLagTemp_sum60', min_samples=1)

# asrol retLagTemp, by(permno) window(time_avail_m 60) stat(count) minimum(1) gen(retLagTemp_count60)
df = asrol(df, 'permno', 'time_avail_m', '1mo', 60, 'ret_lag120', 'count', 'retLagTemp_count60', min_samples=1)

# Generate (retLagTemp_sum60 - retTemp1)/(retLagTemp_count60 - retTemp2)
df['MomOffSeason11YrPlus'] = (df['retLagTemp_sum60'] - df['retTemp1']) / (df['retLagTemp_count60'] - df['retTemp2'])

# SAVE
print(f"Calculated MomOffSeason11YrPlus for {df['MomOffSeason11YrPlus'].notna().sum()} observations")

save_predictor(df, 'MomOffSeason11YrPlus')
print("MomOffSeason11YrPlus.py completed successfully")