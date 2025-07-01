#!/usr/bin/env python3
"""
CRSP-Compustat Linking Table download script.

Python equivalent of A_CCMLinkingTable.do

Downloads the CRSP-Compustat merged linking table from WRDS.

Note to Claude: Do not put use MAX_ROWS_DL in this script, even when testing.
"""

import os
import pandas as pd
from dotenv import load_dotenv
from sqlalchemy import create_engine
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
# from config import MAX_ROWS_DL # do not use for this script
from utils.column_standardizer_yaml import standardize_columns

print("=" * 60, flush=True)
print("🔗 A_CCMLinkingTable.py - CRSP-Compustat Linking Table", flush=True)
print("=" * 60, flush=True)

load_dotenv()

# Create SQLAlchemy engine for database connection
engine = create_engine(
    f"postgresql://{os.getenv('WRDS_USERNAME')}:{os.getenv('WRDS_PASSWORD')}@wrds-pgdata.wharton.upenn.edu:9737/wrds"
)

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

# Add row limit for debugging if configured (do not use for this script)
# if MAX_ROWS_DL > 0:
#     QUERY += f" LIMIT {MAX_ROWS_DL}"
#     print(f"DEBUG MODE: Limiting to {MAX_ROWS_DL} rows", flush=True)

ccm_data = pd.read_sql_query(QUERY, engine)
engine.dispose()

# Convert date columns to proper datetime format
ccm_data['linkdt'] = pd.to_datetime(ccm_data['linkdt'])
ccm_data['linkenddt'] = pd.to_datetime(ccm_data['linkenddt'])

# Ensure directories exist
os.makedirs("../pyData/Intermediate", exist_ok=True)

# Save CSV version with original column names (to match Stata format exactly)
ccm_csv_data = ccm_data.copy()
# Convert date columns to Stata string format for CSV
ccm_csv_data['linkdt'] = ccm_csv_data['linkdt'].dt.strftime('%d%b%Y').str.lower()
ccm_csv_data['linkenddt'] = ccm_csv_data['linkenddt'].dt.strftime('%d%b%Y').str.lower()
# Apply column standardization to ensure consistent data types
ccm_csv_data = standardize_columns(ccm_csv_data, 'CCMLinkingTable.csv')
ccm_csv_data.to_csv("../pyData/Intermediate/CCMLinkingTable.csv", index=False)

# Save parquet version with processed column names (for internal use)
ccm_parquet_data = ccm_data.copy()
# Rename columns for parquet version
ccm_parquet_data = ccm_parquet_data.rename(columns={
    'linkdt': 'timeLinkStart_d',
    'linkenddt': 'timeLinkEnd_d',
    'lpermno': 'permno'
})
# Convert NaN to empty strings to match Stata behavior
ccm_parquet_data['naics'] = ccm_parquet_data['naics'].fillna('')
ccm_parquet_data['cik'] = ccm_parquet_data['cik'].fillna('')
# Apply column standardization from 01_columns.yaml
ccm_parquet_data = standardize_columns(ccm_parquet_data, 'CCMLinkingTable')
ccm_parquet_data.to_parquet(
    "../pyData/Intermediate/CCMLinkingTable.parquet", index=False
)

print(f"CCM Linking Table downloaded with {len(ccm_data)} records", flush=True)
print(f"Unique companies (gvkey): {ccm_data['gvkey'].nunique()}", flush=True)
print(f"Unique stocks (lpermno): {ccm_data['lpermno'].nunique()}", flush=True)
print("=" * 60, flush=True)
print("✅ A_CCMLinkingTable.py completed successfully", flush=True)
print("=" * 60, flush=True)
