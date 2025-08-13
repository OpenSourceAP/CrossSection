# ABOUTME: Share Volume - volatility of share volume (vol/shrout) over 3 months
# ABOUTME: Usage: python3 ShareVol.py (run from pyCode/ directory)

import polars as pl
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'utils'))
from savepredictor import save_predictor

# Data load
signal_master = pl.read_parquet("../pyData/Intermediate/SignalMasterTable.parquet")
monthly_crsp = pl.read_parquet("../pyData/Intermediate/monthlyCRSP.parquet")

# Start with signal master table
df = signal_master.select(["permno", "time_avail_m", "sicCRSP", "exchcd"])

# Merge with monthly CRSP for volume and shares outstanding
df = df.join(
    monthly_crsp.select(["permno", "time_avail_m", "shrout", "vol"]),
    on=["permno", "time_avail_m"],
    how="inner"
)

# Sort by permno and time_avail_m (critical for proper lag operations)
df = df.sort(["permno", "time_avail_m"])

# Signal construction
# tempShareVol = (vol + l1.vol + l2.vol)/(3*shrout)*100
# Use time-based lags to match Stata's calendar-based lag operators

# Create time-based lag data for 1 and 2 months
df_l1 = df.select(["permno", "time_avail_m", "vol"]).with_columns([
    (pl.col("time_avail_m") + pl.duration(days=32)).dt.truncate("1mo").cast(pl.Datetime("ns")).alias("time_avail_m_lag1")
]).select(["permno", "time_avail_m_lag1", "vol"]).rename({"time_avail_m_lag1": "time_avail_m", "vol": "l1_vol"})

df_l2 = df.select(["permno", "time_avail_m", "vol"]).with_columns([
    (pl.col("time_avail_m") + pl.duration(days=62)).dt.truncate("1mo").cast(pl.Datetime("ns")).alias("time_avail_m_lag2")
]).select(["permno", "time_avail_m_lag2", "vol"]).rename({"time_avail_m_lag2": "time_avail_m", "vol": "l2_vol"})

# Merge lag data back
df = df.join(df_l1, on=["permno", "time_avail_m"], how="left")
df = df.join(df_l2, on=["permno", "time_avail_m"], how="left")

# Calculate tempShareVol - Stata's missing arithmetic: missing values in sum make result missing
df = df.with_columns([
    ((pl.col("vol") + pl.col("l1_vol") + pl.col("l2_vol")) / 
     (3 * pl.col("shrout")) * 100)
    .alias("tempShareVol")
])

# Drop if shrout changes in last 3 months
# Create time-based lag data for shrout
df_l1_shrout = df.select(["permno", "time_avail_m", "shrout"]).with_columns([
    (pl.col("time_avail_m") + pl.duration(days=32)).dt.truncate("1mo").cast(pl.Datetime("ns")).alias("time_avail_m_lag1")
]).select(["permno", "time_avail_m_lag1", "shrout"]).rename({"time_avail_m_lag1": "time_avail_m", "shrout": "l1_shrout"})

df_l2_shrout = df.select(["permno", "time_avail_m", "shrout"]).with_columns([
    (pl.col("time_avail_m") + pl.duration(days=62)).dt.truncate("1mo").cast(pl.Datetime("ns")).alias("time_avail_m_lag2")
]).select(["permno", "time_avail_m_lag2", "shrout"]).rename({"time_avail_m_lag2": "time_avail_m", "shrout": "l2_shrout"})

# Merge shrout lag data back
df = df.join(df_l1_shrout, on=["permno", "time_avail_m"], how="left")
df = df.join(df_l2_shrout, on=["permno", "time_avail_m"], how="left")

# dshrout = shrout != l1.shrout
df = df.with_columns([
    (pl.col("shrout") != pl.col("l1_shrout")).alias("dshrout"),
    (pl.col("l1_shrout") != pl.col("l2_shrout")).alias("l1_dshrout"),
    (pl.col("l2_shrout").shift(1).over("permno") != pl.col("l2_shrout")).alias("l2_dshrout")
])

# Set dshrout = 0 if _n == 1 (first observation for each permno)
df = df.with_columns([
    pl.int_range(pl.len()).over("permno").alias("obs_num")
])

df = df.with_columns([
    pl.when(pl.col("obs_num") == 0)  # 0-indexed, so first observation is 0
    .then(False)
    .otherwise(pl.col("dshrout"))
    .alias("dshrout")
])

# dropObs = 1 if (dshrout + l1.dshrout + l2.dshrout) > 0
# Create time-based lag data for dshrout
df_l1_dshrout = df.select(["permno", "time_avail_m", "dshrout"]).with_columns([
    (pl.col("time_avail_m") + pl.duration(days=32)).dt.truncate("1mo").cast(pl.Datetime("ns")).alias("time_avail_m_lag1")
]).select(["permno", "time_avail_m_lag1", "dshrout"]).rename({"time_avail_m_lag1": "time_avail_m", "dshrout": "l1_dshrout_real"})

df_l2_dshrout = df.select(["permno", "time_avail_m", "dshrout"]).with_columns([
    (pl.col("time_avail_m") + pl.duration(days=62)).dt.truncate("1mo").cast(pl.Datetime("ns")).alias("time_avail_m_lag2")
]).select(["permno", "time_avail_m_lag2", "dshrout"]).rename({"time_avail_m_lag2": "time_avail_m", "dshrout": "l2_dshrout_real"})

# Merge dshrout lag data back
df = df.join(df_l1_dshrout, on=["permno", "time_avail_m"], how="left")
df = df.join(df_l2_dshrout, on=["permno", "time_avail_m"], how="left")

df = df.with_columns([
    (pl.col("dshrout").cast(pl.Int32) + 
     pl.col("l1_dshrout_real").cast(pl.Int32).fill_null(0) + 
     pl.col("l2_dshrout_real").cast(pl.Int32).fill_null(0) > 0).alias("dropObs")
])

# Don't drop if first two months (_n == 1 | _n == 2)
df = df.with_columns([
    pl.when((pl.col("obs_num") == 0) | (pl.col("obs_num") == 1))  # 0-indexed
    .then(None)
    .otherwise(pl.col("dropObs"))
    .alias("dropObs")
])

# Drop if dropObs == 1
df = df.filter(
    (pl.col("dropObs") != True) | (pl.col("dropObs").is_null())
)

# Create ShareVol signal - matches Stata logic exactly
df = df.with_columns([
    pl.when(pl.col("tempShareVol") < 5)
    .then(0)
    .when(pl.col("tempShareVol") > 10)
    .then(1)
    .otherwise(None)
    .alias("ShareVol")
])

# Select final data
result = df.select(["permno", "time_avail_m", "ShareVol"])

# Save predictor
save_predictor(result, "ShareVol")