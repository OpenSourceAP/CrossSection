# ABOUTME: Translates skew1.do to create smirk skewness predictor
# ABOUTME: Run from pyCode/ directory: python3 Predictors/skew1.py

# Run from pyCode/ directory
# Inputs: SignalMasterTable.parquet, OptionMetricsXZZ.parquet
# Output: ../pyData/Predictors/skew1.csv

import pandas as pd
import numpy as np

# DATA LOAD
df = pd.read_parquet('../pyData/Intermediate/SignalMasterTable.parquet')
df = df[['permno', 'time_avail_m', 'secid']].copy()

# Split into two groups: missing secid and non-missing secid
missing_secid = df[df['secid'].isna()].copy()
has_secid = df[df['secid'].notna()].copy()

# Merge with OptionMetrics data for observations with secid
options = pd.read_parquet('../pyData/Intermediate/OptionMetricsXZZ.parquet')
has_secid = has_secid.merge(options, on=['secid', 'time_avail_m'], how='left')

# Combine back together (append missing secid observations)
df_final = pd.concat([has_secid, missing_secid], ignore_index=True)

# SIGNAL CONSTRUCTION
# Construction is done in R1_OptionMetrics.R (skew1 should already be in the data)

# Keep only necessary columns for output
df_final = df_final[['permno', 'time_avail_m', 'skew1']].copy()
df_final = df_final.dropna(subset=['skew1'])

# Convert time_avail_m to yyyymm format like other predictors
df_final['yyyymm'] = df_final['time_avail_m'].dt.year * 100 + df_final['time_avail_m'].dt.month

# Convert to integers for consistency with other predictors
df_final['permno'] = df_final['permno'].astype('int64')
df_final['yyyymm'] = df_final['yyyymm'].astype('int64')

# Keep only required columns and set index
df_final = df_final[['permno', 'yyyymm', 'skew1']].copy()
df_final = df_final.set_index(['permno', 'yyyymm'])

# SAVE
df_final.to_csv('../pyData/Predictors/skew1.csv')

print("skew1 predictor saved successfully")