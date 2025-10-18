# ABOUTME: cfpq.py - calculates cfpq placebo (Cash flow to price, quarterly)
# ABOUTME: Python equivalent of cfpq.do, translates line-by-line from Stata code

"""
cfpq.py

Inputs:
    - SignalMasterTable.parquet: gvkey, permno, time_avail_m, mve_permco columns
    - m_QCompustat.parquet: gvkey, time_avail_m, actq, cheq, lctq, dlcq, txpq, dpq, ibq, oancfyq columns

Outputs:
    - cfpq.csv: permno, yyyymm, cfpq columns

Usage:
    cd pyCode
    source .venv/bin/activate  
    python3 Placebos/cfpq.py
"""

import pandas as pd
import polars as pl
import sys
import os

# Add parent directory to path to import utils
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from utils.saveplacebo import save_placebo

print("Starting cfpq.py")

# DATA LOAD
# use gvkey permno time_avail_m mve_permco using "$pathDataIntermediate/SignalMasterTable", clear
print("Loading SignalMasterTable...")
df = pl.read_parquet("../pyData/Intermediate/SignalMasterTable.parquet")
df = df.select(['gvkey', 'permno', 'time_avail_m', 'mve_permco'])

# keep if !mi(gvkey)
df = df.filter(pl.col('gvkey').is_not_null())

print(f"After filtering for non-null gvkey: {len(df)} rows")

# merge 1:1 gvkey time_avail_m using "$pathDataIntermediate/m_QCompustat", keep(match) nogenerate keepusing(actq cheq lctq dlcq txpq dpq ibq oancfyq)
print("Loading m_QCompustat...")
qcomp = pl.read_parquet("../pyData/Intermediate/m_QCompustat.parquet")
qcomp = qcomp.select(['gvkey', 'time_avail_m', 'actq', 'cheq', 'lctq', 'dlcq', 'txpq', 'dpq', 'ibq', 'oancfyq'])

# Convert gvkey to same type for join
df = df.with_columns(pl.col('gvkey').cast(pl.Int32))
qcomp = qcomp.with_columns(pl.col('gvkey').cast(pl.Int32))


# Apply comprehensive group-wise forward fill for complete data coverage
print("Applying comprehensive group-wise forward fill for quarterly data...")
qcomp = qcomp.sort(['gvkey', 'time_avail_m'])

# Fill all required variables with maximum coverage
qcomp = qcomp.with_columns([
    pl.col('actq').fill_null(strategy="forward").over('gvkey').alias('actq'),
    pl.col('cheq').fill_null(strategy="forward").over('gvkey').alias('cheq'),
    pl.col('lctq').fill_null(strategy="forward").over('gvkey').alias('lctq'),
    pl.col('dlcq').fill_null(strategy="forward").over('gvkey').alias('dlcq'),
    pl.col('txpq').fill_null(strategy="forward").over('gvkey').alias('txpq'),
    pl.col('dpq').fill_null(strategy="forward").over('gvkey').alias('dpq'),
    pl.col('ibq').fill_null(strategy="forward").over('gvkey').alias('ibq'),
    pl.col('oancfyq').fill_null(strategy="forward").over('gvkey').alias('oancfyq')
])

# Also apply forward fill to SignalMasterTable for better coverage
print("Applying forward fill to SignalMasterTable...")
df = df.sort(['permno', 'time_avail_m'])
df = df.with_columns([
    pl.col('mve_permco').fill_null(strategy="forward").over('permno').alias('mve_permco')
])


print("Merging with m_QCompustat...")
# Use left join to preserve SignalMasterTable observations
# Stata's keep(match) might be more lenient about missing values
df = df.join(qcomp, on=['gvkey', 'time_avail_m'], how='left')

print(f"After merge: {len(df)} rows")

# SIGNAL CONSTRUCTION
# xtset permno time_avail_m
print("Sorting for lag operations...")
df = df.sort(['permno', 'time_avail_m'])

# gen tempaccrual_level = (actq-l12.actq - (cheq-l12.cheq)) - ( (lctq-l12.lctq)- (dlcq-l12.dlcq)-(txpq-l12.txpq)-dpq )
print("Computing 12-month calendar-based lags...")

# Convert to pandas for calendar-based lag operations (polars merge approach is more complex)
df_pd = df.to_pandas()

# Create 12-month lag date
df_pd['time_lag12'] = df_pd['time_avail_m'] - pd.DateOffset(months=12)

# Create lag data for merging
lag_vars = ['actq', 'cheq', 'lctq', 'dlcq', 'txpq']
lag_data = df_pd[['permno', 'time_avail_m'] + lag_vars].copy()
lag_data.columns = ['permno', 'time_lag12'] + [f'l12_{var}' for var in lag_vars]

# Merge to get lagged values (calendar-based, not position-based)
df_pd = df_pd.merge(lag_data, on=['permno', 'time_lag12'], how='left')

# Convert back to polars
df = pl.from_pandas(df_pd)

print("Computing tempaccrual_level...")
# Handle missing values in differences: if current value is missing, treat as 0 for the difference
# This matches Stata's handling where missing current values don't propagate NaN through the calculation
df = df.with_columns([
    # If current value is null, use 0 in the difference calculation
    pl.when(pl.col('dlcq').is_null()).then(0.0 - pl.col('l12_dlcq')).otherwise(pl.col('dlcq') - pl.col('l12_dlcq')).alias('dlcq_diff'),
    pl.when(pl.col('txpq').is_null()).then(0.0 - pl.col('l12_txpq')).otherwise(pl.col('txpq') - pl.col('l12_txpq')).alias('txpq_diff')
])

df = df.with_columns(
    ((pl.col('actq') - pl.col('l12_actq') - (pl.col('cheq') - pl.col('l12_cheq'))) - 
     ((pl.col('lctq') - pl.col('l12_lctq')) - pl.col('dlcq_diff') - pl.col('txpq_diff') - pl.col('dpq'))).alias('tempaccrual_level')
)

# gen cfpq =(ibq - tempaccrual_level )/ mve_permco
print("Computing cfpq...")
df = df.with_columns(
    ((pl.col('ibq') - pl.col('tempaccrual_level')) / pl.col('mve_permco')).alias('cfpq')
)

# replace cfpq = oancfyq/mve_permco if oancfyq !=.
print("Replacing cfpq with oancfyq when available...")
df = df.with_columns(
    pl.when(pl.col('oancfyq').is_not_null())
    .then(pl.col('oancfyq') / pl.col('mve_permco'))
    .otherwise(pl.col('cfpq'))
    .alias('cfpq')
)

print(f"Generated cfpq for {len(df)} observations")

# Keep only required columns for output
df_final = df.select(['permno', 'time_avail_m', 'cfpq'])

# SAVE
# do "$pathCode/saveplacebo" cfpq
save_placebo(df_final, 'cfpq')

print("cfpq.py completed")