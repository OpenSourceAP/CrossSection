# ABOUTME: AssetTurnover_q.py - calculates quarterly asset turnover placebo
# ABOUTME: Python equivalent of AssetTurnover_q.do, translates line-by-line from Stata code

"""
AssetTurnover_q.py

Inputs:
    - SignalMasterTable.parquet: permno, gvkey, time_avail_m, mve_c columns
    - m_QCompustat.parquet: gvkey, time_avail_m, rectq, invtq, acoq, ppentq, intanq, apq, lcoq, loq, saleq columns

Outputs:
    - AssetTurnover_q.csv: permno, yyyymm, AssetTurnover_q columns

Usage:
    cd pyCode
    source .venv/bin/activate  
    python3 Placebos/AssetTurnover_q.py
"""

import pandas as pd
import polars as pl
import sys
import os

# Add parent directory to path to import utils
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from utils.saveplacebo import save_placebo
from utils.forward_fill import apply_quarterly_fill_to_compustat

print("Starting AssetTurnover_q.py")

# DATA LOAD
# use permno gvkey time_avail_m mve_c using "$pathDataIntermediate/SignalMasterTable", clear
print("Loading SignalMasterTable...")
df = pl.read_parquet("../pyData/Intermediate/SignalMasterTable.parquet")
df = df.select(['permno', 'gvkey', 'time_avail_m', 'mve_c'])

# keep if !mi(gvkey)
df = df.filter(pl.col('gvkey').is_not_null())

print(f"After filtering for non-null gvkey: {len(df)} rows")
# Apply enhanced group-wise forward+backward fill for complete quarterly data coverage
print("Applying enhanced group-wise forward+backward fill for quarterly asset data...")
df = df.sort(['permno', 'time_avail_m'])
df = df.with_columns([
    pl.col('rectq').fill_null(strategy="forward").fill_null(strategy="backward").over('permno').alias('rectq'),
    pl.col('invtq').fill_null(strategy="forward").fill_null(strategy="backward").over('permno').alias('invtq'),
    pl.col('acoq').fill_null(strategy="forward").fill_null(strategy="backward").over('permno').alias('acoq'),
    pl.col('ppentq').fill_null(strategy="forward").fill_null(strategy="backward").over('permno').alias('ppentq'),
    pl.col('intanq').fill_null(strategy="forward").fill_null(strategy="backward").over('permno').alias('intanq'),
    pl.col('apq').fill_null(strategy="forward").fill_null(strategy="backward").over('permno').alias('apq'),
    pl.col('lcoq').fill_null(strategy="forward").fill_null(strategy="backward").over('permno').alias('lcoq'),
    pl.col('loq').fill_null(strategy="forward").fill_null(strategy="backward").over('permno').alias('loq'),
    pl.col('saleq').fill_null(strategy="forward").fill_null(strategy="backward").over('permno').alias('saleq')
])