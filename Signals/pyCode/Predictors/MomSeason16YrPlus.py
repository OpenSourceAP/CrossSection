# ABOUTME: Calculates seasonal momentum (years 16-20) following Heston and Sadka 2008 Table 2 Years 16-20 Annual
# ABOUTME: long-term seasonal momentum using returns from 16-20 years ago

"""
MomSeason16YrPlus.py

Usage:
    Run from [Repo-Root]/Signals/pyCode/
    python3 Predictors/MomSeason16YrPlus.py

Inputs:
    - SignalMasterTable.parquet: Master table with columns [permno, time_avail_m, ret]

Outputs:
    - MomSeason16YrPlus.csv: CSV file with columns [permno, yyyymm, MomSeason16YrPlus]
"""

import pandas as pd
import numpy as np
import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
from utils.stata_replication import stata_multi_lag
from utils.save_standardized import save_predictor

print("Starting MomSeason16YrPlus.py...")

# DATA LOAD
print("Loading data...")
df = pd.read_parquet("../pyData/Intermediate/SignalMasterTable.parquet")
df = df[["permno", "time_avail_m", "ret"]].copy()

# SIGNAL CONSTRUCTION
# Update 0 if mi(ret)
df["ret"] = df["ret"].fillna(0)

# foreach n of numlist 191(12)240 { Generate l`n'.ret }
# This creates lags for periods: 191, 203, 215, 227, 239 months
lag_periods = list(range(191, 241, 12))  # 191, 203, 215, 227, 239
df = stata_multi_lag(df, "permno", "time_avail_m", "ret", lag_periods)

# eGenerate rowtotal(temp*), missing
lag_cols = [f"ret_lag{n}" for n in lag_periods]
df["retTemp1"] = df[lag_cols].sum(axis=1)
# Handle case where all values are NaN - should return NaN, not 0
all_missing = df[lag_cols].isna().all(axis=1)
df.loc[all_missing, "retTemp1"] = np.nan

# eGenerate rownonmiss(temp*)
df["retTemp2"] = df[lag_cols].notna().sum(axis=1)

# Generate retTemp1/retTemp2
df["MomSeason16YrPlus"] = df["retTemp1"] / df["retTemp2"]

# SAVE
print(
    f"Calculated MomSeason16YrPlus for {df['MomSeason16YrPlus'].notna().sum()} observations"
)

save_predictor(df, "MomSeason16YrPlus")
print("MomSeason16YrPlus.py completed successfully")
