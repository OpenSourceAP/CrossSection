# %%
# ABOUTME: TrendFactor predictor using daily data with 11 moving averages and cross-sectional regressions
# ABOUTME: Usage: python3 TrendFactor.py (run from pyCode/ directory)
# inputs: dailyCRSP.parquet, SignalMasterTable.parquet
# outputs: TrendFactor.csv

import pandas as pd
import polars as pl
from polars import coalesce, col, lit  # for convenience
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", ".."))
from utils.save_standardized import save_predictor
from utils.stata_replication import stata_ineq_pl
from utils.asrol import asrol_fast
from utils.stata_replication import stata_quantile
from utils.asreg import asreg_collinear


# %%

print("=" * 80)
print("🏗️  TrendFactor.py")
print("Generating TrendFactor predictor using daily data with moving averages")
print("=" * 80)

print("📊 Loading daily CRSP data...")

# 1. Compute moving averages
# use permno time_d prc cfacpr using "$pathDataIntermediate/dailyCRSP", clear
daily_crsp = pl.read_parquet("../pyData/Intermediate/dailyCRSP.parquet")

# convert time_d to datetime[D]
# tbc: should standardize in DataDownloads
daily_crsp = daily_crsp.with_columns(col("time_d").cast(pl.Date).alias("time_d"))

df_daily = daily_crsp.select(["permno", "time_d", "prc", "cfacpr"])
print(f"Daily CRSP data: {len(df_daily):,} observations")

print("🔄 Computing adjusted prices and time variables...")

# Adjust prices for splits etc
# gen P = abs(prc)/cfacpr
df_daily = df_daily.with_columns((pl.col("prc").abs() / pl.col("cfacpr")).alias("P"))

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
df_daily_pd = df_daily.to_pandas()

for L in lag_lengths:
    print(f"  Computing {L}-day moving average...")
    # asrol P, window(time_temp `L') stat(mean) by(permno) gen(A_`L')
    df_daily_pd = asrol_fast(
        df_daily_pd,
        group_col="permno",
        time_col="time_temp",
        value_col="P",
        window=L,
        stat="mean",
        new_col_name=f"A_{L}",
        min_periods=1,  # Allow partial windows like Stata default
    )

# Convert back to polars
df_daily = pl.from_pandas(df_daily_pd).with_columns(
    col("time_avail_m").cast(pl.Date).alias("time_avail_m")
)

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

# %%

print(
    "📊 Creating monthly data with future returns and moving averages for regressions"
)

# 2. Run cross-sectional regressions on monthly data
# use permno time_avail_m ret prc exchcd shrcd mve_c using "$pathDataIntermediate/SignalMasterTable", clear
reg_input = pl.read_parquet(
    "../pyData/Intermediate/SignalMasterTable.parquet",
    columns=["permno", "time_avail_m", "ret", "prc", "exchcd", "shrcd", "mve_c"],
).with_columns(col("time_avail_m").cast(pl.Date).alias("time_avail_m"))

print("🎯 Computing size deciles based on NYSE stocks...")

# new, using stata_quantile function
qu10_data = reg_input.filter(pl.col("exchcd") == 1).to_pandas()
qu10_data = (
    qu10_data.groupby("time_avail_m")
    .agg(qu10=("mve_c", lambda x: stata_quantile(x, 0.10)))
    .reset_index()
)
qu10_data = pl.from_pandas(qu10_data).with_columns(
    col("time_avail_m").cast(pl.Date).alias("time_avail_m")
)

# Merge back
reg_input = reg_input.join(qu10_data, on="time_avail_m", how="left")


print("🔍 Applying filters for regression sample...")

# Filters need to be imposed here rather than at portfolio stage
reg_input = reg_input.filter(
    ((pl.col("exchcd") == 1) | (pl.col("exchcd") == 2) | (pl.col("exchcd") == 3))
    & ((pl.col("shrcd") == 10) | (pl.col("shrcd") == 11))
    & stata_ineq_pl(pl.col("prc").abs(), ">=", 5)
    & stata_ineq_pl(pl.col("mve_c"), ">=", pl.col("qu10"))
).drop(["exchcd", "shrcd", "qu10", "mve_c", "prc"])

print(f"After applying filters: {len(reg_input):,} observations")

# Merge moving averages
reg_input = reg_input.join(temp_ma, on=["permno", "time_avail_m"], how="inner")

print(f"After merging moving averages: {len(reg_input):,} observations")


print("Preparing for cross-sectional regression...")

print("Carefully creating fRet with left join")
# the cast(pl.Date) is important to ensure the merge works
reg_input = reg_input.sort(["permno", "time_avail_m"])
templead = (
    reg_input.with_columns(
        col("time_avail_m").dt.offset_by("-1mo").cast(pl.Date).alias("time_avail_m")
    )
    .rename({"ret": "fRet"})
    .select(["permno", "time_avail_m", "fRet"])
)

# left merge the fRet back into the original data
reg_input = reg_input.join(templead, on=["permno", "time_avail_m"], how="left").sort(
    ["time_avail_m", "permno"]
)


# %%

print("🔧 asreg regressions with asreg_collinear")

# bys time_avail_m: asreg fRet A_*
# Run cross-sectional regression by time_avail_m using asreg_collinear helper
feature_cols = [f"A_{L}" for L in lag_lengths]

betas_by_month = asreg_collinear(
    reg_input.to_pandas(),
    y="fRet",
    X="A_*",  # Will be expanded to all A_* columns
    by="time_avail_m",
    window=None,  # None means use all data per group (cross-sectional)
    add_constant=True,
    drop_collinear=True,
)
betas_by_month = pl.from_pandas(betas_by_month).with_columns(
    pl.col("time_avail_m").cast(pl.Date)
)

# %%

print("📊 Computing 12-month rolling averages of beta coefficients...")

# For each lag length, compute rolling mean of beta coefficients
# asrol _b_A_`L', window(time_avail_m -13 -1) stat(mean) gen(EBeta_`L')
# This excludes the current month (uses months t-13 to t-1)
# Use min_samples=1 to allow partial windows in early periods (matches Stata default behavior)
for L in lag_lengths:
    betas_by_month = betas_by_month.with_columns(
        pl.col(f"_b_A_{L}")
        .shift(1)  # Exclude current month
        .rolling_mean(
            window_size=12, min_samples=1
        )  # Allow partial windows to match Stata
        .alias(f"EBeta_{L}")
    )


# Keep only time and expected betas
ebeta_cols = [f"EBeta_{L}" for L in lag_lengths]
temp_beta = betas_by_month.select(["time_avail_m"] + ebeta_cols)

# %%

print("🎯 Computing TrendFactor as the smoothed regression model predictions")

# grab the moving averages for each permno-month and make long
cols_A = [col for col in reg_input.columns if col.startswith("A_")]
df_final = (
    reg_input.select(["permno", "time_avail_m"] + cols_A)
    .unpivot(index=["time_avail_m", "permno"], variable_name="name", value_name="MA")
    .with_columns(col("name").str.replace("A_", "").cast(pl.Int64).alias("lag"))
    .select(["permno", "time_avail_m", "lag", "MA"])
)

# convert smoothed betas to long
beta_long = betas_by_month.unpivot(
    index="time_avail_m", variable_name="name", value_name="EBeta"
).filter(col("name").str.starts_with("EBeta_")).with_columns(
    col("name").str.replace("EBeta_", "").cast(pl.Int64).alias("lag")
).select(
    ["time_avail_m", "lag", "EBeta"]
)

# join the betas to the moving averages and compute the trend factor
# if there are NAs, TrendFactor is null (not zero!)
df_final = df_final.join(beta_long, on=["time_avail_m", "lag"], how="left").with_columns(
    EBeta_MA = pl.col("EBeta") * pl.col("MA")
).group_by(["permno", "time_avail_m"]).agg(
    TrendFactor = col('EBeta_MA').sum(),
    N_MA_used = col('EBeta_MA').is_not_null().sum() # required since python sum of nulls is zero
).filter(col('N_MA_used') == 11) # 11 is the number of MA used in the regression

print(f"Generated TrendFactor values: {len(df_final):,} observations")

#%%

print("💾 Saving TrendFactor predictor...")
save_predictor(df_final, "TrendFactor")
print("✅ TrendFactor.csv saved successfully")
print("🎉 TrendFactor computation completed!")