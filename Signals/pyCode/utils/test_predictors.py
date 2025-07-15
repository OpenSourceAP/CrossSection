# ABOUTME: test_predictors.py - validates Python predictor outputs against Stata CSV files
# ABOUTME: Precision validation script for predictor CSV files following CLAUDE.md requirements

"""
test_predictors.py

Usage:
    cd pyCode/
    source .venv/bin/activate
    python3 utils/test_predictors.py                    # Test all predictors
    python3 utils/test_predictors.py --predictors Accruals  # Test specific predictor

Precision Validation (per CLAUDE.md:251-255):
1. Column names and order match exactly
2. Python observations are a superset of Stata observations
3. For common observations, Pth percentile absolute difference < TOL_DIFF
   - common observations are observations that are in both Stata and Python

Inputs:
    - Stata CSV files in ../Data/Predictors/
    - Python CSV files in ../pyData/Predictors/

Outputs:
    - Console validation results with ✓/✗ symbols
    - Validation log saved to ../Logs/testout_predictors.md
    - Feedback showing worst observations and differences
"""

import pandas as pd
import argparse
from pathlib import Path
from datetime import datetime
import sys

# ================================
# VALIDATION CONFIGURATION
# ================================

PTH_PERCENTILE = 1.00  # 100th percentile (maximum)
TOL_DIFF = 1e-6  # Tolerance for absolute differences
INDEX_COLS = ['permno', 'yyyymm']  # Index columns for observations

def load_csv_robust(file_path):
    """Load CSV file with robust error handling"""
    try:
        df = pd.read_csv(file_path)
        return df
    except Exception as e:
        print(f"Error loading {file_path}: {e}")
        return None

def validate_precision_requirements(stata_df, python_df, predictor_name):
    """
    Perform precision validation following CLAUDE.md requirements
    Returns (passed, results_dict)
    """
    results = {}
    
    # Set index for both dataframes
    try:
        stata_indexed = stata_df.set_index(INDEX_COLS)
        python_indexed = python_df.set_index(INDEX_COLS)
    except KeyError as e:
        print(f"  ✗ Missing index columns: {e}")
        return False, {'error': f'Missing index columns: {e}'}
    
    # 1. Column names and order match exactly
    stata_cols = list(stata_indexed.columns)
    python_cols = list(python_indexed.columns)
    
    cols_match = stata_cols == python_cols
    results['columns_match'] = cols_match
    results['stata_columns'] = stata_cols
    results['python_columns'] = python_cols
    
    if not cols_match:
        print(f"  ✗ Column names mismatch")
        print(f"    Stata:  {stata_cols}")
        print(f"    Python: {python_cols}")
        return False, results
    else:
        print(f"  ✓ Column names match: {stata_cols}")
    
    # 2. Python observations are superset of Stata observations
    stata_obs = set(stata_indexed.index)
    python_obs = set(python_indexed.index)
    
    is_superset = python_obs.issuperset(stata_obs)
    results['is_superset'] = is_superset
    results['stata_obs_count'] = len(stata_obs)
    results['python_obs_count'] = len(python_obs)
    
    if is_superset:
        print(f"  ✓ Python observations are superset of Stata: Stata={len(stata_obs)}, Python={len(python_obs)}")
    else:
        missing_obs = stata_obs - python_obs
        print(f"  ✗ Python missing {len(missing_obs)} Stata observations")
        results['missing_observations'] = list(missing_obs)[:10]  # Show first 10
        return False, results
    
    # 3. For common observations, Pth percentile absolute difference < TOL_DIFF
    common_obs = stata_indexed.index.intersection(python_indexed.index)
    results['common_obs_count'] = len(common_obs)
    
    if len(common_obs) == 0:
        print(f"  ✗ No common observations found")
        return False, results
    
    cobs_stata = stata_indexed.loc[common_obs]
    cobs_python = python_indexed.loc[common_obs]
    
    # Calculate absolute differences
    cobs_diff = abs(cobs_python - cobs_stata)
    
    # Get Pth percentile of absolute differences
    pth_percentile_diff = cobs_diff.abs().quantile(PTH_PERCENTILE).iloc[0]
    
    precision_ok = pth_percentile_diff < TOL_DIFF
    results['pth_percentile_diff'] = pth_percentile_diff
    results['precision_ok'] = precision_ok
    
    if precision_ok:
        print(f"  ✓ Precision acceptable: {PTH_PERCENTILE*100:.0f}th percentile diff = {pth_percentile_diff:.2e} < {TOL_DIFF:.2e}")
    else:
        print(f"  ✗ Precision failed: {PTH_PERCENTILE*100:.0f}th percentile diff = {pth_percentile_diff:.2e} >= {TOL_DIFF:.2e}")
    
    # Generate feedback for failed precision
    if not precision_ok:
        results['feedback'] = generate_feedback(cobs_stata, cobs_python, cobs_diff, predictor_name)
    
    return cols_match and is_superset and precision_ok, results

def generate_feedback(cobs_stata, cobs_python, cobs_diff, predictor_name):
    """
    Generate feedback showing worst observations and differences
    """
    feedback = {}
    
    # Find observations with differences >= TOL_DIFF
    bad_idx = cobs_diff[cobs_diff[predictor_name] > TOL_DIFF].index
    
    if len(bad_idx) > 0:
        bad_python = cobs_python.loc[bad_idx].rename(columns={predictor_name: 'python'})
        bad_stata = cobs_stata.loc[bad_idx].rename(columns={predictor_name: 'stata'})
        
        bad_df = bad_python.join(bad_stata, on=INDEX_COLS)
        bad_df['diff'] = bad_df['python'] - bad_df['stata']
        
        # Most recent observations that exceed tolerance
        recent_bad = bad_df.reset_index().sort_values(by='yyyymm', ascending=False).head(10)
        feedback['recent_bad'] = recent_bad
        
        # Observations with largest differences
        largest_diff = bad_df.reset_index().sort_values(by='diff', key=abs, ascending=False).head(10)
        feedback['largest_diff'] = largest_diff
        
        feedback['bad_count'] = len(bad_idx)
        feedback['total_count'] = len(cobs_diff)
        feedback['bad_ratio'] = len(bad_idx) / len(cobs_diff)
    
    return feedback

def validate_predictor(predictor_name):
    """Validate a single predictor against Stata output"""
    
    print(f"\n=== Validating {predictor_name} ===")
    
    # Load Stata CSV
    stata_path = Path(f"../Data/Predictors/{predictor_name}.csv")
    if not stata_path.exists():
        print(f"  ✗ Stata file not found: {stata_path}")
        return False, {}
    
    stata_df = load_csv_robust(stata_path)
    if stata_df is None:
        return False, {}
    
    # Load Python CSV
    python_path = Path(f"../pyData/Predictors/{predictor_name}.csv") 
    if not python_path.exists():
        print(f"  ✗ Python file not found: {python_path}")
        return False, {}
    
    python_df = load_csv_robust(python_path)
    if python_df is None:
        return False, {}
    
    print(f"  Loaded Stata: {len(stata_df)} rows, Python: {len(python_df)} rows")
    
    # Perform precision validation
    passed, results = validate_precision_requirements(stata_df, python_df, predictor_name)
    
    return passed, results

def get_available_predictors():
    """Get list of available predictor files"""
    stata_dir = Path("../Data/Predictors/")
    python_dir = Path("../pyData/Predictors/")
    
    stata_files = set()
    python_files = set()
    
    if stata_dir.exists():
        stata_files = {f.stem for f in stata_dir.glob("*.csv")}
    
    if python_dir.exists():
        python_files = {f.stem for f in python_dir.glob("*.csv")}
    
    # Return predictors that exist in both or either
    all_predictors = stata_files.union(python_files)
    return sorted(list(all_predictors))

def write_markdown_log(all_results, test_predictors, passed_count):
    """Write detailed results to markdown log file"""
    log_path = Path("../Logs/testout_predictors.md")
    
    with open(log_path, 'w') as f:
        f.write(f"# Predictor Validation Results\n\n")
        f.write(f"**Generated**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
        f.write(f"**Configuration**:\n")
        f.write(f"- PTH_PERCENTILE: {PTH_PERCENTILE}\n")
        f.write(f"- TOL_DIFF: {TOL_DIFF}\n")
        f.write(f"- INDEX_COLS: {INDEX_COLS}\n\n")
        
        f.write(f"## Summary\n\n")
        f.write(f"- **Tested**: {len(test_predictors)}\n")
        f.write(f"- **Passed**: {passed_count}\n")
        f.write(f"- **Failed**: {len(test_predictors) - passed_count}\n\n")
        
        f.write(f"## Detailed Results\n\n")
        
        for predictor, result in all_results.items():
            f.write(f"### {predictor}\n\n")
            
            if result['passed']:
                f.write(f"**Status**: ✓ PASSED\n\n")
            else:
                f.write(f"**Status**: ✗ FAILED\n\n")
            
            details = result['details']
            
            if 'error' in details:
                f.write(f"**Error**: {details['error']}\n\n")
                continue
            
            # Write basic info
            f.write(f"**Columns**: {details.get('stata_columns', 'N/A')}\n\n")
            f.write(f"**Observations**:\n")
            f.write(f"- Stata:  {details['stata_obs_count']:,}\n")
            f.write(f"- Python: {details['python_obs_count']:,}\n")
            f.write(f"- Common: {details['common_obs_count']:,}\n\n")
            
            # Write precision results
            if 'pth_percentile_diff' in details:
                f.write(f"**Pth percentile absolute difference**: {details['pth_percentile_diff']:.2e} (tolerance: {TOL_DIFF:.2e})\n\n")
            
            # Write feedback if available
            if 'feedback' in details:
                feedback = details['feedback']
                f.write(f"**Feedback**:\n")
                f.write(f"- Num observations with diff >= TOL_DIFF: {feedback.get('bad_count', 0)}/{feedback.get('total_count', 0)} ({feedback.get('bad_ratio', 0):.3%})\n\n")
                
                if 'recent_bad' in feedback and len(feedback['recent_bad']) > 0:
                    f.write(f"**Most Recent Bad Observations**:\n")
                    f.write(f"```\n{feedback['recent_bad'].to_string()}\n```\n\n")
                
                if 'largest_diff' in feedback and len(feedback['largest_diff']) > 0:
                    f.write(f"**Largest Differences**:\n")
                    f.write(f"```\n{feedback['largest_diff'].to_string()}\n```\n\n")
            
            f.write("---\n\n")
    
    print(f"\nDetailed results written to: {log_path}")

def main():
    parser = argparse.ArgumentParser(description='Validate Python predictor outputs against Stata CSV files')
    parser.add_argument('--predictors', '-p', nargs='+', help='Specific predictors to validate')
    parser.add_argument('--list', '-l', action='store_true', help='List available predictors and exit')
    
    args = parser.parse_args()
    
    available_predictors = get_available_predictors()
    
    if args.list:
        print("Available predictors:")
        for pred in available_predictors:
            print(f"  {pred}")
        return
    
    # Select predictors to test
    if args.predictors:
        test_predictors = args.predictors
        # Check if all requested predictors are available
        missing = set(test_predictors) - set(available_predictors)
        if missing:
            print(f"Warning: These predictors not found: {missing}")
    else:
        test_predictors = available_predictors
    
    if not test_predictors:
        print("No predictors to test")
        return
    
    print(f"Testing {len(test_predictors)} predictors: {test_predictors}")
    
    # Validate each predictor
    all_results = {}
    passed_count = 0
    
    for predictor in test_predictors:
        passed, results = validate_predictor(predictor)
        all_results[predictor] = {'passed': passed, 'details': results}
        if passed:
            passed_count += 1
            print(f"  ✓ {predictor} PASSED")
        else:
            print(f"  ✗ {predictor} FAILED")
            # Print feedback for failed predictors
            if 'feedback' in results and isinstance(results['feedback'], dict):
                feedback = results['feedback']
                print(f"    Bad observations: {feedback.get('bad_count', 0)}/{feedback.get('total_count', 0)} ({feedback.get('bad_ratio', 0):.1%})")
    
    # Write markdown log
    write_markdown_log(all_results, test_predictors, passed_count)
    
    # Summary
    print(f"\n=== SUMMARY ===")
    print(f"Tested: {len(test_predictors)}")
    print(f"Passed: {passed_count}")
    print(f"Failed: {len(test_predictors) - passed_count}")
    
    if passed_count == len(test_predictors):
        print("🎉 ALL TESTS PASSED!")
        sys.exit(0)
    else:
        print("❌ SOME TESTS FAILED")
        sys.exit(1)

if __name__ == "__main__":
    main()