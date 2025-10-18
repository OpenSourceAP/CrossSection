# ABOUTME: EBM_q.py - calculates EBM_q placebo (Enterprise component of BM, quarterly)
# ABOUTME: Python equivalent of EBM_q.do, translates line-by-line from Stata code

"""
EBM_q.py

Inputs:
    - SignalMasterTable.parquet: permno, gvkey, time_avail_m, mve_permco columns
    - m_QCompustat.parquet: gvkey, time_avail_m, cheq, dlttq, dlcq, pstkq, ceqq columns

Outputs:
    - EBM_q.csv: permno, yyyymm, EBM_q columns

Usage:
    cd pyCode
    source .venv/bin/activate  
    python3 Placebos/EBM_q.py
"""

import pandas as pd
import polars as pl
import sys
import os

# Add parent directory to path to import utils
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from utils.saveplacebo import save_placebo

print("Starting EBM_q.py")

# DATA LOAD
# use permno gvkey time_avail_m mve_permco using "$pathDataIntermediate/SignalMasterTable", clear
print("Loading SignalMasterTable...")
df = pl.read_parquet("../pyData/Intermediate/SignalMasterTable.parquet")
df = df.select(['permno', 'gvkey', 'time_avail_m', 'mve_permco'])

# keep if !mi(gvkey)
df = df.filter(pl.col('gvkey').is_not_null())

print(f"After filtering for non-null gvkey: {len(df)} rows")

# merge 1:1 gvkey time_avail_m using "$pathDataIntermediate/m_QCompustat", keepusing(cheq dlttq dlcq pstkq ceqq) nogenerate keep(match)
print("Loading m_QCompustat...")
qcomp = pl.read_parquet("../pyData/Intermediate/m_QCompustat.parquet")
qcomp = qcomp.select(['gvkey', 'time_avail_m', 'cheq', 'dlttq', 'dlcq', 'pstkq', 'ceqq'])

# Convert gvkey to same type for join
df = df.with_columns(pl.col('gvkey').cast(pl.Int32))
qcomp = qcomp.with_columns(pl.col('gvkey').cast(pl.Int32))

print("Merging with m_QCompustat...")
df = df.join(qcomp, on=['gvkey', 'time_avail_m'], how='inner')

print(f"After merge: {len(df)} rows")

# SIGNAL CONSTRUCTION
# gen temp = cheq - dlttq - dlcq - pstkq
print("Computing temp...")
df = df.with_columns(
    (pl.col('cheq') - pl.col('dlttq') - pl.col('dlcq') - pl.col('pstkq')).alias('temp')
)

# gen EBM_q = (ceqq + temp)/(mve_permco + temp)
print("Computing EBM_q...")
df = df.with_columns(
    ((pl.col('ceqq') + pl.col('temp')) / (pl.col('mve_permco') + pl.col('temp'))).alias('EBM_q')
)

print(f"Generated EBM_q for {len(df)} observations")

# Keep only required columns for output
df_final = df.select(['permno', 'time_avail_m', 'EBM_q'])

# SAVE
# do "$pathCode/saveplacebo" EBM_q
save_placebo(df_final, 'EBM_q')

print("EBM_q.py completed")