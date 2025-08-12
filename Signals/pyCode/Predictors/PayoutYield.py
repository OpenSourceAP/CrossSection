# ABOUTME: Translates PayoutYield.do to calculate payout yield
# ABOUTME: Run with: python3 Predictors/PayoutYield.py

# Calculates payout yield using Compustat and market value data
# Input: ../pyData/Intermediate/m_aCompustat.parquet, ../pyData/Intermediate/SignalMasterTable.parquet
# Output: ../pyData/Predictors/PayoutYield.csv

import pandas as pd
import numpy as np

# DATA LOAD
# Load m_aCompustat with specific columns
df = pd.read_parquet('../pyData/Intermediate/m_aCompustat.parquet', 
                     columns=['permno', 'time_avail_m', 'dvc', 'prstkc', 'pstkrv', 'sstk', 'sic', 'ceq', 'datadate'])

# bysort permno time_avail_m: keep if _n == 1 (deduplicate)
df = df.drop_duplicates(['permno', 'time_avail_m'], keep='first')

# merge 1:1 permno time_avail_m using SignalMasterTable, keep(match) keepusing(mve_c)
signal_master = pd.read_parquet('../pyData/Intermediate/SignalMasterTable.parquet', 
                                columns=['permno', 'time_avail_m', 'mve_c'])

df = df.merge(signal_master, on=['permno', 'time_avail_m'], how='inner')

# SIGNAL CONSTRUCTION
# Sort for lag operation (xtset permno time_avail_m)
df = df.sort_values(['permno', 'time_avail_m'])

# Create 6-month lag of mve_c (l6.mve_c)
# Stata l6. means 6 months back in calendar time
# Use efficient merge-based approach for calendar lag
df['lag6_date'] = df['time_avail_m'] - pd.DateOffset(months=6)

# Create lag lookup table
lag_lookup = df[['permno', 'time_avail_m', 'mve_c']].copy()
lag_lookup = lag_lookup.rename(columns={'time_avail_m': 'lag6_date', 'mve_c': 'mve_c_l6'})

# Merge to get 6-month lagged values
df = df.merge(lag_lookup, on=['permno', 'lag6_date'], how='left')

# gen PayoutYield = (dvc + prstkc + pstkrv)/l6.mve_c
df['PayoutYield'] = (df['dvc'] + df['prstkc'] + df['pstkrv']) / df['mve_c_l6']

# replace PayoutYield = . if PayoutYield <= 0
df.loc[df['PayoutYield'] <= 0, 'PayoutYield'] = np.nan

# FILTER
# destring sic, replace (convert sic to numeric)
df['sic'] = pd.to_numeric(df['sic'], errors='coerce')

# keep if (sic < 6000 | sic >= 7000) & ceq > 0
# In Stata, missing ceq values are treated as large positive numbers, so ceq > 0 is TRUE for missing
df = df[((df['sic'] < 6000) | (df['sic'] >= 7000)) & ((df['ceq'] > 0) | df['ceq'].isna())]

# sort permno time_avail_m
df = df.sort_values(['permno', 'time_avail_m'])

# bysort permno: keep if _n >= 24 (require at least 24 observations per permno)
df['obs_count'] = df.groupby('permno').cumcount() + 1
df = df[df['obs_count'] >= 24]

# Keep only observations with valid PayoutYield (not missing/infinite)
df = df.dropna(subset=['PayoutYield'])
df = df[np.isfinite(df['PayoutYield'])]

# Keep only required columns for final output
result = df[['permno', 'time_avail_m', 'PayoutYield']].copy()

# Convert time_avail_m to yyyymm format
result['yyyymm'] = result['time_avail_m'].dt.year * 100 + result['time_avail_m'].dt.month

# Final format matching Stata output
result = result[['permno', 'yyyymm', 'PayoutYield']]

# Convert permno and yyyymm to int
result['permno'] = result['permno'].astype(int)
result['yyyymm'] = result['yyyymm'].astype(int)

# SAVE
result.to_csv('../pyData/Predictors/PayoutYield.csv', index=False)

print(f"PayoutYield predictor created with {len(result)} observations")