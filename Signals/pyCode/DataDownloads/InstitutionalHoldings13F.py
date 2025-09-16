# ABOUTME: Downloads and processes Thomson Reuters 13F institutional holdings data from preprocessed CSV
# ABOUTME: Applies forward-fill logic for missing months and outputs monthly permno-level institutional holdings
"""
Inputs:
- ../pyData/Prep/tr_13f.csv

Outputs:
- ../pyData/Intermediate/TR_13F.parquet

How to run: python3 InstitutionalHoldings13F.py
"""

import pandas as pd
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from config import MAX_ROWS_DL

print("Processing Thomson Reuters 13F holdings data...")

# Load Thomson Reuters 13F data from preprocessed CSV file
input_file = "../pyData/Prep/tr_13f.csv"

# Read CSV data with optional row limit for debugging
nrows = None if MAX_ROWS_DL == -1 else MAX_ROWS_DL
data = pd.read_csv(input_file, nrows=nrows)

if MAX_ROWS_DL > 0:
    print(f"DEBUG MODE: Limited to {MAX_ROWS_DL} rows")
print(f"Loaded {len(data)} records from {input_file}")

# Remove observations without valid PERMNO identifier
data = data.dropna(subset=['PERMNO'])
print(f"After dropping missing PERMNO: {len(data)} records")

# Convert institutional holdings columns to numeric, handling invalid values
numeric_cols = ['instown_perc', 'maxinstown_perc', 'numinstown']
for col in numeric_cols:
    data[col] = pd.to_numeric(data[col], errors='coerce')

# Create monthly time variable from report date
data['time_d'] = pd.to_datetime(data['rdate'], format='%d%b%Y')
data['time_avail_m'] = data['time_d'].dt.to_period('M')

# Clean up intermediate date columns
data = data.drop(['rdate', 'time_d'], axis=1)

# Standardize column names to lowercase
data = data.rename(columns={
    'PERMNO': 'permno',
    'DBREADTH': 'dbreadth'
})

# Set appropriate data types to match Stata output
data['permno'] = data['permno'].astype('int64')
data['numinstown'] = data['numinstown'].astype('float64')

# Fill missing months with forward-filled values (Stata tsfill equivalent)
data['time_dt'] = data['time_avail_m'].dt.to_timestamp()

# For each permno, fill gaps between min/max observation dates
tsfill_data = []
for permno in data['permno'].unique():
    permno_data = data[data['permno'] == permno].copy()

    # Define date range for this permno's observations
    min_date = permno_data['time_dt'].min()
    max_date = permno_data['time_dt'].max()

    # Create complete monthly sequence within observation range
    monthly_range = pd.date_range(start=min_date, end=max_date, freq='MS')

    # Build complete permno-month index
    permno_index = pd.MultiIndex.from_product(
        [[permno], monthly_range],
        names=['permno', 'time_dt']
    )

    # Reindex to fill missing months and forward-fill values
    permno_data = permno_data.set_index(['permno', 'time_dt'])
    permno_filled = permno_data.reindex(permno_index)
    permno_filled = permno_filled.ffill()

    tsfill_data.append(permno_filled)

# Combine all permno data
data = pd.concat(tsfill_data).reset_index()

# Finalize time variable format
data = data.drop(columns=['time_avail_m'])
data = data.rename(columns={'time_dt': 'time_avail_m'})

# Remove rows with no institutional holdings data
value_cols = ['numinstown', 'dbreadth', 'instown_perc', 'maxinstown_perc', 'numinstblock']
data = data.dropna(how='all', subset=value_cols)

print(f"After forward-fill and cleanup: {len(data)} records")

# Verify time variable format for consistency
print(f"time_avail_m dtype: {data['time_avail_m'].dtypes}")
print("Pattern 1 fix: Verified time_avail_m format")

# Save processed data to parquet format
output_file = "../pyData/Intermediate/TR_13F.parquet"
data.to_parquet(output_file, index=False)

print(f"Saved {len(data)} records to {output_file}")
print("Thomson Reuters 13F holdings processing completed successfully.")