# ABOUTME: Realized minus Implied Volatility spread following Bali and Hovakimian 2009, Table 3 Panel A
# ABOUTME: Calculates difference between realized volatility (past 30 days) and ATM implied volatility

"""
Usage:
    python3 Predictors/ZZ1_RIVolSpread.py

Inputs:
    - pyData/Prep/bali_hovak_imp_vol.csv
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
from config import PATCH_OPTIONM_IV

# Check for Option Metrics patch
if PATCH_OPTIONM_IV:
    print("WARNING: PATCH_OPTIONM_IV is True, using 2023 vintage from openassetpricing")
    print("See https://github.com/OpenSourceAP/CrossSection/issues/156")
    from openassetpricing import OpenAP
    openap = OpenAP(2023)
    df = openap.dl_signal('polars', ['RIVolSpread'])
    df = df.rename({'yyyymm': 'time_avail_m'})
    save_predictor(df, 'RIVolSpread')
    sys.exit()

# Clean OptionMetrics data
df_bh = pd.read_csv('../pyData/Prep/bali_hovak_imp_vol.csv')
df_bh['time_avail_m'] = pd.to_datetime(df_bh['date']).dt.to_period('M').dt.to_timestamp()

# Rename implied volatility column
df_bh = df_bh.rename(columns={'mean_imp_vol': 'impvol'})

# Remove unnecessary columns
df_bh = df_bh.drop(columns=['mean_day', 'nobs', 'ticker'], errors='ignore')

# Reshape to wide format with call/put flags as columns
df_pivot = df_bh.pivot_table(index=['secid', 'time_avail_m'], 
                              columns='cp_flag', 
                              values='impvol',
                              aggfunc='first').reset_index()
df_pivot.columns.name = None
df_pivot = df_pivot.rename(columns={'C': 'impvolC', 'P': 'impvolP'})

# Calculate average implied volatility from calls and puts
df_pivot['impvol'] = (df_pivot['impvolC'] + df_pivot['impvolP']) / 2

# Use call volatility if average is missing but call data exists
df_pivot.loc[df_pivot['impvol'].isna() & df_pivot['impvolC'].notna(), 'impvol'] = df_pivot['impvolC']

# Use put volatility if average is missing but put data exists
df_pivot.loc[df_pivot['impvol'].isna() & df_pivot['impvolP'].notna(), 'impvol'] = df_pivot['impvolP']

# Select final implied volatility columns
temp = df_pivot[['secid', 'time_avail_m', 'impvol']]

# Clean Realized vol data
df_rv = pd.read_csv('../pyData/Predictors/RealizedVol.csv')

# Convert YYYYMM format to date
df_rv['time_avail_m'] = pd.to_datetime(
    df_rv['yyyymm'].astype(str).str[:4] + '-' + 
    df_rv['yyyymm'].astype(str).str[4:] + '-01'
)

# Remove original date column
df_rv = df_rv.drop(columns=['yyyymm'])

# Annualize realized volatility
df_rv['RealizedVol'] = df_rv['RealizedVol'] * np.sqrt(252)

# Store cleaned realized volatility data
temp2 = df_rv

print("Starting ZZ1_RIVolSpread.py...")

# DATA LOAD
print("Loading data...")
# Load master data with security identifiers
master = pd.read_parquet('../pyData/Intermediate/SignalMasterTable.parquet',
                         columns=['permno', 'time_avail_m', 'secid', 'sicCRSP'])

# Add secid-based data (many to one match due to permno-secid not being unique in crsp)
# Remove observations without security identifier
master = master[master['secid'].notna()]

# Merge with implied volatility data
df = master.merge(temp, on=['secid', 'time_avail_m'], how='left')

# Remove closed-end funds (SIC 6720-6730)
df = df[(df['sicCRSP'] < 6720) | (df['sicCRSP'] > 6730)]

# Remove REITs (SIC 6798)
df = df[df['sicCRSP'] != 6798]

# Keep only observations with valid security ID and implied volatility
df = df[df['secid'].notna() & df['impvol'].notna()]

# Merge with realized volatility data
df = df.merge(temp2, on=['permno', 'time_avail_m'], how='left')

# SIGNAL CONSTRUCTION

# Calculate realized minus implied volatility spread
df['RIVolSpread'] = df['RealizedVol'] - df['impvol']

# Keep only valid spread observations
df = df[df['RIVolSpread'].notna()]

# SAVE
save_predictor(df[['permno', 'time_avail_m', 'RIVolSpread']], 'RIVolSpread')
print("ZZ1_RIVolSpread.py completed successfully")