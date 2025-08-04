# ABOUTME: InvGrowth.py - calculates inventory growth predictor
# ABOUTME: Line-by-line translation of InvGrowth.do following CLAUDE.md translation philosophy

"""
InvGrowth.py

Usage:
    cd pyCode/
    source .venv/bin/activate
    python3 Predictors/InvGrowth.py

Inputs:
    - ../pyData/Intermediate/m_aCompustat.parquet
    - ../pyData/Intermediate/GNPdefl.parquet

Outputs:
    - ../pyData/Predictors/InvGrowth.csv (columns: permno, yyyymm, InvGrowth)
"""

import pandas as pd
import numpy as np
from pathlib import Path

print("Starting InvGrowth predictor...")

# DATA LOAD
# use gvkey permno time_avail_m invt sic ppent at using "$pathDataIntermediate/m_aCompustat", clear
print("Loading m_aCompustat data...")
df = pd.read_parquet('../pyData/Intermediate/m_aCompustat.parquet', 
                     columns=['gvkey', 'permno', 'time_avail_m', 'invt', 'sic', 'ppent', 'at'])
print(f"Loaded {len(df):,} Compustat observations")

# merge m:1 time_avail_m using "$pathDataIntermediate/GNPdefl", keep(match) nogenerate
print("Loading GNPdefl data...")
gnp = pd.read_parquet('../pyData/Intermediate/GNPdefl.parquet')
print(f"Loaded {len(gnp):,} GNPdefl observations")

print("Merging with GNPdefl...")
# Stata keep(match) = inner join
df = pd.merge(df, gnp, on='time_avail_m', how='inner')
print(f"After merging with GNPdefl: {len(df):,} observations")

# replace invt = invt/gnpdefl // op uses cpi
print("Adjusting invt for inflation...")
df['invt'] = df['invt'] / df['gnpdefl']

# Sample selection
print("Applying sample selection filters...")

# drop if substr(sic,1,1) == "4"
# drop if substr(sic,1,1) == "6"
df['sic_str'] = df['sic'].astype(str)
before_sic = len(df)
df = df[~df['sic_str'].str.startswith('4')].copy()
df = df[~df['sic_str'].str.startswith('6')].copy()
print(f"After SIC filter (dropped SIC 4xxx and 6xxx): {len(df):,} observations (dropped {before_sic - len(df):,})")

# drop if at <= 0 | ppent <= 0
before_at_ppent = len(df)
df = df[(df['at'] > 0) & (df['ppent'] > 0)].copy()
print(f"After AT/PPENT filter: {len(df):,} observations (dropped {before_at_ppent - len(df):,})")

# SIGNAL CONSTRUCTION
print("Constructing InvGrowth signal...")

# bysort permno time_avail_m: keep if _n == 1  // deletes a few observations
before_dedup = len(df)
df = df.drop_duplicates(subset=['permno', 'time_avail_m'], keep='first')
print(f"After deduplication: {len(df):,} observations (dropped {before_dedup - len(df):,} duplicates)")

# xtset permno time_avail_m
# gen InvGrowth = invt/l12.invt - 1
print("Calculating 12-month lag for inventory growth...")

# Sort by permno and time_avail_m for lag calculation
df = df.sort_values(['permno', 'time_avail_m']).copy()

# Create 12-month lag using pandas groupby and shift
# Stata's l12.invt means 12 periods back, so we use shift(12)
df['invt_lag12'] = df.groupby('permno')['invt'].shift(12)

# gen InvGrowth = invt/l12.invt - 1
df['InvGrowth'] = df['invt'] / df['invt_lag12'] - 1

# Keep only observations with valid InvGrowth
result = df[['permno', 'time_avail_m', 'InvGrowth']].copy()
result = result.dropna(subset=['InvGrowth']).copy()

print(f"Generated InvGrowth values for {len(result):,} observations")

# Convert time_avail_m to yyyymm
result['yyyymm'] = result['time_avail_m'].dt.year * 100 + result['time_avail_m'].dt.month

# Prepare final output
final_result = result[['permno', 'yyyymm', 'InvGrowth']].copy()

# SAVE
print("Saving predictor...")
Path('../pyData/Predictors').mkdir(parents=True, exist_ok=True)
final_result.to_csv('../pyData/Predictors/InvGrowth.csv', index=False)

print("saving InvGrowth")
print(f"Saved {len(final_result)} rows to ../pyData/Predictors/InvGrowth.csv")
print("InvGrowth predictor completed successfully!")