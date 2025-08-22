# ABOUTME: AssetLiquidityBook.py - calculates asset liquidity placebo
# ABOUTME: Python equivalent of AssetLiquidityBook.do, translates line-by-line from Stata code

"""
AssetLiquidityBook.py

Inputs:
    - m_aCompustat.parquet: gvkey, permno, time_avail_m, che, act, at, gdwl, intan columns

Outputs:
    - AssetLiquidityBook.csv: permno, yyyymm, AssetLiquidityBook columns

Usage:
    cd pyCode
    source .venv/bin/activate  
    python3 Placebos/AssetLiquidityBook.py
"""

import pandas as pd
import polars as pl
import sys
import os

# Add parent directory to path to import utils
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from utils.saveplacebo import save_placebo

print("Starting AssetLiquidityBook.py")

# DATA LOAD
# use gvkey permno time_avail_m che act at gdwl intan at using "$pathDataIntermediate/m_aCompustat", clear
print("Loading m_aCompustat...")
df = pl.read_parquet("../pyData/Intermediate/m_aCompustat.parquet")
df = df.select(['gvkey', 'permno', 'time_avail_m', 'che', 'act', 'at', 'gdwl', 'intan'])

print(f"After loading: {len(df)} rows")

# SIGNAL CONSTRUCTION
# xtset permno time_avail_m
print("Sorting for lag operations...")
df = df.sort(['permno', 'time_avail_m'])

# Convert to pandas for lag operations
df_pd = df.to_pandas()

# Create 1-month lag date
df_pd['time_lag1'] = df_pd['time_avail_m'] - pd.DateOffset(months=1)

# Create lag data for merging
lag_vars = ['at']
lag_data = df_pd[['permno', 'time_avail_m'] + lag_vars].copy()
lag_data.columns = ['permno', 'time_lag1'] + [f'l1_{var}' for var in lag_vars]

# Merge lag data
df_pd = df_pd.merge(lag_data, on=['permno', 'time_lag1'], how='left')

# Convert back to polars
df = pl.from_pandas(df_pd.drop(columns=['time_lag1']))

# gen AssetLiquidityBook = (che + .75*(act - che) + .5*(at - act - gdwl - intan))/l.at
print("Computing AssetLiquidityBook...")
df = df.with_columns(
    ((pl.col('che') + 0.75 * (pl.col('act') - pl.col('che')) + 
      0.5 * (pl.col('at') - pl.col('act') - pl.col('gdwl') - pl.col('intan'))) / 
     pl.col('l1_at')).alias('AssetLiquidityBook')
)

print(f"Generated AssetLiquidityBook for {len(df)} observations")

# Keep only required columns for output
df_final = df.select(['permno', 'time_avail_m', 'AssetLiquidityBook'])

# SAVE
# do "$pathCode/saveplacebo" AssetLiquidityBook
save_placebo(df_final, 'AssetLiquidityBook')

print("AssetLiquidityBook.py completed")