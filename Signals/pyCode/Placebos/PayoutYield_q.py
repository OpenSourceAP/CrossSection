# ABOUTME: PayoutYield_q.py - calculates payout yield placebo (quarterly)
# ABOUTME: Python equivalent of PayoutYield_q.do, translates line-by-line from Stata code

"""
PayoutYield_q.py

Inputs:
    - SignalMasterTable.parquet: permno, gvkey, time_avail_m, mve_c columns
    - m_QCompustat.parquet: gvkey, time_avail_m, dvpsxq, cshoq, ajexq, prstkcyq, pstkq columns

Outputs:
    - PayoutYield_q.csv: permno, yyyymm, PayoutYield_q columns

Usage:
    cd pyCode
    source .venv/bin/activate  
    python3 Placebos/PayoutYield_q.py
"""

import pandas as pd
import polars as pl
import sys
import os

# Add parent directory to path to import utils
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from utils.saveplacebo import save_placebo

print("Starting PayoutYield_q.py")

# DATA LOAD
# use permno gvkey time_avail_m mve_c using "$pathDataIntermediate/SignalMasterTable", clear
print("Loading SignalMasterTable...")
df = pl.read_parquet("../pyData/Intermediate/SignalMasterTable.parquet")
df = df.select(['permno', 'gvkey', 'time_avail_m', 'mve_c'])

# keep if !mi(gvkey)
df = df.filter(pl.col('gvkey').is_not_null())

print(f"After filtering for non-null gvkey: {len(df)} rows")

# merge 1:1 gvkey time_avail_m using "$pathDataIntermediate/m_QCompustat", keepusing(dvpsxq cshoq ajexq prstkcyq pstkq) nogenerate keep(match)
print("Loading m_QCompustat...")
qcomp = pl.read_parquet("../pyData/Intermediate/m_QCompustat.parquet")
qcomp = qcomp.select(['gvkey', 'time_avail_m', 'dvpsxq', 'cshoq', 'ajexq', 'prstkcyq', 'pstkq'])

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

# gen tempDiv = dvpsxq*cshoq*ajexq
print("Computing tempDiv...")
df = df.with_columns(
    (pl.col('dvpsxq') * pl.col('cshoq') * pl.col('ajexq')).alias('tempDiv')
)

# Need calendar-based lags for l3.pstkq and l6.mve_c
print("Computing 3-month and 6-month calendar-based lags...")

# Convert to pandas for calendar-based lag operations
df_pd = df.to_pandas()

# Create 3-month and 6-month lag dates
df_pd['time_lag3'] = df_pd['time_avail_m'] - pd.DateOffset(months=3)
df_pd['time_lag6'] = df_pd['time_avail_m'] - pd.DateOffset(months=6)

# Create lag data for merging (3-month lag for pstkq)
lag3_data = df_pd[['permno', 'time_avail_m', 'pstkq']].copy()
lag3_data.columns = ['permno', 'time_lag3', 'l3_pstkq']

# Create lag data for merging (6-month lag for mve_c)
lag6_data = df_pd[['permno', 'time_avail_m', 'mve_c']].copy()
lag6_data.columns = ['permno', 'time_lag6', 'l6_mve_c']

# Merge to get lagged values
df_pd = df_pd.merge(lag3_data, on=['permno', 'time_lag3'], how='left')
df_pd = df_pd.merge(lag6_data, on=['permno', 'time_lag6'], how='left')

# Convert back to polars
df = pl.from_pandas(df_pd)

# gen tempTotalPayout = tempDiv + prstkcyq + (pstkq - l3.pstkq)
print("Computing tempTotalPayout...")
df = df.with_columns(
    (pl.col('tempDiv') + pl.col('prstkcyq') + (pl.col('pstkq') - pl.col('l3_pstkq'))).alias('tempTotalPayout')
)

# gen PayoutYield_q = tempTotalPayout/l6.mve_c
print("Computing PayoutYield_q...")
df = df.with_columns(
    (pl.col('tempTotalPayout') / pl.col('l6_mve_c')).alias('PayoutYield_q')
)

# replace PayoutYield_q = . if PayoutYield_q <= 0
print("Setting non-positive PayoutYield_q to null...")
df = df.with_columns(
    pl.when(pl.col('PayoutYield_q') <= 0)
    .then(None)
    .otherwise(pl.col('PayoutYield_q'))
    .alias('PayoutYield_q')
)

print(f"Generated PayoutYield_q for {len(df)} observations")

# Keep only required columns for output
df_final = df.select(['permno', 'time_avail_m', 'PayoutYield_q'])

# SAVE
# do "$pathCode/saveplacebo" PayoutYield_q
save_placebo(df_final, 'PayoutYield_q')

print("PayoutYield_q.py completed")