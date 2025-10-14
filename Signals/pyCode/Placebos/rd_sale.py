# ABOUTME: rd_sale.py - calculates rd_sale placebo (R&D-to-sales ratio)
# ABOUTME: Python equivalent of rd_sale.do, translates line-by-line from Stata code

"""
rd_sale.py

Inputs:
    - m_aCompustat.parquet: gvkey, permno, time_avail_m, xrd, sale columns

Outputs:
    - rd_sale.csv: permno, yyyymm, rd_sale columns

Usage:
    cd pyCode
    source .venv/bin/activate  
    python3 Placebos/rd_sale.py
"""

import pandas as pd
import polars as pl
import sys
import os

# Add parent directory to path to import utils
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from utils.saveplacebo import save_placebo

print("Starting rd_sale.py")

# DATA LOAD
# use gvkey permno time_avail_m xrd sale using "$pathDataIntermediate/m_aCompustat", clear
print("Loading m_aCompustat...")
df = pl.read_parquet("../pyData/Intermediate/m_aCompustat.parquet")
df = df.select(['gvkey', 'permno', 'time_avail_m', 'xrd', 'sale'])

print(f"After loading: {len(df)} rows")

# SIGNAL CONSTRUCTION
# xtset permno time_avail_m
print("Sorting for lag operations...")
df = df.sort(['permno', 'time_avail_m'])

# gen rd_sale = l12.xrd/l12.sale  // Returns seem to be strongest in the second year after portfolio formation
print("Computing 12-month lag and rd_sale...")
df = df.with_columns([
    pl.col('xrd').shift(12).over('permno').alias('l12_xrd'),
    pl.col('sale').shift(12).over('permno').alias('l12_sale')
])

df = df.with_columns(
    (pl.col('l12_xrd') / pl.col('l12_sale')).alias('rd_sale')
)

# replace rd_sale = . if rd_sale == 0
print("Setting rd_sale to null where it equals 0...")
df = df.with_columns(
    pl.when(pl.col('rd_sale') == 0)
    .then(None)
    .otherwise(pl.col('rd_sale'))
    .alias('rd_sale')
)

print(f"Generated rd_sale for {len(df)} observations")

# Keep only required columns for output
df_final = df.select(['permno', 'time_avail_m', 'rd_sale'])

# SAVE
# do "$pathCode/saveplacebo" rd_sale
save_placebo(df_final, 'rd_sale')

print("rd_sale.py completed")