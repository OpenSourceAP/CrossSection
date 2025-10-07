#%%
# ABOUTME: Analyst Recommendations and Short Interest following Drake, Rees and Swanson 2011, Table 7b
# ABOUTME: Binary signal: 1 for lowest quintile short interest & recommendations, 0 for highest quintiles
"""
Usage:
    python3 Predictors/Recomm_ShortInterest.py

Inputs:
    - IBES_Recommendations.parquet: IBES analyst recommendations data
    - SignalMasterTable.parquet: Master table with gvkey, tickerIBES mappings
    - monthlyCRSP.parquet: CRSP data for shares outstanding (shrout)
    - monthlyShortInterest.parquet: Short interest data (shortint)

Outputs:
    - Recomm_ShortInterest.csv: Binary signal (0/1) for extreme recommendation-short interest combinations
"""

import polars as pl
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from utils.save_standardized import save_predictor
from utils.stata_fastxtile import fastxtile
from datetime import date
from utils.stata_replication import fill_date_gaps

print("=" * 80)
print("🏗️  Recomm_ShortInterest.py")
print("Generating Recommendation and Short Interest predictor")
print("=" * 80)


#%
# ===================================================================
# STEP 1: PREPARE CONSENSUS RECOMMENDATION DATA
# ===================================================================
print("📊 Loading IBES Recommendations data...")

# Load IBES recommendations
ibes_recs = pl.read_parquet("../pyData/Intermediate/IBES_Recommendations.parquet",
                            columns=["tickerIBES", "amaskcd", "anndats", "time_avail_m", "ireccd"]).with_columns(
                                pl.col("time_avail_m").cast(pl.Date),
                                pl.col("anndats").cast(pl.Date)
                            )

print(f"Loaded IBES Recommendations: {len(ibes_recs):,} observations")

# for duplicate tickerIBES-amaskcd-anndats, take the mean recommendation
ibes_recs = ibes_recs.group_by(["tickerIBES", "amaskcd", "time_avail_m", "anndats"]).agg(
    pl.col("ireccd").mean()
)

#%%

# drop if anndats is after the IBES consensus recommendation date (approximately)
# page 5 says "We also require that the individual analyst recommendations be issued on or before the IBES consensus recommendation date" and "IBES calculates consensus recommendation on the Thursday before the third Friday of the month (ranging from the 14th to the 20th of the month)."
# Let's approximate with the 17th of the month

ibes_recs = ibes_recs.with_columns(
    ibes_cons_date = pl.col('time_avail_m').dt.offset_by('16d')
).with_columns(
    ireccd_ok = pl.when(
        pl.col('anndats') <= pl.col('ibes_cons_date')
    ).then(
        pl.col('ireccd')
    ).otherwise(
        None
    )    
)

#%%
# keep last recommendation for each tickerIBES-amaskcd-time_avail_m
# p 5 "We use only the most recent individual analyst recommendation"
ibes_recs = ibes_recs.group_by(
    ["tickerIBES", "time_avail_m", "amaskcd"], maintain_order=True).last()


# assume recommendation is valid for recc_extension months after the anndats
# Table 7 "we construct portfolios monthly
# based on the quintile rank of analyst recommendations and short interest selected in the current month and in each of the past five months six-month holding period"

rec_extension = '5mo'

# fill in time-series gaps by tickerIBES-amaskcd
ibes_recs = ibes_recs.with_columns(
    ticker_analyst = pl.concat_str([pl.col("tickerIBES"), pl.col("amaskcd")], separator="_")
)
ibes_recs = fill_date_gaps(ibes_recs,"ticker_analyst","time_avail_m","1mo",
    end_padding=rec_extension # allow recommendations to be extended after the last rec
).with_columns(
    pl.col('ticker_analyst').str.split("_").list.get(0).alias("tickerIBES")
).sort(['ticker_analyst', 'time_avail_m'])

# define ireccd12: the latest recommendation within rec_extension months
ibes_recs = ibes_recs.with_columns(
    ireccd12 = pl.col('ireccd_ok') 
).with_columns(
    pl.col('anndats').forward_fill().over('ticker_analyst'),
    pl.col('ireccd12').forward_fill().over('ticker_analyst')
).with_columns(
    pl.when(
        pl.col('time_avail_m') > pl.col('anndats').dt.offset_by(rec_extension)
    ).then(
        None
    ).otherwise(
        pl.col('ireccd12')
    ).alias('ireccd12')
)


#%%

# take mean across analysts for each stock-month
stock_rec = ibes_recs.with_columns(
    pl.col('tickerIBES').forward_fill().over('ticker_analyst')
).group_by(["tickerIBES", "time_avail_m"]).agg(
    pl.col("ireccd12").mean()
).filter(
    pl.col("ireccd12").is_not_null()
)

print(f"After taking mean recommendation within each stock-month: {len(stock_rec):,} observations")

#%%

# ===================================================================
# STEP 2: MERGE RECOMMENDATIONS AND SHORT INTEREST ONTO SIGNALMASTER
# ===================================================================
print("📊 Loading SignalMasterTable, CRSP, and Short Interest data...")

# DATA LOAD
signal_master = pl.read_parquet("../pyData/Intermediate/SignalMasterTable.parquet",
                                columns=["permno", "gvkey", "tickerIBES", "time_avail_m"]).with_columns(
    pl.col("time_avail_m").cast(pl.Date)
)

# drop if missing gvkey or tickerIBES
signal_master = signal_master.filter(pl.col("gvkey").is_not_null() & pl.col("tickerIBES").is_not_null())
print(f"Loaded SignalMasterTable: {len(signal_master):,} observations")

# merge with monthlyCRSP
crsp = pl.read_parquet("../pyData/Intermediate/monthlyCRSP.parquet",
                        columns=["permno", "time_avail_m", "shrout"]).with_columns(
    pl.col("time_avail_m").cast(pl.Date)
)

# Create df: this is our working df for now 
df = signal_master.join(crsp, on=["permno", "time_avail_m"], how="inner")
print(f"SignalMasterTable merged with CRSP: {len(df):,} observations")

# merge with monthlyShortInterest
short_interest = pl.read_parquet("../pyData/Intermediate/monthlyShortInterest.parquet",
    columns=["gvkey", "time_avail_m", "shortint"]).with_columns(
    pl.col("time_avail_m").cast(pl.Date)
)

# Cast gvkey to match data types
short_interest = short_interest.with_columns(pl.col("gvkey").cast(pl.Float64))

df = df.join(short_interest, on=["gvkey", "time_avail_m"], how="inner")
print(f"After merging with short interest: {len(df):,} observations")


# merge with recommendations
df = df.join(stock_rec, on=["tickerIBES", "time_avail_m"], how="inner")
print(f"After merging with recommendations: {len(df):,} observations")

#%%

# ===================================================================
# STEP 3: SIGNAL CONSTRUCTION
# ===================================================================
print("🧮 Signal construction...")

# SIGNAL CONSTRUCTION
# Create ShortInterest = shortint/shrout
df = df.with_columns(
    (pl.col("shortint") / pl.col("shrout")).alias("ShortInterest")
)

# Create ConsRecomm = 6 - ireccd to align with coding in Drake, Rees, Swanson (2011)
df = df.with_columns(
    (6 - pl.col("ireccd12")).alias("ConsRecomm")
)

print("📊 Computing quintiles using stata_fastxtile...")

# Convert to pandas for fastxtile, then back to polars
df_pandas = df.to_pandas()

# Create quintiles for ShortInterest
df_pandas['QuintShortInterest'] = fastxtile(df_pandas, "ShortInterest", by="time_avail_m", n=5)

# Create quintiles for ConsRecomm
df_pandas['QuintConsRecomm'] = fastxtile(df_pandas, "ConsRecomm", by="time_avail_m", n=5)

# Convert back to polars
df = pl.from_pandas(df_pandas)

#%%

# Define binary signal: pessimistic vs optimistic cases
# 1 if both QuintShortInterest == 1 and QuintConsRecomm == 1 (pessimistic)
# 0 if both QuintShortInterest == 5 and QuintConsRecomm == 5 (optimistic)
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


# ===================================================================
# STEP 4: SAVE OUTPUT
# ===================================================================
print("💾 Saving Recomm_ShortInterest predictor...")
save_predictor(df, "Recomm_ShortInterest")
print("✅ Recomm_ShortInterest.csv saved successfully")

