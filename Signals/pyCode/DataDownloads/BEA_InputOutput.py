"""
ABOUTME: Download BEA Input-Output tables for Input-Output Momentum signal calculation
ABOUTME: Inputs: BEA.gov URLs for pre-1997 xlsx files and 1997-present zip file
ABOUTME: Outputs: 4 xlsx files in pyData/Intermediate/:
  - IOMake_Before_Redefinitions_1963-1996_Summary.xlsx
  - IOUse_Before_Redefinitions_PRO_1963-1996_Summary.xlsx
  - Supply_Tables_1997-20XX_Summary.xlsx
  - Supply-Use_Framework_1997-20XX_Summary.xlsx
ABOUTME: Usage: python BEA_InputOutput.py (run from pyCode/)
"""

import os
import requests
import zipfile
import re


data_dir = os.path.join('..', 'pyData', 'Intermediate')

# Download required pre-1997 tables directly as xlsx
pre1997_urls = [
    ("https://apps.bea.gov/industry/xls/io-annual/IOMake_Before_Redefinitions_1963-1996_Summary.xlsx",
        "IOMake_Before_Redefinitions_1963-1996_Summary.xlsx"),
    ("https://apps.bea.gov/industry/xls/io-annual/IOUse_Before_Redefinitions_PRO_1963-1996_Summary.xlsx",
        "IOUse_Before_Redefinitions_PRO_1963-1996_Summary.xlsx")
]

for url, filename in pre1997_urls:
    filepath = os.path.join(data_dir, filename)
    response = requests.get(url, stream=True, timeout=300)
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    with open(filepath, 'wb') as f:
        for chunk in response.iter_content(chunk_size=8192):
            f.write(chunk)

# Download all 1997-present tables as zip
zip_url = "https://apps.bea.gov//industry/iTables%20Static%20Files/AllTablesSUP.zip"
zip_path = os.path.join(data_dir, 'temp_bea.zip')

response = requests.get(zip_url, stream=True, timeout=300)
with open(zip_path, 'wb') as f:
    for chunk in response.iter_content(chunk_size=8192):
        f.write(chunk)

# unzip the necessary files for 1997-present
with zipfile.ZipFile(zip_path, 'r') as zip_ref:
    file_list = zip_ref.namelist()

    supply_files = [f for f in file_list if re.search(r"Supply_Tables_1997-2[0-9]{3}_Summary\.xlsx", f, re.IGNORECASE)]
    use_files = [f for f in file_list if re.search(r"Supply-Use_Framework_1997-2[0-9]{3}_Summary\.xlsx", f, re.IGNORECASE)]

    zip_ref.extract(supply_files[0], data_dir)
    zip_ref.extract(use_files[0], data_dir)

os.unlink(zip_path)