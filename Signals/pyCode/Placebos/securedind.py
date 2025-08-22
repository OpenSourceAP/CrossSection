# ABOUTME: securedind.py - calculates securedind placebo (Secured debt indicator)
# ABOUTME: Python equivalent of securedind.do, translates line-by-line from Stata code

"""
securedind.py

Inputs:
    - m_aCompustat.parquet: gvkey, permno, time_avail_m, dm columns

Outputs:
    - securedind.csv: permno, yyyymm, securedind columns

Usage:
    cd pyCode
    source .venv/bin/activate  
    python3 Placebos/securedind.py
"""

import pandas as pd
import polars as pl
import sys
import os

# Add parent directory to path to import utils
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from utils.saveplacebo import save_placebo

print("Starting securedind.py")

# DATA LOAD
# use gvkey permno time_avail_m dm using "$pathDataIntermediate/m_aCompustat", clear
print("Loading m_aCompustat...")
df = pl.read_parquet("../pyData/Intermediate/m_aCompustat.parquet")
df = df.select(['gvkey', 'permno', 'time_avail_m', 'dm'])

print(f"After loading: {len(df)} rows")

# SIGNAL CONSTRUCTION
# bysort permno time_avail_m: keep if _n == 1  // deletes a few observations
print("Dropping duplicates...")
df = df.unique(subset=['permno', 'time_avail_m'])

print(f"After dropping duplicates: {len(df)} rows")

# gen securedind = 0
# replace securedind = 1 if dm !=. & dm !=0
print("Computing securedind...")
df = df.with_columns(
    pl.when((pl.col('dm').is_not_null()) & (pl.col('dm') != 0))
    .then(1)
    .otherwise(0)
    .alias('securedind')
)

print(f"Generated securedind for {len(df)} observations")

# Keep only required columns for output
df_final = df.select(['permno', 'time_avail_m', 'securedind'])

# SAVE
# do "$pathCode/saveplacebo" securedind
save_placebo(df_final, 'securedind')

print("securedind.py completed")