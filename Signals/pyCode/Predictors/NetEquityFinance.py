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
# Load required variables from Compustat annual data
m_aCompustat = pd.read_parquet('../pyData/Intermediate/m_aCompustat.parquet', 
                               columns=['gvkey', 'permno', 'time_avail_m', 'sstk', 'prstkc', 'at', 'dv'])
df = m_aCompustat.copy()
print(f"Loaded m_aCompustat data: {len(df)} observations")

# SIGNAL CONSTRUCTION
# Remove duplicate observations by permno and time_avail_m
df = df.drop_duplicates(subset=['permno', 'time_avail_m'], keep='first')
print(f"After deduplicating by permno time_avail_m: {len(df)} observations")

# Sort data by permno and time for time-series operations
df = df.sort_values(['permno', 'time_avail_m'])

# Calculate net equity financing as net equity issuance scaled by average assets
# Create 12-month lag of total assets
df['l12_at'] = df.groupby('permno')['at'].shift(12)

# Calculate NetEquityFinance
df['NetEquityFinance'] = (df['sstk'] - df['prstkc'] - df['dv']) / (0.5 * (df['at'] + df['l12_at']))

# Remove extreme values (absolute value greater than 1)
df.loc[df['NetEquityFinance'].abs() > 1, 'NetEquityFinance'] = np.nan

print(f"NetEquityFinance calculated for {df['NetEquityFinance'].notna().sum()} observations")

# SAVE
# Save the NetEquityFinance predictor to CSV
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