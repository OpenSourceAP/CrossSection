"""
CRSP Monthly data download script - Python equivalent of I_CRSPmonthly.do

Downloads CRSP monthly stock file (MSF) with company names and delisting info.
"""

import os
import pandas as pd
import numpy as np
from dotenv import load_dotenv
from sqlalchemy import create_engine
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from config import MAX_ROWS_DL
from utils.column_standardizer_yaml import standardize_columns

print("=" * 60, flush=True)
print("📊 I_CRSPmonthly.py - CRSP Monthly Stock Data", flush=True)
print("=" * 60, flush=True)

load_dotenv()

# Create SQLAlchemy engine for database connection
engine = create_engine(
    f"postgresql://{os.getenv('WRDS_USERNAME')}:{os.getenv('WRDS_PASSWORD')}@wrds-pgdata.wharton.upenn.edu:9737/wrds"
)

QUERY = """
SELECT a.permno, a.permco, a.date, a.ret, a.retx, a.vol, a.shrout, a.prc, a.cfacshr, a.bidlo, a.askhi,
       b.shrcd, b.exchcd, b.siccd, b.ticker, b.shrcls,
       c.dlstcd, c.dlret
FROM crsp.msf as a
LEFT JOIN crsp.msenames as b
ON a.permno=b.permno AND b.namedt<=a.date AND a.date<=b.nameendt
LEFT JOIN crsp.msedelist as c
ON a.permno=c.permno AND date_trunc('month', a.date) = date_trunc('month', c.dlstdt)
"""

# Add row limit for debugging if configured
if MAX_ROWS_DL > 0:
    QUERY += f" LIMIT {MAX_ROWS_DL}"
    print(f"DEBUG MODE: Limiting to {MAX_ROWS_DL} rows", flush=True)

crsp_data = pd.read_sql_query(QUERY, engine)
engine.dispose()

# Ensure directories exist
os.makedirs("../pyData/Intermediate", exist_ok=True)

# Handle string columns that should be empty strings instead of NaN (to match Stata behavior)
# In Stata, missing string values appear as empty strings, not NaN
string_columns = ['ticker', 'shrcls']
for col in string_columns:
    if col in crsp_data.columns:
        crsp_data[col] = crsp_data[col].fillna('')

# Convert date to Stata format for CSV export to match expected format
crsp_data_csv = crsp_data.copy()
crsp_data_csv['date'] = pd.to_datetime(crsp_data_csv['date'])
# Convert to Stata date string format: "31dec1985"
crsp_data_csv['date'] = crsp_data_csv['date'].dt.strftime('%d%b%Y').str.lower()

# Export for R processing (equivalent to CSV export in Stata)
crsp_data_csv.to_csv("../pyData/Intermediate/mCRSP.csv", index=False)

# Make 2 digit SIC (rename siccd to sicCRSP like in Stata)
crsp_data['sicCRSP'] = crsp_data['siccd']
crsp_data['sic2D'] = crsp_data['sicCRSP'].astype(str).str[:2]

# Convert back to numeric, handling non-numeric values
crsp_data['sic2D'] = pd.to_numeric(crsp_data['sic2D'], errors='coerce')
crsp_data['sicCRSP'] = pd.to_numeric(crsp_data['sicCRSP'], errors='coerce')

# Drop original siccd column (equivalent to Stata's rename)
crsp_data = crsp_data.drop('siccd', axis=1)

# Create monthly date (equivalent to Stata's mofd function)
crsp_data['date'] = pd.to_datetime(crsp_data['date'])
# Keep as datetime64[ns] instead of Period to maintain type compatibility with DTA format
crsp_data['time_avail_m'] = crsp_data['date'].dt.to_period('M').dt.to_timestamp()

# Drop original date column
crsp_data = crsp_data.drop('date', axis=1)

# === Incorporate delisting return ===
# Replace missing dlret with -0.35 for specific delisting codes on NYSE/AMEX
mask1 = (crsp_data['dlret'].isna() &
         ((crsp_data['dlstcd'] == 500) |
          ((crsp_data['dlstcd'] >= 520) & (crsp_data['dlstcd'] <= 584))) &
         ((crsp_data['exchcd'] == 1) | (crsp_data['exchcd'] == 2)))
crsp_data.loc[mask1, 'dlret'] = -0.35

# Replace missing dlret with -0.55 for NASDAQ (exchcd == 3)
mask2 = (crsp_data['dlret'].isna() &
         ((crsp_data['dlstcd'] == 500) |
          ((crsp_data['dlstcd'] >= 520) & (crsp_data['dlstcd'] <= 584))) &
         (crsp_data['exchcd'] == 3))
crsp_data.loc[mask2, 'dlret'] = -0.55

# Cap delisting return at -1
crsp_data.loc[(crsp_data['dlret'] < -1) & crsp_data['dlret'].notna(), 'dlret'] = -1

# Fill remaining missing dlret with 0
crsp_data['dlret'] = crsp_data['dlret'].fillna(0)

# Update returns to incorporate delisting returns
# Handle case where ret < -1 (updated in 2022 02)
crsp_data['ret'] = (1 + crsp_data['ret']) * (1 + crsp_data['dlret']) - 1

# Use dlret if ret is missing but dlret is not zero
mask3 = crsp_data['ret'].isna() & (crsp_data['dlret'] != 0)
crsp_data.loc[mask3, 'ret'] = crsp_data.loc[mask3, 'dlret']

# === Compute market value of equity ===

# Converting units (shares in thousands, volume in ten-thousands)
crsp_data['shrout'] = crsp_data['shrout'] / 1000
crsp_data['vol'] = crsp_data['vol'] / 10000

# Market value = Common shares outstanding * |Price|
crsp_data['mve_c'] = crsp_data['shrout'] * np.abs(crsp_data['prc'])

# Add mve_permco = market value at the company level
permco_dat = crsp_data.query('~mve_c.isna()').groupby(['permco','time_avail_m']).agg(
    mve_permco=("mve_c", "sum")
).reset_index()

crsp_data = crsp_data.merge(permco_dat, on=['permco', 'time_avail_m'], how='left')

# Housekeeping - drop columns
crsp_data = crsp_data.drop(['dlret', 'dlstcd', 'permco'], axis=1)

# Standardize columns to match DTA file
crsp_data = standardize_columns(crsp_data, "monthlyCRSP")

# Save the data
crsp_data.to_parquet("../pyData/Intermediate/monthlyCRSP.parquet", index=False)

print(f"CRSP Monthly data downloaded with {len(crsp_data)} records", flush=True)
print(f"Date range: {crsp_data['time_avail_m'].min()} to {crsp_data['time_avail_m'].max()}", flush=True)
print("=" * 60, flush=True)
print("✅ I_CRSPmonthly.py completed successfully", flush=True)
print("=" * 60, flush=True)