# ABOUTME: Amihud's illiquidity following Amihud 2002, Table 2
# ABOUTME: calculates past twelve month average of daily return divided by turnover

"""
Illiquidity.py

Usage:
    Run from [Repo-Root]/Signals/pyCode/
    python3 Predictors/Illiquidity.py

Inputs:
    - dailyCRSP.parquet: Daily CRSP data with columns [permno, time_d, ret, prc, vol]

Outputs:
    - Illiquidity.csv: CSV file with columns [permno, yyyymm, Illiquidity]
"""

import pandas as pd
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parents[1]))
from utils.stata_replication import stata_multi_lag
import numpy as np

# DATA LOAD
print("Loading dailyCRSP data...")
df = pd.read_parquet("../pyData/Intermediate/dailyCRSP.parquet")

# SIGNAL CONSTRUCTION
print("Constructing Illiquidity signal...")

# Convert time_d to monthly time_avail_m (year * 100 + month format)
df["time_avail_m"] = df["time_d"].dt.to_period("M").dt.start_time

# Calculate daily illiquidity measure
df["ill"] = np.abs(df["ret"]) / (np.abs(df["prc"]) * df["vol"])

# Handle division by zero and inf values
df["ill"] = df["ill"].replace([np.inf, -np.inf], np.nan)

# Monthly average of daily illiquidity
monthly_ill = df.groupby(["permno", "time_avail_m"])["ill"].mean().reset_index()

# Sort for lag operations
monthly_ill = monthly_ill.sort_values(["permno", "time_avail_m"])

# Calculate 12-month rolling mean using lags
monthly_ill["_observed"] = True
monthly_ill = stata_multi_lag(monthly_ill, "permno", "time_avail_m", "ill", list(range(1, 12)))
monthly_ill = monthly_ill.loc[monthly_ill["_observed"].eq(True)].drop(columns="_observed")

# Calculate 12-month rolling mean
# Require ALL 12 values to be non-missing for the calculation
# If any value is missing, the result is missing
illiquidity_cols = [
    "ill",
    "ill_lag1",
    "ill_lag2",
    "ill_lag3",
    "ill_lag4",
    "ill_lag5",
    "ill_lag6",
    "ill_lag7",
    "ill_lag8",
    "ill_lag9",
    "ill_lag10",
    "ill_lag11",
]

# Count non-missing values for each observation
monthly_ill["non_missing_count"] = monthly_ill[illiquidity_cols].count(axis=1)

# Calculate mean, but only if ALL 12 values are present (matching Stata's behavior)
monthly_ill["Illiquidity"] = np.where(
    monthly_ill["non_missing_count"] == 12,
    monthly_ill[illiquidity_cols].mean(axis=1),
    np.nan,
)

# Prepare final output - rename time_avail_m to yyyymm for consistency
result = monthly_ill[["permno", "time_avail_m", "Illiquidity"]].copy()
result["yyyymm"] = result["time_avail_m"].dt.year * 100 + result["time_avail_m"].dt.month
result = result[["permno", "yyyymm", "Illiquidity"]]

# Drop rows with missing Illiquidity values
result = result.dropna(subset=["Illiquidity"])

print(f"Final dataset shape: {result.shape}")
print("Sample of final data:")
print(result.head())

# SAVE
result.to_csv("../pyData/Predictors/Illiquidity.csv", index=False)
print("Saved to ../pyData/Predictors/Illiquidity.csv")
