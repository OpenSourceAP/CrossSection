# ABOUTME: Downloads CRSP-Compustat linking table with company and stock identifiers
# ABOUTME: Filters for primary links (LC/LU + P/C) and converts to CSV/Parquet formats
"""
Inputs:
- comp.names (company master file)
- crsp.ccmxpf_lnkhist (CRSP-Compustat link history)

Outputs:
- ../pyData/Intermediate/CCMLinkingTable.parquet

How to run: python3 CCMLinkingTable.py
"""

import os
import sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from utils.debug_mode import log_selection
from utils.wrds_connection import get_wrds_engine, release_wrds_engine
from utils.download_paths import intermediate_path
import pandas as pd
from dotenv import load_dotenv

# Display script header
print("=" * 60, flush=True)
print("🔗 CCMLinkingTable.py - CRSP-Compustat Linking Table", flush=True)
print("=" * 60, flush=True)

# Load environment variables for database credentials
log_selection("CCMLinkingTable")
load_dotenv()

# Create database connection to WRDS
engine = get_wrds_engine()

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
df = pd.read_sql_query(QUERY, engine)
release_wrds_engine(engine)

# Enforce formats
df[['lpermno','lpermco']] = df[['lpermno','lpermco']].astype('Int64')
df[['linkdt','linkenddt']] = df[['linkdt','linkenddt']].astype('datetime64[ns]')

# rename columns
df = df.rename(columns={
    'linkdt': 'timeLinkStart_d',
    'linkenddt': 'timeLinkEnd_d',
    'lpermno': 'permno',
    'lpermco': 'permco'
})
df['naics'] = df['naics'].fillna('')
df['cik'] = df['cik'].fillna('')
df.to_parquet(intermediate_path("CCMLinkingTable.parquet"), index=False)

# Display summary statistics
print(f"CCM Linking Table downloaded with {len(df)} records", flush=True)
print(f"Unique companies (gvkey): {df['gvkey'].nunique()}", flush=True)
print(f"Unique stocks (permno): {df['permno'].nunique()}", flush=True)
print("=" * 60, flush=True)
print("✅ CCMLinkingTable.py completed successfully", flush=True)
print("=" * 60, flush=True)