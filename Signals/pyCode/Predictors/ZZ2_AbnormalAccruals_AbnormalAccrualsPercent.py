# ABOUTME: Abnormal Accruals predictor from Xie 2001 (AR), Table 3
# ABOUTME: Uses cross-sectional regressions by year and industry to calculate residual accruals after controlling for firm characteristics

import polars as pl
import polars_ols as pls  # Registers .least_squares namespace
import pandas as pd
import numpy as np
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from utils.save_standardized import save_predictor, save_placebo
from utils.stata_replication import fill_date_gaps_pl, stata_multi_lag
from utils.winsor2 import winsor2

print("=" * 80)
print("🏗️  ZZ2_AbnormalAccruals_AbnormalAccrualsPercent.py")
print("Generating Abnormal Accruals predictor using Xie (2001) methodology")
print("=" * 80)

# DATA LOAD
print("📊 Loading a_aCompustat data...")
# Load required Compustat annual data variables
df = pl.read_parquet("../pyData/Intermediate/a_aCompustat.parquet")
df = df.select(["gvkey", "permno", "time_avail_m", "fyear", "datadate", "at", "oancf", "fopt", 
               "act", "che", "lct", "dlc", "ib", "sale", "ppegt", "ni", "sic"])
print(f"Loaded a_aCompustat: {len(df):,} observations")

# Merge with exchange code data from SignalMasterTable
signal_master = pl.read_parquet("../pyData/Intermediate/SignalMasterTable.parquet")
signal_master = signal_master.select(["permno", "time_avail_m", "exchcd"])

df = df.join(signal_master, on=["permno", "time_avail_m"], how="left")

print(f"After merging with SignalMasterTable: {len(df):,} observations")

print("🧮 Computing abnormal accruals following Xie (2001)...")

# set up for lagging
df = df.with_columns(fyear_date = pl.date(pl.col("fyear"), 1, 1))
df = fill_date_gaps_pl(df, group_col="gvkey", time_col="fyear_date", period_str="12mo")
df = df.with_columns(pl.col("fyear").fill_null(strategy="forward").over("gvkey"))

# lag using stata_multi_lag utility
df = stata_multi_lag(df, group_col="gvkey", time_col="fyear_date", 
                     value_col=["act", "che", "lct", "dlc", "at"], 
                     lag_list=[1], prefix="l", fill_gaps=False, freq="Y")

# cash flow from operations and ratios
df = df.with_columns([
    # cash flow from operations (depends on the mnemonic of the time)
    pl.when(pl.col("oancf").is_not_null())
    .then(pl.col("oancf"))
    .otherwise(
        pl.col("fopt") - (pl.col("act") - pl.col("l1_act")) + 
        (pl.col("che") - pl.col("l1_che")) + (pl.col("lct") - pl.col("l1_lct")) - 
        (pl.col("dlc") - pl.col("l1_dlc"))
    )
    .alias("tempCFO"),
    
    # Generate 1/l.at
    (1 / pl.col("l1_at")).alias("tempInvTA")
])

# Generate (ib - tempCFO) / l.at
df = df.with_columns(
    ((pl.col("ib") - pl.col("tempCFO")) / pl.col("l1_at")).alias("tempAccruals")
)

# Generate (sale - l.sale)/l.at and ppegt/l.at
df = stata_multi_lag(df, group_col="gvkey", time_col="fyear_date", 
                     value_col=["sale"], lag_list=[1], prefix="l", fill_gaps=False, freq="Y")

df = df.with_columns([
    ((pl.col("sale") - pl.col("l1_sale")) / pl.col("l1_at")).alias("tempDelRev"),
    (pl.col("ppegt") / pl.col("l1_at")).alias("tempPPE")
])

print("📊 Applying winsorization at 0.1% and 99.9% levels...")

# Apply winsorization to handle extreme values - trim rows where ANY variable is extreme
temp_cols = ["tempAccruals", "tempInvTA", "tempDelRev", "tempPPE"]
df = winsor2(df, temp_cols, replace=True, trim=True, cuts=[0.1, 99.9], by=["fyear"])

print("🏭 Running cross-sectional regressions by year and industry (SIC2)...")

# Create 2-digit SIC code for industry grouping
# Convert to pandas for proven SIC handling, then back to polars
df_pandas_temp = df.to_pandas()
df_pandas_temp['sic'] = pd.to_numeric(df_pandas_temp['sic'], errors='coerce')
df_pandas_temp['sic2'] = np.floor(df_pandas_temp['sic'] / 100).astype('Int32')
df = pl.from_pandas(df_pandas_temp)


# Run cross-sectional regressions by year and industry to extract residuals
df_with_residuals = df.with_columns(
    pl.col("tempAccruals").least_squares.ols(
        pl.col("tempInvTA"), pl.col("tempDelRev"), pl.col("tempPPE"),
        mode="residuals",
        add_intercept=True,
        null_policy="drop"
    ).over(['fyear', 'sic2']).alias("resid")
)

# Add the observation count for filtering
df_with_residuals = df_with_residuals.with_columns(
    pl.col("tempAccruals").count().over(["fyear", "sic2"]).alias("_Nobs")
)

# Rename residuals for consistency
df_with_residuals = df_with_residuals.with_columns(
    pl.col("resid").alias("_residuals")
).drop("resid")

# Filter groups with insufficient observations (minimum 6 per Xie 2001)
df_with_residuals = df_with_residuals.filter(pl.col("_Nobs") >= 6)

# Remove NASDAQ observations before 1982 (data quality issues)
df_with_residuals = df_with_residuals.filter(
    ~((pl.col("exchcd") == 3) & (pl.col("fyear") < 1982))
)


# Set final AbnormalAccruals variable
df_with_residuals = df_with_residuals.with_columns(
    pl.col("_residuals").alias("AbnormalAccruals")
)

# Remove duplicates, keeping first observation per permno-fyear
df_with_residuals = df_with_residuals.sort(["permno", "fyear"])
df_with_residuals = df_with_residuals.group_by(["permno", "fyear"], maintain_order=True).first()

print(f"After cross-sectional regressions and filtering: {len(df_with_residuals):,} observations")

# Calculate Abnormal Accruals as percentage of net income
df_with_residuals = df_with_residuals.with_columns([
    pl.col("at").shift(1).over("permno").alias("l_at_permno"),
    (pl.col("AbnormalAccruals") * pl.col("at").shift(1).over("permno") / pl.col("ni").abs())
    .alias("AbnormalAccrualsPercent")
])


#%%
print("📅 Expanding to permno-monthly observations...")

df_expanded = fill_date_gaps_pl(df_with_residuals, group_col="permno", time_col="time_avail_m", period_str="1mo", end_padding="12mo")

# Fill forward AbnormalAccruals and AbnormalAccrualsPercent within each permno
df_expanded = df_expanded.sort(["permno", "time_avail_m"]).with_columns([
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