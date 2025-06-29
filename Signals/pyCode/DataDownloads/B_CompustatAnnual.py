#!/usr/bin/env python3
"""
Compustat Annual data download script.

Python equivalent of B_CompustatAnnual.do
Downloads Compustat annual fundamental data and creates both
annual and monthly versions.
"""

import os
import pandas as pd
import numpy as np
from dotenv import load_dotenv
from sqlalchemy import create_engine
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from config import MAX_ROWS_DL
from utils.column_standardizer_yaml import yaml_standardize_columns
import pyarrow as pa

print("=" * 60, flush=True)
print("📈 B_CompustatAnnual.py - Compustat Annual Fundamentals", flush=True)
print("=" * 60, flush=True)

load_dotenv()

# Create SQLAlchemy engine for database connection
engine = create_engine(
    f"postgresql://{os.getenv('WRDS_USERNAME')}:{os.getenv('WRDS_PASSWORD')}@wrds-pgdata.wharton.upenn.edu:9737/wrds"
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

compustat_data = pd.read_sql_query(QUERY, engine)
engine.dispose()

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

# Save CompustatAnnual.csv BEFORE any derived variables or zero-fill (matches Stata line 30)
compustat_csv_data = compustat_data.copy()

# Convert gvkey to integer to match Stata format
compustat_csv_data['gvkey'] = pd.to_numeric(compustat_csv_data['gvkey'])

# Convert datadate to string format to match Stata expectations
compustat_csv_data['datadate'] = compustat_csv_data['datadate'].dt.strftime('%d%b%Y').str.lower()

# Remove extra columns from CCMLinkingTable merge 
ccm_extra_columns = ['timeLinkStart_d', 'timeLinkEnd_d', 'cik', 'linkprim', 'linktype', 'sic', 'cnum', 'permno', 'liid', 'naics', 'lpermco']
for col in ccm_extra_columns:
    if col in compustat_csv_data.columns:
        compustat_csv_data = compustat_csv_data.drop(col, axis=1)

# Save CompustatAnnual.csv with raw missing values (matching Stata's export at line 30)
compustat_csv_data.to_csv(
    "../pyData/Intermediate/CompustatAnnual.csv", index=False
)

print(f"CompustatAnnual.csv saved with {len(compustat_csv_data)} records", flush=True)

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

# Variables where missing is assumed to be 0 (exact match to Stata logic in lines 63-69)
# From Stata: nopi dvt ob dm dc aco ap intan ao lco lo rect invt drc spi gdwl che dp act lct tstkp dvpa scstkc sstk mib ivao prstkc prstkcc txditc ivst
zero_fill_vars = ['nopi', 'dvt', 'ob', 'dm', 'dc', 'aco', 'ap', 'intan', 'ao',
                  'lco', 'lo', 'rect', 'invt', 'drc', 'spi', 'gdwl', 'che',
                  'dp', 'act', 'lct', 'tstkp', 'dvpa', 'scstkc', 'sstk',
                  'mib', 'ivao', 'prstkc', 'prstkcc', 'txditc', 'ivst']

# Apply zero-fill logic exactly as in Stata
for var in zero_fill_vars:
    if var in compustat_data.columns:
        compustat_data[var] = compustat_data[var].fillna(0)

# Create zero-filled versions of expense variables
compustat_data['xad0'] = compustat_data['xad'].fillna(0)
compustat_data['xint0'] = compustat_data['xint'].fillna(0)
compustat_data['xsga0'] = compustat_data['xsga'].fillna(0)


def preserve_dtypes_for_parquet(df):
    """
    Preserve pandas dtypes when saving to parquet to match DTA file types.
    Handles null-only columns and ensures consistent type preservation.
    """
    # Create a copy to avoid modifying original
    df_copy = df.copy()
    
    # Define explicit type mapping based on DTA file structure
    dtype_map = {
        # Integer columns that should stay as int32
        'gvkey': 'int32',
        'fyear': 'int16', 
        'permno': 'int32',
        'lpermco': 'int32',
        
        # String columns that should be preserved even if null
        'conm': 'string',
        'tic': 'string', 
        'cusip': 'string',
        'cnum': 'string',
        'cik': 'string',
        'sic': 'string',
        'naics': 'string',
        
        # Float columns that should stay float64 even if all null
        'naicsh': 'float64',
        'sich': 'float64',
        'cshrc': 'float64',
        'dlcch': 'float64', 
        'dltis': 'float64',
        'dltr': 'float64',
        'drlt': 'float64',
        'dv': 'float64',
        'dvpd': 'float64',
        'fatb': 'float64',
        'fatl': 'float64',
        'ffo': 'float64',
        'fincf': 'float64',
        'fopt': 'float64',
        'gdwlia': 'float64',
        'gdwlip': 'float64',
        'gwo': 'float64',
        'ivncf': 'float64',
        'msa': 'float64',
        'oancf': 'float64',
        'recta': 'float64',
        'txfo': 'float64',
        'txfed': 'float64',
        'wcapch': 'float64',
        'xad': 'float64',
        'xrd': 'float64',
        
        # Float32 columns that should be preserved as float32
        'dr': 'float32',
        'xad0': 'float32',
        'xint0': 'float32', 
        'xsga0': 'float32',
        
        # Columns that should remain float64 (not convert to int64)
        'dm': 'float64',
        'drc': 'float64',
        'gdwl': 'float64',
        'dvpa': 'float64',
        'ob': 'float64',
        'prstkc': 'float64',
        'prstkcc': 'float64',
        'scstkc': 'float64',
        'sstk': 'float64',
        'tstkp': 'float64',
    }
    
    # Apply dtype mapping
    for col, target_dtype in dtype_map.items():
        if col in df_copy.columns:
            try:
                if target_dtype == 'string':
                    # For string columns, ensure they're treated as string type
                    df_copy[col] = df_copy[col].astype('string')
                elif target_dtype.startswith('float'):
                    # For float columns, preserve as float even if all null
                    df_copy[col] = pd.to_numeric(df_copy[col], errors='coerce').astype(target_dtype)
                elif target_dtype.startswith('int'):
                    # For integer columns, handle nulls properly
                    if df_copy[col].isna().all():
                        # If all null, keep as nullable int
                        df_copy[col] = df_copy[col].astype(f'{target_dtype.capitalize()}')
                    else:
                        df_copy[col] = pd.to_numeric(df_copy[col], errors='coerce').astype(target_dtype)
            except Exception as e:
                print(f"Warning: Could not convert {col} to {target_dtype}: {e}")
    
    return df_copy

# Also save full parquet version for internal use (with all derived variables)
compustat_data.to_parquet(
    "../pyData/Intermediate/CompustatAnnual.parquet", index=False
)

# Clean up for annual version
annual_data = compustat_data.drop(columns=[
    'timeLinkStart_d', 'timeLinkEnd_d', 'linkprim', 'liid', 'linktype'
])
annual_data['gvkey'] = pd.to_numeric(annual_data['gvkey'])

# Assume 6 month reporting lag - replicate Stata's mofd(datadate) + 6 logic
# Stata's mofd() converts to beginning of month, then adds 6 months
annual_data['time_avail_m'] = (
    annual_data['datadate'].dt.to_period('M') + 6
).dt.to_timestamp()

# Save annual version with preserved dtypes
annual_data_typed = preserve_dtypes_for_parquet(annual_data)

# Standardize columns using YAML schema
annual_data_typed = yaml_standardize_columns(annual_data_typed, "a_aCompustat")

annual_data_typed.to_parquet("../pyData/Intermediate/a_aCompustat.parquet", index=False)

# Create monthly version (expand each row 12 times) - replicate Stata logic exactly
print("Expanding annual data to monthly...", flush=True)
monthly_data = annual_data.copy()
monthly_data = pd.concat([monthly_data] * 12, ignore_index=True)

# Replicate Stata's logic: bysort gvkey tempTime: replace time_avail_m = time_avail_m + _n - 1
monthly_data = monthly_data.sort_values(['gvkey', 'time_avail_m']).reset_index(drop=True)
monthly_data['tempTime'] = monthly_data['time_avail_m']
monthly_data['month_offset'] = monthly_data.groupby(['gvkey', 'tempTime']).cumcount()

# Add months using period arithmetic to match Stata's monthly format
monthly_data['time_avail_m'] = (
    monthly_data['time_avail_m'].dt.to_period('M') + monthly_data['month_offset']
).dt.to_timestamp()

monthly_data = monthly_data.drop('tempTime', axis=1)

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

# Save monthly version with preserved dtypes
monthly_data_typed = preserve_dtypes_for_parquet(monthly_data)

# Standardize columns using YAML schema
monthly_data_typed = yaml_standardize_columns(monthly_data_typed, "m_aCompustat")

monthly_data_typed.to_parquet("../pyData/Intermediate/m_aCompustat.parquet", index=False)

print(f"Annual version saved with {len(annual_data)} records", flush=True)
print(f"Monthly version saved with {len(monthly_data)} records", flush=True)
print("=" * 60, flush=True)
print("✅ B_CompustatAnnual.py completed successfully", flush=True)
print("=" * 60, flush=True)
