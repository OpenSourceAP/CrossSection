# ABOUTME: Translates Mom12mOffSeason.do to create twelve-month momentum without seasonal part
# ABOUTME: Run from pyCode/ directory: python3 Predictors/Mom12mOffSeason.py

# Run from pyCode/ directory
# Inputs: SignalMasterTable.parquet
# Output: ../pyData/Predictors/Mom12mOffSeason.csv

import pandas as pd
import numpy as np
import sys
sys.path.append('.')
from utils.asrol import asrol
from utils.savepredictor import save_predictor

# DATA LOAD
df = pd.read_parquet('../pyData/Intermediate/SignalMasterTable.parquet')
df = df[['permno', 'time_avail_m', 'ret']].copy()

# SIGNAL CONSTRUCTION
# replace ret = 0 if mi(ret)
df['ret'] = df['ret'].fillna(0)

# asrol ret, by(permno) window(time_avail_m 10) stat(mean) minimum(6) gen(Mom12mOffSeason) xf(focal)
# xf(focal) excludes focal (most recent) return
df = asrol(df, 'permno', 'time_avail_m', 'ret', 10, 'mean', 'Mom12mOffSeason', min_periods=6, exclude_focal=True)

# SAVE
save_predictor(df, 'Mom12mOffSeason')