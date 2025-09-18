# ABOUTME: Enterprise Multiple following Loughran and Wellman 2011, Table 3B
# ABOUTME: calculates enterprise value divided by operating income before depreciation
"""
Usage:
    python3 Predictors/EntMult.py

Inputs:
    - m_aCompustat.parquet: Monthly Compustat data with columns [permno, time_avail_m, dltt, dlc, dc, che, oibdp, ceq]
    - SignalMasterTable.parquet: Monthly master table with mve_c

Outputs:
    - EntMult.csv: CSV file with columns [permno, yyyymm, EntMult]
    - EntMult = (mve_c + dltt + dlc + dc - che) / oibdp, exclude if ceq < 0 or oibdp < 0
"""

import pandas as pd
import numpy as np

# DATA LOAD
df = pd.read_parquet("../pyData/Intermediate/m_aCompustat.parquet")
df = df[
    ["gvkey", "permno", "time_avail_m", "dltt", "dlc", "dc", "che", "oibdp", "ceq"]
].copy()

# Merge with SignalMasterTable
smt = pd.read_parquet("../pyData/Intermediate/SignalMasterTable.parquet")
df = df.merge(
    smt[["permno", "time_avail_m", "mve_c"]], on=["permno", "time_avail_m"], how="inner"
)

# SIGNAL CONSTRUCTION
# Calculate enterprise multiple as enterprise value divided by operating income
# Enterprise value = market value + long-term debt + debt in current liabilities + debt due in one year - cash and equivalents
# Operating income before depreciation serves as the earnings measure
df["EntMult"] = (df["mve_c"] + df["dltt"] + df["dlc"] + df["dc"] - df["che"]) / df[
    "oibdp"
]

# Apply screening filters: exclude observations with negative book equity or negative operating income
df.loc[(df["ceq"] < 0) | (df["oibdp"] < 0), "EntMult"] = np.nan

# Keep only necessary columns for output
df_final = df[["permno", "time_avail_m", "EntMult"]].copy()
df_final = df_final.dropna(subset=["EntMult"])

# Convert time_avail_m to yyyymm format like other predictors
df_final["yyyymm"] = (
    df_final["time_avail_m"].dt.year * 100 + df_final["time_avail_m"].dt.month
)

# Convert to integers for consistency with other predictors
df_final["permno"] = df_final["permno"].astype("int64")
df_final["yyyymm"] = df_final["yyyymm"].astype("int64")

# Keep only required columns and set index
df_final = df_final[["permno", "yyyymm", "EntMult"]].copy()
df_final = df_final.set_index(["permno", "yyyymm"])

# SAVE
df_final.to_csv("../pyData/Predictors/EntMult.csv")

print("EntMult predictor saved successfully")
