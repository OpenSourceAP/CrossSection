# ABOUTME: Translates EarningsSurprise.do to calculate standardized earnings surprise
# ABOUTME: Run with: python3 Predictors/EarningsSurprise.py

# Calculates earnings surprise using Compustat quarterly data
# Input: ../pyData/Intermediate/SignalMasterTable.parquet, ../pyData/Intermediate/m_QCompustat.parquet
# Output: ../pyData/Predictors/EarningsSurprise.csv

import pandas as pd
import numpy as np

# DATA LOAD
# Load SignalMasterTable with specific columns
df = pd.read_parquet('../pyData/Intermediate/SignalMasterTable.parquet', 
                     columns=['permno', 'gvkey', 'time_avail_m'])

# keep if !mi(gvkey)
df = df.dropna(subset=['gvkey'])

# merge 1:1 gvkey time_avail_m using m_QCompustat, keepusing(epspxq) nogenerate keep(match)
qcompustat = pd.read_parquet('../pyData/Intermediate/m_QCompustat.parquet', 
                             columns=['gvkey', 'time_avail_m', 'epspxq'])

df = df.merge(qcompustat, on=['gvkey', 'time_avail_m'], how='inner')

# SIGNAL CONSTRUCTION
# xtset permno time_avail_m
df = df.sort_values(['permno', 'time_avail_m'])

# gen GrTemp = (epspxq - l12.epspxq)
# Stata uses calendar-based lags with xtset - exact date matching
df['date_lag12'] = df['time_avail_m'] - pd.DateOffset(months=12)
temp_merge = df[['permno', 'time_avail_m', 'epspxq']].copy()
temp_merge.columns = ['permno', 'date_lag12', 'epspxq_l12']
df = df.merge(temp_merge, on=['permno', 'date_lag12'], how='left')
df = df.drop('date_lag12', axis=1)
df['GrTemp'] = df['epspxq'] - df['epspxq_l12']

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

# gen EarningsSurprise = epspxq - l12.epspxq - Drift
df['EarningsSurprise'] = df['epspxq'] - df['epspxq_l12'] - df['Drift']

# Drop grtemp lag columns
df = df.drop(columns=grtemp_lag_cols)

# foreach n of numlist 3(3)24: gen temp`n' = l`n'.EarningsSurprise
# Create calendar-based lags 3, 6, 9, 12, 15, 18, 21, 24 months of EarningsSurprise for SD calculation
for n in range(3, 25, 3):
    df[f'date_lag{n}'] = df['time_avail_m'] - pd.DateOffset(months=n)
    temp_merge = df[['permno', 'time_avail_m', 'EarningsSurprise']].copy()
    temp_merge.columns = ['permno', f'date_lag{n}', f'es_lag{n}']
    df = df.merge(temp_merge, on=['permno', f'date_lag{n}'], how='left')
    df = df.drop(f'date_lag{n}', axis=1)

# egen SD = rowsd(temp*)
# Stata's rowsd() uses sample std with n-1 denominator (ddof=1)
es_lag_cols = [f'es_lag{n}' for n in range(3, 25, 3)]
df['SD'] = df[es_lag_cols].std(axis=1, ddof=1)

# replace EarningsSurprise = EarningsSurprise/SD
# Stata divides by SD even when SD is extremely small, creating large values
df['EarningsSurprise'] = df['EarningsSurprise'] / df['SD']
# Replace inf/-inf with NaN to match Stata's behavior when SD = 0 exactly
df['EarningsSurprise'] = df['EarningsSurprise'].replace([np.inf, -np.inf], np.nan)

# Keep only observations with valid EarningsSurprise and reliable SD
# Stata appears to filter out observations with unreliable SD calculations
df = df.dropna(subset=['EarningsSurprise'])
df = df.dropna(subset=['SD'])  # Remove observations where SD = NaN  
df = df[df['SD'] > 1e-10]  # Remove observations where SD is essentially zero

# Keep only required columns for final output
result = df[['permno', 'time_avail_m', 'EarningsSurprise']].copy()

# Convert time_avail_m to yyyymm format
result['yyyymm'] = result['time_avail_m'].dt.year * 100 + result['time_avail_m'].dt.month

# Final format matching Stata output
result = result[['permno', 'yyyymm', 'EarningsSurprise']]

# Convert permno and yyyymm to int
result['permno'] = result['permno'].astype(int)
result['yyyymm'] = result['yyyymm'].astype(int)

# SAVE
result.to_csv('../pyData/Predictors/EarningsSurprise.csv', index=False)

print(f"EarningsSurprise predictor created with {len(result)} observations")