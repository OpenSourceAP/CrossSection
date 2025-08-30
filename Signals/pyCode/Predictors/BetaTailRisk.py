# ABOUTME: BetaTailRisk.py - generates tail risk beta using custom tail risk factor and polars-ols rolling regressions
# ABOUTME: Python translation of BetaTailRisk.do using polars for tail risk calculation and direct polars-ols for exact Stata replication

"""
BetaTailRisk.py

Generates tail risk beta predictor from daily and monthly return data:
- Creates monthly tail risk factor from daily returns (5th percentile tail excess returns)
- BetaTailRisk: Coefficient from regression ret ~ tailex over 120-month rolling windows
- Rolling 120-month regression of returns on tail risk factor with minimum 72 observations per window

Usage:
    cd pyCode/
    source .venv/bin/activate  
    python3 Predictors/BetaTailRisk.py

Inputs:
    - ../pyData/Intermediate/dailyCRSP.parquet (permno, time_d, ret)
    - ../pyData/Intermediate/monthlyCRSP.parquet (permno, time_avail_m, ret, shrcd)

Outputs:
    - ../pyData/Predictors/BetaTailRisk.csv
    - ../pyData/Intermediate/TailRisk.parquet (monthly tail risk factor)

Requirements:
    - Tail risk factor: log(ret/retp5) for returns in bottom 5% each month
    - Rolling 120-month windows with minimum 72 observations per window
    - Filter out non-common stocks (shrcd > 11)
    - Rolling window regression behavior with proper minimum observation constraints
"""

import polars as pl
import polars_ols as pls  # Registers .least_squares namespace
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from utils.save_standardized import save_predictor

print("=" * 80)
print("🏗️  BetaTailRisk.py")
print("Generating Tail Risk Beta predictor")
print("=" * 80)

# PART 1: CREATE TAIL RISK FACTOR FROM DAILY DATA
print("📊 Part 1: Creating monthly tail risk factor from daily returns...")

# Load daily CRSP data
print("Loading dailyCRSP.parquet...")
daily_crsp = pl.read_parquet("../pyData/Intermediate/dailyCRSP.parquet").select(["permno", "time_d", "ret"])
print(f"Loaded daily CRSP: {len(daily_crsp):,} daily observations")

# Convert daily dates to monthly
daily_crsp = daily_crsp.with_columns([
    pl.col("time_d").dt.truncate("1mo").alias("time_avail_m")
])


print("Calculating 5th percentile returns by month...")
# Calculate 5th percentile of returns by month (retp5)
# Use "lower" interpolation method for 5th percentile calculation
monthly_p5 = daily_crsp.group_by("time_avail_m").agg([
    pl.col("ret").quantile(0.05, interpolation="lower").alias("retp5")
])

print(f"Generated monthly 5th percentiles for {len(monthly_p5):,} months")


# Merge back to daily data
daily_with_p5 = daily_crsp.join(monthly_p5, on="time_avail_m", how="inner")

print("Filtering to tail observations (bottom 5%) and calculating tail excess returns...")
# Keep only observations where ret <= retp5 (tail observations)
tail_data = daily_with_p5.filter(
    pl.col("ret") <= pl.col("retp5")
)


# Calculate tail excess return: tailex = log(ret/retp5)
tail_data = tail_data.with_columns([
    (pl.col("ret") / pl.col("retp5")).log().alias("tailex")
])


print(f"Filtered to {len(tail_data):,} tail observations")

# Calculate monthly average tail excess return
monthly_tailrisk = tail_data.group_by("time_avail_m").agg([
    pl.col("tailex").mean().alias("tailex")
]).sort("time_avail_m")

print(f"Generated monthly tail risk factor for {len(monthly_tailrisk):,} months")

# Save intermediate tail risk factor
monthly_tailrisk.write_parquet("../pyData/Intermediate/TailRisk.parquet")
print("Saved TailRisk.parquet")

# PART 2: BETA REGRESSION WITH MONTHLY DATA  
print("📊 Part 2: Computing tail risk betas from monthly returns...")

# Load monthly CRSP data  
print("Loading monthlyCRSP.parquet...")
monthly_crsp = pl.read_parquet("../pyData/Intermediate/monthlyCRSP.parquet").select(["permno", "time_avail_m", "ret", "shrcd"])
print(f"Loaded monthly CRSP: {len(monthly_crsp):,} monthly observations")

# Merge with tail risk factor
print("Merging with tail risk factor...")
df = monthly_crsp.join(monthly_tailrisk, on="time_avail_m", how="left").sort(["permno", "time_avail_m"])
print(f"After merging: {len(df):,} observations")



# Convert time_avail_m to integer for window-based regression
# Time starts from Jan 1960 = 0
df = df.with_columns([
    ((pl.col("time_avail_m").dt.year() - 1960) * 12 + (pl.col("time_avail_m").dt.month() - 1)).alias("time_avail_m_int")
])

print(f"Computing rolling 120-month tail risk betas for {df['permno'].n_unique():,} unique permnos...")
print("Rolling 120-month regression windows with minimum 72 observations per permno")

# Apply direct polars-ols rolling regression
# Sort by permno and time_avail_m_int for deterministic window order
df = df.sort(["permno", "time_avail_m_int"])

df_with_beta = df.with_columns(
    pl.col("ret").least_squares.rolling_ols(
        pl.col("tailex"),
        window_size=120,
        min_periods=72,
        mode="coefficients",
        add_intercept=True,
        null_policy="drop"
    ).over("permno").alias("coef")
).with_columns([
    pl.col("coef").struct.field("const").alias("b_const"),
    pl.col("coef").struct.field("tailex").alias("b_tailex")
])

# Extract tail risk beta coefficient
df_with_beta = df_with_beta.with_columns(
    pl.col("b_tailex").alias("BetaTailRisk")
)

# Apply filters: remove missing betas and non-common stocks (shrcd > 11)
df_final = df_with_beta.filter(
    pl.col("BetaTailRisk").is_not_null() & 
    (pl.col("shrcd") <= 11)
).select(["permno", "time_avail_m", "BetaTailRisk"])


print(f"Generated BetaTailRisk values: {len(df_final):,} observations")

if len(df_final) > 0:
    # Convert to pandas for summary stats (maintaining compatibility with save_predictor)
    df_final_pd = df_final.to_pandas()
    
    print(f"BetaTailRisk summary stats:")
    print(f"  Mean: {df_final_pd['BetaTailRisk'].mean():.4f}")
    print(f"  Std: {df_final_pd['BetaTailRisk'].std():.4f}")
    print(f"  Min: {df_final_pd['BetaTailRisk'].min():.4f}")  
    print(f"  Max: {df_final_pd['BetaTailRisk'].max():.4f}")

    # SAVE
    print("💾 Saving BetaTailRisk predictor...")
    save_predictor(df_final_pd, "BetaTailRisk")
    print("✅ BetaTailRisk.csv saved successfully")
else:
    print("⚠️ No BetaTailRisk values generated - check data and parameters")
    
print("=" * 80)
print("✅ BetaTailRisk.py Complete")
print("Tail risk beta predictor generated using polars rolling window regression")
print("=" * 80)