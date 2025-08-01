# ABOUTME: ChNAnalyst.py - calculates decline in analyst coverage predictor
# ABOUTME: Line-by-line translation of ChNAnalyst.do following CLAUDE.md translation philosophy

"""
ChNAnalyst.py

Usage:
    cd pyCode/
    source .venv/bin/activate
    python3 Predictors/ChNAnalyst.py

Inputs:
    - ../pyData/Intermediate/IBES_EPS_Unadj.parquet
    - ../pyData/Intermediate/SignalMasterTable.parquet

Outputs:
    - ../pyData/Predictors/ChNAnalyst.csv (columns: permno, yyyymm, ChNAnalyst)
"""

import pandas as pd
import numpy as np
from pathlib import Path

# Prep IBES data
# use "$pathDataIntermediate/IBES_EPS_Unadj", replace
ibes_df = pd.read_parquet('../pyData/Intermediate/IBES_EPS_Unadj.parquet')

# keep if fpi == "1" 
ibes_df = ibes_df[ibes_df['fpi'] == "1"].copy()

# gen tmp = 1 if fpedats != . & fpedats > statpers + 30
ibes_df['tmp'] = np.where(
    ibes_df['fpedats'].notna() & (ibes_df['fpedats'] > ibes_df['statpers'] + pd.Timedelta(days=30)),
    1, 
    np.nan
)

# bys tickerIBES: replace meanest = meanest[_n-1] if mi(tmp) & fpedats == fpedats[_n-1]
ibes_df = ibes_df.sort_values(['tickerIBES', 'time_avail_m'])
ibes_df['meanest_lag1'] = ibes_df.groupby('tickerIBES')['meanest'].shift(1)
ibes_df['fpedats_lag1'] = ibes_df.groupby('tickerIBES')['fpedats'].shift(1)

mask_replace = ibes_df['tmp'].isna() & (ibes_df['fpedats'] == ibes_df['fpedats_lag1'])
ibes_df.loc[mask_replace, 'meanest'] = ibes_df.loc[mask_replace, 'meanest_lag1']

# drop tmp
ibes_df = ibes_df.drop(columns=['tmp', 'meanest_lag1', 'fpedats_lag1'])

# keep tickerIBES time_avail_m numest statpers fpedats
temp_ibes = ibes_df[['tickerIBES', 'time_avail_m', 'numest', 'statpers', 'fpedats']].copy()

# DATA LOAD
# use permno time_avail_m tickerIBES mve_c using "$pathDataIntermediate/SignalMasterTable", clear
df = pd.read_parquet('../pyData/Intermediate/SignalMasterTable.parquet', 
                     columns=['permno', 'time_avail_m', 'tickerIBES', 'mve_c'])

# merge m:1 tickerIBES time_avail_m using "$pathtemp/temp", keep(master match) nogenerate 
df = pd.merge(df, temp_ibes, on=['tickerIBES', 'time_avail_m'], how='left')

# SIGNAL CONSTRUCTION
# xtset permno time_avail_m
df = df.sort_values(['permno', 'time_avail_m']).reset_index(drop=True)

# gen ChNAnalyst = 1 if numest < l3.numest & !mi(l3.numest)
# Use calendar-based lag (3 months back) instead of positional lag
df['numest_l3_date'] = df['time_avail_m'] - pd.DateOffset(months=3)
numest_lag = df[['permno', 'time_avail_m', 'numest']].rename(columns={'time_avail_m': 'numest_l3_date', 'numest': 'numest_l3'})
df = df.merge(numest_lag, on=['permno', 'numest_l3_date'], how='left')
df = df.drop(columns=['numest_l3_date'])
df['ChNAnalyst'] = np.nan

mask_decline = (df['numest'] < df['numest_l3']) & df['numest_l3'].notna()
df.loc[mask_decline, 'ChNAnalyst'] = 1

# replace ChNAnalyst = 0 if numest >= l3.numest & !mi(numest)
mask_no_decline = (df['numest'] >= df['numest_l3']) & df['numest'].notna()
df.loc[mask_no_decline, 'ChNAnalyst'] = 0

# replace ChNAnalyst = . if time_avail_m >= ym(1987,7) & time_avail_m <= ym(1987,9) 
# In Stata, ym(1987,7) = 198707, ym(1987,9) = 198709
mask_1987 = (df['time_avail_m'] >= pd.Timestamp('1987-07-01')) & (df['time_avail_m'] <= pd.Timestamp('1987-09-01'))
df.loc[mask_1987, 'ChNAnalyst'] = np.nan

# only works in small firms (OP tab 2)
# egen temp = fastxtile(mve_c), n(5)
def fastxtile(series, n_quantiles=5):
    try:
        series_clean = series.replace([np.inf, -np.inf], np.nan)
        return pd.qcut(series_clean, q=n_quantiles, labels=False, duplicates='drop') + 1
    except Exception:
        return pd.Series(np.nan, index=series.index)

df['temp'] = fastxtile(df['mve_c'], n_quantiles=5)

# keep if temp <= 2
df = df[df['temp'] <= 2].copy()

# Keep only needed columns and non-missing values
result = df[['permno', 'time_avail_m', 'ChNAnalyst']].copy()
result = result.dropna(subset=['ChNAnalyst']).copy()

# Convert time_avail_m to yyyymm
result['yyyymm'] = result['time_avail_m'].dt.year * 100 + result['time_avail_m'].dt.month

# Prepare final output
final_result = result[['permno', 'yyyymm', 'ChNAnalyst']].copy()

# SAVE
Path('../pyData/Predictors').mkdir(parents=True, exist_ok=True)
final_result.to_csv('../pyData/Predictors/ChNAnalyst.csv', index=False)

print(f"ChNAnalyst predictor saved: {len(final_result)} observations")