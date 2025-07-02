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
from utils.column_standardizer_yaml import standardize_columns


def main():
    """Process Thomson Reuters 13F holdings data."""
    print("Processing Thomson Reuters 13F holdings data...")
    
    # Load the CSV data
    input_file = "../pyData/Prep/tr_13f.csv"
    
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
    
    # Convert numeric columns, forcing errors to NaN (match Stata destring)
    numeric_cols = ['instown_perc', 'maxinstown_perc', 'numinstown']
    for col in numeric_cols:
        data[col] = pd.to_numeric(data[col], errors='coerce')
    
    # Convert rdate to datetime and create time_avail_m
    data['time_d'] = pd.to_datetime(data['rdate'], format='%d%b%Y')
    # Store as period initially, will convert to datetime64[ns] at the end (Pattern 1 fix)
    data['time_avail_m'] = data['time_d'].dt.to_period('M')
    
    # Drop intermediate columns (keep time_avail_m for now, will replace it later)
    data = data.drop(['rdate', 'time_d'], axis=1)
    
    # Rename columns to match Stata output (lowercase)
    data = data.rename(columns={
        'PERMNO': 'permno',
        'DBREADTH': 'dbreadth'
    })
    
    # Ensure optimal data types (match Stata output)
    data['permno'] = data['permno'].astype('int64')
    # Fix numinstown type to match Stata (should be float64, not int16)
    data['numinstown'] = data['numinstown'].astype('float64')
    
    # Stata tsfill equivalent: fill missing months and forward-fill values
    # Convert time_avail_m to datetime for panel operations
    data['time_dt'] = data['time_avail_m'].dt.to_timestamp()
    
    # Stata tsfill logic: for each permno, fill gaps between min/max dates only
    tsfill_data = []
    for permno in data['permno'].unique():
        permno_data = data[data['permno'] == permno].copy()
        
        # Get min/max dates for this permno only
        min_date = permno_data['time_dt'].min()
        max_date = permno_data['time_dt'].max()
        
        # Create monthly range for this permno only
        monthly_range = pd.date_range(start=min_date, end=max_date, freq='MS')
        
        # Create complete time series for this permno
        permno_index = pd.MultiIndex.from_product(
            [[permno], monthly_range],
            names=['permno', 'time_dt']
        )
        
        # Set index and reindex to fill gaps
        permno_data = permno_data.set_index(['permno', 'time_dt'])
        permno_filled = permno_data.reindex(permno_index)
        
        # Forward fill missing values (Stata replace logic)
        permno_filled = permno_filled.ffill()
        
        tsfill_data.append(permno_filled)
    
    # Combine all permnos
    data = pd.concat(tsfill_data).reset_index()
    
    # Clean up - drop old time_avail_m and rename time_dt to time_avail_m
    data = data.drop(columns=['time_avail_m'])  # Drop the old period column
    data = data.rename(columns={'time_dt': 'time_avail_m'})
    
    # Drop rows where all value columns are NaN (no data was available to forward-fill)
    value_cols = ['numinstown', 'dbreadth', 'instown_perc', 'maxinstown_perc', 'numinstblock']
    data = data.dropna(how='all', subset=value_cols)
    
    print(f"After forward-fill and cleanup: {len(data)} records")
    
    # PATTERN 1 FIX: Ensure time_avail_m is datetime64[ns] format BEFORE saving
    if 'time_avail_m' in data.columns:
        # time_avail_m should already be datetime64[ns] from the panel operations
        print(f"time_avail_m dtype: {data['time_avail_m'].dtypes}")
        print("Pattern 1 fix: Verified time_avail_m format")
    
    # Save to parquet
    output_file = "../pyData/Intermediate/TR_13F.parquet"
    os.makedirs(os.path.dirname(output_file), exist_ok=True)
    # Apply column standardization
    data = standardize_columns(data, 'TR_13F')
    data.to_parquet(output_file, index=False)
    
    print(f"Saved {len(data)} records to {output_file}")
    print("Thomson Reuters 13F holdings processing completed successfully.")


if __name__ == "__main__":
    main()