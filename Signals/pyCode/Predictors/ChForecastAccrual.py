# ABOUTME: ChForecastAccrual.py - calculates change in forecast and accrual predictor
# ABOUTME: Line-by-line translation of ChForecastAccrual.do following CLAUDE.md translation philosophy

"""
ChForecastAccrual.py

Usage:
    cd pyCode/
    source .venv/bin/activate
    python3 Predictors/ChForecastAccrual.py

Inputs:
    - ../pyData/Intermediate/IBES_EPS_Unadj.parquet
    - ../pyData/Intermediate/m_aCompustat.parquet
    - ../pyData/Intermediate/SignalMasterTable.parquet

Outputs:
    - ../pyData/Predictors/ChForecastAccrual.csv (columns: permno, yyyymm, ChForecastAccrual)
"""

import pandas as pd
import numpy as np
from pathlib import Path

# Prep IBES data
# use "$pathDataIntermediate/IBES_EPS_Unadj", replace
ibes_df = pd.read_parquet('../pyData/Intermediate/IBES_EPS_Unadj.parquet')

# keep if fpi == "1" 
ibes_df = ibes_df[ibes_df['fpi'] == "1"].copy()

# save "$pathtemp/temp", replace
temp_ibes = ibes_df.copy()

# DATA LOAD
# use permno time_avail_m act che lct dlc txp at using "$pathDataIntermediate/m_aCompustat", clear
df = pd.read_parquet('../pyData/Intermediate/m_aCompustat.parquet', 
                     columns=['permno', 'time_avail_m', 'act', 'che', 'lct', 'dlc', 'txp', 'at'])

# bysort permno time_avail_m: keep if _n == 1  // deletes a few observations
df = df.drop_duplicates(subset=['permno', 'time_avail_m'], keep='first').copy()

# merge 1:1 permno time_avail_m using "$pathDataIntermediate/SignalMasterTable", keep(master match) nogenerate keepusing(tickerIBES)
signal_master = pd.read_parquet('../pyData/Intermediate/SignalMasterTable.parquet', 
                               columns=['permno', 'time_avail_m', 'tickerIBES'])
df = pd.merge(df, signal_master, on=['permno', 'time_avail_m'], how='left')

# merge m:1 tickerIBES time_avail_m using "$pathtemp/temp", keep(master match) nogenerate keepusing(meanest)
# Stata keep(master match) means keep all master observations plus matches (LEFT join)
temp_ibes_subset = temp_ibes[['tickerIBES', 'time_avail_m', 'meanest']].copy()
df = pd.merge(df, temp_ibes_subset, on=['tickerIBES', 'time_avail_m'], how='left')

# SIGNAL CONSTRUCTION
# xtset permno time_avail_m
df = df.sort_values(['permno', 'time_avail_m']).reset_index(drop=True)

# gen tempAccruals = ( (act - l12.act) - (che - l12.che) - ( (lct - l12.lct) - (dlc - l12.dlc) - (txp - l12.txp) )) / ( (at + l12.at)/2)
# Use calendar-based lag (12 months back) instead of positional lag
def create_calendar_lag(df, var_name, months=12):
    df[f'{var_name}_l{months}_date'] = df['time_avail_m'] - pd.DateOffset(months=months)
    lag_data = df[['permno', 'time_avail_m', var_name]].rename(
        columns={'time_avail_m': f'{var_name}_l{months}_date', var_name: f'{var_name}_l{months}'})
    df = df.merge(lag_data, on=['permno', f'{var_name}_l{months}_date'], how='left')
    df = df.drop(columns=[f'{var_name}_l{months}_date'])
    return df

for var in ['act', 'che', 'lct', 'dlc', 'txp', 'at']:
    df = create_calendar_lag(df, var, 12)

df['tempAccruals'] = ((df['act'] - df['act_l12']) - (df['che'] - df['che_l12']) - 
                      ((df['lct'] - df['lct_l12']) - (df['dlc'] - df['dlc_l12']) - (df['txp'] - df['txp_l12']))) / ((df['at'] + df['at_l12']) / 2)

# egen tempsort = fastxtile(tempAccruals), by(time_avail_m) n(2)
def fastxtile(series, n_quantiles=2):
    try:
        series_clean = series.replace([np.inf, -np.inf], np.nan)
        return pd.qcut(series_clean, q=n_quantiles, labels=False, duplicates='drop') + 1
    except Exception:
        return pd.Series(np.nan, index=series.index)

df['tempsort'] = df.groupby('time_avail_m')['tempAccruals'].transform(lambda x: fastxtile(x, 2))

# gen ChForecastAccrual = 1 if meanest > l.meanest & !mi(meanest) & !mi(l.meanest)
# Use calendar-based lag (1 month back) instead of positional lag
df = create_calendar_lag(df, 'meanest', 1)
df['meanest_l'] = df['meanest_l1']
df = df.drop(columns=['meanest_l1'])
df['ChForecastAccrual'] = np.nan

# Set to 1 if forecast increased
mask_increase = (df['meanest'] > df['meanest_l']) & df['meanest'].notna() & df['meanest_l'].notna()
df.loc[mask_increase, 'ChForecastAccrual'] = 1

# replace ChForecastAccrual = 0 if meanest < l.meanest & !mi(meanest) & !mi(l.meanest)
mask_decrease = (df['meanest'] < df['meanest_l']) & df['meanest'].notna() & df['meanest_l'].notna()
df.loc[mask_decrease, 'ChForecastAccrual'] = 0

# replace ChForecastAccrual = . if tempsort == 1
df.loc[df['tempsort'] == 1, 'ChForecastAccrual'] = np.nan

# Keep only needed columns and non-missing values
result = df[['permno', 'time_avail_m', 'ChForecastAccrual']].copy()
result = result.dropna(subset=['ChForecastAccrual']).copy()

# Convert time_avail_m to yyyymm
result['yyyymm'] = result['time_avail_m'].dt.year * 100 + result['time_avail_m'].dt.month

# Prepare final output
final_result = result[['permno', 'yyyymm', 'ChForecastAccrual']].copy()

# SAVE
Path('../pyData/Predictors').mkdir(parents=True, exist_ok=True)
final_result.to_csv('../pyData/Predictors/ChForecastAccrual.csv', index=False)

print(f"ChForecastAccrual predictor saved: {len(final_result)} observations")