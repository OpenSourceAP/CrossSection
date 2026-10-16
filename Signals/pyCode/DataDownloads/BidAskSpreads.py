# ABOUTME: Processes high-frequency bid-ask spread data from preprocessed CSV file
# ABOUTME: Converts yearm format to time_avail_m and creates hf_spread from espread_pct_mean
"""
Inputs:
- ../pyData/Prep/hf_monthly.csv (preprocessed high-frequency data with yearm and espread_pct_mean)

Outputs:
- ../pyData/Intermediate/hf_spread.parquet

How to run: from Signals/pyCode, run python3 DataDownloads/BidAskSpreads.py

Use the project Python environment at /opt/venv/projects/openap.
"""

import pandas as pd
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from config import DEBUG_MODE
from utils.debug_mode import get_debug_row_limit

DEBUG_ROWS = get_debug_row_limit("BidAskSpreads")

print("Processing high-frequency bid-ask spread data...")

# Read the prepared security-month spread estimates used by the spread signal.
input_file = "../pyData/Prep/hf_monthly.csv"

data = pd.read_csv(input_file)
print(f"Loaded {len(data)} records from {input_file}")

# Align the source YYYYMM labels with the monthly calendar used by other signals.
data['yearm'] = data['yearm'].astype(str)
data['y'] = data['yearm'].str[:4].astype(int)
data['m'] = data['yearm'].str[4:6].astype(int)

data['time_avail_m'] = pd.PeriodIndex.from_fields(
    year=data['y'], month=data['m'], freq='M'
)

# Expose the source effective-spread measure under the name expected by signals.
data['hf_spread'] = data['espread_pct_mean']

# Retain only security-months with both an identifier and a usable spread.
data = data[['permno', 'time_avail_m', 'hf_spread']].copy()
data = data.dropna()
print(f"After dropping missing values: {len(data)} records")

# Store security identifiers and months in the standard signal-data format.
data['permno'] = data['permno'].astype('int64')
data['time_avail_m'] = data['time_avail_m'].dt.to_timestamp()

# Apply debugging row limit if configured
if DEBUG_MODE:
    data = data.head(DEBUG_ROWS)
    print(f"DEBUG MODE: Limited to {DEBUG_ROWS} rows")

# Save monthly security-level spreads for downstream signals.
output_file = "../pyData/Intermediate/hf_spread.parquet"
data.to_parquet(output_file, index=False)

print(f"Saved {len(data)} records to {output_file}")
print("High-frequency bid-ask spread processing completed successfully.")
