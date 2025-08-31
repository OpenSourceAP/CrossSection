# Plan for streamlining Predictors/*.py

Some files are excessively long and complicated.

## Task for a given script

1. Read the script. Think about how it can be simplified.
    - Consider using `utils/save_standardized.py` to simplify the saving process
    - Consider using `utils/asrol.py` to simplify the rolling window means and standard deviations
    - Consider using `utils/stata_replication.py`'s `stata_multi_lag` to simplify the lagging operations (but only if it actually makes things simpler)
2. Implement the changes
3. Run the script
4. Run `utils/test_predictor --predictors [script_name]`
5. Compare the test results with `Logs/testout_predictors 0831n2.md`
    - search for the predictor name in the file
6. If the test results are different, think about how to fix it.
7. Report the results below.
    - mark with ✅ if the script is simplified and the test results are at least as good as the original

## Progress Tracking
- ChNAnalyst.py 