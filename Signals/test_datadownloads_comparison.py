#!/usr/bin/env python3
"""
Generalized test script to compare Python and Stata outputs for DataDownloads.

Compares any DataDownloads script output using precise numerical comparison.
Python files must be in parquet format, Stata files in dta format.
"""

import argparse
import os
import sys
import time
import pandas as pd
import numpy as np
import pyreadstat


# Mapping from script names to output file names
SCRIPT_TO_FILES = {
    "A_CCMLinkingTable": "CCMLinkingTable",
    "B_CompustatAnnual": "CompustatAnnual",
    "C_CompustatQuarterly": "CompustatQuarterly",
    "D_CompustatPensions": "CompustatPensions",
    "E_CompustatBusinessSegments": "CompustatSegments",
    "F_CompustatCustomerSegments": "CompustatSegmentDataCustomers",
    "G_CompustatShortInterest": "monthlyShortInterest",
    "H_CRSPDistributions": "CRSPdistributions",
    "I_CRSPmonthly": "monthlyCRSP",
    "I2_CRSPmonthlyraw": "monthlyCRSPraw",
    "J_CRSPdaily": "dailyCRSP",
    "K_CRSPAcquisitions": "m_CRSPAcquisitions",
    "L_IBES_EPS_Unadj": "IBES_EPS_Unadj",
    "L2_IBES_EPS_Adj": "IBES_EPS_Adj",
    "M_IBES_Recommendations": "IBES_Recommendations",
    "N_IBES_UnadjustedActuals": "IBES_UnadjustedActuals",
    "O_Daily_Fama-French": "dailyFF",
    "P_Monthly_Fama-French": "monthlyFF",
    "Q_MarketReturns": "monthlyMarket",
    "R_MonthlyLiquidityFactor": "monthlyLiquidity",
    "S_QFactorModel": "d_qfactor",
    "T_VIX": "d_vix",
    "U_GNPDeflator": "GNPdefl",
    "V_TBill3M": "TBill3M",
    "X_SPCreditRatings": "m_SP_creditratings",
    "X2_CIQCreditRatings": "m_CIQ_creditratings",
    "ZA_IPODates": "IPODates",
    "ZB_PIN": "pin_monthly",
    "ZC_GovernanceIndex": "GovIndex",
    "ZF_CRSPIBESLink": "IBESCRSPLinkingTable",
    "ZI_PatentCitations": "PatentDataProcessed",
    "ZL_CRSPOPTIONMETRICS": "OPTIONMETRICSCRSPLinkingTable",
}


def load_stata_data(script_name):
    """Load Stata DTA file for given script."""
    if script_name not in SCRIPT_TO_FILES:
        return None, f"Unknown script: {script_name}"

    filename = SCRIPT_TO_FILES[script_name]

    # Try .dta first
    dta_path = f"Data/Intermediate/{filename}.dta"
    if os.path.exists(dta_path):
        try:
            df, _ = pyreadstat.read_dta(dta_path)
            print(f"📊 Stata data loaded: {len(df):,} records ({filename}.dta)")
            return df, None
        except Exception as e:
            return None, f"Error reading {dta_path}: {e}"

    # Try .csv as fallback
    csv_path = f"Data/Intermediate/{filename}.csv"
    if os.path.exists(csv_path):
        try:
            df = pd.read_csv(csv_path)
            print(f"📊 Stata data loaded: {len(df):,} records ({filename}.csv)")
            return df, None
        except Exception as e:
            return None, f"Error reading {csv_path}: {e}"

    return None, f"Stata file not found: {dta_path}"


def load_python_data(script_name):
    """Load Python Parquet file for given script."""
    if script_name not in SCRIPT_TO_FILES:
        return None, f"Unknown script: {script_name}"

    filename = SCRIPT_TO_FILES[script_name]
    parquet_path = f"pyData/Intermediate/{filename}.parquet"

    if not os.path.exists(parquet_path):
        return None, f"Python file not found: {parquet_path}"

    try:
        df = pd.read_parquet(parquet_path)
        print(f"📊 Python data loaded: {len(df):,} records ({filename}.parquet)")
        return df, None
    except Exception as e:
        return None, f"Error reading {parquet_path}: {e}"


def compare_dataframes_precise(stata_df, python_df, n_rows=1000):
    """
    Precise numerical comparison of dataframes.

    Converts first N rows to numerical matrices, computes absolute differences,
    and reports error percentiles.
    """
    print("\n" + "="*64)
    print("🔍 PRECISE NUMERICAL COMPARISON")
    print("="*64)

    # Basic validation
    print(f"Stata records:  {len(stata_df):,}")
    print(f"Python records: {len(python_df):,}")

    if len(stata_df) != len(python_df):
        print("❌ Record counts don't match - cannot proceed with comparison")
        return "FAILED"

    # Column validation
    stata_cols = set(stata_df.columns)
    python_cols = set(python_df.columns)
    common_cols = stata_cols & python_cols

    print(f"Common columns: {len(common_cols)}")
    if stata_cols != python_cols:
        stata_only = stata_cols - python_cols
        python_only = python_cols - stata_cols
        if stata_only:
            print(f"⚠️  Stata-only columns: {sorted(stata_only)}")
        if python_only:
            print(f"⚠️  Python-only columns: {sorted(python_only)}")

    # Determine number of rows to compare
    max_rows = min(len(stata_df), len(python_df), n_rows)
    print(f"\n🔢 Comparing first {max_rows} rows")

    # Get subset of data
    stata_subset = stata_df.head(max_rows)[sorted(common_cols)]
    python_subset = python_df.head(max_rows)[sorted(common_cols)]

    # Identify numeric columns that can be compared
    numeric_cols = []
    for col in sorted(common_cols):
        if (pd.api.types.is_numeric_dtype(stata_subset[col]) and
                pd.api.types.is_numeric_dtype(python_subset[col])):
            numeric_cols.append(col)

    print(f"Numeric columns for comparison: {len(numeric_cols)}")
    if numeric_cols:
        cols_display = (
            f"Columns: {numeric_cols[:5]}"
            f"{'...' if len(numeric_cols) > 5 else ''}"
        )
        print(cols_display)

    if not numeric_cols:
        print("❌ No common numeric columns found for comparison")
        return "NO_NUMERIC"

    # Convert to matrices
    print("\n📊 Converting to numerical matrices...")
    stata_matrix = stata_subset[numeric_cols].values.astype(float)
    python_matrix = python_subset[numeric_cols].values.astype(float)

    print(f"Matrix dimensions: {stata_matrix.shape}")

    # Handle missing values consistently
    stata_mask = np.isfinite(stata_matrix)
    python_mask = np.isfinite(python_matrix)
    valid_mask = stata_mask & python_mask

    # Compute absolute differences only for valid (non-missing) values
    abs_diff = np.abs(stata_matrix - python_matrix)
    valid_diffs = abs_diff[valid_mask]

    print(f"Valid comparisons: {len(valid_diffs):,} out of "
          f"{stata_matrix.size:,} total elements")

    if len(valid_diffs) == 0:
        print("❌ No valid numerical comparisons possible")
        return "NO_VALID"

    # Compute error percentiles
    print("\n📈 ABSOLUTE DIFFERENCE PERCENTILES")
    print("-" * 50)

    percentiles = [50, 90, 95, 99, 100]
    perc_values = np.percentile(valid_diffs, percentiles)

    for p, val in zip(percentiles, perc_values):
        if p == 50:
            print(f"Median (50th):     {val:.2e}")
        elif p == 100:
            print(f"Maximum (100th):   {val:.2e}")
        else:
            print(f"{p}th percentile:    {val:.2e}")

    # Count exact matches
    exact_matches = np.sum(valid_diffs == 0)
    exact_pct = (exact_matches / len(valid_diffs)) * 100
    print(f"\nExact matches:     {exact_matches:,} ({exact_pct:.2f}%)")

    # Report on different tolerances
    print("\n🎯 TOLERANCE ANALYSIS")
    print("-" * 50)
    tolerances = [1e-15, 1e-12, 1e-10, 1e-8, 1e-6]

    for tol in tolerances:
        within_tol = np.sum(valid_diffs <= tol)
        pct = (within_tol / len(valid_diffs)) * 100
        print(f"Within {tol:.0e}:     {within_tol:,} ({pct:.2f}%)")

    # Check for any systematic differences by column
    print("\n📋 COLUMN-WISE ANALYSIS")
    print("-" * 50)

    for i, col in enumerate(numeric_cols[:10]):  # Show first 10 columns
        col_stata = stata_matrix[:, i]
        col_python = python_matrix[:, i]
        col_mask = np.isfinite(col_stata) & np.isfinite(col_python)

        if np.sum(col_mask) > 0:
            col_diffs = np.abs(col_stata[col_mask] - col_python[col_mask])
            max_diff = np.max(col_diffs)
            mean_diff = np.mean(col_diffs)
            exact_matches_col = np.sum(col_diffs == 0)

            print(f"{col[:18]:18} | Max: {max_diff:.2e} | "
                  f"Mean: {mean_diff:.2e} | "
                  f"Exact: {exact_matches_col}")

    # Overall assessment
    print("\n🏆 OVERALL ASSESSMENT")
    print("-" * 50)

    max_diff = perc_values[-1]
    if max_diff == 0:
        print("✅ PERFECT MATCH: All values are identical")
        return "PERFECT"
    elif max_diff < 1e-12:
        print("✅ EXCELLENT: Differences are within machine precision")
        return "EXCELLENT"
    elif max_diff < 1e-8:
        print("✅ VERY GOOD: Differences are negligible")
        return "VERY_GOOD"
    elif max_diff < 1e-6:
        print("⚠️  ACCEPTABLE: Small numerical differences detected")
        return "ACCEPTABLE"
    else:
        print(
            "❌ SIGNIFICANT: Large differences detected - "
            "investigation needed"
        )
        return "SIGNIFICANT"


def check_file_availability():
    """Check which script files are available for testing."""
    available = {}

    for script_name, filename in SCRIPT_TO_FILES.items():
        stata_dta = f"Data/Intermediate/{filename}.dta"
        stata_csv = f"Data/Intermediate/{filename}.csv"
        python_parquet = f"pyData/Intermediate/{filename}.parquet"

        stata_exists = os.path.exists(stata_dta) or os.path.exists(stata_csv)
        python_exists = os.path.exists(python_parquet)

        if stata_exists and python_exists:
            # Get record count for summary
            try:
                if os.path.exists(stata_dta):
                    df, _ = pyreadstat.read_dta(stata_dta)
                else:
                    df = pd.read_csv(stata_csv)
                record_count = len(df)
            except Exception:
                record_count = "unknown"

            available[script_name] = {
                'status': 'ready',
                'records': record_count
            }
        elif stata_exists:
            available[script_name] = {
                'status': 'missing_python',
                'records': None
            }
        elif python_exists:
            available[script_name] = {
                'status': 'missing_stata',
                'records': None
            }
        else:
            available[script_name] = {
                'status': 'missing_both',
                'records': None
            }

    return available


def list_available_scripts():
    """List all available scripts and their status."""
    print("📋 Available DataDownloads Scripts for Comparison:")
    print("="*64)

    availability = check_file_availability()

    ready = []
    missing_python = []
    missing_both = []

    for script_name, info in availability.items():
        if info['status'] == 'ready':
            ready.append((script_name, info['records']))
        elif info['status'] == 'missing_python':
            missing_python.append(script_name)
        else:
            missing_both.append(script_name)

    if ready:
        print("\n✅ Ready for Testing (both files exist):")
        for script_name, records in ready:
            if isinstance(records, int):
                print(f"   {script_name:<25} ({records:,} records)")
            else:
                print(f"   {script_name:<25} ({records} records)")

    if missing_python:
        print("\n⚠️  Partially Available (missing Python parquet):")
        for script_name in missing_python:
            print(f"   {script_name:<25} (Stata: ✅, Python: ❌)")

    if missing_both:
        print("\n❌ Not Available (both missing):")
        for script_name in missing_both[:10]:  # Show first 10
            print(f"   {script_name}")
        if len(missing_both) > 10:
            print(f"   ... and {len(missing_both) - 10} more")

    # Summary
    total = len(availability)
    ready_count = len(ready)
    partial_count = len(missing_python)
    missing_count = len(missing_both)

    print(f"\n📊 Summary: {ready_count}/{total} scripts ready, "
          f"{partial_count}/{total} need parquet migration, "
          f"{missing_count}/{total} not run yet")


def test_single_script(script_name, n_rows=1000):
    """Test a single script comparison."""
    print(f"🧪 Testing DataDownloads Output Comparison: {script_name}")
    print("="*64)

    # Load data
    stata_df, stata_error = load_stata_data(script_name)
    python_df, python_error = load_python_data(script_name)

    if stata_df is None or python_df is None:
        print("❌ Cannot proceed - missing data files\n")
        if stata_error:
            print(f"❌ {stata_error}")
        if python_error:
            print(f"❌ {python_error}")

        print("\n💡 To generate the files:")
        print(f"1. Run Stata: do Code/DataDownloads/{script_name}.do")
        print(f"2. Run Python: python3 pyCode/DataDownloads/{script_name}.py")
        print("\n⚠️  Note: Python script must output .parquet format")
        return "MISSING_FILES"

    # Run comparison
    result = compare_dataframes_precise(stata_df, python_df, n_rows)

    print(f"\n{'='*64}")
    print(f"🏁 Comparison complete for {script_name}!")
    print("="*64)

    return result


def test_all_scripts(n_rows=1000):
    """Test all available scripts."""
    print("🧪 Testing All DataDownloads Scripts")
    print("="*64)

    availability = check_file_availability()
    ready_scripts = [name for name, info in availability.items()
                     if info['status'] == 'ready']

    if not ready_scripts:
        print("❌ No scripts are ready for testing")
        print("💡 Run --list to see what files are missing")
        return

    results = {}
    start_time = time.time()

    for i, script_name in enumerate(ready_scripts, 1):
        print(f"\n[{i}/{len(ready_scripts)}] {script_name}...")
        script_start = time.time()

        # Load data quietly
        stata_df, _ = load_stata_data(script_name)
        python_df, _ = load_python_data(script_name)

        if stata_df is not None and python_df is not None:
            result = compare_dataframes_precise(stata_df, python_df, n_rows)
            script_time = time.time() - script_start

            # Show brief result
            status_map = {
                'PERFECT': '✅ PERFECT MATCH',
                'EXCELLENT': '✅ EXCELLENT',
                'VERY_GOOD': '✅ VERY GOOD',
                'ACCEPTABLE': '⚠️  ACCEPTABLE',
                'SIGNIFICANT': '❌ SIGNIFICANT'
            }
            status = status_map.get(result, f"❌ {result}")
            print(f"    {status} ({script_time:.1f}s)")
            results[script_name] = result
        else:
            results[script_name] = "FAILED"
            print("    ❌ FAILED (missing files)")

    # Summary
    total_time = time.time() - start_time
    print(f"\n{'='*64}")
    print("📊 BATCH TESTING SUMMARY")
    print("="*64)

    perfect = sum(1 for r in results.values() if r == 'PERFECT')
    excellent = sum(1 for r in results.values() if r == 'EXCELLENT')
    very_good = sum(1 for r in results.values() if r == 'VERY_GOOD')
    acceptable = sum(1 for r in results.values() if r == 'ACCEPTABLE')
    issues = sum(1 for r in results.values() if r in ['SIGNIFICANT'])
    failed = sum(1 for r in results.values()
                 if r in ['FAILED', 'NO_NUMERIC', 'NO_VALID'])

    total = len(results)
    print(f"✅ Perfect Matches:  {perfect}/{total} scripts")
    if excellent > 0:
        print(f"✅ Excellent:        {excellent}/{total} scripts")
    if very_good > 0:
        print(f"✅ Very Good:        {very_good}/{total} scripts")
    if acceptable > 0:
        print(f"⚠️  Acceptable:       {acceptable}/{total} scripts")
    if issues > 0:
        print(f"❌ Issues:           {issues}/{total} scripts")
    if failed > 0:
        print(f"❌ Failed:           {failed}/{total} scripts")

    print(f"\n🕐 Total testing time: {total_time:.1f} seconds")

    if issues == 0 and failed == 0:
        print("🎯 Overall Status: ALL TESTS PASSED")
    elif issues > 0:
        print("⚠️  Overall Status: SOME ISSUES DETECTED")
    else:
        print("❌ Overall Status: SOME TESTS FAILED")


def main():
    """Main function with command line interface."""
    parser = argparse.ArgumentParser(
        description=(
            "Compare Python and Stata outputs for DataDownloads scripts"
        )
    )
    parser.add_argument(
        'script_name',
        nargs='?',
        help='Name of the script to test (e.g., A_CCMLinkingTable)'
    )
    parser.add_argument(
        '--list',
        action='store_true',
        help='List available scripts and their status'
    )
    parser.add_argument(
        '--all',
        action='store_true',
        help='Test all available scripts'
    )
    parser.add_argument(
        '--rows',
        type=int,
        default=1000,
        help='Number of rows to compare (default: 1000)'
    )

    args = parser.parse_args()

    if args.list:
        list_available_scripts()
    elif args.all:
        test_all_scripts(args.rows)
    elif args.script_name:
        if args.script_name not in SCRIPT_TO_FILES:
            print(f"❌ Unknown script: {args.script_name}")
            print("\n💡 Available scripts:")
            scripts = list(SCRIPT_TO_FILES.keys())
            for i in range(0, len(scripts), 4):
                line = ", ".join(scripts[i:i+4])
                print(f"   {line}")
            print("\n📖 Usage:")
            print(f"   python {sys.argv[0]} <script_name>")
            print(f"   python {sys.argv[0]} --list")
            print(f"   python {sys.argv[0]} --all")
            sys.exit(1)

        test_single_script(args.script_name, args.rows)
    else:
        print("❌ No script specified")
        print("\n📖 Usage:")
        print(f"   python {sys.argv[0]} <script_name>")
        print(f"   python {sys.argv[0]} --list")
        print(f"   python {sys.argv[0]} --all")
        print("\n💡 Use --list to see available scripts")
        sys.exit(1)


if __name__ == "__main__":
    main()
