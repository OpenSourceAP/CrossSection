# ABOUTME: Calculates industry-adjusted real estate holdings following Tuzel 2010 Table 5
# ABOUTME: Run from pyCode/ directory: python3 Predictors/realestate.py

# Inputs: m_aCompustat.parquet, SignalMasterTable.parquet
# Output: ../pyData/Predictors/realestate.csv

import pandas as pd
import numpy as np

# DATA LOAD
df = pd.read_parquet("../pyData/Intermediate/m_aCompustat.parquet")
df = df[
    [
        "permno",
        "time_avail_m",
        "ppenb",
        "ppenls",
        "fatb",
        "fatl",
        "ppegt",
        "ppent",
        "at",
    ]
].copy()

# Merge with SignalMasterTable
smt = pd.read_parquet("../pyData/Intermediate/SignalMasterTable.parquet")
df = df.merge(
    smt[["permno", "time_avail_m", "sicCRSP"]],
    on=["permno", "time_avail_m"],
    how="inner",
)

# Sample selection
df["sicCRSP"] = df["sicCRSP"].astype(str)
df["sic2D"] = df["sicCRSP"].str[:2]

# Count observations by industry-time and keep only industries with >= 5 observations
df["tempN"] = df.groupby(["sic2D", "time_avail_m"])["at"].transform("count")
df = df[df["tempN"] >= 5].copy()

# Drop observations with missing key variables
df = df.dropna(subset=["at"])
df = df[(df["ppent"].notna()) | (df["ppegt"].notna())].copy()

# SIGNAL CONSTRUCTION
# Calculate real estate ratios using old and new methods
df["re_old"] = (df["ppenb"] + df["ppenls"]) / df["ppent"]
df["re_new"] = (df["fatb"] + df["fatl"]) / df["ppegt"]


# Use new method, fallback to old method if new is missing
df["re"] = df["re_new"]
df.loc[df["re_new"].isna(), "re"] = df["re_old"]

# Convert infinite values to NaN (division by zero)
df["re"] = df["re"].replace([np.inf, -np.inf], np.nan)


# Extract year and decade
df["year"] = df["time_avail_m"].dt.year
df["decade"] = (df["year"] // 10) * 10

# Industry adjustment - subtract industry mean
df["tempMean"] = df.groupby(["sic2D", "time_avail_m"])["re"].transform("mean")


df["realestate"] = df["re"] - df["tempMean"]


# Keep only necessary columns for output
df_final = df[["permno", "time_avail_m", "realestate"]].copy()
df_final = df_final.dropna(subset=["realestate"])

# Convert time_avail_m to yyyymm format like other predictors
df_final["yyyymm"] = (
    df_final["time_avail_m"].dt.year * 100 + df_final["time_avail_m"].dt.month
)

# Convert to integers for consistency with other predictors
df_final["permno"] = df_final["permno"].astype("int64")
df_final["yyyymm"] = df_final["yyyymm"].astype("int64")

# Keep only required columns and set index
df_final = df_final[["permno", "yyyymm", "realestate"]].copy()
df_final = df_final.set_index(["permno", "yyyymm"])

# SAVE
df_final.to_csv("../pyData/Predictors/realestate.csv")

print("realestate predictor saved successfully")
