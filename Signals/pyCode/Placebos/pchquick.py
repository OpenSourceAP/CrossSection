# ABOUTME: pchquick.py - calculates pchquick placebo (Change in quick ratio)
# ABOUTME: Python equivalent of pchquick.do, translates line-by-line from Stata code

"""
pchquick.py

Inputs:
    - m_aCompustat.parquet: gvkey, permno, time_avail_m, act, invt, lct columns

Outputs:
    - pchquick.csv: permno, yyyymm, pchquick columns

Usage:
    cd pyCode
    source .venv/bin/activate  
    python3 Placebos/pchquick.py
"""

import pandas as pd
import polars as pl
import sys
import os

# Add parent directory to path to import utils
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from utils.saveplacebo import save_placebo
from utils.forward_fill import apply_quarterly_fill_to_compustat

print("Starting pchquick.py")

# DATA LOAD
# use gvkey permno time_avail_m act invt lct using "$pathDataIntermediate/m_aCompustat", clear
print("Loading m_aCompustat...")
df = pl.read_parquet("../pyData/Intermediate/m_aCompustat.parquet")
df = df.select(['gvkey', 'permno', 'time_avail_m', 'act', 'invt', 'lct'])

print(f"After loading: {len(df)} rows")

print("Applying forward-fill for missing annual values...")
df = apply_quarterly_fill_to_compustat(df, quarterly_columns=['act', 'invt', 'lct'])

# SIGNAL CONSTRUCTION
# bysort permno time_avail_m: keep if _n == 1  // deletes a few observations
print("Dropping duplicates...")
df = df.unique(subset=['permno', 'time_avail_m'])

print(f"After dropping duplicates: {len(df)} rows")

# xtset permno time_avail_m
print("Sorting for lag operations...")
df = df.sort(['permno', 'time_avail_m'])

# gen pchquick = ( (act-invt)/lct - (l12.act-l12.invt)/l12.lct ) /  ((l12.act-l12.invt)/l12.lct)
print("Computing 12-month lag and pchquick...")
df = df.with_columns([
    pl.col('act').shift(12).over('permno').alias('l12_act'),
    pl.col('invt').shift(12).over('permno').alias('l12_invt'),
    pl.col('lct').shift(12).over('permno').alias('l12_lct')
])

# Calculate current and lagged quick ratios (handle division by zero)
df = df.with_columns([
    pl.when(pl.col('lct') == 0)
    .then(None)
    .otherwise((pl.col('act') - pl.col('invt')) / pl.col('lct'))
    .alias('current_quick'),
    pl.when(pl.col('l12_lct') == 0)
    .then(None)
    .otherwise((pl.col('l12_act') - pl.col('l12_invt')) / pl.col('l12_lct'))
    .alias('lag_quick')
])

# Calculate percent change (handle division by zero)
df = df.with_columns(
    pl.when(pl.col('lag_quick') == 0)
    .then(None)
    .otherwise((pl.col('current_quick') - pl.col('lag_quick')) / pl.col('lag_quick'))
    .alias('pchquick')
)

# replace pchquick = 0 if pchquick ==. & l12.pchquick ==.
# This means: set pchquick to 0 if both current calculation is missing AND lagged calculation would be missing
print("Applying Stata's special missing value logic...")
df = df.with_columns(
    pl.col('pchquick').shift(12).over('permno').alias('l12_pchquick')
)

df = df.with_columns(
    pl.when((pl.col('pchquick').is_null()) & (pl.col('l12_pchquick').is_null()))
    .then(0.0)
    .otherwise(pl.col('pchquick'))
    .alias('pchquick')
)

print(f"Generated pchquick for {len(df)} observations")

# Keep only required columns for output
df_final = df.select(['permno', 'time_avail_m', 'pchquick'])

# SAVE
# do "$pathCode/saveplacebo" pchquick
save_placebo(df_final, 'pchquick')

print("pchquick.py completed")