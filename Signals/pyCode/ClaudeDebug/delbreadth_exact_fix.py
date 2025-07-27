# ABOUTME: Find exact fix for DelBreadth by using previous values from TR_13F
# ABOUTME: Run from pyCode/ directory: python3 ClaudeDebug/delbreadth_exact_fix.py

import pandas as pd
import numpy as np

def implement_exact_fix():
    """Implement the exact fix by carrying forward previous TR_13F values"""
    
    print("=== Implementing Exact DelBreadth Fix ===")
    
    # The expected values match the PREVIOUS TR_13F values:
    # 92182, 200904/200905: expect 0.069 = 200903 value
    # 92332, 200808: expect 0.577 = 200806 value
    
    # Load data
    df = pd.read_parquet('../pyData/Intermediate/SignalMasterTable.parquet')
    df = df[['permno', 'time_avail_m', 'exchcd', 'mve_c']].copy()
    
    tr_13f = pd.read_parquet('../pyData/Intermediate/TR_13F.parquet')
    tr_13f = tr_13f[['permno', 'time_avail_m', 'dbreadth']].copy()
    
    # Merge with TR_13F data
    df = df.merge(tr_13f, on=['permno', 'time_avail_m'], how='left')
    df = df.sort_values(['permno', 'time_avail_m'])
    
    # The issue: we need better forward-fill logic
    # Current approach loses values if there's no prior data at the FIRST observation
    # But TR_13F has data, it's just that our tsfill in TR_13F creation didn't extend far enough
    
    # Let's try a more complete fill approach:
    # 1. For each permno, get ALL their TR_13F dates
    # 2. For each SMT observation, find the last TR_13F value before/at that date
    
    result_rows = []
    
    permnos = df['permno'].unique()
    print(f"Processing {len(permnos)} permnos...")
    
    for i, permno in enumerate(permnos):
        if i % 10000 == 0:
            print(f"  Processed {i}/{len(permnos)} permnos")
            
        permno_smt = df[df['permno'] == permno].copy()
        permno_tr13f = tr_13f[tr_13f['permno'] == permno].copy()
        
        if len(permno_tr13f) == 0:
            # No TR_13F data for this permno - keep as NaN
            permno_smt['dbreadth_fixed'] = np.nan
        else:
            # For each SMT date, find the last TR_13F value at or before that date
            permno_smt['dbreadth_fixed'] = np.nan
            
            for idx, row in permno_smt.iterrows():
                smt_date = row['time_avail_m']
                
                # Find TR_13F observations at or before this date
                valid_tr13f = permno_tr13f[permno_tr13f['time_avail_m'] <= smt_date]
                
                if len(valid_tr13f) > 0:
                    # Use the most recent TR_13F value
                    most_recent = valid_tr13f.loc[valid_tr13f['time_avail_m'].idxmax()]
                    permno_smt.loc[idx, 'dbreadth_fixed'] = most_recent['dbreadth']
        
        result_rows.append(permno_smt)
    
    df_fixed = pd.concat(result_rows, ignore_index=True)
    
    # Test the specific missing observations
    missing_obs = [
        (92182, 200904, 0.069),
        (92182, 200905, 0.069),
        (92332, 200808, 0.577)
    ]
    
    print("\\nTesting fixed values:")
    print("permno   yyyymm   expected  original  fixed")
    print("-" * 50)
    
    fixes_found = 0
    for permno, yyyymm, expected in missing_obs:
        year = yyyymm // 100
        month = yyyymm % 100
        target_date = pd.to_datetime(f"{year}-{month:02d}-01")
        
        row = df_fixed[(df_fixed['permno'] == permno) & (df_fixed['time_avail_m'] == target_date)]
        
        if len(row) > 0:
            r = row.iloc[0]
            original = r['dbreadth'] if pd.notna(r['dbreadth']) else 'NaN'
            fixed = r['dbreadth_fixed'] if pd.notna(r['dbreadth_fixed']) else 'NaN'
            
            print(f"{permno:6d}   {yyyymm:6d}   {expected:7.3f}   {original:>7}   {fixed:>7}")
            
            if pd.notna(r['dbreadth_fixed']) and abs(r['dbreadth_fixed'] - expected) < 0.001:
                fixes_found += 1
                print(f"         *** EXACT MATCH! ***")
            elif pd.isna(r['dbreadth']) and pd.notna(r['dbreadth_fixed']):
                print(f"         Fixed missing value (diff = {abs(r['dbreadth_fixed'] - expected):.3f})")
    
    print(f"\\nFound exact fixes for {fixes_found} out of 3 missing observations")
    
    if fixes_found == 3:
        print("\\n=== SUCCESS: All missing observations can be fixed! ===")
        return True
    else:
        print("\\n=== Partial success - some observations still need investigation ===")
        return False

if __name__ == "__main__":
    success = implement_exact_fix()
    
    if success:
        print("\\nReady to implement fix in DelBreadth.py")