# ABOUTME: OperProf.py - calculates operating profitability predictor
# ABOUTME: Operating profitability excluding small-cap stocks with size filtering

"""
OperProf predictor calculation

Usage:
    cd pyCode/
    source .venv/bin/activate
    python3 Predictors/OperProf.py

Inputs:
    - ../pyData/Intermediate/SignalMasterTable.parquet (permno, time_avail_m, mve_c, gvkey)
    - ../pyData/Intermediate/m_aCompustat.parquet (gvkey, time_avail_m, revt, cogs, xsga, xint, ceq)

Outputs:
    - ../pyData/Predictors/OperProf.csv (permno, yyyymm, OperProf)
"""

import pandas as pd
import numpy as np
import sys
sys.path.insert(0, '.')
from utils.stata_fastxtile import fastxtile

# DATA LOAD
signal_master = pd.read_parquet("../pyData/Intermediate/SignalMasterTable.parquet", 
                               columns=['permno', 'gvkey', 'time_avail_m', 'mve_c'])

# Drop observations with missing gvkey
df = signal_master.dropna(subset=['gvkey']).copy()

# Merge with Compustat data
compustat = pd.read_parquet("../pyData/Intermediate/m_aCompustat.parquet", 
                           columns=['gvkey', 'time_avail_m', 'revt', 'cogs', 'xsga', 'xint', 'ceq'])

df = pd.merge(df, compustat, on=['gvkey', 'time_avail_m'], how='inner')

# SIGNAL CONSTRUCTION
# Calculate temporary profitability (handle missing values like Stata)
# In Stata, missing values in arithmetic operations are often treated as 0
df['xsga'] = df['xsga'].fillna(0)
df['tempprof'] = (df['revt'] - df['cogs'] - df['xsga'] - df['xint']) / df['ceq']

# Create size terciles by time_avail_m and exclude smallest tercile
df['tempsizeq'] = fastxtile(df, 'mve_c', by='time_avail_m', n=3)

# Set tempprof to missing for smallest size tercile
df.loc[df['tempsizeq'] == 1, 'tempprof'] = pd.NA

# Assign to OperProf
df['OperProf'] = df['tempprof']

# Drop missing values
df = df.dropna(subset=['OperProf'])

# Convert time_avail_m to yyyymm
df['yyyymm'] = df['time_avail_m'].dt.year * 100 + df['time_avail_m'].dt.month

# Keep required columns and order
df = df[['permno', 'yyyymm', 'OperProf']].copy()

# SAVE
df.to_csv("../pyData/Predictors/OperProf.csv", index=False)
print(f"OperProf: Saved {len(df):,} observations")