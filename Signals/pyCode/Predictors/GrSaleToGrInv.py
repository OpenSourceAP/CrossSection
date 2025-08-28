# ABOUTME: GrSaleToGrInv.py - calculates GrSaleToGrInv predictor using sales growth over inventory growth
# ABOUTME: Direct line-by-line translation from Stata Code/Predictors/GrSaleToGrInv.do

"""
GrSaleToGrInv.py

Usage:
    cd pyCode/
    source .venv/bin/activate
    python3 Predictors/GrSaleToGrInv.py

Inputs:
    - m_aCompustat.parquet: Monthly Compustat data with columns [gvkey, permno, time_avail_m, sale, invt]

Outputs:
    - GrSaleToGrInv.csv: CSV file with columns [permno, yyyymm, GrSaleToGrInv]
    - Primary: ((sale- (.5*(l12.sale + l24.sale)))/(.5*(l12.sale + l24.sale))) - ((invt- (.5*(l12.invt + l24.invt)))/(.5*(l12.invt + l24.invt)))
    - Fallback: ((sale-l12.sale)/l12.sale)-((invt-l12.invt)/l12.invt) if primary is missing
"""

import pandas as pd
import numpy as np
from pathlib import Path
import sys
import os

# Add utils directory to path for imports
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from utils.save_standardized import save_predictor


print("Starting GrSaleToGrInv.py...")

# DATA LOAD
print("Loading m_aCompustat data...")

# Load m_aCompustat - equivalent to Stata: use gvkey permno time_avail_m sale invt using "$pathDataIntermediate/m_aCompustat", clear
m_aCompustat_path = Path("../pyData/Intermediate/m_aCompustat.parquet")
if not m_aCompustat_path.exists():
    raise FileNotFoundError(f"Required input file not found: {m_aCompustat_path}")

df = pd.read_parquet(m_aCompustat_path)

# Keep only the columns we need
required_cols = ['gvkey', 'permno', 'time_avail_m', 'sale', 'invt']
missing_cols = [col for col in required_cols if col not in df.columns]
if missing_cols:
    raise ValueError(f"Missing required columns in m_aCompustat: {missing_cols}")

df = df[required_cols].copy()

print(f"Loaded m_aCompustat: {df.shape[0]} rows, {df.shape[1]} columns")

# SIGNAL CONSTRUCTION

# bysort permno time_avail_m: keep if _n == 1  // deletes a few observations
print("Removing duplicate permno-time_avail_m observations...")
df = df.drop_duplicates(['permno', 'time_avail_m'], keep='first')

# xtset permno time_avail_m
print("Setting up panel data (sorting by permno, time_avail_m)...")
df = df.sort_values(['permno', 'time_avail_m'])

# Create 12 and 24-month lags for both sale and invt
print("Calculating 12 and 24-month lags...")

df['l12_sale'] = df.groupby('permno')['sale'].shift(12)
df['l24_sale'] = df.groupby('permno')['sale'].shift(24)
df['l12_invt'] = df.groupby('permno')['invt'].shift(12)
df['l24_invt'] = df.groupby('permno')['invt'].shift(24)

# Primary formula: GrSaleToGrInv = ((sale- (.5*(l12.sale + l24.sale)))/(.5*(l12.sale + l24.sale))) - ((invt- (.5*(l12.invt + l24.invt)))/(.5*(l12.invt + l24.invt)))
print("Calculating primary GrSaleToGrInv formula...")

# Calculate average of 12 and 24-month lags
df['avg_l12_l24_sale'] = 0.5 * (df['l12_sale'] + df['l24_sale'])
df['avg_l12_l24_invt'] = 0.5 * (df['l12_invt'] + df['l24_invt'])

# Calculate sales growth component
df['sale_growth'] = np.where(
    df['avg_l12_l24_sale'] == 0,
    np.nan,  # Division by zero = missing
    (df['sale'] - df['avg_l12_l24_sale']) / df['avg_l12_l24_sale']
)

# Calculate inventory growth component  
df['invt_growth'] = np.where(
    df['avg_l12_l24_invt'] == 0,
    np.nan,  # Division by zero = missing
    (df['invt'] - df['avg_l12_l24_invt']) / df['avg_l12_l24_invt']
)

# Primary GrSaleToGrInv calculation
df['GrSaleToGrInv'] = df['sale_growth'] - df['invt_growth']

# Fallback formula: replace GrSaleToGrInv = ((sale-l12.sale)/l12.sale)-((invt-l12.invt)/l12.invt) if mi(GrSaleToGrInv)
print("Applying fallback formula for missing values...")

# Calculate fallback components
df['sale_growth_12m'] = np.where(
    df['l12_sale'] == 0,
    np.nan,  # Division by zero = missing
    (df['sale'] - df['l12_sale']) / df['l12_sale']
)

df['invt_growth_12m'] = np.where(
    df['l12_invt'] == 0,
    np.nan,  # Division by zero = missing
    (df['invt'] - df['l12_invt']) / df['l12_invt']
)

df['GrSaleToGrInv_fallback'] = df['sale_growth_12m'] - df['invt_growth_12m']

# Apply fallback when primary is missing (equivalent to Stata's mi() function)
df['GrSaleToGrInv'] = np.where(
    df['GrSaleToGrInv'].isna(),
    df['GrSaleToGrInv_fallback'],
    df['GrSaleToGrInv']
)

print(f"Calculated GrSaleToGrInv for {df['GrSaleToGrInv'].notna().sum()} observations")

# Clean up intermediate columns
df = df[['gvkey', 'permno', 'time_avail_m', 'GrSaleToGrInv']].copy()

# SAVE
# do "$pathCode/savepredictor" GrSaleToGrInv
save_predictor(df, 'GrSaleToGrInv')

print("GrSaleToGrInv.py completed successfully")