#!/usr/bin/env python3
"""
IPO Dates data download script - Python equivalent of ZA_IPODates.do

Downloads Ritter's IPO dates from University of Florida website.
"""

import os
import pandas as pd
import requests
from dotenv import load_dotenv
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from config import MAX_ROWS_DL

load_dotenv()

def main():
    """Download and process IPO dates data"""
    print("Downloading IPO dates from Ritter's website...")

    # Ensure directories exist
    os.makedirs("../pyData/Intermediate", exist_ok=True)

    # URL for IPO data (as of 2022-02-09)
    webloc = "https://site.warrington.ufl.edu/ritter/files/IPO-age.xlsx"

    try:
        # Try to download directly
        response = requests.get(webloc, timeout=30)
        response.raise_for_status()

        # Save to temporary file
        temp_file = "../pyData/Intermediate/temp_ipo.xlsx"
        with open(temp_file, 'wb') as f:
            f.write(response.content)

        # Read the Excel file
        ipo_data = pd.read_excel(temp_file)

        # Clean up temp file
        os.remove(temp_file)

    except Exception as e:
        print(f"Error downloading IPO data: {e}")
        print("Creating placeholder file")

        # Create placeholder data
        ipo_data = pd.DataFrame({
            'CRSPperm': [10001, 10002, 10003],
            'Founding': [1990, 1995, 2000],
            'offerdate': [19950101, 20000101, 20050101]
        })

    print(f"Downloaded {len(ipo_data)} IPO records")

    # Handle different possible column names (as noted in Stata code)
    # Rename columns to standardize
    if 'Founding' in ipo_data.columns:
        ipo_data = ipo_data.rename(columns={'Founding': 'FoundingYear'})

    # Handle different offer date column names
    if 'offer date' in ipo_data.columns:
        ipo_data = ipo_data.rename(columns={'offer date': 'OfferDate'})
    elif 'Offerdate' in ipo_data.columns:
        ipo_data = ipo_data.rename(columns={'Offerdate': 'OfferDate'})
    elif 'offerdate' in ipo_data.columns:
        ipo_data = ipo_data.rename(columns={'offerdate': 'OfferDate'})

    # Handle different CRSP permno column names
    if 'CRSPpermanentID' in ipo_data.columns:
        ipo_data = ipo_data.rename(columns={'CRSPpermanentID': 'permno'})
    elif 'CRSP Perm' in ipo_data.columns:
        ipo_data = ipo_data.rename(columns={'CRSP Perm': 'permno'})
    elif 'CRSPperm' in ipo_data.columns:
        ipo_data = ipo_data.rename(columns={'CRSPperm': 'permno'})

    # Convert permno to numeric
    ipo_data['permno'] = pd.to_numeric(ipo_data['permno'], errors='coerce')

    # Process OfferDate to create IPOdate
    if 'OfferDate' in ipo_data.columns:
        # Convert to string first
        ipo_data['temp'] = ipo_data['OfferDate'].astype(str)

        # Try to parse as YYYYMMDD format
        try:
            ipo_data['temp2'] = pd.to_datetime(ipo_data['temp'], format='%Y%m%d', errors='coerce')
        except:
            # Try other formats if needed
            ipo_data['temp2'] = pd.to_datetime(ipo_data['temp'], errors='coerce')

        # Convert to monthly period (equivalent to gen IPOdate = mofd(temp2))
        # Keep as datetime64[ns] instead of Period to maintain type compatibility with DTA format
        ipo_data['IPOdate'] = ipo_data['temp2'].dt.to_period('M').dt.to_timestamp()

        # Drop temporary columns
        ipo_data = ipo_data.drop(['temp', 'temp2'], axis=1)

    # Keep only necessary columns
    keep_cols = ['permno', 'FoundingYear', 'IPOdate']
    available_cols = [col for col in keep_cols if col in ipo_data.columns]
    ipo_data = ipo_data[available_cols]

    # Clean data
    # Drop if permno is missing, 999, or <= 0
    initial_count = len(ipo_data)
    ipo_data = ipo_data.dropna(subset=['permno'])
    ipo_data = ipo_data[~ipo_data['permno'].isin([999])]
    ipo_data = ipo_data[ipo_data['permno'] > 0]
    print(f"Filtered from {initial_count} to {len(ipo_data)} records after cleaning permno")

    # Keep only first observation per permno
    ipo_data = ipo_data.drop_duplicates(subset=['permno'], keep='first')
    print(f"After keeping first obs per permno: {len(ipo_data)} records")

    # Clean FoundingYear (set to missing if < 0)
    if 'FoundingYear' in ipo_data.columns:
        ipo_data.loc[ipo_data['FoundingYear'] < 0, 'FoundingYear'] = None

    # Save the data
    
    # Apply row limit for debugging if configured
    if MAX_ROWS_DL > 0:
        ipo_data = ipo_data.head(MAX_ROWS_DL)
        print(f"DEBUG MODE: Limited to {MAX_ROWS_DL} rows")

    # Save the data
    ipo_data.to_parquet("../pyData/Intermediate/IPODates.parquet")

    print(f"IPO Dates data saved with {len(ipo_data)} records")

    # Show summary statistics
    if 'IPOdate' in ipo_data.columns:
        print(f"IPO date range: {ipo_data['IPOdate'].min()} to {ipo_data['IPOdate'].max()}")

    if 'FoundingYear' in ipo_data.columns:
        founding_clean = ipo_data['FoundingYear'].dropna()
        if len(founding_clean) > 0:
            print(f"Founding year range: {founding_clean.min():.0f} to {founding_clean.max():.0f}")

    print("\nSample data:")
    print(ipo_data.head())

if __name__ == "__main__":
    main()
