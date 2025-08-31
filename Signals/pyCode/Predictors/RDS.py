# ABOUTME: Real Dirty Surplus following Landsman et al. 2011, Table 4
# ABOUTME: calculates real dirty surplus as change in book equity minus dirty surplus minus earnings plus dividends

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

# Track which values were originally missing to handle edge cases
df['recta_orig_missing'] = df['recta'].isna()
df['msa_orig_missing'] = df['msa'].isna()

# Replace missing recta and msa with 0
df['recta'] = df['recta'].fillna(0)
df['msa'] = df['msa'].fillna(0)

# Create 12-month lags using time-based approach
df['time_lag12'] = df['time_avail_m'] - pd.DateOffset(months=12)

# Create lag data for merge (include missing flags)
lag_vars = ['msa', 'recta', 'pcupsu', 'paddml', 'ceq', 'csho']
lag_data = df[['permno', 'time_avail_m'] + lag_vars + ['recta_orig_missing', 'msa_orig_missing']].copy()
lag_data.columns = (['permno', 'time_lag12'] + [f'l12_{var}' for var in lag_vars] + 
                   ['l12_recta_orig_missing', 'l12_msa_orig_missing'])

# Merge to get lagged values
df = df.merge(lag_data, on=['permno', 'time_lag12'], how='left')

# Calculate dirty surplus (DS)
# min(pcupsu - paddml, 0) - min(l12.pcupsu - l12.paddml, 0)
# Handle missing pension data by treating as 0 in the min() function
def min_pension(pcupsu, paddml):
    if pd.isna(pcupsu) or pd.isna(paddml):
        return 0  # Treat missing pension data as 0 in min() function
    return min(pcupsu - paddml, 0)

pension_current = df.apply(lambda row: min_pension(row['pcupsu'], row['paddml']), axis=1)
pension_lag = df.apply(lambda row: min_pension(row['l12_pcupsu'], row['l12_paddml']), axis=1)

# Note: msa and recta are already filled with 0 above for current values
# But we should NOT fill lag values - let NaN propagate naturally
df['DS'] = ((df['msa'] - df['l12_msa']) + 
            (df['recta'] - df['l12_recta']) + 
            0.65 * (pension_current - pension_lag))

# Calculate RDS
df['RDS'] = ((df['ceq'] - df['l12_ceq']) - df['DS'] - (df['ni'] - df['dvp']) + 
             df['dvc'] - df['prcc_f'] * (df['csho'] - df['l12_csho']))

# Filter out observations where both current and lagged msa/recta were originally missing
# This prevents meaningless 0-0=0 calculations
both_missing_mask = (
    (df['recta_orig_missing'] & df['l12_recta_orig_missing'].fillna(True).infer_objects(copy=False)) &
    (df['msa_orig_missing'] & df['l12_msa_orig_missing'].fillna(True).infer_objects(copy=False))
)

# Set RDS to missing for these problematic cases
df.loc[both_missing_mask, 'RDS'] = np.nan

# Drop missing values
df = df.dropna(subset=['RDS'])

# Convert time_avail_m to yyyymm
df['yyyymm'] = df['time_avail_m'].dt.year * 100 + df['time_avail_m'].dt.month

# Keep required columns and order
df = df[['permno', 'yyyymm', 'RDS']].copy()

# SAVE
df.to_csv("../pyData/Predictors/RDS.csv", index=False)
print(f"RDS: Saved {len(df):,} observations")