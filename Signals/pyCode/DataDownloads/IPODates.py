# ABOUTME: Downloads IPO dates data from Ritter's website at University of Florida
# ABOUTME: Processes IPO dates and founding years data to create monthly IPO date records per permno
"""
Inputs:
- https://site.warrington.ufl.edu/ritter/files/IPO-age.xlsx (online data source)

Outputs:
- ../pyData/Intermediate/IPODates.parquet

How to run: from Signals/pyCode, run python3 DataDownloads/IPODates.py

Use the project Python environment at /opt/venv/projects/openap.
"""

import os
import pandas as pd
import requests
from dotenv import load_dotenv
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from config import DEBUG_MODE
from utils.debug_mode import get_debug_row_limit

DEBUG_ROWS = get_debug_row_limit("IPODates")

load_dotenv()

print("Downloading IPO dates from Ritter's website...")

# Obtain offering dates and founding years for stock-age and company-age signals.
webloc = "https://site.warrington.ufl.edu/ritter/files/IPO-age.xlsx"

response = requests.get(webloc, timeout=30)
response.raise_for_status()

temp_file = "../pyData/Intermediate/temp_ipo.xlsx"
with open(temp_file, 'wb') as f:
    f.write(response.content)

ipo_data = pd.read_excel(temp_file)
os.remove(temp_file)

print(f"Downloaded {len(ipo_data)} IPO records")

# Use the stock identifier and age-field names expected by downstream signals.
ipo_data = ipo_data.rename(columns={'Founding': 'FoundingYear'})
ipo_data = ipo_data.rename(columns={'offer date': 'OfferDate'})
ipo_data = ipo_data.rename(columns={'CRSP Perm': 'permno'})

# Make stock identifiers usable for linking, treating invalid identifiers as missing.
ipo_data['permno'] = pd.to_numeric(ipo_data['permno'], errors='coerce')

# Record the IPO month so stock age can be measured on the monthly signal calendar.
offer_date_text = ipo_data['OfferDate'].astype(str)
offer_date = pd.to_datetime(offer_date_text, format='%Y%m%d', errors='coerce')
ipo_data['IPOdate'] = offer_date.dt.to_period('M').dt.to_timestamp()

# Retain the stock identifier, founding year, and IPO month needed for age calculations.
keep_cols = ['permno', 'FoundingYear', 'IPOdate']
available_cols = [col for col in keep_cols if col in ipo_data.columns]
ipo_data = ipo_data[available_cols]

# Exclude missing identifiers and source placeholders that cannot identify a CRSP security.
initial_count = len(ipo_data)
ipo_data = ipo_data.dropna(subset=['permno'])
ipo_data = ipo_data[~ipo_data['permno'].isin([999])]
ipo_data = ipo_data[ipo_data['permno'] > 0]
print(f"Filtered from {initial_count} to {len(ipo_data)} records after cleaning permno")

# Keep one source record per stock so age-data joins do not duplicate observations.
ipo_data = ipo_data.drop_duplicates(subset=['permno'], keep='first')
print(f"After keeping first obs per permno: {len(ipo_data)} records")

# Treat negative founding-year placeholders as unknown company ages.
ipo_data.loc[ipo_data['FoundingYear'] < 0, 'FoundingYear'] = None

# Apply debug row limit if configured
if DEBUG_MODE:
    ipo_data = ipo_data.head(DEBUG_ROWS)
    print(f"DEBUG MODE: Limited to {DEBUG_ROWS} rows")

# Save stock-level IPO and founding dates for downstream age signals.
ipo_data.to_parquet("../pyData/Intermediate/IPODates.parquet")
print(f"IPO Dates data saved with {len(ipo_data)} records")

print(f"IPO date range: {ipo_data['IPOdate'].min()} to {ipo_data['IPOdate'].max()}")

founding_clean = ipo_data['FoundingYear'].dropna()
print(f"Founding year range: {founding_clean.min():.0f} to {founding_clean.max():.0f}")

print("\nSample data:")
print(ipo_data.head())
