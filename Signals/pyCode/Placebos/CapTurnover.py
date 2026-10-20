# ABOUTME: CapTurnover.py - calculates capital turnover placebo
# ABOUTME: Python equivalent of CapTurnover.do, translates line-by-line from Stata code

"""
CapTurnover.py

Inputs:
    - m_aCompustat.parquet: gvkey, permno, time_avail_m, sale, at columns

Outputs:
    - CapTurnover.csv: permno, yyyymm, CapTurnover columns

Usage:
    cd pyCode
    source .venv/bin/activate  
    python3 Placebos/CapTurnover.py
"""

import pandas as pd
import polars as pl
import sys
import os

# Add parent directory to path to import utils
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from utils.stata_replication import fill_date_gaps, stata_multi_lag
from utils.saveplacebo import save_placebo

print("Starting CapTurnover.py")

# DATA LOAD
# use gvkey permno time_avail_m sale at using "$pathDataIntermediate/m_aCompustat", clear
print("Loading m_aCompustat...")
df = pl.read_parquet("../pyData/Intermediate/m_aCompustat.parquet")
df = df.select(['gvkey', 'permno', 'time_avail_m', 'sale', 'at'])

print(f"Loaded {len(df)} rows")

# SIGNAL CONSTRUCTION
# bysort permno time_avail_m: keep if _n == 1  // deletes a few observations
print("Removing duplicates...")
df = df.unique(subset=['permno', 'time_avail_m'], keep='first')

print(f"After removing duplicates: {len(df)} rows")

# xtset permno time_avail_m
print("Sorting for lag operations...")
df = df.sort(['permno', 'time_avail_m'])

# gen CapTurnover = l12.sale/l24.at
print("Computing 12-month and 24-month calendar-based lags and CapTurnover...")

# Calendar endpoints require the target month; retain only observed rows.
df = df.with_columns(pl.lit(True).alias("_observed"))
df = fill_date_gaps(df, "permno", "time_avail_m", "1mo")
df = stata_multi_lag(df, "permno", "time_avail_m", ['sale'], [12], prefix="l", fill_gaps=False)
df = stata_multi_lag(df, "permno", "time_avail_m", ['at'], [24], prefix="l", fill_gaps=False)
df = df.filter(pl.col("_observed").eq(True)).drop("_observed")
# Match the former Pandas-to-Polars conversion of computed NaN values.
df = df.fill_nan(None)

df = df.with_columns(
    (pl.col('l12_sale') / pl.col('l24_at')).alias('CapTurnover')
)

print(f"Generated CapTurnover for {len(df)} observations")

# Keep only required columns for output
df_final = df.select(['permno', 'time_avail_m', 'CapTurnover'])

# SAVE
# do "$pathCode/saveplacebo" CapTurnover
save_placebo(df_final, 'CapTurnover')

print("CapTurnover.py completed")
