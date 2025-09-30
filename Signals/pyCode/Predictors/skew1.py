# ABOUTME: Volatility smirk near the money following Xing, Zhang, and Zhao 2010, Table 3A
# ABOUTME: calculates volatility smirk predictor using OptionMetrics implied volatility differences

"""
skew1.py

Usage:
    Run from [Repo-Root]/Signals/pyCode/
    python3 Predictors/skew1.py

Inputs:
    - SignalMasterTable.parquet: Monthly master table with columns [permno, time_avail_m, secid]
    - OptionMetricsXZZ.csv: Options data with Skew1 already calculated

Outputs:
    - skew1.csv: CSV file with columns [permno, yyyymm, skew1]
"""

import pandas as pd
import numpy as np
import sys
import os

# Add utils directory to path for imports
sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
from utils.save_standardized import save_predictor
from config import PATCH_OPTIONM_IV

print("Starting skew1.py...")

# Check for Option Metrics patch
if PATCH_OPTIONM_IV:
    print("WARNING: PATCH_OPTIONM_IV is True, using 2023 vintage from openassetpricing")
    print("See https://github.com/OpenSourceAP/CrossSection/issues/156")
    from openassetpricing import OpenAP

    openap = OpenAP(2023)
    df = openap.dl_signal("polars", ["skew1"])
    df = df.rename({"yyyymm": "time_avail_m"})
    save_predictor(df, "skew1")
    sys.exit()

# DATA LOAD
df = pd.read_parquet("../pyData/Intermediate/SignalMasterTable.parquet")
df = df[["permno", "time_avail_m", "secid"]].copy()

# Split into two groups: missing secid and non-missing secid
missing_secid = df[df["secid"].isna()].copy()
has_secid = df[df["secid"].notna()].copy()

# Merge with OptionMetrics data for observations with secid
options = pd.read_csv("../pyData/Prep/OptionMetricsXZZ.csv")
options = options.rename(columns={"Skew1": "skew1"})
options["time_avail_m"] = (
    pd.to_datetime(options["time_avail_m"]).dt.to_period("M").dt.to_timestamp()
)
has_secid = has_secid.merge(options, on=["secid", "time_avail_m"], how="left")

# Combine back together (append missing secid observations)
df_final = pd.concat([has_secid, missing_secid], ignore_index=True)

# SIGNAL CONSTRUCTION
# Construction is done in R1_OptionMetrics.R (skew1 should already be in the data)

# Keep only necessary columns for output
df_final = df_final[["permno", "time_avail_m", "skew1"]].copy()
df_final = df_final.dropna(subset=["skew1"])

# Convert time_avail_m to yyyymm format like other predictors
df_final["yyyymm"] = (
    df_final["time_avail_m"].dt.year * 100 + df_final["time_avail_m"].dt.month
)

# Convert to integers for consistency with other predictors
df_final["permno"] = df_final["permno"].astype("int64")
df_final["yyyymm"] = df_final["yyyymm"].astype("int64")

# Keep only required columns and set index
df_final = df_final[["permno", "yyyymm", "skew1"]].copy()
df_final = df_final.set_index(["permno", "yyyymm"])

# SAVE
df_final.to_csv("../pyData/Predictors/skew1.csv")

print("skew1 predictor saved successfully")
