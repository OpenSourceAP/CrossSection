# ABOUTME: Tax_q.py - calculates taxable income to income ratio placebo (quarterly)
# ABOUTME: Python equivalent of Tax_q.do, translates line-by-line from Stata code

"""
Tax_q.py

Inputs:
    - SignalMasterTable.parquet: permno, gvkey, time_avail_m, mve_permco columns
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
# use permno gvkey time_avail_m mve_permco using "$pathDataIntermediate/SignalMasterTable", clear
print("Loading SignalMasterTable...")
df = pl.read_parquet("../pyData/Intermediate/SignalMasterTable.parquet")
df = df.select(['permno', 'gvkey', 'time_avail_m', 'mve_permco'])

# keep if !mi(gvkey)
df = df.filter(pl.col('gvkey').is_not_null())

print(f"After filtering for non-null gvkey: {len(df)} rows")

# merge 1:1 gvkey time_avail_m using "$pathDataIntermediate/m_QCompustat", keepusing(piq niq) nogenerate keep(match)
print("Loading m_QCompustat...")
qcomp = pl.read_parquet("../pyData/Intermediate/m_QCompustat.parquet")
qcomp = qcomp.select(['gvkey', 'time_avail_m', 'piq', 'niq'])
# Apply enhanced group-wise forward-only fill for complete data coverage
print("Applying enhanced group-wise forward-only fill for quarterly data...")
qcomp = qcomp.sort(['gvkey', 'time_avail_m'])
qcomp = qcomp.with_columns([
    pl.col('piq').fill_null(strategy="forward").over('gvkey').alias('piq'),
    pl.col('niq').fill_null(strategy="forward").over('gvkey').alias('niq')
])