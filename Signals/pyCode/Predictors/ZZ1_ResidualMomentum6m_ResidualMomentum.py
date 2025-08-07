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
import polars_ols  # registers .least_squares namespace
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from utils.savepredictor import save_predictor
from utils.saveplacebo import save_placebo

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

# Sort by permno and time_avail_m (important for time series operations)
df = df.sort(["permno", "time_avail_m"])

# Perform rolling 36-month FF3 regressions using polars-ols
print("Running rolling 36-month FF3 regressions by permno...")
print("Processing", df['permno'].n_unique(), "unique permnos...")

# Rolling FF3 regression to get residuals
df = df.with_columns(
    pl.col("retrf")
    .least_squares.rolling_ols(
        pl.col("mktrf"), 
        pl.col("hml"), 
        pl.col("smb"),
        window_size=36,
        mode="residuals"
    )
    .over("permno")
    .alias("_residuals")
)

print(f"Completed rolling regressions for {len(df):,} observations")

# Calculate lagged residuals and rolling momentum signals using pure Polars
print("Calculating lagged residuals and momentum signals...")
df = df.with_columns([
    # Lag residuals by 1 month: temp = l1._residuals
    pl.col("_residuals").shift(1).over("permno").alias("temp")
]).with_columns([
    # 6-month rolling statistics
    pl.col("temp").rolling_mean(window_size=6, min_samples=6).over("permno").alias("mean6_temp"),
    pl.col("temp").rolling_std(window_size=6, min_samples=6).over("permno").alias("sd6_temp"),
    # 11-month rolling statistics  
    pl.col("temp").rolling_mean(window_size=11, min_samples=11).over("permno").alias("mean11_temp"),
    pl.col("temp").rolling_std(window_size=11, min_samples=11).over("permno").alias("sd11_temp")
]).with_columns([
    # Calculate momentum signals
    (pl.col("mean6_temp") / pl.col("sd6_temp")).alias("ResidualMomentum6m"),
    (pl.col("mean11_temp") / pl.col("sd11_temp")).alias("ResidualMomentum")
])

print("Calculating 6-month and 11-month rolling momentum signals...")

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