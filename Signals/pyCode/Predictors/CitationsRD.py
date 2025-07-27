# ABOUTME: Translates CitationsRD.do to create R&D citations ratio predictor
# ABOUTME: Run from pyCode/ directory: python3 Predictors/CitationsRD.py

# Run from pyCode/ directory
# Inputs: SignalMasterTable.parquet, m_aCompustat.parquet, PatentDataProcessed.parquet, monthlyCRSP.parquet  
# Output: ../pyData/Predictors/CitationsRD.csv

import pandas as pd
import numpy as np
import sys
import os

# No need for additional imports for rolling calculations

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

# Set panel structure and create 6-month lag of ncitscale
print("Creating lags...")
df = df.sort_values(['permno', 'time_avail_m'])
df['temp'] = df.groupby('permno')['ncitscale'].shift(6)  # l6.ncitscale
df['temp'] = df['temp'].fillna(0)
df['ncitscale'] = df['temp']
df = df.drop(columns=['temp'])

# SIGNAL CONSTRUCTION  
# Create 24-month lag of xrd BEFORE filtering (important!)
df['xrd_lag'] = df.groupby('permno')['xrd'].shift(24)  # l24.xrd
df['xrd_lag'] = df['xrd_lag'].fillna(0)
print(f"After creating lags: {df.shape}")

# Form portfolios only in June AFTER creating lags
print("Filtering to June observations...")
df = df[df['time_avail_m'] >= '1975-01']  # >= ym(1975,1)
df = df[df['time_avail_m'].dt.month == 6]  # month(dofm(time_avail_m)) == 6 (June)
print(f"After June filter: {df.shape}")

# OPTIMIZED: Use even more efficient rolling sum calculation
# Pre-sort once and use transform for better performance
print("Creating optimized rolling sums...")
df = df.sort_values(['permno', 'time_avail_m'])

# Use pandas transform with 4-year rolling window
# 48 months on monthly data = 4 years on June-only data
print("  Computing 4-year rolling XRD sums...")
df['sum_xrd'] = df.groupby('permno')['xrd_lag'].transform(
    lambda x: x.rolling(window=4, min_periods=1).sum()
)

print("  Computing 4-year rolling citation sums...")  
df['sum_ncit'] = df.groupby('permno')['ncitscale'].transform(
    lambda x: x.rolling(window=4, min_periods=1).sum()
)

# Create temporary CitationsRD signal
df['tempCitationsRD'] = np.where(df['sum_xrd'] > 0, df['sum_ncit'] / df['sum_xrd'], np.nan)

# Filter
# bysort gvkey (time_avail_m): drop if _n <= 2
df = df.sort_values(['gvkey', 'time_avail_m'])
df = df.groupby('gvkey').apply(lambda x: x.iloc[2:]).reset_index(drop=True)

# Drop financial firms
df = df[~((df['sicCRSP'] >= 6000) & (df['sicCRSP'] <= 6999))]

# Drop if ceq < 0
df = df[df['ceq'] >= 0]

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
def create_fastxtile_terciles(group):
    """Replicate Stata's fastxtile exactly - equal-sized groups of valid observations"""
    valid_signals = group['tempCitationsRD'].dropna()
    
    if len(valid_signals) < 3:
        # Not enough valid observations for terciles
        group['maincat'] = np.nan
        return group
    
    # Create breakpoints for equal-sized terciles
    n_valid = len(valid_signals)
    tercile_size = n_valid / 3
    
    # Sort valid values to find breakpoints
    sorted_values = valid_signals.sort_values()
    
    # Find 33rd and 67th percentile breakpoints
    breakpoint_1 = sorted_values.iloc[int(tercile_size) - 1] if int(tercile_size) > 0 else sorted_values.iloc[0]
    breakpoint_2 = sorted_values.iloc[int(2 * tercile_size) - 1] if int(2 * tercile_size) > 0 else sorted_values.iloc[-1]
    
    # Handle ties by using <= for lower categories and > for upper
    group['maincat'] = np.nan
    group.loc[group['tempCitationsRD'] <= breakpoint_1, 'maincat'] = 1
    group.loc[(group['tempCitationsRD'] > breakpoint_1) & (group['tempCitationsRD'] <= breakpoint_2), 'maincat'] = 2  
    group.loc[group['tempCitationsRD'] > breakpoint_2, 'maincat'] = 3
    
    return group

df = df.groupby('time_avail_m').apply(create_fastxtile_terciles).reset_index(drop=True)

# Create CitationsRD signal: 1 if small & high, 0 if small & low  
df['CitationsRD'] = np.nan
df.loc[(df['sizecat'] == 1) & (df['maincat'] == 3), 'CitationsRD'] = 1
df.loc[(df['sizecat'] == 1) & (df['maincat'] == 1), 'CitationsRD'] = 0

# Also assign CitationsRD = 0 to small companies with middle tercile
# This handles companies with missing/low patent data that don't reach high tercile
df.loc[(df['sizecat'] == 1) & (df['maincat'] == 2), 'CitationsRD'] = 0

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