# ABOUTME: Downloads Compustat customer segment data from WRDS for customer momentum analysis
# ABOUTME: Processes data, converts dates to Stata format, saves as CSV for downstream processing
"""
Inputs:
- compseg.wrds_seg_customer (WRDS database)

Outputs:
- ../pyData/Intermediate/CompustatSegmentDataCustomers.csv

How to run: python F_CompustatCustomerSegments.py
"""

import os
from sqlalchemy import create_engine
import pandas as pd
from dotenv import load_dotenv

load_dotenv()

# Create database connection to WRDS
engine = create_engine(
    f"postgresql://{os.getenv('WRDS_USERNAME')}:{os.getenv('WRDS_PASSWORD')}@wrds-pgdata.wharton.upenn.edu:9737/wrds"
)

# Query to download all customer segment data
QUERY = """
SELECT a.*
FROM compseg.wrds_seg_customer as a
"""

# Execute query and download data
customer_data = pd.read_sql_query(QUERY, engine)
engine.dispose()

print(f"Downloaded {len(customer_data)} customer segment records")

# Data processing: rename srcdate to datadate
customer_data = customer_data.rename(columns={'srcdate': 'datadate'})

# Convert gvkey to numeric format
customer_data['gvkey'] = pd.to_numeric(customer_data['gvkey'])

# Convert datadate to Stata string format
customer_data['datadate'] = pd.to_datetime(customer_data['datadate'])
customer_data['datadate'] = customer_data['datadate'].dt.strftime('%d%b%Y').str.lower()

# Save data
customer_data.to_csv("../pyData/Intermediate/CompustatSegmentDataCustomers.csv", index=False)

print(f"Compustat Customer Segments data saved with {len(customer_data)} records")

# Display summary information
print(f"Date range: {customer_data['datadate'].min()} to {customer_data['datadate'].max()}")
print(f"Unique companies: {customer_data['gvkey'].nunique()}")

print("\nSample data:")
print(customer_data.head())
