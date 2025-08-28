#%%

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
from utils.asrol import asrol_fast
from utils.stata_replication import stata_ineq_pd

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

#%%

# DATA LOAD
df = pd.read_parquet('../pyData/Intermediate/SignalMasterTable.parquet')
df = df[['permno', 'time_avail_m']].copy()

# Merge with dividend amounts
df = df.merge(tempdivamt, on=['permno', 'time_avail_m'], how='left')

# Sort for lag operations
df = df.sort_values(['permno', 'time_avail_m'])

# CRITICAL: Identify the first observation with actual dividend data for each permno
# This matches Stata's behavior where observations before first dividend data are effectively excluded
first_div_obs = df[df['cd3'].notna()].groupby('permno')['time_avail_m'].min().reset_index()
first_div_obs.columns = ['permno', 'first_div_date']

# Merge to get first dividend observation date
df = df.merge(first_div_obs, on='permno', how='left')

# Only keep observations from first dividend observation onward
# This matches Stata's effective behavior after the merge step
df = df[(df['time_avail_m'] >= df['first_div_date']) | df['first_div_date'].isna()]
df = df.drop('first_div_date', axis=1)

# Fill missing cd3 with previous value (equivalent to Stata's l1.cd3 logic)
# Stata: replace cd3 = l1.cd3 if cd3 == .
# This should ONLY fill missing values, not override existing values
df['cd3'] = df.groupby('permno')['cd3'].fillna(method='ffill')

# Replace missing dividend amounts with 0
df['divamt'] = df['divamt'].fillna(0)


# Create dividend paid indicator
df['divpaid'] = (df['divamt'] > 0).astype(int)

# Drop monthly dividends (OP drops monthly div unless otherwise noted - p5)
df = df[df['cd3'] != 2]

# Keep if cd3 < 6 (Tab 2 note) - exact match to Stata logic
df = df[df['cd3'] < 6]


#%%

# SIGNAL CONSTRUCTION
# Short all others with a dividend in last 12 months
# Use fast asrol for 12-month rolling sum of dividend payments
df = asrol_fast(df, 'permno', 'time_avail_m', 'divpaid', 12, stat='sum', new_col_name='div12', min_periods=1)

# Initialize DivSeason: 0 if had dividends in last 12 months, otherwise missing (NaN)
# This exactly replicates Stata's: gen DivSeason = 0 if div12 > 0
df['DivSeason'] = np.where(df['div12'] > 0, 0, np.nan)

# Long if dividend month is predicted
# OP page 5: "unknown and missing frequency are assumed quarterly"

# Create lags for dividend prediction logic
for lag in [2, 5, 8, 11]:
    df[f'divpaid_lag{lag}'] = df.groupby('permno')['divpaid'].shift(lag)

# temp3: quarterly, unknown, or missing frequency with expected dividend timing
# cd3 == 3 (quarterly) | cd3 == 0 (unknown) | cd3 == 1 (annual treated as quarterly?)
# with dividends 2, 5, 8, or 11 months ago
# In Stata: l2.divpaid | l5.divpaid | l8.divpaid | l11.divpaid
# This is TRUE if any lag is 1 OR if any lag is missing (Stata treats missing as positive infinity)
df['temp3'] = ((df['cd3'].isin([0, 1, 3])) & 
               (stata_ineq_pd(df['divpaid_lag2'], ">", 0) | 
                stata_ineq_pd(df['divpaid_lag5'], ">", 0) | 
                stata_ineq_pd(df['divpaid_lag8'], ">", 0) | 
                stata_ineq_pd(df['divpaid_lag11'], ">", 0))).astype(int)

# temp4: semi-annual (cd3 == 4) with dividends 5 or 11 months ago
# In Stata: l5.divpaid | l11.divpaid
df['temp4'] = ((df['cd3'] == 4) & 
               (stata_ineq_pd(df['divpaid_lag5'], ">", 0) | 
                stata_ineq_pd(df['divpaid_lag11'], ">", 0))).astype(int)

# temp5: annual (cd3 == 5) with dividend 11 months ago
# In Stata: l11.divpaid
df['temp5'] = ((df['cd3'] == 5) & stata_ineq_pd(df['divpaid_lag11'], ">", 0)).astype(int)

# Replace DivSeason = 1 if any temp condition is met
df.loc[(df['temp3'] == 1) | (df['temp4'] == 1) | (df['temp5'] == 1), 'DivSeason'] = 1

# Keep only necessary columns for output
df_final = df[['permno', 'time_avail_m', 'DivSeason']].copy()

# CRITICAL: Match Stata's savepredictor.do behavior - drop if DivSeason == .
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
