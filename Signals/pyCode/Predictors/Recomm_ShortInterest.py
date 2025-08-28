#%%

# ABOUTME: Recommendation and Short Interest predictor combining analyst sentiment with short interest
# ABOUTME: Usage: python3 Recomm_ShortInterest.py (run from pyCode/ directory)

import polars as pl
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from utils.save_standardized import save_predictor
from utils.stata_fastxtile import fastxtile
from utils.asrol import asrol_fast
from datetime import date

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


# convert datetime to date
ibes_recs = ibes_recs.with_columns(
    pl.col("time_avail_m").dt.date().alias("time_avail_m"),
    pl.col("anndats").dt.date().alias("anndats")
)
print(f"Loaded IBES Recommendations: {len(ibes_recs):,} observations")


# bys tickerIBES amaskcd time_avail_m (anndats): keep if _n==_N  
# Keep only latest recommendation per firm-month
ibes_recs = ibes_recs.sort(["tickerIBES", "amaskcd", "time_avail_m", "anndats"])
ibes_recs = ibes_recs.group_by(["tickerIBES", "amaskcd", "time_avail_m"], maintain_order=True).last()
ibes_recs = ibes_recs.select(["tickerIBES", "amaskcd", "anndats", "time_avail_m", "ireccd"]) 

print(f"After keeping latest recommendation per month: {len(ibes_recs):,} observations")

# create rec_expand: assumes recommendations are valid for 12 months
for i in range(1, 12):
    temp = ibes_recs.with_columns(
        (pl.col("time_avail_m").dt.offset_by(f'{i}mo').alias("time_avail_m"))
    )    
    if i == 1:
        rec_expand = ibes_recs.vstack(temp)
    else:
        rec_expand = rec_expand.vstack(temp)

rec_expand = rec_expand.sort(["tickerIBES", "amaskcd", "anndats", "time_avail_m"])

# keep only the most recent anndats for each tickerIBES-amaskcd-time_avail_m
# (if an analyst updates the rec, then take it on)
rec_expand = rec_expand.sort(["tickerIBES", "amaskcd", "time_avail_m", "anndats"])
rec_expand = rec_expand.group_by(["tickerIBES", "amaskcd", "time_avail_m"], maintain_order=True).last()

print(f"After expanding to assume recommendations are valid for 12 months: {len(rec_expand):,} observations")

# take mean recommendation within each stock-month
stock_rec = rec_expand.group_by(["tickerIBES", "time_avail_m"]).agg(pl.col("ireccd").mean())

print(f"After taking mean recommendation within each stock-month: {len(stock_rec):,} observations")


#%%

# ===================================================================
# STEP 2: MERGE RECOMMENDATIONS AND SHORT INTEREST ONTO SIGNALMASTER
# ===================================================================
print("📊 Loading SignalMasterTable, CRSP, and Short Interest data...")

# DATA LOAD
# use permno gvkey tickerIBES time_avail_m bh1m using "$pathDataIntermediate/SignalMasterTable", clear
signal_master = pl.read_parquet("../pyData/Intermediate/SignalMasterTable.parquet")
signal_master = signal_master.select(["permno", "gvkey", "tickerIBES", "time_avail_m"])

# Convert time_avail_m to date
signal_master = signal_master.with_columns(
    pl.col("time_avail_m").dt.date().alias("time_avail_m")
)

# drop if mi(gvkey) | mi(tickerIBES)
signal_master = signal_master.filter(pl.col("gvkey").is_not_null() & pl.col("tickerIBES").is_not_null())
print(f"Loaded SignalMasterTable: {len(signal_master):,} observations")

# merge 1:1 permno time_avail_m using "$pathDataIntermediate/monthlyCRSP", keep(match) nogenerate keepusing(shrout)
crsp = pl.read_parquet("../pyData/Intermediate/monthlyCRSP.parquet")
crsp = crsp.select(["permno", "time_avail_m", "shrout"])

# Convert time_avail_m to date
crsp = crsp.with_columns(
    pl.col("time_avail_m").dt.date().alias("time_avail_m")
)

# Create df: this is our working df for now 
df = signal_master.join(crsp, on=["permno", "time_avail_m"], how="inner")
print(f"SignalMasterTable merged with CRSP: {len(df):,} observations")


# merge 1:1 gvkey time_avail_m using "$pathDataIntermediate/monthlyShortInterest", keep(match) nogenerate keepusing(shortint)
short_interest = pl.read_parquet("../pyData/Intermediate/monthlyShortInterest.parquet")
short_interest = short_interest.select(["gvkey", "time_avail_m", "shortint"])

# Convert time_avail_m to date
short_interest = short_interest.with_columns(
    pl.col("time_avail_m").dt.date().alias("time_avail_m")
)

# Cast gvkey to match data types
short_interest = short_interest.with_columns(pl.col("gvkey").cast(pl.Float64))

df = df.join(short_interest, on=["gvkey", "time_avail_m"], how="inner")
print(f"After merging with short interest: {len(df):,} observations")


# merge m:1 tickerIBES time_avail_m using tempRec, keep(match) nogenerate
df = df.join(stock_rec, on=["tickerIBES", "time_avail_m"], how="inner")
print(f"After merging with recommendations: {len(df):,} observations")

#%%

# ===================================================================
# STEP 3: SIGNAL CONSTRUCTION
# ===================================================================
print("🧮 Signal construction...")

# SIGNAL CONSTRUCTION
# gen ShortInterest = shortint/shrout
df = df.with_columns(
    (pl.col("shortint") / pl.col("shrout")).alias("ShortInterest")
)

# gen ConsRecomm = 6 - ireccd  // To align with coding in Drake, Rees, Swanson (2011)
df = df.with_columns(
    (6 - pl.col("ireccd")).alias("ConsRecomm")
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


# Show distribution of signal assignments
print("--- Signal summary ---")
signal_counts = df.group_by("Recomm_ShortInterest").agg(pl.len().alias("count"))
print(f"Signal distribution: {signal_counts}")
print("Time period:")
print(f"{df['time_avail_m'].dt.date().min()} to {df['time_avail_m'].dt.date().max()}")

# keep if !mi(Recomm_ShortInterest)
result = df.filter(pl.col("Recomm_ShortInterest").is_not_null())
result = result.select(["permno", "time_avail_m", "Recomm_ShortInterest"])


# ===================================================================
# STEP 4: SAVE OUTPUT
# ===================================================================
print("💾 Saving Recomm_ShortInterest predictor...")
save_predictor(result, "Recomm_ShortInterest")
print("✅ Recomm_ShortInterest.csv saved successfully")
