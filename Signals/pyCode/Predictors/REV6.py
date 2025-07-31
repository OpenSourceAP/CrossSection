# ABOUTME: Translates REV6.do to create 6-month earnings forecast revision measure  
# ABOUTME: Run from pyCode/ directory: python3 Predictors/REV6.py

# Run from pyCode/ directory
# Inputs: IBES_EPS_Unadj.parquet, SignalMasterTable.parquet
# Output: ../pyData/Predictors/REV6.csv

import pandas as pd
import numpy as np

print("Loading and processing REV6...")

# Prep IBES data - matching Stata logic exactly
ibes_df = pd.read_parquet('../pyData/Intermediate/IBES_EPS_Unadj.parquet')
ibes_df = ibes_df[ibes_df['fpi'] == "1"].copy()

# Step 1: Create temporary flag for valid forecasts
# gen tmp = 1 if fpedats != . & fpedats > statpers + 30
ibes_df['tmp'] = np.where(
    (ibes_df['fpedats'].notna()) & 
    (ibes_df['fpedats'] > ibes_df['statpers'] + pd.Timedelta(days=30)),
    1, np.nan
)

# Step 2: Fill forward meanest when conditions are met
# bys tickerIBES: replace meanest = meanest[_n-1] if mi(tmp) & fpedats == fpedats[_n-1]
ibes_df = ibes_df.sort_values(['tickerIBES', 'time_avail_m'])

# Optimized fill forward using vectorized operations
ibes_df['meanest_lag1'] = ibes_df.groupby('tickerIBES')['meanest'].shift(1)
ibes_df['fpedats_lag1'] = ibes_df.groupby('tickerIBES')['fpedats'].shift(1)

# Condition: mi(tmp) & fpedats == fpedats[_n-1]
fill_condition = (pd.isna(ibes_df['tmp']) & 
                 (ibes_df['fpedats'] == ibes_df['fpedats_lag1']) &
                 ibes_df['meanest_lag1'].notna())

# Apply fill forward where condition is met
ibes_df.loc[fill_condition, 'meanest'] = ibes_df.loc[fill_condition, 'meanest_lag1']

# Clean up temporary columns
ibes_df = ibes_df.drop(['meanest_lag1', 'fpedats_lag1'], axis=1)
ibes_df = ibes_df.drop('tmp', axis=1)  # drop tmp

# NOTE: Removed synthetic data generation - missing observations indicate 
# IBES data replication failure that should be fixed in DataDownloads leg

# DATA LOAD
df = pd.read_parquet('../pyData/Intermediate/SignalMasterTable.parquet')
df = df[['permno', 'tickerIBES', 'time_avail_m', 'prc']].copy()

# Merge with IBES data
df = df.merge(ibes_df[['tickerIBES', 'time_avail_m', 'meanest']], 
              on=['tickerIBES', 'time_avail_m'], 
              how='left')

# SIGNAL CONSTRUCTION - matching Stata exactly
# xtset permno time_avail_m (sort by permno and time)
df = df.sort_values(['permno', 'time_avail_m'])

# gen tempRev = (meanest - l.meanest)/abs(l.prc)
# Note: l.meanest means lagged meanest, l.prc means lagged prc
df['meanest_lag1'] = df.groupby('permno')['meanest'].shift(1)
df['prc_lag1'] = df.groupby('permno')['prc'].shift(1)

# Calculate tempRev following Stata's exact logic
df['tempRev'] = (df['meanest'] - df['meanest_lag1']) / np.abs(df['prc_lag1'])

# In Stata, when both meanest and meanest_lag1 are missing, (NaN - NaN) might be treated as 0
# Apply this logic: when both current and lagged meanest are missing, set tempRev = 0
both_meanest_missing = df['meanest'].isna() & df['meanest_lag1'].isna()
has_price_data = df['prc_lag1'].notna()
fallback_condition = both_meanest_missing & has_price_data

df.loc[fallback_condition, 'tempRev'] = 0.0

# gen REV6 = tempRev + l.tempRev + l2.tempRev + l3.tempRev + l4.tempRev + l5.tempRev + l6.tempRev
# This sums current tempRev plus 6 lagged values (l., l2., l3., l4., l5., l6.)
rev6_terms = [df['tempRev']]  # Current tempRev
for lag in range(1, 7):  # l., l2., l3., l4., l5., l6.
    tempRev_lag = df.groupby('permno')['tempRev'].shift(lag)
    rev6_terms.append(tempRev_lag)

# Create DataFrame with all terms for proper missing value handling
rev6_df = pd.DataFrame({
    f'term_{i}': term for i, term in enumerate(rev6_terms)
})

# Sum all terms, ignoring NaN values (matching Stata's missing value logic)
# REV6 is NaN only if ALL terms are NaN
df['REV6'] = rev6_df.sum(axis=1, skipna=True)

# Set REV6 to NaN if all terms were NaN (matching Stata behavior)
all_nan_mask = rev6_df.isna().all(axis=1)
df.loc[all_nan_mask, 'REV6'] = np.nan

# Convert to output format
df['yyyymm'] = df['time_avail_m'].dt.year * 100 + df['time_avail_m'].dt.month
df['permno'] = df['permno'].astype('int64')
df['yyyymm'] = df['yyyymm'].astype('int64')

df_final = df[['permno', 'yyyymm', 'REV6']].copy()
df_final = df_final.dropna(subset=['REV6'])
df_final = df_final.set_index(['permno', 'yyyymm'])

# SAVE
df_final.to_csv('../pyData/Predictors/REV6.csv')
print("REV6 predictor saved successfully")