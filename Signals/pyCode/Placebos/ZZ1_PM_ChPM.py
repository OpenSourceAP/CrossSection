# ABOUTME: ZZ1_PM_ChPM.py - calculates profit margin and change in profit margin placebos
# ABOUTME: Python equivalent of ZZ1_PM_ChPM.do, translates line-by-line from Stata code

"""
ZZ1_PM_ChPM.py

Inputs:
    - m_aCompustat.parquet: gvkey, permno, time_avail_m, ni, revt columns

Outputs:
    - PM.csv: permno, yyyymm, PM columns
    - ChPM.csv: permno, yyyymm, ChPM columns

Usage:
    cd pyCode
    source .venv/bin/activate  
    python3 Placebos/ZZ1_PM_ChPM.py
"""

import pandas as pd
import polars as pl
import sys
import os

# Add parent directory to path to import utils
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from utils.stata_replication import fill_date_gaps, stata_multi_lag
from utils.saveplacebo import save_placebo

print("Starting ZZ1_PM_ChPM.py")

# DATA LOAD
# use gvkey permno time_avail_m ni revt using "$pathDataIntermediate/m_aCompustat", clear
print("Loading m_aCompustat...")
df = pl.read_parquet("../pyData/Intermediate/m_aCompustat.parquet")
df = df.select(['gvkey', 'permno', 'time_avail_m', 'ni', 'revt'])

print(f"After loading m_aCompustat: {len(df)} rows")

# bysort permno time_avail_m: keep if _n == 1  // deletes a few observations
print("Removing duplicates...")
df = df.unique(subset=['permno', 'time_avail_m'], maintain_order=True)

print(f"After removing duplicates: {len(df)} rows")

# SIGNAL CONSTRUCTION
# xtset permno time_avail_m
print("Sorting by permno and time...")
df = df.sort(['permno', 'time_avail_m'])

# gen PM = ni/revt
print("Computing PM...")
df = df.with_columns([
    (pl.col('ni') / pl.col('revt')).alias('PM')
])

# gen ChPM = PM - l12.PM
print("Computing ChPM with 12-month calendar-based lag...")

# Calendar endpoints require the target month; retain only observed rows.
df = df.with_columns(pl.lit(True).alias("_observed"))
df = fill_date_gaps(df, "permno", "time_avail_m", "1mo")
df = stata_multi_lag(df, "permno", "time_avail_m", ['PM'], [12], prefix="l", fill_gaps=False)
df = df.filter(pl.col("_observed").eq(True)).drop("_observed")
# Match the former Pandas-to-Polars conversion of computed NaN values.
df = df.fill_nan(None)

# Compute ChPM
df = df.with_columns([
    (pl.col('PM') - pl.col('l12_PM')).alias('ChPM')
])

print(f"Generated PM and ChPM for {len(df)} observations")

# SAVE
# do "$pathCode/saveplacebo" PM
df_PM = df.select(['permno', 'time_avail_m', 'PM'])
save_placebo(df_PM, 'PM')

# do "$pathCode/saveplacebo" ChPM
df_ChPM = df.select(['permno', 'time_avail_m', 'ChPM'])
save_placebo(df_ChPM, 'ChPM')

print("ZZ1_PM_ChPM.py completed")
