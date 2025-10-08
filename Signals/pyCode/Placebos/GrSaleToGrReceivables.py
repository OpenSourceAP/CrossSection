# ABOUTME: GrSaleToGrReceivables.py - calculates sales growth over receivables growth placebo
# ABOUTME: Python equivalent of GrSaleToGrReceivables.do, translates line-by-line from Stata code

"""
GrSaleToGrReceivables.py

Inputs:
    - m_aCompustat.parquet: gvkey, permno, time_avail_m, sale, rect columns

Outputs:
    - GrSaleToGrReceivables.csv: permno, yyyymm, GrSaleToGrReceivables columns

Usage:
    cd pyCode
    source .venv/bin/activate  
    python3 Placebos/GrSaleToGrReceivables.py
"""

import pandas as pd
import polars as pl
import sys
import os

# Add parent directory to path to import utils
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from utils.saveplacebo import save_placebo

print("Starting GrSaleToGrReceivables.py")

# DATA LOAD
# use gvkey permno time_avail_m sale rect using "$pathDataIntermediate/m_aCompustat", clear
print("Loading m_aCompustat...")
df = pl.read_parquet("../pyData/Intermediate/m_aCompustat.parquet")
df = df.select(['gvkey', 'permno', 'time_avail_m', 'sale', 'rect'])

print(f"After loading m_aCompustat: {len(df)} rows")

# SIGNAL CONSTRUCTION
# bysort permno time_avail_m: keep if _n == 1  // deletes a few observations
print("Removing duplicates...")
df = df.unique(subset=['permno', 'time_avail_m'], maintain_order=True)

print(f"After removing duplicates: {len(df)} rows")

# xtset permno time_avail_m
print("Sorting by permno and time...")
df = df.sort(['permno', 'time_avail_m'])

# Create lags for complex calculation
print("Computing lags...")
df = df.with_columns([
    pl.col('sale').shift(12).over('permno').alias('l12_sale'),
    pl.col('sale').shift(24).over('permno').alias('l24_sale'),
    pl.col('rect').shift(12).over('permno').alias('l12_rect'),
    pl.col('rect').shift(24).over('permno').alias('l24_rect')
])

# gen GrSaleToGrReceivables = ((sale- (.5*(l12.sale + l24.sale)))/(.5*(l12.sale + l24.sale))) - ((rect- (.5*(l12.rect + l24.rect)))/(.5*(l12.rect + l24.rect)))
print("Computing GrSaleToGrReceivables...")
df = df.with_columns([
    # Average of l12 and l24 sales
    ((pl.col('l12_sale') + pl.col('l24_sale')) * 0.5).alias('avg_sale_lag'),
    # Average of l12 and l24 receivables
    ((pl.col('l12_rect') + pl.col('l24_rect')) * 0.5).alias('avg_rect_lag')
])

df = df.with_columns(
    (((pl.col('sale') - pl.col('avg_sale_lag')) / pl.col('avg_sale_lag')) -
     ((pl.col('rect') - pl.col('avg_rect_lag')) / pl.col('avg_rect_lag'))).alias('GrSaleToGrReceivables')
)

# replace GrSaleToGrReceivables = ((sale-l12.sale)/l12.sale)-((rect-l12.rect)/l12.rect) if mi(GrSaleToGrReceivables)
print("Applying fallback calculation for missing values...")
df = df.with_columns(
    pl.when(pl.col('GrSaleToGrReceivables').is_null())
    .then(((pl.col('sale') - pl.col('l12_sale')) / pl.col('l12_sale')) -
          ((pl.col('rect') - pl.col('l12_rect')) / pl.col('l12_rect')))
    .otherwise(pl.col('GrSaleToGrReceivables'))
    .alias('GrSaleToGrReceivables')
)

print(f"Generated GrSaleToGrReceivables for {len(df)} observations")

# Keep only required columns for output
df_final = df.select(['permno', 'time_avail_m', 'GrSaleToGrReceivables'])

# SAVE
# do "$pathCode/saveplacebo" GrSaleToGrReceivables
save_placebo(df_final, 'GrSaleToGrReceivables')

print("GrSaleToGrReceivables.py completed")