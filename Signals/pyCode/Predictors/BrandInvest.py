# ABOUTME: Brand capital investment following Belo, Lin and Vitorino 2014, Table 1A r^S
# ABOUTME: calculates brand investment rate as advertising expense divided by brand capital

"""
BrandInvest.py

Usage:
    Run from [Repo-Root]/Signals/pyCode/
    python3 Predictors/BrandInvest.py

Inputs:
    - a_aCompustat.parquet: Annual Compustat data with columns [gvkey, permno, time_avail_m, fyear, datadate, xad, xad0, at, sic]

Outputs:
    - BrandInvest.csv: CSV file with columns [permno, yyyymm, BrandInvest]
"""

import pandas as pd
import numpy as np
import sys
import os

# Add utils directory to path for imports
sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
from utils.save_standardized import save_predictor

print("Starting BrandInvest predictor...")

# DATA LOAD
print("Loading a_aCompustat data...")
df = pd.read_parquet(
    "../pyData/Intermediate/a_aCompustat.parquet",
    columns=[
        "gvkey",
        "permno",
        "time_avail_m",
        "fyear",
        "datadate",
        "xad",
        "xad0",
        "at",
        "sic",
    ],
)

print(f"Loaded {len(df):,} annual Compustat observations")

# SIGNAL CONSTRUCTION
print("Constructing BrandInvest signal...")

# Sort by gvkey and fyear (equivalent to xtset gvkey fyear)
df = df.sort_values(["gvkey", "fyear"])

# Calculate brand capital accumulation
print("Calculating brand capital accumulation...")

# Create OK flag for non-missing xad
df["OK"] = df["xad"].notna()

# BrandCapital was not shown to predict in OP
# Initialize BrandCapital for first observation of each gvkey with non-missing xad
# BrandCapital = xad/(.5 + .1) for first non-missing xad observation
df["BrandCapital"] = np.nan
df["tempYear"] = np.nan

# Process each gvkey separately
for gvkey in df["gvkey"].unique():
    gvkey_mask = df["gvkey"] == gvkey
    gvkey_data = df[gvkey_mask].copy()

    # Find first non-missing xad observation
    ok_data = gvkey_data[gvkey_data["OK"]].copy()
    if len(ok_data) > 0:
        first_idx = ok_data.index[0]
        first_xad = ok_data.loc[first_idx, "xad"]
        first_year = ok_data.loc[first_idx, "fyear"]

        # Initialize brand capital for first observation
        df.loc[first_idx, "BrandCapital"] = first_xad / (
            0.5 + 0.1
        )  # 0.6 depreciation rate
        df.loc[first_idx, "tempYear"] = first_year

# Calculate FirstNMyear (minimum year with non-missing xad by gvkey)
df["FirstNMyear"] = df.groupby("gvkey")["tempYear"].transform("min")

# Create tempxad (xad with missing values replaced by 0)
df["tempxad"] = df["xad"].fillna(0)

# Fill missing BrandCapital with 0 initially
df["BrandCapital"] = df["BrandCapital"].fillna(0)

# Calculate cumulative brand capital with depreciation
print("Applying depreciation and accumulation...")

# Process each gvkey separately for cumulative calculation
for gvkey in df["gvkey"].unique():
    gvkey_mask = df["gvkey"] == gvkey
    gvkey_data = df[gvkey_mask].copy()

    # Sort by fyear and apply cumulative formula
    gvkey_data = gvkey_data.sort_values("fyear")

    for i in range(1, len(gvkey_data)):
        curr_idx = gvkey_data.index[i]
        prev_idx = gvkey_data.index[i - 1]

        # BrandCapital = (1-.5)*l.BrandCapital + tempxad for observations after first
        prev_brand_capital = df.loc[prev_idx, "BrandCapital"]
        curr_tempxad = df.loc[curr_idx, "tempxad"]

        df.loc[curr_idx, "BrandCapital"] = (1 - 0.5) * prev_brand_capital + curr_tempxad

# Apply exclusion rules
# Set BrandCapital to missing if before FirstNMyear or if original xad was missing
df.loc[df["FirstNMyear"].isna() | (df["fyear"] < df["FirstNMyear"]), "BrandCapital"] = (
    np.nan
)
df.loc[df["xad"].isna(), "BrandCapital"] = np.nan

# Scale BrandCapital by total assets (replace BrandCapital = BrandCapital/at)
df["BrandCapital"] = df["BrandCapital"] / df["at"]

# Calculate BrandInvest = xad0/l.BrandCapital
df["l_BrandCapital"] = df.groupby("gvkey")["BrandCapital"].shift(1)
df["BrandInvest"] = df["xad0"] / df["l_BrandCapital"]

# Filter by industry (exclude utilities and financials)
print("Applying industry filters...")

# Convert sic to numeric if it's string
df["sic_numeric"] = pd.to_numeric(df["sic"], errors="coerce")

# filter (OP page 4)
# Drop utilities (4900-4999) and financials (6000-6999)
before_filter = len(df)
df = df[~((df["sic_numeric"] >= 4900) & (df["sic_numeric"] <= 4999))]
df = df[~((df["sic_numeric"] >= 6000) & (df["sic_numeric"] <= 6999))]
print(f"Filtered out {before_filter - len(df):,} observations (utilities/financials)")

# Keep only December data (equivalent to keep if month(datadate) == 12)
df["month"] = pd.to_datetime(df["datadate"]).dt.month
df = df[df["month"] == 12]
print(f"Kept only December observations: {len(df):,}")

# Expand to monthly (equivalent to expand 12)
print("Expanding annual data to monthly...")

expanded_dfs = []
for month_offset in range(12):  # 0 to 11 months
    df_copy = df.copy()
    df_copy["time_avail_m"] = df_copy["time_avail_m"] + pd.DateOffset(
        months=month_offset
    )
    expanded_dfs.append(df_copy)

expanded_df = pd.concat(expanded_dfs, ignore_index=True)
print(f"After monthly expansion: {len(expanded_df):,} observations")

# Remove overlapping observations (keep latest datadate for each gvkey-time_avail_m)
expanded_df = expanded_df.sort_values(["gvkey", "time_avail_m", "datadate"])
expanded_df = expanded_df.drop_duplicates(["gvkey", "time_avail_m"], keep="last")

# Final deduplication by permno-time_avail_m
expanded_df = expanded_df.drop_duplicates(["permno", "time_avail_m"], keep="first")

print(f"After deduplication: {len(expanded_df):,} observations")
print(
    f"Generated BrandInvest values for {expanded_df['BrandInvest'].notna().sum():,} observations"
)

# Clean up temporary columns
expanded_df = expanded_df.drop(
    columns=[
        "OK",
        "tempYear",
        "FirstNMyear",
        "tempxad",
        "BrandCapital",
        "l_BrandCapital",
        "sic_numeric",
        "month",
    ]
)

# SAVE
print("Saving predictor...")
save_predictor(expanded_df, "BrandInvest")

print("BrandInvest predictor completed successfully!")
