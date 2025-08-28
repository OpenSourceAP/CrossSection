# ABOUTME: Translates MomSeasonShort.do to create short-term seasonal momentum
# ABOUTME: Run from pyCode/ directory: python3 Predictors/MomSeasonShort.py

# Run from pyCode/ directory
# Inputs: SignalMasterTable.parquet
# Output: ../pyData/Predictors/MomSeasonShort.csv

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

# gen MomSeasonShort = l11.ret
df = stata_multi_lag(df, 'permno', 'time_avail_m', 'ret', [11])
df['MomSeasonShort'] = df['ret_lag11']

# SAVE
save_predictor(df, 'MomSeasonShort')