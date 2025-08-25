# ABOUTME: pchgm_pchsale.py - calculates margin growth over sales growth placebo
# ABOUTME: Python equivalent of pchgm_pchsale.do, translates line-by-line from Stata code

"""
pchgm_pchsale.py

Inputs:
    - m_aCompustat.parquet: gvkey, permno, time_avail_m, sale, cogs columns

Outputs:
    - pchgm_pchsale.csv: permno, yyyymm, pchgm_pchsale columns

Usage:
    cd pyCode
    source .venv/bin/activate  
    python3 Placebos/pchgm_pchsale.py
"""

import pandas as pd
import polars as pl
import sys
import os

# Add parent directory to path to import utils
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from utils.saveplacebo import save_placebo

print("Starting pchgm_pchsale.py")

# DATA LOAD
# use gvkey permno time_avail_m sale cogs using "$pathDataIntermediate/m_aCompustat", clear
print("Loading m_aCompustat...")
df = pl.read_parquet("../pyData/Intermediate/m_aCompustat.parquet")
df = df.select(['gvkey', 'permno', 'time_avail_m', 'sale', 'cogs'])

print(f"After loading m_aCompustat: {len(df)} rows")

# SIGNAL CONSTRUCTION
# bysort permno time_avail_m: keep if _n == 1  // deletes a few observations
print("Removing duplicates...")
df = df.unique(subset=['permno', 'time_avail_m'], maintain_order=True)

print(f"After removing duplicates: {len(df)} rows")

# xtset permno time_avail_m
print("Sorting by permno and time...")
df = df.sort(['permno', 'time_avail_m'])

# gen pchgm_pchsale = (((sale-cogs)-(l12.sale-l12.cogs))/(l12.sale-l12.cogs))-((sale-l12.sale)/l12.sale)
print("Computing lags and pchgm_pchsale...")

# Create 12-month lags
df = df.with_columns([
    pl.col('sale').shift(12).over('permno').alias('l12_sale'),
    pl.col('cogs').shift(12).over('permno').alias('l12_cogs')
])

# Calculate the components
df = df.with_columns([
    # Current gross margin: sale - cogs
    (pl.col('sale') - pl.col('cogs')).alias('gm_current'),
    # Lagged gross margin: l12.sale - l12.cogs  
    (pl.col('l12_sale') - pl.col('l12_cogs')).alias('gm_lagged'),
    # Sales change: sale - l12.sale
    (pl.col('sale') - pl.col('l12_sale')).alias('sale_change')
])

# Calculate pchgm_pchsale = ((gm_current - gm_lagged) / gm_lagged) - (sale_change / l12_sale)
df = df.with_columns(
    (((pl.col('gm_current') - pl.col('gm_lagged')) / pl.col('gm_lagged')) -
     (pl.col('sale_change') / pl.col('l12_sale'))).alias('pchgm_pchsale')
)

print(f"Generated pchgm_pchsale for {len(df)} observations")

# Keep only required columns for output
df_final = df.select(['permno', 'time_avail_m', 'pchgm_pchsale'])

# SAVE
# do "$pathCode/saveplacebo" pchgm_pchsale
save_placebo(df_final, 'pchgm_pchsale')

print("pchgm_pchsale.py completed")