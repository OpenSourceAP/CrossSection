# ABOUTME: dVolPut.py - calculates change in put option implied volatility
# ABOUTME: Change in 30-day, 50-delta put option implied volatility from previous month

"""
dVolPut predictor calculation

Usage:
    cd pyCode/
    source .venv/bin/activate
    python3 Predictors/dVolPut.py

Inputs:
    - ../pyData/Intermediate/OptionMetricsVolSurf.parquet (secid, time_avail_m, days, delta, cp_flag, impl_vol)
    - ../pyData/Intermediate/SignalMasterTable.parquet (permno, time_avail_m, secid)

Outputs:
    - ../pyData/Predictors/dVolPut.csv (permno, yyyymm, dVolPut)
"""

import pandas as pd
import numpy as np
import sys
import os

# Add utils directory to path for imports
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from utils.save_standardized import save_predictor

# DATA LOAD
# Clean OptionMetrics data
options_df = pd.read_parquet("../pyData/Intermediate/OptionMetricsVolSurf.parquet", 
                            columns=['secid', 'time_avail_m', 'days', 'delta', 'cp_flag', 'impl_vol'])

# SIGNAL CONSTRUCTION
# Screen: 30 days and delta = 50
options_df = options_df[(options_df['days'] == 30) & (abs(options_df['delta']) == 50)]

# Keep only put options
options_df = options_df[options_df['cp_flag'] == 'P']

# Sort data for lag operations
options_df = options_df.sort_values(['secid', 'time_avail_m'])

# Create 1-month lag of implied volatility
options_df['l1_impl_vol'] = options_df.groupby('secid')['impl_vol'].shift(1)

# Calculate change in put implied volatility
options_df['dVolPut'] = options_df['impl_vol'] - options_df['l1_impl_vol']

# Keep required columns
temp_df = options_df[['secid', 'time_avail_m', 'dVolPut']].copy()

# Merge onto master table
signal_df = pd.read_parquet("../pyData/Intermediate/SignalMasterTable.parquet", 
                           columns=['permno', 'time_avail_m', 'secid'])
df = signal_df.merge(temp_df, on=['secid', 'time_avail_m'], how='left')

# Keep required columns 
df = df[['permno', 'time_avail_m', 'dVolPut']].copy()

# SAVE
save_predictor(df, 'dVolPut')