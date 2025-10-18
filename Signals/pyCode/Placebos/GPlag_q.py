# ABOUTME: GPlag_q.py - calculates gross profitability quarterly placebo
# ABOUTME: Python equivalent of GPlag_q.do, translates line-by-line from Stata code

"""
GPlag_q.py

Inputs:
    - SignalMasterTable.parquet: permno, gvkey, time_avail_m, mve_permco columns
    - m_QCompustat.parquet: gvkey, time_avail_m, revtq, cogsq, atq columns

Outputs:
    - GPlag_q.csv: permno, yyyymm, GPlag_q columns

Usage:
    cd pyCode
    source .venv/bin/activate  
    python3 Placebos/GPlag_q.py
"""

import pandas as pd
import polars as pl
import sys
import os

# Add parent directory to path to import utils
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from utils.saveplacebo import save_placebo

print("Starting GPlag_q.py")

# DATA LOAD
# use permno gvkey time_avail_m mve_permco using "$pathDataIntermediate/SignalMasterTable", clear
print("Loading SignalMasterTable...")
df = pl.read_parquet("../pyData/Intermediate/SignalMasterTable.parquet")
df = df.select(['permno', 'gvkey', 'time_avail_m', 'mve_permco'])

# keep if !mi(gvkey)
df = df.filter(pl.col('gvkey').is_not_null())

print(f"After filtering for non-null gvkey: {len(df)} rows")

# merge 1:1 gvkey time_avail_m using "$pathDataIntermediate/m_QCompustat", keepusing(revtq cogsq atq) nogenerate keep(match)
print("Loading m_QCompustat...")
qcomp = pl.read_parquet("../pyData/Intermediate/m_QCompustat.parquet")
qcomp = qcomp.select(['gvkey', 'time_avail_m', 'revtq', 'cogsq', 'atq'])

# Convert gvkey to same type for join
df = df.with_columns(pl.col('gvkey').cast(pl.Int32))
qcomp = qcomp.with_columns(pl.col('gvkey').cast(pl.Int32))


# Apply comprehensive group-wise forward fill for complete data coverage
print("Applying comprehensive group-wise forward fill for quarterly data...")
qcomp = qcomp.sort(['gvkey', 'time_avail_m'])

# Fill revtq, cogsq, and atq with maximum coverage
qcomp = qcomp.with_columns([
    pl.col('revtq').fill_null(strategy="forward").over('gvkey').alias('revtq'),
    pl.col('cogsq').fill_null(strategy="forward").over('gvkey').alias('cogsq'),
    pl.col('atq').fill_null(strategy="forward").over('gvkey').alias('atq')
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
print("Sorting by permno and time...")
df = df.sort(['permno', 'time_avail_m'])


# Convert to pandas for calendar-based 3-month lag operations
print("Converting to calendar-based 3-month lag...")
df_pd = df.to_pandas()

# Create 3-month lag date
df_pd['time_lag3'] = df_pd['time_avail_m'] - pd.DateOffset(months=3)

# Create lag data for merging
lag3_data = df_pd[['permno', 'time_avail_m', 'atq']].copy()
lag3_data.columns = ['permno', 'time_lag3', 'l3_atq']

# Merge to get lagged values (calendar-based, not position-based)
df_pd = df_pd.merge(lag3_data, on=['permno', 'time_lag3'], how='left')

# Convert back to polars
df = pl.from_pandas(df_pd)


# Compute GPlag_q with enhanced null handling and calendar-based lag
print("Computing GPlag_q with enhanced division handling...")
df = df.with_columns([
    pl.when((pl.col('l3_atq').is_null()) | (pl.col('l3_atq') == 0))
    .then(None)  # If l3_atq is null/zero, result is null
    .otherwise((pl.col('revtq') - pl.col('cogsq')) / pl.col('l3_atq'))
    .alias('GPlag_q')
])

print(f"Generated GPlag_q for {len(df)} observations")

# Keep only required columns for output
df_final = df.select(['permno', 'time_avail_m', 'GPlag_q'])

# SAVE
# do "$pathCode/saveplacebo" GPlag_q
save_placebo(df_final, 'GPlag_q')

print("GPlag_q.py completed")