# ABOUTME: Mom12mOffSeason.py - generates 12-month momentum without seasonal component
# ABOUTME: Python translation of Mom12mOffSeason.do using simple rolling mean excluding focal return

"""
Mom12mOffSeason.py

Generates 12-month momentum without seasonal component using simple rolling mean:
- Mom12mOffSeason: 10-month rolling mean excluding the most recent return (focal)

Usage:
    cd pyCode/
    source .venv/bin/activate  
    python3 Predictors/Mom12mOffSeason.py

Inputs:
    - ../pyData/Intermediate/SignalMasterTable.parquet (permno, time_avail_m, ret)

Outputs:
    - ../pyData/Predictors/Mom12mOffSeason.csv

Requirements:
    - 10-month rolling windows with minimum 6 observations
    - Exclude focal (most recent) return from rolling calculation
"""

import polars as pl
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from utils.savepredictor import save_predictor

print("=" * 80)
print("🏗️  Mom12mOffSeason.py")
print("Generating 12-month momentum without seasonal component")
print("=" * 80)

# DATA LOAD
print("📊 Loading SignalMasterTable data...")

# Load SignalMasterTable data (permno, time_avail_m, ret)
print("Loading SignalMasterTable.parquet...")
df = pl.read_parquet("../pyData/Intermediate/SignalMasterTable.parquet").select(["permno", "time_avail_m", "ret"])
print(f"Loaded SignalMasterTable: {len(df):,} monthly observations")

# SIGNAL CONSTRUCTION
print("🧮 Computing 12-month momentum without seasonal component...")

# Replace missing returns with 0 (following Stata logic)
df = df.with_columns(
    pl.col("ret").fill_null(0.0)
)

# Sort by permno and time for rolling operations
df = df.sort(["permno", "time_avail_m"])

print("📊 Computing 10-month rolling mean excluding focal return...")

# Shift ret by 1 to exclude focal (most recent) return, then calculate rolling mean
# This replicates Stata's asrol with xf(focal) option
df_final = df.with_columns(
    # First shift returns by 1 to exclude focal return
    pl.col("ret").shift(1).over("permno").alias("ret_lagged")
).with_columns(
    # Then calculate 10-month rolling mean with minimum 6 observations
    pl.col("ret_lagged").rolling_mean(window_size=10, min_samples=6).over("permno").alias("Mom12mOffSeason")
).select(["permno", "time_avail_m", "Mom12mOffSeason"]).filter(
    pl.col("Mom12mOffSeason").is_not_null() & pl.col("Mom12mOffSeason").is_finite()
)

print(f"Generated Mom12mOffSeason values: {len(df_final):,} observations")
print(f"Mom12mOffSeason summary stats:")
print(f"  Mean: {df_final['Mom12mOffSeason'].mean():.6f}")
print(f"  Std: {df_final['Mom12mOffSeason'].std():.6f}")
print(f"  Min: {df_final['Mom12mOffSeason'].min():.6f}")  
print(f"  Max: {df_final['Mom12mOffSeason'].max():.6f}")

# SAVE
print("💾 Saving Mom12mOffSeason predictor...")
save_predictor(df_final, "Mom12mOffSeason")
print("✅ Mom12mOffSeason.csv saved successfully")