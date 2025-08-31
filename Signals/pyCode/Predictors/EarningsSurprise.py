# ABOUTME: Translates EarningsSurprise.do to calculate standardized earnings surprise
# ABOUTME: Run with: python3 Predictors/EarningsSurprise.py

# Calculates earnings surprise using Compustat quarterly data
# Input: ../pyData/Intermediate/SignalMasterTable.parquet, ../pyData/Intermediate/m_QCompustat.parquet
# Output: ../pyData/Predictors/EarningsSurprise.csv

import pandas as pd
import numpy as np

# DATA LOAD
# Load SignalMasterTable with specific columns
df = pd.read_parquet('../pyData/Intermediate/SignalMasterTable.parquet', 
                     columns=['permno', 'gvkey', 'time_avail_m'])

# Filter to observations with valid gvkey identifiers
df = df.dropna(subset=['gvkey'])

# Merge with quarterly Compustat data to get earnings per share
qcompustat = pd.read_parquet('../pyData/Intermediate/m_QCompustat.parquet', 
                             columns=['gvkey', 'time_avail_m', 'epspxq'])

df = df.merge(qcompustat, on=['gvkey', 'time_avail_m'], how='inner')

# SIGNAL CONSTRUCTION
# Sort data by company and time for time series operations
df = df.sort_values(['permno', 'time_avail_m'])

# Calculate quarterly earnings growth over 12-month period
df['date_lag12'] = df['time_avail_m'] - pd.DateOffset(months=12)
temp_merge = df[['permno', 'time_avail_m', 'epspxq']].copy()
temp_merge.columns = ['permno', 'date_lag12', 'epspxq_l12']
df = df.merge(temp_merge, on=['permno', 'date_lag12'], how='left')
df = df.drop('date_lag12', axis=1)
df['GrTemp'] = df['epspxq'] - df['epspxq_l12']

# Create lagged earnings growth values at 3-month intervals for drift calculation
for n in range(3, 25, 3):
    df[f'date_lag{n}'] = df['time_avail_m'] - pd.DateOffset(months=n)
    temp_merge = df[['permno', 'time_avail_m', 'GrTemp']].copy()
    temp_merge.columns = ['permno', f'date_lag{n}', f'grtemp_lag{n}']
    df = df.merge(temp_merge, on=['permno', f'date_lag{n}'], how='left')
    df = df.drop(f'date_lag{n}', axis=1)

# Calculate average earnings growth over past 8 quarters (drift component)
grtemp_lag_cols = [f'grtemp_lag{n}' for n in range(3, 25, 3)]
df['Drift'] = df[grtemp_lag_cols].mean(axis=1)

# Calculate earnings surprise as growth minus historical drift
df['EarningsSurprise'] = df['epspxq'] - df['epspxq_l12'] - df['Drift']

# Drop grtemp lag columns
df = df.drop(columns=grtemp_lag_cols)

# Create lagged earnings surprise values for volatility calculation
for n in range(3, 25, 3):
    df[f'date_lag{n}'] = df['time_avail_m'] - pd.DateOffset(months=n)
    temp_merge = df[['permno', 'time_avail_m', 'EarningsSurprise']].copy()
    temp_merge.columns = ['permno', f'date_lag{n}', f'es_lag{n}']
    df = df.merge(temp_merge, on=['permno', f'date_lag{n}'], how='left')
    df = df.drop(f'date_lag{n}', axis=1)

# Calculate standard deviation of historical earnings surprises
es_lag_cols = [f'es_lag{n}' for n in range(3, 25, 3)]
df['SD'] = df[es_lag_cols].std(axis=1, ddof=1)

# Standardize earnings surprise by dividing by historical volatility
df['EarningsSurprise'] = df['EarningsSurprise'] / df['SD']
# Replace infinite values with missing when standard deviation is zero
df['EarningsSurprise'] = df['EarningsSurprise'].replace([np.inf, -np.inf], np.nan)

# Keep only observations with valid standardized earnings surprise
df = df.dropna(subset=['EarningsSurprise'])
# Remove observations with missing or near-zero standard deviation
df = df.dropna(subset=['SD'])
df = df[df['SD'] > 1e-10]

# Keep only required columns for final output
result = df[['permno', 'time_avail_m', 'EarningsSurprise']].copy()

# Convert time_avail_m to yyyymm format
result['yyyymm'] = result['time_avail_m'].dt.year * 100 + result['time_avail_m'].dt.month

# Final output format
result = result[['permno', 'yyyymm', 'EarningsSurprise']]

# Convert permno and yyyymm to int
result['permno'] = result['permno'].astype(int)
result['yyyymm'] = result['yyyymm'].astype(int)

# SAVE
result.to_csv('../pyData/Predictors/EarningsSurprise.csv', index=False)

print(f"EarningsSurprise predictor created with {len(result)} observations")