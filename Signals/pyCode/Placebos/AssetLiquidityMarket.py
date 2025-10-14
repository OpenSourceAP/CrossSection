# ABOUTME: AssetLiquidityMarket.py - calculates asset liquidity placebo (market scaled)
# ABOUTME: Python equivalent of AssetLiquidityMarket.do, translates line-by-line from Stata code

"""
AssetLiquidityMarket.py

Inputs:
    - m_aCompustat.parquet: gvkey, permno, time_avail_m, che, act, at, gdwl, intan, prcc_f, csho, ceq columns

Outputs:
    - AssetLiquidityMarket.csv: permno, yyyymm, AssetLiquidityMarket columns

Usage:
    cd pyCode
    source .venv/bin/activate  
    python3 Placebos/AssetLiquidityMarket.py
"""

import pandas as pd
import polars as pl
import sys
import os

# Add parent directory to path to import utils
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from utils.save_standardized import save_placebo
from utils.stata_replication import stata_multi_lag

print("Starting AssetLiquidityMarket.py")

# DATA LOAD
# use gvkey permno time_avail_m che act at gdwl intan prcc_f csho ceq using "$pathDataIntermediate/m_aCompustat", clear
print("Loading m_aCompustat...")
df = pl.read_parquet("../pyData/Intermediate/m_aCompustat.parquet")
df = df.select(['gvkey', 'permno', 'time_avail_m', 'che', 'act', 'at', 'gdwl', 'intan', 'prcc_f', 'csho', 'ceq'])

print(f"After loading: {len(df)} rows")

# bysort permno time_avail_m: keep if _n == 1  // deletes a few observations
print("Dropping duplicates...")
df = df.unique(subset=['permno', 'time_avail_m'])

print(f"After dropping duplicates: {len(df)} rows")

# SIGNAL CONSTRUCTION
# xtset permno time_avail_m
print("Sorting for lag operations...")
df = df.sort(['permno', 'time_avail_m'])

# Convert to pandas for stata_multi_lag
df_pd = df.to_pandas()

# Create 1-month lags using stata_multi_lag
print("Computing 1-month lags using stata_multi_lag...")
lag_vars = ['at', 'prcc_f', 'csho', 'ceq']
for var in lag_vars:
    df_pd = stata_multi_lag(df_pd, 'permno', 'time_avail_m', var, [1], freq='M', prefix='l')

# Convert back to polars
df = pl.from_pandas(df_pd)

# gen AssetLiquidityMarket = (che + .75*(act - che) + .5*(at - act - gdwl - intan))/(l.at + l.prcc_f*l.csho - l.ceq)
print("Computing AssetLiquidityMarket...")
df = df.with_columns(
    ((pl.col('che') + 0.75 * (pl.col('act') - pl.col('che')) + 
      0.5 * (pl.col('at') - pl.col('act') - pl.col('gdwl') - pl.col('intan'))) / 
     (pl.col('l1_at') + pl.col('l1_prcc_f') * pl.col('l1_csho') - pl.col('l1_ceq'))).alias('AssetLiquidityMarket')
)

print(f"Generated AssetLiquidityMarket for {len(df)} observations")

# Keep only required columns for output
df_final = df.select(['permno', 'time_avail_m', 'AssetLiquidityMarket'])

# SAVE
# do "$pathCode/saveplacebo" AssetLiquidityMarket
save_placebo(df_final, 'AssetLiquidityMarket')

print("AssetLiquidityMarket.py completed")