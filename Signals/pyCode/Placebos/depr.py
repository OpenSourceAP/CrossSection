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

# SIGNAL CONSTRUCTION
# bysort permno time_avail_m: keep if _n == 1  // deletes a few observations
print("Dropping duplicates...")
df = df.unique(subset=['permno', 'time_avail_m'])

print(f"After dropping duplicates: {len(df)} rows")

# gen depr = dp/ppent
print("Computing depr...")
df = df.with_columns(
    (pl.col('dp') / pl.col('ppent')).alias('depr')
)

print(f"Generated depr for {len(df)} observations")

# Keep only required columns for output
df_final = df.select(['permno', 'time_avail_m', 'depr'])

# SAVE
# do "$pathCode/saveplacebo" depr
save_placebo(df_final, 'depr')

print("depr.py completed")