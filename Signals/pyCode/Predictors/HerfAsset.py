# ABOUTME: Translates HerfAsset.do to create asset-based industry concentration predictor
# ABOUTME: Run from pyCode/ directory: python3 Predictors/HerfAsset.py

# Run from pyCode/ directory
# Inputs: m_aCompustat.parquet, SignalMasterTable.parquet
# Output: ../pyData/Predictors/HerfAsset.csv

import pandas as pd
import numpy as np
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from utils.asrol import asrol

# DATA LOAD
df = pd.read_parquet('../pyData/Intermediate/m_aCompustat.parquet')
df = df[['permno', 'time_avail_m', 'at']].copy()

# CHECKPOINT 1: Check initial data load
print("CHECKPOINT 1: After loading m_aCompustat")
print(f"Total observations: {len(df)}")
target_date = pd.Timestamp('2007-04-01')
print("Sample observations for problematic permnos:")
test_obs = df[(df['permno'] == 10006) & (df['time_avail_m'] == target_date)]
if not test_obs.empty:
    print(f"Permno 10006, 2007m4: {test_obs[['permno', 'time_avail_m', 'at']].iloc[0].to_dict()}")
test_obs = df[(df['permno'] == 11406) & (df['time_avail_m'] == target_date)]
if not test_obs.empty:
    print(f"Permno 11406, 2007m4: {test_obs[['permno', 'time_avail_m', 'at']].iloc[0].to_dict()}")

# Merge with SignalMasterTable
smt = pd.read_parquet('../pyData/Intermediate/SignalMasterTable.parquet')
smt = smt[['permno', 'time_avail_m', 'sicCRSP', 'shrcd']].copy()

df = df.merge(smt, on=['permno', 'time_avail_m'], how='inner')

# CHECKPOINT 2: Check after merge with SignalMasterTable
print("\nCHECKPOINT 2: After merge with SignalMasterTable")
print(f"Total observations: {len(df)}")
test_obs = df[(df['permno'] == 10006) & (df['time_avail_m'] == target_date)]
if not test_obs.empty:
    print(f"Permno 10006, 2007m4: {test_obs[['permno', 'time_avail_m', 'at', 'sicCRSP', 'shrcd']].iloc[0].to_dict()}")
test_obs = df[(df['permno'] == 11406) & (df['time_avail_m'] == target_date)]
if not test_obs.empty:
    print(f"Permno 11406, 2007m4: {test_obs[['permno', 'time_avail_m', 'at', 'sicCRSP', 'shrcd']].iloc[0].to_dict()}")

# Sort for lag operations
df = df.sort_values(['permno', 'time_avail_m'])

# SIGNAL CONSTRUCTION
# Create 4-digit SIC code
df['tempSIC'] = df['sicCRSP'].astype(str)
df['sic3D'] = df['tempSIC'].str[:4]

# CHECKPOINT 3: Check SIC code creation
print("\nCHECKPOINT 3: After creating SIC codes")
test_obs = df[(df['permno'] == 10006) & (df['time_avail_m'] == target_date)]
if not test_obs.empty:
    print(f"Permno 10006, 2007m4: {test_obs[['permno', 'time_avail_m', 'sicCRSP', 'tempSIC', 'sic3D']].iloc[0].to_dict()}")
test_obs = df[(df['permno'] == 11406) & (df['time_avail_m'] == target_date)]
if not test_obs.empty:
    print(f"Permno 11406, 2007m4: {test_obs[['permno', 'time_avail_m', 'sicCRSP', 'tempSIC', 'sic3D']].iloc[0].to_dict()}")

# Calculate industry assets by SIC and month
df['indasset'] = df.groupby(['sic3D', 'time_avail_m'])['at'].transform('sum')

# Calculate firm's asset share squared
df['temp'] = (df['at'] / df['indasset']) ** 2

# Calculate Herfindahl index by industry-month
df['tempHerf'] = df.groupby(['sic3D', 'time_avail_m'])['temp'].transform('sum')

# CHECKPOINT 4: Check before asrol (moving average)
print("\nCHECKPOINT 4: Before asrol moving average")
test_obs = df[(df['permno'] == 10006) & (df['time_avail_m'] == target_date)]
if not test_obs.empty:
    print(f"Permno 10006, 2007m4: {test_obs[['permno', 'time_avail_m', 'at', 'indasset', 'temp', 'tempHerf']].iloc[0].to_dict()}")
test_obs = df[(df['permno'] == 11406) & (df['time_avail_m'] == target_date)]
if not test_obs.empty:
    print(f"Permno 11406, 2007m4: {test_obs[['permno', 'time_avail_m', 'at', 'indasset', 'temp', 'tempHerf']].iloc[0].to_dict()}")
print(f"Sample of tempHerf values - mean: {df['tempHerf'].mean():.6f}, std: {df['tempHerf'].std():.6f}")
print(f"tempHerf range: {df['tempHerf'].min():.6f} to {df['tempHerf'].max():.6f}")

# Take 3-year moving average using asrol
df = asrol(df, 'permno', 'time_avail_m', 'tempHerf', 36, 'mean', min_periods=12)
df = df.rename(columns={'mean36_tempHerf': 'HerfAsset'})

# CHECKPOINT 5: Check after asrol moving average
print("\nCHECKPOINT 5: After asrol moving average")
test_obs = df[(df['permno'] == 10006) & (df['time_avail_m'] == target_date)]
if not test_obs.empty:
    print(f"Permno 10006, 2007m4: {test_obs[['permno', 'time_avail_m', 'tempHerf', 'HerfAsset']].iloc[0].to_dict()}")
test_obs = df[(df['permno'] == 11406) & (df['time_avail_m'] == target_date)]
if not test_obs.empty:
    print(f"Permno 11406, 2007m4: {test_obs[['permno', 'time_avail_m', 'tempHerf', 'HerfAsset']].iloc[0].to_dict()}")
print(f"Non-null HerfAsset observations: {df['HerfAsset'].notna().sum()}")
print(f"HerfAsset range: {df['HerfAsset'].min():.6f} to {df['HerfAsset'].max():.6f}")

# Set to missing if not common stock
df.loc[df['shrcd'] > 11, 'HerfAsset'] = np.nan

# CHECKPOINT 6: Check after shrcd filter
print("\nCHECKPOINT 6: After shrcd > 11 filter")
test_obs = df[(df['permno'] == 10006) & (df['time_avail_m'] == target_date)]
if not test_obs.empty:
    print(f"Permno 10006, 2007m4: {test_obs[['permno', 'time_avail_m', 'shrcd', 'HerfAsset']].iloc[0].to_dict()}")
test_obs = df[(df['permno'] == 11406) & (df['time_avail_m'] == target_date)]
if not test_obs.empty:
    print(f"Permno 11406, 2007m4: {test_obs[['permno', 'time_avail_m', 'shrcd', 'HerfAsset']].iloc[0].to_dict()}")
print(f"Non-null HerfAsset observations: {df['HerfAsset'].notna().sum()}")

# Missing if regulated industry (Barclay and Smith 1995 definition)
df['year'] = df['time_avail_m'].dt.year

# Regulated industries before deregulation dates
df.loc[(df['tempSIC'].isin(['4011', '4210', '4213'])) & (df['year'] <= 1980), 'HerfAsset'] = np.nan
df.loc[(df['tempSIC'] == '4512') & (df['year'] <= 1978), 'HerfAsset'] = np.nan
df.loc[(df['tempSIC'].isin(['4812', '4813'])) & (df['year'] <= 1982), 'HerfAsset'] = np.nan
df.loc[df['tempSIC'].str[:2] == '49', 'HerfAsset'] = np.nan

# CHECKPOINT 7: Check after all regulated industry filters
print("\nCHECKPOINT 7: After regulated industry filters")
test_obs = df[(df['permno'] == 10006) & (df['time_avail_m'] == target_date)]
if not test_obs.empty:
    print(f"Permno 10006, 2007m4: {test_obs[['permno', 'time_avail_m', 'year', 'tempSIC', 'HerfAsset']].iloc[0].to_dict()}")
test_obs = df[(df['permno'] == 11406) & (df['time_avail_m'] == target_date)]
if not test_obs.empty:
    print(f"Permno 11406, 2007m4: {test_obs[['permno', 'time_avail_m', 'year', 'tempSIC', 'HerfAsset']].iloc[0].to_dict()}")
print(f"Non-null HerfAsset observations: {df['HerfAsset'].notna().sum()}")
print(f"Final sample statistics - mean: {df['HerfAsset'].mean():.6f}, std: {df['HerfAsset'].std():.6f}")
print(f"HerfAsset range: {df['HerfAsset'].min():.6f} to {df['HerfAsset'].max():.6f}")

# Keep only necessary columns for output
df_final = df[['permno', 'time_avail_m', 'HerfAsset']].copy()
df_final = df_final.dropna(subset=['HerfAsset'])

# Convert time_avail_m to yyyymm format like other predictors
df_final['yyyymm'] = df_final['time_avail_m'].dt.year * 100 + df_final['time_avail_m'].dt.month

# Convert to integers for consistency with other predictors
df_final['permno'] = df_final['permno'].astype('int64')
df_final['yyyymm'] = df_final['yyyymm'].astype('int64')

# Keep only required columns and set index
df_final = df_final[['permno', 'yyyymm', 'HerfAsset']].copy()
df_final = df_final.set_index(['permno', 'yyyymm'])

# CHECKPOINT 8: Final output check
print("\nCHECKPOINT 8: Final output before save")
print(f"Final observations: {len(df_final)}")
print("Sample of final data:")
print(df_final.head(10))
print(f"Final HerfAsset range: {df_final['HerfAsset'].min():.6f} to {df_final['HerfAsset'].max():.6f}")

# SAVE
df_final.to_csv('../pyData/Predictors/HerfAsset.csv')

print("HerfAsset predictor saved successfully")