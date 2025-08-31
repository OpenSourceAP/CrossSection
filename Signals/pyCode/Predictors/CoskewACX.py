# ABOUTME: Translates CoskewACX.do to generate coskewness following Ang, Chen, Xing 2006 with 12-month batched processing
# ABOUTME: Replicates ACX appendix equation B-9 using daily CRSP data processed in monthly batches (Jan-Dec)
#
# This script translates Code/Predictors/CoskewACX.do to Python
# Following Appendix and Table 8 caption from Ang, Chen, Xing 2006
# 
# Algorithm overview:
# 1. Load daily CRSP and Fama-French data from 1962-07-02 onwards
# 2. Convert returns to continuous-time compounded excess returns
# 3. Process data in 12 monthly batches (m=1 to 12 for Jan to Dec)
# 4. For each batch m: create overlapping 12-month periods ending in month m
# 5. Demean returns within each 12-month period
# 6. Calculate coskewness using sample moments: E[r*m^2] / (sqrt(E[r^2]) * E[m^2])
# 7. Filter observations with too many missing values (>5 missing vs max in period)
# 8. Combine all 12 batches into final output
#
# Input: ../pyData/Intermediate/dailyCRSP.parquet, ../pyData/Intermediate/dailyFF.parquet
# Output: ../pyData/Predictors/CoskewACX.csv
#
# Run: python3 CoskewACX.py (from pyCode/ directory with .venv activated)

import polars as pl
import numpy as np
from pathlib import Path
import warnings
warnings.filterwarnings('ignore')

# Set up paths
base_path = Path("../pyData")
intermediate_path = base_path / "Intermediate" 
predictors_path = base_path / "Predictors"
predictors_path.mkdir(exist_ok=True)

print("Loading daily CRSP data...")

# Load daily CRSP data
daily_crsp = pl.read_parquet(intermediate_path / "dailyCRSP.parquet")
print(f"Loaded dailyCRSP: {daily_crsp.shape} rows")

# Keep only data from 1962-07-02 onwards
daily_crsp = daily_crsp.filter(
    pl.col("time_d") >= pl.date(1962, 7, 2)
)
print(f"After 1962-07-02 filter: {daily_crsp.shape} rows")

print("Loading daily Fama-French data...")

# Load daily Fama-French data
daily_ff = pl.read_parquet(intermediate_path / "dailyFF.parquet")
print(f"Loaded dailyFF: {daily_ff.shape} rows")

print("Merging CRSP and FF data...")

# Merge with Fama-French data, keeping only matching dates with valid mktrf and rf
merged_data = daily_crsp.join(
    daily_ff.select(["time_d", "mktrf", "rf"]),
    on="time_d",
    how="inner"
).filter(
    pl.col("mktrf").is_not_null() & pl.col("rf").is_not_null()
)

print(f"After merging with FF: {merged_data.shape} rows")

# Create market return by adding risk-free rate to market excess return
merged_data = merged_data.with_columns([
    (pl.col("mktrf") + pl.col("rf")).alias("mkt")
])

print("Converting to continuous-time compounded returns...")

# Convert to continuous-time compounded excess returns using natural log transformation
merged_data = merged_data.with_columns([
    (pl.col("mkt").add(1).log() - pl.col("rf").add(1).log()).alias("mkt"),
    (pl.col("ret").add(1).log() - pl.col("rf").add(1).log()).alias("ret")
]).drop("rf")

print(f"Data ready for processing: {merged_data.shape} rows")

# Sort by permno and reverse chronological order for rolling window calculations
merged_data = merged_data.sort(["permno", "time_d"], descending=[False, True])

print("Starting 12-month batch processing loop...")

# Initialize list to store results from each batch
batch_results = []

# Process 12 batches, one for each month (January through December)
for m in range(1, 13):
    print(f"Processing batch {m}/12...")
    
    # Start with the merged data for this batch
    batch_df = merged_data.clone()
    
    # Create time availability marker for observations in month m
    batch_df = batch_df.with_columns([
        pl.when(pl.col("time_d").dt.month() == m)
        .then((pl.col("time_d").dt.year() - 1960) * 12 + (pl.col("time_d").dt.month() - 1))
        .otherwise(None)
        .alias("time_avail_m")
    ])
    
    # Forward fill time markers within each security to create rolling 12-month periods
    batch_df = batch_df.with_columns([
        pl.col("time_avail_m").forward_fill().over("permno").alias("time_avail_m_filled")
    ])
    
    # Remove observations without valid time periods
    batch_df = batch_df.filter(pl.col("time_avail_m_filled").is_not_null())
    
    # Remove daily date column as it's no longer needed
    batch_df = batch_df.drop("time_d")
    
    print(f"  Batch {m}: {batch_df.shape[0]} observations after time assignment")
    
    # Calculate mean returns for each security-period to enable demeaning
    means_df = batch_df.group_by(["permno", "time_avail_m_filled"]).agg([
        pl.col("ret").mean().alias("E_ret"),
        pl.col("mkt").mean().alias("E_mkt")
    ])
    
    # Create demeaned returns by subtracting period means (tilde notation in ACX appendix)
    batch_df = batch_df.join(means_df, on=["permno", "time_avail_m_filled"], how="inner")
    batch_df = batch_df.with_columns([
        (pl.col("ret") - pl.col("E_ret")).alias("ret_demeaned"),
        (pl.col("mkt") - pl.col("E_mkt")).alias("mkt_demeaned")
    ]).drop(["E_ret", "E_mkt"])
    
    # Calculate squared terms and cross-products needed for coskewness formula
    batch_df = batch_df.with_columns([
        pl.col("ret_demeaned").pow(2).alias("ret2"),
        pl.col("mkt_demeaned").pow(2).alias("mkt2"),
        (pl.col("ret_demeaned") * pl.col("mkt_demeaned").pow(2)).alias("ret_mkt2")
    ])
    
    # Calculate sample moments: E[r*m²], E[r²], E[m²] for each security-period
    coskew_df = batch_df.group_by(["permno", "time_avail_m_filled"]).agg([
        pl.col("ret_mkt2").mean().alias("E_ret_mkt2"),
        pl.col("ret2").mean().alias("E_ret2"),
        pl.col("mkt2").mean().alias("E_mkt2"),
        pl.col("ret_demeaned").count().alias("nobs")
    ])
    
    # Calculate coskewness using ACX formula: E[r*m²] / (sqrt(E[r²]) * E[m²])
    coskew_df = coskew_df.with_columns([
        (pl.col("E_ret_mkt2") / (pl.col("E_ret2").sqrt() * pl.col("E_mkt2"))).alias("CoskewACX")
    ])
    
    # Filter out observations with insufficient data (>5 missing vs maximum in period)
    max_nobs_df = coskew_df.group_by("time_avail_m_filled").agg([
        pl.col("nobs").max().alias("max_nobs")
    ])
    
    coskew_df = coskew_df.join(max_nobs_df, on="time_avail_m_filled", how="inner")
    coskew_df = coskew_df.filter(
        (pl.col("max_nobs") - pl.col("nobs")) <= 5
    )
    
    # Keep only required columns and rename time_avail_m_filled back to time_avail_m
    batch_result = coskew_df.select([
        pl.col("permno"),
        pl.col("time_avail_m_filled").alias("time_avail_m"), 
        pl.col("CoskewACX")
    ])
    
    batch_results.append(batch_result)
    print(f"  Batch {m}: {batch_result.shape[0]} final observations")

print("Combining all batches...")

# Combine results from all 12 monthly batches
final_result = pl.concat(batch_results)

print(f"Final combined dataset: {final_result.shape} rows")

# Convert time_avail_m back to standard yyyymm format for consistency with other predictors
final_result = final_result.with_columns([
    (1960 + pl.col("time_avail_m") // 12).cast(pl.Int64).alias("yyyy"),
    (pl.col("time_avail_m") % 12 + 1).cast(pl.Int64).alias("mm")
]).with_columns([
    (pl.col("yyyy") * 100 + pl.col("mm")).alias("yyyymm")
]).select([
    "permno", "yyyymm", "CoskewACX"
])

# Sort by permno and yyyymm for consistency
final_result = final_result.sort(["permno", "yyyymm"])

print("Final summary statistics:")
print(final_result.describe())

print("Saving to CSV...")

# Save final coskewness predictor results
final_result.write_csv(predictors_path / "CoskewACX.csv")

print(f"✅ CoskewACX.csv saved with {final_result.shape[0]} observations")
print("CoskewACX translation complete!")