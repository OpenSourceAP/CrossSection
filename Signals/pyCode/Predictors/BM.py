# ABOUTME: Book-to-market ratio following Stattman (1980), Table 3 (loosely)
# ABOUTME: Calculates log of tangible book equity (ceqt) over market equity matched at FYE

"""
Usage:
    python3 Predictors/BM.py

Inputs:
    - m_aCompustat.parquet: Monthly Compustat data with columns [permno, time_avail_m, datadate, ceqt]
    - SignalMasterTable.parquet: Monthly master table with mve_permco

Outputs:
    - BM.csv: CSV file with columns [permno, yyyymm, BM]
    - BM = log(ceqt/market_equity), where market equity is matched at FYE with 6-month lag

Note:
    Stattman is a really really old paper. We're interpreting his Table 3 using FF-1992/1993-style methods.    
"""

import pandas as pd
import numpy as np
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils.stata_replication import stata_multi_lag
from utils.save_standardized import save_predictor

print("Starting BM.py...")

# DATA LOAD
# Load m_aCompustat data with specific columns
print("Loading m_aCompustat data...")
m_compustat = pd.read_parquet('../pyData/Intermediate/m_aCompustat.parquet',
                              columns=['permno', 'time_avail_m', 'datadate', 'ceqt'])

# Load SignalMasterTable with specific columns
print("Loading SignalMasterTable...")
signal_master = pd.read_parquet('../pyData/Intermediate/SignalMasterTable.parquet',
                                columns=['permno', 'time_avail_m', 'mve_permco'])
print(f"Loaded m_aCompustat: {m_compustat.shape[0]} rows")
print(f"Loaded SignalMasterTable: {signal_master.shape[0]} rows")

# Merge accounting data with market data
print("Merging with SignalMasterTable...")
df = pd.merge(m_compustat, signal_master, on=['permno', 'time_avail_m'], how='right')
print(f"After merge: {df.shape[0]} rows")

# find the market equity that matches datadate (based on 6 month lag)
# (see "Company Data" section)
df = stata_multi_lag(df, 'permno', 'time_avail_m', 'mve_permco', [6], prefix='l')
df = stata_multi_lag(df, 'permno', 'time_avail_m', 'time_avail_m', [6], prefix='l', fill_gaps=False)

# Only use market equity if lag period matches datadate month
# Since time_avail_m is already first of month, just check year-month match
df['me_datadate'] = df['l6_mve_permco']
mask = (df['l6_time_avail_m'].dt.to_period('M') != df['datadate'].dt.to_period('M'))
df.loc[mask, 'me_datadate'] = np.nan

# Forward fill market equity by permno
df['me_datadate'] = df.groupby('permno')['me_datadate'].ffill()


# SIGNAL CONSTRUCTION
print("Calculating BM signal...")
# Stattman 1980 does not actually take logs but does everything nonparametrically anyway
# but he does drop negative ceqt
df = df.query('ceqt > 0')
df['BM'] = np.log(df['ceqt'] / df['me_datadate'])

# SAVE using save_predictor utility
save_predictor(df[['permno', 'time_avail_m', 'BM']], 'BM')
print("BM.py completed successfully")