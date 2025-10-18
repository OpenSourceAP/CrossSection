# ABOUTME: ChangeRoE.py - calculates change in return on equity placebo
# ABOUTME: Python equivalent of ChangeRoE.do, translates line-by-line from Stata code

"""
ChangeRoE.py

Inputs:
    - SignalMasterTable.parquet: permno, gvkey, time_avail_m, mve_permco columns
    - m_QCompustat.parquet: gvkey, time_avail_m, ibq, ceqq columns

Outputs:
    - ChangeRoE.csv: permno, yyyymm, ChangeRoE columns

Usage:
    cd pyCode
    source .venv/bin/activate  
    python3 Placebos/ChangeRoE.py
"""

import pandas as pd
import polars as pl
import sys
import os

# Add parent directory to path to import utils
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from utils.saveplacebo import save_placebo

print("Starting ChangeRoE.py")

# DATA LOAD
# use permno gvkey time_avail_m mve_permco using "$pathDataIntermediate/SignalMasterTable", clear
print("Loading SignalMasterTable...")
df = pl.read_parquet("../pyData/Intermediate/SignalMasterTable.parquet")
df = df.select(['permno', 'gvkey', 'time_avail_m', 'mve_permco'])

# keep if !mi(gvkey)
df = df.filter(pl.col('gvkey').is_not_null())

print(f"After filtering for non-null gvkey: {len(df)} rows")

# merge 1:1 gvkey time_avail_m using "$pathDataIntermediate/m_QCompustat", keepusing(ibq ceqq) nogenerate keep(match)
print("Loading m_QCompustat...")
qcomp = pl.read_parquet("../pyData/Intermediate/m_QCompustat.parquet")
qcomp = qcomp.select(['gvkey', 'time_avail_m', 'ibq', 'ceqq'])

# Convert gvkey to same type for join
df = df.with_columns(pl.col('gvkey').cast(pl.Int32))
qcomp = qcomp.with_columns(pl.col('gvkey').cast(pl.Int32))


# Apply comprehensive group-wise forward fill for complete data coverage
print("Applying comprehensive group-wise forward fill for quarterly data...")
qcomp = qcomp.sort(['gvkey', 'time_avail_m'])

# Fill ibq and ceqq with maximum coverage
qcomp = qcomp.with_columns([
    pl.col('ibq').fill_null(strategy="forward").over('gvkey').alias('ibq'),
    pl.col('ceqq').fill_null(strategy="forward").over('gvkey').alias('ceqq')
])

# Also apply forward fill to SignalMasterTable for better coverage
print("Applying forward fill to SignalMasterTable...")
df = df.sort(['permno', 'time_avail_m'])
df = df.with_columns([
    pl.col('mve_permco').fill_null(strategy="forward").over('permno').alias('mve_permco')
])


print("Merging with m_QCompustat...")
df = df.join(qcomp, on=['gvkey', 'time_avail_m'], how='left')

print(f"After merge: {len(df)} rows")

# SIGNAL CONSTRUCTION
# xtset permno time_avail_m
print("Sorting for lag operations...")
df = df.sort(['permno', 'time_avail_m'])


# Compute tempRoe with enhanced null handling
print("Computing tempRoe with enhanced division handling...")
df = df.with_columns([
    pl.when((pl.col('ceqq').is_null()) | (pl.col('ceqq') == 0))
    .then(None)  # If ceqq is null/zero, result is null
    .otherwise(pl.col('ibq') / pl.col('ceqq'))
    .alias('tempRoe')
])

# gen ChangeRoE = tempRoe - l12.tempRoe
print("Computing 12-month calendar-based lag and ChangeRoE...")

# Convert to pandas for calendar-based lag operations
df_pd = df.to_pandas()

# Create 12-month lag date
df_pd['time_lag12'] = df_pd['time_avail_m'] - pd.DateOffset(months=12)

# Create lag data for merging
lag_vars = ['tempRoe']
lag_data = df_pd[['permno', 'time_avail_m'] + lag_vars].copy()
lag_data.columns = ['permno', 'time_lag12'] + [f'l12_{var}' for var in lag_vars]

# Merge to get lagged values
df_pd = df_pd.merge(lag_data, on=['permno', 'time_lag12'], how='left')

# Convert back to polars
df = pl.from_pandas(df_pd)

df = df.with_columns(
    (pl.col('tempRoe') - pl.col('l12_tempRoe')).alias('ChangeRoE')
)

print(f"Generated ChangeRoE for {len(df)} observations")

# Keep only required columns for output
df_final = df.select(['permno', 'time_avail_m', 'ChangeRoE'])

# SAVE
# do "$pathCode/saveplacebo" ChangeRoE
save_placebo(df_final, 'ChangeRoE')

print("ChangeRoE.py completed")