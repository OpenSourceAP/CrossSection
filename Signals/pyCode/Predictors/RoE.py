# ABOUTME: Return on Equity following Haugen and Baker 1996, Table 1, return on equity
# ABOUTME: calculates net income (ni) divided by book value of equity (ceq)
"""
Usage:
    python3 Predictors/RoE.py

Inputs:
    - ../pyData/Intermediate/m_aCompustat.parquet: Monthly Compustat data with columns [permno, time_avail_m, ni, ceq]

Outputs:
    - RoE.csv: CSV file with columns [permno, yyyymm, RoE]
    - RoE = ni/ceq, following Haugen and Baker 1996 definition
"""

import pandas as pd

# DATA LOAD
df = pd.read_parquet(
    "../pyData/Intermediate/m_aCompustat.parquet",
    columns=["gvkey", "permno", "time_avail_m", "ni", "ceq"],
)

# SIGNAL CONSTRUCTION
# Remove duplicates by permno and time_avail_m (keep first)
df = df.groupby(["permno", "time_avail_m"]).first().reset_index()

# Calculate RoE
df["RoE"] = df["ni"] / df["ceq"]

# Drop missing values
df = df.dropna(subset=["RoE"])

# Convert time_avail_m to yyyymm
df["yyyymm"] = df["time_avail_m"].dt.year * 100 + df["time_avail_m"].dt.month

# Keep required columns and order
df = df[["permno", "yyyymm", "RoE"]].copy()

# SAVE
df.to_csv("../pyData/Predictors/RoE.csv", index=False)
print(f"RoE: Saved {len(df):,} observations")
