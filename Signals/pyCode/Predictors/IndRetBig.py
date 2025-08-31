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
# Load required columns from SignalMasterTable
df = pd.read_parquet('../pyData/Intermediate/SignalMasterTable.parquet')
df = df[['permno', 'time_avail_m', 'ret', 'mve_c', 'sicCRSP']].copy()

# Convert datetime time_avail_m to integer yyyymm to match Stata format
df['yyyymm'] = df['time_avail_m'].dt.year * 100 + df['time_avail_m'].dt.month


# SIGNAL CONSTRUCTION

# Generate Fama-French 48 industry classification from SIC codes
df['tempFF48'] = sicff(df['sicCRSP'], industry=48)


# Drop observations with missing industry classification
df = df.dropna(subset=['tempFF48'])


# Calculate relative rank of market value within industry-month groups
df = relrank(df, 'mve_c', by=['tempFF48', 'yyyymm'], out='tempRK')


# Save original dataset before filtering
df_original = df.copy()


# Keep only large companies (market value rank > 70th percentile)
df_big = df[(df['tempRK'] > 0.7) & df['tempRK'].notna()].copy()


# Calculate mean returns by industry-month for large companies only
industry_returns = df_big.groupby(['tempFF48', 'time_avail_m'])['ret'].mean().reset_index()
industry_returns = industry_returns.rename(columns={'ret': 'IndRetBig'})


# Restore original dataset for merging
df = df_original.copy()


# Merge industry returns back to all companies
df = df.merge(industry_returns, on=['tempFF48', 'time_avail_m'], how='left')


# Set IndRetBig to missing for companies that are themselves large (>= 70th percentile)
df.loc[df['tempRK'] >= 0.7, 'IndRetBig'] = np.nan



# SAVE
save_predictor(df, 'IndRetBig')

print("IndRetBig predictor saved successfully")