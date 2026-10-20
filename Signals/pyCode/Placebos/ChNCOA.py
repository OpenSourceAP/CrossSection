# ABOUTME: ChNCOA.py - calculates change in non-current operating assets placebo
# ABOUTME: Python equivalent of ChNCOA.do, translates line-by-line from Stata code

"""
ChNCOA.py

Inputs:
    - m_aCompustat.parquet: gvkey, permno, time_avail_m, at, act, ivao columns

Outputs:
    - ChNCOA.csv: permno, yyyymm, ChNCOA columns

Usage:
    cd pyCode
    source .venv/bin/activate  
    python3 Placebos/ChNCOA.py
"""

import pandas as pd
import polars as pl
import sys
import os

# Add parent directory to path to import utils
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from utils.stata_replication import fill_date_gaps, stata_multi_lag
from utils.saveplacebo import save_placebo

print("Starting ChNCOA.py")

# DATA LOAD
# use gvkey permno time_avail_m at act ivao using "$pathDataIntermediate/m_aCompustat", clear
print("Loading m_aCompustat...")
df = pl.read_parquet("../pyData/Intermediate/m_aCompustat.parquet")
df = df.select(['gvkey', 'permno', 'time_avail_m', 'at', 'act', 'ivao'])

print(f"After loading: {len(df)} rows")

# bysort permno time_avail_m: keep if _n == 1  // deletes a few observations
print("Dropping duplicates...")
df = df.unique(subset=['permno', 'time_avail_m'])

print(f"After dropping duplicates: {len(df)} rows")

# SIGNAL CONSTRUCTION
# xtset permno time_avail_m
print("Sorting for lag operations...")
df = df.sort(['permno', 'time_avail_m'])

# gen temp = at - act - ivao
# replace temp = at - act if mi(ivao)
print("Computing temp...")
df = df.with_columns(
    pl.when(pl.col('ivao').is_not_null())
    .then(pl.col('at') - pl.col('act') - pl.col('ivao'))
    .otherwise(pl.col('at') - pl.col('act'))
    .alias('temp')
)

# Convert to pandas for lag operations
# Calendar endpoints require the target month; retain only observed rows.
df = df.with_columns(pl.lit(True).alias("_observed"))
df = fill_date_gaps(df, "permno", "time_avail_m", "1mo")
df = stata_multi_lag(df, "permno", "time_avail_m", ['temp', 'at'], [12], prefix="l", fill_gaps=False)
df = df.filter(pl.col("_observed").eq(True)).drop("_observed")
# Match the former Pandas-to-Polars conversion of computed NaN values.
df = df.fill_nan(None)

# gen ChNCOA = (temp - l12.temp)/l12.at
print("Computing ChNCOA...")
df = df.with_columns(
    ((pl.col('temp') - pl.col('l12_temp')) / pl.col('l12_at')).alias('ChNCOA')
)

print(f"Generated ChNCOA for {len(df)} observations")

# Keep only required columns for output
df_final = df.select(['permno', 'time_avail_m', 'ChNCOA'])

# SAVE
# do "$pathCode/saveplacebo" ChNCOA
save_placebo(df_final, 'ChNCOA')

print("ChNCOA.py completed")
