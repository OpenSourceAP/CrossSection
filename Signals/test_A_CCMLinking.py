#!/usr/bin/env python3
"""
Test script to compare Python and Stata outputs for A_CCMLinkingTable.

Compares pyData/Intermediate/CCMLinkingTable.parquet with
Data/Intermediate/CCMLinkingTable.dta using precise numerical comparison.
"""

import os
import pandas as pd
import numpy as np
import pyreadstat


def load_stata_data():
    """Load Stata DTA file"""
    stata_path = "Data/Intermediate/CCMLinkingTable.dta"
    if not os.path.exists(stata_path):
        print(f"❌ Stata file not found: {stata_path}")
        return None

    df, _ = pyreadstat.read_dta(stata_path)
    print(f"📊 Stata data loaded: {len(df)} records")
    return df


def load_python_data():
    """Load Python Parquet file"""
    python_path = "pyData/Intermediate/CCMLinkingTable.parquet"
    if not os.path.exists(python_path):
        print(f"❌ Python file not found: {python_path}")
        return None

    df = pd.read_parquet(python_path)
    print(f"📊 Python data loaded: {len(df)} records")
    return df


def compare_dataframes_precise(stata_df, python_df, n_rows=1000):
    """
    Precise numerical comparison of dataframes.

    Converts first N rows to numerical matrices, computes absolute differences,
    and reports error percentiles.
    """
    print("\n" + "="*60)
    print("🔍 PRECISE NUMERICAL COMPARISON")
    print("="*60)

    # Basic validation
    print(f"Stata records:  {len(stata_df):,}")
    print(f"Python records: {len(python_df):,}")

    if len(stata_df) != len(python_df):
        print("❌ Record counts don't match - cannot proceed with comparison")
        return

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
    cols_display = (
        f"Columns: {numeric_cols[:5]}"
        f"{'...' if len(numeric_cols) > 5 else ''}"
    )
    print(cols_display)

    if not numeric_cols:
        print("❌ No common numeric columns found for comparison")
        return

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
        return

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

    if perc_values[-1] == 0:  # Max difference is 0
        print("✅ PERFECT MATCH: All values are identical")
    elif perc_values[-1] < 1e-12:
        print("✅ EXCELLENT: Differences are within machine precision")
    elif perc_values[-1] < 1e-8:
        print("✅ VERY GOOD: Differences are negligible")
    elif perc_values[-1] < 1e-6:
        print("⚠️  ACCEPTABLE: Small numerical differences detected")
    else:
        print(
            "❌ SIGNIFICANT: Large differences detected - "
            "investigation needed"
        )


def main():
    """Main function to run the precise comparison test."""
    print("🧪 Testing A_CCMLinkingTable Output Comparison")
    print("=" * 60)

    # Load data
    stata_df = load_stata_data()
    python_df = load_python_data()

    if stata_df is None or python_df is None:
        print("❌ Cannot proceed - missing data files")
        print("\nTo generate the files:")
        print(
            "1. Run Stata: do Code/DataDownloads/A_CCMLinkingTable.do"
        )
        print(
            "2. Run Python: python3 pyCode/DataDownloads/A_CCMLinkingTable.py"
        )
        return

    # Run precise numerical comparison
    compare_dataframes_precise(stata_df, python_df, n_rows=1000)

    print("\n" + "="*60)
    print("🏁 Precise comparison complete!")
    print("="*60)


if __name__ == "__main__":
    main()
