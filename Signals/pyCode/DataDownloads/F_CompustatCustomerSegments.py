# ABOUTME: Downloads Compustat customer segment data from WRDS for customer momentum analysis
# ABOUTME: Processes and standardizes data, converts dates to Stata format, saves as CSV for downstream processing
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
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from utils.column_standardizer_yaml import standardize_columns

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

# Create output directory
os.makedirs("../pyData/Intermediate", exist_ok=True)

# Data processing: rename srcdate to datadate
if 'srcdate' in customer_data.columns:
    customer_data = customer_data.rename(columns={'srcdate': 'datadate'})

# Convert gvkey to numeric format
customer_data['gvkey'] = pd.to_numeric(customer_data['gvkey'], errors='coerce')

# Convert datadate to Stata string format
if 'datadate' in customer_data.columns:
    customer_data['datadate'] = pd.to_datetime(customer_data['datadate'])
    customer_data['datadate'] = customer_data['datadate'].dt.strftime('%d%b%Y').str.lower()

# Apply column standardization and save data
customer_data = standardize_columns(customer_data, 'CompustatSegmentDataCustomers')
customer_data.to_csv("../pyData/Intermediate/CompustatSegmentDataCustomers.csv", index=False)

print(f"Compustat Customer Segments data saved with {len(customer_data)} records")

# Display summary information
if 'datadate' in customer_data.columns:
    print(f"Date range: {customer_data['datadate'].min()} to {customer_data['datadate'].max()}")

if 'gvkey' in customer_data.columns:
    print(f"Unique companies: {customer_data['gvkey'].nunique()}")

print("\nSample data:")
print(customer_data.head())
