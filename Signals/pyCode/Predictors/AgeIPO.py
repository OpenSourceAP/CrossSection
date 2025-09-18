# ABOUTME: Age-based predictor following Ritter 1991, Table 9A
# ABOUTME: Computes firm age relative to founding year for companies that went public 3-36 months ago

"""
AgeIPO.py

Usage:
    Run from [Repo-Root]/Signals/pyCode/

    python3 Predictors/AgeIPO.py

Inputs:
    - SignalMasterTable.parquet: Monthly master table with permno, time_avail_m
    - IPODates.parquet: IPO dates with columns [permno, IPOdate, FoundingYear]

Outputs:
    - AgeIPO.csv: CSV file with columns [permno, yyyymm, AgeIPO]
    - AgeIPO = year - FoundingYear, only for recent IPO firms (3-36 months post-IPO)
    - Requires at least 100 IPO firms per month
"""

import pandas as pd
import numpy as np
from pathlib import Path
import sys
import os

# Add utils directory to path for imports
sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
from utils.save_standardized import save_predictor


print("Starting AgeIPO.py...")

# DATA LOAD
print("Loading SignalMasterTable data...")

# Load SignalMasterTable with firm identifiers and time availability dates
signal_master_path = Path("../pyData/Intermediate/SignalMasterTable.parquet")
if not signal_master_path.exists():
    raise FileNotFoundError(f"Required input file not found: {signal_master_path}")

df = pd.read_parquet(signal_master_path)

# Keep only the columns we need
required_cols = ["permno", "time_avail_m"]
missing_cols = [col for col in required_cols if col not in df.columns]
if missing_cols:
    raise ValueError(f"Missing required columns in SignalMasterTable: {missing_cols}")

df = df[required_cols].copy()

print(f"Loaded SignalMasterTable: {df.shape[0]} rows, {df.shape[1]} columns")

# Merge with IPO dates data to get founding years and IPO dates
print("Merging with IPODates...")

ipo_dates_path = Path("../pyData/Intermediate/IPODates.parquet")
if not ipo_dates_path.exists():
    raise FileNotFoundError(f"Required input file not found: {ipo_dates_path}")

ipo_dates = pd.read_parquet(ipo_dates_path)
required_ipo_cols = ["permno", "IPOdate", "FoundingYear"]
missing_ipo_cols = [col for col in required_ipo_cols if col not in ipo_dates.columns]
if missing_ipo_cols:
    raise ValueError(f"Missing required columns in IPODates: {missing_ipo_cols}")

ipo_dates = ipo_dates[required_ipo_cols].copy()

# Left join to preserve all master table observations
df = pd.merge(df, ipo_dates, on="permno", how="left")

print(f"After merging with IPODates: {df.shape[0]} rows")

# SIGNAL CONSTRUCTION

# Create flag for recent IPO firms (3-36 months post-IPO)
print("Calculating recent IPO filter...")

# Calculate months since IPO
months_since_ipo = (
    df["time_avail_m"] - df["IPOdate"]
).dt.days / 30.44  # Convert to months

# Recent IPO filter: 3-36 months post-IPO
df["tempipo"] = (months_since_ipo <= 36) & (months_since_ipo >= 3)
df.loc[df["IPOdate"].isna(), "tempipo"] = np.nan

# Calculate firm age as current year minus founding year
print("Calculating AgeIPO...")
df["AgeIPO"] = df["time_avail_m"].dt.year - df["FoundingYear"]

# Restrict to only recent IPO firms
df.loc[df["tempipo"] == 0, "AgeIPO"] = np.nan
df.loc[df["tempipo"].isna(), "AgeIPO"] = np.nan

# Apply minimum threshold of IPO firms per month to ensure statistical validity
print("Applying minimum IPO firms per month filter...")

# Count IPO firms per month (tempipo == 1)
df["tempTotal"] = df.groupby("time_avail_m")["tempipo"].transform("sum")

# Require at least 100 IPO firms per month (20*5)
df.loc[df["tempTotal"] < 100, "AgeIPO"] = np.nan

# Clean up temporary columns
df = df.drop(columns=["tempipo", "tempTotal", "IPOdate", "FoundingYear"])

print(f"Calculated AgeIPO for {df['AgeIPO'].notna().sum()} observations")

# SAVE
# Save the predictor using standardized format
save_predictor(df, "AgeIPO")

print("AgeIPO.py completed successfully")
