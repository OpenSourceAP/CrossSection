# ABOUTME: Downloads Compustat quarterly fundamental data and expands to monthly availability
# ABOUTME: Processes quarterly data with proper timing lags and converts YTD items to quarterly
"""
Inputs:
- comp.fundq (Compustat quarterly fundamentals from WRDS)

Outputs:
- ../pyData/Intermediate/m_QCompustat.parquet
- ../pyData/Intermediate/CompustatQuarterly.parquet

How to run: python3 C_CompustatQuarterly.py
"""

# Import required libraries
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

# Print script header
print("=" * 60, flush=True)
print(
    "📊 C_CompustatQuarterly.py - Compustat Quarterly Fundamentals",
    flush=True
)
print("=" * 60, flush=True)

# Load environment variables and create database connection
load_dotenv()
engine = create_engine(
    f"postgresql://{os.getenv('WRDS_USERNAME')}:{os.getenv('WRDS_PASSWORD')}@wrds-pgdata.wharton.upenn.edu:9737/wrds"
)

# Define SQL query to download quarterly fundamental data
# Filters for consolidated (C), primary (D), standardized (STD), USD, industrial format
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

# Apply debug row limit if configured
if MAX_ROWS_DL > 0:
    QUERY += f" LIMIT {MAX_ROWS_DL}"
    print(f"DEBUG MODE: Limiting to {MAX_ROWS_DL} rows", flush=True)

# Download data from WRDS and convert to polars for faster processing
compustat_q_pd = pd.read_sql_query(QUERY, engine)
engine.dispose()
print(f"Downloaded {len(compustat_q_pd):,} quarterly records", flush=True)
compustat_q = pl.from_pandas(compustat_q_pd)
del compustat_q_pd

# Create output directory
os.makedirs("../pyData/Intermediate", exist_ok=True)

print("Processing with Polars for optimal performance...", flush=True)

# Remove duplicate records by keeping most recent data for each fiscal quarter
compustat_q = (
    compustat_q
    .sort(['gvkey', 'fyearq', 'fqtr', 'datadate'])
    .group_by(['gvkey', 'fyearq', 'fqtr'])
    .last()
)
print(f"After removing duplicates: {len(compustat_q):,} records", flush=True)

# Calculate data availability timing with 3-month lag assumption
compustat_q = compustat_q.with_columns([
    pl.col('datadate').cast(pl.Date),
    pl.col('rdq').cast(pl.Date)
])

# Convert to pandas for period arithmetic to match Stata's mofd() + 3 behavior
temp_df = compustat_q.to_pandas()
temp_df['time_avail_m'] = (
    temp_df['datadate'].dt.to_period('M') + 3
).dt.to_timestamp()
compustat_q = pl.from_pandas(temp_df)
del temp_df

# Adjust availability timing using actual filing dates when later than 3-month assumption
temp_df = compustat_q.to_pandas()
rdq_monthly = temp_df['rdq'].dt.to_period('M').dt.to_timestamp()
mask = temp_df['rdq'].notna() & (rdq_monthly > temp_df['time_avail_m'])
temp_df.loc[mask, 'time_avail_m'] = rdq_monthly[mask]
compustat_q = pl.from_pandas(temp_df)
del temp_df

# Remove records with excessively late filings (> 6 months after quarter end)
temp_df = compustat_q.to_pandas()
rdq_months = temp_df['rdq'].dt.to_period('M')
datadate_months = temp_df['datadate'].dt.to_period('M')
month_diff = (rdq_months - datadate_months).apply(lambda x: x.n if pd.notna(x) else 0)
drop_mask = temp_df['rdq'].notna() & (month_diff > 6)
temp_df = temp_df[~drop_mask]
compustat_q = pl.from_pandas(temp_df)
del temp_df
print(f"After removing late releases: {len(compustat_q):,} records", flush=True)

# Remove duplicates by keeping most recent data for each company-month combination
compustat_q = (
    compustat_q
    .sort(['gvkey', 'time_avail_m', 'datadate'])
    .group_by(['gvkey', 'time_avail_m'])
    .last()
)

print(f"After removing time duplicates: {len(compustat_q):,} records", flush=True)

# Fill missing values with zero for balance sheet and cash flow variables
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

# Convert year-to-date items to quarterly by taking differences
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

# Expand quarterly data to monthly by creating 3 monthly records per quarter
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

# Standardize column names and data types using YAML schema
monthly_compustat_pd = standardize_columns(monthly_compustat_pd, "m_QCompustat")

# Save data to parquet files with timestamp precision matching Stata
monthly_compustat_pd.to_parquet("../pyData/Intermediate/m_QCompustat.parquet", index=False, use_deprecated_int96_timestamps=True)
monthly_compustat_pd.to_parquet("../pyData/Intermediate/CompustatQuarterly.parquet", index=False, use_deprecated_int96_timestamps=True)

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
