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
from utils.asrol import asrol
from utils.stata_ineq import stata_ineq_pd

# PREP DISTRIBUTIONS DATA
dist_df = pd.read_parquet('../pyData/Intermediate/CRSPdistributions.parquet')
dist_df = dist_df[['permno', 'cd1', 'cd2', 'cd3', 'divamt', 'exdt']].copy()

# CHECKPOINT 1: Check initial data for problematic permnos
print("=== CHECKPOINT 1: Check initial data for problematic permnos ===")
for pn in [10001, 10006, 11406, 12473]:
    print(f"\n--- Permno {pn} ---")
    total_count = len(dist_df[dist_df['permno'] == pn])
    print(f"Total observations for permno {pn}: {total_count}")
    
    test_data = dist_df[(dist_df['permno'] == pn) & 
                       (dist_df['exdt'].dt.year >= 1986) & (dist_df['exdt'].dt.year <= 1987)]
    if not test_data.empty:
        print(f"permno {pn} data (1986-1987):")
        print(test_data[['permno', 'cd1', 'cd2', 'cd3', 'divamt', 'exdt']].to_string(index=False))
    else:
        print(f"No data found for permno {pn} in 1986-1987")

# Keep if cd1 == 1 & cd2 == 2 (regular cash dividends)
dist_df = dist_df[(dist_df['cd1'] == 1) & (dist_df['cd2'] == 2)]

# CHECKPOINT 2: Check after filtering cd1==1 & cd2==2 for problematic permnos
print("\n=== CHECKPOINT 2: Check after filtering cd1==1 & cd2==2 for problematic permnos ===")
for pn in [10001, 10006, 11406, 12473]:
    print(f"\n--- Permno {pn} ---")
    total_count = len(dist_df[dist_df['permno'] == pn])
    print(f"Total observations for permno {pn} after filter: {total_count}")
    
    test_data = dist_df[(dist_df['permno'] == pn) & 
                       (dist_df['exdt'].dt.year >= 1986) & (dist_df['exdt'].dt.year <= 1987)]
    if not test_data.empty:
        print(f"permno {pn} data after cd1==1 & cd2==2 filter:")
        print(test_data[['permno', 'cd1', 'cd2', 'cd3', 'divamt', 'exdt']].to_string(index=False))
    else:
        print(f"No data found for permno {pn} after filter")

# Select timing variable and convert to monthly
# (p5 says exdt is used)
dist_df['time_avail_m'] = pd.to_datetime(dist_df['exdt'].dt.to_period('M').dt.start_time)

# CHECKPOINT 3: Check before dropping missing time_avail_m/divamt
print("\n=== CHECKPOINT 3: Check before dropping missing time_avail_m/divamt ===")
for pn in [10001, 10006, 11406, 12473]:
    print(f"\n--- Permno {pn} ---")
    total_count = len(dist_df[dist_df['permno'] == pn])
    print(f"Total observations for permno {pn} before dropping missing: {total_count}")
    
    test_data = dist_df[(dist_df['permno'] == pn) & 
                       (dist_df['exdt'].dt.year >= 1986) & (dist_df['exdt'].dt.year <= 1987)]
    if not test_data.empty:
        print(f"permno {pn} data before dropping missing values:")
        print(test_data[['permno', 'cd3', 'divamt', 'exdt', 'time_avail_m']].to_string(index=False))
    else:
        print(f"No data found for permno {pn}")

dist_df = dist_df.dropna(subset=['time_avail_m', 'divamt'])

# CHECKPOINT 4: Check after dropping missing time_avail_m/divamt
print("\n=== CHECKPOINT 4: Check after dropping missing time_avail_m/divamt ===")
for pn in [10001, 10006, 11406, 12473]:
    print(f"\n--- Permno {pn} ---")
    total_count = len(dist_df[dist_df['permno'] == pn])
    print(f"Total observations for permno {pn} after dropping missing: {total_count}")
    
    test_data = dist_df[(dist_df['permno'] == pn) & 
                       (dist_df['exdt'].dt.year >= 1986) & (dist_df['exdt'].dt.year <= 1987)]
    if not test_data.empty:
        print(f"permno {pn} data after dropping missing values:")
        print(test_data[['permno', 'cd3', 'divamt', 'exdt', 'time_avail_m']].to_string(index=False))
    else:
        print(f"No data found for permno {pn} after dropping missing values")

# Sum across all frequency codes
tempdivamt = dist_df.groupby(['permno', 'cd3', 'time_avail_m'])['divamt'].sum().reset_index()

# CHECKPOINT 5: Check after gcollapse
print("\n=== CHECKPOINT 5: Check after gcollapse ===")
for pn in [10001, 10006, 11406, 12473]:
    print(f"\n--- Permno {pn} ---")
    total_count = len(tempdivamt[tempdivamt['permno'] == pn])
    print(f"Total observations for permno {pn} after gcollapse: {total_count}")
    
    test_data = tempdivamt[(tempdivamt['permno'] == pn) & 
                          (tempdivamt['time_avail_m'] >= pd.Timestamp('1986-01-01')) & 
                          (tempdivamt['time_avail_m'] <= pd.Timestamp('1987-12-01'))]
    if not test_data.empty:
        print(f"permno {pn} data after gcollapse:")
        print(test_data[['permno', 'cd3', 'divamt', 'time_avail_m']].to_string(index=False))
    else:
        print(f"No data found for permno {pn} after gcollapse")

# Clean up a handful of odd two-frequency permno-months
# by keeping the first one (sorted by cd3)
tempdivamt = tempdivamt.sort_values(['permno', 'time_avail_m', 'cd3'])
tempdivamt = tempdivamt.groupby(['permno', 'time_avail_m']).first().reset_index()

# CHECKPOINT 6: Check after keeping first frequency code
print("\n=== CHECKPOINT 6: Check after keeping first frequency code ===")
for pn in [10001, 10006, 11406, 12473]:
    print(f"\n--- Permno {pn} ---")
    total_count = len(tempdivamt[tempdivamt['permno'] == pn])
    print(f"Total observations for permno {pn} after frequency cleanup: {total_count}")
    
    test_data = tempdivamt[(tempdivamt['permno'] == pn) & 
                          (tempdivamt['time_avail_m'] >= pd.Timestamp('1986-01-01')) & 
                          (tempdivamt['time_avail_m'] <= pd.Timestamp('1987-12-01'))]
    if not test_data.empty:
        print(f"permno {pn} data after keeping first frequency code:")
        print(test_data[['permno', 'cd3', 'divamt', 'time_avail_m']].to_string(index=False))
    else:
        print(f"No data found for permno {pn} after frequency cleanup")

# DATA LOAD
df = pd.read_parquet('../pyData/Intermediate/SignalMasterTable.parquet')
df = df[['permno', 'time_avail_m']].copy()

# CHECKPOINT 7: Check SignalMasterTable for our target observations
print("\n=== CHECKPOINT 7: Check SignalMasterTable for our target observations ===")
for pn in [10001, 10006, 11406, 12473]:
    print(f"\n--- Permno {pn} ---")
    total_count = len(df[df['permno'] == pn])
    print(f"Total observations for permno {pn} in SignalMasterTable: {total_count}")
    
    test_data = df[(df['permno'] == pn) & 
                   (df['time_avail_m'] >= pd.Timestamp('1986-01-01')) & 
                   (df['time_avail_m'] <= pd.Timestamp('1987-12-01'))]
    if not test_data.empty:
        print(f"permno {pn} data in SignalMasterTable:")
        print(test_data[['permno', 'time_avail_m']].to_string(index=False))
    else:
        print(f"No data found for permno {pn} in SignalMasterTable")

# Merge with dividend amounts
df = df.merge(tempdivamt, on=['permno', 'time_avail_m'], how='left')

# CHECKPOINT 8: Check after merge
print("\n=== CHECKPOINT 8: Check after merge ===")
for pn in [10001, 10006, 11406, 12473]:
    print(f"\n--- Permno {pn} ---")
    total_count = len(df[df['permno'] == pn])
    print(f"Total observations for permno {pn} after merge: {total_count}")
    
    test_data = df[(df['permno'] == pn) & 
                   (df['time_avail_m'] >= pd.Timestamp('1986-01-01')) & 
                   (df['time_avail_m'] <= pd.Timestamp('1987-12-01'))]
    if not test_data.empty:
        print(f"permno {pn} data after merge:")
        print(test_data[['permno', 'time_avail_m', 'cd3', 'divamt']].to_string(index=False))
    else:
        print(f"No data found for permno {pn} after merge")

# Sort for lag operations
df = df.sort_values(['permno', 'time_avail_m'])

# Fill missing cd3 with previous value (equivalent to Stata's l1.cd3 logic)
# Stata: replace cd3 = l1.cd3 if cd3 == .
# This should ONLY fill missing values, not override existing values
df['cd3'] = df.groupby('permno')['cd3'].fillna(method='ffill')

# Replace missing dividend amounts with 0
df['divamt'] = df['divamt'].fillna(0)

# Handle cd3 = NaN for early periods with no distributions yet
# OP page 5: "unknown and missing frequency are assumed quarterly"
# So cd3 = NaN should be treated as quarterly (cd3 = 3)
df['cd3'] = df['cd3'].fillna(3)

# Create dividend paid indicator
df['divpaid'] = (df['divamt'] > 0).astype(int)

# CHECKPOINT 9: Check after filling missing values and creating divpaid
print("\n=== CHECKPOINT 9: Check after filling missing values and creating divpaid ===")
for pn in [10001, 10006, 11406, 12473]:
    print(f"\n--- Permno {pn} ---")
    total_count = len(df[df['permno'] == pn])
    print(f"Total observations for permno {pn} after creating divpaid: {total_count}")
    
    test_data = df[(df['permno'] == pn) & 
                   (df['time_avail_m'] >= pd.Timestamp('1986-01-01')) & 
                   (df['time_avail_m'] <= pd.Timestamp('1987-12-01'))]
    if not test_data.empty:
        print(f"permno {pn} data after creating divpaid:")
        print(test_data[['permno', 'time_avail_m', 'cd3', 'divamt', 'divpaid']].to_string(index=False))
    else:
        print(f"No data found for permno {pn}")

# Drop monthly dividends (OP drops monthly div unless otherwise noted - p5)
df = df[df['cd3'] != 2]

# CHECKPOINT 10: Check after dropping monthly dividends (cd3==2)
print("\n=== CHECKPOINT 10: Check after dropping monthly dividends (cd3==2) ===")
for pn in [10001, 10006, 11406, 12473]:
    print(f"\n--- Permno {pn} ---")
    total_count = len(df[df['permno'] == pn])
    print(f"Total observations for permno {pn} after dropping monthly dividends: {total_count}")
    
    test_data = df[(df['permno'] == pn) & 
                   (df['time_avail_m'] >= pd.Timestamp('1986-01-01')) & 
                   (df['time_avail_m'] <= pd.Timestamp('1987-12-01'))]
    if not test_data.empty:
        print(f"permno {pn} data after dropping monthly dividends:")
        print(test_data[['permno', 'time_avail_m', 'cd3', 'divamt', 'divpaid']].to_string(index=False))
    else:
        print(f"No data found for permno {pn} after dropping monthly dividends")

# Keep if cd3 < 6 (Tab 2 note) - exact match to Stata logic
df = df[df['cd3'] < 6]

# CHECKPOINT 11: Check after keeping only cd3 < 6
print("\n=== CHECKPOINT 11: Check after keeping only cd3 < 6 ===")
for pn in [10001, 10006, 11406, 12473]:
    print(f"\n--- Permno {pn} ---")
    total_count = len(df[df['permno'] == pn])
    print(f"Total observations for permno {pn} after cd3 < 6 filter: {total_count}")
    
    test_data = df[(df['permno'] == pn) & 
                   (df['time_avail_m'] >= pd.Timestamp('1986-01-01')) & 
                   (df['time_avail_m'] <= pd.Timestamp('1987-12-01'))]
    if not test_data.empty:
        print(f"permno {pn} data after cd3 < 6 filter:")
        print(test_data[['permno', 'time_avail_m', 'cd3', 'divamt', 'divpaid']].to_string(index=False))
    else:
        print(f"No data found for permno {pn} after cd3 < 6 filter")

# CRITICAL FIX: Filter to only include observations from the first dividend month onward
# This must be done BEFORE creating lags to match Stata's behavior
first_div_dates = df[df['divamt'] > 0].groupby('permno')['time_avail_m'].min().reset_index()
first_div_dates.columns = ['permno', 'first_div_date']

# Merge to get first dividend date for each permno-month
df = df.merge(first_div_dates, on='permno', how='left')

# Only keep observations from first dividend date onward (not before)
# If no dividends ever observed, keep all (first_div_date will be NaN)
df = df[(df['time_avail_m'] >= df['first_div_date']) | df['first_div_date'].isna()]

# Drop the helper column
df = df.drop('first_div_date', axis=1)

# CHECKPOINT 11B: Check after first dividend date filtering (Python-specific step)
print("\n=== CHECKPOINT 11B: Check after first dividend date filtering ===")
for pn in [10001, 10006, 11406, 12473]:
    print(f"\n--- Permno {pn} ---")
    total_count = len(df[df['permno'] == pn])
    print(f"Total observations for permno {pn} after filtering: {total_count}")
    
    test_data = df[(df['permno'] == pn) & 
                   (df['time_avail_m'] >= pd.Timestamp('1986-01-01')) & 
                   (df['time_avail_m'] <= pd.Timestamp('1987-12-01'))]
    if not test_data.empty:
        print(f"permno {pn} data after filtering:")
        print(test_data[['permno', 'time_avail_m', 'cd3', 'divamt', 'divpaid']].to_string(index=False))
    else:
        print(f"No data found for permno {pn} after filtering")

# SIGNAL CONSTRUCTION
# Short all others with a dividend in last 12 months
# Use fast asrol for 12-month rolling sum of dividend payments
df = asrol(df, 'permno', 'time_avail_m', 'divpaid', 12, stat='sum', new_col_name='div12', min_periods=1)

# CHECKPOINT 12: Check div12 rolling sum calculation
print("\n=== CHECKPOINT 12: Check div12 rolling sum calculation ===")
for pn in [10001, 10006, 11406, 12473]:
    print(f"\n--- Permno {pn} ---")
    total_count = len(df[df['permno'] == pn])
    print(f"Total observations for permno {pn} after div12 calculation: {total_count}")
    
    test_data = df[(df['permno'] == pn) & 
                   (df['time_avail_m'] >= pd.Timestamp('1986-01-01')) & 
                   (df['time_avail_m'] <= pd.Timestamp('1987-12-01'))]
    if not test_data.empty:
        print(f"permno {pn} data with div12:")
        print(test_data[['permno', 'time_avail_m', 'cd3', 'divpaid', 'div12']].to_string(index=False))
    else:
        print(f"No data found for permno {pn}")

# Initialize DivSeason: 0 if had dividends in last 12 months, otherwise missing (NaN)
# This exactly replicates Stata's: gen DivSeason = 0 if div12 > 0
df['DivSeason'] = np.where(df['div12'] > 0, 0, np.nan)

# CHECKPOINT 13: Check initial DivSeason assignment
print("\n=== CHECKPOINT 13: Check initial DivSeason assignment ===")
for pn in [10001, 10006, 11406, 12473]:
    print(f"\n--- Permno {pn} ---")
    total_count = len(df[df['permno'] == pn])
    print(f"Total observations for permno {pn} with initial DivSeason: {total_count}")
    
    test_data = df[(df['permno'] == pn) & 
                   (df['time_avail_m'] >= pd.Timestamp('1986-01-01')) & 
                   (df['time_avail_m'] <= pd.Timestamp('1987-12-01'))]
    if not test_data.empty:
        print(f"permno {pn} data with initial DivSeason:")
        print(test_data[['permno', 'time_avail_m', 'cd3', 'divpaid', 'div12', 'DivSeason']].to_string(index=False))
    else:
        print(f"No data found for permno {pn}")

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

# CHECKPOINT 14: Check temp variables for prediction logic
print("\n=== CHECKPOINT 14: Check temp variables for prediction logic ===")
for pn in [10001, 10006, 11406, 12473]:
    print(f"\n--- Permno {pn} ---")
    total_count = len(df[df['permno'] == pn])
    print(f"Total observations for permno {pn} with temp variables: {total_count}")
    
    test_data = df[(df['permno'] == pn) & 
                   (df['time_avail_m'] >= pd.Timestamp('1986-01-01')) & 
                   (df['time_avail_m'] <= pd.Timestamp('1987-12-01'))]
    if not test_data.empty:
        print(f"permno {pn} data with temp variables:")
        print(test_data[['permno', 'time_avail_m', 'cd3', 'divpaid_lag2', 'divpaid_lag5', 'divpaid_lag8', 'divpaid_lag11', 'temp3', 'temp4', 'temp5']].to_string(index=False))
    else:
        print(f"No data found for permno {pn}")

# Replace DivSeason = 1 if any temp condition is met
df.loc[(df['temp3'] == 1) | (df['temp4'] == 1) | (df['temp5'] == 1), 'DivSeason'] = 1

# CHECKPOINT 15: Check final DivSeason values
print("\n=== CHECKPOINT 15: Check final DivSeason values ===")
for pn in [10001, 10006, 11406, 12473]:
    print(f"\n--- Permno {pn} ---")
    total_count = len(df[df['permno'] == pn])
    print(f"Total observations for permno {pn} with final DivSeason: {total_count}")
    
    test_data = df[(df['permno'] == pn) & 
                   (df['time_avail_m'] >= pd.Timestamp('1986-01-01')) & 
                   (df['time_avail_m'] <= pd.Timestamp('1987-12-01'))]
    if not test_data.empty:
        print(f"permno {pn} data with final DivSeason:")
        print(test_data[['permno', 'time_avail_m', 'cd3', 'div12', 'temp3', 'temp4', 'temp5', 'DivSeason']].to_string(index=False))
    else:
        print(f"No data found for permno {pn}")

# CHECKPOINT 16: Show data drops at critical points
print("\n=== CHECKPOINT 16: Data drop summary ===")
print(f"Total observations in final dataset: {len(df)}")
print("Observations by year:")
year_counts = df['time_avail_m'].dt.year.value_counts().sort_index()
print(year_counts.head(10))

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