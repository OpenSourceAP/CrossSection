# Plan: modify do files to provide more information on the test failures 

# Task

Unless otherwise specified, work on the first TBC script under the "Progress Tracking" section.

## Task 1: get information on bad observations

- Run the `pyCode/Predictors/*.py` script 
- Run `python3 utils/test_predictors.py --predictors PREDICTOR_NAME`
- Check `Logs/testout_predictors.md` for the bad observations
    - Bad observations are identified by permno and yyyymm combinations
    - Use **Largest Differences Before 1950**, if data is available
    - Otherwise, use **Largest Differences**

## Task 2: edit `do` file so that it nicely outputs information on the bad observations

- Read the `Code/Predictors/*.do` file
- Think about the key lines of code where the calculations may be hard to translate
- Add checkpoints at these key lines
    - use `list` to print data on the bad observations
        - be sure to print only the bad permnos
        - be sure to print only the dates near the bad yyyymm
        - check the proper date syntax, it depends on whether the date is a monthly or daily date
    - if `fastxtile` or `xtile` is used, print the related quantiles    
    - clearly mark these debug lines with a comment `- CHECKPOINT N` where N is the checkpoint number

## Task 3: edit the `py` script to match the updated `do` file

- Edit the `py` script to match the updated `do` file
  - For each checkpoint in the `do` file, make the corresponding console output in the `py` script.

STOP HERE. Do not run the scripts.

# Stata Syntax
- `time_avail_m` is a monthly date. To filter, use `if time_avail_m == tm(2007m4)`
  - Do NOT use `if time_avail_m >= 200704`
- `time_d` is a daily date. To filter, use `if time_d == td(01jan2007)`
- `permno` is an integer. To filter, use `if permno == 10051`

# Progress Tracking

- TrendFactor: DONE
- AbnormalAccruals: DONE
- CitationsRD: DONE
- BetaFP: COMPLETED
- OrgCap: COMPLETED
- RDAbility: COMPLETED
- ResidualMomentum: COMPLETED
- PriceDelayRsq: COMPLETED

