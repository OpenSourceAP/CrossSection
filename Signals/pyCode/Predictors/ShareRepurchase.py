# ABOUTME: Translates ShareRepurchase.do to calculate share repurchase indicator
# ABOUTME: Run with: python3 Predictors/ShareRepurchase.py

# Calculates binary indicator for share repurchases using Compustat data
# Input: ../pyData/Intermediate/m_aCompustat.parquet
# Output: ../pyData/Predictors/ShareRepurchase.csv

import pandas as pd
import numpy as np

# DATA LOAD
# Load m_aCompustat with specific columns
df = pd.read_parquet('../pyData/Intermediate/m_aCompustat.parquet', 
                     columns=['gvkey', 'permno', 'time_avail_m', 'prstkc'])

# SIGNAL CONSTRUCTION
# gen ShareRepurchase = (prstkc > 0 & !mi(prstkc))
df['ShareRepurchase'] = ((df['prstkc'] > 0) & (df['prstkc'].notna())).astype(int)

# replace ShareRepurchase = . if mi(prstkc)
df.loc[df['prstkc'].isna(), 'ShareRepurchase'] = np.nan

# Keep only observations with valid ShareRepurchase (not missing)
result = df.dropna(subset=['ShareRepurchase'])

# Keep only required columns for final output
result = result[['permno', 'time_avail_m', 'ShareRepurchase']].copy()

# Convert time_avail_m to yyyymm format
result['yyyymm'] = result['time_avail_m'].dt.year * 100 + result['time_avail_m'].dt.month

# Final format matching Stata output
result = result[['permno', 'yyyymm', 'ShareRepurchase']]

# Convert permno and yyyymm to int, ShareRepurchase to int
result['permno'] = result['permno'].astype(int)
result['yyyymm'] = result['yyyymm'].astype(int)
result['ShareRepurchase'] = result['ShareRepurchase'].astype(int)

# SAVE
result.to_csv('../pyData/Predictors/ShareRepurchase.csv', index=False)

print(f"ShareRepurchase predictor created with {len(result)} observations")