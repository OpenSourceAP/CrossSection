# ABOUTME: OPLeverage_q.py - calculates operating leverage placebo (quarterly)
# ABOUTME: Python equivalent of OPLeverage_q.do, translates line-by-line from Stata code

"""
OPLeverage_q.py

Inputs:
    - SignalMasterTable.parquet: permno, gvkey, time_avail_m, mve_c columns
    - m_QCompustat.parquet: gvkey, time_avail_m, xsgaq, cogsq, atq columns

Outputs:
    - OPLeverage_q.csv: permno, yyyymm, OPLeverage_q columns

Usage:
    cd pyCode
    source .venv/bin/activate  
    python3 Placebos/OPLeverage_q.py
"""

import pandas as pd
import polars as pl
import sys
import os

# Add parent directory to path to import utils
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from utils.saveplacebo import save_placebo

print("Starting OPLeverage_q.py")

# DATA LOAD
# use permno gvkey time_avail_m mve_c using "$pathDataIntermediate/SignalMasterTable", clear
print("Loading SignalMasterTable...")
df = pl.read_parquet("../pyData/Intermediate/SignalMasterTable.parquet")
df = df.select(['permno', 'gvkey', 'time_avail_m', 'mve_c'])

# keep if !mi(gvkey)
df = df.filter(pl.col('gvkey').is_not_null())

print(f"After filtering for non-null gvkey: {len(df)} rows")

# merge 1:1 gvkey time_avail_m using "$pathDataIntermediate/m_QCompustat", keepusing(xsga cogsq atq) nogenerate keep(match)
print("Loading m_QCompustat...")
qcomp = pl.read_parquet("../pyData/Intermediate/m_QCompustat.parquet")
qcomp = qcomp.select(['gvkey', 'time_avail_m', 'xsgaq', 'cogsq', 'atq'])

# Convert gvkey to same type for join
df = df.with_columns(pl.col('gvkey').cast(pl.Int32))
qcomp = qcomp.with_columns(pl.col('gvkey').cast(pl.Int32))

print("Merging with m_QCompustat...")
df = df.join(qcomp, on=['gvkey', 'time_avail_m'], how='inner')

print(f"After merge: {len(df)} rows")

# SIGNAL CONSTRUCTION
# gen tempxsga = 0
# replace tempxsga = xsgaq if xsgaq !=.
print("Computing tempxsga...")
df = df.with_columns(
    pl.when(pl.col('xsgaq').is_not_null())
    .then(pl.col('xsgaq'))
    .otherwise(0)
    .alias('tempxsga')
)

# gen OPLeverage_q = (tempxsga + cogsq)/atq
print("Computing OPLeverage_q...")
df = df.with_columns(
    ((pl.col('tempxsga') + pl.col('cogsq')) / pl.col('atq')).alias('OPLeverage_q')
)

print(f"Generated OPLeverage_q for {len(df)} observations")

# Keep only required columns for output
df_final = df.select(['permno', 'time_avail_m', 'OPLeverage_q'])

# SAVE
# do "$pathCode/saveplacebo" OPLeverage_q
save_placebo(df_final, 'OPLeverage_q')

print("OPLeverage_q.py completed")