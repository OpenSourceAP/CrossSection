# ABOUTME: Total accruals following Richardson et al. 2005, Table 8A TACC
# ABOUTME: calculates total accruals using balance sheet method (before 1988) or cash flow method (1988+)
"""
Usage:
    python3 Predictors/TotalAccruals.py

Inputs:
    - m_aCompustat.parquet: Monthly Compustat data with columns [permno, time_avail_m, ivao, ivst, dltt, dlc, pstk, sstk, prstkc, dv, act, che, lct, at, lt, ni, oancf, ivncf, fincf]

Outputs:
    - TotalAccruals.csv: CSV file with columns [permno, yyyymm, TotalAccruals]
    - TotalAccruals = Before 1988: change in working capital + change in non-current assets + change in financial assets, scaled by lagged assets
    - TotalAccruals = 1988+: net income minus cash flows plus equity financing activities, scaled by lagged assets
"""

import pandas as pd
import numpy as np

# DATA LOAD
df = pd.read_parquet("../pyData/Intermediate/m_aCompustat.parquet")
df = df[
    [
        "permno",
        "time_avail_m",
        "ivao",
        "ivst",
        "dltt",
        "dlc",
        "pstk",
        "sstk",
        "prstkc",
        "dv",
        "act",
        "che",
        "lct",
        "at",
        "lt",
        "ni",
        "oancf",
        "ivncf",
        "fincf",
    ]
].copy()

# Drop duplicates
df = df.drop_duplicates(subset=["permno", "time_avail_m"])

# Sort for lag operations
df = df.sort_values(["permno", "time_avail_m"])

# SIGNAL CONSTRUCTION
# Create temporary variables with missing values set to 0
temp_vars = ["ivao", "ivst", "dltt", "dlc", "pstk", "sstk", "prstkc", "dv"]
for v in temp_vars:
    df[f"temp{v}"] = df[v].fillna(0)

# Calculate working capital, non-current, and financial components
df["tempWc"] = (df["act"] - df["che"]) - (df["lct"] - df["tempdlc"])
df["tempNc"] = (df["at"] - df["act"] - df["tempivao"]) - (
    df["lt"] - df["tempdlc"] - df["tempdltt"]
)
df["tempFi"] = (df["tempivst"] + df["tempivao"]) - (
    df["tempdltt"] + df["tempdlc"] + df["temppstk"]
)

# Calculate 12-month lags
df["tempWc_lag12"] = df.groupby("permno")["tempWc"].shift(12)
df["tempNc_lag12"] = df.groupby("permno")["tempNc"].shift(12)
df["tempFi_lag12"] = df.groupby("permno")["tempFi"].shift(12)
df["at_lag12"] = df.groupby("permno")["at"].shift(12)

# Extract year
df["year"] = df["time_avail_m"].dt.year

# Calculate TotalAccruals based on year
df["TotalAccruals"] = np.nan

# For years <= 1989, use balance sheet method
early_years = df["year"] <= 1989
df.loc[early_years, "TotalAccruals"] = (
    (df["tempWc"] - df["tempWc_lag12"])
    + (df["tempNc"] - df["tempNc_lag12"])
    + (df["tempFi"] - df["tempFi_lag12"])
)

# For years > 1989, use cash flow method
late_years = df["year"] > 1989
df.loc[late_years, "TotalAccruals"] = (
    df["ni"]
    - (df["oancf"] + df["ivncf"] + df["fincf"])
    + (df["sstk"] - df["prstkc"] - df["dv"])
)

# Scale by lagged assets
df["TotalAccruals"] = df["TotalAccruals"] / df["at_lag12"]

# Keep only necessary columns for output
df_final = df[["permno", "time_avail_m", "TotalAccruals"]].copy()
df_final = df_final.dropna(subset=["TotalAccruals"])

# Convert time_avail_m to yyyymm format like other predictors
df_final["yyyymm"] = (
    df_final["time_avail_m"].dt.year * 100 + df_final["time_avail_m"].dt.month
)

# Convert to integers for consistency with other predictors
df_final["permno"] = df_final["permno"].astype("int64")
df_final["yyyymm"] = df_final["yyyymm"].astype("int64")

# Keep only required columns and set index
df_final = df_final[["permno", "yyyymm", "TotalAccruals"]].copy()
df_final = df_final.set_index(["permno", "yyyymm"])

# SAVE
df_final.to_csv("../pyData/Predictors/TotalAccruals.csv")

print("TotalAccruals predictor saved successfully")
