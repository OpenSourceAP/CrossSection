# ABOUTME: Downloads Compustat pension fund data with 1-year availability lag
# ABOUTME: Aggregates to gvkey-year level and applies lag assumption for data availability
"""
Inputs:
- comp.aco_pnfnda (Compustat Annual - Pension Data)

Outputs:
- ../pyData/Intermediate/CompustatPensions.parquet

How to run: from Signals/pyCode, run python3 DataDownloads/CompustatPensions.py

Use the project Python environment at /opt/venv/projects/openap.
"""

import os
from sqlalchemy import create_engine
import pandas as pd
from dotenv import load_dotenv
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from config import DEBUG_MODE
from utils.debug_mode import get_debug_row_limit

DEBUG_ROWS = get_debug_row_limit("CompustatPensions")

print("=" * 60, flush=True)
print("🏦 CompustatPensions.py - Compustat Pension Fund Data", flush=True)
print("=" * 60, flush=True)

load_dotenv()

engine = create_engine(
    f"postgresql://{os.getenv('WRDS_USERNAME')}:{os.getenv('WRDS_PASSWORD')}@wrds-pgdata.wharton.upenn.edu:9737/wrds"
)

# Obtain comparable consolidated pension accounts for pension-related signals.
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
if DEBUG_MODE:
    QUERY += f" LIMIT {DEBUG_ROWS}"
    print(f"DEBUG MODE: Limiting to {DEBUG_ROWS} rows", flush=True)

pensions_data = pd.read_sql_query(QUERY, engine)
engine.dispose()

print(f"Downloaded {len(pensions_data)} pension records")

# Make pension information available in the calendar year after its report date.
pensions_data['datadate'] = pd.to_datetime(pensions_data['datadate'])
pensions_data['year'] = pensions_data['datadate'].dt.year + 1

# Use the earliest report when a company has multiple reports for the same availability year.
pensions_data = pensions_data.sort_values(['gvkey', 'year', 'datadate'])
pensions_data = pensions_data.drop_duplicates(['gvkey', 'year'], keep='first')

print(f"After keeping first obs per gvkey/year: {len(pensions_data)} records")

# Provide company-year pension measures in the format used by downstream signals.
pensions_data = pensions_data.drop('datadate', axis=1)
pensions_data['gvkey'] = pd.to_numeric(pensions_data['gvkey'])

print("\nMissing data summary:")
pension_vars = ['paddml', 'pbnaa', 'pbnvv', 'pbpro', 'pbpru', 'pcupsu', 'pplao', 'pplau']
for var in pension_vars:
    if var in pensions_data.columns:
        missing_count = pensions_data[var].isna().sum()
        total_count = len(pensions_data)
        missing_pct = (missing_count / total_count) * 100
        print(f"  {var}: {missing_count:,} missing ({missing_pct:.1f}%)")

# Save annual pension measures with the availability-year convention applied.
pensions_data.to_parquet("../pyData/Intermediate/CompustatPensions.parquet", index=False)

print(f"\nCompustat Pensions data saved with {len(pensions_data)} records", flush=True)
print(f"Year range: {pensions_data['year'].min()} to {pensions_data['year'].max()}", flush=True)
print("\nSample data:", flush=True)
print(pensions_data.head(), flush=True)
print("=" * 60, flush=True)
print("✅ CompustatPensions.py completed successfully", flush=True)
print("=" * 60, flush=True)
