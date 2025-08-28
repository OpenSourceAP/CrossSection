#%%
# DEBUG

import os
os.chdir(os.path.dirname(__file__))
os.chdir('..')
os.getcwd()

#%%

# ABOUTME: Frazzini-Pedersen beta using rolling correlations and volatility ratios
# ABOUTME: Usage: python3 BetaFP.py (run from pyCode/ directory)

import polars as pl
import polars_ols  # Enable polars-ols functionality
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from utils.save_standardized import save_predictor

# Data load
daily_crsp = pl.read_parquet("../pyData/Intermediate/dailyCRSP.parquet")
daily_ff = pl.read_parquet("../pyData/Intermediate/dailyFF.parquet")

# Select required columns
df = daily_crsp.select(["permno", "time_d", "ret"])

# Merge with FF data
df = df.join(
    daily_ff.select(["time_d", "rf", "mktrf"]),
    on="time_d",
    how="inner"
)

# Calculate excess return
df = df.with_columns([
    (pl.col("ret") - pl.col("rf")).alias("ret"),
    pl.col("ret").log1p().alias("LogRet"),
    pl.col("mktrf").log1p().alias("LogMkt")
])

# Set up time index for rolling window
df = df.sort(["permno", "time_d"])
df = df.with_columns([
    pl.int_range(pl.len()).over("permno").alias("time_temp")
])

#%%

# Calculate 252-day rolling standard deviations
df = df.with_columns([
    pl.col("LogRet")
    .rolling_std(window_size=252, min_samples=120)
    .over("permno")
    .alias("sd252_LogRet"),
    pl.col("LogMkt")
    .rolling_std(window_size=252, min_samples=120)
    .over("permno")
    .alias("sd252_LogMkt")
])

# Create 3-day overlapping returns
df = df.with_columns([
    (pl.col("LogRet").shift(2).over("permno") + 
     pl.col("LogRet").shift(1).over("permno") + 
     pl.col("LogRet")).alias("tempRi"),
    (pl.col("LogMkt").shift(2).over("permno") + 
     pl.col("LogMkt").shift(1).over("permno") + 
     pl.col("LogMkt")).alias("tempRm")
])

# CHECKPOINT 1: Check tempRi and tempRm for bad observations
print("CHECKPOINT 1: tempRi and tempRm values for bad permnos")
checkpoint1_data = df.filter(
    pl.col("permno").is_in([14269, 13389, 11797, 11252, 20271]) &
    (pl.col("time_d") >= pl.date(1941, 11, 1)) &
    (pl.col("time_d") <= pl.date(1942, 3, 31))
).select(["permno", "time_d", "tempRi", "tempRm", "LogRet", "LogMkt"]).sort(["permno", "time_d"])
print(checkpoint1_data)


# Rolling regression on 1260-day window (5 years) with min 500 observations  
# Using 500 minimum to ensure we get enough observations in early periods
rolling_kwargs = polars_ols.RollingKwargs(
    window_size=1260,
    min_periods=500
)

# Calculate R-squared using simple correlation approach: R² = corr²
# This is mathematically equivalent to the regression R² and avoids numerical issues
df = df.with_columns([
    # Rolling correlation between tempRi and tempRm using covariance formula
    # corr = cov(x,y) / (std(x) * std(y))
    ((pl.col("tempRi") * pl.col("tempRm")).rolling_mean(window_size=1260, min_samples=500).over("permno") -
     pl.col("tempRi").rolling_mean(window_size=1260, min_samples=500).over("permno") *
     pl.col("tempRm").rolling_mean(window_size=1260, min_samples=500).over("permno")).alias("cov_temp"),
    
    pl.col("tempRi").rolling_std(window_size=1260, min_samples=500).over("permno").alias("std_tempRi"),
    pl.col("tempRm").rolling_std(window_size=1260, min_samples=500).over("permno").alias("std_tempRm")
])

df = df.with_columns([
    # R² = corr² = (cov / (std_x * std_y))²
    (pl.col("cov_temp") / (pl.col("std_tempRi") * pl.col("std_tempRm"))).pow(2).alias("_R2")
])

# CHECKPOINT 2: Check R2 and standard deviations for bad observations  
print("CHECKPOINT 2: R2 and standard deviations for bad permnos")
checkpoint2_data = df.filter(
    pl.col("permno").is_in([14269, 13389, 11797, 11252, 20271]) &
    (pl.col("time_d") >= pl.date(1941, 11, 1)) &
    (pl.col("time_d") <= pl.date(1942, 3, 31))
).select(["permno", "time_d", "_R2", "sd252_LogRet", "sd252_LogMkt"]).sort(["permno", "time_d"])
print(checkpoint2_data)


# Calculate Frazzini-Pedersen beta
df = df.with_columns([
    (pl.col("_R2").abs().sqrt() * (pl.col("sd252_LogRet") / pl.col("sd252_LogMkt"))).alias("BetaFP")
])

# CHECKPOINT 3: Check final BetaFP calculation for bad observations
print("CHECKPOINT 3: Final BetaFP values for bad permnos") 
checkpoint3_data = df.filter(
    pl.col("permno").is_in([14269, 13389, 11797, 11252, 20271]) &
    (pl.col("time_d") >= pl.date(1941, 11, 1)) &
    (pl.col("time_d") <= pl.date(1942, 3, 31))
).select(["permno", "time_d", "BetaFP", "_R2", "sd252_LogRet", "sd252_LogMkt"]).sort(["permno", "time_d"])
print(checkpoint3_data)


# Convert to monthly and keep last observation per month
df = df.with_columns([
    pl.col("time_d").dt.truncate("1mo").alias("time_avail_m")
])

# Keep last non-missing BetaFP per permno-month
df = df.sort(["permno", "time_avail_m", "time_d"])
df = df.group_by(["permno", "time_avail_m"]).agg([
    pl.col("BetaFP").drop_nulls().last().alias("BetaFP")
])

# CHECKPOINT 4: Check monthly aggregated BetaFP values for bad observations
print("CHECKPOINT 4: Monthly aggregated BetaFP values for bad permnos")
checkpoint4_data = df.filter(
    pl.col("permno").is_in([14269, 13389, 11797, 11252, 20271]) &
    (pl.col("time_avail_m") >= pl.date(1941, 12, 1)) &
    (pl.col("time_avail_m") <= pl.date(1942, 4, 30))
).select(["permno", "time_avail_m", "BetaFP"]).sort(["permno", "time_avail_m"])
print(checkpoint4_data)

# Select final data
result = df.select(["permno", "time_avail_m", "BetaFP"])


# Save predictor
save_predictor(result, "BetaFP")

#%%

# DEBUG: check out largest differences
# **Largest Differences Before 1950**:
# ```
#    permno  yyyymm    python     stata      diff
# 0   14269  194112  4.258444  5.277860 -1.019417
# 1   13389  194108  3.766282  2.927140  0.839142
# 2   14269  194201  3.999881  4.830401 -0.830520
# 3   11797  193702  2.478371  1.648720  0.829651
# 4   11252  194112  4.024742  4.843852 -0.819109
# 5   20271  194408  1.522680  2.332971 -0.810292
# 6   18649  193710  1.339925  2.143693 -0.803768
# 7   11797  193701  2.275098  1.506865  0.768232
# 8   12677  192910  0.713803  1.460106 -0.746303
# 9   14269  194202  4.036062  4.760625 -0.724563
# ```

result.dtypes

#%%
result.filter(
    pl.col("permno") == 14269,
    pl.col("time_avail_m") > pl.date(1941, 9, 1)
).sort("time_avail_m")

#%%