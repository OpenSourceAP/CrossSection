# ABOUTME: Predictors validation script comparing Python vs Stata predictor outputs
# ABOUTME: Checks column names, types, row counts, and performs by-keys deviation analysis for predictor signals
#
# Usage:
#   python3 utils/test_predictors.py [--signals SIGNAL1 SIGNAL2] [--maxrows N] [--tolerance FLOAT]
#
# Arguments:
#   --signals     Specific signals to validate (default: all available signals)
#   --list        List all available signals and exit
#   --maxrows     Maximum rows to load (default: all rows, use for testing)
#   --tolerance   Tolerance for numeric comparisons (default: 1e-12)
#
# Input Files:
#   ../Data/Predictors/*.csv          (Stata reference data)
#   ../pyData/Predictors/*.csv        (Python data to validate)
#
# Output:
#   Console output with validation results showing:
#   - Basic validation: column names, types, row counts
#   - By-keys validation: common rows analysis using (permno, yyyymm)
#   - Imperfect rows/cells analysis with vectorized comparison
#   - Overall pass/fail summary with execution time
#
# Examples:
#   python3 utils/test_predictors.py                           # Validate all signals
#   python3 utils/test_predictors.py --list                    # Show available signals
#   python3 utils/test_predictors.py --signals Accruals        # Test one signal
#   python3 utils/test_predictors.py --signals Accruals AccrualsBM  # Test specific signals
#   python3 utils/test_predictors.py --maxrows 1000            # Test with row limit

import pandas as pd
import numpy as np
from pathlib import Path
import argparse
import time
import sys
import glob

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

def get_available_signals():
    """Get list of available signals by examining Stata output directory"""
    stata_dir = Path("../Data/Predictors")
    if not stata_dir.exists():
        return []
    
    stata_files = list(stata_dir.glob("*.csv"))
    signals = [f.stem for f in stata_files]  # Remove .csv extension
    return sorted(signals)

def load_signal_data(signal_name, maxrows=None):
    """Load both Stata and Python versions of a predictor signal"""
    
    print(f"Loading {signal_name} data...")
    
    # Load Stata version
    stata_path = Path(f"../Data/Predictors/{signal_name}.csv")
    if not stata_path.exists():
        raise FileNotFoundError(f"Stata file not found: {stata_path}")
    
    print(f"  Loading Stata data from: {stata_path}")
    start_time = time.time()
    
    if maxrows and maxrows > 0:
        stata_df = pd.read_csv(stata_path, nrows=maxrows)
    else:
        stata_df = pd.read_csv(stata_path)
    
    print(f"  Stata data loaded in {time.time() - start_time:.2f}s: {stata_df.shape}")
    
    # Load Python version
    python_path = Path(f"../pyData/Predictors/{signal_name}.csv")
    if not python_path.exists():
        raise FileNotFoundError(f"Python file not found: {python_path}")
    
    print(f"  Loading Python data from: {python_path}")
    start_time = time.time()
    
    if maxrows and maxrows > 0:
        python_df = pd.read_csv(python_path, nrows=maxrows)
    else:
        python_df = pd.read_csv(python_path)
    
    print(f"  Python data loaded in {time.time() - start_time:.2f}s: {python_df.shape}")
    
    return stata_df, python_df

def print_basic_validation_results(basic_results, signal_name):
    """Print basic validation results for predictor signals"""
    print("\n" + "="*80)
    print(f"BASIC VALIDATION - {signal_name}")
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

def print_by_keys_validation_results(keys_results, signal_name):
    """Print by-keys validation results for predictor signals"""
    print("\n" + "="*80)
    print(f"BY-KEYS VALIDATION - {signal_name}")
    print("="*80)
    
    keys = ['permno', 'yyyymm']
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

def validate_single_signal(signal_name, maxrows=None, tolerance=1e-12):
    """Validate a single predictor signal"""
    
    try:
        # Load data
        stata_df, python_df = load_signal_data(signal_name, maxrows=maxrows)
        
        # Run efficient validations using imported functions
        keys = ['permno', 'yyyymm']
        
        # Basic validation using val_one_basics
        basic_results = val_one_basics(signal_name, stata_df, python_df)
        print_basic_validation_results(basic_results, signal_name)
        
        # By-keys validation using val_one_crow
        keys_results = val_one_crow(signal_name, basic_results, stata_df, python_df, keys, tolerance)
        print_by_keys_validation_results(keys_results, signal_name)
        
        # Return validation results
        passed = 0
        total = len(keys_results['validations'])
        
        for validation in keys_results['validations']:
            if "✓" in validation:
                passed += 1
        
        return {
            'signal_name': signal_name,
            'passed': passed,
            'total': total,
            'success': passed == total,
            'validations': keys_results['validations'],
            'analysis': keys_results.get('analysis')
        }
        
    except Exception as e:
        print(f"\nError validating {signal_name}: {e}")
        import traceback
        traceback.print_exc()
        return {
            'signal_name': signal_name,
            'passed': 0,
            'total': 0,
            'success': False,
            'error': str(e)
        }

def main():
    """Main validation function"""
    
    parser = argparse.ArgumentParser(description='Validate predictor Python vs Stata outputs')
    parser.add_argument('--signals', nargs='*', help='Specific signals to validate (default: all signals)')
    parser.add_argument('--list', action='store_true', help='List all available signals and exit')
    parser.add_argument('--maxrows', type=int, default=None, help='Maximum rows to load (default: all rows)')
    parser.add_argument('--tolerance', type=float, default=1e-12, help='Tolerance for numeric comparisons')
    
    args = parser.parse_args()
    
    # Check that script is being run from the correct directory (pyCode/)
    if not Path("01_DownloadData.py").exists():
        print("ERROR: This script must be run from the pyCode/ directory.")
        print("Usage: cd pyCode/ && python3 utils/test_predictors.py")
        sys.exit(1)
    
    # Get available signals
    available_signals = get_available_signals()
    
    if not available_signals:
        print("ERROR: No predictor signals found in ../Data/Predictors/")
        print("Make sure Stata predictors have been generated first.")
        sys.exit(1)
    
    # List signals if requested
    if args.list:
        print("Available predictor signals for validation:")
        print("=" * 50)
        for i, signal in enumerate(available_signals, 1):
            print(f"{i:2d}. {signal}")
        print(f"\nTotal: {len(available_signals)} signals")
        return
    
    # Determine which signals to validate
    if args.signals:
        # Validate that requested signals exist
        invalid_signals = [s for s in args.signals if s not in available_signals]
        if invalid_signals:
            print(f"Error: Invalid signals specified: {invalid_signals}")
            print("Use --list to see available signals")
            return
        signals_to_validate = args.signals
    else:
        signals_to_validate = available_signals
    
    print("Predictor Signals Validation")
    print("=" * 80)
    print(f"Signals to validate: {len(signals_to_validate)}")
    print(f"Max rows: {args.maxrows if args.maxrows else 'All'}")
    print(f"Tolerance: {args.tolerance}")
    
    start_time = time.time()
    
    # Validate each signal
    results = []
    for signal in signals_to_validate:
        print(f"\n{'='*80}")
        print(f"VALIDATING SIGNAL: {signal}")
        print(f"{'='*80}")
        
        result = validate_single_signal(signal, maxrows=args.maxrows, tolerance=args.tolerance)
        results.append(result)
    
    # Overall summary
    print("\n" + "="*80)
    print("OVERALL VALIDATION SUMMARY")
    print("="*80)
    
    total_signals = len(results)
    successful_signals = len([r for r in results if r['success']])
    failed_signals = total_signals - successful_signals
    
    print(f"\nSignals validated: {total_signals}")
    print(f"Successful: {successful_signals}")
    print(f"Failed: {failed_signals}")
    
    # Detail by signal
    for result in results:
        signal_name = result['signal_name']
        if result['success']:
            print(f"✓ {signal_name}: {result['passed']}/{result['total']} tests passed")
        else:
            if 'error' in result:
                print(f"✗ {signal_name}: ERROR - {result['error']}")
            else:
                print(f"✗ {signal_name}: {result['passed']}/{result['total']} tests passed")
    
    print(f"\nTotal runtime: {time.time() - start_time:.2f}s")
    
    if successful_signals == total_signals:
        print("🎉 All signal validations PASSED!")
        return 0
    else:
        print("❌ Some signal validations FAILED - review output above")
        return 1

if __name__ == "__main__":
    sys.exit(main())