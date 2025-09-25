# ABOUTME: Book leverage following Fama and French 1992, Table 3 Ln(A/BE)
# ABOUTME: calculates book leverage as total assets divided by book value of equity plus deferred taxes

"""
BookLeverage.py

Usage:
    Run from [Repo-Root]/Signals/pyCode/

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
sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
from utils.save_standardized import save_predictor


print("Starting BookLeverage.py...")

# DATA LOAD
print("Loading m_aCompustat data...")

# Load monthly Compustat data with required balance sheet variables
m_aCompustat_path = Path("../pyData/Intermediate/m_aCompustat.parquet")
if not m_aCompustat_path.exists():
    raise FileNotFoundError(f"Required input file not found: {m_aCompustat_path}")

df = pd.read_parquet(m_aCompustat_path)

# Keep only the columns we need
required_cols = [
    "permno",
    "time_avail_m",
    "at",
    "lt",
    "txditc",
    "pstk",
    "pstkrv",
    "pstkl",
    "seq",
    "ceq",
]
missing_cols = [col for col in required_cols if col not in df.columns]
if missing_cols:
    raise ValueError(f"Missing required columns in m_aCompustat: {missing_cols}")

df = df[required_cols].copy()

print(f"Loaded m_aCompustat: {df.shape[0]} rows, {df.shape[1]} columns")

# Remove duplicate observations by keeping first occurrence for each firm-month
print("Deduplicating by permno time_avail_m...")
df = df.drop_duplicates(subset=["permno", "time_avail_m"], keep="first")
print(f"After deduplication: {df.shape[0]} rows")

# SIGNAL CONSTRUCTION

# Set deferred tax credits to zero when missing
df["txditc"] = df["txditc"].fillna(0)

# Calculate preferred stock using hierarchical fallback: pstk, then pstkrv, then pstkl
print("Calculating tempPS with fallback logic...")
df["tempPS"] = df["pstk"].copy()
df["tempPS"] = df["tempPS"].fillna(df["pstkrv"])
df["tempPS"] = df["tempPS"].fillna(df["pstkl"])

# Calculate stockholders equity using hierarchical fallback: seq, then ceq+preferred stock, then assets minus liabilities
print("Calculating tempSE with fallback logic...")
df["tempSE"] = df["seq"].copy()
df["tempSE"] = df["tempSE"].fillna(df["ceq"] + df["tempPS"])
df["tempSE"] = df["tempSE"].fillna(df["at"] - df["lt"])

# Calculate book leverage as total assets divided by book equity (stockholders equity plus deferred taxes minus preferred stock)
print("Calculating BookLeverage...")

# Calculate book equity (denominator)
df["book_equity"] = df["tempSE"] + df["txditc"] - df["tempPS"]

# Handle division by zero with correct missing value handling
df["BookLeverage"] = np.where(
    df["book_equity"] == 0,
    np.nan,  # Division by zero = missing
    df["at"] / df["book_equity"]  # pandas: missing/missing = NaN naturally
)

print(f"Calculated BookLeverage for {df['BookLeverage'].notna().sum()} observations")

# SAVE
# Save the predictor using standardized format
save_predictor(df, "BookLeverage")

print("BookLeverage.py completed successfully")
