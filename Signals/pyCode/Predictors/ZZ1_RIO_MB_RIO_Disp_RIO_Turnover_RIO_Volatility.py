#%%
# ABOUTME: Residual Institutional Ownership (RIO) predictors following Nagel 2005, Table 2B, 2, 2, 2E
# ABOUTME: RIO_MB, RIO_Disp, RIO_Turnover, RIO_Volatility combining institutional ownership with market-to-book, forecast dispersion, turnover, and volatility
"""
Usage:
    python3 Predictors/ZZ1_RIO_MB_RIO_Disp_RIO_Turnover_RIO_Volatility.py

Inputs:
    - IBES_EPS_Unadj.parquet: IBES forecast data with columns [tickerIBES, time_avail_m, stdev]
    - MSigma_InstitutionalOwnership.parquet: Institutional ownership data
    - SignalMasterTable.parquet: Monthly master table with market cap and other variables
    - MSigma_Vol_m.parquet: Monthly volume data
    - m_crsp.parquet: CRSP monthly returns

Outputs:
    - RIO_MB.csv: RIO quintile for stocks in highest MB quintile
    - RIO_Disp.csv: RIO quintile for stocks in high forecast dispersion quintiles  
    - RIO_Turnover.csv: RIO quintile for stocks in highest turnover quintile
    - RIO_Volatility.csv: RIO quintile for stocks in highest volatility quintile
    
All predictors use residual institutional ownership (RIO) which controls for size effects in institutional holdings
"""

import polars as pl
import pandas as pd
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from utils.save_standardized import save_predictor
from utils.stata_fastxtile import fastxtile
from utils.asrol import asrol


print("=" * 80)
print("🏗️  ZZ1_RIO_MB_RIO_Disp_RIO_Turnover_RIO_Volatility.py")
print("Generating Real Investment Opportunities (RIO) predictors")
print("=" * 80)

print("📊 Preparing IBES data...")

# Prep IBES data
# use "$pathDataIntermediate/IBES_EPS_Unadj", replace
# keep if fpi == "1" 
ibes_eps = pl.read_parquet("../pyData/Intermediate/IBES_EPS_Unadj.parquet")
temp_ibes = ibes_eps.filter(pl.col("fpi") == "1")
temp_ibes = temp_ibes.select(["tickerIBES", "time_avail_m", "stdev"])
print(f"IBES EPS data: {len(temp_ibes):,} observations")

print("📊 Loading main data sources...")

# DATA LOAD
# use permno tickerIBES time_avail_m exchcd mve_c using "$pathDataIntermediate/SignalMasterTable", clear
signal_master = pl.read_parquet("../pyData/Intermediate/SignalMasterTable.parquet")
df = signal_master.select(["permno", "tickerIBES", "time_avail_m", "exchcd", "mve_c"])
print(f"SignalMasterTable: {len(df):,} observations")

# merge 1:1 permno time_avail_m using "$pathDataIntermediate/TR_13F", keep(master match) nogenerate keepusing(instown_perc)
tr_13f = pl.read_parquet("../pyData/Intermediate/TR_13F.parquet")
df = df.join(tr_13f.select(["permno", "time_avail_m", "instown_perc"]), on=["permno", "time_avail_m"], how="left")

# merge 1:1 permno time_avail_m using "$pathDataIntermediate/m_aCompustat", keep(master match) nogenerate keepusing(at ceq txditc)
m_compustat = pl.read_parquet("../pyData/Intermediate/m_aCompustat.parquet")
df = df.join(m_compustat.select(["permno", "time_avail_m", "at", "ceq", "txditc"]), on=["permno", "time_avail_m"], how="left")

# merge 1:1 permno time_avail_m using "$pathDataIntermediate/monthlyCRSP", keep(master match) nogenerate keepusing(vol shrout ret)
crsp = pl.read_parquet("../pyData/Intermediate/monthlyCRSP.parquet")
df = df.join(crsp.select(["permno", "time_avail_m", "vol", "shrout", "ret"]), on=["permno", "time_avail_m"], how="left")

# merge m:1 tickerIBES time_avail_m using tempIBES, keep(master match) nogenerate keepusing (stdev)
df = df.join(temp_ibes, on=["tickerIBES", "time_avail_m"], how="left")

print(f"After merging all data sources: {len(df):,} observations")


print("🔍 Applying size filters...")

# filter below 20th pct NYSE me 
# do before indep sort
# bys time_avail_m: astile sizecat = mve_c, qc(exchcd==1 | exchcd == 2) nq(5)
# This creates NYSE/AMEX-based size quintiles but assigns them to ALL observations
# First, compute percentile breakpoints based ONLY on NYSE/AMEX stocks
df = df.with_columns(
    pl.when((pl.col("exchcd") == 1) | (pl.col("exchcd") == 2))
    .then(pl.col("mve_c"))
    .otherwise(None)
    .alias("nyse_amex_mve")
)

# Calculate quintile breakpoints for each time_avail_m using only NYSE/AMEX stocks
df = df.with_columns(
    pl.col("nyse_amex_mve").quantile(0.2).over("time_avail_m").alias("p20"),
    pl.col("nyse_amex_mve").quantile(0.4).over("time_avail_m").alias("p40"),
    pl.col("nyse_amex_mve").quantile(0.6).over("time_avail_m").alias("p60"),
    pl.col("nyse_amex_mve").quantile(0.8).over("time_avail_m").alias("p80")
)

# Assign ALL observations to quintiles based on NYSE/AMEX breakpoints
df = df.with_columns(
    pl.when(pl.col("mve_c") <= pl.col("p20")).then(1)
    .when(pl.col("mve_c") <= pl.col("p40")).then(2)
    .when(pl.col("mve_c") <= pl.col("p60")).then(3)  
    .when(pl.col("mve_c") <= pl.col("p80")).then(4)
    .otherwise(5)
    .alias("sizecat")
)

# drop if sizecat == 1
df = df.filter(pl.col("sizecat") != 1)
print(f"After filtering bottom size quintile: {len(df):,} observations")


# Clean up temporary columns
df = df.drop(["nyse_amex_mve", "p20", "p40", "p60", "p80", "sizecat"])

print("🏛️ Computing Residual Institutional Ownership (RIO)...")

# Residual Institutional Ownership sort
# CRITICAL FIX: Match Stata's sequential replace logic exactly
# gen temp = instown_perc/100
df = df.with_columns(
    pl.when(pl.col("instown_perc").is_null())
    .then(None)  # Keep as null initially
    .otherwise(pl.col("instown_perc") / 100)
    .alias("temp")
)

# replace temp = 0 if mi(temp)
df = df.with_columns(
    pl.when(pl.col("temp").is_null())
    .then(0.0)
    .otherwise(pl.col("temp"))
    .alias("temp")
)

# replace temp = .9999 if temp > .9999
df = df.with_columns(
    pl.when(pl.col("temp") > 0.9999)
    .then(0.9999)
    .otherwise(pl.col("temp"))
    .alias("temp")
)

# replace temp = .0001 if temp < .0001 (this catches temp=0 from missing data!)
df = df.with_columns(
    pl.when(pl.col("temp") < 0.0001)
    .then(0.0001)
    .otherwise(pl.col("temp"))
    .alias("temp")
)

# gen RIO = log(temp/(1-temp)) + 23.66 - 2.89*log(mve_c) + .08*(log(mve_c))^2
df = df.with_columns(
    (
        (pl.col("temp") / (1 - pl.col("temp"))).log() + 
        23.66 - 
        2.89 * pl.col("mve_c").log() + 
        0.08 * (pl.col("mve_c").log()).pow(2)
    ).alias("RIO")
)


# xtset permno time_avail_m
# gen RIOlag = l6.RIO
# CRITICAL FIX: Use calendar-based lag (6 months) instead of position-based shift(6)
# This matches Stata's l6. behavior which goes back 6 calendar months
df = df.sort(["permno", "time_avail_m"])

# Convert to pandas for easier date arithmetic
df_pandas = df.to_pandas()

# Calculate the exact 6-month lag date for each observation
df_pandas['lag_date'] = df_pandas['time_avail_m'] - pd.DateOffset(months=6)

# Create lookup for RIO values by permno and date
rio_lookup = df_pandas.set_index(['permno', 'time_avail_m'])['RIO']

# Get RIOlag by looking up RIO at lag_date
df_pandas['RIOlag'] = df_pandas.apply(
    lambda row: rio_lookup.get((row['permno'], row['lag_date']), None), 
    axis=1
)

# Convert back to polars (lag_date was already used and not in dataframe)
df = pl.from_pandas(df_pandas)

# egen cat_RIO = fastxtile(RIOlag), n(5) by(time_avail_m)
# Convert to pandas for fastxtile operation
df_pandas = df.to_pandas()
df_pandas['cat_RIO'] = fastxtile(df_pandas, 'RIOlag', by='time_avail_m', n=5)
# Convert back to polars
df = pl.from_pandas(df_pandas)


print("📊 Computing characteristic variables...")

# Forecast dispersion, market-to-book, turnover, volatiltity sorts
# replace txditc = 0 if mi(txditc)
df = df.with_columns(
    pl.when(pl.col("txditc").is_null()).then(0.0).otherwise(pl.col("txditc")).alias("txditc")
)

# gen MB = mve_c/(ceq + txditc)
# replace MB = . if (ceq + txditc) < 0
df = df.with_columns(
    pl.when((pl.col("ceq") + pl.col("txditc")) < 0)
    .then(None)
    .otherwise(pl.col("mve_c") / (pl.col("ceq") + pl.col("txditc")))
    .alias("MB")
)

# gen Disp = stdev/at if stdev > 0
df = df.with_columns(
    pl.when(pl.col("stdev") > 0)
    .then(pl.col("stdev") / pl.col("at"))
    .otherwise(None)
    .alias("Disp")
)

# gen Turnover = vol/shrout
df = df.with_columns(
    (pl.col("vol") / pl.col("shrout")).alias("Turnover")
)

# bys permno: asrol ret, gen(Volatility) stat(sd) window(time_avail_m 12) min(6)
# Use asrol_legacy for rolling standard deviation
df_pandas_vol = df.to_pandas()

df_pandas_vol = asrol(
    df_pandas_vol,
    group_col='permno',
    time_col='time_avail_m',
    freq='1mo',
    window=12,
    value_col='ret',
    stat='std',
    new_col_name='Volatility',
    min_samples=6
)

df = pl.from_pandas(df_pandas_vol)

# drop rows missing mve_c
# it seems our asrol fills in gaps too aggressively
df = df.filter(pl.col("mve_c").is_not_null())

print("🏷️ Creating characteristic quintiles and RIO interactions...")

# Create characteristic quintiles and RIO interactions
variables = ["MB", "Disp", "Volatility", "Turnover"]

# Convert to pandas for fastxtile operations
df_pandas = df.to_pandas()

for var in variables:
    # egen cat_`v' = fastxtile(`v'), n(5) by(time_avail_m)
    df_pandas[f'cat_{var}'] = fastxtile(df_pandas, var, by='time_avail_m', n=5)
    
    # gen RIO_`v' = cat_RIO if cat_`v' == 5
    df_pandas[f'RIO_{var}'] = df_pandas['cat_RIO'].where(df_pandas[f'cat_{var}'] == 5)

# Convert back to polars
df = pl.from_pandas(df_pandas)


# patch for Dispersion
# replace RIO_Disp = cat_RIO if cat_Disp >= 4 & cat_Disp != .
df = df.with_columns(
    pl.when((pl.col("cat_Disp") >= 4) & (pl.col("cat_Disp").is_not_null()))
    .then(pl.col("cat_RIO"))
    .otherwise(pl.col("RIO_Disp"))
    .alias("RIO_Disp")
)


print("💾 Saving RIO predictors...")

# Save all RIO predictors
rio_predictors = ["RIO_MB", "RIO_Disp", "RIO_Turnover", "RIO_Volatility"]

for predictor in rio_predictors:
    result = df.select(["permno", "time_avail_m", predictor])
    valid_result = result.filter(pl.col(predictor).is_not_null())
    
    print(f"Generated {predictor}: {len(valid_result):,} observations")
    if len(valid_result) > 0:
        print(f"  Value distribution:")
        print(valid_result.group_by(predictor).agg(pl.len().alias("count")).sort(predictor))
    
    save_predictor(result, predictor)
    print(f"✅ {predictor}.csv saved successfully")

print("🎉 All RIO predictors completed!")