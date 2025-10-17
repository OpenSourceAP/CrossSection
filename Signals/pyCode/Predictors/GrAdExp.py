# ABOUTME: Growth in advertising expenses following Lou 2014 RFS, Table 2A Year 1 Excess
# ABOUTME: calculates log growth in advertising expenses with size and threshold filters

"""
GrAdExp.py

Usage:
    Run from [Repo-Root]/Signals/pyCode/
    python3 Predictors/GrAdExp.py

Inputs:
    - m_aCompustat.parquet: Monthly Compustat data with columns [permno, time_avail_m, at, xad]
    - SignalMasterTable.parquet: Monthly master table with mve_c

Outputs:
    - GrAdExp.csv: CSV file with columns [permno, yyyymm, GrAdExp]
"""

import pandas as pd
import numpy as np
from pathlib import Path
import sys
import os

# Add utils directory to path for imports
sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
from utils.save_standardized import save_predictor


print("Starting GrAdExp.py...")

# DATA LOAD
print("Loading m_aCompustat data...")

# Load m_aCompustat
m_aCompustat_path = Path("../pyData/Intermediate/m_aCompustat.parquet")

df = pd.read_parquet(m_aCompustat_path, columns=["permno", "time_avail_m", "at", "xad"])

print(f"Loaded m_aCompustat: {df.shape[0]} rows, {df.shape[1]} columns")

# Remove duplicate observations by permno and time_avail_m
print("Removing duplicate observations...")
initial_count = df.shape[0]
df = df.drop_duplicates(subset=["permno", "time_avail_m"], keep="first")
duplicates_removed = initial_count - df.shape[0]
if duplicates_removed > 0:
    print(f"Removed {duplicates_removed} duplicate observations")

# Merge with SignalMasterTable to get market value data
print("Merging with SignalMasterTable...")

signal_master = pd.read_parquet("../pyData/Intermediate/SignalMasterTable.parquet", 
    columns=["permno", "time_avail_m", "mve_c"])

# Left join to preserve all master records
df = pd.merge(df, signal_master, on=["permno", "time_avail_m"], how="left")

print(f"After merging with SignalMasterTable: {df.shape[0]} rows")

# SIGNAL CONSTRUCTION

# Sort data for lag calculations
print("Sorting data by permno and time_avail_m...")
df = df.sort_values(["permno", "time_avail_m"])


print("Calculating GrAdExp...")

# First calculate log of xad for current and lagged values
with np.errstate(divide="ignore", invalid="ignore"):
    df["log_xad"] = np.log(df["xad"])

# Calculate growth in advertising expenses 
df["log_xad_l12"] = df.groupby("permno")["log_xad"].shift(12)
df["GrAdExp"] = df["log_xad"] - df["log_xad_l12"]

# Calculate size deciles for filtering
print("Calculating size deciles...")

# Calculate size deciles using groupby, transform, qcut pattern (based on mve_c)
df["tempSize"] = df.groupby("time_avail_m")["mve_c"].transform(
    lambda x: pd.qcut(x, q=10, labels=False, duplicates="drop") + 1
)

# Filter out small advertising expenses and smallest size decile
print("Applying filters...")
initial_valid = df["GrAdExp"].notna().sum()

# Set to missing if xad < 0.1 or in smallest size decile
df.loc[(df["xad"] < 0.1) | (df["tempSize"] == 1), "GrAdExp"] = np.nan

final_valid = df["GrAdExp"].notna().sum()
filtered_out = initial_valid - final_valid
print(f"Filtered out {filtered_out} observations (xad < 0.1 or smallest size decile)")
print(f"Final GrAdExp calculated for {final_valid} observations")

# SAVE
save_predictor(df, "GrAdExp")

print("GrAdExp.py completed successfully")
