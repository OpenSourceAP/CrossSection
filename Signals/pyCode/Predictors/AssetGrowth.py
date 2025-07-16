# ABOUTME: AssetGrowth.py - calculates AssetGrowth predictor using 12-month asset growth
# ABOUTME: Direct line-by-line translation from Stata Code/Predictors/AssetGrowth.do

"""
AssetGrowth.py

Usage:
    cd pyCode/
    source .venv/bin/activate
    python3 Predictors/AssetGrowth.py

Inputs:
    - m_aCompustat.parquet: Monthly Compustat data with columns [gvkey, permno, time_avail_m, at]

Outputs:
    - AssetGrowth.csv: CSV file with columns [permno, yyyymm, AssetGrowth]
    - AssetGrowth = (at - l12.at)/l12.at (12-month asset growth)
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
    AssetGrowth
    12-month asset growth
    """
    
    print("Starting AssetGrowth.py...")
    
    # DATA LOAD
    print("Loading m_aCompustat data...")
    
    # Load m_aCompustat - equivalent to Stata: use gvkey permno time_avail_m at using "$pathDataIntermediate/m_aCompustat", clear
    m_aCompustat_path = Path("../pyData/Intermediate/m_aCompustat.parquet")
    if not m_aCompustat_path.exists():
        raise FileNotFoundError(f"Required input file not found: {m_aCompustat_path}")
    
    df = pd.read_parquet(m_aCompustat_path)
    
    # Keep only the columns we need
    required_cols = ['gvkey', 'permno', 'time_avail_m', 'at']
    missing_cols = [col for col in required_cols if col not in df.columns]
    if missing_cols:
        raise ValueError(f"Missing required columns in m_aCompustat: {missing_cols}")
    
    df = df[required_cols].copy()
    
    print(f"Loaded m_aCompustat: {df.shape[0]} rows, {df.shape[1]} columns")
    
    # SIGNAL CONSTRUCTION
    
    # xtset permno time_avail_m
    print("Setting up panel data (sorting by permno, time_avail_m)...")
    df = df.sort_values(['permno', 'time_avail_m'])
    
    # gen AssetGrowth = (at - l12.at)/l12.at 
    print("Calculating 12-month lag and AssetGrowth...")
    
    # Create 12-month lag using simple shift (Method 1 from StataDocs)
    df['l12_at'] = df.groupby('permno')['at'].shift(12)
    
    # Calculate AssetGrowth with domain-aware missing value handling
    # Following missing/missing = 1.0 pattern from Journal/2025-07-16_missing_missing_equals_one_pattern.md
    df['AssetGrowth'] = np.where(
        df['l12_at'] == 0,
        np.nan,  # Division by zero = missing
        np.where(
            df['at'].isna() & df['l12_at'].isna(),
            1.0,  # missing/missing = 1.0 (no change)
            (df['at'] - df['l12_at']) / df['l12_at']
        )
    )
    
    print(f"Calculated AssetGrowth for {df['AssetGrowth'].notna().sum()} observations")
    
    # SAVE
    # do "$pathCode/savepredictor" AssetGrowth
    save_predictor(df, 'AssetGrowth')
    
    print("AssetGrowth.py completed successfully")


if __name__ == "__main__":
    main()