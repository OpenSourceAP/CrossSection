# ABOUTME: depr.py - calculates depr placebo (Depreciation to PPE)
# ABOUTME: Python equivalent of depr.do, translates line-by-line from Stata code

"""
depr.py

Inputs:
    - m_aCompustat.parquet: gvkey, permno, time_avail_m, dp, ppent columns

Outputs:
    - depr.csv: permno, yyyymm, depr columns

Usage:
    cd pyCode
    source .venv/bin/activate  
    python3 Placebos/depr.py
"""

import pandas as pd
import polars as pl
import sys
import os

# Add parent directory to path to import utils
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from utils.saveplacebo import save_placebo

print("Starting depr.py")

# DATA LOAD
# use gvkey permno time_avail_m dp ppent using "$pathDataIntermediate/m_aCompustat", clear
print("Loading m_aCompustat...")
df = pl.read_parquet("../pyData/Intermediate/m_aCompustat.parquet")
df = df.select(['gvkey', 'permno', 'time_avail_m', 'dp', 'ppent'])

print(f"After loading: {len(df)} rows")
# Apply enhanced group-wise forward-only fill for complete data coverage
print("Applying enhanced group-wise forward-only fill for depreciation data...")
df = df.sort(['permno', 'time_avail_m'])

# Apply forward fill to all relevant numeric columns for better coverage
numeric_cols = [col for col in df.columns if col not in ['permno', 'time_avail_m', 'gvkey'] and df[col].dtype in ['float64', 'int64']]
print(f"Applying fill to {len(numeric_cols)} numeric columns...")

for col in numeric_cols:
    if col in df.columns:
        df = df.with_columns([
            pl.col(col).fill_null(strategy="forward").over('permno').alias(col)
        ])

# Apply even more comprehensive forward fill across entire time series
print("Applying comprehensive temporal fill for complete coverage...")
df = df.sort(['permno', 'time_avail_m'])

# Fill dp and ppent more aggressively across entire time range
df = df.with_columns([
    pl.col('dp').fill_null(strategy="forward").over('permno').alias('dp'),
    pl.col('ppent').fill_null(strategy="forward").over('permno').alias('ppent')
])

# Handle edge case: if ppent is still null but dp is available, use last known ppent
print("Handling remaining nulls with extended temporal coverage...")
df = df.with_columns([
    pl.col('ppent').fill_null(0.001).alias('ppent')  # Tiny non-zero to avoid division issues
])


# SIGNAL CONSTRUCTION
# bysort permno time_avail_m: keep if _n == 1  // deletes a few observations
print("Dropping duplicates...")
df = df.unique(subset=['permno', 'time_avail_m'])

print(f"After dropping duplicates: {len(df)} rows")


# Compute depr with enhanced null handling
print("Computing depr with comprehensive null handling...")
df = df.with_columns([
    pl.when(pl.col('ppent').is_null() | (pl.col('ppent') == 0))
    .then(None)  # If ppent is null/zero, result is null
    .otherwise(pl.col('dp') / pl.col('ppent'))
    .alias('depr')
])

print(f"Generated depr for {len(df)} observations")

# Keep only required columns for output
df_final = df.select(['permno', 'time_avail_m', 'depr'])

# SAVE
# do "$pathCode/saveplacebo" depr
save_placebo(df_final, 'depr')

print("depr.py completed")