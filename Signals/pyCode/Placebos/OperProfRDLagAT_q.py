# ABOUTME: OperProfRDLagAT_q.py - calculates quarterly operating profits to lagged assets placebo
# ABOUTME: Python equivalent of OperProfRDLagAT_q.do, translates line-by-line from Stata code

"""
OperProfRDLagAT_q.py

Inputs:
    - SignalMasterTable.parquet: permno, gvkey, time_avail_m, prc columns
    - m_QCompustat.parquet: gvkey, time_avail_m, xrdq, revtq, cogsq, xsgaq, atq columns

Outputs:
    - OperProfRDLagAT_q.csv: permno, yyyymm, OperProfRDLagAT_q columns

Usage:
    cd pyCode
    source .venv/bin/activate  
    python3 Placebos/OperProfRDLagAT_q.py
"""

import pandas as pd
import polars as pl
import sys
import os

# Add parent directory to path to import utils
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from utils.saveplacebo import save_placebo

print("Starting OperProfRDLagAT_q.py")

# DATA LOAD
# use permno gvkey time_avail_m prc using "$pathDataIntermediate/SignalMasterTable", clear
print("Loading SignalMasterTable...")
df = pl.read_parquet("../pyData/Intermediate/SignalMasterTable.parquet")
df = df.select(['permno', 'gvkey', 'time_avail_m', 'prc'])

# drop if mi(gvkey)
df = df.filter(pl.col('gvkey').is_not_null())

print(f"After filtering for non-null gvkey: {len(df)} rows")

# merge 1:1 gvkey time_avail_m using "$pathDataIntermediate/m_QCompustat", keepusing(xrdq revtq cogsq xsgaq atq) nogenerate keep(match)
print("Loading m_QCompustat...")
comp = pl.read_parquet("../pyData/Intermediate/m_QCompustat.parquet")
comp = comp.select(['gvkey', 'time_avail_m', 'xrdq', 'revtq', 'cogsq', 'xsgaq', 'atq'])

# Convert gvkey to same type for join
df = df.with_columns(pl.col('gvkey').cast(pl.Int32))
comp = comp.with_columns(pl.col('gvkey').cast(pl.Int32))


print("Merging with m_QCompustat...")
df = df.join(comp, on=['gvkey', 'time_avail_m'], how='inner')  # keep(match)

print(f"After merge: {len(df)} rows")

# SIGNAL CONSTRUCTION
# Sort for lag operations
print("Sorting by permno and time...")
df = df.sort(['permno', 'time_avail_m'])

# gen tempXRD = xrdq
# replace tempXRD = 0 if mi(tempXRD)
print("Creating tempXRD with zero replacement for missing...")
df = df.with_columns([
    pl.col('xrdq').fill_null(0).alias('tempXRD')
])


# Create 3-month calendar-based lag (like Stata's l3.)
print("Creating calendar-based 3-month lag of atq...")
df_pd = df.to_pandas()
df_pd['target_lag_date'] = df_pd['time_avail_m'] - pd.DateOffset(months=3)

# Create lag data
lag_data = df_pd[['permno', 'time_avail_m', 'atq']].copy()
lag_data = lag_data.rename(columns={'atq': 'l3_atq', 'time_avail_m': 'target_lag_date'})

# Merge to get lagged values
df_pd = df_pd.merge(lag_data, on=['permno', 'target_lag_date'], how='left')

# Convert back to polars
df = pl.from_pandas(df_pd.drop(columns=['target_lag_date']))

# Compute OperProfRDLagAT_q = (revtq - cogsq - xsgaq + tempXRD)/l3.atq
print("Computing OperProfRDLagAT_q...")
df = df.with_columns([
    ((pl.col('revtq') - pl.col('cogsq') - pl.col('xsgaq') + pl.col('tempXRD')) / pl.col('l3_atq'))
    .alias('OperProfRDLagAT_q')
])

print(f"Generated OperProfRDLagAT_q for {len(df)} observations")

# Keep only required columns
df_final = df.select(['permno', 'time_avail_m', 'OperProfRDLagAT_q'])

# SAVE
# do "$pathCode/saveplacebo" OperProfRDLagAT_q
save_placebo(df_final, 'OperProfRDLagAT_q')

print("OperProfRDLagAT_q.py completed")