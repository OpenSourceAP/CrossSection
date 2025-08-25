# ABOUTME: pchsaleinv.py - calculates change in sales to inventory placebo
# ABOUTME: Python equivalent of pchsaleinv.do, translates line-by-line from Stata code

"""
pchsaleinv.py

Inputs:
    - m_aCompustat.parquet: gvkey, permno, time_avail_m, sale, invt columns

Outputs:
    - pchsaleinv.csv: permno, yyyymm, pchsaleinv columns

Usage:
    cd pyCode
    source .venv/bin/activate  
    python3 Placebos/pchsaleinv.py
"""

import pandas as pd
import polars as pl
import sys
import os

# Add parent directory to path to import utils
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from utils.saveplacebo import save_placebo

print("Starting pchsaleinv.py")

# DATA LOAD
# use gvkey permno time_avail_m sale invt using "$pathDataIntermediate/m_aCompustat", clear
print("Loading m_aCompustat...")
df = pl.read_parquet("../pyData/Intermediate/m_aCompustat.parquet")
df = df.select(['gvkey', 'permno', 'time_avail_m', 'sale', 'invt'])

print(f"After loading m_aCompustat: {len(df)} rows")

# SIGNAL CONSTRUCTION
# bysort permno time_avail_m: keep if _n == 1  // deletes a few observations
print("Removing duplicates...")
df = df.unique(subset=['permno', 'time_avail_m'], maintain_order=True)

print(f"After removing duplicates: {len(df)} rows")

# xtset permno time_avail_m
print("Sorting by permno and time...")
df = df.sort(['permno', 'time_avail_m'])

# gen pchsaleinv = ( (sale/invt)-(l12.sale/l12.invt) ) / (l12.sale/l12.invt)
print("Computing lags and pchsaleinv...")

# Create 12-month lags
df = df.with_columns([
    pl.col('sale').shift(12).over('permno').alias('l12_sale'),
    pl.col('invt').shift(12).over('permno').alias('l12_invt')
])

# Calculate the components
df = df.with_columns([
    # Current sale-to-inventory ratio
    (pl.col('sale') / pl.col('invt')).alias('saleinv_current'),
    # Lagged sale-to-inventory ratio
    (pl.col('l12_sale') / pl.col('l12_invt')).alias('saleinv_lagged')
])

# Calculate pchsaleinv = (saleinv_current - saleinv_lagged) / saleinv_lagged
df = df.with_columns(
    ((pl.col('saleinv_current') - pl.col('saleinv_lagged')) / 
     pl.col('saleinv_lagged')).alias('pchsaleinv')
)

print(f"Generated pchsaleinv for {len(df)} observations")

# Keep only required columns for output
df_final = df.select(['permno', 'time_avail_m', 'pchsaleinv'])

# SAVE
# do "$pathCode/saveplacebo" pchsaleinv
save_placebo(df_final, 'pchsaleinv')

print("pchsaleinv.py completed")