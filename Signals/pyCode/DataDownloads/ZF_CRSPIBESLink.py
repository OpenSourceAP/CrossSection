# ABOUTME: Downloads and processes CRSP-IBES linking table from preprocessed iclink.csv file
# ABOUTME: Filters to high-quality links and creates mapping between IBES tickers and CRSP permnos
"""
Inputs:
- ../pyData/Prep/iclink.csv (CRSP-IBES linking data)

Outputs:
- ../pyData/Intermediate/IBESCRSPLinkingTable.parquet

How to run: python3 ZF_CRSPIBESLink.py
"""

import os
import pandas as pd
from pathlib import Path
from dotenv import load_dotenv
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from config import MAX_ROWS_DL
from utils.column_standardizer_yaml import standardize_columns

load_dotenv()

def main():
    print("Processing CRSP-IBES linking data...")

    # Create output directory
    os.makedirs("../pyData/Intermediate", exist_ok=True)

    # Load CRSP-IBES linking data from preprocessed file
    iclink_path = Path("../pyData/Prep/iclink.csv")

    if iclink_path.exists():
        iclink_data = pd.read_csv(iclink_path)
        print(f"Loaded {len(iclink_data)} linking records from iclink.csv")

        # Filter to high-quality links only (SCORE <= 2)
        if 'SCORE' in iclink_data.columns:
            initial_count = len(iclink_data)
            iclink_data = iclink_data[iclink_data['SCORE'] <= 2]
            print(f"Filtered to {len(iclink_data)} records with SCORE <= 2")

        # Keep only the best match per PERMNO (lowest SCORE, then highest TICKER as tiebreaker)
        if 'PERMNO' in iclink_data.columns and 'SCORE' in iclink_data.columns:
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
        available_cols = [col for col in keep_cols if col in iclink_data.columns]
        final_data = iclink_data[available_cols]

    else:
        print("WARNING: iclink.csv not found in ../pyData/Prep/")
        print("Creating placeholder linking table")

        # Create minimal placeholder data when source file is missing
        final_data = pd.DataFrame({
            'tickerIBES': ['AAPL', 'MSFT', 'GOOGL'],
            'permno': [14593, 10107, 90319]
        })

    # Apply row limit for debugging if configured
    if MAX_ROWS_DL > 0:
        final_data = final_data.head(MAX_ROWS_DL)
        print(f"DEBUG MODE: Limited to {MAX_ROWS_DL} rows")

    # Apply column standardization and save final linking table
    final_data = standardize_columns(final_data, 'IBESCRSPLinkingTable')
    final_data.to_parquet("../pyData/Intermediate/IBESCRSPLinkingTable.parquet", index=False)

    print(f"IBES-CRSP Linking Table saved with {len(final_data)} records")

    # Display summary statistics and sample data
    if 'permno' in final_data.columns:
        print(f"Unique permnos: {final_data['permno'].nunique()}")

    if 'tickerIBES' in final_data.columns:
        print(f"Unique IBES tickers: {final_data['tickerIBES'].nunique()}")

    print("\nSample data:")
    print(final_data.head())

if __name__ == "__main__":
    main()
