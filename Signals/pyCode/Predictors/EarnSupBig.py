# ABOUTME: Creates Industry Earnings Surprise Big Companies (EarnSupBig) predictor
# ABOUTME: Run from pyCode/ directory: python3 Predictors/EarnSupBig.py

# Creates earnings surprise then calculates industry averages for big companies

import pandas as pd
import numpy as np
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from utils.save_standardized import save_predictor
from utils.stata_replication import relrank
from utils.sicff import sicff

print("Creating EarnSupBig predictor...")

# --------------
# Calculate earnings surprise
# DATA LOAD
# Load identifiers from master table
df = pd.read_parquet('../pyData/Intermediate/SignalMasterTable.parquet')
df = df[['permno', 'gvkey', 'time_avail_m']].copy()


# Filter to observations with valid gvkey identifiers
df = df.dropna(subset=['gvkey'])


# Merge with quarterly Compustat earnings data
m_qcompustat = pd.read_parquet('../pyData/Intermediate/m_QCompustat.parquet')
m_qcompustat = m_qcompustat[['gvkey', 'time_avail_m', 'epspxq']].copy()

df = df.merge(m_qcompustat, on=['gvkey', 'time_avail_m'], how='inner')


# SIGNAL CONSTRUCTION
# Sort data for time series operations
df = df.sort_values(['permno', 'time_avail_m'])

# Calculate quarterly earnings growth over 12-month period
df['GrTemp'] = df.groupby('permno')['epspxq'].transform(lambda x: x - x.shift(12))


# Create lagged earnings growth values for drift calculation
for n in range(3, 25, 3):  # 3, 6, 9, 12, 15, 18, 21, 24
    df[f'temp{n}'] = df.groupby('permno')['GrTemp'].transform(lambda x: x.shift(n))

# Calculate average earnings growth drift
temp_cols = [f'temp{n}' for n in range(3, 25, 3)]
df['Drift'] = df[temp_cols].mean(axis=1)


# Calculate earnings surprise as growth minus drift
df['EarningsSurprise'] = df.groupby('permno')['epspxq'].transform(lambda x: x - x.shift(12)) - df['Drift']


# Clean up temporary variables
df = df.drop(columns=temp_cols)

# Create lagged earnings surprise values for volatility calculation
for n in range(3, 25, 3):  # 3, 6, 9, 12, 15, 18, 21, 24
    df[f'temp{n}'] = df.groupby('permno')['EarningsSurprise'].transform(lambda x: x.shift(n))

# Calculate standard deviation of historical earnings surprises
temp_cols = [f'temp{n}' for n in range(3, 25, 3)]
df['SD'] = df[temp_cols].std(axis=1)


# Store original EarningsSurprise for comparison
df['EarningsSurprise_raw'] = df['EarningsSurprise'].copy()

# Standardize earnings surprise by dividing by historical volatility
MIN_SD_THRESHOLD = 1e-8
df['EarningsSurprise'] = np.where(
    (df['SD'] == 0) | df['SD'].isna() | (abs(df['SD']) < MIN_SD_THRESHOLD), 
    np.nan, 
    df['EarningsSurprise'] / df['SD']
)


# Clean up temporary variables
df = df.drop(columns=temp_cols)

# Store earnings surprise data for later use
temp_earnings = df[['permno', 'time_avail_m', 'EarningsSurprise']].copy()

# --------------
# Calculate industry earnings surprise for big companies
# DATA LOAD
# Load market value and industry data
df = pd.read_parquet('../pyData/Intermediate/SignalMasterTable.parquet')
df = df[['permno', 'time_avail_m', 'mve_c', 'sicCRSP']].copy()


# Merge with earnings surprise data
df = df.merge(temp_earnings, on=['permno', 'time_avail_m'], how='left')


# SIGNAL CONSTRUCTION
# Assign Fama-French 48 industry classification
df['tempFF48'] = sicff(df['sicCRSP'], industry=48)


# Filter to observations with valid industry classifications
df = df.dropna(subset=['tempFF48'])


# Calculate market value percentile ranks within industry-month groups
df = relrank(df, "mve_c", by=["tempFF48", "time_avail_m"], out="tempRK")


# Save copy of full dataset
df_original = df.copy()

# Filter to large companies (top 30% by market value within industry)
df_big = df[(df['tempRK'] >= 0.7) & df['tempRK'].notna()].copy()


# Calculate mean earnings surprise by industry-month for large companies only
industry_earnings = df_big.groupby(['tempFF48', 'time_avail_m'])['EarningsSurprise'].mean().reset_index()
industry_earnings = industry_earnings.rename(columns={'EarningsSurprise': 'EarnSupBig'})


# Restore full dataset and merge with industry earnings surprise
df = df_original.copy()
df = df.merge(industry_earnings, on=['tempFF48', 'time_avail_m'], how='left')


# Set EarnSupBig to missing for companies that are themselves large (>= 70th percentile)
df.loc[df['tempRK'] >= 0.7, 'EarnSupBig'] = np.nan


# Variable represents industry earnings surprise from big companies

print(f"Final dataset has {len(df)} observations with {df['EarnSupBig'].notna().sum()} non-missing EarnSupBig values")

# SAVE
save_predictor(df, 'EarnSupBig')

print("EarnSupBig predictor saved successfully")