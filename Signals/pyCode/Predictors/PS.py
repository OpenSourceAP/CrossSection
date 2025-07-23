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

# Create 12-month lags for required variables (time-based, like Stata l12.)
# This approach matches Stata's l12. operator which looks for observations exactly 12 months earlier
df['time_lag12'] = df['time_avail_m'] - pd.DateOffset(months=12)

lag_vars = ['ib', 'at', 'dltt', 'act', 'lct', 'sale', 'shrout']
for var in lag_vars:
    # Create lag data for merging
    lag_data = df[['permno', 'time_avail_m', var]].copy()
    lag_data.columns = ['permno', 'time_lag12', f'l12_{var}']
    
    # Merge back to main dataframe
    df = df.merge(lag_data, on=['permno', 'time_lag12'], how='left')

# Drop temporary column
df = df.drop('time_lag12', axis=1)

# Calculate individual Piotroski components
# p1: Positive net income
df['p1'] = 0
df.loc[df['ib'] > 0, 'p1'] = 1

# p2: Positive operating cash flow
df['p2'] = 0
df.loc[df['fopt'] > 0, 'p2'] = 1

# p3: Improvement in ROA
df['p3'] = 0
df.loc[(df['ib']/df['at'] - df['l12_ib']/df['l12_at']) > 0, 'p3'] = 1

# p4: Cash flow exceeds net income
df['p4'] = 0
df.loc[df['fopt'] > df['ib'], 'p4'] = 1

# p5: Reduction in leverage
df['p5'] = 0
df.loc[(df['dltt']/df['at'] - df['l12_dltt']/df['l12_at']) < 0, 'p5'] = 1

# p6: Improvement in current ratio
df['p6'] = 0
df.loc[(df['act']/df['lct'] - df['l12_act']/df['l12_lct']) > 0, 'p6'] = 1

# p7: Improvement in gross margin
df['tempebit'] = df['ib'] + df['txt'] + df['xint']
df['p7'] = 0
df.loc[(df['tempebit']/df['sale'] - df['tempebit']/df['l12_sale']) > 0, 'p7'] = 1

# p8: Improvement in asset turnover
df['p8'] = 0
df.loc[(df['sale']/df['at'] - df['l12_sale']/df['l12_at']) > 0, 'p8'] = 1

# p9: No increase in shares outstanding
df['p9'] = 0
df.loc[df['shrout'] <= df['l12_shrout'], 'p9'] = 1

# Sum all components
df['PS'] = df['p1'] + df['p2'] + df['p3'] + df['p4'] + df['p5'] + df['p6'] + df['p7'] + df['p8'] + df['p9']

# Set PS to missing if any required variables are missing
df.loc[(df['fopt'].isna()) | (df['ib'].isna()) | (df['at'].isna()) | (df['dltt'].isna()) | 
       (df['sale'].isna()) | (df['act'].isna()) | (df['tempebit'].isna()) | (df['shrout'].isna()), 'PS'] = np.nan

# Restrict to highest BM quintile
df['BM'] = np.log(df['ceq'] / df['mve_c'])
# Handle infinite values in BM
df['BM_clean'] = df['BM'].replace([np.inf, -np.inf], np.nan)
df['temp'] = df.groupby('time_avail_m')['BM_clean'].transform(
    lambda x: pd.qcut(x, q=5, labels=False, duplicates='drop') + 1
)
# Keep only highest BM quintile (quintile 5)
df.loc[df['temp'] != 5, 'PS'] = np.nan

# Drop missing values
df = df.dropna(subset=['PS'])

# Convert time_avail_m to yyyymm
df['yyyymm'] = df['time_avail_m'].dt.year * 100 + df['time_avail_m'].dt.month

# Keep required columns and order
df = df[['permno', 'yyyymm', 'PS']].copy()

# SAVE
df.to_csv("../pyData/Predictors/PS.csv", index=False)
print(f"PS: Saved {len(df):,} observations")