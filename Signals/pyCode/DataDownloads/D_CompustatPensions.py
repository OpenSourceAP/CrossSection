#!/usr/bin/env python3
"""
Compustat Pensions data download script - Python equivalent of D_CompustatPensions.do

Downloads Compustat pension fund data with 1-year availability lag.
Note: Missing data for about 80% of firm-years in most variables except two.
"""

import os
from sqlalchemy import create_engine
import pandas as pd
from dotenv import load_dotenv
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from config import MAX_ROWS_DL
from utils.column_standardizer import standardize_against_dta

print("=" * 60, flush=True)
print("🏦 D_CompustatPensions.py - Compustat Pension Fund Data", flush=True)
print("=" * 60, flush=True)

load_dotenv()

# Create SQLAlchemy engine for database connection
engine = create_engine(
    f"postgresql://{os.getenv('WRDS_USERNAME')}:{os.getenv('WRDS_PASSWORD')}@wrds-pgdata.wharton.upenn.edu:9737/wrds"
)

QUERY = """
SELECT a.gvkey, a.datadate, a.paddml, a.pbnaa, a.pbnvv, a.pbpro,
       a.pbpru, a.pcupsu, a.pplao, a.pplau
FROM COMP.ACO_PNFNDA as a
WHERE a.consol = 'C'
AND a.popsrc = 'D'
AND a.datafmt = 'STD'
AND a.indfmt = 'INDL'
"""

# Add row limit for debugging if configured
if MAX_ROWS_DL > 0:
    QUERY += f" LIMIT {MAX_ROWS_DL}"
    print(f"DEBUG MODE: Limiting to {MAX_ROWS_DL} rows", flush=True)

pensions_data = pd.read_sql_query(QUERY, engine)
engine.dispose()

print(f"Downloaded {len(pensions_data)} pension records")

# Ensure directories exist
os.makedirs("../pyData/Intermediate", exist_ok=True)

# Create year from datadate and add 1-year lag
pensions_data['datadate'] = pd.to_datetime(pensions_data['datadate'])
pensions_data['year'] = pensions_data['datadate'].dt.year + 1  # Assume data available with a lag of one year

# Keep only first observation per gvkey/year combination
# (equivalent to bysort gvkey year (datadate): keep if _n == 1)
pensions_data = pensions_data.sort_values(['gvkey', 'year', 'datadate'])
pensions_data = pensions_data.drop_duplicates(['gvkey', 'year'], keep='first')

print(f"After keeping first obs per gvkey/year: {len(pensions_data)} records")

# Keep year column to match actual Stata output structure, drop datadate
# Actual Stata file has: gvkey, paddml, pbnaa, pbnvv, pbpro, pbpru, pcupsu, pplao, pplau, year
pensions_data = pensions_data.drop('datadate', axis=1)

# Convert gvkey to numeric
pensions_data['gvkey'] = pd.to_numeric(pensions_data['gvkey'])

# Show missing data statistics (equivalent to mdesc)
print("\nMissing data summary:")
pension_vars = ['paddml', 'pbnaa', 'pbnvv', 'pbpro', 'pbpru', 'pcupsu', 'pplao', 'pplau']
for var in pension_vars:
    if var in pensions_data.columns:
        missing_count = pensions_data[var].isna().sum()
        total_count = len(pensions_data)
        missing_pct = (missing_count / total_count) * 100
        print(f"  {var}: {missing_count:,} missing ({missing_pct:.1f}%)")

# Manually ensure columns match actual Stata format (bypass standardize_against_dta issues)
# Actual Stata columns: gvkey, paddml, pbnaa, pbnvv, pbpro, pbpru, pcupsu, pplao, pplau, year
expected_columns = ['gvkey', 'paddml', 'pbnaa', 'pbnvv', 'pbpro', 'pbpru', 'pcupsu', 'pplao', 'pplau', 'year']
pensions_data = pensions_data[expected_columns]

# Save the data
pensions_data.to_parquet("../pyData/Intermediate/CompustatPensions.parquet", index=False)

print(f"\nCompustat Pensions data saved with {len(pensions_data)} records", flush=True)

# Show year range
print(f"Year range: {pensions_data['year'].min()} to {pensions_data['year'].max()}", flush=True)

# Sample data
print("\nSample data:", flush=True)
print(pensions_data.head(), flush=True)
print("=" * 60, flush=True)
print("✅ D_CompustatPensions.py completed successfully", flush=True)
print("=" * 60, flush=True)
