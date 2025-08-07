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

# Load daily CRSP data - equivalent to: use permno time_d ret using "$pathDataIntermediate/dailyCRSP.dta"
daily_crsp = pl.read_parquet(intermediate_path / "dailyCRSP.parquet")
print(f"Loaded dailyCRSP: {daily_crsp.shape} rows")

# Keep only data from 1962-07-02 onwards - equivalent to: keep if time_d >= date("19620702","YMD")
daily_crsp = daily_crsp.filter(
    pl.col("time_d") >= pl.date(1962, 7, 2)
)
print(f"After 1962-07-02 filter: {daily_crsp.shape} rows")

print("Loading daily Fama-French data...")

# Load daily FF data - equivalent to: merge m:1 time_d using "$pathDataIntermediate/dailyFF"
daily_ff = pl.read_parquet(intermediate_path / "dailyFF.parquet")
print(f"Loaded dailyFF: {daily_ff.shape} rows")

print("Merging CRSP and FF data...")

# Merge with FF data - equivalent to: merge m:1 time_d using ... nogenerate keep(match) keepusing(mktrf rf)
merged_data = daily_crsp.join(
    daily_ff.select(["time_d", "mktrf", "rf"]),
    on="time_d",
    how="inner"
).filter(
    pl.col("mktrf").is_not_null() & pl.col("rf").is_not_null()
)

print(f"After merging with FF: {merged_data.shape} rows")

# Create market return - equivalent to: gen mkt = mktrf + rf
merged_data = merged_data.with_columns([
    (pl.col("mktrf") + pl.col("rf")).alias("mkt")
])

print("Converting to continuous-time compounded returns...")

# Convert to continuous-time compounded excess returns - equivalent to:
# replace mkt = log(1+mkt) - log(1+rf) 
# replace ret = log(1+ret) - log(1+rf)
merged_data = merged_data.with_columns([
    (pl.col("mkt").add(1).log() - pl.col("rf").add(1).log()).alias("mkt"),
    (pl.col("ret").add(1).log() - pl.col("rf").add(1).log()).alias("ret")
]).drop("rf")

print(f"Data ready for processing: {merged_data.shape} rows")

# Set up for 12-month periods - equivalent to Stata's reverse time sorting
# Sort by permno and reverse time (temptime = -time_d, then sort permno temptime)
merged_data = merged_data.sort(["permno", "time_d"], descending=[False, True])

print("Starting 12-month batch processing loop...")

# Initialize list to store results from each batch
batch_results = []

# Process 12 batches (m=1 to 12 for Jan to Dec) - equivalent to: forvalues m=1/12
for m in range(1, 13):
    print(f"Processing batch {m}/12...")
    
    # Start with the merged data for this batch
    batch_df = merged_data.clone()
    
    # Create time_avail_m for month m - equivalent to:
    # gen time_avail_m = mofd(time_d) if month(time_d) == `m'
    batch_df = batch_df.with_columns([
        pl.when(pl.col("time_d").dt.month() == m)
        .then((pl.col("time_d").dt.year() - 1960) * 12 + (pl.col("time_d").dt.month() - 1))
        .otherwise(None)
        .alias("time_avail_m")
    ])
    
    # Forward fill time_avail_m within permno groups - equivalent to:
    # by permno: replace time_avail_m = time_avail_m[_n-1] if time_avail_m == .
    batch_df = batch_df.with_columns([
        pl.col("time_avail_m").forward_fill().over("permno").alias("time_avail_m_filled")
    ])
    
    # Drop observations that couldn't be forward-filled - equivalent to: drop if time_avail_m == .
    batch_df = batch_df.filter(pl.col("time_avail_m_filled").is_not_null())
    
    # Drop time_d as it's no longer needed - equivalent to: drop time_d
    batch_df = batch_df.drop("time_d")
    
    print(f"  Batch {m}: {batch_df.shape[0]} observations after time assignment")
    
    # Demean returns within each 12-month period - equivalent to:
    # gcollapse (mean) E_ret = ret E_mkt = mkt, by(permno time_avail_m) merge
    means_df = batch_df.group_by(["permno", "time_avail_m_filled"]).agg([
        pl.col("ret").mean().alias("E_ret"),
        pl.col("mkt").mean().alias("E_mkt")
    ])
    
    # Merge means back and create demeaned returns - equivalent to merge operation and:
    # replace ret = ret - E_ret // called \tilde{r}_{it} in ACX appendix
    # replace mkt = mkt - E_mkt // called \tilde{r}_{mt} in ACX appendix
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
        pl.col("ret_demeaned").count().alias("nobs")
    ])
    
    # Calculate CoskewACX - equivalent to: gen CoskewACX = E_ret_mkt2 / (sqrt(E_ret2) * E_mkt2)
    coskew_df = coskew_df.with_columns([
        (pl.col("E_ret_mkt2") / (pl.col("E_ret2").sqrt() * pl.col("E_mkt2"))).alias("CoskewACX")
    ])
    
    # Filter observations with too many missing values - equivalent to:
    # gcollapse (max) max_nobs = nobs, by (time_avail_m) merge
    # drop if max_nobs - nobs > 5
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

# Combine all 12 batches - equivalent to append using operations in Stata
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

# Save final result - equivalent to: do "$pathCode/savepredictor" CoskewACX
final_result.write_csv(predictors_path / "CoskewACX.csv")

print(f"✅ CoskewACX.csv saved with {final_result.shape[0]} observations")
print("CoskewACX translation complete!")