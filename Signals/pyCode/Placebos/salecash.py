# ABOUTME: salecash.py - calculates salecash placebo (Sales to cash)
# ABOUTME: Python equivalent of salecash.do, translates line-by-line from Stata code

"""
salecash.py

Inputs:
    - m_aCompustat.parquet: gvkey, permno, time_avail_m, sale, che columns

Outputs:
    - salecash.csv: permno, yyyymm, salecash columns

Usage:
    cd pyCode
    source .venv/bin/activate  
    python3 Placebos/salecash.py
"""

import pandas as pd
import polars as pl
import sys
import os

# Add parent directory to path to import utils
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from utils.saveplacebo import save_placebo

print("Starting salecash.py")

# DATA LOAD
# use gvkey permno time_avail_m sale che using "$pathDataIntermediate/m_aCompustat", clear
print("Loading m_aCompustat...")
df = pl.read_parquet("../pyData/Intermediate/m_aCompustat.parquet")
df = df.select(['gvkey', 'permno', 'time_avail_m', 'sale', 'che'])

print(f"After loading: {len(df)} rows")

# SIGNAL CONSTRUCTION
# bysort permno time_avail_m: keep if _n == 1  // deletes a few observations
print("Dropping duplicates...")
df = df.unique(subset=['permno', 'time_avail_m'])

print(f"After dropping duplicates: {len(df)} rows")

# gen salecash = sale/che
print("Computing salecash...")
df = df.with_columns(
    (pl.col('sale') / pl.col('che')).alias('salecash')
)

print(f"Generated salecash for {len(df)} observations")

# Keep only required columns for output
df_final = df.select(['permno', 'time_avail_m', 'salecash'])

# SAVE
# do "$pathCode/saveplacebo" salecash
save_placebo(df_final, 'salecash')

print("salecash.py completed")