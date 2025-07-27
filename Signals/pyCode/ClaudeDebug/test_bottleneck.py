# ABOUTME: Test where CitationsRD gets stuck
# ABOUTME: Run from pyCode/ directory: python3 ClaudeDebug/test_bottleneck.py

import pandas as pd
import numpy as np
import time

def time_step(step_name, func):
    """Time a processing step"""
    print(f"Starting {step_name}...")
    start = time.time()
    result = func()
    end = time.time()
    print(f"  {step_name} completed in {end-start:.1f} seconds")
    return result

print("=== Testing CitationsRD bottlenecks ===")

# Test 1: Data loading
def load_signalmaster():
    df = pd.read_parquet('../pyData/Intermediate/SignalMasterTable.parquet')
    df = df[['permno', 'gvkey', 'time_avail_m', 'mve_c', 'sicCRSP', 'exchcd']].copy()
    df = df[df['time_avail_m'] >= '1970-01']
    return df

df = time_step("SignalMasterTable load + filter", load_signalmaster)
print(f"  Shape: {df.shape}")

# Test 2: Compustat merge
def load_compustat():
    compustat = pd.read_parquet('../pyData/Intermediate/m_aCompustat.parquet')
    compustat = compustat[['permno', 'time_avail_m', 'xrd', 'sich', 'datadate', 'ceq']].copy()
    compustat = compustat[compustat['time_avail_m'] >= '1970-01']
    return compustat

compustat = time_step("Compustat load + filter", load_compustat)
print(f"  Shape: {compustat.shape}")

def merge_compustat():
    result = df.merge(compustat, on=['permno', 'time_avail_m'], how='left')
    result = result.dropna(subset=['gvkey'])
    return result

df = time_step("Compustat merge", merge_compustat)
print(f"  Shape after merge: {df.shape}")

# Test 3: Patent merge
def load_patent():
    patent = pd.read_parquet('../pyData/Intermediate/PatentDataProcessed.parquet')
    patent = patent[['gvkey', 'year', 'ncitscale']].copy()
    return patent

patent = time_step("Patent load", load_patent)
print(f"  Shape: {patent.shape}")

def merge_patent():
    df['year'] = df['time_avail_m'].dt.year
    result = df.merge(patent, on=['gvkey', 'year'], how='left')
    return result

df = time_step("Patent merge", merge_patent)
print(f"  Shape after patent merge: {df.shape}")

# Test 4: Lag creation
def create_lags():
    df_sorted = df.sort_values(['permno', 'time_avail_m'])
    df_sorted['temp'] = df_sorted.groupby('permno')['ncitscale'].shift(6)
    df_sorted['temp'] = df_sorted['temp'].fillna(0)
    df_sorted['ncitscale'] = df_sorted['temp']
    df_sorted = df_sorted.drop(columns=['temp'])
    df_sorted['xrd_lag'] = df_sorted.groupby('permno')['xrd'].shift(24)
    df_sorted['xrd_lag'] = df_sorted['xrd_lag'].fillna(0)
    return df_sorted

df = time_step("Create lags", create_lags)

# Test 5: June filtering  
def june_filter():
    result = df[df['time_avail_m'] >= '1975-01']
    result = result[result['time_avail_m'].dt.month == 6]
    return result

df = time_step("June filter", june_filter)
print(f"  Shape after June filter: {df.shape}")

print("\n=== Bottleneck test complete ===")
print("If this completed quickly, the issue is in the rolling sum calculation")