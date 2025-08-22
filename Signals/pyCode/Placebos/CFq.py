# ABOUTME: CFq.py - calculates CFq placebo (Cash-flow to market, quarterly)
# ABOUTME: Python equivalent of CFq.do, translates line-by-line from Stata code

"""
CFq.py

Inputs:
    - SignalMasterTable.parquet: permno, gvkey, time_avail_m, mve_c columns
    - m_QCompustat.parquet: gvkey, time_avail_m, ibq, dpq columns

Outputs:
    - CFq.csv: permno, yyyymm, CFq columns

Usage:
    cd pyCode
    source .venv/bin/activate  
    python3 Placebos/CFq.py
"""

import pandas as pd
import polars as pl
import sys
import os

# Add parent directory to path to import utils
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from utils.saveplacebo import save_placebo

print("Starting CFq.py")

# DATA LOAD
# use permno gvkey time_avail_m mve_c using "$pathDataIntermediate/SignalMasterTable", clear
print("Loading SignalMasterTable...")
df = pl.read_parquet("../pyData/Intermediate/SignalMasterTable.parquet")
df = df.select(['permno', 'gvkey', 'time_avail_m', 'mve_c'])

# keep if !mi(gvkey)
df = df.filter(pl.col('gvkey').is_not_null())

print(f"After filtering for non-null gvkey: {len(df)} rows")

# merge 1:1 gvkey time_avail_m using "$pathDataIntermediate/m_QCompustat", keepusing(ibq dpq) nogenerate keep(match)
print("Loading m_QCompustat...")
qcomp = pl.read_parquet("../pyData/Intermediate/m_QCompustat.parquet")
qcomp = qcomp.select(['gvkey', 'time_avail_m', 'ibq', 'dpq'])

# Convert gvkey to same type for join
df = df.with_columns(pl.col('gvkey').cast(pl.Int32))
qcomp = qcomp.with_columns(pl.col('gvkey').cast(pl.Int32))

print("Merging with m_QCompustat...")
df = df.join(qcomp, on=['gvkey', 'time_avail_m'], how='inner')

print(f"After merge: {len(df)} rows")

# SIGNAL CONSTRUCTION
# gen CFq = (ibq + dpq)/mve_c
df = df.with_columns(
    ((pl.col('ibq') + pl.col('dpq')) / pl.col('mve_c')).alias('CFq')
)

print(f"Generated CFq for {len(df)} observations")

# Keep only required columns for output
df_final = df.select(['permno', 'time_avail_m', 'CFq'])

# SAVE
# do "$pathCode/saveplacebo" CFq
save_placebo(df_final, 'CFq')

print("CFq.py completed")