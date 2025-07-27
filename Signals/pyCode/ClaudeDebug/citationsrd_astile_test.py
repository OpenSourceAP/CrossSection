# ABOUTME: Test the astile logic fix for CitationsRD
# ABOUTME: Run from pyCode/ directory: python3 ClaudeDebug/citationsrd_astile_test.py

import pandas as pd
import numpy as np

def test_astile_logic():
    """Test if the astile logic fixed the permno 14755 issue"""
    
    print("=== Testing Astile Logic Fix ===")
    
    # Load the new Python output
    python_output = pd.read_csv('../pyData/Predictors/CitationsRD.csv')
    python_output = python_output.set_index(['permno', 'yyyymm'])
    
    # Check permno 14755
    permno_14755_output = python_output[python_output.index.get_level_values('permno') == 14755]
    print(f"Permno 14755 in new output: {len(permno_14755_output)} rows")
    
    if len(permno_14755_output) > 0:
        output_yyyymm = permno_14755_output.index.get_level_values('yyyymm').tolist()
        print("Available yyyymm values:")
        print(sorted(output_yyyymm)[:20])  # First 20
        
        # Check the missing dates
        missing_yyyymm = [201706, 201707, 201708, 201709, 201710, 201711, 201712, 201801, 201802, 201803]
        print("\nChecking originally missing dates:")
        for yyyymm in missing_yyyymm:
            exists = yyyymm in output_yyyymm
            print(f"  {yyyymm}: {'EXISTS' if exists else 'MISSING'}")
    else:
        print("*** Permno 14755 still completely missing! ***")
    
    # Compare with Stata
    stata_output = pd.read_csv('../Data/Predictors/CitationsRD.csv')
    print(f"\nStata output: {len(stata_output)} rows")
    print(f"Python output: {len(python_output)} rows")
    print(f"Difference: {len(stata_output) - len(python_output)} (Python missing)")

def debug_astile_breakpoint():
    """Debug the astile breakpoint calculation"""
    
    print("\n=== Debugging Astile Breakpoint ===")
    
    # Test the astile logic on June 2017 data
    # Load data up to size categorization
    df = pd.read_parquet('../pyData/Intermediate/SignalMasterTable.parquet')
    df = df[['permno', 'gvkey', 'time_avail_m', 'mve_c', 'sicCRSP', 'exchcd']].copy()
    df = df[df['time_avail_m'] >= '1970-01']
    df['year'] = df['time_avail_m'].dt.year
    
    compustat = pd.read_parquet('../pyData/Intermediate/m_aCompustat.parquet')
    compustat = compustat[['permno', 'time_avail_m', 'xrd', 'sich', 'datadate', 'ceq']].copy()
    compustat = compustat[compustat['time_avail_m'] >= '1970-01']
    df = df.merge(compustat, on=['permno', 'time_avail_m'], how='left')
    df = df.dropna(subset=['gvkey'])
    
    patent = pd.read_parquet('../pyData/Intermediate/PatentDataProcessed.parquet')
    patent = patent[['gvkey', 'year', 'ncitscale']].copy()
    df = df.merge(patent, on=['gvkey', 'year'], how='left')
    
    df = df.sort_values(['permno', 'time_avail_m'])
    df['temp'] = df.groupby('permno')['ncitscale'].shift(6)
    df['temp'] = df['temp'].fillna(0)
    df['ncitscale'] = df['temp']
    df = df.drop(columns=['temp'])
    
    df['xrd_lag'] = df.groupby('permno')['xrd'].shift(24)
    df['xrd_lag'] = df['xrd_lag'].fillna(0)
    
    df = df[df['time_avail_m'] >= '1975-01']
    df = df[df['time_avail_m'].dt.month == 6]
    
    df = df.sort_values(['permno', 'time_avail_m'])
    df['sum_xrd'] = df.groupby('permno')['xrd_lag'].transform(
        lambda x: x.rolling(window=4, min_periods=1).sum()
    )
    df['sum_ncit'] = df.groupby('permno')['ncitscale'].transform(
        lambda x: x.rolling(window=4, min_periods=1).sum()
    )
    
    df['tempCitationsRD'] = np.where(df['sum_xrd'] > 0, df['sum_ncit'] / df['sum_xrd'], np.nan)
    
    # Apply filters
    df = df.sort_values(['gvkey', 'time_avail_m'])
    df = df.groupby('gvkey').apply(lambda x: x.iloc[2:]).reset_index(drop=True)
    df = df[~((df['sicCRSP'] >= 6000) & (df['sicCRSP'] <= 6999))]
    df = df[df['ceq'] >= 0]
    
    # Focus on June 2017
    june_2017 = df[df['time_avail_m'] == '2017-06-01'].copy()
    
    # Test both methods
    nyse_stocks = june_2017[june_2017['exchcd'] == 1]
    
    # Method 1: Simple median
    median_mve = nyse_stocks['mve_c'].median()
    
    # Method 2: Astile (qcut)
    nyse_quantiles = pd.qcut(nyse_stocks['mve_c'], q=2, labels=False, duplicates='drop')
    lower_quantile_max = nyse_stocks[nyse_quantiles == 0]['mve_c'].max()
    
    print(f"NYSE stocks in June 2017: {len(nyse_stocks)}")
    print(f"Method 1 (median): {median_mve}")
    print(f"Method 2 (astile breakpoint): {lower_quantile_max}")
    print(f"Difference: {lower_quantile_max - median_mve}")
    
    # Check permno 14755
    permno_14755 = june_2017[june_2017['permno'] == 14755]
    if len(permno_14755) > 0:
        mve_14755 = permno_14755['mve_c'].iloc[0]
        
        print(f"\nPermno 14755 market cap: {mve_14755}")
        print(f"Method 1: mve <= median? {mve_14755 <= median_mve} -> sizecat = {1 if mve_14755 <= median_mve else 2}")
        print(f"Method 2: mve <= astile? {mve_14755 <= lower_quantile_max} -> sizecat = {1 if mve_14755 <= lower_quantile_max else 2}")
        
        # The new method should give sizecat=1 if it fixes the issue

if __name__ == "__main__":
    test_astile_logic()
    debug_astile_breakpoint()