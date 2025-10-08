# ABOUTME: saleinv.py - calculates saleinv placebo (Sales to inventory)
# ABOUTME: Python equivalent of saleinv.do, translates line-by-line from Stata code

"""
saleinv.py

Inputs:
    - m_aCompustat.parquet: gvkey, permno, time_avail_m, sale, invt columns

Outputs:
    - saleinv.csv: permno, yyyymm, saleinv columns

Usage:
    cd pyCode
    source .venv/bin/activate  
    python3 Placebos/saleinv.py
"""

import pandas as pd
import polars as pl
import sys
import os

# Add parent directory to path to import utils
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from utils.saveplacebo import save_placebo

print("Starting saleinv.py")

# DATA LOAD
# use gvkey permno time_avail_m sale invt using "$pathDataIntermediate/m_aCompustat", clear
print("Loading m_aCompustat...")
df = pl.read_parquet("../pyData/Intermediate/m_aCompustat.parquet")
df = df.select(['gvkey', 'permno', 'time_avail_m', 'sale', 'invt'])

print(f"After loading: {len(df)} rows")

# SIGNAL CONSTRUCTION
# bysort permno time_avail_m: keep if _n == 1  // deletes a few observations
print("Dropping duplicates...")
df = df.unique(subset=['permno', 'time_avail_m'])

print(f"After dropping duplicates: {len(df)} rows")

# gen saleinv = sale/invt
print("Computing saleinv...")
df = df.with_columns(
    (pl.col('sale') / pl.col('invt')).alias('saleinv')
)

print(f"Generated saleinv for {len(df)} observations")

# Keep only required columns for output
df_final = df.select(['permno', 'time_avail_m', 'saleinv'])

# SAVE
# do "$pathCode/saveplacebo" saleinv
save_placebo(df_final, 'saleinv')

print("saleinv.py completed")