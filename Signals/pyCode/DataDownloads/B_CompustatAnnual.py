#!/usr/bin/env python3
"""
Compustat Annual data download script.

Python equivalent of B_CompustatAnnual.do
Downloads Compustat annual fundamental data and creates both
annual and monthly versions.
"""

import os
import psycopg2
import pandas as pd
import numpy as np
from dotenv import load_dotenv
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from config import MAX_ROWS_DL

print("=" * 60, flush=True)
print("📈 B_CompustatAnnual.py - Compustat Annual Fundamentals", flush=True)
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
SELECT a.gvkey, a.datadate, a.conm, a.fyear, a.tic, a.cusip, a.naicsh,
       a.sich, a.aco,a.act,a.ajex,a.am,a.ao,a.ap,a.at,a.capx,a.ceq,
       a.ceqt,a.che,a.cogs, a.csho,a.cshrc,a.dcpstk,a.dcvt,a.dlc,
       a.dlcch,a.dltis,a.dltr, a.dltt,a.dm,a.dp,a.drc,a.drlt,a.dv,
       a.dvc,a.dvp,a.dvpa,a.dvpd, a.dvpsx_c,a.dvt,a.ebit,a.ebitda,
       a.emp,a.epspi,a.epspx,a.fatb,a.fatl, a.ffo,a.fincf,a.fopt,
       a.gdwl,a.gdwlia,a.gdwlip,a.gwo,a.ib,a.ibcom, a.intan,a.invt,
       a.ivao,a.ivncf,a.ivst,a.lco,a.lct,a.lo,a.lt,a.mib, a.msa,a.ni,
       a.nopi,a.oancf,a.ob,a.oiadp,a.oibdp,a.pi,a.ppenb,a.ppegt,
       a.ppenls, a.ppent,a.prcc_c,a.prcc_f,a.prstkc,a.prstkcc,a.pstk,
       a.pstkl,a.pstkrv, a.re,a.rect,a.recta,a.revt,a.sale,a.scstkc,
       a.seq,a.spi,a.sstk, a.tstkp,a.txdb,a.txdi,a.txditc,a.txfo,
       a.txfed,a.txp,a.txt, a.wcap,a.wcapch,a.xacc,a.xad,a.xint,
       a.xrd,a.xpp,a.xsga
FROM COMP.FUNDA as a
WHERE a.consol = 'C'
AND a.popsrc = 'D'
AND a.datafmt = 'STD'
AND a.curcd = 'USD'
AND a.indfmt = 'INDL'
"""

# Add row limit for debugging if configured
if MAX_ROWS_DL > 0:
    QUERY += f" LIMIT {MAX_ROWS_DL}"
    print(f"DEBUG MODE: Limiting to {MAX_ROWS_DL} rows", flush=True)

compustat_data = pd.read_sql_query(QUERY, conn)
conn.close()

print(f"Downloaded {len(compustat_data)} annual records", flush=True)

# Ensure directories exist
os.makedirs("../pyData/Intermediate", exist_ok=True)

# Require some reasonable amount of information
compustat_data = compustat_data.dropna(subset=['at', 'prcc_c', 'ni'])
print(
    f"After requiring AT, PRCC_C, NI: {len(compustat_data)} records",
    flush=True
)

# 6 digit CUSIP
compustat_data['cnum'] = compustat_data['cusip'].str[:6]

# Create derived variables and fill missing values
# Deferred revenue (dr) - replicate Stata logic exactly
compustat_data['dr'] = np.nan
# Case 1: Both drc and drlt exist
mask1 = compustat_data['drc'].notna() & compustat_data['drlt'].notna()
compustat_data.loc[mask1, 'dr'] = (
    compustat_data.loc[mask1, 'drc'] +
    compustat_data.loc[mask1, 'drlt']
)
# Case 2: Only drc exists
mask2 = compustat_data['drc'].notna() & compustat_data['drlt'].isna()
compustat_data.loc[mask2, 'dr'] = compustat_data.loc[mask2, 'drc']
# Case 3: Only drlt exists
mask3 = compustat_data['drc'].isna() & compustat_data['drlt'].notna()
compustat_data.loc[mask3, 'dr'] = compustat_data.loc[mask3, 'drlt']

# Convertible debt (dc) - replicate Stata logic exactly
# dcpstk = convertible debt and preferred stock, pstk = preferred stock, dcvt = convertible debt
compustat_data['dc'] = np.nan
# Case 1: dc = dcpstk - pstk if dcpstk > pstk & pstk !=. & dcpstk !=. & dcvt ==.
mask_dc1 = (
    (compustat_data['dcpstk'] > compustat_data['pstk']) &
    compustat_data['pstk'].notna() &
    compustat_data['dcpstk'].notna() &
    compustat_data['dcvt'].isna()
)
compustat_data.loc[mask_dc1, 'dc'] = (
    compustat_data.loc[mask_dc1, 'dcpstk'] -
    compustat_data.loc[mask_dc1, 'pstk']
)
# Case 2: dc = dcpstk if pstk ==. & dcpstk !=. & dcvt ==.
mask_dc2 = (
    compustat_data['pstk'].isna() &
    compustat_data['dcpstk'].notna() &
    compustat_data['dcvt'].isna()
)
compustat_data.loc[mask_dc2, 'dc'] = compustat_data.loc[mask_dc2, 'dcpstk']
# Case 3: dc = dcvt if dc is still missing
mask_dc3 = compustat_data['dc'].isna()
compustat_data.loc[mask_dc3, 'dc'] = compustat_data.loc[mask_dc3, 'dcvt']

# Variables where missing is assumed to be 0 (including dc)
zero_fill_vars = ['nopi', 'dvt', 'ob', 'dm', 'dc', 'aco', 'ap', 'intan', 'ao',
                  'lco', 'lo', 'rect', 'invt', 'drc', 'spi', 'gdwl', 'che',
                  'dp', 'act', 'lct', 'tstkp', 'dvpa', 'scstkc', 'sstk',
                  'mib', 'ivao', 'prstkc', 'prstkcc', 'txditc', 'ivst']

for var in zero_fill_vars:
    if var in compustat_data.columns:
        compustat_data[var] = compustat_data[var].fillna(0)

# Create zero-filled versions of expense variables
compustat_data['xad0'] = compustat_data['xad'].fillna(0)
compustat_data['xint0'] = compustat_data['xint'].fillna(0)
compustat_data['xsga0'] = compustat_data['xsga'].fillna(0)

# Load CCM linking table for merging
ccm_data = pd.read_parquet("../pyData/Intermediate/CCMLinkingTable.parquet")

# Drop overlapping columns from CCM to avoid _x/_y suffixes
ccm_columns_to_drop = ['conm', 'tic', 'cusip'] 
for col in ccm_columns_to_drop:
    if col in ccm_data.columns:
        ccm_data = ccm_data.drop(col, axis=1)

# Merge with CCM linking table
compustat_data = compustat_data.merge(ccm_data, on='gvkey', how='inner')
print(
    f"After merging with CCM links: {len(compustat_data)} records",
    flush=True
)

# Use only if data date is within the validity period of the link
compustat_data['datadate'] = pd.to_datetime(compustat_data['datadate'])
compustat_data['timeLinkStart_d'] = pd.to_datetime(
    compustat_data['timeLinkStart_d']
)
compustat_data['timeLinkEnd_d'] = pd.to_datetime(
    compustat_data['timeLinkEnd_d']
)

valid_link = (
    (compustat_data['timeLinkStart_d'] <= compustat_data['datadate']) &
    (compustat_data['datadate'] <= compustat_data['timeLinkEnd_d'])
)

compustat_data = compustat_data[valid_link]
print(
    f"After filtering for valid link dates: {len(compustat_data)} records",
    flush=True
)

# Save processed data to parquet format (equivalent to Stata's CompustatAnnual.csv)
compustat_data.to_parquet(
    "../pyData/Intermediate/CompustatAnnual.parquet", index=False
)

# Clean up for annual version
annual_data = compustat_data.drop(columns=[
    'timeLinkStart_d', 'timeLinkEnd_d', 'linkprim', 'liid', 'linktype'
])
annual_data['gvkey'] = pd.to_numeric(annual_data['gvkey'])

# Assume 6 month reporting lag
annual_data['time_avail_m'] = (
    annual_data['datadate'] + pd.DateOffset(months=6)
)

# Save annual version
annual_data.to_parquet("../pyData/Intermediate/a_aCompustat.parquet", index=False)

# Create monthly version (expand each row 12 times)
print("Expanding annual data to monthly...", flush=True)
monthly_data = annual_data.copy()
monthly_data = pd.concat([monthly_data] * 12, ignore_index=True)

# Create time series for each observation
monthly_data = monthly_data.sort_values(
    ['gvkey', 'time_avail_m']
).reset_index(drop=True)
monthly_data['month_offset'] = monthly_data.groupby(
    ['gvkey', 'datadate']
).cumcount()
monthly_data['time_avail_m'] = (
    monthly_data['time_avail_m'] +
    pd.to_timedelta(monthly_data['month_offset'] * 30.44, unit='D')
)

# Keep only the most recent info for duplicate time periods
monthly_data = monthly_data.sort_values(
    ['gvkey', 'time_avail_m', 'datadate']
)
monthly_data = monthly_data.drop_duplicates(
    ['gvkey', 'time_avail_m'], keep='last'
)

monthly_data = monthly_data.sort_values(
    ['permno', 'time_avail_m', 'datadate']
)
monthly_data = monthly_data.drop_duplicates(
    ['permno', 'time_avail_m'], keep='last'
)

monthly_data = monthly_data.drop(columns=['month_offset'])
monthly_data.to_parquet("../pyData/Intermediate/m_aCompustat.parquet", index=False)

print(f"Annual version saved with {len(annual_data)} records", flush=True)
print(f"Monthly version saved with {len(monthly_data)} records", flush=True)
print("=" * 60, flush=True)
print("✅ B_CompustatAnnual.py completed successfully", flush=True)
print("=" * 60, flush=True)
