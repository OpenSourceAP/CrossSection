# ABOUTME: Capital expenditure growth following Anderson and Garcia-Feijoo 2006, Tables 3B and 3D
# ABOUTME: Calculates grcapx (2-year growth), grcapx1y (1-year lagged growth), grcapx3y (3-year growth)

"""
ZZ1_grcapx_grcapx1y_grcapx3y.py

Usage:
    Run from [Repo-Root]/Signals/pyCode/

    python3 Predictors/ZZ1_grcapx_grcapx1y_grcapx3y.py

Inputs:
    - m_aCompustat.parquet: Monthly Compustat data with columns [gvkey, permno, time_avail_m, capx, ppent, at]
    - SignalMasterTable.parquet: Master table with exchcd column

Outputs:
    - grcapx.csv: Predictor file with columns [permno, yyyymm, grcapx]
    - grcapx1y.csv: Placebo file with columns [permno, yyyymm, grcapx1y]
    - grcapx3y.csv: Predictor file with columns [permno, yyyymm, grcapx3y]

Signal definitions:
    - grcapx = (capx-l24.capx)/l24.capx (2-year capex growth)
    - grcapx1y = (l12.capx-l24.capx)/l24.capx (1-year capex growth, lagged)
    - grcapx3y = capx/(l12.capx + l24.capx + l36.capx )*3 (3-year capex growth)
"""

import pandas as pd
import numpy as np
from pathlib import Path
import sys
import os

# Add utils directory to path for imports
sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
from utils.save_standardized import save_predictor, save_placebo


print("Starting ZZ1_grcapx_grcapx1y_grcapx3y.py...")

# DATA LOAD
print("Loading m_aCompustat data...")

# Load required columns from monthly Compustat data
m_aCompustat_path = Path("../pyData/Intermediate/m_aCompustat.parquet")
if not m_aCompustat_path.exists():
    raise FileNotFoundError(f"Required input file not found: {m_aCompustat_path}")

df = pd.read_parquet(m_aCompustat_path)

# Keep only the columns we need
required_cols = ["gvkey", "permno", "time_avail_m", "capx", "ppent", "at"]
missing_cols = [col for col in required_cols if col not in df.columns]
if missing_cols:
    raise ValueError(f"Missing required columns in m_aCompustat: {missing_cols}")

df = df[required_cols].copy()

print(f"Loaded m_aCompustat: {df.shape[0]} rows, {df.shape[1]} columns")

# Remove duplicate permno-time_avail_m observations
print("Removing duplicate permno-time_avail_m observations...")
initial_rows = len(df)
df = df.drop_duplicates(subset=["permno", "time_avail_m"], keep="first")
print(f"Removed {initial_rows - len(df)} duplicate observations")

# Merge with SignalMasterTable to get exchange codes
print("Merging with SignalMasterTable...")

signal_master = pd.read_parquet("../pyData/Intermediate/SignalMasterTable.parquet")
signal_master = signal_master[["permno", "time_avail_m", "exchcd"]].copy()

# Inner merge to keep only observations that match in both datasets
df = pd.merge(signal_master, df, on=["permno", "time_avail_m"], how="inner")

print(f"After merge: {df.shape[0]} rows, {df.shape[1]} columns")

# SIGNAL CONSTRUCTION

# Set up panel data by sorting by permno and time
print("Setting up panel data (sorting by permno, time_avail_m)...")
df = df.sort_values(["permno", "time_avail_m"])

# Need Firm Age
# Calculate firm age as sequence number within each permno
print("Calculating FirmAge...")
df["FirmAge"] = df.groupby("permno").cumcount() + 1

# remove stuff we started with (don't have age for)
# Calculate time since CRSP start date
print("Calculating tempcrsptime and applying FirmAge restriction...")
crsp_start = pd.Timestamp("1926-07-01")
df["tempcrsptime"] = ((df["time_avail_m"] - crsp_start).dt.days / 30.44).round().astype(
    int
) + 1

# Set FirmAge to missing if it equals time since CRSP start
df.loc[df["tempcrsptime"] == df["FirmAge"], "FirmAge"] = np.nan

# Create l12_ppent lag first (needed for conditional capx replacement)
print("Creating l12_ppent lag for conditional replacement...")
df["l12_ppent"] = df.groupby("permno")["ppent"].shift(12)

# Replace missing capx with change in ppent for firms with sufficient age
print("Applying conditional capx replacement...")
condition = df["capx"].isna() & (df["FirmAge"] >= 24)
df.loc[condition, "capx"] = df.loc[condition, "ppent"] - df.loc[condition, "l12_ppent"]

# Create lags for capx AFTER the conditional replacement
print("Creating lags for capx after replacement...")
df["l12_capx"] = df.groupby("permno")["capx"].shift(12)
df["l24_capx"] = df.groupby("permno")["capx"].shift(24)
df["l36_capx"] = df.groupby("permno")["capx"].shift(36)

# Calculate the three predictors
print("Calculating predictors...")

# Calculate 2-year capital expenditure growth
df["grcapx"] = (df["capx"] - df["l24_capx"]) / df["l24_capx"]

# Calculate 1-year capital expenditure growth (lagged)
df["grcapx1y"] = (df["l12_capx"] - df["l24_capx"]) / df["l24_capx"]

# Calculate 3-year capital expenditure growth
df["grcapx3y"] = df["capx"] / (df["l12_capx"] + df["l24_capx"] + df["l36_capx"]) * 3

print(f"Calculated grcapx for {df['grcapx'].notna().sum()} observations")
print(f"Calculated grcapx1y for {df['grcapx1y'].notna().sum()} observations")
print(f"Calculated grcapx3y for {df['grcapx3y'].notna().sum()} observations")

# SAVE
# Save grcapx predictor
save_predictor(df, "grcapx")

# Save grcapx1y placebo
save_placebo(df, "grcapx1y")

# Save grcapx3y predictor
save_predictor(df, "grcapx3y")

print("ZZ1_grcapx_grcapx1y_grcapx3y.py completed successfully")
