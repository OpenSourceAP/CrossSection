# ABOUTME: Activism1.py - translates Activism1 predictor from Stata to Python
# ABOUTME: Replicates ZZ1_Activism1_Activism2.do line-by-line, outputs Activism1 signal only

"""
Activism1.py

How to run:
    python3 Predictors/Activism1.py

Inputs:
    - ../pyData/Intermediate/SignalMasterTable.parquet
    - ../pyData/Intermediate/TR_13F.parquet (for maxinstown_perc)
    - ../pyData/Intermediate/monthlyCRSP.parquet (for shrcls)
    - ../pyData/Intermediate/GovIndex.parquet (for G variable)

Outputs:
    - ../pyData/Predictors/Activism1.csv (permno, yyyymm, Activism1)

Signal Construction:
    - Shareholder activism proxy 1: External Gov among Large Blockheld
    - Based on external governance score (24-G) among firms with large blockholdings (top quartile >5%)
    - Excludes dual class shares
"""

import pandas as pd
import polars as pl
from pathlib import Path
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils.savepredictor import save_predictor

# DATA LOAD
print("Loading SignalMasterTable...")
# use permno time_avail_m ticker exchcd mve_c using "$pathDataIntermediate/SignalMasterTable", clear
df = pl.read_parquet("../pyData/Intermediate/SignalMasterTable.parquet").select([
    'permno', 'time_avail_m', 'ticker', 'exchcd', 'mve_c'
])

print(f"Initial data loaded: {df.shape[0]} rows")

# merge 1:1 permno time_avail_m using "$pathDataIntermediate/TR_13F", keep(master match) nogenerate keepusing(maxinstown_perc)
print("Merging with TR_13F...")
tr13f = pl.read_parquet("../pyData/Intermediate/TR_13F.parquet").select([
    'permno', 'time_avail_m', 'maxinstown_perc'
])

df = df.join(tr13f, on=['permno', 'time_avail_m'], how='left')
print(f"After TR_13F merge: {df.shape[0]} rows")

# merge 1:1 permno time_avail_m using "$pathDataIntermediate/monthlyCRSP", keep(master match) nogenerate keepusing(shrcls)
print("Merging with monthlyCRSP...")
mcrsp = pl.read_parquet("../pyData/Intermediate/monthlyCRSP.parquet").select([
    'permno', 'time_avail_m', 'shrcls'
])

df = df.join(mcrsp, on=['permno', 'time_avail_m'], how='left')
print(f"After monthlyCRSP merge: {df.shape[0]} rows")

# * Add ticker-based data (many to one match due to permno-ticker not being unique in crsp)
# preserve
#     keep if mi(ticker)
#     save "$pathtemp/temp", replace
# restore

print("Handling ticker-based merge with GovIndex...")
# Split data into records with missing ticker and non-missing ticker
temp_missing_ticker = df.filter(pl.col('ticker').is_null())
df = df.filter(pl.col('ticker').is_not_null())

print(f"Records with ticker: {df.shape[0]}")
print(f"Records without ticker: {temp_missing_ticker.shape[0]}")

# merge m:1 ticker time_avail_m using "$pathDataIntermediate/GovIndex", keep(master match) nogenerate
gov = pl.read_parquet("../pyData/Intermediate/GovIndex.parquet")
df = df.join(gov, on=['ticker', 'time_avail_m'], how='left')

# append using "$pathtemp/temp"
# Need to add the missing columns from GovIndex to temp_missing_ticker with null values
gov_columns = [col for col in df.columns if col not in temp_missing_ticker.columns]
for col in gov_columns:
    temp_missing_ticker = temp_missing_ticker.with_columns(pl.lit(None).alias(col))

df = pl.concat([df, temp_missing_ticker])
print(f"After GovIndex merge and append: {df.shape[0]} rows")

# SIGNAL CONSTRUCTION

# * Shareholder activism proxy 1
print("Constructing Activism1 signal...")

# gen tempBLOCK = maxinstown_perc if maxinstown_perc > 5
# replace tempBLOCK = 0 if tempBLOCK == .
tempBLOCK = pl.when(pl.col('maxinstown_perc') > 5).then(pl.col('maxinstown_perc')).otherwise(0)
df = df.with_columns(tempBLOCK.alias('tempBLOCK'))

# egen tempBLOCKQuant = fastxtile(tempBLOCK), n(4) by(time_avail_m)
print("Calculating block holding quartiles by time_avail_m...")
df = df.with_columns(
    pl.col('tempBLOCK').qcut(4, labels=['1', '2', '3', '4'], allow_duplicates=True).over('time_avail_m').alias('tempBLOCKQuant')
)

# gen tempEXT = 24 - G
# replace tempEXT = . if G == . 
df = df.with_columns(
    pl.when(pl.col('G').is_null()).then(None)
    .otherwise(24 - pl.col('G'))
    .alias('tempEXT')
)

# replace tempEXT = . if tempBLOCKQuant <= 3
# replace tempEXT = . if !mi(shrcls) // Exclude dual class shares
df = df.with_columns(
    pl.when(pl.col('tempBLOCKQuant') != '4').then(None)  # Keep only quartile 4
    .when(pl.col('shrcls') != '').then(None)  # Exclude dual class shares (non-empty shrcls)
    .otherwise(pl.col('tempEXT'))
    .alias('tempEXT')
)

# gen Activism1 = tempEXT
df = df.with_columns(pl.col('tempEXT').alias('Activism1'))

print(f"Activism1 signal constructed")

# Check for non-missing values
non_missing_count = df.filter(pl.col('Activism1').is_not_null()).shape[0]
print(f"Non-missing Activism1 values: {non_missing_count}")

# SAVE
print("Saving Activism1...")
save_predictor(df.to_pandas(), 'Activism1')

print("Activism1 predictor completed!")