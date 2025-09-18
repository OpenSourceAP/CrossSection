# ABOUTME: Assets-to-market ratio following Fama and French 1992, Table 3 Ln(A/ME)
# ABOUTME: calculates total assets divided by market value of equity
"""
Usage:
    python3 Predictors/AM.py

Inputs:
    - m_aCompustat.parquet: Monthly Compustat data with columns [permno, time_avail_m, at]
    - SignalMasterTable.parquet: Monthly master table with mve_c

Outputs:
    - AM.csv: CSV file with columns [permno, yyyymm, AM]
    - AM = at/mve_c (total assets divided by market value of equity)
"""

import pandas as pd
import numpy as np

# DATA LOAD
df = pd.read_parquet("../pyData/Intermediate/m_aCompustat.parquet")
df = df[["permno", "time_avail_m", "at"]].copy()

# Drop duplicates
df = df.drop_duplicates(subset=["permno", "time_avail_m"])

# Merge with SignalMasterTable to get mve_c
smt = pd.read_parquet("../pyData/Intermediate/SignalMasterTable.parquet")
smt = smt[["permno", "time_avail_m", "mve_c"]].copy()

df = df.merge(smt, on=["permno", "time_avail_m"], how="inner")

# SIGNAL CONSTRUCTION
df["AM"] = df["at"] / df["mve_c"]

# Keep only necessary columns for output
df_final = df[["permno", "time_avail_m", "AM"]].copy()
df_final = df_final.dropna(subset=["AM"])

# Convert time_avail_m to yyyymm format like other predictors
df_final["yyyymm"] = (
    df_final["time_avail_m"].dt.year * 100 + df_final["time_avail_m"].dt.month
)

# Convert to integers for consistency with other predictors
df_final["permno"] = df_final["permno"].astype("int64")
df_final["yyyymm"] = df_final["yyyymm"].astype("int64")

# Keep only required columns and set index
df_final = df_final[["permno", "yyyymm", "AM"]].copy()
df_final = df_final.set_index(["permno", "yyyymm"])

# SAVE
df_final.to_csv("../pyData/Predictors/AM.csv")

print("AM predictor saved successfully")
