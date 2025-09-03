# ABOUTME: Share repurchases following Ikenberry, Lakonishok, Vermaelen 1995, Table 3, All firms Year 1
# ABOUTME: Binary variable equal to 1 if stock repurchase indicated in cash flow statement
"""
Usage:
    python3 Predictors/ShareRepurchase.py

Inputs:
    - m_aCompustat.parquet: Monthly Compustat data with columns [gvkey, permno, time_avail_m, prstkc]

Outputs:
    - ShareRepurchase.csv: CSV file with columns [permno, yyyymm, ShareRepurchase]
    - ShareRepurchase = 1 if prstkc > 0, 0 if prstkc = 0, missing otherwise
"""

import pandas as pd
import numpy as np

# DATA LOAD
# Load m_aCompustat with specific columns
df = pd.read_parquet('../pyData/Intermediate/m_aCompustat.parquet', 
                     columns=['gvkey', 'permno', 'time_avail_m', 'prstkc'])

# SIGNAL CONSTRUCTION
# Create binary indicator: 1 if positive share repurchases, 0 otherwise
df['ShareRepurchase'] = ((df['prstkc'] > 0) & (df['prstkc'].notna())).astype(int)

# Set to missing when underlying data is missing
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