#!/usr/bin/env python3
"""
ABOUTME: Downloads BEA Input-Output tables for Input-Output momentum analysis  
ABOUTME: Downloads 1963-1996 Make/Use tables and 1997+ zip file with Supply/Use tables

Inputs: None (downloads from public BEA URLs)
Outputs: 4 Excel files saved to ../pyData/Intermediate/

How to run: python3 BEA_InputOutput.py
"""

import os
import requests
import tempfile
import zipfile
import re

def download(url, dest):
    """Download file from url to dest"""
    with open(dest, 'wb') as f:
        f.write(requests.get(url).content)

os.makedirs("../pyData/Intermediate", exist_ok=True)

# Download 1963-1996 tables
download("https://apps.bea.gov/industry/xls/io-annual/IOMake_Before_Redefinitions_1963-1996_Summary.xlsx",
         "../pyData/Intermediate/IOMake_Before_Redefinitions_1963-1996_Summary.xlsx")

download("https://apps.bea.gov/industry/xls/io-annual/IOUse_Before_Redefinitions_PRO_1963-1996_Summary.xlsx", 
         "../pyData/Intermediate/IOUse_Before_Redefinitions_PRO_1963-1996_Summary.xlsx")

# Download and extract 1997+ zip
download("https://apps.bea.gov//industry/iTables%20Static%20Files/AllTablesSUP.zip", 
         "../pyData/Intermediate/AllTablesSUP.zip")

with zipfile.ZipFile("../pyData/Intermediate/AllTablesSUP.zip", 'r') as z:
    files = z.namelist()
    supply_file = [f for f in files if "Supply_Tables_" in f and f.endswith(".xlsx")][0]
    use_file = [f for f in files if "Supply-Use_Framework" in f and f.endswith(".xlsx")][0]
    z.extract(supply_file, "../pyData/Intermediate")
    z.extract(use_file, "../pyData/Intermediate")

print("✅ BEA Input-Output tables downloaded successfully")