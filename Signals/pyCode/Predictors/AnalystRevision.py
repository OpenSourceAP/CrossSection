# ABOUTME: AnalystRevision.py - calculates AnalystRevision predictor using IBES analyst estimates
# ABOUTME: Direct line-by-line translation from Stata Code/Predictors/AnalystRevision.do

"""
AnalystRevision.py

Usage:
    cd pyCode/
    source .venv/bin/activate
    python3 Predictors/AnalystRevision.py

Inputs:
    - IBES_EPS_Unadj.parquet: IBES earnings per share data 
    - SignalMasterTable.parquet: Monthly master table with permno, tickerIBES, time_avail_m

Outputs:
    - AnalystRevision.csv: CSV file with columns [permno, yyyymm, AnalystRevision]
    - AnalystRevision = meanest/l.meanest (1-month analyst revision)
"""

import pandas as pd
import numpy as np
from pathlib import Path
import sys
import os

# Add utils directory to path for imports
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from utils.save_standardized import save_predictor


print("Starting AnalystRevision.py...")

# Prep IBES data
print("Loading and preparing IBES data...")

# Load IBES data - equivalent to Stata: use "$pathDataIntermediate/IBES_EPS_Unadj", replace
ibes_path = Path("../pyData/Intermediate/IBES_EPS_Unadj.parquet")
if not ibes_path.exists():
    raise FileNotFoundError(f"Required input file not found: {ibes_path}")

ibes_df = pd.read_parquet(ibes_path)

# keep if fpi == "1"
ibes_df = ibes_df[ibes_df['fpi'] == "1"].copy()

# keep tickerIBES time_avail_m meanest
required_cols = ['tickerIBES', 'time_avail_m', 'meanest']
missing_cols = [col for col in required_cols if col not in ibes_df.columns]
if missing_cols:
    raise ValueError(f"Missing required columns in IBES_EPS_Unadj: {missing_cols}")

ibes_df = ibes_df[required_cols].copy()
print(f"Prepared IBES data: {ibes_df.shape[0]} rows, {ibes_df.shape[1]} columns")

# DATA LOAD
print("Loading SignalMasterTable...")

# Load SignalMasterTable - equivalent to Stata: use permno tickerIBES time_avail_m using "$pathDataIntermediate/SignalMasterTable", clear
signal_master_path = Path("../pyData/Intermediate/SignalMasterTable.parquet")
if not signal_master_path.exists():
    raise FileNotFoundError(f"Required input file not found: {signal_master_path}")

signal_master = pd.read_parquet(signal_master_path)

# Keep only the columns we need
smt_required_cols = ['permno', 'tickerIBES', 'time_avail_m']
smt_missing_cols = [col for col in smt_required_cols if col not in signal_master.columns]
if smt_missing_cols:
    raise ValueError(f"Missing required columns in SignalMasterTable: {smt_missing_cols}")

df = signal_master[smt_required_cols].copy()
print(f"Loaded SignalMasterTable: {df.shape[0]} rows, {df.shape[1]} columns")

# merge m:1 tickerIBES time_avail_m using "$pathtemp/temp", keep(master match) nogenerate
print("Merging with IBES data...")

# Merge (equivalent to keep(master match) - left join)
df = pd.merge(df, ibes_df, on=['tickerIBES', 'time_avail_m'], how='left')

print(f"After merging with IBES data: {df.shape[0]} rows")

# SIGNAL CONSTRUCTION

# xtset permno time_avail_m
print("Setting up panel data (sorting by permno, time_avail_m)...")
df = df.sort_values(['permno', 'time_avail_m'])

# gen AnalystRevision = meanest/l.meanest
print("Calculating 1-month lag and AnalystRevision...")

# Create 1-month lag using simple shift (Method 1 from StataDocs)
df['l_meanest'] = df.groupby('permno')['meanest'].shift(1)

# gen AnalystRevision = meanest/l.meanest
df['AnalystRevision'] = df['meanest'] / df['l_meanest']

print(f"Calculated AnalystRevision for {df['AnalystRevision'].notna().sum()} observations")

# SAVE
# do "$pathCode/savepredictor" AnalystRevision
save_predictor(df, 'AnalystRevision')

print("AnalystRevision.py completed successfully")