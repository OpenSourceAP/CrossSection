# ABOUTME: Translates OperProfRD.do to create R&D-adjusted operating profitability predictor
# ABOUTME: Run from pyCode/ directory: python3 Predictors/OperProfRD.py

# some confusion about lagging assets or not
# OP 2016 JFE seems to lag assets, but 2015 JFE does not
# Yet no lag implies results much closer to OP

# Run from pyCode/ directory
# Inputs: SignalMasterTable.parquet, m_aCompustat.parquet
# Output: ../pyData/Predictors/OperProfRD.csv

import pandas as pd
import numpy as np

# DATA LOAD
df = pd.read_parquet('../pyData/Intermediate/SignalMasterTable.parquet')
df = df[['permno', 'gvkey', 'time_avail_m', 'exchcd', 'sicCRSP', 'mve_c', 'shrcd']].copy()

# Merge with Compustat
comp = pd.read_parquet('../pyData/Intermediate/m_aCompustat.parquet')
comp = comp[['gvkey', 'permno', 'time_avail_m', 'xrd', 'revt', 'cogs', 'xsga', 'at', 'ceq']].copy()

df = df.merge(comp, on=['permno', 'time_avail_m'], how='inner')

# SIGNAL CONSTRUCTION
# Drop duplicates
df = df.drop_duplicates(subset=['permno', 'time_avail_m'])

# Handle missing R&D (like Stata, only fill xrd with 0)
df['tempXRD'] = df['xrd'].fillna(0)

# Calculate R&D-adjusted operating profitability
df['OperProfRD'] = (df['revt'] - df['cogs'] - df['xsga'] + df['tempXRD']) / df['at']

# Apply filters
df = df[
    (df['shrcd'] <= 11) & 
    (~df['mve_c'].isna()) & 
    (~df['ceq'].isna()) & 
    (~df['at'].isna()) &
    (~((df['sicCRSP'] >= 6000) & (df['sicCRSP'] < 7000)))
].copy()

# Keep only necessary columns for output
df_final = df[['permno', 'time_avail_m', 'OperProfRD']].copy()
df_final = df_final.dropna(subset=['OperProfRD'])

# Convert time_avail_m to yyyymm format like other predictors
df_final['yyyymm'] = df_final['time_avail_m'].dt.year * 100 + df_final['time_avail_m'].dt.month

# Convert to integers for consistency with other predictors
df_final['permno'] = df_final['permno'].astype('int64')
df_final['yyyymm'] = df_final['yyyymm'].astype('int64')

# Keep only required columns and set index
df_final = df_final[['permno', 'yyyymm', 'OperProfRD']].copy()
df_final = df_final.set_index(['permno', 'yyyymm'])

# SAVE
df_final.to_csv('../pyData/Predictors/OperProfRD.csv')

print("OperProfRD predictor saved successfully")