# ABOUTME: DelDRC.py - calculates DelDRC predictor (Deferred Revenue)
# ABOUTME: Direct line-by-line translation from Stata Code/Predictors/DelDRC.do

"""
DelDRC.py

Usage:
    cd pyCode/
    source .venv/bin/activate
    python3 Predictors/DelDRC.py

Inputs:
    - m_aCompustat.parquet: Monthly Compustat data with columns [gvkey, permno, time_avail_m, drc, at, ceq, sale, sic]

Outputs:
    - DelDRC.csv: CSV file with columns [permno, yyyymm, DelDRC]
    - Change in deferred revenue normalized by average assets with filters applied
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
    DelDRC
    Deferred Revenue predictor with specific filters
    """
    
    print("Starting DelDRC.py...")
    
    # DATA LOAD
    print("Loading m_aCompustat data...")
    
    # Load m_aCompustat - equivalent to Stata: use gvkey permno time_avail_m drc at ceq sale sic using "$pathDataIntermediate/m_aCompustat", clear
    m_aCompustat_path = Path("../pyData/Intermediate/m_aCompustat.parquet")
    if not m_aCompustat_path.exists():
        raise FileNotFoundError(f"Required input file not found: {m_aCompustat_path}")
    
    df = pd.read_parquet(m_aCompustat_path)
    
    # Keep only the columns we need (equivalent to Stata's 'using' with specific variables)
    required_cols = ['gvkey', 'permno', 'time_avail_m', 'drc', 'at', 'ceq', 'sale', 'sic']
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
    
    # destring sic, replace (sic should already be numeric in parquet, but handle any issues)
    print("Ensuring sic is numeric...")
    df['sic'] = pd.to_numeric(df['sic'], errors='coerce')
    
    # Create lag variables (equivalent to l12. in Stata)
    print("Creating lag variables...")
    df['lag_drc'] = df.groupby('permno')['drc'].shift(12)
    df['lag_at'] = df.groupby('permno')['at'].shift(12)
    
    # gen DelDRC = (drc - l12.drc)/(.5*(at + l12.at))
    print("Calculating DelDRC...")
    df['DelDRC'] = (df['drc'] - df['lag_drc']) / (0.5 * (df['at'] + df['lag_at']))
    
    # replace DelDRC = . if ceq <=0 | (drc == 0 & DelDRC == 0) | sale < 5 | (sic >=6000 & sic < 7000)
    print("Applying filters...")
    
    # Create filter conditions
    filter_condition = (
        (df['ceq'] <= 0) | 
        ((df['drc'] == 0) & (df['DelDRC'] == 0)) | 
        (df['sale'] < 5) | 
        ((df['sic'] >= 6000) & (df['sic'] < 7000))
    )
    
    # Apply the filter - set DelDRC to NaN where filter condition is true
    df.loc[filter_condition, 'DelDRC'] = np.nan
    
    # Clean up temporary variables
    df = df.drop(columns=['lag_drc', 'lag_at'])
    
    print(f"Calculated DelDRC for {df['DelDRC'].notna().sum()} observations")
    
    # SAVE
    # do "$pathCode/savepredictor" DelDRC
    save_predictor(df, 'DelDRC')
    
    print("DelDRC.py completed successfully")


if __name__ == "__main__":
    main()