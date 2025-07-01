#!/usr/bin/env python3
"""
High-frequency bid-ask spread processing - Python equivalent of ZG_BidaskTAQ.do

Processes high-frequency bid-ask spread data from preprocessed CSV file.
Created via Chen-Velikov JFQA code, includes ISSM spreads.
"""

import os
import pandas as pd
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from config import MAX_ROWS_DL
from utils.column_standardizer_yaml import standardize_columns


def main():
    """Process high-frequency bid-ask spread data."""
    print("Processing high-frequency bid-ask spread data...")
    
    # Load the CSV data
    input_file = "../pyData/Prep/hf_monthly.csv"
    
    if not os.path.exists(input_file):
        raise FileNotFoundError(f"Input file not found: {input_file}")
    
    # Read CSV with headers
    data = pd.read_csv(input_file)
    print(f"Loaded {len(data)} records from {input_file}")
    
    # Convert yearm column to string for processing
    data['yearm'] = data['yearm'].astype(str)
    
    # Extract year and month from yearm string (format: YYYYMM)
    data['y'] = data['yearm'].str[:4].astype(int)
    data['m'] = data['yearm'].str[4:6].astype(int)
    
    # Create time_avail_m as period (monthly)
    data['time_avail_m'] = pd.PeriodIndex.from_fields(
        year=data['y'], month=data['m'], freq='M'
    )
    
    # Create hf_spread from espread_pct_mean
    data['hf_spread'] = data['espread_pct_mean']
    
    # Keep only required columns
    data = data[['permno', 'time_avail_m', 'hf_spread']].copy()
    
    # Drop rows with missing values
    data = data.dropna()
    print(f"After dropping missing values: {len(data)} records")
    
    # Ensure optimal data types
    data['permno'] = data['permno'].astype('int64')
    
    # Apply Pattern 1 fix: Convert Period to datetime64[ns] BEFORE saving
    data['time_avail_m'] = data['time_avail_m'].dt.to_timestamp()
    
    # Save to parquet
    output_file = "../pyData/Intermediate/hf_spread.parquet"
    os.makedirs(os.path.dirname(output_file), exist_ok=True)
    
    # Apply row limit for debugging if configured
    if MAX_ROWS_DL > 0:
        data = data.head(MAX_ROWS_DL)
        print(f"DEBUG MODE: Limited to {MAX_ROWS_DL} rows")

    # Save the data
    # Apply column standardization
    data = standardize_columns(data, 'hf_spread')
    data.to_parquet(output_file, index=False)
    
    print(f"Saved {len(data)} records to {output_file}")
    print("High-frequency bid-ask spread processing completed successfully.")


if __name__ == "__main__":
    main()