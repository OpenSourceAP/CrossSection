# ABOUTME: secured.py - calculates secured placebo (Secured debt over liabilities)
# ABOUTME: Python equivalent of secured.do, translates line-by-line from Stata code

"""
secured.py

Inputs:
    - m_aCompustat.parquet: permno, time_avail_m, dm, dltt, dlc columns

Outputs:
    - secured.csv: permno, yyyymm, secured columns

Usage:
    cd pyCode
    source .venv/bin/activate  
    python3 Placebos/secured.py
"""

import pandas as pd
import polars as pl
import sys
import os

# Add parent directory to path to import utils
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from utils.saveplacebo import save_placebo

print("Starting secured.py")

# DATA LOAD
# use permno time_avail_m dm dltt dlc using "$pathDataIntermediate/m_aCompustat", clear
print("Loading m_aCompustat...")
df = pl.read_parquet("../pyData/Intermediate/m_aCompustat.parquet")
df = df.select(['permno', 'time_avail_m', 'dm', 'dltt', 'dlc'])

print(f"After loading: {len(df)} rows")

# SIGNAL CONSTRUCTION
# gen secured = dm/(dltt+dlc)
print("Computing secured...")
df = df.with_columns(
    (pl.col('dm') / (pl.col('dltt') + pl.col('dlc'))).alias('secured')
)

# replace secured = 0 if dltt ==. | dltt ==0 | dlc == .
print("Setting secured to 0 for specific conditions...")
df = df.with_columns(
    pl.when((pl.col('dltt').is_null()) | (pl.col('dltt') == 0) | (pl.col('dlc').is_null()))
    .then(0)
    .otherwise(pl.col('secured'))
    .alias('secured')
)

print(f"Generated secured for {len(df)} observations")

# Keep only required columns for output
df_final = df.select(['permno', 'time_avail_m', 'secured'])

# SAVE
# do "$pathCode/saveplacebo" secured
save_placebo(df_final, 'secured')

print("secured.py completed")