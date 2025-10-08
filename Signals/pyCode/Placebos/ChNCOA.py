# ABOUTME: ChNCOA.py - calculates change in non-current operating assets placebo
# ABOUTME: Python equivalent of ChNCOA.do, translates line-by-line from Stata code

"""
ChNCOA.py

Inputs:
    - m_aCompustat.parquet: gvkey, permno, time_avail_m, at, act, ivao columns

Outputs:
    - ChNCOA.csv: permno, yyyymm, ChNCOA columns

Usage:
    cd pyCode
    source .venv/bin/activate  
    python3 Placebos/ChNCOA.py
"""

import pandas as pd
import polars as pl
import sys
import os

# Add parent directory to path to import utils
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from utils.saveplacebo import save_placebo

print("Starting ChNCOA.py")

# DATA LOAD
# use gvkey permno time_avail_m at act ivao using "$pathDataIntermediate/m_aCompustat", clear
print("Loading m_aCompustat...")
df = pl.read_parquet("../pyData/Intermediate/m_aCompustat.parquet")
df = df.select(['gvkey', 'permno', 'time_avail_m', 'at', 'act', 'ivao'])

print(f"After loading: {len(df)} rows")

# bysort permno time_avail_m: keep if _n == 1  // deletes a few observations
print("Dropping duplicates...")
df = df.unique(subset=['permno', 'time_avail_m'])

print(f"After dropping duplicates: {len(df)} rows")

# SIGNAL CONSTRUCTION
# xtset permno time_avail_m
print("Sorting for lag operations...")
df = df.sort(['permno', 'time_avail_m'])

# gen temp = at - act - ivao
# replace temp = at - act if mi(ivao)
print("Computing temp...")
df = df.with_columns(
    pl.when(pl.col('ivao').is_not_null())
    .then(pl.col('at') - pl.col('act') - pl.col('ivao'))
    .otherwise(pl.col('at') - pl.col('act'))
    .alias('temp')
)

# Convert to pandas for lag operations
df_pd = df.to_pandas()

# Create 12-month lag date
df_pd['time_lag12'] = df_pd['time_avail_m'] - pd.DateOffset(months=12)

# Create lag data for merging
lag_vars = ['temp', 'at']
lag_data = df_pd[['permno', 'time_avail_m'] + lag_vars].copy()
lag_data.columns = ['permno', 'time_lag12'] + [f'l12_{var}' for var in lag_vars]

# Merge lag data
df_pd = df_pd.merge(lag_data, on=['permno', 'time_lag12'], how='left')

# Convert back to polars
df = pl.from_pandas(df_pd.drop(columns=['time_lag12']))

# gen ChNCOA = (temp - l12.temp)/l12.at
print("Computing ChNCOA...")
df = df.with_columns(
    ((pl.col('temp') - pl.col('l12_temp')) / pl.col('l12_at')).alias('ChNCOA')
)

print(f"Generated ChNCOA for {len(df)} observations")

# Keep only required columns for output
df_final = df.select(['permno', 'time_avail_m', 'ChNCOA'])

# SAVE
# do "$pathCode/saveplacebo" ChNCOA
save_placebo(df_final, 'ChNCOA')

print("ChNCOA.py completed")