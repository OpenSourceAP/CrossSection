# ABOUTME: Change in breadth of ownership following Chen, Hong and Stein 2002, Table 4A
# ABOUTME: calculates quarterly change in number of institutional owners from 13F data
"""
Usage:
    python3 Predictors/DelBreadth.py

Inputs:
    - SignalMasterTable.parquet: Monthly master table with columns [permno, time_avail_m, exchcd, mve_c]
    - TR_13F.parquet: 13F data with columns [permno, time_avail_m, dbreadth]

Outputs:
    - DelBreadth.csv: CSV file with columns [permno, yyyymm, DelBreadth]
    - DelBreadth = quarterly change in number of institutional owners (dbreadth)
    - Excludes stocks in lowest quintile by market value of equity (based on NYSE stocks only)
"""

import os
import sys
import pandas as pd
import numpy as np

# Add parent directory to path for utils import
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils.save_standardized import save_predictor

# DATA LOAD
df = pd.read_parquet('../pyData/Intermediate/SignalMasterTable.parquet', 
                     columns=['permno', 'time_avail_m', 'exchcd', 'mve_c'])

# Merge with TR_13F data
tr_13f = pd.read_parquet('../pyData/Intermediate/TR_13F.parquet',
                         columns=['permno', 'time_avail_m', 'dbreadth'])

df = df.merge(tr_13f, on=['permno', 'time_avail_m'], how='left')

# SIGNAL CONSTRUCTION
df['DelBreadth'] = df['dbreadth']

# Calculate 20th percentile of mve_c for NYSE stocks only
nyse_df = df[df['exchcd'] == 1]
percentile_20 = nyse_df.groupby('time_avail_m')['mve_c'].quantile(0.20).reset_index()
percentile_20.columns = ['time_avail_m', 'temp']

# Merge back and apply filter
df = df.merge(percentile_20, on='time_avail_m', how='left')
df.loc[df['mve_c'] < df['temp'], 'DelBreadth'] = np.nan

# SAVE
save_predictor(df, 'DelBreadth')