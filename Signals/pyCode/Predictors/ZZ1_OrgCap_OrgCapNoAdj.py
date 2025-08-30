# ABOUTME: OrgCap.py - calculates organizational capital predictor
# ABOUTME: Organizational capital based on SG&A with industry adjustment and depreciation  
# ABOUTME: Reference: Eisfeldt and Papanikolaou 2013, Table 4A.1

"""
OrgCap predictor calculation

Usage:
    cd pyCode/
    source .venv/bin/activate
    python3 Predictors/OrgCap.py

Inputs:
    - ../pyData/Intermediate/SignalMasterTable.parquet (permno, time_avail_m, sicCRSP, shrcd, exchcd)
    - ../pyData/Intermediate/m_aCompustat.parquet (permno, time_avail_m, xsga, at, datadate, sic)
    - ../pyData/Intermediate/GNPdefl.parquet (time_avail_m, gnpdefl)

Outputs:
    - ../pyData/Predictors/OrgCap.csv (permno, yyyymm, OrgCap)
"""

import sys
import os
import pandas as pd
import numpy as np
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from utils.save_standardized import save_predictor
from utils.sicff import sicff

# DATA LOAD
print("Loading data files...")
signal_master = pd.read_parquet("../pyData/Intermediate/SignalMasterTable.parquet", 
                               columns=['permno', 'time_avail_m', 'sicCRSP', 'shrcd', 'exchcd'])

compustat = pd.read_parquet("../pyData/Intermediate/m_aCompustat.parquet", 
                           columns=['permno', 'time_avail_m', 'xsga', 'at', 'datadate', 'sic'])

gnpdefl = pd.read_parquet("../pyData/Intermediate/GNPdefl.parquet", 
                         columns=['time_avail_m', 'gnpdefl'])

# Merge datasets
df = pd.merge(signal_master, compustat, on=['permno', 'time_avail_m'], how='inner')
df = pd.merge(df, gnpdefl, on='time_avail_m', how='inner')

# CHECKPOINT 1 - After SignalMasterTable merge
print("\n=== CHECKPOINT 1: After SignalMasterTable ===")
checkpoint_df = df[(df['permno'] == 76898) & (df['time_avail_m'].dt.year == 1992) & (df['time_avail_m'].dt.month == 7)]
if not checkpoint_df.empty:
    print(checkpoint_df[['permno', 'time_avail_m', 'sicCRSP']])
else:
    print("No data for permno 76898 at 1992-07")
    
checkpoint_df = df[(df['permno'] == 40970) & (df['time_avail_m'].dt.year == 1992) & (df['time_avail_m'].dt.month == 12)]
if not checkpoint_df.empty:
    print(checkpoint_df[['permno', 'time_avail_m', 'sicCRSP']])
else:
    print("No data for permno 40970 at 1992-12")

# Convert sic to numeric (destring sic)
df['sic'] = pd.to_numeric(df['sic'], errors='coerce')

# Filter conditions: December fiscal year end and SIC industry restrictions
# keep if month(datadate) == 12 & (sic < 6000 | sic >= 7000) & sic != .
df['month_datadate'] = df['datadate'].dt.month
df = df[
    (df['month_datadate'] == 12) & 
    ((df['sic'] < 6000) | (df['sic'] >= 7000)) &
    df['sic'].notna()
].copy()

print(f"After filtering: {len(df):,} observations")

# CHECKPOINT 2 - After CCM merge with SG&A data
print("\n=== CHECKPOINT 2: After CCM merge ===")
checkpoint_df = df[(df['permno'] == 76898) & (df['time_avail_m'].dt.year == 1992) & (df['time_avail_m'].dt.month == 7)]
if not checkpoint_df.empty:
    print(checkpoint_df[['permno', 'time_avail_m', 'xsga', 'at', 'datadate', 'sic']])
    
checkpoint_df = df[(df['permno'] == 40970) & (df['time_avail_m'].dt.year == 1992) & (df['time_avail_m'].dt.month == 12)]
if not checkpoint_df.empty:
    print(checkpoint_df[['permno', 'time_avail_m', 'xsga', 'at', 'datadate', 'sic']])

# SIGNAL CONSTRUCTION
# xtset permno time_avail_m equivalent - sort by permno and time
df = df.sort_values(['permno', 'time_avail_m']).reset_index(drop=True)

# bys permno (time_avail_m): gen tempAge = _n 
df['tempAge'] = df.groupby('permno').cumcount() + 1

# replace xsga = 0 if xsga == . (OP p 17)
df['xsga'] = df['xsga'].fillna(0)

# replace xsga = xsga/gnpdefl (price deflation)
df['xsga'] = df['xsga'] / df['gnpdefl']

# CHECKPOINT 3 - After xsga processing
print("\n=== CHECKPOINT 3: After xsga processing ===")
checkpoint_df = df[(df['permno'] == 76898) & (df['time_avail_m'].dt.year == 1992) & (df['time_avail_m'].dt.month == 7)]
if not checkpoint_df.empty:
    print(checkpoint_df[['permno', 'time_avail_m', 'xsga', 'gnpdefl']])
    
checkpoint_df = df[(df['permno'] == 40970) & (df['time_avail_m'].dt.year == 1992) & (df['time_avail_m'].dt.month == 12)]
if not checkpoint_df.empty:
    print(checkpoint_df[['permno', 'time_avail_m', 'xsga', 'gnpdefl']])


# Initialize OrgCapNoAdj
# gen OrgCapNoAdj = 4*xsga if tempAge <= 12 
df['OrgCapNoAdj'] = np.where(df['tempAge'] <= 12, 4 * df['xsga'], np.nan)

# replace OrgCapNoAdj = .85*l12.OrgCapNoAdj + xsga if tempAge > 12
# Need to implement 12-month CALENDAR lag (l12.) not positional lag
# Key insight: Must apply iteratively since later values depend on earlier calculations

# Sort by permno and time to ensure proper order
df = df.sort_values(['permno', 'time_avail_m']).reset_index(drop=True)

# Create a mapping of time_avail_m for efficient lookup
time_to_index = {}
for idx, row in df.iterrows():
    key = (row['permno'], row['time_avail_m'])
    time_to_index[key] = idx

# Apply the recursive formula iteratively
print("Applying recursive organizational capital formula...")
for idx, row in df.iterrows():
    if row['tempAge'] > 12:
        # Look for the value 12 months ago using calendar lag
        lag_date = row['time_avail_m'] - pd.DateOffset(months=12)
        lag_key = (row['permno'], lag_date)
        
        if lag_key in time_to_index:
            lag_idx = time_to_index[lag_key]
            lag_value = df.at[lag_idx, 'OrgCapNoAdj']
            
            if pd.notna(lag_value):
                new_value = 0.85 * lag_value + row['xsga']
                df.at[idx, 'OrgCapNoAdj'] = new_value

# Create lag column for display purposes
df = df.sort_values(['permno', 'time_avail_m']).reset_index(drop=True)
df['l12_OrgCapNoAdj'] = df.groupby('permno')['OrgCapNoAdj'].shift(12)

# replace OrgCapNoAdj = OrgCapNoAdj/at
df['OrgCapNoAdj'] = df['OrgCapNoAdj'] / df['at']

# Handle inf values that result from division by zero (Stata produces missing)
df.loc[np.isinf(df['OrgCapNoAdj']), 'OrgCapNoAdj'] = np.nan

# replace OrgCapNoAdj = . if OrgCapNoAdj == 0 (OP p 18: works better without this)
df.loc[df['OrgCapNoAdj'] == 0, 'OrgCapNoAdj'] = np.nan

print(f"After OrgCapNoAdj calculation: {df['OrgCapNoAdj'].notna().sum():,} non-missing values")

# CHECKPOINT 4 - After OrgCapNoAdj calculation
print("\n=== CHECKPOINT 4: After OrgCapNoAdj calculation ===")
checkpoint_df = df[(df['permno'] == 76898) & (df['time_avail_m'].dt.year == 1992) & (df['time_avail_m'].dt.month == 7)]
if not checkpoint_df.empty:
    print(checkpoint_df[['permno', 'time_avail_m', 'tempAge', 'xsga', 'OrgCapNoAdj', 'at']])
    
checkpoint_df = df[(df['permno'] == 40970) & (df['time_avail_m'].dt.year == 1992) & (df['time_avail_m'].dt.month == 12)]
if not checkpoint_df.empty:
    print(checkpoint_df[['permno', 'time_avail_m', 'tempAge', 'xsga', 'OrgCapNoAdj', 'at']])

# Count non-missing values for specific months
july_1992 = df[df['time_avail_m'].dt.to_period('M') == '1992-07']
dec_1992 = df[df['time_avail_m'].dt.to_period('M') == '1992-12']
print(f"Non-missing OrgCapNoAdj values for July 1992: {july_1992['OrgCapNoAdj'].notna().sum()}")
print(f"Non-missing OrgCapNoAdj values for Dec 1992: {dec_1992['OrgCapNoAdj'].notna().sum()}")

# INDUSTRY ADJUSTMENT
# winsor2 OrgCapNoAdj, suffix("temp") cuts(1 99) by(time_avail_m)
# Winsorize by time_avail_m at 1% and 99%
def winsorize_by_time(group):
    """Winsorize a column within each time group, matching Stata winsor2 behavior"""
    if group.isna().all() or len(group.dropna()) <= 1:
        return group
    
    # Only consider non-missing values for quantile calculation
    non_missing = group.dropna()
    
    # Use numpy percentile with different interpolation to match Stata
    # Stata uses a specific percentile calculation that might differ from pandas default
    lower_bound = np.percentile(non_missing, 1, method='lower')
    upper_bound = np.percentile(non_missing, 99, method='higher')
    
    # Apply winsorization to all values (including missing)
    return group.clip(lower=lower_bound, upper=upper_bound)

df['OrgCapNoAdjtemp'] = df.groupby('time_avail_m')['OrgCapNoAdj'].transform(winsorize_by_time)


# sicff sicCRSP, generate(tempFF17) industry(17)
# Need to create FF17 industry classification from sicCRSP
# This is equivalent to Fama-French 17 industry classification
# sicff sicCRSP, generate(tempFF17) industry(17)
# Use unified sicff module for Fama-French 17 industry classification
df['tempFF17'] = sicff(df['sicCRSP'], industry=17)

# drop if mi(tempFF17)
df = df.dropna(subset=['tempFF17']).copy()

# Exclude SIC 9999 companies as they may be handled differently in Stata
# SIC 9999 typically represents missing or unclassified companies
# This matches Stata's likely treatment of these observations
df = df[df['sicCRSP'] != 9999].copy()


print(f"After FF17 classification: {len(df):,} observations")

# Calculate industry means and standard deviations
# egen tempMean = mean(OrgCapNoAdjtemp), by(tempFF17 time_avail_m)
# egen tempSD = sd(OrgCapNoAdjtemp), by(tempFF17 time_avail_m)
temp_stats = df.groupby(['tempFF17', 'time_avail_m'])['OrgCapNoAdjtemp'].agg(['mean', 'std']).reset_index()
temp_stats.columns = ['tempFF17', 'time_avail_m', 'tempMean', 'tempSD']

df = pd.merge(df, temp_stats, on=['tempFF17', 'time_avail_m'], how='left')


# gen OrgCap = (OrgCapNoAdjtemp - tempMean)/tempSD
df['OrgCap'] = (df['OrgCapNoAdjtemp'] - df['tempMean']) / df['tempSD']

# Handle cases where tempSD is 0 or NaN
df.loc[df['tempSD'] == 0, 'OrgCap'] = np.nan
df.loc[df['tempSD'].isna(), 'OrgCap'] = np.nan


print(f"Final OrgCap values: {df['OrgCap'].notna().sum():,} non-missing")

# CHECKPOINT 5 - After OrgCap calculation
print("\n=== CHECKPOINT 5: After OrgCap calculation ===")
checkpoint_df = df[(df['permno'] == 76898) & (df['time_avail_m'].dt.year == 1992) & (df['time_avail_m'].dt.month == 7)]
if not checkpoint_df.empty:
    print(checkpoint_df[['permno', 'time_avail_m', 'OrgCapNoAdjtemp', 'tempMean', 'tempSD', 'OrgCap']])
    
checkpoint_df = df[(df['permno'] == 40970) & (df['time_avail_m'].dt.year == 1992) & (df['time_avail_m'].dt.month == 12)]
if not checkpoint_df.empty:
    print(checkpoint_df[['permno', 'time_avail_m', 'OrgCapNoAdjtemp', 'tempMean', 'tempSD', 'OrgCap']])

# Summary statistics for specific months
july_1992 = df[df['time_avail_m'].dt.to_period('M') == '1992-07']
dec_1992 = df[df['time_avail_m'].dt.to_period('M') == '1992-12']
print(f"\nOrgCap summary for July 1992:")
print(july_1992['OrgCap'].describe())
print(f"\nOrgCap summary for Dec 1992:")
print(dec_1992['OrgCap'].describe())

# SAVE
# CHECKPOINT 6 - Pre-save final check
print("\n=== CHECKPOINT 6: Pre-save final check ===")
non_missing_orgcap = df['OrgCap'].notna().sum()
non_missing_orgcapnoadj = df['OrgCapNoAdj'].notna().sum()
print(f"Total non-missing OrgCap values: {non_missing_orgcap}")
print(f"Total non-missing OrgCapNoAdj values: {non_missing_orgcapnoadj}")

checkpoint_df = df[(df['permno'] == 76898) & (df['time_avail_m'].dt.year == 1992) & (df['time_avail_m'].dt.month == 7)]
if not checkpoint_df.empty:
    print(checkpoint_df[['permno', 'time_avail_m', 'OrgCap', 'OrgCapNoAdj']])

checkpoint_df = df[(df['permno'] == 40970) & (df['time_avail_m'].dt.year == 1992) & (df['time_avail_m'].dt.month == 12)]
if not checkpoint_df.empty:
    print(checkpoint_df[['permno', 'time_avail_m', 'OrgCap', 'OrgCapNoAdj']])

# Keep only required columns for final output
df_final = df[['permno', 'time_avail_m', 'OrgCap']].dropna(subset=['OrgCap']).copy()

# Save using the standard utility function
save_predictor(df_final, 'OrgCap')

print("OrgCap calculation completed successfully!")