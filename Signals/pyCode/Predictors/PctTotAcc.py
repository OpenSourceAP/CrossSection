# ABOUTME: Percent Total Accruals predictor from Hafzalla, Lundholm, Van Winkle 2011 (AR), Table 5A
# ABOUTME: Calculates net income minus cash flows from operations, financing and investment, scaled by absolute net income

"""
PctTotAcc.py

Usage:
    Run from [Repo-Root]/Signals/pyCode/
    python3 Predictors/PctTotAcc.py

Inputs:
    - m_aCompustat.parquet: Monthly Compustat data with columns [gvkey, permno, time_avail_m, ni, prstkcc, sstk, dvt, oancf, fincf, ivncf]

Outputs:
    - PctTotAcc.csv: CSV file with columns [permno, yyyymm, PctTotAcc]
"""

import pandas as pd
import numpy as np

# DATA LOAD
df = pd.read_parquet("../pyData/Intermediate/m_aCompustat.parquet")
df = df[
    [
        "gvkey",
        "permno",
        "time_avail_m",
        "ni",
        "prstkcc",
        "sstk",
        "dvt",
        "oancf",
        "fincf",
        "ivncf",
    ]
].copy()

# SIGNAL CONSTRUCTION
# Remove duplicates (deletes a few observations)
df = df.drop_duplicates(["permno", "time_avail_m"])

# Calculate PctTotAcc = (ni - (prstkcc - sstk + dvt + oancf + fincf + ivncf)) / abs(ni)
df["PctTotAcc"] = (
    df["ni"]
    - (df["prstkcc"] - df["sstk"] + df["dvt"] + df["oancf"] + df["fincf"] + df["ivncf"])
) / np.abs(df["ni"])

# Keep only necessary columns for output
df_final = df[["permno", "time_avail_m", "PctTotAcc"]].copy()
df_final = df_final.dropna(subset=["PctTotAcc"])

# Convert time_avail_m to yyyymm format like other predictors
df_final["yyyymm"] = (
    df_final["time_avail_m"].dt.year * 100 + df_final["time_avail_m"].dt.month
)

# Convert to integers for consistency with other predictors
df_final["permno"] = df_final["permno"].astype("int64")
df_final["yyyymm"] = df_final["yyyymm"].astype("int64")

# Keep only required columns and set index
df_final = df_final[["permno", "yyyymm", "PctTotAcc"]].copy()
df_final = df_final.set_index(["permno", "yyyymm"])

# SAVE
df_final.to_csv("../pyData/Predictors/PctTotAcc.csv")

print("PctTotAcc predictor saved successfully")
