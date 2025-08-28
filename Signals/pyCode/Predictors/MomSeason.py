# ABOUTME: Translates MomSeason.do to create seasonal momentum (years 2 to 5)
# ABOUTME: Run from pyCode/ directory: python3 Predictors/MomSeason.py

# Run from pyCode/ directory
# Inputs: SignalMasterTable.parquet
# Output: ../pyData/Predictors/MomSeason.csv

import pandas as pd
import numpy as np
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from utils.stata_replication import stata_multi_lag
from utils.save_standardized import save_predictor

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

# gen MomSeason = retTemp1/retTemp2
df['MomSeason'] = df['retTemp1'] / df['retTemp2']

# SAVE
save_predictor(df, 'MomSeason')