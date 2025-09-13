# ABOUTME: Downloads and processes Corwin-Schultz bid-ask spread data from preprocessed CSV
# ABOUTME: Converts monthly data to permno-time format and saves as parquet file
"""
Inputs:
- ../pyData/Prep/corwin_schultz_spread.csv

Outputs:
- ../pyData/Intermediate/BAspreadsCorwin.parquet

How to run: python3 ZD_CorwinSchultz.py
"""

import os
import pandas as pd
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from config import MAX_ROWS_DL
from utils.column_standardizer_yaml import standardize_columns


def main():
    print("Processing Corwin-Schultz bid-ask spread data...")
    
    # Load preprocessed Corwin-Schultz spread data from CSV
    input_file = "../pyData/Prep/corwin_schultz_spread.csv"
    
    if not os.path.exists(input_file):
        raise FileNotFoundError(f"Input file not found: {input_file}")
    
    data = pd.read_csv(input_file)
    print(f"Loaded {len(data)} records from {input_file}")
    
    # Convert month string (YYYYMM format) to time_avail_m period
    data['month'] = data['month'].astype(str)
    data['y'] = data['month'].str[:4].astype(int)
    data['m'] = data['month'].str[4:6].astype(int)
    data['time_avail_m'] = pd.PeriodIndex.from_fields(
        year=data['y'], month=data['m'], freq='M'
    )
    data = data.drop(['y', 'm', 'month'], axis=1)
    
    # Clean and standardize data
    data = data.dropna(subset=['PERMNO'])
    print(f"After dropping missing PERMNO: {len(data)} records")
    
    data = data.rename(columns={
        'PERMNO': 'permno',
        'hlspread': 'BidAskSpread'
    })
    data['permno'] = data['permno'].astype('int64')
    
    # Convert period to timestamp for parquet compatibility
    data['time_avail_m'] = data['time_avail_m'].dt.to_timestamp()
    
    # Apply debugging row limit if configured
    if MAX_ROWS_DL > 0:
        data = data.head(MAX_ROWS_DL)
        print(f"DEBUG MODE: Limited to {MAX_ROWS_DL} rows")

    # Standardize columns and save to parquet
    output_file = "../pyData/Intermediate/BAspreadsCorwin.parquet"
    os.makedirs(os.path.dirname(output_file), exist_ok=True)
    data = standardize_columns(data, 'BAspreadsCorwin')
    data.to_parquet(output_file, index=False)
    
    print(f"Saved {len(data)} records to {output_file}")
    print("Corwin-Schultz bid-ask spread processing completed successfully.")


if __name__ == "__main__":
    main()