# ABOUTME: Debug CitationsRD missing observations and fastxtile logic issues
# ABOUTME: Run from pyCode/ directory: python3 ClaudeDebug/citationsrd_final_debug.py

import pandas as pd
import numpy as np

def debug_citationsrd_missing():
    """Debug specific missing observations in CitationsRD"""
    
    print("=== CitationsRD Debug: Missing Observations ===")
    
    # Load Stata data to see expected results
    stata_file = '../Data/Predictors/CitationsRD.csv'
    try:
        stata_df = pd.read_csv(stata_file)
        print(f"Stata data loaded: {stata_df.shape}")
        
        # Focus on the missing observation: permno 14755, 201706-201803
        missing_permno = 14755
        missing_dates = [201706, 201707, 201708, 201709, 201710, 201711, 201712, 201801, 201802, 201803]
        
        print(f"\n--- Checking Stata data for permno {missing_permno} ---")
        stata_subset = stata_df[stata_df['permno'] == missing_permno]
        print(f"Stata observations for permno {missing_permno}: {len(stata_subset)}")
        
        if len(stata_subset) > 0:
            print("Sample Stata observations:")
            print(stata_subset.head(10))
            
            # Check if missing dates exist in Stata
            stata_missing = stata_subset[stata_subset['yyyymm'].isin(missing_dates)]
            print(f"\nStata data for missing dates: {len(stata_missing)}")
            if len(stata_missing) > 0:
                print(stata_missing)
        
    except Exception as e:
        print(f"Error loading Stata data: {e}")
    
    print("\n=== Tracing Python Logic ===")
    
    # Load SignalMasterTable
    df = pd.read_parquet('../pyData/Intermediate/SignalMasterTable.parquet')
    df = df[['permno', 'gvkey', 'time_avail_m', 'mve_c', 'sicCRSP', 'exchcd']].copy()
    print(f"SignalMasterTable loaded: {df.shape}")
    
    # Check if permno 14755 exists
    permno_14755 = df[df['permno'] == missing_permno].copy()
    print(f"Permno {missing_permno} in SignalMasterTable: {len(permno_14755)}")
    
    if len(permno_14755) > 0:
        print("Date range for permno 14755:")
        print(f"Min date: {permno_14755['time_avail_m'].min()}")
        print(f"Max date: {permno_14755['time_avail_m'].max()}")
        
        # Check specific missing dates
        missing_time_dates = [pd.to_datetime(f'{str(yyyymm)[:4]}-{str(yyyymm)[4:6]}-01') for yyyymm in missing_dates]
        for missing_date in missing_time_dates:
            exists = len(permno_14755[permno_14755['time_avail_m'] == missing_date]) > 0
            print(f"Date {missing_date.strftime('%Y-%m')}: {'EXISTS' if exists else 'MISSING'}")
    
    # Apply early filtering like in CitationsRD.py
    df = df[df['time_avail_m'] >= '1970-01']
    print(f"After 1970 filter: {df.shape}")
    
    # Generate year
    df['year'] = df['time_avail_m'].dt.year
    
    # Check Compustat merge
    compustat = pd.read_parquet('../pyData/Intermediate/m_aCompustat.parquet')
    compustat = compustat[['permno', 'time_avail_m', 'xrd', 'sich', 'datadate', 'ceq']].copy()
    compustat = compustat[compustat['time_avail_m'] >= '1970-01']
    
    print(f"Compustat data: {compustat.shape}")
    compustat_14755 = compustat[compustat['permno'] == missing_permno]
    print(f"Compustat for permno {missing_permno}: {len(compustat_14755)}")
    
    # Merge
    df = df.merge(compustat, on=['permno', 'time_avail_m'], how='left')
    print(f"After Compustat merge: {df.shape}")
    
    # Check gvkey filtering
    df_before_gvkey = df.copy()
    df = df.dropna(subset=['gvkey'])
    print(f"After dropping missing gvkey: {df.shape}")
    
    permno_14755_after = df[df['permno'] == missing_permno]
    print(f"Permno {missing_permno} after gvkey filter: {len(permno_14755_after)}")
    
    if len(permno_14755_after) == 0:
        print("*** FOUND ISSUE: permno 14755 filtered out by gvkey check ***")
        gvkey_14755 = df_before_gvkey[df_before_gvkey['permno'] == missing_permno]
        print("Gvkey values for permno 14755:")
        print(gvkey_14755[['time_avail_m', 'gvkey']].head(20))
        return
    
    # Continue with patent data
    patent = pd.read_parquet('../pyData/Intermediate/PatentDataProcessed.parquet')
    patent = patent[['gvkey', 'year', 'ncitscale']].copy()
    
    df = df.merge(patent, on=['gvkey', 'year'], how='left')
    print(f"After patent merge: {df.shape}")
    
    permno_14755_after_patent = df[df['permno'] == missing_permno]
    print(f"Permno {missing_permno} after patent merge: {len(permno_14755_after_patent)}")

def debug_fastxtile_logic():
    """Debug the fastxtile tercile logic"""
    
    print("\n=== FastXtile Tercile Logic Debug ===")
    
    # Load test data to see if tercile creation is the issue
    try:
        # Simple test of tercile logic
        test_data = pd.DataFrame({
            'time_avail_m': pd.date_range('2020-06-01', periods=5, freq='MS'),
            'tempCitationsRD': [np.nan, 0.1, 0.2, 0.3, np.nan],
            'sizecat': [1, 1, 1, 1, 1]
        })
        
        print("Test data:")
        print(test_data)
        
        # Apply the logic from CitationsRD.py
        test_data['maincat'] = np.nan
        
        # KEY FIX: Assign maincat=1 to observations with missing tempCitationsRD
        test_data.loc[test_data['tempCitationsRD'].isna(), 'maincat'] = 1.0
        
        # For observations with valid tempCitationsRD, create terciles
        def create_terciles_per_period(group_df):
            if len(group_df) == 0:
                return group_df
            
            citations = group_df['tempCitationsRD']
            
            # Calculate 33rd and 67th percentiles
            q33 = citations.quantile(0.333)
            q67 = citations.quantile(0.667)
            
            # Assign terciles
            group_df['maincat'] = np.where(citations <= q33, 1.0, 
                                          np.where(citations <= q67, 2.0, 3.0))
            
            return group_df
        
        # Apply terciles only to valid data
        valid_mask = test_data['tempCitationsRD'].notna()
        if valid_mask.sum() > 0:
            valid_df = test_data[valid_mask].copy()
            tercile_df = valid_df.groupby('time_avail_m').apply(create_terciles_per_period).reset_index(drop=True)
            test_data.loc[valid_mask, 'maincat'] = tercile_df['maincat'].values
        
        # Create signal
        test_data['CitationsRD'] = np.nan
        test_data.loc[(test_data['sizecat'] == 1) & (test_data['maincat'] == 3), 'CitationsRD'] = 1
        test_data.loc[(test_data['sizecat'] == 1) & (test_data['maincat'] == 1), 'CitationsRD'] = 0
        
        print("\nAfter tercile logic:")
        print(test_data)
        
    except Exception as e:
        print(f"Error in tercile logic test: {e}")

if __name__ == "__main__":
    debug_citationsrd_missing()
    debug_fastxtile_logic()