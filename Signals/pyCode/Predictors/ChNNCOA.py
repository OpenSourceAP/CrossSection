# ABOUTME: ChNNCOA.py - calculates change in net noncurrent operating assets predictor
# ABOUTME: Line-by-line translation of ChNNCOA.do following CLAUDE.md translation philosophy

"""
ChNNCOA.py

Usage:
    cd pyCode/
    source .venv/bin/activate
    python3 Predictors/ChNNCOA.py

Inputs:
    - ../pyData/Intermediate/m_aCompustat.parquet (columns: gvkey, permno, time_avail_m, at, act, ivao, lt, dlc, dltt)

Outputs:
    - ../pyData/Predictors/ChNNCOA.csv (columns: permno, yyyymm, ChNNCOA)
"""

import pandas as pd
import numpy as np
from pathlib import Path

# DATA LOAD
# use gvkey permno time_avail_m at act ivao lt dlc dltt using "$pathDataIntermediate/m_aCompustat", clear
df = pd.read_parquet('../pyData/Intermediate/m_aCompustat.parquet', 
                     columns=['gvkey', 'permno', 'time_avail_m', 'at', 'act', 'ivao', 'lt', 'dlc', 'dltt'])

# SIGNAL CONSTRUCTION
# bysort permno time_avail_m: keep if _n == 1  // deletes a few observations
df = df.drop_duplicates(subset=['permno', 'time_avail_m'], keep='first').copy()

# xtset permno time_avail_m
df = df.sort_values(['permno', 'time_avail_m']).reset_index(drop=True)

# gen temp = ( (at - act - ivao)  - (lt - dlc - dltt) )/at
df['temp'] = ((df['at'] - df['act'] - df['ivao']) - (df['lt'] - df['dlc'] - df['dltt'])) / df['at']

# gen ChNNCOA = temp - l12.temp
df['temp_l12'] = df.groupby('permno')['temp'].shift(12)
df['ChNNCOA'] = df['temp'] - df['temp_l12']

# drop temp*
df = df.drop(columns=['temp', 'temp_l12'])

# Keep only needed columns and non-missing values
result = df[['permno', 'time_avail_m', 'ChNNCOA']].copy()
result = result.dropna(subset=['ChNNCOA']).copy()

# Convert time_avail_m to yyyymm
result['yyyymm'] = result['time_avail_m'].dt.year * 100 + result['time_avail_m'].dt.month

# Prepare final output
final_result = result[['permno', 'yyyymm', 'ChNNCOA']].copy()

# SAVE
Path('../pyData/Predictors').mkdir(parents=True, exist_ok=True)
final_result.to_csv('../pyData/Predictors/ChNNCOA.csv', index=False)

print(f"ChNNCOA predictor saved: {len(final_result)} observations")