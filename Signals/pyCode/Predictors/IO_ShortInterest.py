# ABOUTME: Translates IO_ShortInterest.do - calculates institutional ownership for high short interest stocks
# ABOUTME: Run from pyCode/ directory: python3 Predictors/IO_ShortInterest.py

# Inputs: 
#   - ../pyData/Intermediate/SignalMasterTable.parquet 
#   - ../pyData/Intermediate/TR_13F.parquet
#   - ../pyData/Intermediate/monthlyCRSP.parquet
#   - ../pyData/Intermediate/monthlyShortInterest.parquet
# Outputs:
#   - ../pyData/Predictors/IO_ShortInterest.csv

import pandas as pd
import numpy as np

print("Starting IO_ShortInterest calculation...")

# DATA LOAD
# use permno gvkey time_avail_m using "$pathDataIntermediate/SignalMasterTable", clear
signal_master = pd.read_parquet('../pyData/Intermediate/SignalMasterTable.parquet', columns=['permno', 'gvkey', 'time_avail_m'])

# merge 1:1 permno time_avail_m using "$pathDataIntermediate/TR_13F", keep(master match) nogenerate keepusing(instown_perc)
tr_13f = pd.read_parquet('../pyData/Intermediate/TR_13F.parquet', columns=['permno', 'time_avail_m', 'instown_perc'])
df = pd.merge(signal_master, tr_13f, on=['permno', 'time_avail_m'], how='left', validate='1:1')
print(f"After merge with TR_13F: {len(df)} observations")

# merge 1:1 permno time_avail_m using "$pathDataIntermediate/monthlyCRSP", keep(master match) nogenerate keepusing(shrout)
monthly_crsp = pd.read_parquet('../pyData/Intermediate/monthlyCRSP.parquet', columns=['permno', 'time_avail_m', 'shrout'])
df = pd.merge(df, monthly_crsp, on=['permno', 'time_avail_m'], how='left', validate='1:1')
print(f"After merge with monthlyCRSP: {len(df)} observations")

# preserve - save current state
df_preserved = df.copy()

# keep if mi(gvkey) - keep missing gvkey observations
df_missing_gvkey = df[df['gvkey'].isna()].copy()
print(f"Observations with missing gvkey: {len(df_missing_gvkey)}")

# save "$pathtemp/temp", replace - temporarily store obs with missing gvkeys
# (In Python, we just keep this as df_missing_gvkey)

# restore - restore original state
df = df_preserved.copy()

# drop if mi(gvkey) - drop missing gvkey observations
df = df[df['gvkey'].notna()]
print(f"After dropping missing gvkey: {len(df)} observations")

# merge 1:1 gvkey time_avail_m using "$pathDataIntermediate/monthlyShortInterest", keep(master match) nogenerate keepusing(shortint)
monthly_short = pd.read_parquet('../pyData/Intermediate/monthlyShortInterest.parquet', columns=['gvkey', 'time_avail_m', 'shortint'])
df = pd.merge(df, monthly_short, on=['gvkey', 'time_avail_m'], how='left', validate='1:1')
print(f"After merge with monthlyShortInterest: {len(df)} observations")

# * Append obs without gvkey again
# append using "$pathtemp/temp"
df = pd.concat([df, df_missing_gvkey], ignore_index=True)
print(f"After appending missing gvkey observations: {len(df)} observations")

# SIGNAL CONSTRUCTION
# gen tempshortratio = shortint/shrout
df['tempshortratio'] = df['shortint'] / df['shrout']

# replace tempshortratio = 0 if tempshortratio == .
df['tempshortratio'] = df['tempshortratio'].fillna(0)

# sort time_avail_m
df = df.sort_values('time_avail_m')

# by time_avail_m: egen temps99 = pctile(shortint/shrout), p(99)
# Calculate 99th percentile of shortint/shrout by time_avail_m
df['shortint_shrout'] = df['shortint'] / df['shrout']
df['temps99'] = df.groupby('time_avail_m')['shortint_shrout'].transform(lambda x: x.quantile(0.99))

# gen temp = instown_perc
df['temp'] = df['instown_perc'].copy()

# replace temp = 0 if mi(temp)
df['temp'] = df['temp'].fillna(0)

# replace temp = . if tempshortratio < temps99
df.loc[df['tempshortratio'] < df['temps99'], 'temp'] = np.nan

# gen IO_ShortInterest = temp
df['IO_ShortInterest'] = df['temp']

print(f"IO_ShortInterest calculated for {df['IO_ShortInterest'].notna().sum()} observations")

# cap drop temp*
# (Clean up temporary variables - equivalent to dropping temp variables)

# SAVE
# do "$pathCode/savepredictor" IO_ShortInterest
result = df[['permno', 'time_avail_m', 'IO_ShortInterest']].copy()
result = result.dropna(subset=['IO_ShortInterest'])

# Convert time_avail_m to yyyymm format
result['yyyymm'] = result['time_avail_m'].dt.year * 100 + result['time_avail_m'].dt.month
result = result[['permno', 'yyyymm', 'IO_ShortInterest']].copy()

# Convert to integers where appropriate
result['permno'] = result['permno'].astype(int)
result['yyyymm'] = result['yyyymm'].astype(int)

print(f"Final output: {len(result)} observations")
result.to_csv('../pyData/Predictors/IO_ShortInterest.csv', index=False)
print("IO_ShortInterest.csv saved successfully")