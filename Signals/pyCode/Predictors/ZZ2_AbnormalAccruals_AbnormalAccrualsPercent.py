# ABOUTME: Abnormal Accruals predictor using Xie (2001) cross-sectional regressions by year and industry
# ABOUTME: Usage: python3 ZZ2_AbnormalAccruals_AbnormalAccrualsPercent.py (run from pyCode/ directory)

import polars as pl
import polars_ols as pls  # Registers .least_squares namespace
import pandas as pd
import numpy as np
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from utils.save_standardized import save_predictor, save_placebo
from utils.stata_replication import fill_date_gaps_pl
from utils.winsor2 import winsor2

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

print("🧮 Computing abnormal accruals following Xie (2001)...")

# set up for lagging
df = df.with_columns(fyear_date = pl.date(pl.col("fyear"), 1, 1))
df = fill_date_gaps_pl(df, group_col="gvkey", time_col="fyear_date", period_str="12mo")
df = df.with_columns(pl.col("fyear").fill_null(strategy="forward").over("gvkey"))

# lag
df = df.with_columns([
    pl.col("act").shift(1).over("gvkey").alias("l_act"),
    pl.col("che").shift(1).over("gvkey").alias("l_che"),
    pl.col("lct").shift(1).over("gvkey").alias("l_lct"),
    pl.col("dlc").shift(1).over("gvkey").alias("l_dlc"),
    pl.col("at").shift(1).over("gvkey").alias("l_at")
])

# cash flow from operations (depends on the mnemonic of the time)
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

print("📊 Applying winsorization at 0.1% and 99.9% levels...")

# winsor2 temp*, replace cuts(0.1 99.9) trim by(fyear)
# Note: Modified to better match Stata's behavior - trim rows where ANY variable is extreme
temp_cols = ["tempAccruals", "tempInvTA", "tempDelRev", "tempPPE"]
df = winsor2(df, temp_cols, replace=True, trim=True, cuts=[0.1, 99.9], by=["fyear"])

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
df_with_residuals = df.with_columns(
    pl.col("tempAccruals").least_squares.ols(
        pl.col("tempInvTA"), pl.col("tempDelRev"), pl.col("tempPPE"),
        mode="residuals",
        add_intercept=True,
        null_policy="drop"
    ).over(['fyear', 'sic2']).alias("resid")
).filter(
    pl.col("tempAccruals").count().over(['fyear', 'sic2']) >= 1
),
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


#%%
print("📅 Expanding to permno-monthly observations...")

df_expanded = fill_date_gaps_pl(df_with_residuals, group_col="permno", time_col="time_avail_m", period_str="1mo", end_padding="12mo")

# Fill forward AbnormalAccruals and AbnormalAccrualsPercent within each permno
df_expanded = df_expanded.sort(["permno", "time_avail_m"])
df_expanded = df_expanded.with_columns([
    pl.col("AbnormalAccruals").fill_null(strategy="forward").over("permno"),
    pl.col("AbnormalAccrualsPercent").fill_null(strategy="forward").over("permno")
])

#%% 
# save

# not sure why, but we need to cast permno to int64
df_expanded = df_expanded.with_columns(pl.col("permno").cast(pl.Int64))

print("💾 Saving AbnormalAccruals predictor...")
save_predictor(df_expanded, "AbnormalAccruals")
print("✅ AbnormalAccruals.csv saved successfully")

print("💾 Saving AbnormalAccrualsPercent predictor...")
save_placebo(df_expanded, "AbnormalAccrualsPercent")
print("✅ AbnormalAccrualsPercent.csv saved successfully")

#%%

# sum statas

print(f"Generated AbnormalAccruals values: {len(df_expanded):,} observations")
valid_aa = df_expanded.filter(pl.col("AbnormalAccruals").is_not_null())
print(f"Non-null AbnormalAccruals: {len(valid_aa):,} observations")

if len(valid_aa) > 0:
    print(f"AbnormalAccruals summary stats:")
    print(f"  Mean: {valid_aa['AbnormalAccruals'].mean():.6f}")
    print(f"  Std: {valid_aa['AbnormalAccruals'].std():.6f}")
    print(f"  Min: {valid_aa['AbnormalAccruals'].min():.6f}")
    print(f"  Max: {valid_aa['AbnormalAccruals'].max():.6f}")


#%%
df_expanded.select(["permno", "time_avail_m", "AbnormalAccruals", "AbnormalAccrualsPercent"]).head(30)