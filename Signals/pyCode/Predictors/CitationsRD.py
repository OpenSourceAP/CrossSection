# ABOUTME: Translates CitationsRD.do to create R&D citations ratio predictor
# ABOUTME: Run from pyCode/ directory: python3 Predictors/CitationsRD.py

# Run from pyCode/ directory
# Inputs: SignalMasterTable.parquet, m_aCompustat.parquet, PatentDataProcessed.parquet, monthlyCRSP.parquet  
# Output: ../pyData/Predictors/CitationsRD.csv

import pandas as pd
import numpy as np
import sys
import os
sys.path.append('.')
from utils.stata_fastxtile import fastxtile
from utils.stata_asreg_asrol import asrol
from utils.stata_replication import stata_multi_lag

# DATA LOAD with early filtering for performance
print("Loading SignalMasterTable...")
df = pd.read_parquet('../pyData/Intermediate/SignalMasterTable.parquet')
df = df[['permno', 'gvkey', 'time_avail_m', 'mve_c', 'sicCRSP', 'exchcd']].copy()

# OPTIMIZATION: Filter to post-1970 data early to reduce memory usage
df = df[df['time_avail_m'] >= '1970-01']  # Need extra history for lags
print(f"After early date filter: {df.shape}")

# Generate year from time_avail_m
df['year'] = df['time_avail_m'].dt.year

# Merge with Compustat annual data (also filtered early)
print("Loading and merging Compustat...")
compustat = pd.read_parquet('../pyData/Intermediate/m_aCompustat.parquet')
compustat = compustat[['permno', 'time_avail_m', 'xrd', 'sich', 'datadate', 'ceq']].copy()
compustat = compustat[compustat['time_avail_m'] >= '1970-01']  # Match filtering

df = df.merge(compustat, on=['permno', 'time_avail_m'], how='left')
print(f"After Compustat merge: {df.shape}")

# Drop if gvkey is missing (early filtering)
df = df.dropna(subset=['gvkey'])
print(f"After dropping missing gvkey: {df.shape}")

# Patent citation dataset
print("Loading and merging patent data...")
patent = pd.read_parquet('../pyData/Intermediate/PatentDataProcessed.parquet')
patent = patent[['gvkey', 'year', 'ncitscale']].copy()

df = df.merge(patent, on=['gvkey', 'year'], how='left')
print(f"After patent merge: {df.shape}")

# Set panel structure and create calendar-based lags (to match Stata l6/l24 behavior)
print("Creating calendar-based lags...")
df = df.sort_values(['permno', 'time_avail_m'])

# Create calendar-based lags using standardized stata_multi_lag
df = stata_multi_lag(df, 'permno', 'time_avail_m', 'ncitscale', [6], freq='M')
df = stata_multi_lag(df, 'permno', 'time_avail_m', 'xrd', [24], freq='M')

# Rename lag columns and fill missing with 0 to match original behavior
df['ncitscale'] = df['ncitscale_lag6'].fillna(0)
df['xrd_lag'] = df['xrd_lag24'].fillna(0)

# Clean up lag columns
df = df.drop(columns=['ncitscale_lag6', 'xrd_lag24'])
print(f"After creating lags: {df.shape}")

# Form portfolios only in June AFTER creating lags
print("Filtering to June observations...")
df = df[df['time_avail_m'] >= '1975-01']  # >= ym(1975,1)
df = df[df['time_avail_m'].dt.month == 6]  # month(dofm(time_avail_m)) == 6 (June)

print(f"After June filter: {df.shape}")

# Calendar-based rolling sums using standardized asrol implementation
# Stata: asrol xrd_lag, window(time_avail_m 48) stat(sum) 
print("Creating calendar-based rolling sums...")

print("  Computing 48-month calendar rolling XRD sums...")
# asrol xrd_lag, window(time_avail_m 48) stat(sum) by(permno)
df = asrol(df, 'permno', 'time_avail_m', 'xrd_lag', 48, stat='sum', new_col_name='sum_xrd')

print("  Computing 48-month calendar rolling citation sums...")
# asrol ncitscale, window(time_avail_m 48) stat(sum) by(permno)
df = asrol(df, 'permno', 'time_avail_m', 'ncitscale', 48, stat='sum', new_col_name='sum_ncit')

# Create temporary CitationsRD signal
df['tempCitationsRD'] = np.where(df['sum_xrd'] > 0, df['sum_ncit'] / df['sum_xrd'], np.nan)

# Filter
# bysort gvkey (time_avail_m): drop if _n <= 2
df = df.sort_values(['gvkey', 'time_avail_m'])
df = df.groupby('gvkey').apply(lambda x: x.iloc[2:]).reset_index(drop=True)

# Drop financial firms
df = df[~((df['sicCRSP'] >= 6000) & (df['sicCRSP'] <= 6999))]

# Drop if ceq < 0 (match Stata exactly: keeps NaN values)
df = df[~(df['ceq'] < 0)]

# Double independent sort
# Size categories using astile logic: equal-sized groups based on NYSE breakpoints
def calculate_size_breakpoints(group):
    nyse_stocks = group[group['exchcd'] == 1]
    if len(nyse_stocks) == 0:
        return group
    
    # Stata astile: create equal-sized groups based on NYSE quantiles
    # astile sizecat = mve_c, qc(exchcd == 1) nq(2)
    # This creates 2 equal-sized groups using NYSE stocks as the universe for breakpoints
    
    try:
        # Use qcut on NYSE stocks to get the 50th percentile breakpoint
        nyse_sorted = nyse_stocks['mve_c'].sort_values()
        breakpoint = nyse_sorted.quantile(0.5)  # 50th percentile
        
        # Apply the breakpoint to all stocks
        group['sizecat'] = np.where(group['mve_c'] <= breakpoint, 1, 2)
        
    except Exception:
        # Fallback in case of issues
        median_mve = nyse_stocks['mve_c'].median()
        group['sizecat'] = np.where(group['mve_c'] <= median_mve, 1, 2)
    
    return group

df = df.groupby('time_avail_m').apply(calculate_size_breakpoints).reset_index(drop=True)


# Main category using fastxtile logic exactly like Stata
print("Creating tercile categories...")

# Stata: egen maincat = fastxtile(tempCitationsRD), by(time_avail_m) n(3)
# fastxtile creates equal-sized groups based on VALID (non-missing) observations
df['maincat'] = fastxtile(df, 'tempCitationsRD', by='time_avail_m', n=3)


# Create CitationsRD signal: 1 if small & high, 0 if small & low  
df['CitationsRD'] = np.nan
df.loc[(df['sizecat'] == 1) & (df['maincat'] == 3), 'CitationsRD'] = 1
df.loc[(df['sizecat'] == 1) & (df['maincat'] == 1), 'CitationsRD'] = 0


# OPTIMIZED: Expand back to monthly using more efficient approach
print("Expanding to monthly observations...")

# Keep only necessary columns for expansion to reduce memory usage
keep_cols = ['permno', 'gvkey', 'time_avail_m', 'CitationsRD']
df_slim = df[keep_cols].copy()

# Use list comprehension with pre-allocated DataFrames
df_expanded = pd.concat([
    df_slim.assign(time_avail_m=df_slim['time_avail_m'] + pd.DateOffset(months=i))
    for i in range(12)
], ignore_index=True)

df = df_expanded.sort_values(['gvkey', 'time_avail_m'])

# Keep only necessary columns for output
df_final = df[['permno', 'time_avail_m', 'CitationsRD']].copy()
df_final = df_final.dropna(subset=['CitationsRD'])

# Convert time_avail_m to yyyymm format like other predictors
df_final['yyyymm'] = df_final['time_avail_m'].dt.year * 100 + df_final['time_avail_m'].dt.month

# Convert to integers for consistency with other predictors
df_final['permno'] = df_final['permno'].astype('int64')
df_final['yyyymm'] = df_final['yyyymm'].astype('int64')

# Keep only required columns and set index
df_final = df_final[['permno', 'yyyymm', 'CitationsRD']].copy()
df_final = df_final.set_index(['permno', 'yyyymm'])

# SAVE
df_final.to_csv('../pyData/Predictors/CitationsRD.csv')

print("CitationsRD predictor saved successfully")