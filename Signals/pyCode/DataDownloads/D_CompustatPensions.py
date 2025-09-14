# ABOUTME: Downloads Compustat pension fund data with 1-year availability lag
# ABOUTME: Aggregates to gvkey-year level and applies lag assumption for data availability
"""
Inputs:
- comp.aco_pnfnda (Compustat Annual - Pension Data)

Outputs:
- ../pyData/Intermediate/CompustatPensions.parquet

How to run: python3 D_CompustatPensions.py
"""

# Setup imports and configuration
import os
from sqlalchemy import create_engine
import pandas as pd
from dotenv import load_dotenv
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from config import MAX_ROWS_DL

print("=" * 60, flush=True)
print("🏦 D_CompustatPensions.py - Compustat Pension Fund Data", flush=True)
print("=" * 60, flush=True)

load_dotenv()

# Connect to WRDS database
engine = create_engine(
    f"postgresql://{os.getenv('WRDS_USERNAME')}:{os.getenv('WRDS_PASSWORD')}@wrds-pgdata.wharton.upenn.edu:9737/wrds"
)

# Query pension fund data from Compustat annual pension dataset
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

# Download data and close connection
pensions_data = pd.read_sql_query(QUERY, engine)
engine.dispose()

print(f"Downloaded {len(pensions_data)} pension records")


# Process data with 1-year availability lag
pensions_data['datadate'] = pd.to_datetime(pensions_data['datadate'])
pensions_data['year'] = pensions_data['datadate'].dt.year + 1

# Keep only first observation per gvkey/year combination
pensions_data = pensions_data.sort_values(['gvkey', 'year', 'datadate'])
pensions_data = pensions_data.drop_duplicates(['gvkey', 'year'], keep='first')

print(f"After keeping first obs per gvkey/year: {len(pensions_data)} records")

# Clean up data structure and convert types
pensions_data = pensions_data.drop('datadate', axis=1)
pensions_data['gvkey'] = pd.to_numeric(pensions_data['gvkey'])

# Display missing data statistics
print("\nMissing data summary:")
pension_vars = ['paddml', 'pbnaa', 'pbnvv', 'pbpro', 'pbpru', 'pcupsu', 'pplao', 'pplau']
for var in pension_vars:
    if var in pensions_data.columns:
        missing_count = pensions_data[var].isna().sum()
        total_count = len(pensions_data)
        missing_pct = (missing_count / total_count) * 100
        print(f"  {var}: {missing_count:,} missing ({missing_pct:.1f}%)")


# Save processed data to parquet
pensions_data.to_parquet("../pyData/Intermediate/CompustatPensions.parquet", index=False)

# Display completion summary
print(f"\nCompustat Pensions data saved with {len(pensions_data)} records", flush=True)
print(f"Year range: {pensions_data['year'].min()} to {pensions_data['year'].max()}", flush=True)
print("\nSample data:", flush=True)
print(pensions_data.head(), flush=True)
print("=" * 60, flush=True)
print("✅ D_CompustatPensions.py completed successfully", flush=True)
print("=" * 60, flush=True)
