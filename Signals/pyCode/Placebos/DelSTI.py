# ABOUTME: DelSTI.py - calculates change in short-term investment placebo
# ABOUTME: Python equivalent of DelSTI.do, translates line-by-line from Stata code

"""
DelSTI.py

Inputs:
    - m_aCompustat.parquet: gvkey, permno, time_avail_m, ivst, at columns

Outputs:
    - DelSTI.csv: permno, yyyymm, DelSTI columns

Usage:
    cd pyCode
    source .venv/bin/activate  
    python3 Placebos/DelSTI.py
"""

import pandas as pd
import polars as pl
import sys
import os

# Add parent directory to path to import utils
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from utils.saveplacebo import save_placebo

print("Starting DelSTI.py")

# DATA LOAD
# use gvkey permno time_avail_m ivst at using "$pathDataIntermediate/m_aCompustat", clear
print("Loading m_aCompustat...")
df = pl.read_parquet("../pyData/Intermediate/m_aCompustat.parquet")
df = df.select(['gvkey', 'permno', 'time_avail_m', 'ivst', 'at'])

print(f"After loading: {len(df)} rows")

# bysort permno time_avail_m: keep if _n == 1  // deletes a few observations
print("Dropping duplicates...")
df = df.unique(subset=['permno', 'time_avail_m'])

print(f"After dropping duplicates: {len(df)} rows")

# SIGNAL CONSTRUCTION
# xtset permno time_avail_m
print("Sorting for lag operations...")
df = df.sort(['permno', 'time_avail_m'])

# Convert to pandas for lag operations
df_pd = df.to_pandas()

# Create 12-month lag date
df_pd['time_lag12'] = df_pd['time_avail_m'] - pd.DateOffset(months=12)

# Create lag data for merging
lag_vars = ['at', 'ivst']
lag_data = df_pd[['permno', 'time_avail_m'] + lag_vars].copy()
lag_data.columns = ['permno', 'time_lag12'] + [f'l12_{var}' for var in lag_vars]

# Merge lag data
df_pd = df_pd.merge(lag_data, on=['permno', 'time_lag12'], how='left')

# Convert back to polars
df = pl.from_pandas(df_pd.drop(columns=['time_lag12']))

# gen tempAvAT = .5*(at + l12.at)
print("Computing tempAvAT...")
df = df.with_columns(
    (0.5 * (pl.col('at') + pl.col('l12_at'))).alias('tempAvAT')
)

# gen DelSTI = ivst - l12.ivst
# replace DelSTI = DelSTI/tempAvAT
print("Computing DelSTI...")
df = df.with_columns(
    ((pl.col('ivst') - pl.col('l12_ivst')) / pl.col('tempAvAT')).alias('DelSTI')
)

print(f"Generated DelSTI for {len(df)} observations")

# Keep only required columns for output
df_final = df.select(['permno', 'time_avail_m', 'DelSTI'])

# SAVE
# do "$pathCode/saveplacebo" DelSTI
save_placebo(df_final, 'DelSTI')

print("DelSTI.py completed")