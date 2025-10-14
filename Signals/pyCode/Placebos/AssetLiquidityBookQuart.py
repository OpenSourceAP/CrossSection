# ABOUTME: AssetLiquidityBookQuart.py - calculates quarterly asset liquidity placebo
# ABOUTME: Python equivalent of AssetLiquidityBookQuart.do, translates line-by-line from Stata code

"""
AssetLiquidityBookQuart.py

Inputs:
    - SignalMasterTable.parquet: permno, gvkey, time_avail_m columns
    - m_QCompustat.parquet: gvkey, time_avail_m, gdwlq, intanq, cheq, actq, atq columns

Outputs:
    - AssetLiquidityBookQuart.csv: permno, yyyymm, AssetLiquidityBookQuart columns

Usage:
    cd pyCode
    source .venv/bin/activate  
    python3 Placebos/AssetLiquidityBookQuart.py
"""

import pandas as pd
import polars as pl
import sys
import os

# Add parent directory to path to import utils
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from utils.saveplacebo import save_placebo

print("Starting AssetLiquidityBookQuart.py")

# DATA LOAD
# use permno gvkey time_avail_m using "$pathDataIntermediate/SignalMasterTable", clear
print("Loading SignalMasterTable...")
df = pl.read_parquet("../pyData/Intermediate/SignalMasterTable.parquet")
df = df.select(['permno', 'gvkey', 'time_avail_m'])

# keep if !mi(gvkey)
df = df.filter(pl.col('gvkey').is_not_null())

print(f"After filtering for non-null gvkey: {len(df)} rows")

# merge 1:1 gvkey time_avail_m using "$pathDataIntermediate/m_QCompustat", keepusing(gdwlq intanq cheq actq atq) nogenerate keep(match)
print("Loading m_QCompustat...")
qcomp = pl.read_parquet("../pyData/Intermediate/m_QCompustat.parquet")
qcomp = qcomp.select(['gvkey', 'time_avail_m', 'gdwlq', 'intanq', 'cheq', 'actq', 'atq'])

# Convert gvkey to same type for join
df = df.with_columns(pl.col('gvkey').cast(pl.Int32))
qcomp = qcomp.with_columns(pl.col('gvkey').cast(pl.Int32))

print("Merging with m_QCompustat...")
df = df.join(qcomp, on=['gvkey', 'time_avail_m'], how='inner')

print(f"After merge: {len(df)} rows")

# SIGNAL CONSTRUCTION
# xtset permno time_avail_m
print("Sorting for lag operations...")
df = df.sort(['permno', 'time_avail_m'])

# replace gdwlq = 0 if mi(gdwlq)
# replace intanq = 0 if mi(intanq)
print("Replacing missing gdwlq and intanq with 0...")
df = df.with_columns([
    pl.col('gdwlq').fill_null(0).alias('gdwlq'),
    pl.col('intanq').fill_null(0).alias('intanq')
])

# Create 1-period lag using polars (position-based like Stata l. operator)
df = df.with_columns(
    pl.col('atq').shift(1).over('permno').alias('l1_atq')
)

# gen AssetLiquidityBookQuart = (cheq + .75*(actq - cheq) + .5*(atq - actq - gdwlq - intanq))/l.atq
print("Computing AssetLiquidityBookQuart...")
df = df.with_columns(
    ((pl.col('cheq') + 0.75 * (pl.col('actq') - pl.col('cheq')) + 
      0.5 * (pl.col('atq') - pl.col('actq') - pl.col('gdwlq') - pl.col('intanq'))) / 
     pl.col('l1_atq')).alias('AssetLiquidityBookQuart')
)

print(f"Generated AssetLiquidityBookQuart for {len(df)} observations")

# Keep only required columns for output
df_final = df.select(['permno', 'time_avail_m', 'AssetLiquidityBookQuart'])

# SAVE
# do "$pathCode/saveplacebo" AssetLiquidityBookQuart
save_placebo(df_final, 'AssetLiquidityBookQuart')

print("AssetLiquidityBookQuart.py completed")