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

# Keep only observations with dVolPut data
df = df.dropna(subset=['dVolPut'])

# Convert time_avail_m to yyyymm
df['yyyymm'] = df['time_avail_m'].dt.year * 100 + df['time_avail_m'].dt.month

# Keep required columns and order
df = df[['permno', 'yyyymm', 'dVolPut']].copy()

# SAVE
df.to_csv("../pyData/Predictors/dVolPut.csv", index=False)
print(f"dVolPut: Saved {len(df):,} observations")