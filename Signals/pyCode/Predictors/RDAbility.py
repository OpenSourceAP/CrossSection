# ABOUTME: R&D ability predictor using Cohen, Diether and Malloy (2013) methodology
# ABOUTME: Usage: python3 RDAbility.py (run from pyCode/ directory)

import polars as pl
import pandas as pd
import numpy as np
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from utils.savepredictor import save_predictor
from utils.stata_fastxtile import fastxtile
from utils.asreg import asreg
from utils.asrol import asrol

print("=" * 80)
print("RDAbility.py")
print("Generating R&D ability predictor using Cohen, Diether and Malloy (2013) methodology")
print("=" * 80)

# DATA LOAD
print("Loading a_aCompustat data...")
df = pl.read_parquet("../pyData/Intermediate/a_aCompustat.parquet")
df = df.select(["gvkey", "permno", "time_avail_m", "fyear", "datadate", "xrd", "sale"])
print(f"Loaded Compustat: {len(df):,} observations")

# SIGNAL CONSTRUCTION - Following Stata code line by line with careful missing value handling

# xtset gvkey fyear - sort by gvkey fyear for lag operations
df = df.sort(["gvkey", "fyear"])

# gen tempXRD = xrd
df = df.with_columns(pl.col("xrd").alias("tempXRD"))

# replace tempXRD = . if tempXRD <0
# Critical fix: In Stata, missing values are treated as positive infinity
# So tempXRD < 0 is false for missing values, only affecting non-missing negative values
df = df.with_columns(
    pl.when((pl.col("tempXRD") < 0) & pl.col("tempXRD").is_not_null())
    .then(None)
    .otherwise(pl.col("tempXRD"))
    .alias("tempXRD")
)

# gen tempSale = sale
df = df.with_columns(pl.col("sale").alias("tempSale"))

# replace tempSale = . if tempSale < 0
# Same logic: only non-missing negative values become missing
df = df.with_columns(
    pl.when((pl.col("tempSale") < 0) & pl.col("tempSale").is_not_null())
    .then(None)
    .otherwise(pl.col("tempSale"))
    .alias("tempSale")
)

# gen tempY = log(tempSale/l.tempSale)
# Create lag first using shift
df = df.with_columns(
    pl.col("tempSale").shift(1).over("gvkey").alias("l_tempSale")
)

# Apply log to ratio - handle division and log issues carefully
df = df.with_columns(
    pl.when(
        pl.col("tempSale").is_not_null() & 
        pl.col("l_tempSale").is_not_null() & 
        (pl.col("l_tempSale") > 0) &
        (pl.col("tempSale") > 0)  # Add condition to exclude zero sales
    )
    .then((pl.col("tempSale") / pl.col("l_tempSale")).log())
    .otherwise(None)
    .alias("tempY")
)

# gen tempX = log(1 + tempXRD/tempSale)
df = df.with_columns(
    pl.when(
        pl.col("tempXRD").is_not_null() & 
        pl.col("tempSale").is_not_null() & 
        (pl.col("tempSale") > 0)
    )
    .then((1 + pl.col("tempXRD") / pl.col("tempSale")).log())
    .otherwise(None)
    .alias("tempX")
)

# gen tempNonZero = .
# gen tempXLag = .
df = df.with_columns([
    pl.lit(None, dtype=pl.Float64).alias("tempNonZero"),
    pl.lit(None, dtype=pl.Float64).alias("tempXLag")
])

print("Processing lag regressions...")

# Loop through each lag 1 to 5  
for n in range(1, 6):
    print(f"Processing lag {n}...")
    
    # replace tempXLag = l`n'.tempX
    df = df.with_columns(
        pl.col("tempX").shift(n).over("gvkey").alias("tempXLag")
    )
    
    # asreg tempY tempXLag, window(fyear 8) min(6) by(gvkey)
    result = asreg(
        df, 
        y="tempY", 
        X=["tempXLag"], 
        by=["gvkey"], 
        t="fyear",
        mode="rolling", 
        window_size=8, 
        min_samples=6,
        outputs=("coef",),
        coef_prefix="b_"
    )
    
    # rename _b_tempXLag gammaAbility`n'
    df = df.with_columns(
        result["b_tempXLag"].alias(f"gammaAbility{n}")
    )
    
    # replace tempNonZero = tempXLag >0 & !mi(tempXLag)
    # In Stata: missing values are handled explicitly
    df = df.with_columns(
        ((pl.col("tempXLag") > 0) & pl.col("tempXLag").is_not_null()).alias("tempNonZero")
    )
    
    # asrol tempNonZero, window(fyear 8) min(6) by(gvkey) stat(mean) gen(tempMean)
    # Use asrol_legacy for exact Stata behavior that matches asrol
    df_pandas = df.to_pandas()
    df_pandas = df_pandas.sort_values(['gvkey', 'fyear'])
    
    # Calculate rolling mean per gvkey with exactly 8-year window and min 6 observations (matches Stata asrol min(6))
    df_pandas = asrol(
        df_pandas,
        group_col='gvkey',
        time_col='fyear', 
        value_col='tempNonZero',
        window=8,
        stat='mean',
        new_col_name='tempMean',
        min_periods=6
    )
    
    df = pl.from_pandas(df_pandas)
    
    # replace gammaAbility`n' = . if tempMean < .5 & !mi(tempMean)
    # Critical fix: In Stata, missing tempMean is treated as positive infinity
    # So tempMean < 0.5 is false for missing values, condition only applies to non-missing
    df = df.with_columns(
        pl.when((pl.col("tempMean") < 0.5) & pl.col("tempMean").is_not_null())
        .then(None)
        .otherwise(pl.col(f"gammaAbility{n}"))
        .alias(f"gammaAbility{n}")
    )
    
    # drop tempMean
    df = df.drop("tempMean")

# drop temp* (except gamma columns)
df = df.drop(["tempXRD", "tempSale", "tempY", "tempX", "tempNonZero", "tempXLag", "l_tempSale"])

# egen RDAbility = rowmean(gammaAbil*)
gamma_cols = [f"gammaAbility{n}" for n in range(1, 6)]
df = df.with_columns(
    pl.concat_list([pl.col(col) for col in gamma_cols])
    .list.mean()
    .alias("RDAbility")
)


# gen tempRD = xrd/sale
df = df.with_columns(
    pl.when(
        pl.col("xrd").is_not_null() & 
        pl.col("sale").is_not_null() & 
        (pl.col("sale") > 0)
    )
    .then(pl.col("xrd") / pl.col("sale"))
    .otherwise(None)
    .alias("tempRD")
)

# replace tempRD = . if xrd <= 0
# Critical fix: In Stata, missing xrd is treated as positive infinity
# So xrd <= 0 is FALSE for missing values, meaning they stay unchanged
# Only non-missing values <= 0 should become missing
df = df.with_columns(
    pl.when((pl.col("xrd") <= 0) & pl.col("xrd").is_not_null())
    .then(None)
    .otherwise(pl.col("tempRD"))
    .alias("tempRD")
)

# egen tempRDQuant = fastxtile(tempRD), n(3) by(time_avail_m)
# Convert to pandas for fastxtile
df_pandas = df.to_pandas()
df_pandas['tempRDQuant'] = fastxtile(df_pandas, 'tempRD', by='time_avail_m', n=3)
df = pl.from_pandas(df_pandas)


# replace RDAbility = . if tempRDQuant != 3
# Critical fix: In Stata, missing tempRDQuant is treated as positive infinity
# So tempRDQuant != 3 is TRUE for missing values, making RDAbility missing
df = df.with_columns(
    pl.when((pl.col("tempRDQuant") != 3) | pl.col("tempRDQuant").is_null())
    .then(None)
    .otherwise(pl.col("RDAbility"))
    .alias("RDAbility")
)

# replace RDAbility = . if xrd <=0
# Critical fix: In Stata, missing xrd is treated as positive infinity  
# So xrd <= 0 is FALSE for missing values, meaning they stay unchanged
# Only non-missing values <= 0 should make RDAbility missing
df = df.with_columns(
    pl.when((pl.col("xrd") <= 0) & pl.col("xrd").is_not_null())
    .then(None)
    .otherwise(pl.col("RDAbility"))
    .alias("RDAbility")
)

# cap drop temp*
df = df.drop(["tempRD", "tempRDQuant"] + gamma_cols)

print("Expanding to monthly observations...")

# Critical section: Monthly expansion logic
# * Expand to monthly
# gen temp = 12
# expand temp
# This creates 12 copies of each observation

# First, debug the pre-expansion count
pre_expand_count = len(df)
print(f"Before expansion: {pre_expand_count:,} observations")

df_monthly = []
for i in range(12):
    df_copy = df.clone()
    df_copy = df_copy.with_columns(pl.lit(i).alias("expand_n"))
    df_monthly.append(df_copy)

df = pl.concat(df_monthly)
print(f"After expansion: {len(df):,} observations")


# drop temp
# gen tempTime = time_avail_m
df = df.with_columns(pl.col("time_avail_m").alias("tempTime"))

# bysort gvkey tempTime: replace time_avail_m = time_avail_m + _n - 1
# This adds the expand index (0-11) to each time_avail_m
df = df.with_columns(
    pl.col("time_avail_m").dt.offset_by(
        pl.concat_str(pl.col("expand_n"), pl.lit("mo"))
    ).alias("time_avail_m")
)

# drop tempTime
df = df.drop(["tempTime", "expand_n"])

print("Applying final filters...")

# bysort gvkey time_avail_m (datadate): keep if _n == _N
# Keep the last observation within each gvkey-time_avail_m group when sorted by datadate
df = df.sort(["gvkey", "time_avail_m", "datadate"])
df = df.group_by(["gvkey", "time_avail_m"], maintain_order=True).last()
print(f"After gvkey-time filter: {len(df):,} observations")

# bysort permno time_avail_m: keep if _n == 1
# Keep the first observation within each permno-time_avail_m group
df = df.sort(["permno", "time_avail_m"])
df = df.group_by(["permno", "time_avail_m"], maintain_order=True).first()
print(f"After permno-time filter: {len(df):,} observations")


# Select final columns
result = df.select(["permno", "time_avail_m", "RDAbility"])

print(f"Generated RDAbility values: {len(result):,} observations")
valid_rd = result.filter(pl.col("RDAbility").is_not_null())
print(f"Non-null RDAbility: {len(valid_rd):,} observations")
if len(valid_rd) > 0:
    print(f"RDAbility summary stats:")
    print(f"  Mean: {valid_rd['RDAbility'].mean():.6f}")
    print(f"  Std: {valid_rd['RDAbility'].std():.6f}")
    print(f"  Min: {valid_rd['RDAbility'].min():.6f}")
    print(f"  Max: {valid_rd['RDAbility'].max():.6f}")

print("Saving RDAbility predictor...")
save_predictor(result, "RDAbility")
print("RDAbility.csv saved successfully")