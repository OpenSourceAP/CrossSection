# ABOUTME: ChAssetTurnover.py - calculates change in asset turnover predictor
# ABOUTME: Line-by-line translation of ChAssetTurnover.do following CLAUDE.md translation philosophy

"""
ChAssetTurnover.py

Usage:
    cd pyCode/
    source .venv/bin/activate
    python3 Predictors/ChAssetTurnover.py

Inputs:
    - ../pyData/Intermediate/m_aCompustat.parquet (columns: gvkey, permno, time_avail_m, rect, invt, aco, ppent, intan, ap, lco, lo, sale)

Outputs:
    - ../pyData/Predictors/ChAssetTurnover.csv (columns: permno, yyyymm, ChAssetTurnover)
"""

import pandas as pd
import numpy as np
from pathlib import Path

# DATA LOAD
df = pd.read_parquet('../pyData/Intermediate/m_aCompustat.parquet', 
                     columns=['gvkey', 'permno', 'time_avail_m', 'rect', 'invt', 'aco', 'ppent', 'intan', 'ap', 'lco', 'lo', 'sale'])

# SIGNAL CONSTRUCTION
# bysort permno time_avail_m: keep if _n == 1  // deletes a few observations
df = df.drop_duplicates(subset=['permno', 'time_avail_m'], keep='first').copy()

# xtset permno time_avail_m
df = df.sort_values(['permno', 'time_avail_m']).reset_index(drop=True)

# Handle missing values consistent with Stata's behavior
# Forward-fill missing ppent values within each permno group
df['ppent'] = df.groupby('permno')['ppent'].ffill()

# gen temp = (rect + invt + aco + ppent + intan - ap - lco - lo) 
df['temp'] = df['rect'] + df['invt'] + df['aco'] + df['ppent'] + df['intan'] - df['ap'] - df['lco'] - df['lo']

# gen AssetTurnover = sale/((temp + l12.temp)/2)
# Use calendar-based lag (12 months back) instead of positional lag
# Optimized version using merge for better performance
df['temp_l12_date'] = df['time_avail_m'] - pd.DateOffset(months=12)
temp_lag = df[['permno', 'time_avail_m', 'temp']].rename(columns={'time_avail_m': 'temp_l12_date', 'temp': 'temp_l12'})
df = df.merge(temp_lag, on=['permno', 'temp_l12_date'], how='left')
df = df.drop(columns=['temp_l12_date'])

df['AssetTurnover'] = df['sale'] / ((df['temp'] + df['temp_l12']) / 2)

# drop temp
df = df.drop(columns=['temp', 'temp_l12'])

# replace AssetTurnover = . if AssetTurnover < 0
df.loc[df['AssetTurnover'] < 0, 'AssetTurnover'] = np.nan

# gen ChAssetTurnover = AssetTurnover - l12.AssetTurnover
df['AssetTurnover_l12_date'] = df['time_avail_m'] - pd.DateOffset(months=12)
asset_turnover_lag = df[['permno', 'time_avail_m', 'AssetTurnover']].rename(columns={'time_avail_m': 'AssetTurnover_l12_date', 'AssetTurnover': 'AssetTurnover_l12'})
df = df.merge(asset_turnover_lag, on=['permno', 'AssetTurnover_l12_date'], how='left')
df = df.drop(columns=['AssetTurnover_l12_date'])

df['ChAssetTurnover'] = df['AssetTurnover'] - df['AssetTurnover_l12']

# Keep only needed columns and non-missing values
result = df[['permno', 'time_avail_m', 'ChAssetTurnover']].copy()
result = result.dropna(subset=['ChAssetTurnover']).copy()

# Convert time_avail_m to yyyymm
result['yyyymm'] = result['time_avail_m'].dt.year * 100 + result['time_avail_m'].dt.month

# Prepare final output
final_result = result[['permno', 'yyyymm', 'ChAssetTurnover']].copy()

# SAVE
Path('../pyData/Predictors').mkdir(parents=True, exist_ok=True)
final_result.to_csv('../pyData/Predictors/ChAssetTurnover.csv', index=False)

print(f"ChAssetTurnover predictor saved: {len(final_result)} observations")