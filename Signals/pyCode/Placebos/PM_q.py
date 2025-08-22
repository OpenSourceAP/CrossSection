# ABOUTME: PM_q.py - calculates quarterly profit margin placebo
# ABOUTME: Python equivalent of PM_q.do, translates line-by-line from Stata code

"""
PM_q.py

Inputs:
    - SignalMasterTable.parquet: permno, gvkey, time_avail_m, mve_c columns
    - m_QCompustat.parquet: gvkey, time_avail_m, niq, revtq columns

Outputs:
    - PM_q.csv: permno, yyyymm, PM_q columns

Usage:
    cd pyCode
    source .venv/bin/activate  
    python3 Placebos/PM_q.py
"""

import pandas as pd
import polars as pl
import sys
import os

# Add parent directory to path to import utils
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from utils.saveplacebo import save_placebo

print("Starting PM_q.py")

# DATA LOAD
# use permno gvkey time_avail_m mve_c using "$pathDataIntermediate/SignalMasterTable", clear
print("Loading SignalMasterTable...")
df = pl.read_parquet("../pyData/Intermediate/SignalMasterTable.parquet")
df = df.select(['permno', 'gvkey', 'time_avail_m', 'mve_c'])

# keep if !mi(gvkey)
df = df.filter(pl.col('gvkey').is_not_null())

print(f"After filtering for non-null gvkey: {len(df)} rows")

# merge 1:1 gvkey time_avail_m using "$pathDataIntermediate/m_QCompustat", keepusing(niq revtq) nogenerate keep(match)
print("Loading m_QCompustat...")
qcomp = pl.read_parquet("../pyData/Intermediate/m_QCompustat.parquet")
qcomp = qcomp.select(['gvkey', 'time_avail_m', 'niq', 'revtq'])

# Convert gvkey to same type for join
df = df.with_columns(pl.col('gvkey').cast(pl.Int32))
qcomp = qcomp.with_columns(pl.col('gvkey').cast(pl.Int32))

print("Merging with m_QCompustat...")
df = df.join(qcomp, on=['gvkey', 'time_avail_m'], how='inner')

print(f"After merge: {len(df)} rows")

# SIGNAL CONSTRUCTION
# gen PM_q = niq/revtq
print("Computing PM_q...")
df = df.with_columns(
    (pl.col('niq') / pl.col('revtq')).alias('PM_q')
)

print(f"Generated PM_q for {len(df)} observations")

# Keep only required columns for output
df_final = df.select(['permno', 'time_avail_m', 'PM_q'])

# SAVE
# do "$pathCode/saveplacebo" PM_q
save_placebo(df_final, 'PM_q')

print("PM_q.py completed")