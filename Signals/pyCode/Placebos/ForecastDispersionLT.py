# ABOUTME: ForecastDispersionLT.py - calculates long-term EPS forecast dispersion placebo
# ABOUTME: Python equivalent of ForecastDispersionLT.do, translates line-by-line from Stata code

"""
ForecastDispersionLT.py

Inputs:
    - IBES_EPS_Unadj.parquet: tickerIBES, time_avail_m, fpi, stdev, numest columns
    - SignalMasterTable.parquet: permno, time_avail_m, tickerIBES columns

Outputs:
    - ForecastDispersionLT.csv: permno, yyyymm, ForecastDispersionLT columns

Usage:
    cd pyCode
    source .venv/bin/activate  
    python3 Placebos/ForecastDispersionLT.py
"""

import pandas as pd
import polars as pl
import sys
import os

# Add parent directory to path to import utils
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from utils.saveplacebo import save_placebo

print("Starting ForecastDispersionLT.py")

# // Prep IBES data
# use "$pathDataIntermediate/IBES_EPS_Unadj", replace
# keep if fpi == "0" 
print("Loading and filtering IBES_EPS_Unadj...")
ibes = pl.read_parquet("../pyData/Intermediate/IBES_EPS_Unadj.parquet")
ibes = ibes.filter(pl.col('fpi') == "0")
ibes = ibes.select(['tickerIBES', 'time_avail_m', 'stdev', 'numest'])

print(f"After filtering IBES for fpi == '0': {len(ibes)} rows")

# DATA LOAD
# use permno time_avail_m tickerIBES using "$pathDataIntermediate/SignalMasterTable", clear
print("Loading SignalMasterTable...")
df = pl.read_parquet("../pyData/Intermediate/SignalMasterTable.parquet")
df = df.select(['permno', 'time_avail_m', 'tickerIBES'])

print(f"Loaded SignalMasterTable: {len(df)} rows")

# merge m:1 tickerIBES time_avail_m using "$pathtemp/temp", keep(master match) nogenerate keepusing(stdev numest)
print("Merging with IBES data...")
df = df.join(ibes, on=['tickerIBES', 'time_avail_m'], how='left')

print(f"After merge: {len(df)} rows")

# SIGNAL CONSTRUCTION
# gen ForecastDispersionLT = stdev if numest > 1 & !mi(numest)
print("Computing ForecastDispersionLT...")
df = df.with_columns([
    pl.when((pl.col('numest') > 1) & pl.col('numest').is_not_null())
    .then(pl.col('stdev'))
    .otherwise(None)
    .alias('ForecastDispersionLT')
])

print(f"Generated ForecastDispersionLT for {len(df)} observations")

# Keep only required columns
df_final = df.select(['permno', 'time_avail_m', 'ForecastDispersionLT'])

# SAVE
# do "$pathCode/saveplacebo" ForecastDispersionLT
save_placebo(df_final, 'ForecastDispersionLT')

print("ForecastDispersionLT.py completed")