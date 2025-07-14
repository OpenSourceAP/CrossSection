# ABOUTME: Accruals.py - Accruals signal based on Sloan 1996, direct translation from Accruals.do
# ABOUTME: Line-by-line translation preserving exact Stata logic and execution order

import pandas as pd
import numpy as np
from pathlib import Path
import sys

# Import savepredictor from parent directory
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from savepredictor import savepredictor

def main():
    """
    Accruals
    Direct translation from Accruals.do
    """
    
    print("Starting Accruals.py...")
    
    # DATA LOAD
    # use gvkey permno time_avail_m txp act che lct dlc at dp using "$pathDataIntermediate/m_aCompustat", clear
    print("Loading m_aCompustat data...")
    
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
    df = df.drop_duplicates(subset=['permno', 'time_avail_m'], keep='first')
    
    # xtset permno time_avail_m
    df = df.sort_values(['permno', 'time_avail_m'])
    
    # gen tempTXP = txp
    # replace tempTXP = 0 if mi(txp)
    df['tempTXP'] = df['txp'].copy()
    df['tempTXP'] = df['tempTXP'].fillna(0)
    
    # see eq 1, p 6 of Sloan 1996	
    # gen Accruals = ( (act - l12.act) - (che - l12.che) ///
    # 	- ( (lct - l12.lct) - (dlc - l12.dlc) - (tempTXP - l12.tempTXP) ) ///
    # 	- dp ) / ( (at + l12.at)/2)
    
    # Create 12-month lags (equivalent to l12. in Stata)
    df['act_l12'] = df.groupby('permno')['act'].shift(12)
    df['che_l12'] = df.groupby('permno')['che'].shift(12)
    df['lct_l12'] = df.groupby('permno')['lct'].shift(12)
    df['dlc_l12'] = df.groupby('permno')['dlc'].shift(12)
    df['tempTXP_l12'] = df.groupby('permno')['tempTXP'].shift(12)
    df['at_l12'] = df.groupby('permno')['at'].shift(12)
    
    # Calculate Accruals using Sloan 1996 equation 1
    df['Accruals'] = (
        (df['act'] - df['act_l12']) - (df['che'] - df['che_l12']) -
        ((df['lct'] - df['lct_l12']) - (df['dlc'] - df['dlc_l12']) - (df['tempTXP'] - df['tempTXP_l12'])) -
        df['dp']
    ) / ((df['at'] + df['at_l12']) / 2)
    
    # drop temp*
    df = df.drop(columns=[col for col in df.columns if col.startswith('temp')])
    df = df.drop(columns=[col for col in df.columns if col.endswith('_l12')])
    
    print(f"After signal construction: {df.shape[0]} rows")
    print(f"Accruals non-missing values: {df['Accruals'].notna().sum()}")
    
    # SAVE
    # do "$pathCode/savepredictor" Accruals
    savepredictor(df, 'Accruals')
    
    print("Accruals.py completed successfully")

if __name__ == "__main__":
    main()