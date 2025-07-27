# ABOUTME: Debug the size categorization logic in CitationsRD
# ABOUTME: Run from pyCode/ directory: python3 ClaudeDebug/citationsrd_size_debug.py

import pandas as pd
import numpy as np

def debug_size_categorization():
    """Debug why permno 14755 gets sizecat=2 instead of sizecat=1"""
    
    print("=== Debugging Size Categorization for June 2017 ===")
    
    # Load data up to size categorization step
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
    
    # Focus on June 2017 before size categorization
    june_2017 = df[df['time_avail_m'] == '2017-06-01'].copy()
    print(f"June 2017 data before size categorization: {len(june_2017)}")
    
    # Check NYSE stocks
    nyse_stocks = june_2017[june_2017['exchcd'] == 1]
    print(f"NYSE stocks in June 2017: {len(nyse_stocks)}")
    
    if len(nyse_stocks) > 0:
        nyse_median = nyse_stocks['mve_c'].median()
        print(f"NYSE median market cap: {nyse_median}")
        
        # Check permno 14755
        permno_14755 = june_2017[june_2017['permno'] == 14755]
        if len(permno_14755) > 0:
            mve_14755 = permno_14755['mve_c'].iloc[0]
            exchcd_14755 = permno_14755['exchcd'].iloc[0]
            
            print(f"\nPermno 14755:")
            print(f"  Market cap: {mve_14755}")
            print(f"  Exchange code: {exchcd_14755}")
            print(f"  NYSE median: {nyse_median}")
            print(f"  mve_c <= median? {mve_14755 <= nyse_median}")
            
            if mve_14755 <= nyse_median:
                expected_sizecat = 1
            else:
                expected_sizecat = 2
            
            print(f"  Expected sizecat: {expected_sizecat}")
            
            if expected_sizecat == 2:
                print("  *** ISSUE: Permno 14755 is classified as large stock (sizecat=2) ***")
                print("  *** But Stata expects it to be small stock (sizecat=1) ***")
                
                # Check if the Stata logic is different
                print("\n=== Stata Logic Analysis ===")
                print("Stata code: bys time_avail_m: astile sizecat = mve_c, qc(exchcd == 1) nq(2)")
                print("This means: within each time period, create size quintiles based on mve_c")
                print("but only NYSE stocks (exchcd==1) determine the breakpoints")
                
                # Maybe there's a difference in the data or the median calculation
                print(f"\nNYSE market cap statistics:")
                print(f"  Count: {len(nyse_stocks)}")
                print(f"  Min: {nyse_stocks['mve_c'].min()}")
                print(f"  25th percentile: {nyse_stocks['mve_c'].quantile(0.25)}")
                print(f"  Median (50th): {nyse_stocks['mve_c'].median()}")
                print(f"  75th percentile: {nyse_stocks['mve_c'].quantile(0.75)}")
                print(f"  Max: {nyse_stocks['mve_c'].max()}")
                
                # Check if permno 14755 is close to the median
                diff_from_median = mve_14755 - nyse_median
                print(f"\nPermno 14755 market cap difference from median: {diff_from_median}")
                
                if abs(diff_from_median) < 100:  # Within $100M
                    print("*** POSSIBLE ISSUE: Very close to median - rounding/precision difference? ***")

def check_stata_astile_logic():
    """Check if there's a difference between astile and simple median split"""
    
    print("\n=== Checking astile vs simple median logic ===")
    
    # Stata's astile with nq(2) creates 2 quantiles
    # qc(exchcd == 1) means use exchcd==1 stocks to determine breakpoints
    # This should be equivalent to median split based on NYSE stocks
    
    # But maybe there's a subtle difference in how ties are handled
    print("Stata astile logic:")
    print("- astile creates quantiles with approximately equal numbers of observations")
    print("- nq(2) creates 2 groups (below/above median)")
    print("- qc(exchcd == 1) uses only NYSE stocks to determine breakpoints")
    print("")
    print("Python logic:")
    print("- Calculate median of NYSE stocks")
    print("- Assign sizecat=1 if mve_c <= median, sizecat=2 if mve_c > median")
    print("")
    print("Potential differences:")
    print("1. Tie handling (what happens when mve_c exactly equals median)")
    print("2. Missing value handling")
    print("3. Floating point precision")

if __name__ == "__main__":
    debug_size_categorization()
    check_stata_astile_logic()