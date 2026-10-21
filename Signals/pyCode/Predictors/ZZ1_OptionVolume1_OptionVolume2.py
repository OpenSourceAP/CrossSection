# ABOUTME: Option trading volume predictors following Johnson and So 2012 JFE, Table 2A
# ABOUTME: OptionVolume1 = option to stock volume ratio, OptionVolume2 = abnormal option volume (current/6-month average)

"""
ZZ1_OptionVolume1_OptionVolume2.py

Usage:
    Run from [Repo-Root]/Signals/pyCode/
    python3 Predictors/ZZ1_OptionVolume1_OptionVolume2.py

Inputs:
    - SignalMasterTable.parquet: Signal master table with columns [permno, time_avail_m, secid, prc, shrcd]
    - monthlyCRSP.parquet: Monthly CRSP data with columns [permno, time_avail_m, vol]
    - OptionMetricsVolume.csv: Option volume data with columns [secid, date, optvolume_js12]

Outputs:
    - OptionVolume1.csv: CSV file with columns [permno, yyyymm, OptionVolume1]
    - OptionVolume2.csv: CSV file with columns [permno, yyyymm, OptionVolume2]
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
from utils.stata_replication import fill_date_gaps, stata_multi_lag

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
df["_observed"] = True
df = fill_date_gaps(df, "permno", "time_avail_m")
for var in ("optvolume_js12", "vol"):
    df = stata_multi_lag(df, "permno", "time_avail_m", var, [1], prefix="l", fill_gaps=False)
df = df.rename(columns={"l1_optvolume_js12": "l1_optvolume"})
df.loc[df["l1_optvolume"].isna() | df["l1_vol"].isna(), "OptionVolume1"] = np.nan

df = stata_multi_lag(df, "permno", "time_avail_m", "OptionVolume1", list(range(1, 7)), fill_gaps=False)
df = df.rename(columns={f"OptionVolume1_lag{n}": f"tempVol{n}" for n in range(1, 7)})
df = df.loc[df["_observed"].eq(True)].drop(columns="_observed").copy()


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
