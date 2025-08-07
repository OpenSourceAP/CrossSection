# ABOUTME: Translates Code/Predictors/Mom6mJunk.do to calculate 6-month momentum for junk stocks
# ABOUTME: Creates junk stock momentum signal using CIQ and SP credit ratings with forward fill

"""
This script calculates 6-month momentum for junk-rated stocks (credit rating <= 14).

How to run:
    cd pyCode/
    source .venv/bin/activate
    python3 Predictors/Mom6mJunk.py

Inputs:
    - ../pyData/Intermediate/m_CIQ_creditratings.parquet
    - ../pyData/Intermediate/SignalMasterTable.parquet  
    - ../pyData/Intermediate/m_SP_creditratings.parquet

Outputs:
    - ../pyData/Predictors/Mom6mJunk.csv (permno, yyyymm, Mom6mJunk)

Logic:
    1. Clean CIQ credit ratings by removing suffixes
    2. Create numerical rating scale (0-22) from D to AAA
    3. Merge with SignalMasterTable and SP ratings
    4. Forward fill missing CIQ ratings
    5. Use SP ratings as fallback for missing CIQ ratings
    6. Calculate 6-month momentum for junk stocks (rating <= 14)
"""

import pandas as pd
import numpy as np
import os

# Set working directory to pyCode
os.chdir('/Users/chen1678/Library/CloudStorage/Dropbox/oap-ac/CrossSection/Signals/pyCode')

# Clean CIQ ratings
df_ciq = pd.read_parquet("../pyData/Intermediate/m_CIQ_creditratings.parquet")

# Convert ratingdate to time_avail_m (year-month format to match SignalMasterTable)
df_ciq['ratingdate'] = pd.to_datetime(df_ciq['ratingdate'])
# Create time_avail_m as first day of month to match SignalMasterTable format
df_ciq['time_avail_m'] = df_ciq['ratingdate'].dt.to_period('M').dt.to_timestamp()

# Use existing numerical rating (currentratingnum is already 0-22)
# Note: The original Stata code remapped D=1, C=2, etc. but the Python download
# script uses D=1, C=2, etc. so we can use currentratingnum directly
df_ciq['credratciq'] = df_ciq['currentratingnum']

# Convert gvkey to numeric to match SignalMasterTable
df_ciq['gvkey'] = pd.to_numeric(df_ciq['gvkey'], errors='coerce')

# Keep only needed columns
temp_ciq_rat = df_ciq[['gvkey', 'time_avail_m', 'credratciq']].copy()

# DATA LOAD
df = pd.read_parquet("../pyData/Intermediate/SignalMasterTable.parquet")
df = df[['gvkey', 'permno', 'time_avail_m', 'ret']].copy()
df = df.dropna(subset=['gvkey'])

# Merge with SP credit ratings
df_sp = pd.read_parquet("../pyData/Intermediate/m_SP_creditratings.parquet")
df = pd.merge(df, df_sp, on=['gvkey', 'time_avail_m'], how='left')

# Merge with CIQ ratings
df = pd.merge(df, temp_ciq_rat, on=['gvkey', 'time_avail_m'], how='left')

# Fill missing credratciq with most recent
# Sort by permno and time_avail_m
df = df.sort_values(['permno', 'time_avail_m'])

# Forward fill credratciq within each permno
df['credratciq'] = df.groupby('permno')['credratciq'].ffill()

# Coalesce credit ratings - use CIQ if available, otherwise SP
df.loc[df['credrat'].isna(), 'credrat'] = df.loc[df['credrat'].isna(), 'credratciq']

# SIGNAL CONSTRUCTION
# Set index for time series operations
df = df.sort_values(['permno', 'time_avail_m'])

# Replace missing returns with 0
df.loc[df['ret'].isna(), 'ret'] = 0

# Calculate 6-month momentum using lags
df['ret_lag1'] = df.groupby('permno')['ret'].shift(1)
df['ret_lag2'] = df.groupby('permno')['ret'].shift(2)
df['ret_lag3'] = df.groupby('permno')['ret'].shift(3)
df['ret_lag4'] = df.groupby('permno')['ret'].shift(4)
df['ret_lag5'] = df.groupby('permno')['ret'].shift(5)

# Calculate Mom6m
df['Mom6m'] = ((1 + df['ret_lag1']) * (1 + df['ret_lag2']) * (1 + df['ret_lag3']) * 
               (1 + df['ret_lag4']) * (1 + df['ret_lag5'])) - 1

# Create Mom6mJunk for junk stocks (rating <= 14 and > 0)
df['Mom6mJunk'] = np.where((df['credrat'] <= 14) & (df['credrat'] > 0), df['Mom6m'], np.nan)

# Keep only necessary columns and create yyyymm
# Convert time_avail_m datetime to YYYYMM integer format
df['yyyymm'] = df['time_avail_m'].dt.year * 100 + df['time_avail_m'].dt.month
result = df[['permno', 'yyyymm', 'Mom6mJunk']].copy()

# Drop rows where Mom6mJunk is missing
result = result.dropna(subset=['Mom6mJunk'])

# Ensure permno and yyyymm are integers
result['permno'] = result['permno'].astype(int)
result['yyyymm'] = result['yyyymm'].astype(int)

# Sort by permno, yyyymm
result = result.sort_values(['permno', 'yyyymm'])

# Save to CSV
os.makedirs("../pyData/Predictors", exist_ok=True)
result.to_csv("../pyData/Predictors/Mom6mJunk.csv", index=False)

print(f"Mom6mJunk saved with {len(result)} observations")