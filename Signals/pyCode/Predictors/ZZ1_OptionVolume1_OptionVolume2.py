# ABOUTME: Option trading volume predictors following Johnson and So 2012 JFE, Table 2A
# ABOUTME: OptionVolume1 = option to stock volume ratio, OptionVolume2 = abnormal option volume (current/6-month average)

"""
Usage:
    python3 Predictors/ZZ1_OptionVolume1_OptionVolume2.py

Inputs:
    - pyData/Intermediate/SignalMasterTable.parquet
    - pyData/Intermediate/monthlyCRSP.parquet
    - pyData/Prep/OptionMetricsVolume.csv

Outputs:
    - pyData/Predictors/OptionVolume1.csv - Option to stock volume ratio
    - pyData/Predictors/OptionVolume2.csv - Abnormal option volume (current/6-month average)

Note:
    - ac 2025-09: updated to exclude mechanical trading volume associated with traders rolling forward to the next expiration date. we still use monthly signals, so we don't have t-stats as large as in Table 2A. But mean returns are mostly monotonic in the signals.
"""

# --------------
# Johnson and So 2012 JFE
print("Starting ZZ1_OptionVolume1_OptionVolume2.py...")

# DATA LOAD
print("Loading data...")
import pandas as pd
import numpy as np
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils.save_standardized import save_predictor

print("Started ZZ1_OptionVolume1_OptionVolume2.py...")

# Load required columns from SignalMasterTable
df = pd.read_parquet(
    "../pyData/Intermediate/SignalMasterTable.parquet",
    columns=["permno", "time_avail_m", "secid", "prc", "shrcd"],
)

# Merge with monthly CRSP data to get stock volume
crsp = pd.read_parquet(
    "../pyData/Intermediate/monthlyCRSP.parquet",
    columns=["permno", "time_avail_m", "vol"],
)
df = df.merge(crsp, on=["permno", "time_avail_m"], how="left")

# Load daily option volume
optvold = pd.read_csv(
    "../pyData/Prep/OptionMetricsVolume.csv",
    usecols=["secid", "date", "optvolume_js12"],
).rename(columns={"optvolume_js12": "optvolume_js12"})

# aggregate option volume to monthly
# OP aggregates to weekly (Table 2, also page 7). But for simplicity we aggregate to monthly
# time to expiration filters were already applied in PrepScripts/OptionMetricsVolume.R
optvold["time_avail_m"] = (
    pd.to_datetime(optvold["date"]).dt.to_period("M").dt.start_time
)
optvolm = (
    optvold.groupby(["secid", "time_avail_m"])["optvolume_js12"].sum().reset_index()
)

# merge option volume to df
df = df.merge(optvolm, on=["secid", "time_avail_m"], how="left")

# SIGNAL CONSTRUCTION

# Calculate OptionVolume1 as ratio of option volume to stock volume
df["OptionVolume1"] = df["optvolume_js12"] / df["vol"]

# Set OptionVolume1 to missing if prior period option or stock volume is missing
# Create lagged optvolume_js12 and vol for the condition check
df = df.sort_values(["permno", "time_avail_m"])
df["l1_optvolume"] = df.groupby("permno")["optvolume_js12"].shift(1)
df["l1_vol"] = df.groupby("permno")["vol"].shift(1)
df.loc[df["l1_optvolume"].isna() | df["l1_vol"].isna(), "OptionVolume1"] = np.nan

# Create 6 lags of OptionVolume1 for calculating 6-month moving average
for n in range(1, 7):
    df[f"tempVol{n}"] = df.groupby("permno")["OptionVolume1"].shift(n)

# Calculate 6-month moving average of OptionVolume1
temp_cols = [f"tempVol{n}" for n in range(1, 7)]
df["tempMean"] = df[temp_cols].mean(axis=1)

# Calculate OptionVolume2 as current ratio divided by 6-month average
df["OptionVolume2"] = df["OptionVolume1"] / df["tempMean"]

# SAVE
# Save OptionVolume1 predictor
save_predictor(df[["permno", "time_avail_m", "OptionVolume1"]], "OptionVolume1")
print("ZZ1_OptionVolume1_OptionVolume2.py completed successfully")

# Save OptionVolume2 predictor
save_predictor(df[["permno", "time_avail_m", "OptionVolume2"]], "OptionVolume2")
print("ZZ1_OptionVolume1_OptionVolume2.py completed successfully")
