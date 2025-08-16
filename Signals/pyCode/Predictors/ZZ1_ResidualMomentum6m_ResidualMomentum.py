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
from utils.asreg import asreg

# Debug constants - replace with actual problematic observation from test results
DEBUG_PERMNO = 43880  # Replace with actual value
DEBUG_YYYYMM = 199301  # Replace with actual value (e.g., 200704)
DEBUG_DATE = pl.date(DEBUG_YYYYMM//100, DEBUG_YYYYMM%100, 1)  # Convert to polars date

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

# CHECKPOINT 1: After data merge and excess return calculation
print(f"CHECKPOINT 1: After data merge and excess return calculation for permno={DEBUG_PERMNO}")
checkpoint_data = df.filter(
    (pl.col("permno") == DEBUG_PERMNO) & 
    (pl.col("time_avail_m") == DEBUG_DATE)
).head(10)
if checkpoint_data.height > 0:
    print(checkpoint_data.select(["permno", "time_avail_m", "ret", "rf", "retrf", "mktrf", "hml", "smb"]))

# Sort by permno and time_avail_m (important for time series operations)
df = df.sort(["permno", "time_avail_m"])

# Create time_temp = _n by permno (position-based indexing like Stata)
print("Creating time_temp position index by permno...")
df = df.with_columns(
    pl.int_range(pl.len()).over("permno").alias("time_temp")
)

# CHECKPOINT 2: After creating time_temp position index
print(f"CHECKPOINT 2: After creating time_temp for permno={DEBUG_PERMNO}, yyyymm={DEBUG_YYYYMM}")
checkpoint_data = df.filter(
    (pl.col("permno") == DEBUG_PERMNO) & 
    (pl.col("time_avail_m") == DEBUG_DATE)
).head(10)
if checkpoint_data.height > 0:
    print(checkpoint_data.select(["permno", "time_avail_m", "time_temp", "retrf"]))
permno_count = df.filter(pl.col("permno") == DEBUG_PERMNO).height
print(f"Total observations for permno {DEBUG_PERMNO}: {permno_count}")

print("Running rolling 36-observation FF3 regressions by permno using asreg helper...")
print("Processing", df['permno'].n_unique(), "unique permnos...")

# Use asreg helper for rolling FF3 regression with residuals
# Rolling 36-observation windows with minimum 36 observations (exact Stata asreg match)
# Use time_temp (position-based) instead of time_avail_m (calendar-based)
df = asreg(
    df,
    y="retrf",
    X=["mktrf", "hml", "smb"],
    by=["permno"],
    t="time_temp", 
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

# CHECKPOINT 3: After rolling FF3 regression
print(f"CHECKPOINT 3: After rolling FF3 regression for permno={DEBUG_PERMNO}, yyyymm={DEBUG_YYYYMM}")
checkpoint_data = df.filter(
    (pl.col("permno") == DEBUG_PERMNO) & 
    (pl.col("time_avail_m") == DEBUG_DATE)
).head(5)
if checkpoint_data.height > 0:
    print(checkpoint_data.select(["permno", "time_avail_m", "time_temp", "_residuals", "retrf", "mktrf"]))
    # Show summary stats
    summary = checkpoint_data.select([
        pl.col("_residuals").count().alias("resid_count"),
        pl.col("_residuals").mean().alias("resid_mean"),
        pl.col("_residuals").std().alias("resid_std")
    ])
    print("Residual summary stats:", summary)
non_null_count = df.filter(
    (pl.col("permno") == DEBUG_PERMNO) & 
    (pl.col("_residuals").is_not_null())
).height
print(f"Non-null residuals for permno {DEBUG_PERMNO}: {non_null_count}")

print(f"Completed rolling regressions for {len(df):,} observations")

# Calculate lagged residuals and rolling momentum signals using pure Polars
print("Calculating lagged residuals and momentum signals...")
df = df.with_columns([
    # Lag residuals by 1 observation: temp = l1._residuals
    pl.col("_residuals").shift(1).over("permno").alias("temp")
])

# CHECKPOINT 4: After lagged residuals calculation
print(f"CHECKPOINT 4: After lagged residuals for permno={DEBUG_PERMNO}, yyyymm={DEBUG_YYYYMM}")
checkpoint_data = df.filter(
    (pl.col("permno") == DEBUG_PERMNO) & 
    (pl.col("time_avail_m") == DEBUG_DATE)
).head(5)
if checkpoint_data.height > 0:
    print(checkpoint_data.select(["permno", "time_avail_m", "time_temp", "_residuals", "temp"]))
# Show recent observations
recent_data = df.filter(pl.col("permno") == DEBUG_PERMNO).tail(10)
print("Recent observations for permno:", recent_data.select(["permno", "time_avail_m", "time_temp", "_residuals", "temp"]))
non_null_temp_count = df.filter(
    (pl.col("permno") == DEBUG_PERMNO) & 
    (pl.col("temp").is_not_null())
).height
print(f"Non-null temp (lagged residuals) for permno {DEBUG_PERMNO}: {non_null_temp_count}")

df = df.with_columns([
    # 6-observation rolling statistics (position-based, min 6 observations)
    pl.col("temp").rolling_mean(window_size=6, min_samples=6).over("permno").alias("mean6_temp"),
    pl.col("temp").rolling_std(window_size=6, min_samples=6).over("permno").alias("sd6_temp"),
    # 11-observation rolling statistics (position-based, min 11 observations)
    pl.col("temp").rolling_mean(window_size=11, min_samples=11).over("permno").alias("mean11_temp"),
    pl.col("temp").rolling_std(window_size=11, min_samples=11).over("permno").alias("sd11_temp")
])

# CHECKPOINT 5: After 6-month rolling statistics
print(f"CHECKPOINT 5: After 6-month rolling statistics for permno={DEBUG_PERMNO}, yyyymm={DEBUG_YYYYMM}")
checkpoint_data = df.filter(
    (pl.col("permno") == DEBUG_PERMNO) & 
    (pl.col("time_avail_m") == DEBUG_DATE)
)
if checkpoint_data.height > 0:
    print(checkpoint_data.select(["permno", "time_avail_m", "temp", "mean6_temp", "sd6_temp"]))
    # Show summary stats
    summary = checkpoint_data.select([
        pl.col("mean6_temp").alias("mean6"),
        pl.col("sd6_temp").alias("sd6")
    ])
    print("6-month rolling stats:", summary)

df = df.with_columns([
    # Calculate momentum signals
    (pl.col("mean6_temp") / pl.col("sd6_temp")).alias("ResidualMomentum6m"),
    (pl.col("mean11_temp") / pl.col("sd11_temp")).alias("ResidualMomentum")
])

print("Calculating 6-observation and 11-observation rolling momentum signals...")

# Display signal summary statistics
print("\n📈 Signal summary statistics:")
print(f"ResidualMomentum6m - Mean: {df.select(pl.col('ResidualMomentum6m').mean()).item():.4f}, Std: {df.select(pl.col('ResidualMomentum6m').std()).item():.4f}")
print(f"ResidualMomentum - Mean: {df.select(pl.col('ResidualMomentum').mean()).item():.4f}, Std: {df.select(pl.col('ResidualMomentum').std()).item():.4f}")
print(f"Non-missing ResidualMomentum6m: {df.select(pl.col('ResidualMomentum6m').is_not_null().sum()).item():,}")
print(f"Non-missing ResidualMomentum: {df.select(pl.col('ResidualMomentum').is_not_null().sum()).item():,}")

# CHECKPOINT 6: After 11-month rolling statistics and final calculation
print(f"CHECKPOINT 6: After 11-month rolling stats for permno={DEBUG_PERMNO}, yyyymm={DEBUG_YYYYMM}")
checkpoint_data = df.filter(
    (pl.col("permno") == DEBUG_PERMNO) & 
    (pl.col("time_avail_m") == DEBUG_DATE)
)
if checkpoint_data.height > 0:
    print(checkpoint_data.select(["permno", "time_avail_m", "temp", "mean11_temp", "sd11_temp", "ResidualMomentum"]))
    # Show summary stats
    summary = checkpoint_data.select([
        pl.col("mean11_temp").alias("mean11"),
        pl.col("sd11_temp").alias("sd11"),
        pl.col("ResidualMomentum").alias("momentum")
    ])
    print("11-month rolling stats:", summary)
    # Show final predictors
    final_predictors = checkpoint_data.select(["permno", "time_avail_m", "ResidualMomentum6m", "ResidualMomentum"])
    print("Final predictor values:", final_predictors)

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