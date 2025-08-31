# ABOUTME: Excluded Expenses following Doyle, Lundholm and Soliman 2003, Table 5, total exclusions
# ABOUTME: calculates difference between IBES unadjusted earnings and Compustat quarterly EPS

"""
Usage:
    python3 Predictors/ExclExp.py

Inputs:
    - SignalMasterTable.parquet: Monthly master table with gvkey and tickerIBES mappings
    - m_QCompustat.parquet: Monthly quarterly Compustat data with epspiq
    - IBES_UnadjustedActuals.parquet: IBES unadjusted actual earnings with int0a

Outputs:
    - ExclExp.csv: CSV file with columns [permno, yyyymm, ExclExp]
    - ExclExp = int0a - epspiq, winsorized at 1% and 99% levels
"""

import pandas as pd
import numpy as np

# DATA LOAD
df = pd.read_parquet('../pyData/Intermediate/SignalMasterTable.parquet')
df = df[['permno', 'gvkey', 'time_avail_m', 'tickerIBES']].copy()
df = df.dropna(subset=['gvkey'])

# Merge with quarterly Compustat
q_compustat = pd.read_parquet('../pyData/Intermediate/m_QCompustat.parquet')
df = df.merge(q_compustat[['gvkey', 'time_avail_m', 'epspiq']], on=['gvkey', 'time_avail_m'], how='inner')

# Merge with IBES actuals
ibes = pd.read_parquet('../pyData/Intermediate/IBES_UnadjustedActuals.parquet')
df = df.merge(ibes[['tickerIBES', 'time_avail_m', 'int0a']], on=['tickerIBES', 'time_avail_m'], how='left')

# SIGNAL CONSTRUCTION
df['ExclExp'] = df['int0a'] - df['epspiq']

# Winsorize at 1% and 99% (trim extreme values)
q1 = df['ExclExp'].quantile(0.01)
q99 = df['ExclExp'].quantile(0.99)
df['ExclExp'] = np.clip(df['ExclExp'], q1, q99)

# Keep only necessary columns for output
df_final = df[['permno', 'time_avail_m', 'ExclExp']].copy()
df_final = df_final.dropna(subset=['ExclExp'])

# Convert time_avail_m to yyyymm format like other predictors
df_final['yyyymm'] = df_final['time_avail_m'].dt.year * 100 + df_final['time_avail_m'].dt.month

# Convert to integers for consistency with other predictors
df_final['permno'] = df_final['permno'].astype('int64')
df_final['yyyymm'] = df_final['yyyymm'].astype('int64')

# Keep only required columns and set index
df_final = df_final[['permno', 'yyyymm', 'ExclExp']].copy()
df_final = df_final.set_index(['permno', 'yyyymm'])

# SAVE
df_final.to_csv('../pyData/Predictors/ExclExp.csv')

print("ExclExp predictor saved successfully")