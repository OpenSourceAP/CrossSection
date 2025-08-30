# ABOUTME: Creates Industry Earnings Surprise Big Companies (EarnSupBig) predictor
# ABOUTME: Run from pyCode/ directory: python3 Predictors/EarnSupBig.py

# EarnSupBig predictor translation from Code/Predictors/EarnSupBig.do
# Line-by-line translation preserving exact order and logic
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
# make earnings surprise (copied from EarningsSurprise.do)
# DATA LOAD
# Stata: use permno gvkey time_avail_m using "$pathDataIntermediate/SignalMasterTable", clear
df = pd.read_parquet('../pyData/Intermediate/SignalMasterTable.parquet')
df = df[['permno', 'gvkey', 'time_avail_m']].copy()


# Stata: keep if !mi(gvkey)
df = df.dropna(subset=['gvkey'])


# Stata: merge 1:1 gvkey time_avail_m using "$pathDataIntermediate/m_QCompustat", keepusing(epspxq) nogenerate keep(match)
m_qcompustat = pd.read_parquet('../pyData/Intermediate/m_QCompustat.parquet')
m_qcompustat = m_qcompustat[['gvkey', 'time_avail_m', 'epspxq']].copy()

df = df.merge(m_qcompustat, on=['gvkey', 'time_avail_m'], how='inner')


# SIGNAL CONSTRUCTION
# Stata: xtset permno time_avail_m
df = df.sort_values(['permno', 'time_avail_m'])

# Stata: gen GrTemp = (epspxq - l12.epspxq)
df['GrTemp'] = df.groupby('permno')['epspxq'].transform(lambda x: x - x.shift(12))


# Stata: foreach n of numlist 3(3)24 { gen temp`n' = l`n'.GrTemp }
for n in range(3, 25, 3):  # 3, 6, 9, 12, 15, 18, 21, 24
    df[f'temp{n}'] = df.groupby('permno')['GrTemp'].transform(lambda x: x.shift(n))

# Stata: egen Drift = rowmean(temp*)
temp_cols = [f'temp{n}' for n in range(3, 25, 3)]
df['Drift'] = df[temp_cols].mean(axis=1)


# Stata: gen EarningsSurprise = epspxq - l12.epspxq - Drift
df['EarningsSurprise'] = df.groupby('permno')['epspxq'].transform(lambda x: x - x.shift(12)) - df['Drift']


# Stata: cap drop temp*
df = df.drop(columns=temp_cols)

# Stata: foreach n of numlist 3(3)24 { gen temp`n' = l`n'.EarningsSurprise }
for n in range(3, 25, 3):  # 3, 6, 9, 12, 15, 18, 21, 24
    df[f'temp{n}'] = df.groupby('permno')['EarningsSurprise'].transform(lambda x: x.shift(n))

# Stata: egen SD = rowsd(temp*)
temp_cols = [f'temp{n}' for n in range(3, 25, 3)]
df['SD'] = df[temp_cols].std(axis=1)


# Store original EarningsSurprise for comparison
df['EarningsSurprise_raw'] = df['EarningsSurprise'].copy()

# Stata: replace EarningsSurprise = EarningsSurprise/SD
# Handle division by zero and very small SD values to prevent astronomical results
MIN_SD_THRESHOLD = 1e-8
df['EarningsSurprise'] = np.where(
    (df['SD'] == 0) | df['SD'].isna() | (abs(df['SD']) < MIN_SD_THRESHOLD), 
    np.nan, 
    df['EarningsSurprise'] / df['SD']
)


# Stata: cap drop temp*
df = df.drop(columns=temp_cols)

# Stata: save "$pathtemp/temp", replace
temp_earnings = df[['permno', 'time_avail_m', 'EarningsSurprise']].copy()

# --------------
# actually make EarnSupBig
# DATA LOAD
# Stata: use permno time_avail_m mve_c sicCRSP using "$pathDataIntermediate/SignalMasterTable", clear
df = pd.read_parquet('../pyData/Intermediate/SignalMasterTable.parquet')
df = df[['permno', 'time_avail_m', 'mve_c', 'sicCRSP']].copy()


# Stata: merge 1:1 permno time_avail_m using "$pathtemp/temp", keep(master match) nogenerate
df = df.merge(temp_earnings, on=['permno', 'time_avail_m'], how='left')


# SIGNAL CONSTRUCTION
# Stata: sicff sicCRSP, generate(tempFF48) industry(48)
# Use unified sicff module for Fama-French 48 industry classification
df['tempFF48'] = sicff(df['sicCRSP'], industry=48)


# Stata: drop if mi(tempFF48)
df = df.dropna(subset=['tempFF48'])


# Stata: bys tempFF48 time_avail_m: relrank mve_c, gen(tempRK) ref(mve_c)
# Use the relrank utility function
df = relrank(df, "mve_c", by=["tempFF48", "time_avail_m"], out="tempRK")


# Stata: preserve
df_original = df.copy()

# Stata: keep if tempRK >=.7 & !mi(tempRK)
df_big = df[(df['tempRK'] >= 0.7) & df['tempRK'].notna()].copy()


# Stata: gcollapse (mean) EarningsSurprise, by(tempFF48 time_avail_m)
# Calculate mean EarningsSurprise by industry-month for large companies only
industry_earnings = df_big.groupby(['tempFF48', 'time_avail_m'])['EarningsSurprise'].mean().reset_index()
industry_earnings = industry_earnings.rename(columns={'EarningsSurprise': 'EarnSupBig'})


# Stata: save "$pathtemp/temp",replace
# Stata: restore
df = df_original.copy()

# Stata: merge m:1 tempFF48 time_avail_m using "$pathtemp/temp", nogenerate
df = df.merge(industry_earnings, on=['tempFF48', 'time_avail_m'], how='left')


# Stata: replace EarnSupBig = . if tempRK >= .7
# Set EarnSupBig to missing for companies that are themselves large (>= 70th percentile)
df.loc[df['tempRK'] >= 0.7, 'EarnSupBig'] = np.nan


# Stata: label var EarnSupBig "Industry Earnings surprise big companies"
# (No need to implement label in Python)

print(f"Final dataset has {len(df)} observations with {df['EarnSupBig'].notna().sum()} non-missing EarnSupBig values")

# SAVE
# Stata: do "$pathCode/savepredictor" EarnSupBig
save_predictor(df, 'EarnSupBig')

print("EarnSupBig predictor saved successfully")