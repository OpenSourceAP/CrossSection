# ABOUTME: ChInv.py - calculates change in inventory predictor
# ABOUTME: Line-by-line translation of ChInv.do following CLAUDE.md translation philosophy

"""
ChInv.py

Usage:
    cd pyCode/
    source .venv/bin/activate
    python3 Predictors/ChInv.py

Inputs:
    - ../pyData/Intermediate/m_aCompustat.parquet (columns: gvkey, permno, time_avail_m, at, invt)

Outputs:
    - ../pyData/Predictors/ChInv.csv (columns: permno, yyyymm, ChInv)
"""

import pandas as pd
import numpy as np
from pathlib import Path

# DATA LOAD
# use gvkey permno time_avail_m at invt using "$pathDataIntermediate/m_aCompustat", clear
df = pd.read_parquet('../pyData/Intermediate/m_aCompustat.parquet', 
                     columns=['gvkey', 'permno', 'time_avail_m', 'at', 'invt'])

# SIGNAL CONSTRUCTION
# bysort permno time_avail_m: keep if _n == 1  // deletes a few observations
df = df.drop_duplicates(subset=['permno', 'time_avail_m'], keep='first').copy()

# xtset permno time_avail_m
df = df.sort_values(['permno', 'time_avail_m']).reset_index(drop=True)

# gen ChInv = (invt-l12.invt)/((at+l12.at)/2)
df['invt_l12'] = df.groupby('permno')['invt'].shift(12)
df['at_l12'] = df.groupby('permno')['at'].shift(12)
df['ChInv'] = (df['invt'] - df['invt_l12']) / ((df['at'] + df['at_l12']) / 2)

# Keep only needed columns and non-missing values
result = df[['permno', 'time_avail_m', 'ChInv']].copy()
result = result.dropna(subset=['ChInv']).copy()

# Convert time_avail_m to yyyymm
result['yyyymm'] = result['time_avail_m'].dt.year * 100 + result['time_avail_m'].dt.month

# Prepare final output
final_result = result[['permno', 'yyyymm', 'ChInv']].copy()

# SAVE
Path('../pyData/Predictors').mkdir(parents=True, exist_ok=True)
final_result.to_csv('../pyData/Predictors/ChInv.csv', index=False)

print(f"ChInv predictor saved: {len(final_result)} observations")