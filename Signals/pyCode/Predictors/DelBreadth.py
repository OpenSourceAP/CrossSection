# ABOUTME: Change in breadth of ownership following Chen, Hong and Stein 2002, Table 4A
# ABOUTME: calculates quarterly change in number of institutional owners from 13F data

"""
DelBreadth.py

Usage:
    Run from [Repo-Root]/Signals/pyCode/
    python3 Predictors/DelBreadth.py

Inputs:
    - SignalMasterTable.parquet: Monthly master table with columns [permno, time_avail_m, exchcd, mve_c]
    - TR_13F.parquet: 13F data with columns [permno, time_avail_m, dbreadth]

Outputs:
    - DelBreadth.csv: CSV file with columns [permno, yyyymm, DelBreadth]
"""

import pandas as pd
import numpy as np

# DATA LOAD
df = pd.read_parquet("../pyData/Intermediate/SignalMasterTable.parquet")
df = df[["permno", "time_avail_m", "exchcd", "mve_c"]].copy()

# Merge with TR_13F data
tr_13f = pd.read_parquet("../pyData/Intermediate/TR_13F.parquet")
tr_13f = tr_13f[["permno", "time_avail_m", "dbreadth"]].copy()

df = df.merge(tr_13f, on=["permno", "time_avail_m"], how="left")

# SIGNAL CONSTRUCTION
df["DelBreadth"] = df["dbreadth"]

# Create temporary data to calculate 20th percentile of mve_c for NYSE stocks
# Keep if exchcd == 1 (NYSE stocks only)
nyse_df = df[df["exchcd"] == 1].copy()

# Calculate 20th percentile of mve_c by time_avail_m for NYSE stocks
percentile_20 = nyse_df.groupby("time_avail_m")["mve_c"].quantile(0.20).reset_index()
percentile_20.columns = ["time_avail_m", "temp"]

# Merge back with full dataset
df = df.merge(percentile_20, on="time_avail_m", how="left")

# Replace DelBreadth with missing if mve_c < temp (20th percentile cutoff)
df.loc[df["mve_c"] < df["temp"], "DelBreadth"] = np.nan

# Clean up
df = df.drop(columns=["temp"])

# Keep only necessary columns for output
df_final = df[["permno", "time_avail_m", "DelBreadth"]].copy()
df_final = df_final.dropna(subset=["DelBreadth"])

# Convert time_avail_m to yyyymm format like other predictors
df_final["yyyymm"] = (
    df_final["time_avail_m"].dt.year * 100 + df_final["time_avail_m"].dt.month
)

# Convert to integers for consistency with other predictors
df_final["permno"] = df_final["permno"].astype("int64")
df_final["yyyymm"] = df_final["yyyymm"].astype("int64")

# Keep only required columns and set index
df_final = df_final[["permno", "yyyymm", "DelBreadth"]].copy()
df_final = df_final.set_index(["permno", "yyyymm"])

# SAVE
df_final.to_csv("../pyData/Predictors/DelBreadth.csv")

print("DelBreadth predictor saved successfully")
