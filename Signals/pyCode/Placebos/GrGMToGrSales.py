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

# Create lags for complex calculation
print("Computing lags...")
df = df.with_columns([
    pl.col('tempGM').shift(12).over('permno').alias('l12_tempGM'),
    pl.col('tempGM').shift(24).over('permno').alias('l24_tempGM'),
    pl.col('sale').shift(12).over('permno').alias('l12_sale'),
    pl.col('sale').shift(24).over('permno').alias('l24_sale')
])

# gen GrGMToGrSales = ((tempGM- (.5*(l12.tempGM + l24.tempGM)))/(.5*(l12.tempGM + l24.tempGM))) - ((sale- (.5*(l12.sale + l24.sale)))/(.5*(l12.sale + l24.sale)))
print("Computing GrGMToGrSales...")
df = df.with_columns([
    # Average of l12 and l24 gross margins
    ((pl.col('l12_tempGM') + pl.col('l24_tempGM')) * 0.5).alias('avg_gm_lag'),
    # Average of l12 and l24 sales
    ((pl.col('l12_sale') + pl.col('l24_sale')) * 0.5).alias('avg_sale_lag')
])

df = df.with_columns(
    (((pl.col('tempGM') - pl.col('avg_gm_lag')) / pl.col('avg_gm_lag')) -
     ((pl.col('sale') - pl.col('avg_sale_lag')) / pl.col('avg_sale_lag'))).alias('GrGMToGrSales')
)

# replace GrGMToGrSales = ((tempGM-l12.tempGM)/l12.tempGM)- ((sale-l12.sale)/l12.sale) if mi(GrGMToGrSales)
print("Applying fallback calculation for missing values...")
df = df.with_columns(
    pl.when(pl.col('GrGMToGrSales').is_null())
    .then(((pl.col('tempGM') - pl.col('l12_tempGM')) / pl.col('l12_tempGM')) -
          ((pl.col('sale') - pl.col('l12_sale')) / pl.col('l12_sale')))
    .otherwise(pl.col('GrGMToGrSales'))
    .alias('GrGMToGrSales')
)

print(f"Generated GrGMToGrSales for {len(df)} observations")

# Keep only required columns for output
df_final = df.select(['permno', 'time_avail_m', 'GrGMToGrSales'])

# SAVE
# do "$pathCode/saveplacebo" GrGMToGrSales
save_placebo(df_final, 'GrGMToGrSales')

print("GrGMToGrSales.py completed")