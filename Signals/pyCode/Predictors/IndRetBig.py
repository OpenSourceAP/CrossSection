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

print(f"Loaded {len(df)} observations from SignalMasterTable")

# SIGNAL CONSTRUCTION

# Stata: sicff sicCRSP, generate(tempFF48) industry(48)
# Use unified sicff module for Fama-French 48 industry classification
df['tempFF48'] = sicff(df['sicCRSP'], industry=48)

# Stata: drop if mi(tempFF48)
df = df.dropna(subset=['tempFF48'])

print(f"After dropping missing FF48 industries: {len(df)} observations")

# Stata: bys tempFF48 time_avail_m: relrank mve_c, gen(tempRK) ref(mve_c)
# Use utils/relrank to match Stata's exact behavior
df = relrank(df, 'mve_c', by=['tempFF48', 'yyyymm'], out='tempRK')

print(f"Calculated tempRK ranks for {df['tempRK'].notna().sum()} observations")

# Stata: preserve
df_original = df.copy()

# Stata: keep if tempRK >=.7 & !mi(tempRK)
df_big = df[(df['tempRK'] >= 0.7) & df['tempRK'].notna()].copy()

print(f"Large companies (tempRK >= 0.7): {len(df_big)} observations")

# Stata: gcollapse (mean) ret, by(tempFF48 time_avail_m)
# Calculate mean returns by industry-month for large companies only
industry_returns = df_big.groupby(['tempFF48', 'yyyymm'])['ret'].mean().reset_index()
industry_returns = industry_returns.rename(columns={'ret': 'IndRetBig'})

print(f"Calculated industry returns for {len(industry_returns)} industry-month groups")

# Stata: save "$pathtemp/temp",replace
# Stata: restore
df = df_original.copy()
# Ensure yyyymm column exists for merge (df_original was created after yyyymm conversion)
# No need to recreate yyyymm since df_original already contains it

# Stata: merge m:1 tempFF48 time_avail_m using "$pathtemp/temp", nogenerate
df = df.merge(industry_returns, on=['tempFF48', 'yyyymm'], how='left')

# Stata: replace IndRetBig = . if tempRK >= .7
# Set IndRetBig to missing for companies that are themselves large (>= 70th percentile)
df.loc[df['tempRK'] >= 0.7, 'IndRetBig'] = np.nan

print(f"Set IndRetBig to missing for {(df['tempRK'] >= 0.7).sum()} large companies")

# Stata: label var IndRetBig "Industry return big companies"
# (No need to implement label in Python)

print(f"Final dataset has {len(df)} observations with {df['IndRetBig'].notna().sum()} non-missing IndRetBig values")

# SAVE
# Stata: do "$pathCode/savepredictor" IndRetBig
save_predictor(df, 'IndRetBig')

print("IndRetBig predictor saved successfully")