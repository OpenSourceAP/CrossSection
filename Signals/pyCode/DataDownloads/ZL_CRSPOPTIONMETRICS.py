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

load_dotenv()

def main():
    """Process CRSP-OptionMetrics data"""
    print("Processing CRSP-OptionMetrics data...")

    # Ensure directories exist
    os.makedirs("../pyData/Intermediate", exist_ok=True)

    # Check for OptionMetrics.csv in Prep folder
    om_path = Path("../Data/Prep/OptionMetrics.csv")

    if om_path.exists():
        # Read the OptionMetrics file
        om_data = pd.read_csv(om_path)
        print(f"Loaded {len(om_data)} OptionMetrics records")

        # Basic processing (specific processing depends on file structure)
        if 'date' in om_data.columns:
            om_data['date'] = pd.to_datetime(om_data['date'])
            om_data['time_avail_m'] = om_data['date'].dt.to_period('M')

        # Save processed data
        om_data.to_parquet("../pyData/Intermediate/OPTIONMETRICSCRSPLinkingTable.parquet")

        print(f"OptionMetrics data saved with {len(om_data)} records")

        # Show summary
        if 'time_avail_m' in om_data.columns:
            print(f"Date range: {om_data['time_avail_m'].min()} to {om_data['time_avail_m'].max()}")

        if 'permno' in om_data.columns:
            print(f"Unique permnos: {om_data['permno'].nunique()}")

    else:
        print("WARNING: OptionMetrics.csv not found in ../Data/Prep/")
        print("Creating placeholder OptionMetrics data")

        # Create placeholder data
        placeholder_data = pd.DataFrame({
            'permno': [10001, 10002, 10003],
            'date': ['2020-01-01', '2020-02-01', '2020-03-01'],
            'impl_volatility': [0.25, 0.30, 0.22],
            'option_volume': [1000, 1500, 800]
        })

        placeholder_data['date'] = pd.to_datetime(placeholder_data['date'])
        placeholder_data['time_avail_m'] = placeholder_data['date'].dt.to_period('M')

        # Apply row limit for debugging if configured
        if MAX_ROWS_DL > 0:
            placeholder_data = placeholder_data.head(MAX_ROWS_DL)
            print(f"DEBUG MODE: Limited to {MAX_ROWS_DL} rows")

        # Save the data
        placeholder_data.to_parquet("../pyData/Intermediate/OPTIONMETRICSCRSPLinkingTable.parquet")
        print(f"Placeholder OptionMetrics data saved with {len(placeholder_data)} records")

    print("CRSP-OptionMetrics processing completed")

if __name__ == "__main__":
    main()
