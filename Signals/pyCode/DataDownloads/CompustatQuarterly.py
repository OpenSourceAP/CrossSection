# ABOUTME: Downloads Compustat quarterly fundamental data and expands to monthly availability
# ABOUTME: Processes quarterly data with proper timing lags and converts YTD items to quarterly
"""
Inputs:
- comp.fundq (Compustat quarterly fundamentals from WRDS)

Outputs:
- ../pyData/Intermediate/m_QCompustat.parquet
- ../pyData/Intermediate/CompustatQuarterly.parquet

How to run: from Signals/pyCode, run python3 DataDownloads/CompustatQuarterly.py

Use the project Python environment at /opt/venv/projects/openap.
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
from config import DEBUG_MODE
from utils.debug_mode import get_debug_row_limit

DEBUG_ROWS = get_debug_row_limit("CompustatQuarterly")

print("=" * 60, flush=True)
print(
    "📊 CompustatQuarterly.py - Compustat Quarterly Fundamentals",
    flush=True
)
print("=" * 60, flush=True)

load_dotenv()
engine = create_engine(
    f"postgresql://{os.getenv('WRDS_USERNAME')}:{os.getenv('WRDS_PASSWORD')}@wrds-pgdata.wharton.upenn.edu:9737/wrds"
)

# Obtain standardized, consolidated USD industrial accounts for comparable quarterly fundamentals.
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
if DEBUG_MODE:
    QUERY += f" LIMIT {DEBUG_ROWS}"
    print(f"DEBUG MODE: Limiting to {DEBUG_ROWS} rows", flush=True)

# Load quarterly fundamentals for the monthly accounting-signal panel.
compustat_q_pd = pd.read_sql_query(QUERY, engine)
engine.dispose()
print(f"Downloaded {len(compustat_q_pd):,} quarterly records", flush=True)
compustat_q = pl.from_pandas(compustat_q_pd)
del compustat_q_pd

print("Processing with Polars for optimal performance...", flush=True)

# Keep the latest fiscal quarter-end date when a company has several records for one fiscal quarter.
compustat_q = (
    compustat_q
    .sort(['gvkey', 'fyearq', 'fqtr', 'datadate'])
    .group_by(['gvkey', 'fyearq', 'fqtr'])
    .last()
)
print(f"After removing duplicates: {len(compustat_q):,} records", flush=True)

# Set quarterly accounts to become available three months after the fiscal quarter-end month.
compustat_q = compustat_q.with_columns([
    pl.col('datadate').cast(pl.Date),
    pl.col('rdq').cast(pl.Date)
])

temp_df = compustat_q.to_pandas()
temp_df['time_avail_m'] = (
    temp_df['datadate'].dt.to_period('M') + 3
).dt.to_timestamp()
compustat_q = pl.from_pandas(temp_df)
del temp_df

# Delay availability further when the earnings announcement occurs after the assumed lag.
temp_df = compustat_q.to_pandas()
rdq_monthly = temp_df['rdq'].dt.to_period('M').dt.to_timestamp()
has_later_announcement = temp_df['rdq'].notna() & (rdq_monthly > temp_df['time_avail_m'])
temp_df.loc[has_later_announcement, 'time_avail_m'] = rdq_monthly[has_later_announcement]
compustat_q = pl.from_pandas(temp_df)
del temp_df

# Exclude reports announced more than six months after the quarter-end month.
temp_df = compustat_q.to_pandas()
rdq_months = temp_df['rdq'].dt.to_period('M')
datadate_months = temp_df['datadate'].dt.to_period('M')
month_diff = (rdq_months - datadate_months).apply(lambda x: x.n if pd.notna(x) else 0)
is_excessively_late = temp_df['rdq'].notna() & (month_diff > 6)
temp_df = temp_df[~is_excessively_late]
compustat_q = pl.from_pandas(temp_df)
del temp_df
print(f"After removing late releases: {len(compustat_q):,} records", flush=True)

# Prefer the latest report when several quarters first become available in the same month.
compustat_q = (
    compustat_q
    .sort(['gvkey', 'time_avail_m', 'datadate'])
    .group_by(['gvkey', 'time_avail_m'])
    .last()
)

print(f"After removing time duplicates: {len(compustat_q):,} records", flush=True)

# Apply the existing missing-as-zero convention to selected balance-sheet and cash-flow items.
zero_fill_vars = [
    'acoq', 'actq', 'apq', 'cheq', 'dpq', 'drcq', 'invtq', 'intanq',
    'ivaoq', 'gdwlq', 'lcoq', 'lctq', 'loq', 'mibq', 'prstkcy',
    'rectq', 'sstky', 'txditcq'
]

zero_fill_exprs = []
for var in zero_fill_vars:
    if var in compustat_q.columns:
        if var == 'ivaoq':
            # Keep investment amounts in the floating-point format expected downstream.
            zero_fill_exprs.append(pl.col(var).fill_null(0).cast(pl.Float64))
        else:
            zero_fill_exprs.append(pl.col(var).fill_null(0))

if zero_fill_exprs:
    compustat_q = compustat_q.with_columns(zero_fill_exprs)

# Recover individual-quarter flows from cumulative fiscal-year totals.
print("Converting year-to-date items to quarterly...", flush=True)
compustat_q = compustat_q.sort(['gvkey', 'fyearq', 'fqtr'])

ytd_vars = ['sstky', 'prstkcy', 'oancfy', 'fopty']
ytd_exprs = []

for var in ytd_vars:
    if var in compustat_q.columns:
        var_q = var + 'q'

        # Q1 is already quarterly; later quarters exclude earlier year-to-date amounts.
        current_ytd = pl.col(var).cast(pl.Float64)
        previous_ytd = current_ytd.shift(1).over(['gvkey', 'fyearq'])
        ytd_exprs.append(
            pl.when(pl.col('fqtr') == 1)
            .then(current_ytd)
            .otherwise(current_ytd - previous_ytd)
            .alias(var_q)
        )

if ytd_exprs:
    compustat_q = compustat_q.with_columns(ytd_exprs)

# Carry each quarterly report across three monthly signal dates.
print("Expanding quarterly data to monthly...", flush=True)

month_offsets = pl.Series("month_offset", [0, 1, 2])

monthly_compustat = compustat_q.join(
    pl.DataFrame({"month_offset": month_offsets}),
    how="cross"
)

temp_df = monthly_compustat.to_pandas()
# Advance availability by calendar months so different month lengths do not shift signal dates.
temp_df['time_avail_m'] = (
    temp_df['time_avail_m'].dt.to_period('M') + temp_df['month_offset']
).dt.to_timestamp()

monthly_compustat = pl.from_pandas(temp_df).drop('month_offset')
del temp_df

print(f"Expanded to {len(monthly_compustat):,} monthly records", flush=True)

# Prefer the latest report where quarterly availability windows overlap.
monthly_compustat = (
    monthly_compustat
    .sort(['gvkey', 'time_avail_m', 'datadate'])
    .group_by(['gvkey', 'time_avail_m'])
    .last()
)

# Distinguish fiscal quarter-end dates from annual accounting dates in downstream joins.
monthly_compustat = monthly_compustat.with_columns([
    pl.col('gvkey').cast(pl.Int64),
    pl.col('datadate').alias('datadateq')
]).drop('datadate')

monthly_compustat_pd = monthly_compustat.to_pandas()

# Save the same monthly quarterly-fundamentals panel under both downstream filenames.
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
print("✅ CompustatQuarterly.py completed successfully", flush=True)
print("=" * 60, flush=True)
