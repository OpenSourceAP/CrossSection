# ABOUTME: ZZ1_ResidualMomentum6m_ResidualMomentum.py - generates ResidualMomentum6m and ResidualMomentum predictors
# ABOUTME: Python translation of ZZ1_ResidualMomentum6m_ResidualMomentum.do using polars for rolling FF3 regressions

"""
ZZ1_ResidualMomentum6m_ResidualMomentum.py

Generates two momentum predictors based on Fama-French 3-factor model residuals:
- ResidualMomentum6m: 6-month residual momentum (placebo)
- ResidualMomentum: 12-month residual momentum based on FF3 residuals (predictor)

Usage:
    cd pyCode/
    source .venv/bin/activate
    python3 Predictors/ZZ1_ResidualMomentum6m_ResidualMomentum.py

Inputs:
    - ../pyData/Intermediate/monthlyCRSP.parquet (permno, time_avail_m, ret)
    - ../pyData/Intermediate/monthlyFF.parquet (time_avail_m, rf, mktrf, smb, hml)

Outputs:
    - ../pyData/Placebos/ResidualMomentum6m.csv
    - ../pyData/Predictors/ResidualMomentum.csv

Requirements:
    - Rolling 36-month FF3 regressions with minimum 36 observations
    - Residuals are lagged by 1 month before momentum calculation
    - 6-month and 11-month rolling windows for momentum signals
"""

import polars as pl
import polars.selectors as cs
import numpy as np
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from utils.savepredictor import save_predictor
from utils.saveplacebo import save_placebo
from utils.stata_asreg_asrol import asreg_polars as asreg


print("=" * 80)
print("🏗️  ZZ1_ResidualMomentum6m_ResidualMomentum.py")
print("Generating ResidualMomentum6m and ResidualMomentum predictors")
print("=" * 80)

# DATA LOAD
print("📊 Loading monthly CRSP and Fama-French data...")

# Load monthly CRSP data (permno, time_avail_m, ret)
print("Loading monthlyCRSP.parquet...")
crsp = pl.read_parquet("../pyData/Intermediate/monthlyCRSP.parquet").select(["permno", "time_avail_m", "ret"])
print(f"Loaded CRSP: {len(crsp):,} monthly observations")

# Load monthly FF factors and merge
print("Loading monthlyFF.parquet...")
ff = pl.read_parquet("../pyData/Intermediate/monthlyFF.parquet").select(["time_avail_m", "rf", "mktrf", "hml", "smb"])
print(f"Loaded FF factors: {len(ff):,} monthly observations")

# Merge CRSP and FF data (equivalent to Stata's merge m:1 ... keep(match))
print("Merging CRSP and FF data...")
df = crsp.join(ff, on="time_avail_m", how="inner")
print(f"Merged dataset: {len(df):,} observations")

# SIGNAL CONSTRUCTION
print("\n🔧 Starting signal construction...")

# Calculate excess returns: retrf = ret - rf
print("Calculating excess returns (retrf = ret - rf)...")
df = df.with_columns((pl.col("ret") - pl.col("rf")).alias("retrf"))

# CHECKPOINT 1: Check retrf calculation for problematic observations
print("\n=== CHECKPOINT 1: retrf calculation for problematic observations ===")
debug_filter = (
    ((pl.col("permno") == 43880) & (pl.col("time_avail_m") >= 199301) & (pl.col("time_avail_m") <= 199306)) |
    ((pl.col("permno") == 79490) & (pl.col("time_avail_m") >= 200712) & (pl.col("time_avail_m") <= 200803)) |
    ((pl.col("permno") == 85570) & (pl.col("time_avail_m") >= 200712) & (pl.col("time_avail_m") <= 200803)) |
    ((pl.col("permno") == 13725) & (pl.col("time_avail_m") >= 193501) & (pl.col("time_avail_m") <= 193512))
)
debug_df = df.filter(debug_filter).select(["permno", "time_avail_m", "ret", "rf", "retrf"]).sort(["permno", "time_avail_m"])
print(debug_df)
print()


# Sort by permno and time_avail_m (important for time series operations)
df = df.sort(["permno", "time_avail_m"])

# Create time_temp = _n by permno (position-based indexing like Stata)
print("Creating time_temp position index by permno...")
df = df.with_columns(
    pl.int_range(pl.len()).over("permno").alias("time_temp")
)


print("Running rolling 36-observation FF3 regressions by permno using asreg helper...")
print("Processing", df['permno'].n_unique(), "unique permnos...")

# Use asreg helper for rolling FF3 regression with residuals  
# Rolling 36-observation windows with minimum 36 observations (exact Stata asreg match)
# Use time_temp (position-based) to match Stata's approach exactly
df = asreg(
    df,
    y="retrf",
    X=["mktrf", "hml", "smb"],
    by=["permno"],
    t="time_temp",  # Use position-based time_temp to match Stata exactly 
    mode="rolling",
    window_size=36,
    min_samples=36,
    add_intercept=True,  # Explicit parameter to match Stata asreg default behavior
    outputs=("resid",),
    null_policy="ignore",  # Match Stata's handling of missing values
    solve_method="svd",  # Match Stata's OLS solver method
    collect=True
)

# Rename residual column to match existing code
df = df.with_columns(
    pl.col("resid").alias("_residuals")
).drop("resid")

print(f"Completed rolling regressions for {len(df):,} observations")

# CHECKPOINT 2: Check FF3 regression results for problematic observations
print("\n=== CHECKPOINT 2: FF3 regression results for problematic observations ===")
debug_df2 = df.filter(debug_filter).select(["permno", "time_avail_m", "time_temp", "_residuals"]).sort(["permno", "time_avail_m"])
print(debug_df2)
print()

# Calculate lagged residuals and rolling momentum signals using pure Polars
print("Calculating lagged residuals and momentum signals...")
df = df.with_columns([
    # Lag residuals by 1 observation: temp = l1._residuals
    pl.col("_residuals").shift(1).over("permno").alias("temp")
])

# CHECKPOINT 3: Check lagged residuals
print("\n=== CHECKPOINT 3: lagged residuals ===")
debug_df3 = df.filter(debug_filter).select(["permno", "time_avail_m", "time_temp", "_residuals", "temp"]).sort(["permno", "time_avail_m"])
print(debug_df3)
print()


df = df.with_columns([
    # 6-observation rolling statistics (position-based, min 6 observations)  
    pl.col("temp").rolling_mean(window_size=6, min_samples=6).over("permno").alias("mean6_temp"),
    pl.col("temp").rolling_std(window_size=6, min_samples=6, ddof=1).over("permno").alias("sd6_temp"),
    # 11-observation rolling statistics (position-based, min 11 observations)
    pl.col("temp").rolling_mean(window_size=11, min_samples=11).over("permno").alias("mean11_temp"), 
    pl.col("temp").rolling_std(window_size=11, min_samples=11, ddof=1).over("permno").alias("sd11_temp")
])


df = df.with_columns([
    # Calculate momentum signals
    (pl.col("mean6_temp") / pl.col("sd6_temp")).alias("ResidualMomentum6m"),
    (pl.col("mean11_temp") / pl.col("sd11_temp")).alias("ResidualMomentum")
])

print("Calculating 6-observation and 11-observation rolling momentum signals...")

# CHECKPOINT 4: Check 6-month rolling statistics
print("\n=== CHECKPOINT 4: 6-month rolling statistics ===")
debug_df4 = df.filter(debug_filter).select(["permno", "time_avail_m", "time_temp", "temp", "mean6_temp", "sd6_temp", "ResidualMomentum6m"]).sort(["permno", "time_avail_m"])
print(debug_df4)
print()

# CHECKPOINT 5: Check 11-month rolling statistics and final ResidualMomentum
print("\n=== CHECKPOINT 5: 11-month rolling statistics and final ResidualMomentum ===")
debug_df5 = df.filter(debug_filter).select(["permno", "time_avail_m", "time_temp", "temp", "mean11_temp", "sd11_temp", "ResidualMomentum"]).sort(["permno", "time_avail_m"])
print(debug_df5)
print()

# Display signal summary statistics
print("\n📈 Signal summary statistics:")
print(f"ResidualMomentum6m - Mean: {df.select(pl.col('ResidualMomentum6m').mean()).item():.4f}, Std: {df.select(pl.col('ResidualMomentum6m').std()).item():.4f}")
print(f"ResidualMomentum - Mean: {df.select(pl.col('ResidualMomentum').mean()).item():.4f}, Std: {df.select(pl.col('ResidualMomentum').std()).item():.4f}")
print(f"Non-missing ResidualMomentum6m: {df.select(pl.col('ResidualMomentum6m').is_not_null().sum()).item():,}")
print(f"Non-missing ResidualMomentum: {df.select(pl.col('ResidualMomentum').is_not_null().sum()).item():,}")


# SAVE
print("\n💾 Saving signals...")

# Convert to pandas for save functions (they expect pandas DataFrames)
final_df = df.select(['permno', 'time_avail_m', 'ResidualMomentum6m', 'ResidualMomentum']).to_pandas()

# Save ResidualMomentum6m as placebo
save_placebo(final_df[['permno', 'time_avail_m', 'ResidualMomentum6m']], 'ResidualMomentum6m')

# Save ResidualMomentum as predictor
save_predictor(final_df[['permno', 'time_avail_m', 'ResidualMomentum']], 'ResidualMomentum')

print("\n" + "=" * 80)
print("✅ ZZ1_ResidualMomentum6m_ResidualMomentum.py completed successfully")
print("Generated 2 signals:")
print("  • ResidualMomentum6m: 6 month residual momentum (Placebo)")
print("  • ResidualMomentum: Momentum based on FF3 residuals (Predictor)")
print("=" * 80)