# ABOUTME: R&D ability predictor using Cohen, Diether and Malloy (2013) methodology
# ABOUTME: Usage: python3 RDAbility.py (run from pyCode/ directory)

import polars as pl
import polars_ols  # registers .least_squares namespace
import pandas as pd
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from utils.savepredictor import save_predictor
from utils.stata_fastxtile import fastxtile

print("=" * 80)
print("🏗️  RDAbility.py")
print("Generating R&D ability predictor using Cohen, Diether and Malloy (2013) methodology")
print("=" * 80)

# Data load
print("📊 Loading a_aCompustat data...")
df = pl.read_parquet("../pyData/Intermediate/a_aCompustat.parquet")
df = df.select(["gvkey", "permno", "time_avail_m", "fyear", "datadate", "xrd", "sale"])
print(f"Loaded Compustat: {len(df):,} observations")

# Sort by gvkey and fyear for lag operations
df = df.sort(["gvkey", "fyear"])

print("🧮 Signal construction following Stata logic line by line...")

# gen tempXRD = xrd
# replace tempXRD = . if tempXRD <0
df = df.with_columns(
    pl.when(pl.col("xrd") < 0).then(None).otherwise(pl.col("xrd")).alias("tempXRD")
)

# gen tempSale = sale
# replace tempSale = . if tempSale < 0
df = df.with_columns(
    pl.when(pl.col("sale") < 0).then(None).otherwise(pl.col("sale")).alias("tempSale")
)

# gen tempY = log(tempSale/l.tempSale)
df = df.with_columns([
    pl.col("tempSale").shift(1).over("gvkey").alias("lag_tempSale")
])

df = df.with_columns(
    (pl.col("tempSale") / pl.col("lag_tempSale")).log().alias("tempY")
)

# gen tempX = log(1 + tempXRD/tempSale)
df = df.with_columns(
    (1 + pl.col("tempXRD") / pl.col("tempSale")).log().alias("tempX")
)

# For each lag from 1 to 5, compute gammaAbility using rolling regression
for n in range(1, 6):
    print(f"Processing lag {n}...")
    
    # replace tempXLag = l`n'.tempX
    df = df.with_columns(
        pl.col("tempX").shift(n).over("gvkey").alias("tempXLag")
    )
    
    # Rolling regression: asreg tempY tempXLag, window(fyear 8) min(6) by(gvkey)
    # Use polars-ols for rolling regression with 8-year window
    df = df.with_columns(
        pl.col("tempY")
        .least_squares.rolling_ols(
            pl.col("tempXLag"),
            window_size=8,
            min_periods=6,
            mode="coefficients"
        )
        .over("gvkey")
        .alias("_b_coeffs")
    )
    
    # Extract coefficient (slope) - this is gammaAbility`n'
    df = df.with_columns(
        pl.col("_b_coeffs").struct.field("tempXLag").alias(f"gammaAbility{n}")
    )
    
    # replace tempNonZero = tempXLag >0 & !mi(tempXLag)
    df = df.with_columns(
        ((pl.col("tempXLag") > 0) & (pl.col("tempXLag").is_not_null())).alias("tempNonZero")
    )
    
    # asrol tempNonZero, window(fyear 8) min(6) by(gvkey) stat(mean) gen(tempMean)
    df = df.with_columns(
        pl.col("tempNonZero")
        .cast(pl.Float64)
        .rolling_mean(window_size=8, min_samples=6)
        .over("gvkey")
        .alias("tempMean")
    )
    
    # replace gammaAbility`n' = . if tempMean < .5 & !mi(tempMean)
    df = df.with_columns(
        pl.when((pl.col("tempMean") < 0.5) & (pl.col("tempMean").is_not_null()))
        .then(None)
        .otherwise(pl.col(f"gammaAbility{n}"))
        .alias(f"gammaAbility{n}")
    )
    
    # drop tempMean, _b_coeffs
    df = df.drop(["tempMean", "_b_coeffs"])

# drop temp*
df = df.drop(["tempXRD", "tempSale", "tempY", "tempX", "tempXLag", "lag_tempSale", "tempNonZero"])

# egen RDAbility = rowmean(gammaAbil*)
gamma_cols = [f"gammaAbility{n}" for n in range(1, 6)]
df = df.with_columns(
    pl.concat_list([pl.col(col) for col in gamma_cols])
    .list.mean()
    .alias("RDAbility")
)

# gen tempRD = xrd/sale
# replace tempRD = . if xrd <= 0
df = df.with_columns(
    pl.when(pl.col("xrd") <= 0)
    .then(None)
    .otherwise(pl.col("xrd") / pl.col("sale"))
    .alias("tempRD")
)

# egen tempRDQuant = fastxtile(tempRD), n(3) by(time_avail_m)
# Use robust fastxtile for tercile assignment (handles infinite values automatically)
# Convert to pandas properly with all needed columns, ensuring proper index alignment
df_pandas_full = df.to_pandas()
df_pandas_full['tempRDQuant'] = fastxtile(df_pandas_full, 'tempRD', by='time_avail_m', n=3)
# Convert back to polars, preserving all data integrity
df = pl.from_pandas(df_pandas_full)

# replace RDAbility = . if tempRDQuant != 3
df = df.with_columns(
    pl.when(pl.col("tempRDQuant") != 3)
    .then(None)
    .otherwise(pl.col("RDAbility"))
    .alias("RDAbility")
)

# replace RDAbility = . if xrd <=0
df = df.with_columns(
    pl.when(pl.col("xrd") <= 0)
    .then(None)
    .otherwise(pl.col("RDAbility"))
    .alias("RDAbility")
)

print("📅 Expanding to monthly observations...")

# Expand to monthly - following Stata logic
# gen temp = 12
# expand temp
# This means each annual observation becomes 12 monthly observations
df_monthly = []
for i in range(12):
    df_copy = df.clone()
    df_copy = df_copy.with_columns(pl.lit(i).alias("month_offset"))
    df_monthly.append(df_copy)

df_expanded = pl.concat(df_monthly)

# bysort gvkey tempTime: replace time_avail_m = time_avail_m + _n - 1
# This adds 0, 1, 2, ..., 11 months to time_avail_m for the 12 copies
# Add month_offset to time_avail_m
df_expanded = df_expanded.with_columns(
    pl.col("time_avail_m").dt.offset_by(pl.concat_str(pl.col("month_offset"), pl.lit("mo"))).alias("time_avail_m")
)

# bysort gvkey time_avail_m (datadate): keep if _n == _N
df_expanded = df_expanded.sort(["gvkey", "time_avail_m", "datadate"])
df_expanded = df_expanded.group_by(["gvkey", "time_avail_m"], maintain_order=True).last()

# bysort permno time_avail_m: keep if _n == 1
df_expanded = df_expanded.sort(["permno", "time_avail_m"])
df_expanded = df_expanded.group_by(["permno", "time_avail_m"], maintain_order=True).first()

# Clean up columns
df_expanded = df_expanded.drop(["month_offset", "tempRDQuant", "tempRD"])

# Select final data
result = df_expanded.select(["permno", "time_avail_m", "RDAbility"])

print(f"Generated RDAbility values: {len(result):,} observations")
valid_rd = result.filter(pl.col("RDAbility").is_not_null())
print(f"Non-null RDAbility: {len(valid_rd):,} observations")
if len(valid_rd) > 0:
    print(f"RDAbility summary stats:")
    print(f"  Mean: {valid_rd['RDAbility'].mean():.6f}")
    print(f"  Std: {valid_rd['RDAbility'].std():.6f}")
    print(f"  Min: {valid_rd['RDAbility'].min():.6f}")
    print(f"  Max: {valid_rd['RDAbility'].max():.6f}")

print("💾 Saving RDAbility predictor...")
save_predictor(result, "RDAbility")
print("✅ RDAbility.csv saved successfully")