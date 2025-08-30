# ABOUTME: Calculates industry momentum by computing market-cap weighted average of 6-month momentum within 2-digit SIC industry groups
# ABOUTME: Run from pyCode/ directory: python3 Predictors/IndMom.py

# Industry Momentum predictor translation from Code/Predictors/IndMom.do
# Line-by-line translation preserving exact order and logic

import pandas as pd
import numpy as np
import os

# DATA LOAD
# Stata: use permno time_avail_m ret sicCRSP mve_c using "$pathDataIntermediate/SignalMasterTable", clear
df = pd.read_parquet('../pyData/Intermediate/SignalMasterTable.parquet')
df = df[['permno', 'time_avail_m', 'ret', 'sicCRSP', 'mve_c']].copy()

# SIGNAL CONSTRUCTION

# Convert SIC codes to string and extract first 2 digits for industry grouping
df['sicCRSP'] = df['sicCRSP'].astype(str)
df['sic2D'] = df['sicCRSP'].str[:2]

# Replace missing returns with 0 for momentum calculations
df.loc[df['ret'].isna(), 'ret'] = 0

# Sort data for lag operations (ensuring proper panel structure)
df = df.sort_values(['permno', 'time_avail_m'])

# Create calendar-based lags for months t-1 to t-5 using time-based merges
for lag in range(1, 6):
    # Create lag data by shifting time_avail_m forward by lag months
    df_lag = df[['permno', 'time_avail_m', 'ret']].copy()
    df_lag['time_avail_m'] = df_lag['time_avail_m'] + pd.DateOffset(months=lag)
    df_lag = df_lag.rename(columns={'ret': f'l{lag}_ret'})
    df = df.merge(df_lag[['permno', 'time_avail_m', f'l{lag}_ret']], 
                  on=['permno', 'time_avail_m'], how='left')

# Compounds monthly returns over months t-5 to t-1 to create individual 6-month momentum
df['Mom6m'] = ((1 + df['l1_ret']) * (1 + df['l2_ret']) * (1 + df['l3_ret']) * 
               (1 + df['l4_ret']) * (1 + df['l5_ret'])) - 1

# CHECKPOINT 4: After Mom6m calculation
print("CHECKPOINT 4: After Mom6m calculation")
for permno in problem_permnos:
    test_obs = df[(df['permno'] == permno) & (df['time_avail_m'] == test_date_2021m11)]
    if not test_obs.empty:
        row = test_obs.iloc[0]
        print(f"Permno {permno} 2021m11: l1_ret={row['l1_ret']}, l2_ret={row['l2_ret']}, l3_ret={row['l3_ret']}, l4_ret={row['l4_ret']}, l5_ret={row['l5_ret']}, Mom6m={row['Mom6m']}")
    else:
        print(f"Permno {permno} 2021m11: NOT FOUND")
test_obs_11406 = df[(df['permno'] == 11406) & (df['time_avail_m'] == test_date_2007m4)]
if not test_obs_11406.empty:
    row = test_obs_11406.iloc[0]
    print(f"Permno 11406 2007m4: l1_ret={row['l1_ret']}, l2_ret={row['l2_ret']}, l3_ret={row['l3_ret']}, l4_ret={row['l4_ret']}, l5_ret={row['l5_ret']}, Mom6m={row['Mom6m']}")
else:
    print("Permno 11406 2007m4: NOT FOUND")

# CHECKPOINT 5: Before IndMom calculation - Industry groups in 2021m11
print("CHECKPOINT 5: Before IndMom calculation - Industry groups in 2021m11")
nov_2021_data = df[df['time_avail_m'] == test_date_2021m11]
valid_nov_data = nov_2021_data[nov_2021_data['Mom6m'].notna() & nov_2021_data['mve_c'].notna()]
industry_counts = valid_nov_data['sic2D'].value_counts().sort_index()
print("Industry counts with valid Mom6m and mve_c:")
for sic, count in industry_counts.head(10).items():
    print(f"  sic2D {sic}: {count} obs")

# Calculate market-cap weighted average of Mom6m within each 2-digit SIC industry group by month
# Uses market value (mve_c) as weights, requires both Mom6m and mve_c to be non-missing
def calculate_weighted_mean(group):
    # Match Stata's exact logic: require both Mom6m and mve_c to be non-missing AND mve_c > 0
    valid_mask = group['Mom6m'].notna() & group['mve_c'].notna() & (group['mve_c'] > 0)
    if not valid_mask.any():
        return np.nan
    
    valid_mom = group.loc[valid_mask, 'Mom6m'].astype('float64')
    valid_weights = group.loc[valid_mask, 'mve_c'].astype('float64')
    
    # Use higher precision calculation
    numerator = (valid_mom * valid_weights).sum()
    denominator = valid_weights.sum()
    
    if denominator == 0:
        return np.nan
    
    return numerator / denominator

# Calculate weighted means by group to match Stata wtmean exactly
# Stata's egen wtmean uses formula: SUM(weight * value) / SUM(weight) with no outlier handling
# Use higher precision to match Stata's numerical behavior
group_weighted_means = df.groupby(['sic2D', 'time_avail_m']).apply(calculate_weighted_mean, include_groups=False).reset_index()
group_weighted_means.columns = ['sic2D', 'time_avail_m', 'IndMom']

# Convert to float64 for higher precision
group_weighted_means['IndMom'] = group_weighted_means['IndMom'].astype('float64')

# Merge back to get IndMom for all observations
# Stata's egen assigns the group weighted mean to ALL observations in the group,
# even those with missing Mom6m, as long as the group has some valid observations
df = df.merge(group_weighted_means, on=['sic2D', 'time_avail_m'], how='left')

# CHECKPOINT 6: After IndMom calculation
print("CHECKPOINT 6: After IndMom calculation")
test_date_2022m2 = pd.Timestamp('2022-02-01')

# Show problem permnos for 2021m11
for permno in problem_permnos:
    test_obs = df[(df['permno'] == permno) & (df['time_avail_m'] == test_date_2021m11)]
    if not test_obs.empty:
        row = test_obs.iloc[0]
        print(f"Permno {permno} 2021m11: sic2D={row['sic2D']}, Mom6m={row['Mom6m']}, mve_c={row['mve_c']}, IndMom={row['IndMom']}")
    else:
        print(f"Permno {permno} 2021m11: NOT FOUND")

# Show problem permnos for 2022m2
for permno in problem_permnos:
    test_obs = df[(df['permno'] == permno) & (df['time_avail_m'] == test_date_2022m2)]
    if not test_obs.empty:
        row = test_obs.iloc[0]
        print(f"Permno {permno} 2022m2: sic2D={row['sic2D']}, Mom6m={row['Mom6m']}, mve_c={row['mve_c']}, IndMom={row['IndMom']}")
    else:
        print(f"Permno {permno} 2022m2: NOT FOUND")

# Control observation
test_obs_11406 = df[(df['permno'] == 11406) & (df['time_avail_m'] == test_date_2007m4)]
if not test_obs_11406.empty:
    row = test_obs_11406.iloc[0]
    print(f"Permno 11406 2007m4: sic2D={row['sic2D']}, Mom6m={row['Mom6m']}, mve_c={row['mve_c']}, IndMom={row['IndMom']}")
else:
    print("Permno 11406 2007m4: NOT FOUND")

# SAVE
# Stata equivalent: do "$pathCode/savepredictor" IndMom
# Clean up: drop if IndMom == .
df_output = df[df['IndMom'].notna()].copy()

# Convert time_avail_m to yyyymm format
df_output['yyyymm'] = (df_output['time_avail_m'].dt.year * 100 + 
                       df_output['time_avail_m'].dt.month)

# Keep only required columns and set order
df_output = df_output[['permno', 'yyyymm', 'IndMom']]

# Create output directory if it doesn't exist
os.makedirs('../pyData/Predictors', exist_ok=True)

# Save to CSV
df_output.to_csv('../pyData/Predictors/IndMom.csv', index=False)

print(f"IndMom predictor saved with {len(df_output)} observations")
print(f"Date range: {df_output['yyyymm'].min()} to {df_output['yyyymm'].max()}")