# ABOUTME: AssetTurnover.py - calculates AssetTurnover placebo (Asset Turnover)
# ABOUTME: Python equivalent of AssetTurnover.do, translates line-by-line from Stata code

"""
AssetTurnover.py

Inputs:
    - m_aCompustat.parquet: gvkey, permno, time_avail_m, rect, invt, aco, ppent, intan, ap, lco, lo, sale columns

Outputs:
    - AssetTurnover.csv: permno, yyyymm, AssetTurnover columns

Usage:
    cd pyCode
    source .venv/bin/activate  
    python3 Placebos/AssetTurnover.py
"""

import pandas as pd
import polars as pl
import sys
import os

# Add parent directory to path to import utils
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from utils.saveplacebo import save_placebo

print("Starting AssetTurnover.py")

# DATA LOAD
# use gvkey permno time_avail_m rect invt aco ppent intan ap lco lo sale using "$pathDataIntermediate/m_aCompustat", clear
print("Loading m_aCompustat...")
df = pl.read_parquet("../pyData/Intermediate/m_aCompustat.parquet")
df = df.select(['gvkey', 'permno', 'time_avail_m', 'rect', 'invt', 'aco', 'ppent', 'intan', 'ap', 'lco', 'lo', 'sale'])

print(f"After loading: {len(df)} rows")

# SIGNAL CONSTRUCTION
# bysort permno time_avail_m: keep if _n == 1  // deletes a few observations
print("Dropping duplicates...")
df = df.unique(subset=['permno', 'time_avail_m'])

print(f"After dropping duplicates: {len(df)} rows")

# xtset permno time_avail_m
print("Sorting for lag operations...")
df = df.sort(['permno', 'time_avail_m'])

# gen temp = (rect + invt + aco + ppent + intan - ap - lco - lo)
print("Computing temp asset measure...")
df = df.with_columns(
    (pl.col('rect') + pl.col('invt') + pl.col('aco') + pl.col('ppent') + pl.col('intan') 
     - pl.col('ap') - pl.col('lco') - pl.col('lo')).alias('temp')
)

# gen AssetTurnover = sale/((temp + l12.temp)/2)
print("Computing 12-month lag and AssetTurnover...")
df = df.with_columns(
    pl.col('temp').shift(12).over('permno').alias('l12_temp')
)

df = df.with_columns(
    (pl.col('sale') / ((pl.col('temp') + pl.col('l12_temp')) / 2)).alias('AssetTurnover')
)

# replace AssetTurnover = . if AssetTurnover < 0
print("Setting negative AssetTurnover to null...")
df = df.with_columns(
    pl.when(pl.col('AssetTurnover') < 0)
    .then(None)
    .otherwise(pl.col('AssetTurnover'))
    .alias('AssetTurnover')
)

print(f"Generated AssetTurnover for {len(df)} observations")

# Keep only required columns for output
df_final = df.select(['permno', 'time_avail_m', 'AssetTurnover'])

# SAVE
# do "$pathCode/saveplacebo" AssetTurnover
save_placebo(df_final, 'AssetTurnover')

print("AssetTurnover.py completed")