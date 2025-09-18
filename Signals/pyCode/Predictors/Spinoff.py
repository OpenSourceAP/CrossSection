# ABOUTME: Spinoff following Cusatis, Miles and Woolridge 1993, Table 3B I-24
# ABOUTME: Creates spinoff indicator predictor for firms identified in CRSP acquisition data

# Run from pyCode/ directory
# Inputs: SignalMasterTable.parquet, m_CRSPAcquisitions.parquet
# Output: ../pyData/Predictors/Spinoff.csv

import pandas as pd
import numpy as np

# DATA LOAD
df = pd.read_parquet("../pyData/Intermediate/SignalMasterTable.parquet")
df = df[["permno", "time_avail_m"]].copy()

acquisitions = pd.read_parquet("../pyData/Intermediate/m_CRSPAcquisitions.parquet")
df = df.merge(acquisitions, on="permno", how="left")

# SIGNAL CONSTRUCTION
# Create firm age (number of observations for each permno)
df = df.sort_values(["permno", "time_avail_m"])
df["FirmAgeNoScreen"] = df.groupby("permno").cumcount() + 1

# Create Spinoff signal: 1 if SpinoffCo == 1 & FirmAgeNoScreen <= 24
df["Spinoff"] = np.where((df["SpinoffCo"] == 1) & (df["FirmAgeNoScreen"] <= 24), 1, 0)

# Keep only necessary columns for output
df_final = df[["permno", "time_avail_m", "Spinoff"]].copy()
df_final = df_final.dropna(subset=["Spinoff"])

# Convert time_avail_m to yyyymm format like other predictors
df_final["yyyymm"] = (
    df_final["time_avail_m"].dt.year * 100 + df_final["time_avail_m"].dt.month
)

# Convert to integers for consistency with other predictors
df_final["permno"] = df_final["permno"].astype("int64")
df_final["yyyymm"] = df_final["yyyymm"].astype("int64")
df_final["Spinoff"] = df_final["Spinoff"].astype("int64")

# Keep only required columns and set index
df_final = df_final[["permno", "yyyymm", "Spinoff"]].copy()
df_final = df_final.set_index(["permno", "yyyymm"])

# SAVE
df_final.to_csv("../pyData/Predictors/Spinoff.csv")

print("Spinoff predictor saved successfully")
