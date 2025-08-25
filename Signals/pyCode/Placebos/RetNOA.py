# ABOUTME: RetNOA.py - calculates return on net operating assets placebo
# ABOUTME: Python equivalent of RetNOA.do, translates line-by-line from Stata code

"""
RetNOA.py

Inputs:
    - m_aCompustat.parquet: gvkey, permno, time_avail_m, at, che, ivao, dlc, dltt, mib, pstk, oiadp, ceq columns

Outputs:
    - RetNOA.csv: permno, yyyymm, RetNOA columns

Usage:
    cd pyCode
    source .venv/bin/activate  
    python3 Placebos/RetNOA.py
"""

import pandas as pd
import polars as pl
import sys
import os

# Add parent directory to path to import utils
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from utils.saveplacebo import save_placebo

print("Starting RetNOA.py")

# DATA LOAD
# use gvkey permno time_avail_m at che ivao dlc dltt mib pstk oiadp ceq using "$pathDataIntermediate/m_aCompustat", clear
print("Loading m_aCompustat...")
df = pl.read_parquet("../pyData/Intermediate/m_aCompustat.parquet")
df = df.select(['gvkey', 'permno', 'time_avail_m', 'at', 'che', 'ivao', 'dlc', 'dltt', 'mib', 'pstk', 'oiadp', 'ceq'])

print(f"Loaded data: {len(df)} rows")

# SIGNAL CONSTRUCTION
# bysort permno time_avail_m: keep if _n == 1  // deletes a few observations
print("Removing duplicates...")
df = df.unique(subset=['permno', 'time_avail_m'], maintain_order=True)

print(f"After removing duplicates: {len(df)} rows")

# Sort for lag operations
print("Sorting by permno and time...")
df = df.sort(['permno', 'time_avail_m'])

# gen tempOA = at - che - ivao
# replace tempOA = at - che if mi(ivao)
print("Computing tempOA...")
df = df.with_columns([
    pl.when(pl.col('ivao').is_not_null())
    .then(pl.col('at') - pl.col('che') - pl.col('ivao'))
    .otherwise(pl.col('at') - pl.col('che'))
    .alias('tempOA')
])

# foreach v of varlist dlc dltt mib pstk {
# gen temp`v' = `v'
# replace temp`v' = 0 if mi(`v')
# }
print("Computing temp variables with zero replacement for missing...")
df = df.with_columns([
    pl.col('dlc').fill_null(0).alias('tempdlc'),
    pl.col('dltt').fill_null(0).alias('tempdltt'), 
    pl.col('mib').fill_null(0).alias('tempmib'),
    pl.col('pstk').fill_null(0).alias('temppstk')
])

# gen tempOL = at - tempdlc - tempdltt - tempmib - temppstk - ceq
print("Computing tempOL...")
df = df.with_columns([
    (pl.col('at') - pl.col('tempdlc') - pl.col('tempdltt') - pl.col('tempmib') - pl.col('temppstk') - pl.col('ceq')).alias('tempOL')
])

# Create lags
print("Computing 12 and 24 month lags...")
df = df.with_columns([
    pl.col('oiadp').shift(12).over('permno').alias('l12_oiadp'),
    pl.col('tempOA').shift(24).over('permno').alias('l24_tempOA'),
    pl.col('tempOL').shift(24).over('permno').alias('l24_tempOL')
])

# gen RetNOA = l12.oiadp/(l24.tempOA - l24.tempOL)
print("Computing RetNOA...")
df = df.with_columns([
    (pl.col('l12_oiadp') / (pl.col('l24_tempOA') - pl.col('l24_tempOL'))).alias('RetNOA')
])

print(f"Generated RetNOA for {len(df)} observations")

# Keep only required columns
df_final = df.select(['permno', 'time_avail_m', 'RetNOA'])

# SAVE
# do "$pathCode/saveplacebo" RetNOA
save_placebo(df_final, 'RetNOA')

print("RetNOA.py completed")