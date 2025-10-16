# ABOUTME: EarningsValueRelevance, EarningsTimeliness, and EarningsConservatism placebos
# ABOUTME: Python equivalent of ZZ1_EarningsValueRelevance_EarningsTimeliness_EarningsConservatism.do using rolling regressions

"""
Usage:
    python3 Placebos/ZZ1_EarningsValueRelevance_EarningsTimeliness_EarningsConservatism.py

Inputs:
    - monthlyCRSP.parquet: permno, time_avail_m, ret, prc, shrout columns
    - a_aCompustat.parquet: gvkey, permno, datadate, fyear, ib columns

Outputs:
    - EarningsValueRelevance.csv: permno, yyyymm, EarningsValueRelevance columns
    - EarningsTimeliness.csv: permno, yyyymm, EarningsTimeliness columns
    - EarningsConservatism.csv: permno, yyyymm, EarningsConservatism columns
"""

import polars as pl
import pandas as pd
import sys
import os
import numpy as np

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from utils.save_standardized import save_placebo

print("Starting ZZ1_EarningsValueRelevance_EarningsTimeliness_EarningsConservatism.py...")

print("Step 1: Loading and preparing monthly CRSP data...")
# Load monthly CRSP data
monthly_crsp = pl.read_parquet("../pyData/Intermediate/monthlyCRSP.parquet")
crsp = monthly_crsp.select(["permno", "time_avail_m", "ret", "prc", "shrout"]).rename({"time_avail_m": "time_m"})

# Replace missing returns with 0 (following Stata logic)
crsp = crsp.with_columns([
    pl.col("ret").fill_null(0)
])

print(f"Loaded CRSP: {len(crsp):,} observations")

# Sort for lag operations
crsp = crsp.sort(["permno", "time_m"])

print("Step 2: Computing 15-month momentum...")
# Compute 15-month return: (1+f2.ret)*(1+f.ret)*(1+ret)*(1+l.ret)*...*(1+l11.ret) - 1

# Create lead and lag variables
crsp = crsp.with_columns([
    pl.col("ret").shift(-2).over("permno").alias("f2_ret"),  # 2 months future
    pl.col("ret").shift(-1).over("permno").alias("f_ret"),   # 1 month future
    pl.col("ret").shift(1).over("permno").alias("l_ret"),    # 1 month lag
    pl.col("ret").shift(2).over("permno").alias("l2_ret"),   # 2 months lag
    pl.col("ret").shift(3).over("permno").alias("l3_ret"),   # 3 months lag
    pl.col("ret").shift(4).over("permno").alias("l4_ret"),   # 4 months lag
    pl.col("ret").shift(5).over("permno").alias("l5_ret"),   # 5 months lag
    pl.col("ret").shift(6).over("permno").alias("l6_ret"),   # 6 months lag
    pl.col("ret").shift(7).over("permno").alias("l7_ret"),   # 7 months lag
    pl.col("ret").shift(8).over("permno").alias("l8_ret"),   # 8 months lag
    pl.col("ret").shift(9).over("permno").alias("l9_ret"),   # 9 months lag
    pl.col("ret").shift(10).over("permno").alias("l10_ret"), # 10 months lag
    pl.col("ret").shift(11).over("permno").alias("l11_ret")  # 11 months lag
])

# Calculate 15-month momentum
crsp = crsp.with_columns([
    ((1 + pl.col("f2_ret")) * (1 + pl.col("f_ret")) * (1 + pl.col("ret")) * 
     (1 + pl.col("l_ret")) * (1 + pl.col("l2_ret")) * (1 + pl.col("l3_ret")) * 
     (1 + pl.col("l4_ret")) * (1 + pl.col("l5_ret")) * (1 + pl.col("l6_ret")) * 
     (1 + pl.col("l7_ret")) * (1 + pl.col("l8_ret")) * (1 + pl.col("l9_ret")) * 
     (1 + pl.col("l10_ret")) * (1 + pl.col("l11_ret")) - 1).alias("tempMom15m"),
    
    # Calculate market cap
    (pl.col("prc").abs() * pl.col("shrout")).alias("tempmktcap")
])

# Keep only required columns for merge
crsp_temp = crsp.select(["permno", "time_m", "tempMom15m", "tempmktcap"])

print("Step 3: Loading Compustat annual data...")
# Load annual Compustat data
compustat_annual = pl.read_parquet("../pyData/Intermediate/a_aCompustat.parquet")
compustat = compustat_annual.select(["gvkey", "permno", "datadate", "fyear", "ib"])

# Create monthly time variable to match with CRSP
compustat = compustat.with_columns([
    pl.col("datadate").dt.truncate("1mo").alias("time_m")
])

print(f"Loaded Compustat: {len(compustat):,} observations")

print("Step 4: Merging data...")
# Merge with CRSP data (following master match logic)
df = compustat.join(crsp_temp, on=["permno", "time_m"], how="left")

print(f"After merge: {len(df):,} observations")

print("Step 5: Computing earnings variables...")
# Sort by gvkey and fyear for lag operations (following xtset gvkey fyear)
df = df.sort(["gvkey", "fyear"])

# Compute earnings variables
df = df.with_columns([
    # tempEarn = ib / tempmktcap
    (pl.col("ib") / pl.col("tempmktcap")).alias("tempEarn"),
    # tempDEarn = (ib - l.ib) / tempmktcap (change in earnings)
    ((pl.col("ib") - pl.col("ib").shift(1).over("gvkey")) / pl.col("tempmktcap")).alias("tempDEarn")
])

# Track observations that have complete data for regression eligibility (for reporting)
df_valid = df.filter(
    pl.col("tempEarn").is_not_null() &
    pl.col("tempDEarn").is_not_null() &
    pl.col("tempMom15m").is_not_null()
)

print(f"Data for regressions: {len(df_valid):,} observations")

# Create additional variables for second regression
df = df.with_columns([
    pl.when(pl.col("tempMom15m").is_null())
    .then(None)
    .otherwise((pl.col("tempMom15m") < 0).cast(pl.Float64))
    .alias("tempNeg")
])

df = df.with_columns([
    (pl.col("tempNeg") * pl.col("tempMom15m")).alias("tempInter")
])

print("Step 6: Converting to pandas for rolling regressions...")
# Convert to pandas for rolling regression processing
df_pandas = df.to_pandas()

print("Step 7: Running rolling regressions...")
# Helper to fit OLS while dropping collinear regressors (mirrors Stata's behavior)
def fit_ols_with_collinearity(X, y, min_obs=10, tol=1e-6):
    """Fit OLS with sequential column selection to drop collinear regressors."""
    if len(y) < min_obs:
        return None, None, None
    selected_columns = []
    selected_data = []
    for idx in range(X.shape[1]):
        candidate = X[:, [idx]]
        tentative = candidate if not selected_data else np.hstack(selected_data + [candidate])
        singular_values = np.linalg.svd(tentative, compute_uv=False)
        if singular_values.size == 0:
            continue
        max_sv = singular_values[0]
        effective_rank = np.sum(singular_values > tol * max_sv) if max_sv > 0 else 0
        if effective_rank > len(selected_data):
            selected_data.append(candidate)
            selected_columns.append(idx)
    if not selected_data:
        return None, selected_columns, None
    X_selected = np.hstack(selected_data)
    beta = np.linalg.lstsq(X_selected, y, rcond=None)[0]
    full_beta = np.zeros(X.shape[1])
    for coeff, col_idx in zip(beta, selected_columns):
        full_beta[col_idx] = coeff
    y_hat = X_selected @ beta
    ss_tot = ((y - y.mean()) ** 2).sum()
    ss_res = ((y - y_hat) ** 2).sum()
    r_squared = 1 - ss_res / ss_tot if ss_tot != 0 else None
    return full_beta, selected_columns, r_squared

# Function to perform rolling window regressions by gvkey
def rolling_regressions_by_gvkey(group):
    """Perform 10-year rolling window regressions for each gvkey"""
    group = group.sort_values('fyear').reset_index(drop=False)  # Keep original index
    results = []
    
    for i in range(len(group)):
        # Define 10-year window: current observation plus up to 9 previous years
        start_idx = max(0, i - 9)
        window_data = group.iloc[start_idx:i+1]
        
        if len(window_data) >= 10:  # Minimum 10 observations to match Stata asreg min(10)
            try:
                # Prepare data for regressions
                reg1_data = window_data[['tempMom15m', 'tempEarn', 'tempDEarn']].dropna()
                if len(reg1_data) >= 10:
                    X1 = np.column_stack([
                        np.ones(len(reg1_data)),
                        reg1_data['tempEarn'].to_numpy(),
                        reg1_data['tempDEarn'].to_numpy()
                    ])
                    y1 = reg1_data['tempMom15m'].to_numpy()
                    beta1, cols1, r2_vr = fit_ols_with_collinearity(X1, y1)
                else:
                    beta1, cols1, r2_vr = (None, None, None)
                
                reg2_data = window_data[['tempEarn', 'tempNeg', 'tempMom15m', 'tempInter']].dropna()
                if len(reg2_data) >= 10:
                    X2 = np.column_stack([
                        np.ones(len(reg2_data)),
                        reg2_data['tempNeg'].to_numpy(),
                        reg2_data['tempMom15m'].to_numpy(),
                        reg2_data['tempInter'].to_numpy()
                    ])
                    y2 = reg2_data['tempEarn'].to_numpy()
                    beta2, cols2, r2_tl = fit_ols_with_collinearity(X2, y2)
                    if beta2 is None:
                        b_tempMom15m = None
                        b_tempInter = None
                        conservatism = None
                    else:
                        b_tempMom15m = beta2[2]
                        b_tempInter = beta2[3]
                        if np.isnan(b_tempMom15m) or abs(b_tempMom15m) < 1e-12:
                            conservatism = None
                        else:
                            conservatism = (b_tempMom15m + b_tempInter) / b_tempMom15m
                else:
                    r2_tl = None
                    b_tempMom15m = None
                    b_tempInter = None
                    conservatism = None
                
                if beta1 is None:
                    r2_vr = None
                
                # Store results for this observation using original index
                results.append({
                    'index': group.iloc[i]['index'],  # Use original DataFrame index
                    'EarningsValueRelevance': r2_vr,
                    'EarningsTimeliness': r2_tl,
                    'EarningsConservatism': conservatism
                })
                
            except Exception as e:
                # Skip problematic regressions
                results.append({
                    'index': group.iloc[i]['index'],  # Use original DataFrame index
                    'EarningsValueRelevance': None,
                    'EarningsTimeliness': None,
                    'EarningsConservatism': None
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

print("Step 8: Merging results back to dataframe...")
# Convert results to DataFrame and merge back
if all_results:
    results_df = pd.DataFrame(all_results).set_index('index')
    
    # Merge back to original dataframe
    df_pandas.loc[results_df.index, 'EarningsValueRelevance'] = results_df['EarningsValueRelevance']
    df_pandas.loc[results_df.index, 'EarningsTimeliness'] = results_df['EarningsTimeliness'] 
    df_pandas.loc[results_df.index, 'EarningsConservatism'] = results_df['EarningsConservatism']

    # Convert back to polars
    df_with_results = pl.from_pandas(df_pandas[['gvkey', 'permno', 'datadate', 'fyear', 
                                               'EarningsValueRelevance', 'EarningsTimeliness', 'EarningsConservatism']])
else:
    print("No regression results generated")
    df_with_results = pl.from_pandas(df_pandas[['gvkey', 'permno', 'datadate', 'fyear']]).with_columns([
        pl.lit(None).alias('EarningsValueRelevance'),
        pl.lit(None).alias('EarningsTimeliness'), 
        pl.lit(None).alias('EarningsConservatism')
    ])

print("Step 9: Expanding to monthly frequency...")
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
df_monthly = df_monthly.unique(subset=["permno", "time_avail_m"], keep="first")

print(f"After monthly expansion: {len(df_monthly):,} observations")

print("Step 10: Saving results...")
# Separate and save each placebo
earnings_value_relevance = df_monthly.select(["permno", "time_avail_m", "EarningsValueRelevance"]).filter(
    pl.col("EarningsValueRelevance").is_not_null()
)
earnings_timeliness = df_monthly.select(["permno", "time_avail_m", "EarningsTimeliness"]).filter(
    pl.col("EarningsTimeliness").is_not_null()
)
earnings_conservatism = df_monthly.select(["permno", "time_avail_m", "EarningsConservatism"]).filter(
    pl.col("EarningsConservatism").is_not_null()
)

# Save all three placebos
save_placebo(earnings_value_relevance, "EarningsValueRelevance")
save_placebo(earnings_timeliness, "EarningsTimeliness")  
save_placebo(earnings_conservatism, "EarningsConservatism")

print(f"Generated {len(earnings_value_relevance)} EarningsValueRelevance observations")
print(f"Generated {len(earnings_timeliness)} EarningsTimeliness observations")
print(f"Generated {len(earnings_conservatism)} EarningsConservatism observations")

print("ZZ1_EarningsValueRelevance_EarningsTimeliness_EarningsConservatism.py completed successfully")
