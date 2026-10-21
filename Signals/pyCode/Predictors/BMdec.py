# ABOUTME: Book to market using December ME following Fama and French 1992, Table 3 Ln(BE/ME)
# ABOUTME: calculates book-to-market ratio using most recent December value of market equity

"""
BMdec.py

Usage:
    Run from [Repo-Root]/Signals/pyCode/
    python3 Predictors/BMdec.py

Inputs:
    - m_aCompustat.parquet: Monthly Compustat data with columns [permno, time_avail_m, txditc, seq, ceq, at, lt, pstk, pstkrv, pstkl]
    - monthlyCRSP.parquet: Monthly CRSP data with columns [permno, time_avail_m, prc, shrout]

Outputs:
    - BMdec.csv: CSV file with columns [permno, yyyymm, BMdec]
"""

import pandas as pd
import numpy as np
import sys
import os

# Add utils directory to path for imports
sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
from utils.save_standardized import save_predictor
from utils.stata_replication import stata_multi_lag

print("Starting BMdec predictor...")

# DATA LOAD
print("Loading m_aCompustat data...")
compustat_df = pd.read_parquet(
    "../pyData/Intermediate/m_aCompustat.parquet",
    columns=[
        "permno",
        "time_avail_m",
        "txditc",
        "seq",
        "ceq",
        "at",
        "lt",
        "pstk",
        "pstkrv",
        "pstkl",
    ],
)

print(f"Loaded {len(compustat_df):,} Compustat observations")

# Remove duplicate observations for the same permno-month combination, keeping the first occurrence
compustat_df = compustat_df.drop_duplicates(["permno", "time_avail_m"], keep="first")
print(f"After deduplication: {len(compustat_df):,} observations")

print("Loading monthlyCRSP data...")
crsp_df = pd.read_parquet(
    "../pyData/Intermediate/monthlyCRSP.parquet",
    columns=["permno", "time_avail_m", "prc", "shrout"],
)

print(f"Loaded {len(crsp_df):,} CRSP observations")

# Merge Compustat and CRSP data on permno and time_avail_m, keeping only matched observations
print("Merging Compustat and CRSP data...")
df = pd.merge(compustat_df, crsp_df, on=["permno", "time_avail_m"], how="inner")
print(f"After merge: {len(df):,} observations")

# SIGNAL CONSTRUCTION
print("Constructing BMdec signal...")

# Sort data by firm identifier and month for time-series operations
df = df.sort_values(["permno", "time_avail_m"])

# Extract month and year information
df["month"] = df["time_avail_m"].dt.month
df["year"] = df["time_avail_m"].dt.year

# Calculate market equity only for December observations (absolute price × shares outstanding)
df["tempME"] = np.where(df["month"] == 12, abs(df["prc"]) * df["shrout"], np.nan)

# Assign December market equity to all months within the same firm-year
# Using min() effectively selects the single non-missing December value per firm-year
df["tempDecME"] = df.groupby(["permno", "year"])["tempME"].transform("min")

# Compute book equity using standard accounting definitions
# Step 1: Handle txditc (replace missing with 0)
df["txditc"] = df["txditc"].fillna(0)

# Step 2: Compute preferred stock (tempPS)
df["tempPS"] = df["pstk"].copy()
df["tempPS"] = df["tempPS"].fillna(df["pstkrv"])
df["tempPS"] = df["tempPS"].fillna(df["pstkl"])

# Step 3: Compute shareholders equity (tempSE)
df["tempSE"] = df["seq"].copy()
# If seq is missing, use ceq + tempPS
mask_seq_missing = df["tempSE"].isna()
df.loc[mask_seq_missing, "tempSE"] = (
    df.loc[mask_seq_missing, "ceq"] + df.loc[mask_seq_missing, "tempPS"]
)
# If still missing, use at - lt
mask_still_missing = df["tempSE"].isna()
df.loc[mask_still_missing, "tempSE"] = (
    df.loc[mask_still_missing, "at"] - df.loc[mask_still_missing, "lt"]
)

# Step 4: Compute book equity
df["tempBE"] = df["tempSE"] + df["txditc"] - df["tempPS"]

# Preserve observed rows while filling the monthly grid for calendar lags.
df["_observed"] = True
df = stata_multi_lag(df, "permno", "time_avail_m", "tempDecME", [12, 17])
df = df.rename(columns={'tempDecME_lag12': 'l12_tempDecME', 'tempDecME_lag17': 'l17_tempDecME'})
df = df.loc[df["_observed"].eq(True)].drop(columns="_observed")

# Calculate book-to-market ratio using appropriate December market equity lag
# Handle division by zero and missing value cases appropriately

# For months >= 6: use l12.tempDecME
# For months < 6: use l17.tempDecME

# First calculate both potential ratios with correct missing value handling
df["bm_with_l12"] = np.where(
    df["l12_tempDecME"] == 0,
    np.nan,  # Division by zero = missing
    df["tempBE"] / df["l12_tempDecME"]  # pandas: missing/missing = NaN naturally
)

df["bm_with_l17"] = np.where(
    df["l17_tempDecME"] == 0,
    np.nan,  # Division by zero = missing
    df["tempBE"] / df["l17_tempDecME"]  # pandas: missing/missing = NaN naturally
)

# Now assign based on month
df["BMdec"] = np.where(df["month"] >= 6, df["bm_with_l12"], df["bm_with_l17"])

print(f"Generated BMdec values for {df['BMdec'].notna().sum():,} observations")

# Remove temporary calculation columns that are no longer needed
temp_cols = [
    col for col in df.columns if col.startswith("temp") or col.startswith("bm_with")
]
df = df.drop(columns=temp_cols + ["month", "year"])

# SAVE
print("Saving predictor...")
save_predictor(df, "BMdec")

print("BMdec predictor completed successfully!")
