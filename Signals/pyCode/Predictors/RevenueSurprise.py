# ABOUTME: Revenue Surprise following Jegadeesh and Livnat 2006, Journal of Accounting and Economics, Table 7 Model 1 SURGE
# ABOUTME: calculates standardized revenue surprise scaled by revenue per share standard deviation

"""
RevenueSurprise.py

Usage:
    Run from [Repo-Root]/Signals/pyCode/
    python3 Predictors/RevenueSurprise.py

Inputs:
    - SignalMasterTable.parquet: Master table with columns [permno, gvkey, time_avail_m]
    - m_QCompustat.parquet: Quarterly Compustat data with columns [gvkey, time_avail_m, revtq, cshprq]

Outputs:
    - RevenueSurprise.csv: CSV file with columns [permno, yyyymm, RevenueSurprise]
"""

import pandas as pd
import numpy as np

# DATA LOAD
# Load SignalMasterTable with specific columns
df = pd.read_parquet(
    "../pyData/Intermediate/SignalMasterTable.parquet",
    columns=["permno", "gvkey", "time_avail_m"],
)

# Keep observations with valid gvkey
df = df.dropna(subset=["gvkey"])

# Merge with quarterly Compustat data for revenue and shares outstanding
qcompustat = pd.read_parquet(
    "../pyData/Intermediate/m_QCompustat.parquet",
    columns=["gvkey", "time_avail_m", "revtq", "cshprq"],
)

df = df.merge(qcompustat, on=["gvkey", "time_avail_m"], how="inner")

# SIGNAL CONSTRUCTION
# Sort by firm and time for panel calculations
df = df.sort_values(["permno", "time_avail_m"])

# Calculate revenue per share
df["revps"] = df["revtq"] / df["cshprq"]

# Calculate year-over-year change in revenue per share
# Use calendar-based lags for exact date matching
df["date_lag12"] = df["time_avail_m"] - pd.DateOffset(months=12)
temp_merge = df[["permno", "time_avail_m", "revps"]].copy()
temp_merge.columns = ["permno", "date_lag12", "revps_l12"]
df = df.merge(temp_merge, on=["permno", "date_lag12"], how="left")
df = df.drop("date_lag12", axis=1)
df["GrTemp"] = df["revps"] - df["revps_l12"]

# Create historical revenue changes for drift calculation
# Use 3, 6, 9, 12, 15, 18, 21, 24 month lags of revenue changes
for n in range(3, 25, 3):
    df[f"date_lag{n}"] = df["time_avail_m"] - pd.DateOffset(months=n)
    temp_merge = df[["permno", "time_avail_m", "GrTemp"]].copy()
    temp_merge.columns = ["permno", f"date_lag{n}", f"grtemp_lag{n}"]
    df = df.merge(temp_merge, on=["permno", f"date_lag{n}"], how="left")
    df = df.drop(f"date_lag{n}", axis=1)

# Calculate mean of historical revenue changes
grtemp_lag_cols = [f"grtemp_lag{n}" for n in range(3, 25, 3)]
df["Drift"] = df[grtemp_lag_cols].mean(axis=1)

# Calculate revenue surprise as change minus historical drift
df["RevenueSurprise"] = df["revps"] - df["revps_l12"] - df["Drift"]

# Drop grtemp lag columns
df = df.drop(columns=grtemp_lag_cols)

# Create historical revenue surprises for volatility calculation
# Use 3, 6, 9, 12, 15, 18, 21, 24 month lags of revenue surprises
for n in range(3, 25, 3):
    df[f"date_lag{n}"] = df["time_avail_m"] - pd.DateOffset(months=n)
    temp_merge = df[["permno", "time_avail_m", "RevenueSurprise"]].copy()
    temp_merge.columns = ["permno", f"date_lag{n}", f"rs_lag{n}"]
    df = df.merge(temp_merge, on=["permno", f"date_lag{n}"], how="left")
    df = df.drop(f"date_lag{n}", axis=1)

# Calculate standard deviation of historical revenue surprises
# Use sample standard deviation with n-1 denominator
rs_lag_cols = [f"rs_lag{n}" for n in range(3, 25, 3)]
df["SD"] = df[rs_lag_cols].std(axis=1, ddof=1)

# Standardize revenue surprise by historical volatility
# Division by very small SD can create large values
df["RevenueSurprise"] = df["RevenueSurprise"] / df["SD"]
# Replace infinite values with NaN when SD = 0
df["RevenueSurprise"] = df["RevenueSurprise"].replace([np.inf, -np.inf], np.nan)

# Keep only observations with valid RevenueSurprise and reliable SD
# Filter out observations with unreliable SD calculations
df = df.dropna(subset=["RevenueSurprise"])
df = df.dropna(subset=["SD"])  # Remove observations where SD = NaN
df = df[df["SD"] > 1e-8]  # Remove observations where SD is essentially zero

# Keep only required columns for final output
result = df[["permno", "time_avail_m", "RevenueSurprise"]].copy()

# Convert time_avail_m to yyyymm format
result["yyyymm"] = (
    result["time_avail_m"].dt.year * 100 + result["time_avail_m"].dt.month
)

# Format final output
result = result[["permno", "yyyymm", "RevenueSurprise"]]

# Convert permno and yyyymm to int
result["permno"] = result["permno"].astype(int)
result["yyyymm"] = result["yyyymm"].astype(int)

# SAVE
result.to_csv("../pyData/Predictors/RevenueSurprise.csv", index=False)

print(f"RevenueSurprise predictor created with {len(result)} observations")
