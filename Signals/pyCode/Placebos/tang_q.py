# ABOUTME: tang_q.py - calculates tang_q placebo (Tangibility, quarterly)
# ABOUTME: Python equivalent of tang_q.do, translates line-by-line from Stata code

"""
tang_q.py

Inputs:
    - SignalMasterTable.parquet: permno, gvkey, time_avail_m, mve_permco columns
    - m_QCompustat.parquet: gvkey, time_avail_m, cheq, rectq, invtq, ppegtq, atq columns

Outputs:
    - tang_q.csv: permno, yyyymm, tang_q columns

Usage:
    cd pyCode
    source .venv/bin/activate  
    python3 Placebos/tang_q.py
"""

import pandas as pd
import polars as pl
import sys
import os

# Add parent directory to path to import utils
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from utils.saveplacebo import save_placebo
from utils.forward_fill import apply_quarterly_fill_to_compustat

print("Starting tang_q.py")

# DATA LOAD
# use permno gvkey time_avail_m mve_permco using "$pathDataIntermediate/SignalMasterTable", clear
print("Loading SignalMasterTable...")
df = pl.read_parquet("../pyData/Intermediate/SignalMasterTable.parquet")
df = df.select(['permno', 'gvkey', 'time_avail_m', 'mve_permco'])

# keep if !mi(gvkey)
df = df.filter(pl.col('gvkey').is_not_null())

print(f"After filtering for non-null gvkey: {len(df)} rows")

# merge 1:1 gvkey time_avail_m using "$pathDataIntermediate/m_QCompustat", keepusing(cheq rectq invtq ppegtq atq) nogenerate keep(match)
print("Loading m_QCompustat...")
qcomp = pl.read_parquet("../pyData/Intermediate/m_QCompustat.parquet")
qcomp = qcomp.select(['gvkey', 'time_avail_m', 'cheq', 'rectq', 'invtq', 'ppegtq', 'atq'])

# Convert gvkey to same type for join
df = df.with_columns(pl.col('gvkey').cast(pl.Int32))
qcomp = qcomp.with_columns(pl.col('gvkey').cast(pl.Int32))

print("Applying forward fill for missing quarterly values...")
qcomp = qcomp.sort(['gvkey', 'time_avail_m'])
qcomp = apply_quarterly_fill_to_compustat(
    qcomp,
    quarterly_columns=['cheq', 'rectq', 'invtq', 'ppegtq', 'atq']
)

print("Merging with m_QCompustat...")
# Use left join to preserve SignalMasterTable observations
# Stata's keep(match) might be more lenient about missing values
df = df.join(qcomp, on=['gvkey', 'time_avail_m'], how='left')

print(f"After merge: {len(df)} rows")

# SIGNAL CONSTRUCTION
# gen tang_q = (cheq + .715*rectq + .547*invtq + .535*ppegtq)/atq
df = df.with_columns(
    ((pl.col('cheq') + 0.715 * pl.col('rectq') + 0.547 * pl.col('invtq') + 0.535 * pl.col('ppegtq')) / pl.col('atq')).alias('tang_q')
)

print(f"Generated tang_q for {len(df)} observations")

# Keep only required columns for output
df_final = df.select(['permno', 'time_avail_m', 'tang_q'])

# SAVE
# do "$pathCode/saveplacebo" tang_q
save_placebo(df_final, 'tang_q')

print("tang_q.py completed")
