# ABOUTME: Downloads the shared CRSP-Compustat link history and company identifiers.
# ABOUTME: Keeps primary links and checks the link key before saving Parquet.
"""
Inputs:
- comp.names (company master file)
- crsp.ccmxpf_lnkhist (CCM link history used with both CRSP SIZ and CIZ)
- OPENAP_DATA_ROOT (optional output root; defaults to Signals/pyData)

Outputs:
- <data root>/Intermediate/CCMLinkingTable.parquet

How to run: from the project root, python3 Signals/pyCode/DataDownloads/CCMLinkingTable.py
DEBUG_MODE reads the full link history for the Stage 1 comparison.

Use the project Python environment at /opt/venv/projects/openap.
"""

import os
import sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from config import DATA_ROOT
from utils.debug_mode import log_selection
from utils.wrds_connection import get_wrds_engine
import pandas as pd
from dotenv import load_dotenv

(DATA_ROOT / 'Intermediate').mkdir(parents=True, exist_ok=True)

print("=" * 60, flush=True)
print("🔗 CCMLinkingTable.py - CRSP-Compustat Linking Table", flush=True)
print("=" * 60, flush=True)

log_selection("CCMLinkingTable")
load_dotenv()

engine = get_wrds_engine()

# Obtain primary company-security links and their validity periods for merging datasets.
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

try:
    df = pd.read_sql_query(QUERY, engine)
finally:
    engine.dispose()

# Preserve whole-number stock identifiers and usable link dates, including missing end dates.
df[['lpermno', 'lpermco']] = df[['lpermno', 'lpermco']].astype('Int64')
df[['linkdt', 'linkenddt']] = df[['linkdt', 'linkenddt']].astype('datetime64[ns]')

# Use the link-field names expected by downstream company-security joins.
df = df.rename(columns={
    'linkdt': 'timeLinkStart_d',
    'linkenddt': 'timeLinkEnd_d',
    'lpermno': 'permno',
    'lpermco': 'permco'
})
df['naics'] = df['naics'].fillna('')
df['cik'] = df['cik'].fillna('')

# Reject missing or repeated link identities before downstream joins can multiply rows.
key = ['gvkey', 'permno', 'permco', 'liid', 'linktype', 'linkprim', 'timeLinkStart_d']
if df[key].isna().any().any():
    raise ValueError(f"CCM link has null key values: {key}")
duplicate_count = int(df.duplicated(key, keep=False).sum())
if duplicate_count:
    raise ValueError(f"CCM link has {duplicate_count} rows with duplicate {key} keys")

# Save the validated link history for matching accounting and stock data.
df.to_parquet(DATA_ROOT / 'Intermediate/CCMLinkingTable.parquet', index=False)

print(f"CCM Linking Table downloaded with {len(df)} records", flush=True)
print(f"Unique companies (gvkey): {df['gvkey'].nunique()}", flush=True)
print(f"Unique stocks (permno): {df['permno'].nunique()}", flush=True)
print("=" * 60, flush=True)
print("✅ CCMLinkingTable.py completed successfully", flush=True)
print("=" * 60, flush=True)
