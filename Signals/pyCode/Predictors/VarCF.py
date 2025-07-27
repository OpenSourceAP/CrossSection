# ABOUTME: Translates VarCF.do to create cash-flow variance predictor
# ABOUTME: Run from pyCode/ directory: python3 Predictors/VarCF.py

# Run from pyCode/ directory
# Inputs: m_aCompustat.parquet, SignalMasterTable.parquet
# Output: ../pyData/Predictors/VarCF.csv

import pandas as pd
import numpy as np
import sys
import os

# Add the parent directory to sys.path to import utils
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils.data_utils import asrol

# DATA LOAD
df = pd.read_parquet('../pyData/Intermediate/m_aCompustat.parquet')
df = df[['gvkey', 'permno', 'time_avail_m', 'ib', 'dp']].copy()

# Merge with SignalMasterTable
smt = pd.read_parquet('../pyData/Intermediate/SignalMasterTable.parquet')
df = df.merge(smt[['permno', 'time_avail_m', 'mve_c']], on=['permno', 'time_avail_m'], how='inner')

# Sort for rolling operations
df = df.sort_values(['permno', 'time_avail_m'])

# SIGNAL CONSTRUCTION
# Create temporary cash flow measure
df['tempCF'] = (df['ib'] + df['dp']) / df['mve_c']

# Calculate rolling standard deviation over 60 months (minimum 24)
df = asrol(df, 'permno', 'time_avail_m', 'tempCF', 60, stat='std', new_col_name='sigma', min_periods=24)

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