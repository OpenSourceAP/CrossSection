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
# Apply enhanced group-wise forward+backward fill for complete data coverage
print("Applying enhanced group-wise forward+backward fill for asset data...")
df = df.sort(['permno', 'time_avail_m'])
df = df.with_columns([
    pl.col('rect').fill_null(strategy="forward").fill_null(strategy="backward").over('permno').alias('rect'),
    pl.col('invt').fill_null(strategy="forward").fill_null(strategy="backward").over('permno').alias('invt'),
    pl.col('aco').fill_null(strategy="forward").fill_null(strategy="backward").over('permno').alias('aco'),
    pl.col('ppent').fill_null(strategy="forward").fill_null(strategy="backward").over('permno').alias('ppent'),
    pl.col('intan').fill_null(strategy="forward").fill_null(strategy="backward").over('permno').alias('intan'),
    pl.col('ap').fill_null(strategy="forward").fill_null(strategy="backward").over('permno').alias('ap'),
    pl.col('lco').fill_null(strategy="forward").fill_null(strategy="backward").over('permno').alias('lco'),
    pl.col('lo').fill_null(strategy="forward").fill_null(strategy="backward").over('permno').alias('lo'),
    pl.col('sale').fill_null(strategy="forward").fill_null(strategy="backward").over('permno').alias('sale')
])

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
print("Computing 12-month calendar-based lag and AssetTurnover...")

# Convert to pandas for calendar-based lag operations
df_pd = df.to_pandas()

# Create 12-month lag date
df_pd['time_lag12'] = df_pd['time_avail_m'] - pd.DateOffset(months=12)

# Create lag data for merging
lag_data = df_pd[['permno', 'time_avail_m', 'temp']].copy()
lag_data.columns = ['permno', 'time_lag12', 'l12_temp']

# Merge to get lagged values (calendar-based, not position-based)
df_pd = df_pd.merge(lag_data, on=['permno', 'time_lag12'], how='left')

# Convert back to polars
df = pl.from_pandas(df_pd)

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