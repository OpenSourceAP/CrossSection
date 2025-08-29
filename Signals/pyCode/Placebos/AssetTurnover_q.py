# ABOUTME: AssetTurnover_q.py - calculates AssetTurnover_q placebo (Asset Turnover, quarterly)
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

# Convert gvkey to same type for join
df = df.with_columns(pl.col('gvkey').cast(pl.Int32))
qcomp = qcomp.with_columns(pl.col('gvkey').cast(pl.Int32))

print("Merging with m_QCompustat...")
# keep(match) means inner join
df = df.join(qcomp, on=['gvkey', 'time_avail_m'], how='inner')

print(f"After merge: {len(df)} rows")

# SIGNAL CONSTRUCTION
# xtset permno time_avail_m
# gen temp = (rectq + invtq + acoq + ppentq + intanq - apq - lcoq - loq)
print("Computing temp variable...")
df = df.with_columns(
    (pl.col('rectq') + pl.col('invtq') + pl.col('acoq') + pl.col('ppentq') + pl.col('intanq') - 
     pl.col('apq') - pl.col('lcoq') - pl.col('loq')).alias('temp')
)

# Sort for lag operations
print("Sorting for lag operations...")
df = df.sort(['permno', 'time_avail_m'])

print("Computing 12-period calendar-based lag...")

# Convert to pandas for easier date manipulation
df_pd = df.to_pandas()

# Create 12-month lag date (exactly 1 year earlier)
df_pd['target_lag_date'] = df_pd['time_avail_m'] - pd.DateOffset(months=12)

# Create a lookup dataframe for lagged values
lag_df = df_pd[['permno', 'time_avail_m', 'temp']].copy()
lag_df = lag_df.rename(columns={'temp': 'l12_temp', 'time_avail_m': 'target_lag_date'})

# Merge to get lagged values
df_pd = df_pd.merge(lag_df, on=['permno', 'target_lag_date'], how='left')

# Convert back to polars
df = pl.from_pandas(df_pd.drop(columns=['target_lag_date']))

# gen AssetTurnover_q = saleq/((temp + l12.temp)/2)
print("Computing AssetTurnover_q...")
df = df.with_columns(
    (pl.col('saleq') / ((pl.col('temp') + pl.col('l12_temp')) / 2)).alias('AssetTurnover_q')
)

# replace AssetTurnover_q = . if AssetTurnover_q < 0
print("Applying negative filter...")
df = df.with_columns(
    pl.when(pl.col('AssetTurnover_q') < 0)
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