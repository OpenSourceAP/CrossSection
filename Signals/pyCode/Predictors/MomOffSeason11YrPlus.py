# ABOUTME: Calculates off-season momentum (years 11-15) following Heston and Sadka 2008 Table 2 Years 11-15 Nonannual
# ABOUTME: Run from pyCode/ directory: python3 Predictors/MomOffSeason11YrPlus.py

# Run from pyCode/ directory
# Inputs: SignalMasterTable.parquet
# Output: ../pyData/Predictors/MomOffSeason11YrPlus.csv

import pandas as pd
import numpy as np
import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
from utils.stata_replication import fill_date_gaps, stata_multi_lag
from utils.save_standardized import save_predictor

print("Starting MomOffSeason11YrPlus.py...")

# DATA LOAD
print("Loading data...")
df = pd.read_parquet("../pyData/Intermediate/SignalMasterTable.parquet")
df = df[["permno", "time_avail_m", "ret"]].copy()

# SIGNAL CONSTRUCTION

# Replace missing returns with 0
df = fill_date_gaps(df, "permno", "time_avail_m", "1mo")
df["ret"] = df["ret"].fillna(0)

# Define Years 11-15 before predicted month (we're predicting 1 month after time_avail_m)
years_range = [11, 15]
lag_start = (years_range[0] - 1) * 12
lag_end = years_range[1] * 12

# Exclude same calendar month as predicted month
# A lag represents same month when (lag + 1) % 12 == 0
off_season_lags = [lag for lag in range(lag_start, lag_end) if (lag + 1) % 12 != 0]

print(f"Creating {len(off_season_lags)} off-season lag variables...")
df = stata_multi_lag(df, "permno", "time_avail_m", "ret", off_season_lags)

# Average returns from years 11-15, excluding same calendar month
lag_cols = [f"ret_lag{n}" for n in off_season_lags]
df["MomOffSeason11YrPlus"] = df[lag_cols].mean(axis=1)

# SAVE
print(
    f"Calculated MomOffSeason11YrPlus for {df['MomOffSeason11YrPlus'].notna().sum()} observations"
)

save_predictor(df, "MomOffSeason11YrPlus")
print("MomOffSeason11YrPlus.py completed successfully")
