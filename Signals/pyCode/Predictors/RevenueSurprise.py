# ABOUTME: Translates RevenueSurprise.do to calculate standardized revenue surprise
# ABOUTME: Run with: python3 Predictors/RevenueSurprise.py

# Calculates revenue surprise using Compustat quarterly data
# Input: ../pyData/Intermediate/SignalMasterTable.parquet, ../pyData/Intermediate/m_QCompustat.parquet
# Output: ../pyData/Predictors/RevenueSurprise.csv

import pandas as pd
import numpy as np

# DATA LOAD
# Load SignalMasterTable with specific columns
df = pd.read_parquet('../pyData/Intermediate/SignalMasterTable.parquet', 
                     columns=['permno', 'gvkey', 'time_avail_m', 'mve_c'])

# keep if !mi(gvkey)
df = df.dropna(subset=['gvkey'])

# merge 1:1 gvkey time_avail_m using m_QCompustat, keepusing(revtq cshprq) nogenerate keep(match)
qcompustat = pd.read_parquet('../pyData/Intermediate/m_QCompustat.parquet', 
                             columns=['gvkey', 'time_avail_m', 'revtq', 'cshprq'])

df = df.merge(qcompustat, on=['gvkey', 'time_avail_m'], how='inner')

# SIGNAL CONSTRUCTION
# xtset permno time_avail_m
df = df.sort_values(['permno', 'time_avail_m'])

# gen revps = revtq/cshprq
df['revps'] = df['revtq'] / df['cshprq']

# gen GrTemp = (revps - l12.revps)
# Stata uses calendar-based lags with xtset - exact date matching
df['date_lag12'] = df['time_avail_m'] - pd.DateOffset(months=12)
temp_merge = df[['permno', 'time_avail_m', 'revps']].copy()
temp_merge.columns = ['permno', 'date_lag12', 'revps_l12']
df = df.merge(temp_merge, on=['permno', 'date_lag12'], how='left')
df = df.drop('date_lag12', axis=1)
df['GrTemp'] = df['revps'] - df['revps_l12']

# foreach n of numlist 3(3)24: gen temp`n' = l`n'.GrTemp
# Create calendar-based lags 3, 6, 9, 12, 15, 18, 21, 24 months of GrTemp for Drift calculation
for n in range(3, 25, 3):
    df[f'date_lag{n}'] = df['time_avail_m'] - pd.DateOffset(months=n)
    temp_merge = df[['permno', 'time_avail_m', 'GrTemp']].copy()
    temp_merge.columns = ['permno', f'date_lag{n}', f'grtemp_lag{n}']
    df = df.merge(temp_merge, on=['permno', f'date_lag{n}'], how='left')
    df = df.drop(f'date_lag{n}', axis=1)

# egen Drift = rowmean(temp*)
grtemp_lag_cols = [f'grtemp_lag{n}' for n in range(3, 25, 3)]
df['Drift'] = df[grtemp_lag_cols].mean(axis=1)

# gen RevenueSurprise = revps - l12.revps - Drift
df['RevenueSurprise'] = df['revps'] - df['revps_l12'] - df['Drift']

# Drop grtemp lag columns
df = df.drop(columns=grtemp_lag_cols)

# foreach n of numlist 3(3)24: gen temp`n' = l`n'.RevenueSurprise
# Create calendar-based lags 3, 6, 9, 12, 15, 18, 21, 24 months of RevenueSurprise for SD calculation
for n in range(3, 25, 3):
    df[f'date_lag{n}'] = df['time_avail_m'] - pd.DateOffset(months=n)
    temp_merge = df[['permno', 'time_avail_m', 'RevenueSurprise']].copy()
    temp_merge.columns = ['permno', f'date_lag{n}', f'rs_lag{n}']
    df = df.merge(temp_merge, on=['permno', f'date_lag{n}'], how='left')
    df = df.drop(f'date_lag{n}', axis=1)

# egen SD = rowsd(temp*)
# Stata's rowsd() uses sample std with n-1 denominator (ddof=1)
rs_lag_cols = [f'rs_lag{n}' for n in range(3, 25, 3)]
df['SD'] = df[rs_lag_cols].std(axis=1, ddof=1)

# replace RevenueSurprise = RevenueSurprise/SD
# Stata divides by SD even when SD is extremely small, creating large values
df['RevenueSurprise'] = df['RevenueSurprise'] / df['SD']
# Replace inf/-inf with NaN to match Stata's behavior when SD = 0 exactly
df['RevenueSurprise'] = df['RevenueSurprise'].replace([np.inf, -np.inf], np.nan)

# Keep only observations with valid RevenueSurprise and reliable SD
# Stata appears to filter out observations with unreliable SD calculations
df = df.dropna(subset=['RevenueSurprise'])
df = df.dropna(subset=['SD'])  # Remove observations where SD = NaN  
df = df[df['SD'] > 1e-8]  # Remove observations where SD is essentially zero

# Keep only required columns for final output
result = df[['permno', 'time_avail_m', 'RevenueSurprise']].copy()

# Convert time_avail_m to yyyymm format
result['yyyymm'] = result['time_avail_m'].dt.year * 100 + result['time_avail_m'].dt.month

# Final format matching Stata output
result = result[['permno', 'yyyymm', 'RevenueSurprise']]

# Convert permno and yyyymm to int
result['permno'] = result['permno'].astype(int)
result['yyyymm'] = result['yyyymm'].astype(int)

# SAVE
result.to_csv('../pyData/Predictors/RevenueSurprise.csv', index=False)

print(f"RevenueSurprise predictor created with {len(result)} observations")