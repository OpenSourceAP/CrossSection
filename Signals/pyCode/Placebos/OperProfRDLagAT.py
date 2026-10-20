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
from utils.stata_replication import fill_date_gaps, stata_multi_lag
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


print("Computing calendar-based 12-month lag...")
# Calendar endpoints require the target month; retain only observed rows.
df = df.with_columns(pl.lit(True).alias("_observed"))
df = fill_date_gaps(df, "permno", "time_avail_m", "1mo")
df = stata_multi_lag(df, "permno", "time_avail_m", ['at'], [12], prefix="l", fill_gaps=False)
df = df.filter(pl.col("_observed").eq(True)).drop("_observed")
# Match the former Pandas-to-Polars conversion of computed NaN values.
df = df.fill_nan(None)


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
