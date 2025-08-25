# ABOUTME: ZZ1_currat_pchcurrat.py - calculates current ratio and change in current ratio placebos
# ABOUTME: Python equivalent of ZZ1_currat_pchcurrat.do, translates line-by-line from Stata code

"""
ZZ1_currat_pchcurrat.py

Inputs:
    - m_aCompustat.parquet: gvkey, permno, time_avail_m, act, che, rect, invt, lct, ap columns

Outputs:
    - currat.csv: permno, yyyymm, currat columns
    - pchcurrat.csv: permno, yyyymm, pchcurrat columns

Usage:
    cd pyCode
    source .venv/bin/activate  
    python3 Placebos/ZZ1_currat_pchcurrat.py
"""

import pandas as pd
import polars as pl
import sys
import os

# Add parent directory to path to import utils
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from utils.saveplacebo import save_placebo

print("Starting ZZ1_currat_pchcurrat.py")

# DATA LOAD
# use gvkey permno time_avail_m act che rect invt lct ap using "$pathDataIntermediate/m_aCompustat", clear
print("Loading m_aCompustat...")
df = pl.read_parquet("../pyData/Intermediate/m_aCompustat.parquet")
df = df.select(['gvkey', 'permno', 'time_avail_m', 'act', 'che', 'rect', 'invt', 'lct', 'ap'])

print(f"After loading m_aCompustat: {len(df)} rows")

# SIGNAL CONSTRUCTION
# bysort permno time_avail_m: keep if _n == 1  // deletes a few observations
print("Removing duplicates...")
df = df.unique(subset=['permno', 'time_avail_m'], maintain_order=True)

print(f"After removing duplicates: {len(df)} rows")

# xtset permno time_avail_m
print("Sorting by permno and time...")
df = df.sort(['permno', 'time_avail_m'])

# gen act2 = act
# replace act2 = che + rect + invt if act2 ==.
print("Computing act2...")
df = df.with_columns([
    pl.col('act').alias('act2')
])

df = df.with_columns([
    pl.when(pl.col('act2').is_null())
    .then(pl.col('che') + pl.col('rect') + pl.col('invt'))
    .otherwise(pl.col('act2'))
    .alias('act2')
])

# replace lct = ap if lct ==.
print("Updating lct...")
df = df.with_columns([
    pl.when(pl.col('lct').is_null())
    .then(pl.col('ap'))
    .otherwise(pl.col('lct'))
    .alias('lct')
])

# gen currat = act2/lct
print("Computing currat...")
df = df.with_columns([
    (pl.col('act2') / pl.col('lct')).alias('currat')
])

# gen pchcurrat = (currat - l12.currat)/(l12.currat)
print("Computing pchcurrat with 12-month lag...")
df = df.with_columns([
    pl.col('currat').shift(12).over('permno').alias('l12_currat')
])

df = df.with_columns([
    ((pl.col('currat') - pl.col('l12_currat')) / pl.col('l12_currat')).alias('pchcurrat')
])

# replace pchcurrat = 0 if pchcurrat ==.
print("Setting missing pchcurrat to 0...")
df = df.with_columns([
    pl.when(pl.col('pchcurrat').is_null())
    .then(0.0)
    .otherwise(pl.col('pchcurrat'))
    .alias('pchcurrat')
])

print(f"Generated currat and pchcurrat for {len(df)} observations")

# SAVE
# do "$pathCode/saveplacebo" currat
df_currat = df.select(['permno', 'time_avail_m', 'currat'])
save_placebo(df_currat, 'currat')

# do "$pathCode/saveplacebo" pchcurrat
df_pchcurrat = df.select(['permno', 'time_avail_m', 'pchcurrat'])
save_placebo(df_pchcurrat, 'pchcurrat')

print("ZZ1_currat_pchcurrat.py completed")