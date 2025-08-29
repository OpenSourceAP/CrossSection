# ABOUTME: Translates MomOffSeason16YrPlus.do to create off-season momentum for years 16-20
# ABOUTME: Run from pyCode/ directory: python3 Predictors/MomOffSeason16YrPlus.py

# Run from pyCode/ directory
# Inputs: SignalMasterTable.parquet
# Output: ../pyData/Predictors/MomOffSeason16YrPlus.csv

import pandas as pd
import numpy as np
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from utils.stata_replication import stata_multi_lag
from utils.asrol import asrol
from utils.save_standardized import save_predictor

print("Starting MomOffSeason16YrPlus.py...")

# DATA LOAD
print("Loading data...")
df = pd.read_parquet('../pyData/Intermediate/SignalMasterTable.parquet')
df = df[['permno', 'time_avail_m', 'ret']].copy()

# SIGNAL CONSTRUCTION
# replace ret = 0 if mi(ret)
df['ret'] = df['ret'].fillna(0)

# foreach n of numlist 191(12)239 { gen temp`n' = l`n'.ret }
# This creates lags for periods: 191, 203, 215, 227, 239 months
lag_periods = list(range(191, 240, 12))  # 191, 203, 215, 227, 239
df = stata_multi_lag(df, 'permno', 'time_avail_m', 'ret', lag_periods)

# egen retTemp1 = rowtotal(temp*), missing
lag_cols = [f'ret_lag{n}' for n in lag_periods]
df['retTemp1'] = df[lag_cols].sum(axis=1)
# Handle case where all values are NaN - should return NaN, not 0
all_missing = df[lag_cols].isna().all(axis=1)
df.loc[all_missing, 'retTemp1'] = np.nan

# egen retTemp2 = rownonmiss(temp*)
df['retTemp2'] = df[lag_cols].notna().sum(axis=1)

# gen retLagTemp = l180.ret
df = stata_multi_lag(df, 'permno', 'time_avail_m', 'ret', [180])

# asrol retLagTemp, by(permno) window(time_avail_m 60) stat(sum) minimum(36) gen(sum60_retLagTemp)
df = asrol(df, 'permno', 'time_avail_m', '1mo', 60, 'ret_lag180', 'sum', 'sum60_retLagTemp', min_samples=36)

# asrol retLagTemp, by(permno) window(time_avail_m 60) stat(count) minimum(36) gen(count60_retLagTemp)
df = asrol(df, 'permno', 'time_avail_m', '1mo', 60, 'ret_lag180', 'count', 'count60_retLagTemp', min_samples=36)

# gen MomOffSeason16YrPlus = (sum60_retLagTemp - retTemp1)/(count60_retLagTemp - retTemp2)
df['MomOffSeason16YrPlus'] = (df['sum60_retLagTemp'] - df['retTemp1']) / (df['count60_retLagTemp'] - df['retTemp2'])

# SAVE
print(f"Calculated MomOffSeason16YrPlus for {df['MomOffSeason16YrPlus'].notna().sum()} observations")

save_predictor(df, 'MomOffSeason16YrPlus')
print("MomOffSeason16YrPlus.py completed successfully")