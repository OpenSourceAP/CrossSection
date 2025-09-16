# ABOUTME: Downloads CRSP daily stock file (DSF) data in yearly chunks to manage memory efficiently
# ABOUTME: Creates two output files: full daily data with returns/volume and price-only version
"""
Inputs:
- crsp.dsf (CRSP Daily Stock File from WRDS)

Outputs:
- ../pyData/Intermediate/dailyCRSP.parquet (full daily data with returns, volume, prices)
- ../pyData/Intermediate/dailyCRSPprc.parquet (price-only version)

How to run: python3 CRSPDaily.py
"""

# Import required libraries and setup
import os
import pandas as pd
import numpy as np
from datetime import datetime
from dotenv import load_dotenv
from sqlalchemy import create_engine
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from config import MAX_ROWS_DL

load_dotenv()

def get_crsp_daily_year(year, engine):
    # Download CRSP daily data for a specific year
    query = f"""
    SELECT a.permno, a.date, a.ret, a.vol, a.shrout, a.prc, a.cfacshr, a.cfacpr
    FROM crsp.dsf as a
    WHERE date >= '{year}-01-01' and date <= '{year}-12-31'
    """

    data = pd.read_sql_query(query, engine)
    print(f"Downloaded {len(data)} records for year {year}")
    return data

# Main processing - download CRSP daily data
print("Starting CRSP Daily data download...")

# Setup database connection
engine = create_engine(
    f"postgresql://{os.getenv('WRDS_USERNAME')}:{os.getenv('WRDS_PASSWORD')}@wrds-pgdata.wharton.upenn.edu:9737/wrds"
)

# Determine year range for download (debug mode downloads only 1932, production mode downloads 1926-current)
current_year = datetime.now().year
if MAX_ROWS_DL > 0:
    year_range = [1932]
    print(f"DEBUG MODE: Only downloading year 1932 (instead of 1926-{current_year})")
else:
    year_range = range(1926, current_year + 1)
    print(f"PRODUCTION MODE: Downloading years 1926-{current_year}")

# Download data year by year to manage memory
all_data = []

for year in year_range:
    print(f"Processing year {year}...")
    year_data = get_crsp_daily_year(year, engine)
    all_data.append(year_data)
    import time
    time.sleep(1)

engine.dispose()

# Combine and process all downloaded data
print("Combining all years of data...")
combined_data = pd.concat(all_data, ignore_index=True)
print(f"Total records downloaded: {len(combined_data)}")
combined_data = combined_data.rename(columns={'date': 'time_d'})

# Create and save full daily file with returns, volume, and prices
full_columns = ['permno', 'time_d', 'ret', 'vol', 'prc', 'cfacpr', 'shrout']
daily_full = combined_data[full_columns].copy()
daily_full['permno'] = daily_full['permno'].astype('int32')
daily_full['time_d'] = pd.to_datetime(daily_full['time_d']).dt.floor('D')
daily_full.to_parquet("../pyData/Intermediate/dailyCRSP.parquet", index=False)
print(f"Saved full daily CRSP data with {len(daily_full)} records")

# Create and save price-only file (prices, adjustment factors, shares outstanding)
price_columns = ['permno', 'time_d', 'prc', 'cfacpr', 'shrout']
daily_prc = combined_data[price_columns].copy()
daily_prc['permno'] = daily_prc['permno'].astype('int32')
daily_prc['time_d'] = pd.to_datetime(daily_prc['time_d']).dt.floor('D')
daily_prc.to_parquet("../pyData/Intermediate/dailyCRSPprc.parquet", index=False)
print(f"Saved price-only daily CRSP data with {len(daily_prc)} records")

# Display date range summary
min_date = pd.to_datetime(combined_data['time_d']).min()
max_date = pd.to_datetime(combined_data['time_d']).max()
print(f"Date range: {min_date.strftime('%Y-%m-%d')} to {max_date.strftime('%Y-%m-%d')}")
