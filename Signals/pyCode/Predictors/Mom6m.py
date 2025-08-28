# ABOUTME: Translates Mom6m.do to create six-month momentum predictor
# ABOUTME: Run from pyCode/ directory: python3 Predictors/Mom6m.py

# Run from pyCode/ directory
# Inputs: SignalMasterTable.parquet
# Output: ../pyData/Predictors/Mom6m.csv

import pandas as pd
import numpy as np
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils.stata_replication import stata_multi_lag
from utils.save_standardized import save_predictor

# DATA LOAD
df = pd.read_parquet('../pyData/Intermediate/SignalMasterTable.parquet')
df = df[['permno', 'time_avail_m', 'ret']].copy()

# Sort for lag operations
df = df.sort_values(['permno', 'time_avail_m'])

# SIGNAL CONSTRUCTION
# Replace missing returns with 0
df['ret'] = df['ret'].fillna(0)

# Calculate lags using stata_multi_lag for calendar validation
df = stata_multi_lag(df, 'permno', 'time_avail_m', 'ret', [1, 2, 3, 4, 5])

# Calculate 6-month momentum (geometric return)
df['Mom6m'] = ((1 + df['ret_lag1']) * 
               (1 + df['ret_lag2']) * 
               (1 + df['ret_lag3']) * 
               (1 + df['ret_lag4']) * 
               (1 + df['ret_lag5'])) - 1

# Keep only necessary columns for output
df_final = df[['permno', 'time_avail_m', 'Mom6m']].copy()

# SAVE
save_predictor(df_final, 'Mom6m')