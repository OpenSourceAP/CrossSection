# ABOUTME: NetPayoutYield_q.py - calculates net payout yield placebo (quarterly)
# ABOUTME: Python equivalent of NetPayoutYield_q.do, translates line-by-line from Stata code

"""
NetPayoutYield_q.py

Inputs:
    - SignalMasterTable.parquet: permno, gvkey, time_avail_m, mve_c columns
    - m_QCompustat.parquet: gvkey, time_avail_m, dvpsxq, cshoq, ajexq, prstkcyq, pstkq, sstkyq columns

Outputs:
    - NetPayoutYield_q.csv: permno, yyyymm, NetPayoutYield_q columns

Usage:
    cd pyCode
    source .venv/bin/activate  
    python3 Placebos/NetPayoutYield_q.py
"""

import pandas as pd
import polars as pl
import sys
import os

# Add parent directory to path to import utils
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from utils.saveplacebo import save_placebo
from utils.forward_fill import apply_quarterly_fill_to_compustat

print("Starting NetPayoutYield_q.py")

# DATA LOAD
# use permno gvkey time_avail_m mve_c using "$pathDataIntermediate/SignalMasterTable", clear
print("Loading SignalMasterTable...")
df = pl.read_parquet("../pyData/Intermediate/SignalMasterTable.parquet")
df = df.select(['permno', 'gvkey', 'time_avail_m', 'mve_c'])

# keep if !mi(gvkey)
df = df.filter(pl.col('gvkey').is_not_null())

print(f"After filtering for non-null gvkey: {len(df)} rows")

# merge 1:1 gvkey time_avail_m using "$pathDataIntermediate/m_QCompustat", keepusing(dvpsxq cshoq ajexq prstkcyq pstkq sstkyq) nogenerate keep(match)
print("Loading m_QCompustat...")
qcomp = pl.read_parquet("../pyData/Intermediate/m_QCompustat.parquet")
qcomp = qcomp.select(['gvkey', 'time_avail_m', 'dvpsxq', 'cshoq', 'ajexq', 'prstkcyq', 'pstkq', 'sstkyq'])

# Convert gvkey to same type for join
df = df.with_columns(pl.col('gvkey').cast(pl.Int32))
qcomp = qcomp.with_columns(pl.col('gvkey').cast(pl.Int32))

print("Applying forward-fill for missing quarterly values...")
qcomp = apply_quarterly_fill_to_compustat(qcomp, quarterly_columns=['dvpsxq', 'cshoq', 'ajexq', 'prstkcyq', 'pstkq', 'sstkyq'])

print("Merging with m_QCompustat...")
df = df.join(qcomp, on=['gvkey', 'time_avail_m'], how='inner')

print(f"After merge: {len(df)} rows")

# SIGNAL CONSTRUCTION
# xtset permno time_avail_m
print("Sorting for lag operations...")
df = df.sort(['permno', 'time_avail_m'])

# Convert to pandas for lag operations
df_pd = df.to_pandas()

# Create 3-month lag date
df_pd['time_lag3'] = df_pd['time_avail_m'] - pd.DateOffset(months=3)

# Create lag data for merging
lag_vars = ['pstkq']
lag_data = df_pd[['permno', 'time_avail_m'] + lag_vars].copy()
lag_data.columns = ['permno', 'time_lag3'] + [f'l3_{var}' for var in lag_vars]

# Merge lag data
df_pd = df_pd.merge(lag_data, on=['permno', 'time_lag3'], how='left')

# Convert back to polars
df = pl.from_pandas(df_pd.drop(columns=['time_lag3']))

# gen tempDiv = dvpsxq*cshoq*ajexq
print("Computing tempDiv...")
df = df.with_columns(
    (pl.col('dvpsxq') * pl.col('cshoq') * pl.col('ajexq')).alias('tempDiv')
)

# gen tempTotalPayout = tempDiv + prstkcyq + (pstkq - l3.pstkq)
print("Computing tempTotalPayout...")
df = df.with_columns(
    (pl.col('tempDiv') + pl.col('prstkcyq') + (pl.col('pstkq') - pl.col('l3_pstkq'))).alias('tempTotalPayout')
)

# gen NetPayoutYield_q = (tempTotalPayout - sstkyq - (pstkq - l3.pstkq))/mve_c
print("Computing NetPayoutYield_q...")
df = df.with_columns(
    ((pl.col('tempTotalPayout') - pl.col('sstkyq') - (pl.col('pstkq') - pl.col('l3_pstkq'))) / pl.col('mve_c')).alias('NetPayoutYield_q')
)

print(f"Generated NetPayoutYield_q for {len(df)} observations")

# Keep only required columns for output
df_final = df.select(['permno', 'time_avail_m', 'NetPayoutYield_q'])

# SAVE
# do "$pathCode/saveplacebo" NetPayoutYield_q
save_placebo(df_final, 'NetPayoutYield_q')

print("NetPayoutYield_q.py completed")