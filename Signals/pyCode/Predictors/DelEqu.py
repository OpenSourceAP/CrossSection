# ABOUTME: DelEqu.py - calculates change in common equity scaled by average total assets
# ABOUTME: Change in common equity from prior 12 months divided by average total assets

"""
DelEqu predictor calculation

Usage:
    cd pyCode/
    source .venv/bin/activate
    python3 Predictors/DelEqu.py

Inputs:
    - ../pyData/Intermediate/m_aCompustat.parquet (gvkey, permno, time_avail_m, at, ceq)

Outputs:
    - ../pyData/Predictors/DelEqu.csv (permno, yyyymm, DelEqu)
"""

import pandas as pd
import numpy as np

# DATA LOAD
df = pd.read_parquet("../pyData/Intermediate/m_aCompustat.parquet", 
                     columns=['gvkey', 'permno', 'time_avail_m', 'at', 'ceq'])

# SIGNAL CONSTRUCTION
# Remove duplicates by permno time_avail_m (keep first)
df = df.drop_duplicates(subset=['permno', 'time_avail_m'], keep='first')

# Sort data for lag operations
df = df.sort_values(['permno', 'time_avail_m'])

# Create 12-month lags using time-based approach
df['time_lag12'] = df['time_avail_m'] - pd.DateOffset(months=12)

# Create lag data for merge
lag_data = df[['permno', 'time_avail_m', 'at', 'ceq']].copy()
lag_data.columns = ['permno', 'time_lag12', 'l12_at', 'l12_ceq']

# Merge to get lagged values
df = df.merge(lag_data, on=['permno', 'time_lag12'], how='left')

# Calculate average total assets
df['tempAvAT'] = 0.5 * (df['at'] + df['l12_at'])

# Calculate change in equity scaled by average assets
df['DelEqu'] = (df['ceq'] - df['l12_ceq']) / df['tempAvAT']

# Drop missing values
df = df.dropna(subset=['DelEqu'])

# Convert time_avail_m to yyyymm
df['yyyymm'] = df['time_avail_m'].dt.year * 100 + df['time_avail_m'].dt.month

# Keep required columns and order
df = df[['permno', 'yyyymm', 'DelEqu']].copy()

# SAVE
df.to_csv("../pyData/Predictors/DelEqu.csv", index=False)
print(f"DelEqu: Saved {len(df):,} observations")