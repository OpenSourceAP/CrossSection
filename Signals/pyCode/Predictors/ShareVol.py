# ABOUTME: Share Volume - volatility of share volume (vol/shrout) over 3 months
# ABOUTME: Usage: python3 ShareVol.py (run from pyCode/ directory)

import polars as pl
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'utils'))
from savepredictor import save_predictor
from stata_replication import stata_ineq_pl

# DATA LOAD
# use permno time_avail_m sicCRSP exchcd using "$pathDataIntermediate/SignalMasterTable", clear
signal_master = pl.read_parquet("../pyData/Intermediate/SignalMasterTable.parquet")
df = signal_master.select(["permno", "time_avail_m", "sicCRSP", "exchcd"])

# merge 1:1 permno time_avail_m using "$pathDataIntermediate/monthlyCRSP", keepusing(shrout vol) nogenerate keep(match)
monthly_crsp = pl.read_parquet("../pyData/Intermediate/monthlyCRSP.parquet")
df = df.join(
    monthly_crsp.select(["permno", "time_avail_m", "shrout", "vol"]),
    on=["permno", "time_avail_m"],
    how="inner"  # keep(match) in Stata = inner join
)

# SIGNAL CONSTRUCTION
# Sort for lag operations (equivalent to xtset permno time_avail_m)
df = df.sort(["permno", "time_avail_m"])

# gen tempShareVol = (vol + l1.vol + l2.vol)/(3*shrout)*100
# Use position-based lags (l1.vol, l2.vol) - Stata's xtset makes these position-based within permno
df = df.with_columns([
    pl.col("vol").shift(1).over("permno").alias("l1_vol"),
    pl.col("vol").shift(2).over("permno").alias("l2_vol"),
    pl.col("shrout").shift(1).over("permno").alias("l1_shrout")
])

df = df.with_columns([
    ((pl.col("vol") + pl.col("l1_vol") + pl.col("l2_vol")) / 
     (3 * pl.col("shrout")) * 100).alias("tempShareVol")
])

# * drop if shrout changes in last 3 months
# gen dshrout = shrout != l1.shrout
df = df.with_columns([
    (pl.col("shrout") != pl.col("l1_shrout")).alias("dshrout")
])

# bys permno (time_avail_m): replace dshrout = 0 if _n == 1  // Set to no change in first month
df = df.with_columns([
    pl.int_range(pl.len()).over("permno").alias("_n")
])

df = df.with_columns([
    pl.when(pl.col("_n") == 0)  # First observation (0-indexed)
    .then(False)
    .otherwise(pl.col("dshrout"))
    .alias("dshrout")
])

# Create l1.dshrout and l2.dshrout using position-based lags
df = df.with_columns([
    pl.col("dshrout").shift(1).over("permno").alias("l1_dshrout"),
    pl.col("dshrout").shift(2).over("permno").alias("l2_dshrout")
])

# gen dropObs = 1 if (dshrout + l1.dshrout + l2.dshrout) > 0
# Convert boolean to int (True=1, False=0) for addition, treating null as 0
df = df.with_columns([
    (pl.col("dshrout").cast(pl.Int32) + 
     pl.col("l1_dshrout").fill_null(False).cast(pl.Int32) + 
     pl.col("l2_dshrout").fill_null(False).cast(pl.Int32) > 0).alias("dropObs")
])

# bys permno (time_avail_m): replace dropObs = . if _n == 1 | _n == 2  // Don't drop if first two months
df = df.with_columns([
    pl.when((pl.col("_n") == 0) | (pl.col("_n") == 1))  # First two observations
    .then(None)
    .otherwise(pl.col("dropObs"))
    .alias("dropObs")
])

# drop if dropObs == 1
df = df.filter(
    (pl.col("dropObs") != True) | (pl.col("dropObs").is_null())
)

# gen ShareVol = 0 if tempShareVol < 5 
# replace ShareVol = 1 if tempShareVol > 10
# Note: In Stata, missing tempShareVol is treated as positive infinity
# So missing values satisfy "tempShareVol > 10" and get ShareVol = 1
df = df.with_columns([
    pl.when(stata_ineq_pl(pl.col("tempShareVol"), "<", pl.lit(5)))
    .then(0)
    .when(stata_ineq_pl(pl.col("tempShareVol"), ">", pl.lit(10)))
    .then(1)
    .otherwise(None)
    .alias("ShareVol")
])

# Select final columns - keep ALL observations, including those with missing ShareVol
# (though in this case there should be no missing ShareVol due to Stata's missing=infinity logic)
result = df.select(["permno", "time_avail_m", "ShareVol"])

# SAVE
save_predictor(result, "ShareVol")