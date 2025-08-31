#%%

# ABOUTME: Creates seasonal dividend yield predictor based on expected dividend timing patterns
# ABOUTME: Run from pyCode/ directory: python3 Predictors/DivSeason.py

# Run from pyCode/ directory
# Inputs: CRSPdistributions.parquet, SignalMasterTable.parquet
# Output: ../pyData/Predictors/DivSeason.csv

import pandas as pd
import numpy as np
import sys
import os

# Add the parent directory to sys.path to import utils
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils.asrol import asrol
from utils.stata_replication import stata_ineq_pd
from utils.save_standardized import save_predictor

print("Starting DivSeason.py...")

# PREP DISTRIBUTIONS DATA
print("Loading CRSP distributions data...")
dist_df = pd.read_parquet('../pyData/Intermediate/CRSPdistributions.parquet')
dist_df = dist_df[['permno', 'cd1', 'cd2', 'cd3', 'divamt', 'exdt']].copy()
print(f"Loaded distributions data: {dist_df.shape[0]} rows")

# Keep if cd1 == 1 & cd2 == 2 (regular cash dividends)
dist_df = dist_df[(dist_df['cd1'] == 1) & (dist_df['cd2'] == 2)]
print(f"After filtering for regular cash dividends: {dist_df.shape[0]} rows")

# Select timing variable and convert to monthly
# (p5 says exdt is used)
dist_df['time_avail_m'] = pd.to_datetime(dist_df['exdt'].dt.to_period('M').dt.start_time)

dist_df = dist_df.dropna(subset=['time_avail_m', 'divamt'])

# Sum across all frequency codes
tempdivamt = dist_df.groupby(['permno', 'cd3', 'time_avail_m'])['divamt'].sum().reset_index()

# Clean up a handful of odd two-frequency permno-months
# by keeping the first one (sorted by cd3)
tempdivamt = tempdivamt.sort_values(['permno', 'time_avail_m', 'cd3'])
tempdivamt = tempdivamt.groupby(['permno', 'time_avail_m']).first().reset_index()

#%%

# DATA LOAD
print("Loading SignalMasterTable...")
df = pd.read_parquet('../pyData/Intermediate/SignalMasterTable.parquet')
df = df[['permno', 'time_avail_m']].copy()
print(f"Loaded SignalMasterTable: {df.shape[0]} rows")

# Merge with dividend amounts
print("Merging with dividend amounts...")
df = df.merge(tempdivamt, on=['permno', 'time_avail_m'], how='left')
print(f"After merge: {df.shape[0]} rows")

# Sort for lag operations
df = df.sort_values(['permno', 'time_avail_m'])

# Identify first observation with dividend data for each company
# Only analyze periods from when dividend history becomes available
first_div_obs = df[df['cd3'].notna()].groupby('permno')['time_avail_m'].min().reset_index()
first_div_obs.columns = ['permno', 'first_div_date']

# Merge to get first dividend observation date
df = df.merge(first_div_obs, on='permno', how='left')

# Keep only observations from first dividend record onward
# This ensures consistent dividend frequency tracking
df = df[(df['time_avail_m'] >= df['first_div_date']) | df['first_div_date'].isna()]
df = df.drop('first_div_date', axis=1)

# Fill missing dividend frequency codes with previous value for consistency
# This forward-fills missing frequency codes to maintain continuity
df['cd3'] = df.groupby('permno')['cd3'].ffill()

# Replace missing dividend amounts with 0
df['divamt'] = df['divamt'].fillna(0)


# Create dividend paid indicator
df['divpaid'] = (df['divamt'] > 0).astype(int)

# Drop monthly dividends (OP drops monthly div unless otherwise noted (p5))
df = df[df['cd3'] != 2]

# Keep if cd3 < 6 (Tab 2 note) - exact match to Stata logic
df = df[df['cd3'] < 6]

#%%

# SIGNAL CONSTRUCTION
print("Calculating DivSeason signal...")
# Short all others with a dividend in last 12 months
# Use calendar-based asrol for 12-month rolling sum of dividend payments
print("Creating 12-month rolling dividend payments...")
df = asrol(df, 'permno', 'time_avail_m', '1mo', 12, 'divpaid', 'sum', new_col_name='divpaid_sum')


# Initialize DivSeason: 0 for companies with dividends in last 12 months, missing otherwise
# Companies without recent dividends are not eligible for the seasonal strategy
df['DivSeason'] = np.where(df['divpaid_sum'] > 0, 0, np.nan)

# Long if dividend month is predicted
# OP page 5: "unkown and missing frequency are assumed quarterly"

# Create lags for dividend prediction logic
print("Creating lag variables for dividend prediction...")
for lag in [2, 5, 8, 11]:
    df[f'divpaid_lag{lag}'] = df.groupby('permno')['divpaid'].shift(lag)

# Quarterly or unknown frequency companies with expected dividend timing
# For quarterly payers, check for dividends 2, 5, 8, or 11 months ago
# This identifies companies likely to pay dividends based on their historical quarterly pattern
df['temp3'] = ((df['cd3'].isin([0, 1, 3])) & 
               (stata_ineq_pd(df['divpaid_lag2'], ">", 0) | 
                stata_ineq_pd(df['divpaid_lag5'], ">", 0) | 
                stata_ineq_pd(df['divpaid_lag8'], ">", 0) | 
                stata_ineq_pd(df['divpaid_lag11'], ">", 0))).astype(int)

# Semi-annual frequency companies with expected dividend timing
# Check for dividends 5 or 11 months ago to predict next semi-annual payment
df['temp4'] = ((df['cd3'] == 4) & 
               (stata_ineq_pd(df['divpaid_lag5'], ">", 0) | 
                stata_ineq_pd(df['divpaid_lag11'], ">", 0))).astype(int)

# Annual frequency companies with expected dividend timing
# Check for dividend 11 months ago to predict next annual payment
df['temp5'] = ((df['cd3'] == 5) & stata_ineq_pd(df['divpaid_lag11'], ">", 0)).astype(int)

# Replace DivSeason = 1 if any temp condition is met
df.loc[(df['temp3'] == 1) | (df['temp4'] == 1) | (df['temp5'] == 1), 'DivSeason'] = 1

# Keep only necessary columns for output
df_final = df[['permno', 'time_avail_m', 'DivSeason']].copy()
print(f"Calculated DivSeason for {df_final['DivSeason'].notna().sum()} observations")

# SAVE using standardized save_predictor function
save_predictor(df_final, 'DivSeason')
print("DivSeason.py completed successfully")
