# ABOUTME: Downloads IPO dates data from Ritter's website at University of Florida
# ABOUTME: Processes IPO dates and founding years data to create monthly IPO date records per permno
"""
Inputs:
- https://site.warrington.ufl.edu/ritter/files/IPO-age.xlsx (online data source)

Outputs:
- ../pyData/Intermediate/IPODates.parquet

How to run: python3 IPODates.py
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

print("Downloading IPO dates from Ritter's website...")

# Set URL for Ritter's IPO data Excel file
webloc = "https://site.warrington.ufl.edu/ritter/files/IPO-age.xlsx"

# Download IPO data from website
response = requests.get(webloc, timeout=30)
response.raise_for_status()

temp_file = "../pyData/Intermediate/temp_ipo.xlsx"
with open(temp_file, 'wb') as f:
    f.write(response.content)

ipo_data = pd.read_excel(temp_file)
os.remove(temp_file)

print(f"Downloaded {len(ipo_data)} IPO records")

# Standardize column names to handle different possible variations
ipo_data = ipo_data.rename(columns={'Founding': 'FoundingYear'})
ipo_data = ipo_data.rename(columns={'offer date': 'OfferDate'})
ipo_data = ipo_data.rename(columns={'CRSP Perm': 'permno'})

# Convert permno to numeric format
ipo_data['permno'] = pd.to_numeric(ipo_data['permno'], errors='coerce')

# Process offer date to create monthly IPO date variable
ipo_data['temp'] = ipo_data['OfferDate'].astype(str)
ipo_data['temp2'] = pd.to_datetime(ipo_data['temp'], format='%Y%m%d', errors='coerce')
ipo_data['IPOdate'] = ipo_data['temp2'].dt.to_period('M').dt.to_timestamp()
ipo_data = ipo_data.drop(['temp', 'temp2'], axis=1)

# Select final columns to keep
keep_cols = ['permno', 'FoundingYear', 'IPOdate']
available_cols = [col for col in keep_cols if col in ipo_data.columns]
ipo_data = ipo_data[available_cols]

# Clean permno data - remove missing, invalid (999), and non-positive values
initial_count = len(ipo_data)
ipo_data = ipo_data.dropna(subset=['permno'])
ipo_data = ipo_data[~ipo_data['permno'].isin([999])]
ipo_data = ipo_data[ipo_data['permno'] > 0]
print(f"Filtered from {initial_count} to {len(ipo_data)} records after cleaning permno")

# Keep only first observation per permno to avoid duplicates
ipo_data = ipo_data.drop_duplicates(subset=['permno'], keep='first')
print(f"After keeping first obs per permno: {len(ipo_data)} records")

# Clean FoundingYear - set negative values to missing
ipo_data.loc[ipo_data['FoundingYear'] < 0, 'FoundingYear'] = None

# Apply debug row limit if configured
if MAX_ROWS_DL > 0:
    ipo_data = ipo_data.head(MAX_ROWS_DL)
    print(f"DEBUG MODE: Limited to {MAX_ROWS_DL} rows")

# Save to parquet
ipo_data.to_parquet("../pyData/Intermediate/IPODates.parquet")
print(f"IPO Dates data saved with {len(ipo_data)} records")

# Display summary statistics
print(f"IPO date range: {ipo_data['IPOdate'].min()} to {ipo_data['IPOdate'].max()}")

founding_clean = ipo_data['FoundingYear'].dropna()
print(f"Founding year range: {founding_clean.min():.0f} to {founding_clean.max():.0f}")

print("\nSample data:")
print(ipo_data.head())
