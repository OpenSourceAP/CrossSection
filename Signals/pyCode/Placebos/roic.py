# ABOUTME: roic.py - calculates roic placebo (Return on invested capital)
# ABOUTME: Python equivalent of roic.do, translates line-by-line from Stata code

"""
roic.py

Inputs:
    - m_aCompustat.parquet: gvkey, permno, time_avail_m, ebit, nopi, ceq, lt, che columns

Outputs:
    - roic.csv: permno, yyyymm, roic columns

Usage:
    cd pyCode
    source .venv/bin/activate  
    python3 Placebos/roic.py
"""

import pandas as pd
import polars as pl
import sys
import os

# Add parent directory to path to import utils
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from utils.saveplacebo import save_placebo

print("Starting roic.py")

# DATA LOAD
# use gvkey permno time_avail_m ebit nopi ceq lt che using "$pathDataIntermediate/m_aCompustat", clear
print("Loading m_aCompustat...")
df = pl.read_parquet("../pyData/Intermediate/m_aCompustat.parquet")
df = df.select(['gvkey', 'permno', 'time_avail_m', 'ebit', 'nopi', 'ceq', 'lt', 'che'])

print(f"After loading: {len(df)} rows")

# SIGNAL CONSTRUCTION
# bysort permno time_avail_m: keep if _n == 1  // deletes a few observations
print("Dropping duplicates...")
df = df.unique(subset=['permno', 'time_avail_m'])

print(f"After dropping duplicates: {len(df)} rows")

# gen roic = (ebit - nopi)/(ceq + lt - che)
print("Computing roic...")
df = df.with_columns(
    ((pl.col('ebit') - pl.col('nopi')) / (pl.col('ceq') + pl.col('lt') - pl.col('che'))).alias('roic')
)

print(f"Generated roic for {len(df)} observations")

# Keep only required columns for output
df_final = df.select(['permno', 'time_avail_m', 'roic'])

# SAVE
# do "$pathCode/saveplacebo" roic
save_placebo(df_final, 'roic')

print("roic.py completed")