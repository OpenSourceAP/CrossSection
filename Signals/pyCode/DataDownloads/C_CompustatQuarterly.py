#!/usr/bin/env python3
"""
Compustat Quarterly data download script.

Python equivalent of C_CompustatQuarterly.do
Downloads Compustat quarterly fundamental data and creates monthly version.
"""

import os
import psycopg2
import pandas as pd
import polars as pl
import numpy as np
from dotenv import load_dotenv

print("=" * 60, flush=True)
print(
    "📊 C_CompustatQuarterly.py - Compustat Quarterly Fundamentals",
    flush=True
)
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
SELECT a.gvkey, a.datadate, a.fyearq, a.fqtr, a.datacqtr,
    a.datafqtr, a.acoq, a.actq,a.ajexq,a.apq,a.atq,a.ceqq,a.cheq,
    a.cogsq,a.cshoq,a.cshprq, a.dlcq,a.dlttq,a.dpq,a.drcq,a.drltq,
    a.dvpsxq,a.dvpq,a.dvy,a.epspiq,a.epspxq,a.fopty, a.gdwlq,a.ibq,
    a.invtq,a.intanq,a.ivaoq,a.lcoq,a.lctq,a.loq,a.ltq,a.mibq,
    a.niq,a.oancfy,a.oiadpq,a.oibdpq,a.piq,a.ppentq,a.ppegtq,
    a.prstkcy,a.prccq, a.pstkq,a.rdq,a.req,a.rectq,a.revtq,
    a.saleq,a.seqq,a.sstky,a.txdiq, a.txditcq,a.txpq,a.txtq,
    a.xaccq,a.xintq,a.xsgaq,a.xrdq, a.capxy
FROM COMP.FUNDQ as a
WHERE a.consol = 'C'
AND a.popsrc = 'D'
AND a.datafmt = 'STD'
AND a.curcdq = 'USD'
AND a.indfmt = 'INDL'
"""

# Load data with pandas first
compustat_q_pd = pd.read_sql_query(QUERY, conn)
conn.close()

print(f"Downloaded {len(compustat_q_pd):,} quarterly records", flush=True)

# Convert to polars for much faster processing
compustat_q = pl.from_pandas(compustat_q_pd)
del compustat_q_pd  # Free memory

# Ensure directories exist
os.makedirs("../pyData/Intermediate", exist_ok=True)

print("Processing with Polars for optimal performance...", flush=True)

# Keep only the most recent data for each fiscal quarter
# (equivalent to bys gvkey fyearq fqtr (datadate): keep if _n == _N)
compustat_q = (
    compustat_q
    .sort(['gvkey', 'fyearq', 'fqtr', 'datadate'])
    .group_by(['gvkey', 'fyearq', 'fqtr'])
    .last()
)

print(f"After removing duplicates: {len(compustat_q):,} records", flush=True)

# Data availability assumed with 3 month lag and patch with rdq
# (equivalent to gen time_avail_m = mofd(datadate) + 3)
compustat_q = compustat_q.with_columns([
    # Add 3 months to datadate
    (pl.col('datadate') + pl.duration(days=90)).alias('time_avail_m'),
    # Convert dates to proper datetime
    pl.col('datadate').cast(pl.Date),
    pl.col('rdq').cast(pl.Date)
])

# Patch cases with earlier data availability using rdq
# (equivalent to replace time_avail_m = mofd(rdq) if !mi(rdq) & mofd(rdq) > time_avail_m)
compustat_q = compustat_q.with_columns(
    pl.when(
        pl.col('rdq').is_not_null() & 
        (pl.col('rdq') > pl.col('time_avail_m'))
    )
    .then(pl.col('rdq'))
    .otherwise(pl.col('time_avail_m'))
    .alias('time_avail_m')
)

# Drop cases with very late release (> 6 months)
# (equivalent to drop if mofd(rdq) - mofd(datadate) > 6 & !mi(rdq))
compustat_q = compustat_q.filter(
    ~(
        pl.col('rdq').is_not_null() &
        ((pl.col('rdq') - pl.col('datadate')).dt.total_days() > 180)
    )
)

print(f"After removing late releases: {len(compustat_q):,} records", flush=True)

# Keep most recent info for same gvkey/time_avail_m combinations
# (equivalent to bys gvkey time_avail_m (datadate): keep if _n == _N)
compustat_q = (
    compustat_q
    .sort(['gvkey', 'time_avail_m', 'datadate'])
    .group_by(['gvkey', 'time_avail_m'])
    .last()
)

print(f"After removing time duplicates: {len(compustat_q):,} records", flush=True)

# For these variables, missing is assumed to be 0
zero_fill_vars = [
    'acoq', 'actq', 'apq', 'cheq', 'dpq', 'drcq', 'invtq', 'intanq',
    'ivaoq', 'gdwlq', 'lcoq', 'lctq', 'loq', 'mibq', 'prstkcy',
    'rectq', 'sstky', 'txditcq'
]

# Fill missing values with 0 using polars
zero_fill_exprs = [
    pl.col(var).fill_null(0) for var in zero_fill_vars if var in compustat_q.columns
]
if zero_fill_exprs:
    compustat_q = compustat_q.with_columns(zero_fill_exprs)

# Prepare year-to-date items (convert to quarterly) - OPTIMIZED WITH POLARS
print("Converting year-to-date items to quarterly...", flush=True)
compustat_q = compustat_q.sort(['gvkey', 'fyearq', 'fqtr'])

ytd_vars = ['sstky', 'prstkcy', 'oancfy', 'fopty']
ytd_exprs = []

for var in ytd_vars:
    if var in compustat_q.columns:
        var_q = var + 'q'
        
        # Create quarterly version: Q1 gets full value, Q2-Q4 get difference from previous
        ytd_exprs.append(
            pl.when(pl.col('fqtr') == 1)
            .then(pl.col(var))
            .otherwise(
                pl.col(var) - pl.col(var).shift(1).over(['gvkey', 'fyearq'])
            )
            .alias(var_q)
        )

if ytd_exprs:
    compustat_q = compustat_q.with_columns(ytd_exprs)

# Convert to monthly by expanding each quarter to 3 months
print("Expanding quarterly data to monthly...", flush=True)

# Create month offsets (0, 1, 2) for expansion
month_offsets = pl.Series("month_offset", [0, 1, 2])

# Cross join with month offsets to expand
monthly_compustat = compustat_q.join(
    pl.DataFrame({"month_offset": month_offsets}),
    how="cross"
)

# Update time_avail_m with the month offset
monthly_compustat = monthly_compustat.with_columns(
    (pl.col('time_avail_m') + pl.duration(days=pl.col('month_offset') * 30)).alias('time_avail_m')
)

# Remove the month_offset column
monthly_compustat = monthly_compustat.drop('month_offset')

print(f"Expanded to {len(monthly_compustat):,} monthly records", flush=True)

# Keep most recent info for same gvkey/time_avail_m after expansion
# (equivalent to bysort gvkey time_avail_m (datadate): keep if _n == _N)
monthly_compustat = (
    monthly_compustat
    .sort(['gvkey', 'time_avail_m', 'datadate'])
    .group_by(['gvkey', 'time_avail_m'])
    .last()
)

# Rename datadate to datadateq and convert gvkey to numeric
monthly_compustat = monthly_compustat.with_columns([
    pl.col('gvkey').cast(pl.Int64),
    pl.col('datadate').alias('datadateq')
]).drop('datadate')

# Convert back to pandas for saving (polars parquet support is excellent)
monthly_compustat_pd = monthly_compustat.to_pandas()

# Convert time_avail_m to period for pandas compatibility
monthly_compustat_pd['time_avail_m'] = pd.to_datetime(monthly_compustat_pd['time_avail_m']).dt.to_period('M')

# Save the data in both pickle and parquet formats
monthly_compustat_pd.to_pickle("../pyData/Intermediate/m_QCompustat.pkl")
monthly_compustat_pd.to_parquet("../pyData/Intermediate/CompustatQuarterly.parquet")

print(
    f"Compustat Quarterly data saved with "
    f"{len(monthly_compustat_pd):,} monthly records", flush=True
)
print(
    f"Date range: {monthly_compustat_pd['time_avail_m'].min()} to "
    f"{monthly_compustat_pd['time_avail_m'].max()}", flush=True
)
print("=" * 60, flush=True)
print("✅ C_CompustatQuarterly.py completed successfully", flush=True)
print("=" * 60, flush=True)
