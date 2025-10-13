# ABOUTME: ZZ2_IdioVolCAPM_ReturnSkewCAPM.py - calculates CAPM idiosyncratic volatility and skewness placebos
# ABOUTME: Python equivalent of ZZ2_IdioVolCAPM_ReturnSkewCAPM.do, translates line-by-line from Stata code

"""
ZZ2_IdioVolCAPM_ReturnSkewCAPM.py

Inputs:
    - ../pyData/Intermediate/dailyCRSP.parquet: permno, time_d, ret columns.
    - ../pyData/Intermediate/dailyFF.parquet: time_d, rf, mktrf columns.

Outputs:
    - ../pyData/Placebos/IdioVolCAPM.csv: permno, time_avail_m, IdioVolCAPM columns.
    - ../pyData/Placebos/ReturnSkewCAPM.csv: permno, time_avail_m, ReturnSkewCAPM columns.

How to run:
    cd Signals/pyCode
    source .venv/bin/activate
    python3 Placebos/ZZ2_IdioVolCAPM_ReturnSkewCAPM.py

Example:
    python3 Placebos/ZZ2_IdioVolCAPM_ReturnSkewCAPM.py
"""

import polars as pl
import polars_ols as pls  # Registers .least_squares namespace
import sys
import os

# Add parent directory to path to import utils
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from utils.save_standardized import save_placebo

print("Starting ZZ2_IdioVolCAPM_ReturnSkewCAPM.py")

# DATA LOAD
print("Loading dailyCRSP...")
daily_crsp = pl.read_parquet("../pyData/Intermediate/dailyCRSP.parquet").select(
    ["permno", "time_d", "ret"]
)
print(f"Loaded daily CRSP rows: {len(daily_crsp):,}")

print("Loading dailyFF...")
daily_ff = pl.read_parquet("../pyData/Intermediate/dailyFF.parquet").select(
    ["time_d", "rf", "mktrf"]
)
print(f"Loaded daily FF rows: {len(daily_ff):,}")

print("Merging with dailyFF...")
df = daily_crsp.join(daily_ff, on="time_d", how="inner")
print(f"After merge: {len(df):,} rows")

print("Computing excess returns...")
df = df.with_columns((pl.col("ret") - pl.col("rf")).alias("ret")).drop("rf")

print("Sorting and creating time_avail_m...")
df = (
    df.sort(["permno", "time_d"])
    .with_columns(pl.col("time_d").dt.truncate("1mo").alias("time_avail_m"))
)

# SIGNAL CONSTRUCTION
print("Running CAPM regressions by permno-month using polars_ols...")
group_cols = ["permno", "time_avail_m"]

df_with_residuals = df.with_columns(
    [
        pl.col("ret")
        .least_squares.ols(
            pl.col("mktrf"),
            mode="residuals",
            add_intercept=True,
            null_policy="drop",
        )
        .over(group_cols)
        .alias("_residuals"),
        pl.len().over(group_cols).alias("_Nobs"),
    ]
)

print("Filtering to groups with >=15 observations and valid residuals...")
df_filtered = df_with_residuals.filter(
    (pl.col("_Nobs") >= 15) & pl.col("_residuals").is_not_null()
)
print(f"Observations after filtering: {len(df_filtered):,}")

print("Aggregating residual moments to construct placebos...")
placebos = df_filtered.group_by(group_cols).agg(
    [
        pl.col("_residuals").std().alias("IdioVolCAPM"),
        pl.col("_residuals").skew().alias("ReturnSkewCAPM"),
    ]
)

if placebos.is_empty():
    print("WARNING: No placebo observations generated")
else:
    print(f"Generated {len(placebos):,} permno-month placebo rows")

# Prepare individual outputs
df_vol = placebos.select(["permno", "time_avail_m", "IdioVolCAPM"])
df_skew = placebos.select(["permno", "time_avail_m", "ReturnSkewCAPM"])

# SAVE
save_placebo(df_vol, "IdioVolCAPM")
save_placebo(df_skew, "ReturnSkewCAPM")

print(f"Generated {len(df_vol):,} IdioVolCAPM observations")
print(f"Generated {len(df_skew):,} ReturnSkewCAPM observations")
print("ZZ2_IdioVolCAPM_ReturnSkewCAPM.py completed")
