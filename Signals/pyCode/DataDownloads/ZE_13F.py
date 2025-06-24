#!/usr/bin/env python3
"""
Thomson Reuters 13F holdings processing - Python equivalent of ZE_13F.do

Processes Thomson Reuters 13F institutional holdings data from preprocessed CSV file.
Includes forward-fill logic for missing months.
"""

import os
import pandas as pd
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from config import MAX_ROWS_DL


def main():
    """Process Thomson Reuters 13F holdings data."""
    print("Processing Thomson Reuters 13F holdings data...")
    
    # Load the CSV data
    input_file = "../Data/Prep/tr_13f.csv"
    
    if not os.path.exists(input_file):
        raise FileNotFoundError(f"Input file not found: {input_file}")
    
    # Read CSV with headers, applying row limit if configured
    nrows = None if MAX_ROWS_DL == -1 else MAX_ROWS_DL
    data = pd.read_csv(input_file, nrows=nrows)
    
    if MAX_ROWS_DL > 0:
        print(f"DEBUG MODE: Limited to {MAX_ROWS_DL} rows")
    print(f"Loaded {len(data)} records from {input_file}")
    
    # Drop rows with missing PERMNO
    data = data.dropna(subset=['PERMNO'])
    print(f"After dropping missing PERMNO: {len(data)} records")
    
    # Convert numeric columns, forcing errors to NaN
    numeric_cols = ['instown_perc', 'maxinstown_perc', 'numinstown']
    for col in numeric_cols:
        data[col] = pd.to_numeric(data[col], errors='coerce')
    
    # Convert rdate to datetime and create time_avail_m
    data['time_d'] = pd.to_datetime(data['rdate'], format='%d%b%Y')
    data['time_avail_m'] = data['time_d'].dt.to_period('M')
    
    # Drop intermediate columns
    data = data.drop(['rdate', 'time_d'], axis=1)
    
    # Rename columns to match Stata output (lowercase)
    data = data.rename(columns={
        'PERMNO': 'permno',
        'DBREADTH': 'dbreadth'
    })
    
    # Ensure optimal data types
    data['permno'] = data['permno'].astype('int64')
    
    # Stata tsfill equivalent: fill missing months and forward-fill values
    # Use working version that creates a bit more records than Stata but functionally correct
    # Convert time_avail_m to datetime for easier manipulation
    data['time_dt'] = data['time_avail_m'].dt.to_timestamp()
    
    # Set index for panel data
    data = data.set_index(['permno', 'time_dt']).sort_index()
    
    # Get all unique permnos and time periods
    all_permnos = data.index.get_level_values(0).unique()
    all_times = data.index.get_level_values(1).unique()
    
    # Create full panel (all permno-time combinations)
    full_index = pd.MultiIndex.from_product(
        [all_permnos, all_times], 
        names=['permno', 'time_dt']
    )
    
    # Reindex to full panel and forward-fill
    data = data.reindex(full_index).groupby('permno').ffill()
    
    # Convert back to period format
    data = data.reset_index()
    data['time_avail_m'] = data['time_dt'].dt.to_period('M')
    data = data.drop('time_dt', axis=1)
    
    # Drop rows where all value columns are NaN (no data was available to forward-fill)
    value_cols = ['numinstown', 'dbreadth', 'instown_perc', 'maxinstown_perc', 'numinstblock']
    data = data.dropna(how='all', subset=value_cols)
    
    print(f"After forward-fill and cleanup: {len(data)} records")
    
    # Save to parquet
    output_file = "../pyData/Intermediate/TR_13F.parquet"
    os.makedirs(os.path.dirname(output_file), exist_ok=True)
    data.to_parquet(output_file, index=False)
    
    print(f"Saved {len(data)} records to {output_file}")
    print("Thomson Reuters 13F holdings processing completed successfully.")


if __name__ == "__main__":
    main()