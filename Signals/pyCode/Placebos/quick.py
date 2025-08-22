# ABOUTME: quick.py - calculates quick placebo (Quick ratio)
# ABOUTME: Python equivalent of quick.do, translates line-by-line from Stata code

"""
quick.py

Inputs:
    - m_aCompustat.parquet: gvkey, permno, time_avail_m, act, invt, lct columns

Outputs:
    - quick.csv: permno, yyyymm, quick columns

Usage:
    cd pyCode
    source .venv/bin/activate  
    python3 Placebos/quick.py
"""

import pandas as pd
import polars as pl
import sys
import os

# Add parent directory to path to import utils
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from utils.saveplacebo import save_placebo

print("Starting quick.py")

# DATA LOAD
# use gvkey permno time_avail_m act invt lct using "$pathDataIntermediate/m_aCompustat", clear
print("Loading m_aCompustat...")
df = pl.read_parquet("../pyData/Intermediate/m_aCompustat.parquet")
df = df.select(['gvkey', 'permno', 'time_avail_m', 'act', 'invt', 'lct'])

print(f"After loading: {len(df)} rows")

# SIGNAL CONSTRUCTION
# bysort permno time_avail_m: keep if _n == 1  // deletes a few observations
print("Dropping duplicates...")
df = df.unique(subset=['permno', 'time_avail_m'])

print(f"After dropping duplicates: {len(df)} rows")

# gen quick = (act - invt)/lct
print("Computing quick ratio...")
df = df.with_columns(
    ((pl.col('act') - pl.col('invt')) / pl.col('lct')).alias('quick')
)

print(f"Generated quick for {len(df)} observations")

# Keep only required columns for output
df_final = df.select(['permno', 'time_avail_m', 'quick'])

# SAVE
# do "$pathCode/saveplacebo" quick
save_placebo(df_final, 'quick')

print("quick.py completed")