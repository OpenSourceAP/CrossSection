# ABOUTME: Calculates institutional ownership for high short interest stocks
# ABOUTME: Run from pyCode/ directory: python3 Predictors/IO_ShortInterest.py

import pandas as pd
import numpy as np
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils.savepredictor import save_predictor

# DATA LOAD
signal_master = pd.read_parquet('../pyData/Intermediate/SignalMasterTable.parquet', columns=['permno', 'gvkey', 'time_avail_m'])
tr_13f = pd.read_parquet('../pyData/Intermediate/TR_13F.parquet', columns=['permno', 'time_avail_m', 'instown_perc'])
df = pd.merge(signal_master, tr_13f, on=['permno', 'time_avail_m'], how='left', validate='1:1')

monthly_crsp = pd.read_parquet('../pyData/Intermediate/monthlyCRSP.parquet', columns=['permno', 'time_avail_m', 'shrout'])
df = pd.merge(df, monthly_crsp, on=['permno', 'time_avail_m'], how='left', validate='1:1')

# preserve - keep missing gvkey observations
df_missing_gvkey = df[df['gvkey'].isna()].copy()

# restore - drop missing gvkey observations
df = df[df['gvkey'].notna()]

monthly_short = pd.read_parquet('../pyData/Intermediate/monthlyShortInterest.parquet', columns=['gvkey', 'time_avail_m', 'shortint'])
df = pd.merge(df, monthly_short, on=['gvkey', 'time_avail_m'], how='left', validate='1:1')

# append using temp
df = pd.concat([df, df_missing_gvkey], ignore_index=True)

# SIGNAL CONSTRUCTION
df['tempshortratio'] = df['shortint'] / df['shrout']
df['tempshortratio'] = df['tempshortratio'].fillna(0)

df = df.sort_values('time_avail_m')
# Calculate 99th percentile on raw ratio (excluding NaN) before fillna, matching Stata's pctile behavior
temps99_by_month = df.groupby('time_avail_m').apply(
    lambda g: (g['shortint'] / g['shrout']).quantile(0.99)
)
df['temps99'] = df['time_avail_m'].map(temps99_by_month)

df['temp'] = df['instown_perc'].fillna(0)
# Set temp to NaN if tempshortratio < temps99 OR if temps99 is NaN (no valid data for that month)
df.loc[(df['tempshortratio'] < df['temps99']) | df['temps99'].isna(), 'temp'] = np.nan
df['IO_ShortInterest'] = df['temp']

# SAVE
save_predictor(df, 'IO_ShortInterest')