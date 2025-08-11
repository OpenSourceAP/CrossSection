# ABOUTME: Coskewness.py - generates coskewness predictor using 60-batch processing strategy  
# ABOUTME: Direct line-by-line translation of Coskewness.do with correct forward-fill logic

"""
Coskewness.py

Direct translation of Coskewness.do using 60-batch forward-fill processing:
- Creates 60 different time alignment patterns using mod(time_avail_m, 60)
- Forward-fill creates overlapping time series within permno groups  
- Simple demeaning approach (not CAPM residuals) following ACX methodology
- Coskewness: E[ret * mkt^2] / (sqrt(E[ret^2]) * E[mkt^2])

Usage:
    cd pyCode/
    source .venv/bin/activate  
    python3 Predictors/Coskewness.py

Inputs:
    - ../pyData/Intermediate/monthlyCRSP.parquet (permno, time_avail_m, ret)
    - ../pyData/Intermediate/monthlyFF.parquet (time_avail_m, mktrf, rf)

Outputs:
    - ../pyData/Predictors/Coskewness.csv

Algorithm:
    For m=0 to 59:
      1. Set time_avail_m = null where m60 != m  
      2. Forward-fill time_avail_m within permno groups
      3. Drop observations where time_avail_m still null
      4. Simple demean ret and mkt by (permno, time_avail_m)  
      5. Calculate coskewness moments, require >= 12 obs
"""

import polars as pl
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from utils.savepredictor import save_predictor

print("=" * 80)
print("🏗️  Coskewness.py")
print("Direct translation of Coskewness.do with corrected forward-fill logic")
print("=" * 80)

# DATA LOAD - following Stata exactly
print("📊 Loading data...")
print("Loading monthlyCRSP.parquet...")
crsp = pl.read_parquet("../pyData/Intermediate/monthlyCRSP.parquet").select(["permno", "time_avail_m", "ret"])
print(f"Loaded CRSP: {len(crsp):,} observations")

print("Loading monthlyFF.parquet...")  
ff = pl.read_parquet("../pyData/Intermediate/monthlyFF.parquet").select(["time_avail_m", "mktrf", "rf"])
print(f"Loaded FF: {len(ff):,} observations")

# MERGE - replicating Stata merge m:1 time_avail_m using monthlyFF
df = crsp.join(ff, on="time_avail_m", how="inner")
print(f"After merge: {len(df):,} observations")

# Convert to excess returns in place (following Stata logic exactly)
df = df.with_columns([
    pl.col("mktrf").alias("mkt"),  # replace mkt = mktrf
    (pl.col("ret") - pl.col("rf")).alias("ret")  # replace ret = ret - rf  
]).drop("rf")

# Set up for looping over 60-month window sets (following Stata setup)
df = df.sort(["permno", "time_avail_m"])

# Convert time_avail_m to integer format matching Stata's mofd() function
# Stata time starts from Jan 1960 = 0
df = df.with_columns([
    ((pl.col("time_avail_m").dt.year() - 1960) * 12 + (pl.col("time_avail_m").dt.month() - 1)).alias("time_avail_m_int")
]).with_columns([
    (pl.col("time_avail_m_int") % 60).alias("m60")  # gen m60 = mod(time_avail_m, 60)
])

print(f"Generated m60 variable with values 0-59")

# Clear any previous temp results  
all_batches = []

# Main loop: forvalues m=0/59 
print("🔄 Processing 60 batches with forward-fill logic...")
for m in range(60):
    print(f"Processing batch {m}")
    
    # Start with full dataset for each batch (use "$pathtemp/tempmerge")
    batch_df = df.select(["permno", "time_avail_m", "time_avail_m_int", "m60", "ret", "mkt"])
    
    # Stata step 1: replace time_avail_m = . if m60 != `m'
    batch_df = batch_df.with_columns([
        pl.when(pl.col("m60") != m)
        .then(None)
        .otherwise(pl.col("time_avail_m_int")) 
        .alias("time_avail_m_batch")
    ])
    
    # Stata step 2: by permno: replace time_avail_m = time_avail_m[_n-1] if time_avail_m == .
    batch_df = batch_df.with_columns([
        pl.col("time_avail_m_batch")
        .forward_fill()
        .over("permno")
        .alias("time_avail_m_filled")
    ])
    
    # Stata step 3: drop if time_avail_m == .
    batch_df = batch_df.filter(pl.col("time_avail_m_filled").is_not_null())
    
    if len(batch_df) == 0:
        print(f"  Batch {m}: No observations after forward-fill, skipping")
        continue
        
    print(f"  Batch {m}: {len(batch_df):,} observations after forward-fill")
    
    # Simple de-meaning following ACX (gcollapse (mean) E_ret = ret, by(permno time_avail_m) merge)
    batch_df = batch_df.with_columns([
        pl.col("ret").mean().over(["permno", "time_avail_m_filled"]).alias("E_ret"),
        pl.col("mkt").mean().over(["permno", "time_avail_m_filled"]).alias("E_mkt")
    ]).with_columns([
        (pl.col("ret") - pl.col("E_ret")).alias("ret_demeaned"),  # replace ret = ret - E_ret
        (pl.col("mkt") - pl.col("E_mkt")).alias("mkt_demeaned")   # replace mkt = mkt - E_mkt  
    ])
    
    # Calculate coskewness with sample moments (following Stata exactly)
    batch_df = batch_df.with_columns([
        (pl.col("ret_demeaned") ** 2).alias("ret2"),                    # gen ret2 = ret^2
        (pl.col("mkt_demeaned") ** 2).alias("mkt2"),                    # gen mkt2 = mkt^2  
        (pl.col("ret_demeaned") * pl.col("mkt_demeaned") ** 2).alias("ret_mkt2")  # gen ret_mkt2 = ret*mkt2
    ])
    
    # CRITICAL FIX: Filter out null returns before moment calculations (like Stata does)
    # gcollapse (mean) E_ret_mkt2=ret_mkt2 E_ret2=ret2 E_mkt2=mkt2 (count) nobs=ret, by(permno time_avail_m)
    batch_result = batch_df.filter(
        pl.col("ret").is_not_null()  # Only include observations with non-null returns
    ).group_by(["permno", "time_avail_m_filled"]).agg([
        pl.col("ret_mkt2").mean().alias("E_ret_mkt2"),
        pl.col("ret2").mean().alias("E_ret2"),
        pl.col("mkt2").mean().alias("E_mkt2"), 
        pl.len().alias("nobs")  # Count only non-null observations
    ]).with_columns([
        # gen Coskewness = E_ret_mkt2 / (sqrt(E_ret2) * E_mkt2)  // eq B-9
        (pl.col("E_ret_mkt2") / (pl.col("E_ret2").sqrt() * pl.col("E_mkt2"))).alias("Coskewness")
    ]).filter(
        pl.col("nobs") >= 12  # keep if nobs >= 12
    ).select([
        "permno", 
        pl.col("time_avail_m_filled").alias("time_avail_m"),  # Use filled time for grouping
        "Coskewness"
    ])
    
    print(f"  Batch {m}: Generated {len(batch_result):,} coskewness observations")
    
    if len(batch_result) > 0:
        all_batches.append(batch_result)

# Append all batches (following Stata: foreach file in `files' { append using `file' })
print("🔗 Appending all batches...")
if len(all_batches) == 0:
    print("❌ No results from any batch!")
    df_final = pl.DataFrame({
        "permno": [], "time_avail_m": [], "Coskewness": []
    }, schema={"permno": pl.Int32, "time_avail_m": pl.Int32, "Coskewness": pl.Float64})
else:
    df_final = pl.concat(all_batches)
    
    # Convert time_avail_m back to datetime for save_predictor
    df_final = df_final.with_columns([
        # Convert back to datetime: add months to Jan 1960
        pl.date(1960, 1, 1).dt.offset_by(pl.col("time_avail_m").cast(pl.String) + "mo").alias("time_avail_m")
    ])
    
    # Sort and clean (following Stata: sort permno time_avail_m)
    df_final = df_final.sort(["permno", "time_avail_m"]).filter(
        pl.col("Coskewness").is_not_null() & pl.col("Coskewness").is_finite()
    )

print(f"Final Coskewness observations: {len(df_final):,}")

if len(df_final) > 0:
    print("Summary statistics:")
    print(f"  Mean: {df_final['Coskewness'].mean():.6f}")
    print(f"  Std:  {df_final['Coskewness'].std():.6f}")
    print(f"  Min:  {df_final['Coskewness'].min():.6f}")  
    print(f"  Max:  {df_final['Coskewness'].max():.6f}")

# SAVE (do "$pathCode/savepredictor" Coskewness)
print("💾 Saving predictor...")
save_predictor(df_final, "Coskewness")
print("✅ Coskewness.csv saved successfully")