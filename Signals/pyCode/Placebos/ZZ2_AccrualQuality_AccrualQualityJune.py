# ABOUTME: ZZ2_AccrualQuality_AccrualQualityJune.py - calculates accrual quality placebos
# ABOUTME: Python equivalent of ZZ2_AccrualQuality_AccrualQualityJune.do, translates line-by-line from Stata code

"""
ZZ2_AccrualQuality_AccrualQualityJune.py

Inputs:
    - a_aCompustat.parquet: gvkey, permno, time_avail_m, datadate, fyear, ib, act, che, lct, dlc, dp, at, sale, sic, ppegt columns

Outputs:
    - AccrualQuality.csv: permno, yyyymm, AccrualQuality columns
    - AccrualQualityJune.csv: permno, yyyymm, AccrualQualityJune columns

Usage:
    cd pyCode
    source .venv/bin/activate  
    python3 Placebos/ZZ2_AccrualQuality_AccrualQualityJune.py
"""

import pandas as pd
import polars as pl
import numpy as np
import sys
import os

# Add parent directory to path to import utils
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from utils.save_standardized import save_placebo
from utils.sicff import sicff

print("Starting ZZ2_AccrualQuality_AccrualQualityJune.py")

# DATA LOAD
print("Loading a_aCompustat...")
df = pl.read_parquet("../pyData/Intermediate/a_aCompustat.parquet")
df = df.select(['gvkey', 'permno', 'time_avail_m', 'datadate', 'fyear', 'ib', 'act', 'che', 'lct', 'dlc', 'dp', 'at', 'sale', 'sic', 'ppegt'])

print(f"Loaded data: {len(df)} rows")

# SIGNAL CONSTRUCTION
# Sort by gvkey and fyear
print("Sorting by gvkey and fyear...")
df = df.sort(['gvkey', 'fyear'])

# Create lags needed for accruals calculation
print("Computing lags...")
df = df.with_columns([
    pl.col('act').shift(1).over('gvkey').alias('l_act'),
    pl.col('che').shift(1).over('gvkey').alias('l_che'),
    pl.col('lct').shift(1).over('gvkey').alias('l_lct'),
    pl.col('dlc').shift(1).over('gvkey').alias('l_dlc'),
    pl.col('at').shift(1).over('gvkey').alias('l_at')
])

# Compute accruals and related variables
print("Computing accrual quality components...")

# gen tempAccruals = ( (act - l.act) - (che - l.che) - ( (lct - l.lct) - (dlc - l.dlc)  ) - dp) / ( (at + l.at)/2)
df = df.with_columns([
    (((pl.col('act') - pl.col('l_act')) - (pl.col('che') - pl.col('l_che')) - 
      ((pl.col('lct') - pl.col('l_lct')) - (pl.col('dlc') - pl.col('l_dlc'))) - 
      pl.col('dp')) / ((pl.col('at') + pl.col('l_at')) / 2)).alias('tempAccruals')
])

# gen tempCAcc = tempAccruals + dp/( (at + l.at)/2)
df = df.with_columns([
    (pl.col('tempAccruals') + pl.col('dp') / ((pl.col('at') + pl.col('l_at')) / 2)).alias('tempCAcc')
])

# gen tempRev = sale/( (at + l.at)/2)
df = df.with_columns([
    (pl.col('sale') / ((pl.col('at') + pl.col('l_at')) / 2)).alias('tempRev')
])

# gen tempDelRev = tempRev - l.tempRev
df = df.with_columns([
    pl.col('tempRev').shift(1).over('gvkey').alias('l_tempRev')
])
df = df.with_columns([
    (pl.col('tempRev') - pl.col('l_tempRev')).alias('tempDelRev')
])

# gen tempPPE = ppegt/( (at + l.at)/2)
df = df.with_columns([
    (pl.col('ppegt') / ((pl.col('at') + pl.col('l_at')) / 2)).alias('tempPPE')
])

# gen tempCFO = ib/( (at + l.at)/2) - tempAccruals
df = df.with_columns([
    (pl.col('ib') / ((pl.col('at') + pl.col('l_at')) / 2) - pl.col('tempAccruals')).alias('tempCFO')
])

# Create lags of tempCFO for regression (l(-1/1).tempCFO means lag -1, 0, 1)
df = df.with_columns([
    pl.col('tempCFO').shift(-1).over('gvkey').alias('f1_tempCFO'),  # Lead 1
    pl.col('tempCFO').shift(1).over('gvkey').alias('l1_tempCFO')    # Lag 1
])

# Convert sic to numeric and add FF48 industry classification
print("Adding industry classification...")
df = df.with_columns([
    pl.col('sic').cast(pl.Utf8).str.extract(r'(\d+)', 1).cast(pl.Int32, strict=False).alias('sic_numeric')
])

# Convert to pandas for sicff and regression processing
df_pandas = df.to_pandas()

# Apply FF48 industry classification
print("Computing FF48 industries...")
df_pandas['FF48'] = sicff(df_pandas['sic_numeric'].fillna(0).astype(int))

# Remove missing FF48
df_pandas = df_pandas[df_pandas['FF48'].notna()].copy()

print(f"After adding FF48 industries: {len(df_pandas)} rows")

# Run regressions for each year and industry to get residuals using Stata-compatible regression
print("Running year-industry regressions...")
from utils.stata_regress import regress
import statsmodels.api as sm

df_pandas['tempResid'] = np.nan

# Group by year and industry to run regressions (matching Stata's approach)
for (year, industry), group in df_pandas.groupby(['fyear', 'FF48']):
    # Apply 20-observation threshold first (matching Stata line 33)
    if len(group) < 20:
        continue  # Skip groups with < 20 observations
    
    # Prepare regression variables
    y = group['tempCAcc']
    X_cols = ['l1_tempCFO', 'tempCFO', 'f1_tempCFO', 'tempDelRev', 'tempPPE']
    X = group[X_cols]
    
    # Replace infinity values with NaN
    X = X.replace([np.inf, -np.inf], np.nan)
    y = y.replace([np.inf, -np.inf], np.nan)
    
    # Check if we have enough valid observations
    valid_mask = y.notna() & X.notna().all(axis=1)
    
    if valid_mask.sum() >= 6:  # Need minimum observations for regression
        try:
            # Use Stata-compatible regress function 
            # This matches Stata's exact regression behavior including collinearity handling
            model, keep_cols, drop_cols, reasons, full_coefs = regress(
                X.loc[valid_mask], 
                y.loc[valid_mask], 
                add_constant=True, 
                omit_collinear=True
            )
            
            # Predict for all observations in group (including invalid ones)
            # Build design matrix with constant
            X_with_const = sm.add_constant(X.fillna(0))  # Fill NaN with 0 for prediction
            y_pred = model.predict(X_with_const)
            
            # Calculate residuals, but only keep for valid observations
            residuals = y - y_pred
            residuals = residuals.where(valid_mask, np.nan)
            
            # Assign back to dataframe
            df_pandas.loc[group.index, 'tempResid'] = residuals
            
        except Exception as e:
            pass  # Skip if regression fails

# Compute rolling standard deviation of residuals
print("Computing rolling standard deviation of residuals...")
df_final = pl.from_pandas(df_pandas)

# Sort by gvkey and fyear for lag operations
df_final = df_final.sort(['gvkey', 'fyear'])

# Create lags of tempResid for rolling std calculation
df_final = df_final.with_columns([
    pl.col('tempResid').shift(1).over('gvkey').alias('tempResid1'),
    pl.col('tempResid').shift(2).over('gvkey').alias('tempResid2'),
    pl.col('tempResid').shift(3).over('gvkey').alias('tempResid3'),
    pl.col('tempResid').shift(4).over('gvkey').alias('tempResid4')
])

# Convert back to pandas for rowwise std calculation
df_pandas_final = df_final.to_pandas()

# Calculate rowwise standard deviation of residuals (current + 4 lags)
residual_cols = ['tempResid', 'tempResid1', 'tempResid2', 'tempResid3', 'tempResid4']
df_pandas_final['tempN'] = df_pandas_final[residual_cols].isna().sum(axis=1)
df_pandas_final['AQ'] = df_pandas_final[residual_cols].std(axis=1, skipna=True)

# Replace AQ with missing if more than 1 missing value (tempN > 1)
df_pandas_final.loc[df_pandas_final['tempN'] > 1, 'AQ'] = np.nan

# Create AccrualQuality with 1-year lag (since construction uses one year ahead operating cash flow)
df_pandas_final = df_pandas_final.sort_values(['gvkey', 'fyear'])
df_pandas_final['AccrualQuality'] = df_pandas_final.groupby('gvkey')['AQ'].shift(1)

print(f"Generated AccrualQuality for {len(df_pandas_final)} annual observations")

# Expand to monthly data (replicating Stata's exact logic)
print("Expanding to monthly data...")

# Create 12 copies of each row (equivalent to Stata's expand 12)
df_expanded = pd.concat([df_pandas_final] * 12, ignore_index=True)

# Add month offsets (equivalent to Stata's _n - 1 logic)
df_expanded = df_expanded.sort_values(['gvkey', 'time_avail_m', 'datadate'])
df_expanded['month_offset'] = df_expanded.groupby(['gvkey', 'time_avail_m', 'datadate']).cumcount()

# Update time_avail_m to match Stata's exact output pattern
# Key insight: AccrualQuality for fyear N becomes available from (fyear N time_avail_m - 12 months) to (fyear N time_avail_m - 1 month)
# So fyear 1986 (time_avail_m = 1987-06) → available from 1986-06 to 1987-05
# This means: base_time_avail_m + [month_offset - 12] where month_offset = 0,1,2,...,11  
df_expanded['time_avail_m'] = df_expanded.apply(
    lambda row: row['time_avail_m'] + pd.DateOffset(months=int(row['month_offset']) - 12), axis=1
)

# Drop the temporary column
df_expanded = df_expanded.drop('month_offset', axis=1)

# Keep latest datadate for each permno-time combination (equivalent to Stata's bysort permno time_avail_m (datadate): keep if _n == _N)
df_expanded = df_expanded.sort_values(['permno', 'time_avail_m', 'datadate'])
df_expanded = df_expanded.groupby(['permno', 'time_avail_m']).tail(1)

# Create June version (AccrualQualityJune) BEFORE filtering missing AccrualQuality
df_expanded['AccrualQualityJune'] = np.where(
    df_expanded['time_avail_m'].dt.month == 6, 
    df_expanded['AccrualQuality'], 
    np.nan
)

# Forward fill AccrualQualityJune within each permno (do this BEFORE filtering)
df_expanded = df_expanded.sort_values(['permno', 'time_avail_m'])
df_expanded['AccrualQualityJune'] = df_expanded.groupby('permno')['AccrualQualityJune'].ffill()

# Now filter out rows with missing AccrualQuality (but preserve AccrualQualityJune forward-filled values)
# Keep rows where either AccrualQuality OR AccrualQualityJune is not null
df_expanded = df_expanded[df_expanded['AccrualQuality'].notna() | df_expanded['AccrualQualityJune'].notna()]

print(f"After monthly expansion: {len(df_expanded)} observations")

# Convert back to polars for saving
df_final = pl.from_pandas(df_expanded[['permno', 'time_avail_m', 'AccrualQuality', 'AccrualQualityJune']])

# Split for separate saves
df_accrual = df_final.select(['permno', 'time_avail_m', 'AccrualQuality'])
df_accrual_june = df_final.select(['permno', 'time_avail_m', 'AccrualQualityJune'])

# SAVE
save_placebo(df_accrual, 'AccrualQuality')
save_placebo(df_accrual_june, 'AccrualQualityJune')

print(f"Generated {len(df_accrual)} AccrualQuality observations")
print(f"Generated {len(df_accrual_june)} AccrualQualityJune observations")

print("ZZ2_AccrualQuality_AccrualQualityJune.py completed")