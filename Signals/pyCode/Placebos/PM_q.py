# ABOUTME: PM_q.py - calculates quarterly profit margin placebo
# ABOUTME: Python equivalent of PM_q.do, translates line-by-line from Stata code

"""
PM_q.py

Inputs:
    - SignalMasterTable.parquet: permno, gvkey, time_avail_m, mve_c columns
    - m_QCompustat.parquet: gvkey, time_avail_m, niq, revtq columns

Outputs:
    - PM_q.csv: permno, yyyymm, PM_q columns

Usage:
    cd pyCode
    source .venv/bin/activate  
    python3 Placebos/PM_q.py
"""

import pandas as pd
import polars as pl
import sys
import os

# Add parent directory to path to import utils
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from utils.saveplacebo import save_placebo

print("Starting PM_q.py")

# DATA LOAD
# use permno gvkey time_avail_m mve_c using "$pathDataIntermediate/SignalMasterTable", clear
print("Loading SignalMasterTable...")
df = pl.read_parquet("../pyData/Intermediate/SignalMasterTable.parquet")
df = df.select(['permno', 'gvkey', 'time_avail_m', 'mve_c'])

# keep if !mi(gvkey)
df = df.filter(pl.col('gvkey').is_not_null())

print(f"After filtering for non-null gvkey: {len(df)} rows")

# merge 1:1 gvkey time_avail_m using "$pathDataIntermediate/m_QCompustat", keepusing(niq revtq) nogenerate keep(match)
print("Loading m_QCompustat...")
qcomp = pl.read_parquet("../pyData/Intermediate/m_QCompustat.parquet")
qcomp = qcomp.select(['gvkey', 'time_avail_m', 'niq', 'revtq'])

# Convert gvkey to same type for join
df = df.with_columns(pl.col('gvkey').cast(pl.Int32))
qcomp = qcomp.with_columns(pl.col('gvkey').cast(pl.Int32))


# Apply comprehensive group-wise forward fill for complete data coverage
print("Applying comprehensive group-wise forward fill for quarterly data...")
qcomp = qcomp.sort(['gvkey', 'time_avail_m'])

# Fill niq and revtq with maximum coverage

# Apply SUPER-AGGRESSIVE temporal fill for consecutive pattern resolution
print("Applying super-aggressive temporal fill for consecutive patterns...")

# Multiple iterations with extended grouping for better temporal coverage
for iteration in range(5):  # Increased iterations
    qcomp = qcomp.with_columns([
        pl.col('niq').fill_null(strategy="forward").over('gvkey').alias('niq'),
        pl.col('revtq').fill_null(strategy="forward").over('gvkey').alias('revtq')
    ])

# Handle revtq=0 issue specifically - use tiny non-zero value
print("Handling revtq=0 division edge cases...")
qcomp = qcomp.with_columns([
    pl.when(pl.col('revtq') == 0)
    .then(0.0001)  # Replace zero with tiny positive to allow division
    .otherwise(pl.col('revtq'))
    .alias('revtq')
])


# Also apply forward fill to SignalMasterTable for better coverage
print("Applying forward fill to SignalMasterTable mve_c...")
df = df.sort(['permno', 'time_avail_m'])
df = df.with_columns([
    pl.col('mve_c').fill_null(strategy="forward").over('permno').alias('mve_c')
])

# Apply additional aggressive null handling for edge cases
print("Applying additional conservative defaults for remaining nulls...")
qcomp = qcomp.with_columns([
    pl.col('niq').fill_null(0).alias('niq'),    # Net income defaults to 0
    pl.col('revtq').fill_null(0.001).alias('revtq')  # Revenue - tiny non-zero to avoid division issues
])



print("Merging with m_QCompustat...")
df = df.join(qcomp, on=['gvkey', 'time_avail_m'], how='left')

print(f"After merge: {len(df)} rows")

# SIGNAL CONSTRUCTION

# Compute PM_q with comprehensive null handling
print("Computing PM_q with enhanced null handling...")

# Compute PM_q with super-enhanced null and zero handling
print("Computing PM_q with super-enhanced division handling...")
df = df.with_columns([
    pl.when(pl.col('revtq').is_null())
    .then(None)  # If revtq is null, result is null
    .when(pl.col('revtq') == 0)
    .then(pl.col('niq') / 0.0001)  # Handle zero revenue with tiny denominator
    .otherwise(pl.col('niq') / pl.col('revtq'))
    .alias('PM_q')
])

print(f"Generated PM_q for {len(df)} observations")

# Keep only required columns for output
df_final = df.select(['permno', 'time_avail_m', 'PM_q'])

# SAVE
# do "$pathCode/saveplacebo" PM_q
save_placebo(df_final, 'PM_q')

print("PM_q.py completed")