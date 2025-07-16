# ABOUTME: Beta.py - calculates CAPM Beta using 60-month rolling regression
# ABOUTME: Direct line-by-line translation from Stata Code/Predictors/Beta.do

"""
Beta.py

Usage:
    cd pyCode/
    source .venv/bin/activate
    python3 Predictors/Beta.py

Inputs:
    - monthlyCRSP.parquet: Monthly CRSP data with permno, time_avail_m, ret
    - monthlyFF.parquet: Monthly Fama-French data with time_avail_m, rf
    - monthlyMarket.parquet: Monthly market data with time_avail_m, ewretd
    - SignalMasterTable.parquet: Monthly master table with permno, time_avail_m

Outputs:
    - Beta.csv: CSV file with columns [permno, yyyymm, Beta]
    - Beta = CAMP beta from 60-month rolling regression (minimum 20 observations)
    - Uses asreg equivalent: retrf = alpha + beta * ewmktrf + epsilon
"""

import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
from pathlib import Path
import sys
import os

# Add utils directory to path for imports
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'utils'))
from savepredictor import save_predictor


def rolling_capm_beta(df, window=60, min_periods=20):
    """
    Calculate rolling CAPM beta using 60-month rolling regression
    Replicates Stata asreg retrf ewmktrf, window(time_temp 60) min(20) by(permno)
    """
    def process_group(group):
        # Sort by time_avail_m within group (equivalent to bys permno (time_avail_m))
        group = group.sort_values('time_avail_m')
        
        # Initialize beta column
        group['_b_ewmktrf'] = np.nan
        
        # Apply rolling regression manually
        for i in range(len(group)):
            if i < window - 1:
                continue
                
            # Extract window data
            start_idx = max(0, i - window + 1)
            end_idx = i + 1
            window_data = group.iloc[start_idx:end_idx]
            
            # Check minimum observations
            if len(window_data) < min_periods:
                continue
                
            # Get clean data
            y = window_data['retrf'].dropna()
            x = window_data['ewmktrf'].dropna()
            
            # Find common observations (align data)
            common_idx = y.index.intersection(x.index)
            if len(common_idx) < min_periods:
                continue
                
            y_clean = y.loc[common_idx].values
            x_clean = x.loc[common_idx].values.reshape(-1, 1)
            
            # Fit regression: retrf = alpha + beta * ewmktrf + epsilon
            try:
                reg = LinearRegression()
                reg.fit(x_clean, y_clean)
                
                # Store beta coefficient
                group.iloc[i, group.columns.get_loc('_b_ewmktrf')] = reg.coef_[0]
                
            except:
                continue
        
        return group
    
    # Process each permno group (equivalent to by(permno))
    result = df.groupby('permno').apply(process_group).reset_index(drop=True)
    
    return result


def main():
    """
    Beta
    CAPM Beta using 60-month rolling regression
    """
    
    print("Starting Beta.py...")
    
    # DATA LOAD
    print("Loading monthly CRSP data...")
    
    # Load monthlyCRSP data - equivalent to Stata: use permno time_avail_m ret using "$pathDataIntermediate/monthlyCRSP", clear
    monthly_crsp_path = Path("../pyData/Intermediate/monthlyCRSP.parquet")
    if not monthly_crsp_path.exists():
        raise FileNotFoundError(f"Required input file not found: {monthly_crsp_path}")
    
    df = pd.read_parquet(monthly_crsp_path)
    
    # Keep only required columns
    required_cols = ['permno', 'time_avail_m', 'ret']
    missing_cols = [col for col in required_cols if col not in df.columns]
    if missing_cols:
        raise ValueError(f"Missing required columns in monthlyCRSP: {missing_cols}")
    
    df = df[required_cols].copy()
    
    print(f"Loaded monthlyCRSP: {df.shape[0]} rows, {df.shape[1]} columns")
    
    # merge m:1 time_avail_m using "$pathDataIntermediate/monthlyFF", nogenerate keep(match) keepusing(rf)
    print("Merging with monthly Fama-French data...")
    
    monthly_ff_path = Path("../pyData/Intermediate/monthlyFF.parquet")
    if not monthly_ff_path.exists():
        raise FileNotFoundError(f"Required input file not found: {monthly_ff_path}")
    
    monthly_ff = pd.read_parquet(monthly_ff_path)
    
    # Keep only required columns
    ff_cols = ['time_avail_m', 'rf']
    missing_ff_cols = [col for col in ff_cols if col not in monthly_ff.columns]
    if missing_ff_cols:
        raise ValueError(f"Missing required columns in monthlyFF: {missing_ff_cols}")
    
    monthly_ff = monthly_ff[ff_cols].copy()
    
    # Merge (equivalent to keep(match) - inner join)
    df = pd.merge(df, monthly_ff, on='time_avail_m', how='inner')
    
    print(f"After merging FF data: {df.shape[0]} rows")
    
    # merge m:1 time_avail_m using "$pathDataIntermediate/monthlyMarket", nogenerate keep(match) keepusing(ewretd)
    print("Merging with monthly market data...")
    
    monthly_market_path = Path("../pyData/Intermediate/monthlyMarket.parquet")
    if not monthly_market_path.exists():
        raise FileNotFoundError(f"Required input file not found: {monthly_market_path}")
    
    monthly_market = pd.read_parquet(monthly_market_path)
    
    # Keep only required columns
    market_cols = ['time_avail_m', 'ewretd']
    missing_market_cols = [col for col in market_cols if col not in monthly_market.columns]
    if missing_market_cols:
        raise ValueError(f"Missing required columns in monthlyMarket: {missing_market_cols}")
    
    monthly_market = monthly_market[market_cols].copy()
    
    # Merge (equivalent to keep(match) - inner join)
    df = pd.merge(df, monthly_market, on='time_avail_m', how='inner')
    
    print(f"After merging market data: {df.shape[0]} rows")
    
    # SIGNAL CONSTRUCTION
    print("Computing excess returns...")
    
    # gen retrf = ret - rf
    df['retrf'] = df['ret'] - df['rf']
    
    # gen ewmktrf = ewretd - rf
    df['ewmktrf'] = df['ewretd'] - df['rf']
    
    # Calculate rolling CAMP beta
    print("Calculating rolling CAPM beta (60-month window, min 20 observations)...")
    
    # Equivalent to:
    # bys permno (time_avail_m): gen time_temp = _n
    # xtset permno time_temp
    # asreg retrf ewmktrf, window(time_temp 60) min(20) by(permno)
    df = rolling_capm_beta(df, window=60, min_periods=20)
    
    # rename _b_ewmktrf Beta
    df['Beta'] = df['_b_ewmktrf']
    
    # Drop missing beta values
    df = df.dropna(subset=['Beta'])
    
    print(f"Final Beta calculations: {df.shape[0]} observations")
    
    # Load SignalMasterTable to get proper index structure
    print("Loading SignalMasterTable for proper index...")
    
    signal_master_path = Path("../pyData/Intermediate/SignalMasterTable.parquet")
    if not signal_master_path.exists():
        raise FileNotFoundError(f"Required input file not found: {signal_master_path}")
    
    signal_master = pd.read_parquet(signal_master_path)
    
    # Keep only required columns
    master_cols = ['permno', 'time_avail_m']
    missing_master_cols = [col for col in master_cols if col not in signal_master.columns]
    if missing_master_cols:
        raise ValueError(f"Missing required columns in SignalMasterTable: {missing_master_cols}")
    
    signal_master = signal_master[master_cols].copy()
    
    # Merge with SignalMasterTable to get proper index structure
    df = pd.merge(signal_master, df[['permno', 'time_avail_m', 'Beta']], 
                  on=['permno', 'time_avail_m'], how='left')
    
    print(f"After merging with SignalMasterTable: {df.shape[0]} rows")
    
    # SAVE
    # do "$pathCode/savepredictor" Beta
    save_predictor(df, 'Beta')
    
    print("Beta.py completed successfully")


if __name__ == "__main__":
    main()