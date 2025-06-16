#!/usr/bin/env python3
"""
Compustat Pensions data download script - Python equivalent of D_CompustatPensions.do

Downloads Compustat pension fund data with 1-year availability lag.
Note: Missing data for about 80% of firm-years in most variables except two.
"""

import os
import psycopg2
import pandas as pd
from dotenv import load_dotenv

load_dotenv()

conn = psycopg2.connect(
    host="wrds-pgdata.wharton.upenn.edu",
    port=9737,
    database="wrds",
    user=os.getenv("WRDS_USERNAME"),
    password=os.getenv("WRDS_PASSWORD")
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

pensions_data = pd.read_sql_query(QUERY, conn)
conn.close()

print(f"Downloaded {len(pensions_data)} pension records")

# Ensure directories exist
os.makedirs("../Data/Intermediate", exist_ok=True)

# Create year from datadate and add 1-year lag
pensions_data['datadate'] = pd.to_datetime(pensions_data['datadate'])
pensions_data['year'] = pensions_data['datadate'].dt.year + 1  # Assume data available with a lag of one year

# Keep only first observation per gvkey/year combination
# (equivalent to bysort gvkey year (datadate): keep if _n == 1)
pensions_data = pensions_data.sort_values(['gvkey', 'year', 'datadate'])
pensions_data = pensions_data.drop_duplicates(['gvkey', 'year'], keep='first')

print(f"After keeping first obs per gvkey/year: {len(pensions_data)} records")

# Drop datadate as in original code
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

# Save the data
pensions_data.to_pickle("../Data/Intermediate/CompustatPensions.pkl")

print(f"\nCompustat Pensions data saved with {len(pensions_data)} records")

# Show year range
print(f"Year range: {pensions_data['year'].min()} to {pensions_data['year'].max()}")

# Sample data
print("\nSample data:")
print(pensions_data.head())