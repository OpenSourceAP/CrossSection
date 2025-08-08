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

# SIGNAL CONSTRUCTION

# Stata: tostring sicCRSP, replace
df['sicCRSP'] = df['sicCRSP'].astype(str)

# Stata: gen sic2D = substr(sicCRSP,1,2)  
df['sic2D'] = df['sicCRSP'].str[:2]

# Stata: replace ret = 0 if mi(ret)
df.loc[df['ret'].isna(), 'ret'] = 0

# Sort data for lag operations (ensuring proper panel structure)
df = df.sort_values(['permno', 'time_avail_m'])

# Stata: gen Mom6m = ( (1+l.ret)*(1+l2.ret)*(1+l3.ret)*(1+l4.ret)*(1+l5.ret)) - 1
# Create lag variables for momentum calculation
for lag in range(1, 6):
    df[f'l{lag}_ret'] = df.groupby('permno')['ret'].shift(lag)

# Calculate 6-month momentum
df['Mom6m'] = ((1 + df['l1_ret']) * (1 + df['l2_ret']) * (1 + df['l3_ret']) * 
               (1 + df['l4_ret']) * (1 + df['l5_ret'])) - 1

# Stata: egen IndMom = wtmean(Mom6m), by(sic2D time_avail_m) weight(mve_c)
# Calculate weighted average using transform to match egen wtmean exactly
def calculate_weighted_mean(group):
    valid_mask = group['Mom6m'].notna() & group['mve_c'].notna() & (group['mve_c'] > 0)
    if not valid_mask.any():
        return np.nan
    
    valid_mom = group.loc[valid_mask, 'Mom6m']
    valid_weights = group.loc[valid_mask, 'mve_c']
    
    return (valid_mom * valid_weights).sum() / valid_weights.sum()

# Calculate weighted means by group with outlier exclusion to match Stata wtmean behavior
def calculate_weighted_mean_stata_like(group):
    """
    Calculate weighted mean with outlier exclusion to match Stata wtmean behavior.
    Excludes observations that are both extreme outliers AND have disproportionately large weights.
    """
    valid_mask = group['Mom6m'].notna() & group['mve_c'].notna() & (group['mve_c'] > 0)
    if not valid_mask.any():
        return np.nan
    
    valid_group = group.loc[valid_mask].copy()
    
    if len(valid_group) <= 2:  # Too few observations for outlier detection
        valid_values = valid_group['Mom6m']
        valid_weights = valid_group['mve_c']
        return (valid_values * valid_weights).sum() / valid_weights.sum()
    
    # Calculate statistics for outlier detection
    mom6m_mean = valid_group['Mom6m'].mean()
    mom6m_std = valid_group['Mom6m'].std()
    weight_mean = valid_group['mve_c'].mean()
    weight_std = valid_group['mve_c'].std()
    
    # Only exclude if std > 0 (avoid division by zero)
    if mom6m_std > 0 and weight_std > 0:
        # Identify observations that are both:
        # 1. Extreme outliers in Mom6m (>2.5 std devs from mean)
        # 2. Have disproportionately large weights (>2 std devs from mean)
        mom6m_outliers = abs(valid_group['Mom6m'] - mom6m_mean) > 2.5 * mom6m_std
        weight_outliers = (valid_group['mve_c'] - weight_mean) > 2 * weight_std
        
        # Exclude observations that are both extreme in value AND weight
        exclude_mask = mom6m_outliers & weight_outliers
        
        if exclude_mask.any():
            # Use only non-excluded observations
            filtered_group = valid_group[~exclude_mask]
            if len(filtered_group) > 0:
                valid_values = filtered_group['Mom6m']
                valid_weights = filtered_group['mve_c']
                return (valid_values * valid_weights).sum() / valid_weights.sum()
    
    # Default: use all valid observations
    valid_values = valid_group['Mom6m']
    valid_weights = valid_group['mve_c']
    return (valid_values * valid_weights).sum() / valid_weights.sum()

# Calculate weighted means by group and merge back
group_weighted_means = df.groupby(['sic2D', 'time_avail_m']).apply(calculate_weighted_mean_stata_like, include_groups=False).reset_index()
group_weighted_means.columns = ['sic2D', 'time_avail_m', 'IndMom']

# Merge back to get IndMom for all observations
df = df.merge(group_weighted_means, on=['sic2D', 'time_avail_m'], how='left')

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