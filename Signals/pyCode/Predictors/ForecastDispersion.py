# ABOUTME: ForecastDispersion.py - calculates ForecastDispersion predictor using IBES analyst forecast dispersion
# ABOUTME: Direct line-by-line translation from Stata Code/Predictors/ForecastDispersion.do

"""
ForecastDispersion.py

Usage:
    cd pyCode/
    source .venv/bin/activate
    python3 Predictors/ForecastDispersion.py

Inputs:
    - IBES_EPS_Unadj.parquet: IBES earnings per share data 
    - SignalMasterTable.parquet: Monthly master table with permno, tickerIBES, time_avail_m

Outputs:
    - ForecastDispersion.csv: CSV file with columns [permno, yyyymm, ForecastDispersion]
    - ForecastDispersion = stdev/abs(meanest) (EPS forecast dispersion)
"""

import pandas as pd
import numpy as np
from pathlib import Path
import sys
import os

# Add utils directory to path for imports
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from utils.save_standardized import save_predictor


print("Starting ForecastDispersion.py...")

# Prep IBES data
print("Loading and preparing IBES data...")

# Load IBES data - equivalent to Stata: use "$pathDataIntermediate/IBES_EPS_Unadj", replace
ibes_path = Path("../pyData/Intermediate/IBES_EPS_Unadj.parquet")
if not ibes_path.exists():
    raise FileNotFoundError(f"Required input file not found: {ibes_path}")

ibes_df = pd.read_parquet(ibes_path)

# keep if fpi == "1"
ibes_df = ibes_df[ibes_df['fpi'] == "1"].copy()

# keep if fpedats != . // & fpedats > statpers + 30 //
# In Python, != . means not null/NaN
ibes_df = ibes_df[ibes_df['fpedats'].notna()].copy()

print(f"Prepared IBES data: {ibes_df.shape[0]} rows, {ibes_df.shape[1]} columns")

# DATA LOAD
print("Loading SignalMasterTable...")

# Load SignalMasterTable - equivalent to Stata: use permno time_avail_m tickerIBES using "$pathDataIntermediate/SignalMasterTable", clear
signal_master_path = Path("../pyData/Intermediate/SignalMasterTable.parquet")
if not signal_master_path.exists():
    raise FileNotFoundError(f"Required input file not found: {signal_master_path}")

signal_master = pd.read_parquet(signal_master_path)

# Keep only the columns we need
smt_required_cols = ['permno', 'time_avail_m', 'tickerIBES']
smt_missing_cols = [col for col in smt_required_cols if col not in signal_master.columns]
if smt_missing_cols:
    raise ValueError(f"Missing required columns in SignalMasterTable: {smt_missing_cols}")

df = signal_master[smt_required_cols].copy()
print(f"Loaded SignalMasterTable: {df.shape[0]} rows, {df.shape[1]} columns")

# merge m:1 tickerIBES time_avail_m using "$pathtemp/temp", keep(master match) nogenerate keepusing(stdev meanest)
print("Merging with IBES data...")

# Check required columns for merge
ibes_required_cols = ['tickerIBES', 'time_avail_m', 'stdev', 'meanest']
ibes_missing_cols = [col for col in ibes_required_cols if col not in ibes_df.columns]
if ibes_missing_cols:
    raise ValueError(f"Missing required columns in IBES_EPS_Unadj: {ibes_missing_cols}")

# Keep only the columns we need from IBES (equivalent to keepusing)
ibes_merge = ibes_df[ibes_required_cols].copy()

# Merge (equivalent to keep(master match) - left join)
df = pd.merge(df, ibes_merge, on=['tickerIBES', 'time_avail_m'], how='left')

print(f"After merging with IBES data: {df.shape[0]} rows")

# SIGNAL CONSTRUCTION
print("Calculating ForecastDispersion...")

# gen ForecastDispersion = stdev/abs(meanest)
df['ForecastDispersion'] = df['stdev'] / np.abs(df['meanest'])

print(f"Calculated ForecastDispersion for {df['ForecastDispersion'].notna().sum()} observations")

# SAVE
# do "$pathCode/savepredictor" ForecastDispersion
save_predictor(df, 'ForecastDispersion')

print("ForecastDispersion.py completed successfully")