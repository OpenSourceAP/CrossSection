# ABOUTME: Payout Yield following Boudoukh et al. 2007, Table 6B
# ABOUTME: calculates payout yield predictor scaled by market value of equity
"""
Usage:
    python3 Predictors/PayoutYield.py

Inputs:
    - m_aCompustat.parquet: Monthly Compustat data with columns [permno, time_avail_m, dvc, prstkc, pstkrv, sstk, sic, ceq, datadate]
    - SignalMasterTable.parquet: Monthly master table with mve_permco

Outputs:
    - PayoutYield.csv: CSV file with columns [permno, yyyymm, PayoutYield]
    - PayoutYield = (dvc + prstkc + max(pstkrv, 0))/mve_permco, lagged 6 months
    - Excludes financial firms (SIC 6000-6999), ceq <= 0, PayoutYield <= 0, or < 2 years in CRSP
"""

import pandas as pd
import numpy as np

# DATA LOAD
# Load m_aCompustat with specific columns
df = pd.read_parquet('../pyData/Intermediate/m_aCompustat.parquet', 
                     columns=['permno', 'time_avail_m', 'dvc', 'prstkc', 'pstkrv', 'sstk', 'sic', 'ceq', 'datadate'])

# Remove duplicate records within each permno-month combination
df = df.drop_duplicates(['permno', 'time_avail_m'], keep='first')

# Merge market value data from SignalMasterTable
signal_master = pd.read_parquet('../pyData/Intermediate/SignalMasterTable.parquet', 
                                columns=['permno', 'time_avail_m', 'mve_permco'])

df = df.merge(signal_master, on=['permno', 'time_avail_m'], how='inner')

# SIGNAL CONSTRUCTION
# Sort data chronologically within each company
df = df.sort_values(['permno', 'time_avail_m'])

# Create 6-month lagged market value for payout yield calculation
# Use calendar-based lag (6 months prior) rather than positional lag
df['lag6_date'] = df['time_avail_m'] - pd.DateOffset(months=6)

# Create lag lookup table
lag_lookup = df[['permno', 'time_avail_m', 'mve_permco']].copy()
lag_lookup = lag_lookup.rename(columns={'time_avail_m': 'lag6_date', 'mve_permco': 'mve_permco_l6'})

# Merge to get 6-month lagged values
df = df.merge(lag_lookup, on=['permno', 'lag6_date'], how='left')

# Calculate payout yield as total payouts divided by lagged market value
df['PayoutYield'] = (df['dvc'] + df['prstkc'] + df['pstkrv']) / df['mve_permco_l6']

# Set negative or zero payout yields to missing
df.loc[df['PayoutYield'] <= 0, 'PayoutYield'] = np.nan

# FILTER
# Convert SIC codes to numeric format
df['sic'] = pd.to_numeric(df['sic'], errors='coerce')

# Filter out financial companies and require positive book equity
# Include missing book equity values (treated as valid)
df = df[((df['sic'] < 6000) | (df['sic'] >= 7000)) & ((df['ceq'] > 0) | df['ceq'].isna())]

# Sort data chronologically
df = df.sort_values(['permno', 'time_avail_m'])

# Require at least 24 historical observations per company
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