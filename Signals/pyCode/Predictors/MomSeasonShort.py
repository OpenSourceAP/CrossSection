# ABOUTME: Translates MomSeasonShort.do to create short-term seasonal momentum
# ABOUTME: Run from pyCode/ directory: python3 Predictors/MomSeasonShort.py

# Run from pyCode/ directory
# Inputs: SignalMasterTable.parquet
# Output: ../pyData/Predictors/MomSeasonShort.csv

import pandas as pd
import numpy as np
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from utils.stata_replication import stata_multi_lag
from utils.save_standardized import save_predictor

print("Starting MomSeasonShort.py...")

# DATA LOAD
print("Loading SignalMasterTable...")
df = pd.read_parquet('../pyData/Intermediate/SignalMasterTable.parquet')
df = df[['permno', 'time_avail_m', 'ret']].copy()
print(f"Loaded data: {df.shape[0]} rows")

# SIGNAL CONSTRUCTION
print("Filling missing returns with 0...")
# replace ret = 0 if mi(ret)
df['ret'] = df['ret'].fillna(0)

# gen MomSeasonShort = l11.ret
print("Creating 11-month lag for seasonal momentum...")
df = stata_multi_lag(df, 'permno', 'time_avail_m', 'ret', [11])
df['MomSeasonShort'] = df['ret_lag11']
print(f"Calculated MomSeasonShort for {df['MomSeasonShort'].notna().sum()} observations")

# SAVE
save_predictor(df, 'MomSeasonShort')
print("MomSeasonShort.py completed successfully")