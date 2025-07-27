# ABOUTME: Test rolling sum performance on CitationsRD June data
# ABOUTME: Run from pyCode/ directory: python3 ClaudeDebug/test_rolling.py

import pandas as pd
import numpy as np
import time

print("=== Testing rolling sum performance ===")

# Load the June-filtered data (from our bottleneck test)
df = pd.read_parquet('../pyData/Intermediate/SignalMasterTable.parquet')
df = df[['permno', 'gvkey', 'time_avail_m', 'mve_c', 'sicCRSP', 'exchcd']].copy()
df = df[df['time_avail_m'] >= '1970-01']
df['year'] = df['time_avail_m'].dt.year

compustat = pd.read_parquet('../pyData/Intermediate/m_aCompustat.parquet')
compustat = compustat[['permno', 'time_avail_m', 'xrd', 'sich', 'datadate', 'ceq']].copy()
compustat = compustat[compustat['time_avail_m'] >= '1970-01']

df = df.merge(compustat, on=['permno', 'time_avail_m'], how='left')
df = df.dropna(subset=['gvkey'])

patent = pd.read_parquet('../pyData/Intermediate/PatentDataProcessed.parquet')
patent = patent[['gvkey', 'year', 'ncitscale']].copy()
df = df.merge(patent, on=['gvkey', 'year'], how='left')

# Create lags quickly
df = df.sort_values(['permno', 'time_avail_m'])
df['temp'] = df.groupby('permno')['ncitscale'].shift(6).fillna(0)
df['ncitscale'] = df['temp']
df = df.drop(columns=['temp'])
df['xrd_lag'] = df.groupby('permno')['xrd'].shift(24).fillna(0)

# Filter to June
df = df[df['time_avail_m'] >= '1975-01']
df = df[df['time_avail_m'].dt.month == 6]

print(f"June data shape: {df.shape}")

# Test rolling sum on progressively larger subsets
subset_sizes = [1000, 5000, 10000, 50000]

for size in subset_sizes:
    if size > len(df):
        size = len(df)
    
    subset = df.head(size).copy()
    print(f"\nTesting rolling sum on {size} observations...")
    
    start = time.time()
    subset['sum_xrd'] = subset.groupby('permno')['xrd_lag'].transform(
        lambda x: x.rolling(window=4, min_periods=1).sum()
    )
    subset['sum_ncit'] = subset.groupby('permno')['ncitscale'].transform(
        lambda x: x.rolling(window=4, min_periods=1).sum()
    )
    end = time.time()
    
    print(f"  Completed in {end-start:.1f} seconds ({(end-start)/size*1000:.2f} ms per observation)")
    
    if end-start > 30:  # If taking more than 30 seconds, stop
        print(f"  Too slow, stopping test")
        break

print("\n=== Rolling sum test complete ===")

# Estimate time for full dataset
if len(subset_sizes) > 0:
    last_time = end-start
    last_size = size
    full_estimate = (last_time / last_size) * len(df)
    print(f"Estimated time for full dataset ({len(df)} obs): {full_estimate:.1f} seconds")