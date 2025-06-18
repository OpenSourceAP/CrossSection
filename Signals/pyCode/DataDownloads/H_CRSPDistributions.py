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

dist_data = pd.read_sql_query(QUERY, conn)
conn.close()

# Ensure directories exist
os.makedirs("../pyData/Intermediate", exist_ok=True)

print("Downloaded {len(dist_data)} distribution records")

# Remove duplicates (equivalent to bysort permno distcd paydt: keep if _n == 1)
# These are data errors, e.g. see permno 93338 or 93223
initial_count = len(dist_data)
dist_data = dist_data.drop_duplicates(subset=['permno', 'distcd', 'paydt'], keep='first')
duplicates_removed = initial_count - len(dist_data)

if duplicates_removed > 0:
    print("Removed {duplicates_removed} duplicate records")

# For convenience, extract components of distribution code
# Convert distcd to string and extract individual digits
dist_data['distcd_str'] = dist_data['distcd'].astype(str).str.zfill(4)  # Pad with zeros to ensure 4 digits

# Extract each digit as separate columns
dist_data['cd1'] = pd.to_numeric(dist_data['distcd_str'].str[0], errors='coerce')
dist_data['cd2'] = pd.to_numeric(dist_data['distcd_str'].str[1], errors='coerce')
dist_data['cd3'] = pd.to_numeric(dist_data['distcd_str'].str[2], errors='coerce')
dist_data['cd4'] = pd.to_numeric(dist_data['distcd_str'].str[3], errors='coerce')

# Drop the temporary string column
dist_data = dist_data.drop('distcd_str', axis=1)

# Save the data
dist_data.to_pickle("../pyData/Intermediate/CRSPdistributions.pkl")

print("CRSP Distributions data saved with {len(dist_data)} records", flush=True)

# Show sample of distribution codes
print("\nSample distribution codes:", flush=True)
sample_codes = dist_data['distcd'].value_counts().head(10)
print(sample_codes, flush=True)
print("=" * 60, flush=True)
print("✅ H_CRSPDistributions.py completed successfully", flush=True)
print("=" * 60, flush=True)
