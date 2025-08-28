# ABOUTME: DelCOA.py - calculates DelCOA predictor (Change in current operating assets)
# ABOUTME: Direct line-by-line translation from Stata Code/Predictors/DelCOA.do

"""
DelCOA.py

Usage:
    cd pyCode/
    source .venv/bin/activate
    python3 Predictors/DelCOA.py

Inputs:
    - m_aCompustat.parquet: Monthly Compustat data with columns [gvkey, permno, time_avail_m, at, act, che]

Outputs:
    - DelCOA.csv: CSV file with columns [permno, yyyymm, DelCOA]
    - Change in current operating assets normalized by average assets
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
    DelCOA
    Change in current operating assets normalized by average assets
    """
    
    print("Starting DelCOA.py...")
    
    # DATA LOAD
    print("Loading m_aCompustat data...")
    
    # Load m_aCompustat - equivalent to Stata: use gvkey permno time_avail_m at act che using "$pathDataIntermediate/m_aCompustat", clear
    m_aCompustat_path = Path("../pyData/Intermediate/m_aCompustat.parquet")
    if not m_aCompustat_path.exists():
        raise FileNotFoundError(f"Required input file not found: {m_aCompustat_path}")
    
    df = pd.read_parquet(m_aCompustat_path)
    ##Print query of df == 23033 (bad permno), tell claude to add similiar feedback for debugging
    # Keep only the columns we need (equivalent to Stata's 'using' with specific variables)
    required_cols = ['gvkey', 'permno', 'time_avail_m', 'at', 'act', 'che']
    missing_cols = [col for col in required_cols if col not in df.columns]
    if missing_cols:
        raise ValueError(f"Missing required columns in m_aCompustat: {missing_cols}")
    
    df = df[required_cols].copy()
    
    print(f"Loaded m_aCompustat: {df.shape[0]} rows, {df.shape[1]} columns")
    
    # SIGNAL CONSTRUCTION
    
    # bysort permno time_avail_m: keep if _n == 1  // deletes a few observations
    print("Deduplicating by permno time_avail_m...")
    df = df.drop_duplicates(subset=['permno', 'time_avail_m'], keep='first')
    print(f"After deduplication: {df.shape[0]} rows")
    
    # xtset permno time_avail_m (setup for lag operations)
    print("Setting up panel data structure...")
    df = df.sort_values(['permno', 'time_avail_m'])
    
    # Create lag variables (equivalent to l12. in Stata)
    print("Creating lag variables...")
    df['lag_at'] = df.groupby('permno')['at'].shift(12)
    df['lag_act'] = df.groupby('permno')['act'].shift(12)
    df['lag_che'] = df.groupby('permno')['che'].shift(12)
    
    # gen tempAvAT = .5*(at + l12.at)
    print("Creating tempAvAT...")
    df['tempAvAT'] = 0.5 * (df['at'] + df['lag_at'])
    
    # gen DelCOA = (act - che) - (l12.act - l12.che)
    print("Calculating DelCOA...")
    df['DelCOA'] = (df['act'] - df['che']) - (df['lag_act'] - df['lag_che'])
    
    # replace DelCOA = DelCOA/tempAvAT
    df['DelCOA'] = df['DelCOA'] / df['tempAvAT']
    
    # Clean up temporary variables
    df = df.drop(columns=['lag_at', 'lag_act', 'lag_che', 'tempAvAT'])
    
    print(f"Calculated DelCOA for {df['DelCOA'].notna().sum()} observations")
    
    # SAVE
    # do "$pathCode/savepredictor" DelCOA
    save_predictor(df, 'DelCOA')
    
    print("DelCOA.py completed successfully")


if __name__ == "__main__":
    main()