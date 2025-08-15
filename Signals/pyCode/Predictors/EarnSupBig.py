# ABOUTME: Creates Industry Earnings Surprise Big Companies (EarnSupBig) predictor
# ABOUTME: Run from pyCode/ directory: python3 Predictors/EarnSupBig.py

# EarnSupBig predictor translation from Code/Predictors/EarnSupBig.do
# Line-by-line translation preserving exact order and logic
# Creates earnings surprise then calculates industry averages for big companies

import pandas as pd
import numpy as np
import sys
sys.path.append('.')
from utils.savepredictor import save_predictor
from utils.relrank import relrank
from utils.sicff import sicff

print("Creating EarnSupBig predictor...")

# --------------
# make earnings surprise (copied from EarningsSurprise.do)
# DATA LOAD
# Stata: use permno gvkey time_avail_m using "$pathDataIntermediate/SignalMasterTable", clear
df = pd.read_parquet('../pyData/Intermediate/SignalMasterTable.parquet')
df = df[['permno', 'gvkey', 'time_avail_m']].copy()

# CHECKPOINT 1: Initial data load
print(f"CHECKPOINT 1: Loaded {len(df)} observations from SignalMasterTable")
april_2007 = pd.Timestamp('2007-04-01')
debug_permnos = [10006, 11406, 12473, 10051]
april_2007_data = df[df['time_avail_m'] == april_2007]
if len(april_2007_data) > 0:
    debug_data = april_2007_data[april_2007_data['permno'].isin(debug_permnos)]
    if len(debug_data) > 0:
        print("CHECKPOINT 1 - April 2007 debug permnos:")
        print(debug_data[['permno', 'gvkey', 'time_avail_m']].to_string())

# Stata: keep if !mi(gvkey)
df = df.dropna(subset=['gvkey'])

# CHECKPOINT 2: After removing missing gvkey
print(f"CHECKPOINT 2: After dropping missing gvkey: {len(df)} observations")
april_2007_data = df[df['time_avail_m'] == april_2007]
if len(april_2007_data) > 0:
    debug_data = april_2007_data[april_2007_data['permno'].isin(debug_permnos)]
    if len(debug_data) > 0:
        print("CHECKPOINT 2 - April 2007 debug permnos:")
        print(debug_data[['permno', 'gvkey', 'time_avail_m']].to_string())

# Stata: merge 1:1 gvkey time_avail_m using "$pathDataIntermediate/m_QCompustat", keepusing(epspxq) nogenerate keep(match)
m_qcompustat = pd.read_parquet('../pyData/Intermediate/m_QCompustat.parquet')
m_qcompustat = m_qcompustat[['gvkey', 'time_avail_m', 'epspxq']].copy()

df = df.merge(m_qcompustat, on=['gvkey', 'time_avail_m'], how='inner')

# CHECKPOINT 3: After merge with m_QCompustat
print(f"CHECKPOINT 3: After merge with m_QCompustat: {len(df)} observations")
april_2007_data = df[df['time_avail_m'] == april_2007]
if len(april_2007_data) > 0:
    debug_data = april_2007_data[april_2007_data['permno'].isin(debug_permnos)]
    if len(debug_data) > 0:
        print("CHECKPOINT 3 - April 2007 debug permnos:")
        print(debug_data[['permno', 'gvkey', 'time_avail_m', 'epspxq']].to_string())

# SIGNAL CONSTRUCTION
# Stata: xtset permno time_avail_m
df = df.sort_values(['permno', 'time_avail_m'])

# Stata: gen GrTemp = (epspxq - l12.epspxq)
df['GrTemp'] = df.groupby('permno')['epspxq'].transform(lambda x: x - x.shift(12))

# CHECKPOINT 4: After calculating GrTemp (12-month lag)
print(f"CHECKPOINT 4: GrTemp calculated for {df['GrTemp'].notna().sum()} observations")
april_2007_data = df[df['time_avail_m'] == april_2007]
if len(april_2007_data) > 0:
    debug_data = april_2007_data[april_2007_data['permno'].isin(debug_permnos)]
    if len(debug_data) > 0:
        print("CHECKPOINT 4 - April 2007 debug permnos:")
        print(debug_data[['permno', 'time_avail_m', 'epspxq', 'GrTemp']].to_string())

# Stata: foreach n of numlist 3(3)24 { gen temp`n' = l`n'.GrTemp }
for n in range(3, 25, 3):  # 3, 6, 9, 12, 15, 18, 21, 24
    df[f'temp{n}'] = df.groupby('permno')['GrTemp'].transform(lambda x: x.shift(n))

# Stata: egen Drift = rowmean(temp*)
temp_cols = [f'temp{n}' for n in range(3, 25, 3)]
df['Drift'] = df[temp_cols].mean(axis=1)

# Stata: gen EarningsSurprise = epspxq - l12.epspxq - Drift
df['EarningsSurprise'] = df.groupby('permno')['epspxq'].transform(lambda x: x - x.shift(12)) - df['Drift']

# CHECKPOINT 5: After calculating EarningsSurprise
print(f"CHECKPOINT 5: EarningsSurprise calculated for {df['EarningsSurprise'].notna().sum()} observations")
april_2007_data = df[df['time_avail_m'] == april_2007]
if len(april_2007_data) > 0:
    debug_data = april_2007_data[april_2007_data['permno'].isin(debug_permnos)]
    if len(debug_data) > 0:
        print("CHECKPOINT 5 - April 2007 debug permnos:")
        print(debug_data[['permno', 'time_avail_m', 'epspxq', 'Drift', 'EarningsSurprise']].to_string())

# Stata: cap drop temp*
df = df.drop(columns=temp_cols)

# Stata: foreach n of numlist 3(3)24 { gen temp`n' = l`n'.EarningsSurprise }
for n in range(3, 25, 3):  # 3, 6, 9, 12, 15, 18, 21, 24
    df[f'temp{n}'] = df.groupby('permno')['EarningsSurprise'].transform(lambda x: x.shift(n))

# Stata: egen SD = rowsd(temp*)
temp_cols = [f'temp{n}' for n in range(3, 25, 3)]
df['SD'] = df[temp_cols].std(axis=1)

# Stata: replace EarningsSurprise = EarningsSurprise/SD
# Handle division by zero and very small SD values to prevent astronomical results
MIN_SD_THRESHOLD = 1e-8
df['EarningsSurprise'] = np.where(
    (df['SD'] == 0) | df['SD'].isna() | (abs(df['SD']) < MIN_SD_THRESHOLD), 
    np.nan, 
    df['EarningsSurprise'] / df['SD']
)

# CHECKPOINT 6: After standardizing EarningsSurprise
print(f"CHECKPOINT 6: Standardized EarningsSurprise for {df['EarningsSurprise'].notna().sum()} observations")
april_2007_data = df[df['time_avail_m'] == april_2007]
if len(april_2007_data) > 0:
    debug_data = april_2007_data[april_2007_data['permno'].isin(debug_permnos)]
    if len(debug_data) > 0:
        print("CHECKPOINT 6 - April 2007 debug permnos:")
        print(debug_data[['permno', 'time_avail_m', 'SD', 'EarningsSurprise']].to_string())

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

# CHECKPOINT 7: Second data load for EarnSupBig
print(f"CHECKPOINT 7: Loaded {len(df)} observations from SignalMasterTable for EarnSupBig")
april_2007_data = df[df['time_avail_m'] == april_2007]
if len(april_2007_data) > 0:
    debug_data = april_2007_data[april_2007_data['permno'].isin(debug_permnos)]
    if len(debug_data) > 0:
        print("CHECKPOINT 7 - April 2007 debug permnos:")
        print(debug_data[['permno', 'time_avail_m', 'mve_c', 'sicCRSP']].to_string())

# Stata: merge 1:1 permno time_avail_m using "$pathtemp/temp", keep(master match) nogenerate
df = df.merge(temp_earnings, on=['permno', 'time_avail_m'], how='left')

# CHECKPOINT 8: After merge with earnings surprise data
print(f"CHECKPOINT 8: After merge with earnings data: {len(df)} observations")
print(f"CHECKPOINT 8: With non-missing EarningsSurprise: {df['EarningsSurprise'].notna().sum()} observations")
april_2007_data = df[df['time_avail_m'] == april_2007]
if len(april_2007_data) > 0:
    debug_data = april_2007_data[april_2007_data['permno'].isin(debug_permnos)]
    if len(debug_data) > 0:
        print("CHECKPOINT 8 - April 2007 debug permnos:")
        print(debug_data[['permno', 'time_avail_m', 'mve_c', 'sicCRSP', 'EarningsSurprise']].to_string())

# SIGNAL CONSTRUCTION
# Stata: sicff sicCRSP, generate(tempFF48) industry(48)
# Use unified sicff module for Fama-French 48 industry classification
df['tempFF48'] = sicff(df['sicCRSP'], industry=48)

# CHECKPOINT 9: After FF48 industry classification
print(f"CHECKPOINT 9: FF48 industries assigned to {df['tempFF48'].notna().sum()} observations")
april_2007_data = df[df['time_avail_m'] == april_2007]
if len(april_2007_data) > 0:
    debug_data = april_2007_data[april_2007_data['permno'].isin(debug_permnos)]
    if len(debug_data) > 0:
        print("CHECKPOINT 9 - April 2007 debug permnos:")
        print(debug_data[['permno', 'time_avail_m', 'sicCRSP', 'tempFF48']].to_string())

# Stata: drop if mi(tempFF48)
df = df.dropna(subset=['tempFF48'])

# CHECKPOINT 10: After dropping missing FF48 industries
print(f"CHECKPOINT 10: After dropping missing FF48: {len(df)} observations")
april_2007_data = df[df['time_avail_m'] == april_2007]
if len(april_2007_data) > 0:
    debug_data = april_2007_data[april_2007_data['permno'].isin(debug_permnos)]
    if len(debug_data) > 0:
        print("CHECKPOINT 10 - April 2007 debug permnos:")
        print(debug_data[['permno', 'time_avail_m', 'tempFF48', 'mve_c']].to_string())

# Stata: bys tempFF48 time_avail_m: relrank mve_c, gen(tempRK) ref(mve_c)
# Use the relrank utility function
df = relrank(df, "mve_c", by=["tempFF48", "time_avail_m"], out="tempRK")

# CHECKPOINT 11: After calculating relrank
print(f"CHECKPOINT 11: Relrank calculated for {df['tempRK'].notna().sum()} observations")
april_2007_data = df[df['time_avail_m'] == april_2007]
if len(april_2007_data) > 0:
    debug_data = april_2007_data[april_2007_data['permno'].isin(debug_permnos)]
    if len(debug_data) > 0:
        print("CHECKPOINT 11 - April 2007 debug permnos:")
        print(debug_data[['permno', 'time_avail_m', 'tempFF48', 'mve_c', 'tempRK']].to_string())

# Stata: preserve
df_original = df.copy()

# Stata: keep if tempRK >=.7 & !mi(tempRK)
df_big = df[(df['tempRK'] >= 0.7) & df['tempRK'].notna()].copy()

# CHECKPOINT 12: Large companies only (tempRK >= 0.7)
print(f"CHECKPOINT 12: Large companies (tempRK >= 0.7): {len(df_big)} observations")
april_2007_data = df_big[df_big['time_avail_m'] == april_2007]
if len(april_2007_data) > 0:
    debug_data = april_2007_data[april_2007_data['permno'].isin(debug_permnos)]
    if len(debug_data) > 0:
        print("CHECKPOINT 12 - April 2007 debug permnos:")
        print(debug_data[['permno', 'time_avail_m', 'tempFF48', 'tempRK', 'EarningsSurprise']].to_string())

# Stata: gcollapse (mean) EarningsSurprise, by(tempFF48 time_avail_m)
# Calculate mean EarningsSurprise by industry-month for large companies only
industry_earnings = df_big.groupby(['tempFF48', 'time_avail_m'])['EarningsSurprise'].mean().reset_index()
industry_earnings = industry_earnings.rename(columns={'EarningsSurprise': 'EarnSupBig'})

# CHECKPOINT 13: Industry-month averages for large companies
print(f"CHECKPOINT 13: Industry-month groups with EarnSupBig: {len(industry_earnings)} groups")
april_2007_data = industry_earnings[industry_earnings['time_avail_m'] == april_2007]
if len(april_2007_data) > 0:
    print("CHECKPOINT 13 - April 2007 industry averages:")
    print(april_2007_data[['tempFF48', 'time_avail_m', 'EarnSupBig']].to_string())

# Stata: save "$pathtemp/temp",replace
# Stata: restore
df = df_original.copy()

# Stata: merge m:1 tempFF48 time_avail_m using "$pathtemp/temp", nogenerate
df = df.merge(industry_earnings, on=['tempFF48', 'time_avail_m'], how='left')

# CHECKPOINT 14: After merging industry averages back
print(f"CHECKPOINT 14: After merging industry averages: {len(df)} observations")
print(f"CHECKPOINT 14: With non-missing EarnSupBig: {df['EarnSupBig'].notna().sum()} observations")
april_2007_data = df[df['time_avail_m'] == april_2007]
if len(april_2007_data) > 0:
    debug_data = april_2007_data[april_2007_data['permno'].isin(debug_permnos)]
    if len(debug_data) > 0:
        print("CHECKPOINT 14 - April 2007 debug permnos:")
        print(debug_data[['permno', 'time_avail_m', 'tempFF48', 'tempRK', 'EarnSupBig']].to_string())

# Stata: replace EarnSupBig = . if tempRK >= .7
# Set EarnSupBig to missing for companies that are themselves large (>= 70th percentile)
df.loc[df['tempRK'] >= 0.7, 'EarnSupBig'] = np.nan

# CHECKPOINT 15: Final result after setting large companies to missing
print(f"CHECKPOINT 15: Final EarnSupBig (excluding large companies): {df['EarnSupBig'].notna().sum()} observations")
april_2007_data = df[df['time_avail_m'] == april_2007]
if len(april_2007_data) > 0:
    debug_data = april_2007_data[april_2007_data['permno'].isin(debug_permnos)]
    if len(debug_data) > 0:
        print("CHECKPOINT 15 - April 2007 debug permnos:")
        print(debug_data[['permno', 'time_avail_m', 'tempFF48', 'tempRK', 'EarnSupBig']].to_string())

# Stata: label var EarnSupBig "Industry Earnings surprise big companies"
# (No need to implement label in Python)

print(f"Final dataset has {len(df)} observations with {df['EarnSupBig'].notna().sum()} non-missing EarnSupBig values")

# SAVE
# Stata: do "$pathCode/savepredictor" EarnSupBig
save_predictor(df, 'EarnSupBig')

print("EarnSupBig predictor saved successfully")