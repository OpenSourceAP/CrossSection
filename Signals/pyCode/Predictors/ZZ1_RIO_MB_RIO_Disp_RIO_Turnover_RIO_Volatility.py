#%%
# debug

import os
os.chdir(os.path.dirname(os.path.abspath(__file__)))
os.chdir('..')
#%%

# ABOUTME: RIO predictors combining institutional ownership with various characteristics
# ABOUTME: Usage: python3 ZZ1_RIO_MB_RIO_Disp_RIO_Turnover_RIO_Volatility.py (run from pyCode/ directory)

import polars as pl
import pandas as pd
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from utils.save_standardized import save_predictor
from utils.stata_fastxtile import fastxtile, fastxtile_pd
from utils.asrol import asrol
from utils.stata_replication import stata_multi_lag
import numpy as np

print("=" * 80)
print("🏗️  ZZ1_RIO_MB_RIO_Disp_RIO_Turnover_RIO_Volatility.py")
print("Generating Real Investment Opportunities (RIO) predictors")
print("=" * 80)

print("📊 Preparing IBES data...")

# Prep IBES data
# use "$pathDataIntermediate/IBES_EPS_Unadj", replace
# keep if fpi == "1" 
ibes_eps = pl.read_parquet("../pyData/Intermediate/IBES_EPS_Unadj.parquet").filter(
    pl.col("fpi") == "1"
).select(["tickerIBES", "time_avail_m", "stdev"])

print(f"IBES EPS data: {len(ibes_eps):,} observations")

print("📊 Loading main data sources...")

# DATA LOAD
# use permno tickerIBES time_avail_m exchcd mve_c using "$pathDataIntermediate/SignalMasterTable", clear
df = pl.read_parquet("../pyData/Intermediate/SignalMasterTable.parquet").select(
    ["permno", "tickerIBES", "time_avail_m", "exchcd", "mve_c"]
)

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
df = df.join(ibes_eps, on=["tickerIBES", "time_avail_m"], how="left")

print(f"After merging all data sources: {len(df):,} observations")

#%% Drop stocks in bottom NYSE/AMEX size quintile
# pedantically replicate old Stata code
from utils.stata_replication import stata_multi_lag, stata_quantile

# calculate 20th percentile of NYSE/AMEX mve_c, using stata's exact method
me_pd = df.select(['permno', 'time_avail_m', 'mve_c', 'exchcd']).filter(
    (pl.col("exchcd") == 1) | (pl.col("exchcd") == 2)
).to_pandas()
me_pd = (
    me_pd.groupby("time_avail_m").agg(
        me_20pct = ("mve_c", lambda x: stata_quantile(x, 0.2))
    ).reset_index()
)
me_pd = pl.from_pandas(me_pd)

# applying size filter
print("Removing stocks in bottom NYSE/AMEX size quintile...")

df = df.join(me_pd, on="time_avail_m", how="left").filter(
    (pl.col("mve_c") > pl.col("me_20pct")) & (pl.col("mve_c").is_not_null())
)

print(f"After filtering bottom size quintile: {len(df):,} observations")

#%%
print("🏛️ Computing Residual Institutional Ownership (RIO)...")

# construct cleaned institutional ownership
df = df.with_columns(
    instown = (pl.col("instown_perc") / 100)
).with_columns(
    pl.when(pl.col("instown").is_null()).then(0.0).otherwise(pl.col("instown")).alias("instown")
).with_columns(
    pl.when(pl.col("instown") > 0.9999).then(0.9999).otherwise(pl.col("instown")).alias("instown")
).with_columns(
    pl.when(pl.col("instown") < 0.0001).then(0.0001).otherwise(pl.col("instown")).alias("instown")
)

# construct residual institutional ownership (RIO)
df = df.with_columns(
    log_me = np.log(pl.col("mve_c"))
).with_columns(
    RIO = np.log(pl.col("instown") / (1 - pl.col("instown"))) + 23.66 - 2.89 * pl.col("log_me") + 0.08 * (pl.col("log_me")).pow(2)
)

#%%
from utils.stata_replication import stata_multi_lag, stata_quantile

# form RIO quintiles, based on lagged RIO
df = stata_multi_lag(df, "permno", "time_avail_m", "RIO", [6], freq="M", prefix="l")
df = df.with_columns(
    cat_RIO = fastxtile(df, "l6_RIO", by="time_avail_m", n=5)
)

print("📊 Computing interaction signals")

df = df.with_columns(
    pl.col('txditc').fill_null(0.0),
    pl.when(pl.col('ceq')+pl.col('txditc') > 0).then(
        pl.col('mve_c') / (pl.col('ceq') + pl.col('txditc'))
    ).otherwise(None)
    .alias('MB')
).with_columns(
    pl.when(pl.col('stdev') > 0).then(pl.col('stdev') / pl.col('at')).otherwise(None)
    .alias('Disp')
).with_columns(
    (pl.col('vol') / pl.col('shrout'))
    .alias('Turnover')
)

df = asrol(df, 'permno', 'time_avail_m', '1mo', 12, 'ret', 'std',
    new_col_name='Volatility', min_samples=6)


#%%


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