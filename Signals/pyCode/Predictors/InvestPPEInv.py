# ABOUTME: InvestPPEInv.py - calculates InvestPPEInv predictor using PPE and inventory changes to assets
# ABOUTME: Direct line-by-line translation from Stata Code/Predictors/InvestPPEInv.do

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


def main():
    """
    InvestPPEInv
    PPE and inventory changes to assets
    """
    
    print("Starting InvestPPEInv.py...")
    
    # DATA LOAD
    print("Loading m_aCompustat data...")
    
    # Load m_aCompustat - equivalent to Stata: use gvkey permno time_avail_m ppegt invt at using "$pathDataIntermediate/m_aCompustat", clear
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
    
    # bysort permno time_avail_m: keep if _n == 1  // deletes a few observations
    print("Removing duplicate permno-time_avail_m observations...")
    initial_rows = len(df)
    df = df.drop_duplicates(subset=['permno', 'time_avail_m'], keep='first')
    print(f"Removed {initial_rows - len(df)} duplicate observations")
    
    # xtset permno time_avail_m
    print("Setting up panel data (sorting by permno, time_avail_m)...")
    df = df.sort_values(['permno', 'time_avail_m'])
    
    # Create 12-month lags: l12.ppegt, l12.invt, l12.at
    print("Calculating 12-month lags...")
    df['l12_ppegt'] = df.groupby('permno')['ppegt'].shift(12)
    df['l12_invt'] = df.groupby('permno')['invt'].shift(12)
    df['l12_at'] = df.groupby('permno')['at'].shift(12)
    
    # gen tempPPE = ppegt - l12.ppegt
    print("Calculating tempPPE...")
    df['tempPPE'] = df['ppegt'] - df['l12_ppegt']
    
    # gen tempInv = invt - l12.invt
    print("Calculating tempInv...")
    df['tempInv'] = df['invt'] - df['l12_invt']
    
    # gen InvestPPEInv = (tempPPE + tempInv)/l12.at
    print("Calculating InvestPPEInv...")
    df['InvestPPEInv'] = np.where(
        df['l12_at'] == 0,
        np.nan,  # Division by zero = missing
        (df['tempPPE'] + df['tempInv']) / df['l12_at']
    )
    
    print(f"Calculated InvestPPEInv for {df['InvestPPEInv'].notna().sum()} observations")
    
    # SAVE
    # do "$pathCode/savepredictor" InvestPPEInv
    save_predictor(df, 'InvestPPEInv')
    
    print("InvestPPEInv.py completed successfully")


if __name__ == "__main__":
    main()