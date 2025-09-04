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
import numpy as np
import sys
import os

# Add parent directory to path to import utils
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from utils.save_standardized import save_placebo

print("Starting fgr5yrNoLag.py")

# Prep IBES data
# use "$pathDataIntermediate/IBES_EPS_Unadj", replace
print("Loading IBES_EPS_Unadj...")
ibes = pd.read_parquet("../pyData/Intermediate/IBES_EPS_Unadj.parquet")

# keep if fpi == "0"
print("Filtering for fpi == 0...")
ibes = ibes[ibes['fpi'] == "0"].copy()

# rename meanest fgr5yr
ibes = ibes.rename(columns={'meanest': 'fgr5yr'})

print(f"After IBES processing: {len(ibes)} rows")

# DATA LOAD
# use permno time_avail_m ceq ib txdi dv sale ni dp using "$pathDataIntermediate/m_aCompustat", clear
print("Loading m_aCompustat...")
df = pd.read_parquet("../pyData/Intermediate/m_aCompustat.parquet")
df = df[['permno', 'time_avail_m', 'ceq', 'ib', 'txdi', 'dv', 'sale', 'ni', 'dp']].copy()

print(f"After loading m_aCompustat: {len(df)} rows")

# merge 1:1 permno time_avail_m using "$pathDataIntermediate/SignalMasterTable", keep(using match) nogenerate keepusing(tickerIBES)  
print("Loading SignalMasterTable...")
signal_df = pd.read_parquet("../pyData/Intermediate/SignalMasterTable.parquet")
signal_df = signal_df[['permno', 'time_avail_m', 'tickerIBES']].copy()

print("Merging with SignalMasterTable...")
# keep(using match) means keep observations from SignalMasterTable (using) and matched observations
# Start with m_aCompustat, then merge SignalMasterTable data where matches exist
df = df.merge(signal_df, on=['permno', 'time_avail_m'], how='inner')

print(f"After merge with SignalMasterTable: {len(df)} rows")

# merge m:1 tickerIBES time_avail_m using "$pathtemp/temp", keep(match) nogenerate keepusing(fgr5yr)
print("Merging with IBES data...")
df = df.merge(ibes[['tickerIBES', 'time_avail_m', 'fgr5yr']], 
              on=['tickerIBES', 'time_avail_m'], how='inner')

print(f"After merge with IBES: {len(df)} rows")

# SIGNAL CONSTRUCTION
# xtset permno time_avail_m
print("Sorting...")
df = df.sort_values(['permno', 'time_avail_m'])

# gen fgr5yrNoLag = fgr5yr
print("Setting fgr5yrNoLag...")
df['fgr5yrNoLag'] = df['fgr5yr']

# replace fgr5yrNoLag = . if ceq == . | ib == . | txdi == . | dv == . | sale == . | ni == . | dp == .
print("Applying missing value filters...")
# Set fgr5yrNoLag to NaN when any required variable is missing, but keep the row
required_vars = ['ceq', 'ib', 'txdi', 'dv', 'sale', 'ni', 'dp']
missing_mask = df[required_vars].isna().any(axis=1)
df.loc[missing_mask, 'fgr5yrNoLag'] = np.nan

print(f"Generated fgr5yrNoLag for {len(df)} observations")

# Keep only required columns for output
df_final = df[['permno', 'time_avail_m', 'fgr5yrNoLag']].copy()

# Convert to Polars for save_placebo
df_final_pl = pl.from_pandas(df_final)

# SAVE - use standard save_placebo function 
save_placebo(df_final_pl, 'fgr5yrNoLag')

print("fgr5yrNoLag.py completed")