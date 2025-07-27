# ABOUTME: Debug exactly what happens to June 2017 observation for permno 14755
# ABOUTME: Run from pyCode/ directory: python3 ClaudeDebug/citationsrd_june2017_debug.py

import pandas as pd
import numpy as np

def debug_june_2017_signal_assignment():
    """Debug the signal assignment for June 2017 specifically"""
    
    print("=== Debugging June 2017 Signal Assignment ===")
    
    # Create test data that mimics the June 2017 situation
    # From my debugging: June 2017 has tempCitationsRD = 0.0
    test_data = pd.DataFrame({
        'permno': [14755],
        'time_avail_m': [pd.to_datetime('2017-06-01')],
        'tempCitationsRD': [0.0],
        'sizecat': [1],  # Small stock
        'gvkey': [187551.0]
    })
    
    print("Test data (June 2017 for permno 14755):")
    print(test_data)
    
    # Apply the fastxtile logic (but this needs realistic data)
    # The issue might be that June 2017 has unusual tercile behavior
    
    # Let me load actual June 2017 data to see the distribution
    print("\n=== Loading Actual June 2017 Data ===")
    
    # Load and process real data up to June 2017 stage
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
    
    # Size categories
    def calculate_size_breakpoints(group):
        nyse_stocks = group[group['exchcd'] == 1]
        if len(nyse_stocks) == 0:
            return group
        
        median_mve = nyse_stocks['mve_c'].median()
        group['sizecat'] = np.where(group['mve_c'] <= median_mve, 1, 2)
        return group
    
    df = df.groupby('time_avail_m').apply(calculate_size_breakpoints).reset_index(drop=True)
    
    # Focus on June 2017
    june_2017 = df[df['time_avail_m'] == '2017-06-01'].copy()
    print(f"June 2017 data: {len(june_2017)} observations")
    
    if len(june_2017) > 0:
        # Check permno 14755
        permno_14755_june2017 = june_2017[june_2017['permno'] == 14755]
        print(f"Permno 14755 in June 2017: {len(permno_14755_june2017)}")
        
        if len(permno_14755_june2017) > 0:
            print("Permno 14755 June 2017 data:")
            print(permno_14755_june2017[['permno', 'tempCitationsRD', 'sizecat', 'mve_c']])
        
        # Check distribution of tempCitationsRD
        citations = june_2017['tempCitationsRD'].dropna()
        print(f"\nJune 2017 tempCitationsRD distribution:")
        print(f"Total non-null: {len(citations)}")
        print(f"Min: {citations.min()}, Max: {citations.max()}")
        print(f"Quantiles: 0.333={citations.quantile(0.333)}, 0.667={citations.quantile(0.667)}")
        
        # Apply tercile logic
        def create_fastxtile_terciles(group):
            try:
                group['maincat'] = pd.qcut(group['tempCitationsRD'], q=3, labels=False, duplicates='drop') + 1
                return group
            except Exception as e:
                print(f"QCut failed: {e}")
                if group['tempCitationsRD'].notna().sum() > 0:
                    group['maincat'] = 1.0
                else:
                    group['maincat'] = np.nan
                return group
        
        june_2017 = create_fastxtile_terciles(june_2017)
        
        # Check what maincat permno 14755 gets
        permno_14755_with_maincat = june_2017[june_2017['permno'] == 14755]
        if len(permno_14755_with_maincat) > 0:
            maincat = permno_14755_with_maincat['maincat'].iloc[0]
            sizecat = permno_14755_with_maincat['sizecat'].iloc[0]
            tempCitationsRD = permno_14755_with_maincat['tempCitationsRD'].iloc[0]
            
            print(f"\nPermno 14755 June 2017 results:")
            print(f"  tempCitationsRD: {tempCitationsRD}")
            print(f"  sizecat: {sizecat}")
            print(f"  maincat: {maincat}")
            
            # Determine signal
            if sizecat == 1 and maincat == 3:
                signal = 1
            elif sizecat == 1 and maincat == 1:
                signal = 0
            else:
                signal = np.nan
            
            print(f"  CitationsRD signal: {signal}")
            
            if pd.isna(signal):
                print("  *** PROBLEM: No signal assigned! ***")
                print(f"  Condition 1 (sizecat==1 & maincat==3): {sizecat==1 and maincat==3}")
                print(f"  Condition 2 (sizecat==1 & maincat==1): {sizecat==1 and maincat==1}")
            else:
                print(f"  Signal assigned correctly: {signal}")
                print(f"  This should expand to 201706-201805")

if __name__ == "__main__":
    debug_june_2017_signal_assignment()