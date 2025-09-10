# ABOUTME: Downloads Compustat quarterly fundamental data and processes it into monthly format
# ABOUTME: Handles quarterly-to-monthly expansion, duplicate removal, and late reporting adjustments
"""
Inputs:
- COMP.FUNDQ (Compustat quarterly fundamentals via WRDS)

Outputs:
- ../pyData/Intermediate/m_QCompustat.parquet
- ../pyData/Intermediate/CompustatQuarterly.parquet

How to run: python3 C_CompustatQuarterly.py
"""

import os
import pandas as pd
import polars as pl
from dotenv import load_dotenv
from sqlalchemy import create_engine
import sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from config import MAX_ROWS_DL
from utils.column_standardizer_yaml import standardize_columns

print("=" * 60)
print("📊 C_CompustatQuarterly.py - Compustat Quarterly Fundamentals")
print("=" * 60)

load_dotenv()
engine = create_engine(f"postgresql://{os.getenv('WRDS_USERNAME')}:{os.getenv('WRDS_PASSWORD')}@wrds-pgdata.wharton.upenn.edu:9737/wrds")

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
WHERE a.consol = 'C' AND a.popsrc = 'D' AND a.datafmt = 'STD' AND a.curcdq = 'USD' AND a.indfmt = 'INDL'
"""

if MAX_ROWS_DL > 0:
    QUERY += f" LIMIT {MAX_ROWS_DL}"
    print(f"DEBUG MODE: Limiting to {MAX_ROWS_DL} rows")

compustat_q_pd = pd.read_sql_query(QUERY, engine)
engine.dispose()
print(f"Downloaded {len(compustat_q_pd):,} quarterly records")

os.makedirs("../pyData/Intermediate", exist_ok=True)
compustat_q = (
    pl.from_pandas(compustat_q_pd)
    .sort(['gvkey', 'fyearq', 'fqtr', 'datadate'])
    .group_by(['gvkey', 'fyearq', 'fqtr'])
    .last()
    .with_columns([
        pl.col('datadate').cast(pl.Date),
        pl.col('rdq').cast(pl.Date)
    ])
)
del compustat_q_pd
print(f"After removing duplicates: {len(compustat_q):,} records")

# Calculate time availability and drop late releases
temp_df = compustat_q.to_pandas()
temp_df['time_avail_m'] = (temp_df['datadate'].dt.to_period('M') + 3).dt.to_timestamp()
rdq_monthly = temp_df['rdq'].dt.to_period('M').dt.to_timestamp()
mask = temp_df['rdq'].notna() & (rdq_monthly > temp_df['time_avail_m'])
temp_df.loc[mask, 'time_avail_m'] = rdq_monthly[mask]

# Drop late releases (> 6 months after quarter end)
month_diff = (temp_df['rdq'].dt.to_period('M') - temp_df['datadate'].dt.to_period('M')).apply(lambda x: x.n if pd.notna(x) else 0)
temp_df = temp_df[~(temp_df['rdq'].notna() & (month_diff > 6))]

compustat_q = (
    pl.from_pandas(temp_df)
    .sort(['gvkey', 'time_avail_m', 'datadate'])
    .group_by(['gvkey', 'time_avail_m'])
    .last()
    .with_columns([
        pl.col(var).fill_null(0).cast(pl.Float64) if var == 'ivaoq' else pl.col(var).fill_null(0)
        for var in ['acoq', 'actq', 'apq', 'cheq', 'dpq', 'drcq', 'invtq', 'intanq', 'ivaoq', 'gdwlq', 'lcoq', 'lctq', 'loq', 'mibq', 'prstkcy', 'rectq', 'sstky', 'txditcq']
        if var in compustat_q.columns
    ])
    .sort(['gvkey', 'fyearq', 'fqtr'])
    .with_columns([
        pl.when(pl.col('fqtr') == 1)
        .then(pl.col(var).cast(pl.Float64))
        .otherwise(pl.col(var).cast(pl.Float64) - pl.col(var).cast(pl.Float64).shift(1).over(['gvkey', 'fyearq']))
        .alias(var + 'q')
        for var in ['sstky', 'prstkcy', 'oancfy', 'fopty'] if var in compustat_q.columns
    ])
)
del temp_df
print(f"After processing: {len(compustat_q):,} records")

# Expand quarterly data to monthly
monthly_compustat = compustat_q.join(pl.DataFrame({"month_offset": [0, 1, 2]}), how="cross")
temp_df = monthly_compustat.to_pandas()
temp_df['time_avail_m'] = (temp_df['time_avail_m'].dt.to_period('M') + temp_df['month_offset']).dt.to_timestamp()

monthly_compustat = (
    pl.from_pandas(temp_df)
    .drop('month_offset')
    .sort(['gvkey', 'time_avail_m', 'datadate'])
    .group_by(['gvkey', 'time_avail_m'])
    .last()
    .with_columns([
        pl.col('gvkey').cast(pl.Int64),
        pl.col('datadate').alias('datadateq')
    ])
    .drop('datadate')
)
del temp_df
print(f"Expanded to {len(monthly_compustat):,} monthly records")

# Save output files
monthly_compustat_pd = standardize_columns(monthly_compustat.to_pandas(), "m_QCompustat")
monthly_compustat_pd.to_parquet("../pyData/Intermediate/m_QCompustat.parquet", index=False, use_deprecated_int96_timestamps=True)
monthly_compustat_pd.to_parquet("../pyData/Intermediate/CompustatQuarterly.parquet", index=False, use_deprecated_int96_timestamps=True)

print(f"Compustat Quarterly data saved with {len(monthly_compustat_pd):,} monthly records")
print(f"Date range: {monthly_compustat_pd['time_avail_m'].min()} to {monthly_compustat_pd['time_avail_m'].max()}")
print("=" * 60)
print("✅ C_CompustatQuarterly.py completed successfully")
print("=" * 60)
