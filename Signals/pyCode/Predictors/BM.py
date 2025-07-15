# ABOUTME: Translates BM.do predictor to create Book-to-market ratio based on Stattman (1980)
# ABOUTME: Run from pyCode/ directory: python3 Predictors/BM.py

# BM based on the original, Dennis Stattman (1980)
# see https://github.com/OpenSourceAP/CrossSection/issues/126

import pandas as pd
import numpy as np

# DATA LOAD
# Load m_aCompustat data
m_compustat = pd.read_parquet('../pyData/Intermediate/m_aCompustat.parquet')
m_compustat = m_compustat[['permno', 'time_avail_m', 'datadate', 'ceqt']].copy()

# Load SignalMasterTable
signal_master = pd.read_parquet('../pyData/Intermediate/SignalMasterTable.parquet')
signal_master = signal_master[['permno', 'time_avail_m', 'mve_c']].copy()

# Merge 1:1 permno time_avail_m, keep using match
df = pd.merge(m_compustat, signal_master, on=['permno', 'time_avail_m'], how='inner')

# find the market equity that matches datadate (based on 6 month lag)
# (see "Company Data" section)

# Sort by permno and time_avail_m for proper lagging
df = df.sort_values(['permno', 'time_avail_m'])

# Create 6-month lag of mve_c
df['me_datadate'] = df.groupby('permno')['mve_c'].shift(6)

# Replace me_datadate with missing if l6.time_avail_m != mofd(datadate)
# First create the 6-month lagged time_avail_m
df['time_avail_m_lag6'] = df.groupby('permno')['time_avail_m'].shift(6)

# Convert both to Period('M') format for comparison (equivalent to Stata's monthly dates)
df['time_avail_m_lag6_period'] = pd.to_datetime(df['time_avail_m_lag6']).dt.to_period('M')
df['datadate_period'] = pd.to_datetime(df['datadate']).dt.to_period('M')

# Replace me_datadate with NaN if lagged time doesn't match datadate month
df.loc[df['time_avail_m_lag6_period'] != df['datadate_period'], 'me_datadate'] = np.nan

# Forward fill me_datadate within each permno (only fill NaN values)
df['me_datadate'] = df.groupby('permno')['me_datadate'].ffill()

# SIGNAL CONSTRUCTION
# Stattman 1980 does not actually take logs but does everything nonparametrically anyway
# but he does drop negative ceqt, which logs takes care of
df['BM'] = np.log(df['ceqt'] / df['me_datadate'])

# Keep only necessary columns for output
output_df = df[['permno', 'time_avail_m', 'BM']].copy()

# Convert time_avail_m to yyyymm integer format (YYYYMM)
output_df['yyyymm'] = pd.to_datetime(output_df['time_avail_m']).dt.year * 100 + pd.to_datetime(output_df['time_avail_m']).dt.month

# Keep only necessary columns
output_df = output_df[['permno', 'yyyymm', 'BM']].copy()

# Remove rows with missing BM values
output_df = output_df.dropna(subset=['BM'])

# Set index as required
output_df = output_df.set_index(['permno', 'yyyymm']).sort_index()

# SAVE
output_df.to_csv('../pyData/Predictors/BM.csv')