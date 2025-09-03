# ABOUTME: pchdepr.py - calculates pchdepr placebo (Change in depreciation to gross PPE)
# ABOUTME: Python equivalent of pchdepr.do, translates line-by-line from Stata code

"""
pchdepr.py

Inputs:
    - m_aCompustat.parquet: gvkey, permno, time_avail_m, dp, ppent columns

Outputs:
    - pchdepr.csv: permno, yyyymm, pchdepr columns

Usage:
    cd pyCode
    source .venv/bin/activate  
    python3 Placebos/pchdepr.py
"""

import pandas as pd
import polars as pl
import sys
import os

# Add parent directory to path to import utils
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from utils.save_standardized import save_placebo

print("Starting pchdepr.py")

# DATA LOAD
# use gvkey permno time_avail_m dp ppent using "$pathDataIntermediate/m_aCompustat", clear
print("Loading m_aCompustat...")
df = pl.read_parquet("../pyData/Intermediate/m_aCompustat.parquet")
df = df.select(['gvkey', 'permno', 'time_avail_m', 'dp', 'ppent'])

print(f"After loading: {len(df)} rows")

# SIGNAL CONSTRUCTION
# bysort permno time_avail_m: keep if _n == 1  // deletes a few observations
print("Dropping duplicates...")
df = df.unique(subset=['permno', 'time_avail_m'])

print(f"After dropping duplicates: {len(df)} rows")

# xtset permno time_avail_m
print("Sorting for lag operations...")
df = df.sort(['permno', 'time_avail_m'])

# Forward-fill ppent to handle missing values (same as KZ)
print("Forward-filling missing ppent values...")
df = df.with_columns([
    pl.col('ppent').forward_fill().over('permno').alias('ppent')
])

print("ppent forward-fill completed")

# gen pchdepr = ((dp/ppent)-(l12.dp/l12.ppent))/(l12.dp/l12.ppent)
print("Computing 12-month lag and pchdepr...")
df = df.with_columns([
    pl.col('dp').shift(12).over('permno').alias('l12_dp'),
    pl.col('ppent').shift(12).over('permno').alias('l12_ppent')
])

# Calculate current and lagged ratios
df = df.with_columns([
    (pl.col('dp') / pl.col('ppent')).alias('current_ratio'),
    (pl.col('l12_dp') / pl.col('l12_ppent')).alias('lag_ratio')
])

# Calculate percent change
df = df.with_columns(
    ((pl.col('current_ratio') - pl.col('lag_ratio')) / pl.col('lag_ratio')).alias('pchdepr')
)

print(f"Generated pchdepr for {len(df)} observations")

# Keep only required columns for output
df_final = df.select(['permno', 'time_avail_m', 'pchdepr'])

# SAVE
# do "$pathCode/saveplacebo" pchdepr
save_placebo(df_final, 'pchdepr')

print("pchdepr.py completed")