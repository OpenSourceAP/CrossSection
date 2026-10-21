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
from utils.stata_replication import fill_date_gaps, stata_multi_lag
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

# Apply enhanced group-wise forward-only fill for complete data coverage
print("Applying enhanced group-wise forward-only fill for R&D data...")
qcomp = qcomp.sort(['gvkey', 'time_avail_m'])
qcomp = qcomp.with_columns([
    pl.col('saleq').fill_null(strategy="forward").over('gvkey').alias('saleq'),
    pl.col('xrdq').fill_null(strategy="forward").over('gvkey').alias('xrdq')
])

# Convert gvkey to same type for join
df = df.with_columns(pl.col('gvkey').cast(pl.Int32))
qcomp = qcomp.with_columns(pl.col('gvkey').cast(pl.Int32))

print("Merging with m_QCompustat...")
# Use left join to preserve SignalMasterTable observations
# Stata's keep(match) might be more lenient about missing values
df = df.join(qcomp, on=['gvkey', 'time_avail_m'], how='left')

print(f"After merge: {len(df)} rows")

# SIGNAL CONSTRUCTION
# xtset permno time_avail_m
print("Sorting for lag operations...")
df = df.sort(['permno', 'time_avail_m'])

# gen rd_sale_q = l12.xrdq/l12.saleq
print("Computing 12-month calendar-based lag and rd_sale_q...")

# Calendar endpoints require the target month; retain only observed rows.
df = df.with_columns(pl.lit(True).alias("_observed"))
df = fill_date_gaps(df, "permno", "time_avail_m", "1mo")
df = stata_multi_lag(df, "permno", "time_avail_m", ['xrdq', 'saleq'], [12], prefix="l", fill_gaps=False)
df = df.filter(pl.col("_observed").eq(True)).drop("_observed")
# Match the former Pandas-to-Polars conversion of computed NaN values.
df = df.fill_nan(None)

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
