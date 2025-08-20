# ABOUTME: Abnormal Accruals predictor using Xie (2001) cross-sectional regressions by year and industry
# ABOUTME: Usage: python3 ZZ2_AbnormalAccruals_AbnormalAccrualsPercent.py (run from pyCode/ directory)

import polars as pl
import pandas as pd
import numpy as np
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from utils.asreg import asreg
from utils.savepredictor import save_predictor
from utils.saveplacebo import save_placebo

print("=" * 80)
print("🏗️  ZZ2_AbnormalAccruals_AbnormalAccrualsPercent.py")
print("Generating Abnormal Accruals predictor using Xie (2001) methodology")
print("=" * 80)

# DATA LOAD
print("📊 Loading a_aCompustat data...")
# use gvkey permno time_avail_m fyear datadate at oancf fopt act che lct dlc ib sale ppegt ni sic using "$pathDataIntermediate/a_aCompustat", clear
df = pl.read_parquet("../pyData/Intermediate/a_aCompustat.parquet")
df = df.select(["gvkey", "permno", "time_avail_m", "fyear", "datadate", "at", "oancf", "fopt", 
               "act", "che", "lct", "dlc", "ib", "sale", "ppegt", "ni", "sic"])
print(f"Loaded a_aCompustat: {len(df):,} observations")

# merge 1:1 permno time_avail_m using "$pathDataIntermediate/SignalMasterTable", keep(master match) keepusing(exchcd)
signal_master = pl.read_parquet("../pyData/Intermediate/SignalMasterTable.parquet")
signal_master = signal_master.select(["permno", "time_avail_m", "exchcd"])

df = df.join(signal_master, on=["permno", "time_avail_m"], how="left")
print(f"After merging with SignalMasterTable: {len(df):,} observations")

# Sort by gvkey and fyear for lag operations
df = df.sort(["gvkey", "fyear"])

print("🧮 Computing abnormal accruals following Xie (2001)...")

# SIGNAL CONSTRUCTION
# xtset gvkey fyear

# Compute abnormal accruals for Xie (2001)
# gen tempCFO = oancf
# replace tempCFO = fopt - (act - l.act) + (che - l.che) + (lct - l.lct) - (dlc - l.dlc) if mi(tempCFO)
df = df.with_columns([
    # Create lagged variables
    pl.col("act").shift(1).over("gvkey").alias("l_act"),
    pl.col("che").shift(1).over("gvkey").alias("l_che"),
    pl.col("lct").shift(1).over("gvkey").alias("l_lct"),
    pl.col("dlc").shift(1).over("gvkey").alias("l_dlc"),
    pl.col("at").shift(1).over("gvkey").alias("l_at")
])

df = df.with_columns(
    pl.when(pl.col("oancf").is_not_null())
    .then(pl.col("oancf"))
    .otherwise(
        pl.col("fopt") - (pl.col("act") - pl.col("l_act")) + 
        (pl.col("che") - pl.col("l_che")) + (pl.col("lct") - pl.col("l_lct")) - 
        (pl.col("dlc") - pl.col("l_dlc"))
    )
    .alias("tempCFO")
)

# gen tempAccruals = (ib - tempCFO) / l.at
df = df.with_columns(
    ((pl.col("ib") - pl.col("tempCFO")) / pl.col("l_at")).alias("tempAccruals")
)

# gen tempInvTA = 1/l.at
df = df.with_columns(
    (1 / pl.col("l_at")).alias("tempInvTA")
)

# gen tempDelRev = (sale - l.sale)/l.at
df = df.with_columns([
    pl.col("sale").shift(1).over("gvkey").alias("l_sale")
])

df = df.with_columns(
    ((pl.col("sale") - pl.col("l_sale")) / pl.col("l_at")).alias("tempDelRev")
)

# gen tempPPE = ppegt/l.at
df = df.with_columns(
    (pl.col("ppegt") / pl.col("l_at")).alias("tempPPE")
)

# - CHECKPOINT 1: Check key variables after initial computation
print("=== CHECKPOINT 1: After initial variable computation ===")
checkpoint1_data = df.filter(
    ((pl.col("permno") == 84005) & (pl.col("fyear") == 2000)) |
    ((pl.col("permno") == 85712) & (pl.col("fyear") == 2000)) |
    ((pl.col("permno") == 77649) & (pl.col("fyear") == 1997))
)
if len(checkpoint1_data) > 0:
    print(checkpoint1_data.select(["gvkey", "permno", "fyear", "datadate", "tempCFO", "tempAccruals", "tempInvTA", "tempDelRev", "tempPPE"]))

print("📊 Applying winsorization at 0.1% and 99.9% levels...")

# winsor2 temp*, replace cuts(0.1 99.9) trim by(fyear)
# Note: Modified to better match Stata's behavior - trim rows where ANY variable is extreme
temp_cols = ["tempAccruals", "tempInvTA", "tempDelRev", "tempPPE"]

# First, identify rows to trim (if ANY temp variable is outside [0.1, 99.9] percentiles)
for year in df["fyear"].unique().to_list():
    year_mask = (df["fyear"] == year)
    year_data = df.filter(year_mask)
    
    # Mark rows to trim if ANY variable is outside range
    trim_mask = pl.lit(False)
    for col in temp_cols:
        col_data = year_data.filter(pl.col(col).is_not_null())[col].to_numpy()
        if len(col_data) > 0:
            p001 = np.percentile(col_data, 0.1)
            p999 = np.percentile(col_data, 99.9)
            trim_mask = trim_mask | ((pl.col(col) < p001) | (pl.col(col) > p999))
    
    # Apply trimming - set ALL temp variables to null for trimmed rows
    df = df.with_columns([
        pl.when(year_mask & trim_mask)
        .then(None)
        .otherwise(pl.col(c))
        .alias(c)
        for c in temp_cols
    ])

# - CHECKPOINT 2: Check variables after winsorization
print("=== CHECKPOINT 2: After winsorization ===")
checkpoint2_data = df.filter(
    ((pl.col("permno") == 84005) & (pl.col("fyear") == 2000)) |
    ((pl.col("permno") == 85712) & (pl.col("fyear") == 2000)) |
    ((pl.col("permno") == 77649) & (pl.col("fyear") == 1997))
)
if len(checkpoint2_data) > 0:
    print(checkpoint2_data.select(["gvkey", "permno", "fyear", "datadate", "tempCFO", "tempAccruals", "tempInvTA", "tempDelRev", "tempPPE"]))

print("🏭 Running cross-sectional regressions by year and industry (SIC2)...")

# destring sic, replace
# gen sic2 = floor(sic/100)
# Convert to pandas for proven SIC handling, then back to polars
df_pandas_temp = df.to_pandas()
df_pandas_temp['sic'] = pd.to_numeric(df_pandas_temp['sic'], errors='coerce')
df_pandas_temp['sic2'] = np.floor(df_pandas_temp['sic'] / 100).astype('Int32')
df = pl.from_pandas(df_pandas_temp)


# bys fyear sic2: asreg tempAccruals tempInvTA tempDelRev tempPPE, fitted
# This runs cross-sectional regressions by year and industry using enhanced asreg helper
df_with_residuals = asreg(
    df,
    y="tempAccruals",
    X=["tempInvTA", "tempDelRev", "tempPPE"],
    by=["fyear", "sic2"],
    mode="group",
    min_samples=1,  # Let all groups run, filter by _Nobs afterwards like Stata
    add_intercept=True,
    outputs=("resid",),
    null_policy="drop",  # Pass through the null policy like original
    solve_method="svd",   # Revert to original SVD method
    collect=True
)

# Add the observation count for filtering (replicating _Nobs from Stata asreg)
df_with_residuals = df_with_residuals.with_columns(
    pl.col("tempAccruals").count().over(["fyear", "sic2"]).alias("_Nobs")
)

# Rename residuals to match Stata's _residuals variable
df_with_residuals = df_with_residuals.with_columns(
    pl.col("resid").alias("_residuals")
).drop("resid")

# - CHECKPOINT 3: Check regression results and _Nobs before dropping
print("=== CHECKPOINT 3: After regression, before dropping _Nobs < 6 ===")
checkpoint3_data = df_with_residuals.filter(
    ((pl.col("permno") == 84005) & (pl.col("fyear") == 2000)) |
    ((pl.col("permno") == 85712) & (pl.col("fyear") == 2000)) |
    ((pl.col("permno") == 77649) & (pl.col("fyear") == 1997))
)
if len(checkpoint3_data) > 0:
    print(checkpoint3_data.select(["gvkey", "permno", "fyear", "sic2", "_Nobs", "_residuals"]))

# drop if _Nobs < 6 // p 360
df_with_residuals = df_with_residuals.filter(pl.col("_Nobs") >= 6)

# drop if exchcd == 3 & fyear < 1982
df_with_residuals = df_with_residuals.filter(
    ~((pl.col("exchcd") == 3) & (pl.col("fyear") < 1982))
)


# rename _residuals AbnormalAccruals
df_with_residuals = df_with_residuals.with_columns(
    pl.col("_residuals").alias("AbnormalAccruals")
)

# drop a few duplicates
# sort permno fyear
# by permno fyear: keep if _n == 1
df_with_residuals = df_with_residuals.sort(["permno", "fyear"])
df_with_residuals = df_with_residuals.group_by(["permno", "fyear"], maintain_order=True).first()

# - CHECKPOINT 4: Check final AbnormalAccruals before monthly expansion
print("=== CHECKPOINT 4: Final AbnormalAccruals values ===")
checkpoint4_data = df_with_residuals.filter(
    ((pl.col("permno") == 84005) & (pl.col("fyear") == 2000)) |
    ((pl.col("permno") == 85712) & (pl.col("fyear") == 2000)) |
    ((pl.col("permno") == 77649) & (pl.col("fyear") == 1997))
)
if len(checkpoint4_data) > 0:
    print(checkpoint4_data.select(["gvkey", "permno", "fyear", "datadate", "AbnormalAccruals"]))

print(f"After cross-sectional regressions and filtering: {len(df_with_residuals):,} observations")


# Abnormal Accruals Percent
# xtset permno fyear
# gen AbnormalAccrualsPercent = AbnormalAccruals*l.at/abs(ni)
df_with_residuals = df_with_residuals.sort(["permno", "fyear"])
df_with_residuals = df_with_residuals.with_columns([
    pl.col("at").shift(1).over("permno").alias("l_at_permno")
])

df_with_residuals = df_with_residuals.with_columns(
    (pl.col("AbnormalAccruals") * pl.col("l_at_permno") / pl.col("ni").abs())
    .alias("AbnormalAccrualsPercent")
)

print("📅 Expanding to monthly observations...")

# Expand to monthly - following Stata logic
# gen temp = 12
# expand temp
df_monthly = []
for i in range(12):
    df_copy = df_with_residuals.clone()
    df_copy = df_copy.with_columns(pl.lit(i).alias("month_offset"))
    df_monthly.append(df_copy)

df_expanded = pl.concat(df_monthly)

# Add month_offset to time_avail_m (equivalent to: bysort gvkey tempTime: replace time_avail_m = time_avail_m + _n - 1)
df_expanded = df_expanded.with_columns(
    pl.col("time_avail_m").dt.offset_by(pl.concat_str(pl.col("month_offset"), pl.lit("mo"))).alias("time_avail_m")
)

# bysort gvkey time_avail_m (datadate): keep if _n == _N
df_expanded = df_expanded.sort(["gvkey", "time_avail_m", "datadate"])
df_expanded = df_expanded.group_by(["gvkey", "time_avail_m"], maintain_order=True).last()

# bysort permno time_avail_m (datadate): keep if _n == _N
df_expanded = df_expanded.sort(["permno", "time_avail_m", "datadate"])
df_expanded = df_expanded.group_by(["permno", "time_avail_m"], maintain_order=True).last()

# Clean up columns
df_expanded = df_expanded.drop(["month_offset"])

# - CHECKPOINT 5: Check final monthly observations for problematic permnos
print("=== CHECKPOINT 5: Final monthly data for problematic observations ===")
# Filter for the problematic permnos and time range around their problem periods
checkpoint5_data = df_expanded.filter(
    ((pl.col("permno") == 84005) & 
     (pl.col("time_avail_m") >= pl.datetime(2001, 1, 1)) &
     (pl.col("time_avail_m") <= pl.datetime(2001, 12, 31))) |
    ((pl.col("permno") == 85712) & 
     (pl.col("time_avail_m") >= pl.datetime(2001, 1, 1)) &
     (pl.col("time_avail_m") <= pl.datetime(2001, 12, 31))) |
    ((pl.col("permno") == 77649) & 
     (pl.col("time_avail_m") >= pl.datetime(1997, 6, 1)) &
     (pl.col("time_avail_m") <= pl.datetime(1998, 6, 30)))
)
if len(checkpoint5_data) > 0:
    print(checkpoint5_data.select(["permno", "time_avail_m", "AbnormalAccruals"]).sort(["permno", "time_avail_m"]))

# Select and save AbnormalAccruals
result_aa = df_expanded.select(["permno", "time_avail_m", "AbnormalAccruals"])

print(f"Generated AbnormalAccruals values: {len(result_aa):,} observations")
valid_aa = result_aa.filter(pl.col("AbnormalAccruals").is_not_null())
print(f"Non-null AbnormalAccruals: {len(valid_aa):,} observations")

if len(valid_aa) > 0:
    print(f"AbnormalAccruals summary stats:")
    print(f"  Mean: {valid_aa['AbnormalAccruals'].mean():.6f}")
    print(f"  Std: {valid_aa['AbnormalAccruals'].std():.6f}")
    print(f"  Min: {valid_aa['AbnormalAccruals'].min():.6f}")
    print(f"  Max: {valid_aa['AbnormalAccruals'].max():.6f}")

print("💾 Saving AbnormalAccruals predictor...")
save_predictor(result_aa, "AbnormalAccruals")
print("✅ AbnormalAccruals.csv saved successfully")

# Also save AbnormalAccrualsPercent
result_aap = df_expanded.select(["permno", "time_avail_m", "AbnormalAccrualsPercent"])

print(f"Generated AbnormalAccrualsPercent values: {len(result_aap):,} observations")
valid_aap = result_aap.filter(pl.col("AbnormalAccrualsPercent").is_not_null())
print(f"Non-null AbnormalAccrualsPercent: {len(valid_aap):,} observations")

if len(valid_aap) > 0:
    print(f"AbnormalAccrualsPercent summary stats:")
    print(f"  Mean: {valid_aap['AbnormalAccrualsPercent'].mean():.6f}")
    print(f"  Std: {valid_aap['AbnormalAccrualsPercent'].std():.6f}")
    print(f"  Min: {valid_aap['AbnormalAccrualsPercent'].min():.6f}")
    print(f"  Max: {valid_aap['AbnormalAccrualsPercent'].max():.6f}")

print("💾 Saving AbnormalAccrualsPercent predictor...")
save_placebo(result_aap, "AbnormalAccrualsPercent")
print("✅ AbnormalAccrualsPercent.csv saved successfully")