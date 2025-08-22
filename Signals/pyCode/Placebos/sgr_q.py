# ABOUTME: sgr_q.py - calculates sgr_q placebo (Quarterly sales growth)
# ABOUTME: Python equivalent of sgr_q.do, translates line-by-line from Stata code

"""
sgr_q.py

Inputs:
    - SignalMasterTable.parquet: permno, gvkey, time_avail_m, mve_c columns
    - m_QCompustat.parquet: gvkey, time_avail_m, saleq columns

Outputs:
    - sgr_q.csv: permno, yyyymm, sgr_q columns

Usage:
    cd pyCode
    source .venv/bin/activate  
    python3 Placebos/sgr_q.py
"""

import pandas as pd
import polars as pl
import sys
import os

# Add parent directory to path to import utils
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from utils.saveplacebo import save_placebo

print("Starting sgr_q.py")

# DATA LOAD
# use permno gvkey time_avail_m mve_c using "$pathDataIntermediate/SignalMasterTable", clear
print("Loading SignalMasterTable...")
df = pl.read_parquet("../pyData/Intermediate/SignalMasterTable.parquet")
df = df.select(['permno', 'gvkey', 'time_avail_m', 'mve_c'])

# keep if !mi(gvkey)
df = df.filter(pl.col('gvkey').is_not_null())

print(f"After filtering for non-null gvkey: {len(df)} rows")

# merge 1:1 gvkey time_avail_m using "$pathDataIntermediate/m_QCompustat", keepusing(saleq) nogenerate keep(match)
print("Loading m_QCompustat...")
qcomp = pl.read_parquet("../pyData/Intermediate/m_QCompustat.parquet")
qcomp = qcomp.select(['gvkey', 'time_avail_m', 'saleq'])

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

# gen sgr_q = (saleq/l12.saleq)-1
print("Computing 12-month calendar-based lag and sgr_q...")

# Convert to pandas for calendar-based lag operations
df_pd = df.to_pandas()

# Create 12-month lag date
df_pd['time_lag12'] = df_pd['time_avail_m'] - pd.DateOffset(months=12)

# Create lag data for merging
lag_data = df_pd[['permno', 'time_avail_m', 'saleq']].copy()
lag_data.columns = ['permno', 'time_lag12', 'l12_saleq']

# Merge to get lagged values (calendar-based, not position-based)
df_pd = df_pd.merge(lag_data, on=['permno', 'time_lag12'], how='left')

# Convert back to polars
df = pl.from_pandas(df_pd)

# Calculate sgr_q with Stata-compatible missing value handling
# Stata treats missing saleq as 0 in ratio calculations
df = df.with_columns([
    # If current saleq is missing, treat as 0; if lag saleq is missing, treat as 0 (but avoid division by zero)
    pl.when(pl.col('saleq').is_null()).then(0.0).otherwise(pl.col('saleq')).alias('saleq_filled'),
    pl.when(pl.col('l12_saleq').is_null()).then(pl.lit(float('inf'))).otherwise(pl.col('l12_saleq')).alias('l12_saleq_filled')
])

df = df.with_columns(
    pl.when(pl.col('l12_saleq_filled') == float('inf'))
    .then(None)  # If denominator was missing, result is missing
    .when(pl.col('l12_saleq_filled') == 0.0) 
    .then(None)  # Avoid division by zero
    .otherwise((pl.col('saleq_filled') / pl.col('l12_saleq_filled')) - 1)
    .alias('sgr_q')
)

print(f"Generated sgr_q for {len(df)} observations")

# Keep only required columns for output
df_final = df.select(['permno', 'time_avail_m', 'sgr_q'])

# SAVE
# do "$pathCode/saveplacebo" sgr_q
save_placebo(df_final, 'sgr_q')

print("sgr_q.py completed")