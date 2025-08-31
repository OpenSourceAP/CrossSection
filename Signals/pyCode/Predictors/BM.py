# ABOUTME: Book-to-market ratio following Stattman (1980), Table 3
# ABOUTME: Calculates log of tangible book equity (ceqt) over market equity matched at FYE

"""
Usage:
    python3 Predictors/BM.py

Inputs:
    - m_aCompustat.parquet: Monthly Compustat data with columns [permno, time_avail_m, datadate, ceqt]
    - SignalMasterTable.parquet: Monthly master table with mve_c

Outputs:
    - BM.csv: CSV file with columns [permno, yyyymm, BM]
    - BM = log(ceqt/market_equity), where market equity is matched at FYE with 6-month lag
"""

import pandas as pd
import numpy as np

print("Starting BM.py...")

# DATA LOAD
# Load m_aCompustat data
print("Loading m_aCompustat data...")
m_compustat = pd.read_parquet('../pyData/Intermediate/m_aCompustat.parquet')
m_compustat = m_compustat[['permno', 'time_avail_m', 'datadate', 'ceqt']].copy()

# Load SignalMasterTable
print("Loading SignalMasterTable...")
signal_master = pd.read_parquet('../pyData/Intermediate/SignalMasterTable.parquet')
signal_master = signal_master[['permno', 'time_avail_m', 'mve_c']].copy()
print(f"Loaded m_aCompustat: {m_compustat.shape[0]} rows")
print(f"Loaded SignalMasterTable: {signal_master.shape[0]} rows")

# Merge accounting data with market data
print("Merging with SignalMasterTable...")
df = pd.merge(m_compustat, signal_master, on=['permno', 'time_avail_m'], how='right')
print(f"After merge: {df.shape[0]} rows")

# find the market equity that matches datadate (based on 6 month lag)
# (see "Company Data" section)

# Sort by permno and time_avail_m for proper lagging
print("Setting up panel data structure...")
df = df.sort_values(['permno', 'time_avail_m'])

# Create 6-month lag of market equity
print("Creating 6-month lag for market equity...")
df['me_datadate'] = df.groupby('permno')['mve_c'].shift(6)
df['l6_time_avail_m'] = df.groupby('permno')['time_avail_m'].shift(6)

# Convert to Period('M') format for comparison
df['l6_time_avail_m_period'] = pd.to_datetime(df['l6_time_avail_m']).dt.to_period('M')
df['datadate_period'] = pd.to_datetime(df['datadate']).dt.to_period('M')

# Only use market equity if lag period matches datadate period
df.loc[df['l6_time_avail_m_period'] != df['datadate_period'], 'me_datadate'] = np.nan

# Forward fill market equity within each firm
df['me_datadate'] = df.groupby('permno')['me_datadate'].ffill()

# Cleanup intermediate columns
df = df.drop(['l6_time_avail_m', 'l6_time_avail_m_period', 'datadate_period'], axis=1)

# SIGNAL CONSTRUCTION
print("Calculating BM signal...")
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
print(f"Calculated BM for {len(output_df)} observations")

# Set index as required
output_df = output_df.set_index(['permno', 'yyyymm']).sort_index()

# SAVE
output_df.to_csv('../pyData/Predictors/BM.csv')
print("BM.py completed successfully")