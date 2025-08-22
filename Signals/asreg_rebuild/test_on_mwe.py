#%%

# ABOUTME: Test script for stata_regress module using MWE data
# ABOUTME: Runs regression with collinearity detection on MWE 1-3

# Inputs: mwe/tf_mwe1.csv, mwe/tf_mwe2.csv, mwe/tf_mwe3.csv
# Outputs: Regression results matching Stata format
# How to run: python3 test_on_mwe.py

import numpy as np
import pandas as pd
from stata_regress import regress

#%%
# Define Functions

def stata_regress_to_df(log_file_path):
    """
    Extract coefficients and standard errors from Stata log file.
    
    Parameters
    ----------
    log_file_path : str
        Path to the Stata .log file
        
    Returns
    -------
    pd.DataFrame
        DataFrame with variable names as index and columns: 'coefficient', 'std_err', 'omitted'
        Omitted variables have coefficient=0.0, std_err=None, and omitted=True
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
            coefficients[var_name] = {'coefficient': 0.0, 'std_err': None, 'omitted': True}
        else:
            # Parse coefficient and standard error
            parts = coef_part.split()
            if len(parts) >= 2:
                try:
                    coef = float(parts[0])
                    std_err = float(parts[1])
                    coefficients[var_name] = {'coefficient': coef,
                                              'std_err': std_err,
                                              'omitted': False}
                except (ValueError, IndexError):
                    continue

    # Convert to DataFrame
    df = pd.DataFrame.from_dict(coefficients, orient='index')
    return df



def regress_out_to_df(model, kept_vars, dropped_vars, original_vars):
    """
    Convert regress output to DataFrame format matching Stata coefficient table.

    Parameters
    ----------
    model : statsmodels regression results
        The fitted model from regress()
    kept_vars : list
        Variables kept in the model
    dropped_vars : list
        Variables dropped due to collinearity
    original_vars : list
        Original variable names in order

    Returns
    -------
    pd.DataFrame
        DataFrame with columns: coefficient, std_err, omitted
        Index contains variable names including _cons
    """
    results = {}
    # Process kept variables (have actual coefficients)
    for i, var in enumerate(kept_vars):
        results[var] = {
            'coefficient': model.params.iloc[i],
            'std_err': model.bse.iloc[i],
            'omitted': False
        }

    # Process dropped variables (omitted due to collinearity)
    for var in dropped_vars:
        results[var] = {
            'coefficient': 0.000000,
            'std_err': np.nan,
            'omitted': True
        }

    # Add constant term
    const_idx = len(kept_vars)  # Constant is last in statsmodels
    results['_cons'] = {
        'coefficient': model.params.iloc[const_idx],
        'std_err': model.bse.iloc[const_idx],
        'omitted': False
    }

    # Create DataFrame in original variable order, then add _cons
    ordered_vars = [var for var in original_vars if var in results] + ['_cons']
    ordered_results = {var: results[var] for var in ordered_vars}

    df = pd.DataFrame.from_dict(ordered_results, orient='index')
    return df

def compare_results(python_df, stata_df):
    """
    Compare Python and Stata regression results.
    
    Parameters
    ----------
    python_df : pd.DataFrame
        DataFrame with columns: coefficient, std_err, omitted
    stata_df : pd.DataFrame  
        DataFrame with columns: coefficient, std_err, omitted
        
    Returns
    -------
    pd.DataFrame
        Comparison DataFrame with columns: name, coef, se, stata, python, diff
    """
    # Get union of all variable names
    all_vars = list(set(python_df.index.tolist() + stata_df.index.tolist()))
    
    comparison_data = []
    
    for var in all_vars:
        # Get Python results
        if var in python_df.index:
            py_coef = python_df.loc[var, 'coefficient']
            py_se = python_df.loc[var, 'std_err']
        else:
            py_coef = np.nan
            py_se = np.nan
            
        # Get Stata results  
        if var in stata_df.index:
            st_coef = stata_df.loc[var, 'coefficient']
            st_se = stata_df.loc[var, 'std_err']
        else:
            st_coef = np.nan
            st_se = np.nan
            
        # Calculate coefficient difference
        if pd.notna(py_coef) and pd.notna(st_coef):
            coef_diff = py_coef - st_coef
        else:
            coef_diff = np.nan
            
        # Calculate standard error difference  
        if pd.notna(py_se) and pd.notna(st_se):
            se_diff = py_se - st_se
        else:
            se_diff = np.nan
            
        comparison_data.append({
            'name': var,
            'coef_python': py_coef,
            'coef_stata': st_coef,
            'coef_diff': coef_diff,
            'se_python': py_se,
            'se_stata': st_se, 
            'se_diff': se_diff
        })
    
    # Create DataFrame
    result_df = pd.DataFrame(comparison_data)
    
    # Sort by variable name for consistent output
    result_df = result_df.sort_values('name').reset_index(drop=True)
    
    return result_df


# %%

# Main

MWE_NUM = 1

"""Test a specific standard regression MWE dataset."""
# Load test data from CSV
df = pd.read_csv(f'mwe/tf_mwe{MWE_NUM}.csv')

# convert all columns to lowercase
df.columns = df.columns.str.lower()

# format time_avail_m to be a datetime
df['temp'] = pd.to_datetime(df['time_avail_m'].str.replace('m', '-'), format='%Y-%m')

# Prepare X and y
x_cols = [col for col in df.columns if col.startswith('a_')]
x = df[x_cols]
y = df['fret']

print(f"\n{'='*70}")
print(f"MWE {MWE_NUM} - Regression Output")
print(f"{'='*70}\n")

# Run regression with collinearity detection
model, keep_cols, drop_cols, reasons = regress(x, y)

print(f"Kept columns: {keep_cols}")
print(f"Dropped columns: {drop_cols}")
print(f"Reasons: {reasons}\n")

# Convert Python results to DataFrame
python_results = regress_out_to_df(model, keep_cols, drop_cols, x_cols)

# Load and parse Stata results
stata_results = stata_regress_to_df(f'mwe/tf_mwe{MWE_NUM}.log')

# Compare results

# Test the function
comparison = compare_results(python_results, stata_results)
print("Comparison Results:")
print("=" * 80)
print(comparison.round(6))
print("\n")

# Summary statistics
print("Summary:")
print(f"Variables compared: {len(comparison)}")
print(f"Max coefficient difference: {comparison['coef_diff'].abs().max():.8f}")
print(f"Max std error difference: {comparison['se_diff'].abs().max():.8f}")


#%%

print(comparison)

#%%



model.params

