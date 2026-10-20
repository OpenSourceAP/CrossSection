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
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parents[1]))
from utils.stata_replication import fill_date_gaps, stata_multi_lag

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

# Keep the monthly grid until all three lag stages are complete.
df["_observed"] = True
df = stata_multi_lag(df, "permno", "time_avail_m", "revps", [12])
df = df.rename(columns={"revps_lag12": "revps_l12"})
df["GrTemp"] = df["revps"] - df["revps_l12"]

df = stata_multi_lag(df, "permno", "time_avail_m", "GrTemp", list(range(3, 25, 3)), fill_gaps=False)
df = df.rename(columns={f"GrTemp_lag{n}": f"grtemp_lag{n}" for n in range(3, 25, 3)})

# Calculate mean of historical revenue changes
grtemp_lag_cols = [f"grtemp_lag{n}" for n in range(3, 25, 3)]
df["Drift"] = df[grtemp_lag_cols].mean(axis=1)

# Calculate revenue surprise as change minus historical drift
df["RevenueSurprise"] = df["revps"] - df["revps_l12"] - df["Drift"]

# Drop grtemp lag columns
df = df.drop(columns=grtemp_lag_cols)

df = stata_multi_lag(df, "permno", "time_avail_m", "RevenueSurprise", list(range(3, 25, 3)), fill_gaps=False)
df = df.rename(columns={f"RevenueSurprise_lag{n}": f"rs_lag{n}" for n in range(3, 25, 3)})
df = df.loc[df["_observed"].eq(True)].drop(columns="_observed").copy()


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
