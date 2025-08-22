# ABOUTME: AssetGrowth_q.py - calculates AssetGrowth_q placebo (Asset Growth, quarterly)
# ABOUTME: Python equivalent of AssetGrowth_q.do, translates line-by-line from Stata code

"""
AssetGrowth_q.py

Inputs:
    - SignalMasterTable.parquet: permno, gvkey, time_avail_m columns
    - m_QCompustat.parquet: gvkey, time_avail_m, atq columns

Outputs:
    - AssetGrowth_q.csv: permno, yyyymm, AssetGrowth_q columns

Usage:
    cd pyCode
    source .venv/bin/activate  
    python3 Placebos/AssetGrowth_q.py
"""

import pandas as pd
import polars as pl
import sys
import os

# Add parent directory to path to import utils
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from utils.saveplacebo import save_placebo

print("Starting AssetGrowth_q.py")

# DATA LOAD
# use permno gvkey time_avail_m using "$pathDataIntermediate/SignalMasterTable", clear
print("Loading SignalMasterTable...")
df = pl.read_parquet("../pyData/Intermediate/SignalMasterTable.parquet")
df = df.select(['permno', 'gvkey', 'time_avail_m'])

# keep if !mi(gvkey)
df = df.filter(pl.col('gvkey').is_not_null())

print(f"After filtering for non-null gvkey: {len(df)} rows")

# merge 1:1 gvkey time_avail_m using "$pathDataIntermediate/m_QCompustat", keepusing(atq) nogenerate keep(match)
print("Loading m_QCompustat...")
qcomp = pl.read_parquet("../pyData/Intermediate/m_QCompustat.parquet")
qcomp = qcomp.select(['gvkey', 'time_avail_m', 'atq'])

# Convert gvkey to same type for join
df = df.with_columns(pl.col('gvkey').cast(pl.Int32))
qcomp = qcomp.with_columns(pl.col('gvkey').cast(pl.Int32))

print("Merging with m_QCompustat...")
df = df.join(qcomp, on=['gvkey', 'time_avail_m'], how='inner')

print(f"After merge: {len(df)} rows")

# SIGNAL CONSTRUCTION
# xtset permno time_avail_m
# gen AssetGrowth_q = (atq - l12.atq)/l12.atq
print("Sorting for lag operations...")
df = df.sort(['permno', 'time_avail_m'])

print("Computing 12-month lag...")
df = df.with_columns(
    pl.col('atq').shift(12).over('permno').alias('l12_atq')
)

print("Computing AssetGrowth_q...")
df = df.with_columns(
    ((pl.col('atq') - pl.col('l12_atq')) / pl.col('l12_atq')).alias('AssetGrowth_q')
)

print(f"Generated AssetGrowth_q for {len(df)} observations")

# Keep only required columns for output
df_final = df.select(['permno', 'time_avail_m', 'AssetGrowth_q'])

# SAVE
# do "$pathCode/saveplacebo" AssetGrowth_q
save_placebo(df_final, 'AssetGrowth_q')

print("AssetGrowth_q.py completed")