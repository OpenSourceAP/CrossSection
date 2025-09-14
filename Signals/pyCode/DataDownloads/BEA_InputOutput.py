## ABOUTME: Download BEA Input-Output tables for Input-Output Momentum signal calculation
## ABOUTME: Downloads pre-1997 and 1997-present BEA IO tables to pyData/Intermediate/
## ABOUTME: Usage: python BEA_InputOutput.py (run from pyCode/)

import os
import sys
import requests
import zipfile
import tempfile
from pathlib import Path
import re

def download_file(url, filepath, description=""):
    """Download a file with progress indication"""
    print(f"Downloading {description}...")
    try:
        response = requests.get(url, stream=True, timeout=300)
        response.raise_for_status()

        # Create directory if it doesn't exist
        os.makedirs(os.path.dirname(filepath), exist_ok=True)

        with open(filepath, 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)

        # Basic validation
        if os.path.getsize(filepath) > 0:
            print(f"✓ Downloaded: {os.path.basename(filepath)}")
            return True
        else:
            print(f"✗ Failed: {os.path.basename(filepath)} (empty file)")
            return False

    except Exception as e:
        print(f"✗ Error downloading {description}: {e}")
        return False

def main():
    # Set project root relative to current working directory
    project_root = '..'
    data_dir = os.path.join(project_root, 'pyData', 'Intermediate')

    print("Downloading BEA Input-Output tables...")

    # Download pre-1997 tables
    print("\nDownloading pre-1997 tables...")

    make_pre1997_url = "https://apps.bea.gov/industry/xls/io-annual/IOMake_Before_Redefinitions_1963-1996_Summary.xlsx"
    make_pre1997_path = os.path.join(data_dir, 'IOMake_Before_Redefinitions_1963-1996_Summary.xlsx')

    use_pre1997_url = "https://apps.bea.gov/industry/xls/io-annual/IOUse_Before_Redefinitions_PRO_1963-1996_Summary.xlsx"
    use_pre1997_path = os.path.join(data_dir, 'IOUse_Before_Redefinitions_PRO_1963-1996_Summary.xlsx')

    success_count = 0
    if download_file(make_pre1997_url, make_pre1997_path, "IOMake pre-1997"):
        success_count += 1
    if download_file(use_pre1997_url, use_pre1997_path, "IOUse pre-1997"):
        success_count += 1

    # Download 1997-present tables
    print("\nDownloading 1997-present tables...")

    zip_url = "https://apps.bea.gov//industry/iTables%20Static%20Files/AllTablesSUP.zip"

    try:
        # Download ZIP to temporary file
        with tempfile.NamedTemporaryFile(delete=False) as tmp_file:
            tmp_path = tmp_file.name

        if download_file(zip_url, tmp_path, "AllTablesSUP.zip"):
            # Extract and find matching files
            with zipfile.ZipFile(tmp_path, 'r') as zip_ref:
                file_list = zip_ref.namelist()

                # Find Supply and Use tables
                supply_pattern = r"Supply_Tables_1997-2[0-9]{3}_Summary\.xlsx"
                use_pattern = r"Supply-Use_Framework_1997-2[0-9]{3}_Summary\.xlsx"

                supply_files = [f for f in file_list if re.search(supply_pattern, f, re.IGNORECASE)]
                use_files = [f for f in file_list if re.search(use_pattern, f, re.IGNORECASE)]

                if len(supply_files) != 1 or len(use_files) != 1:
                    print(f"✗ Error: Expected 1 Supply and 1 Use file, found {len(supply_files)} Supply and {len(use_files)} Use files")
                    sys.exit(1)

                # Extract the files
                supply_file = supply_files[0]
                use_file = use_files[0]

                zip_ref.extract(supply_file, data_dir)
                zip_ref.extract(use_file, data_dir)

                print(f"✓ Extracted: {os.path.basename(supply_file)}")
                print(f"✓ Extracted: {os.path.basename(use_file)}")
                success_count += 2

        # Clean up temporary file
        os.unlink(tmp_path)

    except Exception as e:
        print(f"✗ Error processing ZIP file: {e}")

    # Final status
    print(f"\nDownload complete: {success_count}/4 files successfully downloaded")

    if success_count == 4:
        print("✓ All BEA Input-Output tables downloaded successfully")
        return True
    else:
        print("✗ Some downloads failed")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)