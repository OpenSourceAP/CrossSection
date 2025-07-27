# ABOUTME: Debug the final 2 missing DivSeason observations for permno 92823
# ABOUTME: Run from pyCode/ directory: python3 ClaudeDebug/divseason_final_2_debug.py

import pandas as pd
import numpy as np

def debug_final_2():
    """Debug the final 2 missing observations for permno 92823"""
    
    print("=== Debugging Final 2 Missing DivSeason Observations ===")
    
    target_permno = 92823
    missing_dates = [198510, 198511]
    
    print(f"Missing observations: permno {target_permno}, {missing_dates} (both expected DivSeason = 1)")
    
    # Check if this permno exists in current output
    try:
        current_output = pd.read_csv('../pyData/Predictors/DivSeason.csv')
        current_output = current_output.set_index(['permno', 'yyyymm'])
        
        permno_data = current_output[current_output.index.get_level_values('permno') == target_permno]
        if len(permno_data) > 0:
            min_date = permno_data.index.get_level_values('yyyymm').min()
            max_date = permno_data.index.get_level_values('yyyymm').max()
            print(f"  permno {target_permno}: {len(permno_data)} obs, range {min_date}-{max_date}")
            
            # Check the missing dates
            for yyyymm in missing_dates:
                if (target_permno, yyyymm) in current_output.index:
                    actual = current_output.loc[(target_permno, yyyymm), 'DivSeason']
                    print(f"    {yyyymm}: FOUND with value {actual}")
                else:
                    print(f"    {yyyymm}: MISSING")
                    
            # Show data around the missing dates
            print("\\n  Data around missing dates:")
            nearby_data = permno_data[
                (permno_data.index.get_level_values('yyyymm') >= 198505) &
                (permno_data.index.get_level_values('yyyymm') <= 198515)
            ]
            
            for (permno, yyyymm), row in nearby_data.iterrows():
                status = "***" if yyyymm in missing_dates else "   "
                print(f"    {yyyymm}: {row['DivSeason']} {status}")
        else:
            print(f"  permno {target_permno}: NO DATA")
            
    except Exception as e:
        print(f"Error loading current output: {e}")

def check_smt_existence():
    """Check if these observations exist in SignalMasterTable"""
    
    print("\\n=== SignalMasterTable Check ===")
    
    target_permno = 92823
    missing_dates = [198510, 198511]
    
    smt = pd.read_parquet('../pyData/Intermediate/SignalMasterTable.parquet')
    
    for yyyymm in missing_dates:
        year = yyyymm // 100
        month = yyyymm % 100
        target_date = pd.to_datetime(f"{year}-{month:02d}-01")
        
        exists = ((smt['permno'] == target_permno) & (smt['time_avail_m'] == target_date)).any()
        print(f"  permno {target_permno}, {yyyymm}: {'EXISTS' if exists else 'MISSING'} in SMT")

def trace_logic_for_92823():
    """Trace the DivSeason logic for permno 92823 around the missing dates"""
    
    print("\\n=== Tracing Logic for permno 92823 ===")
    
    target_permno = 92823
    target_yyyymm = 198510
    target_date = pd.to_datetime('1985-10-01')
    
    # Load dividend data
    dist_df = pd.read_parquet('../pyData/Intermediate/CRSPdistributions.parquet')
    dist_df = dist_df[['permno', 'cd1', 'cd2', 'cd3', 'divamt', 'exdt']].copy()
    dist_df = dist_df[(dist_df['cd1'] == 1) & (dist_df['cd2'] == 2)]
    dist_df['time_avail_m'] = pd.to_datetime(dist_df['exdt'].dt.to_period('M').dt.start_time)
    dist_df = dist_df.dropna(subset=['time_avail_m', 'divamt'])
    
    # Get dividend data for this permno
    permno_divs = dist_df[dist_df['permno'] == target_permno].copy()
    permno_divs['yyyymm'] = permno_divs['time_avail_m'].dt.year * 100 + permno_divs['time_avail_m'].dt.month
    permno_divs = permno_divs.sort_values('time_avail_m')
    
    print("\\nDividend data for permno 92823:")
    print("yyyymm   cd3   divamt")
    print("-" * 20)
    for _, row in permno_divs.iterrows():
        status = "***" if row['yyyymm'] in [198510, 198511] else "   "
        print(f"{row['yyyymm']:6d}  {row['cd3']:4.1f}  {row['divamt']:7.3f} {status}")
    
    # Check if there are any special dividends or issues
    special_divs = permno_divs[permno_divs['cd3'] >= 6]
    if len(special_divs) > 0:
        print("\\nSpecial dividends found:")
        for _, row in special_divs.iterrows():
            print(f"  {row['yyyymm']}: cd3={row['cd3']}, divamt={row['divamt']}")
    else:
        print("\\nNo special dividends found")
    
    # Check if target dates have dividend data
    target_div_data = permno_divs[permno_divs['yyyymm'].isin([198510, 198511])]
    if len(target_div_data) > 0:
        print("\\nTarget dates have dividend data:")
        for _, row in target_div_data.iterrows():
            print(f"  {row['yyyymm']}: cd3={row['cd3']}, divamt={row['divamt']}")
    else:
        print("\\nTarget dates have NO dividend data")
        print("This means they should get cd3 from forward-fill logic")

def assess_impact():
    """Assess the impact of these final 2 missing observations"""
    
    print("\\n=== Impact Assessment ===")
    
    print("DivSeason progress:")
    print("- Original missing: 13 observations")
    print("- Current missing: 2 observations") 
    print("- Improvement: 11/13 = 85% reduction")
    print("- New failure rate: 2 / 1,775,339 = 0.00011%")
    
    print("\\nOverall predictor status:")
    print("- DelBreadth: 0 missing (FIXED)")
    print("- DivSeason: 2 missing (99.9999% accuracy)")
    print("- CitationsRD: 576 missing (99.911% accuracy)")
    
    print("\\nRecommendation:")
    print("- 2 missing observations is exceptionally low (0.00011%)")
    print("- May represent true edge cases or data differences")
    print("- Consider moving to CitationsRD for larger impact")

if __name__ == "__main__":
    debug_final_2()
    check_smt_existence()
    trace_logic_for_92823()
    assess_impact()