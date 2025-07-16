# ABOUTME: CBOperProf predictor - calculates cash-based operating profitability
# ABOUTME: Run: python3 pyCode/Predictors/CBOperProf.py

"""
CBOperProf Predictor

Cash-based Operating Profitability calculation with working capital adjustments.

Inputs:
- SignalMasterTable.parquet (permno, gvkey, time_avail_m, exchcd, sicCRSP, shrcd, mve_c)
- m_aCompustat.parquet (permno, time_avail_m, revt, cogs, xsga, xrd, rect, invt, xpp, drc, drlt, ap, xacc, at, ceq)

Outputs:
- CBOperProf.csv (permno, yyyymm, CBOperProf)

This predictor calculates cash-based operating profitability by adjusting operating income
for changes in working capital components over 12 months, then scaling by total assets.
"""

import pandas as pd
import numpy as np
import sys
import os

# Add utils directory to path for imports
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'utils'))
from savepredictor import save_predictor

def main():
    print("Starting CBOperProf predictor...")
    
    # DATA LOAD
    print("Loading SignalMasterTable...")
    signal_master = pd.read_parquet('../pyData/Intermediate/SignalMasterTable.parquet', 
                                   columns=['permno', 'gvkey', 'time_avail_m', 'exchcd', 
                                           'sicCRSP', 'shrcd', 'mve_c'])
    
    print(f"Loaded SignalMasterTable: {len(signal_master):,} observations")
    
    print("Loading m_aCompustat...")
    compustat_df = pd.read_parquet('../pyData/Intermediate/m_aCompustat.parquet', 
                                 columns=['permno', 'time_avail_m', 'revt', 'cogs', 'xsga', 
                                         'xrd', 'rect', 'invt', 'xpp', 'drc', 'drlt', 
                                         'ap', 'xacc', 'at', 'ceq'])
    
    print(f"Loaded m_aCompustat: {len(compustat_df):,} observations")
    
    # Merge SignalMasterTable with m_aCompustat
    print("Merging SignalMasterTable with m_aCompustat...")
    df = pd.merge(signal_master, compustat_df, on=['permno', 'time_avail_m'], how='left')
    
    print(f"After merge: {len(df):,} observations")
    
    # SIGNAL CONSTRUCTION
    print("Constructing CBOperProf signal...")
    
    # Replace missing values with 0 for the specified variables
    # (equivalent to foreach v of varlist revt cogs xsga xrd rect invt xpp drc drlt ap xacc { replace `v' = 0 if mi(`v') })
    zero_fill_vars = ['revt', 'cogs', 'xsga', 'xrd', 'rect', 'invt', 'xpp', 'drc', 'drlt', 'ap', 'xacc']
    for var in zero_fill_vars:
        df[var] = df[var].fillna(0)
    
    # Sort by permno and time_avail_m for lag calculations
    df = df.sort_values(['permno', 'time_avail_m'])
    
    # Create 12-month lags for working capital components
    lag_vars = ['rect', 'invt', 'xpp', 'drc', 'drlt', 'ap', 'xacc']
    for var in lag_vars:
        df[f'l12_{var}'] = df.groupby('permno')[var].shift(12)
    
    # Calculate CBOperProf following the complex formula
    # CBOperProf = (revt - cogs - (xsga - xrd)) - 
    #              (rect - l12.rect) - (invt - l12.invt) - (xpp - l12.xpp) + 
    #              (drc + drlt - l12.drc - l12.drlt) + (ap - l12.ap) + (xacc - l12.xacc)
    
    df['CBOperProf'] = (
        (df['revt'] - df['cogs'] - (df['xsga'] - df['xrd'])) -
        (df['rect'] - df['l12_rect']) - (df['invt'] - df['l12_invt']) - (df['xpp'] - df['l12_xpp']) +
        (df['drc'] + df['drlt'] - df['l12_drc'] - df['l12_drlt']) + 
        (df['ap'] - df['l12_ap']) + (df['xacc'] - df['l12_xacc'])
    )
    
    # Scale by total assets (equivalent to replace CBOperProf = CBOperProf/at)
    # Apply domain-aware missing value handling for division
    df['CBOperProf'] = np.where(
        df['at'] == 0,
        np.nan,  # Division by zero = missing
        np.where(
            df['CBOperProf'].isna() & df['at'].isna(),
            1.0,  # missing/missing = 1.0 (no change)
            df['CBOperProf'] / df['at']
        )
    )
    
    # Calculate BM for filtering (equivalent to gen BM = log(ceq/mve_c))
    df['BM'] = np.log(df['ceq'] / df['mve_c'])
    
    # Apply exclusion criteria
    # replace CBOperProf = . if shrcd > 11 | mi(mve_c) | mi(BM) | mi(at) | (sicCRSP >= 6000 & sicCRSP < 7000)
    exclusion_mask = (
        (df['shrcd'] > 11) |
        df['mve_c'].isna() |
        df['BM'].isna() |
        df['at'].isna() |
        ((df['sicCRSP'] >= 6000) & (df['sicCRSP'] < 7000))
    )
    
    df.loc[exclusion_mask, 'CBOperProf'] = np.nan
    
    print(f"Generated CBOperProf values for {df['CBOperProf'].notna().sum():,} observations")
    print(f"Excluded {exclusion_mask.sum():,} observations due to filtering criteria")
    
    # Clean up temporary columns
    lag_cols_to_drop = [f'l12_{var}' for var in lag_vars]
    df = df.drop(columns=lag_cols_to_drop + ['BM'])
    
    # SAVE
    print("Saving predictor...")
    save_predictor(df, 'CBOperProf')
    
    print("CBOperProf predictor completed successfully!")

if __name__ == "__main__":
    main()