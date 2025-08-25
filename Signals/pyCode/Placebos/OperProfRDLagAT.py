# ABOUTME: OperProfRDLagAT.py - calculates operating profits to lagged assets placebo
# ABOUTME: Python equivalent of OperProfRDLagAT.do, translates line-by-line from Stata code

"""
OperProfRDLagAT.py

Inputs:
    - m_aCompustat.parquet: gvkey, permno, time_avail_m, xrd, revt, cogs, xsga, at columns

Outputs:
    - OperProfRDLagAT.csv: permno, yyyymm, OperProfRDLagAT columns

Usage:
    cd pyCode
    source .venv/bin/activate  
    python3 Placebos/OperProfRDLagAT.py
"""

import pandas as pd
import polars as pl
import sys
import os

# Add parent directory to path to import utils
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from utils.saveplacebo import save_placebo

print("Starting OperProfRDLagAT.py")

# DATA LOAD
# use gvkey permno time_avail_m xrd revt cogs xsga at using "$pathDataIntermediate/m_aCompustat", clear
print("Loading m_aCompustat...")
df = pl.read_parquet("../pyData/Intermediate/m_aCompustat.parquet")
df = df.select(['gvkey', 'permno', 'time_avail_m', 'xrd', 'revt', 'cogs', 'xsga', 'at'])

print(f"Loaded data: {len(df)} rows")

# SIGNAL CONSTRUCTION
# bysort permno time_avail_m: keep if _n == 1  // deletes a few observations
print("Removing duplicates...")
df = df.unique(subset=['permno', 'time_avail_m'], maintain_order=True)

print(f"After removing duplicates: {len(df)} rows")

# Sort for lag operations
print("Sorting by permno and time...")
df = df.sort(['permno', 'time_avail_m'])

# gen tempXRD = xrd
# replace tempXRD = 0 if mi(tempXRD)
print("Creating tempXRD with zero replacement for missing...")
df = df.with_columns([
    pl.col('xrd').fill_null(0).alias('tempXRD')
])

# Create 12-month lag of at
print("Computing 12-month lag of assets...")
df = df.with_columns([
    pl.col('at').shift(12).over('permno').alias('l12_at')
])

# gen OperProfRDLagAT = (revt - cogs - xsga + tempXRD)/l12.at
print("Computing OperProfRDLagAT...")
df = df.with_columns([
    ((pl.col('revt') - pl.col('cogs') - pl.col('xsga') + pl.col('tempXRD')) / pl.col('l12_at')).alias('OperProfRDLagAT')
])

print(f"Generated OperProfRDLagAT for {len(df)} observations")

# Keep only required columns
df_final = df.select(['permno', 'time_avail_m', 'OperProfRDLagAT'])

# SAVE
# do "$pathCode/saveplacebo" OperProfRDLagAT
save_placebo(df_final, 'OperProfRDLagAT')

print("OperProfRDLagAT.py completed")