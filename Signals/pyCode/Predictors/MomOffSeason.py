# ABOUTME: Translates MomOffSeason.do to create off-season long-term reversal
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
from utils.asrol import asrol_fast
from utils.save_standardized import save_predictor

print("Starting MomOffSeason.py...")

# DATA LOAD
print("Loading SignalMasterTable...")
df = pd.read_parquet('../pyData/Intermediate/SignalMasterTable.parquet')
df = df[['permno', 'time_avail_m', 'ret']].copy()
print(f"Loaded data: {df.shape[0]} rows")

# SIGNAL CONSTRUCTION
print("Filling missing returns with 0...")
# replace ret = 0 if mi(ret)
df['ret'] = df['ret'].fillna(0)

# foreach n of numlist 23(12)59 { gen temp`n' = l`n'.ret }
# This creates lags for periods: 23, 35, 47, 59 months
print("Creating lag variables for returns (23, 35, 47, 59 months)...")
lag_periods = [23, 35, 47, 59]
df = stata_multi_lag(df, 'permno', 'time_avail_m', 'ret', lag_periods)

# egen retTemp1 = rowtotal(temp*), missing
lag_cols = [f'ret_lag{n}' for n in lag_periods]
df['retTemp1'] = df[lag_cols].sum(axis=1)
# Handle case where all values are NaN - should return NaN, not 0
all_missing = df[lag_cols].isna().all(axis=1)
df.loc[all_missing, 'retTemp1'] = np.nan

# egen retTemp2 = rownonmiss(temp*)
df['retTemp2'] = df[lag_cols].notna().sum(axis=1)

# gen retLagTemp = l12.ret
df = stata_multi_lag(df, 'permno', 'time_avail_m', 'ret', [12])

# asrol retLagTemp, by(permno) window(time_avail_m 48) stat(sum) minimum(1) gen(retLagTemp_sum48)
df = asrol_fast(df, 'permno', 'time_avail_m', 'ret_lag12', 48, 'sum', 'retLagTemp_sum48', min_periods=1)

# asrol retLagTemp, by(permno) window(time_avail_m 48) stat(count) minimum(1) gen(retLagTemp_count48)
df = asrol_fast(df, 'permno', 'time_avail_m', 'ret_lag12', 48, 'count', 'retLagTemp_count48', min_periods=1)

print("Calculating MomOffSeason signal...")
# gen MomOffSeason = (retLagTemp_sum48 - retTemp1)/(retLagTemp_count48 - retTemp2)
df['MomOffSeason'] = (df['retLagTemp_sum48'] - df['retTemp1']) / (df['retLagTemp_count48'] - df['retTemp2'])
print(f"Calculated MomOffSeason for {df['MomOffSeason'].notna().sum()} observations")

# SAVE
save_predictor(df, 'MomOffSeason')
print("MomOffSeason.py completed successfully")