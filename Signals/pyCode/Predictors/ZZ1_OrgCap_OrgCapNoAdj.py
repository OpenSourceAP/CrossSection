# ABOUTME: OrgCap.py - calculates organizational capital predictor
# ABOUTME: Organizational capital based on SG&A with industry adjustment and depreciation

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
import pandas as pd
import numpy as np
sys.path.append('.')
from utils.savepredictor import save_predictor

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

# SIGNAL CONSTRUCTION
# xtset permno time_avail_m equivalent - sort by permno and time
df = df.sort_values(['permno', 'time_avail_m']).reset_index(drop=True)

# bys permno (time_avail_m): gen tempAge = _n 
df['tempAge'] = df.groupby('permno').cumcount() + 1

# replace xsga = 0 if xsga == . (OP p 17)
df['xsga'] = df['xsga'].fillna(0)

# replace xsga = xsga/gnpdefl (price deflation)
df['xsga'] = df['xsga'] / df['gnpdefl']

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

# replace OrgCapNoAdj = OrgCapNoAdj/at
df['OrgCapNoAdj'] = df['OrgCapNoAdj'] / df['at']

# replace OrgCapNoAdj = . if OrgCapNoAdj == 0 (OP p 18: works better without this)
df.loc[df['OrgCapNoAdj'] == 0, 'OrgCapNoAdj'] = np.nan

print(f"After OrgCapNoAdj calculation: {df['OrgCapNoAdj'].notna().sum():,} non-missing values")

# INDUSTRY ADJUSTMENT
# winsor2 OrgCapNoAdj, suffix("temp") cuts(1 99) by(time_avail_m)
# Winsorize by time_avail_m at 1% and 99%
def winsorize_by_group(group, column, lower_pct=0.01, upper_pct=0.99):
    """Winsorize a column within each group"""
    if group[column].isna().all():
        return group[column]
    
    lower_bound = group[column].quantile(lower_pct)
    upper_bound = group[column].quantile(upper_pct)
    
    return group[column].clip(lower=lower_bound, upper=upper_bound)

df['OrgCapNoAdjtemp'] = df.groupby('time_avail_m')['OrgCapNoAdj'].transform(
    lambda x: winsorize_by_group(pd.DataFrame({'val': x}), 'val')
)

# sicff sicCRSP, generate(tempFF17) industry(17)
# Need to create FF17 industry classification from sicCRSP
# This is equivalent to Fama-French 17 industry classification
def sic_to_ff17(sic):
    """Convert SIC code to Fama-French 17 industry classification"""
    if pd.isna(sic):
        return np.nan
    sic = int(sic)
    
    if 1 <= sic <= 999:
        return 1  # Food
    elif 1000 <= sic <= 1499:
        return 2  # Mining
    elif 1500 <= sic <= 1799:
        return 3  # Construction
    elif 2000 <= sic <= 2399:
        return 4  # Food
    elif 2400 <= sic <= 2499:
        return 5  # Textiles
    elif 2500 <= sic <= 2599:
        return 6  # Construction
    elif 2600 <= sic <= 2699:
        return 7  # Paper
    elif 2700 <= sic <= 2799:
        return 8  # Paper
    elif 2800 <= sic <= 2899:
        return 9  # Chemical
    elif 2900 <= sic <= 2999:
        return 10  # Petroleum
    elif 3000 <= sic <= 3099:
        return 11  # Rubber
    elif 3100 <= sic <= 3199:
        return 12  # Leather
    elif 3200 <= sic <= 3299:
        return 13  # Stone
    elif 3300 <= sic <= 3399:
        return 14  # Metal
    elif 3400 <= sic <= 3499:
        return 15  # Metal
    elif 3500 <= sic <= 3599:
        return 16  # Machinery
    elif 3600 <= sic <= 3699:
        return 17  # Electrical
    elif 3700 <= sic <= 3799:
        return 16  # Machinery (Transportation)
    elif 3800 <= sic <= 3899:
        return 17  # Electrical (Instruments)
    elif 3900 <= sic <= 3999:
        return 18  # Miscellaneous
    elif 4000 <= sic <= 4899:
        return 19  # Transportation
    elif 4900 <= sic <= 4999:
        return 20  # Utilities
    elif 5000 <= sic <= 5999:
        return 21  # Wholesale
    elif 6000 <= sic <= 6999:
        return 22  # Financial
    elif 7000 <= sic <= 8999:
        return 23  # Services
    else:
        return np.nan

# Apply FF17 classification to sicCRSP
df['tempFF17'] = df['sicCRSP'].apply(sic_to_ff17)

# drop if mi(tempFF17)
df = df.dropna(subset=['tempFF17']).copy()

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

# SAVE
# Keep only required columns for final output
df_final = df[['permno', 'time_avail_m', 'OrgCap']].dropna(subset=['OrgCap']).copy()

# Save using the standard utility function
save_predictor(df_final, 'OrgCap')

print("OrgCap calculation completed successfully!")