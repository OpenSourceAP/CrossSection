# ABOUTME: test_predictors.py - validates Python predictor outputs against Stata CSV files
# ABOUTME: Polars-optimized precision validation script with 6x performance improvement

"""
test_predictors.py

Usage:
    cd pyCode/
    source .venv/bin/activate
    python3 utils/test_predictors.py --all             # Test all predictors
    python3 utils/test_predictors.py --predictors Accruals  # Test specific predictor

Precision Validation (per CLAUDE.md:290-304):
1. Columns: Column names and order match exactly
2. Superset: Python observations are a superset of Stata observations
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

# Precision1: goal is 0.01, 1
TOL_DIFF_1 = 0.01  # Standardized difference threshold for imperfect observations
TOL_OBS_1 = 1  # Max allowed percentage of imperfect observations (units: percent)

# Precision2: goal is 0.10, 0.999
TOL_DIFF_2 = 0.10  # Tolerance for Pth percentile standardized difference (Precision2)
EXTREME_Q = 0.999  # Quantile for extreme deviation (not percentile)
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
        # First try normal read
        df = pl.read_csv(file_path)
        # Filter out rows where the predictor value (non-index column) is null or NaN
        predictor_name = Path(file_path).stem
        if predictor_name in df.columns:
            df = df.filter(pl.col(predictor_name).is_finite())
        return df
    except Exception as e:
        print(f"Error loading {file_path}: {e}")
        print(f"Might be because the signals look like integers but are actually floats")
        print(f"Trying with schema overrides for mixed int/float columns")
        # Try with schema overrides for mixed int/float columns
        try:
            # Get the predictor name from the file path
            predictor_name = Path(file_path).stem
            
            # For predictor files, override the predictor column to be Float64
            schema_overrides = {
                'permno': pl.Int64,
                'yyyymm': pl.Int64,
                predictor_name: pl.Float64
            }
            
            df = pl.read_csv(file_path, schema_overrides=schema_overrides)
            print(f"Successfully loaded {file_path} with schema overrides")
            # Filter out rows where the predictor value is null or NaN
            if predictor_name in df.columns:
                df = df.filter(pl.col(predictor_name).is_finite())
            return df
        except Exception as e2:
            print(f"Failed to load {file_path} even with schema overrides: {e2}")
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
    
    # Store individual test results
    results['test_1_passed'] = cols_match
    results['test_2_passed'] = is_superset
    results['test_3_passed'] = precision1_ok
    results['test_4_passed'] = precision2_ok
    
    return cols_match and is_superset and precision1_ok and precision2_ok, results

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
        print(f"  ❌ Test 2 - Superset check: FAILED (Missing {missing_pct:.2f}% > {TOL_SUPERSET}% threshold, {missing_count} observations)")
        
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
        
        if 'largest_diff_before1950' in results:
            if results['largest_diff_before1950'] is not None and len(results['largest_diff_before1950']) > 0:
                md_lines.append("**Largest Differences Before 1950**:\n")
                md_lines.append(f"```\n{results['largest_diff_before1950'].to_string()}\n```\n\n")
            else:
                md_lines.append("**Largest Differences Before 1950**:\n")
                md_lines.append("```\nNo data before 1950\n```\n\n")
    
    md_lines.append("---\n\n")
    
    return md_lines

def validate_predictor(predictor_name):
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
    passed, results = validate_precision_requirements(stata_df, python_df, predictor_name)
    
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
        f.write(f"- TOL_DIFF_1: {TOL_DIFF_1}\n")
        f.write(f"- TOL_OBS_1: {TOL_OBS_1}%\n")
        f.write(f"- EXTREME_Q: {EXTREME_Q}\n")
        f.write(f"- TOL_DIFF_2: {TOL_DIFF_2}\n")
        f.write(f"- INDEX_COLS: {INDEX_COLS}\n\n")
        
        f.write(f"## Summary\n\n")

        f.write(f"Numbers report the **FAILURE** rate. ❌ (100.00%) is BAD.\n\n")
        
        # Create summary table with Python CSV column
        f.write("| Predictor                 | Python CSV | Columns  | Superset  | Precision1   | Precision2              |\n")
        f.write("|---------------------------|------------|----------|-----------|--------------|-------------------------|\n")
        
        # Sort predictors by test results - worst to best
        def sort_key(predictor):
            results = all_results.get(predictor, {})
            
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
                col4 = f"✅ ({EXTREME_Q*100:.3f}th diff {pth_diff:.1E})"
            elif test4 == False:
                pth_diff = results.get('pth_percentile_diff', 0)
                col4 = f"❌ ({EXTREME_Q*100:.3f}th diff {pth_diff:.1E})"
            else:
                col4 = "NA"
            
            # Add asterisk if override was applied
            predictor_display = predictor
            if results.get('override_applied'):
                predictor_display = f"{predictor}*"
            
            f.write(f"| {predictor_display:<25} | {csv_status:<9} | {col1:<7} | {col2:<11} | {col3:<12} | {col4:<23} |\n")
        
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

def format_predictor_statuses(results):
    """Format all status strings for a predictor based on its results"""
    # Python CSV status
    python_csv = "yes" if results.get('python_csv_available', False) else "no"
    
    # Superset status
    test2 = results.get('test_2_passed', None)
    if test2 is True:
        superset_status = "yes (100%)"
    elif test2 is False:
        missing_count = results.get('missing_count', 0)
        stata_obs_count = results.get('stata_obs_count', 1)
        failure_pct = (missing_count / stata_obs_count) * 100
        superset_status = f"no ({failure_pct:.2f}%) ❌"
    else:
        superset_status = "no data ❌"
    
    # Precision1 status
    test3 = results.get('test_3_passed', None)
    if test3 is True:
        bad_pct = results.get('bad_obs_percentage', 0)
        precision1_status = f"yes ({bad_pct:.2f}%)"
    elif test3 is False:
        bad_pct = results.get('bad_obs_percentage', 0)
        precision1_status = f"no ({bad_pct:.2f}%) ❌"
    else:
        precision1_status = "no data ❌"
    
    # Precision2 status
    test4 = results.get('test_4_passed', None)
    if test4 is True:
        pth_diff = results.get('pth_percentile_diff', 0)
        precision2_status = f"yes ({EXTREME_Q*100:.3f}th diff {pth_diff:.1E})"
    elif test4 is False:
        pth_diff = results.get('pth_percentile_diff', 0)
        precision2_status = f"no ({EXTREME_Q*100:.3f}th diff {pth_diff:.1E}) ❌"
    else:
        precision2_status = "no data ❌"
    
    return python_csv, superset_status, precision1_status, precision2_status


def write_predictor_entry(f, predictor, script_name, python_csv, superset_status, precision1_status, precision2_status):
    """Write a single predictor entry to the markdown file"""
    f.write(f"- **{predictor}**\n")
    f.write(f"  - Script: {script_name}\n")
    f.write(f"  - Python CSV: {python_csv}\n")
    f.write(f"  - Superset: {superset_status}\n")
    f.write(f"  - Precision1: {precision1_status}\n")
    f.write(f"  - Precision2: {precision2_status}\n\n")


def write_worst_predictors_log(all_results, test_predictors):
    """Write focused report on worst performing predictors"""
    log_path = Path("../Logs/testworst_predictors.md")
    
    # Load YAML mapping file to get script names
    yaml_path = Path("Predictors/00_map_predictors.yaml")
    script_mapping = {}
    try:
        with open(yaml_path, 'r') as f:
            yaml_data = yaml.safe_load(f)
            for script_name, script_info in yaml_data.items():
                if 'predictors' in script_info:
                    for predictor_csv in script_info['predictors']:
                        predictor_name = predictor_csv.replace('.csv', '')
                        script_mapping[predictor_name] = script_name.replace('.py', '')
    except Exception as e:
        print(f"Warning: Could not load YAML mapping file: {e}")
        # If YAML fails, use predictor name as script name
        for predictor in test_predictors:
            script_mapping[predictor] = predictor

    # Get all predictors that have results (both tested and missing)
    all_predictors_with_results = list(all_results.keys())
    
    # Get predictors to exclude from failing list
    overrides = load_overrides()
    accepted_overrides = set(overrides.keys())
    
    _, _, python_only_csvs = get_available_predictors()
    python_only_set = set(python_only_csvs)
    
    # Identify failing predictors by category
    superset_failing_predictors = []
    other_failing_predictors = []
    
    for predictor in all_predictors_with_results:
        results = all_results.get(predictor, {})
        
        # Skip predictors without Stata CSVs (Python-only)
        if predictor in python_only_set:
            continue
            
        # Skip predictors with accepted overrides
        if predictor in accepted_overrides:
            continue
        
        # Check which tests failed
        test1_failed = results.get('test_1_passed') == False
        test2_failed = results.get('test_2_passed') == False  
        test3_failed = results.get('test_3_passed') == False
        test4_failed = results.get('test_4_passed') == False
        
        # If any test failed, categorize by superset failure
        if test1_failed or test2_failed or test3_failed or test4_failed:
            if test2_failed:
                superset_failing_predictors.append(predictor)
            else:
                other_failing_predictors.append(predictor)
    
    # Map failing predictors to scripts for each category
    superset_failing_scripts = set()
    for predictor in superset_failing_predictors:
        script_name = script_mapping.get(predictor, predictor)
        superset_failing_scripts.add(script_name)
    
    other_failing_scripts = set()
    for predictor in other_failing_predictors:
        script_name = script_mapping.get(predictor, predictor)
        other_failing_scripts.add(script_name)
    
    superset_failing_scripts_sorted = sorted(list(superset_failing_scripts))
    other_failing_scripts_sorted = sorted(list(other_failing_scripts))
    
    # Sort predictors by superset failure (highest failure percentage first)
    def superset_sort_key(predictor):
        results = all_results.get(predictor, {})
        test2 = results.get('test_2_passed', None)
        if test2 == False:
            missing_count = results.get('missing_count', 0)
            stata_obs_count = results.get('stata_obs_count', 1)  # Avoid division by zero
            return (missing_count / stata_obs_count) * 100
        elif test2 == True:
            return -1  # Passed tests go to end
        else:
            return -2  # NA/not tested go to very end
    
    # Sort predictors by precision1 failure (highest bad obs percentage first) 
    def precision1_sort_key(predictor):
        results = all_results.get(predictor, {})
        test3 = results.get('test_3_passed', None)
        if test3 is not None:
            return results.get('bad_obs_percentage', 0)
        else:
            return -1  # NA/not tested go to end
    
    # Get worst 20 for each category
    superset_worst = sorted(all_predictors_with_results, key=superset_sort_key, reverse=True)[:20]
    precision1_worst = sorted(all_predictors_with_results, key=precision1_sort_key, reverse=True)[:20]
    
    with open(log_path, 'w') as f:
        f.write(f"# Scripts That Failed Any Test\n\n")
        f.write(f"**Generated**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
        
        # Write scripts that failed superset test
        f.write(f"**Scripts that failed superset test** (Python missing Stata observations):\n\n")
        if superset_failing_scripts_sorted:
            for script in superset_failing_scripts_sorted:
                f.write(f"{script} ")
            f.write("\n\n")
        else:
            f.write("- No scripts failed superset test\n\n")
        
        # Write scripts that failed other tests
        f.write(f"**Scripts that failed other tests** (but passed superset):\n\n")
        if other_failing_scripts_sorted:
            for script in other_failing_scripts_sorted:
                f.write(f"{script} ")
            f.write("\n\n")
        else:
            f.write("- No scripts failed other tests\n\n")
        
        f.write(f"## Detailed Analysis\n\n")
        f.write(f"This section focuses on the 20 worst predictors by Superset and Precision1 metrics.\n\n")
        
        # Worst Superset section
        f.write("## Worst Superset\n\n")
        f.write("Predictors with highest superset failure rates (Python missing the most Stata observations):\n\n")
        
        for predictor in superset_worst:
            results = all_results.get(predictor, {})
            script_name = script_mapping.get(predictor, predictor)
            
            python_csv, superset_status, precision1_status, precision2_status = format_predictor_statuses(results)
            write_predictor_entry(f, predictor, script_name, python_csv, superset_status, precision1_status, precision2_status)
        
        # Worst Precision1 section
        f.write("## Worst Precision1\n\n")
        f.write("Predictors with highest precision1 failure rates (highest percentage of observations with significant differences):\n\n")
        
        for predictor in precision1_worst:
            results = all_results.get(predictor, {})
            script_name = script_mapping.get(predictor, predictor)
            
            python_csv, superset_status, precision1_status, precision2_status = format_predictor_statuses(results)
            write_predictor_entry(f, predictor, script_name, python_csv, superset_status, precision1_status, precision2_status)
    
    print(f"\nWorst predictors report written to: {log_path}")

def main():
    parser = argparse.ArgumentParser(description='Validate Python predictor outputs against Stata CSV files')
    parser.add_argument('--predictors', '-p', nargs='+', help='Specific predictors to validate')
    parser.add_argument('--list', '-l', action='store_true', help='List available predictors and exit')
    parser.add_argument('--all', '-a', action='store_true', help='Test all available predictors')
    
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
    
    # Add results for Python-only CSVs
    for predictor in include_python_only:
        passed, results, md_lines = validate_predictor(predictor)
        all_md_lines.append(md_lines)
        all_results[predictor] = results
        # Python-only predictors cannot "pass" validation since there's no Stata baseline
    
    # Combine all predictors for summary
    all_predictors = test_predictors + include_missing + include_python_only
    
    # Write markdown log
    write_markdown_log(all_md_lines, all_predictors, passed_count, all_results)
    
    # Write worst predictors report
    write_worst_predictors_log(all_results, all_predictors)
    
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