# ABOUTME: Downloads and processes CRSP-IBES linking table from preprocessed iclink.csv file
# ABOUTME: Filters to high-quality links and creates mapping between IBES tickers and CRSP permnos
"""
Inputs:
- ../pyData/Prep/iclink.csv (CRSP-IBES linking data)

Outputs:
- ../pyData/Intermediate/IBESCRSPLinkingTable.parquet

How to run: python3 CRSPIBESLink.py
"""

import pandas as pd
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from config import MAX_ROWS_DL

print("Processing CRSP-IBES linking data...")

# Load CRSP-IBES linking data from preprocessed file
iclink_data = pd.read_csv("../pyData/Prep/iclink.csv")
print(f"Loaded {len(iclink_data)} linking records from iclink.csv")

# Filter to high-quality links only (SCORE <= 2)
initial_count = len(iclink_data)
iclink_data = iclink_data[iclink_data['SCORE'] <= 2]
print(f"Filtered to {len(iclink_data)} records with SCORE <= 2")

# Keep only the best match per PERMNO (lowest SCORE, then highest TICKER as tiebreaker)
iclink_data = iclink_data.sort_values(['PERMNO', 'SCORE', 'TICKER'], ascending=[True, True, False])
iclink_data = iclink_data.drop_duplicates(['PERMNO'], keep='first')
print(f"After keeping best match per PERMNO: {len(iclink_data)} records")

# Standardize column names and keep only required columns
column_mapping = {
    'TICKER': 'tickerIBES',
    'PERMNO': 'permno'
}
iclink_data = iclink_data.rename(columns=column_mapping)
keep_cols = ['tickerIBES', 'permno']
final_data = iclink_data[keep_cols]

# Apply row limit for debugging if configured
if MAX_ROWS_DL > 0:
    final_data = final_data.head(MAX_ROWS_DL)
    print(f"DEBUG MODE: Limited to {MAX_ROWS_DL} rows")

# Save final linking table
final_data.to_parquet("../pyData/Intermediate/IBESCRSPLinkingTable.parquet", index=False)

print(f"IBES-CRSP Linking Table saved with {len(final_data)} records")

# Display summary statistics and sample data
print(f"Unique permnos: {final_data['permno'].nunique()}")
print(f"Unique IBES tickers: {final_data['tickerIBES'].nunique()}")

print("\nSample data:")
print(final_data.head())
