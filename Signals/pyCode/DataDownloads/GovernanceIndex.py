# ABOUTME: Downloads governance index data from Gompers, Ishii, and Metrick (1990-2007)
# ABOUTME: Creates monthly ticker-level panel with forward-filled G-index values through 2007
"""
Inputs:
- External URL: https://spinup-000d1a-wp-offload-media.s3.amazonaws.com/faculty/wp-content/uploads/sites/7/2019/06/Governance.xlsx

Outputs:
- ../pyData/Intermediate/GovIndex.parquet

How to run: from Signals/pyCode, run python3 DataDownloads/GovernanceIndex.py

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

DEBUG_ROWS = get_debug_row_limit("GovernanceIndex")

load_dotenv()

print("Downloading Governance Index data...")

# Obtain the survey-based governance scores used in the governance signal.
webloc = "https://spinup-000d1a-wp-offload-media.s3.amazonaws.com/faculty/wp-content/uploads/sites/7/2019/06/Governance.xlsx"

response = requests.get(webloc, timeout=60)
response.raise_for_status()

temp_file = "../pyData/Intermediate/temp_governance.xlsx"
with open(temp_file, 'wb') as f:
    f.write(response.content)

# Read the governance-score observations, excluding the workbook introduction.
gov_data = pd.read_excel(temp_file, sheet_name='governance index',
                        skiprows=23, nrows=14000)

os.remove(temp_file)

print(f"Downloaded {len(gov_data)} governance records")

# Remove ticker whitespace so repeated survey observations can be identified consistently.
gov_data['ticker'] = gov_data['ticker'].str.strip()

# Retain one source observation per ticker and survey year.
gov_data = gov_data.drop_duplicates(['ticker', 'year'], keep='first')
print(f"After removing ticker-year duplicates: {len(gov_data)} records")

# Assign the 2000-labelled survey to 1999 under the original signal convention.
gov_data.loc[gov_data['year'] == 2000, 'year'] = 1999

# Begin using each survey score in its specified publication month.
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

# Use January as the assumed publication month for surveys from 2002 onward.
gov_data.loc[gov_data['year'] >= 2002, 'month'] = 1

gov_data['time_avail_m'] = pd.to_datetime(
    gov_data['year'].astype(str) + '-' + gov_data['month'].astype(str) + '-01'
).dt.to_period('M').dt.to_timestamp()

# Carry the latest published score forward between surveys to form a monthly panel.
print("Interpolating time series...")

extended_data = []
for ticker in gov_data['ticker'].unique():
    ticker_data = gov_data[gov_data['ticker'] == ticker].copy()
    ticker_data = ticker_data.sort_values('time_avail_m')

    # Extend the final reported score to January 2007.
    last_row = ticker_data.iloc[-1].copy()
    last_row['time_avail_m'] = pd.Timestamp('2007-01-01')
    ticker_data = pd.concat([ticker_data, pd.DataFrame([last_row])], ignore_index=True)

    # Include every month between the first survey and the end of the extended history.
    min_time = ticker_data['time_avail_m'].min()
    max_time = ticker_data['time_avail_m'].max()
    full_range = pd.date_range(start=min_time, end=max_time, freq='MS')

    ticker_data = ticker_data.set_index('time_avail_m').reindex(full_range)
    ticker_data.index.name = 'time_avail_m'
    ticker_data = ticker_data.reset_index()

    # Use the most recent survey score in months without a new survey.
    ticker_data['ticker'] = ticker_data['ticker'].ffill()
    ticker_data['G'] = ticker_data['G'].ffill()

    extended_data.append(ticker_data)

final_data = pd.concat(extended_data, ignore_index=True)

# Provide one governance score per ticker-month.
keep_cols = ['ticker', 'time_avail_m', 'G']
final_data = final_data[keep_cols]

final_data['time_avail_m'] = pd.to_datetime(final_data['time_avail_m'])
final_data['G'] = final_data['G'].astype('int8')

final_data = final_data.sort_values(['ticker', 'time_avail_m']).reset_index(drop=True)

print(f"After interpolation: {len(final_data)} records")

# Apply row limit for debugging if configured
if DEBUG_MODE:
    final_data = final_data.head(DEBUG_ROWS)
    print(f"DEBUG MODE: Limited to {DEBUG_ROWS} rows")

# Save the monthly governance-score history for downstream signals.
final_data.to_parquet("../pyData/Intermediate/GovIndex.parquet")

print(f"Governance Index data saved with {len(final_data)} records")

print(f"Date range: {final_data['time_avail_m'].min()} to {final_data['time_avail_m'].max()}")
print(f"Unique tickers: {final_data['ticker'].nunique()}")

g_clean = final_data['G'].dropna()
print(f"G-Index summary - Mean: {g_clean.mean():.2f}, Std: {g_clean.std():.2f}")

print("\nSample data:")
print(final_data.head())
