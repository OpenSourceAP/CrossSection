# ABOUTME: dVolCall.py - calculates change in call option implied volatility
# ABOUTME: Change in 30-day, 50-delta call option implied volatility from previous month

# An Ang Bali Cakici 2014 Table II A

"""
dVolCall predictor calculation

Usage:
    Run from [Repo-Root]/Signals/pyCode/

    python3 Predictors/dVolCall.py

Inputs:
    - ../pyData/Prep/OptionMetricsVolSurf.csv (secid, time_avail_m, days, delta, cp_flag, impl_vol)
    - ../pyData/Intermediate/SignalMasterTable.parquet (permno, time_avail_m, secid)

Outputs:
    - ../pyData/Predictors/dVolCall.csv (permno, yyyymm, dVolCall)
"""

import pandas as pd
import numpy as np
import sys
import os

# Add utils directory to path for imports
sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
from utils.save_standardized import save_predictor
from config import PATCH_OPTIONM_IV

print("Starting dVolCall.py...")

# Check for Option Metrics patch
if PATCH_OPTIONM_IV:
    print("WARNING: PATCH_OPTIONM_IV is True, using 2023 vintage from openassetpricing")
    print("See https://github.com/OpenSourceAP/CrossSection/issues/156")
    from openassetpricing import OpenAP

    openap = OpenAP(2023)
    df = openap.dl_signal("polars", ["dVolCall"])
    df = df.rename({"yyyymm": "time_avail_m"})
    save_predictor(df, "dVolCall")
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

# Keep only call options
options_df = options_df[options_df["cp_flag"] == "C"]

# Sort data for lag operations
options_df = options_df.sort_values(["secid", "time_avail_m"])

# Create 1-month lag of implied volatility
options_df["l1_impl_vol"] = options_df.groupby("secid")["impl_vol"].shift(1)

# Calculate change in call implied volatility
options_df["dVolCall"] = options_df["impl_vol"] - options_df["l1_impl_vol"]

# Keep required columns
temp_df = options_df[["secid", "time_avail_m", "dVolCall"]].copy()

# Merge onto master table
signal_df = pd.read_parquet(
    "../pyData/Intermediate/SignalMasterTable.parquet",
    columns=["permno", "time_avail_m", "secid"],
)
df = signal_df.merge(temp_df, on=["secid", "time_avail_m"], how="left")

# Keep required columns
df = df[["permno", "time_avail_m", "dVolCall"]].copy()

# SAVE
print(f"Calculated dVolCall for {df['dVolCall'].notna().sum()} observations")

save_predictor(df, "dVolCall")
print("dVolCall.py completed successfully")
