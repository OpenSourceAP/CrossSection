# ABOUTME: Translates EquityDuration.do to create equity duration measure
# ABOUTME: Run from pyCode/ directory: python3 Predictors/EquityDuration.py

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

# Compute ROE, book equity growth, and cash distributions to equity
df['tempRoE'] = df['ib'] / df.groupby('gvkey')['ceq'].shift(1)
df['temp_g_eq'] = df['sale'] / df.groupby('gvkey')['sale'].shift(1) - 1
df['tempCD'] = df.groupby('gvkey')['ceq'].shift(1) * (df['tempRoE'] - df['temp_g_eq'])

# Inputs from paper
autocorr_roe = 0.57
cost_equity = 0.12
autocorr_growth = 0.24
longrun_growth = 0.06

# Project variables forward for years 1-10
df['tempRoE1'] = autocorr_roe * df['tempRoE'] + cost_equity * (1 - autocorr_roe)
df['temp_g_eq1'] = autocorr_growth * df['temp_g_eq'] + longrun_growth * (1 - autocorr_growth)
df['tempBV1'] = df['ceq'] * (1 + df['temp_g_eq1'])
df['tempCD1'] = df['ceq'] - df['tempBV1'] + df['ceq'] * df['tempRoE1']

# Project for years 2-10
for t in range(2, 11):
    j = t - 1
    df[f'tempRoE{t}'] = autocorr_roe * df[f'tempRoE{j}'] + cost_equity * (1 - autocorr_roe)
    df[f'temp_g_eq{t}'] = autocorr_growth * df[f'temp_g_eq{j}'] + longrun_growth * (1 - autocorr_growth)
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

# Monthly expansion - optimized version matching Stata logic
# expand temp (where temp = 12) - create 12 copies of each row
print("Expanding to monthly observations...")
df_expanded = pd.concat([df] * 12, ignore_index=True)
df_expanded['expansion_n'] = np.tile(np.arange(1, 13), len(df))

# bysort gvkey tempTime: replace time_avail_m = time_avail_m + _n - 1
df_expanded['tempTime'] = df_expanded['time_avail_m']  # Store original time_avail_m
df_expanded['time_avail_m'] = df_expanded['time_avail_m'] + pd.to_timedelta((df_expanded['expansion_n'] - 1) * 30.44, unit='D')
df_expanded['time_avail_m'] = df_expanded['time_avail_m'].dt.to_period('M').dt.to_timestamp()  # Round to month start

# bysort gvkey time_avail_m (datadate): keep if _n == _N
# Keep latest datadate for each gvkey-time combination
df_expanded = df_expanded.sort_values(['gvkey', 'time_avail_m', 'datadate'])
df_monthly = df_expanded.groupby(['gvkey', 'time_avail_m']).tail(1)

# bysort permno time_avail_m: keep if _n == 1
# Keep first observation for each permno-time combination (handles duplicates)
df_monthly = df_monthly.sort_values(['permno', 'time_avail_m']).groupby(['permno', 'time_avail_m']).head(1)

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