# ABOUTME: PS.py - calculates Piotroski F-score (within highest BM quintile)
# ABOUTME: Nine-factor profitability, efficiency, and leverage score restricted to highest book-to-market quintile

"""
PS predictor calculation (Piotroski F-score)

Usage:
    cd pyCode/
    source .venv/bin/activate
    python3 Predictors/PS.py

Inputs:
    - ../pyData/Intermediate/m_aCompustat.parquet (permno, time_avail_m, fopt, oancf, ib, at, dltt, act, lct, txt, xint, sale, ceq)
    - ../pyData/Intermediate/SignalMasterTable.parquet (permno, time_avail_m, mve_c)
    - ../pyData/Intermediate/monthlyCRSP.parquet (permno, time_avail_m, shrout)

Outputs:
    - ../pyData/Predictors/PS.csv (permno, yyyymm, PS)
"""

import pandas as pd
import numpy as np
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils.stata_fastxtile import fastxtile

# DATA LOAD
# Load m_aCompustat data
compustat_df = pd.read_parquet("../pyData/Intermediate/m_aCompustat.parquet", 
                               columns=['permno', 'time_avail_m', 'fopt', 'oancf', 'ib', 'at', 'dltt', 'act', 'lct', 'txt', 'xint', 'sale', 'ceq'])

# Merge with SignalMasterTable
signal_df = pd.read_parquet("../pyData/Intermediate/SignalMasterTable.parquet", 
                           columns=['permno', 'time_avail_m', 'mve_c'])
df = compustat_df.merge(signal_df, on=['permno', 'time_avail_m'], how='inner')

# Merge with monthlyCRSP
crsp_df = pd.read_parquet("../pyData/Intermediate/monthlyCRSP.parquet", 
                         columns=['permno', 'time_avail_m', 'shrout'])
df = df.merge(crsp_df, on=['permno', 'time_avail_m'], how='inner')

# SIGNAL CONSTRUCTION
# Sort data for lag operations
df = df.sort_values(['permno', 'time_avail_m'])

# Replace fopt with oancf if fopt is missing
df['fopt'] = df['fopt'].fillna(df['oancf'])

# Create tempebit before lag creation (needed for accurate comparison)
df['tempebit'] = df['ib'] + df['txt'] + df['xint']

# Create 12-month lags for required variables (Stata-compatible flexible matching)
# Use groupby + shift(12) approach to match Stata's l12. behavior more closely
# This handles missing months better than exact date matching
df_sorted = df.sort_values(['permno', 'time_avail_m'])

lag_vars = ['ib', 'at', 'dltt', 'act', 'lct', 'sale', 'shrout']
for var in lag_vars:
    # Create 12-period lag using shift (more flexible than exact date matching)
    df_sorted[f'l12_{var}'] = df_sorted.groupby('permno')[var].shift(12)

df = df_sorted

# Calculate individual Piotroski components
# p1: Positive net income
df['p1'] = 0
df.loc[df['ib'] > 0, 'p1'] = 1

# p2: Positive operating cash flow
df['p2'] = 0
df.loc[df['fopt'] > 0, 'p2'] = 1

# p3: Improvement in ROA - with Stata missing logic
df['p3'] = 0
# Stata treats missing lags as making the comparison TRUE
condition = (df['ib']/df['at'] - df['l12_ib']/df['l12_at']) > 0
lag_missing = df['l12_ib'].isna() | df['l12_at'].isna()
df.loc[condition | lag_missing, 'p3'] = 1

# p4: Cash flow exceeds net income
df['p4'] = 0
df.loc[df['fopt'] > df['ib'], 'p4'] = 1

# p5: Reduction in leverage - with Stata missing logic
df['p5'] = 0
# Stata treats missing lags as making the comparison TRUE
condition = (df['dltt']/df['at'] - df['l12_dltt']/df['l12_at']) < 0
lag_missing = df['l12_dltt'].isna() | df['l12_at'].isna()
df.loc[condition | lag_missing, 'p5'] = 1

# p6: Improvement in current ratio - with Stata missing logic
df['p6'] = 0
# Stata treats missing lags as making the comparison TRUE
condition = (df['act']/df['lct'] - df['l12_act']/df['l12_lct']) > 0
lag_missing = df['l12_act'].isna() | df['l12_lct'].isna()
df.loc[condition | lag_missing, 'p6'] = 1

# p7: Improvement in gross margin - with Stata missing logic
df['p7'] = 0
# Stata treats missing lags as making the comparison TRUE
condition = (df['tempebit']/df['sale'] - df['tempebit']/df['l12_sale']) > 0
lag_missing = df['l12_sale'].isna()
df.loc[condition | lag_missing, 'p7'] = 1

# p8: Improvement in asset turnover - with Stata missing logic
df['p8'] = 0
# Stata treats missing lags as making the comparison TRUE
condition = (df['sale']/df['at'] - df['l12_sale']/df['l12_at']) > 0
lag_missing = df['l12_sale'].isna() | df['l12_at'].isna()
df.loc[condition | lag_missing, 'p8'] = 1

# p9: No increase in shares outstanding - with Stata missing logic
df['p9'] = 0
# Stata treats missing lags as making the comparison TRUE
condition = df['shrout'] <= df['l12_shrout']
lag_missing = df['l12_shrout'].isna()
df.loc[condition | lag_missing, 'p9'] = 1

# CHECKPOINT 1
print("CHECKPOINT 1 - Piotroski components for permno 10193:")
debug_filter = (df['permno'] == 10193) & (df['time_avail_m'].dt.year == 1988) & (df['time_avail_m'].dt.month.isin([2, 3, 4, 5, 6, 7, 8, 9, 10, 11]))
if debug_filter.any():
    debug_data = df[debug_filter][['permno', 'time_avail_m', 'p1', 'p2', 'p3', 'p4', 'p5', 'p6', 'p7', 'p8', 'p9']].copy()
    print(debug_data.to_string(index=False))
else:
    print("No data for permno 10193 in 1988 Feb-Nov period")

# Sum all components
df['PS'] = df['p1'] + df['p2'] + df['p3'] + df['p4'] + df['p5'] + df['p6'] + df['p7'] + df['p8'] + df['p9']

# Set PS to missing if any required variables are missing
df.loc[(df['fopt'].isna()) | (df['ib'].isna()) | (df['at'].isna()) | (df['dltt'].isna()) | 
       (df['sale'].isna()) | (df['act'].isna()) | (df['tempebit'].isna()) | (df['shrout'].isna()), 'PS'] = np.nan

# Restrict to highest BM quintile
df['BM'] = np.log(df['ceq'] / df['mve_c'])
# Clean infinite values explicitly before fastxtile (following MomRev successful pattern)
df['BM_clean'] = df['BM'].replace([np.inf, -np.inf], np.nan)
# Use robust fastxtile for BM quintiles with cleaned values
df['temp'] = fastxtile(df, 'BM_clean', by='time_avail_m', n=5)

# CHECKPOINT 2
print("CHECKPOINT 2 - BM quintile assignment for permno 10193:")
debug_filter = (df['permno'] == 10193) & (df['time_avail_m'].dt.year == 1988) & (df['time_avail_m'].dt.month.isin([2, 3, 4, 5, 6, 7, 8, 9, 10, 11]))
if debug_filter.any():
    debug_data = df[debug_filter][['permno', 'time_avail_m', 'BM', 'temp', 'PS']].copy()
    print(debug_data.to_string(index=False))
else:
    print("No data for permno 10193 in 1988 Feb-Nov period")

# Keep only highest BM quintile (quintile 5)
df.loc[df['temp'] != 5, 'PS'] = np.nan

# Drop missing values
df = df.dropna(subset=['PS'])

# Convert time_avail_m to yyyymm
df['yyyymm'] = df['time_avail_m'].dt.year * 100 + df['time_avail_m'].dt.month

# Keep required columns and order
df = df[['permno', 'yyyymm', 'PS']].copy()

# Convert to integer types to match Stata output format
df['permno'] = df['permno'].astype('int64')
df['yyyymm'] = df['yyyymm'].astype('int64')

# SAVE
df.to_csv("../pyData/Predictors/PS.csv", index=False)
print(f"PS: Saved {len(df):,} observations")