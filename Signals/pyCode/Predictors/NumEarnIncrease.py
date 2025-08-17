# ABOUTME: Translates NumEarnIncrease.do - counts consecutive quarterly earnings increases
# ABOUTME: Calculates number of consecutive quarters with positive earnings growth

# How to run: python3 Predictors/NumEarnIncrease.py (from pyCode/ directory)
# Inputs: ../pyData/Intermediate/SignalMasterTable.parquet, ../pyData/Intermediate/m_QCompustat.parquet  
# Outputs: ../pyData/Predictors/NumEarnIncrease.csv

import pandas as pd
import numpy as np

# DATA LOAD
df = pd.read_parquet('../pyData/Intermediate/SignalMasterTable.parquet', columns=['permno', 'gvkey', 'time_avail_m'])
df = df[df['gvkey'].notna()]
temp_df = pd.read_parquet('../pyData/Intermediate/m_QCompustat.parquet', columns=['gvkey', 'time_avail_m', 'ibq'])
df = df.merge(temp_df, on=['gvkey', 'time_avail_m'], how='inner')

# SIGNAL CONSTRUCTION
df = df.sort_values(['permno', 'time_avail_m'])

# Create calendar-based lag for quarterly data (l12.ibq means 12 months ago)
df['time_lag12'] = df['time_avail_m'] - pd.DateOffset(months=12)
temp_ibq = df[['permno', 'time_avail_m', 'ibq']].copy()
temp_ibq.columns = ['permno', 'time_lag12', 'l12_ibq']
df = df.merge(temp_ibq, on=['permno', 'time_lag12'], how='left')

df['chearn'] = df['ibq'] - df['l12_ibq']


# Create calendar-based lag variables for chearn (quarterly lags)
for lag in [3, 6, 9, 12, 15, 18, 21, 24]:
    df[f'time_lag{lag}'] = df['time_avail_m'] - pd.DateOffset(months=lag)
    temp_chearn = df[['permno', 'time_avail_m', 'chearn']].copy()
    temp_chearn.columns = ['permno', f'time_lag{lag}', f'l{lag}_chearn']
    df = df.merge(temp_chearn, on=['permno', f'time_lag{lag}'], how='left')

df['nincr'] = 0

# replace nincr = 1 if chearn > 0 & l3.chearn <=0
# Note: In Stata, missing chearn is treated as positive infinity, so chearn > 0 is TRUE when missing
df.loc[((df['chearn'] > 0) | df['chearn'].isna()) & (df['l3_chearn'] <= 0), 'nincr'] = 1

# replace nincr = 2 if chearn > 0 & l3.chearn >0 & l6.chearn <=0  
df.loc[((df['chearn'] > 0) | df['chearn'].isna()) & ((df['l3_chearn'] > 0) | df['l3_chearn'].isna()) & (df['l6_chearn'] <= 0), 'nincr'] = 2

# replace nincr = 3 if chearn > 0 & l3.chearn >0 & l6.chearn >0 & l9.chearn <=0
df.loc[((df['chearn'] > 0) | df['chearn'].isna()) & ((df['l3_chearn'] > 0) | df['l3_chearn'].isna()) & ((df['l6_chearn'] > 0) | df['l6_chearn'].isna()) & (df['l9_chearn'] <= 0), 'nincr'] = 3

# replace nincr = 4 if chearn > 0 & l3.chearn >0 & l6.chearn >0 & l9.chearn >0 & l12.chearn <=0
df.loc[((df['chearn'] > 0) | df['chearn'].isna()) & ((df['l3_chearn'] > 0) | df['l3_chearn'].isna()) & ((df['l6_chearn'] > 0) | df['l6_chearn'].isna()) & ((df['l9_chearn'] > 0) | df['l9_chearn'].isna()) & (df['l12_chearn'] <= 0), 'nincr'] = 4

# replace nincr = 5 if chearn > 0 & l3.chearn >0 & l6.chearn >0 & l9.chearn >0 & l12.chearn >0 & l15.chearn <=0
df.loc[((df['chearn'] > 0) | df['chearn'].isna()) & ((df['l3_chearn'] > 0) | df['l3_chearn'].isna()) & ((df['l6_chearn'] > 0) | df['l6_chearn'].isna()) & ((df['l9_chearn'] > 0) | df['l9_chearn'].isna()) & ((df['l12_chearn'] > 0) | df['l12_chearn'].isna()) & (df['l15_chearn'] <= 0), 'nincr'] = 5

# replace nincr = 6 if chearn > 0 & l3.chearn >0 & l6.chearn >0 & l9.chearn >0 & l12.chearn >0 & l15.chearn >0 & l18.chearn <=0
df.loc[((df['chearn'] > 0) | df['chearn'].isna()) & ((df['l3_chearn'] > 0) | df['l3_chearn'].isna()) & ((df['l6_chearn'] > 0) | df['l6_chearn'].isna()) & ((df['l9_chearn'] > 0) | df['l9_chearn'].isna()) & ((df['l12_chearn'] > 0) | df['l12_chearn'].isna()) & ((df['l15_chearn'] > 0) | df['l15_chearn'].isna()) & (df['l18_chearn'] <= 0), 'nincr'] = 6

# replace nincr = 7 if chearn > 0 & l3.chearn >0 & l6.chearn >0 & l9.chearn >0 & l12.chearn >0 & l15.chearn >0 & l18.chearn >0 & l21.chearn <=0
df.loc[((df['chearn'] > 0) | df['chearn'].isna()) & ((df['l3_chearn'] > 0) | df['l3_chearn'].isna()) & ((df['l6_chearn'] > 0) | df['l6_chearn'].isna()) & ((df['l9_chearn'] > 0) | df['l9_chearn'].isna()) & ((df['l12_chearn'] > 0) | df['l12_chearn'].isna()) & ((df['l15_chearn'] > 0) | df['l15_chearn'].isna()) & ((df['l18_chearn'] > 0) | df['l18_chearn'].isna()) & (df['l21_chearn'] <= 0), 'nincr'] = 7

# replace nincr = 8 if chearn > 0 & l3.chearn >0 & l6.chearn >0 & l9.chearn >0 & l12.chearn >0 & l15.chearn >0 & l18.chearn >0 & l21.chearn >0 & l24.chearn <=0
df.loc[((df['chearn'] > 0) | df['chearn'].isna()) & ((df['l3_chearn'] > 0) | df['l3_chearn'].isna()) & ((df['l6_chearn'] > 0) | df['l6_chearn'].isna()) & ((df['l9_chearn'] > 0) | df['l9_chearn'].isna()) & ((df['l12_chearn'] > 0) | df['l12_chearn'].isna()) & ((df['l15_chearn'] > 0) | df['l15_chearn'].isna()) & ((df['l18_chearn'] > 0) | df['l18_chearn'].isna()) & ((df['l21_chearn'] > 0) | df['l21_chearn'].isna()) & (df['l24_chearn'] <= 0), 'nincr'] = 8

df['NumEarnIncrease'] = df['nincr']


# Create yyyymm
df['yyyymm'] = df['time_avail_m'].dt.year * 100 + df['time_avail_m'].dt.month

# SAVE
result = df[['permno', 'yyyymm', 'NumEarnIncrease']].copy()
result = result.dropna(subset=['NumEarnIncrease'])
result.to_csv('../pyData/Predictors/NumEarnIncrease.csv', index=False)

print(f"NumEarnIncrease: {len(result)} observations saved")