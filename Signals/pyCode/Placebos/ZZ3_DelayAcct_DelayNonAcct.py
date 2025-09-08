# ABOUTME: DelayAcct and DelayNonAcct placebos - accounting vs non-accounting components of price delay
# ABOUTME: Python equivalent of ZZ3_DelayAcct_DelayNonAcct.do using cross-sectional regressions

"""
Usage:
    python3 Placebos/ZZ3_DelayAcct_DelayNonAcct.py

Inputs:
    - PriceDelayRsq.csv: permno, yyyymm, PriceDelayRsq columns (FROM PREDICTORS)
    - SignalMasterTable.parquet: permno, time_avail_m, tickerIBES columns
    - monthlyCRSP.parquet: permno, time_avail_m, shrout columns  
    - m_aCompustat.parquet: permno, time_avail_m, at, spi, ib columns
    - IBES_UnadjustedActuals.parquet: tickerIBES, fy0a, fy0edats columns
    - IBES_EPS_Unadj.parquet: tickerIBES, time_avail_m, meanest, fpedats, statpers columns
    - AccrualQuality.csv: permno, yyyymm, accrualquality columns (FROM PLACEBOS)

Outputs:
    - DelayAcct.csv: permno, yyyymm, DelayAcct columns
    - DelayNonAcct.csv: permno, yyyymm, DelayNonAcct columns
"""

import polars as pl
import sys
import os
from pathlib import Path

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from utils.save_standardized import save_placebo

print("Starting ZZ3_DelayAcct_DelayNonAcct.py...")

# Check dependencies
accrual_quality_file = "../pyData/Placebos/AccrualQuality.csv"
price_delay_file = "../pyData/Predictors/PriceDelayRsq.csv"

if not Path(accrual_quality_file).exists():
    print(f"ERROR: Required dependency {accrual_quality_file} not found!")
    print("Please run ZZ2_AccrualQuality_AccrualQualityJune.py first.")
    exit(1)
    
if not Path(price_delay_file).exists():
    print(f"ERROR: Required dependency {price_delay_file} not found!")
    print("Please run Predictors/ZZ2_PriceDelaySlope_PriceDelayRsq_PriceDelayTstat.py first.")
    exit(1)

print("Step 1: Loading PriceDelay from existing predictor...")
# Load PriceDelay from existing predictor output (following Stata logic)
price_delay_df = pl.read_csv(price_delay_file).with_columns([
    pl.datetime(
        (pl.col("yyyymm") // 100),
        (pl.col("yyyymm") % 100), 
        1
    ).cast(pl.Datetime("us")).alias("time_avail_m")
]).select(["permno", "time_avail_m", "PriceDelayRsq"]).rename({"PriceDelayRsq": "PriceDelay"})

print(f"Loaded {len(price_delay_df)} PriceDelay observations")

print("Step 2: Preparing IBES data...")
# Prep IBES data (following Stata logic)
# Load IBES actuals and keep unique ticker-date combinations
ibes_actuals = pl.read_parquet("../pyData/Intermediate/IBES_UnadjustedActuals.parquet")
ibes_actuals_unique = ibes_actuals.select(["tickerIBES", "fy0a", "fy0edats"]).unique(subset=["tickerIBES", "fy0edats"])

# Load IBES EPS data and filter
ibes_eps = pl.read_parquet("../pyData/Intermediate/IBES_EPS_Unadj.parquet")
ibes_eps_filtered = ibes_eps.filter(
    pl.col("fpi") == "1"
).filter(
    pl.col("fpedats").is_not_null() & 
    (pl.col("fpedats") > pl.col("statpers") + pl.duration(days=30))
).select(["tickerIBES", "time_avail_m", "meanest", "fpedats"]).rename({"fpedats": "fy0edats"})

# Merge IBES data
ibes_combined = ibes_eps_filtered.join(
    ibes_actuals_unique,
    on=["tickerIBES", "fy0edats"],
    how="left"
).select(["tickerIBES", "time_avail_m", "meanest", "fy0a"])

print(f"IBES combined data: {len(ibes_combined)} observations")

print("Step 3: Loading other required data...")
# Load required datasets
signal_master = pl.read_parquet("../pyData/Intermediate/SignalMasterTable.parquet")
monthly_crsp = pl.read_parquet("../pyData/Intermediate/monthlyCRSP.parquet") 
m_acompustat = pl.read_parquet("../pyData/Intermediate/m_aCompustat.parquet")

# Load AccrualQuality
accrual_quality = pl.read_csv(accrual_quality_file).with_columns([
    pl.datetime(
        (pl.col("yyyymm") // 100),
        (pl.col("yyyymm") % 100), 
        1
    ).cast(pl.Datetime("us")).alias("time_avail_m")
])

print("Step 4: Building master dataset...")
# Build master dataset following Stata logic
df = signal_master.select(["permno", "tickerIBES", "time_avail_m"])

# Merge with monthly CRSP
df = df.join(
    monthly_crsp.select(["permno", "time_avail_m", "shrout"]),
    on=["permno", "time_avail_m"],
    how="left"
)

# Merge with Compustat  
df = df.join(
    m_acompustat.select(["permno", "time_avail_m", "at", "spi", "ib"]),
    on=["permno", "time_avail_m"], 
    how="left"
)

# Merge with IBES
df = df.join(
    ibes_combined,
    on=["tickerIBES", "time_avail_m"],
    how="left"
)

# Ensure consistent datetime types before join
df = df.with_columns([
    pl.col("time_avail_m").cast(pl.Datetime("us"))
])

# Merge PriceDelay
df = df.join(
    price_delay_df,
    on=["permno", "time_avail_m"],
    how="left"
)

# Merge AccrualQuality
df = df.join(
    accrual_quality.select(["permno", "time_avail_m", "AccrualQuality"]),
    on=["permno", "time_avail_m"],
    how="left"
)

print(f"Master dataset: {len(df)} observations")

print("Step 5: Computing variables...")
# Sort for lag operations (xtset permno time_avail_m)
df = df.sort(["permno", "time_avail_m"])

# tempSI = spi/(.5*(at + l12.at))
df = df.with_columns([
    pl.col("at").shift(12).over("permno").alias("at_l12")
]).with_columns([
    (pl.col("spi") / (0.5 * (pl.col("at") + pl.col("at_l12")))).alias("tempSI")
])

# Compute earnings surprise following Stata logic
# tempSurprise = meanest - fy0a
df = df.with_columns([
    (pl.col("meanest") - pl.col("fy0a")).alias("tempSurprise")
])

# Create lagged tempSurprise for 12, 24, 36, 48 months
for n in [12, 24, 36, 48]:
    df = df.with_columns([
        pl.col("tempSurprise").shift(n).over("permno").alias(f"tempSurprise{n}")
    ])

# Compute rolling standard deviation (rowsd) and count non-missing (rowmiss)
surf_cols = ["tempSurprise", "tempSurprise12", "tempSurprise24", "tempSurprise36", "tempSurprise48"]
df = df.with_columns([
    pl.concat_list([pl.col(col) for col in surf_cols]).list.eval(pl.element().std()).list.get(0).alias("tempSD"),
    pl.concat_list([pl.col(col) for col in surf_cols]).list.eval(pl.element().is_null().sum()).list.get(0).alias("tempN")
])

# Set tempSD to null if more than 2 missing values
df = df.with_columns([
    pl.when(pl.col("tempN") > 2).then(None).otherwise(pl.col("tempSD")).alias("tempSD")
])

# Compute tempES = abs(tempSurprise) / tempSD
df = df.with_columns([
    (pl.col("tempSurprise").abs() / pl.col("tempSD")).alias("tempES")
])

print("Step 6: Cross-sectional regressions by time period...")
# STRICT STATA REPLICATION: Require ALL variables to be non-null (no flexibility)
# This matches Stata's 'cap reg PriceDelay AccrualQuality tempSI tempES' exactly
df_reg = df.filter(
    pl.col("PriceDelay").is_not_null() & 
    pl.col("AccrualQuality").is_not_null() & 
    pl.col("tempSI").is_not_null() & 
    pl.col("tempES").is_not_null()
)

print(f"Observations for regression: {len(df_reg)}")

# Run cross-sectional regressions by time_avail_m (following Stata levelsof approach)
print("Running cross-sectional regressions...")

unique_dates = df_reg["time_avail_m"].unique().sort()
print(f"Running regressions for {len(unique_dates)} time periods...")

# Process all dates and collect results - STRICT STATA REPLICATION ONLY
all_results = []

for i, date in enumerate(unique_dates):
    if i % 100 == 0:
        print(f"  Processing date {i+1}/{len(unique_dates)}: {date}")
    
    date_data = df_reg.filter(pl.col("time_avail_m") == date)
    
    if len(date_data) >= 10:  # Minimum observations for regression
        try:
            # Convert to pandas for regression
            date_pandas = date_data.to_pandas()
            
            # Clean data for regression (remove infinities) but keep original filtering logic
            import numpy as np
            for col in ['PriceDelay', 'AccrualQuality', 'tempSI', 'tempES']:
                date_pandas = date_pandas[np.isfinite(date_pandas[col])]
            
            if len(date_pandas) >= 10:
                import statsmodels.api as sm
                
                # STRICT STATA APPROACH: Full model only with all 3 predictors
                # Matches: cap reg PriceDelay AccrualQuality tempSI tempES if time_avail_m == `t'
                X = date_pandas[['AccrualQuality', 'tempSI', 'tempES']]
                X = sm.add_constant(X)  # Add constant term like Stata
                y = date_pandas['PriceDelay']
                
                try:
                    # Fit regression (Stata 'reg' equivalent)
                    reg = sm.OLS(y, X).fit()
                    fitted_values = reg.predict(X)
                    
                    # Create results (Stata 'predict' equivalent)  
                    pred_results = date_pandas[['permno', 'time_avail_m', 'PriceDelay']].copy()
                    pred_results['DelayAcct'] = fitted_values
                    pred_results['DelayNonAcct'] = pred_results['PriceDelay'] - pred_results['DelayAcct']
                    
                    # Convert back to polars and add to results
                    reg_result = pl.from_pandas(pred_results[['permno', 'time_avail_m', 'DelayAcct', 'DelayNonAcct']])
                    all_results.append(reg_result)
                    
                except Exception as reg_error:
                    # Handle singular matrix like Stata 'cap reg' (silently skip)
                    pass
                    
        except Exception as e:
            print(f"  Warning: Data processing failed for date {date}: {e}")
            continue

print(f"Successfully processed {len(all_results)} time periods")

if all_results:
    final_results = pl.concat(all_results)
    print(f"Final results: {len(final_results)} observations")
    
    # Separate DelayAcct and DelayNonAcct (both should already exist in final_results)
    delay_acct = final_results.select(["permno", "time_avail_m", "DelayAcct"])
    delay_non_acct = final_results.select(["permno", "time_avail_m", "DelayNonAcct"])
    
    # Save
    save_placebo(delay_acct, "DelayAcct")
    save_placebo(delay_non_acct, "DelayNonAcct")
    
    print(f"Generated {len(delay_acct)} DelayAcct observations")
    print(f"Generated {len(delay_non_acct)} DelayNonAcct observations")
else:
    print("ERROR: No regression results generated")
    exit(1)

print("ZZ3_DelayAcct_DelayNonAcct.py completed successfully")