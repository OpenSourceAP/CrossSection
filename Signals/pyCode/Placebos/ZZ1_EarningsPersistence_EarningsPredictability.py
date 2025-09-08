# ABOUTME: EarningsPersistence and EarningsPredictability placebos
# ABOUTME: Python equivalent of ZZ1_EarningsPersistence_EarningsPredictability.do using rolling regressions

"""
Usage:
    python3 Placebos/ZZ1_EarningsPersistence_EarningsPredictability.py

Inputs:
    - a_aCompustat.parquet: gvkey, permno, time_avail_m, fyear, datadate, epspx, ajex columns

Outputs:
    - EarningsPersistence.csv: permno, yyyymm, EarningsPersistence columns
    - EarningsPredictability.csv: permno, yyyymm, EarningsPredictability columns
"""

import polars as pl
import pandas as pd
import sys
import os
from sklearn.linear_model import LinearRegression
import numpy as np

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from utils.save_standardized import save_placebo

print("Starting ZZ1_EarningsPersistence_EarningsPredictability.py...")

print("Step 1: Loading annual Compustat data...")
# Load annual Compustat data
compustat_annual = pl.read_parquet("../pyData/Intermediate/a_aCompustat.parquet")
df = compustat_annual.select(["gvkey", "permno", "time_avail_m", "fyear", "datadate", "epspx", "ajex"])

print(f"Loaded Compustat: {len(df):,} observations")

print("Step 2: Computing earnings variables...")
# Sort by gvkey and fyear for lag operations (following xtset gvkey fyear)
df = df.sort(["gvkey", "fyear"])

# Create temp = epspx/ajex (adjusted earnings per share)
df = df.with_columns([
    (pl.col("epspx") / pl.col("ajex")).alias("temp")
])

# Create 1-year lag: tempLag = l.temp
df = df.with_columns([
    pl.col("temp").shift(1).over("gvkey").alias("tempLag")
])

# Filter to observations with non-null temp and tempLag for regressions
df_reg = df.filter(
    pl.col("temp").is_not_null() &
    pl.col("tempLag").is_not_null()
)

print(f"Data for regressions: {len(df_reg):,} observations")

print("Step 3: Converting to pandas for rolling regressions...")
# Convert to pandas for rolling regression processing
df_pandas = df_reg.to_pandas()

print("Step 4: Running rolling regressions...")
# Function to perform rolling window regressions by gvkey
def rolling_regressions_by_gvkey(group):
    """Perform 10-year rolling window regressions for each gvkey"""
    group = group.sort_values('fyear').reset_index(drop=False)  # Keep original index
    results = []
    
    for i in range(len(group)):
        # Define 10-year window: current observation plus up to 9 previous years
        start_idx = max(0, i - 9)
        window_data = group.iloc[start_idx:i+1]
        
        if len(window_data) >= 10:  # Minimum 10 observations
            try:
                # Regression: temp ~ tempLag
                y = window_data['temp'].dropna()
                X = window_data[['tempLag']].dropna()
                
                common_idx = y.index.intersection(X.index)
                if len(common_idx) >= 10:
                    y_common = y.loc[common_idx]
                    X_common = X.loc[common_idx]
                    
                    reg = LinearRegression().fit(X_common.values, y_common.values)
                    
                    # EarningsPersistence = coefficient on tempLag
                    persistence = reg.coef_[0]
                    
                    # EarningsPredictability = RMSE^2
                    y_pred = reg.predict(X_common.values)
                    rmse = np.sqrt(np.mean((y_common.values - y_pred) ** 2))
                    predictability = rmse ** 2
                else:
                    persistence = None
                    predictability = None
                
                # Store results for this observation using original index
                results.append({
                    'index': group.iloc[i]['index'],  # Use original DataFrame index
                    'EarningsPersistence': persistence,
                    'EarningsPredictability': predictability
                })
                
            except Exception as e:
                # Skip problematic regressions
                results.append({
                    'index': group.iloc[i]['index'],  # Use original DataFrame index
                    'EarningsPersistence': None,
                    'EarningsPredictability': None
                })
    
    return results

# Process regressions by gvkey
print("Processing rolling regressions by gvkey...")
all_results = []
processed_gvkeys = 0
total_gvkeys = df_pandas['gvkey'].nunique()

for gvkey, group in df_pandas.groupby('gvkey'):
    processed_gvkeys += 1
    if processed_gvkeys % 100 == 0:
        print(f"  Processed {processed_gvkeys}/{total_gvkeys} gvkeys ({processed_gvkeys/total_gvkeys*100:.1f}%)")
    
    if len(group) >= 10:  # Only process gvkeys with sufficient data
        group_results = rolling_regressions_by_gvkey(group)
        all_results.extend(group_results)

print(f"Total regression results: {len(all_results)}")

print("Step 5: Merging results back to dataframe...")
# Convert results to DataFrame and merge back
if all_results:
    results_df = pd.DataFrame(all_results).set_index('index')
    
    # Merge back to original dataframe
    df_pandas.loc[results_df.index, 'EarningsPersistence'] = results_df['EarningsPersistence']
    df_pandas.loc[results_df.index, 'EarningsPredictability'] = results_df['EarningsPredictability']

    # Convert back to polars
    df_with_results = pl.from_pandas(df_pandas[['gvkey', 'permno', 'datadate', 'fyear', 
                                               'EarningsPersistence', 'EarningsPredictability']])
else:
    print("No regression results generated")
    df_with_results = pl.from_pandas(df_pandas[['gvkey', 'permno', 'datadate', 'fyear']]).with_columns([
        pl.lit(None).alias('EarningsPersistence'),
        pl.lit(None).alias('EarningsPredictability')
    ])

print("Step 6: Expanding to monthly frequency...")
# Expand to monthly (following DataDownloads/B_CompustatAnnual.py pattern)
df_with_results = df_with_results.with_columns([
    # time_avail_m = mofd(datadate) + 6 (6 months after fiscal year end)
    (pl.col("datadate").dt.truncate("1mo").dt.offset_by("6mo")).alias("time_avail_m")
])

# Create 12 copies for each annual observation (expand temp = 12)
expanded_list = []
for i in range(12):
    temp_df = df_with_results.with_columns([
        (pl.col("time_avail_m").dt.offset_by(f"{i}mo")).alias("time_avail_m")
    ])
    expanded_list.append(temp_df)

df_monthly = pl.concat(expanded_list)

# Sort and keep last observation by gvkey-time_avail_m and permno-time_avail_m
df_monthly = df_monthly.sort(["gvkey", "time_avail_m", "datadate"])
df_monthly = df_monthly.unique(subset=["gvkey", "time_avail_m"], keep="last")

df_monthly = df_monthly.sort(["permno", "time_avail_m", "datadate"])
df_monthly = df_monthly.unique(subset=["permno", "time_avail_m"], keep="last")

print(f"After monthly expansion: {len(df_monthly):,} observations")

print("Step 7: Saving results...")
# Separate and save each placebo
earnings_persistence = df_monthly.select(["permno", "time_avail_m", "EarningsPersistence"]).filter(
    pl.col("EarningsPersistence").is_not_null()
)
earnings_predictability = df_monthly.select(["permno", "time_avail_m", "EarningsPredictability"]).filter(
    pl.col("EarningsPredictability").is_not_null()
)

# Save both placebos
save_placebo(earnings_persistence, "EarningsPersistence")
save_placebo(earnings_predictability, "EarningsPredictability")

print(f"Generated {len(earnings_persistence)} EarningsPersistence observations")
print(f"Generated {len(earnings_predictability)} EarningsPredictability observations")

print("ZZ1_EarningsPersistence_EarningsPredictability.py completed successfully")