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
# Load accounting data from Compustat
df = pd.read_parquet('../pyData/Intermediate/m_aCompustat.parquet', 
                     columns=['gvkey', 'permno', 'time_avail_m', 'at', 'act', 'ivao', 'lt', 'dlc', 'dltt'])

# SIGNAL CONSTRUCTION
# Remove duplicate observations for same company-month
df = df.drop_duplicates(subset=['permno', 'time_avail_m'], keep='first').copy()

# Sort by company and time to enable lag calculations
df = df.sort_values(['permno', 'time_avail_m']).reset_index(drop=True)

# Calculate net noncurrent operating assets as proportion of total assets
# NNCOA = (Total Assets - Current Assets - Investment in Unconsolidated Subsidiaries) - (Total Liabilities - Current Debt - Long-term Debt)
df['temp'] = ((df['at'] - df['act'] - df['ivao']) - (df['lt'] - df['dlc'] - df['dltt'])) / df['at']

# Calculate 12-month change in net noncurrent operating assets
df['temp_l12'] = df.groupby('permno')['temp'].shift(12)
df['ChNNCOA'] = df['temp'] - df['temp_l12']

# Clean up temporary columns
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