# ABOUTME: stata_ineq.py - Stata-compatible inequality operators with missing value handling
# ABOUTME: Provides functions that replicate Stata's treatment of missing values as positive infinity

"""
stata_ineq.py

Stata-compatible inequality operators that handle missing values according to Stata's rules:
- Missing values are treated as positive infinity in comparisons
- missing > finite = True
- finite > missing = False  
- missing > missing = False
- missing < finite = False
- finite < missing = True
- missing < missing = False

Usage:
    import polars as pl
    from utils.stata_ineq import stata_greater_than, stata_less_than
    
    # Polars expressions
    df.with_columns([
        stata_greater_than(pl.col("x"), pl.col("y")).alias("x_gt_y"),
        stata_less_than(pl.col("x"), pl.col("y")).alias("x_lt_y")
    ])
    
    # NumPy arrays  
    import numpy as np
    x_gt_y_numpy = stata_greater_than_numpy(x_array, y_array)

Functions:
    - stata_greater_than(left, right): Polars expression for left > right with Stata logic
    - stata_less_than(left, right): Polars expression for left < right with Stata logic
    - stata_greater_than_numpy(left, right): NumPy version for pandas/numpy arrays
    - stata_less_than_numpy(left, right): NumPy version for pandas/numpy arrays

Note: These functions implement the exact behavior documented in DocsForClaude/traps.md
"""

import polars as pl
import numpy as np


def stata_greater_than(left, right):
    """
    Polars expression for Stata-compatible greater-than comparison (left > right).
    
    Stata logic:
    - missing > finite = True (missing treated as positive infinity)
    - finite > missing = False
    - missing > missing = False  
    - finite > finite = normal comparison
    
    Args:
        left: Polars expression for left operand
        right: Polars expression for right operand
        
    Returns:
        Polars expression that evaluates to True/False following Stata rules
    """
    return pl.when(
        # Case 1: left is missing, right is not missing → True
        left.is_null() & right.is_not_null()
    ).then(
        pl.lit(True)
    ).when(
        # Case 2: left is not missing, right is missing → False
        left.is_not_null() & right.is_null()
    ).then(
        pl.lit(False)
    ).when(
        # Case 3: both are missing → False
        left.is_null() & right.is_null()
    ).then(
        pl.lit(False)
    ).otherwise(
        # Case 4: both are not missing → normal comparison
        left > right
    )


def stata_less_than(left, right):
    """
    Polars expression for Stata-compatible less-than comparison (left < right).
    
    Stata logic:
    - missing < finite = False (missing treated as positive infinity)
    - finite < missing = True
    - missing < missing = False
    - finite < finite = normal comparison
    
    Args:
        left: Polars expression for left operand
        right: Polars expression for right operand
        
    Returns:
        Polars expression that evaluates to True/False following Stata rules
    """
    return pl.when(
        # Case 1: left is missing, right is not missing → False
        left.is_null() & right.is_not_null()
    ).then(
        pl.lit(False)
    ).when(
        # Case 2: left is not missing, right is missing → True
        left.is_not_null() & right.is_null()
    ).then(
        pl.lit(True)
    ).when(
        # Case 3: both are missing → False
        left.is_null() & right.is_null()
    ).then(
        pl.lit(False)
    ).otherwise(
        # Case 4: both are not missing → normal comparison
        left < right
    )


def stata_greater_than_numpy(left, right):
    """
    NumPy version of Stata-compatible greater-than comparison for pandas/numpy arrays.
    
    Args:
        left: NumPy array or pandas Series for left operand
        right: NumPy array, pandas Series, or scalar for right operand
        
    Returns:
        NumPy boolean array following Stata rules
    """
    left_arr = np.asarray(left)
    
    # Handle scalar right operand
    if np.isscalar(right):
        right_arr = np.full_like(left_arr, right, dtype=float)
    else:
        right_arr = np.asarray(right)
    
    # Create masks for missing values
    left_missing = np.isnan(left_arr)
    right_missing = np.isnan(right_arr)
    
    # Initialize result array
    result = np.zeros_like(left_arr, dtype=bool)
    
    # Case 1: left is missing, right is not missing → True
    result[(left_missing) & (~right_missing)] = True
    
    # Case 2: left is not missing, right is missing → False
    result[(~left_missing) & (right_missing)] = False
    
    # Case 3: both are missing → False
    result[(left_missing) & (right_missing)] = False
    
    # Case 4: both are not missing → normal comparison
    both_not_missing = (~left_missing) & (~right_missing)
    result[both_not_missing] = left_arr[both_not_missing] > right_arr[both_not_missing]
    
    return result


def stata_less_than_numpy(left, right):
    """
    NumPy version of Stata-compatible less-than comparison for pandas/numpy arrays.
    
    Args:
        left: NumPy array or pandas Series for left operand
        right: NumPy array, pandas Series, or scalar for right operand
        
    Returns:
        NumPy boolean array following Stata rules
    """
    left_arr = np.asarray(left)
    
    # Handle scalar right operand
    if np.isscalar(right):
        right_arr = np.full_like(left_arr, right, dtype=float)
    else:
        right_arr = np.asarray(right)
    
    # Create masks for missing values
    left_missing = np.isnan(left_arr)
    right_missing = np.isnan(right_arr)
    
    # Initialize result array
    result = np.zeros_like(left_arr, dtype=bool)
    
    # Case 1: left is missing, right is not missing → False
    result[(left_missing) & (~right_missing)] = False
    
    # Case 2: left is not missing, right is missing → True
    result[(~left_missing) & (right_missing)] = True
    
    # Case 3: both are missing → False
    result[(left_missing) & (right_missing)] = False
    
    # Case 4: both are not missing → normal comparison
    both_not_missing = (~left_missing) & (~right_missing)
    result[both_not_missing] = left_arr[both_not_missing] < right_arr[both_not_missing]
    
    return result