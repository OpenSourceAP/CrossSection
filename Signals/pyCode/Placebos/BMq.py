# ABOUTME: BMq.py - calculates BMq placebo (Book-to-market quarterly)
# ABOUTME: Python equivalent of BMq.do, translates line-by-line from Stata code

"""
BMq.py

Inputs:
    - SignalMasterTable.parquet: permno, gvkey, time_avail_m, mve_permco columns
    - m_QCompustat.parquet: gvkey, time_avail_m, ceqq columns

Outputs:
    - BMq.csv: permno, yyyymm, BMq columns

Usage:
    cd pyCode
    source .venv/bin/activate  
    python3 Placebos/BMq.py
"""

import pandas as pd
import polars as pl
import sys
import os

# Add parent directory to path to import utils
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from utils.saveplacebo import save_placebo
from utils.forward_fill import apply_quarterly_fill_to_compustat

print("Starting BMq.py")

# DATA LOAD
# use permno gvkey time_avail_m mve_permco using "$pathDataIntermediate/SignalMasterTable", clear
print("Loading SignalMasterTable...")
df = pl.read_parquet("../pyData/Intermediate/SignalMasterTable.parquet")
df = df.select(['permno', 'gvkey', 'time_avail_m', 'mve_permco'])

# keep if !mi(gvkey)
df = df.filter(pl.col('gvkey').is_not_null())

print(f"After filtering for non-null gvkey: {len(df)} rows")

# merge 1:1 gvkey time_avail_m using "$pathDataIntermediate/m_QCompustat", keepusing(ceqq) nogenerate keep(match)
print("Loading m_QCompustat...")
qcomp = pl.read_parquet("../pyData/Intermediate/m_QCompustat.parquet")
qcomp = qcomp.select(['gvkey', 'time_avail_m', 'ceqq'])

# Apply forward-fill logic to match Stata's handling of missing quarterly data
print("Applying forward-fill for missing ceqq values...")
qcomp = apply_quarterly_fill_to_compustat(qcomp, quarterly_columns=['ceqq'])

# Convert gvkey to same type for join
df = df.with_columns(pl.col('gvkey').cast(pl.Int32))
qcomp = qcomp.with_columns(pl.col('gvkey').cast(pl.Int32))

print("Merging with m_QCompustat...")
df = df.join(qcomp, on=['gvkey', 'time_avail_m'], how='inner')

print(f"After merge: {len(df)} rows")

# SIGNAL CONSTRUCTION
# gen BMq = log(ceqq/mve_permco)
df = df.with_columns(
    (pl.col('ceqq') / pl.col('mve_permco')).log().alias('BMq')
)

print(f"Generated BMq for {len(df)} observations")

# Keep only required columns for output
df_final = df.select(['permno', 'time_avail_m', 'BMq'])

# SAVE
# do "$pathCode/saveplacebo" BMq
save_placebo(df_final, 'BMq')

print("BMq.py completed")