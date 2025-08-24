# ABOUTME: Translates Herf.do to create industry concentration predictor
# ABOUTME: Run from pyCode/ directory: python3 Predictors/Herf.py

# Run from pyCode/ directory
# Inputs: m_aCompustat.parquet, SignalMasterTable.parquet
# Output: ../pyData/Predictors/Herf.csv

import pandas as pd
import numpy as np
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from utils.stata_asreg_asrol import asrol

# DATA LOAD
df = pd.read_parquet('../pyData/Intermediate/m_aCompustat.parquet')
df = df[['permno', 'time_avail_m', 'sale']].copy()

# CHECKPOINT 1: Check initial data load
print(f"Initial observations after loading m_aCompustat: {len(df)}")
test_date = pd.Timestamp('2007-04-30')
for permno in [10006, 11406, 12473]:
    subset = df[(df['permno'] == permno) & (df['time_avail_m'] == test_date)]
    if not subset.empty:
        print(f"permno {permno}, 2007m4: sale={subset['sale'].iloc[0]}")
    else:
        print(f"permno {permno}, 2007m4: not found in initial data")

# Merge with SignalMasterTable
smt = pd.read_parquet('../pyData/Intermediate/SignalMasterTable.parquet')
smt = smt[['permno', 'time_avail_m', 'sicCRSP', 'shrcd']].copy()

df = df.merge(smt, on=['permno', 'time_avail_m'], how='right')

# CHECKPOINT 2: Check after merge with SignalMasterTable
print(f"Observations after merge with SignalMasterTable: {len(df)}")
for permno in [10006, 11406, 12473]:
    subset = df[(df['permno'] == permno) & (df['time_avail_m'] == test_date)]
    if not subset.empty:
        row = subset.iloc[0]
        print(f"permno {permno}, 2007m4: sale={row['sale']}, sicCRSP={row['sicCRSP']}, shrcd={row['shrcd']}")
    else:
        print(f"permno {permno}, 2007m4: not found after merge")

# Sort for lag operations
df = df.sort_values(['permno', 'time_avail_m'])

# SIGNAL CONSTRUCTION
# Create 4-digit SIC code
df['tempSIC'] = df['sicCRSP'].astype(str)
df['sic3D'] = df['tempSIC'].str[:4]

# CHECKPOINT 3: Check SIC code assignment
for permno in [10006, 11406, 12473]:
    subset = df[(df['permno'] == permno) & (df['time_avail_m'] == test_date)]
    if not subset.empty:
        row = subset.iloc[0]
        print(f"permno {permno}, 2007m4: sicCRSP={row['sicCRSP']}, tempSIC={row['tempSIC']}, sic3D={row['sic3D']}")

# Calculate industry sales by SIC and month (only for non-missing sales)
df['indsale'] = df.groupby(['sic3D', 'time_avail_m'])['sale'].transform('sum')

# CHECKPOINT 4: Check industry sales calculation
for permno in [10006, 11406, 12473]:
    subset = df[(df['permno'] == permno) & (df['time_avail_m'] == test_date)]
    if not subset.empty:
        row = subset.iloc[0]
        print(f"permno {permno}, 2007m4: sale={row['sale']}, sic3D={row['sic3D']}, indsale={row['indsale']}")

# Calculate firm's market share squared (will be NaN if sale is missing)
df['temp'] = (df['sale'] / df['indsale']) ** 2

# Calculate Herfindahl index by industry-month (sum excludes NaN values automatically)
df['tempHerf'] = df.groupby(['sic3D', 'time_avail_m'])['temp'].transform('sum')

# CHECKPOINT 5: Check Herfindahl calculation before asrol
for permno in [10006, 11406, 12473]:
    subset = df[(df['permno'] == permno) & (df['time_avail_m'] == test_date)]
    if not subset.empty:
        row = subset.iloc[0]
        print(f"permno {permno}, 2007m4: sale={row['sale']}, temp={row['temp']}, tempHerf={row['tempHerf']}")

# Take 3-year moving average using asrol
df = asrol(df, 'permno', 'time_avail_m', 'tempHerf', 36, 'mean', min_periods=12)
df = df.rename(columns={'mean36_tempHerf': 'Herf'})

# CHECKPOINT 6: Check after asrol moving average
for permno in [10006, 11406, 12473]:
    subset = df[(df['permno'] == permno) & (df['time_avail_m'] == test_date)]
    if not subset.empty:
        row = subset.iloc[0]
        print(f"permno {permno}, 2007m4: tempHerf={row['tempHerf']}, Herf={row['Herf']}")

# Set to missing if not common stock
df.loc[df['shrcd'] > 11, 'Herf'] = np.nan

# CHECKPOINT 7: Check after shrcd filter
non_missing_herf = df['Herf'].notna().sum()
print(f"Non-missing Herf after shrcd filter: {non_missing_herf}")
for permno in [10006, 11406, 12473]:
    subset = df[(df['permno'] == permno) & (df['time_avail_m'] == test_date)]
    if not subset.empty:
        row = subset.iloc[0]
        print(f"permno {permno}, 2007m4: Herf={row['Herf']}, shrcd={row['shrcd']}")

# Missing if regulated industry (Barclay and Smith 1995 definition)
df['year'] = df['time_avail_m'].dt.year

# Regulated industries before deregulation dates
df.loc[(df['tempSIC'].isin(['4011', '4210', '4213'])) & (df['year'] <= 1980), 'Herf'] = np.nan
df.loc[(df['tempSIC'] == '4512') & (df['year'] <= 1978), 'Herf'] = np.nan
df.loc[(df['tempSIC'].isin(['4812', ' 4813'])) & (df['year'] <= 1982), 'Herf'] = np.nan
df.loc[df['tempSIC'].str[:2] == '49', 'Herf'] = np.nan

# CHECKPOINT 8: Check after regulated industry filters
non_missing_herf = df['Herf'].notna().sum()
print(f"Non-missing Herf after regulated industry filters: {non_missing_herf}")
for permno in [10006, 11406, 12473]:
    subset = df[(df['permno'] == permno) & (df['time_avail_m'] == test_date)]
    if not subset.empty:
        row = subset.iloc[0]
        print(f"permno {permno}, 2007m4: Herf={row['Herf']}, tempSIC={row['tempSIC']}, year={row['year']}")

# Set to missing before 1951 (no sales data)
df.loc[df['year'] < 1951, 'Herf'] = np.nan

# CHECKPOINT 9: Final check before save
non_missing_herf = df['Herf'].notna().sum()
print(f"Final non-missing Herf observations: {non_missing_herf}")
for permno in [10006, 11406, 12473]:
    subset = df[(df['permno'] == permno) & (df['time_avail_m'] == test_date)]
    if not subset.empty:
        row = subset.iloc[0]
        print(f"permno {permno}, 2007m4: Herf={row['Herf']}")

# Keep only necessary columns for output
df_final = df[['permno', 'time_avail_m', 'Herf']].copy()
df_final = df_final.dropna(subset=['Herf'])

# Convert time_avail_m to yyyymm format like other predictors
df_final['yyyymm'] = df_final['time_avail_m'].dt.year * 100 + df_final['time_avail_m'].dt.month

# Convert to integers for consistency with other predictors
df_final['permno'] = df_final['permno'].astype('int64')
df_final['yyyymm'] = df_final['yyyymm'].astype('int64')

# Keep only required columns and set index
df_final = df_final[['permno', 'yyyymm', 'Herf']].copy()
df_final = df_final.set_index(['permno', 'yyyymm'])

# SAVE
df_final.to_csv('../pyData/Predictors/Herf.csv')

print("Herf predictor saved successfully")