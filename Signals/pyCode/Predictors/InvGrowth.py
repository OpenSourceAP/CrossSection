# ABOUTME: Inventory Growth following Belo and Lin 2012, Table 2A EW
# ABOUTME: Creates InvGrowth predictor measuring year-over-year inventory growth using GNP deflator

"""
InvGrowth.py

Usage:
    Run from [Repo-Root]/Signals/pyCode/

    python3 Predictors/InvGrowth.py

Inputs:
    - ../pyData/Intermediate/m_aCompustat.parquet
    - ../pyData/Intermediate/GNPdefl.parquet

Outputs:
    - ../pyData/Predictors/InvGrowth.csv (columns: permno, yyyymm, InvGrowth)
"""

import pandas as pd
import numpy as np
from pathlib import Path

print("Starting InvGrowth predictor...")

# DATA LOAD
print("Loading m_aCompustat data...")
df = pd.read_parquet(
    "../pyData/Intermediate/m_aCompustat.parquet",
    columns=["gvkey", "permno", "time_avail_m", "invt", "sic", "ppent", "at"],
)
print(f"Loaded {len(df):,} Compustat observations")

# Merge with GNP deflator data for inflation adjustment
print("Loading GNPdefl data...")
gnp = pd.read_parquet("../pyData/Intermediate/GNPdefl.parquet")
print(f"Loaded {len(gnp):,} GNPdefl observations")

print("Merging with GNPdefl...")
df = pd.merge(df, gnp, on="time_avail_m", how="inner")
print(f"After merging with GNPdefl: {len(df):,} observations")

# Adjust inventory values for inflation using GNP deflator
print("Adjusting invt for inflation...")
df["invt"] = df["invt"] / df["gnpdefl"]

# Sample selection
print("Applying sample selection filters...")

# Exclude utilities (SIC 4xxx) and financial firms (SIC 6xxx)
df["sic_str"] = df["sic"].astype(str)
before_sic = len(df)
df = df[~df["sic_str"].str.startswith("4")].copy()
df = df[~df["sic_str"].str.startswith("6")].copy()
print(
    f"After SIC filter (dropped SIC 4xxx and 6xxx): {len(df):,} observations (dropped {before_sic - len(df):,})"
)

# Exclude firms with non-positive total assets or property, plant & equipment
before_at_ppent = len(df)
df = df[(df["at"] > 0) & ((df["ppent"] > 0) | df["ppent"].isna())].copy()
print(
    f"After AT/PPENT filter: {len(df):,} observations (dropped {before_at_ppent - len(df):,})"
)

# SIGNAL CONSTRUCTION
print("Constructing InvGrowth signal...")

# Remove duplicate firm-month observations
before_dedup = len(df)
df = df.drop_duplicates(subset=["permno", "time_avail_m"], keep="first")
print(
    f"After deduplication: {len(df):,} observations (dropped {before_dedup - len(df):,} duplicates)"
)

# Calculate 12-month lag for inventory growth
print("Calculating 12-month lag for inventory growth...")

# Sort by permno and time_avail_m for lag calculation
df = df.sort_values(["permno", "time_avail_m"]).copy()

# Create 12-month calendar-based lag for inventory values
print("Implementing efficient calendar-based 12-month lag...")

# Create lag target date for each observation
df["lag_target_date"] = df["time_avail_m"] - pd.DateOffset(months=12)

# Create a dataset for merging lag values
lag_df = df[["permno", "time_avail_m", "invt"]].copy()
lag_df = lag_df.rename(
    columns={"time_avail_m": "lag_target_date", "invt": "invt_lag12"}
)

# Merge to get calendar-based lag values
df = pd.merge(df, lag_df, on=["permno", "lag_target_date"], how="left")

# Clean up temporary columns
df = df.drop(columns=["lag_target_date"])

# Calculate inventory growth as percentage change from 12 months ago
df["InvGrowth"] = df["invt"] / df["invt_lag12"] - 1

# Keep only observations with valid InvGrowth
result = df[["permno", "time_avail_m", "InvGrowth"]].copy()
result = result.dropna(subset=["InvGrowth"]).copy()

print(f"Generated InvGrowth values for {len(result):,} observations")

# Convert time_avail_m to yyyymm
result["yyyymm"] = (
    result["time_avail_m"].dt.year * 100 + result["time_avail_m"].dt.month
)

# Prepare final output
final_result = result[["permno", "yyyymm", "InvGrowth"]].copy()

# SAVE
print("Saving predictor...")
Path("../pyData/Predictors").mkdir(parents=True, exist_ok=True)
final_result.to_csv("../pyData/Predictors/InvGrowth.csv", index=False)

print("saving InvGrowth")
print(f"Saved {len(final_result)} rows to ../pyData/Predictors/InvGrowth.csv")
print("InvGrowth predictor completed successfully!")
