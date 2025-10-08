# ABOUTME: Tax_q.py - calculates taxable income to income ratio placebo (quarterly)
# ABOUTME: Python equivalent of Tax_q.do, translates line-by-line from Stata code

"""
Tax_q.py

Inputs:
    - SignalMasterTable.parquet: permno, gvkey, time_avail_m, mve_c columns
    - m_QCompustat.parquet: gvkey, time_avail_m, piq, niq columns

Outputs:
    - Tax_q.csv: permno, yyyymm, Tax_q columns

Usage:
    cd pyCode
    source .venv/bin/activate  
    python3 Placebos/Tax_q.py
"""

import pandas as pd
import polars as pl
import sys
import os

# Add parent directory to path to import utils
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from utils.saveplacebo import save_placebo

print("Starting Tax_q.py")

# DATA LOAD
# use permno gvkey time_avail_m mve_c using "$pathDataIntermediate/SignalMasterTable", clear
print("Loading SignalMasterTable...")
df = pl.read_parquet("../pyData/Intermediate/SignalMasterTable.parquet")
df = df.select(['permno', 'gvkey', 'time_avail_m', 'mve_c'])

# keep if !mi(gvkey)
df = df.filter(pl.col('gvkey').is_not_null())

print(f"After filtering for non-null gvkey: {len(df)} rows")

# merge 1:1 gvkey time_avail_m using "$pathDataIntermediate/m_QCompustat", keepusing(piq niq) nogenerate keep(match)
print("Loading m_QCompustat...")
qcomp = pl.read_parquet("../pyData/Intermediate/m_QCompustat.parquet")
qcomp = qcomp.select(['gvkey', 'time_avail_m', 'piq', 'niq'])

# Convert gvkey to same type for join
df = df.with_columns(pl.col('gvkey').cast(pl.Int32))
qcomp = qcomp.with_columns(pl.col('gvkey').cast(pl.Int32))

print("Merging with m_QCompustat...")
# keep(match) means inner join
df = df.join(qcomp, on=['gvkey', 'time_avail_m'], how='inner')

print(f"After merge: {len(df)} rows")

# SIGNAL CONSTRUCTION
# gen Tax_q = piq/niq if piq >0 & niq >0
print("Computing Tax_q...")
df = df.with_columns(
    pl.when((pl.col('piq') > 0) & (pl.col('niq') > 0))
    .then(pl.col('piq') / pl.col('niq'))
    .otherwise(None)
    .alias('Tax_q')
)

print(f"Generated Tax_q for {len(df)} observations")

# Keep only required columns for output
df_final = df.select(['permno', 'time_avail_m', 'Tax_q'])

# SAVE
# do "$pathCode/saveplacebo" Tax_q
save_placebo(df_final, 'Tax_q')

print("Tax_q.py completed")