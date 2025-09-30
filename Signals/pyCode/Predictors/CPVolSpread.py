# ABOUTME: Call minus Put Vol following Bali and Hovakimian 2009, Table 3 Panel B
# ABOUTME: Calculates ATM call vol minus ATM put vol spread from OptionMetrics data

"""
CPVolSpread.py

Usage:
    Run from [Repo-Root]/Signals/pyCode/

    python3 Predictors/CPVolSpread.py

Inputs:
    - bali_hovak_imp_vol.csv: Option metrics data with implied volatility by call/put flag
    - SignalMasterTable.parquet: Monthly master table with permno, time_avail_m, secid, sicCRSP

Outputs:
    - CPVolSpread.csv: CSV file with columns [permno, yyyymm, CPVolSpread]
    - CPVolSpread = mean_imp_volC - mean_imp_volP (Call-Put volatility spread)
    - Implements Bali-Hovak (2009) panel B methodology
"""

import pandas as pd
import numpy as np
from pathlib import Path
import sys
import os

# Add utils directory to path for imports
sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
from utils.save_standardized import save_predictor
from config import PATCH_OPTIONM_IV


print("Starting CPVolSpread.py...")

# Patch Option Metrics IV data if configured
if PATCH_OPTIONM_IV:
    print("PATCH_OPTIONM_IV is True, using 2023 vintage from openassetpricing...")
    from openassetpricing import OpenAP

    openap = OpenAP(2023)
    df = openap.dl_signal("polars", ["CPVolSpread"])
    df = df.rename({"yyyymm": "time_avail_m"})
    save_predictor(df, "CPVolSpread")
    print("CPVolSpread.py completed successfully with 2023 vintage patch")
    sys.exit()

# Clean OptionMetrics data
print("Loading and cleaning OptionMetrics data...")

# Load OptionMetrics data
option_metrics_path = Path("../pyData/Prep/bali_hovak_imp_vol.csv")
if not option_metrics_path.exists():
    raise FileNotFoundError(f"Required input file not found: {option_metrics_path}")

options_df = pd.read_csv(option_metrics_path)
options_df["time_avail_m"] = (
    pd.to_datetime(options_df["date"]).dt.to_period("M").dt.to_timestamp()
)

# Remove options with ambiguous call/put flag
options_df = options_df[options_df["cp_flag"] != "BOTH"].copy()

# Keep only current data (non-negative mean_day)
options_df = options_df[options_df["mean_day"] >= 0].copy()

print(
    f"Cleaned OptionMetrics data: {options_df.shape[0]} rows, {options_df.shape[1]} columns"
)

# Reshape data to wide format
# Remove unnecessary columns
options_df = options_df.drop(columns=["mean_day", "nobs", "ticker"])

# Pivot to create separate columns for call and put implied volatility
options_wide = options_df.pivot(
    index=["secid", "time_avail_m"], columns="cp_flag", values="mean_imp_vol"
)
options_wide.columns = [f"mean_imp_vol{col}" for col in options_wide.columns]
options_wide = options_wide.reset_index()

# Compute volatility spread
# CPVolSpread = Call implied vol - Put implied vol
options_wide["CPVolSpread"] = (
    options_wide["mean_imp_volC"] - options_wide["mean_imp_volP"]
)

print(
    f"Computed CPVolSpread for {options_wide['CPVolSpread'].notna().sum()} observations"
)

# DATA LOAD
print("Loading SignalMasterTable...")

# Load SignalMasterTable with required columns
signal_master = pd.read_parquet("../pyData/Intermediate/SignalMasterTable.parquet")

# Keep only the columns we need
required_cols = ["permno", "time_avail_m", "secid", "sicCRSP"]
missing_cols = [col for col in required_cols if col not in signal_master.columns]
if missing_cols:
    raise ValueError(f"Missing required columns in SignalMasterTable: {missing_cols}")

df = signal_master[required_cols].copy()

# Merge with options data using secid
# Remove observations missing secid
df = df.dropna(subset=["secid"])

# Left join with options data on secid and time
df = pd.merge(df, options_wide, on=["secid", "time_avail_m"], how="left")

print(f"After merging with options data: {df.shape[0]} rows")

# Filter out closed-end funds (SIC 6720-6730) and REITs (6798)
# Exclude closed-end funds
df = df[(df["sicCRSP"] < 6720) | (df["sicCRSP"] > 6730)]

# Exclude REITs
df = df[df["sicCRSP"] != 6798]

print(f"After filtering closed-end funds and REITs: {df.shape[0]} rows")

# SIGNAL CONSTRUCTION

# Keep only observations with valid CPVolSpread
df = df.dropna(subset=["CPVolSpread"])

print(f"Final CPVolSpread for {df.shape[0]} observations")

# SAVE
# Save predictor output
save_predictor(df, "CPVolSpread")

print("CPVolSpread.py completed successfully")
