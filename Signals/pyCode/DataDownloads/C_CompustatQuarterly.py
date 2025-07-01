#!/usr/bin/env python3
"""
Compustat Quarterly data download script.

Python equivalent of C_CompustatQuarterly.do
Downloads Compustat quarterly fundamental data and creates monthly version.

tbc: check ivaoq is at least sometimes stored as int64 instead of float64
"""

import os
import pandas as pd
import polars as pl
import numpy as np
from dotenv import load_dotenv
from sqlalchemy import create_engine
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from config import MAX_ROWS_DL
from utils.column_standardizer_yaml import standardize_columns

print("=" * 60, flush=True)
print(
    "📊 C_CompustatQuarterly.py - Compustat Quarterly Fundamentals",
    flush=True
)
print("=" * 60, flush=True)

load_dotenv()

# Create SQLAlchemy engine for database connection
engine = create_engine(
    f"postgresql://{os.getenv('WRDS_USERNAME')}:{os.getenv('WRDS_PASSWORD')}@wrds-pgdata.wharton.upenn.edu:9737/wrds"
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

# Add row limit for debugging if configured
if MAX_ROWS_DL > 0:
    QUERY += f" LIMIT {MAX_ROWS_DL}"
    print(f"DEBUG MODE: Limiting to {MAX_ROWS_DL} rows", flush=True)

# Load data with pandas first
compustat_q_pd = pd.read_sql_query(QUERY, engine)
engine.dispose()

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
# Note: Stata's mofd() + 3 creates beginning-of-month dates
compustat_q = compustat_q.with_columns([
    # Convert dates to proper datetime first
    pl.col('datadate').cast(pl.Date),
    pl.col('rdq').cast(pl.Date)
])

# Convert to pandas temporarily for proper period arithmetic (matching Stata's mofd() behavior)
temp_df = compustat_q.to_pandas()
# Replicate Stata's mofd(datadate) + 3 logic: beginning-of-month + 3 months
temp_df['time_avail_m'] = (
    temp_df['datadate'].dt.to_period('M') + 3
).dt.to_timestamp()

# Convert back to polars
compustat_q = pl.from_pandas(temp_df)
del temp_df  # Free memory

# Patch cases with later data availability using rdq
# (equivalent to replace time_avail_m = mofd(rdq) if !mi(rdq) & mofd(rdq) > time_avail_m)
# This handles cases where actual filing date is later than the 3-month assumption
temp_df = compustat_q.to_pandas()
# Apply Stata's mofd() logic to rdq as well
rdq_monthly = temp_df['rdq'].dt.to_period('M').dt.to_timestamp()
# Update time_avail_m with rdq if rdq is not null and rdq > time_avail_m
mask = temp_df['rdq'].notna() & (rdq_monthly > temp_df['time_avail_m'])
temp_df.loc[mask, 'time_avail_m'] = rdq_monthly[mask]

# Convert back to polars
compustat_q = pl.from_pandas(temp_df)
del temp_df  # Free memory

# Drop cases with very late release (> 6 months)
# (equivalent to drop if mofd(rdq) - mofd(datadate) > 6 & !mi(rdq))
# Need to convert to pandas temporarily to replicate Stata's month arithmetic
temp_df = compustat_q.to_pandas()
# Calculate month difference using period arithmetic to match Stata exactly
rdq_months = temp_df['rdq'].dt.to_period('M')
datadate_months = temp_df['datadate'].dt.to_period('M')
# Convert period difference to integer months
month_diff = (rdq_months - datadate_months).apply(lambda x: x.n if pd.notna(x) else 0)
# Drop rows where month difference > 6 and rdq is not null
drop_mask = temp_df['rdq'].notna() & (month_diff > 6)
temp_df = temp_df[~drop_mask]
# Convert back to polars
compustat_q = pl.from_pandas(temp_df)
del temp_df  # Free memory

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
zero_fill_exprs = []
for var in zero_fill_vars:
    if var in compustat_q.columns:
        if var == 'ivaoq':
            # Explicit float casting for ivaoq to match Stata's float64 type
            zero_fill_exprs.append(pl.col(var).fill_null(0).cast(pl.Float64))
        else:
            zero_fill_exprs.append(pl.col(var).fill_null(0))

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
            .then(pl.col(var).cast(pl.Float64))
            .otherwise(
                pl.col(var).cast(pl.Float64) - pl.col(var).cast(pl.Float64).shift(1).over(['gvkey', 'fyearq'])
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

# Convert to pandas temporarily for proper monthly period arithmetic
temp_df = monthly_compustat.to_pandas()
# Apply proper monthly period arithmetic instead of days-based calculation
# This matches Stata's exact monthly arithmetic
temp_df['time_avail_m'] = (
    temp_df['time_avail_m'].dt.to_period('M') + temp_df['month_offset']
).dt.to_timestamp()

# Convert back to polars and remove the month_offset column
monthly_compustat = pl.from_pandas(temp_df).drop('month_offset')
del temp_df  # Free memory

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

# time_avail_m is already in proper datetime64[ns] format from period arithmetic above
# No additional conversion needed - it already matches Stata's format

# Standardize columns using YAML schema
monthly_compustat_pd = standardize_columns(monthly_compustat_pd, "m_QCompustat")

# Save the data in both pickle and parquet formats
monthly_compustat_pd.to_parquet("../pyData/Intermediate/m_QCompustat.parquet", index=False)
monthly_compustat_pd.to_parquet("../pyData/Intermediate/CompustatQuarterly.parquet", index=False)

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
