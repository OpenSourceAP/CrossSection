# ABOUTME: Coskewness following Harvey and Siddique 2000, in text p 1276
# ABOUTME: calculates systematic coskewness using sample moments of demeaned returns over 60 months
"""
Usage:
    python3 Predictors/Coskewness.py

Inputs:
    - monthlyCRSP.parquet: Monthly CRSP data with columns [permno, time_avail_m, ret]
    - monthlyFF.parquet: Monthly Fama-French data with columns [time_avail_m, mktrf, rf]

Outputs:
    - Coskewness.csv: CSV file with columns [permno, yyyymm, Coskewness]
    - Coskewness = E[r*m^2] / (sqrt(E[r^2]) * E[m^2]) using demeaned returns over 60 months
"""

import polars as pl
import warnings
from pathlib import Path
warnings.filterwarnings('ignore')

# Set up paths
base_path = Path("../pyData")
intermediate_path = base_path / "Intermediate" 
predictors_path = base_path / "Predictors"
predictors_path.mkdir(exist_ok=True)

print("Loading monthly CRSP data...")

# Load monthly CRSP data
monthly_crsp = pl.read_parquet(intermediate_path / "monthlyCRSP.parquet")
print(f"Loaded monthlyCRSP: {monthly_crsp.shape} rows")

print("Loading monthly Fama-French data...")

# Load monthly Fama-French data
monthly_ff = pl.read_parquet(intermediate_path / "monthlyFF.parquet")
print(f"Loaded monthlyFF: {monthly_ff.shape} rows")

print("Merging CRSP and FF data...")

# Merge with FF data to get market returns and risk-free rates
merged_data = monthly_crsp.join(
    monthly_ff.select(["time_avail_m", "mktrf", "rf"]),
    on="time_avail_m",
    how="inner"
).filter(
    pl.col("mktrf").is_not_null() & pl.col("rf").is_not_null()
)

print(f"After merging with FF: {merged_data.shape} rows")

# Convert to excess returns by subtracting risk-free rate
merged_data = merged_data.with_columns([
    pl.col("mktrf").alias("mkt"),
    (pl.col("ret") - pl.col("rf")).alias("ret")
]).drop(["rf", "mktrf"])

print(f"Data ready for processing: {merged_data.shape} rows")

# Sort data in reverse chronological order by permno and time
merged_data = merged_data.sort(["permno", "time_avail_m"], descending=[False, True])

# Convert time to integer format and create 60-month cycle identifier
merged_data = merged_data.with_columns([
    ((pl.col("time_avail_m").dt.year() - 1960) * 12 + (pl.col("time_avail_m").dt.month() - 1)).alias("time_avail_m_int"),
]).with_columns([
    (pl.col("time_avail_m_int") % 60).alias("m60")
])

print(f"Generated m60 variable with values 0-59")

print("Starting 60-batch processing loop...")

# Initialize list to store results from each batch
batch_results = []

# Process data in 60 separate batches corresponding to different month positions in the cycle
for m in range(60):
    print(f"Processing batch {m+1}/60...")
    
    # Start with the merged data for this batch
    batch_df = merged_data.clone()
    
    # Set time values to missing for observations not in current batch
    batch_df = batch_df.with_columns([
        pl.when(pl.col("m60") != m)
        .then(None)
        .otherwise(pl.col("time_avail_m_int"))
        .alias("time_avail_m_batch")
    ])
    
    # Forward fill time values within each permno to create overlapping periods
    batch_df = batch_df.with_columns([
        pl.col("time_avail_m_batch").forward_fill().over("permno").alias("time_avail_m_filled")
    ])
    
    # Remove observations without valid time assignments
    batch_df = batch_df.filter(pl.col("time_avail_m_filled").is_not_null())
    
    # Drop unnecessary columns
    batch_df = batch_df.drop(["time_avail_m", "time_avail_m_int", "m60"])
    
    print(f"  Batch {m+1}: {batch_df.shape[0]} observations after time assignment")
    
    # Calculate mean returns and market returns within each time period
    means_df = batch_df.group_by(["permno", "time_avail_m_filled"]).agg([
        pl.col("ret").mean().alias("E_ret"),
        pl.col("mkt").mean().alias("E_mkt")
    ])
    
    # Demean returns by subtracting period-specific means 
    batch_df = batch_df.join(means_df, on=["permno", "time_avail_m_filled"], how="inner")
    batch_df = batch_df.with_columns([
        (pl.col("ret") - pl.col("E_ret")).alias("ret_demeaned"),
        (pl.col("mkt") - pl.col("E_mkt")).alias("mkt_demeaned")
    ]).drop(["E_ret", "E_mkt"])
    
    # Calculate squared terms and cross-moment needed for coskewness
    batch_df = batch_df.with_columns([
        pl.col("ret_demeaned").pow(2).alias("ret2"),
        pl.col("mkt_demeaned").pow(2).alias("mkt2"),
        (pl.col("ret_demeaned") * pl.col("mkt_demeaned").pow(2)).alias("ret_mkt2")
    ])
    
    # Calculate expected values of moment terms for each permno-time period
    coskew_df = batch_df.group_by(["permno", "time_avail_m_filled"]).agg([
        pl.col("ret_mkt2").mean().alias("E_ret_mkt2"),
        pl.col("ret2").mean().alias("E_ret2"),
        pl.col("mkt2").mean().alias("E_mkt2"),
        pl.col("ret_demeaned").count().alias("nobs")  # Count observations for minimum requirement
    ])
    
    # Calculate coskewness using standardized third moment formula
    coskew_df = coskew_df.with_columns([
        (pl.col("E_ret_mkt2") / (pl.col("E_ret2").sqrt() * pl.col("E_mkt2"))).alias("Coskewness")
    ])
    
    # Require minimum of 12 observations for reliable coskewness estimation
    coskew_df = coskew_df.filter(
        pl.col("nobs") >= 12
    )
    
    # Keep only required columns and rename time_avail_m_filled back to time_avail_m
    batch_result = coskew_df.select([
        pl.col("permno"),
        pl.col("time_avail_m_filled").alias("time_avail_m"), 
        pl.col("Coskewness")
    ])
    
    batch_results.append(batch_result)
    print(f"  Batch {m+1}: {batch_result.shape[0]} final observations")

print("Combining all batches...")

# Combine results from all 60 batches
final_result = pl.concat(batch_results)

print(f"Final combined dataset: {final_result.shape} rows")

# Convert time_avail_m back to standard yyyymm format for consistency with other predictors
final_result = final_result.with_columns([
    (1960 + pl.col("time_avail_m") // 12).cast(pl.Int64).alias("yyyy"),
    (pl.col("time_avail_m") % 12 + 1).cast(pl.Int64).alias("mm")
]).with_columns([
    (pl.col("yyyy") * 100 + pl.col("mm")).alias("yyyymm")
]).select([
    "permno", "yyyymm", "Coskewness"
])

# Sort by permno and yyyymm for consistency
final_result = final_result.sort(["permno", "yyyymm"])

print("Final summary statistics:")
print(final_result.describe())

print("Saving to CSV...")

# Save final result to CSV file
final_result.write_csv(predictors_path / "Coskewness.csv")

print(f"✅ Coskewness.csv saved with {final_result.shape[0]} observations")
print("Coskewness translation complete!")