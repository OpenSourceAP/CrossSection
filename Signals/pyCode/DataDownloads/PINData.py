# ABOUTME: Downloads Probability of Informed Trading (PIN) data from Easley et al. via Dropbox
# ABOUTME: Converts yearly PIN parameters to monthly data with 11-month availability lag
"""
Inputs:
- Dropbox ZIP file containing pin_yearly.csv (Easley et al. PIN data)

Outputs:
- ../pyData/Intermediate/pin_monthly.parquet

Download or source-processing failures stop the script before writing monthly output.

How to run: from Signals/pyCode, run python3 DataDownloads/PINData.py

Use the project Python environment at /opt/venv/projects/openap.
"""

import os
import pandas as pd
import requests
import zipfile
from dotenv import load_dotenv
import sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from config import DEBUG_MODE
from utils.debug_mode import get_debug_row_limit

DEBUG_ROWS = get_debug_row_limit("PINData")

load_dotenv()


def main():
    print("Downloading PIN data from Dropbox...")

    os.makedirs("../pyData/Intermediate", exist_ok=True)

    # Obtain annual informed-trading estimates for the PIN signal.
    webloc = "https://www.dropbox.com/scl/fi/wjjb1rgwbzn8z8cbllzig/cpie_data.zip?rlkey=yz7nzy7phgs8lxsajuvec1mr3&dl=1"

    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Accept-Encoding': 'gzip, deflate',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
        }

        print(f"Attempting to download from: {webloc}")
        response = requests.get(webloc, headers=headers, timeout=30, allow_redirects=True, stream=True)
        response.raise_for_status()

        # Report the received file type to help diagnose failed source downloads.
        content_type = response.headers.get('content-type', '')
        print(f"Content-Type: {content_type}")

        zip_path = "../pyData/Intermediate/cpie_data.zip"
        downloaded_size = 0

        print("Starting download... (this may take a few minutes)")
        with open(zip_path, 'wb') as f:
            chunk_count = 0
            for chunk in response.iter_content(chunk_size=8192):
                if chunk:
                    f.write(chunk)
                    downloaded_size += len(chunk)
                    chunk_count += 1
                    # Print progress every 10MB
                    if chunk_count % 1250 == 0:
                        print(f"Downloaded {downloaded_size / (1024*1024):.1f} MB...")

        print("Download stream completed, checking file...")

        file_size = os.path.getsize(zip_path)
        print(f"Download complete: {file_size} bytes")

        # Reject likely error pages before treating the response as a data archive.
        if file_size < 1000:
            raise ValueError(f"Downloaded file too small ({file_size} bytes), likely an error page")

        # Require annual observations from this download before preparing monthly data.
        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            file_list = zip_ref.namelist()
            print(f"ZIP contains {len(file_list)} files: {file_list[:5]}...")

            # Use only observations from this download, never a leftover extracted CSV.
            with zip_ref.open('pin_yearly.csv') as yearly_file:
                pin_data = pd.read_csv(yearly_file)
        print(f"Successfully loaded PIN data from zip file")

        os.remove(zip_path)
    except Exception as error:
        raise RuntimeError(
            'PIN source download or parsing failed; monthly output was not updated.'
        ) from error

    print(f"Downloaded {len(pin_data)} PIN yearly records")

    # Carry each annual PIN estimate across twelve monthly signal observations.
    monthly_data = []

    for _, row in pin_data.iterrows():
        for month in range(1, 13):
            new_row = row.copy()
            new_row['month'] = month

            # Retain the source year/month alongside the later availability month.
            modate = pd.Period(year=int(row['year']), month=month, freq='M').to_timestamp()
            new_row['modate'] = modate

            # Delay availability by the specified eleven-month lag.
            time_avail_period = pd.Period(year=int(row['year']), month=month, freq='M') + 11
            new_row['time_avail_m'] = time_avail_period.to_timestamp()

            monthly_data.append(new_row)

    pin_monthly = pd.DataFrame(monthly_data)

    print(f"Expanded to {len(pin_monthly)} monthly PIN records")

    # Keep stock identifiers compatible with the monthly CRSP panel.
    pin_monthly['permno'] = pin_monthly['permno'].astype('int64')

    # Apply debugging row limit if configured
    if DEBUG_MODE:
        pin_monthly = pin_monthly.head(DEBUG_ROWS)
        print(f"DEBUG MODE: Limited to {DEBUG_ROWS} rows")

    # Save monthly PIN estimates with their lagged availability dates.
    pin_monthly.to_parquet("../pyData/Intermediate/pin_monthly.parquet", index=False)

    print(f"PIN monthly data saved with {len(pin_monthly)} records")

    if 'time_avail_m' in pin_monthly.columns:
        print(f"Date range: {pin_monthly['time_avail_m'].min()} to {pin_monthly['time_avail_m'].max()}")

    if 'permno' in pin_monthly.columns:
        print(f"Unique permnos: {pin_monthly['permno'].nunique()}")

    param_cols = ['a', 'eb', 'es', 'u', 'd']
    for col in param_cols:
        if col in pin_monthly.columns:
            print(f"{col} summary - Mean: {pin_monthly[col].mean():.4f}, Std: {pin_monthly[col].std():.4f}")

    print("\nSample data:")
    available_cols = ['permno', 'year', 'month', 'time_avail_m'] + param_cols
    display_cols = [col for col in available_cols if col in pin_monthly.columns]
    print(pin_monthly[display_cols].head())


if __name__ == "__main__":
    main()
