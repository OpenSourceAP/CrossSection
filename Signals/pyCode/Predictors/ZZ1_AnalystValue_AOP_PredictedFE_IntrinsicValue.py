# ABOUTME: AnalystValue, AOP, PredictedFE following Frankel and Lee 1998 JAE, Tables 3D, 5C, 8A; IntrinsicValue placebo
# ABOUTME: Multi-stage equity valuation using analyst forecasts and cross-sectional forecast error prediction

import polars as pl
import polars_ols  # registers .least_squares namespace
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from utils.save_standardized import save_predictor, save_placebo
from utils.stata_fastxtile import fastxtile
from utils.stata_replication import relrank
from utils.winsor2 import winsor2

print("=" * 80)
print("🏗️  ZZ1_AnalystValue_AOP_PredictedFE_IntrinsicValue.py")
print("Generating analyst value predictors: AnalystValue, AOP, PredictedFE. Also the placebo IntrinsicValue.")
print("=" * 80)

print("📊 Preparing IBES forecast data...")

# Prep IBES FROE1 (1-year ahead EPS)
print("Loading IBES EPS Unadj for FROE1...")
ibes_eps = pl.read_parquet("../pyData/Intermediate/IBES_EPS_Unadj.parquet")

# Filter 1-year ahead forecasts from May statement periods
# Keep only forecasts extending beyond 30 days from statement period
froe1 = ibes_eps.filter(
    (pl.col("fpi") == "1") & 
    (pl.col("statpers").dt.month() == 5) &
    (pl.col("fpedats").is_not_null()) &
    (pl.col("fpedats") > pl.col("statpers") + pl.duration(days=30))
)

# Add 1-month conservative timing adjustment per original paper
froe1 = froe1.with_columns(
    pl.col("time_avail_m").dt.offset_by("1mo").alias("time_avail_m")
)

# rename meanest feps1
froe1 = froe1.select(["tickerIBES", "time_avail_m", "meanest"]).rename({"meanest": "feps1"})
print(f"FROE1 data: {len(froe1):,} observations")

# Prep IBES FROE2 (2-year ahead EPS)
print("Loading IBES EPS Unadj for FROE2...")
froe2 = ibes_eps.filter(
    (pl.col("fpi") == "2") & 
    (pl.col("statpers").dt.month() == 5)
)

froe2 = froe2.with_columns(
    pl.col("time_avail_m").dt.offset_by("1mo").alias("time_avail_m")
)

froe2 = froe2.select(["tickerIBES", "time_avail_m", "meanest"]).rename({"meanest": "feps2"})
print(f"FROE2 data: {len(froe2):,} observations")

# Prep IBES LTG (Long-term growth)
print("Loading IBES EPS Unadj for LTG...")
ltg = ibes_eps.filter(pl.col("fpi") == "0")
ltg = ltg.select(["tickerIBES", "time_avail_m", "meanest"]).rename({"meanest": "LTG"})
print(f"LTG data: {len(ltg):,} observations")

print("📊 Loading main data sources...")

# DATA LOAD
# Load master table with security identifiers and prices
signal_master = pl.read_parquet("../pyData/Intermediate/SignalMasterTable.parquet")
df = signal_master.select(["permno", "tickerIBES", "time_avail_m", "prc"])
print(f"SignalMasterTable: {len(df):,} observations")

# Add shares outstanding from CRSP 
crsp = pl.read_parquet("../pyData/Intermediate/monthlyCRSP.parquet")
df = df.join(crsp.select(["permno", "time_avail_m", "shrout"]), on=["permno", "time_avail_m"], how="left")

# Add accounting fundamentals from Compustat
m_compustat = pl.read_parquet("../pyData/Intermediate/m_aCompustat.parquet")
df = df.join(
    m_compustat.select(["permno", "time_avail_m", "ceq", "ib", "ibcom", "ni", "sale", "datadate", "dvc", "at"]), 
    on=["permno", "time_avail_m"], 
    how="left"
)

print(f"After merging CRSP and Compustat: {len(df):,} observations")

# Calculate 5-year sales growth
df = df.sort(["permno", "time_avail_m"])
df = df.with_columns(
    (pl.col("sale") / pl.col("sale").shift(60).over("permno")).alias("SG")
)

# Restrict to June observations
df = df.filter(pl.col("time_avail_m").dt.month() == 6)
print(f"After filtering to June observations: {len(df):,} observations")

# Merge with IBES data
# Add 1-year ahead earnings forecasts
df = df.join(froe1, on=["tickerIBES", "time_avail_m"], how="left")
# Add 2-year ahead earnings forecasts
df = df.join(froe2, on=["tickerIBES", "time_avail_m"], how="left")
# Add long-term growth forecasts
df = df.join(ltg, on=["tickerIBES", "time_avail_m"], how="left")

print(f"After merging IBES data: {len(df):,} observations")

print("🧮 Computing financial variables and screens...")

# Common screens and variables
# Sort data by firm and time for panel calculations
df = df.sort(["permno", "time_avail_m"])

# Calculate average book equity using 12-month lag
# Use current book equity for first observation per firm
# Calculate lagged book equity for 12-month average
# Since we filtered to June observations only, previous June is 1 position back
df = df.with_columns([
    pl.col("ceq").shift(1).over("permno").alias("l12_ceq"),
    pl.int_range(pl.len()).over("permno").alias("row_num")
])

df = df.with_columns(
    pl.when(pl.col("row_num") == 0)
    .then(pl.col("ceq"))
    .when(pl.col("l12_ceq").is_null())  # If previous year's ceq is missing, use current year only
    .then(pl.col("ceq"))
    .otherwise((pl.col("ceq") + pl.col("l12_ceq")) / 2)
    .alias("ceq_ave")
)

# Calculate market value of equity
df = df.with_columns(
    (pl.col("shrout") * pl.col("prc").abs()).alias("mve_permco")
)

# Calculate book-to-market ratio
df = df.with_columns(
    (pl.col("ceq") / pl.col("mve_permco")).alias("BM")
)

# Calculate dividend payout ratio
# Use alternative calculation when income is negative
df = df.with_columns(
    pl.when(pl.col("ibcom") < 0)
    .then(pl.col("dvc") / (0.06 * pl.col("at")))
    .otherwise(pl.col("dvc") / pl.col("ibcom"))
    .alias("k")
)

# Calculate return on equity using average book value
df = df.with_columns(
    (pl.col("ibcom") / pl.col("ceq_ave")).alias("ROE")
)

print("📈 Computing forecast-based equity values...")

# p 317 (Appendix) - Multi-stage equity valuation
# Calculate forecasted ROE for year 1
df = df.with_columns(
    (pl.col("feps1") * pl.col("shrout") / pl.col("ceq_ave")).alias("FROE1")
)

# Project book equity for year 1
df = df.with_columns(
    (pl.col("ceq") * (1 + pl.col("FROE1") * (1 - pl.col("k")))).alias("ceq1")
)

# Project book equity using historical ROE
df = df.with_columns(
    (pl.col("ceq") * (1 + pl.col("ROE") * (1 - pl.col("k")))).alias("ceq1h")
)

# Calculate forecasted ROE for year 2
df = df.with_columns(
    (pl.col("feps2") * pl.col("shrout") / ((pl.col("ceq1") + pl.col("ceq")) / 2)).alias("FROE2")
)

# Project book equity for year 2
df = df.with_columns(
    (pl.col("ceq1") * (1 + pl.col("FROE1") * (1 - pl.col("k")))).alias("ceq2")
)

# Project book equity year 2 using historical ROE
df = df.with_columns(
    (pl.col("ceq1h") * (1 + pl.col("ROE") * (1 - pl.col("k")))).alias("ceq2h")
)

# Calculate forecasted ROE for year 3 using long-term growth
# Use year 2 ROE when long-term growth missing
df = df.with_columns(
    pl.when(pl.col("LTG").is_null())
    .then(pl.col("FROE2"))
    .otherwise(pl.col("feps2") * (1 + pl.col("LTG")/100) * pl.col("shrout") / ((pl.col("ceq1") + pl.col("ceq2")) / 2))
    .alias("FROE3")
)

# Project book equity for year 3
df = df.with_columns(
    (pl.col("ceq2") * (1 + pl.col("FROE2") * (1 - pl.col("k")))).alias("ceq3")
)

print("🔍 Applying data screens...")

# Screens
# Apply data quality screens per original methodology
# Exclude extreme ROE values and missing forecast data
# Require June or later datadate and complete forecasts
df = df.filter(
    (pl.col("ceq") > 0) & (pl.col("ceq").is_not_null()) &
    ((pl.col("ROE").abs() <= 1) | pl.col("ROE").is_null()) & 
    ((pl.col("FROE1").abs() <= 1) | pl.col("FROE1").is_null()) & 
    ((pl.col("k") <= 1) | pl.col("k").is_null()) &
    (pl.col("datadate").dt.month() >= 6) &
    (pl.col("feps1").is_not_null()) & (pl.col("feps2").is_not_null())
)

print(f"After applying screens: {len(df):,} observations")

print("💰 Computing analyst and intrinsic values...")

# SIGNAL CONSTRUCTION (annual)
# footnote on p 294 describes r. I find value of r if constant r does not matter
df = df.with_columns(pl.lit(0.12).alias("r"))

# Fixed discount rate of 12% per Frankel and Lee (1998)
# Alternative: Risk adjustment based on book-to-market quintiles could be applied
# Higher book-to-market firms would get higher discount rates reflecting value premium

# p 290: formulas p 294: 3-stage for AnalystValue and 2-stage for IntrinsicValue
# Break down the complex calculations into steps for better debugging

# Calculate components for AnalystValue
df = df.with_columns([
    # Term 1: ceq1
    pl.col("ceq1").alias("av_term1"),
    # Term 2: (FROE1-r)/(1+r)*ceq1
    ((pl.col("FROE1") - pl.col("r")) / (1 + pl.col("r")) * pl.col("ceq1")).alias("av_term2"),
    # Term 3: (FROE2-r)/(1+r)^2*ceq2
    ((pl.col("FROE2") - pl.col("r")) / (1 + pl.col("r")).pow(2) * pl.col("ceq2")).alias("av_term3"),
    # Term 4: (FROE3-r)/(1+r)^2/r*ceq3
    ((pl.col("FROE3") - pl.col("r")) / (1 + pl.col("r")).pow(2) / pl.col("r") * pl.col("ceq3")).alias("av_term4")
])

# Sum the terms and divide by market value
df = df.with_columns(
    ((pl.col("av_term1") + pl.col("av_term2") + pl.col("av_term3") + pl.col("av_term4")) / pl.col("mve_permco"))
    .alias("AnalystValue")
)

# Calculate components for IntrinsicValue  
df = df.with_columns([
    # Term 1: ceq1h
    pl.col("ceq1h").alias("iv_term1"),
    # Term 2: (ROE-r)/(1+r)*ceq1h
    ((pl.col("ROE") - pl.col("r")) / (1 + pl.col("r")) * pl.col("ceq1h")).alias("iv_term2"),
    # Term 3: (ROE-r)/(1+r)/r*ceq2h
    ((pl.col("ROE") - pl.col("r")) / (1 + pl.col("r")) / pl.col("r") * pl.col("ceq2h")).alias("iv_term3")
])

# Sum the terms and divide by market value
df = df.with_columns(
    ((pl.col("iv_term1") + pl.col("iv_term2") + pl.col("iv_term3")) / pl.col("mve_permco"))
    .alias("IntrinsicValue")
)

# Calculate analyst optimism as scaled difference between valuations
df = df.with_columns(
    ((pl.col("AnalystValue") - pl.col("IntrinsicValue")) / pl.col("IntrinsicValue").abs()).alias("AOP")
)

print("🔮 Computing predicted forecast error...")

# ===============================================
# Predicted FE
# ===============================================

# Calculate forecast error as difference between forecasted and realized ROE
# Create time-based 12-month lag for FROE1 (not position-based)
df_lag = df.select(["permno", "time_avail_m", "FROE1"]).with_columns(
    pl.col("time_avail_m").dt.offset_by("12mo").alias("time_avail_m_future")
).select(["permno", "time_avail_m_future", "FROE1"]).rename({"time_avail_m_future": "time_avail_m", "FROE1": "FROE1_lag12"})

df = df.join(df_lag, on=["permno", "time_avail_m"], how="left")

df = df.with_columns(
    (pl.col("FROE1_lag12") - pl.col("ROE")).alias("FErr")
)

# Winsorize forecast errors at 1st and 99th percentiles within each time period
# This removes extreme outliers that could distort cross-sectional regressions
df = winsor2(df, ["FErr"], replace=True, trim=True, cuts=[1, 99], by=["time_avail_m"])

# Convert variables to relative ranks within each time period
# This standardizes variables for cross-sectional forecast error prediction
# Convert to pandas temporarily for relrank processing
df_pandas = df.to_pandas()
variables = ["SG", "BM", "AOP", "LTG"]
for var in variables:
    df_pandas = relrank(df_pandas, var, by="time_avail_m", out=f"rank{var}")
# Convert back to polars
df = pl.from_pandas(df_pandas)

# Lag for forecasting and run reg - create time-based 12-month lags
for var in variables:
    df_lag_rank = df.select(["permno", "time_avail_m", f"rank{var}"]).with_columns(
        pl.col("time_avail_m").dt.offset_by("12mo").alias("time_avail_m_future")
    ).select(["permno", "time_avail_m_future", f"rank{var}"]).rename({
        "time_avail_m_future": "time_avail_m", 
        f"rank{var}": f"lag{var}"
    })
    df = df.join(df_lag_rank, on=["permno", "time_avail_m"], how="left")

# Run cross-sectional regressions of forecast errors on lagged firm characteristics
# This estimates how firm characteristics predict analyst forecast errors
df = df.sort(["time_avail_m", "permno"])

# Use asreg helper with group mode  
df_with_predictions = df.with_columns(
    pl.col("FErr").least_squares.ols(
        pl.col("lagSG"), pl.col("lagBM"), pl.col("lagAOP"), pl.col("lagLTG"),
        mode="coefficients",
        add_intercept=True,
        null_policy="drop"
    ).over(['time_avail_m']).alias("coef")
).with_columns([
    pl.col("coef").struct.field("const").alias("b_const"),
    pl.col("coef").struct.field("lagSG").alias("b_lagSG"),
    pl.col("coef").struct.field("lagBM").alias("b_lagBM"),
    pl.col("coef").struct.field("lagAOP").alias("b_lagAOP"),
    pl.col("coef").struct.field("lagLTG").alias("b_lagLTG")
])

# Rename coefficient columns to match original names
df_with_predictions = df_with_predictions.rename({
    "b_const": "_b_cons",
    "b_lagSG": "_b_lagSG",
    "b_lagBM": "_b_lagBM", 
    "b_lagAOP": "_b_lagAOP",
    "b_lagLTG": "_b_lagLTG"
})

# Calculate predicted forecast error using cross-sectional regression coefficients
df_with_predictions = df_with_predictions.with_columns(
    (
        pl.col("_b_cons") + 
        pl.col("_b_lagSG") * pl.col("rankSG") +
        pl.col("_b_lagBM") * pl.col("rankBM") +
        pl.col("_b_lagAOP") * pl.col("rankAOP") +
        pl.col("_b_lagLTG") * pl.col("rankLTG")
    ).alias("PredictedFE")
)

print("📅 Expanding to monthly observations...")

# Expand each annual observation to 12 monthly observations
# Each predictor value applies for the 12 months following portfolio formation
df_expanded = df_with_predictions.with_columns(
    pl.col("time_avail_m").alias("tempTime")  # Keep original time for grouping
)

# Create 12 copies of each observation with month offsets 0-11
df_monthly = []
for month_offset in range(12):
    df_copy = df_expanded.with_columns(
        pl.col("tempTime").dt.offset_by(f"{month_offset}mo").alias("time_avail_m")
    )
    df_monthly.append(df_copy)

df_expanded = pl.concat(df_monthly)
df_expanded = df_expanded.drop(["tempTime"])

print("💾 Saving predictors...")

# Save multiple predictors
predictors = ["AnalystValue", "AOP", "PredictedFE"]

for predictor in predictors:
    result = df_expanded.select(["permno", "time_avail_m", predictor])
    valid_result = result.filter(pl.col(predictor).is_not_null())
    
    print(f"Generated {predictor}: {len(valid_result):,} observations")
    if len(valid_result) > 0:
        print(f"  Mean: {valid_result[predictor].mean():.6f}")
        print(f"  Std: {valid_result[predictor].std():.6f}")
    
    save_predictor(result, predictor)
    print(f"✅ {predictor}.csv saved successfully")

# Save IntrinsicValue as a placebo
result = df_expanded.select(["permno", "time_avail_m", "IntrinsicValue"])
valid_result = result.filter(pl.col("IntrinsicValue").is_not_null())
save_placebo(result, "IntrinsicValue")
print("✅ IntrinsicValue.csv saved successfully")

print("🎉 All analyst value predictors completed!")