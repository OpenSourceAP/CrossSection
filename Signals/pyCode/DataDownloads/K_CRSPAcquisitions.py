#!/usr/bin/env python3
"""
CRSP Acquisitions data download script - Python equivalent of K_CRSPAcquisitions.do

Downloads CRSP distributions data and processes spinoff companies.
Creates a list of permnos that were created in spinoffs.
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
SELECT a.permno, a.distcd, a.exdt, a.acperm
FROM crsp.msedist as a
"""

acq_data = pd.read_sql_query(QUERY, conn)
conn.close()

print(f"Downloaded {len(acq_data)} distribution records")

# Ensure directories exist
os.makedirs("../Data/Intermediate", exist_ok=True)

# Keep only records where acperm > 999 and not missing
# (equivalent to keep if acperm >999 & acperm <.)
initial_count = len(acq_data)
acq_data = acq_data[(acq_data['acperm'] > 999) & acq_data['acperm'].notna()]
print(f"Filtered to {len(acq_data)} records with acperm > 999")

# Remove records with missing exdt (equivalent to drop if missing(time_d))
acq_data = acq_data.dropna(subset=['exdt'])
print(f"After removing missing exdt: {len(acq_data)} records")

# Rename exdt to time_d and convert to datetime
acq_data = acq_data.rename(columns={'exdt': 'time_d'})
acq_data['time_d'] = pd.to_datetime(acq_data['time_d'])

# Create monthly availability date (equivalent to gen time_avail_m = mofd(time_d))
acq_data['time_avail_m'] = acq_data['time_d'].dt.to_period('M')

# Drop time_d as in original Stata code
acq_data = acq_data.drop('time_d', axis=1)

# According to CRSP documentation:
# http://www.crsp.com/products/documentation/distribution-codes
# distcd identifies true spinoffs using distcd >= 3762 & distcd <= 3764
# But MP don't use it, and it results in a large share of months with no spinoffs.
# So we proceed without the distcd filter

# Turn into list of permnos which were created in spinoffs
# (equivalent to gen SpinoffCo = 1; drop permno; rename acperm permno)
acq_data['SpinoffCo'] = 1
acq_data = acq_data.drop('permno', axis=1)
acq_data = acq_data.rename(columns={'acperm': 'permno'})

# Keep only necessary columns
acq_data = acq_data[['permno', 'SpinoffCo']]

# Remove duplicates (equivalent to duplicates drop)
initial_count = len(acq_data)
acq_data = acq_data.drop_duplicates()
duplicates_removed = initial_count - len(acq_data)
print(f"Removed {duplicates_removed} duplicate records")

# Save the data
acq_data.to_pickle("../Data/Intermediate/m_CRSPAcquisitions.pkl")

print(f"CRSP Acquisitions data saved with {len(acq_data)} unique spinoff companies")

# Show sample data
print("\nSample data:")
print(acq_data.head())

# Show some statistics
print(f"\nUnique spinoff companies: {acq_data['permno'].nunique()}")
print(f"Total records: {len(acq_data)}")