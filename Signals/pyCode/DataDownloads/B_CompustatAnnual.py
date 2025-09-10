# ABOUTME: Downloads Compustat annual fundamental data from WRDS and creates annual/monthly versions
# ABOUTME: Applies data filtering, creates derived variables, and merges with CCM linking data
"""
Inputs:
- comp.funda (WRDS Compustat annual fundamental data)
- ../pyData/Intermediate/CCMLinkingTable.parquet

Outputs:
- ../pyData/Intermediate/a_aCompustat.parquet (annual version)
- ../pyData/Intermediate/m_aCompustat.parquet (monthly version)

How to run: python3 B_CompustatAnnual.py
"""

import os
import pandas as pd
import numpy as np
from dotenv import load_dotenv
from sqlalchemy import create_engine
import sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from config import MAX_ROWS_DL
from utils.column_standardizer_yaml import standardize_columns

print("📈 B_CompustatAnnual.py - Compustat Annual Fundamentals", flush=True)
load_dotenv()
engine = create_engine(f"postgresql://{os.getenv('WRDS_USERNAME')}:{os.getenv('WRDS_PASSWORD')}@wrds-pgdata.wharton.upenn.edu:9737/wrds")

# Query Compustat annual fundamentals with standard filters
QUERY = """
SELECT a.gvkey, a.datadate, a.conm, a.fyear, a.tic, a.cusip, a.naicsh, a.sich, 
       a.aco,a.act,a.ajex,a.am,a.ao,a.ap,a.at,a.capx,a.ceq,a.ceqt,a.che,a.cogs,a.csho,a.cshrc,a.dcpstk,a.dcvt,a.dlc,a.dlcch,a.dltis,a.dltr,
       a.dltt,a.dm,a.dp,a.drc,a.drlt,a.dv,a.dvc,a.dvp,a.dvpa,a.dvpd,a.dvpsx_c,a.dvt,a.ebit,a.ebitda,a.emp,a.epspi,a.epspx,a.fatb,a.fatl,
       a.ffo,a.fincf,a.fopt,a.gdwl,a.gdwlia,a.gdwlip,a.gwo,a.ib,a.ibcom,a.intan,a.invt,a.ivao,a.ivncf,a.ivst,a.lco,a.lct,a.lo,a.lt,a.mib,
       a.msa,a.ni,a.nopi,a.oancf,a.ob,a.oiadp,a.oibdp,a.pi,a.ppenb,a.ppegt,a.ppenls,a.ppent,a.prcc_c,a.prcc_f,a.prstkc,a.prstkcc,a.pstk,a.pstkl,a.pstkrv,
       a.re,a.rect,a.recta,a.revt,a.sale,a.scstkc,a.seq,a.spi,a.sstk,a.tstkp,a.txdb,a.txdi,a.txditc,a.txfo,a.txfed,a.txp,a.txt,a.wcap,a.wcapch,a.xacc,a.xad,a.xint,a.xrd,a.xpp,a.xsga
FROM COMP.FUNDA as a
WHERE a.consol = 'C' AND a.popsrc = 'D' AND a.datafmt = 'STD' AND a.curcd = 'USD' AND a.indfmt = 'INDL'
"""

if MAX_ROWS_DL > 0:
    QUERY += f" LIMIT {MAX_ROWS_DL}"
    print(f"DEBUG MODE: Limiting to {MAX_ROWS_DL} rows", flush=True)

# Download data from WRDS
compustat_data_raw = pd.read_sql_query(QUERY, engine)
engine.dispose()
print(f"Downloaded {len(compustat_data_raw)} annual records", flush=True)

# Fix column types to match Stata behavior (convert null object columns to float)
for col in compustat_data_raw.columns:
    if compustat_data_raw[col].dtype == 'object' and compustat_data_raw[col].isna().all():
        compustat_data_raw[col] = compustat_data_raw[col].astype('float64')

# Apply basic data filters
os.makedirs("../pyData/Intermediate", exist_ok=True)
compustat_data = compustat_data_raw.copy()
compustat_data = compustat_data.dropna(subset=['at', 'prcc_c', 'ni'])
print(f"After requiring AT, PRCC_C, NI: {len(compustat_data)} records", flush=True)

# Create 6-digit CUSIP identifier
compustat_data['cnum'] = compustat_data['cusip'].str[:6]

# Create deferred revenue variable
compustat_data['dr'] = compustat_data['drc'].fillna(0) + compustat_data['drlt'].fillna(0)
compustat_data.loc[compustat_data['drc'].isna() & compustat_data['drlt'].isna(), 'dr'] = np.nan

# Create convertible debt variable with complex logic
compustat_data['dc'] = np.nan
dc1 = (compustat_data['dcpstk'] > compustat_data['pstk']) & compustat_data['pstk'].notna() & compustat_data['dcpstk'].notna() & compustat_data['dcvt'].isna()
dc2 = compustat_data['pstk'].isna() & compustat_data['dcpstk'].notna() & compustat_data['dcvt'].isna()
compustat_data.loc[dc1, 'dc'] = compustat_data.loc[dc1, 'dcpstk'] - compustat_data.loc[dc1, 'pstk']
compustat_data.loc[dc2, 'dc'] = compustat_data.loc[dc2, 'dcpstk']
compustat_data.loc[compustat_data['dc'].isna(), 'dc'] = compustat_data.loc[compustat_data['dc'].isna(), 'dcvt']

# Create zero-filled expense variables for predictor calculations
compustat_data['xint0'] = compustat_data['xint'].fillna(0)
compustat_data['xsga0'] = compustat_data['xsga'].fillna(0)
compustat_data['xad0'] = compustat_data['xad'].fillna(0)

# Fill missing values with zeros for specified variables
zero_fill_vars = ['nopi', 'dvt', 'ob', 'dm', 'dc', 'aco', 'ap', 'intan', 'ao', 'lco', 'lo', 'rect', 'invt', 'drc', 'spi', 'gdwl', 'che', 'dp', 'act', 'lct', 'tstkp', 'dvpa', 'scstkc', 'sstk', 'mib', 'ivao', 'prstkc', 'prstkcc', 'txditc', 'ivst']
for var in zero_fill_vars:
    if var in compustat_data.columns:
        compustat_data[var] = compustat_data[var].fillna(0)

# Merge with CCM linking table to add PERMNO
ccm_data = pd.read_parquet("../pyData/Intermediate/CCMLinkingTable.parquet")
ccm_merge_data = ccm_data.drop(columns=['conm', 'cusip', 'tic'], errors='ignore')
compustat_data = compustat_data.merge(ccm_merge_data, on='gvkey', how='inner')
print(f"After merging with CCM links: {len(compustat_data)} records", flush=True)

# Filter for valid link date ranges
compustat_data['datadate'] = pd.to_datetime(compustat_data['datadate'])
compustat_data['timeLinkStart_d'] = pd.to_datetime(compustat_data['timeLinkStart_d'])
compustat_data['timeLinkEnd_d'] = pd.to_datetime(compustat_data['timeLinkEnd_d'])
compustat_data = compustat_data[(compustat_data['timeLinkStart_d'] <= compustat_data['datadate']) & ((compustat_data['datadate'] <= compustat_data['timeLinkEnd_d']) | compustat_data['timeLinkEnd_d'].isna())]
print(f"After filtering for valid link dates: {len(compustat_data)} records", flush=True)

# Create annual version with 6-month lag for availability
annual_data = compustat_data.drop(columns=['timeLinkStart_d', 'timeLinkEnd_d', 'linkprim', 'liid', 'linktype'])
annual_data['gvkey'] = pd.to_numeric(annual_data['gvkey'])
annual_data['time_avail_m'] = (annual_data['datadate'].dt.to_period('M') + 6).dt.to_timestamp()
annual_data = standardize_columns(annual_data, 'a_aCompustat')
annual_data.to_parquet("../pyData/Intermediate/a_aCompustat.parquet", index=False)
print(f"Annual version saved with {len(annual_data)} records", flush=True)

# Create monthly version by expanding annual data across 12 months
monthly_data = pd.concat([annual_data] * 12, ignore_index=True)
monthly_data = monthly_data.sort_values(['gvkey', 'time_avail_m']).reset_index(drop=True)
monthly_data['month_offset'] = monthly_data.groupby(['gvkey', 'time_avail_m']).cumcount()
monthly_data['time_avail_m'] = (monthly_data['time_avail_m'].dt.to_period('M') + monthly_data['month_offset']).dt.to_timestamp()
monthly_data = monthly_data.sort_values(['gvkey', 'time_avail_m', 'datadate']).drop_duplicates(['gvkey', 'time_avail_m'], keep='last')
monthly_data = monthly_data.sort_values(['permno', 'time_avail_m', 'datadate']).drop_duplicates(['permno', 'time_avail_m'], keep='last')
monthly_data = monthly_data.drop(columns=['month_offset'])
monthly_data = standardize_columns(monthly_data, 'm_aCompustat')
monthly_data.to_parquet("../pyData/Intermediate/m_aCompustat.parquet", index=False)
print(f"Monthly version saved with {len(monthly_data)} records", flush=True)

print("✅ B_CompustatAnnual.py completed successfully", flush=True)