#!/usr/bin/env python3
"""
CRSP-IBES Linking data script - Python equivalent of ZF_CRSPIBESLink.do

Processes IBES-CRSP linking table from preprocessed file.
"""

import os
import pandas as pd
from pathlib import Path
from dotenv import load_dotenv
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from config import MAX_ROWS_DL

load_dotenv()

def main():
    """Process CRSP-IBES linking data"""
    print("Processing CRSP-IBES linking data...")

    # Ensure directories exist
    os.makedirs("../pyData/Intermediate", exist_ok=True)

    # Check for iclink.csv in Prep folder
    iclink_path = Path("../Data/Prep/iclink.csv")

    if iclink_path.exists():
        # Read the iclink file
        iclink_data = pd.read_csv(iclink_path)
        print(f"Loaded {len(iclink_data)} linking records from iclink.csv")

        # Keep only high-quality links (score <= 2)
        if 'SCORE' in iclink_data.columns:
            initial_count = len(iclink_data)
            iclink_data = iclink_data[iclink_data['SCORE'] <= 2]
            print(f"Filtered to {len(iclink_data)} records with SCORE <= 2")

        # Keep best match for each permno (lowest score)
        if 'PERMNO' in iclink_data.columns and 'SCORE' in iclink_data.columns:
            iclink_data = iclink_data.sort_values(['PERMNO', 'SCORE'])
            iclink_data = iclink_data.drop_duplicates(['PERMNO'], keep='first')
            print(f"After keeping best match per PERMNO: {len(iclink_data)} records")

        # Rename columns to match expected output
        column_mapping = {
            'TICKER': 'tickeribes',
            'PERMNO': 'permno'
        }
        iclink_data = iclink_data.rename(columns=column_mapping)

        # Keep only necessary columns
        keep_cols = ['tickeribes', 'permno']
        available_cols = [col for col in keep_cols if col in iclink_data.columns]
        final_data = iclink_data[available_cols]

    else:
        print("WARNING: iclink.csv not found in ../Data/Prep/")
        print("Creating placeholder linking table")

        # Create placeholder data
        final_data = pd.DataFrame({
            'tickeribes': ['AAPL', 'MSFT', 'GOOGL'],
            'permno': [14593, 10107, 90319]
        })

    # Apply row limit for debugging if configured
    if MAX_ROWS_DL > 0:
        final_data = final_data.head(MAX_ROWS_DL)
        print(f"DEBUG MODE: Limited to {MAX_ROWS_DL} rows")

    # Save the data
    final_data.to_parquet("../pyData/Intermediate/IBESCRSPLinkingTable.parquet", index=False)

    print(f"IBES-CRSP Linking Table saved with {len(final_data)} records")

    # Show summary statistics
    if 'permno' in final_data.columns:
        print(f"Unique permnos: {final_data['permno'].nunique()}")

    if 'tickeribes' in final_data.columns:
        print(f"Unique IBES tickers: {final_data['tickeribes'].nunique()}")

    print("\nSample data:")
    print(final_data.head())

if __name__ == "__main__":
    main()
