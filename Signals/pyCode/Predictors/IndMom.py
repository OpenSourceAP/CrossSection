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
test_date = pd.Timestamp('2007-04-01')
checkpoint_permnos = [10006, 11406]
for permno in checkpoint_permnos:
    test_obs = df[(df['permno'] == permno) & (df['time_avail_m'] == test_date)]
    if not test_obs.empty:
        print(f"Permno {permno} 2007m4: ret={test_obs['ret'].iloc[0]}, sicCRSP={test_obs['sicCRSP'].iloc[0]}, mve_c={test_obs['mve_c'].iloc[0]}")
    else:
        print(f"Permno {permno} 2007m4: NOT FOUND")

# SIGNAL CONSTRUCTION

# Stata: tostring sicCRSP, replace
df['sicCRSP'] = df['sicCRSP'].astype(str)

# Stata: gen sic2D = substr(sicCRSP,1,2)  
df['sic2D'] = df['sicCRSP'].str[:2]

# CHECKPOINT 2: After SIC2D creation
non_missing_sic2d = df['sic2D'].notna().sum()
print(f"CHECKPOINT 2: Observations with non-missing sic2D: {non_missing_sic2d}")
for permno in checkpoint_permnos:
    test_obs = df[(df['permno'] == permno) & (df['time_avail_m'] == test_date)]
    if not test_obs.empty:
        print(f"Permno {permno} 2007m4: sicCRSP={test_obs['sicCRSP'].iloc[0]}, sic2D={test_obs['sic2D'].iloc[0]}")
    else:
        print(f"Permno {permno} 2007m4: NOT FOUND")

# Stata: replace ret = 0 if mi(ret)
df.loc[df['ret'].isna(), 'ret'] = 0

# CHECKPOINT 3: After return cleaning
non_missing_ret = df['ret'].notna().sum()
print(f"CHECKPOINT 3: Observations with non-missing ret after cleaning: {non_missing_ret}")
for permno in checkpoint_permnos:
    # Show returns for permnos around 2007m4 period
    date_range = pd.date_range('2007-01-01', '2007-06-01', freq='MS')
    test_obs = df[(df['permno'] == permno) & (df['time_avail_m'].isin(date_range))]
    if not test_obs.empty:
        print(f"Permno {permno} 2007m1-m6 returns:")
        for _, row in test_obs.iterrows():
            print(f"  {row['time_avail_m'].strftime('%Y-%m')}: {row['ret']}")
    else:
        print(f"Permno {permno} 2007m1-m6: NOT FOUND")

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
non_missing_mom6m = df['Mom6m'].notna().sum()
print(f"CHECKPOINT 4: Observations with non-missing Mom6m: {non_missing_mom6m}")
checkpoint_permnos_extended = [10006, 11406, 12473]
for permno in checkpoint_permnos_extended:
    test_obs = df[(df['permno'] == permno) & (df['time_avail_m'] == test_date)]
    if not test_obs.empty:
        row = test_obs.iloc[0]
        print(f"Permno {permno} 2007m4: l1_ret={row['l1_ret']}, l2_ret={row['l2_ret']}, l3_ret={row['l3_ret']}, l4_ret={row['l4_ret']}, l5_ret={row['l5_ret']}, Mom6m={row['Mom6m']}")
    else:
        print(f"Permno {permno} 2007m4: NOT FOUND")

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

# CHECKPOINT 5: After IndMom calculation
non_missing_indmom = df['IndMom'].notna().sum()
print(f"CHECKPOINT 5: Observations with non-missing IndMom: {non_missing_indmom}")
for permno in checkpoint_permnos_extended:
    test_obs = df[(df['permno'] == permno) & (df['time_avail_m'] == test_date)]
    if not test_obs.empty:
        row = test_obs.iloc[0]
        print(f"Permno {permno} 2007m4: sic2D={row['sic2D']}, Mom6m={row['Mom6m']}, mve_c={row['mve_c']}, IndMom={row['IndMom']}")
    else:
        print(f"Permno {permno} 2007m4: NOT FOUND")

# CHECKPOINT 6: Industry group analysis for 2007m4
print("CHECKPOINT 6: Industry groups in 2007m4:")
april_2007 = df[df['time_avail_m'] == test_date]
industry_stats = april_2007.groupby('sic2D').agg({
    'Mom6m': lambda x: x.notna().sum(),
    'mve_c': lambda x: x.notna().sum(),
    'IndMom': 'first'
}).reset_index()
industry_stats.columns = ['sic2D', 'mom6m_count', 'mve_c_count', 'IndMom']
industry_stats = industry_stats[industry_stats['mom6m_count'] > 0]
print(industry_stats.head(10))

# SAVE
# Stata equivalent: do "$pathCode/savepredictor" IndMom
# Clean up: drop if IndMom == .
df_output = df[df['IndMom'].notna()].copy()

# CHECKPOINT 7: Final output count
print(f"CHECKPOINT 7: Final output observations: {len(df_output)}")
print(f"Original observations: {len(df)}")
print(f"Dropped due to missing IndMom: {len(df) - len(df_output)}")

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