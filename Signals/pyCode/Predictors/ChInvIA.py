# ABOUTME: ChInvIA.py - calculates change in capital investment (industry adjusted) predictor
# ABOUTME: Line-by-line translation of ChInvIA.do following CLAUDE.md translation philosophy

"""
ChInvIA.py

Usage:
    cd pyCode/
    source .venv/bin/activate
    python3 Predictors/ChInvIA.py

Inputs:
    - ../pyData/Intermediate/m_aCompustat.parquet (columns: gvkey, permno, time_avail_m, capx, ppent, at)
    - ../pyData/Intermediate/SignalMasterTable.parquet (columns: permno, time_avail_m, sicCRSP)

Outputs:
    - ../pyData/Predictors/ChInvIA.csv (columns: permno, yyyymm, ChInvIA)
"""

import pandas as pd
import numpy as np
from pathlib import Path

# DATA LOAD
# use gvkey permno time_avail_m capx ppent at using "$pathDataIntermediate/m_aCompustat", clear
df = pd.read_parquet('../pyData/Intermediate/m_aCompustat.parquet', 
                     columns=['gvkey', 'permno', 'time_avail_m', 'capx', 'ppent', 'at'])

# merge 1:1 permno time_avail_m using "$pathDataIntermediate/SignalMasterTable", keep(using match) nogenerate keepusing(sicCRSP)
signal_master = pd.read_parquet('../pyData/Intermediate/SignalMasterTable.parquet', 
                               columns=['permno', 'time_avail_m', 'sicCRSP'])
df = pd.merge(signal_master, df, on=['permno', 'time_avail_m'], how='inner')

# SIGNAL CONSTRUCTION
# xtset permno time_avail_m
df = df.sort_values(['permno', 'time_avail_m']).reset_index(drop=True)

# tostring sicCRSP, replace
df['sicCRSP'] = df['sicCRSP'].astype(str)

# gen sic2D = substr(sicCRSP,1,2)
df['sic2D'] = df['sicCRSP'].str[:2]

# replace capx = ppent - l12.ppent if capx ==.
# Use calendar-based lag (12 months back) instead of positional lag
df['ppent_l12_date'] = df['time_avail_m'] - pd.DateOffset(months=12)
ppent_lag = df[['permno', 'time_avail_m', 'ppent']].rename(columns={'time_avail_m': 'ppent_l12_date', 'ppent': 'ppent_l12'})
df = df.merge(ppent_lag, on=['permno', 'ppent_l12_date'], how='left')
df = df.drop(columns=['ppent_l12_date'])

df['capx'] = df['capx'].fillna(df['ppent'] - df['ppent_l12'])

# gen pchcapx = (capx- .5*(l12.capx + l24.capx))/(.5*(l12.capx + l24.capx))
# Use calendar-based lags for capx
df['capx_l12_date'] = df['time_avail_m'] - pd.DateOffset(months=12)
capx_lag12 = df[['permno', 'time_avail_m', 'capx']].rename(columns={'time_avail_m': 'capx_l12_date', 'capx': 'capx_l12'})
df = df.merge(capx_lag12, on=['permno', 'capx_l12_date'], how='left')
df = df.drop(columns=['capx_l12_date'])

df['capx_l24_date'] = df['time_avail_m'] - pd.DateOffset(months=24)
capx_lag24 = df[['permno', 'time_avail_m', 'capx']].rename(columns={'time_avail_m': 'capx_l24_date', 'capx': 'capx_l24'})
df = df.merge(capx_lag24, on=['permno', 'capx_l24_date'], how='left')
df = df.drop(columns=['capx_l24_date'])
df['avg_lag_capx'] = 0.5 * (df['capx_l12'] + df['capx_l24'])

# Handle division by zero - in Stata, division by zero results in missing
df['pchcapx'] = np.where(
    df['avg_lag_capx'] == 0,
    np.nan,
    (df['capx'] - df['avg_lag_capx']) / df['avg_lag_capx']
)

# replace pchcapx = (capx-l12.capx)/l12.capx if mi(pchcapx)
mask_missing = df['pchcapx'].isna()
df.loc[mask_missing, 'pchcapx'] = np.where(
    df.loc[mask_missing, 'capx_l12'] == 0,
    np.nan,
    (df.loc[mask_missing, 'capx'] - df.loc[mask_missing, 'capx_l12']) / df.loc[mask_missing, 'capx_l12']
)

# egen temp = mean(pchcapx), by(sic2D time_avail_m)
df['temp'] = df.groupby(['sic2D', 'time_avail_m'])['pchcapx'].transform('mean')

# gen ChInvIA = pchcapx - temp
df['ChInvIA'] = df['pchcapx'] - df['temp']

# drop temp
df = df.drop(columns=['temp'])

# Keep only needed columns and non-missing values
result = df[['permno', 'time_avail_m', 'ChInvIA']].copy()
result = result.dropna(subset=['ChInvIA']).copy()

# Convert time_avail_m to yyyymm
result['yyyymm'] = result['time_avail_m'].dt.year * 100 + result['time_avail_m'].dt.month

# Prepare final output
final_result = result[['permno', 'yyyymm', 'ChInvIA']].copy()

# SAVE
Path('../pyData/Predictors').mkdir(parents=True, exist_ok=True)
final_result.to_csv('../pyData/Predictors/ChInvIA.csv', index=False)

print(f"ChInvIA predictor saved: {len(final_result)} observations")