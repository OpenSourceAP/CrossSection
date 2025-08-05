#!/usr/bin/env python3
"""
GNP Deflator download script - Python equivalent of U_GNPDeflator.do

Downloads GNP deflator from FRED, expands quarterly to monthly,
and adds 3-month lag.
"""

import os
import time
import pandas as pd
import numpy as np
import requests
from dotenv import load_dotenv
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from config import MAX_ROWS_DL
from utils.column_standardizer_yaml import standardize_columns

load_dotenv()


def download_fred_series(series_id, api_key, max_retries=3, retry_delay=1):
    """Download a series from FRED API with retry logic.

    Args:
        series_id: FRED series identifier
        api_key: FRED API key
        max_retries: Maximum number of retry attempts
        retry_delay: Initial delay between retries (seconds)

    Returns:
        pandas.DataFrame: DataFrame with date and value columns
    """
    url = "https://api.stlouisfed.org/fred/series/observations"
    params = {
        'series_id': series_id,
        'api_key': api_key,
        'file_type': 'json',
        'observation_start': '1900-01-01'
    }

    for attempt in range(max_retries + 1):
        try:
            print(f"Downloading {series_id} (attempt {attempt + 1}...)")
            response = requests.get(url, params=params, timeout=30)
            response.raise_for_status()
            data = response.json()

            # Check for API errors in response
            if 'error_code' in data:
                raise requests.exceptions.RequestException(
                    f"FRED API error {data['error_code']}: "
                    f"{data.get('error_message', 'Unknown error')}"
                )

            if 'observations' in data:
                df = pd.DataFrame(data['observations'])
                if len(df) == 0:
                    print(f"Warning: No observations found for {series_id}")
                    return pd.DataFrame()

                df['date'] = pd.to_datetime(df['date'])
                df['value'] = pd.to_numeric(df['value'], errors='coerce')
                df = df[['date', 'value']].dropna()
                print(f"Successfully downloaded {len(df)} observations")
                return df
            else:
                print(f"No observations found for {series_id}")
                return pd.DataFrame()

        except requests.exceptions.Timeout:
            print(f"Timeout downloading {series_id} (attempt {attempt + 1})")
        except requests.exceptions.ConnectionError:
            print(f"Connection error downloading {series_id} "
                  f"(attempt {attempt + 1})")
        except requests.exceptions.RequestException as e:
            print(f"Request error downloading {series_id}: {e}")
            if "API key" in str(e) or "error_code" in str(e):
                # Don't retry on API key errors
                break
        except Exception as e:
            print(f"Unexpected error downloading {series_id}: {e}")

        if attempt < max_retries:
            delay = retry_delay * (2 ** attempt)  # Exponential backoff
            print(f"Retrying in {delay} seconds...")
            time.sleep(delay)

    print(f"Failed to download {series_id} after {max_retries + 1} attempts")
    return pd.DataFrame()


def main():
    """Main function to download and process GNP deflator data"""
    print("Downloading GNP Deflator from FRED...")

    # Get FRED API key from environment
    fred_api_key = os.getenv("FRED_API_KEY")
    if not fred_api_key:
        print("WARNING: FRED_API_KEY not found in environment variables")
        print("GNP deflator data requires FRED API key. "
              "Creating placeholder file.")

        # Create placeholder data (quarterly data)
        dates = pd.date_range(
            start='2020-01-01', end='2024-12-31', freq='Q'
        )
        placeholder_data = pd.DataFrame({
            'date': dates,
            'value': np.linspace(120, 130, len(dates))  # Fake values
        })

        os.makedirs("../pyData/Intermediate", exist_ok=True)

        # Process placeholder data
        deflator_data = placeholder_data.copy()

    else:
        # Ensure directories exist
        os.makedirs("../pyData/Intermediate", exist_ok=True)

        # Download GNPCTPI (GNP: Chain-type Price Index)
        deflator_data = download_fred_series('GNPCTPI', fred_api_key)

        if deflator_data.empty:
            print("Failed to download GNP deflator data")
            return

    # Convert to monthly periods (preserve as datetime64[ns] for parquet compatibility)
    # (equivalent to gen temp_time_m = mofd(daten))
    # Keep as datetime64[ns] instead of Period to maintain type compatibility with DTA format
    deflator_data['temp_time_m'] = deflator_data['date'].dt.to_period('M').dt.to_timestamp()

    # Expand quarterly data to monthly (equivalent to expand 3)
    monthly_data = []
    for _, row in deflator_data.iterrows():
        # Convert to period for arithmetic, then back to timestamp
        base_period = pd.to_datetime(row['temp_time_m']).to_period('M')
        for i in range(3):  # 3 months per quarter
            new_row = row.copy()
            # Add months and convert back to timestamp
            new_row['time_avail_m'] = (base_period + i).to_timestamp()
            monthly_data.append(new_row)

    monthly_deflator = pd.DataFrame(monthly_data)

    # Add 3-month availability lag
    # (equivalent to replace time_avail_m = time_avail_m + 3)
    # Convert to period for arithmetic, then back to timestamp
    monthly_deflator['time_avail_m'] = (
        pd.to_datetime(monthly_deflator['time_avail_m']).dt.to_period('M') + 3
    ).dt.to_timestamp()

    # Create gnpdefl variable
    # (equivalent to gen gnpdefl = GNPCTPI/100)
    monthly_deflator['gnpdefl'] = monthly_deflator['value'] / 100
    
    # Keep only necessary columns
    final_data = monthly_deflator[['time_avail_m', 'gnpdefl']].copy()

    # Remove duplicates (in case of overlapping quarters)
    final_data = final_data.drop_duplicates(subset=['time_avail_m'])

    # Apply row limit for debugging if configured
    if MAX_ROWS_DL > 0:
        final_data = final_data.head(MAX_ROWS_DL)
        print(f"DEBUG MODE: Limited to {MAX_ROWS_DL} rows")

    # Save the data
    # Apply column standardization
    final_data = standardize_columns(final_data, 'GNPdefl')
    final_data.to_parquet("../pyData/Intermediate/GNPdefl.parquet", index=False)

    print(f"GNP Deflator data saved with {len(final_data)} monthly records")
    date_min = final_data['time_avail_m'].min()
    date_max = final_data['time_avail_m'].max()
    print(f"Date range: {date_min} to {date_max}")

    # Show sample data
    print("\nSample data:")
    print(final_data.head())

    # Show summary statistics
    print("\nGNP Deflator summary:")
    print(f"Mean: {final_data['gnpdefl'].mean():.3f}")
    print(f"Min: {final_data['gnpdefl'].min():.3f}")
    print(f"Max: {final_data['gnpdefl'].max():.3f}")


if __name__ == "__main__":
    main()
