# ABOUTME: sgr.py - calculates sgr placebo (Annual sales growth)
# ABOUTME: Python equivalent of sgr.do, translates line-by-line from Stata code

"""
sgr.py

Inputs:
    - m_aCompustat.parquet: gvkey, permno, time_avail_m, sale columns

Outputs:
    - sgr.csv: permno, yyyymm, sgr columns

Usage:
    cd pyCode
    source .venv/bin/activate  
    python3 Placebos/sgr.py
"""

import pandas as pd
import polars as pl
import sys
import os

# Add parent directory to path to import utils
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from utils.saveplacebo import save_placebo

print("Starting sgr.py")

# DATA LOAD
# use gvkey permno time_avail_m sale using "$pathDataIntermediate/m_aCompustat", clear
print("Loading m_aCompustat...")
df = pl.read_parquet("../pyData/Intermediate/m_aCompustat.parquet")
df = df.select(['gvkey', 'permno', 'time_avail_m', 'sale'])

print(f"After loading: {len(df)} rows")

# SIGNAL CONSTRUCTION
# bysort permno time_avail_m: keep if _n == 1  // deletes a few observations
print("Dropping duplicates...")
df = df.unique(subset=['permno', 'time_avail_m'])

print(f"After dropping duplicates: {len(df)} rows")

# xtset permno time_avail_m
print("Sorting for lag operations...")
df = df.sort(['permno', 'time_avail_m'])

# gen sgr = (sale/l12.sale)-1
print("Computing 12-month lag and sgr...")
df = df.with_columns(
    pl.col('sale').shift(12).over('permno').alias('l12_sale')
)

df = df.with_columns(
    ((pl.col('sale') / pl.col('l12_sale')) - 1).alias('sgr')
)

print(f"Generated sgr for {len(df)} observations")

# Keep only required columns for output
df_final = df.select(['permno', 'time_avail_m', 'sgr'])

# SAVE
# do "$pathCode/saveplacebo" sgr
save_placebo(df_final, 'sgr')

print("sgr.py completed")