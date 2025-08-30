# ABOUTME: Creates Industry Return Big Companies (IndRetBig) predictor by calculating industry returns for large companies
# ABOUTME: Run from pyCode/ directory: python3 Predictors/IndRetBig.py

# IndRetBig predictor translation from Code/Predictors/IndRetBig.do
# Line-by-line translation preserving exact order and logic

import pandas as pd
import numpy as np
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from utils.save_standardized import save_predictor
from utils.stata_replication import relrank
from utils.sicff import sicff

# DATA LOAD
# Stata: use permno time_avail_m ret mve_c sicCRSP using "$pathDataIntermediate/SignalMasterTable", clear
df = pd.read_parquet('../pyData/Intermediate/SignalMasterTable.parquet')
df = df[['permno', 'time_avail_m', 'ret', 'mve_c', 'sicCRSP']].copy()

# Convert datetime time_avail_m to integer yyyymm to match Stata format
df['yyyymm'] = df['time_avail_m'].dt.year * 100 + df['time_avail_m'].dt.month


# SIGNAL CONSTRUCTION

# Stata: sicff sicCRSP, generate(tempFF48) industry(48)
# Use unified sicff module for Fama-French 48 industry classification
df['tempFF48'] = sicff(df['sicCRSP'], industry=48)


# Stata: drop if mi(tempFF48)
df = df.dropna(subset=['tempFF48'])


# Stata: bys tempFF48 time_avail_m: relrank mve_c, gen(tempRK) ref(mve_c)
# Use utils/relrank to match Stata's exact behavior
df = relrank(df, 'mve_c', by=['tempFF48', 'yyyymm'], out='tempRK')


# Stata: preserve
df_original = df.copy()


# Stata: keep if tempRK >=.7 & !mi(tempRK)
# Fix: Use strict inequality to match Stata's exact behavior for companies at tempRK = 0.7
df_big = df[(df['tempRK'] > 0.7) & df['tempRK'].notna()].copy()


# Stata: gcollapse (mean) ret, by(tempFF48 time_avail_m)
# Calculate mean returns by industry-month for large companies only
# Use time_avail_m to match Stata exactly
industry_returns = df_big.groupby(['tempFF48', 'time_avail_m'])['ret'].mean().reset_index()
industry_returns = industry_returns.rename(columns={'ret': 'IndRetBig'})


# Stata: save "$pathtemp/temp",replace
# Stata: restore
df = df_original.copy()
# Ensure yyyymm column exists for merge (df_original was created after yyyymm conversion)
# No need to recreate yyyymm since df_original already contains it


# Stata: merge m:1 tempFF48 time_avail_m using "$pathtemp/temp", nogenerate
df = df.merge(industry_returns, on=['tempFF48', 'time_avail_m'], how='left')


# Stata: replace IndRetBig = . if tempRK >= .7
# Set IndRetBig to missing for companies that are themselves large (>= 70th percentile)
df.loc[df['tempRK'] >= 0.7, 'IndRetBig'] = np.nan


# Stata: label var IndRetBig "Industry return big companies"
# (No need to implement label in Python)

# SAVE
# Stata: do "$pathCode/savepredictor" IndRetBig
save_predictor(df, 'IndRetBig')

print("IndRetBig predictor saved successfully")