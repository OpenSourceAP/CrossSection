# ABOUTME: ChTax predictor - calculates change in taxes
# ABOUTME: Run: python3 pyCode/Predictors/ChTax.py

"""
ChTax Predictor

Change in taxes calculation: (txtq - l12.txtq)/l12.at

Inputs:
- m_aCompustat.parquet (permno, gvkey, time_avail_m, at)
- m_QCompustat.parquet (gvkey, time_avail_m, txtq)

Outputs:
- ChTax.csv (permno, yyyymm, ChTax)

This predictor calculates the change in quarterly taxes scaled by lagged assets.
"""

import pandas as pd
import numpy as np
import sys
import os

# Add utils directory to path for imports
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'utils'))
from savepredictor import save_predictor

def main():
    print("Starting ChTax predictor...")
    
    # DATA LOAD
    print("Loading m_aCompustat data...")
    compustat_df = pd.read_parquet('../pyData/Intermediate/m_aCompustat.parquet', 
                                 columns=['permno', 'gvkey', 'time_avail_m', 'at'])
    
    print(f"Loaded {len(compustat_df):,} Compustat observations")
    
    print("Loading m_QCompustat data...")
    qcompustat_df = pd.read_parquet('../pyData/Intermediate/m_QCompustat.parquet', 
                                   columns=['gvkey', 'time_avail_m', 'txtq'])
    
    print(f"Loaded {len(qcompustat_df):,} quarterly Compustat observations")
    
    # Merge data (equivalent to merge 1:1 gvkey time_avail_m using m_QCompustat, keepusing(txtq) nogenerate keep(match))
    print("Merging Compustat and quarterly data...")
    df = pd.merge(compustat_df, qcompustat_df, on=['gvkey', 'time_avail_m'], how='inner')
    
    print(f"After merge: {len(df):,} observations")
    
    # SIGNAL CONSTRUCTION
    print("Constructing ChTax signal...")
    
    # Sort by gvkey and time_avail_m (equivalent to xtset gvkey time_avail_m)
    df = df.sort_values(['gvkey', 'time_avail_m'])
    
    # Create 12-month lags
    df['l12_txtq'] = df.groupby('gvkey')['txtq'].shift(12)
    df['l12_at'] = df.groupby('gvkey')['at'].shift(12)
    
    # Calculate change in taxes
    df['tax_change'] = df['txtq'] - df['l12_txtq']
    
    # Calculate ChTax = (txtq - l12.txtq)/l12.at with domain-aware missing handling
    df['ChTax'] = np.where(
        df['l12_at'] == 0,
        np.nan,  # Division by zero = missing
        np.where(
            df['tax_change'].isna() & df['l12_at'].isna(),
            1.0,  # missing/missing = 1.0 (no change)
            df['tax_change'] / df['l12_at']
        )
    )
    
    print(f"Generated ChTax values for {df['ChTax'].notna().sum():,} observations")
    
    # Clean up temporary columns
    df = df.drop(columns=['l12_txtq', 'l12_at', 'tax_change'])
    
    # SAVE
    print("Saving predictor...")
    save_predictor(df, 'ChTax')
    
    print("ChTax predictor completed successfully!")

if __name__ == "__main__":
    main()