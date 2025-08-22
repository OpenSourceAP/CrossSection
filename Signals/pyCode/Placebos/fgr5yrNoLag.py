# ABOUTME: fgr5yrNoLag.py - calculates long-term EPS forecast placebo
# ABOUTME: Python equivalent of fgr5yrNoLag.do, translates line-by-line from Stata code

"""
fgr5yrNoLag.py

Inputs:
    - IBES_EPS_Unadj.parquet: permno, time_avail_m, fpi, meanest columns
    - SignalMasterTable.parquet: permno, time_avail_m, tickerIBES columns
    - m_aCompustat.parquet: permno, time_avail_m, ceq, ib, txdi, dv, sale, ni, dp columns

Outputs:
    - fgr5yrNoLag.csv: permno, yyyymm, fgr5yrNoLag columns

Usage:
    cd pyCode
    source .venv/bin/activate  
    python3 Placebos/fgr5yrNoLag.py
"""

import pandas as pd
import polars as pl
import sys
import os

# Add parent directory to path to import utils
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from utils.saveplacebo import save_placebo

print("Starting fgr5yrNoLag.py")

# Prep IBES data
# use "$pathDataIntermediate/IBES_EPS_Unadj", replace
print("Loading IBES_EPS_Unadj...")
ibes = pl.read_parquet("../pyData/Intermediate/IBES_EPS_Unadj.parquet")

# keep if fpi == "0"
print("Filtering for fpi == 0...")
ibes = ibes.filter(pl.col('fpi') == "0")

# rename meanest fgr5yr
ibes = ibes.rename({'meanest': 'fgr5yr'})

print(f"After IBES processing: {len(ibes)} rows")

# DATA LOAD
# use permno time_avail_m ceq ib txdi dv sale ni dp using "$pathDataIntermediate/m_aCompustat", clear
print("Loading m_aCompustat...")
df = pl.read_parquet("../pyData/Intermediate/m_aCompustat.parquet")
df = df.select(['permno', 'time_avail_m', 'ceq', 'ib', 'txdi', 'dv', 'sale', 'ni', 'dp'])

print(f"After loading m_aCompustat: {len(df)} rows")

# merge 1:1 permno time_avail_m using "$pathDataIntermediate/SignalMasterTable", keep(using match) nogenerate keepusing(tickerIBES)
print("Loading SignalMasterTable...")
signal_df = pl.read_parquet("../pyData/Intermediate/SignalMasterTable.parquet")
signal_df = signal_df.select(['permno', 'time_avail_m', 'tickerIBES'])

print("Merging with SignalMasterTable...")
df = df.join(signal_df, on=['permno', 'time_avail_m'], how='inner')

print(f"After merge with SignalMasterTable: {len(df)} rows")

# merge m:1 tickerIBES time_avail_m using "$pathtemp/temp", keep(match) nogenerate keepusing(fgr5yr)
print("Merging with IBES data...")
df = df.join(ibes.select(['tickerIBES', 'time_avail_m', 'fgr5yr']), 
             on=['tickerIBES', 'time_avail_m'], how='inner')

print(f"After merge with IBES: {len(df)} rows")

# SIGNAL CONSTRUCTION
# xtset permno time_avail_m
print("Sorting...")
df = df.sort(['permno', 'time_avail_m'])

# gen fgr5yrNoLag = fgr5yr
print("Setting fgr5yrNoLag...")
df = df.with_columns(pl.col('fgr5yr').alias('fgr5yrNoLag'))

# replace fgr5yrNoLag = . if ceq == . | ib == . | txdi == . | dv == . | sale == . | ni == . | dp == .
print("Applying missing value filters...")
df = df.with_columns(
    pl.when(pl.col('ceq').is_null() | pl.col('ib').is_null() | pl.col('txdi').is_null() |
            pl.col('dv').is_null() | pl.col('sale').is_null() | pl.col('ni').is_null() | pl.col('dp').is_null())
    .then(None)
    .otherwise(pl.col('fgr5yrNoLag'))
    .alias('fgr5yrNoLag')
)

print(f"Generated fgr5yrNoLag for {len(df)} observations")

# Keep only required columns for output
df_final = df.select(['permno', 'time_avail_m', 'fgr5yrNoLag'])

# SAVE
# do "$pathCode/saveplacebo" fgr5yrNoLag
save_placebo(df_final, 'fgr5yrNoLag')

print("fgr5yrNoLag.py completed")