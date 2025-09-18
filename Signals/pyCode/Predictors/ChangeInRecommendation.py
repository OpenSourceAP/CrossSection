# ABOUTME: Change in recommendation following Jegadeesh et al. 2004, Table 3C
# ABOUTME: calculates change in analyst recommendation score from previous month

"""
ChangeInRecommendation.py

Usage:
    Run from [Repo-Root]/Signals/pyCode/
    python3 Predictors/ChangeInRecommendation.py

Inputs:
    - IBES_Recommendations.parquet: IBES analyst recommendations with columns [tickerIBES, amaskcd, anndats, time_avail_m, ireccd]
    - SignalMasterTable.parquet: Monthly master table with permno identifiers

Outputs:
    - ChangeInRecommendation.csv: CSV file with columns [permno, yyyymm, ChangeInRecommendation]
"""

import pandas as pd
import numpy as np

# Load IBES recommendations data
df = pd.read_parquet(
    "../pyData/Intermediate/IBES_Recommendations.parquet",
    columns=["tickerIBES", "amaskcd", "anndats", "time_avail_m", "ireccd"],
)


# Aggregate recommendations to firm-month level
# First: get the last non-missing recommendation for each analyst-firm-month
def last_non_missing(series):
    non_missing = series.dropna()
    return non_missing.iloc[-1] if len(non_missing) > 0 else np.nan


df = (
    df.groupby(["tickerIBES", "amaskcd", "time_avail_m"])["ireccd"]
    .apply(last_non_missing)
    .reset_index()
)

# Then: take the mean recommendation across all analysts for each firm-month
df = df.groupby(["tickerIBES", "time_avail_m"], as_index=False)["ireccd"].mean()

# Reverse the recommendation score so higher values indicate better recommendations
df["opscore"] = 6 - df["ireccd"]

# Sort for lag operation
df = df.sort_values(["tickerIBES", "time_avail_m"])

# Calculate change in recommendation from previous month
df["opscore_lag"] = df.groupby("tickerIBES")["opscore"].shift(1)
df["ChangeInRecommendation"] = np.where(
    df["opscore_lag"].notna(), df["opscore"] - df["opscore_lag"], np.nan
)

# Add permno identifiers by merging with SignalMasterTable
signal_master = pd.read_parquet(
    "../pyData/Intermediate/SignalMasterTable.parquet",
    columns=["permno", "tickerIBES", "time_avail_m"],
)

# Join with master table to get permno, keeping only matched records
df = df.merge(signal_master, on=["tickerIBES", "time_avail_m"], how="inner")

# Keep only observations with valid recommendation changes
df = df.dropna(subset=["ChangeInRecommendation"])

# Keep only required columns for final output
result = df[["permno", "time_avail_m", "ChangeInRecommendation"]].copy()

# Convert time_avail_m to yyyymm format
result["yyyymm"] = (
    result["time_avail_m"].dt.year * 100 + result["time_avail_m"].dt.month
)

# Select final output columns
result = result[["permno", "yyyymm", "ChangeInRecommendation"]]

# Convert permno and yyyymm to int
result["permno"] = result["permno"].astype(int)
result["yyyymm"] = result["yyyymm"].astype(int)

# SAVE
result.to_csv("../pyData/Predictors/ChangeInRecommendation.csv", index=False)

print(f"ChangeInRecommendation predictor created with {len(result)} observations")
