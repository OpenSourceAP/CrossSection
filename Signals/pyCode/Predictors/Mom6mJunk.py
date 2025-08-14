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
df_ciq_raw = pd.read_parquet("../pyData/Intermediate/m_CIQ_creditratings.parquet",
                             columns=['gvkey', 'ratingdate', 'currentratingnum'])

# Convert gvkey to numeric to match SignalMasterTable
df_ciq_raw['gvkey'] = pd.to_numeric(df_ciq_raw['gvkey'], errors='coerce')

# Expand each rating to be valid for 12 months after ratingdate
from dateutil.relativedelta import relativedelta
expanded_ciq_records = []

for _, row in df_ciq_raw.iterrows():
    if pd.notna(row['gvkey']) and pd.notna(row['currentratingnum']):
        base_date = pd.to_datetime(row['ratingdate'])
        for months_offset in range(12):
            time_avail_m = (base_date + relativedelta(months=months_offset)).replace(day=1)
            expanded_ciq_records.append({
                'gvkey': row['gvkey'],
                'time_avail_m': time_avail_m,
                'credratciq': row['currentratingnum']
            })

temp_ciq_rat = pd.DataFrame(expanded_ciq_records)

# Handle duplicates within month by taking the mean rating
temp_ciq_rat = temp_ciq_rat.groupby(['gvkey', 'time_avail_m'])['credratciq'].mean().reset_index()

# DATA LOAD
df = pd.read_parquet("../pyData/Intermediate/SignalMasterTable.parquet")
df = df[['gvkey', 'permno', 'time_avail_m', 'ret']].copy()
df = df.dropna(subset=['gvkey'])

# Merge with SP credit ratings
df_sp = pd.read_parquet("../pyData/Intermediate/m_SP_creditratings.parquet")
df = pd.merge(df, df_sp, on=['gvkey', 'time_avail_m'], how='left')

# Merge with CIQ ratings
df = pd.merge(df, temp_ciq_rat, on=['gvkey', 'time_avail_m'], how='left')

# CHECKPOINT 1: After merging credit ratings
data_10026 = df[(df['permno'] == 10026) & (df['time_avail_m'] == pd.Timestamp('2015-09-01'))]
if not data_10026.empty:
    print("CHECKPOINT 1 - After merging credit ratings:")
    print(data_10026[['permno', 'time_avail_m', 'credrat', 'credratciq']])

# Sort by permno and time_avail_m
df = df.sort_values(['permno', 'time_avail_m'])

# CRITICAL: Implement Stata's tsfill + forward fill logic
# Stata tsfill creates complete balanced panel, then forward fills ratings within permno groups
# This is essential for filling gaps in credit rating data

# Forward fill BOTH SP ratings (credrat) and CIQ ratings (credratciq) within permno groups
# This replicates the effect of Stata's tsfill creating missing periods + forward fill
df['credrat'] = df.groupby('permno')['credrat'].ffill()
df['credratciq'] = df.groupby('permno')['credratciq'].ffill()

# Coalesce credit ratings - use CIQ if available, otherwise SP  
df.loc[df['credrat'].isna(), 'credrat'] = df.loc[df['credrat'].isna(), 'credratciq']

# CHECKPOINT 2: After filling missing credratciq
data_10026 = df[(df['permno'] == 10026) & (df['time_avail_m'] == pd.Timestamp('2015-09-01'))]
if not data_10026.empty:
    print("CHECKPOINT 2 - After filling missing credratciq:")
    print(data_10026[['permno', 'time_avail_m', 'credrat', 'credratciq']])

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

# CHECKPOINT 3: After creating Mom6m
data_10026 = df[(df['permno'] == 10026) & (df['time_avail_m'] == pd.Timestamp('2015-09-01'))]
if not data_10026.empty:
    print("CHECKPOINT 3 - After creating Mom6m:")
    print(data_10026[['permno', 'time_avail_m', 'ret', 'Mom6m']])

# Create Mom6mJunk for junk stocks (rating <= 14 and > 0)
df['Mom6mJunk'] = np.where((df['credrat'] <= 14) & (df['credrat'] > 0), df['Mom6m'], np.nan)

# CHECKPOINT 4: When filtering for junk (credrat <= 14)
data_10026 = df[(df['permno'] == 10026) & (df['time_avail_m'] == pd.Timestamp('2015-09-01'))]
if not data_10026.empty:
    print("CHECKPOINT 4 - When filtering for junk (credrat <= 14):")
    print(data_10026[['permno', 'time_avail_m', 'credrat', 'Mom6m', 'Mom6mJunk']])

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