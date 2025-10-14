# ABOUTME: cashdebt.py - calculates cashdebt placebo (Cash flow to debt)
# ABOUTME: Python equivalent of cashdebt.do, translates line-by-line from Stata code

"""
cashdebt.py

Inputs:
    - m_aCompustat.parquet: gvkey, permno, time_avail_m, ib, dp, lt columns

Outputs:
    - cashdebt.csv: permno, yyyymm, cashdebt columns

Usage:
    cd pyCode
    source .venv/bin/activate  
    python3 Placebos/cashdebt.py
"""

import pandas as pd
import polars as pl
import sys
import os

# Add parent directory to path to import utils
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from utils.saveplacebo import save_placebo

print("Starting cashdebt.py")

# DATA LOAD
# use gvkey permno time_avail_m ib dp lt using "$pathDataIntermediate/m_aCompustat", clear
print("Loading m_aCompustat...")
df = pl.read_parquet("../pyData/Intermediate/m_aCompustat.parquet")
df = df.select(['gvkey', 'permno', 'time_avail_m', 'ib', 'dp', 'lt'])

print(f"After loading: {len(df)} rows")

# SIGNAL CONSTRUCTION
# bysort permno time_avail_m: keep if _n == 1  // deletes a few observations
print("Dropping duplicates...")
df = df.unique(subset=['permno', 'time_avail_m'])

print(f"After dropping duplicates: {len(df)} rows")

# xtset permno time_avail_m
print("Sorting for lag operations...")
df = df.sort(['permno', 'time_avail_m'])

# gen cashdebt = (ib+dp)/((lt+l12.lt)/2)  // Cash flow to debt
print("Computing 12-month lag and cashdebt...")
df = df.with_columns(
    pl.col('lt').shift(12).over('permno').alias('l12_lt')
)

df = df.with_columns(
    ((pl.col('ib') + pl.col('dp')) / ((pl.col('lt') + pl.col('l12_lt')) / 2)).alias('cashdebt')
)

print(f"Generated cashdebt for {len(df)} observations")

# Keep only required columns for output
df_final = df.select(['permno', 'time_avail_m', 'cashdebt'])

# SAVE
# do "$pathCode/saveplacebo" cashdebt
save_placebo(df_final, 'cashdebt')

print("cashdebt.py completed")