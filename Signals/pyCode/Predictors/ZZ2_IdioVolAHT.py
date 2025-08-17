# ABOUTME: Idiosyncratic risk predictor using RMSE from 252-day rolling CAPM regression
# ABOUTME: Usage: python3 ZZ2_IdioVolAHT.py (run from pyCode/ directory)

import polars as pl
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'utils'))
from asreg import asreg
from savepredictor import save_predictor

# Debug constants - replace with actual problematic observation from test results
DEBUG_PERMNO = 10346  # Replace with actual value
DEBUG_YYYYMM = 199508  # Replace with actual value (e.g., 200704)
DEBUG_DATE = pl.date(DEBUG_YYYYMM//100, DEBUG_YYYYMM%100, 1)  # Convert to polars date

# Data load
daily_crsp = pl.read_parquet("../pyData/Intermediate/dailyCRSP.parquet")
daily_ff = pl.read_parquet("../pyData/Intermediate/dailyFF.parquet")

# TEMPORARILY REMOVE 5-year filter to debug superset issue
# daily_crsp = daily_crsp.filter(
#     (pl.col("time_d") >= pl.date(1981, 1, 1)) & 
#     (pl.col("time_d") <= pl.date(1985, 12, 31))
# )
# daily_ff = daily_ff.filter(
#     (pl.col("time_d") >= pl.date(1981, 1, 1)) & 
#     (pl.col("time_d") <= pl.date(1985, 12, 31))
# )

# Select required columns
df = daily_crsp.select(["permno", "time_d", "ret"])

# Merge with FF data
df = df.join(
    daily_ff.select(["time_d", "rf", "mktrf"]),
    on="time_d",
    how="inner"
)

# Calculate excess return (Stata: replace ret = ret - rf)
df = df.with_columns([
    (pl.col("ret") - pl.col("rf")).alias("ret")
])

# CHECKPOINT 1: After data merge and excess return calculation
print(f"CHECKPOINT 1: After data merge and excess return calculation for permno={DEBUG_PERMNO}")
checkpoint_data = df.filter(
    (pl.col("permno") == DEBUG_PERMNO) & 
    (pl.col("time_d") >= pl.date(1995, 7, 1)) & 
    (pl.col("time_d") <= pl.date(1995, 8, 31))
).head(10)
if checkpoint_data.height > 0:
    print(checkpoint_data.select(["permno", "time_d", "ret", "rf", "mktrf"]))
count_debug = df.filter(
    (pl.col("permno") == DEBUG_PERMNO) & 
    (pl.col("time_d") >= pl.date(1995, 7, 1)) & 
    (pl.col("time_d") <= pl.date(1995, 8, 31))
).height
print(f"Count for debug period: {count_debug}")

# Critical: Filter out missing returns before creating time index
# This ensures rolling windows contain exactly 252 valid observations
df = df.filter(pl.col("ret").is_not_null() & pl.col("mktrf").is_not_null())

# Critical: Sort data first (from Beta.py success pattern)
df = df.sort(["permno", "time_d"])

# Set up time index for rolling window (Stata: time_temp = _n)
df = df.with_columns([
    pl.int_range(pl.len()).over("permno").alias("time_temp")
])

# CHECKPOINT 2: After creating time position index
print(f"CHECKPOINT 2: After creating time position for permno={DEBUG_PERMNO}")
checkpoint_data = df.filter(
    (pl.col("permno") == DEBUG_PERMNO) & 
    (pl.col("time_d") >= pl.date(1995, 7, 1)) & 
    (pl.col("time_d") <= pl.date(1995, 8, 31))
).head(10)
if checkpoint_data.height > 0:
    print(checkpoint_data.select(["permno", "time_d", "time_temp", "ret"]))
permno_count = df.filter(pl.col("permno") == DEBUG_PERMNO).height
print(f"Total observations for permno {DEBUG_PERMNO}: {permno_count}")

# Use utils/asreg.py helper for rolling regression with RMSE
# This replicates: asreg ret mktrf, window(time_temp 252) min(100) by(permno) rmse
df = asreg(
    df,
    y="ret",  # Excess return (already calculated above)
    X=["mktrf"],
    by=["permno"],
    t="time_temp", 
    mode="rolling",
    window_size=252,
    min_samples=100,
    add_intercept=True,  # Stata's asreg includes intercept by default
    outputs=("rmse",),  # Only need RMSE output (equivalent to Stata's _rmse)
    coef_prefix="b_"
)

# CHECKPOINT 3: After rolling regression
print(f"CHECKPOINT 3: After rolling regression for permno={DEBUG_PERMNO}")
checkpoint_data = df.filter(
    (pl.col("permno") == DEBUG_PERMNO) & 
    (pl.col("time_d") >= pl.date(1995, 7, 1)) & 
    (pl.col("time_d") <= pl.date(1995, 8, 31))
).head(5)
if checkpoint_data.height > 0:
    print(checkpoint_data.select(["permno", "time_d", "time_temp", "rmse", "ret", "mktrf"]))
    summary = checkpoint_data.select([
        pl.col("rmse").count().alias("rmse_count"),
        pl.col("rmse").mean().alias("rmse_mean"),
        pl.col("rmse").std().alias("rmse_std")
    ])
    print("RMSE summary stats:", summary)
non_null_count = df.filter(
    (pl.col("permno") == DEBUG_PERMNO) & 
    (pl.col("rmse").is_not_null())
).height
print(f"Non-null RMSE for permno {DEBUG_PERMNO}: {non_null_count}")

# Extract IdioVolAHT from RMSE (rename _rmse IdioVolAHT in Stata)
df = df.with_columns([
    pl.col("rmse").alias("IdioVolAHT")
])

# Convert to monthly and keep last observation per month
df = df.with_columns([
    pl.col("time_d").dt.truncate("1mo").alias("time_avail_m")
])

# Keep last non-missing IdioVolAHT per permno-month (Stata: gcollapse (lastnm))
df = df.sort(["permno", "time_avail_m", "time_d"])
df = df.group_by(["permno", "time_avail_m"]).agg([
    pl.col("IdioVolAHT").drop_nulls().last().alias("IdioVolAHT")
])

# CHECKPOINT 4: Before final output
print(f"CHECKPOINT 4: Before final output for permno={DEBUG_PERMNO}")
checkpoint_data = df.filter(
    (pl.col("permno") == DEBUG_PERMNO) & 
    (pl.col("time_avail_m") == DEBUG_DATE)
)
if checkpoint_data.height > 0:
    print(checkpoint_data.select(["permno", "time_avail_m", "IdioVolAHT"]))
    summary = checkpoint_data.select([
        pl.col("IdioVolAHT").count().alias("count"),
        pl.col("IdioVolAHT").mean().alias("mean"),
        pl.col("IdioVolAHT").std().alias("std")
    ])
    print("Final predictor summary:", summary)
non_null_final = df.filter(
    (pl.col("permno") == DEBUG_PERMNO) & 
    (pl.col("IdioVolAHT").is_not_null())
).height
print(f"Non-null IdioVolAHT for permno {DEBUG_PERMNO}: {non_null_final}")

# Select final data
result = df.select(["permno", "time_avail_m", "IdioVolAHT"])

# Save predictor
save_predictor(result, "IdioVolAHT")