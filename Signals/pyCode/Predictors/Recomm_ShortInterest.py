# ABOUTME: Recommendation and Short Interest predictor combining analyst sentiment with short interest
# ABOUTME: Usage: python3 Recomm_ShortInterest.py (run from pyCode/ directory)

import polars as pl
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from utils.savepredictor import save_predictor
from utils.stata_fastxtile import fastxtile

print("=" * 80)
print("🏗️  Recomm_ShortInterest.py")
print("Generating Recommendation and Short Interest predictor")
print("=" * 80)

# ===================================================================
# STEP 1: PREPARE CONSENSUS RECOMMENDATION DATA
# ===================================================================
print("📊 Loading IBES Recommendations data...")

# Load IBES recommendations - exact Stata translation
# use tickerIBES amaskcd anndats time_avail_m ireccd using "$pathDataIntermediate/IBES_Recommendations", clear
ibes_recs = pl.read_parquet("../pyData/Intermediate/IBES_Recommendations.parquet")
ibes_recs = ibes_recs.select(["tickerIBES", "amaskcd", "anndats", "time_avail_m", "ireccd"])

# Convert time_avail_m to integer if datetime (keep as yyyymm integer throughout)
if ibes_recs['time_avail_m'].dtype == pl.Datetime:
    ibes_recs = ibes_recs.with_columns(
        (pl.col("time_avail_m").dt.year() * 100 + pl.col("time_avail_m").dt.month()).alias("time_avail_m")
    )

print(f"Loaded IBES Recommendations: {len(ibes_recs):,} observations")

# bys tickerIBES amaskcd time_avail_m (anndats): keep if _n==_N  
# Keep only latest recommendation per firm-month
ibes_recs = ibes_recs.sort(["tickerIBES", "amaskcd", "time_avail_m", "anndats"])
ibes_recs = ibes_recs.group_by(["tickerIBES", "amaskcd", "time_avail_m"], maintain_order=True).last()

print(f"After keeping latest recommendation per month: {len(ibes_recs):,} observations")

# Create firm ID and prepare for panel operations
# egen tempID = group(tickerIBES amaskcd)
ibes_recs = ibes_recs.with_columns(
    pl.concat_str(
        pl.col("tickerIBES").cast(pl.Utf8), 
        pl.lit("_"), 
        pl.col("amaskcd").cast(pl.Utf8)
    ).alias("tempID")
)

# ===================================================================
# TSFILL IMPLEMENTATION - Create complete time series per tempID
# ===================================================================
print("🔄 Implementing tsfill to create complete time series...")

# Get min/max time range for each tempID
tempid_ranges = ibes_recs.group_by("tempID").agg([
    pl.col("time_avail_m").min().alias("min_time"),
    pl.col("time_avail_m").max().alias("max_time"),
    pl.col("tickerIBES").first().alias("base_tickerIBES"),
    pl.col("amaskcd").first().alias("base_amaskcd")
])

print(f"Creating complete time series for {len(tempid_ranges)} tempIDs...")

# Create complete balanced panel efficiently using polars
def create_complete_panel():
    panel_frames = []
    
    for row in tempid_ranges.iter_rows(named=True):
        tempID = row["tempID"]
        min_time = row["min_time"] 
        max_time = row["max_time"]
        
        # Create all valid months between min and max
        years = range(min_time // 100, (max_time // 100) + 1)
        months = range(1, 13)
        
        # Generate all year-month combinations in range
        valid_times = []
        for year in years:
            for month in months:
                yyyymm = year * 100 + month
                if min_time <= yyyymm <= max_time:
                    valid_times.append(yyyymm)
        
        if valid_times:
            tempid_panel = pl.DataFrame({
                "tempID": [tempID] * len(valid_times),
                "time_avail_m": valid_times,
                "tickerIBES": [row["base_tickerIBES"]] * len(valid_times),
                "amaskcd": [row["base_amaskcd"]] * len(valid_times)
            })
            panel_frames.append(tempid_panel)
    
    return pl.concat(panel_frames) if panel_frames else pl.DataFrame()

# Create complete grid
complete_panel = create_complete_panel()
print(f"Complete balanced panel: {len(complete_panel):,} observations")

# Join original data onto complete panel
ibes_filled = complete_panel.join(
    ibes_recs.select(["tempID", "time_avail_m", "ireccd", "anndats"]), 
    on=["tempID", "time_avail_m"], 
    how="left"
)

# Forward-fill tickerIBES after tsfill
# bys tempID (time_avail_m): replace tickerIBES = tickerIBES[_n-1] if mi(tickerIBES) & _n >1
ibes_filled = ibes_filled.sort(["tempID", "time_avail_m"])
ibes_filled = ibes_filled.with_columns(
    pl.col("tickerIBES").forward_fill().over("tempID")
)

print(f"After tsfill and forward-fill: {len(ibes_filled):,} observations")

# ===================================================================
# ASROL IMPLEMENTATION - Rolling window for most recent recommendation
# ===================================================================
print("🧮 Computing asrol rolling first of ireccd over 12 observations...")

# asrol ireccd, gen(ireccd12) by(tempID) stat(first) window(time_avail_m 12) min(1)
# stat(first) = most recent non-null value within 12 observations (current + previous 11)
ibes_filled = ibes_filled.sort(["tempID", "time_avail_m"])

# Implement rolling first using efficient polars operations
ibes_filled = ibes_filled.with_columns([
    pl.coalesce([
        pl.col("ireccd"),  # Current observation (most recent)
        pl.col("ireccd").shift(1).over("tempID"),   # 1 period back
        pl.col("ireccd").shift(2).over("tempID"),   # 2 periods back  
        pl.col("ireccd").shift(3).over("tempID"),   # 3 periods back
        pl.col("ireccd").shift(4).over("tempID"),   # 4 periods back
        pl.col("ireccd").shift(5).over("tempID"),   # 5 periods back
        pl.col("ireccd").shift(6).over("tempID"),   # 6 periods back
        pl.col("ireccd").shift(7).over("tempID"),   # 7 periods back
        pl.col("ireccd").shift(8).over("tempID"),   # 8 periods back
        pl.col("ireccd").shift(9).over("tempID"),   # 9 periods back
        pl.col("ireccd").shift(10).over("tempID"),  # 10 periods back
        pl.col("ireccd").shift(11).over("tempID"),  # 11 periods back (12 total)
    ]).alias("ireccd12")
])

# Collapse to firm-month level
# gcollapse (mean) ireccd12, by(tickerIBES time_avail_m)  
temp_rec = (ibes_filled
    .filter(pl.col("ireccd12").is_not_null() & pl.col("tickerIBES").is_not_null())
    .group_by(["tickerIBES", "time_avail_m"], maintain_order=True)
    .agg(pl.col("ireccd12").mean())
)

print(f"Consensus recommendations by ticker-month: {len(temp_rec):,} observations")

# ===================================================================
# STEP 2: MERGE RECOMMENDATIONS AND SHORT INTEREST ONTO SIGNALMASTER
# ===================================================================
print("📊 Loading SignalMasterTable, CRSP, and Short Interest data...")

# DATA LOAD
# use permno gvkey tickerIBES time_avail_m bh1m using "$pathDataIntermediate/SignalMasterTable", clear
signal_master = pl.read_parquet("../pyData/Intermediate/SignalMasterTable.parquet")
signal_master = signal_master.select(["permno", "gvkey", "tickerIBES", "time_avail_m"])

# Convert time_avail_m to integer if datetime
if signal_master['time_avail_m'].dtype == pl.Datetime:
    signal_master = signal_master.with_columns(
        (pl.col("time_avail_m").dt.year() * 100 + pl.col("time_avail_m").dt.month()).alias("time_avail_m")
    )

# drop if mi(gvkey) | mi(tickerIBES)
signal_master = signal_master.filter(pl.col("gvkey").is_not_null() & pl.col("tickerIBES").is_not_null())
print(f"Loaded SignalMasterTable: {len(signal_master):,} observations")

# merge 1:1 permno time_avail_m using "$pathDataIntermediate/monthlyCRSP", keep(match) nogenerate keepusing(shrout)
crsp = pl.read_parquet("../pyData/Intermediate/monthlyCRSP.parquet")
crsp = crsp.select(["permno", "time_avail_m", "shrout"])

# Convert time_avail_m to integer if datetime
if crsp['time_avail_m'].dtype == pl.Datetime:
    crsp = crsp.with_columns(
        (pl.col("time_avail_m").dt.year() * 100 + pl.col("time_avail_m").dt.month()).alias("time_avail_m")
    )

df = signal_master.join(crsp, on=["permno", "time_avail_m"], how="inner")
print(f"After merging with CRSP: {len(df):,} observations")

# merge 1:1 gvkey time_avail_m using "$pathDataIntermediate/monthlyShortInterest", keep(match) nogenerate keepusing(shortint)
short_interest = pl.read_parquet("../pyData/Intermediate/monthlyShortInterest.parquet")
short_interest = short_interest.select(["gvkey", "time_avail_m", "shortint"])

# Convert time_avail_m to integer if datetime
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

# ===================================================================
# STEP 3: SIGNAL CONSTRUCTION
# ===================================================================
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

# ===================================================================
# CRITICAL FIX: Use stata_fastxtile for quintile calculations
# ===================================================================
print("📊 Computing quintiles using stata_fastxtile...")

# Convert to pandas for fastxtile, then back to polars
df_pandas = df.to_pandas()

# egen QuintShortInterest = xtile(ShortInterest), n(5) by(time_avail_m)
df_pandas['QuintShortInterest'] = fastxtile(df_pandas, "ShortInterest", by="time_avail_m", n=5)

# egen QuintConsRecomm = xtile(ConsRecomm), n(5) by(time_avail_m)  
df_pandas['QuintConsRecomm'] = fastxtile(df_pandas, "ConsRecomm", by="time_avail_m", n=5)

# Convert back to polars
df = pl.from_pandas(df_pandas)

# Define binary signal: pessimistic vs optimistic cases
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

# ===================================================================
# STEP 4: SAVE OUTPUT
# ===================================================================
print("💾 Saving Recomm_ShortInterest predictor...")
save_predictor(result, "Recomm_ShortInterest")
print("✅ Recomm_ShortInterest.csv saved successfully")