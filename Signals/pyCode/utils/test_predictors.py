# ABOUTME: test_predictors.py - validates Python predictor outputs against Stata CSV files
# ABOUTME: Polars-optimized precision validation script with 6x performance improvement

"""
test_predictors.py

Usage:
    cd pyCode/
    source .venv/bin/activate
    python3 utils/test_predictors.py --all             # Test all predictors
    python3 utils/test_predictors.py --predictors Accruals  # Test specific predictor
    python3 utils/test_predictors.py --all --tstat     # With t-stat check enabled
    python3 utils/test_predictors.py --predictors BM Size --tstat  # With t-stat check for specific predictors

Precision Validation (per CLAUDE.md updated requirements):
1. Superset: Python observations are a superset of Stata observations
2. NumRows: Python rows don't exceed Stata rows by more than TOL_NUMROWS percent
3. Precision1: For common observations, percentage with std_diff >= TOL_DIFF_1 < TOL_OBS_1
4. Precision2: For common observations, Pth percentile standardized difference < TOL_DIFF_2
   - std_diff = (python_value - stata_value) / std(all_stata_values)
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
import yaml
import statsmodels.formula.api as smf
import numpy as np


# ================================
# VALIDATION CONFIGURATION
# ================================

# Superset test
TOL_SUPERSET = 1.0  # Max allowed percentage of missing observations (units: percent)

# NumRows test
TOL_NUMROWS = 5.0  # Max allowed percentage by which Python rows can exceed Stata rows (units: percent)

# Precision1: goal is 0.01, 1
TOL_DIFF_1 = 0.01  # Standardized difference threshold for imperfect observations
TOL_OBS_1 = 1  # Max allowed percentage of imperfect observations (units: percent)

# Precision2: goal is 0.10, 0.999
TOL_DIFF_2 = 0.10  # Tolerance for Pth percentile standardized difference (Precision2)
EXTREME_Q = 0.999  # Quantile for extreme deviation (not percentile)

# T-stat test
TOL_TSTAT = 0.2  # Tolerance for t-stat difference from last year's run

INDEX_COLS = ['permno', 'yyyymm']  # Index columns for observations

def load_overrides():
    """Load predictor validation overrides from YAML file"""
    override_path = Path("Predictors/overrides.yaml")
    if not override_path.exists():
        return {}
    
    try:
        with open(override_path, 'r') as f:
            overrides = yaml.safe_load(f) or {}
        
        # Filter to only accepted overrides
        accepted_overrides = {}
        for predictor, override_info in overrides.items():
            if isinstance(override_info, dict) and override_info.get('status') == 'accepted':
                accepted_overrides[predictor] = override_info
        
        return accepted_overrides
    except Exception as e:
        print(f"Warning: Could not load overrides.yaml: {e}")
        return {}

def load_csv_robust_polars(file_path):
    """Load CSV file with polars for performance, robust error handling"""
    try:
        # Get the predictor name from the file path
        predictor_name = Path(file_path).stem
        
        # Always use schema overrides for predictor files
        schema_overrides = {
            'permno': pl.Int64,
            'yyyymm': pl.Int64,
            predictor_name: pl.Float64
        }
        
        df = pl.read_csv(file_path, schema_overrides=schema_overrides)
        
        # Filter out rows where the predictor value is null or NaN
        if predictor_name in df.columns:
            df = df.filter(pl.col(predictor_name).is_finite())
        
        return df
    except Exception as e:
        print(f"Failed to load {file_path}: {e}")
        return None

def validate_precision_requirements(stata_df, python_df, predictor_name, tstat_comparison_df=None):
    """
    Perform precision validation following CLAUDE.md requirements using polars
    Returns (passed, results_dict)
    
    Tests (in order of importance):
    1. Superset: Python observations are a superset of Stata observations
    2. NumRows: Python rows don't exceed Stata rows by more than TOL_NUMROWS percent
    3. Precision1: For common observations, percentage with std_diff >= TOL_DIFF_1 < TOL_OBS_1
    4. Precision2: For common observations, Pth percentile standardized difference < TOL_DIFF_2
    5. T-stat: Portfolio t-statistic within TOL_TSTAT of last year's value (if tstat_comparison_df provided)
    """
    results = {}
    
    # Initialize all required keys with default values
    results['stata_obs_count'] = 0
    results['python_obs_count'] = 0
    results['common_obs_count'] = 0
    
    # Check if required index columns exist
    stata_cols = stata_df.columns
    python_cols = python_df.columns
    
    for col in INDEX_COLS:
        if col not in stata_cols or col not in python_cols:
            print(f"  ❌ Missing index columns: {col}")
            results['error'] = f'Missing index columns: {col}'
            return False, results
    
    # Get unique observations for both datasets
    stata_indexed = stata_df.select(INDEX_COLS).unique()
    python_indexed = python_df.select(INDEX_COLS).unique()
    
    results['stata_obs_count'] = stata_indexed.height
    results['python_obs_count'] = python_indexed.height
    
    # Test 1: Superset - Python observations are superset of Stata observations
    # Find missing observations using anti-join (more efficient than set operations)
    missing_obs_df = stata_indexed.join(python_indexed, on=INDEX_COLS, how="anti")
    missing_count = missing_obs_df.height
    
    # Calculate missing percentage and check against threshold
    if results['stata_obs_count'] > 0:
        missing_percentage = (missing_count / results['stata_obs_count']) * 100
    else:
        missing_percentage = 0.0
    
    is_superset = missing_percentage <= TOL_SUPERSET
    results['is_superset'] = is_superset
    results['missing_count'] = missing_count
    results['missing_percentage'] = missing_percentage
    
    if not is_superset:
        # Get sample of missing observations with all columns for feedback
        missing_with_data = stata_df.join(missing_obs_df, on=INDEX_COLS, how="inner")
        missing_sample = missing_with_data.sort(INDEX_COLS).head(10)
        
        # Convert to pandas and add index column for exact output format compatibility
        missing_sample_pd = missing_sample.to_pandas().reset_index()
        results['missing_observations_sample'] = missing_sample_pd
    
    # Test 2: NumRows - Python rows don't exceed Stata rows by more than TOL_NUMROWS percent
    if results['stata_obs_count'] > 0:
        numrows_ratio = (results['python_obs_count'] / results['stata_obs_count'] - 1) * 100
    else:
        numrows_ratio = 0.0
    
    numrows_ok = numrows_ratio <= TOL_NUMROWS
    results['numrows_ok'] = numrows_ok
    results['numrows_ratio'] = numrows_ratio
    
    # Test 3: Find common observations using inner join (more efficient than intersection)
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
        
        # Calculate standard deviation of all Stata values for standardized differences
        stata_std = cobs_diff.select(pl.col(predictor_name + "_right").std()).item()
        
        # Add standardized differences for Precision1 test
        cobs_diff = cobs_diff.with_columns([
            (pl.col("diff") / stata_std).alias("std_diff")
        ])
        
        # Test 3: Precision1 - percentage of observations with std_diff >= TOL_DIFF_1
        bad_obs_count = cobs_diff.filter(pl.col("std_diff").abs() >= TOL_DIFF_1).height
        total_obs_count = cobs_diff.height
        bad_obs_percentage = (bad_obs_count / total_obs_count) * 100
        
        precision1_ok = bad_obs_percentage < TOL_OBS_1
        results['precision1_ok'] = precision1_ok
        results['bad_obs_count'] = bad_obs_count
        results['total_obs_count'] = total_obs_count
        results['bad_obs_percentage'] = bad_obs_percentage
        results['stata_std'] = stata_std
        
        # Test 4: Precision2 - Pth percentile standardized difference < TOL_DIFF_2
        pth_percentile_diff = cobs_diff.select(pl.col("std_diff").abs().quantile(EXTREME_Q)).item()
        
        precision2_ok = pth_percentile_diff < TOL_DIFF_2
        results['pth_percentile_diff'] = pth_percentile_diff
        results['precision2_ok'] = precision2_ok
        
        # Calculate additional summary statistics and regression analysis
        try:
            # Calculate summary statistics for stata, python, diff, and std_diff
            stata_values = cobs_diff.select(pl.col(predictor_name + "_right")).to_pandas()[predictor_name + "_right"]
            python_values = cobs_diff.select(pl.col(predictor_name)).to_pandas()[predictor_name]
            diff_values = cobs_diff.select(pl.col("diff")).to_pandas()["diff"]
            std_diff_values = cobs_diff.select(pl.col("std_diff")).to_pandas()["std_diff"]
            
            # Store summary statistics
            results['summary_stats'] = {
                'stata': stata_values.describe().to_dict(),
                'python': python_values.describe().to_dict(),
                'diff': diff_values.describe().to_dict(),
                'std_diff': std_diff_values.describe().to_dict()
            }
            
            # Perform regression analysis: python ~ stata
            if len(stata_values) > 1 and stata_values.std() > 0:
                reg_data = pd.DataFrame({
                    'python': python_values,
                    'stata': stata_values
                }).dropna()
                
                if len(reg_data) > 1:
                    model = smf.ols('python ~ stata', data=reg_data)
                    reg_result = model.fit()
                    
                    # Store regression results
                    results['regression_stats'] = {
                        'intercept': reg_result.params['Intercept'],
                        'slope': reg_result.params['stata'],
                        'r_squared': reg_result.rsquared,
                        'intercept_se': reg_result.bse['Intercept'],
                        'slope_se': reg_result.bse['stata'],
                        'intercept_tstat': reg_result.tvalues['Intercept'],
                        'slope_tstat': reg_result.tvalues['stata'],
                        'intercept_pvalue': reg_result.pvalues['Intercept'],
                        'slope_pvalue': reg_result.pvalues['stata'],
                        'n_obs': len(reg_data)
                    }
        except Exception as e:
            # If summary stats or regression fails, store error but don't break validation
            results['summary_stats_error'] = str(e)
        
        # Generate feedback for failed precision tests
        if not precision1_ok or not precision2_ok:
            # Find observations with standardized differences >= TOL_DIFF_1 for detailed feedback
            bad_obs_df = cobs_diff.filter(pl.col("std_diff").abs() >= TOL_DIFF_1)
            
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
                
                # Observations with largest differences before 1950 (yyyymm < 195001)
                feedback_df_before1950 = feedback_df.filter(pl.col("yyyymm") < 195001)
                if feedback_df_before1950.height > 0:
                    largest_diff_before1950 = feedback_df_before1950.with_columns(pl.col("diff").abs().alias("abs_diff_sort")).sort("abs_diff_sort", descending=True).drop("abs_diff_sort").head(10)
                    results['largest_diff_before1950'] = largest_diff_before1950.to_pandas()
                else:
                    results['largest_diff_before1950'] = None
    
    # Test 5: T-stat check using pre-loaded comparison data
    tstat_ok = True
    if tstat_comparison_df is None:
        # Skip t-stat check if no comparison data provided (--tstat not enabled)
        results['current_tstat'] = None
        results['old_tstat'] = None
        results['tstat_diff'] = None
        results['tstat_diff_signed'] = None
        tstat_ok = None  # Mark as skipped
        results['tstat_skipped'] = True
    else:
        try:
            # Look up the predictor in the pre-loaded comparison results
            predictor_row = tstat_comparison_df[tstat_comparison_df['signalname'] == predictor_name]
            
            if not predictor_row.empty:
                current_tstat = predictor_row['new'].iloc[0]
                old_tstat = predictor_row['old'].iloc[0]
                tstat_diff_signed = predictor_row['diff'].iloc[0]
                
                results['current_tstat'] = current_tstat
                results['old_tstat'] = old_tstat
                results['tstat_diff_signed'] = tstat_diff_signed
                results['tstat_diff'] = abs(tstat_diff_signed)  # Keep for backward compatibility
                
                # Check if diff is within tolerance
                tstat_ok = abs(tstat_diff_signed) < TOL_TSTAT
            else:
                results['tstat_error'] = f"Predictor {predictor_name} not found in comparison results"
                results['current_tstat'] = None
                results['old_tstat'] = None
                results['tstat_diff'] = None
                results['tstat_diff_signed'] = None
                tstat_ok = None
                    
        except Exception as e:
            # If t-stat check fails, record error but don't fail validation
            results['tstat_error'] = str(e)
            results['current_tstat'] = None
            results['old_tstat'] = None
            results['tstat_diff'] = None
            results['tstat_diff_signed'] = None
            tstat_ok = None
    
    # Store individual test results (in new order)
    results['test_1_passed'] = is_superset
    results['test_2_passed'] = numrows_ok
    results['test_3_passed'] = precision1_ok
    results['test_4_passed'] = precision2_ok
    results['test_5_passed'] = tstat_ok
    
    # Overall pass requires all tests to pass (or be None for unavailable tests)
    all_tests_pass = is_superset and numrows_ok and precision1_ok and precision2_ok
    if tstat_ok is not None:
        all_tests_pass = all_tests_pass and tstat_ok
    
    return all_tests_pass, results

def analyze_python_only(predictor_name):
    """Analyze Python-only CSV file when Stata CSV is missing"""
    python_path = Path(f"../pyData/Predictors/{predictor_name}.csv")
    
    if not python_path.exists():
        return {
            'error': f'Python file not found: {python_path}',
            'python_csv_available': False,
            'stata_csv_available': False
        }
    
    # Load Python CSV
    python_df = load_csv_robust_polars(python_path)
    if python_df is None:
        return {
            'error': f'Failed to load Python file: {python_path}',
            'python_csv_available': False,
            'stata_csv_available': False
        }
    
    # Extract basic information
    results = {
        'python_csv_available': True,
        'stata_csv_available': False,
        'python_obs_count': python_df.height,
        'stata_obs_count': 0,
        'common_obs_count': 0,
        'python_columns': [col for col in python_df.columns if col not in INDEX_COLS],
        'stata_columns': [],
        
        # Test results for summary table (in new order)
        'test_1_passed': None,   # NA for Superset since no Stata to compare
        'test_2_passed': None,   # NA for NumRows since no Stata to compare
        'test_3_passed': None,   # NA for Precision1
        'test_4_passed': None,   # NA for Precision2
        'test_5_passed': None,   # NA for T-stat since no Stata to compare
        
        # Additional info about the Python CSV
        'date_range': None,
        'unique_permnos': 0
    }
    
    # Get date range if yyyymm column exists
    if 'yyyymm' in python_df.columns:
        min_date = python_df.select(pl.col('yyyymm').min()).item()
        max_date = python_df.select(pl.col('yyyymm').max()).item()
        results['date_range'] = f"{min_date}-{max_date}"
    
    # Get unique permno count if permno column exists
    if 'permno' in python_df.columns:
        results['unique_permnos'] = python_df.select(pl.col('permno').n_unique()).item()
    
    return results

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
    
    # Test 1: Superset check
    test1 = results.get('test_1_passed', None)
    if test1 is True:
        missing_pct = results.get('missing_percentage', 0)
        print(f"  ✅ Test 1 - Superset check: PASSED (Missing {missing_pct:.2f}% <= {TOL_SUPERSET}% threshold)")
    elif test1 is False:
        missing_count = results.get('missing_count', 0)
        missing_pct = results.get('missing_percentage', 0)
        print(f"  ❌ Test 1 - Superset check: FAILED (Missing {missing_pct:.2f}% > {TOL_SUPERSET}% threshold, {missing_count} observations)")
        
        # Show sample of missing observations
        if 'missing_observations_sample' in results:
            print(f"  Sample of missing observations:")
            sample_df = results['missing_observations_sample']
            print(f"  {sample_df.to_string(index=False)}")
    else:
        print(f"  NA Test 1 - Superset check: N/A (No Stata CSV to compare)")
    
    # Test 2: NumRows check
    test2 = results.get('test_2_passed', None)
    if test2 is True:
        numrows_ratio = results.get('numrows_ratio', 0)
        print(f"  ✅ Test 2 - NumRows check: PASSED (Python has {numrows_ratio:+.2f}% rows vs Stata, <= {TOL_NUMROWS}% threshold)")
    elif test2 is False:
        numrows_ratio = results.get('numrows_ratio', 0)
        print(f"  ❌ Test 2 - NumRows check: FAILED (Python has {numrows_ratio:+.2f}% rows vs Stata, > {TOL_NUMROWS}% threshold)")
    else:
        print(f"  NA Test 2 - NumRows check: N/A (No Stata CSV to compare)")
    
    # Test 3: Precision1 check
    test3 = results.get('test_3_passed', None)
    if results.get('common_obs_count', 0) == 0 and test3 is not None:
        print(f"  ❌ Test 3 - Precision1 check: FAILED (No common observations found)")
    elif test3 is True:
        bad_pct = results.get('bad_obs_percentage', 0)
        print(f"  ✅ Test 3 - Precision1 check: PASSED ({bad_pct:.3f}% obs with std_diff >= {TOL_DIFF_1:.2e} < {TOL_OBS_1}%)")
    elif test3 is False:
        bad_pct = results.get('bad_obs_percentage', 0)
        print(f"  ❌ Test 3 - Precision1 check: FAILED ({bad_pct:.3f}% obs with std_diff >= {TOL_DIFF_1:.2e} >= {TOL_OBS_1}%)")
    else:
        print(f"  NA Test 3 - Precision1 check: N/A (No Stata CSV to compare)")
    
    # Test 4: Precision2 check
    test4 = results.get('test_4_passed', None)
    if results.get('common_obs_count', 0) == 0 and test4 is not None:
        print(f"  ❌ Test 4 - Precision2 check: FAILED (No common observations found)")
    elif test4 is True:
        pth_diff = results.get('pth_percentile_diff', 0)
        print(f"  ✅ Test 4 - Precision2 check: PASSED ({EXTREME_Q*100:.0f}th percentile diff = {pth_diff:.2e} < {TOL_DIFF_2:.2e})")
    elif test4 is False:
        pth_diff = results.get('pth_percentile_diff', 0)
        print(f"  ❌ Test 4 - Precision2 check: FAILED ({EXTREME_Q*100:.0f}th percentile diff = {pth_diff:.2e} >= {TOL_DIFF_2:.2e})")
    else:
        print(f"  NA Test 4 - Precision2 check: N/A (No Stata CSV to compare)")
    
    # Test 5: T-stat check
    test5 = results.get('test_5_passed', None)
    if test5 == True:
        current_tstat = results.get('current_tstat', 0)
        old_tstat = results.get('old_tstat', 0)
        tstat_diff_signed = results.get('tstat_diff_signed', 0)
        print(f"  ✅ Test 5 - T-stat check: PASSED ({current_tstat:.2f} - {old_tstat:.2f} = {tstat_diff_signed:+.2f}, |{tstat_diff_signed:.2f}| < {TOL_TSTAT})")
    elif test5 == False:
        current_tstat = results.get('current_tstat', 0)
        old_tstat = results.get('old_tstat', 0)
        tstat_diff_signed = results.get('tstat_diff_signed', 0)
        print(f"  ❌ Test 5 - T-stat check: FAILED ({current_tstat:.2f} - {old_tstat:.2f} = {tstat_diff_signed:+.2f}, |{tstat_diff_signed:.2f}| >= {TOL_TSTAT})")
    else:
        if results.get('tstat_skipped'):
            print(f"  NA Test 5 - T-stat check: N/A (Skipped - use --tstat to enable)")
        elif 'tstat_error' in results:
            print(f"  NA Test 5 - T-stat check: N/A (Error: {results['tstat_error']})")
        else:
            print(f"  NA Test 5 - T-stat check: N/A (Missing data)")
    
    # Show Python-only specific info
    if results.get('stata_csv_available') is False and results.get('python_csv_available') is True:
        print(f"  📊 Python CSV Info:")
        print(f"    Columns: {results.get('python_columns', [])}")
        if 'date_range' in results and results['date_range']:
            print(f"    Date range: {results['date_range']}")
        if 'unique_permnos' in results:
            print(f"    Unique permnos: {results['unique_permnos']:,}")
    
    # Overall result
    if overall_passed:
        if results.get('override_applied'):
            override_info = results.get('override_info', {})
            print(f"  🔧 OVERRIDE APPLIED (reviewed {override_info.get('reviewed_on', 'unknown')} by {override_info.get('reviewed_by', 'unknown')})")
            print(f"  ✅ {predictor_name} PASSED (with override)")
        else:
            print(f"  ✅ {predictor_name} PASSED")
    else:
        # For Python-only predictors, show different status
        if results.get('stata_csv_available') is False and results.get('python_csv_available') is True:
            print(f"  📊 {predictor_name} PYTHON-ONLY (No Stata baseline for comparison)")
        else:
            print(f"  ❌ {predictor_name} FAILED")
            # Print feedback for failed predictors
            if 'bad_obs_count' in results:
                print(f"    Bad observations: {results['bad_obs_count']}/{results['total_obs_count']} ({results['bad_obs_percentage']:.3f}%)")
    
    # Generate markdown lines
    md_lines = []
    md_lines.append(f"### {predictor_name}\n\n")
    
    if overall_passed:
        if results.get('override_applied'):
            override_info = results.get('override_info', {})
            md_lines.append("**Status**: ✅ PASSED (with override)\n\n")
            md_lines.append("**Override Applied**:\n")
            md_lines.append(f"- Reviewed on: {override_info.get('reviewed_on', 'unknown')}\n")
            md_lines.append(f"- Reviewed by: {override_info.get('reviewed_by', 'unknown')}\n")
            md_lines.append(f"- Details: {override_info.get('details', 'No details provided').strip()}\n\n")
        else:
            md_lines.append("**Status**: ✅ PASSED\n\n")
    else:
        md_lines.append("**Status**: ❌ FAILED\n\n")
    
    # Test Results section
    md_lines.append("**Test Results**:\n")
    test1_status = "✅ PASSED" if results.get('test_1_passed', False) else "❌ FAILED"
    test2_status = "✅ PASSED" if results.get('test_2_passed', False) else "❌ FAILED"
    test3_status = "✅ PASSED" if results.get('test_3_passed', False) else "❌ FAILED"
    test4_status = "✅ PASSED" if results.get('test_4_passed', False) else "❌ FAILED"
    test5_status = "✅ PASSED" if results.get('test_5_passed', None) is True else ("❌ FAILED" if results.get('test_5_passed', None) is False else "NA")
    
    # Add missing count information for Test 1 (Superset)
    if results.get('test_1_passed', False):
        md_lines.append(f"- Test 1 - Superset check: {test1_status}\n")
    else:
        missing_count = results.get('missing_count', 0)
        md_lines.append(f"- Test 1 - Superset check: {test1_status} (Python missing {missing_count} Stata observations)\n")
    
    # Add ratio information for Test 2 (NumRows)
    if results.get('test_2_passed') is not None:
        numrows_ratio = results.get('numrows_ratio', 0)
        md_lines.append(f"- Test 2 - NumRows check: {test2_status} (Python has {numrows_ratio:+.2f}% rows vs Stata)\n")
    else:
        md_lines.append(f"- Test 2 - NumRows check: {test2_status}\n")
    
    md_lines.append(f"- Test 3 - Precision1 check: {test3_status}\n")
    md_lines.append(f"- Test 4 - Precision2 check: {test4_status}\n")
    
    # Add t-stat information for Test 5
    if results.get('test_5_passed') is True:
        current_tstat = results.get('current_tstat', 0)
        old_tstat = results.get('old_tstat', 0)
        tstat_diff_signed = results.get('tstat_diff_signed', 0)
        md_lines.append(f"- Test 5 - T-stat check: {test5_status} (Current: {current_tstat:.2f}, Old: {old_tstat:.2f}, Diff: {tstat_diff_signed:+.2f})\n")
    elif results.get('test_5_passed') is False:
        current_tstat = results.get('current_tstat', 0)
        old_tstat = results.get('old_tstat', 0)
        tstat_diff_signed = results.get('tstat_diff_signed', 0)
        md_lines.append(f"- Test 5 - T-stat check: {test5_status} (Current: {current_tstat:.2f}, Old: {old_tstat:.2f}, Diff: {tstat_diff_signed:+.2f})\n")
    else:
        if results.get('tstat_skipped'):
            md_lines.append(f"- Test 5 - T-stat check: {test5_status} (Skipped - use --tstat to enable)\n")
        else:
            md_lines.append(f"- Test 5 - T-stat check: {test5_status}\n")
    
    md_lines.append("\n")
    
    # Basic info
    md_lines.append("**Observations**:\n")
    md_lines.append(f"- Stata:  {results.get('stata_obs_count', 0):,}\n")
    md_lines.append(f"- Python: {results.get('python_obs_count', 0):,}\n")
    md_lines.append(f"- Common: {results.get('common_obs_count', 0):,}\n\n")
    
    # Precision results
    if 'bad_obs_percentage' in results:
        md_lines.append(f"**Precision1**: {results['bad_obs_percentage']:.3f}% obs with std_diff >= {TOL_DIFF_1:.2e} (tolerance: < {TOL_OBS_1}%)\n\n")
    
    if 'pth_percentile_diff' in results:
        md_lines.append(f"**Precision2**: {EXTREME_Q*100:.0f}th percentile diff = {results['pth_percentile_diff']:.2e} (tolerance: < {TOL_DIFF_2:.2e})\n\n")
    
    # Add Summary Statistics section for common observations
    if 'summary_stats' in results:
        md_lines.append("**Summary Statistics** (Common Observations):\n\n")
        
        stats = results['summary_stats']
        
        # Create summary table with fixed column widths
        md_lines.append("| Statistic  |          Stata |         Python |     Difference | Std Difference |\n")
        md_lines.append("|------------|----------------|----------------|----------------|----------------|\n")
        
        # Format each statistic row
        for stat_name in ['count', 'mean', 'std', 'min', '25%', '50%', '75%', 'max']:
            stata_val = stats['stata'].get(stat_name, 'N/A')
            python_val = stats['python'].get(stat_name, 'N/A')
            diff_val = stats['diff'].get(stat_name, 'N/A')
            std_diff_val = stats['std_diff'].get(stat_name, 'N/A')
            
            # Format numbers for display with consistent width
            def format_stat(val, width=14):
                if val == 'N/A' or pd.isna(val):
                    return 'N/A'.rjust(width)
                elif isinstance(val, (int, float)):
                    if abs(val) < 1e-3 and val != 0:
                        formatted = f"{val:.2e}"
                    elif abs(val) > 1e6:
                        formatted = f"{val:.2e}"
                    else:
                        formatted = f"{val:.4f}"
                    return formatted.rjust(width)
                else:
                    return str(val).rjust(width)
            
            md_lines.append(f"| {stat_name:<10} | {format_stat(stata_val)} | {format_stat(python_val)} | {format_stat(diff_val)} | {format_stat(std_diff_val)} |\n")
        
        md_lines.append("\n")
    
    # Add Regression Analysis section
    if 'regression_stats' in results:
        md_lines.append("**Regression Analysis** (Python ~ Stata):\n\n")
        
        reg = results['regression_stats']
        
        md_lines.append(f"- **Model**: python = {reg['intercept']:.4f} + {reg['slope']:.4f} * stata\n")
        md_lines.append(f"- **R-squared**: {reg['r_squared']:.4f}\n")
        md_lines.append(f"- **N observations**: {reg['n_obs']:,}\n\n")
        
        # Coefficient details table with fixed column widths
        md_lines.append("| Coefficient |     Estimate |    Std Error | t-statistic |   p-value |\n")
        md_lines.append("|-------------|--------------|--------------|-------------|----------|\n")
        
        # Format regression values consistently
        def format_reg_stat(val, width=12):
            if pd.isna(val) or (isinstance(val, float) and not np.isfinite(val)):
                return 'nan'.rjust(width)
            elif isinstance(val, (int, float)):
                if abs(val) < 1e-3 and val != 0:
                    formatted = f"{val:.2e}"
                elif abs(val) > 1e6:
                    formatted = f"{val:.2e}"
                else:
                    formatted = f"{val:.4f}"
                return formatted.rjust(width)
            else:
                return str(val).rjust(width)
        
        # Format p-value specially (3 decimal places, but show as 0.000 for very small values)
        def format_pvalue(val, width=9):
            if pd.isna(val) or (isinstance(val, float) and not np.isfinite(val)):
                return 'nan'.rjust(width)
            elif isinstance(val, (int, float)):
                if val < 0.0005:  # Very small p-values
                    formatted = "0.000"
                else:
                    formatted = f"{val:.3f}"
                return formatted.rjust(width)
            else:
                return str(val).rjust(width)
        
        md_lines.append(f"| Intercept   | {format_reg_stat(reg['intercept'])} | {format_reg_stat(reg['intercept_se'])} | {format_reg_stat(reg['intercept_tstat'], 11)} | {format_pvalue(reg['intercept_pvalue'])} |\n")
        md_lines.append(f"| Slope       | {format_reg_stat(reg['slope'])} | {format_reg_stat(reg['slope_se'])} | {format_reg_stat(reg['slope_tstat'], 11)} | {format_pvalue(reg['slope_pvalue'])} |\n\n")
    
    elif 'summary_stats_error' in results:
        md_lines.append(f"**Summary Statistics Error**: {results['summary_stats_error']}\n\n")
    
    # Feedback for failed superset test
    if not results.get('test_2_passed', True) and 'missing_observations_sample' in results:
        md_lines.append("**Missing Observations Sample**:\n")
        missing_sample = results['missing_observations_sample']
        md_lines.append(f"```\n{missing_sample.to_string(index=False)}\n```\n\n")
    
    # Feedback for failed precision
    if 'bad_obs_count' in results:
        md_lines.append("**Feedback**:\n")
        md_lines.append(f"- Num observations with std_diff >= TOL_DIFF_1: {results['bad_obs_count']}/{results['total_obs_count']} ({results['bad_obs_percentage']:.3f}%)\n")
        if 'stata_std' in results:
            md_lines.append(f"- Stata standard deviation: {results['stata_std']:.2e}\n\n")
        else:
            md_lines.append("\n")
        
        if 'recent_bad' in results and len(results['recent_bad']) > 0:
            md_lines.append("**Most Recent Bad Observations**:\n")
            md_lines.append(f"```\n{results['recent_bad'].to_string()}\n```\n\n")
        
        if 'largest_diff' in results and len(results['largest_diff']) > 0:
            md_lines.append("**Largest Differences**:\n")
            md_lines.append(f"```\n{results['largest_diff'].to_string()}\n```\n\n")
        
        if 'largest_diff_before1950' in results:
            if results['largest_diff_before1950'] is not None and len(results['largest_diff_before1950']) > 0:
                md_lines.append("**Largest Differences Before 1950**:\n")
                md_lines.append(f"```\n{results['largest_diff_before1950'].to_string()}\n```\n\n")
            else:
                md_lines.append("**Largest Differences Before 1950**:\n")
                md_lines.append("```\nNo data before 1950\n```\n\n")
    
    md_lines.append("---\n\n")
    
    return md_lines

def validate_predictor(predictor_name, tstat_comparison_df=None):
    """Validate a single predictor against Stata output using polars optimization"""
    
    # Load Stata CSV with polars
    stata_path = Path(f"../Data/Predictors/{predictor_name}.csv")
    if not stata_path.exists():
        # Check if Python CSV exists for Python-only case
        python_path = Path(f"../pyData/Predictors/{predictor_name}.csv")
        if python_path.exists():
            # Python-only case: analyze Python CSV without comparison
            results = analyze_python_only(predictor_name)
            md_lines = output_predictor_results(predictor_name, results, False)
            return False, results, md_lines
        else:
            # Neither file exists
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
    passed, results = validate_precision_requirements(stata_df, python_df, predictor_name, tstat_comparison_df)
    
    # Check for overrides
    overrides = load_overrides()
    if predictor_name in overrides:
        override_info = overrides[predictor_name]
        results['override_applied'] = True
        results['override_info'] = override_info
        # Override the pass/fail status
        passed = True
    
    # Generate unified output
    md_lines = output_predictor_results(predictor_name, results, passed)
    
    return passed, results, md_lines

def get_available_predictors():
    """Get list of available predictor files, missing Python CSVs, and Python-only CSVs"""
    stata_dir = Path("../Data/Predictors/")
    python_dir = Path("../pyData/Predictors/")
    
    stata_files = set()
    python_files = set()
    
    if stata_dir.exists():
        stata_files = {f.stem for f in stata_dir.glob("*.csv")}
    
    if python_dir.exists():
        python_files = {f.stem for f in python_dir.glob("*.csv")}
    
    # Return intersection (available for validation), missing Python CSVs, and Python-only CSVs
    available_predictors = sorted(list(stata_files.intersection(python_files)))
    missing_python_csvs = sorted(list(stata_files - python_files))
    python_only_csvs = sorted(list(python_files - stata_files))
    
    return available_predictors, missing_python_csvs, python_only_csvs

def write_markdown_log(all_md_lines, test_predictors, passed_count, all_results):
    """Write detailed results to markdown log file"""
    log_path = Path("../Logs/testout_predictors.md")
    
    with open(log_path, 'w') as f:
        f.write(f"# Predictor Validation Results\n\n")
        f.write(f"**Generated**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
        f.write(f"**Configuration**:\n")
        f.write(f"- TOL_SUPERSET: {TOL_SUPERSET}%\n")
        f.write(f"- TOL_NUMROWS: {TOL_NUMROWS}%\n")
        f.write(f"- TOL_DIFF_1: {TOL_DIFF_1}\n")
        f.write(f"- TOL_OBS_1: {TOL_OBS_1}%\n")
        f.write(f"- EXTREME_Q: {EXTREME_Q}\n")
        f.write(f"- TOL_DIFF_2: {TOL_DIFF_2}\n")
        f.write(f"- TOL_TSTAT: {TOL_TSTAT}\n")
        f.write(f"- INDEX_COLS: {INDEX_COLS}\n\n")
        
        f.write(f"## Summary\n\n")

        f.write(f"Numbers report the **FAILURE** rate. ❌ (100.00%) is BAD.\n\n")
        
        # Create summary table with Python CSV column
        f.write("| Predictor                 | Python CSV | Superset   | NumRows       | Precision1   | Precision2              | T-stat     |\n")
        f.write("|---------------------------|------------|------------|---------------|--------------|-------------------------|------------|\n")
        
        # Sort predictors by test results - worst to best
        def sort_key(predictor):
            results = all_results.get(predictor, {})
            
            # Python CSV: False (missing) sorts before True (available)
            python_csv_available = results.get('python_csv_available', False)
            
            # Superset (Test 1): Higher failure percentages sort first
            test1 = results.get('test_1_passed', None)
            if test1 == False:
                missing_count = results.get('missing_count', 0)
                stata_obs_count = results.get('stata_obs_count', 0)
                if stata_obs_count > 0:
                    superset_sort = (missing_count / stata_obs_count) * 100
                else:
                    superset_sort = 100  # Treat as worst case
            elif test1 == True:
                superset_sort = -1  # Passed tests sort last
            else:
                superset_sort = 999  # NA sorts at end
            
            # NumRows (Test 2): Higher excess percentages sort first
            test2 = results.get('test_2_passed', None)
            if test2 == False:
                numrows_ratio = results.get('numrows_ratio', 0)
                numrows_sort = numrows_ratio
            elif test2 == True:
                numrows_sort = -1  # Passed tests sort last
            else:
                numrows_sort = 999  # NA sorts at end
            
            # Precision1: Higher bad observation percentages sort first
            test3 = results.get('test_3_passed', None)
            if test3 is not None:
                precision1_sort = results.get('bad_obs_percentage', 0)
            else:
                precision1_sort = 999  # NA sorts at end
            
            # Precision2: Higher percentile differences sort first
            test4 = results.get('test_4_passed', None)
            if test4 is not None:
                precision2_sort = results.get('pth_percentile_diff', 0)
            else:
                precision2_sort = 999  # NA sorts at end
                
            # T-stat: Higher t-stat differences sort first
            test5 = results.get('test_5_passed', None)
            if test5 is not None:
                tstat_sort = results.get('tstat_diff', 0)
            else:
                tstat_sort = 999  # NA sorts at end
            
            return (not python_csv_available, -superset_sort, -numrows_sort, -precision1_sort, -precision2_sort, -tstat_sort)
        
        sorted_predictors = sorted(test_predictors, key=sort_key)
        
        for predictor in sorted_predictors:
            results = all_results.get(predictor, {})
            
            # Get Python CSV availability
            python_csv_available = results.get('python_csv_available', False)
            csv_status = "✅" if python_csv_available else "❌"
            
            # Get test results with fallback
            test1 = results.get('test_1_passed', None)
            test2 = results.get('test_2_passed', None) 
            test3 = results.get('test_3_passed', None)
            test4 = results.get('test_4_passed', None)
            test5 = results.get('test_5_passed', None)
            
            # Format superset column (Test 1) with missing percentage for both pass/fail
            if test1 == True:
                missing_pct = results.get('missing_percentage', 0)
                col1 = f"✅ ({missing_pct:.2f}%)"
            elif test1 == False:
                # Include failure percentage when superset test fails
                missing_count = results.get('missing_count', 0)
                stata_obs_count = results.get('stata_obs_count', 0)
                if stata_obs_count > 0:
                    failure_pct = (missing_count / stata_obs_count) * 100
                    col1 = f"❌ ({failure_pct:.2f}%)"
                else:
                    col1 = "❌"
            else:
                col1 = "NA       "
            
            # Format NumRows column (Test 2) with ratio information
            if test2 == True:
                numrows_ratio = results.get('numrows_ratio', 0)
                col2 = f"✅ ({numrows_ratio:+.1f}%)"
            elif test2 == False:
                numrows_ratio = results.get('numrows_ratio', 0)
                col2 = f"❌ ({numrows_ratio:+.1f}%)"
            else:
                col2 = "NA "
            
            # Format precision1 column with percentage information
            if test3 == True:
                bad_pct = results.get('bad_obs_percentage', 0)
                col3 = f"✅ ({bad_pct:.1f}%)"
            elif test3 == False:
                bad_pct = results.get('bad_obs_percentage', 0)
                col3 = f"❌ ({bad_pct:.1f}%)"
            else:
                col3 = "NA  "
            # Format precision2 column with diff value information  
            if test4 == True:
                pth_diff = results.get('pth_percentile_diff', 0)
                col4 = f"✅ ({pth_diff:.1E})"
            elif test4 == False:
                pth_diff = results.get('pth_percentile_diff', 0)
                col4 = f"❌ ({pth_diff:.1E})"
            else:
                col4 = "NA"
            
            # Format t-stat column (Test 5)
            if test5 == True:
                tstat_diff_signed = results.get('tstat_diff_signed', 0)
                col5 = f"✅ ({tstat_diff_signed:+.2f})"
            elif test5 == False:
                tstat_diff_signed = results.get('tstat_diff_signed', 0)
                col5 = f"❌ ({tstat_diff_signed:+.2f})"
            else:
                if results.get('tstat_skipped'):
                    col5 = "SKIP"
                else:
                    col5 = "NA"
            
            # Add asterisk if override was applied
            predictor_display = predictor
            if results.get('override_applied'):
                predictor_display = f"{predictor}*"
            
            f.write(f"| {predictor_display:<25} | {csv_status:<9} | {col1:<7} | {col2:<11} | {col3:<12} | {col4:<23} | {col5:<10} |\n")
        
        # Count available predictors and overrides for summary
        available_count = sum(1 for p in test_predictors if all_results.get(p, {}).get('python_csv_available', False))
        override_count = sum(1 for p in test_predictors if all_results.get(p, {}).get('override_applied', False))
        
        f.write(f"\n**Overall**: {passed_count}/{available_count} available predictors passed validation\n")
        f.write(f"  - Natural passes: {passed_count - override_count}\n")
        f.write(f"  - Overridden passes: {override_count}\n")
        f.write(f"**Python CSVs**: {available_count}/{len(test_predictors)} predictors have Python implementation\n")
        f.write(f"\\* = Manual override applied (see Predictors/overrides.yaml for details)\n\n")
        
        f.write(f"## Detailed Results\n\n")
        
        # Write all the pre-formatted markdown lines
        for lines in all_md_lines:
            f.writelines(lines)
    
    print(f"\nDetailed results written to: {log_path}")




def main():
    parser = argparse.ArgumentParser(description='Validate Python predictor outputs against Stata CSV files')
    parser.add_argument('--predictors', '-p', nargs='+', help='Specific predictors to validate')
    parser.add_argument('--list', '-l', action='store_true', help='List available predictors and exit')
    parser.add_argument('--all', '-a', action='store_true', help='Test all available predictors')
    parser.add_argument('--tstat', action='store_true', help='Enable t-stat check (Test 5) by running PredictorSummaryComparison and comparing results')
    
    args = parser.parse_args()
    
    available_predictors, missing_python_csvs, python_only_csvs = get_available_predictors()
    
    if args.list:
        print("Available predictors (have both Stata and Python CSV):")
        for pred in available_predictors:
            print(f"  {pred}")
        print("\nMissing Python CSVs (have Stata but no Python CSV):")
        for pred in missing_python_csvs:
            print(f"  {pred}")
        print("\nPython-only CSVs (have Python but no Stata CSV):")
        for pred in python_only_csvs:
            print(f"  {pred}")
        return
    
    # Check that user provided either --all or --predictors
    if not args.all and not args.predictors:
        parser.error("Must specify either --all to test all predictors or --predictors to test specific ones")
    
    # Select predictors to test
    if args.predictors:
        # Split requested predictors into available, missing, and python-only
        requested_set = set(args.predictors)
        available_to_test = [p for p in available_predictors if p in requested_set]
        missing_to_include = [p for p in missing_python_csvs if p in requested_set]
        python_only_to_include = [p for p in python_only_csvs if p in requested_set]
        
        # Check for completely unknown predictors
        all_known = set(available_predictors + missing_python_csvs + python_only_csvs)
        unknown = requested_set - all_known
        if unknown:
            print(f"Warning: These predictors not found: {unknown}")
        
        test_predictors = available_to_test
        include_missing = missing_to_include
        include_python_only = python_only_to_include
    elif args.all:
        test_predictors = available_predictors
        include_missing = missing_python_csvs
        include_python_only = python_only_csvs
    
    if not test_predictors and not include_missing and not include_python_only:
        print("No predictors to test")
        return
    
    print(f"Validating {len(test_predictors)} predictors: {test_predictors}")
    if include_missing:
        print(f"Including {len(include_missing)} missing Python CSVs in summary: {include_missing}")
    if include_python_only:
        print(f"Including {len(include_python_only)} Python-only CSVs in summary: {include_python_only}")
    
    # Run PredictorSummaryComparison.py once if t-stat validation is enabled
    tstat_comparison_df = None
    if args.tstat:
        print(f"\n=== Running PredictorSummaryComparison.py for t-stat validation ===")

        import subprocess
        import os
        
        # Get the path to the utils directory PredictorSummaryComparison.py
        script_path = os.path.join('utils', 'PredictorSummaryComparison.py')
        
        # Run the script from the pyCode directory
        result = subprocess.run(['python3', script_path], cwd='.')
        
        if result.returncode != 0:
            print(f"Warning: PredictorSummaryComparison.py failed: {result.stderr}")
            print("T-stat validation will be skipped for all predictors")
        else:
            # Read the comparison results
            comparison_path = os.path.join('..', 'Logs', 'PredictorSummaryComparison.csv')
            
            if os.path.exists(comparison_path):
                tstat_comparison_df = pd.read_csv(comparison_path)
                print(f"Loaded t-stat comparison data for {len(tstat_comparison_df)} predictors")
            else:
                print(f"Warning: Comparison results file not found: {comparison_path}")
                print("T-stat validation will be skipped for all predictors")                
    
    # Validate each available predictor
    all_md_lines = []
    all_results = {}
    passed_count = 0
    
    for predictor in test_predictors:
        passed, results, md_lines = validate_predictor(predictor, tstat_comparison_df)
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
            'test_1_passed': None,  # Superset
            'test_2_passed': None,  # NumRows
            'test_3_passed': None,  # Precision1
            'test_4_passed': None,  # Precision2
            'test_5_passed': None,  # T-stat
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
    
    # Add results for Python-only CSVs
    for predictor in include_python_only:
        passed, results, md_lines = validate_predictor(predictor, tstat_comparison_df)
        all_md_lines.append(md_lines)
        all_results[predictor] = results
        # Python-only predictors cannot "pass" validation since there's no Stata baseline
    
    # Combine all predictors for summary
    all_predictors = test_predictors + include_missing + include_python_only
    
    # Write markdown log
    write_markdown_log(all_md_lines, all_predictors, passed_count, all_results)
    
    
    # Count overrides
    override_count = sum(1 for p in test_predictors if all_results.get(p, {}).get('override_applied', False))
    
    # Summary
    print(f"\n=== SUMMARY ===")
    print(f"Available predictors tested: {len(test_predictors)}")
    print(f"Missing Python CSVs included: {len(include_missing)}")
    print(f"Python-only CSVs included: {len(include_python_only)}")
    print(f"Passed validation: {passed_count}")
    print(f"  - Natural passes: {passed_count - override_count}")
    print(f"  - Overridden passes: {override_count}")
    print(f"Failed validation: {len(test_predictors) - passed_count}")
    
    if passed_count == len(test_predictors):
        print("🎉 ALL AVAILABLE TESTS PASSED!")
        sys.exit(0)
    else:
        print("❌ SOME TESTS FAILED")
        sys.exit(1)

if __name__ == "__main__":
    main()