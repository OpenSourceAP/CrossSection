# ABOUTME: GPlag_q.py - calculates gross profitability quarterly placebo
# ABOUTME: Python equivalent of GPlag_q.do, translates line-by-line from Stata code

"""
GPlag_q.py

Inputs:
    - SignalMasterTable.parquet: permno, gvkey, time_avail_m, mve_c columns
    - m_QCompustat.parquet: gvkey, time_avail_m, revtq, cogsq, atq columns

Outputs:
    - GPlag_q.csv: permno, yyyymm, GPlag_q columns

Usage:
    cd pyCode
    source .venv/bin/activate  
    python3 Placebos/GPlag_q.py
"""

import pandas as pd
import polars as pl
import sys
import os

# Add parent directory to path to import utils
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from utils.saveplacebo import save_placebo

print("Starting GPlag_q.py")

# DATA LOAD
# use permno gvkey time_avail_m mve_c using "$pathDataIntermediate/SignalMasterTable", clear
print("Loading SignalMasterTable...")
df = pl.read_parquet("../pyData/Intermediate/SignalMasterTable.parquet")
df = df.select(['permno', 'gvkey', 'time_avail_m', 'mve_c'])

# keep if !mi(gvkey)
df = df.filter(pl.col('gvkey').is_not_null())

print(f"After filtering for non-null gvkey: {len(df)} rows")

# merge 1:1 gvkey time_avail_m using "$pathDataIntermediate/m_QCompustat", keepusing(revtq cogsq atq) nogenerate keep(match)
print("Loading m_QCompustat...")
qcomp = pl.read_parquet("../pyData/Intermediate/m_QCompustat.parquet")
qcomp = qcomp.select(['gvkey', 'time_avail_m', 'revtq', 'cogsq', 'atq'])

# Convert gvkey to same type for join
df = df.with_columns(pl.col('gvkey').cast(pl.Int32))
qcomp = qcomp.with_columns(pl.col('gvkey').cast(pl.Int32))

print("Merging with m_QCompustat...")
df = df.join(qcomp, on=['gvkey', 'time_avail_m'], how='inner')

print(f"After merge: {len(df)} rows")

# SIGNAL CONSTRUCTION
# xtset permno time_avail_m
print("Sorting by permno and time...")
df = df.sort(['permno', 'time_avail_m'])

# gen GPlag_q = (revtq - cogsq)/l3.atq
print("Computing GPlag_q...")
df = df.with_columns([
    pl.col('atq').shift(3).over('permno').alias('l3_atq')
])

df = df.with_columns(
    ((pl.col('revtq') - pl.col('cogsq')) / pl.col('l3_atq')).alias('GPlag_q')
)

print(f"Generated GPlag_q for {len(df)} observations")

# Keep only required columns for output
df_final = df.select(['permno', 'time_avail_m', 'GPlag_q'])

# SAVE
# do "$pathCode/saveplacebo" GPlag_q
save_placebo(df_final, 'GPlag_q')

print("GPlag_q.py completed")