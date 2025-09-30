# ABOUTME: Predicted dividend yield following Litzenberger and Ramaswamy 1979, Table 1
# ABOUTME: calculates predicted dividend yield based on frequency-specific lag structure

"""
DivYieldST.py

Usage:
    Run from [Repo-Root]/Signals/pyCode/
    python3 Predictors/DivYieldST.py

Inputs:
    - CRSPdistributions.parquet: CRSP distributions with columns [permno, cd1, cd2, cd3, divamt, exdt]
    - SignalMasterTable.parquet: Monthly master table with [permno, time_avail_m, prc]
    - monthlyCRSP.parquet: Monthly CRSP data with [permno, time_avail_m, ret, retx]

Outputs:
    - DivYieldST.csv: CSV file with columns [permno, yyyymm, DivYieldST]
"""

import pandas as pd
import numpy as np
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# PREP DISTRIBUTIONS DATA
dist_df = pd.read_parquet("../pyData/Intermediate/CRSPdistributions.parquet")
dist_df = dist_df[["permno", "cd1", "cd2", "cd3", "divamt", "exdt"]].copy()

# Keep dividend distributions only
dist_df = dist_df[(dist_df["cd1"] == 1) & (dist_df["cd2"] == 2)]

# Keep quarterly, semi-annual, and annual distributions
dist_df = dist_df[dist_df["cd3"].isin([3, 4, 5])]

# Convert ex-dividend dates to monthly timestamps
# * (p5 says exdt is used)
dist_df["exdt"] = pd.to_datetime(dist_df["exdt"])
dist_df["time_avail_m"] = dist_df["exdt"].dt.to_period("M").dt.to_timestamp()
dist_df = dist_df.dropna(subset=["time_avail_m", "divamt"])

# Sum dividend amounts by firm, frequency, and month
tempdivamt = (
    dist_df.groupby(["permno", "cd3", "time_avail_m"])["divamt"].sum().reset_index()
)

# For firms with multiple frequencies in same month, prioritize quarterly
tempdivamt = tempdivamt.sort_values(["permno", "time_avail_m", "cd3"])
tempdivamt = tempdivamt.groupby(["permno", "time_avail_m"]).first().reset_index()

# DATA LOAD
df = pd.read_parquet("../pyData/Intermediate/SignalMasterTable.parquet")
df = df[["permno", "time_avail_m", "prc"]].copy()

# Merge with dividend data
df = df.merge(
    tempdivamt[["permno", "time_avail_m", "cd3", "divamt"]],
    on=["permno", "time_avail_m"],
    how="left",
)

# Merge with monthly CRSP data
monthly_crsp = pd.read_parquet("../pyData/Intermediate/monthlyCRSP.parquet")
df = df.merge(
    monthly_crsp[["permno", "time_avail_m", "ret", "retx"]],
    on=["permno", "time_avail_m"],
    how="left",
)

# Sort for lagged operations
df = df.sort_values(["permno", "time_avail_m"])

# Forward-fill dividend frequency codes
df["cd3"] = df.groupby("permno")["cd3"].ffill()

# Set missing dividend amounts to zero
df["divamt"] = df["divamt"].fillna(0)

# Keep only firms that paid dividends in past 12 months
df["div12"] = (
    df.groupby("permno")["divamt"]
    .rolling(window=12, min_periods=1)
    .sum()
    .reset_index(0, drop=True)
)
df = df[(df["div12"] > 0) & df["div12"].notna()]

# Calculate expected dividends based on frequency-specific lags
df["Ediv1"] = np.nan

# Quarterly or unknown frequency: use 2-month lag
mask_quarterly = df["cd3"].isin([3, 0, 1]) | df["cd3"].isna()
df.loc[mask_quarterly, "Ediv1"] = df.groupby("permno")["divamt"].shift(2)

# Semi-annual frequency: use 5-month lag
mask_semiann = df["cd3"] == 4
df.loc[mask_semiann, "Ediv1"] = df.groupby("permno")["divamt"].shift(5)

# Annual frequency: use 11-month lag
mask_annual = df["cd3"] == 5
df.loc[mask_annual, "Ediv1"] = df.groupby("permno")["divamt"].shift(11)

# Calculate expected dividend yield
df["Edy1"] = df["Ediv1"] / abs(df["prc"])

# * this is super janky, but we try to imitate their regression with ports.
# * the key is you need to separate the big mass of stocks with Edy1 = 0.
# * more than 50% of stocks lie in this region.

# Extract positive dividend yields only
df["Edy1pos"] = df["Edy1"].where(df["Edy1"] > 0)

# Rank positive dividend yields into terciles by month
df["DivYieldST"] = df.groupby("time_avail_m")["Edy1pos"].transform(
    lambda x: pd.qcut(x, q=3, labels=False, duplicates="drop") + 1
)

# Assign zero yield to bottom tercile
df.loc[df["Edy1"] == 0, "DivYieldST"] = 0

# Prepare final output
df_final = df[["permno", "time_avail_m", "DivYieldST"]].copy()
df_final = df_final.dropna(subset=["DivYieldST"])

# Convert time_avail_m to yyyymm format
df_final["yyyymm"] = (
    df_final["time_avail_m"].dt.year * 100 + df_final["time_avail_m"].dt.month
)

# Convert to integers for consistency with other predictors
df_final["permno"] = df_final["permno"].astype("int64")
df_final["yyyymm"] = df_final["yyyymm"].astype("int64")

# Keep only required columns and set index
df_final = df_final[["permno", "yyyymm", "DivYieldST"]].copy()
df_final = df_final.set_index(["permno", "yyyymm"])

# SAVE
df_final.to_csv("../pyData/Predictors/DivYieldST.csv")

print("DivYieldST predictor saved successfully")
