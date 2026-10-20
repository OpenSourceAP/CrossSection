# ABOUTME: AssetLiquidityMarketQuart.py - calculates quarterly asset liquidity placebo (market scaled)
# ABOUTME: Python equivalent of AssetLiquidityMarketQuart.do, translates line-by-line from Stata code

"""
AssetLiquidityMarketQuart.py

Inputs:
    - SignalMasterTable.parquet: permno, gvkey, time_avail_m, mve_permco columns
    - m_QCompustat.parquet: gvkey, time_avail_m, gdwlq, intanq, cheq, actq, prccq, cshoq, atq, ceqq columns

Outputs:
    - AssetLiquidityMarketQuart.csv: permno, yyyymm, AssetLiquidityMarketQuart columns

Usage:
    cd pyCode
    source .venv/bin/activate  
    python3 Placebos/AssetLiquidityMarketQuart.py
"""

import pandas as pd
import polars as pl
import sys
import os

# Add parent directory to path to import utils
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from utils.stata_replication import fill_date_gaps, stata_multi_lag
from utils.saveplacebo import save_placebo

print("Starting AssetLiquidityMarketQuart.py")

# DATA LOAD
# use permno gvkey time_avail_m mve_permco using "$pathDataIntermediate/SignalMasterTable", clear
print("Loading SignalMasterTable...")
df = pl.read_parquet("../pyData/Intermediate/SignalMasterTable.parquet")
df = df.select(['permno', 'gvkey', 'time_avail_m', 'mve_permco'])

# keep if !mi(gvkey)
df = df.filter(pl.col('gvkey').is_not_null())

print(f"After filtering for non-null gvkey: {len(df)} rows")

# merge 1:1 gvkey time_avail_m using "$pathDataIntermediate/m_QCompustat", keepusing(gdwlq intanq cheq actq prccq cshoq atq ceqq) nogenerate keep(match)
print("Loading m_QCompustat...")
qcomp = pl.read_parquet("../pyData/Intermediate/m_QCompustat.parquet")
qcomp = qcomp.select(['gvkey', 'time_avail_m', 'gdwlq', 'intanq', 'cheq', 'actq', 'prccq', 'cshoq', 'atq', 'ceqq'])

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

# Convert to pandas for lag operations
# Calendar endpoints require the target month; retain only observed rows.
df = df.with_columns(pl.lit(True).alias("_observed"))
df = fill_date_gaps(df, "permno", "time_avail_m", "1mo")
df = stata_multi_lag(df, "permno", "time_avail_m", ['atq', 'prccq', 'cshoq', 'ceqq'], [1], prefix="l", fill_gaps=False)
df = df.filter(pl.col("_observed").eq(True)).drop("_observed")
# Match the former Pandas-to-Polars conversion of computed NaN values.
df = df.fill_nan(None)

# gen AssetLiquidityMarketQuart = (cheq + .75*(actq - cheq) + .5*(atq - actq - gdwlq - intanq))/(l.atq + l.prccq*l.cshoq - l.ceqq)
print("Computing AssetLiquidityMarketQuart...")
df = df.with_columns(
    ((pl.col('cheq') + 0.75 * (pl.col('actq') - pl.col('cheq')) + 
      0.5 * (pl.col('atq') - pl.col('actq') - pl.col('gdwlq') - pl.col('intanq'))) / 
     (pl.col('l1_atq') + pl.col('l1_prccq') * pl.col('l1_cshoq') - pl.col('l1_ceqq'))).alias('AssetLiquidityMarketQuart')
)

print(f"Generated AssetLiquidityMarketQuart for {len(df)} observations")

# Keep only required columns for output
df_final = df.select(['permno', 'time_avail_m', 'AssetLiquidityMarketQuart'])

# SAVE
# do "$pathCode/saveplacebo" AssetLiquidityMarketQuart
save_placebo(df_final, 'AssetLiquidityMarketQuart')

print("AssetLiquidityMarketQuart.py completed")
