# ABOUTME: test_predictors_polars.py - polars-optimized version of test_predictors.py for faster validation
# ABOUTME: Precision validation script using polars for 5-100x performance improvement while maintaining exact output

"""
test_predictors_polars.py

Usage:
    cd pyCode/
    source .venv/bin/activate
    python3 utils/test_predictors_polars.py                    # Test all predictors
    python3 utils/test_predictors_polars.py --predictors Accruals  # Test specific predictor

Precision Validation (per CLAUDE.md:290-304):
1. Columns: Column names and order match exactly
2. Superset: Python observations are a superset of Stata observations
3. Precision1: For common observations, percentage with diff >= TOL_DIFF_1 < TOL_OBS_1
4. Precision2: For common observations, Pth percentile absolute difference < TOL_DIFF_2
   - common observations are observations that are in both Stata and Python

Inputs:
    - Stata CSV files in ../Data/Predictors/
    - Python CSV files in ../pyData/Predictors/

Outputs:
    - Console validation results with ✅/❌ symbols
    - Validation log saved to ../Logs/testout_predictors.md
    - Feedback showing worst observations and differences

Performance Optimizations:
    - Uses polars for 5-100x faster CSV loading and operations
    - Replaces Python set operations with optimized polars joins
    - Vectorized difference calculations for better performance
    - Maintains exact output compatibility with pandas version
"""

import polars as pl
import pandas as pd
import argparse
from pathlib import Path
from datetime import datetime
import sys

# ================================
# VALIDATION CONFIGURATION
# ================================

PTH_PERCENTILE = 1.00  # 100th percentile (maximum)
TOL_DIFF_1 = 1e-4  # Threshold for identifying imperfect observations (Precision1)
TOL_OBS_1 = 0.1  # Max allowed percentage of imperfect observations (units: percent)
TOL_DIFF_2 = 1e-6  # Tolerance for Pth percentile absolute difference (Precision2)
INDEX_COLS = ['permno', 'yyyymm']  # Index columns for observations

def load_csv_robust_polars(file_path):
    """Load CSV file with polars for performance, robust error handling"""
    try:
        df = pl.read_csv(file_path)
        return df
    except Exception as e:
        print(f"Error loading {file_path}: {e}")
        return None

def validate_precision_requirements(stata_df, python_df, predictor_name):
    """
    Perform precision validation following CLAUDE.md requirements using polars
    Returns (passed, results_dict)
    """
    results = {}
    
    # Initialize all required keys with default values
    results['stata_obs_count'] = 0
    results['python_obs_count'] = 0
    results['common_obs_count'] = 0
    
    # Initialize test results
    cols_match = True
    is_superset = True
    
    # Check if required index columns exist
    stata_cols = stata_df.columns
    python_cols = python_df.columns
    
    for col in INDEX_COLS:
        if col not in stata_cols or col not in python_cols:
            print(f"  ❌ Missing index columns: {col}")
            results['error'] = f'Missing index columns: {col}'
            return False, results
    
    # 1. Column names and order match exactly
    # Get data columns (excluding index columns)
    stata_data_cols = [col for col in stata_cols if col not in INDEX_COLS]
    python_data_cols = [col for col in python_cols if col not in INDEX_COLS]
    
    cols_match = stata_data_cols == python_data_cols
    results['columns_match'] = cols_match
    results['stata_columns'] = stata_data_cols
    results['python_columns'] = python_data_cols
    
    # 2. Python observations are superset of Stata observations
    # Use polars for efficient join-based superset check
    stata_indexed = stata_df.select(INDEX_COLS).unique()
    python_indexed = python_df.select(INDEX_COLS).unique()
    
    results['stata_obs_count'] = stata_indexed.height
    results['python_obs_count'] = python_indexed.height
    
    # Find missing observations using anti-join (more efficient than set operations)
    missing_obs_df = stata_indexed.join(python_indexed, on=INDEX_COLS, how="anti")
    missing_count = missing_obs_df.height
    
    is_superset = missing_count == 0
    results['is_superset'] = is_superset
    
    if not is_superset:
        results['missing_count'] = missing_count
        
        # Get sample of missing observations with all columns for feedback
        missing_with_data = stata_df.join(missing_obs_df, on=INDEX_COLS, how="inner")
        missing_sample = missing_with_data.sort(INDEX_COLS).head(10)
        
        # Convert to pandas and add index column for exact output format compatibility
        missing_sample_pd = missing_sample.to_pandas().reset_index()
        results['missing_observations_sample'] = missing_sample_pd
    
    # 3. Find common observations using inner join (more efficient than intersection)
    common_obs_df = stata_indexed.join(python_indexed, on=INDEX_COLS, how="inner")
    results['common_obs_count'] = common_obs_df.height
    
    precision1_ok = True
    precision2_ok = True
    
    if results['common_obs_count'] == 0:
        precision1_ok = False
        precision2_ok = False
    else:
        # Get common observations data using joins
        cobs_stata = stata_df.join(common_obs_df, on=INDEX_COLS, how="inner")
        cobs_python = python_df.join(common_obs_df, on=INDEX_COLS, how="inner")
        
        # Sort both by index columns to ensure same order
        cobs_stata = cobs_stata.sort(INDEX_COLS)
        cobs_python = cobs_python.sort(INDEX_COLS)
        
        # Join and calculate differences
        cobs_diff = cobs_python.join(
            cobs_stata.select(INDEX_COLS + [predictor_name]), 
            on=INDEX_COLS, 
            how="inner"
        ).with_columns([
            (pl.col(predictor_name) - pl.col(predictor_name + "_right")).alias("diff")
        ]).with_columns([
            pl.col("diff").abs().alias("abs_diff")
        ])
        
        # Test 3: Precision1 - percentage of observations with abs_diff >= TOL_DIFF_1
        bad_obs_count = cobs_diff.filter(pl.col("abs_diff") >= TOL_DIFF_1).height
        total_obs_count = cobs_diff.height
        bad_obs_percentage = (bad_obs_count / total_obs_count) * 100
        
        precision1_ok = bad_obs_percentage < TOL_OBS_1
        results['precision1_ok'] = precision1_ok
        results['bad_obs_count'] = bad_obs_count
        results['total_obs_count'] = total_obs_count
        results['bad_obs_percentage'] = bad_obs_percentage
        
        # Test 4: Precision2 - Pth percentile absolute difference < TOL_DIFF_2
        pth_percentile_diff = cobs_diff.select(pl.col("abs_diff").quantile(PTH_PERCENTILE)).item()
        
        precision2_ok = pth_percentile_diff < TOL_DIFF_2
        results['pth_percentile_diff'] = pth_percentile_diff
        results['precision2_ok'] = precision2_ok
        
        # Generate feedback for failed precision tests
        if not precision1_ok or not precision2_ok:
            # Find observations with differences >= TOL_DIFF_1 for detailed feedback
            bad_obs_df = cobs_diff.filter(pl.col("abs_diff") >= TOL_DIFF_1)
            
            if bad_obs_df.height > 0:
                # Create feedback dataframes with proper column names for output compatibility
                feedback_df = bad_obs_df.select([
                    *INDEX_COLS,
                    pl.col(predictor_name).alias("python"),
                    pl.col(predictor_name + "_right").alias("stata"),
                    pl.col("diff")
                ])
                
                # Most recent observations that exceed tolerance (sorted by yyyymm descending)
                recent_bad = feedback_df.sort("yyyymm", descending=True).head(10)
                results['recent_bad'] = recent_bad.to_pandas()
                
                # Observations with largest differences (sorted by absolute diff descending)
                largest_diff = feedback_df.with_columns(pl.col("diff").abs().alias("abs_diff_sort")).sort("abs_diff_sort", descending=True).drop("abs_diff_sort").head(10)
                results['largest_diff'] = largest_diff.to_pandas()
    
    # Store individual test results
    results['test_1_passed'] = cols_match
    results['test_2_passed'] = is_superset
    results['test_3_passed'] = precision1_ok
    results['test_4_passed'] = precision2_ok
    
    return cols_match and is_superset and precision1_ok and precision2_ok, results

def output_predictor_results(predictor_name, results, overall_passed):
    """
    Output predictor results to both console and return markdown lines
    """
    # Print to console
    print(f"\n=== Validating {predictor_name} ===")
    print(f"  Loaded Stata: {results.get('stata_obs_count', 0)} rows, Python: {results.get('python_obs_count', 0)} rows")
    
    # Handle error case
    if 'error' in results:
        print(f"  ❌ Error: {results['error']}")
        return [
            f"### {predictor_name}\n",
            f"**Status**: ❌ FAILED\n",
            f"**Error**: {results['error']}\n",
            "---\n"
        ]
    
    # Test 1: Column names
    if results.get('test_1_passed', False):
        print(f"  ✅ Test 1 - Column names: PASSED")
    else:
        print(f"  ❌ Test 1 - Column names: FAILED")
        print(f"    Stata:  {results.get('stata_columns', [])}")
        print(f"    Python: {results.get('python_columns', [])}")
    
    # Test 2: Superset check
    if results.get('test_2_passed', False):
        print(f"  ✅ Test 2 - Superset check: PASSED (Stata={results.get('stata_obs_count', 0)}, Python={results.get('python_obs_count', 0)})")
    else:
        missing_count = results.get('missing_count', 0)
        print(f"  ❌ Test 2 - Superset check: FAILED (Python missing {missing_count} Stata observations)")
        
        # Show sample of missing observations
        if 'missing_observations_sample' in results:
            print(f"  Sample of missing observations:")
            sample_df = results['missing_observations_sample']
            print(f"  {sample_df.to_string(index=False)}")
    
    # Test 3: Precision1 check
    if results.get('common_obs_count', 0) == 0:
        print(f"  ❌ Test 3 - Precision1 check: FAILED (No common observations found)")
    elif results.get('test_3_passed', False):
        bad_pct = results.get('bad_obs_percentage', 0)
        print(f"  ✅ Test 3 - Precision1 check: PASSED ({bad_pct:.3f}% obs with diff >= {TOL_DIFF_1:.2e} < {TOL_OBS_1}%)")
    else:
        bad_pct = results.get('bad_obs_percentage', 0)
        print(f"  ❌ Test 3 - Precision1 check: FAILED ({bad_pct:.3f}% obs with diff >= {TOL_DIFF_1:.2e} >= {TOL_OBS_1}%)")
    
    # Test 4: Precision2 check
    if results.get('common_obs_count', 0) == 0:
        print(f"  ❌ Test 4 - Precision2 check: FAILED (No common observations found)")
    elif results.get('test_4_passed', False):
        pth_diff = results.get('pth_percentile_diff', 0)
        print(f"  ✅ Test 4 - Precision2 check: PASSED ({PTH_PERCENTILE*100:.0f}th percentile diff = {pth_diff:.2e} < {TOL_DIFF_2:.2e})")
    else:
        pth_diff = results.get('pth_percentile_diff', 0)
        print(f"  ❌ Test 4 - Precision2 check: FAILED ({PTH_PERCENTILE*100:.0f}th percentile diff = {pth_diff:.2e} >= {TOL_DIFF_2:.2e})")
    
    # Overall result
    if overall_passed:
        print(f"  ✅ {predictor_name} PASSED")
    else:
        print(f"  ❌ {predictor_name} FAILED")
        # Print feedback for failed predictors
        if 'bad_obs_count' in results:
            print(f"    Bad observations: {results['bad_obs_count']}/{results['total_obs_count']} ({results['bad_obs_percentage']:.3f}%)")
    
    # Generate markdown lines
    md_lines = []
    md_lines.append(f"### {predictor_name}\n\n")
    
    if overall_passed:
        md_lines.append("**Status**: ✅ PASSED\n\n")
    else:
        md_lines.append("**Status**: ❌ FAILED\n\n")
    
    # Test Results section
    md_lines.append("**Test Results**:\n")
    test1_status = "✅ PASSED" if results.get('test_1_passed', False) else "❌ FAILED"
    test2_status = "✅ PASSED" if results.get('test_2_passed', False) else "❌ FAILED"
    test3_status = "✅ PASSED" if results.get('test_3_passed', False) else "❌ FAILED"
    test4_status = "✅ PASSED" if results.get('test_4_passed', False) else "❌ FAILED"
    
    md_lines.append(f"- Test 1 - Column names: {test1_status}\n")
    
    # Add missing count information for Test 2
    if results.get('test_2_passed', False):
        md_lines.append(f"- Test 2 - Superset check: {test2_status}\n")
    else:
        missing_count = results.get('missing_count', 0)
        md_lines.append(f"- Test 2 - Superset check: {test2_status} (Python missing {missing_count} Stata observations)\n")
    
    md_lines.append(f"- Test 3 - Precision1 check: {test3_status}\n")
    md_lines.append(f"- Test 4 - Precision2 check: {test4_status}\n\n")
    
    # Basic info
    md_lines.append(f"**Columns**: {results.get('stata_columns', 'N/A')}\n\n")
    md_lines.append("**Observations**:\n")
    md_lines.append(f"- Stata:  {results.get('stata_obs_count', 0):,}\n")
    md_lines.append(f"- Python: {results.get('python_obs_count', 0):,}\n")
    md_lines.append(f"- Common: {results.get('common_obs_count', 0):,}\n\n")
    
    # Precision results
    if 'bad_obs_percentage' in results:
        md_lines.append(f"**Precision1**: {results['bad_obs_percentage']:.3f}% obs with diff >= {TOL_DIFF_1:.2e} (tolerance: < {TOL_OBS_1}%)\n\n")
    
    if 'pth_percentile_diff' in results:
        md_lines.append(f"**Precision2**: {PTH_PERCENTILE*100:.0f}th percentile diff = {results['pth_percentile_diff']:.2e} (tolerance: < {TOL_DIFF_2:.2e})\n\n")
    
    # Feedback for failed superset test
    if not results.get('test_2_passed', True) and 'missing_observations_sample' in results:
        md_lines.append("**Missing Observations Sample**:\n")
        missing_sample = results['missing_observations_sample']
        md_lines.append(f"```\n{missing_sample.to_string(index=False)}\n```\n\n")
    
    # Feedback for failed precision
    if 'bad_obs_count' in results:
        md_lines.append("**Feedback**:\n")
        md_lines.append(f"- Num observations with diff >= TOL_DIFF_1: {results['bad_obs_count']}/{results['total_obs_count']} ({results['bad_obs_percentage']:.3f}%)\n\n")
        
        if 'recent_bad' in results and len(results['recent_bad']) > 0:
            md_lines.append("**Most Recent Bad Observations**:\n")
            md_lines.append(f"```\n{results['recent_bad'].to_string()}\n```\n\n")
        
        if 'largest_diff' in results and len(results['largest_diff']) > 0:
            md_lines.append("**Largest Differences**:\n")
            md_lines.append(f"```\n{results['largest_diff'].to_string()}\n```\n\n")
    
    md_lines.append("---\n\n")
    
    return md_lines

def validate_predictor(predictor_name):
    """Validate a single predictor against Stata output using polars optimization"""
    
    # Load Stata CSV with polars
    stata_path = Path(f"../Data/Predictors/{predictor_name}.csv")
    if not stata_path.exists():
        results = {'error': f'Stata file not found: {stata_path}'}
        md_lines = output_predictor_results(predictor_name, results, False)
        return False, results, md_lines
    
    stata_df = load_csv_robust_polars(stata_path)
    if stata_df is None:
        results = {'error': f'Failed to load Stata file: {stata_path}'}
        md_lines = output_predictor_results(predictor_name, results, False)
        return False, results, md_lines
    
    # Load Python CSV with polars
    python_path = Path(f"../pyData/Predictors/{predictor_name}.csv") 
    if not python_path.exists():
        results = {'error': f'Python file not found: {python_path}'}
        md_lines = output_predictor_results(predictor_name, results, False)
        return False, results, md_lines
    
    python_df = load_csv_robust_polars(python_path)
    if python_df is None:
        results = {'error': f'Failed to load Python file: {python_path}'}
        md_lines = output_predictor_results(predictor_name, results, False)
        return False, results, md_lines
    
    # Perform precision validation
    passed, results = validate_precision_requirements(stata_df, python_df, predictor_name)
    
    # Generate unified output
    md_lines = output_predictor_results(predictor_name, results, passed)
    
    return passed, results, md_lines

def get_available_predictors():
    """Get list of available predictor files and missing Python CSVs"""
    stata_dir = Path("../Data/Predictors/")
    python_dir = Path("../pyData/Predictors/")
    
    stata_files = set()
    python_files = set()
    
    if stata_dir.exists():
        stata_files = {f.stem for f in stata_dir.glob("*.csv")}
    
    if python_dir.exists():
        python_files = {f.stem for f in python_dir.glob("*.csv")}
    
    # Return intersection (available for validation) and missing Python CSVs
    available_predictors = sorted(list(stata_files.intersection(python_files)))
    missing_python_csvs = sorted(list(stata_files - python_files))
    
    return available_predictors, missing_python_csvs

def write_markdown_log(all_md_lines, test_predictors, passed_count, all_results):
    """Write detailed results to markdown log file"""
    log_path = Path("../Logs/testout_predictors.md")
    
    with open(log_path, 'w') as f:
        f.write(f"# Predictor Validation Results\n\n")
        f.write(f"**Generated**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
        f.write(f"**Configuration**:\n")
        f.write(f"- PTH_PERCENTILE: {PTH_PERCENTILE}\n")
        f.write(f"- TOL_DIFF_1: {TOL_DIFF_1}\n")
        f.write(f"- TOL_OBS_1: {TOL_OBS_1}%\n")
        f.write(f"- TOL_DIFF_2: {TOL_DIFF_2}\n")
        f.write(f"- INDEX_COLS: {INDEX_COLS}\n\n")
        
        f.write(f"## Summary\n\n")
        
        # Create summary table with Python CSV column
        f.write("| Predictor                 | Python CSV | Columns  | Superset  | Precision1   | Precision2              |\n")
        f.write("|---------------------------|------------|----------|-----------|--------------|-------------------------|\n")
        
        for predictor in test_predictors:
            results = all_results.get(predictor, {})
            
            # Get Python CSV availability
            python_csv_available = results.get('python_csv_available', False)
            csv_status = "✅" if python_csv_available else "❌"
            
            # Get test results with fallback
            test1 = results.get('test_1_passed', None)
            test2 = results.get('test_2_passed', None) 
            test3 = results.get('test_3_passed', None)
            test4 = results.get('test_4_passed', None)
            
            # Format symbols (emojis for pass/fail, NA for None)
            col1 = "✅" if test1 == True else ("❌" if test1 == False else "NA")
            
            # Format superset column with failure percentage
            if test2 == True:
                col2 = "✅"
            elif test2 == False:
                # Include failure percentage when superset test fails
                missing_count = results.get('missing_count', 0)
                stata_obs_count = results.get('stata_obs_count', 0)
                if stata_obs_count > 0:
                    failure_pct = (missing_count / stata_obs_count) * 100
                    col2 = f"❌ ({failure_pct:.2f}%)"
                else:
                    col2 = "❌"
            else:
                col2 = "NA"
            
            # Format precision1 column with percentage information
            if test3 == True:
                bad_pct = results.get('bad_obs_percentage', 0)
                col3 = f"✅ ({bad_pct:.2f}%)"
            elif test3 == False:
                bad_pct = results.get('bad_obs_percentage', 0)
                col3 = f"❌ ({bad_pct:.2f}%)"
            else:
                col3 = "NA"
            # Format precision2 column with diff value information  
            if test4 == True:
                pth_diff = results.get('pth_percentile_diff', 0)
                col4 = f"✅ (100th diff {pth_diff:.1E})"
            elif test4 == False:
                pth_diff = results.get('pth_percentile_diff', 0)
                col4 = f"❌ (100th diff {pth_diff:.1E})"
            else:
                col4 = "NA"
            
            f.write(f"| {predictor:<25} | {csv_status:<9} | {col1:<7} | {col2:<11} | {col3:<12} | {col4:<23} |\n")
        
        # Count available predictors for summary
        available_count = sum(1 for p in test_predictors if all_results.get(p, {}).get('python_csv_available', False))
        
        f.write(f"\n**Overall**: {passed_count}/{available_count} available predictors passed validation\n")
        f.write(f"**Python CSVs**: {available_count}/{len(test_predictors)} predictors have Python implementation\n\n")
        
        f.write(f"## Detailed Results\n\n")
        
        # Write all the pre-formatted markdown lines
        for lines in all_md_lines:
            f.writelines(lines)
    
    print(f"\nDetailed results written to: {log_path}")

def main():
    parser = argparse.ArgumentParser(description='Validate Python predictor outputs against Stata CSV files using polars optimization')
    parser.add_argument('--predictors', '-p', nargs='+', help='Specific predictors to validate')
    parser.add_argument('--list', '-l', action='store_true', help='List available predictors and exit')
    
    args = parser.parse_args()
    
    available_predictors, missing_python_csvs = get_available_predictors()
    
    if args.list:
        print("Available predictors (have both Stata and Python CSV):")
        for pred in available_predictors:
            print(f"  {pred}")
        print("\nMissing Python CSVs (have Stata but no Python CSV):")
        for pred in missing_python_csvs:
            print(f"  {pred}")
        return
    
    # Select predictors to test
    if args.predictors:
        # Split requested predictors into available and missing
        requested_set = set(args.predictors)
        available_to_test = [p for p in available_predictors if p in requested_set]
        missing_to_include = [p for p in missing_python_csvs if p in requested_set]
        
        # Check for completely unknown predictors
        all_known = set(available_predictors + missing_python_csvs)
        unknown = requested_set - all_known
        if unknown:
            print(f"Warning: These predictors not found in Stata data: {unknown}")
        
        test_predictors = available_to_test
        include_missing = missing_to_include
    else:
        test_predictors = available_predictors
        include_missing = missing_python_csvs
    
    if not test_predictors and not include_missing:
        print("No predictors to test")
        return
    
    print(f"Validating {len(test_predictors)} predictors: {test_predictors}")
    if include_missing:
        print(f"Including {len(include_missing)} missing Python CSVs in summary: {include_missing}")
    
    # Validate each available predictor
    all_md_lines = []
    all_results = {}
    passed_count = 0
    
    for predictor in test_predictors:
        passed, results, md_lines = validate_predictor(predictor)
        results['python_csv_available'] = True
        all_md_lines.append(md_lines)
        all_results[predictor] = results
        if passed:
            passed_count += 1
    
    # Add dummy results for missing Python CSVs
    for predictor in include_missing:
        print(f"\n=== {predictor} ===")
        print(f"  ❌ Python CSV missing: ../pyData/Predictors/{predictor}.csv")
        
        # Create dummy results for missing Python CSV
        dummy_results = {
            'python_csv_available': False,
            'test_1_passed': None,
            'test_2_passed': None, 
            'test_3_passed': None,
            'test_4_passed': None,
            'error': 'Python CSV file not found'
        }
        all_results[predictor] = dummy_results
        
        # Create minimal markdown for missing predictors
        md_lines = [
            f"### {predictor}\n\n",
            "**Status**: ❌ MISSING PYTHON CSV\n\n",
            f"**Error**: Python CSV file not found: ../pyData/Predictors/{predictor}.csv\n\n",
            "---\n\n"
        ]
        all_md_lines.append(md_lines)
    
    # Combine all predictors for summary
    all_predictors = test_predictors + include_missing
    
    # Write markdown log
    write_markdown_log(all_md_lines, all_predictors, passed_count, all_results)
    
    # Summary
    print(f"\n=== SUMMARY ===")
    print(f"Available predictors tested: {len(test_predictors)}")
    print(f"Missing Python CSVs included: {len(include_missing)}")
    print(f"Passed validation: {passed_count}")
    print(f"Failed validation: {len(test_predictors) - passed_count}")
    
    if passed_count == len(test_predictors):
        print("🎉 ALL AVAILABLE TESTS PASSED!")
        sys.exit(0)
    else:
        print("❌ SOME TESTS FAILED")
        sys.exit(1)

if __name__ == "__main__":
    main()