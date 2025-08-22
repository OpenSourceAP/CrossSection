# ABOUTME: cfpq.py - calculates cfpq placebo (Cash flow to price, quarterly)
# ABOUTME: Python equivalent of cfpq.do, translates line-by-line from Stata code

"""
cfpq.py

Inputs:
    - SignalMasterTable.parquet: gvkey, permno, time_avail_m, mve_c columns
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
# use gvkey permno time_avail_m mve_c using "$pathDataIntermediate/SignalMasterTable", clear
print("Loading SignalMasterTable...")
df = pl.read_parquet("../pyData/Intermediate/SignalMasterTable.parquet")
df = df.select(['gvkey', 'permno', 'time_avail_m', 'mve_c'])

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

print("Merging with m_QCompustat...")
df = df.join(qcomp, on=['gvkey', 'time_avail_m'], how='inner')

print(f"After merge: {len(df)} rows")

# SIGNAL CONSTRUCTION
# xtset permno time_avail_m
print("Sorting for lag operations...")
df = df.sort(['permno', 'time_avail_m'])

# gen tempaccrual_level = (actq-l12.actq - (cheq-l12.cheq)) - ( (lctq-l12.lctq)- (dlcq-l12.dlcq)-(txpq-l12.txpq)-dpq )
print("Computing 12-month lags...")
df = df.with_columns([
    pl.col('actq').shift(12).over('permno').alias('l12_actq'),
    pl.col('cheq').shift(12).over('permno').alias('l12_cheq'),
    pl.col('lctq').shift(12).over('permno').alias('l12_lctq'),
    pl.col('dlcq').shift(12).over('permno').alias('l12_dlcq'),
    pl.col('txpq').shift(12).over('permno').alias('l12_txpq')
])

print("Computing tempaccrual_level...")
df = df.with_columns(
    ((pl.col('actq') - pl.col('l12_actq') - (pl.col('cheq') - pl.col('l12_cheq'))) - 
     ((pl.col('lctq') - pl.col('l12_lctq')) - (pl.col('dlcq') - pl.col('l12_dlcq')) - 
      (pl.col('txpq') - pl.col('l12_txpq')) - pl.col('dpq'))).alias('tempaccrual_level')
)

# gen cfpq =(ibq - tempaccrual_level )/ mve_c
print("Computing cfpq...")
df = df.with_columns(
    ((pl.col('ibq') - pl.col('tempaccrual_level')) / pl.col('mve_c')).alias('cfpq')
)

# replace cfpq = oancfyq/mve_c if oancfyq !=.
print("Replacing cfpq with oancfyq when available...")
df = df.with_columns(
    pl.when(pl.col('oancfyq').is_not_null())
    .then(pl.col('oancfyq') / pl.col('mve_c'))
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