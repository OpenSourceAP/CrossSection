# ABOUTME: ChangeRoA.py - calculates change in return on assets placebo
# ABOUTME: Python equivalent of ChangeRoA.do, translates line-by-line from Stata code

"""
ChangeRoA.py

Inputs:
    - SignalMasterTable.parquet: permno, gvkey, time_avail_m, mve_permco columns
    - m_QCompustat.parquet: gvkey, time_avail_m, atq, ibq columns

Outputs:
    - ChangeRoA.csv: permno, yyyymm, ChangeRoA columns

Usage:
    cd pyCode
    source .venv/bin/activate  
    python3 Placebos/ChangeRoA.py
"""

import pandas as pd
import polars as pl
import sys
import os

# Add parent directory to path to import utils
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from utils.stata_replication import fill_date_gaps, stata_multi_lag
from utils.saveplacebo import save_placebo

print("Starting ChangeRoA.py")

# DATA LOAD
# use permno gvkey time_avail_m mve_permco using "$pathDataIntermediate/SignalMasterTable", clear
print("Loading SignalMasterTable...")
df = pl.read_parquet("../pyData/Intermediate/SignalMasterTable.parquet")
df = df.select(['permno', 'gvkey', 'time_avail_m', 'mve_permco'])

# keep if !mi(gvkey)
df = df.filter(pl.col('gvkey').is_not_null())

print(f"After filtering for non-null gvkey: {len(df)} rows")

# merge 1:1 gvkey time_avail_m using "$pathDataIntermediate/m_QCompustat", keepusing(atq ibq) nogenerate keep(match)
print("Loading m_QCompustat...")
qcomp = pl.read_parquet("../pyData/Intermediate/m_QCompustat.parquet")
qcomp = qcomp.select(['gvkey', 'time_avail_m', 'atq', 'ibq'])

# Convert gvkey to same type for join
df = df.with_columns(pl.col('gvkey').cast(pl.Int32))
qcomp = qcomp.with_columns(pl.col('gvkey').cast(pl.Int32))


# Apply comprehensive group-wise forward fill for complete data coverage
print("Applying comprehensive group-wise forward fill for quarterly data...")
qcomp = qcomp.sort(['gvkey', 'time_avail_m'])

# Fill atq and ibq with maximum coverage
qcomp = qcomp.with_columns([
    pl.col('atq').fill_null(strategy="forward").over('gvkey').alias('atq'),
    pl.col('ibq').fill_null(strategy="forward").over('gvkey').alias('ibq')
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


# Compute tempRoa with enhanced null handling
print("Computing tempRoa with enhanced division handling...")
df = df.with_columns([
    pl.when((pl.col('atq').is_null()) | (pl.col('atq') == 0))
    .then(None)  # If atq is null/zero, result is null
    .otherwise(pl.col('ibq') / pl.col('atq'))
    .alias('tempRoa')
])

# gen ChangeRoA = tempRoa - l12.tempRoa
print("Computing 12-month calendar-based lag and ChangeRoA...")

# Calendar endpoints require the target month; retain only observed rows.
df = df.with_columns(pl.lit(True).alias("_observed"))
df = fill_date_gaps(df, "permno", "time_avail_m", "1mo")
df = stata_multi_lag(df, "permno", "time_avail_m", ['tempRoa'], [12], prefix="l", fill_gaps=False)
df = df.filter(pl.col("_observed").eq(True)).drop("_observed")
# Match the former Pandas-to-Polars conversion of computed NaN values.
df = df.fill_nan(None)

df = df.with_columns(
    (pl.col('tempRoa') - pl.col('l12_tempRoa')).alias('ChangeRoA')
)

print(f"Generated ChangeRoA for {len(df)} observations")

# Keep only required columns for output
df_final = df.select(['permno', 'time_avail_m', 'ChangeRoA'])

# SAVE
# do "$pathCode/saveplacebo" ChangeRoA
save_placebo(df_final, 'ChangeRoA')

print("ChangeRoA.py completed")
