# ABOUTME: Translates DivInit.do to create dividend initiation predictor
# ABOUTME: Run from pyCode/ directory: python3 Predictors/DivInit.py

# Run from pyCode/ directory
# Inputs: CRSPdistributions.parquet, SignalMasterTable.parquet
# Output: ../pyData/Predictors/DivInit.csv

import pandas as pd
import numpy as np
import sys
import os

# Add the parent directory to sys.path to import utils
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils.asrol import asrol_fast

# PREP DISTRIBUTIONS DATA
dist_df = pd.read_parquet('../pyData/Intermediate/CRSPdistributions.parquet')

# Cash dividends only (cd2 == 2 | cd2 == 3)
dist_df = dist_df[(dist_df['cd2'] == 2) | (dist_df['cd2'] == 3)]

# Collapse by exdt: this date tends to come first
dist_df['time_avail_m'] = pd.to_datetime(dist_df['exdt'].dt.to_period('M').dt.start_time)
dist_df = dist_df.dropna(subset=['time_avail_m', 'divamt'])

# Sum dividends by permno and time_avail_m
tempdivamt = dist_df.groupby(['permno', 'time_avail_m'])['divamt'].sum().reset_index()

# DATA LOAD
df = pd.read_parquet('../pyData/Intermediate/SignalMasterTable.parquet')
df = df[['permno', 'time_avail_m', 'exchcd', 'shrcd']].copy()

# Merge with dividend amounts
df = df.merge(tempdivamt, on=['permno', 'time_avail_m'], how='left')

# SIGNAL CONSTRUCTION
# Replace missing dividend amounts with 0
df['divamt'] = df['divamt'].fillna(0)

# Rolling 24-month sum of dividends using asrol
df = asrol_fast(df, 'permno', 'time_avail_m', 'divamt', 24, stat='sum', new_col_name='divsum')

# Sort by permno and time_avail_m for lag calculation
df = df.sort_values(['permno', 'time_avail_m'])

# Create dividend initiation indicator
# temp = divamt > 0 & l1.divsum == 0
df['divsum_lag1'] = df.groupby('permno')['divsum'].shift(1)
df['temp'] = (df['divamt'] > 0) & (df['divsum_lag1'] == 0)
df['temp'] = df['temp'].fillna(False).astype(int)  # Convert boolean to numeric

# Keep for 6 months using asrol
df = asrol_fast(df, 'permno', 'time_avail_m', 'temp', 6, stat='sum', new_col_name='initsum')

# Create final DivInit signal (initsum == 1)
df['DivInit'] = (df['initsum'] == 1).astype(int)

# Keep only necessary columns for output
df_final = df[['permno', 'time_avail_m', 'DivInit']].copy()
df_final = df_final.dropna(subset=['DivInit'])

# Convert time_avail_m to yyyymm format like other predictors
df_final['yyyymm'] = df_final['time_avail_m'].dt.year * 100 + df_final['time_avail_m'].dt.month

# Convert to integers for consistency with other predictors
df_final['permno'] = df_final['permno'].astype('int64')
df_final['yyyymm'] = df_final['yyyymm'].astype('int64')

# Keep only required columns and set index
df_final = df_final[['permno', 'yyyymm', 'DivInit']].copy()
df_final = df_final.set_index(['permno', 'yyyymm'])

# SAVE
df_final.to_csv('../pyData/Predictors/DivInit.csv')

print("DivInit predictor saved successfully")