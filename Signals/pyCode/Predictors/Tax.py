# ABOUTME: Tax_fixed.py - calculates taxable income to income ratio predictor with correct missing value handling
# ABOUTME: Tax rate adjusted measure using historical corporate tax rates by year

"""
Tax predictor calculation

Usage:
    cd pyCode/
    source .venv/bin/activate
    python3 Predictors/Tax_fixed.py

Inputs:
    - ../pyData/Intermediate/m_aCompustat.parquet (permno, time_avail_m, txfo, txfed, ib, txt, txdi)

Outputs:
    - ../pyData/Predictors/Tax.csv (permno, yyyymm, Tax)
"""

import pandas as pd
import numpy as np

# DATA LOAD
df = pd.read_parquet("../pyData/Intermediate/m_aCompustat.parquet", 
                     columns=['permno', 'time_avail_m', 'txfo', 'txfed', 'ib', 'txt', 'txdi'])

# Remove duplicates by permno and time_avail_m (keep first)
df = df.groupby(['permno', 'time_avail_m']).first().reset_index()

# SIGNAL CONSTRUCTION
# Extract year from time_avail_m
df['year'] = df['time_avail_m'].dt.year

# Define highest tax rate by year
df['tr'] = 0.48  # Default rate
df.loc[(df['year'] >= 1979) & (df['year'] <= 1986), 'tr'] = 0.46
df.loc[df['year'] == 1987, 'tr'] = 0.4
df.loc[(df['year'] >= 1988) & (df['year'] <= 1992), 'tr'] = 0.34
df.loc[df['year'] >= 1993, 'tr'] = 0.35


# Step 1: gen Tax = ((txfo+txfed)/tr)/ib
df['Tax'] = ((df['txfo'] + df['txfed']) / df['tr']) / df['ib']

# Step 2: replace Tax = ((txt-txdi)/tr)/ib if txfo ==. | txfed ==.
condition_missing = df['txfo'].isna() | df['txfed'].isna()
df.loc[condition_missing, 'Tax'] = ((df['txt'] - df['txdi']) / df['tr']) / df['ib']

# Step 3: replace Tax = 1 if (txfo + txfed > 0 | txt > txdi) & ib <=0
# Handle the division by zero case first (ib = 0)
# When ib = 0, any tax activity should result in Tax = 1
div_by_zero = (df['ib'] == 0) & (
    (df['txfo'].notna() & (df['txfo'] != 0)) |
    (df['txfed'].notna() & (df['txfed'] != 0)) |
    (df['txt'].notna() & (df['txt'] != 0)) |
    (df['txdi'].notna() & (df['txdi'] != 0))
)
df.loc[div_by_zero, 'Tax'] = 1.0

# Handle NaN values after steps 1-2 when ib <= 0
cond_step3_simple = df['Tax'].isna() & (df['ib'] <= 0).fillna(False)
df.loc[cond_step3_simple, 'Tax'] = 1.0

# Handle standard Stata condition: (txfo + txfed > 0 | txt > txdi) & ib <=0
# When txfed is missing but txfo > 0, Stata treats this as txfo + txfed > 0
cond_txfo_txfed_fixed = (
    (df['txfed'].isna() & (df['txfo'] > 0).fillna(False)) |
    (~df['txfed'].isna() & (df['txfo'] + df['txfed'] > 0).fillna(False))
)
cond_txt_txdi = (df['txt'] > df['txdi']).fillna(False)

# Additional condition: when both txfo and txfed are missing but there's tax activity and ib <= 0
cond_both_missing = (df['txfo'].isna() & df['txfed'].isna() & 
                     ((df['txt'].notna() & (df['txt'] != 0)) | (df['txdi'].notna() & (df['txdi'] != 0))) &
                     (df['ib'] <= 0).fillna(False))

cond_standard = (cond_txfo_txfed_fixed | cond_txt_txdi | cond_both_missing) & (df['ib'] <= 0).fillna(False)
df.loc[cond_standard, 'Tax'] = 1.0


# Convert time_avail_m to yyyymm
df['yyyymm'] = df['time_avail_m'].dt.year * 100 + df['time_avail_m'].dt.month

# Keep only finite Tax values (no NaN, no infinite)
df = df[df['Tax'].notna() & np.isfinite(df['Tax'])].copy()

# Keep required columns and order
df = df[['permno', 'yyyymm', 'Tax']].copy()

# SAVE
df.to_csv("../pyData/Predictors/Tax.csv", index=False)
print(f"Tax: Saved {len(df):,} observations")