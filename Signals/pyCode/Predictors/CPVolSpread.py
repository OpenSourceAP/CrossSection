# ABOUTME: CPVolSpread.py - calculates CPVolSpread predictor using option implied volatility spread
# ABOUTME: Direct line-by-line translation from Stata Code/Predictors/CPVolSpread.do

"""
CPVolSpread.py

Usage:
    cd pyCode/
    source .venv/bin/activate
    python3 Predictors/CPVolSpread.py

Inputs:
    - OptionMetricsBH.parquet: Option metrics data with implied volatility by call/put flag
    - SignalMasterTable.parquet: Monthly master table with permno, time_avail_m, secid, sicCRSP

Outputs:
    - CPVolSpread.csv: CSV file with columns [permno, yyyymm, CPVolSpread]
    - CPVolSpread = mean_imp_volC - mean_imp_volP (Call-Put volatility spread)
    - Implements Bali-Hovak (2009) panel B methodology
"""

import pandas as pd
import numpy as np
from pathlib import Path
import sys
import os

# Add utils directory to path for imports
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from utils.save_standardized import save_predictor


print("Starting CPVolSpread.py...")

# Clean OptionMetrics data 
print("Loading and cleaning OptionMetrics data...")

# Load OptionMetrics data - equivalent to Stata: use "$pathDataIntermediate/OptionMetricsBH", clear
option_metrics_path = Path("../pyData/Intermediate/OptionMetricsBH.parquet")
if not option_metrics_path.exists():
    raise FileNotFoundError(f"Required input file not found: {option_metrics_path}")

options_df = pd.read_parquet(option_metrics_path)

# drop if cp_flag == "BOTH" 
options_df = options_df[options_df['cp_flag'] != "BOTH"].copy()

# keep if mean_day >= 0 // OP doesn't mention this, but seems we may not want stale data
options_df = options_df[options_df['mean_day'] >= 0].copy()

print(f"Cleaned OptionMetrics data: {options_df.shape[0]} rows, {options_df.shape[1]} columns")

# * make wide
# drop mean_day nobs ticker
options_df = options_df.drop(columns=['mean_day', 'nobs', 'ticker'])

# reshape wide mean_imp_vol, i(secid time_avail_m) j(cp_flag) string
options_wide = options_df.pivot(index=['secid', 'time_avail_m'], columns='cp_flag', values='mean_imp_vol')
options_wide.columns = [f'mean_imp_vol{col}' for col in options_wide.columns]
options_wide = options_wide.reset_index()

# * compute vol spread
# gen CPVolSpread = mean_imp_volC - mean_imp_volP
options_wide['CPVolSpread'] = options_wide['mean_imp_volC'] - options_wide['mean_imp_volP']

print(f"Computed CPVolSpread for {options_wide['CPVolSpread'].notna().sum()} observations")

# DATA LOAD
print("Loading SignalMasterTable...")

# Load SignalMasterTable - equivalent to Stata: use permno time_avail_m secid sicCRSP using "$pathDataIntermediate/SignalMasterTable", clear
signal_master_path = Path("../pyData/Intermediate/SignalMasterTable.parquet")
if not signal_master_path.exists():
    raise FileNotFoundError(f"Required input file not found: {signal_master_path}")

signal_master = pd.read_parquet(signal_master_path)

# Keep only the columns we need
required_cols = ['permno', 'time_avail_m', 'secid', 'sicCRSP']
missing_cols = [col for col in required_cols if col not in signal_master.columns]
if missing_cols:
    raise ValueError(f"Missing required columns in SignalMasterTable: {missing_cols}")

df = signal_master[required_cols].copy()

# * Add secid-based data (many to one match due to permno-secid not being unique in crsp)
# drop if mi(secid)
df = df.dropna(subset=['secid'])

# merge m:1 secid time_avail_m using "$pathtemp/temp", keep(master match) nogenerate
df = pd.merge(df, options_wide, on=['secid', 'time_avail_m'], how='left')

print(f"After merging with options data: {df.shape[0]} rows")

# * drop closed-end funds (6720 : 6730) and REITs (6798)
# keep if (sicCRSP < 6720 | sicCRSP > 6730)
df = df[(df['sicCRSP'] < 6720) | (df['sicCRSP'] > 6730)]

# keep if sicCRSP != 6798
df = df[df['sicCRSP'] != 6798]

print(f"After filtering closed-end funds and REITs: {df.shape[0]} rows")

# SIGNAL CONSTRUCTION

# drop if CPVolSpread == .
df = df.dropna(subset=['CPVolSpread'])

print(f"Final CPVolSpread for {df.shape[0]} observations")

# SAVE
# do "$pathCode/savepredictor" CPVolSpread
save_predictor(df, 'CPVolSpread')

print("CPVolSpread.py completed successfully")