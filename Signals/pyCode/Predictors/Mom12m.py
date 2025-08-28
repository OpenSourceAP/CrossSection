# ABOUTME: Translates Mom12m.do to create twelve-month momentum predictor
# ABOUTME: Run from pyCode/ directory: python3 Predictors/Mom12m.py

# Run from pyCode/ directory
# Inputs: SignalMasterTable.parquet
# Output: ../pyData/Predictors/Mom12m.csv

import pandas as pd
import numpy as np
import sys
import os
sys.path.append('.')
from utils.stata_replication import stata_multi_lag
from utils.savepredictor import save_predictor

# DATA LOAD
df = pd.read_parquet('../pyData/Intermediate/SignalMasterTable.parquet')
df = df[['permno', 'time_avail_m', 'ret']].copy()

# Sort for lag operations
df = df.sort_values(['permno', 'time_avail_m'])

# SIGNAL CONSTRUCTION
# Replace missing returns with 0
df['ret'] = df['ret'].fillna(0)

# Calculate lags using stata_multi_lag for calendar validation
df = stata_multi_lag(df, 'permno', 'time_avail_m', 'ret', [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11])

# Calculate 12-month momentum (geometric return over 11 months)
df['Mom12m'] = ((1 + df['ret_lag1']) *
                (1 + df['ret_lag2']) *
                (1 + df['ret_lag3']) *
                (1 + df['ret_lag4']) *
                (1 + df['ret_lag5']) *
                (1 + df['ret_lag6']) *
                (1 + df['ret_lag7']) *
                (1 + df['ret_lag8']) *
                (1 + df['ret_lag9']) *
                (1 + df['ret_lag10']) *
                (1 + df['ret_lag11'])) - 1


# Keep only necessary columns for output
df_final = df[['permno', 'time_avail_m', 'Mom12m']].copy()

# SAVE
save_predictor(df_final, 'Mom12m')