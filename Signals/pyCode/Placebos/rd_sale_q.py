# ABOUTME: rd_sale_q.py - calculates rd_sale_q placebo (R&D-to-sales ratio, quarterly)
# ABOUTME: Python equivalent of rd_sale_q.do, translates line-by-line from Stata code

"""
rd_sale_q.py

Inputs:
    - SignalMasterTable.parquet: permno, gvkey, time_avail_m, prc columns
    - m_QCompustat.parquet: gvkey, time_avail_m, xrdq, saleq columns

Outputs:
    - rd_sale_q.csv: permno, yyyymm, rd_sale_q columns

Usage:
    cd pyCode
    source .venv/bin/activate  
    python3 Placebos/rd_sale_q.py
"""

import pandas as pd
import polars as pl
import sys
import os

# Add parent directory to path to import utils
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from utils.saveplacebo import save_placebo

print("Starting rd_sale_q.py")

# DATA LOAD
# use permno gvkey time_avail_m prc using "$pathDataIntermediate/SignalMasterTable", clear
print("Loading SignalMasterTable...")
df = pl.read_parquet("../pyData/Intermediate/SignalMasterTable.parquet")
df = df.select(['permno', 'gvkey', 'time_avail_m', 'prc'])

# drop if mi(gvkey)
df = df.filter(pl.col('gvkey').is_not_null())

print(f"After filtering for non-null gvkey: {len(df)} rows")

# merge 1:1 gvkey time_avail_m using "$pathDataIntermediate/m_QCompustat", keepusing(xrdq saleq) nogenerate keep(match)
print("Loading m_QCompustat...")
qcomp = pl.read_parquet("../pyData/Intermediate/m_QCompustat.parquet")
qcomp = qcomp.select(['gvkey', 'time_avail_m', 'xrdq', 'saleq'])

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

# gen rd_sale_q = l12.xrdq/l12.saleq
print("Computing 12-month calendar-based lag and rd_sale_q...")

# Convert to pandas for calendar-based lag operations (same approach as cfpq.py)
df_pd = df.to_pandas()

# Create 12-month lag date
df_pd['time_lag12'] = df_pd['time_avail_m'] - pd.DateOffset(months=12)

# Create lag data for merging
lag_vars = ['xrdq', 'saleq']
lag_data = df_pd[['permno', 'time_avail_m'] + lag_vars].copy()
lag_data.columns = ['permno', 'time_lag12'] + [f'l12_{var}' for var in lag_vars]

# Merge to get lagged values (calendar-based, not position-based)
df_pd = df_pd.merge(lag_data, on=['permno', 'time_lag12'], how='left')

# Convert back to polars
df = pl.from_pandas(df_pd)

df = df.with_columns(
    (pl.col('l12_xrdq') / pl.col('l12_saleq')).alias('rd_sale_q')
)

# replace rd_sale_q = . if rd_sale_q == 0
print("Setting rd_sale_q to null where it equals 0...")
df = df.with_columns(
    pl.when(pl.col('rd_sale_q') == 0)
    .then(None)
    .otherwise(pl.col('rd_sale_q'))
    .alias('rd_sale_q')
)

print(f"Generated rd_sale_q for {len(df)} observations")

# Keep only required columns for output
df_final = df.select(['permno', 'time_avail_m', 'rd_sale_q'])

# SAVE
# do "$pathCode/saveplacebo" rd_sale_q
save_placebo(df_final, 'rd_sale_q')

print("rd_sale_q.py completed")