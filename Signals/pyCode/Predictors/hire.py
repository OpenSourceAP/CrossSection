# ABOUTME: hire.py - calculates employee growth rate
# ABOUTME: Employee growth rate over prior 12 months, scaled by average employment

"""
hire predictor calculation

Usage:
    cd pyCode/
    source .venv/bin/activate
    python3 Predictors/hire.py

Inputs:
    - ../pyData/Intermediate/m_aCompustat.parquet (permno, time_avail_m, emp)

Outputs:
    - ../pyData/Predictors/hire.csv (permno, yyyymm, hire)
"""

import pandas as pd
import numpy as np

# DATA LOAD
df = pd.read_parquet("../pyData/Intermediate/m_aCompustat.parquet", 
                     columns=['permno', 'time_avail_m', 'emp'])

# SIGNAL CONSTRUCTION
# Remove duplicates by permno time_avail_m (keep first)
df = df.drop_duplicates(subset=['permno', 'time_avail_m'], keep='first')

# Sort data for lag operations
df = df.sort_values(['permno', 'time_avail_m'])

# Create 12-month lags using time-based approach
df['time_lag12'] = df['time_avail_m'] - pd.DateOffset(months=12)

# Create lag data for merge
lag_data = df[['permno', 'time_avail_m', 'emp']].copy()
lag_data.columns = ['permno', 'time_lag12', 'l12_emp']

# Merge to get lagged values
df = df.merge(lag_data, on=['permno', 'time_lag12'], how='left')

# Calculate hire rate
df['hire'] = (df['emp'] - df['l12_emp']) / (0.5 * (df['emp'] + df['l12_emp']))

# Replace with 0 if either emp or l12_emp is missing
df.loc[(df['emp'].isna()) | (df['l12_emp'].isna()), 'hire'] = 0

# Set to missing if year < 1965
df.loc[df['time_avail_m'].dt.year < 1965, 'hire'] = np.nan

# Drop missing values
df = df.dropna(subset=['hire'])

# Convert time_avail_m to yyyymm
df['yyyymm'] = df['time_avail_m'].dt.year * 100 + df['time_avail_m'].dt.month

# Keep required columns and order
df = df[['permno', 'yyyymm', 'hire']].copy()

# SAVE
df.to_csv("../pyData/Predictors/hire.csv", index=False)
print(f"hire: Saved {len(df):,} observations")