# ABOUTME: nanalyst.py - calculates number of analysts placebo
# ABOUTME: Python equivalent of nanalyst.do, translates line-by-line from Stata code

"""
nanalyst.py

Inputs:
    - IBES_EPS_Unadj.parquet: permno, time_avail_m, fpi, numest columns
    - SignalMasterTable.parquet: permno, time_avail_m, tickerIBES columns

Outputs:
    - nanalyst.csv: permno, yyyymm, nanalyst columns

Usage:
    cd pyCode
    source .venv/bin/activate  
    python3 Placebos/nanalyst.py
"""

import pandas as pd
import polars as pl
import sys
import os

# Add parent directory to path to import utils
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from utils.saveplacebo import save_placebo

print("Starting nanalyst.py")

# Prep IBES data
# use "$pathDataIntermediate/IBES_EPS_Unadj", replace
print("Loading IBES_EPS_Unadj...")
ibes = pl.read_parquet("../pyData/Intermediate/IBES_EPS_Unadj.parquet")

# keep if fpi == "1"
print("Filtering for fpi == 1...")
ibes = ibes.filter(pl.col('fpi') == "1")

print(f"After IBES processing: {len(ibes)} rows")

# DATA LOAD
# use permno time_avail_m tickerIBES using "$pathDataIntermediate/SignalMasterTable", clear
print("Loading SignalMasterTable...")
df = pl.read_parquet("../pyData/Intermediate/SignalMasterTable.parquet")
df = df.select(['permno', 'time_avail_m', 'tickerIBES'])

print(f"After loading SignalMasterTable: {len(df)} rows")

# merge m:1 tickerIBES time_avail_m using "$pathtemp/temp", keep(master match) nogenerate keepusing(numest)
print("Merging with IBES data...")
df = df.join(ibes.select(['tickerIBES', 'time_avail_m', 'numest']), 
             on=['tickerIBES', 'time_avail_m'], how='left')

print(f"After merge with IBES: {len(df)} rows")

# SIGNAL CONSTRUCTION
# gen nanalyst = numest
print("Setting nanalyst...")
df = df.with_columns(pl.col('numest').alias('nanalyst'))

# replace nanalyst = 0 if yofd(dofm(time_avail_m)) >=1989 & mi(nanalyst)
print("Applying 1989+ missing value replacement...")
df = df.with_columns(
    pl.when((pl.col('time_avail_m').dt.year() >= 1989) & pl.col('nanalyst').is_null())
    .then(0)
    .otherwise(pl.col('nanalyst'))
    .alias('nanalyst')
)

print(f"Generated nanalyst for {len(df)} observations")

# Keep only required columns for output  
# IMPORTANT: Do NOT drop null nanalyst values - keep all observations like Stata
df_final = df.select(['permno', 'time_avail_m', 'nanalyst'])

print(f"Final observations before save: {len(df_final)}")
print(f"Non-null nanalyst values: {df_final.filter(pl.col('nanalyst').is_not_null()).shape[0]}")
print(f"Null nanalyst values: {df_final.filter(pl.col('nanalyst').is_null()).shape[0]}")

# SAVE
# SPECIAL HANDLING: Unlike other placebos, nanalyst keeps null values for pre-1989 observations
# Cannot use save_placebo() which drops nulls - do manual save like Stata
print("Manual save to preserve null values for pre-1989 observations...")

# Convert to CSV format manually (replicating save_placebo logic but keeping nulls)
df_save = df_final.with_columns(
    (pl.col("time_avail_m").dt.year() * 100 + pl.col("time_avail_m").dt.month()).alias("yyyymm")
)

# Keep only required columns: permno yyyymm nanalyst (including nulls!)
df_save = df_save.select(['permno', 'yyyymm', 'nanalyst'])

# Save as CSV
import os
os.makedirs("../pyData/Placebos", exist_ok=True)
df_save.write_csv("../pyData/Placebos/nanalyst.csv")

print(f"Saved {len(df_save)} rows to ../pyData/Placebos/nanalyst.csv (including nulls)")

print("nanalyst.py completed")