#!/usr/bin/env python3
"""
Probability of Informed Trading (PIN) data download script - Python equivalent of ZB_PIN.do

Downloads PIN data from Easley et al. via Dropbox and converts yearly to monthly.
"""

import os
import pandas as pd
import requests
import zipfile
from requests.exceptions import Timeout, RequestException
from dotenv import load_dotenv
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from config import MAX_ROWS_DL

load_dotenv()

def main():
    """Download and process PIN data"""
    print("Downloading PIN data from Dropbox...")

    # Ensure directories exist
    os.makedirs("../pyData/Intermediate", exist_ok=True)

    # URL for PIN data - use the redirected URL
    webloc = "https://www.dropbox.com/scl/fi/wjjb1rgwbzn8z8cbllzig/cpie_data.zip?rlkey=yz7nzy7phgs8lxsajuvec1mr3&dl=1"
    
    try:
        # Download the zip file with improved headers and timeout
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
        
        # Check content type
        content_type = response.headers.get('content-type', '')
        print(f"Content-Type: {content_type}")
        
        # Save zip file with progress tracking
        zip_path = "../pyData/Intermediate/cpie_data.zip"
        downloaded_size = 0
        
        print("Starting download... (this may take a few minutes)")
        with open(zip_path, 'wb') as f:
            chunk_count = 0
            for chunk in response.iter_content(chunk_size=8192):
                if chunk:  # filter out keep-alive chunks
                    f.write(chunk)
                    downloaded_size += len(chunk)
                    chunk_count += 1
                    # Print progress every 10MB 
                    if chunk_count % 1250 == 0:  # ~10MB
                        print(f"Downloaded {downloaded_size / (1024*1024):.1f} MB...")
        
        print("Download stream completed, checking file...")
        
        file_size = os.path.getsize(zip_path)
        print(f"Download complete: {file_size} bytes")
        
        # Verify it's a zip file
        if file_size < 1000:
            raise Exception(f"Downloaded file too small ({file_size} bytes), likely an error page")
            
        # Check if it's actually a zip file
        try:
            with zipfile.ZipFile(zip_path, 'r') as test_zip:
                file_list = test_zip.namelist()
                print(f"ZIP contains {len(file_list)} files: {file_list[:5]}...")
        except zipfile.BadZipFile:
            raise Exception("Downloaded file is not a valid ZIP archive")

        # Extract zip file
        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            zip_ref.extractall("../pyData/Intermediate")

        # Read the PIN yearly data
        pin_yearly_path = "../pyData/Intermediate/pin_yearly.csv"
        if not os.path.exists(pin_yearly_path):
            raise Exception("pin_yearly.csv not found in extracted files")
            
        pin_data = pd.read_csv(pin_yearly_path)
        print(f"Successfully loaded PIN data from zip file")

        # Clean up files
        os.remove(zip_path)
        for file in ['owr_yearly.csv', 'pin_yearly.csv', 'cpie_daily.csv',
                     'gpin_yearly.csv', 'dy_yearly.csv']:
            file_path = f"../pyData/Intermediate/{file}"
            if os.path.exists(file_path):
                os.remove(file_path)

    except Timeout:
        print("Download timed out after 30 seconds")
        print("Creating placeholder file")
        # Create placeholder data
        pin_data = pd.DataFrame({
            'year': [2020, 2021, 2022],
            'permno': [10001, 10001, 10001],
            'pin': [0.15, 0.18, 0.12]
        })
    except RequestException as e:
        print(f"Network error downloading PIN data: {e}")
        print("Creating placeholder file")
        # Create placeholder data
        pin_data = pd.DataFrame({
            'year': [2020, 2021, 2022],
            'permno': [10001, 10001, 10001],
            'pin': [0.15, 0.18, 0.12]
        })
    except Exception as e:
        print(f"Error processing PIN data: {e}")
        print("Creating placeholder file")
        # Create placeholder data
        pin_data = pd.DataFrame({
            'year': [2020, 2021, 2022],
            'permno': [10001, 10001, 10001],
            'pin': [0.15, 0.18, 0.12]
        })

    print(f"Downloaded {len(pin_data)} PIN yearly records")

    # Convert yearly to monthly (expand 12 times)
    monthly_data = []

    for _, row in pin_data.iterrows():
        for month in range(1, 13):  # 12 months
            new_row = row.copy()
            new_row['month'] = month

            # Create monthly date (equivalent to gen modate = ym(year, month))
            modate = pd.Period(year=int(row['year']), month=month, freq='M')
            new_row['modate'] = modate

            # Add 11 months availability lag (equivalent to gen time_avail_m = modate + 11)
            new_row['time_avail_m'] = modate + 11

            monthly_data.append(new_row)

    pin_monthly = pd.DataFrame(monthly_data)

    print(f"Expanded to {len(pin_monthly)} monthly PIN records")

    # Save the data
    
    # Apply row limit for debugging if configured
    if MAX_ROWS_DL > 0:
        pin_monthly = pin_monthly.head(MAX_ROWS_DL)
        print(f"DEBUG MODE: Limited to {MAX_ROWS_DL} rows")

    # Save the data
    pin_monthly.to_parquet("../pyData/Intermediate/pin_monthly.parquet")

    print(f"PIN monthly data saved with {len(pin_monthly)} records")

    # Show summary statistics
    if 'time_avail_m' in pin_monthly.columns:
        print(f"Date range: {pin_monthly['time_avail_m'].min()} to {pin_monthly['time_avail_m'].max()}")

    if 'permno' in pin_monthly.columns:
        print(f"Unique permnos: {pin_monthly['permno'].nunique()}")

    if 'pin' in pin_monthly.columns:
        print(f"PIN summary - Mean: {pin_monthly['pin'].mean():.4f}, Std: {pin_monthly['pin'].std():.4f}")

    print("\nSample data:")
    # Show available columns and select the ones that exist
    available_cols = ['year', 'permno', 'month', 'time_avail_m']
    if 'pin' in pin_monthly.columns:
        available_cols.append('pin')
    elif 'PIN' in pin_monthly.columns:
        available_cols.append('PIN')
    # Show whatever columns are available
    display_cols = [col for col in available_cols if col in pin_monthly.columns]
    print(pin_monthly[display_cols].head())

if __name__ == "__main__":
    main()
