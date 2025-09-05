# ABOUTME: Institutional ownership among high short interest stocks following Asquith, Pathak and Ritter 2005, Table 5, EW 99th
# ABOUTME: Excludes stocks below 99th percentile of short interest, calculates institutional ownership for remaining stocks
"""
Usage:
    python3 Predictors/IO_ShortInterest.py

Inputs:
    - SignalMasterTable.parquet: Monthly master table with columns [permno, time_avail_m]
    - TR_13F.parquet: 13F institutional ownership data with columns [permno, time_avail_m, instown_perc]
    - monthlyCRSP.parquet: Monthly CRSP data with columns [permno, time_avail_m, shrout]
    - monthlyShortInterest.parquet: Short interest data with columns [permno, time_avail_m, shortint]

Outputs:
    - IO_ShortInterest.csv: CSV file with columns [permno, yyyymm, IO_ShortInterest]
    - IO_ShortInterest = institutional ownership for stocks with short interest above 99th percentile, missing otherwise
"""

import pandas as pd
import numpy as np
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils.save_standardized import save_predictor

print("Starting IO_ShortInterest.py...")

# DATA LOAD
print("Loading data...")
signal_master = pd.read_parquet('../pyData/Intermediate/SignalMasterTable.parquet', columns=['permno', 'time_avail_m'])
tr_13f = pd.read_parquet('../pyData/Intermediate/TR_13F.parquet', columns=['permno', 'time_avail_m', 'instown_perc'])
df = pd.merge(signal_master, tr_13f, on=['permno', 'time_avail_m'], how='left', validate='1:1')

monthly_crsp = pd.read_parquet('../pyData/Intermediate/monthlyCRSP.parquet', columns=['permno', 'time_avail_m', 'shrout'])
df = pd.merge(df, monthly_crsp, on=['permno', 'time_avail_m'], how='left', validate='1:1')

monthly_short = pd.read_parquet('../pyData/Intermediate/monthlyShortInterest.parquet', columns=['permno', 'time_avail_m', 'shortint'])
df = pd.merge(df, monthly_short, on=['permno', 'time_avail_m'], how='left', validate='1:1')

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
print(f"Calculated IO_ShortInterest for {df['IO_ShortInterest'].notna().sum()} observations")

save_predictor(df, 'IO_ShortInterest')
print("IO_ShortInterest.py completed successfully")