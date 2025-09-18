# ABOUTME: Firm age since CRSP coverage start following Barry and Brown 1984 Table 3
# ABOUTME: calculates months since start of CRSP coverage, excluding original CRSP firms

"""
FirmAge.py

Usage:
    Run from [Repo-Root]/Signals/pyCode/
    python3 Predictors/FirmAge.py

Inputs:
    - SignalMasterTable.parquet: Monthly master table with columns [gvkey, permno, time_avail_m, exchcd]

Outputs:
    - FirmAge.csv: CSV file with columns [permno, yyyymm, FirmAge]
"""

import pandas as pd
import numpy as np

# DATA LOAD
df = pd.read_parquet("../pyData/Intermediate/SignalMasterTable.parquet")
df = df[["gvkey", "permno", "time_avail_m", "exchcd"]].copy()

# Sort for time series operations
df = df.sort_values(["permno", "time_avail_m"])

# SIGNAL CONSTRUCTION

# Calculate firm age as months since first appearance in dataset
df["FirmAge"] = df.groupby("permno").cumcount() + 1

# Calculate months since CRSP started (July 1926) to identify original CRSP firms
crsp_start = pd.Timestamp("1926-07-01")
df["tempcrsptime"] = ((df["time_avail_m"] - crsp_start).dt.days / 30.44).round().astype(
    int
) + 1

# Exclude firms that started trading when CRSP began (age = CRSP time)
df.loc[df["tempcrsptime"] == df["FirmAge"], "FirmAge"] = np.nan

# Keep only necessary columns for output
df_final = df[["permno", "time_avail_m", "FirmAge"]].copy()
df_final = df_final.dropna(subset=["FirmAge"])

# Convert time_avail_m to yyyymm format like other predictors
df_final["yyyymm"] = (
    df_final["time_avail_m"].dt.year * 100 + df_final["time_avail_m"].dt.month
)

# Convert to integers for consistency with other predictors
df_final["permno"] = df_final["permno"].astype("int64")
df_final["yyyymm"] = df_final["yyyymm"].astype("int64")

# Keep only required columns and set index
df_final = df_final[["permno", "yyyymm", "FirmAge"]].copy()
df_final = df_final.set_index(["permno", "yyyymm"])

# SAVE
df_final.to_csv("../pyData/Predictors/FirmAge.csv")

print("FirmAge predictor saved successfully")
