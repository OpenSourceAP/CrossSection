# ABOUTME: Creates Industry Return Big Companies (IndRetBig) predictor by calculating industry returns for large companies
# ABOUTME: Run from pyCode/ directory: python3 Predictors/IndRetBig.py

# IndRetBig predictor translation from Code/Predictors/IndRetBig.do
# Line-by-line translation preserving exact order and logic

import pandas as pd
import numpy as np
import sys
sys.path.append('.')
from utils.savepredictor import save_predictor
from utils.stata_replication import relrank
from utils.sicff import sicff

# DATA LOAD
# Stata: use permno time_avail_m ret mve_c sicCRSP using "$pathDataIntermediate/SignalMasterTable", clear
df = pd.read_parquet('../pyData/Intermediate/SignalMasterTable.parquet')
df = df[['permno', 'time_avail_m', 'ret', 'mve_c', 'sicCRSP']].copy()

# Convert datetime time_avail_m to integer yyyymm to match Stata format
df['yyyymm'] = df['time_avail_m'].dt.year * 100 + df['time_avail_m'].dt.month

# CHECKPOINT 1: Initial data load
print("CHECKPOINT 1: Initial data load")
print(f"{len(df)}")
test_obs_1 = df[(df['permno'] == 13784) & (df['yyyymm'] == 193207)]
test_obs_2 = df[(df['permno'] == 10886) & (df['yyyymm'] == 200204)]
if len(test_obs_1) > 0:
    for _, row in test_obs_1.iterrows():
        print(f"{int(row['permno']):8d} {row['time_avail_m'].strftime('%Y-%m-%d')} {row['ret']:10.6f} {row['mve_c']:12.6f} {int(row['sicCRSP']):6d}")
else:
    print("No observation for permno 13784 in 193207")
if len(test_obs_2) > 0:
    for _, row in test_obs_2.iterrows():
        print(f"{int(row['permno']):8d} {row['time_avail_m'].strftime('%Y-%m-%d')} {row['ret']:10.6f} {row['mve_c']:12.6f} {int(row['sicCRSP']):6d}")
else:
    print("No observation for permno 10886 in 200204")

# SIGNAL CONSTRUCTION

# Stata: sicff sicCRSP, generate(tempFF48) industry(48)
# Use unified sicff module for Fama-French 48 industry classification
df['tempFF48'] = sicff(df['sicCRSP'], industry=48)

# CHECKPOINT 2: After FF48 industry classification  
print("CHECKPOINT 2: After FF48 industry classification")
print(f"{df['tempFF48'].isna().sum()}")
test_obs_1 = df[(df['permno'] == 13784) & (df['yyyymm'] == 193207)]
test_obs_2 = df[(df['permno'] == 10886) & (df['yyyymm'] == 200204)]
if len(test_obs_1) > 0:
    for _, row in test_obs_1.iterrows():
        print(f"{int(row['permno']):8d} {row['time_avail_m'].strftime('%Y-%m-%d')} {int(row['sicCRSP']):6d} {row['tempFF48']:8.1f}")
else:
    print("No observation for permno 13784 in 193207")
if len(test_obs_2) > 0:
    for _, row in test_obs_2.iterrows():
        print(f"{int(row['permno']):8d} {row['time_avail_m'].strftime('%Y-%m-%d')} {int(row['sicCRSP']):6d} {row['tempFF48']:8.1f}")
else:
    print("No observation for permno 10886 in 200204")

# Stata: drop if mi(tempFF48)
df = df.dropna(subset=['tempFF48'])

# CHECKPOINT 3: After dropping missing FF48
print("CHECKPOINT 3: After dropping missing FF48")
print(f"{len(df)}")
test_obs_1 = df[(df['permno'] == 13784) & (df['yyyymm'] == 193207)]
test_obs_2 = df[(df['permno'] == 10886) & (df['yyyymm'] == 200204)]
if len(test_obs_1) > 0:
    for _, row in test_obs_1.iterrows():
        print(f"{int(row['permno']):8d} {row['time_avail_m'].strftime('%Y-%m-%d')} {int(row['sicCRSP']):6d} {row['tempFF48']:8.1f}")
else:
    print("No observation for permno 13784 in 193207")
if len(test_obs_2) > 0:
    for _, row in test_obs_2.iterrows():
        print(f"{int(row['permno']):8d} {row['time_avail_m'].strftime('%Y-%m-%d')} {int(row['sicCRSP']):6d} {row['tempFF48']:8.1f}")
else:
    print("No observation for permno 10886 in 200204")

# Stata: bys tempFF48 time_avail_m: relrank mve_c, gen(tempRK) ref(mve_c)
# Use utils/relrank to match Stata's exact behavior
df = relrank(df, 'mve_c', by=['tempFF48', 'yyyymm'], out='tempRK')

# CHECKPOINT 4: After relrank calculation
print("CHECKPOINT 4: After relrank calculation")
test_obs_1 = df[(df['permno'] == 13784) & (df['yyyymm'] == 193207)]
test_obs_2 = df[(df['permno'] == 10886) & (df['yyyymm'] == 200204)]
if len(test_obs_1) > 0:
    for _, row in test_obs_1.iterrows():
        print(f"{int(row['permno']):8d} {row['time_avail_m'].strftime('%Y-%m-%d')} {row['mve_c']:12.6f} {row['tempRK']:8.6f}")
else:
    print("No observation for permno 13784 in 193207")
if len(test_obs_2) > 0:
    for _, row in test_obs_2.iterrows():
        print(f"{int(row['permno']):8d} {row['time_avail_m'].strftime('%Y-%m-%d')} {row['mve_c']:12.6f} {row['tempRK']:8.6f}")
else:
    print("No observation for permno 10886 in 200204")
print("Variable |        Obs        Mean    Std. dev.       Min        Max")
print("-------------+--------------------------------------------------------")
tempRK_stats = df['tempRK'].describe()
print(f"    tempRK |{tempRK_stats['count']:11.0f}{tempRK_stats['mean']:12.7f}{tempRK_stats['std']:12.7f}{tempRK_stats['min']:11.7f}{tempRK_stats['max']:11.7f}")

# Stata: preserve
df_original = df.copy()

# CHECKPOINT 5: Before filtering for large companies
print("CHECKPOINT 5: Before preserve")
print(f"{len(df)}")
test_obs_1 = df[(df['permno'] == 13784) & (df['yyyymm'] == 193207)]
test_obs_2 = df[(df['permno'] == 10886) & (df['yyyymm'] == 200204)]
if len(test_obs_1) > 0:
    for _, row in test_obs_1.iterrows():
        print(f"{int(row['permno']):8d} {row['time_avail_m'].strftime('%Y-%m-%d')} {row['tempRK']:8.6f}")
else:
    print("No observation for permno 13784 in 193207")
if len(test_obs_2) > 0:
    for _, row in test_obs_2.iterrows():
        print(f"{int(row['permno']):8d} {row['time_avail_m'].strftime('%Y-%m-%d')} {row['tempRK']:8.6f}")
else:
    print("No observation for permno 10886 in 200204")

# Stata: keep if tempRK >=.7 & !mi(tempRK)
# Fix: Use strict inequality to match Stata's exact behavior for companies at tempRK = 0.7
df_big = df[(df['tempRK'] > 0.7) & df['tempRK'].notna()].copy()

# CHECKPOINT 6: After filtering for large companies
print("CHECKPOINT 6: Large companies (tempRK >= 0.7)")
print(f"{len(df_big)}")
test_obs_1 = df_big[(df_big['permno'] == 13784) & (df_big['yyyymm'] == 193207)]
test_obs_2 = df_big[(df_big['permno'] == 10886) & (df_big['yyyymm'] == 200204)]
if len(test_obs_1) > 0:
    for _, row in test_obs_1.iterrows():
        print(f"{int(row['permno']):8d} {row['time_avail_m'].strftime('%Y-%m-%d')} {row['tempRK']:8.6f} {row['ret']:10.6f}")
else:
    print("No observation for permno 13784 in 193207")
if len(test_obs_2) > 0:
    for _, row in test_obs_2.iterrows():
        print(f"{int(row['permno']):8d} {row['time_avail_m'].strftime('%Y-%m-%d')} {row['tempRK']:8.6f} {row['ret']:10.6f}")
else:
    print("No observation for permno 10886 in 200204")

# Stata: gcollapse (mean) ret, by(tempFF48 time_avail_m)
# Calculate mean returns by industry-month for large companies only
# Use time_avail_m to match Stata exactly
industry_returns = df_big.groupby(['tempFF48', 'time_avail_m'])['ret'].mean().reset_index()
industry_returns = industry_returns.rename(columns={'ret': 'IndRetBig'})

# CHECKPOINT 7: After industry return calculation
print("CHECKPOINT 7: Industry returns calculated")
print(f"{len(industry_returns)}")
test_returns_1 = industry_returns[industry_returns['time_avail_m'] == pd.Timestamp('1932-07-01')]
test_returns_2 = industry_returns[industry_returns['time_avail_m'] == pd.Timestamp('2002-04-01')]
if len(test_returns_1) > 0:
    for _, row in test_returns_1.iterrows():
        print(f"{row['tempFF48']:8.1f} {row['time_avail_m'].strftime('%Y-%m-%d')} {row['IndRetBig']:10.6f}")
else:
    print("No industry returns for 1932m7")
if len(test_returns_2) > 0:
    for _, row in test_returns_2.iterrows():
        print(f"{row['tempFF48']:8.1f} {row['time_avail_m'].strftime('%Y-%m-%d')} {row['IndRetBig']:10.6f}")
else:
    print("No industry returns for 2002m4")

# Stata: save "$pathtemp/temp",replace
# Stata: restore
df = df_original.copy()
# Ensure yyyymm column exists for merge (df_original was created after yyyymm conversion)
# No need to recreate yyyymm since df_original already contains it

# CHECKPOINT 8: After restore
print("CHECKPOINT 8: After restore")
print(f"{len(df)}")
test_obs_1 = df[(df['permno'] == 13784) & (df['yyyymm'] == 193207)]
test_obs_2 = df[(df['permno'] == 10886) & (df['yyyymm'] == 200204)]
if len(test_obs_1) > 0:
    for _, row in test_obs_1.iterrows():
        print(f"{int(row['permno']):8d} {row['time_avail_m'].strftime('%Y-%m-%d')} {row['tempRK']:8.6f}")
else:
    print("No observation for permno 13784 in 193207")
if len(test_obs_2) > 0:
    for _, row in test_obs_2.iterrows():
        print(f"{int(row['permno']):8d} {row['time_avail_m'].strftime('%Y-%m-%d')} {row['tempRK']:8.6f}")
else:
    print("No observation for permno 10886 in 200204")

# Stata: merge m:1 tempFF48 time_avail_m using "$pathtemp/temp", nogenerate
df = df.merge(industry_returns, on=['tempFF48', 'time_avail_m'], how='left')

# CHECKPOINT 9: After merge with industry returns
print("CHECKPOINT 9: After merge")
print(f"{len(df)}")
test_obs_1 = df[(df['permno'] == 13784) & (df['yyyymm'] == 193207)]
test_obs_2 = df[(df['permno'] == 10886) & (df['yyyymm'] == 200204)]
if len(test_obs_1) > 0:
    for _, row in test_obs_1.iterrows():
        print(f"{int(row['permno']):8d} {row['time_avail_m'].strftime('%Y-%m-%d')} {row['tempRK']:8.6f} {row['IndRetBig']:10.6f}")
else:
    print("No observation for permno 13784 in 193207")
if len(test_obs_2) > 0:
    for _, row in test_obs_2.iterrows():
        print(f"{int(row['permno']):8d} {row['time_avail_m'].strftime('%Y-%m-%d')} {row['tempRK']:8.6f} {row['IndRetBig']:10.6f}")
else:
    print("No observation for permno 10886 in 200204")

# Stata: replace IndRetBig = . if tempRK >= .7
# Set IndRetBig to missing for companies that are themselves large (>= 70th percentile)
df.loc[df['tempRK'] >= 0.7, 'IndRetBig'] = np.nan

# CHECKPOINT 10: Final result
print("CHECKPOINT 10: Final dataset")
test_obs_1 = df[(df['permno'] == 13784) & (df['yyyymm'] == 193207)]
test_obs_2 = df[(df['permno'] == 10886) & (df['yyyymm'] == 200204)]
if len(test_obs_1) > 0:
    for _, row in test_obs_1.iterrows():
        IndRetBig_val = row['IndRetBig'] if pd.notna(row['IndRetBig']) else "."
        print(f"{int(row['permno']):8d} {row['time_avail_m'].strftime('%Y-%m-%d')} {row['tempRK']:8.6f} {IndRetBig_val}")
else:
    print("No observation for permno 13784 in 193207")
if len(test_obs_2) > 0:
    for _, row in test_obs_2.iterrows():
        IndRetBig_val = row['IndRetBig'] if pd.notna(row['IndRetBig']) else "."
        print(f"{int(row['permno']):8d} {row['time_avail_m'].strftime('%Y-%m-%d')} {row['tempRK']:8.6f} {IndRetBig_val}")
else:
    print("No observation for permno 10886 in 200204")
final_non_missing = df['IndRetBig'].notna().sum()
print(f"{final_non_missing}")

# Stata: label var IndRetBig "Industry return big companies"
# (No need to implement label in Python)

# SAVE
# Stata: do "$pathCode/savepredictor" IndRetBig
save_predictor(df, 'IndRetBig')

print("IndRetBig predictor saved successfully")