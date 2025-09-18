# ABOUTME: Net external financing following Bradshaw, Richardson, Sloan 2006, Table 3
# ABOUTME: calculates net external financing predictor scaled by total assets

# Run from pyCode/ directory
# Inputs: m_aCompustat.parquet
# Output: ../pyData/Predictors/XFIN.csv

import pandas as pd
import numpy as np

# DATA LOAD
df = pd.read_parquet("../pyData/Intermediate/m_aCompustat.parquet")
df = df[
    [
        "gvkey",
        "permno",
        "time_avail_m",
        "sstk",
        "dv",
        "prstkc",
        "dltis",
        "dltr",
        "dlcch",
        "at",
    ]
].copy()

# SIGNAL CONSTRUCTION
# Remove duplicates (deletes a few observations)
df = df.drop_duplicates(["permno", "time_avail_m"])

# Replace missing dlcch with 0
df["dlcch"] = df["dlcch"].fillna(0)

# Calculate XFIN = (sstk - dv - prstkc + dltis - dltr + dlcch)/at
df["XFIN"] = (
    df["sstk"] - df["dv"] - df["prstkc"] + df["dltis"] - df["dltr"] + df["dlcch"]
) / df["at"]

# Keep only necessary columns for output
df_final = df[["permno", "time_avail_m", "XFIN"]].copy()
df_final = df_final.dropna(subset=["XFIN"])

# Convert time_avail_m to yyyymm format like other predictors
df_final["yyyymm"] = (
    df_final["time_avail_m"].dt.year * 100 + df_final["time_avail_m"].dt.month
)

# Convert to integers for consistency with other predictors
df_final["permno"] = df_final["permno"].astype("int64")
df_final["yyyymm"] = df_final["yyyymm"].astype("int64")

# Keep only required columns and set index
df_final = df_final[["permno", "yyyymm", "XFIN"]].copy()
df_final = df_final.set_index(["permno", "yyyymm"])

# SAVE
df_final.to_csv("../pyData/Predictors/XFIN.csv")

print("XFIN predictor saved successfully")
