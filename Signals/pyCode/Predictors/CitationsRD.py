# ABOUTME: Creates R&D citations ratio predictor
# ABOUTME: Run from pyCode/ directory: python3 Predictors/CitationsRD.py

# Run from pyCode/ directory
# Inputs: SignalMasterTable.parquet, m_aCompustat.parquet, PatentDataProcessed.parquet, monthlyCRSP.parquet  
# Output: ../pyData/Predictors/CitationsRD.csv

import pandas as pd
import numpy as np
import polars as pl
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from utils.stata_fastxtile import fastxtile
from utils.stata_replication import stata_multi_lag, stata_quantile
from utils.save_standardized import save_predictor
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

# Set panel structure and create calendar-based lags
print("Creating calendar-based lags...")
df = df.sort_values(['permno', 'time_avail_m'])

# Create calendar-based lags: 6-month lag for citations, 24-month lag for R&D
df = stata_multi_lag(df, 'permno', 'time_avail_m', 'ncitscale', [6], freq='M')
df = stata_multi_lag(df, 'permno', 'time_avail_m', 'xrd', [24], freq='M')

# Rename lag columns and fill missing with 0
df['ncitscale'] = df['ncitscale_lag6'].fillna(0)
df['xrd_lag'] = df['xrd_lag24'].fillna(0)

# Clean up lag columns
df = df.drop(columns=['ncitscale_lag6', 'xrd_lag24'])
print(f"After creating lags: {df.shape}")

# Form portfolios only in June AFTER creating lags
print("Filtering to June observations...")
df = df[df['time_avail_m'] >= '1975-01']  # Filter to 1975 onwards
df = df[df['time_avail_m'].dt.month == 6]  # Keep only June observations

print(f"After June filter: {df.shape}")

# Calculate 48-month rolling sums for R&D and citations 
print("Creating calendar-based rolling sums...")

# Convert to polars for asrol operations
df_pl = pl.from_pandas(df)

print("  Computing 48-month calendar rolling XRD sums...")
# Calculate 48-month rolling sum of R&D expenses by firm
df_pl = asrol(df_pl, 'permno', 'time_avail_m', '1mo', 48, 'xrd_lag', 'sum', 'sum_xrd', min_samples=1)

print("  Computing 48-month calendar rolling citation sums...")
# Calculate 48-month rolling sum of scaled citations by firm  
df_pl = asrol(df_pl, 'permno', 'time_avail_m', '1mo', 48, 'ncitscale', 'sum', 'sum_ncit', min_samples=1)

# Convert back to pandas
df = df_pl.to_pandas()

# Create temporary CitationsRD signal
df['tempCitationsRD'] = np.where(df['sum_xrd'] > 0, df['sum_ncit'] / df['sum_xrd'], np.nan)

# Drop first two observations per firm to ensure adequate history
df = df.sort_values(['gvkey', 'time_avail_m'])
df = df.groupby('gvkey').apply(lambda x: x.iloc[2:]).reset_index(drop=True)

# Drop financial firms
df = df.assign(sicCRSP = lambda x: x['sicCRSP'].fillna(np.inf)) # treat missing SIC codes as non-financial
df = df[~((df['sicCRSP'] >= 6000) & (df['sicCRSP'] <= 6999))]

# Drop firms with negative book equity (keeps missing values)
df = df[~(df['ceq'] < 0)]

# Double independent sort by size and CitationsRD ratio

# Size categories using NYSE breakpoints
print("Creating size categories...")

# Calculate NYSE median for each time period
nyse_medians = df[df['exchcd'] == 1].groupby('time_avail_m')['mve_c'].apply(
    lambda x: stata_quantile(x, 0.5)
).reset_index()
nyse_medians.columns = ['time_avail_m', 'nyse_median']

# Merge medians back to main dataset
df = df.merge(nyse_medians, on='time_avail_m', how='left')

# Create size categories: 1 if <= NYSE median, 2 if > NYSE median
df['sizecat'] = np.where(df['mve_c'] <= df['nyse_median'], 1, 2)

# Clean up
df = df.drop(columns=['nyse_median'])

# Create tercile categories for CitationsRD ratio
print("Creating CitationsRD tercile categories...")

# Create equal-sized groups based on valid observations
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

# SAVE
save_predictor(df, 'CitationsRD')
