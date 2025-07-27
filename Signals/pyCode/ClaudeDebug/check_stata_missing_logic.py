# ABOUTME: Check what Stata does with missing tempCitationsRD observations
# ABOUTME: Run from pyCode/ directory: python3 ClaudeDebug/check_stata_missing_logic.py

import pandas as pd
import numpy as np

def check_stata_missing_behavior():
    """Check what Stata actually outputs for observations with missing tempCitationsRD"""
    
    print("=== Checking Stata Behavior for Missing TempCitationsRD ===")
    
    # Load Stata output
    stata_df = pd.read_csv('../Data/Predictors/CitationsRD.csv')
    print(f"Stata output: {len(stata_df)} rows")
    
    # Focus on permno 14755 and the missing date range
    permno_14755_stata = stata_df[stata_df['permno'] == 14755].copy()
    print(f"Permno 14755 in Stata: {len(permno_14755_stata)} rows")
    
    if len(permno_14755_stata) > 0:
        print("Stata output for permno 14755 (first 20):")
        print(permno_14755_stata.head(20))
        
        # Check the specific missing dates
        missing_yyyymm = [201706, 201707, 201708, 201709, 201710, 201711, 201712, 201801, 201802, 201803]
        stata_missing = permno_14755_stata[permno_14755_stata['yyyymm'].isin(missing_yyyymm)]
        
        print(f"\nStata data for 'missing' dates: {len(stata_missing)}")
        if len(stata_missing) > 0:
            print(stata_missing)
            
            # What values does Stata assign?
            unique_values = stata_missing['CitationsRD'].unique()
            print(f"CitationsRD values in 'missing' range: {unique_values}")
            
            # This tells us: Stata DOES output these observations, probably with CitationsRD=0
            # This means they come from June 2017 data where tempCitationsRD was 0.0 (not missing)
    
    # Check a broader pattern - do any observations have CitationsRD but come from missing tempCitationsRD?
    print("\n=== Checking if Stata outputs observations from missing tempCitationsRD ===")
    
    # To determine this, I need to check if the pattern suggests that missing tempCitationsRD 
    # observations get maincat assigned and then CitationsRD assigned
    
    # Look at the distribution of CitationsRD values in Stata
    stata_values = stata_df['CitationsRD'].value_counts().sort_index()
    print("Stata CitationsRD value distribution:")
    print(stata_values)
    
    # If Stata only outputs 0 and 1, then it means:
    # - maincat=1 and sizecat=1 -> CitationsRD=0 
    # - maincat=3 and sizecat=1 -> CitationsRD=1
    # - Everything else (including missing maincat) -> not in output
    
    # But if we see other values or patterns, it means something different

def analyze_june_2017_pattern():
    """Analyze what should happen to June 2017 observation"""
    
    print("\n=== Analyzing June 2017 Pattern ===")
    
    # The key insight from my debugging:
    # - June 2017 exists for permno 14755
    # - tempCitationsRD = 0.0 (not missing!)
    # - This should get maincat via terciles
    # - With sizecat=1, it should get a CitationsRD value
    # - This should then expand to 201706-201805
    
    # But my current output shows 201806+ only
    # This suggests the issue is NOT missing tempCitationsRD
    # The issue is that June 2017 is getting filtered out somewhere
    
    print("From debugging, June 2017 has:")
    print("- tempCitationsRD = 0.0 (not missing)")
    print("- Should get maincat = 1 (lowest tercile)")  
    print("- With sizecat = 1, should get CitationsRD = 0")
    print("- Should expand to 201706-201805")
    print("")
    print("But Python output starts from 201806")
    print("This suggests June 2017 is being filtered out or not assigned a signal")

if __name__ == "__main__":
    check_stata_missing_behavior()
    analyze_june_2017_pattern()