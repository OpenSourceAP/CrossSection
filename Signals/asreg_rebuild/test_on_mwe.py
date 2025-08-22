# %%

# ABOUTME: Test script for stata_regress module using MWE data
# ABOUTME: Tests regress function that returns full coefficients with zeros for omitted vars

# Inputs: mwe/tf_mwe1.csv, mwe/tf_mwe2.csv, mwe/tf_mwe3.csv
# Outputs: Regression results matching Stata format
# How to run: python3 test_on_mwe.py

import numpy as np
import pandas as pd
from stata_regress import regress

# %%
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

    with open(log_file_path, "r") as f:
        lines = f.readlines()

    # Find coefficient table start and end
    coef_start = None
    coef_end = None

    for i, line in enumerate(lines):
        # Look for coefficient table header
        if "| Coefficient  Std. err." in line:
            coef_start = i + 1  # Start from next line (separator is already past)
        elif (
            coef_start is not None
            and line.startswith("-------------")
            and i > coef_start
        ):
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
        if "|" not in line:
            continue

        var_part, coef_part = line.split("|", 1)
        var_name = var_part.strip()
        coef_part = coef_part.strip()

        # Handle omitted variables
        if "(omitted)" in coef_part:
            coefficients[var_name] = {
                "coefficient": 0.0,
                "std_err": None,
                "omitted": True,
            }
        else:
            # Parse coefficient and standard error
            parts = coef_part.split()
            if len(parts) >= 2:
                try:
                    coef = float(parts[0])
                    std_err = float(parts[1])
                    coefficients[var_name] = {
                        "coefficient": coef,
                        "std_err": std_err,
                        "omitted": False,
                    }
                except (ValueError, IndexError):
                    continue

    # Convert to DataFrame
    df = pd.DataFrame.from_dict(coefficients, orient="index")
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
        Comparison DataFrame with columns: name, variable, python, stata, diff
    """
    py_long = pd.melt(
        python_df[["coefficient", "std_err"]],
        var_name="variable",
        value_name="python",
        ignore_index=False,
    ).reset_index()

    st_long = pd.melt(
        stata_df[["coefficient", "std_err"]],
        var_name="variable",
        value_name="stata",
        ignore_index=False,
    ).reset_index()

    both = (
        pd.merge(py_long, st_long, on=["index", "variable"], how="outer")
        .rename(columns={"index": "name"})
        .sort_values(["variable", "name"])
        .assign(diff=lambda x: x["python"] - x["stata"])
    )

    return both


# %%

# Main

MWE_NUM = 3

"""Test a specific standard regression MWE dataset."""
# Load test data from CSV
df = pd.read_csv(f"mwe/tf_mwe{MWE_NUM}.csv")

# convert all columns to lowercase
df.columns = df.columns.str.lower()

# format time_avail_m to be a datetime
df["temp"] = pd.to_datetime(df["time_avail_m"].str.replace("m", "-"), format="%Y-%m")

# Prepare X and y
x_cols = [col for col in df.columns if col.startswith("a_")]
x = df[x_cols]
y = df["fret"]

print(f"\n{'='*70}")
print(f"MWE {MWE_NUM} - Regression Output")
print(f"{'='*70}\n")

# Run regression with collinearity detection
model, keep_cols, drop_cols, reasons, python_results = regress(x, y)

print(f"Kept columns: {keep_cols}")
print(f"Dropped columns: {drop_cols}")
print(f"Reasons: {reasons}\n")

# Load and parse Stata results
stata_results = stata_regress_to_df(f"mwe/tf_mwe{MWE_NUM}.log")

# Compare results
comparison = compare_results(python_results, stata_results)
print("Comparison Results:")
print("=" * 80)
print(comparison.round(6))
print("\n")

# Summary statistics
print("Summary:")
print(f"Variables compared: {len(comparison)}")
print(f"Max coefficient difference: {comparison['diff'].abs().max():.8f}")

# Filter for coefficient and std_err differences separately
coef_diff = comparison[comparison['variable'] == 'coefficient']['diff']
se_diff = comparison[comparison['variable'] == 'std_err']['diff']
print(f"Max coefficient difference: {coef_diff.abs().max():.8f}")
print(f"Max std error difference: {se_diff.abs().max():.8f}")

#%%

