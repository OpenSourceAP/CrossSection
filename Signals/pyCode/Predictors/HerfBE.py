# ABOUTME: Industry concentration (equity) following Hou and Robinson 2006, Table 2, H(Equity)
# ABOUTME: calculates three-year rolling average of Herfindahl index based on firm book equity
"""
Usage:
    python3 Predictors/HerfBE.py

Inputs:
    - m_aCompustat.parquet: Monthly Compustat data with columns [permno, time_avail_m, txditc, pstk, pstkrv, pstkl, seq, ceq, at, lt]
    - SignalMasterTable.parquet: Monthly master table with sicCRSP, shrcd

Outputs:
    - HerfBE.csv: CSV file with columns [permno, yyyymm, HerfBE]
    - HerfBE = 3-year rolling average of industry Herfindahl index based on book equity, excludes regulated industries
"""

import pandas as pd
import numpy as np
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from utils.asrol import asrol

# DATA LOAD
df = pd.read_parquet('../pyData/Intermediate/m_aCompustat.parquet')
df = df[['permno', 'time_avail_m', 'txditc', 'pstk', 'pstkrv', 'pstkl', 'seq', 'ceq', 'at', 'lt']].copy()

# Drop duplicates
df = df.drop_duplicates(subset=['permno', 'time_avail_m'])

# Merge with SignalMasterTable
smt = pd.read_parquet('../pyData/Intermediate/SignalMasterTable.parquet')
smt = smt[['permno', 'time_avail_m', 'sicCRSP', 'shrcd']].copy()

df = df.merge(smt, on=['permno', 'time_avail_m'], how='inner')

# Sort for lag operations
df = df.sort_values(['permno', 'time_avail_m'])

# SIGNAL CONSTRUCTION
# Create 4-digit SIC code
df['tempSIC'] = df['sicCRSP'].astype(str)
df['sic3D'] = df['tempSIC'].str[:4]

# Compute book equity
df['txditc'] = df['txditc'].fillna(0)

# Calculate preferred stock
df['tempPS'] = df['pstk']
df['tempPS'] = df['tempPS'].fillna(df['pstkrv'])
df['tempPS'] = df['tempPS'].fillna(df['pstkl'])

# Calculate stockholders equity
df['tempSE'] = df['seq']
df['tempSE'] = df['tempSE'].fillna(df['ceq'] + df['tempPS'])
df['tempSE'] = df['tempSE'].fillna(df['at'] - df['lt'])

# Calculate book equity
df['tempBE'] = df['tempSE'] + df['txditc'] - df['tempPS']

# Calculate industry book equity by SIC and month
df['indequity'] = df.groupby(['sic3D', 'time_avail_m'])['tempBE'].transform('sum')

# Calculate firm's book equity share squared
df['temp'] = (df['tempBE'] / df['indequity']) ** 2

# Calculate Herfindahl index by industry-month
df['tempHerf'] = df.groupby(['sic3D', 'time_avail_m'])['temp'].transform('sum')

# Take 3-year moving average using asrol
df = asrol(df, 'permno', 'time_avail_m', '1mo', 36, 'tempHerf', 'mean', 'mean36_tempHerf', min_samples=12)
df = df.rename(columns={'mean36_tempHerf': 'HerfBE'})

# Set to missing if not common stock
df.loc[df['shrcd'] > 11, 'HerfBE'] = np.nan

# Missing if regulated industry (Barclay and Smith 1995 definition)
df['year'] = df['time_avail_m'].dt.year

# Regulated industries before deregulation dates
df.loc[(df['tempSIC'].isin(['4011', '4210', '4213'])) & (df['year'] <= 1980), 'HerfBE'] = np.nan
df.loc[(df['tempSIC'] == '4512') & (df['year'] <= 1978), 'HerfBE'] = np.nan
df.loc[(df['tempSIC'].isin(['4812', '4813'])) & (df['year'] <= 1982), 'HerfBE'] = np.nan
df.loc[df['tempSIC'].str[:2] == '49', 'HerfBE'] = np.nan

# Keep only necessary columns for output
df_final = df[['permno', 'time_avail_m', 'HerfBE']].copy()
df_final = df_final.dropna(subset=['HerfBE'])

# Convert time_avail_m to yyyymm format like other predictors
df_final['yyyymm'] = df_final['time_avail_m'].dt.year * 100 + df_final['time_avail_m'].dt.month

# Convert to integers for consistency with other predictors
df_final['permno'] = df_final['permno'].astype('int64')
df_final['yyyymm'] = df_final['yyyymm'].astype('int64')

# Keep only required columns and set index
df_final = df_final[['permno', 'yyyymm', 'HerfBE']].copy()
df_final = df_final.set_index(['permno', 'yyyymm'])

# SAVE
df_final.to_csv('../pyData/Predictors/HerfBE.csv')

print("HerfBE predictor saved successfully")