# ABOUTME: ZScore.py - calculates Altman Z-Score placebo
# ABOUTME: Python equivalent of ZScore.do, translates line-by-line from Stata code

"""
ZScore.py

Inputs:
    - m_aCompustat.parquet: gvkey, permno, time_avail_m, act, lct, at, lt, re, ni, xint, txt, revt, sic columns
    - SignalMasterTable.parquet: permno, time_avail_m, mve_c columns

Outputs:
    - ZScore.csv: permno, yyyymm, ZScore columns

Usage:
    cd pyCode
    source .venv/bin/activate  
    python3 Placebos/ZScore.py
"""

import pandas as pd
import polars as pl
import sys
import os

# Add parent directory to path to import utils
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from utils.saveplacebo import save_placebo

print("Starting ZScore.py")

# DATA LOAD
# use gvkey permno time_avail_m act lct at lt re ni xint txt revt sic using "$pathDataIntermediate/m_aCompustat", clear
print("Loading m_aCompustat...")
df = pl.read_parquet("../pyData/Intermediate/m_aCompustat.parquet")
df = df.select(['gvkey', 'permno', 'time_avail_m', 'act', 'lct', 'at', 'lt', 're', 'ni', 'xint', 'txt', 'revt', 'sic'])

print(f"After loading: {len(df)} rows")

# bysort permno time_avail_m: keep if _n == 1  // deletes a few observations
print("Dropping duplicates...")
df = df.unique(subset=['permno', 'time_avail_m'])

print(f"After dropping duplicates: {len(df)} rows")

# merge 1:1 permno time_avail_m using "$pathDataIntermediate/SignalMasterTable", keep(match) nogenerate keepusing(mve_c)
print("Loading SignalMasterTable...")
signal_df = pl.read_parquet("../pyData/Intermediate/SignalMasterTable.parquet")
signal_df = signal_df.select(['permno', 'time_avail_m', 'mve_c'])

print("Merging with SignalMasterTable...")
df = df.join(signal_df, on=['permno', 'time_avail_m'], how='inner')

print(f"After merge: {len(df)} rows")

# SIGNAL CONSTRUCTION
# gen ZScore = 1.2*(act - lct)/at + 1.4*(re/at) + 3.3*(ni + xint + txt)/at + .6*(mve_c/lt) + revt/at
print("Computing ZScore...")
df = df.with_columns(
    (1.2 * (pl.col('act') - pl.col('lct')) / pl.col('at') + 
     1.4 * pl.col('re') / pl.col('at') + 
     3.3 * (pl.col('ni') + pl.col('xint') + pl.col('txt')) / pl.col('at') + 
     0.6 * pl.col('mve_c') / pl.col('lt') + 
     pl.col('revt') / pl.col('at')).alias('ZScore')
)

# destring sic, replace
# Convert sic to numeric (Polars handles this automatically if it's string)
print("Processing SIC codes...")
df = df.with_columns(
    pl.col('sic').cast(pl.Float64, strict=False)
)

# replace ZScore = . if (sic >3999 & sic < 5000) | sic > 5999
print("Applying SIC filters...")
df = df.with_columns(
    pl.when(((pl.col('sic') > 3999) & (pl.col('sic') < 5000)) | (pl.col('sic') > 5999))
    .then(None)
    .otherwise(pl.col('ZScore'))
    .alias('ZScore')
)

print(f"Generated ZScore for {len(df)} observations")

# Keep only required columns for output
df_final = df.select(['permno', 'time_avail_m', 'ZScore'])

# SAVE
# do "$pathCode/saveplacebo" ZScore
save_placebo(df_final, 'ZScore')

print("ZScore.py completed")