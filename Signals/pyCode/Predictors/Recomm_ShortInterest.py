#%%

# debug
import os
os.chdir(os.path.dirname(os.path.abspath(__file__)))
os.chdir('..')
from polars import col as cc
import pandas as pd

# ABOUTME: Recommendation and Short Interest predictor combining analyst sentiment with short interest
# ABOUTME: Usage: python3 Recomm_ShortInterest.py (run from pyCode/ directory)

import polars as pl
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from utils.save_standardized import save_predictor
from utils.stata_fastxtile import fastxtile
from datetime import date

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
# use tickerIBES amaskcd anndats time_avail_m ireccd using "$pathDataIntermediate/IBES_Recommendations", clear
ibes_recs = pl.read_parquet("../pyData/Intermediate/IBES_Recommendations.parquet",
                            columns=["tickerIBES", "amaskcd", "anndats", "time_avail_m", "ireccd"]).with_columns(
                                pl.col("time_avail_m").cast(pl.Date),
                                pl.col("anndats").cast(pl.Date)
                            )

print(f"Loaded IBES Recommendations: {len(ibes_recs):,} observations")

# fill in time-series gaps by tickerIBES-amaskcd
from utils.stata_replication import fill_date_gaps
ibes_recs = ibes_recs.with_columns(
    ticker_analyst = pl.concat_str([pl.col("tickerIBES"), pl.col("amaskcd")], separator="_")
)
ibes_recs = fill_date_gaps(ibes_recs,"ticker_analyst","time_avail_m","1mo").with_columns(
    pl.col('ticker_analyst').str.split("_").list.get(0).alias("tickerIBES")
).sort(['ticker_analyst', 'time_avail_m'])

# define ireccd12: the latest recommendation within 12 months
ibes_recs = ibes_recs.with_columns(
    ireccd12 = pl.col('ireccd') 
).with_columns(
    pl.col('anndats').forward_fill().over('ticker_analyst'),
    pl.col('ireccd12').forward_fill().over('ticker_analyst')
).with_columns(
    pl.when(
        pl.col('time_avail_m') > pl.col('anndats').dt.offset_by('11mo')
    ).then(
        None
    ).otherwise(
        pl.col('ireccd12')
    ).alias('ireccd12')
)

#%% debug
pl.Config.set_tbl_rows(36)

print(
    ibes_recs.filter(
        cc('tickerIBES') == 'GFGC', cc('time_avail_m') <= pl.date(2017, 2, 1)
    ).sort(['time_avail_m','ticker_analyst']).tail(36)
)

#%% debug

# compare with stata
stata0 = pd.read_stata('../Human/temp_rs_asrol.dta')
stata0 = pl.from_pandas(stata0).with_columns(
    cc('anndats').cast(pl.Date), cc('time_avail_m').cast(pl.Date), cc('amaskcd').cast(pl.Int32),
    cc('ireccd').cast(pl.Int8), cc('ireccd12').cast(pl.Int8)
)

#%% debug
pl.Config.set_tbl_rows(36)

# check on GFGC 122399 in 2016m10
print(
stata0.filter(
    cc('tickerIBES') == 'GFGC', cc('tempID') == 122399,
    cc('time_avail_m') <= pl.date(2017, 3, 1)
).sort(['time_avail_m','tempID']).tail(36)
)

#%% debug

# compare stata and ibes_recs in detail
pl.Config.set_tbl_rows(12)

stata = stata0.with_columns(
    ticker_analyst = pl.concat_str([pl.col("tickerIBES"), pl.col("amaskcd")], separator="_")
).sort(['ticker_analyst','time_avail_m']).with_columns(
    cc('anndats').forward_fill().over('ticker_analyst')
)

both = ibes_recs.join(
    stata.select(['ticker_analyst','time_avail_m','anndats','ireccd','ireccd12']),
    on = ['ticker_analyst','time_avail_m'],
    how = 'left'
).sort(['ticker_analyst','time_avail_m']).with_columns(
    cc('time_avail_m').cast(pl.Date)
)





#%%

# take mean recommendation within each stock-month
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
# use permno gvkey tickerIBES time_avail_m bh1m using "$pathDataIntermediate/SignalMasterTable", clear
signal_master = pl.read_parquet("../pyData/Intermediate/SignalMasterTable.parquet",
                                columns=["permno", "gvkey", "tickerIBES", "time_avail_m"]).with_columns(
    pl.col("time_avail_m").cast(pl.Date)
)

# drop if mi(gvkey) | mi(tickerIBES)
signal_master = signal_master.filter(pl.col("gvkey").is_not_null() & pl.col("tickerIBES").is_not_null())
print(f"Loaded SignalMasterTable: {len(signal_master):,} observations")

# merge 1:1 permno time_avail_m using "$pathDataIntermediate/monthlyCRSP", keep(match) nogenerate keepusing(shrout)
crsp = pl.read_parquet("../pyData/Intermediate/monthlyCRSP.parquet",
                        columns=["permno", "time_avail_m", "shrout"]).with_columns(
    pl.col("time_avail_m").cast(pl.Date)
)

# Create df: this is our working df for now 
df = signal_master.join(crsp, on=["permno", "time_avail_m"], how="inner")
print(f"SignalMasterTable merged with CRSP: {len(df):,} observations")

# merge 1:1 gvkey time_avail_m using "$pathDataIntermediate/monthlyShortInterest", keep(match) nogenerate keepusing(shortint)
short_interest = pl.read_parquet("../pyData/Intermediate/monthlyShortInterest.parquet",
    columns=["gvkey", "time_avail_m", "shortint"]).with_columns(
    pl.col("time_avail_m").cast(pl.Date)
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
    (6 - pl.col("ireccd12")).alias("ConsRecomm")
)

print("📊 Computing quintiles using stata_fastxtile...")

# Convert to pandas for fastxtile, then back to polars
df_pandas = df.to_pandas()

# egen QuintShortInterest = xtile(ShortInterest), n(5) by(time_avail_m)
df_pandas['QuintShortInterest'] = fastxtile(df_pandas, "ShortInterest", by="time_avail_m", n=5)

# egen QuintConsRecomm = xtile(ConsRecomm), n(5) by(time_avail_m)  
df_pandas['QuintConsRecomm'] = fastxtile(df_pandas, "ConsRecomm", by="time_avail_m", n=5)

# Convert back to polars
df = pl.from_pandas(df_pandas)

#%% debug
pl.Config.set_tbl_rows(36)

# take a survey of obs by month
print(
    df.group_by("time_avail_m").agg(
        cc('permno').n_unique().alias("n_permno"),
        cc('ShortInterest').count().alias("n_ShortInterest"),
        cc('ConsRecomm').count().alias("n_ConsRecomm"),
        cc('QuintShortInterest').count().alias("n_QSI"),
        cc('QuintConsRecomm').count().alias("n_QCR")
    ).sort("time_avail_m").head(36)
)

pl.Config.set_tbl_rows(10)

#%%

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


# ===================================================================
# STEP 4: SAVE OUTPUT
# ===================================================================
print("💾 Saving Recomm_ShortInterest predictor...")
save_predictor(df, "Recomm_ShortInterest")
print("✅ Recomm_ShortInterest.csv saved successfully")

#%%
# read in the dta

import pandas as pd

sorted(os.listdir('../Human/'))
stata0 = pd.read_stata('../Human/temp_rs_last.dta')
stata0 = pl.from_pandas(stata0).with_columns(
   pl.col('time_avail_m').dt.date().alias('time_avail_m')
)
#%%
index_col = ['permno', 'time_avail_m']
target_cols = ['ShortInterest', 'ConsRecomm', 'Recomm_ShortInterest']


statalong = stata0.select(index_col + target_cols).unpivot(index=index_col, variable_name = 'name', value_name = 'stata').with_columns(
   pl.col('stata').cast(pl.Float64)
)


dflong = df.with_columns(
   pl.col('time_avail_m').dt.date().alias('time_avail_m')
).select(index_col + target_cols).unpivot(index=index_col, variable_name = 'name', value_name = 'python').with_columns(
   pl.col('python').cast(pl.Float64)
)


both = statalong.join(
   dflong, on = ['permno','time_avail_m','name'], how='full', coalesce=True
).sort(['permno','time_avail_m','name']).filter(
   cc('time_avail_m') >= pl.date(2010, 1, 1)
)


both = (
   both.with_columns(
       pl.when(pl.col('stata').is_null() & pl.col('python').is_null())
       .then(0)
       .when(pl.col('stata').is_not_null() & pl.col('python').is_not_null())
       .then(pl.col('stata') - pl.col('python'))
       .otherwise(pl.lit(float("inf")))
       .alias("diff")
   )
   .sort(pl.col("diff").abs(), descending=True)
)

aa = both.filter(
    cc('name') == 'ConsRecomm'
)


#%%

# check on permno 10001 in 2012-01
print(
    stata0.filter(
        cc('permno') == 10001, cc('time_avail_m') == pl.date(2012, 1, 1)
    )
)

print(
    ibes_recs.filter(
        cc('tickerIBES') == 'GFGC', cc('time_avail_m') <= pl.date(2012, 1, 1)
    )
)   