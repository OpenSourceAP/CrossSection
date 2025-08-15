# Plan: modify do files to provide more information on the precision failures 

## Context

Some scripts are failing the precision tests. We've been struggling to diagnose the problem using just the `do` file and the do file output in `Data/Predictors/*.csv`. The goal is to get more information.

The goal is *not* to fix the problem, just yet. First, we're just getting helpful information.

## Task 1: edit `do` file to provide more information on the precision failure.

- Obtain a list of observations that fail the precision test
  - Run `python3 utils/test_predictors.py --predictors` on a predictor
  - Check `Logs/testout_predictors.md` "Largest Differences" for the bad permno and yyyymm combinations 
- Add to the `do` file checkpoints that output helpful information about the bad observations
  - Read the `do` file and think about key lines of code where observations may be dropped
  - At these key lines
    - use `list` to print data on the bad observations
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