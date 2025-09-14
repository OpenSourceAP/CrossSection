# ABOUTME: Downloads governance index data from Gompers, Ishii, and Metrick (1990-2007)
# ABOUTME: Creates monthly ticker-level panel with forward-filled G-index values through 2007
"""
Inputs:
- External URL: https://spinup-000d1a-wp-offload-media.s3.amazonaws.com/faculty/wp-content/uploads/sites/7/2019/06/Governance.xlsx

Outputs:
- ../pyData/Intermediate/GovIndex.parquet

How to run: python3 ZC_GovernanceIndex.py
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

print("Downloading Governance Index data...")

# Download governance index data from Gompers, Ishii, and Metrick
webloc = "https://spinup-000d1a-wp-offload-media.s3.amazonaws.com/faculty/wp-content/uploads/sites/7/2019/06/Governance.xlsx"

# Download Excel file from web
response = requests.get(webloc, timeout=60)
response.raise_for_status()

# Save to temporary file
temp_file = "../pyData/Intermediate/temp_governance.xlsx"
with open(temp_file, 'wb') as f:
    f.write(response.content)

# Read governance index sheet (equivalent to importing A24:F14024)
gov_data = pd.read_excel(temp_file, sheet_name='governance index',
                        skiprows=23, nrows=14000)

# Clean up temp file
os.remove(temp_file)

print(f"Downloaded {len(gov_data)} governance records")

# Clean and deduplicate data
gov_data['ticker'] = gov_data['ticker'].str.strip()

# Keep first observation per ticker-year combination
gov_data = gov_data.drop_duplicates(['ticker', 'year'], keep='first')
print(f"After removing ticker-year duplicates: {len(gov_data)} records")

# Fix year 2000 data (treat as 1999 per original specification)
gov_data.loc[gov_data['year'] == 2000, 'year'] = 1999

# Assign publication months for each survey year
month_mapping = {
    1990: 9,
    1993: 7,
    1995: 7,
    1998: 2,
    1999: 11
}

gov_data['month'] = None
for year, month in month_mapping.items():
    gov_data.loc[gov_data['year'] == year, 'month'] = month

# For years >= 2002, assume January publication
gov_data.loc[gov_data['year'] >= 2002, 'month'] = 1

# Create monthly time availability variable
gov_data['time_avail_m'] = pd.to_datetime(
    gov_data['year'].astype(str) + '-' + gov_data['month'].astype(str) + '-01'
).dt.to_period('M').dt.to_timestamp()

# Create monthly panel by interpolating between survey dates
print("Interpolating time series...")

# For each ticker, create monthly observations through 2007
extended_data = []
for ticker in gov_data['ticker'].unique():
    ticker_data = gov_data[gov_data['ticker'] == ticker].copy()
    ticker_data = ticker_data.sort_values('time_avail_m')

    # Extend final observation to 2007-01
    last_row = ticker_data.iloc[-1].copy()
    last_row['time_avail_m'] = pd.Timestamp('2007-01-01')
    ticker_data = pd.concat([ticker_data, pd.DataFrame([last_row])], ignore_index=True)

    # Fill in monthly observations between survey dates
    min_time = ticker_data['time_avail_m'].min()
    max_time = ticker_data['time_avail_m'].max()
    full_range = pd.date_range(start=min_time, end=max_time, freq='MS')

    # Reindex to monthly frequency and forward fill G-index values
    ticker_data = ticker_data.set_index('time_avail_m').reindex(full_range)
    ticker_data.index.name = 'time_avail_m'
    ticker_data = ticker_data.reset_index()

    # Forward fill ticker and G-index values
    ticker_data['ticker'] = ticker_data['ticker'].ffill()
    ticker_data['G'] = ticker_data['G'].ffill()

    extended_data.append(ticker_data)

# Combine all tickers into final dataset
final_data = pd.concat(extended_data, ignore_index=True)

# Keep only necessary columns for output
keep_cols = ['ticker', 'time_avail_m', 'G']
final_data = final_data[keep_cols]

# Format columns for output
final_data['time_avail_m'] = pd.to_datetime(final_data['time_avail_m'])
final_data['G'] = final_data['G'].astype('int8')

# Sort by ticker and date
final_data = final_data.sort_values(['ticker', 'time_avail_m']).reset_index(drop=True)

print(f"After interpolation: {len(final_data)} records")

# Apply row limit for debugging if configured
if MAX_ROWS_DL > 0:
    final_data = final_data.head(MAX_ROWS_DL)
    print(f"DEBUG MODE: Limited to {MAX_ROWS_DL} rows")

# Save final dataset
final_data.to_parquet("../pyData/Intermediate/GovIndex.parquet")

print(f"Governance Index data saved with {len(final_data)} records")

# Display summary statistics
print(f"Date range: {final_data['time_avail_m'].min()} to {final_data['time_avail_m'].max()}")
print(f"Unique tickers: {final_data['ticker'].nunique()}")

g_clean = final_data['G'].dropna()
print(f"G-Index summary - Mean: {g_clean.mean():.2f}, Std: {g_clean.std():.2f}")

print("\nSample data:")
print(final_data.head())
