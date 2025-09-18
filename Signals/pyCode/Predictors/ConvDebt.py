# ABOUTME: Convertible debt indicator following Valta 2016, Table 4 DCONV
# ABOUTME: Binary variable equal to 1 if deferred charges (dc) > 0 or common shares reserved for convertible debt (cshrc) > 0

"""
ConvDebt Predictor

Convertible debt indicator calculation.

Inputs:
- m_aCompustat.parquet (gvkey, permno, time_avail_m, dc, cshrc)

Outputs:
- ConvDebt.csv (permno, yyyymm, ConvDebt)

This predictor calculates:
1. ConvDebt = 0 by default
2. ConvDebt = 1 if (dc != . & dc != 0) | (cshrc != . & cshrc != 0)
"""

import pandas as pd
import numpy as np
import sys
import os

# Add utils directory to path for imports
sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
from utils.save_standardized import save_predictor

print("Starting ConvDebt predictor...")

# DATA LOAD
print("Loading m_aCompustat data...")
df = pd.read_parquet(
    "../pyData/Intermediate/m_aCompustat.parquet",
    columns=["gvkey", "permno", "time_avail_m", "dc", "cshrc"],
)

print(f"Loaded {len(df):,} Compustat observations")

# SIGNAL CONSTRUCTION
print("Constructing ConvDebt signal...")

# Deduplicate by permno time_avail_m
df = df.drop_duplicates(["permno", "time_avail_m"], keep="first")
print(f"After deduplication: {len(df):,} observations")

# Sort by permno and time_avail_m
df = df.sort_values(["permno", "time_avail_m"])

# Calculate ConvDebt indicator
# ConvDebt = 0 by default
df["ConvDebt"] = 0

# ConvDebt = 1 if convertible debt exists (non-zero dc) or converted shares exist (non-zero cshrc)
df.loc[
    ((df["dc"].notna()) & (df["dc"] != 0))
    | ((df["cshrc"].notna()) & (df["cshrc"] != 0)),
    "ConvDebt",
] = 1

print(f"Generated ConvDebt values for {len(df):,} observations")
print(f"ConvDebt = 1 for {(df['ConvDebt'] == 1).sum():,} observations")

# SAVE
print("Saving predictor...")
save_predictor(df, "ConvDebt")

print("ConvDebt predictor completed successfully!")
