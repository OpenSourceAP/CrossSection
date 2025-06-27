#!/usr/bin/env python3
"""
CRSP Distributions data download script - Python equivalent of H_CRSPDistributions.do

Downloads CRSP distributions data (dividends, splits, etc.)
http://www.crsp.org/products/documentation/distribution-codes
"""

import os
import psycopg2
import pandas as pd
import numpy as np
from dotenv import load_dotenv
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from config import MAX_ROWS_DL

print("=" * 60, flush=True)
print("💰 H_CRSPDistributions.py - CRSP Dividends & Distributions", flush=True)
print("=" * 60, flush=True)

load_dotenv()

conn = psycopg2.connect(
    host="wrds-pgdata.wharton.upenn.edu",
    port=9737,
    database="wrds",
    user=os.getenv("WRDS_USERNAME"),
    password=os.getenv("WRDS_PASSWORD")
)

QUERY = """
SELECT d.permno, d.divamt, d.distcd, d.facshr, d.rcrddt, d.exdt, d.paydt
FROM crsp.msedist as d
"""

# Add row limit for debugging if configured
if MAX_ROWS_DL > 0:
    QUERY += f" LIMIT {MAX_ROWS_DL}"
    print(f"DEBUG MODE: Limiting to {MAX_ROWS_DL} rows", flush=True)

dist_data = pd.read_sql_query(QUERY, conn)
conn.close()

# Ensure directories exist
os.makedirs("../pyData/Intermediate", exist_ok=True)

print(f"Downloaded {len(dist_data)} distribution records")

# Replicate Stata's exact duplicate removal logic:
# "bysort permno distcd paydt: keep if _n == 1" 
# This means: sort by permno distcd paydt, then keep first record in each group
initial_count = len(dist_data)

# Sort first (this is what bysort does), then remove duplicates
# Stata's "bysort permno distcd paydt" sorts by exactly these 3 columns
# For tied records, Stata may use the original dataset order as tie-breaker
# We need to replicate this by using a stable sort that preserves original order for ties
dist_data = dist_data.sort_values(['permno', 'distcd', 'paydt'], kind='stable').reset_index(drop=True)
dist_data = dist_data.drop_duplicates(subset=['permno', 'distcd', 'paydt'], keep='first')
duplicates_removed = initial_count - len(dist_data)

if duplicates_removed > 0:
    print(f"Removed {duplicates_removed} duplicate records")

# For convenience, extract components of distribution code
# IMPORTANT: In Stata, the tostring distcd happens AFTER deduplication
# So we need to work with the numeric distcd for digit extraction
# Convert distcd to string and extract individual digits
dist_data['distcd_str'] = dist_data['distcd'].astype(str).str.zfill(4)  # Pad with zeros to ensure 4 digits

# Extract each digit as separate columns
dist_data['cd1'] = pd.to_numeric(dist_data['distcd_str'].str[0], errors='coerce')
dist_data['cd2'] = pd.to_numeric(dist_data['distcd_str'].str[1], errors='coerce')
dist_data['cd3'] = pd.to_numeric(dist_data['distcd_str'].str[2], errors='coerce')
dist_data['cd4'] = pd.to_numeric(dist_data['distcd_str'].str[3], errors='coerce')

# Drop the temporary string column
dist_data = dist_data.drop('distcd_str', axis=1)

# Convert date columns to datetime format to match Stata expectations
date_columns = ['rcrddt', 'exdt', 'paydt']
for col in date_columns:
    if col in dist_data.columns:
        dist_data[col] = pd.to_datetime(dist_data[col])

# Standardize columns to match DTA file
from utils.column_standardizer import standardize_against_dta
dist_data = standardize_against_dta(
    dist_data, 
    "../Data/Intermediate/CRSPdistributions.dta",
    "CRSPdistributions"
)

# Save the data
dist_data.to_parquet("../pyData/Intermediate/CRSPdistributions.parquet")

print(f"CRSP Distributions data saved with {len(dist_data)} records", flush=True)

# Show sample of distribution codes
print("\nSample distribution codes:", flush=True)
sample_codes = dist_data['distcd'].value_counts().head(10)
print(sample_codes, flush=True)
print("=" * 60, flush=True)
print("✅ H_CRSPDistributions.py completed successfully", flush=True)
print("=" * 60, flush=True)
