# ABOUTME: Calculates 6-month momentum following Jegadeesh and Titman 1993 Table 1A K=3 row 6
# ABOUTME: Run from pyCode/ directory: python3 Predictors/Mom6m.py

# Run from pyCode/ directory
# Inputs: SignalMasterTable.parquet
# Output: ../pyData/Predictors/Mom6m.csv

import pandas as pd
import numpy as np
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils.stata_replication import stata_multi_lag
from utils.save_standardized import save_predictor

print("=" * 80)
print("🏗️  Mom6m.py")
print("Creating six-month momentum predictor")
print("=" * 80)

# DATA LOAD
print("📊 Loading SignalMasterTable data...")
df = pd.read_parquet("../pyData/Intermediate/SignalMasterTable.parquet")
df = df[["permno", "time_avail_m", "ret"]].copy()
print(f"Loaded: {len(df):,} observations")

# Sort for lag operations
df = df.sort_values(["permno", "time_avail_m"])

# SIGNAL CONSTRUCTION
print("🧮 Computing 6-month momentum signal...")
# Replace missing returns with 0 for momentum calculations
df["ret"] = df["ret"].fillna(0)

# Create 5 monthly lags (t-1 to t-5) using calendar-aware lag function
df = stata_multi_lag(df, "permno", "time_avail_m", "ret", [1, 2, 3, 4, 5])

# Compounds monthly returns over months t-5 to t-1 to create 6-month momentum (skips current month t)
df["Mom6m"] = (
    (1 + df["ret_lag1"])
    * (1 + df["ret_lag2"])
    * (1 + df["ret_lag3"])
    * (1 + df["ret_lag4"])
    * (1 + df["ret_lag5"])
) - 1

# Keep only necessary columns for output
df_final = df[["permno", "time_avail_m", "Mom6m"]].copy()

# SAVE
print("💾 Saving Mom6m predictor...")
save_predictor(df_final, "Mom6m")
print("✅ Mom6m.csv saved successfully")

print("=" * 80)
print("✅ Mom6m.py Complete")
print("Six-month momentum predictor generated successfully")
print("=" * 80)
