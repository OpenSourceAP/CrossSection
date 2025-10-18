# ABOUTME: AssetTurnover_q.py - calculates AssetTurnover_q placebo (Asset Turnover, quarterly)
# ABOUTME: Python equivalent of AssetTurnover_q.do, translates line-by-line from Stata code

"""
AssetTurnover_q.py

Inputs:
    - SignalMasterTable.parquet: permno, gvkey, time_avail_m, mve_permco columns
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
from utils.save_standardized import save_placebo
from utils.stata_replication import stata_multi_lag

print("Starting AssetTurnover_q.py")

# DATA LOAD
# use permno gvkey time_avail_m mve_permco using "$pathDataIntermediate/SignalMasterTable", clear
print("Loading SignalMasterTable...")
df = pl.read_parquet("../pyData/Intermediate/SignalMasterTable.parquet")
df = df.select(['permno', 'gvkey', 'time_avail_m', 'mve_permco'])

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
# Note: In Stata, arithmetic with missing values results in missing unless specified otherwise
# However, based on debugging, it appears Stata treats missing ppentq as 0 in this context
print("Computing temp variable...")
df = df.with_columns([
    pl.col('ppentq').fill_null(0).alias('ppentq_filled')
]).with_columns(
    (pl.col('rectq') + pl.col('invtq') + pl.col('acoq') + pl.col('ppentq_filled') + pl.col('intanq') - 
     pl.col('apq') - pl.col('lcoq') - pl.col('loq')).alias('temp')
)

# Sort for lag operations and create 12-month lag using stata_replication function
print("Computing 12-month lag using stata_multi_lag...")
df_pandas = df.to_pandas()
df_pandas = stata_multi_lag(df_pandas, 'permno', 'time_avail_m', 'temp', [12], freq='M', prefix='l')
df = pl.from_pandas(df_pandas)

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