# ABOUTME: Recommendation and Short Interest predictor combining analyst sentiment with short interest
# ABOUTME: Usage: python3 Recomm_ShortInterest.py (run from pyCode/ directory)

import polars as pl
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from utils.savepredictor import save_predictor

print("=" * 80)
print("🏗️  Recomm_ShortInterest.py")
print("Generating Recommendation and Short Interest predictor")
print("=" * 80)

print("📊 Loading IBES Recommendations data...")

# Prepare consensus recommendation
# use tickerIBES amaskcd anndats time_avail_m ireccd using "$pathDataIntermediate/IBES_Recommendations", clear
ibes_recs = pl.read_parquet("../pyData/Intermediate/IBES_Recommendations.parquet")
ibes_recs = ibes_recs.select(["tickerIBES", "amaskcd", "anndats", "time_avail_m", "ireccd"])

# Convert time_avail_m to integer if it's datetime
if ibes_recs['time_avail_m'].dtype == pl.Datetime:
    ibes_recs = ibes_recs.with_columns(
        (pl.col("time_avail_m").dt.year() * 100 + pl.col("time_avail_m").dt.month()).alias("time_avail_m")
    )

print(f"Loaded IBES Recommendations: {len(ibes_recs):,} observations")

# bys tickerIBES amaskcd time_avail_m (anndats): keep if _n==_N  // Drop if more than one recommendation per month
ibes_recs = ibes_recs.sort(["tickerIBES", "amaskcd", "time_avail_m", "anndats"])
ibes_recs = ibes_recs.group_by(["tickerIBES", "amaskcd", "time_avail_m"], maintain_order=True).last()

print(f"After keeping latest recommendation per month: {len(ibes_recs):,} observations")

# Use latest analyst recommendation at most 12 months prior to month t
# egen tempID = group(tickerIBES amaskcd)
ibes_recs = ibes_recs.with_columns(
    pl.concat_str(
        pl.col("tickerIBES").cast(pl.Utf8), 
        pl.lit("_"), 
        pl.col("amaskcd").cast(pl.Utf8)
    ).alias("tempID")
)

# xtset tempID time
# tsfill
# This fills in missing time periods for each tempID
print("🔄 Forward-filling recommendations over 12-month windows...")

# Create a complete time grid for each tempID
time_range = ibes_recs.select(["time_avail_m"]).unique().sort("time_avail_m")

# For each unique tempID, create a complete time series
tempid_list = ibes_recs.select(["tempID", "tickerIBES"]).unique()

# Create full time series for each tempID (this is like tsfill)
full_grid = []
for tempid_row in tempid_list.iter_rows():
    tempid, ticker = tempid_row
    temp_df = time_range.with_columns([
        pl.lit(tempid).alias("tempID"),
        pl.lit(ticker).alias("tickerIBES")
    ])
    full_grid.append(temp_df)

full_time_series = pl.concat(full_grid)

# Merge back with the original data
ibes_filled = full_time_series.join(
    ibes_recs.drop("tickerIBES"),  # avoid duplicate column
    on=["tempID", "time_avail_m"],
    how="left"
)

# fill tickerIBES
# bys tempID (time_avail_m): replace tickerIBES = tickerIBES[_n-1] if mi(tickerIBES) & _n >1
ibes_filled = ibes_filled.sort(["tempID", "time_avail_m"])
ibes_filled = ibes_filled.with_columns(
    pl.col("tickerIBES").forward_fill().over("tempID")
)

# asrol ireccd, gen(ireccd12) by(tempID) stat(first) window(time_avail_m 12) min(1) 
# This gets the first (most recent) ireccd value within the past 12 observations
# "window(time_avail_m 12)" means 12 observations, not 12 months!
# stat(first) means the most recent non-null value within that window
ibes_filled = ibes_filled.sort(["tempID", "time_avail_m"])

# Forward fill with a limit of 11 (so it covers 12 observations total)
ibes_filled = ibes_filled.with_columns(
    pl.col("ireccd")
    .forward_fill(limit=11)  # Fill up to 11 forward (12 total including current)
    .over("tempID")
    .alias("ireccd12")
)

# collapse down to firm-month
# gcollapse (mean) ireccd12, by(tickerIBES time_avail_m)  
temp_rec = (ibes_filled
    .filter(pl.col("ireccd12").is_not_null() & pl.col("tickerIBES").is_not_null())
    .group_by(["tickerIBES", "time_avail_m"], maintain_order=True)
    .agg(pl.col("ireccd12").mean())
)

print(f"Consensus recommendations by ticker-month: {len(temp_rec):,} observations")

print("📊 Loading SignalMasterTable, CRSP, and Short Interest data...")

# DATA LOAD
# use permno gvkey tickerIBES time_avail_m bh1m using "$pathDataIntermediate/SignalMasterTable", clear
signal_master = pl.read_parquet("../pyData/Intermediate/SignalMasterTable.parquet")
signal_master = signal_master.select(["permno", "gvkey", "tickerIBES", "time_avail_m"])

# Convert time_avail_m to integer if it's datetime
if signal_master['time_avail_m'].dtype == pl.Datetime:
    signal_master = signal_master.with_columns(
        (pl.col("time_avail_m").dt.year() * 100 + pl.col("time_avail_m").dt.month()).alias("time_avail_m")
    )

signal_master = signal_master.filter(pl.col("gvkey").is_not_null() & pl.col("tickerIBES").is_not_null())
print(f"Loaded SignalMasterTable: {len(signal_master):,} observations")

# merge 1:1 permno time_avail_m using "$pathDataIntermediate/monthlyCRSP", keep(match) nogenerate keepusing(shrout)
crsp = pl.read_parquet("../pyData/Intermediate/monthlyCRSP.parquet")
crsp = crsp.select(["permno", "time_avail_m", "shrout"])

# Convert time_avail_m to integer if it's datetime
if crsp['time_avail_m'].dtype == pl.Datetime:
    crsp = crsp.with_columns(
        (pl.col("time_avail_m").dt.year() * 100 + pl.col("time_avail_m").dt.month()).alias("time_avail_m")
    )

df = signal_master.join(crsp, on=["permno", "time_avail_m"], how="inner")
print(f"After merging with CRSP: {len(df):,} observations")

# merge 1:1 gvkey time_avail_m using "$pathDataIntermediate/monthlyShortInterest", keep(match) nogenerate keepusing(shortint)
short_interest = pl.read_parquet("../pyData/Intermediate/monthlyShortInterest.parquet")
short_interest = short_interest.select(["gvkey", "time_avail_m", "shortint"])

# Convert time_avail_m to integer if it's datetime
if short_interest['time_avail_m'].dtype == pl.Datetime:
    short_interest = short_interest.with_columns(
        (pl.col("time_avail_m").dt.year() * 100 + pl.col("time_avail_m").dt.month()).alias("time_avail_m")
    )

# Cast gvkey to match data types
short_interest = short_interest.with_columns(pl.col("gvkey").cast(pl.Float64))

df = df.join(short_interest, on=["gvkey", "time_avail_m"], how="inner")
print(f"After merging with short interest: {len(df):,} observations")

# merge m:1 tickerIBES time_avail_m using tempRec, keep(match) nogenerate
df = df.join(temp_rec, on=["tickerIBES", "time_avail_m"], how="inner")
print(f"After merging with recommendations: {len(df):,} observations")

print("🧮 Signal construction...")

# SIGNAL CONSTRUCTION
# gen ShortInterest = shortint/shrout
df = df.with_columns(
    (pl.col("shortint") / pl.col("shrout")).alias("ShortInterest")
)

# gen ConsRecomm = 6 - ireccd12  // To align with coding in Drake, Rees, Swanson (2011)
df = df.with_columns(
    (6 - pl.col("ireccd12")).alias("ConsRecomm")
)

# egen QuintShortInterest = xtile(ShortInterest), n(5) by(time_avail_m)
df = df.with_columns(
    pl.col("ShortInterest")
    .rank(method="ordinal")
    .over("time_avail_m")
    .alias("temp_rank_short")
)

df = df.with_columns(
    pl.col("temp_rank_short")
    .truediv(pl.col("temp_rank_short").max().over("time_avail_m"))
    .mul(5)
    .ceil()
    .cast(pl.Int32)
    .alias("QuintShortInterest")
)

# egen QuintConsRecomm = xtile(ConsRecomm), n(5) by(time_avail_m)
df = df.with_columns(
    pl.col("ConsRecomm")
    .rank(method="ordinal")
    .over("time_avail_m")
    .alias("temp_rank_recomm")
)

df = df.with_columns(
    pl.col("temp_rank_recomm")
    .truediv(pl.col("temp_rank_recomm").max().over("time_avail_m"))
    .mul(5)
    .ceil()
    .cast(pl.Int32)
    .alias("QuintConsRecomm")
)

# cap drop Recomm_ShortInterest
# gen Recomm_ShortInterest = .
# replace Recomm_ShortInterest = 1 if QuintShortInterest == 1 & QuintConsRecomm ==1
# replace Recomm_ShortInterest = 0 if QuintShortInterest == 5 & QuintConsRecomm ==5
df = df.with_columns(
    pl.when((pl.col("QuintShortInterest") == 1) & (pl.col("QuintConsRecomm") == 1))
    .then(1)
    .when((pl.col("QuintShortInterest") == 5) & (pl.col("QuintConsRecomm") == 5))
    .then(0)
    .otherwise(None)
    .alias("Recomm_ShortInterest")
)

# keep if !mi(Recomm_ShortInterest)
result = df.filter(pl.col("Recomm_ShortInterest").is_not_null())
result = result.select(["permno", "time_avail_m", "Recomm_ShortInterest"])

print(f"Generated Recomm_ShortInterest values: {len(result):,} observations")
if len(result) > 0:
    print(f"Value distribution:")
    print(result.group_by("Recomm_ShortInterest").agg(pl.len().alias("count")))

print("💾 Saving Recomm_ShortInterest predictor...")
save_predictor(result, "Recomm_ShortInterest")
print("✅ Recomm_ShortInterest.csv saved successfully")