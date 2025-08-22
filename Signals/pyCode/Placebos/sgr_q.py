# ABOUTME: sgr_q.py - calculates sgr_q placebo (Quarterly sales growth)
# ABOUTME: Python equivalent of sgr_q.do, translates line-by-line from Stata code

"""
sgr_q.py

Inputs:
    - SignalMasterTable.parquet: permno, gvkey, time_avail_m, mve_c columns
    - m_QCompustat.parquet: gvkey, time_avail_m, saleq columns

Outputs:
    - sgr_q.csv: permno, yyyymm, sgr_q columns

Usage:
    cd pyCode
    source .venv/bin/activate  
    python3 Placebos/sgr_q.py
"""

import pandas as pd
import polars as pl
import sys
import os

# Add parent directory to path to import utils
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from utils.saveplacebo import save_placebo

print("Starting sgr_q.py")

# DATA LOAD
# use permno gvkey time_avail_m mve_c using "$pathDataIntermediate/SignalMasterTable", clear
print("Loading SignalMasterTable...")
df = pl.read_parquet("../pyData/Intermediate/SignalMasterTable.parquet")
df = df.select(['permno', 'gvkey', 'time_avail_m', 'mve_c'])

# keep if !mi(gvkey)
df = df.filter(pl.col('gvkey').is_not_null())

print(f"After filtering for non-null gvkey: {len(df)} rows")

# merge 1:1 gvkey time_avail_m using "$pathDataIntermediate/m_QCompustat", keepusing(saleq) nogenerate keep(match)
print("Loading m_QCompustat...")
qcomp = pl.read_parquet("../pyData/Intermediate/m_QCompustat.parquet")
qcomp = qcomp.select(['gvkey', 'time_avail_m', 'saleq'])

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

# gen sgr_q = (saleq/l12.saleq)-1
print("Computing 12-month lag and sgr_q...")
df = df.with_columns(
    pl.col('saleq').shift(12).over('permno').alias('l12_saleq')
)

df = df.with_columns(
    ((pl.col('saleq') / pl.col('l12_saleq')) - 1).alias('sgr_q')
)

print(f"Generated sgr_q for {len(df)} observations")

# Keep only required columns for output
df_final = df.select(['permno', 'time_avail_m', 'sgr_q'])

# SAVE
# do "$pathCode/saveplacebo" sgr_q
save_placebo(df_final, 'sgr_q')

print("sgr_q.py completed")