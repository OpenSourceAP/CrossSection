#!/usr/bin/env python3
"""
Compustat Customer Segments data download script - Python equivalent of F_CompustatCustomerSegments.do

Downloads Compustat customer segment data for customer momentum analysis.
"""

import os
import psycopg2
import pandas as pd
from dotenv import load_dotenv

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

customer_data = pd.read_sql_query(QUERY, conn)
conn.close()

print(f"Downloaded {len(customer_data)} customer segment records")

# Ensure directories exist
os.makedirs("../Data/Intermediate", exist_ok=True)

# Rename srcdate to datadate (equivalent to rename srcdate datadate)
if 'srcdate' in customer_data.columns:
    customer_data = customer_data.rename(columns={'srcdate': 'datadate'})

# Save as both pickle and CSV (CSV needed for R processing)
customer_data.to_pickle("../Data/Intermediate/CompustatSegmentDataCustomers.pkl")
customer_data.to_csv("../Data/Intermediate/CompustatSegmentDataCustomers.csv", index=False)

print(f"Compustat Customer Segments data saved with {len(customer_data)} records")

# Show summary information
if 'datadate' in customer_data.columns:
    customer_data['datadate'] = pd.to_datetime(customer_data['datadate'])
    print(f"Date range: {customer_data['datadate'].min().strftime('%Y-%m-%d')} to {customer_data['datadate'].max().strftime('%Y-%m-%d')}")

if 'gvkey' in customer_data.columns:
    print(f"Unique companies: {customer_data['gvkey'].nunique()}")

print("\nSample data:")
print(customer_data.head())