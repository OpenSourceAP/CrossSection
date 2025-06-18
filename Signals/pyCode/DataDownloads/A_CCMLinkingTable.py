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

ccm_data = pd.read_sql_query(QUERY, conn)
conn.close()

# Rename columns to match expected format from Stata
ccm_data = ccm_data.rename(columns={
    'linkdt': 'timeLinkStart_d',
    'linkenddt': 'timeLinkEnd_d',
    'lpermno': 'permno'
})

# Ensure directories exist
os.makedirs("../pyData/Intermediate", exist_ok=True)

# Save the data
ccm_data.to_csv("../pyData/Intermediate/CCMLinkingTable.csv", index=False)
ccm_data.to_parquet(
    "../pyData/Intermediate/CCMLinkingTable.parquet", index=False
)

print("CCM Linking Table downloaded with {len(ccm_data)} records", flush=True)
print("Unique companies (gvkey): {ccm_data['gvkey'].nunique()}", flush=True)
print("Unique stocks (permno): {ccm_data['permno'].nunique()}", flush=True)
print("=" * 60, flush=True)
print("✅ A_CCMLinkingTable.py completed successfully", flush=True)
print("=" * 60, flush=True)
