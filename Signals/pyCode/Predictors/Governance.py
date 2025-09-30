# ABOUTME: Governance Index following Gompers, Ishii and Metrick 2003, Table 7 Panel 1
# ABOUTME: calculates corporate governance score predictor using governance index data

"""
Governance.py

Usage:
    Run from [Repo-Root]/Signals/pyCode/
    python3 Predictors/Governance.py

Inputs:
    - SignalMasterTable.parquet: Monthly master table with columns [permno, time_avail_m, ticker, exchcd, mve_c]
    - GovIndex.parquet: Governance index data with columns [ticker, time_avail_m, G]

Outputs:
    - Governance.csv: CSV file with columns [permno, yyyymm, Governance]
"""

import pandas as pd
import numpy as np

# DATA LOAD
df = pd.read_parquet("../pyData/Intermediate/SignalMasterTable.parquet")
df = df[["permno", "time_avail_m", "ticker", "exchcd", "mve_c"]].copy()

# Split into records with and without ticker
df_no_ticker = df[df["ticker"].isna()].copy()
df_with_ticker = df[~df["ticker"].isna()].copy()

# Merge governance data for records with ticker
gov = pd.read_parquet("../pyData/Intermediate/GovIndex.parquet")
df_with_ticker = df_with_ticker.merge(gov, on=["ticker", "time_avail_m"], how="left")

# Combine back together
df = pd.concat([df_with_ticker, df_no_ticker], ignore_index=True)

# SIGNAL CONSTRUCTION
df["Governance"] = df["G"].copy()

# Apply bounds: min 5, max 14
df.loc[df["G"] <= 5, "Governance"] = 5
df.loc[(df["G"] >= 14) & (~df["G"].isna()), "Governance"] = 14

# Keep only necessary columns for output
df_final = df[["permno", "time_avail_m", "Governance"]].copy()
df_final = df_final.dropna(subset=["Governance"])

# Convert time_avail_m to yyyymm format like other predictors
df_final["yyyymm"] = (
    df_final["time_avail_m"].dt.year * 100 + df_final["time_avail_m"].dt.month
)

# Convert to integers for consistency with other predictors
df_final["permno"] = df_final["permno"].astype("int64")
df_final["yyyymm"] = df_final["yyyymm"].astype("int64")

# Keep only required columns and set index
df_final = df_final[["permno", "yyyymm", "Governance"]].copy()
df_final = df_final.set_index(["permno", "yyyymm"])

# SAVE
df_final.to_csv("../pyData/Predictors/Governance.csv")

print("Governance predictor saved successfully")
