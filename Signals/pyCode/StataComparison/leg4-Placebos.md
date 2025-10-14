# Placebos Leg

Replicates `Code/03_CreatePlacebos.do`, which in turn calls scripts in `Code/Placebos/`, in alphabetical order.

## Variable Handling Rules for Placebos/

How to interpret various variable types found in pyData/Intermediate/

### Dates
- time_avail_m  
    - Convert to Period dtype with monthly frequency (M)
- datadate
    - Convert to Period dtype with monthly frequency (M)
- yyyymm
    - Convert to integer

## Requirements

### Basic requirements
- For each do file in `Code/Placebos/`, say `AMq.do` there is
  - a corresponding python script `pyCode/Placebos/AMq.py`
  - a corresponding csv file `pyData/Placebos/AMq.csv`
    - No parquet files
- Output has columns (permno, yyyymm, [placebo_name])
  - index is (permno, yyyymm), both are integers
    - index defines an "observation"
  - [placebo_name] is "AMq", "AssetGrowth_q", etc. This column contains the signal values
- The logic of each do file in `Code/Placebos/` is replicated precisely, line by line
  - Exception: the `saveplacebo.do` has an option to save in a format other than csv. Remove this option.
  - Validation checks the Simple and Precision requirements below

### Precision requirements:
**IMPORTANT**: Precision requirements are checked by running `python3 StataComparison/test_placebos.py`. This script outputs `Logs/testout_placebos.md`. Here, 'common observations' are observations that are in both Stata and Python.

1. Columns: Column names and order match exactly
  - This is trivial if the indexes match
2. Superset: Python observations are a superset of Stata observations
  - All Stata observations should be found in the Python data
  - Data source differences typically cannot explain a failure in this test
  - ***IMPORTANT: data availability issues and historical data differences rarely explain a failure in this test***
      - Check Logs/testout_dl.md shows that data availability issues happen only in:
        - **Python missing Stata rows**:
          - [CompustatAnnual](#compustatannual) (3)
          - [CRSPdistributions](#crspdistributions) (1163)
          - [m_CIQ_creditratings](#mciqcreditratings) (228480)
          - [InputOutputMomentumProcessed](#inputoutputmomentumprocessed) (12)
          - [customerMom](#customermom) (138)      
3. Precision1: For common observations, the percentage for which std_diff >= TOL_DIFF_1 is less than TOL_OBS_1. std_diff is the difference between the python and stata values, divided by the standard deviation of all stata values.
4. Precision2: For common observations, Pth percentile absolute difference < TOL_DIFF_2
