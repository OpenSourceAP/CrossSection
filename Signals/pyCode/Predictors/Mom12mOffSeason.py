# ABOUTME: Momentum without the seasonal part following Heston and Sadka 2008 Table 2 Year 1 Nonannual
# ABOUTME: Run from pyCode/ directory: python3 Predictors/Mom12mOffSeason.py

# Run from pyCode/ directory
# Inputs: SignalMasterTable.parquet
# Output: ../pyData/Predictors/Mom12mOffSeason.csv

import pandas as pd
import numpy as np
import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
from utils.stata_replication import fill_date_gaps, stata_multi_lag
from utils.save_standardized import save_predictor

print("Starting Mom12mOffSeason.py...")

# DATA LOAD
print("Loading data...")
df = pd.read_parquet("../pyData/Intermediate/SignalMasterTable.parquet")
df = df[["permno", "time_avail_m", "ret"]].copy()

# SIGNAL CONSTRUCTION

# Replace missing returns with 0
df = fill_date_gaps(df, "permno", "time_avail_m", "1mo")
df["ret"] = df["ret"].fillna(0)

# We're predicting 1 month after time_avail_m
# Construct lags for the 1 year before the predicted month
# Excluding the same calendar month as the predicted month
# But also excluding the current month (due to STreversal effects)
off_season_lags = [lag for lag in range(1, 11) if (lag + 1) % 12 != 0]

print(f"Creating {len(off_season_lags)} off-season lag variables...")
df = stata_multi_lag(df, "permno", "time_avail_m", "ret", off_season_lags)

# Average returns from lags 1-10, excluding same calendar month
lag_cols = [f"ret_lag{n}" for n in off_season_lags]
df["Mom12mOffSeason"] = df[lag_cols].mean(axis=1)

# SAVE
num_obs = df["Mom12mOffSeason"].notna().sum()
print(f"Calculated Mom12mOffSeason for {num_obs} observations")

save_predictor(df, "Mom12mOffSeason")
print("Mom12mOffSeason.py completed successfully")
