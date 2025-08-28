# ABOUTME: Translates High52.do - calculates 52-week high ratio using daily CRSP price data
# ABOUTME: Run from pyCode/ directory: python3 Predictors/High52.py

# Inputs:
#   - ../pyData/Intermediate/dailyCRSP.parquet
# Outputs:
#   - ../pyData/Predictors/High52.csv

import pandas as pd
import numpy as np

print("Starting High52 calculation...")

# DATA LOAD
# use "$pathDataIntermediate/dailyCRSP.dta", clear
daily_crsp = pd.read_parquet('../pyData/Intermediate/dailyCRSP.parquet')
df = daily_crsp.copy()
print(f"Loaded dailyCRSP data: {len(df)} observations")

# SIGNAL CONSTRUCTION
# gen time_avail_m = mofd(time_d)
# format time_avail_m %tm
df['time_avail_m'] = df['time_d'].dt.to_period('M').dt.start_time

# gen prcadj = abs(prc)  
# OP does not appear to adjust prices for splits and cfacpr has look-ahead bias. 
# See discussion here: https://github.com/OpenSourceAP/CrossSection/issues/95#issuecomment-2286803178
df['prcadj'] = df['prc'].abs()

# gcollapse (max) maxpr = prcadj (lastnm) prcadj, by(permno time_avail_m)
# This means: group by permno and time_avail_m, take max of prcadj as maxpr, and last non-missing prcadj
df_collapsed = df.groupby(['permno', 'time_avail_m']).agg(
    maxpr=('prcadj', 'max'),
    prcadj=('prcadj', 'last')  # lastnm means last non-missing
).reset_index()

print(f"After collapse by permno and time_avail_m: {len(df_collapsed)} observations")

# xtset permno time_avail_m
df = df_collapsed.sort_values(['permno', 'time_avail_m'])

# gen temp = max(l1.maxpr, l2.maxpr, l3.maxpr, l4.maxpr, l5.maxpr, l6.maxpr,
#     l7.maxpr, l8.maxpr, l9.maxpr, l10.maxpr, l11.maxpr, l12.maxpr)

# Create 12-month lags of maxpr
for i in range(1, 13):
    df[f'l{i}_maxpr'] = df.groupby('permno')['maxpr'].shift(i)

# Calculate maximum across all 12 lags
lag_columns = [f'l{i}_maxpr' for i in range(1, 13)]
df['temp'] = df[lag_columns].max(axis=1)

# gen High52 = prcadj / temp
df['High52'] = df['prcadj'] / df['temp']

print(f"High52 calculated for {df['High52'].notna().sum()} observations")

# drop temp*
# (Clean up temporary variables)

# SAVE
# do "$pathCode/savepredictor" High52
result = df[['permno', 'time_avail_m', 'High52']].copy()
result = result.dropna(subset=['High52'])

# Convert time_avail_m to yyyymm format
result['yyyymm'] = result['time_avail_m'].dt.year * 100 + result['time_avail_m'].dt.month
result = result[['permno', 'yyyymm', 'High52']].copy()

# Convert to integers where appropriate
result['permno'] = result['permno'].astype(int)
result['yyyymm'] = result['yyyymm'].astype(int)

print(f"Final output: {len(result)} observations")
result.to_csv('../pyData/Predictors/High52.csv', index=False)
print("High52.csv saved successfully")