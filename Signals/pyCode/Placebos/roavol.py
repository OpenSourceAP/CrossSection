# ABOUTME: roavol.py - calculates RoA volatility placebo
# ABOUTME: Python equivalent of roavol.do, translates line-by-line from Stata code

"""
roavol.py

Inputs:
    - SignalMasterTable.parquet: permno, gvkey, time_avail_m columns
    - m_QCompustat.parquet: gvkey, time_avail_m, ibq, atq columns

Outputs:
    - roavol.csv: permno, yyyymm, roavol columns

Usage:
    cd pyCode
    source .venv/bin/activate  
    python3 Placebos/roavol.py
"""

import pandas as pd
import polars as pl
import sys
import os

# Add parent directory to path to import utils
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from utils.save_standardized import save_placebo
from utils.asrol import asrol
from utils.stata_replication import stata_multi_lag

print("Starting roavol.py")

# DATA LOAD
# use permno gvkey time_avail_m using "$pathDataIntermediate/SignalMasterTable", clear
print("Loading SignalMasterTable...")
df = pl.read_parquet("../pyData/Intermediate/SignalMasterTable.parquet")
df = df.select(['permno', 'gvkey', 'time_avail_m'])

# keep if !mi(gvkey)
df = df.filter(pl.col('gvkey').is_not_null())

print(f"After filtering for non-null gvkey: {len(df)} rows")

# merge 1:1 gvkey time_avail_m using "$pathDataIntermediate/m_QCompustat", keepusing(ibq atq) nogenerate keep(match)
print("Loading m_QCompustat...")
qcomp = pl.read_parquet("../pyData/Intermediate/m_QCompustat.parquet")
qcomp = qcomp.select(['gvkey', 'time_avail_m', 'ibq', 'atq'])

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

# gen roaq = ibq/l3.atq
print("Computing roaq with 3-quarter lag using stata_multi_lag...")
df_pandas = df.to_pandas()
df_pandas = stata_multi_lag(df_pandas, 'permno', 'time_avail_m', 'atq', [3], freq='M', prefix='l')
df = pl.from_pandas(df_pandas)

df = df.with_columns(
    (pl.col('ibq') / pl.col('l3_atq')).alias('roaq')
)

# bys permno: asrol roaq, gen(roavol) stat(sd) window(time_avail_m 48) min(24)
print("Computing rolling standard deviation...")
# Use time-based rolling window with 48 months and min 24 periods
df = asrol(df,
           group_col='permno',
           time_col='time_avail_m',
           freq='1mo',
           window=48,
           value_col='roaq',
           stat='sd',
           new_col_name='roavol',
           min_samples=24)  # Match Stata's min(24)

print(f"Generated roavol for {len(df)} observations")

# Keep only required columns for output
df_final = df.select(['permno', 'time_avail_m', 'roavol'])

# SAVE
# do "$pathCode/saveplacebo" roavol
save_placebo(df_final, 'roavol')

print("roavol.py completed")