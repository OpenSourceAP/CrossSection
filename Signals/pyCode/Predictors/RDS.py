# ABOUTME: RDS.py - calculates Real Dirty Surplus measure
# ABOUTME: Real dirty surplus incorporating changes in equity, dirty surplus, earnings, dividends, and share issuance

"""
RDS predictor calculation

Usage:
    cd pyCode/
    source .venv/bin/activate
    python3 Predictors/RDS.py

Inputs:
    - ../pyData/Intermediate/m_aCompustat.parquet (permno, gvkey, time_avail_m, recta, ceq, ni, dvp, dvc, prcc_f, csho, msa)
    - ../pyData/Intermediate/CompustatPensions.parquet (gvkey, year, pcupsu, paddml)

Outputs:
    - ../pyData/Predictors/RDS.csv (permno, yyyymm, RDS)
"""

import pandas as pd
import numpy as np

# DATA LOAD
# Load m_aCompustat data
compustat_df = pd.read_parquet("../pyData/Intermediate/m_aCompustat.parquet", 
                               columns=['permno', 'gvkey', 'time_avail_m', 'recta', 'ceq', 'ni', 'dvp', 'dvc', 'prcc_f', 'csho', 'msa'])

# Create year variable for pension data merge
compustat_df['year'] = compustat_df['time_avail_m'].dt.year

# Merge with CompustatPensions
pensions_df = pd.read_parquet("../pyData/Intermediate/CompustatPensions.parquet", 
                             columns=['gvkey', 'year', 'pcupsu', 'paddml'])
df = compustat_df.merge(pensions_df, on=['gvkey', 'year'], how='left')

# SIGNAL CONSTRUCTION
# Sort data for lag operations
df = df.sort_values(['permno', 'time_avail_m'])

# Replace missing recta with 0
df['recta'] = df['recta'].fillna(0)

# Create 12-month lags using time-based approach
df['time_lag12'] = df['time_avail_m'] - pd.DateOffset(months=12)

# Create lag data for merge
lag_vars = ['msa', 'recta', 'pcupsu', 'paddml', 'ceq', 'csho']
lag_data = df[['permno', 'time_avail_m'] + lag_vars].copy()
lag_data.columns = ['permno', 'time_lag12'] + [f'l12_{var}' for var in lag_vars]

# Merge to get lagged values
df = df.merge(lag_data, on=['permno', 'time_lag12'], how='left')

# Calculate dirty surplus (DS)
# min(pcupsu - paddml, 0) - min(l12.pcupsu - l12.paddml, 0)
# Stata treats missing pension data as 0 in the min() function
def stata_min_pension(pcupsu, paddml):
    if pd.isna(pcupsu) or pd.isna(paddml):
        return 0  # Stata treats missing pension data as 0 in min() function
    return min(pcupsu - paddml, 0)

pension_current = df.apply(lambda row: stata_min_pension(row['pcupsu'], row['paddml']), axis=1)
pension_lag = df.apply(lambda row: stata_min_pension(row['l12_pcupsu'], row['l12_paddml']), axis=1)

df['DS'] = ((df['msa'] - df['l12_msa']) + 
            (df['recta'] - df['l12_recta']) + 
            0.65 * (pension_current - pension_lag))

# Calculate RDS
df['RDS'] = ((df['ceq'] - df['l12_ceq']) - df['DS'] - (df['ni'] - df['dvp']) + 
             df['dvc'] - df['prcc_f'] * (df['csho'] - df['l12_csho']))

# Drop missing values
df = df.dropna(subset=['RDS'])

# Convert time_avail_m to yyyymm
df['yyyymm'] = df['time_avail_m'].dt.year * 100 + df['time_avail_m'].dt.month

# Keep required columns and order
df = df[['permno', 'yyyymm', 'RDS']].copy()

# SAVE
df.to_csv("../pyData/Predictors/RDS.csv", index=False)
print(f"RDS: Saved {len(df):,} observations")