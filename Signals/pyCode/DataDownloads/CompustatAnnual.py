# ABOUTME: Downloads Compustat annual fundamental data from WRDS and processes into annual/monthly versions
# ABOUTME: Creates zero-filled variables, includes CCM linking, and applies 6-month reporting lag
"""
Inputs:
- WRDS comp.funda database (annual fundamentals)
- comp.names (company master file)
- crsp.ccmxpf_lnkhist (CRSP-Compustat link history)

Outputs:
- ../pyData/Intermediate/CompustatAnnual.csv
- ../pyData/Intermediate/a_aCompustat.parquet
- ../pyData/Intermediate/m_aCompustat.parquet

How to run: python CompustatAnnual.py
"""

import os
import pandas as pd
import numpy as np
from dotenv import load_dotenv
from sqlalchemy import create_engine
import sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from config import MAX_ROWS_DL

# Print script header
print("=" * 60, flush=True)
print("📈 CompustatAnnual.py - Compustat Annual Fundamentals", flush=True)
print("=" * 60, flush=True)

# Load environment variables and create database connection
load_dotenv()
engine = create_engine(
    f"postgresql://{os.getenv('WRDS_USERNAME')}:{os.getenv('WRDS_PASSWORD')}@wrds-pgdata.wharton.upenn.edu:9737/wrds"
)

# Define SQL query to download Compustat annual fundamentals data
QUERY = """
SELECT a.gvkey, a.datadate, a.conm, a.fyear, a.tic, a.cusip, a.naicsh, a.sich, 
       a.aco,a.act,a.ajex,a.am,a.ao,a.ap,a.at,a.capx,a.ceq,a.ceqt,a.che,a.cogs,
       a.csho,a.cshrc,a.dcpstk,a.dcvt,a.dlc,a.dlcch,a.dltis,a.dltr,
       a.dltt,a.dm,a.dp,a.drc,a.drlt,a.dv,a.dvc,a.dvp,a.dvpa,a.dvpd,
       a.dvpsx_c,a.dvt,a.ebit,a.ebitda,a.emp,a.epspi,a.epspx,a.fatb,a.fatl,
       a.ffo,a.fincf,a.fopt,a.gdwl,a.gdwlia,a.gdwlip,a.gwo,a.ib,a.ibcom,
       a.intan,a.invt,a.ivao,a.ivncf,a.ivst,a.lco,a.lct,a.lo,a.lt,a.mib,
       a.msa,a.ni,a.nopi,a.oancf,a.ob,a.oiadp,a.oibdp,a.pi,a.ppenb,a.ppegt,
       a.ppenls,
       a.ppent,a.prcc_c,a.prcc_f,a.prstkc,a.prstkcc,a.pstk,a.pstkl,a.pstkrv,
       a.re,a.rect,a.recta,a.revt,a.sale,a.scstkc,a.seq,a.spi,a.sstk,
       a.tstkp,a.txdb,a.txdi,a.txditc,a.txfo,a.txfed,a.txp,a.txt,
       a.wcap,a.wcapch,a.xacc,a.xad,a.xint,a.xrd,a.xpp,a.xsga
FROM COMP.FUNDA as a
WHERE a.consol = 'C'
AND a.popsrc = 'D'
AND a.datafmt = 'STD'
AND a.curcd = 'USD'
AND a.indfmt = 'INDL'
"""

# Apply row limit for debugging mode if configured
if MAX_ROWS_DL > 0:
    QUERY += f" LIMIT {MAX_ROWS_DL}"
    print(f"DEBUG MODE: Limiting to {MAX_ROWS_DL} rows", flush=True)

# Execute query and download data from WRDS
compustat_data_raw = pd.read_sql_query(QUERY, engine)
print(f"Downloaded {len(compustat_data_raw)} annual records", flush=True)

# Fix column types: convert object columns with all None values to float64
for col in compustat_data_raw.columns:
    if (compustat_data_raw[col].dtype == 'object' and 
        compustat_data_raw[col].isna().all()):
        compustat_data_raw[col] = compustat_data_raw[col].astype('float64')


# Save raw CSV immediately with Stata-formatted dates
compustat_csv = compustat_data_raw.copy()
compustat_csv['datadate'] = pd.to_datetime(compustat_csv['datadate']).dt.strftime('%d%b%Y').str.lower()
compustat_csv.to_csv("../pyData/Intermediate/CompustatAnnual.csv", index=False)
print(f"CompustatAnnual.csv saved with {len(compustat_csv)} records", flush=True)

# Create working copy for further processing
compustat_data = compustat_data_raw.copy()

# Filter to records with required fields: total assets, price, and net income
compustat_data = compustat_data.dropna(subset=['at', 'prcc_c', 'ni'])
print(f"After requiring AT, PRCC_C, NI: {len(compustat_data)} records", flush=True)

# Extract 6-digit CUSIP identifier
compustat_data['cnum'] = compustat_data['cusip'].str[:6]

# Create derived variable: deferred revenue (dr) from drc and drlt components
compustat_data['dr'] = np.nan
# Sum both current and long-term deferred revenue when both exist
mask1 = compustat_data['drc'].notna() & compustat_data['drlt'].notna()
compustat_data.loc[mask1, 'dr'] = (
    compustat_data.loc[mask1, 'drc'] + compustat_data.loc[mask1, 'drlt']
)
# Use only current deferred revenue when long-term is missing
mask2 = compustat_data['drc'].notna() & compustat_data['drlt'].isna()
compustat_data.loc[mask2, 'dr'] = compustat_data.loc[mask2, 'drc']
# Use only long-term deferred revenue when current is missing
mask3 = compustat_data['drc'].isna() & compustat_data['drlt'].notna()
compustat_data.loc[mask3, 'dr'] = compustat_data.loc[mask3, 'drlt']

# Create derived variable: convertible debt (dc) using complex logic
compustat_data['dc'] = np.nan
# Calculate convertible debt as difference when dcpstk > pstk and dcvt is missing
mask_dc1 = (
    (compustat_data['dcpstk'] > compustat_data['pstk']) &
    compustat_data['pstk'].notna() &
    compustat_data['dcpstk'].notna() &
    compustat_data['dcvt'].isna()
)
compustat_data.loc[mask_dc1, 'dc'] = (
    compustat_data.loc[mask_dc1, 'dcpstk'] - compustat_data.loc[mask_dc1, 'pstk']
)
# Use dcpstk directly when pstk is missing and dcvt is missing
mask_dc2 = (
    compustat_data['pstk'].isna() &
    compustat_data['dcpstk'].notna() &
    compustat_data['dcvt'].isna()
)
compustat_data.loc[mask_dc2, 'dc'] = compustat_data.loc[mask_dc2, 'dcpstk']
# Fall back to dcvt for remaining missing convertible debt values
mask_dc3 = compustat_data['dc'].isna()
compustat_data.loc[mask_dc3, 'dc'] = compustat_data.loc[mask_dc3, 'dcvt']

# Create zero-filled versions of expense variables
compustat_data['xint0'] = 0.0  # 0.0 ensures float64
compustat_data.loc[compustat_data['xint'].notna(), 'xint0'] = compustat_data['xint']

compustat_data['xsga0'] = 0.0
compustat_data.loc[compustat_data['xsga'].notna(), 'xsga0'] = compustat_data['xsga']

compustat_data['xad0'] = compustat_data['xad'].fillna(0)

# Fill missing values with zero for specified balance sheet and income statement items
zero_fill_vars = ['nopi', 'dvt', 'ob', 'dm', 'dc', 'aco', 'ap', 'intan', 'ao',
                  'lco', 'lo', 'rect', 'invt', 'drc', 'spi', 'gdwl', 'che',
                  'dp', 'act', 'lct', 'tstkp', 'dvpa', 'scstkc', 'sstk',
                  'mib', 'ivao', 'prstkc', 'prstkcc', 'txditc', 'ivst']

for var in zero_fill_vars:
    compustat_data[var] = compustat_data[var].fillna(0)

# Download CCM linking table data directly (removing dependency on CCMLinkingTable.py)
print("Downloading CCM linking table data...", flush=True)
CCM_QUERY = """
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

# Execute CCM linking query using same engine
ccm_data = pd.read_sql_query(CCM_QUERY, engine)

# Process CCM data with same logic as CCMLinkingTable.py
ccm_data[['lpermno','lpermco']] = ccm_data[['lpermno','lpermco']].astype('Int64')
ccm_data[['linkdt','linkenddt']] = ccm_data[['linkdt','linkenddt']].astype('datetime64[ns]')

# Rename columns to match expected format
ccm_data = ccm_data.rename(columns={
    'linkdt': 'timeLinkStart_d',
    'linkenddt': 'timeLinkEnd_d',
    'lpermno': 'permno',
    'lpermco': 'permco'
})
ccm_data['naics'] = ccm_data['naics'].fillna('')
ccm_data['cik'] = ccm_data['cik'].fillna('')
print(f"CCM linking table loaded with {len(ccm_data)} records", flush=True)

# Close database connection after both queries are complete
engine.dispose()

# Remove duplicate columns from CCM data to replicate Stata's joinby update behavior
ccm_columns_to_drop = ['conm', 'cusip', 'tic']  # Keep these from compustat_data
ccm_merge_data = ccm_data.drop(columns=[col for col in ccm_columns_to_drop if col in ccm_data.columns])

# Merge tables without creating duplicate column suffixes
compustat_data = compustat_data.merge(ccm_merge_data, on='gvkey', how='inner')
print(f"After merging with CCM links: {len(compustat_data)} records", flush=True)


# Filter records to valid CCM link date ranges
compustat_data['datadate'] = pd.to_datetime(compustat_data['datadate'])
compustat_data['timeLinkStart_d'] = pd.to_datetime(compustat_data['timeLinkStart_d'])
compustat_data['timeLinkEnd_d'] = pd.to_datetime(compustat_data['timeLinkEnd_d'])

# Apply date filtering where missing end dates indicate active links
temp = (
    (compustat_data['timeLinkStart_d'] <= compustat_data['datadate']) &
    ((compustat_data['datadate'] <= compustat_data['timeLinkEnd_d']) | 
     compustat_data['timeLinkEnd_d'].isna())
)
compustat_data = compustat_data[temp]
print(f"After filtering for valid link dates: {len(compustat_data)} records", flush=True)

# Create annual version of the dataset
annual_data = compustat_data.copy()

# Remove CCM linking metadata columns
annual_data = annual_data.drop(columns=['timeLinkStart_d', 'timeLinkEnd_d', 'linkprim', 'liid', 'linktype'])

# Convert gvkey to numeric format
annual_data['gvkey'] = pd.to_numeric(annual_data['gvkey'])

# Add 6-month reporting lag to determine data availability date
annual_data['time_avail_m'] = (
    annual_data['datadate'].dt.to_period('M') + 6
).dt.to_timestamp()

# Save annual version
annual_data.to_parquet("../pyData/Intermediate/a_aCompustat.parquet", index=False)
print(f"Annual version saved with {len(annual_data)} records", flush=True)

# Create monthly version by expanding annual data
monthly_data = annual_data.copy()

# Replicate each annual record 12 times for monthly availability
monthly_data = pd.concat([monthly_data] * 12, ignore_index=True)

# Add sequential month offsets within each gvkey-time group
monthly_data = monthly_data.sort_values(['gvkey', 'time_avail_m']).reset_index(drop=True)
monthly_data['tempTime'] = monthly_data['time_avail_m']
monthly_data['month_offset'] = monthly_data.groupby(['gvkey', 'tempTime']).cumcount()

# Apply month offsets to create monthly availability dates
monthly_data['time_avail_m'] = (
    monthly_data['time_avail_m'].dt.to_period('M') + monthly_data['month_offset']
).dt.to_timestamp()

monthly_data = monthly_data.drop('tempTime', axis=1)

# Remove duplicates keeping most recent data for each gvkey-month and permno-month
monthly_data = monthly_data.sort_values(['gvkey', 'time_avail_m', 'datadate'])
monthly_data = monthly_data.drop_duplicates(['gvkey', 'time_avail_m'], keep='last')

monthly_data = monthly_data.sort_values(['permno', 'time_avail_m', 'datadate'])
monthly_data = monthly_data.drop_duplicates(['permno', 'time_avail_m'], keep='last')

monthly_data = monthly_data.drop(columns=['month_offset'])

# Save monthly version
monthly_data.to_parquet("../pyData/Intermediate/m_aCompustat.parquet", index=False)
print(f"Monthly version saved with {len(monthly_data)} records", flush=True)

print("=" * 60, flush=True)
print("✅ CompustatAnnual.py completed successfully", flush=True)
print("=" * 60, flush=True)