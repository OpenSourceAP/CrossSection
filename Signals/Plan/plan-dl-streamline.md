# Plan for streamlining DataDownloads/*.py

Some files are excessively long and complicated.

## Task for a given script

1. Think about how to reduce the number of lines of code
2. Implement the changes
3. Test the script
    - Run `utils/sum_dl.py [script_name]` to get new summary statistics
    - Compare the new summary statistics with `Logs/from-0908/sumout_dl_[script_name].md`
4. If the new summary statistics are different, try to fix it.
5. Report the results below.
    - mark with ✅ if the script is simplified and the summary statistics are IDENTICAL to the original

If no script is specified, work on the first TBC script.

## Progress Tracking

- ✅ A_CCMLinkingTable.py - Simplified from 97 to 51 lines (47% reduction). Removed duplicate imports, eliminated redundant data copying, streamlined column operations, consolidated print statements. All tests pass with identical results.
- ✅ ZH2_OptionMetricsCleaning.py - Simplified from 140 to 57 lines (59% reduction). Removed unused function, eliminated redundant logic, consolidated file operations. All tests pass with identical results.
