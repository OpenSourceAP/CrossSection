# ABOUTME: Cash-flow to price variance following Haugen and Baker 1996, Table 1 variability in cf to price
# ABOUTME: Rolling variance of (ib+dp)/mve_c over the past 60 months (minimum 24 months data required)

"""
VarCF.py

Usage:
    Run from [Repo-Root]/Signals/pyCode/
    python3 Predictors/VarCF.py

Inputs:
    - SignalMasterTable.parquet: Monthly master table with columns [permno, time_avail_m, mve_c]
    - m_aCompustat.parquet: Monthly Compustat data with columns [permno, time_avail_m, ib, dp]

Outputs:
    - VarCF.csv: CSV file with columns [permno, yyyymm, VarCF]
"""

import pandas as pd
import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
from utils.asrol import asrol

# Read SignalMasterTable
smt = pd.read_parquet("../pyData/Intermediate/SignalMasterTable.parquet")
df = smt[["permno", "time_avail_m", "mve_c"]].copy()

# Merge with m_aCompustat data (left join to keep all SignalMasterTable observations)
compustat = pd.read_parquet("../pyData/Intermediate/m_aCompustat.parquet")
compustat = compustat[["permno", "time_avail_m", "ib", "dp"]].copy()
df = df.merge(compustat, on=["permno", "time_avail_m"], how="left")

# Sort for rolling operations
df = df.sort_values(["permno", "time_avail_m"])

# SIGNAL CONSTRUCTION
# Calculate cash flow to price ratio
df["tempCF"] = (df["ib"] + df["dp"]) / df["mve_c"]

# Calculate rolling standard deviation using asrol (60-month window, min 24 periods)
print(f"Calculating rolling statistics for {df['permno'].nunique()} firms...")

# Sort data for rolling operations
df = df.sort_values(["permno", "time_avail_m"])

# Use asrol for 60-month rolling standard deviation with minimum 24 periods
df = asrol(
    df, "permno", "time_avail_m", "1mo", 60, "tempCF", "std", "sigma", min_samples=24
)

print("Rolling statistics calculation completed")

# Calculate variance from standard deviation
df["VarCF"] = df["sigma"] ** 2

# Keep only necessary columns for output
df_final = df[["permno", "time_avail_m", "VarCF"]].copy()
df_final = df_final.dropna(subset=["VarCF"])

# Convert time_avail_m to yyyymm format like other predictors
df_final["yyyymm"] = (
    df_final["time_avail_m"].dt.year * 100 + df_final["time_avail_m"].dt.month
)

# Convert to integers for consistency with other predictors
df_final["permno"] = df_final["permno"].astype("int64")
df_final["yyyymm"] = df_final["yyyymm"].astype("int64")

# Keep only required columns and set index
df_final = df_final[["permno", "yyyymm", "VarCF"]].copy()
df_final = df_final.set_index(["permno", "yyyymm"])

# SAVE
df_final.to_csv("../pyData/Predictors/VarCF.csv")

print("VarCF predictor saved successfully")
