# ABOUTME: Translates VarCF.do to create cash-flow variance predictor
# ABOUTME: Run from pyCode/ directory: python3 Predictors/VarCF.py

# Run from pyCode/ directory
# Inputs: m_aCompustat.parquet, SignalMasterTable.parquet
# Output: ../pyData/Predictors/VarCF.csv

import pandas as pd
import numpy as np
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from utils.asrol import asrol_fast

# DATA LOAD
# Start with SignalMasterTable like Stata's "using" dataset
smt = pd.read_parquet('../pyData/Intermediate/SignalMasterTable.parquet')
df = smt[['permno', 'time_avail_m', 'mve_c']].copy()

# Merge with m_aCompustat data (left join to keep all SignalMasterTable observations)
compustat = pd.read_parquet('../pyData/Intermediate/m_aCompustat.parquet')
compustat = compustat[['permno', 'time_avail_m', 'ib', 'dp']].copy()
df = df.merge(compustat, on=['permno', 'time_avail_m'], how='left')

# Note: This replicates Stata's "merge 1:1 permno time_avail_m using SignalMasterTable, keep(using match)"
# We keep all SignalMasterTable observations, with ib/dp missing for observations not in m_aCompustat

# Sort for rolling operations
df = df.sort_values(['permno', 'time_avail_m'])

# SIGNAL CONSTRUCTION
# Create temporary cash flow measure
df['tempCF'] = (df['ib'] + df['dp']) / df['mve_c']

# Calculate rolling standard deviation using asrol (60-month window, min 24 periods)
print(f"Calculating rolling statistics for {df['permno'].nunique()} firms...")

# Sort data for rolling operations
df = df.sort_values(['permno', 'time_avail_m'])

# Use asrol for 60-month rolling standard deviation with minimum 24 periods
df = asrol_fast(df, 'permno', 'time_avail_m', 'tempCF', 60, stat='sd', new_col_name='sigma', min_periods=24)

print("Rolling statistics calculation completed")

# VarCF = sigma^2
df['VarCF'] = df['sigma'] ** 2

# Keep only necessary columns for output
df_final = df[['permno', 'time_avail_m', 'VarCF']].copy()
df_final = df_final.dropna(subset=['VarCF'])

# Convert time_avail_m to yyyymm format like other predictors
df_final['yyyymm'] = df_final['time_avail_m'].dt.year * 100 + df_final['time_avail_m'].dt.month

# Convert to integers for consistency with other predictors
df_final['permno'] = df_final['permno'].astype('int64')
df_final['yyyymm'] = df_final['yyyymm'].astype('int64')

# Keep only required columns and set index
df_final = df_final[['permno', 'yyyymm', 'VarCF']].copy()
df_final = df_final.set_index(['permno', 'yyyymm'])

# SAVE
df_final.to_csv('../pyData/Predictors/VarCF.csv')

print("VarCF predictor saved successfully")