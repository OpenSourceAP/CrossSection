# ABOUTME: ETR.py - calculates effective tax rate placebo
# ABOUTME: Python equivalent of ETR.do, translates line-by-line from Stata code

"""
ETR.py

Inputs:
    - m_aCompustat.parquet: gvkey, permno, time_avail_m, am, txt, pi, epspx, ajex, prcc_f columns

Outputs:
    - ETR.csv: permno, yyyymm, ETR columns

Usage:
    cd pyCode
    source .venv/bin/activate  
    python3 Placebos/ETR.py
"""

import pandas as pd
import polars as pl
import sys
import os

# Add parent directory to path to import utils
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from utils.saveplacebo import save_placebo

print("Starting ETR.py")

# DATA LOAD
# use gvkey permno time_avail_m am txt pi am epspx ajex prcc_f using "$pathDataIntermediate/m_aCompustat", clear
print("Loading m_aCompustat...")
df = pl.read_parquet("../pyData/Intermediate/m_aCompustat.parquet")
df = df.select(['gvkey', 'permno', 'time_avail_m', 'am', 'txt', 'pi', 'epspx', 'ajex', 'prcc_f'])

print(f"After loading: {len(df)} rows")

# bysort permno time_avail_m: keep if _n == 1  // deletes a few observations
print("Dropping duplicates...")
df = df.unique(subset=['permno', 'time_avail_m'])

print(f"After dropping duplicates: {len(df)} rows")

# SIGNAL CONSTRUCTION
# xtset permno time_avail_m
print("Sorting for lag operations...")
df = df.sort(['permno', 'time_avail_m'])

# replace am = 0 if mi(am)
print("Replacing missing am with 0...")
df = df.with_columns(pl.col('am').fill_null(0))

# gen tempTaxOverEBT = txt/(pi + am)
print("Computing tempTaxOverEBT...")
df = df.with_columns(
    (pl.col('txt') / (pl.col('pi') + pl.col('am'))).alias('tempTaxOverEBT')
)

# gen tempEarn = epspx/ajex
print("Computing tempEarn...")
df = df.with_columns(
    (pl.col('epspx') / pl.col('ajex')).alias('tempEarn')
)

# Convert to pandas for lag operations (need l12, l24, l36, and l.prcc_f)
df_pd = df.to_pandas()

# Create multiple lags
lag_periods = [1, 12, 24, 36]
for lag_months in lag_periods:
    df_pd[f'time_lag{lag_months}'] = df_pd['time_avail_m'] - pd.DateOffset(months=lag_months)
    
    if lag_months == 1:
        # For l.prcc_f
        lag_vars = ['prcc_f']
        col_prefix = 'l'
    else:
        # For l12, l24, l36 of tempTaxOverEBT and tempEarn
        lag_vars = ['tempTaxOverEBT', 'tempEarn']
        col_prefix = f'l{lag_months}'
    
    # Create lag data
    lag_data = df_pd[['permno', 'time_avail_m'] + lag_vars].copy()
    lag_data.columns = ['permno', f'time_lag{lag_months}'] + [f'{col_prefix}_{var}' for var in lag_vars]
    
    # Merge lag data
    df_pd = df_pd.merge(lag_data, on=['permno', f'time_lag{lag_months}'], how='left')

# Drop lag date columns
lag_columns = [f'time_lag{i}' for i in lag_periods]
df_pd = df_pd.drop(columns=lag_columns)

# Convert back to polars
df = pl.from_pandas(df_pd)

# gen ETR = ( tempTaxOverEBT - 1/3*(l12.tempTaxOverEBT + l24.tempTaxOverEBT + l36.tempTaxOverEBT))*((tempEarn - l12.tempEarn)/l.prcc_f)
print("Computing ETR...")
df = df.with_columns(
    ((pl.col('tempTaxOverEBT') - (1.0/3.0) * (pl.col('l12_tempTaxOverEBT') + pl.col('l24_tempTaxOverEBT') + pl.col('l36_tempTaxOverEBT'))) *
     ((pl.col('tempEarn') - pl.col('l12_tempEarn')) / pl.col('l_prcc_f'))).alias('ETR')
)

print(f"Generated ETR for {len(df)} observations")

# Keep only required columns for output
df_final = df.select(['permno', 'time_avail_m', 'ETR'])

# SAVE
# do "$pathCode/saveplacebo" ETR
save_placebo(df_final, 'ETR')

print("ETR.py completed")