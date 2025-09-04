# ABOUTME: EPq.py - calculates EPq placebo (Earnings-to-price ratio, quarterly)
# ABOUTME: Python equivalent of EPq.do, translates line-by-line from Stata code

"""
EPq.py

Inputs:
    - SignalMasterTable.parquet: permno, gvkey, time_avail_m, mve_c columns
    - m_QCompustat.parquet: gvkey, time_avail_m, ibq columns

Outputs:
    - EPq.csv: permno, yyyymm, EPq columns

Usage:
    cd pyCode
    source .venv/bin/activate  
    python3 Placebos/EPq.py
"""

import pandas as pd
import polars as pl
import sys
import os

# Add parent directory to path to import utils
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from utils.save_standardized import save_placebo
from utils.stata_replication import stata_multi_lag

print("Starting EPq.py")

# DATA LOAD
# use permno gvkey time_avail_m mve_c using "$pathDataIntermediate/SignalMasterTable", clear
print("Loading SignalMasterTable...")
df = pl.read_parquet("../pyData/Intermediate/SignalMasterTable.parquet")
df = df.select(['permno', 'gvkey', 'time_avail_m', 'mve_c'])

# keep if !mi(gvkey)
df = df.filter(pl.col('gvkey').is_not_null())

print(f"After filtering for non-null gvkey: {len(df)} rows")

# merge 1:1 gvkey time_avail_m using "$pathDataIntermediate/m_QCompustat", keepusing(ibq) nogenerate keep(match)
print("Loading m_QCompustat...")
qcomp = pl.read_parquet("../pyData/Intermediate/m_QCompustat.parquet")
qcomp = qcomp.select(['gvkey', 'time_avail_m', 'ibq'])

# Convert gvkey to same type for join
df = df.with_columns(pl.col('gvkey').cast(pl.Int32))
qcomp = qcomp.with_columns(pl.col('gvkey').cast(pl.Int32))

print("Merging with m_QCompustat...")
# keep(match) means inner join
df = df.join(qcomp, on=['gvkey', 'time_avail_m'], how='inner')

print(f"After merge: {len(df)} rows")

# SIGNAL CONSTRUCTION
# xtset permno time_avail_m
# gen EPq = ibq/l6.mve_c
print("Sorting for lag operations...")
df = df.sort(['permno', 'time_avail_m'])

# Calculate 6-month lag using stata_multi_lag
print("Computing 6-month lag using stata_multi_lag...")

# Convert to pandas for stata_multi_lag
df_pandas = df.to_pandas()
df_pandas = stata_multi_lag(df_pandas, 'permno', 'time_avail_m', 'mve_c', [6], freq='M', prefix='l')

# Convert back to polars
df = pl.from_pandas(df_pandas)

df = df.with_columns(
    (pl.col('ibq') / pl.col('l6_mve_c')).alias('EPq')
)

# replace EPq = . if EPq < 0
print("Setting negative EPq to null...")
df = df.with_columns(
    pl.when(pl.col('EPq') < 0)
    .then(None)
    .otherwise(pl.col('EPq'))
    .alias('EPq')
)

print(f"Generated EPq for {len(df)} observations")

# Keep only required columns for output
df_final = df.select(['permno', 'time_avail_m', 'EPq'])

# SAVE
# do "$pathCode/saveplacebo" EPq
save_placebo(df_final, 'EPq')

print("EPq.py completed")