# ABOUTME: Price delay predictors using daily return regressions with market lags
# ABOUTME: Usage: python3 ZZ2_PriceDelaySlope_PriceDelayRsq_PriceDelayTstat.py (run from pyCode/ directory)
# ABOUTME: Options: --test-permnos N (run on first N permnos for testing)

import polars as pl
import polars_ols  # registers .least_squares namespace
import sys
import os
import argparse

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from utils.savepredictor import save_predictor

# Parse command line arguments
parser = argparse.ArgumentParser(
    description="Generate price delay predictors using daily data regressions"
)
parser.add_argument(
    "--test-permnos",
    type=int,
    help="Run on first N permnos for testing (default: all permnos)",
)
args = parser.parse_args()

print("=" * 80)
print("🏗️  ZZ2_PriceDelaySlope_PriceDelayRsq_PriceDelayTstat.py")
print("Generating price delay predictors using daily data regressions")
print("=" * 80)

# Global parameters from Stata code
nlag = 4
weightscale = 1

print("📊 Preparing daily Fama-French data with lags...")

# Prep mkt lag data
# use "$pathDataIntermediate/dailyFF", clear
daily_ff = pl.read_parquet("../pyData/Intermediate/dailyFF.parquet")
daily_ff = daily_ff.select(["time_d", "mktrf", "rf"]).sort("time_d")

# Create market return lags
for n in range(1, nlag + 1):
    daily_ff = daily_ff.with_columns(pl.col("mktrf").shift(n).alias(f"mktLag{n}"))

print(f"Daily FF data with {nlag} lags: {len(daily_ff):,} observations")

print("📊 Loading daily CRSP data...")

# Load daily crsp
daily_crsp = pl.read_parquet("../pyData/Intermediate/dailyCRSP.parquet")
df = daily_crsp.select(["permno", "time_d", "ret"])
print(f"Daily CRSP data: {len(df):,} observations")

# Merge with daily FF data
df = df.join(daily_ff, on="time_d", how="inner")

# replace ret = ret - rf
df = df.with_columns((pl.col("ret") - pl.col("rf")).alias("ret"))

print(f"After merging and adjusting returns: {len(df):,} observations")

# Optional permno filtering for testing
if args.test_permnos:
    print(f"\n🧪 TESTING MODE: Filtering to first {args.test_permnos} permnos...")
    # Get first N permnos deterministically
    unique_permnos = df.select("permno").unique().sort("permno").head(args.test_permnos)
    test_permno_list = unique_permnos.to_series().to_list()
    print(
        f"   Testing permnos: {test_permno_list[0]} to {test_permno_list[-1]} ({len(test_permno_list)} permnos)"
    )

    # Filter data to test permnos only
    df = df.filter(pl.col("permno").is_in(test_permno_list))
    print(f"   After filtering to test permnos: {len(df):,} observations")
else:
    print("\n📊 FULL DATASET MODE: Processing all permnos")

print("📅 Setting up time variables for June regressions...")

# Set up for Regressions in each June
# time_avail_m is the most next June after the obs
# Stata logic: time_avail_m = mofd(mdy(6,30,year(dofm(time_m+6))))
df = df.with_columns([pl.col("time_d").dt.truncate("1mo").alias("time_m")])

# Add 6 months to time_m, then extract the year, then create June of that year
df = df.with_columns(pl.col("time_m").dt.offset_by("6mo").alias("time_m_plus_6"))

df = df.with_columns(
    pl.datetime(pl.col("time_m_plus_6").dt.year(), 6, 30)
    .dt.truncate("1mo")
    .alias("time_avail_m")
)

print("🏃 Running regressions by group...")

# Sort for regressions
df = df.sort(["time_avail_m", "permno", "time_d"])

print("  Filtering groups with minimum 26 observations and data quality checks...")

# Count observations per group and check data quality
group_stats = df.group_by(["time_avail_m", "permno"]).agg(
    [
        pl.len().alias("group_count"),
        pl.col("ret").var().alias("ret_var"),
        pl.col("mktrf").var().alias("mktrf_var"),
        pl.col("ret").count().alias("ret_non_null"),
        pl.col("mktrf").count().alias("mktrf_non_null"),
    ]
)

# Filter to groups that meet all quality criteria:
# 1. >= 26 observations
# 2. Non-zero variance in both ret and mktrf
# 3. Sufficient non-null observations after dropna
valid_groups = group_stats.filter(
    (pl.col("group_count") >= 26)
    & (pl.col("ret_var") > 0)
    & (pl.col("mktrf_var") > 0)
    & (pl.col("ret_non_null") >= 26)
    & (pl.col("mktrf_non_null") >= 26)
    & (pl.col("ret_var").is_not_null())
    & (pl.col("mktrf_var").is_not_null())
)

print(f"Groups before quality filtering: {len(group_stats):,}")
print(f"Groups after quality filtering: {len(valid_groups):,}")
print(
    f"  Filtered out {len(group_stats) - len(valid_groups):,} groups with data quality issues"
)

# Ready for full dataset processing
print("🚀 Processing all valid groups")

# Keep only data for valid groups
df = df.join(
    valid_groups.select(["time_avail_m", "permno"]),
    on=["time_avail_m", "permno"],
    how="inner",
)
print(
    f"After filtering for minimum observations and data quality: {len(df):,} observations"
)

print("  Running regressions (one per group)...")

# Group by time_avail_m and permno, then run ONE regression per group
lag_features = [f"mktLag{n}" for n in range(1, nlag + 1)]

# Run restricted regression for each group using SVD for numerical stability
print(f"  Running restricted regressions on {len(valid_groups):,} groups...")
restricted_results = df.group_by(["time_avail_m", "permno"], maintain_order=True).agg(
    pl.col("ret")
    .least_squares.ols(
        "mktrf",
        mode="statistics",
        add_intercept=True,
        null_policy="drop",
        solve_method="svd",
    )
    .alias("_stats_restricted")
)

print(f"  Running unrestricted regressions on {len(valid_groups):,} groups...")
# Run unrestricted regression for each group using SVD for numerical stability
unrestricted_results = df.group_by(["time_avail_m", "permno"], maintain_order=True).agg(
    [
        pl.col("ret")
        .least_squares.ols(
            "mktrf",
            *lag_features,
            mode="coefficients",
            add_intercept=True,
            null_policy="drop",
            solve_method="svd",
        )
        .alias("_b_coeffs"),
        pl.col("ret")
        .least_squares.ols(
            "mktrf",
            *lag_features,
            mode="statistics",
            add_intercept=True,
            null_policy="drop",
            solve_method="svd",
        )
        .alias("_stats_unrestricted"),
    ]
)

# Combine results
df_results = restricted_results.join(
    unrestricted_results, on=["time_avail_m", "permno"], how="inner"
)

print("📊 Extracting coefficients and R-squared values...")

# Extract R-squared from statistics structures (field name is 'r2', not 'r_squared')
df_results = df_results.with_columns(
    [
        pl.col("_stats_restricted").struct.field("r2").alias("R2Restricted"),
        pl.col("_stats_unrestricted").struct.field("r2").alias("_R2"),
    ]
)

# Extract coefficients
coeff_extracts = [pl.col("_b_coeffs").struct.field("mktrf").alias("_b_mktrf")]
for n in range(1, nlag + 1):
    coeff_extracts.append(
        pl.col("_b_coeffs").struct.field(f"mktLag{n}").alias(f"_b_mktLag{n}")
    )

df_results = df_results.with_columns(coeff_extracts)

# Extract t-statistics from the unrestricted statistics
# The t_values field contains a list of t-statistics for each coefficient
# Order: [mktrf, mktLag1, mktLag2, mktLag3, mktLag4, const]
tstat_extracts = [
    pl.col("_stats_unrestricted").struct.field("t_values").list.get(0).alias("_t_mktrf")
]
for n in range(1, nlag + 1):
    tstat_extracts.append(
        pl.col("_stats_unrestricted")
        .struct.field("t_values")
        .list.get(n)
        .alias(f"_t_mktLag{n}")
    )
df_results = df_results.with_columns(tstat_extracts)

print("📅 Filtering for valid results and June endpoints...")

# Need to get the last observation date for each group to check if it's June
# Join back with original data to get time_d info
last_dates = df.group_by(["time_avail_m", "permno"], maintain_order=True).agg(
    pl.col("time_d").last().alias("last_time_d")
)

df_results = df_results.join(last_dates, on=["time_avail_m", "permno"], how="left")

# drop if _R2 == .
# keep if month(time_d) == 6 // drop if last obs is not June
df_monthly = df_results.filter(
    (pl.col("_R2").is_not_null()) & (pl.col("last_time_d").dt.month() == 6)
)

print(f"Monthly data after filtering: {len(df_monthly):,} observations")

print("🎯 Constructing price delay signals...")

# Construct D1: PriceDelayRsq
df_monthly = df_monthly.with_columns(
    (1 - pl.col("R2Restricted") / pl.col("_R2")).alias("PriceDelayRsq")
)

# Construct D2: PriceDelaySlope
weighted_terms_slope = []
lag_terms = []

for n in range(1, nlag + 1):
    weighted_terms_slope.append((n / weightscale) * pl.col(f"_b_mktLag{n}"))
    lag_terms.append(pl.col(f"_b_mktLag{n}"))

temp_sum1_slope = pl.sum_horizontal(weighted_terms_slope)
temp_sum2_slope = pl.sum_horizontal(lag_terms)

df_monthly = df_monthly.with_columns(
    (temp_sum1_slope / (pl.col("_b_mktrf") + temp_sum2_slope)).alias("PriceDelaySlope")
)

# Construct D3: PriceDelayTstat
weighted_terms_tstat = []
tstat_terms = []

for n in range(1, nlag + 1):
    weighted_terms_tstat.append((n / weightscale) * pl.col(f"_t_mktLag{n}"))
    tstat_terms.append(pl.col(f"_t_mktLag{n}"))

temp_sum1_tstat = pl.sum_horizontal(weighted_terms_tstat)
temp_sum2_tstat = pl.sum_horizontal(tstat_terms)

df_monthly = df_monthly.with_columns(
    (temp_sum1_tstat / (pl.col("_t_mktrf") + temp_sum2_tstat)).alias("PriceDelayTstat")
)

print("📊 Applying winsorization and time adjustment...")

# replace time_avail_m = time_avail_m + 1 // Hou and Moskowitz skip one month
df_monthly = df_monthly.with_columns(
    pl.col("time_avail_m").dt.offset_by("1mo").alias("time_avail_m")
)

print("📅 Forward-filling to monthly frequency...")

# Fill to monthly - Replicate Stata's xtset + tsfill + forward-fill behavior
# This is different from using SignalMasterTable - we create complete time series per permno
price_delay_cols = ["PriceDelaySlope", "PriceDelayRsq", "PriceDelayTstat"]
df_calc_values = df_monthly.select(["permno", "time_avail_m"] + price_delay_cols)

print(f"  Calculated values: {len(df_calc_values):,} observations")

# Replicate Stata's tsfill: create missing time periods within each permno's range
print("  Creating complete time series per permno (like Stata's tsfill)...")

# Get min/max time_avail_m for each permno
permno_ranges = df_calc_values.group_by("permno").agg(
    [
        pl.col("time_avail_m").min().alias("min_time"),
        pl.col("time_avail_m").max().alias("max_time"),
    ]
)

print(f"  Processing {len(permno_ranges)} permnos...")

# Use polars date_range for each permno - more reliable approach
expanded_data = []

# Process in smaller batches for memory efficiency
batch_size = 100
total_permnos = len(permno_ranges)

for batch_start in range(0, total_permnos, batch_size):
    batch_end = min(batch_start + batch_size, total_permnos)
    batch_ranges = permno_ranges.slice(batch_start, batch_end - batch_start)

    if batch_start % 1000 == 0:  # Progress indicator
        print(
            f"    Processing batch {batch_start//batch_size + 1}/{(total_permnos-1)//batch_size + 1}..."
        )

    for row in batch_ranges.iter_rows(named=True):
        permno = row["permno"]
        min_time = row["min_time"]
        max_time = row["max_time"]

        try:
            # Create monthly date range for this permno
            time_range = pl.date_range(min_time, max_time, interval="1mo", eager=True)

            batch_data = pl.DataFrame(
                {"permno": [permno] * len(time_range), "time_avail_m": time_range}
            )
            expanded_data.append(batch_data)

        except Exception as e:
            print(f"    Warning: Could not create range for permno {permno}: {e}")

# Combine all batches
if expanded_data:
    complete_grid = pl.concat(expanded_data)
    print(f"  Complete grid after tsfill: {len(complete_grid):,} observations")

    # Ensure matching datetime types for join
    complete_grid = complete_grid.with_columns(
        pl.col("time_avail_m").cast(pl.Datetime("us"))
    )
    df_calc_values = df_calc_values.with_columns(
        pl.col("time_avail_m").cast(pl.Datetime("us"))
    )

    # Join calculated values onto complete grid
    df_monthly = complete_grid.join(
        df_calc_values, on=["permno", "time_avail_m"], how="left"
    )

    print("  Forward-filling missing values within each permno...")
    # Forward-fill missing values within each permno (like Stata's forward-fill)
    df_monthly = df_monthly.sort(["permno", "time_avail_m"])
    for col in price_delay_cols:
        df_monthly = df_monthly.with_columns(pl.col(col).forward_fill().over("permno"))

    print(f"  After forward-filling: {len(df_monthly):,} observations")
else:
    print("  ⚠️  No valid permno ranges found")
    df_monthly = df_calc_values

print("💾 Saving price delay predictors...")

# Save all three predictors
for predictor in price_delay_cols:
    result = df_monthly.select(["permno", "time_avail_m", predictor])
    valid_result = result.filter(pl.col(predictor).is_not_null())

    print(f"Generated {predictor}: {len(valid_result):,} observations")
    if len(valid_result) > 0:
        print(f"  Mean: {valid_result[predictor].mean():.6f}")
        print(f"  Std: {valid_result[predictor].std():.6f}")

    save_predictor(result, predictor)
    print(f"✅ {predictor}.csv saved successfully")

print("🎉 All price delay predictors completed!")
