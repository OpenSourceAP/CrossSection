# ABOUTME: AccrualsBM.py - calculates AccrualsBM predictor combining accruals and book-to-market
# ABOUTME: Direct line-by-line translation from Stata Code/Predictors/AccrualsBM.do

"""
AccrualsBM.py

Usage:
    cd pyCode/
    source .venv/bin/activate
    python3 Predictors/AccrualsBM.py

Inputs:
    - m_aCompustat.parquet: Monthly Compustat data with columns [gvkey, permno, time_avail_m, ceq, act, che, lct, dlc, txp, at]
    - SignalMasterTable.parquet: Monthly master table with mve_c

Outputs:
    - AccrualsBM.csv: CSV file with columns [permno, yyyymm, AccrualsBM]
    - Binary signal: 1 if high BM + low accruals, 0 if low BM + high accruals
"""

import pandas as pd
import numpy as np
from pathlib import Path
import sys
import os

# Add utils directory to path for imports
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'utils'))
from savepredictor import save_predictor


def fastxtile(series, n_quantiles=5):
    """
    Python equivalent of Stata's fastxtile function using pd.qcut
    Returns quantile ranks (1 to n_quantiles) for a series
    Following StataDocs/fastxtile.md recommendations
    """
    try:
        # Handle -inf values by replacing them with NaN before quantile calculation
        # This matches Stata's behavior where extreme values are excluded from quantile calculation
        series_clean = series.replace([np.inf, -np.inf], np.nan)
        
        # Use pd.qcut with duplicates='drop' as recommended in StataDocs
        return pd.qcut(series_clean, q=n_quantiles, labels=False, duplicates='drop') + 1
    except Exception:
        # Fallback for edge cases (all NaN, insufficient data, etc.)
        return pd.Series(np.nan, index=series.index)


def main():
    """
    AccrualsBM
    Combines accruals and book-to-market into binary signal
    """
    
    print("Starting AccrualsBM.py...")
    
    # DATA LOAD
    print("Loading m_aCompustat data...")
    
    # Load m_aCompustat - equivalent to Stata: use gvkey permno time_avail_m ceq act che lct dlc txp at using "$pathDataIntermediate/m_aCompustat", clear
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
    
    # Merge (equivalent to keep(using match) - right join to keep all SignalMasterTable obs)
    df = pd.merge(df, signal_master, on=['permno', 'time_avail_m'], how='right')
    
    print(f"After merging with SignalMasterTable: {df.shape[0]} rows")
    
    # xtset permno time_avail_m (setup for lag operations)
    print("Setting up panel data structure...")
    df = df.sort_values(['permno', 'time_avail_m'])
    
    # SIGNAL CONSTRUCTION
    
    # gen BM = log(ceq/mve_c)
    print("Calculating BM...")
    df['BM'] = np.log(df['ceq'] / df['mve_c'])
    
    # Create lag variables for accruals calculation
    print("Creating lag variables for accruals...")
    df['lag_act'] = df.groupby('permno')['act'].shift(12)
    df['lag_che'] = df.groupby('permno')['che'].shift(12)
    df['lag_lct'] = df.groupby('permno')['lct'].shift(12)
    df['lag_dlc'] = df.groupby('permno')['dlc'].shift(12)
    df['lag_txp'] = df.groupby('permno')['txp'].shift(12)
    df['lag_at'] = df.groupby('permno')['at'].shift(12)
    
    # gen tempacc = ( (act - l12.act) - (che - l12.che) - ( (lct - l12.lct) - (dlc - l12.dlc) - (txp - l12.txp) )) / ( (at + l12.at)/2)
    print("Calculating tempacc...")
    df['tempacc'] = (
        (df['act'] - df['lag_act']) - (df['che'] - df['lag_che']) -
        ((df['lct'] - df['lag_lct']) - (df['dlc'] - df['lag_dlc']) - (df['txp'] - df['lag_txp']))
    ) / ((df['at'] + df['lag_at']) / 2)
    
    # egen tempqBM = fastxtile(BM), by(time_avail_m) n(5)
    print("Creating BM quintiles...")
    df['tempqBM'] = df.groupby('time_avail_m')['BM'].transform(lambda x: fastxtile(x, 5))
    
    # egen tempqAcc = fastxtile(tempacc), by(time_avail_m) n(5)
    print("Creating accruals quintiles...")
    df['tempqAcc'] = df.groupby('time_avail_m')['tempacc'].transform(lambda x: fastxtile(x, 5))
    
    # gen AccrualsBM = 1 if tempqBM == 5 & tempqAcc == 1
    # replace AccrualsBM = 0 if tempqBM == 1 & tempqAcc == 5
    # replace AccrualsBM = . if ceq <0
    print("Generating AccrualsBM signal...")
    df['AccrualsBM'] = np.nan
    
    # High BM (quintile 5) and low accruals (quintile 1) = 1
    df.loc[(df['tempqBM'] == 5) & (df['tempqAcc'] == 1), 'AccrualsBM'] = 1
    
    # Low BM (quintile 1) and high accruals (quintile 5) = 0
    df.loc[(df['tempqBM'] == 1) & (df['tempqAcc'] == 5), 'AccrualsBM'] = 0
    
    # Set missing if negative book equity
    df.loc[df['ceq'] < 0, 'AccrualsBM'] = np.nan
    
    # drop temp*
    temp_cols = [col for col in df.columns if col.startswith('temp')]
    lag_cols = [col for col in df.columns if col.startswith('lag_')]
    drop_cols = temp_cols + lag_cols
    df = df.drop(columns=drop_cols)
    
    print(f"Calculated AccrualsBM for {df['AccrualsBM'].notna().sum()} observations")
    
    # SAVE
    # do "$pathCode/savepredictor" AccrualsBM
    save_predictor(df, 'AccrualsBM')
    
    print("AccrualsBM.py completed successfully")


if __name__ == "__main__":
    main()