# ABOUTME: Growth in book equity following Lockwood and Prombutr 2010, Table 4A SUSG
# ABOUTME: calculates ratio of book equity to book equity in the previous year

"""
Usage:
    python3 Predictors/ChEQ.py

Inputs:
    - m_aCompustat.parquet: Monthly Compustat data with columns [gvkey, permno, time_avail_m, ceq]

Outputs:
    - ChEQ.csv: CSV file with columns [permno, yyyymm, ChEQ]
    - ChEQ = ceq/l12.ceq, included only if book equity is positive this year and last year
"""

import pandas as pd
import numpy as np
import sys
import os

# Add utils directory to path for imports
sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
from utils.save_standardized import save_predictor

print("Starting ChEQ predictor...")

# DATA LOAD
print("Loading m_aCompustat data...")
df = pd.read_parquet(
    "../pyData/Intermediate/m_aCompustat.parquet",
    columns=["gvkey", "permno", "time_avail_m", "ceq"],
)

print(f"Loaded {len(df):,} Compustat observations")

# Keep only the first record for each permno-month combination
df = df.drop_duplicates(["permno", "time_avail_m"], keep="first")
print(f"After deduplication: {len(df):,} observations")

# SIGNAL CONSTRUCTION
print("Constructing ChEQ signal...")

# Sort by company and date for calculating lagged values
df = df.sort_values(["permno", "time_avail_m"])

# Create 12-month lag of ceq
df["l12_ceq"] = df.groupby("permno")["ceq"].shift(12)

# Calculate sustainable growth as current equity divided by equity from 12 months ago
# Only calculate when both current and lagged equity are positive
df["ChEQ"] = np.where(
    (df["ceq"] > 0) & (df["l12_ceq"] > 0), df["ceq"] / df["l12_ceq"], np.nan
)

print(f"Generated ChEQ values for {df['ChEQ'].notna().sum():,} observations")

# Clean up temporary columns
df = df.drop(columns=["l12_ceq"])

# SAVE
print("Saving predictor...")
save_predictor(df, "ChEQ")

print("ChEQ predictor completed successfully!")
