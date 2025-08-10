# ABOUTME: Translates EarningsStreak.do to calculate earnings streak indicator
# ABOUTME: Run with: python3 Predictors/EarningsStreak.py

# Calculates earnings streak using IBES EPS data
# Input: ../pyData/Intermediate/IBES_EPS_Adj.parquet, ../pyData/Intermediate/SignalMasterTable.parquet
# Output: ../pyData/Predictors/EarningsStreak.csv

import pandas as pd
import numpy as np

# PROCESS ACTUALS
# Load IBES_EPS_Adj data
df = pd.read_parquet('../pyData/Intermediate/IBES_EPS_Adj.parquet')

# keep if fpi == "6"
df = df[df['fpi'] == "6"]

# drop if actual == . | meanest == . | price == .
df = df.dropna(subset=['actual', 'meanest', 'price'])

# use actual release date as date of availability
# drop time_avail_m
df = df.drop(columns=['time_avail_m'])

# gen time_avail_m = mofd(anndats_act)
df['time_avail_m'] = pd.to_datetime(df['anndats_act']).dt.to_period('M').dt.start_time

# keep the last forecast before the actual release
# sort tickerIBES time_avail_m anndats_act statpers
df = df.sort_values(['tickerIBES', 'time_avail_m', 'anndats_act', 'statpers'])

# by tickerIBES time_avail_m: keep if _n == _N
df = df.groupby(['tickerIBES', 'time_avail_m']).last().reset_index()

# Define Surp (positive / negative surprise) and Streak (consistent Surp)
# gen surp = (actual - meanest)/price
df['surp'] = (df['actual'] - df['meanest']) / df['price']

# sort tickerIBES anndats_act
df = df.sort_values(['tickerIBES', 'anndats_act'])

# by tickerIBES: gen streak = sign(surp) == sign(surp[_n-1])
df['surp_sign'] = np.sign(df['surp'])
df['surp_sign_lag'] = df.groupby('tickerIBES')['surp_sign'].shift(1)
df['streak'] = (df['surp_sign'] == df['surp_sign_lag']).astype(int)

# Convert to Positive Streak vs Negative Streak
# keep if streak == 1
df = df[df['streak'] == 1]

# Create temp IBES data (equivalent to save "$pathtemp/tempibes")
temp_ibes = df[['tickerIBES', 'time_avail_m', 'anndats_act', 'fpi', 'surp']].copy()

# FILL TO MONTHLY AND ADD PERMNOS
# Load SignalMasterTable
signal_df = pd.read_parquet('../pyData/Intermediate/SignalMasterTable.parquet', 
                            columns=['permno', 'time_avail_m', 'tickerIBES'])

# merge m:1 tickerIBES time_avail_m using temp_ibes, keep(master match) nogenerate
df = signal_df.merge(temp_ibes, on=['tickerIBES', 'time_avail_m'], how='left')

# drop fpi tickerIBES
df = df.drop(columns=['fpi', 'tickerIBES'])

# xtset permno time_avail_m (sort for panel operations)
df = df.sort_values(['permno', 'time_avail_m'])

# drop stale or empty
# replace anndats_act = l1.anndats_act if anndats_act == .
# Try both forward and backward fill to capture Stata's behavior
df['anndats_act'] = df.groupby('permno')['anndats_act'].ffill()
df['anndats_act'] = df.groupby('permno')['anndats_act'].bfill()

# drop if anndats_act == .
df = df.dropna(subset=['anndats_act'])

# drop if time_avail_m - mofd(anndats_act) > 6 (drop if stale)
# Convert anndats_act to monthly period for comparison
df['anndats_act_month'] = pd.to_datetime(df['anndats_act']).dt.to_period('M').dt.start_time
df['month_diff'] = (df['time_avail_m'].dt.to_period('M') - df['anndats_act_month'].dt.to_period('M')).apply(lambda x: x.n)
df = df[df['month_diff'] <= 6]

# the signal is just surp among streak == 1, but we've already kept only streak == 1
# gen EarningsStreak = surp
df['EarningsStreak'] = df['surp']

# replace EarningsStreak = l1.EarningsStreak if EarningsStreak == .
# This needs to forward-fill within each permno group
df['EarningsStreak'] = df.groupby('permno')['EarningsStreak'].ffill()

# After forward-fill, all observations should have EarningsStreak values
# Only drop if still missing (shouldn't happen with proper forward-fill)
initial_count = len(df)
df = df.dropna(subset=['EarningsStreak'])
if len(df) < initial_count:
    print(f"Warning: Dropped {initial_count - len(df)} observations with missing EarningsStreak after forward-fill")

# Keep only required columns for final output
result = df[['permno', 'time_avail_m', 'EarningsStreak']].copy()

# Convert time_avail_m to yyyymm format
result['yyyymm'] = result['time_avail_m'].dt.year * 100 + result['time_avail_m'].dt.month

# Final format matching Stata output
result = result[['permno', 'yyyymm', 'EarningsStreak']]

# Convert permno and yyyymm to int
result['permno'] = result['permno'].astype(int)
result['yyyymm'] = result['yyyymm'].astype(int)

# SAVE
result.to_csv('../pyData/Predictors/EarningsStreak.csv', index=False)

print(f"EarningsStreak predictor created with {len(result)} observations")