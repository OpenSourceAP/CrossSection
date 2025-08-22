#%%

#!/usr/bin/env python3
# ABOUTME: Test script for stata_regress module using MWE data
# ABOUTME: Runs regression with collinearity detection on MWE 1-3

# Inputs: mwe/tf_mwe1.csv, mwe/tf_mwe2.csv, mwe/tf_mwe3.csv
# Outputs: Regression results matching Stata format
# How to run: python3 test_on_mwe.py

import numpy as np
import pandas as pd
from stata_regress import regress, format_regression_output


def extract_stata_coefficients(log_file_path):
    """
    Extract coefficients and standard errors from Stata log file.
    
    Parameters
    ----------
    log_file_path : str
        Path to the Stata .log file
        
    Returns
    -------
    dict
        Dictionary with variable names as keys and {'coef': float, 'std_err': float} as values
        Omitted variables have coef=0.0 and std_err=None
    """
    coefficients = {}
    
    with open(log_file_path, 'r') as f:
        lines = f.readlines()
    
    # Find coefficient table start and end
    coef_start = None
    coef_end = None
    
    for i, line in enumerate(lines):
        # Look for coefficient table header
        if "| Coefficient  Std. err." in line:
            coef_start = i + 1  # Start from next line (separator is already past)
        elif coef_start is not None and line.startswith("-------------") and i > coef_start:
            coef_end = i
            break
    
    if coef_start is None or coef_end is None:
        raise ValueError("Could not find coefficient table in log file")
    
    # Parse coefficient rows
    for i in range(coef_start, coef_end):
        line = lines[i].strip()
        if not line or line.startswith("---"):
            continue
            
        # Split on pipe separator
        if '|' not in line:
            continue
            
        var_part, coef_part = line.split('|', 1)
        var_name = var_part.strip()
        coef_part = coef_part.strip()
        
        # Handle omitted variables
        if "(omitted)" in coef_part:
            coefficients[var_name] = {'coef': 0.0, 'std_err': None}
        else:
            # Parse coefficient and standard error
            parts = coef_part.split()
            if len(parts) >= 2:
                try:
                    coef = float(parts[0])
                    std_err = float(parts[1])
                    coefficients[var_name] = {'coef': coef, 'std_err': std_err}
                except (ValueError, IndexError):
                    continue
    
    return coefficients


def test_regress(mwe_num):
    
    """Test a specific standard regression MWE dataset."""
    # Load test data from CSV
    df = pd.read_csv(f'mwe/tf_mwe{mwe_num}.csv')

    # Prepare X and y
    X_cols = ['A_3', 'A_5', 'A_10', 'A_20', 'A_50', 'A_100',
              'A_200', 'A_400', 'A_600', 'A_800', 'A_1000']
    X = df[X_cols]
    y = df['fRet']

    print(f"\n{'='*70}")
    print(f"MWE {mwe_num} - Regression Output")
    print(f"{'='*70}\n")

    # Run regression with collinearity detection
    model, keep_cols, drop_cols, reasons = regress(X, y)

    print(f"Kept columns: {keep_cols}")
    print(f"Dropped columns: {drop_cols}")
    print(f"Reasons: {reasons}\n")

    # Format output to match Stata
    format_regression_output(model, keep_cols, drop_cols)

    # Print additional statistics
    print(f"\nNumber of obs = {len(model.model.endog)}")
    print(f"R-squared = {model.rsquared:.4f}")
    print(f"Adj R-squared = {model.rsquared_adj:.4f}")
    print(f"Root MSE = {np.sqrt(model.mse_resid):.4f}")

    # Expected results from Stata logs
    expected = {
        1: {
            'dropped': ['a_100', 'a_200', 'a_400', 'a_600',
                       'a_800', 'a_1000'],
            'n_obs': 433,
            'r_squared': 0.0136
        },
        2: {
            'dropped': ['a_200', 'a_400', 'a_600', 'a_800',
                       'a_1000'],
            'n_obs': 1309,
            'r_squared': 0.0849
        },
        3: {
            'dropped': ['a_400', 'a_600', 'a_800', 'a_1000'],
            'n_obs': 2199,
            'r_squared': 0.0939
        }
    }

    exp = expected[mwe_num]
    print(f"\n--- Comparison with Stata ---")
    print(f"Expected dropped: {exp['dropped']}")
    print(f"Expected n_obs: {exp['n_obs']}")
    print(f"Expected R-squared: {exp['r_squared']:.4f}")


#%%


"""Run tests for MWE 1-3."""
for mwe_num in [1, 2, 3]:
    test_regress(mwe_num)

