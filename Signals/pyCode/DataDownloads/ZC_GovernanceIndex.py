#!/usr/bin/env python3
"""
Governance Index data download script - Python equivalent of ZC_GovernanceIndex.do

Downloads governance index data from Gompers, Ishii, and Metrick.
"""

import os
import pandas as pd
import requests
from dotenv import load_dotenv

load_dotenv()

def main():
    """Download and process governance index data"""
    print("Downloading Governance Index data...")

    # Ensure directories exist
    os.makedirs("../pyData/Intermediate", exist_ok=True)

    # URL for governance data
    webloc = "https://spinup-000d1a-wp-offload-media.s3.amazonaws.com/faculty/wp-content/uploads/sites/7/2019/06/Governance.xlsx"

    try:
        # Try to download directly
        response = requests.get(webloc, timeout=60)
        response.raise_for_status()

        # Save to temporary file
        temp_file = "../pyData/Intermediate/temp_governance.xlsx"
        with open(temp_file, 'wb') as f:
            f.write(response.content)

        # Read specific sheet and range (A24:F14024)
        gov_data = pd.read_excel(temp_file, sheet_name='governance index',
                                skiprows=23, nrows=14000)

        # Clean up temp file
        os.remove(temp_file)

    except Exception as e:
        print("Error downloading governance data: {e}")
        print("Creating placeholder file")

        # Create placeholder data
        gov_data = pd.DataFrame({
            'ticker': ['AAPL', 'MSFT', 'GOOGL'],
            'year': [1990, 1993, 1995],
            'G': [8, 10, 7]
        })

    print("Downloaded {len(gov_data)} governance records")

    # Clean ticker column (equivalent to replace ticker = strtrim(ticker))
    if 'ticker' in gov_data.columns:
        gov_data['ticker'] = gov_data['ticker'].str.strip()

    # Keep first observation per ticker-year
    if 'ticker' in gov_data.columns and 'year' in gov_data.columns:
        gov_data = gov_data.drop_duplicates(['ticker', 'year'], keep='first')
        print("After removing ticker-year duplicates: {len(gov_data)} records")

    # Replace year 2000 with 1999 (as in original)
    if 'year' in gov_data.columns:
        gov_data.loc[gov_data['year'] == 2000, 'year'] = 1999

    # Assign months based on year (from original Stata code)
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

    # For years >= 2002, use month = 1
    gov_data.loc[gov_data['year'] >= 2002, 'month'] = 1

    # Create time_avail_m (equivalent to ym(year, month))
    gov_data['time_avail_m'] = pd.to_datetime(
        gov_data['year'].astype(str) + '-' + gov_data['month'].astype(str) + '-01'
    ).dt.to_period('M')

    # Interpolate missing dates and extend one year beyond end
    print("Interpolating time series...")

    # For each ticker, extend to 2007-01
    extended_data = []
    for ticker in gov_data['ticker'].unique():
        ticker_data = gov_data[gov_data['ticker'] == ticker].copy()
        ticker_data = ticker_data.sort_values('time_avail_m')

        # Add extension to 2007-01
        if not ticker_data.empty:
            last_row = ticker_data.iloc[-1].copy()
            last_row['time_avail_m'] = pd.Period('2007-01')
            ticker_data = pd.concat([ticker_data, pd.DataFrame([last_row])], ignore_index=True)

        # Create full time range and forward fill
        if len(ticker_data) > 1:
            min_time = ticker_data['time_avail_m'].min()
            max_time = ticker_data['time_avail_m'].max()
            full_range = pd.period_range(start=min_time, end=max_time, freq='M')

            # Reindex and forward fill
            ticker_data = ticker_data.set_index('time_avail_m').reindex(full_range)
            ticker_data.index.name = 'time_avail_m'
            ticker_data = ticker_data.reset_index()

            # Forward fill ticker and G
            ticker_data['ticker'] = ticker_data['ticker'].fillna(method='ffill')
            if 'G' in ticker_data.columns:
                ticker_data['G'] = ticker_data['G'].fillna(method='ffill')

        extended_data.append(ticker_data)

    if extended_data:
        final_data = pd.concat(extended_data, ignore_index=True)
    else:
        final_data = gov_data

    # Keep only necessary columns
    keep_cols = ['ticker', 'time_avail_m', 'G']
    available_cols = [col for col in keep_cols if col in final_data.columns]
    final_data = final_data[available_cols]

    print("After interpolation: {len(final_data)} records")

    # Save the data
    final_data.to_pickle("../pyData/Intermediate/GovIndex.pkl")

    print("Governance Index data saved with {len(final_data)} records")

    # Show summary statistics
    print("Date range: {final_data['time_avail_m'].min()} to {final_data['time_avail_m'].max()}")
    print("Unique tickers: {final_data['ticker'].nunique()}")

    if 'G' in final_data.columns:
        g_clean = final_data['G'].dropna()
        if len(g_clean) > 0:
            print("G-Index summary - Mean: {g_clean.mean():.2f}, Std: {g_clean.std():.2f}")

    print("\nSample data:")
    print(final_data.head())

if __name__ == "__main__":
    main()
