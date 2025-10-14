# ABOUTME: GPlag.py - calculates gross profitability with lagged assets placebo
# ABOUTME: Python equivalent of GPlag.do, translates line-by-line from Stata code

"""
GPlag.py

Inputs:
    - m_aCompustat.parquet: gvkey, permno, time_avail_m, sale, cogs, at columns

Outputs:
    - GPlag.csv: permno, yyyymm, GPlag columns

Usage:
    cd pyCode
    source .venv/bin/activate  
    python3 Placebos/GPlag.py
"""

import pandas as pd
import polars as pl
import sys
import os

# Add parent directory to path to import utils
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from utils.saveplacebo import save_placebo

print("Starting GPlag.py")

# DATA LOAD
# use gvkey permno time_avail_m sale cogs at using "$pathDataIntermediate/m_aCompustat", clear
print("Loading m_aCompustat...")
df = pl.read_parquet("../pyData/Intermediate/m_aCompustat.parquet")
df = df.select(['gvkey', 'permno', 'time_avail_m', 'sale', 'cogs', 'at'])

print(f"After loading m_aCompustat: {len(df)} rows")

# SIGNAL CONSTRUCTION
# xtset permno time_avail_m
print("Sorting by permno and time...")
df = df.sort(['permno', 'time_avail_m'])

# gen GPlag = (sale-cogs)/l12.at
print("Computing GPlag...")
df = df.with_columns([
    pl.col('at').shift(12).over('permno').alias('l12_at')
])

df = df.with_columns(
    ((pl.col('sale') - pl.col('cogs')) / pl.col('l12_at')).alias('GPlag')
)

print(f"Generated GPlag for {len(df)} observations")

# Keep only required columns for output
df_final = df.select(['permno', 'time_avail_m', 'GPlag'])

# SAVE
# do "$pathCode/saveplacebo" GPlag
save_placebo(df_final, 'GPlag')

print("GPlag.py completed")