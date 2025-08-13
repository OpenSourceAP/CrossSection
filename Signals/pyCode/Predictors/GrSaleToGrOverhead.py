# ABOUTME: GrSaleToGrOverhead.py - calculates GrSaleToGrOverhead predictor using sales and overhead growth
# ABOUTME: Direct line-by-line translation from Stata Code/Predictors/GrSaleToGrOverhead.do

"""
GrSaleToGrOverhead.py

Usage:
    cd pyCode/
    source .venv/bin/activate
    python3 Predictors/GrSaleToGrOverhead.py

Inputs:
    - m_aCompustat.parquet: Monthly Compustat data with columns [gvkey, permno, time_avail_m, sale, xsga]

Outputs:
    - GrSaleToGrOverhead.csv: CSV file with columns [permno, yyyymm, GrSaleToGrOverhead]
    - GrSaleToGrOverhead = Sales growth minus overhead growth (using 12 and 24-month lags)
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
    GrSaleToGrOverhead
    Sales growth over overhead growth
    """
    
    print("Starting GrSaleToGrOverhead.py...")
    
    # DATA LOAD
    print("Loading m_aCompustat data...")
    
    # Load m_aCompustat - equivalent to Stata: use gvkey permno time_avail_m sale xsga using "$pathDataIntermediate/m_aCompustat", clear
    m_aCompustat_path = Path("../pyData/Intermediate/m_aCompustat.parquet")
    if not m_aCompustat_path.exists():
        raise FileNotFoundError(f"Required input file not found: {m_aCompustat_path}")
    
    df = pd.read_parquet(m_aCompustat_path)
    
    # Keep only the columns we need
    required_cols = ['gvkey', 'permno', 'time_avail_m', 'sale', 'xsga']
    missing_cols = [col for col in required_cols if col not in df.columns]
    if missing_cols:
        raise ValueError(f"Missing required columns in m_aCompustat: {missing_cols}")
    
    df = df[required_cols].copy()
    
    print(f"Loaded m_aCompustat: {df.shape[0]} rows, {df.shape[1]} columns")
    
    # SIGNAL CONSTRUCTION
    
    # bysort permno time_avail_m: keep if _n == 1  // deletes a few observations
    print("Removing duplicate observations (bysort permno time_avail_m: keep if _n == 1)...")
    df = df.drop_duplicates(subset=['permno', 'time_avail_m'], keep='first')
    
    # xtset permno time_avail_m
    print("Setting up panel data (sorting by permno, time_avail_m)...")
    df = df.sort_values(['permno', 'time_avail_m'])
    
    # Create 12-month and 24-month lags
    print("Calculating 12-month and 24-month lags...")
    df['l12_sale'] = df.groupby('permno')['sale'].shift(12)
    df['l24_sale'] = df.groupby('permno')['sale'].shift(24)
    df['l12_xsga'] = df.groupby('permno')['xsga'].shift(12)
    df['l24_xsga'] = df.groupby('permno')['xsga'].shift(24)
    
    # Primary formula: GrSaleToGrOverhead = 
    # ( (sale- (.5*(l12.sale + l24.sale)))/(.5*(l12.sale + l24.sale)) ) 
    # -( (xsga- (.5*(l12.xsga+l24.xsga))) /(.5*(l12.xsga+l24.xsga)) )
    print("Calculating GrSaleToGrOverhead using primary formula...")
    
    # Calculate intermediate values
    df['avg_sale_lag'] = 0.5 * (df['l12_sale'] + df['l24_sale'])
    df['avg_xsga_lag'] = 0.5 * (df['l12_xsga'] + df['l24_xsga'])
    
    # Calculate sales growth component: (sale - avg_sale_lag) / avg_sale_lag
    df['sale_growth'] = np.where(
        df['avg_sale_lag'] == 0,
        np.nan,  # Division by zero = missing
        (df['sale'] - df['avg_sale_lag']) / df['avg_sale_lag']
    )
    
    # Calculate overhead growth component: (xsga - avg_xsga_lag) / avg_xsga_lag
    df['overhead_growth'] = np.where(
        df['avg_xsga_lag'] == 0,
        np.nan,  # Division by zero = missing
        (df['xsga'] - df['avg_xsga_lag']) / df['avg_xsga_lag']
    )
    
    # Primary formula: sales growth minus overhead growth
    df['GrSaleToGrOverhead'] = df['sale_growth'] - df['overhead_growth']
    
    # Fallback formula: replace GrSaleToGrOverhead = ((sale-l12.sale)/l12.sale)-((xsga-l12.xsga)/l12.xsga) if mi(GrSaleToGrOverhead)
    print("Applying fallback formula where primary formula is missing...")
    
    # Calculate fallback sales growth: (sale - l12.sale) / l12.sale
    df['fallback_sale_growth'] = np.where(
        df['l12_sale'] == 0,
        np.nan,  # Division by zero = missing
        (df['sale'] - df['l12_sale']) / df['l12_sale']
    )
    
    # Calculate fallback overhead growth: (xsga - l12.xsga) / l12.xsga
    df['fallback_overhead_growth'] = np.where(
        df['l12_xsga'] == 0,
        np.nan,  # Division by zero = missing
        (df['xsga'] - df['l12_xsga']) / df['l12_xsga']
    )
    
    # Fallback formula: sales growth minus overhead growth (12-month version)
    df['fallback_GrSaleToGrOverhead'] = df['fallback_sale_growth'] - df['fallback_overhead_growth']
    
    # Apply fallback where primary is missing
    df['GrSaleToGrOverhead'] = np.where(
        df['GrSaleToGrOverhead'].isna(),
        df['fallback_GrSaleToGrOverhead'],
        df['GrSaleToGrOverhead']
    )
    
    print(f"Calculated GrSaleToGrOverhead for {df['GrSaleToGrOverhead'].notna().sum()} observations")
    
    # SAVE
    # do "$pathCode/savepredictor" GrSaleToGrOverhead
    save_predictor(df, 'GrSaleToGrOverhead')
    
    print("GrSaleToGrOverhead.py completed successfully")


if __name__ == "__main__":
    main()