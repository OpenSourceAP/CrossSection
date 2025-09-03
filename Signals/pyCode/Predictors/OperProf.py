#%%
# debug
import os
os.chdir(os.path.join(os.path.dirname(__file__), '..'))

# ABOUTME: Operating profitability following Fama and French 2006, Table 3 Y_t/B_t
# ABOUTME: calculates operating profits scaled by book equity, excluding smallest size tercile

"""
Usage:
    python3 Predictors/OperProf.py

Inputs:
    - SignalMasterTable.parquet: Monthly master table with mve_c for size filtering
    - m_aCompustat.parquet: Monthly Compustat data with revt, cogs, xsga, xint, ceq

Outputs:
    - OperProf.csv: CSV file with columns [permno, yyyymm, OperProf]
    - OperProf = (revt - cogs - xsga - xint) / ceq, excluding smallest size tercile
"""

# Notes:
# Excludes smallest size tercile to simulate NYSE size breakpoints
# This approach follows Fama-French methodology which overweights large cap stocks
# Operating profitability = (revenue - cogs - sga - interest) / equity
# Removing SGA expenses significantly improves signal strength (similar to Novy-Marx)

import pandas as pd
import numpy as np
import sys
sys.path.insert(0, '.')

#%%

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
with np.errstate(over='ignore', invalid='ignore'):
    df['tempprof'] = (df['revt'] - df['cogs'] - df['xsga'] - df['xint']) / df['ceq']


# Create size terciles by time_avail_m and exclude smallest tercile
df['tempsizeq'] = (
    df.groupby('time_avail_m')['mve_c']
    .transform(lambda x: pd.qcut(x, q=3, labels=False, duplicates='drop') + 1)
)

# Set tempprof to missing for smallest size tercile
df.loc[df['tempsizeq'] == 1, 'tempprof'] = pd.NA

#%%

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

