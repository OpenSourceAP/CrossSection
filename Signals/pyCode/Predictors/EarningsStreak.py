# ABOUTME: Calculates earnings surprise streak following Loh and Warachka 2012 Table 3B Spread FF3 Streaks
# ABOUTME: Input: IBES_EPS_Adj.parquet, SignalMasterTable.parquet | Output: EarningsStreak.csv | Run: python3 Predictors/EarningsStreak.py

# Computes earnings streak indicator by identifying consecutive earnings surprises with the same sign
# Uses quarterly earnings announcements with 6-month forecast horizon from IBES data
# Input: ../pyData/Intermediate/IBES_EPS_Adj.parquet, ../pyData/Intermediate/SignalMasterTable.parquet  
# Output: ../pyData/Predictors/EarningsStreak.csv

import pandas as pd
import numpy as np

# PROCESS EARNINGS ACTUALS
# Load IBES EPS data with actual earnings and consensus forecasts
df = pd.read_parquet('../pyData/Intermediate/IBES_EPS_Adj.parquet')

# Filter for 6-month forecast horizon
df = df[df['fpi'] == "6"]

# Remove observations missing actual earnings, consensus forecast, or price
df = df.dropna(subset=['actual', 'meanest', 'price'])

# Set availability date to actual announcement date
# Remove existing time_avail_m column
df = df.drop(columns=['time_avail_m'])

# Create monthly availability date from actual announcement date
df['time_avail_m'] = pd.to_datetime(df['anndats_act']).dt.to_period('M').dt.start_time

# Select the most recent forecast for each ticker-month combination
# Sort by ticker, month, announcement date, and statistical period
df = df.sort_values(['tickerIBES', 'time_avail_m', 'anndats_act', 'statpers'])

# Keep only the last (most recent) forecast per ticker-month
df = df.groupby(['tickerIBES', 'time_avail_m']).last().reset_index()

# CALCULATE EARNINGS SURPRISES AND STREAKS
# Calculate price-scaled earnings surprise
df['surp'] = (df['actual'] - df['meanest']) / df['price']

# Sort by ticker and announcement date for time series analysis
df = df.sort_values(['tickerIBES', 'anndats_act'])

# Identify streaks: consecutive surprises with same sign (positive or negative)
df['surp_sign'] = np.sign(df['surp'])
df['surp_sign_lag'] = df.groupby('tickerIBES')['surp_sign'].shift(1)
df['streak'] = (df['surp_sign'] == df['surp_sign_lag']).astype(int)

# Filter to keep only streak observations (consecutive same-sign surprises)
df = df[df['streak'] == 1]

# Create temporary dataset with streak information
temp_ibes = df[['tickerIBES', 'time_avail_m', 'anndats_act', 'fpi', 'surp']].copy()

# EXPAND TO MONTHLY PANEL AND MAP TO PERMNOS
# Load master table linking IBES tickers to CRSP permnos across all months
signal_df = pd.read_parquet('../pyData/Intermediate/SignalMasterTable.parquet', 
                            columns=['permno', 'time_avail_m', 'tickerIBES'])

# Merge streak data onto monthly panel structure
df = signal_df.merge(temp_ibes, on=['tickerIBES', 'time_avail_m'], how='left')

# Remove temporary identifiers
df = df.drop(columns=['fpi', 'tickerIBES'])

# Sort by permno and time for panel data operations
df = df.sort_values(['permno', 'time_avail_m'])

# FILL FORWARD ANNOUNCEMENT DATES AND FILTER STALE DATA
# Forward-fill announcement dates within each permno to propagate latest earnings
df['anndats_act'] = df.groupby('permno')['anndats_act'].ffill()

# Remove observations without announcement dates
df = df.dropna(subset=['anndats_act'])

# Remove earnings announcements older than 6 months
df['anndats_act_month'] = pd.to_datetime(df['anndats_act']).dt.to_period('M').dt.start_time
df['month_diff'] = (df['time_avail_m'].dt.to_period('M') - df['anndats_act_month'].dt.to_period('M')).apply(lambda x: x.n)
df = df[df['month_diff'] <= 6]

# CREATE FINAL SIGNAL: earnings surprise magnitude for streak observations
df['EarningsStreak'] = df['surp']

# Forward-fill signal values within each permno to maintain signal until next earnings
df['EarningsStreak'] = df.groupby('permno')['EarningsStreak'].ffill()

# Check for remaining missing values after forward-fill
initial_count = len(df)
df = df.dropna(subset=['EarningsStreak'])
if len(df) < initial_count:
    print(f"Warning: Dropped {initial_count - len(df)} observations with missing EarningsStreak after forward-fill")

# FORMAT OUTPUT DATA
# Select final columns for output
result = df[['permno', 'time_avail_m', 'EarningsStreak']].copy()

# Convert datetime to yyyymm integer format
result['yyyymm'] = result['time_avail_m'].dt.year * 100 + result['time_avail_m'].dt.month

# Arrange columns in standard format
result = result[['permno', 'yyyymm', 'EarningsStreak']]

# Convert to integer types
result['permno'] = result['permno'].astype(int)
result['yyyymm'] = result['yyyymm'].astype(int)

# SAVE RESULTS
result.to_csv('../pyData/Predictors/EarningsStreak.csv', index=False)

print(f"EarningsStreak predictor created with {len(result)} observations")