# ABOUTME: CapTurnover_q.py - calculates quarterly capital turnover placebo
# ABOUTME: Python equivalent of CapTurnover_q.do, translates line-by-line from Stata code

"""
CapTurnover_q.py

Inputs:
    - SignalMasterTable.parquet: permno, gvkey, time_avail_m columns
    - m_QCompustat.parquet: gvkey, time_avail_m, atq, saleq columns

Outputs:
    - CapTurnover_q.csv: permno, yyyymm, CapTurnover_q columns

Usage:
    cd pyCode
    source .venv/bin/activate  
    python3 Placebos/CapTurnover_q.py
"""

import pandas as pd
import polars as pl
import sys
import os

# Add parent directory to path to import utils
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from utils.saveplacebo import save_placebo

print("Starting CapTurnover_q.py")

# DATA LOAD
# use permno gvkey time_avail_m using "$pathDataIntermediate/SignalMasterTable", clear
print("Loading SignalMasterTable...")
df = pl.read_parquet("../pyData/Intermediate/SignalMasterTable.parquet")
df = df.select(['permno', 'gvkey', 'time_avail_m'])

# keep if !mi(gvkey)
df = df.filter(pl.col('gvkey').is_not_null())

print(f"After filtering for non-null gvkey: {len(df)} rows")

# merge 1:1 gvkey time_avail_m using "$pathDataIntermediate/m_QCompustat", keepusing(atq saleq) nogenerate keep(match)
print("Loading m_QCompustat...")
qcomp = pl.read_parquet("../pyData/Intermediate/m_QCompustat.parquet")
qcomp = qcomp.select(['gvkey', 'time_avail_m', 'atq', 'saleq'])

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

# gen CapTurnover_q = saleq/l3.atq
print("Computing 3-month calendar-based lag and CapTurnover_q...")

# Convert to pandas for calendar-based lag operations
df_pd = df.to_pandas()

# Create 3-month lag date
df_pd['time_lag3'] = df_pd['time_avail_m'] - pd.DateOffset(months=3)

# Create lag data for merging
lag_vars = ['atq']
lag_data = df_pd[['permno', 'time_avail_m'] + lag_vars].copy()
lag_data.columns = ['permno', 'time_lag3'] + [f'l3_{var}' for var in lag_vars]

# Merge to get lagged values
df_pd = df_pd.merge(lag_data, on=['permno', 'time_lag3'], how='left')

# Convert back to polars
df = pl.from_pandas(df_pd)

df = df.with_columns(
    (pl.col('saleq') / pl.col('l3_atq')).alias('CapTurnover_q')
)

print(f"Generated CapTurnover_q for {len(df)} observations")

# Keep only required columns for output
df_final = df.select(['permno', 'time_avail_m', 'CapTurnover_q'])

# SAVE
# do "$pathCode/saveplacebo" CapTurnover_q
save_placebo(df_final, 'CapTurnover_q')

print("CapTurnover_q.py completed")