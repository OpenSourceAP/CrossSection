# ABOUTME: ChNCOL.py - calculates change in non-current operating liabilities placebo
# ABOUTME: Python equivalent of ChNCOL.do, translates line-by-line from Stata code

"""
ChNCOL.py

Inputs:
    - m_aCompustat.parquet: gvkey, permno, time_avail_m, lt, dlc, dltt, at columns

Outputs:
    - ChNCOL.csv: permno, yyyymm, ChNCOL columns

Usage:
    cd pyCode
    source .venv/bin/activate  
    python3 Placebos/ChNCOL.py
"""

import pandas as pd
import polars as pl
import sys
import os

# Add parent directory to path to import utils
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from utils.save_standardized import save_placebo
from utils.stata_replication import stata_multi_lag

print("Starting ChNCOL.py")

# DATA LOAD
# use gvkey permno time_avail_m lt dlc dltt at using "$pathDataIntermediate/m_aCompustat", clear
print("Loading m_aCompustat...")
df = pl.read_parquet("../pyData/Intermediate/m_aCompustat.parquet")
df = df.select(['gvkey', 'permno', 'time_avail_m', 'lt', 'dlc', 'dltt', 'at'])

print(f"After loading: {len(df)} rows")

# bysort permno time_avail_m: keep if _n == 1  // deletes a few observations
print("Dropping duplicates...")
df = df.unique(subset=['permno', 'time_avail_m'])

print(f"After dropping duplicates: {len(df)} rows")

# SIGNAL CONSTRUCTION
# xtset permno time_avail_m
print("Sorting for lag operations...")
df = df.sort(['permno', 'time_avail_m'])

# gen temp = lt - dlc - dltt
# replace temp = lt - dlc if mi(dltt)
print("Computing temp...")
df = df.with_columns(
    pl.when(pl.col('dltt').is_not_null())
    .then(pl.col('lt') - pl.col('dlc') - pl.col('dltt'))
    .otherwise(pl.col('lt') - pl.col('dlc'))
    .alias('temp')
)

# Convert to pandas for stata_multi_lag
df_pd = df.to_pandas()

# Create 12-month lags using stata_multi_lag
print("Computing 12-month lags using stata_multi_lag...")
lag_vars = ['temp', 'at']
for var in lag_vars:
    df_pd = stata_multi_lag(df_pd, 'permno', 'time_avail_m', var, [12], freq='M', prefix='l')

# Convert back to polars
df = pl.from_pandas(df_pd)

# gen ChNCOL = (temp - l12.temp)/l12.at
print("Computing ChNCOL...")
df = df.with_columns(
    ((pl.col('temp') - pl.col('l12_temp')) / pl.col('l12_at')).alias('ChNCOL')
)

print(f"Generated ChNCOL for {len(df)} observations")

# Keep only required columns for output
df_final = df.select(['permno', 'time_avail_m', 'ChNCOL'])

# SAVE
# do "$pathCode/saveplacebo" ChNCOL
save_placebo(df_final, 'ChNCOL')

print("ChNCOL.py completed")