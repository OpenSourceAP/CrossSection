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
import numpy as np
import sys
import os

# Add parent directory to path to import utils
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from utils.save_standardized import save_placebo
from utils.forward_fill import apply_quarterly_fill_to_compustat
from utils.stata_replication import stata_multi_lag

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
print("Computing 12-month position lag and pchquick...")
# Fill missing values with 0 to match Stata behavior
df = df.with_columns([
    pl.col('act').fill_null(0),
    pl.col('invt').fill_null(0), 
    pl.col('lct').fill_null(0)
])

# Create calendar-based lags (matching Stata's l12.)
print("Calculating 12-month calendar-based lags...")
df = stata_multi_lag(
    df,
    group_col='permno',
    time_col='time_avail_m',
    value_col=['act', 'invt', 'lct'],
    lag_list=[12],
    freq='M',
    prefix='l',
    fill_gaps=True
)

# Fill lag nulls with 0 as well
df = df.with_columns([
    pl.col('l12_act').fill_null(0),
    pl.col('l12_invt').fill_null(0),
    pl.col('l12_lct').fill_null(0)
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
    pl.when((pl.col('lag_quick') == 0) | pl.col('lag_quick').is_null() | pl.col('current_quick').is_null())
    .then(None)
    .otherwise((pl.col('current_quick') - pl.col('lag_quick')) / pl.col('lag_quick'))
    .alias('pchquick')
)

# Convert to pandas for the iterative missing value logic
df_pd = df.to_pandas()

# replace pchquick = 0 if pchquick ==. & l12.pchquick ==.
# This is the key Stata logic that creates the 0.0 values that Python is missing
print("Applying Stata's special missing value logic...")

# Apply the rule iteratively until no more changes
print("Applying Stata's special rule iteratively...")

for pass_num in range(10):  # Allow multiple passes for full propagation
    # Calculate 12-month lag of pchquick (position-based like Stata's l12.)
    df_pd['l12_pchquick'] = df_pd.groupby('permno')['pchquick'].shift(12)
    
    # Identify observations where both pchquick and l12_pchquick are missing
    both_missing = df_pd['pchquick'].isna() & df_pd['l12_pchquick'].isna()
    changes = both_missing.sum()
    
    if changes > 0:
        print(f"Pass {pass_num + 1}: {changes} observations being set to 0.0")
        df_pd.loc[both_missing, 'pchquick'] = 0.0
    else:
        print(f"Pass {pass_num + 1}: No changes needed, stopping")
        break

# Convert back to polars
df = pl.from_pandas(df_pd)

print(f"Generated pchquick for {len(df_pd)} observations")

# Convert back to polars and keep only required columns for output
df_final = pl.from_pandas(df_pd[['permno', 'time_avail_m', 'pchquick']])

# SAVE
# do "$pathCode/saveplacebo" pchquick
save_placebo(df_final, 'pchquick')

print("pchquick.py completed")