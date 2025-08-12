# ABOUTME: Translates Coskewness.do to generate coskewness predictor using 60-batch processing strategy
# ABOUTME: Replicates exact Stata logic with simplified time handling following CoskewACX pattern
#
# This script translates Code/Predictors/Coskewness.do to Python
# Using monthly CRSP data with 60-batch forward-fill processing
# 
# Algorithm overview:
# 1. Load monthly CRSP and Fama-French data
# 2. Convert to simple excess returns (ret - rf, mkt = mktrf) 
# 3. Process data in 60 monthly batches (m=0 to 59) based on mod(time_avail_m, 60)
# 4. For each batch m: forward-fill time_avail_m to create overlapping periods
# 5. Demean returns within each time period (simple demeaning, not CAPM residuals)
# 6. Calculate coskewness using sample moments: E[r*m^2] / (sqrt(E[r^2]) * E[m^2])
# 7. Filter to require >= 12 observations per period
# 8. Combine all 60 batches into final output
#
# Input: ../pyData/Intermediate/monthlyCRSP.parquet, ../pyData/Intermediate/monthlyFF.parquet
# Output: ../pyData/Predictors/Coskewness.csv
#
# Run: python3 Coskewness.py (from pyCode/ directory with .venv activated)

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

# Load monthly CRSP data - equivalent to: use permno time_avail_m ret using "$pathDataIntermediate/monthlyCRSP.dta"
monthly_crsp = pl.read_parquet(intermediate_path / "monthlyCRSP.parquet")
print(f"Loaded monthlyCRSP: {monthly_crsp.shape} rows")

print("Loading monthly Fama-French data...")

# Load monthly FF data - equivalent to: merge m:1 time_avail_m using "$pathDataIntermediate/monthlyFF"
monthly_ff = pl.read_parquet(intermediate_path / "monthlyFF.parquet")
print(f"Loaded monthlyFF: {monthly_ff.shape} rows")

print("Merging CRSP and FF data...")

# Merge with FF data - equivalent to: merge m:1 time_avail_m using ... nogenerate keep(match) keepusing(mktrf rf)
merged_data = monthly_crsp.join(
    monthly_ff.select(["time_avail_m", "mktrf", "rf"]),
    on="time_avail_m",
    how="inner"
).filter(
    pl.col("mktrf").is_not_null() & pl.col("rf").is_not_null()
)

print(f"After merging with FF: {merged_data.shape} rows")

# Convert to excess returns "in place" - equivalent to:
# replace mkt = mktrf
# replace ret = ret - rf
merged_data = merged_data.with_columns([
    pl.col("mktrf").alias("mkt"),
    (pl.col("ret") - pl.col("rf")).alias("ret")
]).drop(["rf", "mktrf"])

print(f"Data ready for processing: {merged_data.shape} rows")

# Set up for looping over 60-month window sets - equivalent to Stata's reverse time sorting
# gen temptime = -time_avail_m, sort permno temptime, drop temptime
merged_data = merged_data.sort(["permno", "time_avail_m"], descending=[False, True])

# Convert time_avail_m to integer format matching Stata's time format
# gen m60 = mod(time_avail_m,60) // month in a 60 month per year calender
merged_data = merged_data.with_columns([
    ((pl.col("time_avail_m").dt.year() - 1960) * 12 + (pl.col("time_avail_m").dt.month() - 1)).alias("time_avail_m_int"),
]).with_columns([
    (pl.col("time_avail_m_int") % 60).alias("m60")
])

print(f"Generated m60 variable with values 0-59")

print("Starting 60-batch processing loop...")

# Initialize list to store results from each batch
batch_results = []

# Process 60 batches (m=0 to 59) - equivalent to: forvalues m=0/59
for m in range(60):
    print(f"Processing batch {m+1}/60...")
    
    # Start with the merged data for this batch
    batch_df = merged_data.clone()
    
    # Create time_avail_m for batch m - equivalent to:
    # replace time_avail_m = . if m60 != `m'
    batch_df = batch_df.with_columns([
        pl.when(pl.col("m60") != m)
        .then(None)
        .otherwise(pl.col("time_avail_m_int"))
        .alias("time_avail_m_batch")
    ])
    
    # Forward fill time_avail_m within permno groups - equivalent to:
    # by permno: replace time_avail_m = time_avail_m[_n-1] if time_avail_m == .
    batch_df = batch_df.with_columns([
        pl.col("time_avail_m_batch").forward_fill().over("permno").alias("time_avail_m_filled")
    ])
    
    # Drop observations that couldn't be forward-filled - equivalent to: drop if time_avail_m == .
    batch_df = batch_df.filter(pl.col("time_avail_m_filled").is_not_null())
    
    # Drop unnecessary columns
    batch_df = batch_df.drop(["time_avail_m", "time_avail_m_int", "m60"])
    
    print(f"  Batch {m+1}: {batch_df.shape[0]} observations after time assignment")
    
    # Simple de-meaning following ACX - equivalent to:
    # gcollapse (mean) E_ret = ret, by(permno time_avail_m) merge
    means_df = batch_df.group_by(["permno", "time_avail_m_filled"]).agg([
        pl.col("ret").mean().alias("E_ret"),
        pl.col("mkt").mean().alias("E_mkt")
    ])
    
    # Merge means back and create demeaned returns - equivalent to merge operation and:
    # replace ret = ret - E_ret
    # replace mkt = mkt - E_mkt 
    batch_df = batch_df.join(means_df, on=["permno", "time_avail_m_filled"], how="inner")
    batch_df = batch_df.with_columns([
        (pl.col("ret") - pl.col("E_ret")).alias("ret_demeaned"),
        (pl.col("mkt") - pl.col("E_mkt")).alias("mkt_demeaned")
    ]).drop(["E_ret", "E_mkt"])
    
    # Calculate moment terms - equivalent to:
    # gen ret2 = ret^2
    # gen mkt2 = mkt^2  
    # gen ret_mkt2 = ret*mkt2
    batch_df = batch_df.with_columns([
        pl.col("ret_demeaned").pow(2).alias("ret2"),
        pl.col("mkt_demeaned").pow(2).alias("mkt2"),
        (pl.col("ret_demeaned") * pl.col("mkt_demeaned").pow(2)).alias("ret_mkt2")
    ])
    
    # Calculate coskewness with sample moments - equivalent to:
    # gcollapse (mean) E_ret_mkt2=ret_mkt2 E_ret2=ret2 E_mkt2=mkt2 (count) nobs=ret, by(permno time_avail_m)
    coskew_df = batch_df.group_by(["permno", "time_avail_m_filled"]).agg([
        pl.col("ret_mkt2").mean().alias("E_ret_mkt2"),
        pl.col("ret2").mean().alias("E_ret2"),
        pl.col("mkt2").mean().alias("E_mkt2"),
        pl.col("ret_demeaned").count().alias("nobs")  # Count observations for minimum requirement
    ])
    
    # Calculate Coskewness - equivalent to: gen Coskewness = E_ret_mkt2 / (sqrt(E_ret2) * E_mkt2) // eq B-9
    coskew_df = coskew_df.with_columns([
        (pl.col("E_ret_mkt2") / (pl.col("E_ret2").sqrt() * pl.col("E_mkt2"))).alias("Coskewness")
    ])
    
    # Filter minimum observations - equivalent to: keep if nobs >= 12
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

# Combine all 60 batches - equivalent to append using operations in Stata
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

# Save final result - equivalent to: do "$pathCode/savepredictor" Coskewness
final_result.write_csv(predictors_path / "Coskewness.csv")

print(f"✅ Coskewness.csv saved with {final_result.shape[0]} observations")
print("Coskewness translation complete!")