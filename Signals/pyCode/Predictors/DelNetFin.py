# ABOUTME: Change in net financial assets following Richardson et al. 2005, Table 8B DeltaFin
# ABOUTME: Change in net financial assets (financial assets minus liabilities) from prior 12 months divided by average total assets

"""
DelNetFin predictor calculation

Usage:
    cd pyCode/
    source .venv/bin/activate
    python3 Predictors/DelNetFin.py

Inputs:
    - ../pyData/Intermediate/m_aCompustat.parquet (gvkey, permno, time_avail_m, at, pstk, dltt, dlc, ivst, ivao)

Outputs:
    - ../pyData/Predictors/DelNetFin.csv (permno, yyyymm, DelNetFin)
"""

import pandas as pd
import numpy as np

# DATA LOAD
df = pd.read_parquet("../pyData/Intermediate/m_aCompustat.parquet", 
                     columns=['gvkey', 'permno', 'time_avail_m', 'at', 'pstk', 'dltt', 'dlc', 'ivst', 'ivao'])

# SIGNAL CONSTRUCTION
# Remove duplicates by permno time_avail_m (keep first)
df = df.drop_duplicates(subset=['permno', 'time_avail_m'], keep='first')

# Sort data for lag operations
df = df.sort_values(['permno', 'time_avail_m'])

# Create 12-month lags using time-based approach
df['time_lag12'] = df['time_avail_m'] - pd.DateOffset(months=12)

# Handle missing pstk values
df['tempPSTK'] = df['pstk'].fillna(0)

# Calculate net financial assets (financial assets minus liabilities)
df['temp'] = (df['ivst'] + df['ivao']) - (df['dltt'] + df['dlc'] + df['tempPSTK'])

# Create lag data for merge
lag_data = df[['permno', 'time_avail_m', 'at', 'temp']].copy()
lag_data.columns = ['permno', 'time_lag12', 'l12_at', 'l12_temp']

# Merge to get lagged values
df = df.merge(lag_data, on=['permno', 'time_lag12'], how='left')

# Calculate average total assets
df['tempAvAT'] = 0.5 * (df['at'] + df['l12_at'])

# Calculate change in net financial assets scaled by average assets
df['DelNetFin'] = (df['temp'] - df['l12_temp']) / df['tempAvAT']

# Drop missing values
df = df.dropna(subset=['DelNetFin'])

# Convert time_avail_m to yyyymm
df['yyyymm'] = df['time_avail_m'].dt.year * 100 + df['time_avail_m'].dt.month

# Keep required columns and order
df = df[['permno', 'yyyymm', 'DelNetFin']].copy()

# SAVE
df.to_csv("../pyData/Predictors/DelNetFin.csv", index=False)
print(f"DelNetFin: Saved {len(df):,} observations")