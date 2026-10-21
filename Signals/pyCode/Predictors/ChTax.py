# ABOUTME: Change in Taxes following Thomas and Zhang 2011, Table 2, column (1)
# ABOUTME: calculates 4-quarter change in quarterly total taxes scaled by lagged total assets

"""
ChTax.py

Usage:
    Run from [Repo-Root]/Signals/pyCode/
    python3 Predictors/ChTax.py

Inputs:
    - m_aCompustat.parquet: Monthly Compustat data with columns [permno, gvkey, time_avail_m, at]
    - m_QCompustat.parquet: Quarterly Compustat data with columns [gvkey, time_avail_m, txtq]

Outputs:
    - ChTax.csv: CSV file with columns [permno, yyyymm, ChTax]
"""

import pandas as pd
import numpy as np
import sys
import os

# Add utils directory to path for imports
sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
from utils.save_standardized import save_predictor
from utils.stata_replication import stata_multi_lag


print("Starting ChTax predictor...")

# DATA LOAD
print("Loading m_aCompustat data...")
compustat_df = pd.read_parquet(
    "../pyData/Intermediate/m_aCompustat.parquet",
    columns=["permno", "gvkey", "time_avail_m", "at"],
)

print(f"Loaded {len(compustat_df):,} Compustat observations")

print("Loading m_QCompustat data...")
qcompustat_df = pd.read_parquet(
    "../pyData/Intermediate/m_QCompustat.parquet",
    columns=["gvkey", "time_avail_m", "txtq"],
)

print(f"Loaded {len(qcompustat_df):,} quarterly Compustat observations")

# Merge annual and quarterly Compustat data on company and date
print("Merging Compustat and quarterly data...")
df = pd.merge(compustat_df, qcompustat_df, on=["gvkey", "time_avail_m"], how="inner")

print(f"After merge: {len(df):,} observations")

# SIGNAL CONSTRUCTION
print("Constructing ChTax signal...")

# Sort by company and time for lag calculations
df = df.sort_values(["gvkey", "time_avail_m"])

# Preserve observed rows while filling the monthly grid for calendar lags.
df["_observed"] = True
df = stata_multi_lag(df, "gvkey", "time_avail_m", "txtq", [12])
df = df.rename(columns={'txtq_lag12': 'l12_txtq'})
df = stata_multi_lag(df, "gvkey", "time_avail_m", "at", [12], fill_gaps=False)
df = df.rename(columns={'at_lag12': 'l12_at'})
df = df.loc[df["_observed"].eq(True)].drop(columns="_observed")
# Inserted gvkey-grid rows had missing permno, which made the column float
df["permno"] = df["permno"].astype("int64")

# Calculate change in taxes scaled by lagged total assets
df["ChTax"] = (df["txtq"] - df["l12_txtq"]) / df["l12_at"]

print(f"Generated ChTax values for {df['ChTax'].notna().sum():,} observations")

# SAVE
print("Saving predictor...")
save_predictor(df, "ChTax")

print("ChTax predictor completed successfully!")
