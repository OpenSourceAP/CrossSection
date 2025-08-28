# ABOUTME: Translates Mom12mOffSeason predictor from Stata to Python
# ABOUTME: Creates 12-month momentum excluding focal (most recent) return

"""
Mom12mOffSeason Predictor Translation

This script translates the Stata predictor Mom12mOffSeason.do to Python.
Calculates 10-month rolling mean excluding the focal (most recent) return.

Usage:
    python3 Predictors/Mom12mOffSeason.py
    
Input:
    - pyData/Intermediate/SignalMasterTable.parquet (columns: permno, time_avail_m, ret)
    
Output:
    - pyData/Predictors/Mom12mOffSeason.csv (columns: permno, yyyymm, Mom12mOffSeason)
"""

import pandas as pd
import numpy as np
import os
import sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from utils.save_standardized import save_predictor

print("Starting Mom12mOffSeason predictor translation...")

# DATA LOAD
print("Loading SignalMasterTable...")
df = pd.read_parquet('../pyData/Intermediate/SignalMasterTable.parquet')

# Keep only required columns: permno, time_avail_m, ret
df = df[['permno', 'time_avail_m', 'ret']].copy()
print(f"Loaded {len(df)} observations")

# Sort data by permno and time_avail_m (equivalent to xtset)
df = df.sort_values(['permno', 'time_avail_m'])
print("Data sorted by permno and time_avail_m")


# SIGNAL CONSTRUCTION
print("Starting signal construction...")

# Replace missing returns with 0 (equivalent to: replace ret = 0 if mi(ret))
df['ret'] = df['ret'].fillna(0)
print("Replaced missing returns with 0")


# Calculate 10-month calendar-based rolling statistics
# Need to exclude focal (current) observation from the rolling calculation
print("Computing 10-month calendar-based rolling statistics excluding focal return...")

# Import relativedelta for calendar-based calculations
from dateutil.relativedelta import relativedelta

# Implement true calendar-based rolling to exactly match Stata asrol
# This will be slow but is necessary for correct results
print("Computing true calendar-based rolling statistics (this may take several minutes)...")

# Convert to yyyymm integer for efficient calendar arithmetic
df['yyyymm'] = df['time_avail_m'].dt.year * 100 + df['time_avail_m'].dt.month

def calculate_calendar_rolling_fast(group):
    group = group.sort_values('yyyymm').reset_index(drop=True)
    n_obs = len(group)
    mom_values = np.full(n_obs, np.nan)
    
    # Pre-compute all yyyymm values for efficient comparison
    yyyymm_values = group['yyyymm'].values
    ret_values = group['ret'].values
    
    for i in range(n_obs):
        current_yyyymm = yyyymm_values[i]
        
        # Calculate 10-month calendar window start (9 months back)
        current_year = current_yyyymm // 100
        current_month = current_yyyymm % 100
        
        start_month = current_month - 9
        start_year = current_year
        while start_month <= 0:
            start_month += 12
            start_year -= 1
        
        window_start_yyyymm = start_year * 100 + start_month
        
        # Find observations in calendar window, excluding focal
        window_mask = (
            (yyyymm_values >= window_start_yyyymm) & 
            (yyyymm_values <= current_yyyymm) &
            (yyyymm_values != current_yyyymm)
        )
        
        # Calculate mean if minimum 6 observations
        window_returns = ret_values[window_mask]
        if len(window_returns) >= 6:
            mom_values[i] = np.mean(window_returns)
    
    group['Mom12mOffSeason'] = mom_values
    return group[['permno', 'time_avail_m', 'ret', 'Mom12mOffSeason']]

print("Processing groups (this will take time for large dataset)...")
df = df.groupby('permno', group_keys=False).apply(calculate_calendar_rolling_fast)


# Keep only observations with valid Mom12mOffSeason values
df_final = df.dropna(subset=['Mom12mOffSeason']).copy()
print(f"Generated {len(df_final)} valid Mom12mOffSeason observations")

# SAVE
save_predictor(df, 'Mom12mOffSeason')