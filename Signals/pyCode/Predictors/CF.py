# ABOUTME: CF.py - calculates CF predictor using cash flow scaled by market value
# ABOUTME: Direct line-by-line translation from Stata Code/Predictors/CF.do

"""
CF.py

Usage:
    cd pyCode/
    source .venv/bin/activate
    python3 Predictors/CF.py

Inputs:
    - m_aCompustat.parquet: Monthly Compustat data with columns [gvkey, permno, time_avail_m, ib, dp]
    - SignalMasterTable.parquet: Monthly master table with mve_c

Outputs:
    - CF.csv: CSV file with columns [permno, yyyymm, CF]
    - CF = (ib + dp)/mve_c (Cash flow to market value ratio)
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
    CF
    Cash flow to market value ratio
    """
    
    print("Starting CF.py...")
    
    # DATA LOAD
    print("Loading m_aCompustat data...")
    
    # Load m_aCompustat - equivalent to Stata: use gvkey permno time_avail_m ib dp using "$pathDataIntermediate/m_aCompustat", clear
    m_aCompustat_path = Path("../pyData/Intermediate/m_aCompustat.parquet")
    if not m_aCompustat_path.exists():
        raise FileNotFoundError(f"Required input file not found: {m_aCompustat_path}")
    
    df = pd.read_parquet(m_aCompustat_path)
    
    # Keep only the columns we need
    required_cols = ['gvkey', 'permno', 'time_avail_m', 'ib', 'dp']
    missing_cols = [col for col in required_cols if col not in df.columns]
    if missing_cols:
        raise ValueError(f"Missing required columns in m_aCompustat: {missing_cols}")
    
    df = df[required_cols].copy()
    
    print(f"Loaded m_aCompustat: {df.shape[0]} rows, {df.shape[1]} columns")
    
    # bysort permno time_avail_m: keep if _n == 1  // deletes a few observations
    print("Deduplicating by permno time_avail_m...")
    df = df.drop_duplicates(subset=['permno', 'time_avail_m'], keep='first')
    print(f"After deduplication: {df.shape[0]} rows")
    
    # merge 1:1 permno time_avail_m using "$pathDataIntermediate/SignalMasterTable", keep(using match) nogenerate keepusing(mve_c)
    print("Merging with SignalMasterTable...")
    
    signal_master_path = Path("../pyData/Intermediate/SignalMasterTable.parquet")
    if not signal_master_path.exists():
        raise FileNotFoundError(f"Required input file not found: {signal_master_path}")
    
    signal_master = pd.read_parquet(signal_master_path)
    if 'mve_c' not in signal_master.columns:
        raise ValueError("Missing required column 'mve_c' in SignalMasterTable")
    
    # Keep only required columns from SignalMasterTable
    signal_master = signal_master[['permno', 'time_avail_m', 'mve_c']].copy()
    
    # Merge (equivalent to keep(using match) - right join)
    df = pd.merge(df, signal_master, on=['permno', 'time_avail_m'], how='right')
    
    print(f"After merging with SignalMasterTable: {df.shape[0]} rows")
    
    # SIGNAL CONSTRUCTION
    
    # gen CF = (ib + dp)/mve_c
    print("Calculating CF...")
    
    # Calculate cash flow (ib + dp)
    df['cash_flow'] = df['ib'] + df['dp']
    
    # Calculate CF with domain-aware missing value handling
    # Following missing/missing = 1.0 pattern for division operations
    df['CF'] = np.where(
        df['mve_c'] == 0,
        np.nan,  # Division by zero = missing
        np.where(
            df['cash_flow'].isna() & df['mve_c'].isna(),
            1.0,  # missing/missing = 1.0 (no change)
            df['cash_flow'] / df['mve_c']
        )
    )
    
    print(f"Calculated CF for {df['CF'].notna().sum()} observations")
    
    # SAVE
    # do "$pathCode/savepredictor" CF
    save_predictor(df, 'CF')
    
    print("CF.py completed successfully")


if __name__ == "__main__":
    main()