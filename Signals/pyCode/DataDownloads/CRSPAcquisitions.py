# ABOUTME: Downloads CRSP distributions data to identify companies created in spinoffs
# ABOUTME: Filters for acquisition permnos and creates a list of spinoff companies
"""
Inputs:
- crsp.msedist (CRSP distributions data)

Outputs:
- ../pyData/Intermediate/m_CRSPAcquisitions.parquet

How to run: python3 CRSPAcquisitions.py
"""

import os
from sqlalchemy import create_engine
import pandas as pd
from dotenv import load_dotenv
import sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from config import DEBUG_MODE
from utils.debug_mode import log_selection, sql_date_window

load_dotenv()

engine = create_engine(
    f"postgresql://{os.getenv('WRDS_USERNAME')}:{os.getenv('WRDS_PASSWORD')}@wrds-pgdata.wharton.upenn.edu:9737/wrds"
)

QUERY = """
SELECT a.permno, a.distcd, a.exdt, a.acperm
FROM crsp.msedist as a
"""

log_selection("CRSPAcquisitions")
predicate, query_params = sql_date_window("a.exdt", "events")
QUERY += f" WHERE {predicate}"

acq_data = pd.read_sql_query(QUERY, engine, params=query_params)
if DEBUG_MODE:
    missing_exdt = pd.read_sql_query(
        "SELECT COUNT(*) AS missing_exdt FROM crsp.msedist WHERE exdt IS NULL",
        engine,
    ).iloc[0]["missing_exdt"]
    print(f"Source records with missing exdt (outside debug window): {missing_exdt}", flush=True)
engine.dispose()

print(f"Downloaded {len(acq_data)} distribution records")


initial_count = len(acq_data)
acq_data = acq_data[(acq_data['acperm'] > 999) & acq_data['acperm'].notna()]
print(f"Filtered to {len(acq_data)} records with acperm > 999")

acq_data = acq_data.dropna(subset=['exdt'])
print(f"After removing missing exdt: {len(acq_data)} records")

acq_data = acq_data.rename(columns={'exdt': 'time_d'})
acq_data['time_d'] = pd.to_datetime(acq_data['time_d'])

acq_data['time_avail_m'] = acq_data['time_d'].dt.to_period('M').dt.to_timestamp()

acq_data = acq_data.drop('time_d', axis=1)

acq_data['SpinoffCo'] = 1
acq_data = acq_data.drop('permno', axis=1)
acq_data = acq_data.rename(columns={'acperm': 'permno'})

acq_data = acq_data[['permno', 'SpinoffCo']]

initial_count = len(acq_data)
acq_data = acq_data.drop_duplicates()
duplicates_removed = initial_count - len(acq_data)
print(f"Removed {duplicates_removed} duplicate records")


acq_data.to_parquet("../pyData/Intermediate/m_CRSPAcquisitions.parquet", index=False)

print(f"CRSP Acquisitions data saved with {len(acq_data)} unique spinoff companies")

print("\nSample data:")
print(acq_data.head())

print(f"\nUnique spinoff companies: {acq_data['permno'].nunique()}")
print(f"Total records: {len(acq_data)}")
