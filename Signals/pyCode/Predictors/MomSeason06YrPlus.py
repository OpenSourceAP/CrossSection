# ABOUTME: Translates MomSeason06YrPlus.do to create seasonal momentum (years 6-10)
# ABOUTME: Run from pyCode/ directory: python3 Predictors/MomSeason06YrPlus.py

# Run from pyCode/ directory
# Inputs: SignalMasterTable.parquet
# Output: ../pyData/Predictors/MomSeason06YrPlus.csv

import pandas as pd
import numpy as np
import sys
sys.path.append('.')
from utils.stata_replication import stata_multi_lag
from utils.savepredictor import save_predictor

# DATA LOAD
df = pd.read_parquet('../pyData/Intermediate/SignalMasterTable.parquet')
df = df[['permno', 'time_avail_m', 'ret']].copy()

# SIGNAL CONSTRUCTION
# replace ret = 0 if mi(ret)
df['ret'] = df['ret'].fillna(0)

# foreach n of numlist 71(12)120 { gen temp`n' = l`n'.ret }
# This creates lags for periods: 71, 83, 95, 107, 119 months
lag_periods = list(range(71, 121, 12))  # 71, 83, 95, 107, 119
df = stata_multi_lag(df, 'permno', 'time_avail_m', 'ret', lag_periods)

# egen retTemp1 = rowtotal(temp*), missing
lag_cols = [f'ret_lag{n}' for n in lag_periods]
df['retTemp1'] = df[lag_cols].sum(axis=1)
# Handle case where all values are NaN - should return NaN, not 0
all_missing = df[lag_cols].isna().all(axis=1)
df.loc[all_missing, 'retTemp1'] = np.nan

# egen retTemp2 = rownonmiss(temp*)
df['retTemp2'] = df[lag_cols].notna().sum(axis=1)

# gen MomSeason06YrPlus = retTemp1/retTemp2
df['MomSeason06YrPlus'] = df['retTemp1'] / df['retTemp2']

# SAVE
save_predictor(df, 'MomSeason06YrPlus')