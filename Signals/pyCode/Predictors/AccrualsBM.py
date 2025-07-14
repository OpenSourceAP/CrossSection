# ABOUTME: AccrualsBM.py - Accruals and BM signal, direct translation from AccrualsBM.do  
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
    AccrualsBM
    Direct translation from AccrualsBM.do
    """
    
    print("Starting AccrualsBM.py...")
    
    # DATA LOAD
    # use gvkey permno time_avail_m ceq act che lct dlc txp at using "$pathDataIntermediate/m_aCompustat", clear
    print("Loading m_aCompustat data...")
    
    m_aCompustat_path = Path("../pyData/Intermediate/m_aCompustat.parquet")
    if not m_aCompustat_path.exists():
        raise FileNotFoundError(f"Required input file not found: {m_aCompustat_path}")
    
    df = pd.read_parquet(m_aCompustat_path)
    
    # Keep only the columns we need
    required_cols = ['gvkey', 'permno', 'time_avail_m', 'ceq', 'act', 'che', 'lct', 'dlc', 'txp', 'at']
    missing_cols = [col for col in required_cols if col not in df.columns]
    if missing_cols:
        raise ValueError(f"Missing required columns in m_aCompustat: {missing_cols}")
    
    df = df[required_cols].copy()
    
    # bysort permno time_avail_m: keep if _n == 1  // deletes a few observations
    df = df.drop_duplicates(subset=['permno', 'time_avail_m'], keep='first')
    
    print(f"Loaded m_aCompustat: {df.shape[0]} rows, {df.shape[1]} columns")
    
    # merge 1:1 permno time_avail_m using "$pathDataIntermediate/SignalMasterTable", keep(using match) nogenerate keepusing(mve_c)
    print("Merging with SignalMasterTable...")
    
    SignalMasterTable_path = Path("../pyData/Intermediate/SignalMasterTable.parquet")
    if not SignalMasterTable_path.exists():
        raise FileNotFoundError(f"Required input file not found: {SignalMasterTable_path}")
    
    smt_df = pd.read_parquet(SignalMasterTable_path)
    
    # Keep only the columns we need from SignalMasterTable
    smt_cols = ['permno', 'time_avail_m', 'mve_c']
    missing_smt_cols = [col for col in smt_cols if col not in smt_df.columns]
    if missing_smt_cols:
        raise ValueError(f"Missing required columns in SignalMasterTable: {missing_smt_cols}")
    
    smt_df = smt_df[smt_cols].copy()
    
    # Merge (equivalent to keep(using match) - keep using + match, which means right join)
    # Stata keep(using match) = keep rows from using dataset + matched rows = right join
    df = df.merge(smt_df, on=['permno', 'time_avail_m'], how='right')
    
    print(f"After SignalMasterTable merge: {df.shape[0]} rows")
    
    # xtset permno time_avail_m
    df = df.sort_values(['permno', 'time_avail_m'])
    
    # SIGNAL CONSTRUCTION
    # gen BM = log(ceq/mve_c)
    df['BM'] = np.log(df['ceq'] / df['mve_c'])
    
    # gen tempacc = ( (act - l12.act) - (che - l12.che) - ( (lct - l12.lct) - ///
    # 	(dlc - l12.dlc) - (txp - l12.txp) )) / ( (at + l12.at)/2)
    
    # Create 12-month lags
    df['act_l12'] = df.groupby('permno')['act'].shift(12)
    df['che_l12'] = df.groupby('permno')['che'].shift(12)
    df['lct_l12'] = df.groupby('permno')['lct'].shift(12)
    df['dlc_l12'] = df.groupby('permno')['dlc'].shift(12)
    df['txp_l12'] = df.groupby('permno')['txp'].shift(12)
    df['at_l12'] = df.groupby('permno')['at'].shift(12)
    
    # Calculate temporary accruals
    df['tempacc'] = (
        (df['act'] - df['act_l12']) - (df['che'] - df['che_l12']) -
        ((df['lct'] - df['lct_l12']) - (df['dlc'] - df['dlc_l12']) - (df['txp'] - df['txp_l12']))
    ) / ((df['at'] + df['at_l12']) / 2)
    
    # egen tempqBM = fastxtile(BM), by(time_avail_m) n(5)
    # egen tempqAcc = fastxtile(tempacc), by(time_avail_m) n(5)
    df['tempqBM'] = df.groupby('time_avail_m')['BM'].transform(lambda x: pd.qcut(x, q=5, labels=False, duplicates='drop') + 1)
    df['tempqAcc'] = df.groupby('time_avail_m')['tempacc'].transform(lambda x: pd.qcut(x, q=5, labels=False, duplicates='drop') + 1)
    
    # gen AccrualsBM = 1 if tempqBM == 5 & tempqAcc == 1
    # replace AccrualsBM = 0 if tempqBM == 1 & tempqAcc == 5
    # replace AccrualsBM = . if ceq <0
    df['AccrualsBM'] = np.nan
    df.loc[(df['tempqBM'] == 5) & (df['tempqAcc'] == 1), 'AccrualsBM'] = 1
    df.loc[(df['tempqBM'] == 1) & (df['tempqAcc'] == 5), 'AccrualsBM'] = 0
    df.loc[df['ceq'] < 0, 'AccrualsBM'] = np.nan
    
    # drop temp*
    df = df.drop(columns=[col for col in df.columns if col.startswith('temp')])
    df = df.drop(columns=[col for col in df.columns if col.endswith('_l12')])
    
    print(f"After signal construction: {df.shape[0]} rows")
    print(f"AccrualsBM non-missing values: {df['AccrualsBM'].notna().sum()}")
    print(f"AccrualsBM = 1: {(df['AccrualsBM'] == 1).sum()}")
    print(f"AccrualsBM = 0: {(df['AccrualsBM'] == 0).sum()}")
    
    # SAVE
    # do "$pathCode/savepredictor" AccrualsBM
    savepredictor(df, 'AccrualsBM')
    
    print("AccrualsBM.py completed successfully")

if __name__ == "__main__":
    main()