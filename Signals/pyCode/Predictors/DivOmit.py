# ABOUTME: Translates DivOmit.do to create dividend omission predictor
# ABOUTME: Run from pyCode/ directory: python3 Predictors/DivOmit.py

# Run from pyCode/ directory
# Inputs: CRSPdistributions.parquet, SignalMasterTable.parquet
# Output: ../pyData/Predictors/DivOmit.csv

import pandas as pd
import numpy as np
import sys
import os

# Add the parent directory to sys.path to import utils
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils.asrol import asrol_calendar_pd

# PREP DISTRIBUTIONS DATA
dist_df = pd.read_parquet('../pyData/Intermediate/CRSPdistributions.parquet')

# Cash dividends only (cd2 == 2 | cd2 == 3)
dist_df = dist_df[(dist_df['cd2'] == 2) | (dist_df['cd2'] == 3)]

# Collapse by exdt: this date tends to come first
dist_df['time_avail_m'] = pd.to_datetime(dist_df['exdt'].dt.to_period('M').dt.start_time)
dist_df = dist_df.dropna(subset=['time_avail_m', 'divamt'])

# Sum dividends by permno and time_avail_m
tempdivamt = dist_df.groupby(['permno', 'time_avail_m'])['divamt'].sum().reset_index()

# DATA LOAD
df = pd.read_parquet('../pyData/Intermediate/SignalMasterTable.parquet')
df = df[['permno', 'time_avail_m', 'exchcd', 'shrcd']].copy()

# Merge with dividend amounts
df = df.merge(tempdivamt, on=['permno', 'time_avail_m'], how='left')

# SIGNAL CONSTRUCTION
# OP selects "companies that had existed on the NYSE or AMEX for more than one year and paid regular period div"
# but we're more flexible
df['div'] = df['divamt']
df['div'] = df['div'].fillna(0)

# Create dividend indicator
#gen divind = div > 0 & (exchcd == 1 | exchcd == 2)
#gen divind = div > 0 
df['divind'] = (df['div'] > 0).astype(int)

# Sort data for lag calculations
df = df.sort_values(['permno', 'time_avail_m'])

# QUARTERLY OMISSION (3-month window)
# Rolling 3-month sum of dividend indicators
df['sum3_divind'] = asrol_calendar_pd(df, 'permno', 'time_avail_m', 'divind', stat='sum', window='3mo', min_obs=1)['divind_sum']

# Company paid dividend in the quarter
df['temppaid'] = (df['sum3_divind'] == 1).astype(int)

# Rolling 18-month mean of quarterly payment indicator
df['mean18_temppaid'] = asrol_calendar_pd(df, 'permno', 'time_avail_m', 'temppaid', stat='mean', window='18mo', min_obs=1)['temppaid_mean']

# Regular payer indicator
df['temppayer'] = (df['mean18_temppaid'] == 1).astype(int)

# Create lags for omission logic
df['sum3_divind_lag1'] = df.groupby('permno')['sum3_divind'].shift(1)
df['temppayer_lag3'] = df.groupby('permno')['temppayer'].shift(3)

# Quarterly omission: no dividend now, had dividend last quarter, was regular payer 3 months ago
df['omit_3'] = ((df['sum3_divind'] == 0) & 
                (df['sum3_divind_lag1'] > 0) & 
                (df['temppayer_lag3'] == 1)).astype(int)

# Drop temporary columns
df = df.drop(columns=['temppaid', 'sum3_divind', 'mean18_temppaid', 'temppayer', 
                      'sum3_divind_lag1', 'temppayer_lag3'])

# SEMI-ANNUAL OMISSION (6-month window)
# Rolling 6-month sum of dividend indicators
df['sum6_divind'] = asrol_calendar_pd(df, 'permno', 'time_avail_m', 'divind', stat='sum', window='6mo', min_obs=1)['divind_sum']

# Company paid dividend in the semi-annual period
df['temppaid'] = (df['sum6_divind'] == 1).astype(int)

# Rolling 18-month mean of semi-annual payment indicator
df['mean18_temppaid'] = asrol_calendar_pd(df, 'permno', 'time_avail_m', 'temppaid', stat='mean', window='18mo', min_obs=1)['temppaid_mean']

# Regular payer indicator
df['temppayer'] = (df['mean18_temppaid'] == 1).astype(int)

# Create lags for omission logic
df['sum6_divind_lag1'] = df.groupby('permno')['sum6_divind'].shift(1)
df['temppayer_lag6'] = df.groupby('permno')['temppayer'].shift(6)

# Semi-annual omission: no dividend now, had dividend last period, was regular payer 6 months ago
df['omit_6'] = ((df['sum6_divind'] == 0) & 
                (df['sum6_divind_lag1'] > 0) & 
                (df['temppayer_lag6'] == 1)).astype(int)

# Drop temporary columns
df = df.drop(columns=['temppaid', 'sum6_divind', 'mean18_temppaid', 'temppayer',
                      'sum6_divind_lag1', 'temppayer_lag6'])

# ANNUAL OMISSION (12-month window)
# Rolling 12-month sum of dividend indicators
df['sum12_divind'] = asrol_calendar_pd(df, 'permno', 'time_avail_m', 'divind', stat='sum', window='12mo', min_obs=1)['divind_sum']

# Company paid dividend in the annual period
df['temppaid'] = (df['sum12_divind'] == 1).astype(int)

# Rolling 24-month mean of annual payment indicator
df['mean24_temppaid'] = asrol_calendar_pd(df, 'permno', 'time_avail_m', 'temppaid', stat='mean', window='24mo', min_obs=1)['temppaid_mean']

# Regular payer indicator
df['temppayer'] = (df['mean24_temppaid'] == 1).astype(int)

# Create lags for omission logic
df['sum12_divind_lag1'] = df.groupby('permno')['sum12_divind'].shift(1)
df['temppayer_lag12'] = df.groupby('permno')['temppayer'].shift(12)

# Annual omission: no dividend now, had dividend last period, was regular payer 12 months ago
df['omit_12'] = ((df['sum12_divind'] == 0) & 
                 (df['sum12_divind_lag1'] > 0) & 
                 (df['temppayer_lag12'] == 1)).astype(int)

# Drop temporary columns
df = df.drop(columns=['temppaid', 'sum12_divind', 'mean24_temppaid', 'temppayer',
                      'sum12_divind_lag1', 'temppayer_lag12'])

# COMBINE OMISSION INDICATORS
# Any type of omission
df['omitnow'] = ((df['omit_3'] == 1) | (df['omit_6'] == 1) | (df['omit_12'] == 1)).astype(int)

# Rolling 2-month sum to extend signal
df['temp'] = asrol_calendar_pd(df, 'permno', 'time_avail_m', 'omitnow', stat='sum', window='2mo', min_obs=1)['omitnow_sum']

# Final dividend omission signal
df['DivOmit'] = (df['temp'] == 1).astype(int)

# Keep only necessary columns for output
df_final = df[['permno', 'time_avail_m', 'DivOmit']].copy()
df_final = df_final.dropna(subset=['DivOmit'])

# Convert time_avail_m to yyyymm format like other predictors
df_final['yyyymm'] = df_final['time_avail_m'].dt.year * 100 + df_final['time_avail_m'].dt.month

# Convert to integers for consistency with other predictors
df_final['permno'] = df_final['permno'].astype('int64')
df_final['yyyymm'] = df_final['yyyymm'].astype('int64')

# Keep only required columns and set index
df_final = df_final[['permno', 'yyyymm', 'DivOmit']].copy()
df_final = df_final.set_index(['permno', 'yyyymm'])

# SAVE
df_final.to_csv('../pyData/Predictors/DivOmit.csv')

print("DivOmit predictor saved successfully")