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
from utils.stata_replication import fill_date_gaps, stata_multi_lag
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

# Create the Stata one-month calendar lag.
# Calendar endpoints require the target month; retain only observed rows.
df = df.with_columns(pl.lit(True).alias("_observed"))
df = fill_date_gaps(df, "permno", "time_avail_m", "1mo")
df = stata_multi_lag(df, "permno", "time_avail_m", ['at'], [1], prefix="l", fill_gaps=False)
df = df.filter(pl.col("_observed").eq(True)).drop("_observed")

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
