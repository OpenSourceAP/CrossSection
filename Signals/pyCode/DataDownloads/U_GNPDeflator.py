# ABOUTME: Downloads quarterly GNP deflator from FRED API and expands to monthly with 3-month lag
# ABOUTME: Processes GNPCTPI index data and outputs monthly time series for economic analysis
"""
Inputs:
- FRED API (GNPCTPI series - GNP: Chain-type Price Index)
- FRED_API_KEY environment variable

Outputs:
- ../pyData/Intermediate/GNPdefl.parquet

How to run: python3 U_GNPDeflator.py
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


# Download FRED series with retry logic
def download_fred_series(series_id, api_key, max_retries=3, retry_delay=1):
    # Set up FRED API request parameters
    url = "https://api.stlouisfed.org/fred/series/observations"
    params = {
        'series_id': series_id,
        'api_key': api_key,
        'file_type': 'json',
        'observation_start': '1900-01-01'
    }

    # Retry loop for robust downloading
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

            # Process successful response
            if 'observations' in data:
                df = pd.DataFrame(data['observations'])
                if len(df) == 0:
                    print(f"Warning: No observations found for {series_id}")
                    return pd.DataFrame()

                # Clean and format data
                df['date'] = pd.to_datetime(df['date'])
                df['value'] = pd.to_numeric(df['value'], errors='coerce')
                df = df[['date', 'value']].dropna()
                print(f"Successfully downloaded {len(df)} observations")
                return df
            else:
                print(f"No observations found for {series_id}")
                return pd.DataFrame()

        # Handle various error types
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

        # Exponential backoff before retry
        if attempt < max_retries:
            delay = retry_delay * (2 ** attempt)
            print(f"Retrying in {delay} seconds...")
            time.sleep(delay)

    print(f"Failed to download {series_id} after {max_retries + 1} attempts")
    return pd.DataFrame()


# Main processing function
def main():
    print("Downloading GNP Deflator from FRED...")

    # Check for FRED API key
    fred_api_key = os.getenv("FRED_API_KEY")
    if not fred_api_key:
        print("WARNING: FRED_API_KEY not found in environment variables")
        print("GNP deflator data requires FRED API key. "
              "Creating placeholder file.")

        # Create placeholder quarterly data for testing
        dates = pd.date_range(
            start='2020-01-01', end='2024-12-31', freq='Q'
        )
        placeholder_data = pd.DataFrame({
            'date': dates,
            'value': np.linspace(120, 130, len(dates))
        })

        os.makedirs("../pyData/Intermediate", exist_ok=True)
        deflator_data = placeholder_data.copy()

    else:
        # Download real data from FRED
        os.makedirs("../pyData/Intermediate", exist_ok=True)
        deflator_data = download_fred_series('GNPCTPI', fred_api_key)

        if deflator_data.empty:
            print("Failed to download GNP deflator data")
            return

    # Convert quarterly dates to monthly periods
    deflator_data['temp_time_m'] = deflator_data['date'].dt.to_period('M').dt.to_timestamp()

    # Expand quarterly data to monthly (3 months per quarter)
    monthly_data = []
    for _, row in deflator_data.iterrows():
        base_period = pd.to_datetime(row['temp_time_m']).to_period('M')
        for i in range(3):
            new_row = row.copy()
            new_row['time_avail_m'] = (base_period + i).to_timestamp()
            monthly_data.append(new_row)

    monthly_deflator = pd.DataFrame(monthly_data)

    # Add 3-month availability lag for realistic data timing
    monthly_deflator['time_avail_m'] = (
        pd.to_datetime(monthly_deflator['time_avail_m']).dt.to_period('M') + 3
    ).dt.to_timestamp()

    # Convert index to ratio (divide by 100)
    monthly_deflator['gnpdefl'] = monthly_deflator['value'] / 100
    
    # Keep final columns and remove duplicates
    final_data = monthly_deflator[['time_avail_m', 'gnpdefl']].copy()
    final_data = final_data.drop_duplicates(subset=['time_avail_m'])

    # Apply debug row limit if configured
    if MAX_ROWS_DL > 0:
        final_data = final_data.head(MAX_ROWS_DL)
        print(f"DEBUG MODE: Limited to {MAX_ROWS_DL} rows")

    # Standardize columns and save to parquet
    final_data = standardize_columns(final_data, 'GNPdefl')
    final_data.to_parquet("../pyData/Intermediate/GNPdefl.parquet", index=False)

    # Print summary information
    print(f"GNP Deflator data saved with {len(final_data)} monthly records")
    date_min = final_data['time_avail_m'].min()
    date_max = final_data['time_avail_m'].max()
    print(f"Date range: {date_min} to {date_max}")

    print("\nSample data:")
    print(final_data.head())

    print("\nGNP Deflator summary:")
    print(f"Mean: {final_data['gnpdefl'].mean():.3f}")
    print(f"Min: {final_data['gnpdefl'].min():.3f}")
    print(f"Max: {final_data['gnpdefl'].max():.3f}")


if __name__ == "__main__":
    main()
