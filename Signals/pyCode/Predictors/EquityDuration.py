# ABOUTME: Creates equity duration measure using cash flow projections and discount rates
# ABOUTME: Run from pyCode/ directory: python3 Predictors/EquityDuration.py

# OP uses FF style: HDMLD is (S/HD + B/HD)/2 - (S/LD + B/LD)/2

# Run from pyCode/ directory  
# Inputs: a_aCompustat.parquet
# Output: ../pyData/Predictors/EquityDuration.csv

import pandas as pd
import numpy as np

print("Loading and processing EquityDuration...")

# DATA LOAD
df = pd.read_parquet('../pyData/Intermediate/a_aCompustat.parquet')
df = df[['gvkey', 'permno', 'time_avail_m', 'fyear', 'datadate', 'ceq', 'ib', 'sale', 'prcc_f', 'csho']].copy()

# SIGNAL CONSTRUCTION
df = df.sort_values(['gvkey', 'fyear'])

# Inputs from paper (define early for use in fallback logic)
autocorr_roe = 0.57
cost_equity = 0.12
autocorr_growth = 0.24
longrun_growth = 0.06

# Compute ROE, book equity growth, and cash distributions to equity
df['tempRoE'] = df['ib'] / df.groupby('gvkey')['ceq'].shift(1)

# Handle division by zero: Update df.groupby('gvkey')['sale'].shift(1)
df['temp_g_eq'] = df['sale'] / sale_lag - 1
df['temp_g_eq'] = df['temp_g_eq'].replace([np.inf, -np.inf], np.nan)

# Handle missing growth rates in cash distribution calculation by filling with zero
ceq_lag = df.groupby('gvkey')['ceq'].shift(1)
df['tempCD'] = ceq_lag * (df['tempRoE'] - df['temp_g_eq'].fillna(0))

# Project variables forward for years 1-10
df['tempRoE1'] = autocorr_roe * df['tempRoE'] + cost_equity * (1 - autocorr_roe)
df['temp_g_eq1'] = autocorr_growth * df['temp_g_eq'].fillna(0) + longrun_growth * (1 - autocorr_growth)
df['tempBV1'] = df['ceq'] * (1 + df['temp_g_eq1'])
df['tempCD1'] = df['ceq'] - df['tempBV1'] + df['ceq'] * df['tempRoE1']

# Project for years 2-10
for t in range(2, 11):
    j = t - 1
    df[f'tempRoE{t}'] = autocorr_roe * df[f'tempRoE{j}'] + cost_equity * (1 - autocorr_roe)
    df[f'temp_g_eq{t}'] = autocorr_growth * df[f'temp_g_eq{j}'].fillna(0) + longrun_growth * (1 - autocorr_growth)
    df[f'tempBV{t}'] = df[f'tempBV{j}'] * (1 + df[f'temp_g_eq{t}'])
    df[f'tempCD{t}'] = df[f'tempBV{j}'] - df[f'tempBV{t}'] + df[f'tempBV{j}'] * df[f'tempRoE{t}']

discount_rate = 1 + cost_equity

# Calculate MD_Part1 and PV_Part1
md_terms = []
pv_terms = []
for t in range(1, 11):
    md_terms.append(t * df[f'tempCD{t}'] / (discount_rate**t))
    pv_terms.append(df[f'tempCD{t}'] / (discount_rate**t))

df['MD_Part1'] = sum(md_terms)
df['PV_Part1'] = sum(pv_terms)

# Compute equity duration
df['tempME'] = df['prcc_f'] * df['csho']
df['EquityDuration'] = (df['MD_Part1'] / df['tempME'] + 
                        (10 + (1 + cost_equity) / cost_equity) * (1 - df['PV_Part1'] / df['tempME']))

# Monthly expansion - create 12 monthly observations for each annual observation
# This spreads annual data across the following 12 months
print("Expanding to monthly observations...")
df_expanded = pd.concat([df] * 12, ignore_index=True)
df_expanded['expansion_n'] = np.repeat(np.arange(1, 13), len(df))

# Add sequential months to each expanded observation
df_expanded['tempTime'] = df_expanded['time_avail_m']  # Store original time_avail_m

# Add months correctly - efficiently handle month addition
df_expanded['months_to_add'] = df_expanded['expansion_n'] - 1

# Convert to period and add months, then back to timestamp
df_expanded['time_period'] = df_expanded['tempTime'].dt.to_period('M')
df_expanded['new_period'] = df_expanded['time_period'] + df_expanded['months_to_add']
df_expanded['time_avail_m'] = df_expanded['new_period'].dt.to_timestamp()

# Clean up temporary columns
df_expanded = df_expanded.drop(['months_to_add', 'time_period', 'new_period'], axis=1)

# For each company-month combination, keep the observation with the latest data date
df_expanded = df_expanded.sort_values(['gvkey', 'time_avail_m', 'datadate'])
df_monthly = df_expanded.groupby(['gvkey', 'time_avail_m']).tail(1)

# For each permno-month combination, keep the first observation (handles duplicates)
# Prioritize observations with valid EquityDuration values in tie-breaking
# Create a temporary column for sorting to put non-missing values first
df_monthly['temp_na_sort'] = df_monthly['EquityDuration'].isna()
df_monthly = df_monthly.sort_values(['permno', 'time_avail_m', 'temp_na_sort', 'gvkey', 'datadate']).groupby(['permno', 'time_avail_m']).head(1)
df_monthly = df_monthly.drop('temp_na_sort', axis=1)

# Clean up temporary columns
df_monthly = df_monthly.drop(['expansion_n', 'tempTime'], axis=1)

# Convert to output format
df_monthly['yyyymm'] = df_monthly['time_avail_m'].dt.year * 100 + df_monthly['time_avail_m'].dt.month
df_monthly['permno'] = df_monthly['permno'].astype('int64')
df_monthly['yyyymm'] = df_monthly['yyyymm'].astype('int64')

df_final = df_monthly[['permno', 'yyyymm', 'EquityDuration']].copy()
df_final = df_final.dropna(subset=['EquityDuration'])
df_final = df_final.set_index(['permno', 'yyyymm'])

# SAVE
df_final.to_csv('../pyData/Predictors/EquityDuration.csv')
print("EquityDuration predictor saved successfully")