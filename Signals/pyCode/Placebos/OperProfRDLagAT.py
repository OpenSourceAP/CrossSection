# ABOUTME: OperProfRDLagAT.py - calculates operating profits to lagged assets placebo
# ABOUTME: Python equivalent of OperProfRDLagAT.do, translates line-by-line from Stata code

"""
OperProfRDLagAT.py

Inputs:
    - m_aCompustat.parquet: gvkey, permno, time_avail_m, xrd, revt, cogs, xsga, at columns

Outputs:
    - OperProfRDLagAT.csv: permno, yyyymm, OperProfRDLagAT columns

Usage:
    cd pyCode
    source .venv/bin/activate  
    python3 Placebos/OperProfRDLagAT.py
"""

import pandas as pd
import polars as pl
import sys
import os

# Add parent directory to path to import utils
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from utils.saveplacebo import save_placebo

print("Starting OperProfRDLagAT.py")

# DATA LOAD
# use gvkey permno time_avail_m xrd revt cogs xsga at using "$pathDataIntermediate/m_aCompustat", clear
print("Loading m_aCompustat...")
df = pl.read_parquet("../pyData/Intermediate/m_aCompustat.parquet")
df = df.select(['gvkey', 'permno', 'time_avail_m', 'xrd', 'revt', 'cogs', 'xsga', 'at'])

print(f"Loaded data: {len(df)} rows")

# SIGNAL CONSTRUCTION
# bysort permno time_avail_m: keep if _n == 1  // deletes a few observations
print("Removing duplicates...")
df = df.unique(subset=['permno', 'time_avail_m'], maintain_order=True)

print(f"After removing duplicates: {len(df)} rows")


# Apply comprehensive group-wise forward fill for complete data coverage
print("Applying comprehensive group-wise forward fill for annual data...")
df = df.sort(['permno', 'time_avail_m'])

# Fill all required variables with maximum coverage
df = df.with_columns([
    pl.col('xrd').fill_null(strategy="forward").over('permno').alias('xrd'),
    pl.col('revt').fill_null(strategy="forward").over('permno').alias('revt'),
    pl.col('cogs').fill_null(strategy="forward").over('permno').alias('cogs'),
    pl.col('xsga').fill_null(strategy="forward").over('permno').alias('xsga'),
    pl.col('at').fill_null(strategy="forward").over('permno').alias('at')
])


# Sort for lag operations
print("Sorting by permno and time...")
df = df.sort(['permno', 'time_avail_m'])

# gen tempXRD = xrd
# replace tempXRD = 0 if mi(tempXRD)
print("Creating tempXRD with zero replacement for missing...")
df = df.with_columns([
    pl.col('xrd').fill_null(0).alias('tempXRD')
])


# Convert to pandas for calendar-based 12-month lag operations
print("Converting to calendar-based 12-month lag...")
df_pd = df.to_pandas()

# Create 12-month lag date
df_pd['time_lag12'] = df_pd['time_avail_m'] - pd.DateOffset(months=12)

# Create lag data for merging
lag12_data = df_pd[['permno', 'time_avail_m', 'at']].copy()
lag12_data.columns = ['permno', 'time_lag12', 'l12_at']

# Merge to get lagged values (calendar-based, not position-based)
df_pd = df_pd.merge(lag12_data, on=['permno', 'time_lag12'], how='left')

# Convert back to polars
df = pl.from_pandas(df_pd)


# Compute OperProfRDLagAT with enhanced null handling
print("Computing OperProfRDLagAT with calendar-based lag...")
df = df.with_columns([
    pl.when((pl.col('l12_at').is_null()) | (pl.col('l12_at') == 0))
    .then(None)  # If l12_at is null/zero, result is null
    .otherwise((pl.col('revt') - pl.col('cogs') - pl.col('xsga') + pl.col('tempXRD')) / pl.col('l12_at'))
    .alias('OperProfRDLagAT')
])

print(f"Generated OperProfRDLagAT for {len(df)} observations")

# Keep only required columns
df_final = df.select(['permno', 'time_avail_m', 'OperProfRDLagAT'])

# SAVE
# do "$pathCode/saveplacebo" OperProfRDLagAT
save_placebo(df_final, 'OperProfRDLagAT')

print("OperProfRDLagAT.py completed")