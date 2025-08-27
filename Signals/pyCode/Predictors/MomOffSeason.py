# ABOUTME: Translates MomOffSeason predictor from Stata to Python
# ABOUTME: Creates off-season long-term reversal by removing seasonal components

import pandas as pd
import numpy as np
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from utils.stata_replication import stata_multi_lag
from utils.stata_asreg_asrol import asrol
from utils.savepredictor import save_predictor

print("Starting MomOffSeason predictor translation...")

# DATA LOAD
# use permno time_avail_m ret using "$pathDataIntermediate/SignalMasterTable", clear
print("Loading SignalMasterTable...")
df = pd.read_parquet('../pyData/Intermediate/SignalMasterTable.parquet')
df = df[['permno', 'time_avail_m', 'ret']].copy()
print(f"Loaded {len(df)} observations")

# Sort data by permno and time_avail_m (equivalent to xtset)
df = df.sort_values(['permno', 'time_avail_m'])
print("Data sorted by permno and time_avail_m")

# SIGNAL CONSTRUCTION
print("Starting signal construction...")

# replace ret = 0 if mi(ret)
df['ret'] = df['ret'].fillna(0)
print("Replaced missing returns with 0")

# foreach n of numlist 23(12)59 {
#     gen temp`n' = l`n'.ret
# }
# This creates lags for periods: 23, 35, 47, 59 months
lag_periods = [23, 35, 47, 59]
print(f"Creating seasonal lags for periods: {lag_periods}")
df = stata_multi_lag(df, 'permno', 'time_avail_m', 'ret', lag_periods)

# Rename lag columns to match Stata temp variable names
for n in lag_periods:
    df[f'temp{n}'] = df[f'ret_lag{n}']

temp_vars = [f'temp{n}' for n in lag_periods]

# egen retTemp1 = rowtotal(temp*), missing
# The 'missing' option means if all values are missing, return missing (not 0)
df['retTemp1'] = df[temp_vars].sum(axis=1)
# Handle case where all values are NaN - should return NaN, not 0
all_missing = df[temp_vars].isna().all(axis=1)
df.loc[all_missing, 'retTemp1'] = np.nan
print("Calculated retTemp1 (seasonal row total)")

# egen retTemp2 = rownonmiss(temp*)
df['retTemp2'] = df[temp_vars].notna().sum(axis=1)
print("Calculated retTemp2 (seasonal row non-missing count)")

# gen retLagTemp = l12.ret
print("Creating retLagTemp (lag 12 months)...")
df = stata_multi_lag(df, 'permno', 'time_avail_m', 'ret', [12])
df['retLagTemp'] = df['ret_lag12']

# Create time index for asrol (requires integer time variable)
df = df.sort_values(['permno', 'time_avail_m'])
df['time_temp'] = df.groupby('permno').cumcount() + 1

# asrol retLagTemp, by(permno) window(time_avail_m 48) stat(sum) minimum(1) gen(retLagTemp_sum48)
print("Calculating 48-month rolling sum using asrol...")
df = asrol(
    df,
    group_col='permno',
    time_col='time_temp', 
    value_col='retLagTemp',
    window=48,
    stat='sum',
    new_col_name='retLagTemp_sum48',
    min_periods=1
)

# asrol retLagTemp, by(permno) window(time_avail_m 48) stat(count) minimum(1) gen(retLagTemp_count48)
print("Calculating 48-month rolling count using asrol...")
df = asrol(
    df,
    group_col='permno',
    time_col='time_temp',
    value_col='retLagTemp', 
    window=48,
    stat='count',
    new_col_name='retLagTemp_count48',
    min_periods=1
)

# gen MomOffSeason = (retLagTemp_sum48 - retTemp1)/(retLagTemp_count48 - retTemp2)
df['MomOffSeason'] = (df['retLagTemp_sum48'] - df['retTemp1']) / (df['retLagTemp_count48'] - df['retTemp2'])
# Handle division by zero - when denominator is 0, result should be NaN
df.loc[(df['retLagTemp_count48'] - df['retTemp2']) == 0, 'MomOffSeason'] = np.nan
print("Calculated MomOffSeason predictor")

# save
save_predictor(df, 'MomOffSeason')