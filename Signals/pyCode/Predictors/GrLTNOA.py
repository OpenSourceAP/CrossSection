# ABOUTME: GrLTNOA.py - calculates GrLTNOA predictor using growth in long term net operating assets
# ABOUTME: Direct line-by-line translation from Stata Code/Predictors/GrLTNOA.do

"""
GrLTNOA.py

Usage:
    cd pyCode/
    source .venv/bin/activate
    python3 Predictors/GrLTNOA.py

Inputs:
    - m_aCompustat.parquet: Monthly Compustat data with columns [gvkey, permno, time_avail_m, rect, invt, ppent, aco, intan, ao, ap, lco, lo, at, dp]

Outputs:
    - GrLTNOA.csv: CSV file with columns [permno, yyyymm, GrLTNOA]
    - GrLTNOA = Growth in long term net operating assets
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
    GrLTNOA
    Growth in long term net operating assets
    """
    
    print("Starting GrLTNOA.py...")
    
    # DATA LOAD
    print("Loading m_aCompustat data...")
    
    # Load m_aCompustat - equivalent to Stata: use gvkey permno time_avail_m rect invt ppent aco intan ao ap lco lo at dp using "$pathDataIntermediate/m_aCompustat", clear
    m_aCompustat_path = Path("../pyData/Intermediate/m_aCompustat.parquet")
    if not m_aCompustat_path.exists():
        raise FileNotFoundError(f"Required input file not found: {m_aCompustat_path}")
    
    df = pd.read_parquet(m_aCompustat_path)
    
    # Keep only the columns we need
    required_cols = ['gvkey', 'permno', 'time_avail_m', 'rect', 'invt', 'ppent', 'aco', 'intan', 'ao', 'ap', 'lco', 'lo', 'at', 'dp']
    missing_cols = [col for col in required_cols if col not in df.columns]
    if missing_cols:
        raise ValueError(f"Missing required columns in m_aCompustat: {missing_cols}")
    
    df = df[required_cols].copy()
    
    print(f"Loaded m_aCompustat: {df.shape[0]} rows, {df.shape[1]} columns")
    
    # SIGNAL CONSTRUCTION
    
    # bysort permno time_avail_m: keep if _n == 1  // deletes a few observations
    print("Removing duplicate observations...")
    initial_count = len(df)
    df = df.drop_duplicates(subset=['permno', 'time_avail_m'], keep='first')
    dropped_count = initial_count - len(df)
    if dropped_count > 0:
        print(f"Dropped {dropped_count} duplicate observations")
    
    # xtset permno time_avail_m
    print("Setting up panel data (sorting by permno, time_avail_m)...")
    df = df.sort_values(['permno', 'time_avail_m'])
    
    # Calculate 12-month lags for all required variables
    print("Calculating 12-month lags...")
    lag_vars = ['rect', 'invt', 'ppent', 'aco', 'intan', 'ao', 'ap', 'lco', 'lo', 'at']
    
    for var in lag_vars:
        df[f'l12_{var}'] = df.groupby('permno')[var].shift(12)
    
    # gen GrLTNOA = (rect + invt + ppent + aco + intan + ao - ap - lco - lo)/at - (l12.rect + l12.invt + 
    #     l12.ppent + l12.aco + l12.intan + l12.ao - l12.ap - l12.lco - l12.lo)/l12.at 
    #     - ( rect - l12.rect + invt - l12.invt + aco - l12.aco - (ap - l12.ap + lco - l12.lco) - dp )/((at + l12.at)/2)
    print("Calculating GrLTNOA...")
    
    # Current period LTNOA/at
    current_ltnoa = (df['rect'] + df['invt'] + df['ppent'] + df['aco'] + df['intan'] + df['ao'] - 
                     df['ap'] - df['lco'] - df['lo']) / df['at']
    
    # Lagged LTNOA/at
    lagged_ltnoa = (df['l12_rect'] + df['l12_invt'] + df['l12_ppent'] + df['l12_aco'] + df['l12_intan'] + df['l12_ao'] - 
                    df['l12_ap'] - df['l12_lco'] - df['l12_lo']) / df['l12_at']
    
    # Change in working capital and depreciation adjustment
    # (rect - l12.rect + invt - l12.invt + aco - l12.aco - (ap - l12.ap + lco - l12.lco) - dp) / ((at + l12.at)/2)
    wc_adjustment = ((df['rect'] - df['l12_rect']) + (df['invt'] - df['l12_invt']) + (df['aco'] - df['l12_aco']) - 
                     ((df['ap'] - df['l12_ap']) + (df['lco'] - df['l12_lco'])) - df['dp']) / ((df['at'] + df['l12_at']) / 2)
    
    # Calculate GrLTNOA
    df['GrLTNOA'] = current_ltnoa - lagged_ltnoa - wc_adjustment
    
    print(f"Calculated GrLTNOA for {df['GrLTNOA'].notna().sum()} observations")
    
    # SAVE
    # do "$pathCode/savepredictor" GrLTNOA
    save_predictor(df, 'GrLTNOA')
    
    print("GrLTNOA.py completed successfully")


if __name__ == "__main__":
    main()