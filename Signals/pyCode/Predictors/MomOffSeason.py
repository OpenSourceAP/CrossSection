# ABOUTME: Translates MomOffSeason.do to create off-season long-term reversal
# ABOUTME: Run from pyCode/ directory: python3 Predictors/MomOffSeason.py

# Run from pyCode/ directory
# Inputs: SignalMasterTable.parquet
# Output: ../pyData/Predictors/MomOffSeason.csv

import pandas as pd
import numpy as np
import sys
sys.path.append('.')
from utils.stata_replication import stata_multi_lag
from utils.asrol import asrol
from utils.savepredictor import save_predictor

# DATA LOAD
df = pd.read_parquet('../pyData/Intermediate/SignalMasterTable.parquet')
df = df[['permno', 'time_avail_m', 'ret']].copy()

# SIGNAL CONSTRUCTION
# replace ret = 0 if mi(ret)
df['ret'] = df['ret'].fillna(0)

# foreach n of numlist 23(12)59 { gen temp`n' = l`n'.ret }
# This creates lags for periods: 23, 35, 47, 59 months
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
df = asrol(df, 'permno', 'time_avail_m', 'ret_lag12', 48, 'sum', 'retLagTemp_sum48', min_periods=1)

# asrol retLagTemp, by(permno) window(time_avail_m 48) stat(count) minimum(1) gen(retLagTemp_count48)
df = asrol(df, 'permno', 'time_avail_m', 'ret_lag12', 48, 'count', 'retLagTemp_count48', min_periods=1)

# gen MomOffSeason = (retLagTemp_sum48 - retTemp1)/(retLagTemp_count48 - retTemp2)
df['MomOffSeason'] = (df['retLagTemp_sum48'] - df['retTemp1']) / (df['retLagTemp_count48'] - df['retTemp2'])

# SAVE
save_predictor(df, 'MomOffSeason')