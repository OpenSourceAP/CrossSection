# ABOUTME: MomOffSeason06YrPlus.py - generates off-season long-term reversal for years 6-10
# ABOUTME: Python translation of MomOffSeason06YrPlus.do using seasonal return extraction

"""
MomOffSeason06YrPlus.py

Generates off-season long-term reversal predictor for years 6-10 by removing seasonal components:
- MomOffSeason06YrPlus: (60-month momentum - seasonal returns) / (60-month count - seasonal count)
- Seasonal returns: ret[t-71], ret[t-83], ret[t-95], ret[t-107], ret[t-119] (every 12 months)
- Base lag: ret[t-60] for rolling calculation

Usage:
    cd pyCode/
    source .venv/bin/activate  
    python3 Predictors/MomOffSeason06YrPlus.py

Inputs:
    - ../pyData/Intermediate/SignalMasterTable.parquet (permno, time_avail_m, ret)

Outputs:
    - ../pyData/Predictors/MomOffSeason06YrPlus.csv

Requirements:
    - 60-month rolling windows for base momentum calculation
    - Seasonal return extraction at specific lags for years 6-10
"""

import polars as pl
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from utils.savepredictor import save_predictor
from utils.time_based_operations import time_based_lag

print("=" * 80)
print("🏗️  MomOffSeason06YrPlus.py")
print("Generating off-season long-term reversal for years 6-10")
print("=" * 80)

# DATA LOAD
print("📊 Loading SignalMasterTable data...")

# Load SignalMasterTable data (permno, time_avail_m, ret)
print("Loading SignalMasterTable.parquet...")
df = pl.read_parquet("../pyData/Intermediate/SignalMasterTable.parquet").select(["permno", "time_avail_m", "ret"])
print(f"Loaded SignalMasterTable: {len(df):,} monthly observations")

# SIGNAL CONSTRUCTION
print("🧮 Computing off-season long-term reversal for years 6-10...")

# Replace missing returns with 0 (following Stata logic)
df = df.with_columns(
    pl.col("ret").fill_null(0.0)
)

# Sort by permno and time for lag operations
df = df.sort(["permno", "time_avail_m"])

print("🗓️  Extracting seasonal returns for years 6-10 (every 12 months)...")

# Extract seasonal returns: ret[t-71], ret[t-83], ret[t-95], ret[t-107], ret[t-119]
# These are returns from 71, 83, 95, 107, and 119 months ago (seasonal pattern for years 6-10)
df = df.with_columns([
    pl.col("ret").shift(71).over("permno").alias("temp71"),
    pl.col("ret").shift(83).over("permno").alias("temp83"), 
    pl.col("ret").shift(95).over("permno").alias("temp95"),
    pl.col("ret").shift(107).over("permno").alias("temp107"),
    pl.col("ret").shift(119).over("permno").alias("temp119")
])

# Calculate seasonal return sum and count (following Stata's rowtotal/rownonmiss logic)
df = df.with_columns([
    # Sum of seasonal returns - fill nulls with 0 to match Stata's rowtotal behavior with missing option
    pl.concat_list([
        pl.col("temp71").fill_null(0.0),
        pl.col("temp83").fill_null(0.0), 
        pl.col("temp95").fill_null(0.0),
        pl.col("temp107").fill_null(0.0),
        pl.col("temp119").fill_null(0.0)
    ]).list.sum().alias("retTemp1"),
    # Count of non-null seasonal returns - use list evaluation
    pl.concat_list(["temp71", "temp83", "temp95", "temp107", "temp119"]).list.eval(
        pl.element().is_not_null().sum()
    ).list.get(0).alias("retTemp2")
])

print("📊 Computing 60-month rolling momentum base...")

# Get ret[t-60] for 60-month rolling calculation (using time-based lag to match Stata's l60.ret)
df = time_based_lag(df, lag_months=60, value_col="ret", alias="retLagTemp")

# Calculate 60-month rolling sum and count using rolling operations
df = df.with_columns([
    pl.col("retLagTemp").rolling_sum(window_size=60, min_samples=1).over("permno").alias("retLagTemp_sum60"),
    # For rolling count: create indicator (1 if not null, 0 if null) then rolling sum
    pl.col("retLagTemp").is_not_null().cast(pl.Int32).rolling_sum(window_size=60, min_samples=1).over("permno").alias("retLagTemp_count60")
])

print("🧮 Computing final MomOffSeason06YrPlus predictor...")

# Calculate MomOffSeason06YrPlus: (60-month sum - seasonal sum) / (60-month count - seasonal count)
# Calculate final predictor - let savepredictor handle filtering and formatting
df_final = df.with_columns(
    ((pl.col("retLagTemp_sum60") - pl.col("retTemp1")) / 
     (pl.col("retLagTemp_count60") - pl.col("retTemp2"))).alias("MomOffSeason06YrPlus")
).select(["permno", "time_avail_m", "MomOffSeason06YrPlus"])

print(f"Generated MomOffSeason06YrPlus values: {len(df_final):,} observations")
print(f"MomOffSeason06YrPlus summary stats:")
print(f"  Mean: {df_final['MomOffSeason06YrPlus'].mean():.6f}")
print(f"  Std: {df_final['MomOffSeason06YrPlus'].std():.6f}")
print(f"  Min: {df_final['MomOffSeason06YrPlus'].min():.6f}")  
print(f"  Max: {df_final['MomOffSeason06YrPlus'].max():.6f}")

# SAVE
print("💾 Saving MomOffSeason06YrPlus predictor...")
save_predictor(df_final, "MomOffSeason06YrPlus")
print("✅ MomOffSeason06YrPlus.csv saved successfully")