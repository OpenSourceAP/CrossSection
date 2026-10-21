# ABOUTME: Change in put option implied volatility following Ang, Bali, Cakici 2014 Table II B
# ABOUTME: calculates change in 30-day, 50-delta put option implied volatility from previous month

"""
dVolPut.py

Usage:
    Run from [Repo-Root]/Signals/pyCode/
    python3 Predictors/dVolPut.py

Inputs:
    - If PATCH_OPTIONM_IV (config.py): only the 2023-vintage dVolPut from Google Drive, via utils/optionm_patch.py (issue #156)
    - OptionMetricsVolSurf.csv: Option metrics volatility surface data with columns [secid, time_avail_m, days, delta, cp_flag, impl_vol]
    - SignalMasterTable.parquet: Master table with columns [permno, time_avail_m, secid]

Outputs:
    - dVolPut.csv: CSV file with columns [permno, yyyymm, dVolPut]
"""

import pandas as pd
import numpy as np
import sys
import os

# Add utils directory to path for imports
sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
from utils.save_standardized import save_predictor
from utils.stata_replication import stata_multi_lag
from utils.optionm_patch import load_optionm_patch
from config import PATCH_OPTIONM_IV

print("Starting dVolPut.py...")

# Check for Option Metrics patch
if PATCH_OPTIONM_IV:
    print("WARNING: PATCH_OPTIONM_IV is True, using 2023 vintage via Google Drive")
    print("See https://github.com/OpenSourceAP/CrossSection/issues/156")
    df = load_optionm_patch("dVolPut")
    save_predictor(df, "dVolPut")
    sys.exit()

# DATA LOAD
print("Loading data...")
# Clean OptionMetrics data
options_df = pd.read_csv("../pyData/Prep/OptionMetricsVolSurf.csv")
options_df["time_avail_m"] = (
    pd.to_datetime(options_df["time_avail_m"]).dt.to_period("M").dt.to_timestamp()
)
options_df = options_df[
    ["secid", "time_avail_m", "days", "delta", "cp_flag", "impl_vol"]
]

# SIGNAL CONSTRUCTION
# Screen: 30 days and delta = 50
options_df = options_df[(options_df["days"] == 30) & (abs(options_df["delta"]) == 50)]

# Keep only put options
options_df = options_df[options_df["cp_flag"] == "P"]

# Sort data for lag operations
options_df = options_df.sort_values(["secid", "time_avail_m"])

# Create 1-month lag of implied volatility
# Fill calendar gaps for lags, then restore the observed rows.
options_df["_observed"] = True
options_df = stata_multi_lag(options_df, "secid", "time_avail_m", "impl_vol", [1])
options_df = options_df.rename(columns={"impl_vol_lag1": "l1_impl_vol"})
options_df = options_df.loc[options_df["_observed"].eq(True)].drop(columns="_observed")

# Calculate change in put implied volatility
options_df["dVolPut"] = options_df["impl_vol"] - options_df["l1_impl_vol"]

# Keep required columns
temp_df = options_df[["secid", "time_avail_m", "dVolPut"]].copy()

# Merge onto master table
signal_df = pd.read_parquet(
    "../pyData/Intermediate/SignalMasterTable.parquet",
    columns=["permno", "time_avail_m", "secid"],
)
df = signal_df.merge(temp_df, on=["secid", "time_avail_m"], how="left")

# Keep required columns
df = df[["permno", "time_avail_m", "dVolPut"]].copy()

# SAVE
print(f"Calculated dVolPut for {df['dVolPut'].notna().sum()} observations")

save_predictor(df, "dVolPut")
print("dVolPut.py completed successfully")
