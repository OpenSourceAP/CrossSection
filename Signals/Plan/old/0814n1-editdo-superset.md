# Plan: modify do files to provide more information on the superset failure

## Context

Some scripts are failing the superset test. We've been struggling to diagnose the problem using just the `do` file and the do file output in `Data/Predictors/*.csv`. The goal is to get more information.

The goal is *not* to fix the problem, just yet. First, we're just getting helpful information.

## Task 1: edit `do` file to provide more information on the superset failure.

- Obtain a list of observations that are in Stata but not in Python
  - Run `python3 utils/test_predictors.py --predictors` on a predictor
  - Check `Logs/testout_predictors.md` "Missing Observations Sample" for the permno and yyyymm combinations that are missing
- Add to the `do` file checkpoints that output helpful information about the missing observations
  - Read the `do` file and think about key lines of code where observations may be dropped
  - At these key lines
    - use `list` to print data on the missing observations
    - if `fastxtile` or `xtile` is used, print the related quantiles    
    - clearly mark these debug lines with a comment `* CHECKPOINT N` where N is the checkpoint number
  - The console output of the `do` file will be retrieved and used by a future Claude Code session to debug the issue

## Task 2: edit the `py` script to match the updated `do` file

- Edit the `py` script to match the updated `do` file
  - For each checkpoint in the `do` file, make the corresponding console output in the `py` script

## Stata Syntax
- `time_avail_m` is a monthly date. To filter, use `if time_avail_m == tm(2007m4)`
  - Do NOT use `if time_avail_m >= 200704`
- `permno` is an integer. To filter, use `if permno == 10051`