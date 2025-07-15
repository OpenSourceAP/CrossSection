# ABOUTME: Accruals.py - calculates Accruals predictor using Sloan 1996 formula
# ABOUTME: Direct line-by-line translation from Stata Code/Predictors/Accruals.do

"""
Accruals.py

Usage:
    cd pyCode/
    source .venv/bin/activate
    python3 Predictors/Accruals.py

Inputs:
    - m_aCompustat.parquet: Monthly Compustat data with columns [gvkey, permno, time_avail_m, txp, act, che, lct, dlc, at, dp]

Outputs:
    - Accruals.csv: CSV file with columns [permno, yyyymm, Accruals]
    - Implements Sloan 1996 equation 1 (page 6)
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
    Accruals
    Implements Sloan 1996's accruals measure (equation 1, page 6)
    """
    
    print("Starting Accruals.py...")
    
    # DATA LOAD
    print("Loading m_aCompustat data...")
    
    # Load m_aCompustat - equivalent to Stata: use gvkey permno time_avail_m txp act che lct dlc at dp using "$pathDataIntermediate/m_aCompustat", clear
    m_aCompustat_path = Path("../pyData/Intermediate/m_aCompustat.parquet")
    if not m_aCompustat_path.exists():
        raise FileNotFoundError(f"Required input file not found: {m_aCompustat_path}")
    
    df = pd.read_parquet(m_aCompustat_path)
    
    # Keep only the columns we need (equivalent to Stata's 'using' with specific variables)
    required_cols = ['gvkey', 'permno', 'time_avail_m', 'txp', 'act', 'che', 'lct', 'dlc', 'at', 'dp']
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
    
    # gen tempTXP = txp
    # replace tempTXP = 0 if mi(txp)
    df['tempTXP'] = df['txp'].fillna(0)
    
    # Create lag variables (equivalent to l12. in Stata)
    print("Creating lag variables...")
    df['lag_act'] = df.groupby('permno')['act'].shift(12)
    df['lag_che'] = df.groupby('permno')['che'].shift(12)
    df['lag_lct'] = df.groupby('permno')['lct'].shift(12)
    df['lag_dlc'] = df.groupby('permno')['dlc'].shift(12)
    df['lag_tempTXP'] = df.groupby('permno')['tempTXP'].shift(12)
    df['lag_at'] = df.groupby('permno')['at'].shift(12)
    
    # Accruals calculation - see eq 1, p 6 of Sloan 1996
    # gen Accruals = ( (act - l12.act) - (che - l12.che) ///
    # 	- ( (lct - l12.lct) - (dlc - l12.dlc) - (tempTXP - l12.tempTXP) ) ///
    # 	- dp ) / ( (at + l12.at)/2)
    print("Calculating Accruals...")
    
    df['Accruals'] = (
        (df['act'] - df['lag_act']) - (df['che'] - df['lag_che']) -
        ((df['lct'] - df['lag_lct']) - (df['dlc'] - df['lag_dlc']) - (df['tempTXP'] - df['lag_tempTXP'])) -
        df['dp']
    ) / ((df['at'] + df['lag_at']) / 2)
    
    # drop temp*
    df = df.drop(columns=['tempTXP', 'lag_act', 'lag_che', 'lag_lct', 'lag_dlc', 'lag_tempTXP', 'lag_at'])
    
    print(f"Calculated Accruals for {df['Accruals'].notna().sum()} observations")
    
    # SAVE
    # do "$pathCode/savepredictor" Accruals
    save_predictor(df, 'Accruals')
    
    print("Accruals.py completed successfully")


if __name__ == "__main__":
    main()