# ABOUTME: MomOffSeason.py - generates off-season long-term reversal predictor  
# ABOUTME: Python translation of MomOffSeason.do using seasonal return extraction

"""
MomOffSeason.py

Generates off-season long-term reversal predictor by removing seasonal components from long-term momentum:
- MomOffSeason: (48-month momentum - seasonal returns) / (48-month count - seasonal count)
- Seasonal returns: ret[t-23], ret[t-35], ret[t-47], ret[t-59] (every 12 months)

Usage:
    cd pyCode/
    source .venv/bin/activate  
    python3 Predictors/MomOffSeason.py

Inputs:
    - ../pyData/Intermediate/SignalMasterTable.parquet (permno, time_avail_m, ret)

Outputs:
    - ../pyData/Predictors/MomOffSeason.csv

Requirements:
    - 48-month rolling windows for base momentum calculation
    - Seasonal return extraction at 12-month intervals
    - Handle missing returns (set to 0 as per Stata logic)
"""

import polars as pl
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from utils.savepredictor import save_predictor
from utils.time_based_operations import time_based_lag

print("=" * 80)
print("🏗️  MomOffSeason.py")
print("Generating off-season long-term reversal predictor")
print("=" * 80)

# DATA LOAD
print("📊 Loading SignalMasterTable data...")

# Load SignalMasterTable data (permno, time_avail_m, ret)
print("Loading SignalMasterTable.parquet...")
df = pl.read_parquet("../pyData/Intermediate/SignalMasterTable.parquet").select(["permno", "time_avail_m", "ret"])
print(f"Loaded SignalMasterTable: {len(df):,} monthly observations")

# SIGNAL CONSTRUCTION
print("🧮 Computing off-season long-term reversal...")

# Replace missing returns with 0 (following Stata logic)
df = df.with_columns(
    pl.col("ret").fill_null(0.0)
)

# Sort by permno and time for lag operations
df = df.sort(["permno", "time_avail_m"])

print("🗓️  Extracting seasonal returns (every 12 months)...")

# Extract seasonal returns: ret[t-23], ret[t-35], ret[t-47], ret[t-59]
# These are returns from 23, 35, 47, and 59 months ago (seasonal pattern)
df = df.with_columns([
    pl.col("ret").shift(23).over("permno").alias("temp23"),
    pl.col("ret").shift(35).over("permno").alias("temp35"), 
    pl.col("ret").shift(47).over("permno").alias("temp47"),
    pl.col("ret").shift(59).over("permno").alias("temp59")
])

# Calculate seasonal return sum and count (following Stata's rowtotal/rownonmiss logic)
# Use a simpler approach: sum non-null values and count non-null values
df = df.with_columns([
    # Sum of seasonal returns (only non-null values) - Polars list.sum() automatically ignores nulls
    pl.concat_list(["temp23", "temp35", "temp47", "temp59"]).list.sum().alias("retTemp1"),
    # Count of non-null seasonal returns - use list evaluation
    pl.concat_list(["temp23", "temp35", "temp47", "temp59"]).list.eval(
        pl.element().is_not_null().sum()
    ).list.get(0).alias("retTemp2")
])

print("📊 Computing 48-month rolling momentum base...")

# Get ret[t-12] for 48-month rolling calculation (using time-based lag to match Stata's l12.ret)
df = time_based_lag(df, lag_months=12, value_col="ret", alias="retLagTemp")

# Calculate 48-month rolling sum and count using rolling operations
# This replicates Stata's asrol retLagTemp, window(time_avail_m 48) stat(sum/count)
# For rolling count, create a binary indicator for non-null values then sum
df = df.with_columns([
    pl.col("retLagTemp").rolling_sum(window_size=48, min_samples=1).over("permno").alias("retLagTemp_sum48"),
    # For rolling count: create indicator (1 if not null, 0 if null) then rolling sum
    pl.col("retLagTemp").is_not_null().cast(pl.Int32).rolling_sum(window_size=48, min_samples=1).over("permno").alias("retLagTemp_count48")
])

print("🧮 Computing final off-season momentum predictor...")

# Calculate MomOffSeason: (48-month sum - seasonal sum) / (48-month count - seasonal count)
df_final = df.with_columns(
    ((pl.col("retLagTemp_sum48") - pl.col("retTemp1")) / 
     (pl.col("retLagTemp_count48") - pl.col("retTemp2"))).alias("MomOffSeason")
).select(["permno", "time_avail_m", "MomOffSeason"]).filter(
    pl.col("MomOffSeason").is_not_null() & pl.col("MomOffSeason").is_finite()
)

print(f"Generated MomOffSeason values: {len(df_final):,} observations")
print(f"MomOffSeason summary stats:")
print(f"  Mean: {df_final['MomOffSeason'].mean():.6f}")
print(f"  Std: {df_final['MomOffSeason'].std():.6f}")
print(f"  Min: {df_final['MomOffSeason'].min():.6f}")  
print(f"  Max: {df_final['MomOffSeason'].max():.6f}")

# SAVE
print("💾 Saving MomOffSeason predictor...")
save_predictor(df_final, "MomOffSeason")
print("✅ MomOffSeason.csv saved successfully")