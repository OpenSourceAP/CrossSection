# ABOUTME: Calculates Net Operating Assets following Hirshleifer et al. 2004 Table 4
# ABOUTME: Run from pyCode/ directory: python3 Predictors/NOA.py

# Inputs: m_aCompustat.parquet
# Output: ../pyData/Predictors/NOA.csv

import pandas as pd
import numpy as np

print("Starting NOA calculation...")

# DATA LOAD
m_aCompustat = pd.read_parquet(
    "../pyData/Intermediate/m_aCompustat.parquet",
    columns=[
        "gvkey",
        "permno",
        "time_avail_m",
        "at",
        "che",
        "dltt",
        "mib",
        "dc",
        "ceq",
    ],
)
df = m_aCompustat.copy()
print(f"Loaded m_aCompustat data: {len(df)} observations")

# SIGNAL CONSTRUCTION
# Remove duplicate permno-month observations
df = df.drop_duplicates(subset=["permno", "time_avail_m"], keep="first")
print(f"After deduplicating by permno time_avail_m: {len(df)} observations")

# Sort by panel structure
df = df.sort_values(["permno", "time_avail_m"])

# Calculate Operating Assets (OA = total assets - cash)
df["OA"] = df["at"] - df["che"]

# Calculate Operating Liabilities (OL = total assets - long-term debt - minority interest - deferred charges - book equity)
df["OL"] = df["at"] - df["dltt"] - df["mib"] - df["dc"] - df["ceq"]

# Calculate NOA = (OA - OL) scaled by lagged total assets
df["l12_at"] = df.groupby("permno")["at"].shift(12)

# Calculate NOA
df["NOA"] = (df["OA"] - df["OL"]) / df["l12_at"]

print(f"NOA calculated for {df['NOA'].notna().sum()} observations")

# SAVE
result = df[["permno", "time_avail_m", "NOA"]].copy()
result = result.dropna(subset=["NOA"])

# Convert time_avail_m to yyyymm format
result["yyyymm"] = (
    result["time_avail_m"].dt.year * 100 + result["time_avail_m"].dt.month
)
result = result[["permno", "yyyymm", "NOA"]].copy()

# Convert to integers where appropriate
result["permno"] = result["permno"].astype(int)
result["yyyymm"] = result["yyyymm"].astype(int)

print(f"Final output: {len(result)} observations")
result.to_csv("../pyData/Predictors/NOA.csv", index=False)
print("NOA.csv saved successfully")
