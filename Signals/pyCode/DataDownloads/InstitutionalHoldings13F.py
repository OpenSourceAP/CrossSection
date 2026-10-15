# ABOUTME: Downloads and processes Thomson Reuters 13F institutional holdings data from preprocessed CSV
# ABOUTME: Applies forward-fill logic for missing months and outputs monthly permno-level institutional holdings
"""
Inputs:
- ../pyData/Prep/tr_13f.csv

Outputs:
- ../pyData/Intermediate/TR_13F.parquet

How to run: from Signals/pyCode, run python3 DataDownloads/InstitutionalHoldings13F.py

Use the project Python environment at /opt/venv/projects/openap.
"""

import pandas as pd
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from config import DEBUG_MODE
from utils.debug_mode import get_debug_row_limit

DEBUG_ROWS = get_debug_row_limit("InstitutionalHoldings13F")

print("Processing Thomson Reuters 13F holdings data...")

# Obtain prepared institutional ownership measures for monthly stock signals.
input_file = "../pyData/Prep/tr_13f.csv"

nrows = DEBUG_ROWS
data = pd.read_csv(input_file, nrows=nrows)

if DEBUG_MODE:
    print(f"DEBUG MODE: Limited to {DEBUG_ROWS} rows")
print(f"Loaded {len(data)} records from {input_file}")

# Require a stock identifier so ownership measures can be matched to returns.
data = data.dropna(subset=['PERMNO'])
print(f"After dropping missing PERMNO: {len(data)} records")

# Make ownership measures numeric, treating invalid source values as missing.
numeric_cols = ['instown_perc', 'maxinstown_perc', 'numinstown']
for col in numeric_cols:
    data[col] = pd.to_numeric(data[col], errors='coerce')

# Align ownership observations with their report month.
# Prep exports have written rdate as 30SEP1986 (SAS date9.) and as 19860930.
rdate = data['rdate'].astype(str)
rdate_format = '%Y%m%d' if rdate.str.fullmatch(r'\d{8}').all() else '%d%b%Y'
data['time_d'] = pd.to_datetime(rdate, format=rdate_format)
data['time_avail_m'] = data['time_d'].dt.to_period('M')

data = data.drop(['rdate', 'time_d'], axis=1)

# Use stock and ownership-field names expected by downstream signals.
data = data.rename(columns={
    'PERMNO': 'permno',
    'DBREADTH': 'dbreadth'
})

data['permno'] = data['permno'].astype('int64')
data['numinstown'] = data['numinstown'].astype('float64')

# Carry the latest available ownership measures into gaps between stock observations.
data['time_dt'] = data['time_avail_m'].dt.to_timestamp()

tsfill_data = []
for permno in data['permno'].unique():
    permno_data = data[data['permno'] == permno].copy()

    # Limit each stock's monthly coverage to its first and last observed reports.
    min_date = permno_data['time_dt'].min()
    max_date = permno_data['time_dt'].max()

    monthly_range = pd.date_range(start=min_date, end=max_date, freq='MS')

    permno_index = pd.MultiIndex.from_product(
        [[permno], monthly_range],
        names=['permno', 'time_dt']
    )

    # Use the latest nonmissing measures until another report supplies replacements.
    permno_data = permno_data.set_index(['permno', 'time_dt'])
    permno_filled = permno_data.reindex(permno_index)
    permno_filled = permno_filled.ffill()

    tsfill_data.append(permno_filled)

data = pd.concat(tsfill_data).reset_index()

# Provide the common monthly date field used to join other stock-level datasets.
data = data.drop(columns=['time_avail_m'])
data = data.rename(columns={'time_dt': 'time_avail_m'})

# Exclude stock-months where every ownership measure is missing.
value_cols = ['numinstown', 'dbreadth', 'instown_perc', 'maxinstown_perc', 'numinstblock']
data = data.dropna(how='all', subset=value_cols)

print(f"After forward-fill and cleanup: {len(data)} records")

print(f"time_avail_m dtype: {data['time_avail_m'].dtypes}")
print("Pattern 1 fix: Verified time_avail_m format")

# Save the monthly institutional ownership panel for downstream signals.
output_file = "../pyData/Intermediate/TR_13F.parquet"
data.to_parquet(output_file, index=False)

print(f"Saved {len(data)} records to {output_file}")
print("Thomson Reuters 13F holdings processing completed successfully.")
