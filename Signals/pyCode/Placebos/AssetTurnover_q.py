# ABOUTME: AssetTurnover_q.py - calculates quarterly asset turnover placebo
# ABOUTME: Python equivalent of AssetTurnover_q.do, translates line-by-line from Stata code

"""
AssetTurnover_q.py

Inputs:
    - SignalMasterTable.parquet: permno, gvkey, time_avail_m, mve_c columns
    - m_QCompustat.parquet: gvkey, time_avail_m, rectq, invtq, acoq, ppentq, intanq, apq, lcoq, loq, saleq columns

Outputs:
    - AssetTurnover_q.csv: permno, yyyymm, AssetTurnover_q columns

Usage:
    cd pyCode
    source .venv/bin/activate  
    python3 Placebos/AssetTurnover_q.py
"""

import pandas as pd
import polars as pl
import sys
import os

# Add parent directory to path to import utils
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from utils.saveplacebo import save_placebo
from utils.forward_fill import apply_quarterly_fill_to_compustat

print("Starting AssetTurnover_q.py")

# DATA LOAD
# use permno gvkey time_avail_m mve_c using "$pathDataIntermediate/SignalMasterTable", clear
print("Loading SignalMasterTable...")
df = pl.read_parquet("../pyData/Intermediate/SignalMasterTable.parquet")
df = df.select(['permno', 'gvkey', 'time_avail_m', 'mve_c'])

# keep if !mi(gvkey)
df = df.filter(pl.col('gvkey').is_not_null())

print(f"After filtering for non-null gvkey: {len(df)} rows")

# merge 1:1 gvkey time_avail_m using "$pathDataIntermediate/m_QCompustat", keepusing(rectq invtq acoq ppentq intanq apq lcoq loq saleq) nogenerate keep(match)
print("Loading m_QCompustat...")
qcomp = pl.read_parquet("../pyData/Intermediate/m_QCompustat.parquet")
qcomp = qcomp.select(['gvkey', 'time_avail_m', 'rectq', 'invtq', 'acoq', 'ppentq', 'intanq', 'apq', 'lcoq', 'loq', 'saleq'])

# Remove forward-fill to match Stata behavior exactly
# print("Applying forward-fill for missing quarterly values...")
# qcomp = apply_quarterly_fill_to_compustat(qcomp, quarterly_columns=['rectq', 'invtq', 'acoq', 'ppentq', 'intanq', 'apq', 'lcoq', 'loq', 'saleq'])

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

# gen temp = (rectq + invtq + acoq + ppentq + intanq - apq - lcoq - loq)
# Fill nulls with 0 to match Stata's implicit behavior in arithmetic operations
print("Computing temp variable...")
df = df.with_columns([
    pl.col('rectq').fill_null(0.0),
    pl.col('invtq').fill_null(0.0),
    pl.col('acoq').fill_null(0.0),
    pl.col('ppentq').fill_null(0.0),
    pl.col('intanq').fill_null(0.0),
    pl.col('apq').fill_null(0.0),
    pl.col('lcoq').fill_null(0.0),
    pl.col('loq').fill_null(0.0)
])

df = df.with_columns(
    (pl.col('rectq') + pl.col('invtq') + pl.col('acoq') + pl.col('ppentq') + 
     pl.col('intanq') - pl.col('apq') - pl.col('lcoq') - pl.col('loq')).alias('temp')
)

# gen AssetTurnover_q = saleq/((temp + l12.temp)/2)
# First filter out observations where saleq is null to match Stata's implicit behavior
print("Filtering for non-null saleq...")
df = df.filter(pl.col('saleq').is_not_null())

print("Computing 12-month calendar-based lag and AssetTurnover_q...")

# Convert to pandas for calendar-based lag operations (same approach as rd_sale_q.py)
df_pd = df.to_pandas()

# Create 12-month lag date
df_pd['time_lag12'] = df_pd['time_avail_m'] - pd.DateOffset(months=12)

# Create lag data for merging
lag_vars = ['temp']
lag_data = df_pd[['permno', 'time_avail_m'] + lag_vars].copy()
lag_data.columns = ['permno', 'time_lag12'] + [f'l12_{var}' for var in lag_vars]

# Merge to get lagged values (calendar-based, not position-based)
df_pd = df_pd.merge(lag_data, on=['permno', 'time_lag12'], how='left')

# Convert back to polars
df = pl.from_pandas(df_pd)

df = df.with_columns(
    (pl.col('saleq') / ((pl.col('temp') + pl.col('l12_temp')) / 2)).alias('AssetTurnover_q')
)

# replace AssetTurnover_q = . if AssetTurnover_q < 0
# Also filter out infinite and null values to match Stata's implicit behavior
print("Setting negative, infinite, and null AssetTurnover_q to null...")
df = df.with_columns(
    pl.when((pl.col('AssetTurnover_q') < 0) | 
            pl.col('AssetTurnover_q').is_infinite() |
            pl.col('AssetTurnover_q').is_null())
    .then(None)
    .otherwise(pl.col('AssetTurnover_q'))
    .alias('AssetTurnover_q')
)

print(f"Generated AssetTurnover_q for {len(df)} observations")

# Keep only required columns for output
df_final = df.select(['permno', 'time_avail_m', 'AssetTurnover_q'])

# SAVE
# do "$pathCode/saveplacebo" AssetTurnover_q
save_placebo(df_final, 'AssetTurnover_q')

print("AssetTurnover_q.py completed")