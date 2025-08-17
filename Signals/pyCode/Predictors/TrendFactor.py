# ABOUTME: TrendFactor predictor using daily data with 11 moving averages and cross-sectional regressions
# ABOUTME: Usage: python3 TrendFactor.py (run from pyCode/ directory)

import polars as pl
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from utils.savepredictor import save_predictor
from utils.stata_ineq import stata_ineq_pl
from utils.asrol import asrol

print("=" * 80)
print("🏗️  TrendFactor.py")
print("Generating TrendFactor predictor using daily data with moving averages")
print("=" * 80)

print("📊 Loading daily CRSP data...")

# 1. Compute moving averages
# use permno time_d prc cfacpr using "$pathDataIntermediate/dailyCRSP", clear
daily_crsp = pl.read_parquet("../pyData/Intermediate/dailyCRSP.parquet")
df_daily = daily_crsp.select(["permno", "time_d", "prc", "cfacpr"])
print(f"Daily CRSP data: {len(df_daily):,} observations")

print("🔄 Computing adjusted prices and time variables...")

# Adjust prices for splits etc
# gen P = abs(prc)/cfacpr 
df_daily = df_daily.with_columns(
    (pl.col("prc").abs() / pl.col("cfacpr")).alias("P")
)

# Generate time variable without trading day gaps for simplicity and generate month variable for sorting
# bys permno (time_d): gen time_temp = _n
df_daily = df_daily.sort(["permno", "time_d"])
df_daily = df_daily.with_columns(
    pl.int_range(pl.len()).over("permno").alias("time_temp")
)

# gen time_avail_m = mofd(time_d)
df_daily = df_daily.with_columns(
    pl.col("time_d").dt.truncate("1mo").alias("time_avail_m")
)

print("📈 Computing moving averages for 11 different lags...")

# Calculate moving average prices for various lag lengths
# xtset permno time_temp
lag_lengths = [3, 5, 10, 20, 50, 100, 200, 400, 600, 800, 1000]

# Convert to pandas for asrol_legacy operations
import pandas as pd
df_daily_pd = df_daily.to_pandas()

for L in lag_lengths:
    print(f"  Computing {L}-day moving average...")
    # asrol P, window(time_temp `L') stat(mean) by(permno) gen(A_`L')
    df_daily_pd = asrol(
        df_daily_pd,
        group_col='permno',
        time_col='time_temp',
        value_col='P',
        window=L,
        stat='mean',
        new_col_name=f'A_{L}',
        min_periods=1  # Allow partial windows like Stata default
    )

# Convert back to polars
df_daily = pl.from_pandas(df_daily_pd)

print("📅 Keeping only end-of-month observations...")

# Keep only last observation each month
# bys permno time_avail_m (time_d): keep if _n == _N
df_daily = df_daily.sort(["permno", "time_avail_m", "time_d"])
df_monthly = df_daily.group_by(["permno", "time_avail_m"], maintain_order=True).last()


print(f"Monthly data after filtering: {len(df_monthly):,} observations")

# Normalize by closing price at end of month
for L in lag_lengths:
    df_monthly = df_monthly.with_columns(
        (pl.col(f"A_{L}") / pl.col("P")).alias(f"A_{L}")
    )


# Keep only needed columns
moving_avg_cols = [f"A_{L}" for L in lag_lengths]
temp_ma = df_monthly.select(["permno", "time_avail_m"] + moving_avg_cols)

print("📊 Loading monthly data for cross-sectional regressions...")

# 2. Run cross-sectional regressions on monthly data
# use permno time_avail_m ret prc exchcd shrcd mve_c using "$pathDataIntermediate/SignalMasterTable", clear
signal_master = pl.read_parquet("../pyData/Intermediate/SignalMasterTable.parquet")
df = signal_master.select(["permno", "time_avail_m", "ret", "prc", "exchcd", "shrcd", "mve_c"])
print(f"SignalMasterTable: {len(df):,} observations")

print("🎯 Computing size deciles based on NYSE stocks...")

# Calculate size deciles based on NYSE stocks only
nyse_data = df.filter(pl.col("exchcd") == 1)
qu10_data = (nyse_data
    .group_by("time_avail_m")
    .agg(pl.col("mve_c").quantile(0.1).alias("qu10"))
)

# Merge back
df = df.join(qu10_data, on="time_avail_m", how="left")

print("🔍 Applying filters for regression sample...")

# Filters need to be imposed here rather than at portfolio stage
df = df.filter(
    ((pl.col("exchcd") == 1) | (pl.col("exchcd") == 2) | (pl.col("exchcd") == 3)) &
    ((pl.col("shrcd") == 10) | (pl.col("shrcd") == 11)) &
    (pl.col("prc").abs() >= 5) &
    stata_ineq_pl(pl.col("mve_c"), ">", pl.col("qu10"))
)

print(f"After applying filters: {len(df):,} observations")

# Merge moving averages
df = df.join(temp_ma, on=["permno", "time_avail_m"], how="inner")
print(f"After merging moving averages: {len(df):,} observations")

print("📊 Running cross-sectional regressions...")

# Cross-sectional regression of returns on trend signals in month t-1
# xtset permno time_avail_m
df = df.sort(["permno", "time_avail_m"])

# gen fRet = f.ret  // Lead the return instead of lagging all moving averages
df = df.with_columns(
    pl.col("ret").shift(-1).over("permno").alias("fRet")
)


# bys time_avail_m: asreg fRet A_*
# Run cross-sectional regression by time_avail_m using utils/asreg.py helper
feature_cols = [f"A_{L}" for L in lag_lengths]

print("🔧 Using asreg helper for cross-sectional regressions...")
from utils.asreg import asreg

df_with_betas = asreg(
    df, 
    y="fRet",
    X=feature_cols,
    by=["time_avail_m"], 
    mode="group",
    add_intercept=True,
    outputs=("coef",),
    coef_prefix="_b_",
    null_policy="drop",
    min_samples=1,  # Allow all samples to match Stata behavior (was 12)
    solve_method="lu",  # Use LU decomposition for numerical stability
    collect=False  # Keep as LazyFrame for continued processing
).collect()  # Collect after asreg processing


print("📊 Computing 12-month rolling averages of beta coefficients...")

# Take 12-month rolling average of MA beta coefficients
# Create time-level dataset with betas
time_level_data = (df_with_betas
    .group_by("time_avail_m", maintain_order=True)
    .first()
    .sort("time_avail_m")
)

# For each lag length, compute rolling mean of beta coefficients
# asrol _b_A_`L', window(time_avail_m -13 -1) stat(mean) gen(EBeta_`L')
# This excludes the current month (uses months t-13 to t-1)
# Use min_samples=1 to allow partial windows in early periods (matches Stata default behavior)
for L in lag_lengths:
    time_level_data = time_level_data.with_columns(
        pl.col(f"_b_A_{L}")
        .shift(1)  # Exclude current month  
        .rolling_mean(window_size=12, min_samples=1)  # Allow partial windows to match Stata
        .alias(f"EBeta_{L}")
    )


# Keep only time and expected betas
ebeta_cols = [f"EBeta_{L}" for L in lag_lengths]
temp_beta = time_level_data.select(["time_avail_m"] + ebeta_cols)

# Merge back to main data
df_final = df_with_betas.join(temp_beta, on="time_avail_m", how="left")


print("🎯 Computing TrendFactor...")

# Calculate expected return E[r] = \sum E[\beta_i]A_L_i
trend_terms = []
for L in lag_lengths:
    trend_terms.append(pl.col(f"EBeta_{L}") * pl.col(f"A_{L}"))

df_final = df_final.with_columns(
    pl.sum_horizontal(trend_terms).alias("TrendFactor")
)


# Select final result
result = df_final.select(["permno", "time_avail_m", "TrendFactor"])

print(f"Generated TrendFactor values: {len(result):,} observations")
valid_trend = result.filter(pl.col("TrendFactor").is_not_null())
print(f"Non-null TrendFactor: {len(valid_trend):,} observations")

if len(valid_trend) > 0:
    print(f"TrendFactor summary stats:")
    print(f"  Mean: {valid_trend['TrendFactor'].mean():.6f}")
    print(f"  Std: {valid_trend['TrendFactor'].std():.6f}")
    print(f"  Min: {valid_trend['TrendFactor'].min():.6f}")
    print(f"  Max: {valid_trend['TrendFactor'].max():.6f}")

print("💾 Saving TrendFactor predictor...")
save_predictor(result, "TrendFactor")
print("✅ TrendFactor.csv saved successfully")
print("🎉 TrendFactor computation completed!")