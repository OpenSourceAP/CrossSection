# ABOUTME: RD_q.py - calculates R&D-to-market cap ratio placebo (quarterly)
# ABOUTME: Python equivalent of RD_q.do, translates line-by-line from Stata code

"""
RD_q.py

Inputs:
    - SignalMasterTable.parquet: permno, gvkey, time_avail_m, mve_c columns
    - m_QCompustat.parquet: gvkey, time_avail_m, xrdq columns

Outputs:
    - RD_q.csv: permno, yyyymm, RD_q columns

Usage:
    cd pyCode
    source .venv/bin/activate  
    python3 Placebos/RD_q.py
"""

import pandas as pd
import polars as pl
import sys
import os

# Add parent directory to path to import utils
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from utils.saveplacebo import save_placebo

print("Starting RD_q.py")

# DATA LOAD
# use permno gvkey time_avail_m mve_c using "$pathDataIntermediate/SignalMasterTable", clear
print("Loading SignalMasterTable...")
df = pl.read_parquet("../pyData/Intermediate/SignalMasterTable.parquet")
df = df.select(['permno', 'gvkey', 'time_avail_m', 'mve_c'])

# drop if mi(gvkey)
df = df.filter(pl.col('gvkey').is_not_null())

print(f"After filtering for non-null gvkey: {len(df)} rows")

# merge 1:1 gvkey time_avail_m using "$pathDataIntermediate/m_QCompustat", keepusing(xrdq) nogenerate keep(match)
print("Loading m_QCompustat...")
qcomp = pl.read_parquet("../pyData/Intermediate/m_QCompustat.parquet")
qcomp = qcomp.select(['gvkey', 'time_avail_m', 'xrdq'])

# Convert gvkey to same type for join
df = df.with_columns(pl.col('gvkey').cast(pl.Int32))
qcomp = qcomp.with_columns(pl.col('gvkey').cast(pl.Int32))

print("Merging with m_QCompustat...")
df = df.join(qcomp, on=['gvkey', 'time_avail_m'], how='inner')

print(f"After merge: {len(df)} rows")

# SIGNAL CONSTRUCTION
# gen RD_q = xrdq/mve_c
print("Computing RD_q...")
df = df.with_columns(
    (pl.col('xrdq') / pl.col('mve_c')).alias('RD_q')
)

print(f"Generated RD_q for {len(df)} observations")

# Keep only required columns for output
df_final = df.select(['permno', 'time_avail_m', 'RD_q'])

# SAVE
# do "$pathCode/saveplacebo" RD_q
save_placebo(df_final, 'RD_q')

print("RD_q.py completed")