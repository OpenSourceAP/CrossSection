# ABOUTME: Share Volume following Datar, Naik and Radcliffe 1998, Table 2A Turnover
# ABOUTME: calculates binary signal based on share volume thresholds (0 if <5%, 1 if >10%)
"""
Usage:
    python3 Predictors/ShareVol.py

Inputs:
    - SignalMasterTable.parquet: Monthly master table with [permno, time_avail_m, sicCRSP, exchcd]
    - monthlyCRSP.parquet: Monthly CRSP data with [permno, time_avail_m, shrout, vol]

Outputs:
    - ShareVol.csv: CSV file with columns [permno, yyyymm, ShareVol]
    - ShareVol = 0 if 3-month average share volume < 5%, 1 if > 10%, missing otherwise
"""

import polars as pl
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from utils.save_standardized import save_predictor
from utils.stata_replication import stata_ineq_pl

print("Starting ShareVol.py...")

# DATA LOAD
print("Loading SignalMasterTable...")
# Load base universe of stocks with identifiers and classification data
signal_master = pl.read_parquet("../pyData/Intermediate/SignalMasterTable.parquet")
df = signal_master.select(["permno", "time_avail_m", "sicCRSP", "exchcd"])
print(f"Loaded SignalMasterTable: {df.shape[0]} rows")

print("Merging with monthly CRSP data...")
# Add volume and shares outstanding data from monthly CRSP
monthly_crsp = pl.read_parquet("../pyData/Intermediate/monthlyCRSP.parquet")
df = df.join(
    monthly_crsp.select(["permno", "time_avail_m", "shrout", "vol"]),
    on=["permno", "time_avail_m"],
    how="inner"
)
print(f"After merge: {df.shape[0]} rows")

# SIGNAL CONSTRUCTION
print("Setting up panel data structure...")
# Sort data to enable time series operations within each stock
df = df.sort(["permno", "time_avail_m"])

print("Creating lag variables for volume calculation...")
# Calculate 3-month rolling share volume using current and previous 2 months
df = df.with_columns([
    pl.col("vol").shift(1).over("permno").alias("l1_vol"),
    pl.col("vol").shift(2).over("permno").alias("l2_vol"),
    pl.col("shrout").shift(1).over("permno").alias("l1_shrout")
])

df = df.with_columns([
    ((pl.col("vol") + pl.col("l1_vol") + pl.col("l2_vol")) / 
     (3 * pl.col("shrout")) * 100).alias("tempShareVol")
])

# Exclude observations where shares outstanding changed in the past 3 months
# Identify changes in shares outstanding
df = df.with_columns([
    (pl.col("shrout") != pl.col("l1_shrout")).alias("dshrout")
])

# Set up observation numbering for each stock
df = df.with_columns([
    pl.int_range(pl.len()).over("permno").alias("_n")
])

# Set no change for first observation (no prior period to compare)
df = df.with_columns([
    pl.when(pl.col("_n") == 0)
    .then(False)
    .otherwise(pl.col("dshrout"))
    .alias("dshrout")
])

# Create lagged indicators of shares outstanding changes
df = df.with_columns([
    pl.col("dshrout").shift(1).over("permno").alias("l1_dshrout"),
    pl.col("dshrout").shift(2).over("permno").alias("l2_dshrout")
])

# Flag observations for dropping if any change occurred in current or prior 2 months
df = df.with_columns([
    (pl.col("dshrout").cast(pl.Int32) + 
     pl.col("l1_dshrout").fill_null(False).cast(pl.Int32) + 
     pl.col("l2_dshrout").fill_null(False).cast(pl.Int32) > 0).alias("dropObs")
])

# Don't drop first two observations as they lack full history
df = df.with_columns([
    pl.when((pl.col("_n") == 0) | (pl.col("_n") == 1))
    .then(None)
    .otherwise(pl.col("dropObs"))
    .alias("dropObs")
])

# Filter out flagged observations
df = df.filter(
    (pl.col("dropObs") != True) | (pl.col("dropObs").is_null())
)

# Create binary signal based on share volume thresholds
# Low volume (< 5) = 0, high volume (> 10) = 1, middle range remains missing
# Missing share volume values are treated as high and assigned 1
df = df.with_columns([
    pl.when(stata_ineq_pl(pl.col("tempShareVol"), "<", pl.lit(5)))
    .then(0)
    .when(stata_ineq_pl(pl.col("tempShareVol"), ">", pl.lit(10)))
    .then(1)
    .otherwise(None)
    .alias("ShareVol")
])

print("Calculating ShareVol signal...")
# Select final result columns
result = df.select(["permno", "time_avail_m", "ShareVol"])
print(f"Calculated ShareVol for {result.shape[0]} observations")

# SAVE
save_predictor(result, "ShareVol")
print("ShareVol.py completed successfully")