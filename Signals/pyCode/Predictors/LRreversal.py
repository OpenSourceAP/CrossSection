# ABOUTME: Long-run reversal following De Bondt and Thaler 1985, Table 1, three-year
# ABOUTME: calculates stock return between months t-36 and t-13 for long-term reversal signal

"""
LRreversal.py

Usage:
    Run from [Repo-Root]/Signals/pyCode/
    python3 Predictors/LRreversal.py

Inputs:
    - SignalMasterTable.parquet: Monthly master table with columns [permno, time_avail_m, ret]

Outputs:
    - LRreversal.csv: CSV file with columns [permno, yyyymm, LRreversal]
"""

import pandas as pd
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parents[1]))
from utils.stata_replication import stata_multi_lag
import numpy as np

# DATA LOAD
df = pd.read_parquet("../pyData/Intermediate/SignalMasterTable.parquet")
df = df[["permno", "time_avail_m", "ret"]].copy()

# Sort for lag operations
df = df.sort_values(["permno", "time_avail_m"])

# SIGNAL CONSTRUCTION
# Replace missing returns with 0 for momentum calculations
df["ret"] = df["ret"].fillna(0)

# Create 24 monthly lags (t-13 to t-36) for long-term reversal calculation
df["_observed"] = True
df = stata_multi_lag(df, "permno", "time_avail_m", "ret", list(range(13, 37)))
df = df.loc[df["_observed"].eq(True)].drop(columns="_observed")
lag_cols = [f"ret_lag{i}" for i in range(13, 37)]

# Compounds monthly returns over months t-36 to t-13 to create long-term reversal signal
product = df[lag_cols[0]] * 0 + 1  # Initialize to 1
for col in lag_cols:
    product = product * (1 + df[col])

df["LRreversal"] = product - 1

# Keep only necessary columns for output
df_final = df[["permno", "time_avail_m", "LRreversal"]].copy()
df_final = df_final.dropna(subset=["LRreversal"])

# Convert time_avail_m to yyyymm format like other predictors
df_final["yyyymm"] = (
    df_final["time_avail_m"].dt.year * 100 + df_final["time_avail_m"].dt.month
)

# Convert to integers for consistency with other predictors
df_final["permno"] = df_final["permno"].astype("int64")
df_final["yyyymm"] = df_final["yyyymm"].astype("int64")

# Keep only required columns and set index
df_final = df_final[["permno", "yyyymm", "LRreversal"]].copy()
df_final = df_final.set_index(["permno", "yyyymm"])

# SAVE
df_final.to_csv("../pyData/Predictors/LRreversal.csv")

print("LRreversal predictor saved successfully")
