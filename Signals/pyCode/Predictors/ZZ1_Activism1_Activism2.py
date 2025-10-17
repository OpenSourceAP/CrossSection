# ABOUTME: Activism1 (takeover vulnerability) and Activism2 (active shareholders) following Cremers and Nair 2005, Tables 3A and 4A
# ABOUTME: Creates shareholder activism proxy predictors based on institutional ownership and governance metrics

"""
ZZ1_Activism1_Activism2.py

How to run:
    python3 Predictors/ZZ1_Activism1_Activism2.py

Inputs:
    - ../pyData/Intermediate/SignalMasterTable.parquet
    - ../pyData/Intermediate/TR_13F.parquet (for maxinstown_perc)
    - ../pyData/Intermediate/monthlyCRSP.parquet (for shrcls)
    - ../pyData/Intermediate/GovIndex.parquet (for G variable)

Outputs:
    - ../pyData/Predictors/Activism1.csv (permno, yyyymm, Activism1)
    - ../pyData/Predictors/Activism2.csv (permno, yyyymm, Activism2)

Signal Construction:
    - Activism1: Shareholder activism proxy 1: External Gov among Large Blockheld
    - Activism2: Shareholder activism proxy 2: Blockholdings among High External Governance
"""

import pandas as pd
import polars as pl
import numpy as np
from pathlib import Path
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils.save_standardized import save_predictor
from utils.stata_fastxtile import fastxtile

# DATA LOAD
print("Loading SignalMasterTable...")
# Load main signal table with key variables
df = pl.read_parquet("../pyData/Intermediate/SignalMasterTable.parquet").select(
    ["permno", "time_avail_m", "ticker", "exchcd"]
)

print(f"Initial data loaded: {df.shape[0]} rows")

# Merge with 13F data to get maximum institutional ownership percentages
print("Merging with TR_13F...")
tr13f = pl.read_parquet("../pyData/Intermediate/TR_13F.parquet").select(
    ["permno", "time_avail_m", "maxinstown_perc"]
)

df = df.join(tr13f, on=["permno", "time_avail_m"], how="left")
print(f"After TR_13F merge: {df.shape[0]} rows")

# Merge with monthly CRSP data to get share class information
print("Merging with monthlyCRSP...")
mcrsp = pl.read_parquet("../pyData/Intermediate/monthlyCRSP.parquet").select(
    ["permno", "time_avail_m", "shrcls"]
)

df = df.join(mcrsp, on=["permno", "time_avail_m"], how="left")
print(f"After monthlyCRSP merge: {df.shape[0]} rows")

# Handle ticker-based merging by preserving records with missing tickers separately

print("Handling ticker-based merge with GovIndex...")
# Split data into records with missing ticker and non-missing ticker
temp_missing_ticker = df.filter(pl.col("ticker").is_null())
df = df.filter(pl.col("ticker").is_not_null())

print(f"Records with ticker: {df.shape[0]}")
print(f"Records without ticker: {temp_missing_ticker.shape[0]}")

# Merge governance index data by ticker for records with valid tickers
gov = pl.read_parquet("../pyData/Intermediate/GovIndex.parquet")
df = df.join(gov, on=["ticker", "time_avail_m"], how="left")

# Recombine records with missing tickers, adding null governance columns
gov_columns = [col for col in df.columns if col not in temp_missing_ticker.columns]
for col in gov_columns:
    temp_missing_ticker = temp_missing_ticker.with_columns(pl.lit(None).alias(col))

df = pl.concat([df, temp_missing_ticker])
print(f"After GovIndex merge and append: {df.shape[0]} rows")

# SIGNAL CONSTRUCTION

# Shareholder activism proxy 1: External governance for firms with large institutional blockholdings
print("Constructing Activism1 signal...")

# Create temporary blockholder variable: keep institutional ownership if >5%, otherwise set to 0
tempBLOCK = (
    pl.when(pl.col("maxinstown_perc") > 5).then(pl.col("maxinstown_perc")).otherwise(0)
)
df = df.with_columns(tempBLOCK.alias("tempBLOCK"))

# Calculate quartiles of blockholder variable within each time period
print("Calculating block holding quartiles by time_avail_m...")
# Convert to pandas for fastxtile, then back to polars
with np.errstate(over="ignore", invalid="ignore"):
    df_pandas = df.to_pandas()
    df_pandas["tempBLOCKQuant"] = fastxtile(
        df_pandas, "tempBLOCK", by="time_avail_m", n=4
    )
    df = pl.from_pandas(df_pandas)

# Create external governance measure: 24 minus G-index (higher values = better external governance)
df = df.with_columns(
    pl.when(pl.col("G").is_null())
    .then(None)
    .otherwise(24 - pl.col("G"))
    .alias("tempEXT")
)

# Restrict to top quartile of blockholder firms and exclude dual-class shares
df = df.with_columns(
    pl.when(pl.col("tempBLOCKQuant") <= 3)
    .then(None)  # Keep only quartile 4 (now correctly 1-based)
    .when(pl.col("shrcls") != "")
    .then(None)  # Exclude dual class shares (non-empty shrcls)
    .otherwise(pl.col("tempEXT"))
    .alias("tempEXT")
)

# Final Activism1 signal: external governance among large blockheld firms
df = df.with_columns(pl.col("tempEXT").alias("Activism1"))

print(f"Activism1 signal constructed")

# Check for non-missing values
non_missing_count = df.filter(pl.col("Activism1").is_not_null()).shape[0]
print(f"Non-missing Activism1 values: {non_missing_count}")

# Clean up temporary variables
df = df.drop(["tempBLOCK", "tempBLOCKQuant", "tempEXT"])

# Shareholder activism proxy 2: Blockholdings among high external governance firms
print("Constructing Activism2 signal...")

# Create blockholder variable: keep institutional ownership if >5%, otherwise set to 0
tempBLOCK = (
    pl.when(pl.col("maxinstown_perc") > 5).then(pl.col("maxinstown_perc")).otherwise(0)
)
df = df.with_columns(tempBLOCK.alias("tempBLOCK"))

# Exclude firms with missing governance data and dual-class shares
df = df.with_columns(
    pl.when(pl.col("G").is_null())
    .then(None)
    .when((pl.col("shrcls") != "") & (pl.col("shrcls").is_not_null()))
    .then(None)  # Exclude dual class shares
    .otherwise(pl.col("tempBLOCK"))
    .alias("tempBLOCK")
)

# Restrict to firms with high external governance (external governance >= 19)
df = df.with_columns(
    pl.when((24 - pl.col("G")) < 19)
    .then(None)
    .otherwise(pl.col("tempBLOCK"))
    .alias("tempBLOCK")
)

# Final Activism2 signal: blockholdings among high external governance firms
df = df.with_columns(pl.col("tempBLOCK").alias("Activism2"))

print(f"Activism2 signal constructed")

# Check for non-missing values
non_missing_count = df.filter(pl.col("Activism2").is_not_null()).shape[0]
print(f"Non-missing Activism2 values: {non_missing_count}")

# SAVE
# Save both predictor signals
print("Saving Activism1...")
save_predictor(df.to_pandas(), "Activism1")

print("Saving Activism2...")
save_predictor(df.to_pandas(), "Activism2")

print("Activism1 and Activism2 predictors completed!")
