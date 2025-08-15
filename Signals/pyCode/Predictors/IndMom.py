# ABOUTME: Creates Industry Momentum (IndMom) predictor by calculating weighted mean of 6-month momentum within SIC2 industry groups
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

# CHECKPOINT 1: Initial data load  
print(f"CHECKPOINT 1: Initial observations after data load: {len(df)}")
# Check problematic observations
test_date_2021m11 = pd.Timestamp('2021-11-01')
test_date_2007m4 = pd.Timestamp('2007-04-01')
test_obs_16086 = df[(df['permno'] == 16086) & (df['time_avail_m'] == test_date_2021m11)]
if not test_obs_16086.empty:
    print(f"Permno 16086 2021m11: ret={test_obs_16086['ret'].iloc[0]}, sicCRSP={test_obs_16086['sicCRSP'].iloc[0]}, mve_c={test_obs_16086['mve_c'].iloc[0]}")
else:
    print("Permno 16086 2021m11: NOT FOUND")
test_obs_11406 = df[(df['permno'] == 11406) & (df['time_avail_m'] == test_date_2007m4)]
if not test_obs_11406.empty:
    print(f"Permno 11406 2007m4: ret={test_obs_11406['ret'].iloc[0]}, sicCRSP={test_obs_11406['sicCRSP'].iloc[0]}, mve_c={test_obs_11406['mve_c'].iloc[0]}")
else:
    print("Permno 11406 2007m4: NOT FOUND")

# SIGNAL CONSTRUCTION

# Stata: tostring sicCRSP, replace
df['sicCRSP'] = df['sicCRSP'].astype(str)

# Stata: gen sic2D = substr(sicCRSP,1,2)  
df['sic2D'] = df['sicCRSP'].str[:2]

# CHECKPOINT 2: After sic2D creation
print("CHECKPOINT 2: After sic2D creation")
problem_permnos = [16086, 16338, 21359]
for permno in problem_permnos:
    test_obs = df[(df['permno'] == permno) & (df['time_avail_m'] == test_date_2021m11)]
    if not test_obs.empty:
        print(f"Permno {permno} 2021m11: sicCRSP={test_obs['sicCRSP'].iloc[0]}, sic2D={test_obs['sic2D'].iloc[0]}")
    else:
        print(f"Permno {permno} 2021m11: NOT FOUND")
test_obs_11406 = df[(df['permno'] == 11406) & (df['time_avail_m'] == test_date_2007m4)]
if not test_obs_11406.empty:
    print(f"Permno 11406 2007m4: sicCRSP={test_obs_11406['sicCRSP'].iloc[0]}, sic2D={test_obs_11406['sic2D'].iloc[0]}")
else:
    print("Permno 11406 2007m4: NOT FOUND")

# Stata: replace ret = 0 if mi(ret)
df.loc[df['ret'].isna(), 'ret'] = 0

# CHECKPOINT 3: After return cleaning
print("CHECKPOINT 3: After return cleaning")
date_range_2021 = pd.date_range('2021-06-01', '2021-11-01', freq='MS')
for permno in problem_permnos:
    test_obs = df[(df['permno'] == permno) & (df['time_avail_m'].isin(date_range_2021))]
    if not test_obs.empty:
        print(f"Permno {permno} returns 2021m6-2021m11:")
        for _, row in test_obs.iterrows():
            print(f"  {row['time_avail_m'].strftime('%Y-%m')}: {row['ret']}")
    else:
        print(f"Permno {permno} 2021m6-2021m11: NOT FOUND")

# Sort data for lag operations (ensuring proper panel structure)
df = df.sort_values(['permno', 'time_avail_m'])

# Stata: gen Mom6m = ( (1+l.ret)*(1+l2.ret)*(1+l3.ret)*(1+l4.ret)*(1+l5.ret)) - 1
# Create lag variables for momentum calculation
for lag in range(1, 6):
    df[f'l{lag}_ret'] = df.groupby('permno')['ret'].shift(lag)

# Calculate 6-month momentum
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

# Stata: egen IndMom = wtmean(Mom6m), by(sic2D time_avail_m) weight(mve_c)
# Calculate weighted average using transform to match egen wtmean exactly
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