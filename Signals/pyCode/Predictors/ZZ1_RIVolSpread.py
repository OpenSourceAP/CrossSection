# ABOUTME: ZZ1_RIVolSpread.py - Generates RIVolSpread predictor (Realized minus Implied Volatility)
# ABOUTME: Measures difference between realized and implied volatility (Bali-Hovakimian 2009)

"""
Usage:
    python3 Predictors/ZZ1_RIVolSpread.py

Inputs:
    - pyData/Intermediate/OptionMetricsBH.parquet
    - pyData/Predictors/RealizedVol.csv
    - pyData/Intermediate/SignalMasterTable.parquet

Outputs:
    - pyData/Predictors/RIVolSpread.csv - Realized volatility minus implied volatility spread
"""

# needs to be run after RealizedVol

# --------------
import pandas as pd
import numpy as np
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils.save_standardized import save_predictor

# Clean OptionMetrics data
# use OptionMetricsBH, clear
df_bh = pd.read_parquet('../pyData/Intermediate/OptionMetricsBH.parquet')

# rename mean_imp_vol impvol
df_bh = df_bh.rename(columns={'mean_imp_vol': 'impvol'})

# drop mean_day nobs ticker
df_bh = df_bh.drop(columns=['mean_day', 'nobs', 'ticker'], errors='ignore')

# reshape wide impvol, i(secid time_avail_m) j(cp_flag) string
df_pivot = df_bh.pivot_table(index=['secid', 'time_avail_m'], 
                              columns='cp_flag', 
                              values='impvol',
                              aggfunc='first').reset_index()
df_pivot.columns.name = None
df_pivot = df_pivot.rename(columns={'C': 'impvolC', 'P': 'impvolP'})

# implied vol many stage version (this is closest to the text and closest to results)
# gen impvol = (impvolC + impvolP)/2
df_pivot['impvol'] = (df_pivot['impvolC'] + df_pivot['impvolP']) / 2

# replace impvol = impvolC if impvol == . & impvolC != .
df_pivot.loc[df_pivot['impvol'].isna() & df_pivot['impvolC'].notna(), 'impvol'] = df_pivot['impvolC']

# replace impvol = impvolP if impvol == . & impvolP != .
df_pivot.loc[df_pivot['impvol'].isna() & df_pivot['impvolP'].notna(), 'impvol'] = df_pivot['impvolP']

# keep secid time_avail_m impvol
temp = df_pivot[['secid', 'time_avail_m', 'impvol']]

# Clean Realized vol data
# import delimited RealizedVol.csv, clear varnames(1)
df_rv = pd.read_csv('../pyData/Predictors/RealizedVol.csv')

# gen time_avail_m= ym(floor(yyyymm/100), mod(yyyymm, 100))
df_rv['time_avail_m'] = pd.to_datetime(
    df_rv['yyyymm'].astype(str).str[:4] + '-' + 
    df_rv['yyyymm'].astype(str).str[4:] + '-01'
)

# drop yyyymm
df_rv = df_rv.drop(columns=['yyyymm'])

# replace realizedvol = realizedvol * sqrt(252) // annualize
df_rv['RealizedVol'] = df_rv['RealizedVol'] * np.sqrt(252)

# save temp2, replace
temp2 = df_rv

print("Starting ZZ1_RIVolSpread.py...")

# DATA LOAD
print("Loading data...")
# use permno time_avail_m secid sicCRSP using SignalMasterTable, clear
master = pd.read_parquet('../pyData/Intermediate/SignalMasterTable.parquet',
                         columns=['permno', 'time_avail_m', 'secid', 'sicCRSP'])

# Add secid-based data (many to one match due to permno-secid not being unique in crsp)
# drop if mi(secid)
master = master[master['secid'].notna()]

# merge m:1 secid time_avail_m using temp, keep(master match) nogenerate
df = master.merge(temp, on=['secid', 'time_avail_m'], how='left')

# drop closed-end funds (6720 : 6730) and REITs (6798)
# keep if (sicCRSP < 6720 | sicCRSP > 6730)
df = df[(df['sicCRSP'] < 6720) | (df['sicCRSP'] > 6730)]

# keep if sicCRSP != 6798
df = df[df['sicCRSP'] != 6798]

# drop if mi(secid, impvol)
df = df[df['secid'].notna() & df['impvol'].notna()]

# merge m:1 permno time_avail_m using temp2, keep(master match) nogenerate
df = df.merge(temp2, on=['permno', 'time_avail_m'], how='left')

# SIGNAL CONSTRUCTION

# Realized-Implied vol spread = realized volatility - implied volatility
# gen RIVolSpread = realizedvol - impvol
df['RIVolSpread'] = df['RealizedVol'] - df['impvol']

# drop if RIVolSpread == .
df = df[df['RIVolSpread'].notna()]

# label var RIVolSpread "Bali-Hovak (2009) Realized minus Implied Vol"

# SAVE
# do "$pathCode/savepredictor" RIVolSpread
save_predictor(df[['permno', 'time_avail_m', 'RIVolSpread']], 'RIVolSpread')
print("ZZ1_RIVolSpread.py completed successfully")