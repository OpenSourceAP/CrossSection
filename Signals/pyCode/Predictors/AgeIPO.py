# ABOUTME: AgeIPO.py - calculates AgeIPO predictor using firm age for recent IPO companies
# ABOUTME: Direct line-by-line translation from Stata Code/Predictors/AgeIPO.do

"""
AgeIPO.py

Usage:
    cd pyCode/
    source .venv/bin/activate
    python3 Predictors/AgeIPO.py

Inputs:
    - SignalMasterTable.parquet: Monthly master table with permno, time_avail_m
    - IPODates.parquet: IPO dates with columns [permno, IPOdate, FoundingYear]

Outputs:
    - AgeIPO.csv: CSV file with columns [permno, yyyymm, AgeIPO]
    - AgeIPO = year - FoundingYear, only for recent IPO firms (3-36 months post-IPO)
    - Requires at least 100 IPO firms per month
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
    AgeIPO
    IPO and Age predictor for recent IPO firms
    """
    
    print("Starting AgeIPO.py...")
    
    # DATA LOAD
    print("Loading SignalMasterTable data...")
    
    # Load SignalMasterTable - equivalent to Stata: use permno time_avail_m using "$pathDataIntermediate/SignalMasterTable", clear
    signal_master_path = Path("../pyData/Intermediate/SignalMasterTable.parquet")
    if not signal_master_path.exists():
        raise FileNotFoundError(f"Required input file not found: {signal_master_path}")
    
    df = pd.read_parquet(signal_master_path)
    
    # Keep only the columns we need
    required_cols = ['permno', 'time_avail_m']
    missing_cols = [col for col in required_cols if col not in df.columns]
    if missing_cols:
        raise ValueError(f"Missing required columns in SignalMasterTable: {missing_cols}")
    
    df = df[required_cols].copy()
    
    print(f"Loaded SignalMasterTable: {df.shape[0]} rows, {df.shape[1]} columns")
    
    # merge m:1 permno using "$pathDataIntermediate/IPODates", keep(master match) nogenerate
    print("Merging with IPODates...")
    
    ipo_dates_path = Path("../pyData/Intermediate/IPODates.parquet")
    if not ipo_dates_path.exists():
        raise FileNotFoundError(f"Required input file not found: {ipo_dates_path}")
    
    ipo_dates = pd.read_parquet(ipo_dates_path)
    required_ipo_cols = ['permno', 'IPOdate', 'FoundingYear']
    missing_ipo_cols = [col for col in required_ipo_cols if col not in ipo_dates.columns]
    if missing_ipo_cols:
        raise ValueError(f"Missing required columns in IPODates: {missing_ipo_cols}")
    
    ipo_dates = ipo_dates[required_ipo_cols].copy()
    
    # Merge (equivalent to keep(master match) - left join)
    df = pd.merge(df, ipo_dates, on='permno', how='left')
    
    print(f"After merging with IPODates: {df.shape[0]} rows")
    
    # SIGNAL CONSTRUCTION
    
    # gen tempipo = (time_avail_m - IPOdate <= 36) & (time_avail_m - IPOdate >= 3)
    # replace tempipo = . if IPOdate == .
    print("Calculating recent IPO filter...")
    
    # Calculate months since IPO
    months_since_ipo = (df['time_avail_m'] - df['IPOdate']).dt.days / 30.44  # Convert to months
    
    # Recent IPO filter: 3-36 months post-IPO
    df['tempipo'] = (months_since_ipo <= 36) & (months_since_ipo >= 3)
    df.loc[df['IPOdate'].isna(), 'tempipo'] = np.nan
    
    # gen AgeIPO = year(dofm(time_avail_m)) - FoundingYear
    print("Calculating AgeIPO...")
    df['AgeIPO'] = df['time_avail_m'].dt.year - df['FoundingYear']
    
    # replace AgeIPO = . if tempipo == 0 // only sort recent IPO firms
    df.loc[df['tempipo'] == 0, 'AgeIPO'] = np.nan
    df.loc[df['tempipo'].isna(), 'AgeIPO'] = np.nan
    
    # egen tempTotal = total(tempipo), by(time_avail_m)  // Number of IPO = 1 firms per month
    # replace AgeIPO = . if tempTotal < 20*5
    print("Applying minimum IPO firms per month filter...")
    
    # Count IPO firms per month (tempipo == 1)
    df['tempTotal'] = df.groupby('time_avail_m')['tempipo'].transform('sum')
    
    # Require at least 100 IPO firms per month (20*5)
    df.loc[df['tempTotal'] < 100, 'AgeIPO'] = np.nan
    
    # Clean up temporary columns
    df = df.drop(columns=['tempipo', 'tempTotal', 'IPOdate', 'FoundingYear'])
    
    print(f"Calculated AgeIPO for {df['AgeIPO'].notna().sum()} observations")
    
    # SAVE
    # do "$pathCode/savepredictor" AgeIPO
    save_predictor(df, 'AgeIPO')
    
    print("AgeIPO.py completed successfully")


if __name__ == "__main__":
    main()