# ABOUTME: Creates zero trading day predictors (1M, 6M, 12M versions) from daily CRSP data
# ABOUTME: Calculates daily turnover and counts zero-volume trading days with deflators

# How to run: python3 ZZ1_zerotrade_zerotradeAlt1_zerotradeAlt12.py
# Inputs: ../pyData/Intermediate/dailyCRSP.parquet
# Outputs: ../pyData/Predictors/zerotrade1M.csv, zerotrade6M.csv, zerotrade12M.csv

import pandas as pd
import numpy as np
import warnings
warnings.filterwarnings('ignore')

# DATA LOAD
df = pd.read_parquet('../pyData/Intermediate/dailyCRSP.parquet')

# SIGNAL CONSTRUCTION
df['time_avail_m'] = df['time_d'].dt.year * 100 + df['time_d'].dt.month

df['countzero'] = np.where(df['vol'] == 0, 1, 0)
df['turn'] = df['vol'] / df['shrout']  # daily turnover is the ratio of the number of shares traded on a day to the number of shares outstanding at the end of the day (Liu (2006, p. 635))

df['days'] = 0  # help variable because of some weirdness of collapse

# gcollapse (sum) countzero turn (count) ndays = days, by(permno time_avail_m)
collapsed = df.groupby(['permno', 'time_avail_m']).agg({
    'countzero': 'sum',
    'turn': 'sum', 
    'days': 'count'
}).reset_index()
collapsed = collapsed.rename(columns={'days': 'ndays'})

# xtset permno time_avail_m
collapsed = collapsed.sort_values(['permno', 'time_avail_m']).reset_index(drop=True)

# Group by permno for time series operations
grouped = collapsed.groupby('permno')

# 40n1 Number of days with 0 trades (1 month version)
collapsed['temp_zerotrade'] = (collapsed['countzero'] + ((1/collapsed['turn'])/480000)) * (21/collapsed['ndays'])
collapsed['zerotrade1M'] = grouped['temp_zerotrade'].shift(1)

# 40 Number of days with 0 trades (6 month version)
collapsed['Turn6'] = collapsed['turn'] + grouped['turn'].shift(1) + grouped['turn'].shift(2) + grouped['turn'].shift(3) + grouped['turn'].shift(4) + grouped['turn'].shift(5)
collapsed['countzero6'] = collapsed['countzero'] + grouped['countzero'].shift(1) + grouped['countzero'].shift(2) + grouped['countzero'].shift(3) + grouped['countzero'].shift(4) + grouped['countzero'].shift(5)
collapsed['ndays6'] = collapsed['ndays'] + grouped['ndays'].shift(1) + grouped['ndays'].shift(2) + grouped['ndays'].shift(3) + grouped['ndays'].shift(4) + grouped['ndays'].shift(5)

collapsed['temp_zerotrade6'] = (collapsed['countzero6'] + ((1/collapsed['Turn6'])/11000)) * (21*6/collapsed['ndays6'])  # I use a deflator of 11,000 in constructing LM6 and LM12, and a deflator of 480,000 for LM1 (Liu (2006, fn 4, p. 635))

collapsed['zerotrade6M'] = grouped['temp_zerotrade6'].shift(1)

# 40n12 Number of days with 0 trades (12 month version)
collapsed['Turn12'] = collapsed['turn'] + grouped['turn'].shift(1) + grouped['turn'].shift(2) + grouped['turn'].shift(3) + grouped['turn'].shift(4) + grouped['turn'].shift(5) + grouped['turn'].shift(6) + grouped['turn'].shift(7) + grouped['turn'].shift(8) + grouped['turn'].shift(9) + grouped['turn'].shift(10) + grouped['turn'].shift(11)
collapsed['countzero12'] = collapsed['countzero'] + grouped['countzero'].shift(1) + grouped['countzero'].shift(2) + grouped['countzero'].shift(3) + grouped['countzero'].shift(4) + grouped['countzero'].shift(5) + grouped['countzero'].shift(6) + grouped['countzero'].shift(7) + grouped['countzero'].shift(8) + grouped['countzero'].shift(9) + grouped['countzero'].shift(10) + grouped['countzero'].shift(11)
collapsed['ndays12'] = collapsed['ndays'] + grouped['ndays'].shift(1) + grouped['ndays'].shift(2) + grouped['ndays'].shift(3) + grouped['ndays'].shift(4) + grouped['ndays'].shift(5) + grouped['ndays'].shift(6) + grouped['ndays'].shift(7) + grouped['ndays'].shift(8) + grouped['ndays'].shift(9) + grouped['ndays'].shift(10) + grouped['ndays'].shift(11)

collapsed['temp_zerotrade12'] = (collapsed['countzero12'] + ((1/collapsed['Turn12'])/11000)) * (21*12/collapsed['ndays12'])  # I use a deflator of 11,000 in constructing LM6 and LM12, and a deflator of 480,000 for LM1 (Liu (2006, fn 4, p. 635))

collapsed['zerotrade12M'] = grouped['temp_zerotrade12'].shift(1)

# SAVE
# Save zerotrade1M
zerotrade1M = collapsed[['permno', 'time_avail_m', 'zerotrade1M']].dropna()
zerotrade1M['yyyymm'] = zerotrade1M['time_avail_m']
zerotrade1M = zerotrade1M[['permno', 'yyyymm', 'zerotrade1M']]
zerotrade1M.to_csv('../pyData/Predictors/zerotrade1M.csv', index=False)

# Save zerotrade6M  
zerotrade6M = collapsed[['permno', 'time_avail_m', 'zerotrade6M']].dropna()
zerotrade6M['yyyymm'] = zerotrade6M['time_avail_m']
zerotrade6M = zerotrade6M[['permno', 'yyyymm', 'zerotrade6M']]
zerotrade6M.to_csv('../pyData/Predictors/zerotrade6M.csv', index=False)

# Save zerotrade12M
zerotrade12M = collapsed[['permno', 'time_avail_m', 'zerotrade12M']].dropna()
zerotrade12M['yyyymm'] = zerotrade12M['time_avail_m']
zerotrade12M = zerotrade12M[['permno', 'yyyymm', 'zerotrade12M']]
zerotrade12M.to_csv('../pyData/Predictors/zerotrade12M.csv', index=False)