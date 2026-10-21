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
from utils.stata_replication import fill_date_gaps, stata_multi_lag
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

# Calendar endpoints require the target month; retain only observed rows.
df = df.with_columns(pl.lit(True).alias("_observed"))
df = fill_date_gaps(df, "permno", "time_avail_m", "1mo")
df = stata_multi_lag(df, "permno", "time_avail_m", ['atq'], [3], prefix="l", fill_gaps=False)
df = df.filter(pl.col("_observed").eq(True)).drop("_observed")
# Match the former Pandas-to-Polars conversion of computed NaN values.
df = df.fill_nan(None)

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
