# ABOUTME: Handcode test for predictors

import pandas as pd
import yaml
import io
import sys
import gc
from datetime import datetime
from pathlib import Path
import time
import numpy as np

TOL_DIFF = 1e-6

# ==========================================
# Test Functions
# ==========================================
def test_col_names_order(stata_data, python_data):
    """
    Test if the column names and order are the same
    Out: True if the column names and order are the same, 
         else a dictionary with the column names
    """
    if stata_data.columns.tolist() == python_data.columns.tolist():
        return True
    else:
        return {
            "stata_columns": stata_data.columns.tolist(),
            "python_columns": python_data.columns.tolist()
        }

def test_python_superset_stata(stata_data, python_data):
    """
    Test if the Python observations are a superset of the Stata observations
    Out: True if the Python observations are a superset of the Stata observations,
         else a set of tuples of (permno, yyyymm) that are in the Stata observations but not in the Python observations
    """
    python_keys = set(zip(python_data['permno'], python_data['yyyymm']))
    stata_keys = set(zip(stata_data['permno'], stata_data['yyyymm']))

    return True if python_keys.issuperset(stata_keys) else (stata_keys - python_keys)

def test_common_rows_difference(stata_data, python_data, pct=95):
    """
    Keep only rows that are common on (permno, yyyymm), align them,
    and test whether the `pct`th percentile of |stata - python| is < tol_diff.
    Assumes third column in each DF is the signal.
    Out: True if the 95th percentile of the difference between the Stata and Python signals is less than TOL_DIFF,
         else the 95th percentile of the difference between the Stata and Python signals
    """
    merged = (
        stata_data.merge(
            python_data,
            on=["permno", "yyyymm"],
            suffixes=("_s", "_p"),
            how="inner",
            sort=True     
        )
    )

    if merged.empty:                      
        return "No Common Rows", 1

    s_vals = merged.iloc[:, 2].to_numpy() 
    p_vals = merged.iloc[:, 3].to_numpy() 

    diffs = np.abs(s_vals - p_vals)
    perc_diff = np.percentile(diffs, pct)
    return perc_diff < TOL_DIFF, perc_diff

# ==========================================
# Test Results
# ==========================================
# Right now manually loading data since it is just two signals
stata_acc = pd.read_csv("../../Data/Predictors/Accruals.csv")
python_acc = pd.read_csv("../../pyData/Predictors/Accruals.csv")
stata_accbm = pd.read_csv("../../Data/Predictors/AccrualsBM.csv")
python_accbm = pd.read_csv("../../pyData/Predictors/AccrualsBM.csv")

print(stata_acc.head())
print(python_acc.head())
print(stata_accbm.head())
print(python_accbm.head())

print("\n==============================")
print("🚨 BEGINNING DATA CONSISTENCY TESTS")
print("==============================")
for label, stata_data, python_data in [
    ("ACC", stata_acc, python_acc),
    ("ACCBM", stata_accbm, python_accbm)
]:
    print(f"\n========== Testing {label} ==========")
    print("--------------------------------")
    result_col_names = test_col_names_order(stata_data, python_data)
    if result_col_names is True:
        print("✅ Column names and order match.")
    else:
        print("❌ Column mismatch detected:\n")
        print("**Stata columns:**\n- " + "\n- ".join(result_col_names["stata_columns"]))
        print("\n**Python columns:**\n- " + "\n- ".join(result_col_names["python_columns"]))
    print("--------------------------------")
    result_python_superset = test_python_superset_stata(stata_data, python_data)

    if result_python_superset is True:
        print("✅ Python identifiers fully cover Stata.")
    else:
        print("❌ Identifiers missing in Python which are in Stata:\n")

        # Format the (permno, yyyymm) tuples as ints
        for permno, yyyymm in result_python_superset:
            print(f"- ({int(permno)}, {int(yyyymm)})")
    print("--------------------------------")
    passed, perc_diff = test_common_rows_difference(stata_data, python_data)

    if passed:
        print(f"✅ Signal values agree. 95th percentile diff = {perc_diff:.5e}")
    else:
        print(f"❌ Signal mismatch. 95th percentile diff = {perc_diff:.5e} (exceeds tolerance)")

print("\n==============================")

# ==========================================================
# Insert these below the data loads to test fail conditions
# ==========================================================
#stata_data = stata_data.rename(columns={stata_data.columns[2]: "monkey"})
#stata_data.loc[len(stata_data)] = [39049, 199910, 0.05483]
#stata_data.iloc[: len(stata_data) // 2, 2] = 0.5




