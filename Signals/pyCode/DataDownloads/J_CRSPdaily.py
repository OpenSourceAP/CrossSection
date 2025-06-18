#!/usr/bin/env python3
"""
CRSP Daily data download script - Python equivalent of J_CRSPdaily.do

Downloads CRSP daily stock file (DSF) in yearly chunks to manage memory.
Creates two output files: full daily data and price-only version.
"""

import os
import psycopg2
import pandas as pd
import numpy as np
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

def get_crsp_daily_year(year, conn):
    """Download CRSP daily data for a specific year"""
    query = """
    SELECT a.permno, a.date, a.ret, a.vol, a.shrout, a.prc, a.cfacshr, a.cfacpr
    FROM crsp.dsf as a
    WHERE date >= '{year}-01-01' and date <= '{year}-12-31'
    """

    try:
        data = pd.read_sql_query(query, conn)
        print("Downloaded {len(data)} records for year {year}")
        return data
    except Exception as e:
        print("Error downloading year {year}: {e}")
        return pd.DataFrame()

def main():
    """Main function to download CRSP daily data"""
    print("Starting CRSP Daily data download...")

    # Connect to WRDS
    conn = psycopg2.connect(
        host="wrds-pgdata.wharton.upenn.edu",
        port=9737,
        database="wrds",
        user=os.getenv("WRDS_USERNAME"),
        password=os.getenv("WRDS_PASSWORD")
    )

    # Ensure directories exist
    os.makedirs("../pyData/Intermediate", exist_ok=True)
    os.makedirs("../Data/temp", exist_ok=True)

    # Get current year for end year (equivalent to substr("$S_DATE", -4, 4))
    current_year = datetime.now().year

    # Download data year by year (1926 to current year)
    all_data = []

    for year in range(1926, current_year + 1):
        print("Processing year {year}...")

        year_data = get_crsp_daily_year(year, conn)

        if not year_data.empty:
            all_data.append(year_data)

        # Small pause to avoid connection issues (equivalent to sleep 1000)
        import time
        time.sleep(1)

    conn.close()

    if not all_data:
        print("No data downloaded")
        return

    # Combine all years
    print("Combining all years of data...")
    combined_data = pd.concat(all_data, ignore_index=True)

    print("Total records downloaded: {len(combined_data)}")

    # Rename date to time_d (equivalent to Stata rename)
    combined_data = combined_data.rename(columns={'date': 'time_d'})

    # Create full daily file (equivalent to first save in Stata)
    full_columns = ['permno', 'time_d', 'ret', 'vol', 'prc', 'cfacpr', 'shrout']
    daily_full = combined_data[full_columns].copy()

    # Save full daily data
    daily_full.to_pickle("../pyData/Intermediate/dailyCRSP.pkl")
    print("Saved full daily CRSP data with {len(daily_full)} records")

    # Create price-only file (equivalent to second save in Stata)
    price_columns = ['permno', 'time_d', 'prc', 'cfacpr', 'shrout']
    daily_prc = combined_data[price_columns].copy()

    # Save price-only data
    daily_prc.to_pickle("../pyData/Intermediate/dailyCRSPprc.pkl")
    print("Saved price-only daily CRSP data with {len(daily_prc)} records")

    # Date range info
    min_date = pd.to_datetime(combined_data['time_d']).min()
    max_date = pd.to_datetime(combined_data['time_d']).max()
    print("Date range: {min_date.strftime('%Y-%m-%d')} to {max_date.strftime('%Y-%m-%d')}")

if __name__ == "__main__":
    main()
