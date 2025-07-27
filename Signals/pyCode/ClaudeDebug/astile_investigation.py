# ABOUTME: Investigate Stata's astile function vs our median split approach
# ABOUTME: Run from pyCode/ directory: python3 ClaudeDebug/astile_investigation.py

import pandas as pd
import numpy as np

def investigate_astile_behavior():
    """Investigate what Stata's astile does vs our median split"""
    
    print("=== Stata astile vs Python Implementation Investigation ===")
    
    # From CitationsRD.do: bys time_avail_m: astile sizecat = mve_c, qc(exchcd == 1) nq(2)
    # This means:
    # - Within each time_avail_m group
    # - Create size categories (sizecat) based on market cap (mve_c)  
    # - Use companies where exchcd == 1 (NYSE) to determine quantile cutoffs
    # - Create 2 quantiles (nq=2) - so this creates small (1) and large (2) categories
    
    print("Stata astile command: astile sizecat = mve_c, qc(exchcd == 1) nq(2)")
    print("- Creates 2 size categories based on NYSE breakpoints")
    print("- astile creates EQUAL-SIZED groups within the qualifying condition")
    print("- Different from median split!")
    print()
    
    # The key difference might be:
    # 1. astile creates equal-sized groups (50% each for nq=2)
    # 2. median split creates groups split by median VALUE
    # 3. These are different when there are ties at the median!
    
    print("Key difference: astile vs median split")
    print("- astile: Equal-sized groups (50% of NYSE stocks in each category)")
    print("- median: Split by median value (could be unequal sizes with ties)")
    print()
    
    # Let's test this with sample data
    print("Testing with sample data...")
    
    # Create test data with ties at median
    nyse_mve = [100, 200, 300, 300, 300, 300, 400, 500]  # Median = 300, but 4 companies at median
    
    print(f"NYSE market caps: {nyse_mve}")
    print(f"Median: {np.median(nyse_mve)}")
    
    # Median split approach (what we're doing)
    median_val = np.median(nyse_mve)
    median_small = sum(1 for x in nyse_mve if x < median_val)
    median_large = sum(1 for x in nyse_mve if x >= median_val)
    
    print(f"Median split: Small (<{median_val}): {median_small}, Large (>={median_val}): {median_large}")
    
    # astile approach (equal-sized groups)
    sorted_mve = sorted(nyse_mve)
    n = len(sorted_mve)
    # For nq=2, we want 50% in each group
    # The breakpoint should be between positions n//2-1 and n//2
    if n % 2 == 0:
        # Even number: average of middle two values
        astile_cutoff = (sorted_mve[n//2-1] + sorted_mve[n//2]) / 2
    else:
        # Odd number: middle value
        astile_cutoff = sorted_mve[n//2]
    
    astile_small = sum(1 for x in nyse_mve if x <= astile_cutoff)
    astile_large = sum(1 for x in nyse_mve if x > astile_cutoff)
    
    print(f"astile approach: Small (<={astile_cutoff}): {astile_small}, Large (>{astile_cutoff}): {astile_large}")
    
    if median_val != astile_cutoff:
        print("*** DIFFERENCE FOUND! ***")
        print(f"Median cutoff: {median_val}")
        print(f"astile cutoff: {astile_cutoff}")
    else:
        print("Same cutoff - no difference in this case")

def test_real_data_astile():
    """Test astile logic on real data to see if it explains the missing observations"""
    
    print("\n=== Testing astile on Real Data ===")
    
    # Load real data for a specific time period where we have issues
    df = pd.read_parquet('../pyData/Intermediate/SignalMasterTable.parquet')
    df = df[['permno', 'gvkey', 'time_avail_m', 'mve_c', 'sicCRSP', 'exchcd']].copy()
    
    # Focus on June 2017 (from CitationsRD debug - this had issues)
    target_date = pd.to_datetime('2017-06-01')
    june_2017 = df[df['time_avail_m'] == target_date].copy()
    
    print(f"June 2017 data: {len(june_2017)} total companies")
    
    if len(june_2017) > 0:
        # Filter to valid market cap
        june_2017 = june_2017.dropna(subset=['mve_c'])
        print(f"With valid market cap: {len(june_2017)}")
        
        # Get NYSE stocks (exchcd == 1)
        nyse_stocks = june_2017[june_2017['exchcd'] == 1]
        print(f"NYSE stocks: {len(nyse_stocks)}")
        
        if len(nyse_stocks) > 0:
            # Current median approach
            median_mve = nyse_stocks['mve_c'].median()
            median_small = (june_2017['mve_c'] <= median_mve).sum()
            median_large = (june_2017['mve_c'] > median_mve).sum()
            
            print(f"\nCurrent median approach:")
            print(f"  Median cutoff: {median_mve:.2f}")
            print(f"  Small (<=median): {median_small}")
            print(f"  Large (>median): {median_large}")
            
            # Proper astile approach  
            nyse_sorted = nyse_stocks['mve_c'].sort_values().values
            n = len(nyse_sorted)
            
            # astile with nq=2 creates equal-sized groups
            # So we want the median NYSE stock as the cutoff
            if n % 2 == 0:
                # Even: average of two middle values
                astile_cutoff = (nyse_sorted[n//2-1] + nyse_sorted[n//2]) / 2
            else:
                # Odd: middle value
                astile_cutoff = nyse_sorted[n//2]
            
            astile_small = (june_2017['mve_c'] <= astile_cutoff).sum()
            astile_large = (june_2017['mve_c'] > astile_cutoff).sum()
            
            print(f"\nProper astile approach:")
            print(f"  astile cutoff: {astile_cutoff:.2f}")
            print(f"  Small (<=cutoff): {astile_small}")
            print(f"  Large (>cutoff): {astile_large}")
            
            if abs(median_mve - astile_cutoff) > 0.01:
                print(f"\n*** SIGNIFICANT DIFFERENCE: {abs(median_mve - astile_cutoff):.2f} ***")
                print("This could explain the missing observations!")
                
                # Check how many observations would change categories
                changed = ((june_2017['mve_c'] > min(median_mve, astile_cutoff)) & 
                          (june_2017['mve_c'] <= max(median_mve, astile_cutoff))).sum()
                print(f"Observations that would change categories: {changed}")
            else:
                print("Cutoffs are very similar - not the main issue")

if __name__ == "__main__":
    investigate_astile_behavior()
    test_real_data_astile()