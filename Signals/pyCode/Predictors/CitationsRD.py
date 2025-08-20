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
from utils.asrol import asrol

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

# Create calendar-based lags matching Stata's lag operator behavior
# Stata's l6.var looks for value from 6 months ago in calendar time, not 6 positions back

# Create lag dates for each observation
df['lag6_date'] = df['time_avail_m'] - pd.DateOffset(months=6)
df['lag24_date'] = df['time_avail_m'] - pd.DateOffset(months=24)

# Create a lookup table for lag values by permno and date
lookup_df = df[['permno', 'time_avail_m', 'ncitscale', 'xrd']].copy()

# Merge for 6-month lag of ncitscale
lag6_merge = df[['permno', 'lag6_date']].merge(
    lookup_df[['permno', 'time_avail_m', 'ncitscale']], 
    left_on=['permno', 'lag6_date'],
    right_on=['permno', 'time_avail_m'],
    how='left',
    suffixes=('', '_lag6')
)
df['temp'] = lag6_merge['ncitscale'].fillna(0)
df['ncitscale'] = df['temp']

# Merge for 24-month lag of xrd
lag24_merge = df[['permno', 'lag24_date']].merge(
    lookup_df[['permno', 'time_avail_m', 'xrd']],
    left_on=['permno', 'lag24_date'],
    right_on=['permno', 'time_avail_m'],
    how='left',
    suffixes=('', '_lag24')
)
df['xrd_lag'] = lag24_merge['xrd'].fillna(0)

# Clean up temporary columns
df = df.drop(columns=['temp', 'lag6_date', 'lag24_date'])
print(f"After creating lags: {df.shape}")

# Form portfolios only in June AFTER creating lags
print("Filtering to June observations...")
df = df[df['time_avail_m'] >= '1975-01']  # >= ym(1975,1)

# CHECKPOINT 1: Check observations before June filter
debug_mask = (df['permno'] == 10010) & (df['time_avail_m'] >= '1992-01') & (df['time_avail_m'] <= '1993-12')
if debug_mask.any():
    print("* CHECKPOINT 1: Before June filter")
    print(df.loc[debug_mask, ['permno', 'time_avail_m', 'year', 'gvkey', 'ncitscale']])

df = df[df['time_avail_m'].dt.month == 6]  # month(dofm(time_avail_m)) == 6 (June)

# CHECKPOINT 2: Check observations after June filter  
debug_mask = (df['permno'] == 10010) & (df['time_avail_m'] >= '1992-01') & (df['time_avail_m'] <= '1993-12')
if debug_mask.any():
    print("* CHECKPOINT 2: After June filter")
    print(df.loc[debug_mask, ['permno', 'time_avail_m', 'year', 'gvkey', 'ncitscale']])

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
# CHECKPOINT 3: Check observations before gvkey filter
debug_mask = (df['permno'] == 10010) & (df['time_avail_m'] >= '1992-01') & (df['time_avail_m'] <= '1993-12')
if debug_mask.any():
    print("* CHECKPOINT 3: Before gvkey filter")
    print(df.loc[debug_mask, ['permno', 'time_avail_m', 'gvkey', 'sum_xrd', 'sum_ncit', 'tempCitationsRD']])

# bysort gvkey (time_avail_m): drop if _n <= 2
df = df.sort_values(['gvkey', 'time_avail_m'])
df = df.groupby('gvkey').apply(lambda x: x.iloc[2:]).reset_index(drop=True)

# CHECKPOINT 4: Check observations after gvkey filter
debug_mask = (df['permno'] == 10010) & (df['time_avail_m'] >= '1992-01') & (df['time_avail_m'] <= '1993-12')
if debug_mask.any():
    print("* CHECKPOINT 4: After gvkey filter")
    print(df.loc[debug_mask, ['permno', 'time_avail_m', 'gvkey', 'sum_xrd', 'sum_ncit', 'tempCitationsRD']])

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

# CHECKPOINT 5: Check size categories for problematic observation
debug_mask = (df['permno'] == 10010) & (df['time_avail_m'] >= '1992-01') & (df['time_avail_m'] <= '1993-12')
if debug_mask.any():
    print("* CHECKPOINT 5: Size categories")
    print(df.loc[debug_mask, ['permno', 'time_avail_m', 'mve_c', 'sizecat']])
    # Show NYSE median for comparison for June 1992
    if not df[df['time_avail_m'] == '1992-06'].empty:
        june_1992 = df[df['time_avail_m'] == '1992-06']
        nyse_stocks = june_1992[june_1992['exchcd'] == 1]
        if len(nyse_stocks) > 0:
            print(f"NYSE median mve_c for 1992-06: {nyse_stocks['mve_c'].median()}")
            print(f"NYSE mve_c percentiles: {nyse_stocks['mve_c'].describe()}")

# Main category using fastxtile logic exactly like Stata
print("Creating tercile categories...")

# Stata: egen maincat = fastxtile(tempCitationsRD), by(time_avail_m) n(3)
# fastxtile creates equal-sized groups based on VALID (non-missing) observations
df['maincat'] = fastxtile(df, 'tempCitationsRD', by='time_avail_m', n=3)

# CHECKPOINT 6: Check fastxtile results and quantiles
debug_mask = (df['permno'] == 10010) & (df['time_avail_m'] >= '1992-01') & (df['time_avail_m'] <= '1993-12')
if debug_mask.any():
    print("* CHECKPOINT 6: Fastxtile results")
    print(df.loc[debug_mask, ['permno', 'time_avail_m', 'tempCitationsRD', 'sizecat', 'maincat']])
    # Show distribution for June 1992
    if not df[df['time_avail_m'] == '1992-06'].empty:
        june_1992 = df[df['time_avail_m'] == '1992-06']
        print(f"tempCitationsRD summary for 1992-06:")
        print(june_1992['tempCitationsRD'].describe())
        print(f"maincat distribution:")
        print(june_1992.groupby('maincat')['tempCitationsRD'].agg(['min', 'max', 'count']))

# Create CitationsRD signal: 1 if small & high, 0 if small & low  
df['CitationsRD'] = np.nan
df.loc[(df['sizecat'] == 1) & (df['maincat'] == 3), 'CitationsRD'] = 1
df.loc[(df['sizecat'] == 1) & (df['maincat'] == 1), 'CitationsRD'] = 0

# CHECKPOINT 7: Check final signal assignment
debug_mask = (df['permno'] == 10010) & (df['time_avail_m'] >= '1992-01') & (df['time_avail_m'] <= '1993-12')
if debug_mask.any():
    print("* CHECKPOINT 7: Final signal assignment")
    print(df.loc[debug_mask, ['permno', 'time_avail_m', 'sizecat', 'maincat', 'CitationsRD']])
    # Show signal distribution by size category for June 1992
    if not df[df['time_avail_m'] == '1992-06'].empty:
        june_1992 = df[df['time_avail_m'] == '1992-06']
        print(f"CitationsRD by sizecat for 1992-06:")
        print(june_1992.groupby('sizecat')['CitationsRD'].agg(['mean', 'count']))

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