# ABOUTME: test_placebos.py - validates Python placebo outputs against Stata CSV files
# ABOUTME: Polars-optimized precision validation script adapted from test_predictors.py

"""
test_placebos.py

Usage:
    cd Signals/pyCode/
    source .venv/bin/activate
    python3 StataComparison/test_placebos.py                    # Test all placebos
    python3 StataComparison/test_placebos.py --placebos AMq     # Test specific placebo

Precision Validation (per CLAUDE.md and DocsForClaude/leg4-Placebos.md):
1. Columns: Column names and order match exactly
2. Superset: Python observations are a superset of Stata observations
3. Precision1: For common observations, percentage with std_diff >= TOL_DIFF_1 < TOL_OBS_1
4. Precision2: For common observations, Pth percentile standardized difference < TOL_DIFF_2
   - std_diff = (python_value - stata_value) / std(all_stata_values)
   - common observations are observations that are in both Stata and Python

Inputs:
    - Stata CSV files in ../Data/Placebos/
    - Python CSV files in ../pyData/Placebos/

Outputs:
    - Console validation results with ✅/❌ symbols
    - Validation log saved to ../Logs/testout_placebos.md
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
import statsmodels.formula.api as smf
import numpy as np

# ================================
# VALIDATION CONFIGURATION
# ================================

# Superset test  
TOL_SUPERSET = 0.0  # Max allowed percentage of missing observations (units: percent)

# Precision1
TOL_DIFF_1 = 0.01  # Threshold for identifying imperfect observations (Precision1)
TOL_OBS_1 = 10  # Max allowed percentage of imperfect observations (units: percent)

# Precision2
EXTREME_Q = 0.99  # Quantile for extreme deviation (not percentile)
TOL_DIFF_2 = 1.00  # Tolerance for Pth percentile standardized difference (Precision2)
INDEX_COLS = ['permno', 'yyyymm']  # Index columns for observations

def load_csv_robust_polars(file_path):
    """Load CSV file with polars for performance, robust error handling"""
    try:
        # Get the placebo name from the file path
        placebo_name = Path(file_path).stem
        
        # Always use schema overrides to handle Stata's leading dot format (e.g. .0123 instead of 0.0123)
        schema_overrides = {
            'permno': pl.Int64,
            'yyyymm': pl.Int64,
            placebo_name: pl.Float64
        }
        
        df = pl.read_csv(file_path, schema_overrides=schema_overrides)
        return df
    except Exception as e:
        print(f"Error loading {file_path}: {e}")
        print(f"Trying fallback method...")
        # Try basic read if schema overrides fail
        try:
            df = pl.read_csv(file_path)
            return df
        except Exception as e2:
            print(f"Failed to load {file_path} completely: {e2}")
            return None

def validate_precision_requirements(stata_df, python_df, placebo_name):
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
    
    # Ensure consistent data types for index columns before any join operations
    try:
        # Cast both permno and yyyymm to consistent types (Int64 for both)
        stata_df = stata_df.with_columns([
            pl.col("permno").cast(pl.Int64, strict=False),
            pl.col("yyyymm").cast(pl.Int64, strict=False)
        ])
        python_df = python_df.with_columns([
            pl.col("permno").cast(pl.Int64, strict=False),
            pl.col("yyyymm").cast(pl.Int64, strict=False)
        ])
    except Exception as e:
        print(f"  ❌ Error casting index columns to consistent types: {e}")
        results['error'] = f'Error casting index columns to consistent types: {e}'
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
            cobs_stata.select(INDEX_COLS + [placebo_name]), 
            on=INDEX_COLS, 
            how="inner"
        ).with_columns([
            (pl.col(placebo_name) - pl.col(placebo_name + "_right")).alias("diff")
        ]).with_columns([
            pl.col("diff").abs().alias("abs_diff")
        ])
        
        # Calculate standard deviation of all Stata values for standardized differences
        stata_std = cobs_diff.select(pl.col(placebo_name + "_right").std()).item()
        
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
            stata_values = cobs_diff.select(pl.col(placebo_name + "_right")).to_pandas()[placebo_name + "_right"]
            python_values = cobs_diff.select(pl.col(placebo_name)).to_pandas()[placebo_name]
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
                    pl.col(placebo_name).alias("python"),
                    pl.col(placebo_name + "_right").alias("stata"),
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

def analyze_python_only(placebo_name):
    """Analyze Python-only CSV file when Stata CSV is missing"""
    python_path = Path(f"../pyData/Placebos/{placebo_name}.csv")
    
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
        
        # Test results for summary table
        'test_1_passed': False,  # ❌ for Columns since no Stata to compare
        'test_2_passed': None,   # NA for Superset 
        'test_3_passed': None,   # NA for Precision1
        'test_4_passed': None,   # NA for Precision2
        
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

def output_placebo_results(placebo_name, results, overall_passed):
    """
    Output placebo results to both console and return markdown lines
    """
    # Print to console
    print(f"\n=== Validating {placebo_name} ===")
    print(f"  Loaded Stata: {results.get('stata_obs_count', 0)} rows, Python: {results.get('python_obs_count', 0)} rows")
    
    # Handle error case
    if 'error' in results:
        print(f"  ❌ Error: {results['error']}")
        return [
            f"### {placebo_name}\n",
            f"**Status**: ❌ FAILED\n",
            f"**Error**: {results['error']}\n",
            "---\n"
        ]
    
    # Test 1: Column names
    test1 = results.get('test_1_passed', None)
    if test1 is True:
        print(f"  ✅ Test 1 - Column names: PASSED")
    elif test1 is False:
        print(f"  ❌ Test 1 - Column names: FAILED")
        print(f"    Stata:  {results.get('stata_columns', [])}")
        print(f"    Python: {results.get('python_columns', [])}")
    else:
        print(f"  NA Test 1 - Column names: N/A (No Stata CSV to compare)")
    
    # Test 2: Superset check
    test2 = results.get('test_2_passed', None)
    if test2 is True:
        missing_pct = results.get('missing_percentage', 0)
        print(f"  ✅ Test 2 - Superset check: PASSED (Missing {missing_pct:.2f}% <= {TOL_SUPERSET}% threshold)")
    elif test2 is False:
        missing_count = results.get('missing_count', 0)
        missing_pct = results.get('missing_percentage', 0)
        print(f"  ❌ Test 2 - Superset check: FAILED (Missing {missing_count} observations, {missing_pct:.2f}% > {TOL_SUPERSET}% threshold)")
        
        # Show sample of missing observations
        if 'missing_observations_sample' in results:
            print(f"  Sample of missing observations:")
            sample_df = results['missing_observations_sample']
            print(f"  {sample_df.to_string(index=False)}")
    else:
        print(f"  NA Test 2 - Superset check: N/A (No Stata CSV to compare)")
    
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
        print(f"  ✅ {placebo_name} PASSED")
    else:
        # For Python-only placebos, show different status
        if results.get('stata_csv_available') is False and results.get('python_csv_available') is True:
            print(f"  📊 {placebo_name} PYTHON-ONLY (No Stata baseline for comparison)")
        else:
            print(f"  ❌ {placebo_name} FAILED")
            # Print feedback for failed placebos
            if 'bad_obs_count' in results:
                print(f"    Bad observations: {results['bad_obs_count']}/{results['total_obs_count']} ({results['bad_obs_percentage']:.3f}%)")
    
    # Generate markdown lines
    md_lines = []
    md_lines.append(f"### {placebo_name}\n\n")
    
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
    
    md_lines.append("---\n\n")
    
    return md_lines

def validate_placebo(placebo_name):
    """Validate a single placebo against Stata output using polars optimization"""
    
    # Load Stata CSV with polars
    stata_path = Path(f"../Data/Placebos/{placebo_name}.csv")
    if not stata_path.exists():
        # Check if Python CSV exists for Python-only case
        python_path = Path(f"../pyData/Placebos/{placebo_name}.csv")
        if python_path.exists():
            # Python-only case: analyze Python CSV without comparison
            results = analyze_python_only(placebo_name)
            md_lines = output_placebo_results(placebo_name, results, False)
            return False, results, md_lines
        else:
            # Neither file exists
            results = {'error': f'Stata file not found: {stata_path}'}
            md_lines = output_placebo_results(placebo_name, results, False)
            return False, results, md_lines
    
    stata_df = load_csv_robust_polars(stata_path)
    if stata_df is None:
        results = {'error': f'Failed to load Stata file: {stata_path}'}
        md_lines = output_placebo_results(placebo_name, results, False)
        return False, results, md_lines
    
    # Load Python CSV with polars
    python_path = Path(f"../pyData/Placebos/{placebo_name}.csv") 
    if not python_path.exists():
        results = {'error': f'Python file not found: {python_path}'}
        md_lines = output_placebo_results(placebo_name, results, False)
        return False, results, md_lines
    
    python_df = load_csv_robust_polars(python_path)
    if python_df is None:
        results = {'error': f'Failed to load Python file: {python_path}'}
        md_lines = output_placebo_results(placebo_name, results, False)
        return False, results, md_lines
    
    # Perform precision validation
    passed, results = validate_precision_requirements(stata_df, python_df, placebo_name)
    
    # Generate unified output
    md_lines = output_placebo_results(placebo_name, results, passed)
    
    return passed, results, md_lines

def get_available_placebos():
    """Get list of available placebo files, missing Python CSVs, and Python-only CSVs"""
    stata_dir = Path("../Data/Placebos/")
    python_dir = Path("../pyData/Placebos/")
    
    stata_files = set()
    python_files = set()
    
    if stata_dir.exists():
        stata_files = {f.stem for f in stata_dir.glob("*.csv")}
    
    if python_dir.exists():
        python_files = {f.stem for f in python_dir.glob("*.csv")}
    
    # Return intersection (available for validation), missing Python CSVs, and Python-only CSVs
    available_placebos = sorted(list(stata_files.intersection(python_files)))
    missing_python_csvs = sorted(list(stata_files - python_files))
    python_only_csvs = sorted(list(python_files - stata_files))
    
    return available_placebos, missing_python_csvs, python_only_csvs

def write_markdown_log(all_md_lines, test_placebos, passed_count, all_results):
    """Write detailed results to markdown log file"""
    log_path = Path("../Logs/testout_placebos.md")
    
    with open(log_path, 'w') as f:
        f.write(f"# Placebo Validation Results\n\n")
        f.write(f"**Generated**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
        f.write(f"**Configuration**:\n")
        f.write(f"- TOL_SUPERSET: {TOL_SUPERSET}%\n")
        f.write(f"- TOL_DIFF_1: {TOL_DIFF_1}\n")
        f.write(f"- TOL_OBS_1: {TOL_OBS_1}%\n")
        f.write(f"- EXTREME_Q: {EXTREME_Q}\n")
        f.write(f"- TOL_DIFF_2: {TOL_DIFF_2}\n")
        f.write(f"- INDEX_COLS: {INDEX_COLS}\n\n")
        
        f.write(f"## Summary\n\n")
        
        # Create summary table with Python CSV column
        f.write("| Placebo                   | Python CSV | Columns  | Superset  | Precision1   | Precision2              |\n")
        f.write("|---------------------------|------------|----------|-----------|--------------|-------------------------|\n")
        
        # Sort placebos by test results - worst to best
        def sort_key(placebo):
            results = all_results.get(placebo, {})
            
            # Python CSV: False (missing) sorts before True (available)
            python_csv_available = results.get('python_csv_available', False)
            
            # Columns: False (failed) sorts before True (passed), None last
            test1 = results.get('test_1_passed', None)
            columns_sort = 0 if test1 == False else (1 if test1 == True else 2)
            
            # Superset: Higher failure percentages sort first
            test2 = results.get('test_2_passed', None)
            if test2 == False:
                missing_count = results.get('missing_count', 0)
                stata_obs_count = results.get('stata_obs_count', 0)
                if stata_obs_count > 0:
                    superset_sort = (missing_count / stata_obs_count) * 100
                else:
                    superset_sort = 100  # Treat as worst case
            elif test2 == True:
                superset_sort = -1  # Passed tests sort last
            else:
                superset_sort = 999  # NA sorts at end
            
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
            
            return (not python_csv_available, columns_sort, -superset_sort, -precision1_sort, -precision2_sort)
        
        sorted_placebos = sorted(test_placebos, key=sort_key)
        
        for placebo in sorted_placebos:
            results = all_results.get(placebo, {})
            
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
            
            # Format superset column with missing percentage for both pass/fail
            if test2 == True:
                missing_pct = results.get('missing_percentage', 0)
                col2 = f"✅ ({missing_pct:.2f}%)"
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
                col4 = f"✅ ({EXTREME_Q*100:.0f}th diff {pth_diff:.1E})"
            elif test4 == False:
                pth_diff = results.get('pth_percentile_diff', 0)
                col4 = f"❌ ({EXTREME_Q*100:.0f}th diff {pth_diff:.1E})"
            else:
                col4 = "NA"
            
            f.write(f"| {placebo:<25} | {csv_status:<9} | {col1:<7} | {col2:<11} | {col3:<12} | {col4:<23} |\n")
        
        # Count available placebos for summary
        available_count = sum(1 for p in test_placebos if all_results.get(p, {}).get('python_csv_available', False))
        
        f.write(f"\n**Overall**: {passed_count}/{available_count} available placebos passed validation\n")
        f.write(f"**Python CSVs**: {available_count}/{len(test_placebos)} placebos have Python implementation\n\n")
        
        f.write(f"## Detailed Results\n\n")
        
        # Write all the pre-formatted markdown lines
        for lines in all_md_lines:
            f.writelines(lines)
    
    print(f"\nDetailed results written to: {log_path}")

def main():
    parser = argparse.ArgumentParser(description='Validate Python placebo outputs against Stata CSV files')
    parser.add_argument('--placebos', '-p', nargs='+', help='Specific placebos to validate')
    parser.add_argument('--list', '-l', action='store_true', help='List available placebos and exit')
    
    args = parser.parse_args()
    
    available_placebos, missing_python_csvs, python_only_csvs = get_available_placebos()
    
    if args.list:
        print("Available placebos (have both Stata and Python CSV):")
        for placebo in available_placebos:
            print(f"  {placebo}")
        print("\nMissing Python CSVs (have Stata but no Python CSV):")
        for placebo in missing_python_csvs:
            print(f"  {placebo}")
        print("\nPython-only CSVs (have Python but no Stata CSV):")
        for placebo in python_only_csvs:
            print(f"  {placebo}")
        return
    
    # Select placebos to test
    if args.placebos:
        # Split requested placebos into available, missing, and python-only
        requested_set = set(args.placebos)
        available_to_test = [p for p in available_placebos if p in requested_set]
        missing_to_include = [p for p in missing_python_csvs if p in requested_set]
        python_only_to_include = [p for p in python_only_csvs if p in requested_set]
        
        # Check for completely unknown placebos
        all_known = set(available_placebos + missing_python_csvs + python_only_csvs)
        unknown = requested_set - all_known
        if unknown:
            print(f"Warning: These placebos not found: {unknown}")
        
        test_placebos = available_to_test
        include_missing = missing_to_include
        include_python_only = python_only_to_include
    else:
        test_placebos = available_placebos
        include_missing = missing_python_csvs
        include_python_only = python_only_csvs
    
    if not test_placebos and not include_missing and not include_python_only:
        print("No placebos to test")
        return
    
    print(f"Validating {len(test_placebos)} placebos: {test_placebos}")
    if include_missing:
        print(f"Including {len(include_missing)} missing Python CSVs in summary: {include_missing}")
    if include_python_only:
        print(f"Including {len(include_python_only)} Python-only CSVs in summary: {include_python_only}")
    
    # Validate each available placebo
    all_md_lines = []
    all_results = {}
    passed_count = 0
    
    for placebo in test_placebos:
        passed, results, md_lines = validate_placebo(placebo)
        results['python_csv_available'] = True
        all_md_lines.append(md_lines)
        all_results[placebo] = results
        if passed:
            passed_count += 1
    
    # Add dummy results for missing Python CSVs
    for placebo in include_missing:
        print(f"\n=== {placebo} ===")
        print(f"  ❌ Python CSV missing: ../pyData/Placebos/{placebo}.csv")
        
        # Create dummy results for missing Python CSV
        dummy_results = {
            'python_csv_available': False,
            'test_1_passed': None,
            'test_2_passed': None, 
            'test_3_passed': None,
            'test_4_passed': None,
            'error': 'Python CSV file not found'
        }
        all_results[placebo] = dummy_results
        
        # Create minimal markdown for missing placebos
        md_lines = [
            f"### {placebo}\n\n",
            "**Status**: ❌ MISSING PYTHON CSV\n\n",
            f"**Error**: Python CSV file not found: ../pyData/Placebos/{placebo}.csv\n\n",
            "---\n\n"
        ]
        all_md_lines.append(md_lines)
    
    # Add results for Python-only CSVs
    for placebo in include_python_only:
        passed, results, md_lines = validate_placebo(placebo)
        all_md_lines.append(md_lines)
        all_results[placebo] = results
        # Python-only placebos cannot "pass" validation since there's no Stata baseline
    
    # Combine all placebos for summary
    all_placebos = test_placebos + include_missing + include_python_only
    
    # Write markdown log
    write_markdown_log(all_md_lines, all_placebos, passed_count, all_results)
    
    # Summary
    print(f"\n=== SUMMARY ===")
    print(f"Available placebos tested: {len(test_placebos)}")
    print(f"Missing Python CSVs included: {len(include_missing)}")
    print(f"Python-only CSVs included: {len(include_python_only)}")
    print(f"Passed validation: {passed_count}")
    print(f"Failed validation: {len(test_placebos) - passed_count}")
    
    if passed_count == len(test_placebos):
        print("🎉 ALL AVAILABLE TESTS PASSED!")
        sys.exit(0)
    else:
        print("❌ SOME TESTS FAILED")
        sys.exit(1)

if __name__ == "__main__":
    main()
