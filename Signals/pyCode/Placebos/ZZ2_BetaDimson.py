# ABOUTME: BetaDimson placebo - Dimson beta using lead, contemporaneous, and lagged market returns
# ABOUTME: Rolling regression of daily stock returns on lead, current, and lagged market returns

"""
Usage:
    python3 Placebos/ZZ2_BetaDimson.py

Inputs:
    - dailyCRSP.parquet: Daily CRSP data with columns [permno, time_d, ret]
    - dailyFF.parquet: Daily Fama-French factors with columns [time_d, rf, mktrf]

Outputs:
    - BetaDimson.csv: CSV file with columns [permno, yyyymm, BetaDimson]
    - BetaDimson = sum of coefficients from rolling regression on lead, current, and lag market returns
"""

import polars as pl
import polars_ols as pls  # Registers .least_squares namespace
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from utils.save_standardized import save_placebo

print("Starting ZZ2_BetaDimson.py...")

# DATA LOAD
print("Loading FF data...")
daily_ff = pl.read_parquet("../pyData/Intermediate/dailyFF.parquet")
ff_data = daily_ff.select(["time_d", "rf", "mktrf"])

print("Loading CRSP data...")
daily_crsp = pl.read_parquet("../pyData/Intermediate/dailyCRSP.parquet")

# Get unique permnos and process in batches to manage memory
unique_permnos = daily_crsp['permno'].unique().sort()
print(f"Processing {len(unique_permnos)} permnos in batches...")

batch_size = 100  # Process 100 permnos at a time
results = []

for i in range(0, len(unique_permnos), batch_size):
    batch_permnos = unique_permnos[i:i+batch_size]
    print(f"Processing batch {i//batch_size + 1}/{(len(unique_permnos)-1)//batch_size + 1} (permnos {batch_permnos[0]} to {batch_permnos[-1]})")
    
    # Filter CRSP data for this batch
    df_batch = daily_crsp.filter(pl.col("permno").is_in(batch_permnos.to_list()))
    df_batch = df_batch.select(["permno", "time_d", "ret"])
    
    # Merge with FF data
    df_batch = df_batch.join(ff_data, on="time_d", how="inner")
    
    # Calculate excess return (ret - rf)
    df_batch = df_batch.with_columns([
        (pl.col("ret") - pl.col("rf")).alias("ret")
    ])
    df_batch = df_batch.drop("rf")
    
    # SIGNAL CONSTRUCTION
    # Sort data by permno and time_d
    df_batch = df_batch.sort(["permno", "time_d"])
    
    # Set up time index for rolling window and create lead/lag variables
    df_batch = df_batch.with_columns([
        pl.int_range(pl.len()).over("permno").alias("time_temp")
    ])
    
    # Create lead and lag market returns within each permno group
    df_batch = df_batch.with_columns([
        pl.col("mktrf").shift(-1).over("permno").alias("tempMktLead"),  # f.mktrf
        pl.col("mktrf").shift(1).over("permno").alias("tempMktLag")     # l.mktrf
    ])
    
    # Use polars-ols for rolling regression
    df_batch = df_batch.with_columns(
        pl.col("ret").least_squares.rolling_ols(
            pl.col("tempMktLead"), pl.col("mktrf"), pl.col("tempMktLag"),
            window_size=20,
            min_periods=15,
            mode="coefficients",
            add_intercept=True,
            null_policy="drop"
        ).over("permno").alias("coef")
    ).with_columns([
        pl.col("coef").struct.field("tempMktLead").alias("_b_tempMktLead"),
        pl.col("coef").struct.field("mktrf").alias("_b_mktrf"),
        pl.col("coef").struct.field("tempMktLag").alias("_b_tempMktLag")
    ])
    
    # Calculate BetaDimson = sum of all three beta coefficients
    df_batch = df_batch.with_columns([
        (pl.col("_b_tempMktLead") + pl.col("_b_mktrf") + pl.col("_b_tempMktLag")).alias("BetaDimson")
    ])
    
    # Convert to monthly and collapse
    df_batch = df_batch.with_columns([
        pl.col("time_d").dt.truncate("1mo").alias("time_avail_m")
    ])
    
    # Sort and collapse to keep last non-missing BetaDimson per permno-month
    df_batch = df_batch.sort(["permno", "time_avail_m", "time_d"])
    batch_monthly = df_batch.group_by(["permno", "time_avail_m"]).agg([
        pl.col("BetaDimson").drop_nulls().last().alias("BetaDimson")
    ])
    
    # Add to results
    results.append(batch_monthly.select(["permno", "time_avail_m", "BetaDimson"]))
    
    print(f"Batch complete: {len(batch_monthly)} monthly observations")

# Combine all batches
print("Combining all batches...")
result = pl.concat(results)

# SAVE
save_placebo(result, "BetaDimson")
print("ZZ2_BetaDimson.py completed successfully")