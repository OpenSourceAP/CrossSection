# ABOUTME: Creates InvestPPEInv predictor measuring investment in property, plant, equipment and inventory scaled by assets
# ABOUTME: Run from pyCode/ directory: python3 Predictors/InvestPPEInv.py

"""
InvestPPEInv.py

Usage:
    cd pyCode/
    source .venv/bin/activate
    python3 Predictors/InvestPPEInv.py

Inputs:
    - m_aCompustat.parquet: Monthly Compustat data with columns [gvkey, permno, time_avail_m, ppegt, invt, at]

Outputs:
    - InvestPPEInv.csv: CSV file with columns [permno, yyyymm, InvestPPEInv]
    - InvestPPEInv = (tempPPE + tempInv)/l12.at where:
      - tempPPE = ppegt - l12.ppegt
      - tempInv = invt - l12.invt
"""

import pandas as pd
import numpy as np
from pathlib import Path
import sys
import os

# Add utils directory to path for imports
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from utils.save_standardized import save_predictor


print("Starting InvestPPEInv.py...")

# DATA LOAD
print("Loading m_aCompustat data...")

# Load monthly Compustat data with PPE, inventory, and total assets
m_aCompustat_path = Path("../pyData/Intermediate/m_aCompustat.parquet")
if not m_aCompustat_path.exists():
    raise FileNotFoundError(f"Required input file not found: {m_aCompustat_path}")

df = pd.read_parquet(m_aCompustat_path)

# Keep only the columns we need
required_cols = ['gvkey', 'permno', 'time_avail_m', 'ppegt', 'invt', 'at']
missing_cols = [col for col in required_cols if col not in df.columns]
if missing_cols:
    raise ValueError(f"Missing required columns in m_aCompustat: {missing_cols}")

df = df[required_cols].copy()

print(f"Loaded m_aCompustat: {df.shape[0]} rows, {df.shape[1]} columns")

# SIGNAL CONSTRUCTION

# Remove duplicate firm-month observations
print("Removing duplicate permno-time_avail_m observations...")
initial_rows = len(df)
df = df.drop_duplicates(subset=['permno', 'time_avail_m'], keep='first')
print(f"Removed {initial_rows - len(df)} duplicate observations")

# Sort data by firm and time for time series calculations
print("Setting up panel data (sorting by permno, time_avail_m)...")
df = df.sort_values(['permno', 'time_avail_m'])

# Calculate 12-month lagged values for PPE, inventory, and total assets
print("Calculating 12-month lags...")
df['l12_ppegt'] = df.groupby('permno')['ppegt'].shift(12)
df['l12_invt'] = df.groupby('permno')['invt'].shift(12)
df['l12_at'] = df.groupby('permno')['at'].shift(12)

# Calculate year-over-year change in property, plant and equipment
print("Calculating tempPPE...")
df['tempPPE'] = df['ppegt'] - df['l12_ppegt']

# Calculate year-over-year change in inventory
print("Calculating tempInv...")
df['tempInv'] = df['invt'] - df['l12_invt']

# Calculate investment measure as sum of PPE and inventory changes scaled by lagged total assets
print("Calculating InvestPPEInv...")
df['InvestPPEInv'] = np.where(
    df['l12_at'] == 0,
    np.nan,  # Division by zero = missing
    (df['tempPPE'] + df['tempInv']) / df['l12_at']
)

print(f"Calculated InvestPPEInv for {df['InvestPPEInv'].notna().sum()} observations")

# SAVE
save_predictor(df, 'InvestPPEInv')

print("InvestPPEInv.py completed successfully")