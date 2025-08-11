# ABOUTME: Multi-component analyst value predictor: AnalystValue, AOP, PredictedFE, IntrinsicValue
# ABOUTME: Usage: python3 ZZ1_AnalystValue_AOP_PredictedFE_IntrinsicValue.py (run from pyCode/ directory)

import polars as pl
import polars_ols  # registers .least_squares namespace
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from utils.savepredictor import save_predictor

print("=" * 80)
print("🏗️  ZZ1_AnalystValue_AOP_PredictedFE_IntrinsicValue.py")
print("Generating analyst value predictors: AnalystValue, AOP, PredictedFE, IntrinsicValue")
print("=" * 80)

print("📊 Preparing IBES forecast data...")

# Prep IBES FROE1 (1-year ahead EPS)
print("Loading IBES EPS Unadj for FROE1...")
ibes_eps = pl.read_parquet("../pyData/Intermediate/IBES_EPS_Unadj.parquet")

# keep if fpi == "1" & month(statpers) == 5 // only May p 290
# keep if fpedats != . & fpedats > statpers + 30 // keep only forecasts past June
froe1 = ibes_eps.filter(
    (pl.col("fpi") == "1") & 
    (pl.col("statpers").dt.month() == 5) &
    (pl.col("fpedats").is_not_null()) &
    (pl.col("fpedats") > pl.col("statpers") + pl.duration(days=30))
)

# replace time_avail_m = time_avail_m + 1 // OP is conservative
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
# use permno tickerIBES time_avail_m prc using "$pathDataIntermediate/SignalMasterTable", clear
signal_master = pl.read_parquet("../pyData/Intermediate/SignalMasterTable.parquet")
df = signal_master.select(["permno", "tickerIBES", "time_avail_m", "prc"])
print(f"SignalMasterTable: {len(df):,} observations")

# merge 1:1 permno time_avail_m using "$pathDataIntermediate/monthlyCRSP", keep(master match) nogenerate keepusing(shrout) 
crsp = pl.read_parquet("../pyData/Intermediate/monthlyCRSP.parquet")
df = df.join(crsp.select(["permno", "time_avail_m", "shrout"]), on=["permno", "time_avail_m"], how="left")

# merge 1:1 permno time_avail_m using "$pathDataIntermediate/m_aCompustat", keep(master match) nogenerate keepusing(ceq ib ibcom ni sale datadate dvc at)
m_compustat = pl.read_parquet("../pyData/Intermediate/m_aCompustat.parquet")
df = df.join(
    m_compustat.select(["permno", "time_avail_m", "ceq", "ib", "ibcom", "ni", "sale", "datadate", "dvc", "at"]), 
    on=["permno", "time_avail_m"], 
    how="left"
)

print(f"After merging CRSP and Compustat: {len(df):,} observations")

# gen SG = sale/l60.sale
df = df.sort(["permno", "time_avail_m"])
df = df.with_columns(
    (pl.col("sale") / pl.col("sale").shift(60).over("permno")).alias("SG")
)

# keep if month(dofm(time_avail_m)) == 6
df = df.filter(pl.col("time_avail_m").dt.month() == 6)
print(f"After filtering to June observations: {len(df):,} observations")

# Merge with IBES data
# merge m:1 tickerIBES time_avail_m using "$pathtemp/tempFROE", keep(match) nogenerate
df = df.join(froe1, on=["tickerIBES", "time_avail_m"], how="left")
# merge m:1 tickerIBES time_avail_m using "$pathtemp/tempFROE2", keep(master match) nogenerate
df = df.join(froe2, on=["tickerIBES", "time_avail_m"], how="left")
# merge m:1 tickerIBES time_avail_m using "$pathtemp/tempLTG", keep(master match) nogenerate
df = df.join(ltg, on=["tickerIBES", "time_avail_m"], how="left")

print(f"After merging IBES data: {len(df):,} observations")

print("🧮 Computing financial variables and screens...")

# Common screens and variables
# xtset permno time_avail_m
df = df.sort(["permno", "time_avail_m"])

# gen ceq_ave = (ceq + l12.ceq)/2
# bys permno (time_avail_m): replace ceq_ave = ceq if _n <= 1 // seems important
# NOTE: Since we've filtered to June observations only, l12.ceq means previous June (1 year back = 1 position back)
df = df.with_columns([
    pl.col("ceq").shift(1).over("permno").alias("l12_ceq"),  # Changed from shift(12) to shift(1)
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

# gen mve_c = (shrout * abs(prc))
df = df.with_columns(
    (pl.col("shrout") * pl.col("prc").abs()).alias("mve_c")
)

# gen BM = ceq/mve_c
df = df.with_columns(
    (pl.col("ceq") / pl.col("mve_c")).alias("BM")
)

# gen k = dvc/ibcom // p 288 says ib, but Table 1 says ibcom
# replace k = dvc/(0.06*at) if ibcom < 0
df = df.with_columns(
    pl.when(pl.col("ibcom") < 0)
    .then(pl.col("dvc") / (0.06 * pl.col("at")))
    .otherwise(pl.col("dvc") / pl.col("ibcom"))
    .alias("k")
)

# gen ROE = ibcom/ceq_ave // p 290 or Table 1
df = df.with_columns(
    (pl.col("ibcom") / pl.col("ceq_ave")).alias("ROE")
)

print("📈 Computing forecast-based equity values...")

# p 317 (Appendix) - Multi-stage equity valuation
# gen FROE1 = feps1*shrout/ceq_ave
df = df.with_columns(
    (pl.col("feps1") * pl.col("shrout") / pl.col("ceq_ave")).alias("FROE1")
)

# gen ceq1 = ceq*(1+FROE1*(1-k))
df = df.with_columns(
    (pl.col("ceq") * (1 + pl.col("FROE1") * (1 - pl.col("k")))).alias("ceq1")
)

# gen ceq1h = ceq*(1+ROE*(1-k))
df = df.with_columns(
    (pl.col("ceq") * (1 + pl.col("ROE") * (1 - pl.col("k")))).alias("ceq1h")
)

# gen FROE2 = feps2*shrout/((ceq1 + ceq)/2)
df = df.with_columns(
    (pl.col("feps2") * pl.col("shrout") / ((pl.col("ceq1") + pl.col("ceq")) / 2)).alias("FROE2")
)

# gen ceq2 = ceq1*(1+FROE1*(1-k))
df = df.with_columns(
    (pl.col("ceq1") * (1 + pl.col("FROE1") * (1 - pl.col("k")))).alias("ceq2")
)

# gen ceq2h = ceq1h*(1+ROE*(1-k))
df = df.with_columns(
    (pl.col("ceq1h") * (1 + pl.col("ROE") * (1 - pl.col("k")))).alias("ceq2h")
)

# gen FROE3 = feps2*(1+LTG/100)*shrout/((ceq1+ceq2)/2)
# replace FROE3 = FROE2 if LTG == .
df = df.with_columns(
    pl.when(pl.col("LTG").is_null())
    .then(pl.col("FROE2"))
    .otherwise(pl.col("feps2") * (1 + pl.col("LTG")/100) * pl.col("shrout") / ((pl.col("ceq1") + pl.col("ceq2")) / 2))
    .alias("FROE3")
)

# gen ceq3 = ceq2*(1+FROE2*(1-k))
df = df.with_columns(
    (pl.col("ceq2") * (1 + pl.col("FROE2") * (1 - pl.col("k")))).alias("ceq3")
)

print("🔍 Applying data screens...")

# Screens
# drop if ceq < 0 | ceq == . // page 291
# drop if abs(ROE) > 1 | abs(FROE1) > 1 | k > 1 // page 291
# keep if month(datadate) >= 6 // p 290
# drop if feps2 == . | feps1 == . // p 290
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
    ((pl.col("av_term1") + pl.col("av_term2") + pl.col("av_term3") + pl.col("av_term4")) / pl.col("mve_c"))
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
    ((pl.col("iv_term1") + pl.col("iv_term2") + pl.col("iv_term3")) / pl.col("mve_c"))
    .alias("IntrinsicValue")
)

# gen AOP = (AnalystValue - IntrinsicValue)/abs(IntrinsicValue)
df = df.with_columns(
    ((pl.col("AnalystValue") - pl.col("IntrinsicValue")) / pl.col("IntrinsicValue").abs()).alias("AOP")
)

print("🔮 Computing predicted forecast error...")

# Predicted FE
# gen FErr = l12.FROE1 - ROE // almost works!
df = df.with_columns(
    (pl.col("FROE1").shift(1).over("permno") - pl.col("ROE")).alias("FErr")  # Changed from shift(12) to shift(1)
)

# winsor2 FErr, replace cuts(1 99) trim by(time_avail_m)
df = df.with_columns([
    pl.col("FErr").quantile(0.01).over("time_avail_m").alias("ferr_p01"),
    pl.col("FErr").quantile(0.99).over("time_avail_m").alias("ferr_p99")
])

df = df.with_columns(
    pl.when(pl.col("FErr") < pl.col("ferr_p01"))
    .then(pl.col("ferr_p01"))
    .when(pl.col("FErr") > pl.col("ferr_p99"))
    .then(pl.col("ferr_p99"))
    .otherwise(pl.col("FErr"))
    .alias("FErr")
)

# Convert to ranks
variables = ["SG", "BM", "AOP", "LTG"]
for var in variables:
    df = df.with_columns(
        pl.col(var).rank(method="ordinal").over("time_avail_m")
        .truediv(pl.col(var).count().over("time_avail_m"))
        .alias(f"rank{var}")
    )

# Lag for forecasting and run reg
for var in variables:
    df = df.with_columns(
        pl.col(f"rank{var}").shift(1).over("permno").alias(f"lag{var}")  # Changed from shift(12) to shift(1)
    )

# asreg FErr lag*, by(time_avail_m)
# Always sort data first
df = df.sort(["time_avail_m", "permno"])

# Use asreg helper with group mode  
from utils.asreg import asreg
df_with_predictions = asreg(
    df,
    y="FErr", 
    X=["lagSG", "lagBM", "lagAOP", "lagLTG"],
    by=["time_avail_m"],
    mode="group",
    add_intercept=True,
    outputs=("coef",),
    coef_prefix="_b_",
    null_policy="drop",
    min_samples=5  # Need at least 5 observations for 4 variables + intercept
)

# Rename coefficient columns to match original names
df_with_predictions = df_with_predictions.rename({
    "_b_const": "_b_cons",
    "_b_lagSG": "_b_lagSG",
    "_b_lagBM": "_b_lagBM", 
    "_b_lagAOP": "_b_lagAOP",
    "_b_lagLTG": "_b_lagLTG"
})

# gen PredictedFE = _b_cons + _b_lagSG*rankSG + _b_lagBM*rankBM + _b_lagAOP*rankAOP + _b_lagLTG*rankLTG
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

# EXPAND TO MONTHLY
# Signal relevant for one year
# Replicate Stata: gen temp = 12; expand temp; bysort permno tempTime: replace time_avail_m = time_avail_m + _n - 1
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
predictors = ["AnalystValue", "AOP", "PredictedFE", "IntrinsicValue"]

for predictor in predictors:
    result = df_expanded.select(["permno", "time_avail_m", predictor])
    valid_result = result.filter(pl.col(predictor).is_not_null())
    
    print(f"Generated {predictor}: {len(valid_result):,} observations")
    if len(valid_result) > 0:
        print(f"  Mean: {valid_result[predictor].mean():.6f}")
        print(f"  Std: {valid_result[predictor].std():.6f}")
    
    save_predictor(result, predictor)
    print(f"✅ {predictor}.csv saved successfully")

print("🎉 All analyst value predictors completed!")