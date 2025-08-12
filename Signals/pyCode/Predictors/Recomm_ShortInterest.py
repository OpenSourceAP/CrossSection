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
print("🔄 Implementing tsfill to create complete time series per tempID...")

# Get min/max time_avail_m for each tempID to create complete balanced panels
tempid_ranges = ibes_recs.group_by("tempID").agg([
    pl.col("time_avail_m").min().alias("min_time"),
    pl.col("time_avail_m").max().alias("max_time"),
    pl.col("tickerIBES").first().alias("base_tickerIBES"),
    pl.col("amaskcd").first().alias("base_amaskcd")
])

print(f"Processing {len(tempid_ranges)} tempIDs for tsfill...")

# Create complete monthly time series for each tempID
expanded_data = []
for row in tempid_ranges.iter_rows(named=True):
    tempID = row["tempID"]
    min_time = row["min_time"] 
    max_time = row["max_time"]
    base_ticker = row["base_tickerIBES"]
    base_amask = row["base_amaskcd"]
    
    # Create all months between min and max for this tempID
    month_range = list(range(min_time, max_time + 1))
    # Filter to valid months only (ending in 01-12)
    valid_months = [m for m in month_range if (m % 100) >= 1 and (m % 100) <= 12]
    
    if valid_months:
        tempid_complete = pl.DataFrame({
            "tempID": [tempID] * len(valid_months),
            "time_avail_m": valid_months,
            "tickerIBES": [base_ticker] * len(valid_months),
            "amaskcd": [base_amask] * len(valid_months)
        })
        expanded_data.append(tempid_complete)

# Combine all complete time series
if expanded_data:
    complete_grid = pl.concat(expanded_data)
    print(f"Complete grid after tsfill: {len(complete_grid):,} observations")
    
    # Left join original data onto complete grid to fill in ireccd where available
    ibes_filled = complete_grid.join(
        ibes_recs.select(["tempID", "time_avail_m", "ireccd", "anndats"]), 
        on=["tempID", "time_avail_m"], 
        how="left"
    )
    
    print(f"After joining original data: {len(ibes_filled):,} observations")
else:
    ibes_filled = ibes_recs

# Fill tickerIBES within each tempID (forward fill)
# bys tempID (time_avail_m): replace tickerIBES = tickerIBES[_n-1] if mi(tickerIBES) & _n >1
ibes_filled = ibes_filled.sort(["tempID", "time_avail_m"])
ibes_filled = ibes_filled.with_columns(
    pl.col("tickerIBES").forward_fill().over("tempID")
)

# asrol ireccd, gen(ireccd12) by(tempID) stat(first) window(time_avail_m 12) min(1)
# This gets the first (most recent) ireccd value within the past 12 observations
# "window(time_avail_m 12)" means 12 observations, not 12 months!
# stat(first) means the most recent non-null value within that window
print("🧮 Computing asrol rolling first of ireccd over 12 observations...")

# Sort to ensure proper order for rolling window
ibes_filled = ibes_filled.sort(["tempID", "time_avail_m"])

# Implement rolling window to find first (most recent) non-null ireccd within 12 observations
# asrol with stat(first) and window(time_avail_m 12) means: look at current + previous 11 obs to find most recent non-null
# We implement this by creating a custom rolling first logic using coalesce with shifts
ibes_filled = ibes_filled.with_columns([
    pl.coalesce([
        pl.col("ireccd"),  # Current observation (most recent)
        pl.col("ireccd").shift(1).over("tempID"),  # 1 period back
        pl.col("ireccd").shift(2).over("tempID"),  # 2 periods back  
        pl.col("ireccd").shift(3).over("tempID"),  # 3 periods back
        pl.col("ireccd").shift(4).over("tempID"),  # 4 periods back
        pl.col("ireccd").shift(5).over("tempID"),  # 5 periods back
        pl.col("ireccd").shift(6).over("tempID"),  # 6 periods back
        pl.col("ireccd").shift(7).over("tempID"),  # 7 periods back
        pl.col("ireccd").shift(8).over("tempID"),  # 8 periods back
        pl.col("ireccd").shift(9).over("tempID"),  # 9 periods back
        pl.col("ireccd").shift(10).over("tempID"),  # 10 periods back
        pl.col("ireccd").shift(11).over("tempID"),  # 11 periods back (12 total)
    ]).alias("ireccd12")
])

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
print(f"🔍 Debug: temp_rec has {len(temp_rec):,} rows")
hgr_200704_temprec = temp_rec.filter((pl.col("tickerIBES") == "HGR") & (pl.col("time_avail_m") == 200704))
print(f"🔍 Debug: HGR 200704 in temp_rec: {len(hgr_200704_temprec)} rows")
if len(hgr_200704_temprec) > 0:
    print("🔍 Debug: HGR 200704 temp_rec value:")
    print(hgr_200704_temprec)

hgr_200704_main = df.filter((pl.col("tickerIBES") == "HGR") & (pl.col("time_avail_m") == 200704))
print(f"🔍 Debug: HGR 200704 in main dataset before join: {len(hgr_200704_main)} rows")

df = df.join(temp_rec, on=["tickerIBES", "time_avail_m"], how="inner")
print(f"After merging with recommendations: {len(df):,} observations")

hgr_200704_after = df.filter((pl.col("tickerIBES") == "HGR") & (pl.col("time_avail_m") == 200704))
print(f"🔍 Debug: HGR 200704 after join: {len(hgr_200704_after)} rows")

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

# Check HGR 200704 before final filtering
hgr_200704_before_filter = df.filter((pl.col("tickerIBES") == "HGR") & (pl.col("time_avail_m") == 200704))
print(f"🔍 Debug: HGR 200704 before final filtering: {len(hgr_200704_before_filter)} rows")
if len(hgr_200704_before_filter) > 0:
    print("🔍 Debug: HGR 200704 signal values:")
    print(hgr_200704_before_filter.select(["permno", "QuintShortInterest", "QuintConsRecomm", "Recomm_ShortInterest"]))

# keep if !mi(Recomm_ShortInterest)
result = df.filter(pl.col("Recomm_ShortInterest").is_not_null())
result = result.select(["permno", "time_avail_m", "Recomm_ShortInterest"])

# Check if HGR 200704 (permno 10051) is in final result
hgr_200704_final = result.filter((pl.col("permno") == 10051) & (pl.col("time_avail_m") == 200704))
print(f"🔍 Debug: permno 10051 (HGR) 200704 in final result: {len(hgr_200704_final)} rows")

print(f"Generated Recomm_ShortInterest values: {len(result):,} observations")
if len(result) > 0:
    print(f"Value distribution:")
    print(result.group_by("Recomm_ShortInterest").agg(pl.len().alias("count")))

print("💾 Saving Recomm_ShortInterest predictor...")
save_predictor(result, "Recomm_ShortInterest")
print("✅ Recomm_ShortInterest.csv saved successfully")