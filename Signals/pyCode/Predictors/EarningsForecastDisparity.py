# ABOUTME: Translates EarningsForecastDisparity.do from Stata to Python
# ABOUTME: Calculates difference between long-term and short-term earnings forecasts

# How to run: python3 EarningsForecastDisparity.py
# Inputs: ../pyData/Intermediate/IBES_EPS_Unadj.parquet, SignalMasterTable.parquet, IBES_UnadjustedActuals.parquet
# Outputs: ../pyData/Predictors/EarningsForecastDisparity.csv

import pandas as pd
import numpy as np

# Prep IBES data
# Load IBES_EPS_Unadj and filter for short-term forecasts (fpi == "1")
ibes_eps = pd.read_parquet('../pyData/Intermediate/IBES_EPS_Unadj.parquet')
tempIBESshort = ibes_eps[ibes_eps['fpi'] == "1"].copy()
tempIBESshort = tempIBESshort[(tempIBESshort['fpedats'].notna()) & 
                              (tempIBESshort['fpedats'] > tempIBESshort['statpers'] + pd.Timedelta(days=30))]

# Load IBES_EPS_Unadj and filter for long-term forecasts (fpi == "0")
tempIBESlong = ibes_eps[ibes_eps['fpi'] == "0"].copy()
tempIBESlong = tempIBESlong.rename(columns={'meanest': 'fgr5yr'})

print("Starting EarningsForecastDisparity.py...")

# DATA LOAD
print("Loading data...")
# Load SignalMasterTable
signal_master = pd.read_parquet('../pyData/Intermediate/SignalMasterTable.parquet',
                                columns=['permno', 'time_avail_m', 'tickerIBES'])

# Merge with short-term IBES data: keep(master match) -> how='left'
df = pd.merge(signal_master, 
              tempIBESshort[['tickerIBES', 'time_avail_m', 'meanest']], 
              on=['tickerIBES', 'time_avail_m'], 
              how='left', 
              validate='m:1')

# Merge with long-term IBES data: keep(master match) -> how='left'
df = pd.merge(df, 
              tempIBESlong[['tickerIBES', 'time_avail_m', 'fgr5yr']], 
              on=['tickerIBES', 'time_avail_m'], 
              how='left', 
              validate='m:1')

# Load and merge with IBES actuals
ibes_actuals = pd.read_parquet('../pyData/Intermediate/IBES_UnadjustedActuals.parquet',
                               columns=['tickerIBES', 'time_avail_m', 'fy0a'])
df = pd.merge(df, 
              ibes_actuals, 
              on=['tickerIBES', 'time_avail_m'], 
              how='left', 
              validate='m:1')

# SIGNAL CONSTRUCTION
# Calculate tempShort: 100* (meanest - fy0a)/abs(fy0a)
# Handle division by zero like Stata (set to missing)
df['tempShort'] = np.where(df['fy0a'] == 0, np.nan, 100 * (df['meanest'] - df['fy0a']) / abs(df['fy0a']))

# Calculate EarningsForecastDisparity: fgr5yr - tempShort
df['EarningsForecastDisparity'] = df['fgr5yr'] - df['tempShort']

# Create yyyymm variable
df['yyyymm'] = (df['time_avail_m'].dt.year * 100 + df['time_avail_m'].dt.month).astype(int)

# Keep only required columns and remove missing values
# Only drop rows where EarningsForecastDisparity is missing (not intermediate variables)
result = df[['permno', 'yyyymm', 'EarningsForecastDisparity']].dropna(subset=['EarningsForecastDisparity'])

# Save the predictor
result.to_csv('../pyData/Predictors/EarningsForecastDisparity.csv', index=False)