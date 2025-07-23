# ABOUTME: dVolCall.py - calculates change in call option implied volatility
# ABOUTME: Change in 30-day, 50-delta call option implied volatility from previous month

"""
dVolCall predictor calculation

Usage:
    cd pyCode/
    source .venv/bin/activate
    python3 Predictors/dVolCall.py

Inputs:
    - ../pyData/Intermediate/OptionMetricsVolSurf.parquet (secid, time_avail_m, days, delta, cp_flag, impl_vol)
    - ../pyData/Intermediate/SignalMasterTable.parquet (permno, time_avail_m, secid)

Outputs:
    - ../pyData/Predictors/dVolCall.csv (permno, yyyymm, dVolCall)
"""

import pandas as pd
import numpy as np

# DATA LOAD
# Clean OptionMetrics data
options_df = pd.read_parquet("../pyData/Intermediate/OptionMetricsVolSurf.parquet", 
                            columns=['secid', 'time_avail_m', 'days', 'delta', 'cp_flag', 'impl_vol'])

# SIGNAL CONSTRUCTION
# Screen: 30 days and delta = 50
options_df = options_df[(options_df['days'] == 30) & (abs(options_df['delta']) == 50)]

# Keep only call options
options_df = options_df[options_df['cp_flag'] == 'C']

# Sort data for lag operations
options_df = options_df.sort_values(['secid', 'time_avail_m'])

# Create 1-month lag of implied volatility
options_df['l1_impl_vol'] = options_df.groupby('secid')['impl_vol'].shift(1)

# Calculate change in call implied volatility
options_df['dVolCall'] = options_df['impl_vol'] - options_df['l1_impl_vol']

# Keep required columns
temp_df = options_df[['secid', 'time_avail_m', 'dVolCall']].copy()

# Merge onto master table
signal_df = pd.read_parquet("../pyData/Intermediate/SignalMasterTable.parquet", 
                           columns=['permno', 'time_avail_m', 'secid'])
df = signal_df.merge(temp_df, on=['secid', 'time_avail_m'], how='left')

# Keep only observations with dVolCall data
df = df.dropna(subset=['dVolCall'])

# Convert time_avail_m to yyyymm
df['yyyymm'] = df['time_avail_m'].dt.year * 100 + df['time_avail_m'].dt.month

# Keep required columns and order
df = df[['permno', 'yyyymm', 'dVolCall']].copy()

# SAVE
df.to_csv("../pyData/Predictors/dVolCall.csv", index=False)
print(f"dVolCall: Saved {len(df):,} observations")