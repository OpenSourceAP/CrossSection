# ABOUTME: Downloads 3-month T-bill rate from FRED and aggregates to quarterly averages
# ABOUTME: Creates year-quarter-level dataset with TbillRate3M variable for downstream analysis
"""
Inputs:
- FRED API TB3MS series (monthly 3-month Treasury bill rates)
- FRED_API_KEY environment variable

Outputs:
- ../pyData/Intermediate/TBill3M.parquet

How to run: from Signals/pyCode, run python3 DataDownloads/TreasuryBill3M.py

Use the project Python environment at /opt/venv/projects/openap.
"""

import os
import pandas as pd
import numpy as np
import requests
from dotenv import load_dotenv

load_dotenv()

print("Processing 3-month T-bill rate...")

fred_api_key = os.getenv("FRED_API_KEY")

# Obtain monthly three-month Treasury bill rates for the quarterly interest-rate measure.
print("Downloading TB3MS from FRED...")
url = "https://api.stlouisfed.org/fred/series/observations"
params = {
    'series_id': 'TB3MS',
    'api_key': fred_api_key,
    'file_type': 'json',
    'observation_start': '1900-01-01'
}

response = requests.get(url, params=params, timeout=30)
data = response.json()
df = pd.DataFrame(data['observations'])
df['date'] = pd.to_datetime(df['date'])
df['TB3MS'] = pd.to_numeric(df['value'], errors='coerce')
monthly_data = df[['date', 'TB3MS']].dropna()

print(f"Downloaded {len(monthly_data)} monthly observations")

monthly_data = monthly_data.set_index('date')

# Use the average available monthly rate to represent each calendar quarter.
quarterly_data = monthly_data.resample('QE').mean()
quarterly_data = quarterly_data.dropna().reset_index()

print(f"Aggregated to {len(quarterly_data)} quarterly observations")

# Express the annualized quoted rate as a decimal, without changing its rate convention.
quarterly_data['TbillRate3M'] = quarterly_data['TB3MS'] / 100.0

# Identify calendar quarters for joining the rate to quarterly signal inputs.
quarterly_data['qtr'] = quarterly_data['date'].dt.quarter

quarterly_data['year'] = quarterly_data['date'].dt.year

final_data = quarterly_data[['year', 'qtr', 'TbillRate3M']].copy()

print(f"Final dataset: {len(final_data)} quarterly records")
date_range_start = (
    f"{final_data['year'].min()}Q"
    f"{final_data[final_data['year'] == final_data['year'].min()]['qtr'].min()}"
)
date_range_end = (
    f"{final_data['year'].max()}Q"
    f"{final_data[final_data['year'] == final_data['year'].max()]['qtr'].max()}"
)
print(f"Date range: {date_range_start} to {date_range_end}")

# Save quarterly Treasury bill rates for downstream signals.
final_data.to_parquet("../pyData/Intermediate/TBill3M.parquet", index=False)

print("3-month T-bill rate data saved successfully")

print("\nSample data:")
print(final_data.head())

print("\nT-bill rate summary:")
print(f"Mean: {final_data['TbillRate3M'].mean():.6f}")
print(f"Std: {final_data['TbillRate3M'].std():.6f}")
print(f"Min: {final_data['TbillRate3M'].min():.6f}")
print(f"Max: {final_data['TbillRate3M'].max():.6f}")
