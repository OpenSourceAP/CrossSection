# ABOUTME: Percent Operating Accruals predictor from Hafzalla, Lundholm, Van Winkle 2011 (AR), Table 4A
# ABOUTME: Calculates income before extraordinary items minus net cash flow, scaled by absolute income

"""
PctAcc.py

Usage:
    Run from [Repo-Root]/Signals/pyCode/
    python3 Predictors/PctAcc.py

Inputs:
    - m_aCompustat.parquet: Monthly Compustat data with columns [gvkey, permno, time_avail_m, ib, oancf, dp, act, che, lct, txp, dlc]

Outputs:
    - PctAcc.csv: CSV file with columns [permno, yyyymm, PctAcc]
"""

import pandas as pd
import numpy as np
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parents[1]))
from utils.stata_replication import fill_date_gaps, stata_multi_lag

# DATA LOAD
df = pd.read_parquet("../pyData/Intermediate/m_aCompustat.parquet")
df = df[
    [
        "gvkey",
        "permno",
        "time_avail_m",
        "ib",
        "oancf",
        "dp",
        "act",
        "che",
        "lct",
        "txp",
        "dlc",
    ]
].copy()

# Drop duplicates
df = df.drop_duplicates(subset=["permno", "time_avail_m"])

# Sort data chronologically within each company for lag calculations
df = df.sort_values(["permno", "time_avail_m"])

# SIGNAL CONSTRUCTION
# Basic percent accruals calculation
df["PctAcc"] = (df["ib"] - df["oancf"]) / np.abs(df["ib"])

# Handle case when ib == 0
df.loc[df["ib"] == 0, "PctAcc"] = (df["ib"] - df["oancf"]) / 0.01

# Calculate 12-month lagged values for balance sheet approach when cash flow data is missing
# Keep the full monthly grid until all calendar lags are calculated.
df["_observed"] = True
df = fill_date_gaps(df, "permno", "time_avail_m")
df = stata_multi_lag(df, "permno", "time_avail_m", "act", [12], fill_gaps=False)
df = stata_multi_lag(df, "permno", "time_avail_m", "che", [12], fill_gaps=False)
df = stata_multi_lag(df, "permno", "time_avail_m", "lct", [12], fill_gaps=False)
df = stata_multi_lag(df, "permno", "time_avail_m", "dlc", [12], fill_gaps=False)
df = stata_multi_lag(df, "permno", "time_avail_m", "txp", [12], fill_gaps=False)
# Preserve the source observation set before subsequent calculations.
df = df.loc[df["_observed"].eq(True)].drop(columns="_observed").copy()

# Balance sheet approach: calculate accruals from changes in working capital
alt_calc = (
    (df["act"] - df["act_lag12"])
    - (df["che"] - df["che_lag12"])
    - (
        (df["lct"] - df["lct_lag12"])
        - (df["dlc"] - df["dlc_lag12"])
        - (df["txp"] - df["txp_lag12"])
        - df["dp"]
    )
)

# Apply balance sheet method when cash flow data is unavailable
missing_oancf = df["oancf"].isna()
df.loc[missing_oancf, "PctAcc"] = alt_calc / np.abs(df["ib"])

# Special case: missing cash flow data and zero income
missing_oancf_zero_ib = missing_oancf & (df["ib"] == 0)
df.loc[missing_oancf_zero_ib, "PctAcc"] = alt_calc / 0.01

# Keep only necessary columns for output
df_final = df[["permno", "time_avail_m", "PctAcc"]].copy()
df_final = df_final.dropna(subset=["PctAcc"])

# Convert time_avail_m to yyyymm format like other predictors
df_final["yyyymm"] = (
    df_final["time_avail_m"].dt.year * 100 + df_final["time_avail_m"].dt.month
)

# Convert to integers for consistency with other predictors
df_final["permno"] = df_final["permno"].astype("int64")
df_final["yyyymm"] = df_final["yyyymm"].astype("int64")

# Keep only required columns and set index
df_final = df_final[["permno", "yyyymm", "PctAcc"]].copy()
df_final = df_final.set_index(["permno", "yyyymm"])

# SAVE
df_final.to_csv("../pyData/Predictors/PctAcc.csv")

print("PctAcc predictor saved successfully")
