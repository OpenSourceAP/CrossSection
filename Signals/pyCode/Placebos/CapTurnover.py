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

# Convert to pandas for calendar-based lag operations
df_pd = df.to_pandas()

# Create 12-month and 24-month lag dates
df_pd['time_lag12'] = df_pd['time_avail_m'] - pd.DateOffset(months=12)
df_pd['time_lag24'] = df_pd['time_avail_m'] - pd.DateOffset(months=24)

# Create lag data for merging (12-month lag for sale)
lag12_data = df_pd[['permno', 'time_avail_m', 'sale']].copy()
lag12_data.columns = ['permno', 'time_lag12', 'l12_sale']

# Create lag data for merging (24-month lag for at)
lag24_data = df_pd[['permno', 'time_avail_m', 'at']].copy()
lag24_data.columns = ['permno', 'time_lag24', 'l24_at']

# Merge to get lagged values
df_pd = df_pd.merge(lag12_data, on=['permno', 'time_lag12'], how='left')
df_pd = df_pd.merge(lag24_data, on=['permno', 'time_lag24'], how='left')

# Convert back to polars
df = pl.from_pandas(df_pd)

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