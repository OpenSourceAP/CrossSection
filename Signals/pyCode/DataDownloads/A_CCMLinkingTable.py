#!/usr/bin/env python3
"""
CRSP-Compustat Linking Table download script.

Python equivalent of A_CCMLinkingTable.do

Downloads the CRSP-Compustat merged linking table from WRDS.
"""

import os
import psycopg2
import pandas as pd
from dotenv import load_dotenv
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from config import MAX_ROWS_DL

print("=" * 60, flush=True)
print("🔗 A_CCMLinkingTable.py - CRSP-Compustat Linking Table", flush=True)
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

# Add row limit for debugging if configured
if MAX_ROWS_DL > 0:
    QUERY += f" LIMIT {MAX_ROWS_DL}"
    print(f"DEBUG MODE: Limiting to {MAX_ROWS_DL} rows", flush=True)

ccm_data = pd.read_sql_query(QUERY, conn)
conn.close()

# Convert date columns to proper datetime format
ccm_data['linkdt'] = pd.to_datetime(ccm_data['linkdt'])
ccm_data['linkenddt'] = pd.to_datetime(ccm_data['linkenddt'])

# Rename columns to match expected format from Stata
ccm_data = ccm_data.rename(columns={
    'linkdt': 'timeLinkStart_d',
    'linkenddt': 'timeLinkEnd_d',
    'lpermno': 'permno'
})

# Convert NaN to empty strings to match Stata behavior
ccm_data['naics'] = ccm_data['naics'].fillna('')
ccm_data['cik'] = ccm_data['cik'].fillna('')

# Ensure data type consistency
ccm_data['gvkey'] = ccm_data['gvkey'].astype(str)
ccm_data['naics'] = ccm_data['naics'].astype(str)
ccm_data['cik'] = ccm_data['cik'].astype(str)

# Ensure directories exist
os.makedirs("../pyData/Intermediate", exist_ok=True)

# Save the data
ccm_data.to_csv("../pyData/Intermediate/CCMLinkingTable.csv", index=False)
ccm_data.to_parquet(
    "../pyData/Intermediate/CCMLinkingTable.parquet", index=False
)

print(f"CCM Linking Table downloaded with {len(ccm_data)} records", flush=True)
print(f"Unique companies (gvkey): {ccm_data['gvkey'].nunique()}", flush=True)
print(f"Unique stocks (permno): {ccm_data['permno'].nunique()}", flush=True)
print("=" * 60, flush=True)
print("✅ A_CCMLinkingTable.py completed successfully", flush=True)
print("=" * 60, flush=True)
