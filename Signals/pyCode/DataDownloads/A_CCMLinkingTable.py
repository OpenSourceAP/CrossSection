# ABOUTME: Downloads CRSP-Compustat linking table with company and stock identifiers
# ABOUTME: Filters for primary links (LC/LU + P/C) and converts to CSV/Parquet formats
"""
Inputs:
- comp.names (company master file)
- crsp.ccmxpf_lnkhist (CRSP-Compustat link history)

Outputs:
- ../pyData/Intermediate/CCMLinkingTable.parquet

How to run: python3 A_CCMLinkingTable.py
"""

import os
import pandas as pd
from dotenv import load_dotenv
from sqlalchemy import create_engine
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from utils.column_standardizer_yaml import standardize_columns

# Display script header
print("=" * 60, flush=True)
print("🔗 A_CCMLinkingTable.py - CRSP-Compustat Linking Table", flush=True)
print("=" * 60, flush=True)

# Load environment variables for database credentials
load_dotenv()

# Create database connection to WRDS
engine = create_engine(
    f"postgresql://{os.getenv('WRDS_USERNAME')}:{os.getenv('WRDS_PASSWORD')}@wrds-pgdata.wharton.upenn.edu:9737/wrds"
)

# SQL query to download CRSP-Compustat linking table with primary links only
QUERY = """
SELECT a.gvkey, a.conm, a.tic, a.cusip, a.cik, a.sic, a.naics,
       b.linkprim, b.linktype, b.liid, b.lpermno, b.lpermco,
       b.linkdt, b.linkenddt
FROM comp.names as a
INNER JOIN crsp.ccmxpf_lnkhist as b
ON a.gvkey = b.gvkey
WHERE b.linktype in ('LC', 'LU')
AND b.linkprim in ('P', 'C')
ORDER BY a.gvkey
"""

# Execute query to download linking table data
ccm_data = pd.read_sql_query(QUERY, engine)
engine.dispose()

# Convert date columns to datetime format
ccm_data['linkdt'] = pd.to_datetime(ccm_data['linkdt'])
ccm_data['linkenddt'] = pd.to_datetime(ccm_data['linkenddt'])

# Create output directory
os.makedirs("../pyData/Intermediate", exist_ok=True)

# Prepare and save Parquet version with renamed columns
ccm_parquet_data = ccm_data.copy()
ccm_parquet_data = ccm_parquet_data.rename(columns={
    'linkdt': 'timeLinkStart_d',
    'linkenddt': 'timeLinkEnd_d',
    'lpermno': 'permno'
})
ccm_parquet_data['naics'] = ccm_parquet_data['naics'].fillna('')
ccm_parquet_data['cik'] = ccm_parquet_data['cik'].fillna('')
ccm_parquet_data = standardize_columns(ccm_parquet_data, 'CCMLinkingTable')
ccm_parquet_data.to_parquet("../pyData/Intermediate/CCMLinkingTable.parquet", index=False)

# Display summary statistics

print(f"CCM Linking Table downloaded with {len(ccm_data)} records", flush=True)
print(f"Unique companies (gvkey): {ccm_data['gvkey'].nunique()}", flush=True)
print(f"Unique stocks (lpermno): {ccm_data['lpermno'].nunique()}", flush=True)
print("=" * 60, flush=True)
print("✅ A_CCMLinkingTable.py completed successfully", flush=True)
print("=" * 60, flush=True)
