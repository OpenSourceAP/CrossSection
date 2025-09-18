# ABOUTME: Calculates seasonal momentum following Heston and Sadka 2008 Table 2 Years 2-5 Annual
# ABOUTME: Run from pyCode/ directory: python3 Predictors/MomSeason.py

# Run from pyCode/ directory
# Inputs: SignalMasterTable.parquet
# Output: ../pyData/Predictors/MomSeason.csv

import pandas as pd
import numpy as np
import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
from utils.stata_replication import stata_multi_lag
from utils.save_standardized import save_predictor

print("Starting MomSeason.py...")

# DATA LOAD
print("Loading SignalMasterTable...")
df = pd.read_parquet("../pyData/Intermediate/SignalMasterTable.parquet")
df = df[["permno", "time_avail_m", "ret"]].copy()
print(f"Loaded data: {df.shape[0]} rows")

# SIGNAL CONSTRUCTION
print("Filling missing returns with 0...")
# Update 0 if mi(ret)
df["ret"] = df["ret"].fillna(0)

# foreach n of numlist 23(12)59 { Generate l`n'.ret }
# This creates lags for periods: 23, 35, 47, 59 months
print("Creating lag variables for returns (23, 35, 47, 59 months)...")
lag_periods = [23, 35, 47, 59]
df = stata_multi_lag(df, "permno", "time_avail_m", "ret", lag_periods)

# eGenerate rowtotal(temp*), missing
print("Calculating seasonal momentum signal...")
lag_cols = [f"ret_lag{n}" for n in lag_periods]
df["retTemp1"] = df[lag_cols].sum(axis=1)
# Handle case where all values are NaN - should return NaN, not 0
all_missing = df[lag_cols].isna().all(axis=1)
df.loc[all_missing, "retTemp1"] = np.nan

# eGenerate rownonmiss(temp*)
df["retTemp2"] = df[lag_cols].notna().sum(axis=1)

# Generate retTemp1/retTemp2
df["MomSeason"] = df["retTemp1"] / df["retTemp2"]
print(f"Calculated MomSeason for {df['MomSeason'].notna().sum()} observations")

# SAVE
save_predictor(df, "MomSeason")
print("MomSeason.py completed successfully")
