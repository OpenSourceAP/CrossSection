# ABOUTME: Translates NetEquityFinance.do - calculates net equity financing activity
# ABOUTME: Run from pyCode/ directory: python3 Predictors/NetEquityFinance.py

# Inputs:
#   - ../pyData/Intermediate/m_aCompustat.parquet
# Outputs:
#   - ../pyData/Predictors/NetEquityFinance.csv

import pandas as pd
import numpy as np

print("Starting NetEquityFinance calculation...")

# DATA LOAD
# use gvkey permno time_avail_m sstk prstkc at dv using "$pathDataIntermediate/m_aCompustat", clear
m_aCompustat = pd.read_parquet('../pyData/Intermediate/m_aCompustat.parquet', 
                               columns=['gvkey', 'permno', 'time_avail_m', 'sstk', 'prstkc', 'at', 'dv'])
df = m_aCompustat.copy()
print(f"Loaded m_aCompustat data: {len(df)} observations")

# SIGNAL CONSTRUCTION
# bysort permno time_avail_m: keep if _n == 1  // deletes a few observations
df = df.drop_duplicates(subset=['permno', 'time_avail_m'], keep='first')
print(f"After deduplicating by permno time_avail_m: {len(df)} observations")

# xtset permno time_avail_m
df = df.sort_values(['permno', 'time_avail_m'])

# gen NetEquityFinance = (sstk - prstkc - dv)/(.5*(at + l12.at))
# Create 12-month lag of at
df['l12_at'] = df.groupby('permno')['at'].shift(12)

# Calculate NetEquityFinance
df['NetEquityFinance'] = (df['sstk'] - df['prstkc'] - df['dv']) / (0.5 * (df['at'] + df['l12_at']))

# replace NetEquityFinance = . if abs(NetEquityFinance) > 1
df.loc[df['NetEquityFinance'].abs() > 1, 'NetEquityFinance'] = np.nan

print(f"NetEquityFinance calculated for {df['NetEquityFinance'].notna().sum()} observations")

# SAVE
# do "$pathCode/savepredictor" NetEquityFinance
result = df[['permno', 'time_avail_m', 'NetEquityFinance']].copy()
result = result.dropna(subset=['NetEquityFinance'])

# Convert time_avail_m to yyyymm format
result['yyyymm'] = result['time_avail_m'].dt.year * 100 + result['time_avail_m'].dt.month
result = result[['permno', 'yyyymm', 'NetEquityFinance']].copy()

# Convert to integers where appropriate
result['permno'] = result['permno'].astype(int)
result['yyyymm'] = result['yyyymm'].astype(int)

print(f"Final output: {len(result)} observations")
result.to_csv('../pyData/Predictors/NetEquityFinance.csv', index=False)
print("NetEquityFinance.csv saved successfully")