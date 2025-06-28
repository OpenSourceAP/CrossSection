#!/usr/bin/env python3
"""
CRSP Daily data download script - Python equivalent of J_CRSPdaily.do

Downloads CRSP daily stock file (DSF) in yearly chunks to manage memory.
Creates two output files: full daily data and price-only version.
"""

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
from utils.column_standardizer import standardize_against_dta

load_dotenv()

def get_crsp_daily_year(year, engine):
    """Download CRSP daily data for a specific year"""
    query = f"""
    SELECT a.permno, a.date, a.ret, a.vol, a.shrout, a.prc, a.cfacshr, a.cfacpr
    FROM crsp.dsf as a
    WHERE date >= '{year}-01-01' and date <= '{year}-12-31'
    """

    try:
        data = pd.read_sql_query(query, engine)
        print(f"Downloaded {len(data)} records for year {year}")
        return data
    except Exception as e:
        print(f"Error downloading year {year}: {e}")
        return pd.DataFrame()

def main():
    """Main function to download CRSP daily data"""
    print("Starting CRSP Daily data download...")

    # Create SQLAlchemy engine for database connection
    engine = create_engine(
        f"postgresql://{os.getenv('WRDS_USERNAME')}:{os.getenv('WRDS_PASSWORD')}@wrds-pgdata.wharton.upenn.edu:9737/wrds"
    )

    # Ensure directories exist
    os.makedirs("../pyData/Intermediate", exist_ok=True)
    os.makedirs("../Data/temp", exist_ok=True)

    # Get current year for end year (equivalent to substr("$S_DATE", -4, 4))
    current_year = datetime.now().year

    # Determine year range based on debug mode
    if MAX_ROWS_DL > 0:
        # DEBUG MODE: Only download first year to test quickly
        year_range = [1932]
        print(f"DEBUG MODE: Only downloading year 1932 (instead of 1926-{current_year})")
    else:
        # PRODUCTION MODE: Download all years
        year_range = range(1926, current_year + 1)
        print(f"PRODUCTION MODE: Downloading years 1926-{current_year}")

    # Download data year by year
    all_data = []

    for year in year_range:
        print(f"Processing year {year}...")

        year_data = get_crsp_daily_year(year, engine)

        if not year_data.empty:
            all_data.append(year_data)

        # Small pause to avoid connection issues (equivalent to sleep 1000)
        import time
        time.sleep(1)

    engine.dispose()

    if not all_data:
        print("No data downloaded")
        return

    # Combine all years
    print("Combining all years of data...")
    combined_data = pd.concat(all_data, ignore_index=True)

    print(f"Total records downloaded: {len(combined_data)}")

    # Rename date to time_d (equivalent to Stata rename)
    combined_data = combined_data.rename(columns={'date': 'time_d'})

    # Create full daily file (equivalent to first save in Stata)
    full_columns = ['permno', 'time_d', 'ret', 'vol', 'prc', 'cfacpr', 'shrout']
    daily_full = combined_data[full_columns].copy()

    # Convert data types to match Stata format exactly
    daily_full['permno'] = daily_full['permno'].astype('int32')  # Match Stata int32
    # Ensure datetime64[ns] format to prevent PyArrow date32[day] optimization
    daily_full['time_d'] = pd.to_datetime(daily_full['time_d']).dt.floor('D')

    # Standardize columns to match DTA file
    daily_full = standardize_against_dta(
        daily_full, 
        "../Data/Intermediate/dailyCRSP.dta",
        "dailyCRSP"
    )

    # Save full daily data
    daily_full.to_parquet("../pyData/Intermediate/dailyCRSP.parquet", index=False)
    print(f"Saved full daily CRSP data with {len(daily_full)} records")

    # Create price-only file (equivalent to second save in Stata)
    price_columns = ['permno', 'time_d', 'prc', 'cfacpr', 'shrout']
    daily_prc = combined_data[price_columns].copy()

    # Convert data types to match Stata format exactly
    daily_prc['permno'] = daily_prc['permno'].astype('int32')  # Match Stata int32
    # Ensure datetime64[ns] format to prevent PyArrow date32[day] optimization
    daily_prc['time_d'] = pd.to_datetime(daily_prc['time_d']).dt.floor('D')

    # Standardize columns to match DTA file
    daily_prc = standardize_against_dta(
        daily_prc, 
        "../Data/Intermediate/dailyCRSPprc.dta",
        "dailyCRSPprc"
    )

    # Save price-only data
    daily_prc.to_parquet("../pyData/Intermediate/dailyCRSPprc.parquet", index=False)
    print(f"Saved price-only daily CRSP data with {len(daily_prc)} records")

    # Date range info
    min_date = pd.to_datetime(combined_data['time_d']).min()
    max_date = pd.to_datetime(combined_data['time_d']).max()
    print(f"Date range: {min_date.strftime('%Y-%m-%d')} to {max_date.strftime('%Y-%m-%d')}")

if __name__ == "__main__":
    main()
