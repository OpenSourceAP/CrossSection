# ABOUTME: Downloads Compustat annual fundamental data from WRDS and processes into annual/monthly versions
# ABOUTME: Creates zero-filled variables, includes CCM linking, and applies 6-month reporting lag
"""
Inputs:
- WRDS comp.funda database (annual fundamentals)
- comp.names (company master file)
- crsp.ccmxpf_lnkhist (CCM link history, shared by CRSP SIZ and CIZ)
- OPENAP_COMPUSTAT_EXTRACT: optional saved raw fundamentals parquet to reuse

Outputs (under OPENAP_DATA_ROOT, default Signals/pyData):
- Intermediate/CompustatAnnual.csv
- Intermediate/a_aCompustat.parquet
- Intermediate/m_aCompustat.parquet
- Raw fundamentals parquet when OPENAP_COMPUSTAT_EXTRACT is explicitly set

How to run: from Signals/pyCode, run python3 DataDownloads/CompustatAnnual.py
Set OPENAP_DATA_ROOT to route outputs to a separate migration run directory.

Use the project Python environment at /opt/venv/projects/openap.
"""

import os
from pathlib import Path
import pandas as pd
import numpy as np
from dotenv import load_dotenv
import sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from config import DATA_ROOT
from utils.debug_mode import log_selection, sql_date_window, select_dates
from utils.wrds_connection import get_wrds_engine

(DATA_ROOT / 'Intermediate').mkdir(parents=True, exist_ok=True)

print("=" * 60, flush=True)
print("📈 CompustatAnnual.py - Compustat Annual Fundamentals", flush=True)
print("=" * 60, flush=True)

load_dotenv()
engine = get_wrds_engine()

# Obtain standardized, consolidated USD industrial accounts for comparable annual fundamentals.
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

# Restrict development runs to the shared annual report-date sample.
log_selection("CompustatAnnual")
predicate, query_params = sql_date_window("a.datadate", "annual")
QUERY += f" AND {predicate}"

# Optionally reuse a fixed fundamentals extract so comparison runs share the same input.
configured_extract = os.getenv("OPENAP_COMPUSTAT_EXTRACT")
extract_path = Path(configured_extract).expanduser().resolve() if configured_extract else None
if extract_path is not None:
    extract_path.parent.mkdir(parents=True, exist_ok=True)
if extract_path is not None and extract_path.exists():
    compustat_data_raw = pd.read_parquet(extract_path)
    print(f"Reused {len(compustat_data_raw)} annual records from {extract_path}", flush=True)
else:
    compustat_data_raw = pd.read_sql_query(QUERY, engine, params=query_params)
    print(f"Downloaded {len(compustat_data_raw)} annual records", flush=True)

# Keep entirely missing numeric fields usable in calculations and saved extracts.
for col in compustat_data_raw.columns:
    if (compustat_data_raw[col].dtype == 'object' and
        compustat_data_raw[col].isna().all()):
        compustat_data_raw[col] = compustat_data_raw[col].astype('float64')

if extract_path is not None and not extract_path.exists():
    # Preserve original date values in the reusable input extract.
    compustat_data_raw.to_parquet(extract_path, index=False)
    print(f"Saved reusable Compustat fundamentals to {extract_path}", flush=True)

# Apply the same development sample to saved extracts and freshly downloaded data.
compustat_data_raw = select_dates(compustat_data_raw, "datadate", "annual")

# Keep an unprocessed fundamentals CSV with dates readable by the legacy Stata pipeline.
compustat_csv = compustat_data_raw.copy()
compustat_csv['datadate'] = pd.to_datetime(compustat_csv['datadate']).dt.strftime('%d%b%Y').str.lower()
compustat_csv.to_csv(DATA_ROOT / 'Intermediate/CompustatAnnual.csv', index=False)
print(f"CompustatAnnual.csv saved with {len(compustat_csv)} records", flush=True)

# Prepare signal inputs while preserving the raw fundamentals extract.
compustat_data = compustat_data_raw.copy()

# Require assets, price, and net income for the accounting-signal sample.
compustat_data = compustat_data.dropna(subset=['at', 'prcc_c', 'ni'])
print(f"After requiring AT, PRCC_C, NI: {len(compustat_data)} records", flush=True)

# Provide the company CUSIP prefix for matching other company datasets.
compustat_data['cnum'] = compustat_data['cusip'].str[:6]

# Recover total deferred revenue from whichever current and long-term components exist.
compustat_data['dr'] = np.nan
has_both_revenue_components = compustat_data['drc'].notna() & compustat_data['drlt'].notna()
compustat_data.loc[has_both_revenue_components, 'dr'] = (
    compustat_data.loc[has_both_revenue_components, 'drc']
    + compustat_data.loc[has_both_revenue_components, 'drlt']
)
has_only_current_revenue = compustat_data['drc'].notna() & compustat_data['drlt'].isna()
compustat_data.loc[has_only_current_revenue, 'dr'] = (
    compustat_data.loc[has_only_current_revenue, 'drc']
)
has_only_long_term_revenue = compustat_data['drc'].isna() & compustat_data['drlt'].notna()
compustat_data.loc[has_only_long_term_revenue, 'dr'] = (
    compustat_data.loc[has_only_long_term_revenue, 'drlt']
)

# Recover convertible debt when the direct measure is unavailable.
compustat_data['dc'] = np.nan
# Separate debt from combined debt/preferred stock when preferred stock is known.
can_separate_convertible_debt = (
    (compustat_data['dcpstk'] > compustat_data['pstk']) &
    compustat_data['pstk'].notna() &
    compustat_data['dcpstk'].notna() &
    compustat_data['dcvt'].isna()
)
compustat_data.loc[can_separate_convertible_debt, 'dc'] = (
    compustat_data.loc[can_separate_convertible_debt, 'dcpstk']
    - compustat_data.loc[can_separate_convertible_debt, 'pstk']
)
# Retain the combined amount when preferred stock cannot be separated.
has_only_combined_debt = (
    compustat_data['pstk'].isna() &
    compustat_data['dcpstk'].notna() &
    compustat_data['dcvt'].isna()
)
compustat_data.loc[has_only_combined_debt, 'dc'] = (
    compustat_data.loc[has_only_combined_debt, 'dcpstk']
)
# Use the reported convertible debt amount wherever an estimate is still missing.
needs_reported_debt = compustat_data['dc'].isna()
compustat_data.loc[needs_reported_debt, 'dc'] = compustat_data.loc[needs_reported_debt, 'dcvt']

# Provide expense measures that treat unreported interest, SG&A, and advertising as zero.
compustat_data['xint0'] = 0.0
compustat_data.loc[compustat_data['xint'].notna(), 'xint0'] = compustat_data['xint']

compustat_data['xsga0'] = 0.0
compustat_data.loc[compustat_data['xsga'].notna(), 'xsga0'] = compustat_data['xsga']

compustat_data['xad0'] = compustat_data['xad'].fillna(0)

# Apply the existing missing-as-zero convention to selected accounting items.
zero_fill_vars = ['nopi', 'dvt', 'ob', 'dm', 'dc', 'aco', 'ap', 'intan', 'ao',
                  'lco', 'lo', 'rect', 'invt', 'drc', 'spi', 'gdwl', 'che',
                  'dp', 'act', 'lct', 'tstkp', 'dvpa', 'scstkc', 'sstk',
                  'mib', 'ivao', 'prstkc', 'prstkcc', 'txditc', 'ivst']

for var in zero_fill_vars:
    compustat_data[var] = compustat_data[var].fillna(0)

# Obtain primary company-security links so each report can be matched to its CRSP stock.
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

ccm_data = pd.read_sql_query(CCM_QUERY, engine)

# Keep stock identifiers and link validity dates consistent with the shared linking table.
ccm_data[['lpermno', 'lpermco']] = ccm_data[['lpermno', 'lpermco']].astype('Int64')
ccm_data[['linkdt', 'linkenddt']] = ccm_data[['linkdt', 'linkenddt']].astype('datetime64[ns]')

ccm_data = ccm_data.rename(columns={
    'linkdt': 'timeLinkStart_d',
    'linkenddt': 'timeLinkEnd_d',
    'lpermno': 'permno',
    'lpermco': 'permco'
})
ccm_data['naics'] = ccm_data['naics'].fillna('')
ccm_data['cik'] = ccm_data['cik'].fillna('')
print(f"CCM linking table loaded with {len(ccm_data)} records", flush=True)

engine.dispose()

# Preserve report-specific company names, tickers, and CUSIPs when adding stock links.
ccm_columns_to_drop = ['conm', 'cusip', 'tic']
ccm_merge_data = ccm_data.drop(columns=[col for col in ccm_columns_to_drop if col in ccm_data.columns])

compustat_data = compustat_data.merge(ccm_merge_data, on='gvkey', how='inner')
print(f"After merging with CCM links: {len(compustat_data)} records", flush=True)

# Keep only stock links valid on the accounting report date.
compustat_data['datadate'] = pd.to_datetime(compustat_data['datadate'])
compustat_data['timeLinkStart_d'] = pd.to_datetime(compustat_data['timeLinkStart_d'])
compustat_data['timeLinkEnd_d'] = pd.to_datetime(compustat_data['timeLinkEnd_d'])

# Treat links without an end date as still valid after their start date.
is_within_link_dates = (
    (compustat_data['timeLinkStart_d'] <= compustat_data['datadate']) &
    ((compustat_data['datadate'] <= compustat_data['timeLinkEnd_d']) |
     compustat_data['timeLinkEnd_d'].isna())
)
compustat_data = compustat_data[is_within_link_dates]
print(f"After filtering for valid link dates: {len(compustat_data)} records", flush=True)

# Require one stock link per report so overlapping histories cannot duplicate signal inputs.
duplicate_links = compustat_data.duplicated(['gvkey', 'datadate'], keep=False)
if duplicate_links.any():
    examples = compustat_data.loc[
        duplicate_links, ['gvkey', 'datadate', 'permno', 'permco']
    ].head(10)
    raise ValueError(
        f"{duplicate_links.sum()} rows have repeated (gvkey, datadate) CCM links; "
        f"inspect link intervals before producing annual data:\n{examples}"
    )

# Produce one linked observation per annual report, with a six-month availability lag.
annual_data = compustat_data.copy()

annual_data = annual_data.drop(columns=['timeLinkStart_d', 'timeLinkEnd_d', 'linkprim', 'liid', 'linktype'])

annual_data['gvkey'] = pd.to_numeric(annual_data['gvkey'])

# Delay use of annual accounts until six months after the report month.
annual_data['time_avail_m'] = (
    annual_data['datadate'].dt.to_period('M') + 6
).dt.to_timestamp()

# Save report-level fundamentals with their first availability month.
annual_data.to_parquet(DATA_ROOT / 'Intermediate/a_aCompustat.parquet', index=False)
print(f"Annual version saved with {len(annual_data)} records", flush=True)

# Carry each annual report across twelve monthly signal dates.
monthly_data = annual_data.copy()

monthly_data = pd.concat([monthly_data] * 12, ignore_index=True)

monthly_data = monthly_data.sort_values(['gvkey', 'time_avail_m']).reset_index(drop=True)
monthly_data['tempTime'] = monthly_data['time_avail_m']
monthly_data['month_offset'] = monthly_data.groupby(['gvkey', 'tempTime']).cumcount()

monthly_data['time_avail_m'] = (
    monthly_data['time_avail_m'].dt.to_period('M') + monthly_data['month_offset']
).dt.to_timestamp()

monthly_data = monthly_data.drop('tempTime', axis=1)

# Prefer the latest report when annual availability windows overlap for a company or stock.
monthly_data = monthly_data.sort_values(['gvkey', 'time_avail_m', 'datadate'])
monthly_data = monthly_data.drop_duplicates(['gvkey', 'time_avail_m'], keep='last')

monthly_data = monthly_data.sort_values(['permno', 'time_avail_m', 'datadate'])
monthly_data = monthly_data.drop_duplicates(['permno', 'time_avail_m'], keep='last')

monthly_data = monthly_data.drop(columns=['month_offset'])

# Save monthly fundamentals, restricting development output to the shared monthly sample.
monthly_data = select_dates(monthly_data, "time_avail_m", "monthly")
monthly_data.to_parquet(DATA_ROOT / 'Intermediate/m_aCompustat.parquet', index=False)
print(f"Monthly version saved with {len(monthly_data)} records", flush=True)

print("=" * 60, flush=True)
print("✅ CompustatAnnual.py completed successfully", flush=True)
print("=" * 60, flush=True)
