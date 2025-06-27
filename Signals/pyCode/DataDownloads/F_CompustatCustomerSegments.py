#!/usr/bin/env python3
"""
Compustat Customer Segments data download script - Python equivalent of F_CompustatCustomerSegments.do

Downloads Compustat customer segment data for customer momentum analysis.
"""

import os
import psycopg2
import pandas as pd
from dotenv import load_dotenv
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from config import MAX_ROWS_DL

load_dotenv()

conn = psycopg2.connect(
    host="wrds-pgdata.wharton.upenn.edu",
    port=9737,
    database="wrds",
    user=os.getenv("WRDS_USERNAME"),
    password=os.getenv("WRDS_PASSWORD")
)

QUERY = """
SELECT a.*
FROM compseg.wrds_seg_customer as a
"""

# Add row limit for debugging if configured
if MAX_ROWS_DL > 0:
    QUERY += f" LIMIT {MAX_ROWS_DL}"
    print(f"DEBUG MODE: Limiting to {MAX_ROWS_DL} rows", flush=True)

customer_data = pd.read_sql_query(QUERY, conn)
conn.close()

print(f"Downloaded {len(customer_data)} customer segment records")

# Ensure directories exist
os.makedirs("../pyData/Intermediate", exist_ok=True)

# Rename srcdate to datadate (equivalent to rename srcdate datadate)
if 'srcdate' in customer_data.columns:
    customer_data = customer_data.rename(columns={'srcdate': 'datadate'})

# Convert gvkey to numeric format to match Stata
customer_data['gvkey'] = pd.to_numeric(customer_data['gvkey'], errors='coerce')

# Convert datadate to datetime format to match Stata before saving
if 'datadate' in customer_data.columns:
    customer_data['datadate'] = pd.to_datetime(customer_data['datadate'])

# Save as parquet format
customer_data.to_parquet("../pyData/Intermediate/CompustatSegmentDataCustomers.parquet")

print(f"Compustat Customer Segments data saved with {len(customer_data)} records")

# Show summary information
if 'datadate' in customer_data.columns:
    print(f"Date range: {customer_data['datadate'].min().strftime('%Y-%m-%d')} to {customer_data['datadate'].max().strftime('%Y-%m-%d')}")

if 'gvkey' in customer_data.columns:
    print(f"Unique companies: {customer_data['gvkey'].nunique()}")

print("\nSample data:")
print(customer_data.head())
