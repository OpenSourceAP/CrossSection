#!/usr/bin/env python3
"""
ABOUTME: CRSP-Compustat Linking Table download script
ABOUTME: Downloads the CRSP-Compustat merged linking table from WRDS

Note to Claude: Do not put use MAX_ROWS_DL in this script, even when testing.
"""

import os
import pandas as pd
from dotenv import load_dotenv
from sqlalchemy import create_engine
import sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from utils.column_standardizer_yaml import standardize_columns

print("=" * 60, flush=True)
print("🔗 A_CCMLinkingTable.py - CRSP-Compustat Linking Table", flush=True)
print("=" * 60, flush=True)

load_dotenv()

engine = create_engine(
    f"postgresql://{os.getenv('WRDS_USERNAME')}:{os.getenv('WRDS_PASSWORD')}@wrds-pgdata.wharton.upenn.edu:9737/wrds"
)

ccm_data = pd.read_sql_query("""
SELECT a.gvkey, a.conm, a.tic, a.cusip, a.cik, a.sic, a.naics,
       b.linkprim, b.linktype, b.liid, b.lpermno, b.lpermco,
       b.linkdt, b.linkenddt
FROM comp.names as a
INNER JOIN crsp.ccmxpf_lnkhist as b
ON a.gvkey = b.gvkey
WHERE b.linktype in ('LC', 'LU')
AND b.linkprim in ('P', 'C')
ORDER BY a.gvkey
""", engine)
engine.dispose()

ccm_data['linkdt'] = pd.to_datetime(ccm_data['linkdt'])
ccm_data['linkenddt'] = pd.to_datetime(ccm_data['linkenddt'])

# Save parquet version
parquet_data = ccm_data.rename(columns={
    'linkdt': 'timeLinkStart_d', 'linkenddt': 'timeLinkEnd_d', 'lpermno': 'permno'
})
parquet_data['naics'] = parquet_data['naics'].fillna('')
parquet_data['cik'] = parquet_data['cik'].fillna('')
parquet_data = standardize_columns(parquet_data, 'CCMLinkingTable')
parquet_data.to_parquet("../pyData/Intermediate/CCMLinkingTable.parquet", index=False)

print(f"CCM Linking Table downloaded with {len(ccm_data)} records", flush=True)
print(f"Unique companies (gvkey): {ccm_data['gvkey'].nunique()}", flush=True)
print(f"Unique stocks (lpermno): {ccm_data['lpermno'].nunique()}", flush=True)
print("=" * 60, flush=True)
print("✅ A_CCMLinkingTable.py completed successfully", flush=True)
print("=" * 60, flush=True)
