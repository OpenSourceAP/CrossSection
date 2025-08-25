# ABOUTME: ZZ1_EarningsPersistence_EarningsPredictability.py - calculates earnings persistence and predictability placebos
# ABOUTME: Python equivalent of ZZ1_EarningsPersistence_EarningsPredictability.do, translates line-by-line from Stata code

"""
ZZ1_EarningsPersistence_EarningsPredictability.py

Inputs:
    - a_aCompustat.parquet: gvkey, permno, time_avail_m, fyear, datadate, epspx, ajex columns

Outputs:
    - EarningsPersistence.csv: permno, yyyymm, EarningsPersistence columns
    - EarningsPredictability.csv: permno, yyyymm, EarningsPredictability columns

Usage:
    cd pyCode
    source .venv/bin/activate  
    python3 Placebos/ZZ1_EarningsPersistence_EarningsPredictability.py
"""

import pandas as pd
import polars as pl
import numpy as np
import sys
import os

# Add parent directory to path to import utils
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from utils.saveplacebo import save_placebo
from utils.asreg import asreg

print("Starting ZZ1_EarningsPersistence_EarningsPredictability.py")

# DATA LOAD
# use gvkey permno time_avail_m fyear datadate epspx ajex using "$pathDataIntermediate/a_aCompustat", clear
print("Loading a_aCompustat...")
df = pl.read_parquet("../pyData/Intermediate/a_aCompustat.parquet")
df = df.select(['gvkey', 'permno', 'time_avail_m', 'fyear', 'datadate', 'epspx', 'ajex'])

print(f"Loaded data: {len(df)} rows")

# SIGNAL CONSTRUCTION
# xtset gvkey fyear
print("Sorting by gvkey and fyear...")
df = df.sort(['gvkey', 'fyear'])

# gen temp = epspx/ajex
# gen tempLag = l.temp
print("Computing adjusted EPS and its lag...")
df = df.with_columns([
    (pl.col('epspx') / pl.col('ajex')).alias('temp')
])

df = df.with_columns([
    pl.col('temp').shift(1).over('gvkey').alias('tempLag')
])

# asreg temp tempLag, window(fyear 10) min(10) by(gvkey) fitted rmse
print("Running 10-year rolling earnings persistence regressions...")
df_regression = asreg(
    df, 
    y="temp", 
    X=["tempLag"], 
    by=["gvkey"], 
    t="fyear", 
    mode="rolling", 
    window_size=10, 
    min_samples=10,
    outputs=["coef", "rmse"]
)

# rename _b_tempLag EarningsPersistence
# gen EarningsPredictability = _rmse^2
print("Computing EarningsPersistence and EarningsPredictability...")
df_regression = df_regression.with_columns([
    pl.col('b_tempLag').alias('EarningsPersistence'),  # asreg uses b_ prefix by default
    (pl.col('rmse') ** 2).alias('EarningsPredictability')
])

# Keep only required columns for the expansion
df_annual = df_regression.select(['gvkey', 'permno', 'time_avail_m', 'fyear', 'datadate', 'EarningsPersistence', 'EarningsPredictability'])

print(f"After regression: {len(df_annual)} rows")

# * Expand to monthly
# gen temp = 12
# expand temp
print("Expanding to monthly data...")

# Convert to pandas for easier expansion
df_pandas = df_annual.to_pandas()

# Expand each row to 12 months
expanded_data = []
for _, row in df_pandas.iterrows():
    if pd.notna(row['time_avail_m']):
        base_date = row['time_avail_m']
        for month_offset in range(12):
            new_row = row.copy()
            new_date = base_date + pd.DateOffset(months=month_offset)
            new_row['time_avail_m'] = new_date
            expanded_data.append(new_row)

if expanded_data:
    df_expanded = pd.DataFrame(expanded_data)
    
    # bysort gvkey time_avail_m (datadate): keep if _n == _N
    # Keep the latest datadate for each gvkey-time combination
    df_expanded = df_expanded.sort_values(['gvkey', 'time_avail_m', 'datadate'])
    df_expanded = df_expanded.groupby(['gvkey', 'time_avail_m']).tail(1)
    
    # bysort permno time_avail_m: keep if _n == 1  // deletes a few observations
    df_expanded = df_expanded.drop_duplicates(subset=['permno', 'time_avail_m'], keep='first')
    
    print(f"After monthly expansion: {len(df_expanded)} observations")
    
    # Convert back to polars for saving
    df_final = pl.from_pandas(df_expanded[['permno', 'time_avail_m', 'EarningsPersistence', 'EarningsPredictability']])
    
    # Split into two datasets for separate saves
    df_persistence = df_final.select(['permno', 'time_avail_m', 'EarningsPersistence'])
    df_predictability = df_final.select(['permno', 'time_avail_m', 'EarningsPredictability'])
    
    # SAVE
    # do "$pathCode/saveplacebo" EarningsPersistence
    save_placebo(df_persistence, 'EarningsPersistence')
    
    # do "$pathCode/saveplacebo" EarningsPredictability
    save_placebo(df_predictability, 'EarningsPredictability')
    
    print(f"Generated {len(df_persistence)} EarningsPersistence observations")
    print(f"Generated {len(df_predictability)} EarningsPredictability observations")
else:
    print("No valid data for expansion")

print("ZZ1_EarningsPersistence_EarningsPredictability.py completed")