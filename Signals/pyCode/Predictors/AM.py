# ABOUTME: AM.py - calculates AM predictor using total assets scaled by market value
# ABOUTME: Direct line-by-line translation from Stata Code/Predictors/AM.do

"""
AM.py

Usage:
    cd pyCode/
    source .venv/bin/activate
    python3 Predictors/AM.py

Inputs:
    - m_aCompustat.parquet: Monthly Compustat data with columns [permno, time_avail_m, at]
    - SignalMasterTable.parquet: Monthly master table with mve_c

Outputs:
    - AM.csv: CSV file with columns [permno, yyyymm, AM]
    - AM = at/mve_c (Total assets to market value ratio)
"""

import pandas as pd
import numpy as np
from pathlib import Path
import sys
import os

# Add utils directory to path for imports
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'utils'))
from savepredictor import save_predictor


def main():
    """
    AM
    Total assets to market value ratio
    """
    
    print("Starting AM.py...")
    
    # DATA LOAD
    print("Loading m_aCompustat data...")
    
    # Load m_aCompustat - equivalent to Stata: use permno time_avail_m at using "$pathDataIntermediate/m_aCompustat", clear
    m_aCompustat_path = Path("../pyData/Intermediate/m_aCompustat.parquet")
    if not m_aCompustat_path.exists():
        raise FileNotFoundError(f"Required input file not found: {m_aCompustat_path}")
    
    df = pd.read_parquet(m_aCompustat_path)
    
    # Keep only the columns we need
    required_cols = ['permno', 'time_avail_m', 'at']
    missing_cols = [col for col in required_cols if col not in df.columns]
    if missing_cols:
        raise ValueError(f"Missing required columns in m_aCompustat: {missing_cols}")
    
    df = df[required_cols].copy()
    
    print(f"Loaded m_aCompustat: {df.shape[0]} rows, {df.shape[1]} columns")
    
    # bysort permno time_avail_m: keep if _n == 1  // deletes a few observations
    print("Deduplicating by permno time_avail_m...")
    df = df.drop_duplicates(subset=['permno', 'time_avail_m'], keep='first')
    print(f"After deduplication: {df.shape[0]} rows")
    
    # merge 1:1 permno time_avail_m using "$pathDataIntermediate/SignalMasterTable", keep(match) nogenerate keepusing(mve_c)
    print("Merging with SignalMasterTable...")
    
    signal_master_path = Path("../pyData/Intermediate/SignalMasterTable.parquet")
    if not signal_master_path.exists():
        raise FileNotFoundError(f"Required input file not found: {signal_master_path}")
    
    signal_master = pd.read_parquet(signal_master_path)
    if 'mve_c' not in signal_master.columns:
        raise ValueError("Missing required column 'mve_c' in SignalMasterTable")
    
    # Keep only required columns from SignalMasterTable
    signal_master = signal_master[['permno', 'time_avail_m', 'mve_c']].copy()
    
    # Merge (equivalent to keep(match) - inner join)
    df = pd.merge(df, signal_master, on=['permno', 'time_avail_m'], how='inner')
    
    print(f"After merging with SignalMasterTable: {df.shape[0]} rows")
    
    # SIGNAL CONSTRUCTION
    
    # gen AM = at/mve_c
    print("Calculating AM...")
    df['AM'] = df['at'] / df['mve_c']
    
    print(f"Calculated AM for {df['AM'].notna().sum()} observations")
    
    # SAVE
    # do "$pathCode/savepredictor" AM
    save_predictor(df, 'AM')
    
    print("AM.py completed successfully")


if __name__ == "__main__":
    main()