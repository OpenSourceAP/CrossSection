# ABOUTME: Translates DivSeason.do to create seasonal dividend yield predictor
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
from utils.data_utils import asrol

# PREP DISTRIBUTIONS DATA
dist_df = pd.read_parquet('../pyData/Intermediate/CRSPdistributions.parquet')
dist_df = dist_df[['permno', 'cd1', 'cd2', 'cd3', 'divamt', 'exdt']].copy()

# Keep if cd1 == 1 & cd2 == 2 (regular cash dividends)
dist_df = dist_df[(dist_df['cd1'] == 1) & (dist_df['cd2'] == 2)]

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

# DATA LOAD
df = pd.read_parquet('../pyData/Intermediate/SignalMasterTable.parquet')
df = df[['permno', 'time_avail_m']].copy()

# Merge with dividend amounts
df = df.merge(tempdivamt, on=['permno', 'time_avail_m'], how='left')

# Sort for lag operations
df = df.sort_values(['permno', 'time_avail_m'])

# Fill missing cd3 with previous value (equivalent to Stata's l1.cd3 logic)
# But don't forward-fill special dividend codes (cd3 >= 6) as they should only apply to specific months
df['cd3_original'] = df['cd3'].copy()  # Keep original cd3 values
df['cd3_for_fill'] = df['cd3'].copy()
df.loc[df['cd3'] >= 6, 'cd3_for_fill'] = np.nan  # Clear special dividend codes for forward-fill
df['cd3'] = df.groupby('permno')['cd3_for_fill'].fillna(method='ffill')

# Restore original cd3 values for months that actually had special dividends
df['cd3'] = df['cd3_original'].fillna(df['cd3'])
df = df.drop(columns=['cd3_original', 'cd3_for_fill'])  # Clean up temporary columns

# Replace missing dividend amounts with 0
df['divamt'] = df['divamt'].fillna(0)

# Handle cd3 = NaN for early periods with no distributions yet
# OP page 5: "unknown and missing frequency are assumed quarterly"
# So cd3 = NaN should be treated as quarterly (cd3 = 3)
df['cd3'] = df['cd3'].fillna(3)

# Create dividend paid indicator
df['divpaid'] = (df['divamt'] > 0).astype(int)

# Drop monthly dividends (OP drops monthly div unless otherwise noted - p5)
df = df[df['cd3'] != 2]

# Mark special dividends (cd3 >= 6) for special handling
df['is_special_dividend'] = (df['cd3'] >= 6).astype(int)

# For dividend prediction logic, treat special dividends as if they don't exist
# But keep them in the dataset for output with DivSeason = 0
df['cd3_for_prediction'] = df['cd3'].copy()
df.loc[df['cd3'] >= 6, 'cd3_for_prediction'] = np.nan

# SIGNAL CONSTRUCTION
# Short all others with a dividend in last 12 months
df = asrol(df, 'permno', 'time_avail_m', 'divpaid', 12, stat='sum', new_col_name='div12')

# Initialize DivSeason: 0 if had dividends in last 12 months, otherwise start with 0 for early periods
# This handles the case where companies exist but have no dividend history yet
df['DivSeason'] = np.where(df['div12'] > 0, 0, 0)

# Long if dividend month is predicted
# OP page 5: "unknown and missing frequency are assumed quarterly"

# Create lags for dividend prediction logic
for lag in [2, 5, 8, 11]:
    df[f'divpaid_lag{lag}'] = df.groupby('permno')['divpaid'].shift(lag)

# temp3: quarterly, unknown, or missing frequency with expected dividend timing
# cd3 == 3 (quarterly) | cd3 == 0 (unknown) | cd3 == 1 (annual treated as quarterly?)
# with dividends 2, 5, 8, or 11 months ago
# Use cd3_for_prediction to exclude special dividends from prediction logic
df['temp3'] = ((df['cd3_for_prediction'].isin([0, 1, 3])) & 
               ((df['divpaid_lag2'] == 1) | (df['divpaid_lag5'] == 1) | 
                (df['divpaid_lag8'] == 1) | (df['divpaid_lag11'] == 1))).astype(int)

# temp4: semi-annual (cd3 == 4) with dividends 5 or 11 months ago
df['temp4'] = ((df['cd3_for_prediction'] == 4) & 
               ((df['divpaid_lag5'] == 1) | (df['divpaid_lag11'] == 1))).astype(int)

# temp5: annual (cd3 == 5) with dividend 11 months ago
df['temp5'] = ((df['cd3_for_prediction'] == 5) & (df['divpaid_lag11'] == 1)).astype(int)

# Replace DivSeason = 1 if any temp condition is met
df.loc[(df['temp3'] == 1) | (df['temp4'] == 1) | (df['temp5'] == 1), 'DivSeason'] = 1

# Special dividends (cd3 >= 6) always get DivSeason = 0
df.loc[df['is_special_dividend'] == 1, 'DivSeason'] = 0

# Keep only necessary columns for output
df_final = df[['permno', 'time_avail_m', 'DivSeason']].copy()
df_final = df_final.dropna(subset=['DivSeason'])

# Convert time_avail_m to yyyymm format like other predictors
df_final['yyyymm'] = df_final['time_avail_m'].dt.year * 100 + df_final['time_avail_m'].dt.month

# Convert to integers for consistency with other predictors
df_final['permno'] = df_final['permno'].astype('int64')
df_final['yyyymm'] = df_final['yyyymm'].astype('int64')
df_final['DivSeason'] = df_final['DivSeason'].astype('int64')

# Keep only required columns and set index
df_final = df_final[['permno', 'yyyymm', 'DivSeason']].copy()
df_final = df_final.set_index(['permno', 'yyyymm'])

# SAVE
df_final.to_csv('../pyData/Predictors/DivSeason.csv')

print("DivSeason predictor saved successfully")