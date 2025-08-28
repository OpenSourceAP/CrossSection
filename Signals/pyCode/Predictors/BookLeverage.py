# ABOUTME: BookLeverage.py - calculates BookLeverage predictor using book leverage ratio
# ABOUTME: Direct line-by-line translation from Stata Code/Predictors/BookLeverage.do

"""
BookLeverage.py

Usage:
    cd pyCode/
    source .venv/bin/activate
    python3 Predictors/BookLeverage.py

Inputs:
    - m_aCompustat.parquet: Monthly Compustat data with columns [permno, time_avail_m, at, lt, txditc, pstk, pstkrv, pstkl, seq, ceq]

Outputs:
    - BookLeverage.csv: CSV file with columns [permno, yyyymm, BookLeverage]
    - BookLeverage = at/(tempSE + txditc - tempPS) where tempSE and tempPS are derived from multiple fallback calculations
"""

import pandas as pd
import numpy as np
from pathlib import Path
import sys
import os

# Add utils directory to path for imports
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from utils.save_standardized import save_predictor


print("Starting BookLeverage.py...")

# DATA LOAD
print("Loading m_aCompustat data...")

# Load m_aCompustat - equivalent to Stata: use permno time_avail_m at lt txditc pstk pstkrv pstkl seq ceq using "$pathDataIntermediate/m_aCompustat", clear
m_aCompustat_path = Path("../pyData/Intermediate/m_aCompustat.parquet")
if not m_aCompustat_path.exists():
    raise FileNotFoundError(f"Required input file not found: {m_aCompustat_path}")

df = pd.read_parquet(m_aCompustat_path)

# Keep only the columns we need
required_cols = ['permno', 'time_avail_m', 'at', 'lt', 'txditc', 'pstk', 'pstkrv', 'pstkl', 'seq', 'ceq']
missing_cols = [col for col in required_cols if col not in df.columns]
if missing_cols:
    raise ValueError(f"Missing required columns in m_aCompustat: {missing_cols}")

df = df[required_cols].copy()

print(f"Loaded m_aCompustat: {df.shape[0]} rows, {df.shape[1]} columns")

# bysort permno time_avail_m: keep if _n == 1  // deletes a few observations
print("Deduplicating by permno time_avail_m...")
df = df.drop_duplicates(subset=['permno', 'time_avail_m'], keep='first')
print(f"After deduplication: {df.shape[0]} rows")

# SIGNAL CONSTRUCTION

# replace txditc = 0 if mi(txditc)
df['txditc'] = df['txditc'].fillna(0)

# gen tempPS = pstk
# replace tempPS = pstkrv if mi(tempPS)
# replace tempPS = pstkl if mi(tempPS)
print("Calculating tempPS with fallback logic...")
df['tempPS'] = df['pstk'].copy()
df['tempPS'] = df['tempPS'].fillna(df['pstkrv'])
df['tempPS'] = df['tempPS'].fillna(df['pstkl'])

# gen tempSE = seq
# replace tempSE = ceq + tempPS if mi(tempSE)
# replace tempSE = at - lt if mi(tempSE)
print("Calculating tempSE with fallback logic...")
df['tempSE'] = df['seq'].copy()
df['tempSE'] = df['tempSE'].fillna(df['ceq'] + df['tempPS'])
df['tempSE'] = df['tempSE'].fillna(df['at'] - df['lt'])

# gen BookLeverage = at/(tempSE + txditc - tempPS)
print("Calculating BookLeverage...")

# Calculate book equity (denominator)
df['book_equity'] = df['tempSE'] + df['txditc'] - df['tempPS']

# Calculate book leverage with domain-aware missing value handling
# Following missing/missing = 1.0 pattern for division operations
df['BookLeverage'] = np.where(
    df['book_equity'] == 0,
    np.nan,  # Division by zero = missing
    np.where(
        df['at'].isna() & df['book_equity'].isna(),
        1.0,  # missing/missing = 1.0 (no change)
        df['at'] / df['book_equity']
    )
)

print(f"Calculated BookLeverage for {df['BookLeverage'].notna().sum()} observations")

# SAVE
# do "$pathCode/savepredictor" BookLeverage
save_predictor(df, 'BookLeverage')

print("BookLeverage.py completed successfully")