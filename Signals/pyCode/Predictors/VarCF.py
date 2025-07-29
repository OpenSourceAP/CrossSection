# ABOUTME: Translates VarCF.do to create cash-flow variance predictor
# ABOUTME: Run from pyCode/ directory: python3 Predictors/VarCF.py

# Run from pyCode/ directory
# Inputs: m_aCompustat.parquet, SignalMasterTable.parquet
# Output: ../pyData/Predictors/VarCF.csv

import pandas as pd
import numpy as np

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

# Calculate rolling standard deviation like Stata's asrol
print(f"Calculating rolling statistics for {df['permno'].nunique()} firms...")

# Sort data for rolling operations
df = df.sort_values(['permno', 'time_avail_m'])

def compute_rolling_std_asrol(group):
    """
    Replicate Stata's asrol behavior exactly but efficiently:
    - For EVERY observation, calculate rolling std using 60-month calendar window
    - Use all valid tempCF values within the window
    - Minimum 24 valid observations required
    """
    group = group.copy().sort_values('time_avail_m')
    group['sigma'] = np.nan
    
    # Use pandas rolling with time-based window for efficiency
    group = group.set_index('time_avail_m')
    
    # Apply rolling standard deviation with 60-month window and min 24 periods
    group['sigma'] = group['tempCF'].rolling(
        window='1826D',  # 60 months ≈ 5 years = 1826 days
        min_periods=24
    ).std()
    
    return group.reset_index()

# Apply to each permno group
rolling_results = []
for permno, group in df.groupby('permno'):
    result = compute_rolling_std_asrol(group)
    rolling_results.append(result)

# Combine results
df = pd.concat(rolling_results, ignore_index=True)

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