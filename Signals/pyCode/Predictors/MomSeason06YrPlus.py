# ABOUTME: Calculates seasonal momentum (years 6-10) following Heston and Sadka 2008 Table 2 Years 6-10 Annual
# ABOUTME: measures average returns from 71, 83, 95, 107, 119 months ago

"""
MomSeason06YrPlus.py

Usage:
    Run from [Repo-Root]/Signals/pyCode/
    python3 Predictors/MomSeason06YrPlus.py

Inputs:
    - SignalMasterTable.parquet: Master table with columns [permno, time_avail_m, ret]

Outputs:
    - MomSeason06YrPlus.csv: CSV file with columns [permno, yyyymm, MomSeason06YrPlus]
"""

import pandas as pd
import numpy as np
import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
from utils.stata_replication import stata_multi_lag
from utils.save_standardized import save_predictor

print("Starting MomSeason06YrPlus.py...")

# DATA LOAD
print("Loading data...")
df = pd.read_parquet("../pyData/Intermediate/SignalMasterTable.parquet")
df = df[["permno", "time_avail_m", "ret"]].copy()

# SIGNAL CONSTRUCTION
# Update 0 if mi(ret)
df["ret"] = df["ret"].fillna(0)

# foreach n of numlist 71(12)120 { Generate l`n'.ret }
# This creates lags for periods: 71, 83, 95, 107, 119 months
lag_periods = list(range(71, 121, 12))  # 71, 83, 95, 107, 119
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
df["MomSeason06YrPlus"] = df["retTemp1"] / df["retTemp2"]

# SAVE
print(
    f"Calculated MomSeason06YrPlus for {df['MomSeason06YrPlus'].notna().sum()} observations"
)

save_predictor(df, "MomSeason06YrPlus")
print("MomSeason06YrPlus.py completed successfully")
