# ABOUTME: GrGMToGrSales.py - calculates gross margin growth over sales growth placebo
# ABOUTME: Python equivalent of GrGMToGrSales.do, translates line-by-line from Stata code

"""
GrGMToGrSales.py

Inputs:
    - m_aCompustat.parquet: gvkey, permno, time_avail_m, sale, cogs columns

Outputs:
    - GrGMToGrSales.csv: permno, yyyymm, GrGMToGrSales columns

Usage:
    cd pyCode
    source .venv/bin/activate  
    python3 Placebos/GrGMToGrSales.py
"""

import pandas as pd
import polars as pl
import sys
import os

EPSILON = 1e-12

# Add parent directory to path to import utils
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from utils.saveplacebo import save_placebo

print("Starting GrGMToGrSales.py")

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

# gen tempGM = sale-cogs
df = df.with_columns(
    (pl.col('sale') - pl.col('cogs')).alias('tempGM')
)

# Convert to pandas for calendar-based lag operations
print("Computing calendar-based 12-month and 24-month lags...")
df_pd = df.to_pandas()

# Create 12-month and 24-month lag dates
df_pd['time_lag12'] = df_pd['time_avail_m'] - pd.DateOffset(months=12)
df_pd['time_lag24'] = df_pd['time_avail_m'] - pd.DateOffset(months=24)

# Create lag data for merging (12-month lags)
lag12_data = df_pd[['permno', 'time_avail_m', 'tempGM', 'sale']].copy()
lag12_data.columns = ['permno', 'time_lag12', 'l12_tempGM', 'l12_sale']

# Create lag data for merging (24-month lags)  
lag24_data = df_pd[['permno', 'time_avail_m', 'tempGM', 'sale']].copy()
lag24_data.columns = ['permno', 'time_lag24', 'l24_tempGM', 'l24_sale']

# Merge to get lagged values (calendar-based, not position-based)
df_pd = df_pd.merge(lag12_data, on=['permno', 'time_lag12'], how='left')
df_pd = df_pd.merge(lag24_data, on=['permno', 'time_lag24'], how='left')

# Convert back to polars
df = pl.from_pandas(df_pd)

# gen GrGMToGrSales = ((tempGM- (.5*(l12.tempGM + l24.tempGM)))/(.5*(l12.tempGM + l24.tempGM))) - ((sale- (.5*(l12.sale + l24.sale)))/(.5*(l12.sale + l24.sale)))
print("Computing GrGMToGrSales...")
df = df.with_columns([
    # Average of l12 and l24 gross margins
    ((pl.col('l12_tempGM') + pl.col('l24_tempGM')) * 0.5).alias('avg_gm_lag'),
    # Average of l12 and l24 sales
    ((pl.col('l12_sale') + pl.col('l24_sale')) * 0.5).alias('avg_sale_lag')
])

valid_avg = (
    pl.col('avg_gm_lag').is_not_null() &
    pl.col('avg_sale_lag').is_not_null() &
    (pl.col('avg_gm_lag').abs() > EPSILON) &
    (pl.col('avg_sale_lag').abs() > EPSILON)
)

df = df.with_columns(
    pl.when(valid_avg)
    .then(
        ((pl.col('tempGM') - pl.col('avg_gm_lag')) / pl.col('avg_gm_lag')) -
        ((pl.col('sale') - pl.col('avg_sale_lag')) / pl.col('avg_sale_lag'))
    )
    .otherwise(None)
    .alias('GrGMToGrSales')
)

# replace GrGMToGrSales = ((tempGM-l12.tempGM)/l12.tempGM)- ((sale-l12.sale)/l12.sale) if mi(GrGMToGrSales)
print("Applying fallback calculation for missing values...")
valid_fallback = (
    pl.col('l12_tempGM').is_not_null() &
    pl.col('l12_sale').is_not_null() &
    (pl.col('l12_tempGM').abs() > EPSILON) &
    (pl.col('l12_sale').abs() > EPSILON)
)

df = df.with_columns(
    pl.when(pl.col('GrGMToGrSales').is_null() & valid_fallback)
    .then(
        ((pl.col('tempGM') - pl.col('l12_tempGM')) / pl.col('l12_tempGM')) -
        ((pl.col('sale') - pl.col('l12_sale')) / pl.col('l12_sale'))
    )
    .otherwise(pl.col('GrGMToGrSales'))
    .alias('GrGMToGrSales')
)

# Ensure non-finite values are treated as missing to mirror Stata behavior
df = df.with_columns(
    pl.when(pl.col('GrGMToGrSales').is_finite())
    .then(pl.col('GrGMToGrSales'))
    .otherwise(None)
    .alias('GrGMToGrSales')
)

print(f"Generated GrGMToGrSales for {len(df)} observations")

# Keep only required columns for output
df_final = df.select(['permno', 'time_avail_m', 'GrGMToGrSales'])

# SAVE
# do "$pathCode/saveplacebo" GrGMToGrSales
save_placebo(df_final, 'GrGMToGrSales')

print("GrGMToGrSales.py completed")
