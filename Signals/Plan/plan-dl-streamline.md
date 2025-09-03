# Plan for streamlining Predictors/*.py

Some files are excessively long and complicated.

## Task for a given script

1. Extract the dataset outputs from the script
2. Run `utils/test_dl.py --datasets [dataset_names] --skipcheck --outputname testout_dl_cur` to get the current test results
3. Implement the changes
4. Run the script
5. Run `utils/test_dl.py --datasets [dataset_names] --skipcheck --outputname testout_dl_new` to get the new test results
6. If the test results are different, think about how to fix it.
7. Report the results below.
    - mark with ✅ if the script is simplified and the test results are at least as good as the original

## Progress Tracking

- ✅ ZH2_OptionMetricsCleaning.py - Simplified from 140 to 57 lines (59% reduction). Removed unused function, eliminated redundant logic, consolidated file operations. All tests pass with identical results.