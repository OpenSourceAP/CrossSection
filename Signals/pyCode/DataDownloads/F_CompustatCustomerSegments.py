#!/usr/bin/env python3
"""
Compustat Customer Segments data download script - Python equivalent of F_CompustatCustomerSegments.do

Downloads Compustat customer segment data for customer momentum analysis.

To avoid errors in ZKR_CustomerSegments.py: we remove the row limit. 
Note to Claude: Do not put use MAX_ROWS_DL in this script, even when testing.
"""

import os
from sqlalchemy import create_engine
import pandas as pd
from dotenv import load_dotenv
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
# from config import MAX_ROWS_DL # do not use for this script
from utils.column_standardizer_yaml import standardize_columns

load_dotenv()

# Create SQLAlchemy engine for database connection
engine = create_engine(
    f"postgresql://{os.getenv('WRDS_USERNAME')}:{os.getenv('WRDS_PASSWORD')}@wrds-pgdata.wharton.upenn.edu:9737/wrds"
)

QUERY = """
SELECT a.*
FROM compseg.wrds_seg_customer as a
"""

# # Add row limit for debugging if configured (do not use for this script)
# if MAX_ROWS_DL > 0:
#     QUERY += f" LIMIT {MAX_ROWS_DL}"
#     print(f"DEBUG MODE: Limiting to {MAX_ROWS_DL} rows", flush=True)

customer_data = pd.read_sql_query(QUERY, engine)
engine.dispose()

print(f"Downloaded {len(customer_data)} customer segment records")

# Ensure directories exist
os.makedirs("../pyData/Intermediate", exist_ok=True)

# Rename srcdate to datadate (equivalent to rename srcdate datadate)
if 'srcdate' in customer_data.columns:
    customer_data = customer_data.rename(columns={'srcdate': 'datadate'})

# Convert gvkey to numeric format to match Stata
customer_data['gvkey'] = pd.to_numeric(customer_data['gvkey'], errors='coerce')

# Convert datadate to Stata string format to match expected output
if 'datadate' in customer_data.columns:
    customer_data['datadate'] = pd.to_datetime(customer_data['datadate'])
    # Convert to Stata date string format: "31may1980"
    customer_data['datadate'] = customer_data['datadate'].dt.strftime('%d%b%Y').str.lower()

# Apply column standardization
customer_data = standardize_columns(customer_data, 'CompustatSegmentDataCustomers')
# Save as CSV format to match Stata behavior (used for downstream R processing)
customer_data.to_csv("../pyData/Intermediate/CompustatSegmentDataCustomers.csv", index=False)

print(f"Compustat Customer Segments data saved with {len(customer_data)} records")

# Show summary information
if 'datadate' in customer_data.columns:
    print(f"Date range: {customer_data['datadate'].min()} to {customer_data['datadate'].max()}")

if 'gvkey' in customer_data.columns:
    print(f"Unique companies: {customer_data['gvkey'].nunique()}")

print("\nSample data:")
print(customer_data.head())
