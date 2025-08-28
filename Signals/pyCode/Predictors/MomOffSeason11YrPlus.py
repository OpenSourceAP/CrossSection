# ABOUTME: Translates MomOffSeason11YrPlus.do to create off-season momentum for years 11-15
# ABOUTME: Run from pyCode/ directory: python3 Predictors/MomOffSeason11YrPlus.py

# Run from pyCode/ directory
# Inputs: SignalMasterTable.parquet
# Output: ../pyData/Predictors/MomOffSeason11YrPlus.csv

import pandas as pd
import numpy as np
import sys
sys.path.append('.')
from utils.stata_replication import stata_multi_lag
from utils.stata_asreg_asrol import asrol
from utils.savepredictor import save_predictor

# DATA LOAD
df = pd.read_parquet('../pyData/Intermediate/SignalMasterTable.parquet')
df = df[['permno', 'time_avail_m', 'ret']].copy()

# SIGNAL CONSTRUCTION
# replace ret = 0 if mi(ret)
df['ret'] = df['ret'].fillna(0)

# foreach n of numlist 131(12)179 { gen temp`n' = l`n'.ret }
# This creates lags for periods: 131, 143, 155, 167, 179 months
lag_periods = list(range(131, 180, 12))  # 131, 143, 155, 167, 179
df = stata_multi_lag(df, 'permno', 'time_avail_m', 'ret', lag_periods)

# egen retTemp1 = rowtotal(temp*), missing
lag_cols = [f'ret_lag{n}' for n in lag_periods]
df['retTemp1'] = df[lag_cols].sum(axis=1)
# Handle case where all values are NaN - should return NaN, not 0
all_missing = df[lag_cols].isna().all(axis=1)
df.loc[all_missing, 'retTemp1'] = np.nan

# egen retTemp2 = rownonmiss(temp*)
df['retTemp2'] = df[lag_cols].notna().sum(axis=1)

# gen retLagTemp = l120.ret
df = stata_multi_lag(df, 'permno', 'time_avail_m', 'ret', [120])

# asrol retLagTemp, by(permno) window(time_avail_m 60) stat(sum) minimum(1) gen(retLagTemp_sum60)
df = asrol(df, 'permno', 'time_avail_m', 'ret_lag120', 60, 'sum', 'retLagTemp_sum60', min_periods=1)

# asrol retLagTemp, by(permno) window(time_avail_m 60) stat(count) minimum(1) gen(retLagTemp_count60)
df = asrol(df, 'permno', 'time_avail_m', 'ret_lag120', 60, 'count', 'retLagTemp_count60', min_periods=1)

# gen MomOffSeason11YrPlus = (retLagTemp_sum60 - retTemp1)/(retLagTemp_count60 - retTemp2)
df['MomOffSeason11YrPlus'] = (df['retLagTemp_sum60'] - df['retTemp1']) / (df['retLagTemp_count60'] - df['retTemp2'])

# SAVE
save_predictor(df, 'MomOffSeason11YrPlus')