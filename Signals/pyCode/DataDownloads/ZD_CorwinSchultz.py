#!/usr/bin/env python3
"""
Corwin-Schultz bid-ask spread processing - Python equivalent of ZD_CorwinSchultz.do

Processes Corwin-Schultz bid-ask spread data from preprocessed CSV file.
"""

import os
import pandas as pd


def main():
    """Process Corwin-Schultz bid-ask spread data."""
    print("Processing Corwin-Schultz bid-ask spread data...")
    
    # Load the CSV data
    input_file = "../Data/Prep/corwin_schultz_spread.csv"
    
    if not os.path.exists(input_file):
        raise FileNotFoundError(f"Input file not found: {input_file}")
    
    # Read CSV with headers
    data = pd.read_csv(input_file)
    print(f"Loaded {len(data)} records from {input_file}")
    
    # Convert month column to string for processing
    data['month'] = data['month'].astype(str)
    
    # Extract year and month from month string (format: YYYYMM)
    data['y'] = data['month'].str[:4].astype(int)
    data['m'] = data['month'].str[4:6].astype(int)
    
    # Create time_avail_m as period (monthly)
    data['time_avail_m'] = pd.PeriodIndex.from_fields(
        year=data['y'], month=data['m'], freq='M'
    )
    
    # Drop intermediate columns
    data = data.drop(['y', 'm', 'month'], axis=1)
    
    # Drop rows with missing PERMNO (note: column is uppercase)
    data = data.dropna(subset=['PERMNO'])
    print(f"After dropping missing PERMNO: {len(data)} records")
    
    # Rename columns to match Stata output
    data = data.rename(columns={
        'PERMNO': 'permno',
        'hlspread': 'BidAskSpread'
    })
    
    # Ensure optimal data types
    data['permno'] = data['permno'].astype('int64')
    
    # Save to parquet
    output_file = "../pyData/Intermediate/BAspreadsCorwin.parquet"
    os.makedirs(os.path.dirname(output_file), exist_ok=True)
    data.to_parquet(output_file, index=False)
    
    print(f"Saved {len(data)} records to {output_file}")
    print("Corwin-Schultz bid-ask spread processing completed successfully.")


if __name__ == "__main__":
    main()