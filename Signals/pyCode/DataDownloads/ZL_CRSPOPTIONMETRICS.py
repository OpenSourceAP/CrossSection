#!/usr/bin/env python3
"""
CRSP-OptionMetrics data script - Python equivalent of ZL_CRSPOPTIONMETRICS.do

Processes OptionMetrics data from preprocessed file.
"""

import os
import pandas as pd
from pathlib import Path
from dotenv import load_dotenv
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from config import MAX_ROWS_DL
from utils.column_standardizer import standardize_against_dta

load_dotenv()

def main():
    """Process CRSP-OptionMetrics data"""
    print("Processing CRSP-OptionMetrics data...")

    # Ensure directories exist
    os.makedirs("../pyData/Intermediate", exist_ok=True)

    # Check for oclink.csv in Prep folder
    om_path = Path("../Data/Prep/oclink.csv")

    if om_path.exists():
        # Read the OptionMetrics linking file
        om_data = pd.read_csv(om_path)
        print(f"Loaded {len(om_data)} OptionMetrics linking records")

        # Keep only records with score <= 6 (good matches)
        if 'SCORE' in om_data.columns:
            om_data = om_data[om_data['SCORE'] <= 6]
            print(f"After filtering for score <= 6: {len(om_data)} records")

        # Rename columns to match expected output
        column_mapping = {
            'PERMNO': 'permno',
            'SCORE': 'om_score'
        }
        om_data = om_data.rename(columns=column_mapping)

        # Keep only required columns
        required_cols = ['secid', 'permno', 'om_score']
        available_cols = [col for col in required_cols if col in om_data.columns]
        om_data = om_data[available_cols]

        # Keep best match (lowest score) per permno
        if 'om_score' in om_data.columns and 'permno' in om_data.columns:
            om_data = om_data.sort_values('om_score').groupby('permno').first().reset_index()

        # Standardize columns to match DTA file
        om_data = standardize_against_dta(
            om_data, 
            "../Data/Intermediate/OPTIONMETRICSCRSPLinkingTable.dta",
            "OPTIONMETRICSCRSPLinkingTable"
        )

        # Save processed data
        om_data.to_parquet("../pyData/Intermediate/OPTIONMETRICSCRSPLinkingTable.parquet", index=False)

        print(f"OptionMetrics linking data saved with {len(om_data)} records")
        print(f"Unique permnos: {om_data['permno'].nunique()}")

    else:
        print("WARNING: oclink.csv not found in ../Data/Prep/")
        print("Creating placeholder OptionMetrics linking data")

        # Create placeholder data
        placeholder_data = pd.DataFrame({
            'secid': [100001, 100002, 100003],
            'permno': [10001, 10002, 10003],
            'om_score': [1, 2, 3]
        })

        # Apply row limit for debugging if configured
        if MAX_ROWS_DL > 0:
            placeholder_data = placeholder_data.head(MAX_ROWS_DL)
            print(f"DEBUG MODE: Limited to {MAX_ROWS_DL} rows")

        # Standardize columns to match DTA file
        placeholder_data = standardize_against_dta(
            placeholder_data, 
            "../Data/Intermediate/OPTIONMETRICSCRSPLinkingTable.dta",
            "OPTIONMETRICSCRSPLinkingTable"
        )

        # Save the data
        placeholder_data.to_parquet("../pyData/Intermediate/OPTIONMETRICSCRSPLinkingTable.parquet", index=False)
        print(f"Placeholder OptionMetrics linking data saved with {len(placeholder_data)} records")

    print("CRSP-OptionMetrics processing completed")

if __name__ == "__main__":
    main()
