# ABOUTME: Downloads CRSP distributions data (dividends, splits, etc.) from WRDS database
# ABOUTME: Deduplicates records and extracts distribution code digits for analysis
"""
Inputs:
- crsp.msedist (WRDS database table)

Outputs:
- ../pyData/Intermediate/CRSPdistributions.parquet

How to run: python3 H_CRSPDistributions.py
"""

import os
import sys
from sqlalchemy import create_engine
import pandas as pd
import numpy as np
from dotenv import load_dotenv

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from config import MAX_ROWS_DL
from utils.column_standardizer_yaml import standardize_columns

print("=" * 60, flush=True)
print("💰 H_CRSPDistributions.py - CRSP Dividends & Distributions", flush=True)
print("=" * 60, flush=True)

load_dotenv()

# Create database connection
engine = create_engine(
    f"postgresql://{os.getenv('WRDS_USERNAME')}:"
    f"{os.getenv('WRDS_PASSWORD')}"
    "@wrds-pgdata.wharton.upenn.edu:9737/wrds"
)

# Define SQL query to download distributions data
QUERY = """
SELECT d.permno, d.divamt, d.distcd, d.facshr, d.rcrddt, d.exdt, d.paydt
FROM crsp.msedist as d
"""

# Add row limit for debugging if configured
if MAX_ROWS_DL > 0:
    QUERY += f" LIMIT {MAX_ROWS_DL}"
    print(f"DEBUG MODE: Limiting to {MAX_ROWS_DL} rows", flush=True)

# Execute query and download data
dist_data = pd.read_sql_query(QUERY, engine)
engine.dispose()

# Ensure output directory exists
os.makedirs("../pyData/Intermediate", exist_ok=True)

print(f"Downloaded {len(dist_data)} distribution records")

# Convert date columns to standardized format before processing
datecols = ['rcrddt', 'exdt', 'paydt']
for col in datecols:
    if col in dist_data.columns:
        dist_data[col] = pd.to_datetime(dist_data[col])
        dist_data[col] = dist_data[col].dt.strftime('%Y-%m-%d')

# Remove duplicate records based on permno, dates, and distribution code
id_cols_plus = ['permno'] + datecols + ['distcd']
initial_count = len(dist_data)
dist_data = dist_data.sort_values(by=id_cols_plus)
dist_data = dist_data.drop_duplicates(subset=id_cols_plus, keep='first')
duplicates_removed = initial_count - len(dist_data)

if duplicates_removed > 0:
    print(f"Removed {duplicates_removed} duplicate records")

# Extract individual digits from distribution code for analysis
dist_data['distcd_str'] = (dist_data['distcd'].astype(str)
                           .str.zfill(4))  # Pad with zeros to ensure 4 digits

# Create separate columns for each digit of the distribution code
dist_data['cd1'] = pd.to_numeric(dist_data['distcd_str'].str[0],
                                 errors='coerce')
dist_data['cd2'] = pd.to_numeric(dist_data['distcd_str'].str[1],
                                 errors='coerce')
dist_data['cd3'] = pd.to_numeric(dist_data['distcd_str'].str[2],
                                 errors='coerce')
dist_data['cd4'] = pd.to_numeric(dist_data['distcd_str'].str[3],
                                 errors='coerce')

# Clean up temporary string column
dist_data = dist_data.drop('distcd_str', axis=1)

# Apply column standardization
dist_data = standardize_columns(dist_data, "CRSPdistributions")

# Save processed data to parquet file
dist_data.to_parquet("../pyData/Intermediate/CRSPdistributions.parquet")

print(f"CRSP Distributions data saved with {len(dist_data)} records",
      flush=True)

# Display summary of distribution codes
print("\nSample distribution codes:", flush=True)
sample_codes = dist_data['distcd'].value_counts().head(10)
print(sample_codes, flush=True)
print("=" * 60, flush=True)
print("✅ H_CRSPDistributions.py completed successfully", flush=True)
print("=" * 60, flush=True)