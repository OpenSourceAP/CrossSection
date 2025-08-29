# %%
# ABOUTME: MS.py - generates Mohanram G-score predictor using 8 financial metrics
# ABOUTME: Python translation of MS.do with industry median comparisons and quarterly aggregation

"""
MS.py

Generates Mohanram G-score predictor from financial statement data:
- MS: Binary score (1-8) based on 8 financial strength indicators
- Sample: Lowest BM quintile only, minimum 3 firms per SIC2D-time
- Indicators: ROA, CF-ROA, cash flow quality, earnings volatility, revenue volatility, R&D intensity, capex intensity, advertising intensity
- All comparisons vs industry medians by (sic2D, time_avail_m)

Usage:
    cd pyCode/
    source .venv/bin/activate  
    python3 Predictors/MS.py

Inputs:
    - ../pyData/Intermediate/m_aCompustat.parquet (accounting data)
    - ../pyData/Intermediate/SignalMasterTable.parquet (mve_c, sicCRSP)
    - ../pyData/Intermediate/m_QCompustat.parquet (quarterly data)

Outputs:
    - ../pyData/Predictors/MS.csv

Requirements:
    - Lowest BM quintile sample selection
    - Industry median normalization for all 8 scores
    - Quarterly data aggregation using 12-month rolling means
    - Complex timing logic with seasonal adjustments
"""

import polars as pl
import pandas as pd
import numpy as np
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from utils.save_standardized import save_predictor
from utils.stata_fastxtile import fastxtile
from utils.stata_replication import stata_ineq_pl
from utils.asrol import asrol

print("=" * 80)
print("🏗️  MS.py")
print("Generating Mohanram G-score predictor")
print("=" * 80)

# DATA LOAD
print("📊 Loading Compustat and SignalMasterTable data...")

# Load annual Compustat data
print("Loading m_aCompustat.parquet...")
compustat = pl.read_parquet("../pyData/Intermediate/m_aCompustat.parquet").select([
    "permno", "gvkey", "time_avail_m", "datadate", "at", "ceq", "ni", "oancf", 
    "fopt", "wcapch", "ib", "dp", "xrd", "capx", "xad", "revt"
])
print(f"Loaded m_aCompustat: {len(compustat):,} observations")

# Deduplicate by permno-time_avail_m (following Stata logic)
compustat = compustat.unique(["permno", "time_avail_m"], keep="first")
print(f"After deduplication: {len(compustat):,} observations")

# Load SignalMasterTable for market value and SIC codes
print("Loading SignalMasterTable.parquet...")
smt = pl.read_parquet("../pyData/Intermediate/SignalMasterTable.parquet").select([
    "permno", "time_avail_m", "mve_c", "sicCRSP"
])
print(f"Loaded SignalMasterTable: {len(smt):,} observations")

# Load quarterly Compustat data
print("Loading m_QCompustat.parquet...")
qcompustat = pl.read_parquet("../pyData/Intermediate/m_QCompustat.parquet").select([
    "gvkey", "time_avail_m", "niq", "atq", "saleq", "oancfy", "capxy", "xrdq", 
    "fyearq", "fqtr", "datafqtr", "datadateq"
])
print(f"Loaded m_QCompustat: {len(qcompustat):,} observations")

# MERGE DATA
print("🔗 Merging datasets...")
df = (compustat
    .join(smt, on=["permno", "time_avail_m"], how="inner")
    .join(qcompustat, on=["gvkey", "time_avail_m"], how="left")
    .sort(["permno", "time_avail_m"])
)
print(f"After merging: {len(df):,} observations")

# SAMPLE SELECTION
print("🎯 Applying sample selection criteria...")

# Limit sample to firms in the lowest BM quintile (see p 8 OP)
# (has to be done first!, see also MP)
df = df.with_columns([
    (pl.col("ceq") / pl.col("mve_c")).log().alias("BM")
]).filter(
    pl.col("ceq") > 0  # Positive book equity
)

# Calculate BM quintiles using enhanced fastxtile (pandas-based for accuracy)
# Convert to pandas temporarily for quintile calculation
print("Calculating BM quintiles with enhanced fastxtile...")
df_pd = df.to_pandas()

# Clean infinite BM values explicitly (following successful PS pattern)
df_pd['BM_clean'] = df_pd['BM'].replace([np.inf, -np.inf], np.nan)

# Use enhanced fastxtile for quintile assignment
df_pd['BM_quintile'] = fastxtile(df_pd, 'BM_clean', by='time_avail_m', n=5)

# Convert back to polars and filter for lowest quintile
df = pl.from_pandas(df_pd).filter(
    pl.col("BM_quintile") == 1  # Keep only lowest BM quintile (growth firms)
)


print(f"After BM quintile filter: {len(df):,} observations")

# keep if at least 3 firms in sic2D (p 8)
df = df.with_columns(
    pl.col("sicCRSP").cast(pl.Utf8).str.slice(0, 2).alias("sic2D")
).with_columns(
    pl.len().over(["sic2D", "time_avail_m"]).alias("sic2D_count")
).filter(
    pl.col("sic2D_count") >= 3
)

print(f"After SIC2D minimum filter: {len(df):,} observations")

# PREP VARIABLES
print("🧮 Preparing financial variables...")

# Handle missing values for optional items (following Stata logic)
df = df.with_columns([
    pl.col("xad").fill_null(0.0),
    pl.col("xrdq").fill_null(0.0)
])

# Create quarterly capx and oancf from annual data based on fiscal quarter
# This follows the "locating oancfq" logic from WRDS
df = df.with_columns([
    # capxq: If Q1, use capxy directly. If Q>1, use capxy - lag3(capxy)
    pl.when(pl.col("fqtr") == 1)
    .then(pl.col("capxy"))
    .when((pl.col("fqtr") > 1) & pl.col("fqtr").is_not_null())
    .then(pl.col("capxy") - pl.col("capxy").shift(3).over("permno"))
    .otherwise(pl.lit(None))
    .alias("capxq"),
    
    # oancfq: Same logic as capxq
    pl.when(pl.col("fqtr") == 1)
    .then(pl.col("oancfy"))
    .when((pl.col("fqtr") > 1) & pl.col("fqtr").is_not_null())
    .then(pl.col("oancfy") - pl.col("oancfy").shift(3).over("permno"))
    .otherwise(pl.lit(None))
    .alias("oancfq")
])

print("📈 Computing quarterly aggregations...")

# Aggregate quarterly data using time-based rolling to match Stata's asrol behavior
# Stata's asrol window(time_avail_m 12) min(12) requires exactly 12 observations
# spanning 12 calendar months, not just 12 consecutive data points

# compute rolling means (be strict on windows)
df = asrol(df, 'permno', 'time_avail_m', '1mo', 12, 'niq', 'mean', 'niqsum', min_samples=12)
df = asrol(df, 'permno', 'time_avail_m', '1mo', 12, 'xrdq', 'mean', 'xrdqsum', min_samples=12)
df = asrol(df, 'permno', 'time_avail_m', '1mo', 12, 'oancfq', 'mean', 'oancfqsum', min_samples=12)
df = asrol(df, 'permno', 'time_avail_m', '1mo', 12, 'capxq', 'mean', 'capxqsum', min_samples=12)

# multiply the means by 4 to convert to sums (to match stata)
for col in ['niqsum', 'xrdqsum', 'oancfqsum', 'capxqsum']:
    df = df.with_columns(
        pl.col(col) * 4
    )

# Handle special case for early years (see OP endnote 3)
df = df.with_columns(
    pl.when(pl.col("datadate").dt.year() <= 1988)
    .then(pl.col("fopt") - pl.col("wcapch"))
    .otherwise(pl.col("oancfqsum"))
    .alias("oancfqsum")
)

# ================================================================
# SIGNAL CONSTRUCTION
# ================================================================

print("🎯 Constructing Mohanram G-score components...")

# ----------------------------------------------------------------
# PROFITABILITY AND CASH FLOW SIGNALS
# ----------------------------------------------------------------
print("  Computing profitability and cash flow signals...")

# OP uses annualized financials, but shouldn't much difference...
# atdenom needs to be done later?
df = df.with_columns([
    ((pl.col("atq") + pl.col("atq").shift(3).over("permno")) / 2).alias("atdenom")
])

# Calculate ROA and CF-ROA
df = df.with_columns([
    (pl.col("niqsum") / pl.col("atdenom")).alias("roa"),
    (pl.col("oancfqsum") / pl.col("atdenom")).alias("cfroa")
])

# Calculate industry medians for profitability measures
for v in ["roa", "cfroa"]:
    df = df.with_columns(
        pl.col(v).median().over(["sic2D", "time_avail_m"]).alias(f"md_{v}")
    )

# Create binary indicators m1, m2, m3
df = df.with_columns([
    pl.lit(0).alias("m1"),
    pl.lit(0).alias("m2"),
    pl.lit(0).alias("m3")
])

df = df.with_columns([
    pl.when(stata_ineq_pl(pl.col("roa"), ">", pl.col("md_roa"))).then(pl.lit(1)).otherwise(pl.col("m1")).alias("m1"),
    pl.when(stata_ineq_pl(pl.col("cfroa"), ">", pl.col("md_cfroa"))).then(pl.lit(1)).otherwise(pl.col("m2")).alias("m2"),
    pl.when(stata_ineq_pl(pl.col("oancfqsum"), ">", pl.col("niqsum"))).then(pl.lit(1)).otherwise(pl.col("m3")).alias("m3")
])

# ----------------------------------------------------------------
# "NAIVE EXTRAPOLATION" ACCORDING TO OP
# ----------------------------------------------------------------
print("  Computing naive extrapolation (volatility) measures...")

# Quarterly is used here
df = df.with_columns([
    (pl.col("niq") / pl.col("atq")).alias("roaq"),
    (pl.col("saleq") / pl.col("saleq").shift(3).over("permno")).alias("sg")
])

# Calculate 48-month rolling volatility using asrol_custom
print("    Calculating 48-month rolling volatility...")
df = asrol(df, 'permno', 'time_avail_m', '1mo', 49, 'roaq', 'std', 'niVol', min_samples=18)
df = asrol(df, 'permno', 'time_avail_m', '1mo', 49, 'sg', 'std', 'revVol', min_samples=18)

# Calculate industry medians for volatility measures
for v in ["niVol", "revVol"]:
    df = df.with_columns(
        pl.col(v).median().over(["sic2D", "time_avail_m"]).alias(f"md_{v}")
    )

# Create binary indicators m4, m5
df = df.with_columns([
    pl.lit(0).alias("m4"),
    pl.lit(0).alias("m5")
])

df = df.with_columns([
    pl.when(stata_ineq_pl(pl.col("niVol"), "<", pl.col("md_niVol"))).then(pl.lit(1)).otherwise(pl.col("m4")).alias("m4"),
    pl.when(stata_ineq_pl(pl.col("revVol"), "<", pl.col("md_revVol"))).then(pl.lit(1)).otherwise(pl.col("m5")).alias("m5")
])

# ----------------------------------------------------------------
# "CONSERVATISM" ACCORDING TO OP
# ----------------------------------------------------------------
print("  Computing conservatism (intensity) measures...")

# OP also uses annualized financials here
df = df.with_columns([
    pl.col("atq").shift(3).over("permno").alias("atdenom2")  # (OP p5)
])

df = df.with_columns([
    (pl.col("xrdqsum") / pl.col("atdenom2")).alias("xrdint"),
    (pl.col("capxqsum") / pl.col("atdenom2")).alias("capxint"),
    (pl.col("xad") / pl.col("atdenom2")).alias("xadint")  # I can't find xadq or xady
])

# Calculate industry medians for intensity measures
for v in ["xrdint", "capxint", "xadint"]:
    df = df.with_columns(
        pl.col(v).median().over(["sic2D", "time_avail_m"]).alias(f"md_{v}")
    )

# Create binary indicators m6, m7, m8
df = df.with_columns([
    pl.lit(0).alias("m6"),
    pl.lit(0).alias("m7"),
    pl.lit(0).alias("m8")
])

df = df.with_columns([
    pl.when(stata_ineq_pl(pl.col("xrdint"), ">", pl.col("md_xrdint"))).then(pl.lit(1)).otherwise(pl.col("m6")).alias("m6"),
    pl.when(stata_ineq_pl(pl.col("capxint"), ">", pl.col("md_capxint"))).then(pl.lit(1)).otherwise(pl.col("m7")).alias("m7"),
    pl.when(stata_ineq_pl(pl.col("xadint"), ">", pl.col("md_xadint"))).then(pl.lit(1)).otherwise(pl.col("m8")).alias("m8")
])

# Sum the 8 components to get tempMS
df = df.with_columns(
    (pl.col("m1") + pl.col("m2") + pl.col("m3") + pl.col("m4") + 
     pl.col("m5") + pl.col("m6") + pl.col("m7") + pl.col("m8")).alias("tempMS")
)


# ================================================================
# TIMING LOGIC
# ================================================================
print("📅 Applying timing logic...")

# Fix tempMS at most recent data release for entire year
# Timing is confusing compared to OP because of the mix of annual and quarterly
# data with different lags. This approach gets t-stats closest to op
for v in ["tempMS"]:
    # Replace tempMS with None if month doesn't match (datadate + 6 months) mod 12
    df = df.with_columns([
        pl.when(pl.col("time_avail_m").dt.month() != ((pl.col("datadate").dt.month() + 6) % 12))
        .then(pl.lit(None))
        .otherwise(pl.col(v))
        .alias(v)
    ])
    
    # Forward fill tempMS within permno groups
    df = df.with_columns(
        pl.col(v).forward_fill().over("permno").alias(v)
    )

# Create final MS score
df = df.with_columns(
    pl.col("tempMS").alias("MS")
)

# Apply upper and lower bounds
df = df.with_columns([
    pl.when((pl.col("tempMS") >= 6) & (pl.col("tempMS") <= 8))
    .then(pl.lit(6))
    .otherwise(pl.col("MS"))
    .alias("MS")
])

df = df.with_columns([
    pl.when(pl.col("tempMS") <= 1)
    .then(pl.lit(1))
    .otherwise(pl.col("MS"))
    .alias("MS")
])

# ================================================================
# FINAL OUTPUT
# ================================================================

# Select final columns
df_final = df.select(["permno", "time_avail_m", "MS"]).filter(
    pl.col("MS").is_not_null()
)

print(f"Generated MS values: {len(df_final):,} observations")
print(f"MS summary stats:")
print(f"  Mean: {df_final['MS'].mean():.4f}")
print(f"  Std: {df_final['MS'].std():.4f}")
print(f"  Min: {df_final['MS'].min()}")  
print(f"  Max: {df_final['MS'].max()}")

# SAVE
print("💾 Saving MS predictor...")
save_predictor(df_final, "MS")
print("✅ MS.csv saved successfully")
