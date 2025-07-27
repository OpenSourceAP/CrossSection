# ABOUTME: Translates Herf.do to create industry concentration predictor
# ABOUTME: Run from pyCode/ directory: python3 Predictors/Herf.py

# Run from pyCode/ directory
# Inputs: m_aCompustat.parquet, SignalMasterTable.parquet
# Output: ../pyData/Predictors/Herf.csv

import pandas as pd
import numpy as np
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from utils.data_utils import asrol

# DATA LOAD
df = pd.read_parquet('../pyData/Intermediate/m_aCompustat.parquet')
df = df[['permno', 'time_avail_m', 'sale']].copy()

# Merge with SignalMasterTable
smt = pd.read_parquet('../pyData/Intermediate/SignalMasterTable.parquet')
smt = smt[['permno', 'time_avail_m', 'sicCRSP', 'shrcd']].copy()

df = df.merge(smt, on=['permno', 'time_avail_m'], how='inner')

# Sort for lag operations
df = df.sort_values(['permno', 'time_avail_m'])

# SIGNAL CONSTRUCTION
# Create 4-digit SIC code
df['tempSIC'] = df['sicCRSP'].astype(str)
df['sic3D'] = df['tempSIC'].str[:4]

# Calculate industry sales by SIC and month
df['indsale'] = df.groupby(['sic3D', 'time_avail_m'])['sale'].transform('sum')

# Calculate firm's market share squared
df['temp'] = (df['sale'] / df['indsale']) ** 2

# Calculate Herfindahl index by industry-month
df['tempHerf'] = df.groupby(['sic3D', 'time_avail_m'])['temp'].transform('sum')

# Take 3-year moving average using asrol
df = asrol(df, 'permno', 'time_avail_m', 'tempHerf', 36, 'mean', min_periods=12)
df = df.rename(columns={'mean36_tempHerf': 'Herf'})

# Set to missing if not common stock
df.loc[df['shrcd'] > 11, 'Herf'] = np.nan

# Missing if regulated industry (Barclay and Smith 1995 definition)
df['year'] = df['time_avail_m'].dt.year

# Regulated industries before deregulation dates
df.loc[(df['tempSIC'].isin(['4011', '4210', '4213'])) & (df['year'] <= 1980), 'Herf'] = np.nan
df.loc[(df['tempSIC'] == '4512') & (df['year'] <= 1978), 'Herf'] = np.nan
df.loc[(df['tempSIC'].isin(['4812', '4813'])) & (df['year'] <= 1982), 'Herf'] = np.nan
df.loc[df['tempSIC'].str[:2] == '49', 'Herf'] = np.nan

# Set to missing before 1951 (no sales data)
df.loc[df['year'] < 1951, 'Herf'] = np.nan

# Keep only necessary columns for output
df_final = df[['permno', 'time_avail_m', 'Herf']].copy()
df_final = df_final.dropna(subset=['Herf'])

# Convert time_avail_m to yyyymm format like other predictors
df_final['yyyymm'] = df_final['time_avail_m'].dt.year * 100 + df_final['time_avail_m'].dt.month

# Convert to integers for consistency with other predictors
df_final['permno'] = df_final['permno'].astype('int64')
df_final['yyyymm'] = df_final['yyyymm'].astype('int64')

# Keep only required columns and set index
df_final = df_final[['permno', 'yyyymm', 'Herf']].copy()
df_final = df_final.set_index(['permno', 'yyyymm'])

# SAVE
df_final.to_csv('../pyData/Predictors/Herf.csv')

print("Herf predictor saved successfully")