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
from utils.save_standardized import save_placebo
from utils.stata_replication import stata_multi_lag

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


# Create 3-month lag using stata_multi_lag
print("Computing 3-month lag using stata_multi_lag...")
df_pandas = df.to_pandas()
df_pandas = stata_multi_lag(df_pandas, 'permno', 'time_avail_m', 'atq', [3], freq='M', prefix='l')
df = pl.from_pandas(df_pandas)

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