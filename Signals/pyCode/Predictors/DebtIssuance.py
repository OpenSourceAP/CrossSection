# ABOUTME: Debt Issuance following Spiess and Affleck-Graves 1999, Table 4A EW
# ABOUTME: calculates debt issuance predictor, equal to 1 if debt issuance (dltis) > 0

"""
DebtIssuance.py

Usage:
    cd pyCode/
    source .venv/bin/activate
    python3 Predictors/DebtIssuance.py

Inputs:
    - ../pyData/Intermediate/m_aCompustat.parquet
    - ../pyData/Intermediate/SignalMasterTable.parquet

Outputs:
    - ../pyData/Predictors/DebtIssuance.csv (columns: permno, yyyymm, DebtIssuance)
"""

import pandas as pd
import numpy as np
from pathlib import Path

print("Starting DebtIssuance predictor...")

# DATA LOAD
# Load Compustat data with required fields
print("Loading m_aCompustat data...")
df = pd.read_parquet('../pyData/Intermediate/m_aCompustat.parquet', 
                     columns=['permno', 'time_avail_m', 'ceq', 'dltis'])
print(f"Loaded {len(df):,} Compustat observations")

# Merge with SignalMasterTable to get market value and share code data
print("Loading SignalMasterTable...")
smt = pd.read_parquet('../pyData/Intermediate/SignalMasterTable.parquet', 
                      columns=['permno', 'time_avail_m', 'mve_c', 'shrcd'])
print(f"Loaded {len(smt):,} SignalMasterTable observations")

print("Merging data...")
# Keep only matched observations
df = pd.merge(df, smt, on=['permno', 'time_avail_m'], how='inner')
print(f"After merging: {len(df):,} observations")

print("Constructing DebtIssuance signal...")

# SIGNAL CONSTRUCTION
# Calculate book-to-market ratio
df['BM'] = np.log(df['ceq'] / df['mve_c'])

# Create debt issuance indicator for positive debt issuances
df['DebtIssuance'] = ((df['dltis'] > 0) & df['dltis'].notna()).astype(int)

# Exclude observations with invalid share codes or missing book-to-market ratios
mask_exclude = (df['shrcd'] > 11) | df['BM'].isna()
df.loc[mask_exclude, 'DebtIssuance'] = np.nan

# Keep only non-missing values
result = df[['permno', 'time_avail_m', 'DebtIssuance']].copy()
result = result.dropna(subset=['DebtIssuance']).copy()

print(f"Generated DebtIssuance values for {len(result):,} observations")

# Convert time_avail_m to yyyymm
result['yyyymm'] = result['time_avail_m'].dt.year * 100 + result['time_avail_m'].dt.month

# Prepare final output
final_result = result[['permno', 'yyyymm', 'DebtIssuance']].copy()

# SAVE
print("Saving predictor...")
Path('../pyData/Predictors').mkdir(parents=True, exist_ok=True)
final_result.to_csv('../pyData/Predictors/DebtIssuance.csv', index=False)

print("saving DebtIssuance")
print(f"Saved {len(final_result)} rows to ../pyData/Predictors/DebtIssuance.csv")
print("DebtIssuance predictor completed successfully!")