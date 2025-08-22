# ABOUTME: EarningsSmoothness.py - calculates earnings smoothness placebo
# ABOUTME: Python equivalent of EarningsSmoothness.do, translates line-by-line from Stata code

"""
EarningsSmoothness.py

Inputs:
    - a_aCompustat.parquet: gvkey, permno, time_avail_m, fyear, ib, at, act, lct, che, dlc, dp, datadate columns

Outputs:
    - EarningsSmoothness.csv: permno, yyyymm, EarningsSmoothness columns

Usage:
    cd pyCode
    source .venv/bin/activate  
    python3 Placebos/EarningsSmoothness.py
"""

import pandas as pd
import polars as pl
import numpy as np
import sys
import os

# Add parent directory to path to import utils
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from utils.saveplacebo import save_placebo

print("Starting EarningsSmoothness.py")

# DATA LOAD
# use gvkey permno time_avail_m fyear ib at act lct che dlc dp at datadate using "$pathDataIntermediate/a_aCompustat", clear
print("Loading a_aCompustat...")
df = pl.read_parquet("../pyData/Intermediate/a_aCompustat.parquet")
df = df.select(['gvkey', 'permno', 'time_avail_m', 'fyear', 'ib', 'at', 'act', 'lct', 'che', 'dlc', 'dp', 'datadate'])

print(f"After loading: {len(df)} rows")

# SIGNAL CONSTRUCTION
# xtset gvkey fyear
print("Sorting by gvkey and fyear...")
df = df.sort(['gvkey', 'fyear'])

# Convert to pandas for lag and rolling operations
df_pd = df.to_pandas()

# Create lag for at, act, lct, che, dlc by fyear
lag_vars = ['at', 'act', 'lct', 'che', 'dlc']
for var in lag_vars:
    df_pd[f'l1_{var}'] = df_pd.groupby('gvkey')[var].shift(1)

# gen tempEarnings = ib/l.at
print("Computing tempEarnings...")
df_pd['tempEarnings'] = df_pd['ib'] / df_pd['l1_at']

# gen tempCF = (ib - ( (act - l.act) - (lct - l.lct) - (che - l.che) + (dlc - l.dlc) - dp))/l.at
print("Computing tempCF...")
df_pd['tempCF'] = (df_pd['ib'] - ((df_pd['act'] - df_pd['l1_act']) - 
                                  (df_pd['lct'] - df_pd['l1_lct']) - 
                                  (df_pd['che'] - df_pd['l1_che']) + 
                                  (df_pd['dlc'] - df_pd['l1_dlc']) - 
                                  df_pd['dp'])) / df_pd['l1_at']

# asrol tempEarnings, gen(sd10_tempEarnings) window(fyear 10) min(10) by(gvkey) stat(sd)
# asrol tempCF, gen(sd10_tempCF) window(fyear 10) min(10) by(gvkey) stat(sd)
print("Computing 10-year rolling standard deviations...")
df_pd = df_pd.set_index(['gvkey', 'fyear']).sort_index()

df_pd['sd10_tempEarnings'] = df_pd.groupby('gvkey')['tempEarnings'].rolling(window=10, min_periods=10).std().reset_index(level=0, drop=True)
df_pd['sd10_tempCF'] = df_pd.groupby('gvkey')['tempCF'].rolling(window=10, min_periods=10).std().reset_index(level=0, drop=True)

df_pd = df_pd.reset_index()

# gen EarningsSmoothness = sd10_tempEarnings/sd10_tempCF
print("Computing EarningsSmoothness...")
df_pd['EarningsSmoothness'] = df_pd['sd10_tempEarnings'] / df_pd['sd10_tempCF']

# Convert back to polars
df = pl.from_pandas(df_pd)

# * Expand to monthly
print("Expanding to monthly data...")
# Create 12 copies of each row
df_expanded_list = []
for month in range(12):
    df_month = df.clone()
    df_month = df_month.with_columns(
        (pl.col('time_avail_m') + pl.duration(days=30*month)).alias('time_avail_m')
    )
    df_expanded_list.append(df_month)

df_expanded = pl.concat(df_expanded_list)

# bysort gvkey time_avail_m (datadate): keep if _n == _N
print("Keeping latest datadate for each gvkey-time_avail_m...")
df_expanded = df_expanded.sort(['gvkey', 'time_avail_m', 'datadate'])
df_expanded = df_expanded.group_by(['gvkey', 'time_avail_m']).last()

# bysort permno time_avail_m: keep if _n == 1  // deletes a few observations
print("Dropping duplicates by permno-time_avail_m...")
df_expanded = df_expanded.unique(subset=['permno', 'time_avail_m'], keep='first')

print(f"Generated EarningsSmoothness for {len(df_expanded)} observations")

# Keep only required columns for output
df_final = df_expanded.select(['permno', 'time_avail_m', 'EarningsSmoothness'])

# SAVE
# do "$pathCode/saveplacebo" EarningsSmoothness
save_placebo(df_final, 'EarningsSmoothness')

print("EarningsSmoothness.py completed")