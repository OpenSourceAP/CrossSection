# ABOUTME: Cash predictor - calculates cash to assets ratio
# ABOUTME: Run: python3 pyCode/Predictors/Cash.py

"""
Cash Predictor

Cash to assets ratio calculation: cheq/atq
Uses quarterly Compustat data with complex time expansion logic.

Inputs:
- m_QCompustat.parquet (gvkey, rdq, cheq, atq)
- SignalMasterTable.parquet (permno, gvkey, time_avail_m)

Outputs:
- Cash.csv (permno, yyyymm, Cash)

This predictor calculates cash holdings as a ratio of total quarterly assets,
following the quarterly data expansion and deduplication logic from the original Stata code.
"""

import pandas as pd
import numpy as np
import sys
import os

# Add utils directory to path for imports
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from utils.save_standardized import save_predictor

print("Starting Cash predictor...")

# DATA LOAD - m_QCompustat
# 2020 01 Andrew
# use rdq instead of time_avail_m following OP
# Note: time_avail_m is datadate + 3 months but rdq is unchanged from 
# WRDS download
print("Loading m_QCompustat data...")
qcompustat_df = pd.read_parquet('../pyData/Intermediate/m_QCompustat.parquet', 
                               columns=['gvkey', 'rdq', 'cheq', 'atq'])

print(f"Loaded {len(qcompustat_df):,} quarterly Compustat observations")

# Drop duplicates and filter data (exact Stata deduplication logic)
print("Processing quarterly data...")

# Sort by gvkey rdq (matching Stata: sort gvkey rdq)
qcompustat_df = qcompustat_df.sort_values(['gvkey', 'rdq'])

# Generate dup variable (matching Stata: quietly by gvkey rdq: gen dup = cond(_N==1,0,_n))
qcompustat_df['group_size'] = qcompustat_df.groupby(['gvkey', 'rdq'])['gvkey'].transform('count')
qcompustat_df['obs_num'] = qcompustat_df.groupby(['gvkey', 'rdq']).cumcount() + 1
qcompustat_df['dup'] = np.where(qcompustat_df['group_size'] == 1, 0, qcompustat_df['obs_num'])

# Apply exact Stata filter: keep if !mi(gvkey) & dup == 1 & !mi(atq)
qcompustat_df = qcompustat_df[
    qcompustat_df['gvkey'].notna() & 
    (qcompustat_df['dup'] == 1) & 
    qcompustat_df['atq'].notna()
]

# Clean up temporary columns
qcompustat_df = qcompustat_df.drop(['group_size', 'obs_num', 'dup'], axis=1)

print(f"After deduplication: {len(qcompustat_df):,} observations")

# Define time_avail_m (equivalent to gen time_avail_m = mofd(rdq))
qcompustat_df['time_avail_m'] = pd.to_datetime(qcompustat_df['rdq']).dt.to_period('M').dt.to_timestamp()

# Expand back to monthly (equivalent to Stata expand 3 logic)
print("Expanding quarterly data to monthly...")

# Replicate each row 3 times, then adjust time_avail_m for each copy
# This matches Stata's: expand 3; replace time_avail_m = time_avail_m + _n - 1
expanded_dfs = []
for n in range(1, 4):  # _n goes from 1 to 3 in Stata
    df_copy = qcompustat_df.copy()
    # Add (_n - 1) months to each observation
    df_copy['time_avail_m'] = df_copy['time_avail_m'] + pd.DateOffset(months=n-1)
    expanded_dfs.append(df_copy)

expanded_df = pd.concat(expanded_dfs, ignore_index=True)
print(f"After monthly expansion: {len(expanded_df):,} observations")

# Remove dups: keep newest rdq (most updated announcement)
# Sort by gvkey, time_avail_m, rdq (descending) and keep first
expanded_df = expanded_df.sort_values(['gvkey', 'time_avail_m', 'rdq'], ascending=[True, True, False])
expanded_df = expanded_df.drop_duplicates(['gvkey', 'time_avail_m'], keep='first')

print(f"After removing overlapping announcements: {len(expanded_df):,} observations")

# Load SignalMasterTable for merge
print("Loading SignalMasterTable...")
signal_master = pd.read_parquet('../pyData/Intermediate/SignalMasterTable.parquet', 
                               columns=['permno', 'gvkey', 'time_avail_m'])

# Keep only rows with gvkey
signal_master = signal_master.dropna(subset=['gvkey'])
print(f"Loaded SignalMasterTable: {len(signal_master):,} observations")

# Merge quarterly data with SignalMasterTable
# Use inner join to match Stata's "keep(match)" behavior
print("Merging with SignalMasterTable...")
df = pd.merge(signal_master, expanded_df[['gvkey', 'time_avail_m', 'atq', 'cheq', 'rdq']], 
              on=['gvkey', 'time_avail_m'], how='inner')

print(f"After merge: {len(df):,} observations")

# SIGNAL CONSTRUCTION
print("Constructing Cash signal...")

# Calculate Cash = cheq/atq with domain-aware missing value handling
# Following missing/missing = 1.0 pattern for division operations
df['Cash'] = np.where(
    df['atq'] == 0,
    np.nan,  # Division by zero = missing
    np.where(
        df['cheq'].isna() & df['atq'].isna(),
        1.0,  # missing/missing = 1.0 (no change)
        df['cheq'] / df['atq']
    )
)

print(f"Generated Cash values for {df['Cash'].notna().sum():,} observations")

# Clean up extra columns for save
df = df[['permno', 'time_avail_m', 'Cash']].copy()

# SAVE
print("Saving predictor...")
save_predictor(df, 'Cash')

print("Cash predictor completed successfully!")