# ABOUTME: Consensus Recommendation following Barber et al. 2001, Table 3A
# ABOUTME: Binary variable if monthly mean of recommendations over analysts is greater than 3, and 0 if less or equal to 1.5
"""
Usage:
    python3 Predictors/ConsRecomm.py

Inputs:
    - IBES_Recommendations.parquet: IBES recommendations data with columns [tickerIBES, amaskcd, anndats, time_avail_m, ireccd]
    - SignalMasterTable.parquet: Monthly master table with permno-ticker mapping

Outputs:
    - ConsRecomm.csv: CSV file with columns [permno, yyyymm, ConsRecomm]
    - ConsRecomm = 1 if mean ireccd > 3, ConsRecomm = 0 if mean ireccd <= 1.5 (following Table 3A)
"""

import pandas as pd
import numpy as np
import sys
import os

# Add utils directory to path for imports
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from utils.save_standardized import save_predictor

print("Starting ConsRecomm predictor...")

# PREP IBES DATA
print("Loading IBES Recommendations data...")
ibes_df = pd.read_parquet('../pyData/Intermediate/IBES_Recommendations.parquet', 
                         columns=['tickerIBES', 'amaskcd', 'anndats', 'time_avail_m', 'ireccd'])

print(f"Loaded {len(ibes_df):,} IBES recommendations observations")

# Collapse down to firm-month level
# Sort by time to get last non-missing value within each ticker-analyst-month group
ibes_df = ibes_df.sort_values(['tickerIBES', 'amaskcd', 'time_avail_m', 'anndats'])
ibes_df = ibes_df.groupby(['tickerIBES', 'amaskcd', 'time_avail_m'])['ireccd'].last().reset_index()

print(f"After first collapse: {len(ibes_df):,} observations")

# Aggregate across analysts to get mean recommendation per ticker-month
ibes_df = ibes_df.groupby(['tickerIBES', 'time_avail_m'])['ireccd'].mean().reset_index()

print(f"After second collapse: {len(ibes_df):,} observations")

# Create binary recommendation signal: 1 for sell recommendations, 0 for strong buy
ibes_df['ConsRecomm'] = np.nan
ibes_df.loc[(ibes_df['ireccd'] > 3) & ibes_df['ireccd'].notna(), 'ConsRecomm'] = 1
ibes_df.loc[ibes_df['ireccd'] <= 1.5, 'ConsRecomm'] = 0

print(f"Generated ConsRecomm values for {ibes_df['ConsRecomm'].notna().sum():,} observations")

# Add permno
print("Loading SignalMasterTable...")
signal_master = pd.read_parquet('../pyData/Intermediate/SignalMasterTable.parquet', 
                               columns=['permno', 'time_avail_m', 'tickerIBES'])

print(f"Loaded {len(signal_master):,} SignalMasterTable observations")

# Merge with SignalMasterTable
print("Merging data...")
# One IBES ticker can match multiple permnos
df = pd.merge(ibes_df, signal_master, on=['tickerIBES', 'time_avail_m'], how='inner')

print(f"After merging: {len(df):,} observations")

# Clean up temporary columns
df = df.drop(columns=['ireccd'])

# SAVE
print("Saving predictor...")
save_predictor(df, 'ConsRecomm')

print("ConsRecomm predictor completed successfully!")