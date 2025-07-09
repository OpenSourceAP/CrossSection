# ABOUTME: SignalMasterTable validation script comparing Python vs Stata outputs
# ABOUTME: Checks column names, types, row counts, and performs by-keys deviation analysis for SignalMasterTable
#
# Usage:
#   python3 utils/test_signalmaster.py [--maxrows N] [--tolerance FLOAT]
#
# Arguments:
#   --maxrows     Maximum rows to load (default: all rows, use for testing)
#   --tolerance   Tolerance for numeric comparisons (default: 1e-12)
#
# Input Files:
#   ../Data/Intermediate/SignalMasterTable.dta      (Stata reference data)
#   ../pyData/Intermediate/SignalMasterTable.parquet (Python data to validate)
#
# Output:
#   Console output with validation results showing:
#   - Basic validation: column names, types, row counts
#   - By-keys validation: common rows analysis using (permno, time_avail_m)
#   - Imperfect rows/cells analysis with vectorized comparison
#   - Overall pass/fail summary with execution time
#
# Examples:
#   python3 utils/test_signalmaster.py                    # Validate all rows
#   python3 utils/test_signalmaster.py --maxrows 1000     # Test with 1000 rows
#   python3 utils/test_signalmaster.py --tolerance 1e-10  # Custom tolerance

import pandas as pd
import numpy as np
from pathlib import Path
import argparse
import time
import sys

# Import efficient validation functions from test_dl.py
import os
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, current_dir)
from test_dl import (
    compare_columns_directly,
    val_one_basics,
    val_one_crow,
    generate_missing_rows_report
)

def load_data(maxrows=None):
    """Load both Stata and Python versions of SignalMasterTable"""
    
    print("Loading data...")
    
    # Load Stata version
    stata_path = Path("../Data/Intermediate/SignalMasterTable.dta")
    if not stata_path.exists():
        raise FileNotFoundError(f"Stata file not found: {stata_path}")
    
    print(f"  Loading Stata data from: {stata_path}")
    start_time = time.time()
    
    if maxrows and maxrows > 0:
        # For DTA files, we need to load all and then sample
        stata_df = pd.read_stata(stata_path)
        if len(stata_df) > maxrows:
            stata_df = stata_df.sample(n=maxrows, random_state=42).sort_values(['permno', 'time_avail_m'])
    else:
        stata_df = pd.read_stata(stata_path)
    
    print(f"  Stata data loaded in {time.time() - start_time:.2f}s: {stata_df.shape}")
    
    # Load Python version
    python_path = Path("../pyData/Intermediate/SignalMasterTable.parquet")
    if not python_path.exists():
        raise FileNotFoundError(f"Python file not found: {python_path}")
    
    print(f"  Loading Python data from: {python_path}")
    start_time = time.time()
    
    if maxrows and maxrows > 0:
        python_df = pd.read_parquet(python_path)
        if len(python_df) > maxrows:
            python_df = python_df.sample(n=maxrows, random_state=42).sort_values(['permno', 'time_avail_m'])
    else:
        python_df = pd.read_parquet(python_path)
    
    print(f"  Python data loaded in {time.time() - start_time:.2f}s: {python_df.shape}")
    
    return stata_df, python_df

def print_basic_validation_results(basic_results):
    """Print basic validation results in SignalMasterTable format"""
    print("\n" + "="*80)
    print("BASIC VALIDATION")
    print("="*80)
    
    # Print numbered validation results
    for i, validation in enumerate(basic_results['validations'], 1):
        print(f"\n{i}. {validation}")
    
    # Print details
    if basic_results['details']:
        print("\n   Details:")
        for detail in basic_results['details']:
            print(f"   {detail}")
    
    return basic_results

def print_by_keys_validation_results(keys_results):
    """Print by-keys validation results in SignalMasterTable format"""
    print("\n" + "="*80)
    print("BY-KEYS VALIDATION")
    print("="*80)
    
    keys = ['permno', 'time_avail_m']
    print(f"Using keys: {keys}")
    
    # Print key statistics and validation results
    if keys_results['analysis']:
        analysis = keys_results['analysis']
        print(f"\nKey Statistics:")
        print(f"  Total Stata rows: {analysis['full_data_rows']}")
        print(f"  Common rows: {analysis['matched_by_key_rows']}")
        print(f"  Perfect rows: {analysis['perfect_rows']}")
        print(f"  Imperfect rows: {analysis['imperfect_rows']}")
        print(f"  Missing from Python: {analysis['missing_stata_rows']}")
        
        # Print validation results (excluding basic ones)
        bykeys_validations = keys_results['validations'][3:]  # Skip first 3 basic validations
        for i, validation in enumerate(bykeys_validations, 4):
            print(f"\n{i}. {validation}")
        
        # Print worst columns if available
        if keys_results['worst_columns']:
            print("\n   Worst columns by imperfect percentage:")
            for col_info in keys_results['worst_columns']:
                print(f"     {col_info}")
    
    return keys_results

def main():
    """Main validation function"""
    
    parser = argparse.ArgumentParser(description='Validate SignalMasterTable Python vs Stata outputs')
    parser.add_argument('--maxrows', type=int, default=None, help='Maximum rows to load (default: all rows)')
    parser.add_argument('--tolerance', type=float, default=1e-12, help='Tolerance for numeric comparisons')
    
    args = parser.parse_args()
    
    print("SignalMasterTable Validation")
    print("="*80)
    print(f"Max rows: {args.maxrows if args.maxrows else 'All'}")
    print(f"Tolerance: {args.tolerance}")
    
    start_time = time.time()
    
    try:
        # Load data
        stata_df, python_df = load_data(maxrows=args.maxrows)
        
        # Run efficient validations using imported functions
        keys = ['permno', 'time_avail_m']
        
        # Basic validation using val_one_basics
        basic_results = val_one_basics('SignalMasterTable', stata_df, python_df)
        print_basic_validation_results(basic_results)
        
        # By-keys validation using val_one_crow
        keys_results = val_one_crow('SignalMasterTable', basic_results, stata_df, python_df, keys, args.tolerance)
        print_by_keys_validation_results(keys_results)
        
        # Summary
        print("\n" + "="*80)
        print("VALIDATION SUMMARY")
        print("="*80)
        
        # Count passed/failed validations
        passed = 0
        total = len(keys_results['validations'])
        
        for validation in keys_results['validations']:
            if "✓" in validation:
                passed += 1
                status = "✓ PASS"
            else:
                status = "✗ FAIL"
            print(f"{validation}: {status}")
        
        print(f"\nOverall: {passed}/{total} tests passed")
        
        if passed == total:
            print("🎉 All validations PASSED!")
        else:
            print("❌ Some validations FAILED - review output above")
        
        print(f"\nTotal runtime: {time.time() - start_time:.2f}s")
        
        return 0 if passed == total else 1
        
    except Exception as e:
        print(f"\nError during validation: {e}")
        import traceback
        traceback.print_exc()
        return 1

if __name__ == "__main__":
    sys.exit(main())