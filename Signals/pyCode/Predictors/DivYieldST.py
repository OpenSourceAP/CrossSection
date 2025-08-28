# ABOUTME: Translates DivYieldST.do to create predicted dividend yield predictor  
# ABOUTME: Run from pyCode/ directory: python3 Predictors/DivYieldST.py

# OP is mostly theory, really old, and pretty vague about what it does.
# So we combine their guidelines with our knowledge of the data
# to get results similar to their regression.

# Run from pyCode/ directory
# Inputs: CRSPdistributions.parquet, SignalMasterTable.parquet, monthlyCRSP.parquet
# Output: ../pyData/Predictors/DivYieldST.csv

import pandas as pd
import numpy as np
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils.stata_fastxtile import fastxtile

# PREP DISTRIBUTIONS DATA
dist_df = pd.read_parquet('../pyData/Intermediate/CRSPdistributions.parquet')
dist_df = dist_df[['permno', 'cd1', 'cd2', 'cd3', 'divamt', 'exdt']].copy()

# Keep dividend distributions (cd1=1, cd2=2)
dist_df = dist_df[(dist_df['cd1'] == 1) & (dist_df['cd2'] == 2)]

# Keep quarterly, semi-annual, and annual (cd3 = 3, 4, 5)
dist_df = dist_df[dist_df['cd3'].isin([3, 4, 5])]

# Convert exdt to monthly time_avail_m and drop missing
dist_df['exdt'] = pd.to_datetime(dist_df['exdt'])
dist_df['time_avail_m'] = dist_df['exdt'].dt.to_period('M').dt.to_timestamp()
dist_df = dist_df.dropna(subset=['time_avail_m', 'divamt'])

# Sum across all frequency codes by permno, cd3, time_avail_m
tempdivamt = dist_df.groupby(['permno', 'cd3', 'time_avail_m'])['divamt'].sum().reset_index()

# Clean up odd two-frequency permno-months by keeping first (quarterly code priority)
tempdivamt = tempdivamt.sort_values(['permno', 'time_avail_m', 'cd3'])
tempdivamt = tempdivamt.groupby(['permno', 'time_avail_m']).first().reset_index()

# DATA LOAD
df = pd.read_parquet('../pyData/Intermediate/SignalMasterTable.parquet')
df = df[['permno', 'time_avail_m', 'prc']].copy()

# Merge with dividend data
df = df.merge(tempdivamt[['permno', 'time_avail_m', 'cd3', 'divamt']], 
              on=['permno', 'time_avail_m'], how='left')

# Merge with monthly CRSP data
monthly_crsp = pd.read_parquet('../pyData/Intermediate/monthlyCRSP.parquet')
df = df.merge(monthly_crsp[['permno', 'time_avail_m', 'ret', 'retx']], 
              on=['permno', 'time_avail_m'], how='left')

# Sort for lagged operations
df = df.sort_values(['permno', 'time_avail_m'])

# Fill forward cd3 (replace cd3 = l1.cd3 if cd3 == .)
df['cd3'] = df.groupby('permno')['cd3'].ffill()

# Replace missing divamt with 0
df['divamt'] = df['divamt'].fillna(0)

# Keep only dividend payers: rolling 12-month sum of divamt > 0
df['div12'] = df.groupby('permno')['divamt'].rolling(window=12, min_periods=1).sum().reset_index(0, drop=True)
df = df[(df['div12'] > 0) & df['div12'].notna()]

# Create expected dividend (Ediv1) using lagged values based on frequency
df['Ediv1'] = np.nan

# For quarterly or missing/unknown frequency (cd3 = 3, 0, 1): use 2-month lag
mask_quarterly = df['cd3'].isin([3, 0, 1]) | df['cd3'].isna()
df.loc[mask_quarterly, 'Ediv1'] = df.groupby('permno')['divamt'].shift(2)

# For semi-annual (cd3 = 4): use 5-month lag  
mask_semiann = (df['cd3'] == 4)
df.loc[mask_semiann, 'Ediv1'] = df.groupby('permno')['divamt'].shift(5)

# For annual (cd3 = 5): use 11-month lag
mask_annual = (df['cd3'] == 5)
df.loc[mask_annual, 'Ediv1'] = df.groupby('permno')['divamt'].shift(11)

# Calculate expected dividend yield: Edy1 = Ediv1 / abs(prc)
df['Edy1'] = df['Ediv1'] / abs(df['prc'])

# Create positive dividend yield subset
df['Edy1pos'] = df['Edy1'].where(df['Edy1'] > 0)

# Create DivYieldST as terciles of positive dividend yields by month
# Use robust fastxtile for tercile assignment (n=3)
df['DivYieldST'] = fastxtile(df, 'Edy1pos', by='time_avail_m', n=3)

# Set DivYieldST = 0 for zero dividend yields
df.loc[df['Edy1'] == 0, 'DivYieldST'] = 0

# Prepare final output
df_final = df[['permno', 'time_avail_m', 'DivYieldST']].copy()
df_final = df_final.dropna(subset=['DivYieldST'])

# Convert time_avail_m to yyyymm format
df_final['yyyymm'] = df_final['time_avail_m'].dt.year * 100 + df_final['time_avail_m'].dt.month

# Convert to integers for consistency with other predictors
df_final['permno'] = df_final['permno'].astype('int64')
df_final['yyyymm'] = df_final['yyyymm'].astype('int64')

# Keep only required columns and set index
df_final = df_final[['permno', 'yyyymm', 'DivYieldST']].copy()
df_final = df_final.set_index(['permno', 'yyyymm'])

# SAVE
df_final.to_csv('../pyData/Predictors/DivYieldST.csv')

print("DivYieldST predictor saved successfully")