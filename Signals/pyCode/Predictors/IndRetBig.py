# ABOUTME: Creates Industry Return Big Companies (IndRetBig) predictor by calculating industry returns for large companies
# ABOUTME: Run from pyCode/ directory: python3 Predictors/IndRetBig.py

# IndRetBig predictor translation from Code/Predictors/IndRetBig.do
# Line-by-line translation preserving exact order and logic

import pandas as pd
import numpy as np
import sys
sys.path.append('.')
from utils.savepredictor import save_predictor
from utils.relrank import relrank
from utils.sicff import sicff

# DATA LOAD
# Stata: use permno time_avail_m ret mve_c sicCRSP using "$pathDataIntermediate/SignalMasterTable", clear
df = pd.read_parquet('../pyData/Intermediate/SignalMasterTable.parquet')
df = df[['permno', 'time_avail_m', 'ret', 'mve_c', 'sicCRSP']].copy()

# Convert datetime time_avail_m to integer yyyymm to match Stata format
df['yyyymm'] = df['time_avail_m'].dt.year * 100 + df['time_avail_m'].dt.month

# CHECKPOINT 1: Initial data load
print(f"CHECKPOINT 1: Loaded {len(df)} observations")
test_obs_1 = df[(df['permno'] == 10006) & (df['yyyymm'] == 200704)]
test_obs_2 = df[(df['permno'] == 11406) & (df['yyyymm'] == 200704)]
print(f"Test obs 10006 2007m4: {len(test_obs_1)} rows")
if len(test_obs_1) > 0:
    print(test_obs_1[['permno', 'time_avail_m', 'ret', 'mve_c', 'sicCRSP']].to_string())
print(f"Test obs 11406 2007m4: {len(test_obs_2)} rows")
if len(test_obs_2) > 0:
    print(test_obs_2[['permno', 'time_avail_m', 'ret', 'mve_c', 'sicCRSP']].to_string())

# SIGNAL CONSTRUCTION

# Stata: sicff sicCRSP, generate(tempFF48) industry(48)
# Use unified sicff module for Fama-French 48 industry classification
df['tempFF48'] = sicff(df['sicCRSP'], industry=48)

# CHECKPOINT 2: After FF48 industry classification
print("CHECKPOINT 2: FF48 classification complete")
test_obs_1 = df[(df['permno'] == 10006) & (df['yyyymm'] == 200704)]
test_obs_2 = df[(df['permno'] == 11406) & (df['yyyymm'] == 200704)]
print(f"Test obs 10006 2007m4: {len(test_obs_1)} rows")
if len(test_obs_1) > 0:
    print(test_obs_1[['permno', 'time_avail_m', 'sicCRSP', 'tempFF48']].to_string())
print(f"Test obs 11406 2007m4: {len(test_obs_2)} rows")
if len(test_obs_2) > 0:
    print(test_obs_2[['permno', 'time_avail_m', 'sicCRSP', 'tempFF48']].to_string())
print(f"Missing FF48 observations: {df['tempFF48'].isna().sum()}")

# Stata: drop if mi(tempFF48)
df = df.dropna(subset=['tempFF48'])

# CHECKPOINT 3: After dropping missing FF48
print(f"CHECKPOINT 3: After dropping missing FF48, {len(df)} observations remain")
test_obs_1 = df[(df['permno'] == 10006) & (df['yyyymm'] == 200704)]
test_obs_2 = df[(df['permno'] == 11406) & (df['yyyymm'] == 200704)]
print(f"Test obs 10006 2007m4: {len(test_obs_1)} rows")
if len(test_obs_1) > 0:
    print(test_obs_1[['permno', 'time_avail_m', 'sicCRSP', 'tempFF48']].to_string())
print(f"Test obs 11406 2007m4: {len(test_obs_2)} rows")
if len(test_obs_2) > 0:
    print(test_obs_2[['permno', 'time_avail_m', 'sicCRSP', 'tempFF48']].to_string())

# Stata: bys tempFF48 time_avail_m: relrank mve_c, gen(tempRK) ref(mve_c)
# Use utils/relrank to match Stata's exact behavior
df = relrank(df, 'mve_c', by=['tempFF48', 'yyyymm'], out='tempRK')

# CHECKPOINT 4: After relrank calculation
print("CHECKPOINT 4: Relrank calculation complete")
test_obs_1 = df[(df['permno'] == 10006) & (df['yyyymm'] == 200704)]
test_obs_2 = df[(df['permno'] == 11406) & (df['yyyymm'] == 200704)]
print(f"Test obs 10006 2007m4: {len(test_obs_1)} rows")
if len(test_obs_1) > 0:
    print(test_obs_1[['permno', 'time_avail_m', 'mve_c', 'tempRK']].to_string())
print(f"Test obs 11406 2007m4: {len(test_obs_2)} rows")
if len(test_obs_2) > 0:
    print(test_obs_2[['permno', 'time_avail_m', 'mve_c', 'tempRK']].to_string())
print(f"tempRK summary:")
print(df['tempRK'].describe())
print(f"Calculated tempRK ranks for {df['tempRK'].notna().sum()} observations")

# Stata: preserve
df_original = df.copy()

# CHECKPOINT 5: Before filtering for large companies
print(f"CHECKPOINT 5: Before preserve, {len(df)} observations")
test_obs_1 = df[(df['permno'] == 10006) & (df['yyyymm'] == 200704)]
test_obs_2 = df[(df['permno'] == 11406) & (df['yyyymm'] == 200704)]
print(f"Test obs 10006 2007m4: {len(test_obs_1)} rows")
if len(test_obs_1) > 0:
    print(test_obs_1[['permno', 'time_avail_m', 'tempRK']].to_string())
print(f"Test obs 11406 2007m4: {len(test_obs_2)} rows")
if len(test_obs_2) > 0:
    print(test_obs_2[['permno', 'time_avail_m', 'tempRK']].to_string())

# Stata: keep if tempRK >=.7 & !mi(tempRK)
df_big = df[(df['tempRK'] >= 0.7) & df['tempRK'].notna()].copy()

# CHECKPOINT 6: After filtering for large companies
print(f"CHECKPOINT 6: Large companies (tempRK >= 0.7): {len(df_big)} observations")
test_obs_1 = df_big[(df_big['permno'] == 10006) & (df_big['yyyymm'] == 200704)]
test_obs_2 = df_big[(df_big['permno'] == 11406) & (df_big['yyyymm'] == 200704)]
print(f"Test obs 10006 2007m4: {len(test_obs_1)} rows")
if len(test_obs_1) > 0:
    print(test_obs_1[['permno', 'time_avail_m', 'tempRK', 'ret']].to_string())
print(f"Test obs 11406 2007m4: {len(test_obs_2)} rows")
if len(test_obs_2) > 0:
    print(test_obs_2[['permno', 'time_avail_m', 'tempRK', 'ret']].to_string())

# Stata: gcollapse (mean) ret, by(tempFF48 time_avail_m)
# Calculate mean returns by industry-month for large companies only
industry_returns = df_big.groupby(['tempFF48', 'yyyymm'])['ret'].mean().reset_index()
industry_returns = industry_returns.rename(columns={'ret': 'IndRetBig'})

# CHECKPOINT 7: After industry return calculation
print(f"CHECKPOINT 7: Industry returns calculated for {len(industry_returns)} industry-month groups")
test_returns = industry_returns[industry_returns['yyyymm'] == 200704]
print(f"Industry returns for 2007m4:")
if len(test_returns) > 0:
    print(test_returns[['tempFF48', 'yyyymm', 'IndRetBig']].to_string())

# Stata: save "$pathtemp/temp",replace
# Stata: restore
df = df_original.copy()
# Ensure yyyymm column exists for merge (df_original was created after yyyymm conversion)
# No need to recreate yyyymm since df_original already contains it

# CHECKPOINT 8: After restore
print(f"CHECKPOINT 8: After restore, {len(df)} observations")
test_obs_1 = df[(df['permno'] == 10006) & (df['yyyymm'] == 200704)]
test_obs_2 = df[(df['permno'] == 11406) & (df['yyyymm'] == 200704)]
print(f"Test obs 10006 2007m4: {len(test_obs_1)} rows")
if len(test_obs_1) > 0:
    print(test_obs_1[['permno', 'time_avail_m', 'tempRK']].to_string())
print(f"Test obs 11406 2007m4: {len(test_obs_2)} rows")
if len(test_obs_2) > 0:
    print(test_obs_2[['permno', 'time_avail_m', 'tempRK']].to_string())

# Stata: merge m:1 tempFF48 time_avail_m using "$pathtemp/temp", nogenerate
df = df.merge(industry_returns, on=['tempFF48', 'yyyymm'], how='left')

# CHECKPOINT 9: After merge with industry returns
print(f"CHECKPOINT 9: After merge, {len(df)} observations")
test_obs_1 = df[(df['permno'] == 10006) & (df['yyyymm'] == 200704)]
test_obs_2 = df[(df['permno'] == 11406) & (df['yyyymm'] == 200704)]
print(f"Test obs 10006 2007m4: {len(test_obs_1)} rows")
if len(test_obs_1) > 0:
    print(test_obs_1[['permno', 'time_avail_m', 'tempRK', 'IndRetBig']].to_string())
print(f"Test obs 11406 2007m4: {len(test_obs_2)} rows")
if len(test_obs_2) > 0:
    print(test_obs_2[['permno', 'time_avail_m', 'tempRK', 'IndRetBig']].to_string())
print(f"Non-missing IndRetBig after merge: {df['IndRetBig'].notna().sum()}")

# Stata: replace IndRetBig = . if tempRK >= .7
# Set IndRetBig to missing for companies that are themselves large (>= 70th percentile)
df.loc[df['tempRK'] >= 0.7, 'IndRetBig'] = np.nan

# CHECKPOINT 10: Final result
print("CHECKPOINT 10: Final dataset")
test_obs_1 = df[(df['permno'] == 10006) & (df['yyyymm'] == 200704)]
test_obs_2 = df[(df['permno'] == 11406) & (df['yyyymm'] == 200704)]
print(f"Test obs 10006 2007m4: {len(test_obs_1)} rows")
if len(test_obs_1) > 0:
    print(test_obs_1[['permno', 'time_avail_m', 'tempRK', 'IndRetBig']].to_string())
print(f"Test obs 11406 2007m4: {len(test_obs_2)} rows")
if len(test_obs_2) > 0:
    print(test_obs_2[['permno', 'time_avail_m', 'tempRK', 'IndRetBig']].to_string())
final_non_missing = df['IndRetBig'].notna().sum()
print(f"Total observations: {len(df)}, Non-missing IndRetBig: {final_non_missing}")
print(f"Set IndRetBig to missing for {(df['tempRK'] >= 0.7).sum()} large companies")

# Stata: label var IndRetBig "Industry return big companies"
# (No need to implement label in Python)

# SAVE
# Stata: do "$pathCode/savepredictor" IndRetBig
save_predictor(df, 'IndRetBig')

print("IndRetBig predictor saved successfully")