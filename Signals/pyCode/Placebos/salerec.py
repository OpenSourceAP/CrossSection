# ABOUTME: salerec.py - calculates salerec placebo (Sales to receivables)
# ABOUTME: Python equivalent of salerec.do, translates line-by-line from Stata code

"""
salerec.py

Inputs:
    - m_aCompustat.parquet: gvkey, permno, time_avail_m, sale, rect columns

Outputs:
    - salerec.csv: permno, yyyymm, salerec columns

Usage:
    cd pyCode
    source .venv/bin/activate  
    python3 Placebos/salerec.py
"""

import pandas as pd
import polars as pl
import sys
import os

# Add parent directory to path to import utils
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from utils.saveplacebo import save_placebo

print("Starting salerec.py")

# DATA LOAD
# use gvkey permno time_avail_m sale rect using "$pathDataIntermediate/m_aCompustat", clear
print("Loading m_aCompustat...")
df = pl.read_parquet("../pyData/Intermediate/m_aCompustat.parquet")
df = df.select(['gvkey', 'permno', 'time_avail_m', 'sale', 'rect'])

print(f"After loading: {len(df)} rows")

# SIGNAL CONSTRUCTION
# bysort permno time_avail_m: keep if _n == 1  // deletes a few observations
print("Dropping duplicates...")
df = df.unique(subset=['permno', 'time_avail_m'])

print(f"After dropping duplicates: {len(df)} rows")

# gen salerec = sale/rect
print("Computing salerec...")
df = df.with_columns(
    (pl.col('sale') / pl.col('rect')).alias('salerec')
)

print(f"Generated salerec for {len(df)} observations")

# Keep only required columns for output
df_final = df.select(['permno', 'time_avail_m', 'salerec'])

# SAVE
# do "$pathCode/saveplacebo" salerec
save_placebo(df_final, 'salerec')

print("salerec.py completed")