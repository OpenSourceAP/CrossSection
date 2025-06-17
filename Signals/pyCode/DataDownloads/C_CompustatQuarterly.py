#!/usr/bin/env python3
"""
Compustat Quarterly data download script - Python equivalent of C_CompustatQuarterly.do

Downloads Compustat quarterly fundamental data and creates monthly version.
"""

import os
import psycopg2
import pandas as pd
import numpy as np
from dotenv import load_dotenv

print("=" * 60, flush=True)
print("📊 C_CompustatQuarterly.py - Compustat Quarterly Fundamentals", flush=True)
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
SELECT a.gvkey, a.datadate, a.fyearq, a.fqtr, a.datacqtr, a.datafqtr, a.acoq,
    a.actq,a.ajexq,a.apq,a.atq,a.ceqq,a.cheq,a.cogsq,a.cshoq,a.cshprq,
    a.dlcq,a.dlttq,a.dpq,a.drcq,a.drltq,a.dvpsxq,a.dvpq,a.dvy,a.epspiq,a.epspxq,a.fopty,
    a.gdwlq,a.ibq,a.invtq,a.intanq,a.ivaoq,a.lcoq,a.lctq,a.loq,a.ltq,a.mibq,
    a.niq,a.oancfy,a.oiadpq,a.oibdpq,a.piq,a.ppentq,a.ppegtq,a.prstkcy,a.prccq,
    a.pstkq,a.rdq,a.req,a.rectq,a.revtq,a.saleq,a.seqq,a.sstky,a.txdiq,
    a.txditcq,a.txpq,a.txtq,a.xaccq,a.xintq,a.xsgaq,a.xrdq, a.capxy
FROM COMP.FUNDQ as a
WHERE a.consol = 'C'
AND a.popsrc = 'D'
AND a.datafmt = 'STD'
AND a.curcdq = 'USD'
AND a.indfmt = 'INDL'
"""

compustat_q = pd.read_sql_query(QUERY, conn)
conn.close()

print(f"Downloaded {len(compustat_q)} quarterly records")

# Ensure directories exist
os.makedirs("../pyData/Intermediate", exist_ok=True)

# Convert dates to datetime
compustat_q['datadate'] = pd.to_datetime(compustat_q['datadate'])
compustat_q['rdq'] = pd.to_datetime(compustat_q['rdq'])

# Keep only the most recent data for each fiscal quarter
# (equivalent to bys gvkey fyearq fqtr (datadate): keep if _n == _N)
compustat_q = compustat_q.sort_values(['gvkey', 'fyearq', 'fqtr', 'datadate'])
compustat_q = compustat_q.drop_duplicates(['gvkey', 'fyearq', 'fqtr'], keep='last')

print(f"After removing duplicates: {len(compustat_q)} records")

# Data availability assumed with 3 month lag
# (equivalent to gen time_avail_m = mofd(datadate) + 3)
compustat_q['time_avail_m'] = compustat_q['datadate'] + pd.DateOffset(months=3)

# Patch cases with earlier data availability using rdq
# (equivalent to replace time_avail_m = mofd(rdq) if !mi(rdq) & mofd(rdq) > time_avail_m)
rdq_available = compustat_q['rdq'].notna()
rdq_later = compustat_q['rdq'] + pd.DateOffset(months=0) > compustat_q['time_avail_m']
mask = rdq_available & rdq_later
compustat_q.loc[mask, 'time_avail_m'] = compustat_q.loc[mask, 'rdq']

# Drop cases with very late release (> 6 months)
# (equivalent to drop if mofd(rdq) - mofd(datadate) > 6 & !mi(rdq))
rdq_not_missing = compustat_q['rdq'].notna()
late_release = (compustat_q['rdq'] - compustat_q['datadate']).dt.days > 180  # ~6 months
drop_mask = rdq_not_missing & late_release
compustat_q = compustat_q[~drop_mask]

print(f"After removing late releases: {len(compustat_q)} records")

# Convert time_avail_m to period for consistency
compustat_q['time_avail_m'] = compustat_q['time_avail_m'].dt.to_period('M')

# Keep most recent info for same gvkey/time_avail_m combinations
# (equivalent to bys gvkey time_avail_m (datadate): keep if _n == _N)
compustat_q = compustat_q.sort_values(['gvkey', 'time_avail_m', 'datadate'])
compustat_q = compustat_q.drop_duplicates(['gvkey', 'time_avail_m'], keep='last')

print(f"After removing time duplicates: {len(compustat_q)} records")

# For these variables, missing is assumed to be 0
zero_fill_vars = ['acoq', 'actq', 'apq', 'cheq', 'dpq', 'drcq', 'invtq', 'intanq', 'ivaoq',
                  'gdwlq', 'lcoq', 'lctq', 'loq', 'mibq', 'prstkcy', 'rectq', 'sstky', 'txditcq']

for var in zero_fill_vars:
    if var in compustat_q.columns:
        compustat_q[var] = compustat_q[var].fillna(0)

# Prepare year-to-date items (convert to quarterly)
# Sort by gvkey, fyearq, fqtr for proper calculation
compustat_q = compustat_q.sort_values(['gvkey', 'fyearq', 'fqtr'])

ytd_vars = ['sstky', 'prstkcy', 'oancfy', 'fopty']
for var in ytd_vars:
    if var in compustat_q.columns:
        # Create quarterly version
        var_q = var + 'q'
        
        # First quarter gets the full value
        compustat_q[var_q] = compustat_q[var].where(compustat_q['fqtr'] == 1)
        
        # For other quarters, subtract previous quarter's cumulative value
        for fqtr in [2, 3, 4]:
            mask = compustat_q['fqtr'] == fqtr
            if mask.any():
                # Get previous quarter's cumulative value
                prev_mask = compustat_q['fqtr'] == (fqtr - 1)
                
                # For each gvkey/fyearq combination
                for gvkey, fyearq in compustat_q[mask][['gvkey', 'fyearq']].drop_duplicates().values:
                    curr_idx = compustat_q[(compustat_q['gvkey'] == gvkey) & 
                                          (compustat_q['fyearq'] == fyearq) & 
                                          (compustat_q['fqtr'] == fqtr)].index
                    prev_idx = compustat_q[(compustat_q['gvkey'] == gvkey) & 
                                          (compustat_q['fyearq'] == fyearq) & 
                                          (compustat_q['fqtr'] == (fqtr - 1))].index
                    
                    if len(curr_idx) > 0 and len(prev_idx) > 0:
                        curr_val = compustat_q.loc[curr_idx[0], var]
                        prev_val = compustat_q.loc[prev_idx[0], var]
                        if pd.notna(curr_val) and pd.notna(prev_val):
                            compustat_q.loc[curr_idx[0], var_q] = curr_val - prev_val

# Convert to monthly by expanding each quarter to 3 months
print("Expanding quarterly data to monthly...")

# Create expanded dataset
monthly_data = []
for _, row in compustat_q.iterrows():
    for month_offset in range(3):  # 0, 1, 2 for 3 months
        new_row = row.copy()
        new_row['time_avail_m'] = row['time_avail_m'] + month_offset
        monthly_data.append(new_row)

monthly_compustat = pd.DataFrame(monthly_data)

print(f"Expanded to {len(monthly_compustat)} monthly records")

# Keep most recent info for same gvkey/time_avail_m after expansion
monthly_compustat = monthly_compustat.sort_values(['gvkey', 'time_avail_m', 'datadate'])
monthly_compustat = monthly_compustat.drop_duplicates(['gvkey', 'time_avail_m'], keep='last')

# Rename datadate to datadateq
monthly_compustat = monthly_compustat.rename(columns={'datadate': 'datadateq'})

# Convert gvkey to numeric
monthly_compustat['gvkey'] = pd.to_numeric(monthly_compustat['gvkey'])

# Save the data
monthly_compustat.to_pickle("../pyData/Intermediate/m_QCompustat.pkl")

print(f"Compustat Quarterly data saved with {len(monthly_compustat)} monthly records", flush=True)
print(f"Date range: {monthly_compustat['time_avail_m'].min()} to {monthly_compustat['time_avail_m'].max()}", flush=True)
print("=" * 60, flush=True)
print("✅ C_CompustatQuarterly.py completed successfully", flush=True)
print("=" * 60, flush=True)