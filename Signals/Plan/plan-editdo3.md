# Plan: modify do files to provide more information on the test failures 

Some scripts are failing the `utils/test_predictors.py` tests. We've been struggling to diagnose the problem using just the `do` file and the do file output in `Data/Predictors/-.csv`. The goal is to get more information.

The goal is -not- to fix the problem, just yet. First, we're just getting helpful information.

# Tasks

Unless otherwise specified, work on the first TBC script under the "Progress Tracking" section.

## Task 1: get information on bad observations

- Run the `pyCode/Predictors/-.py` script 
- Run `python3 utils/test_predictors.py --predictors PREDICTOR_NAME`
- Check `Logs/testout_predictors.md` for which failure to focus on
    - If the Superset test fails, focus on it
    - Otherwise, focus on the Precision1 test
- Check `Logs/testout_predictors.md` for the bad observations
    - Bad observations are identified by permno and yyyymm combinations
    - For Superset failure bad observations, use **Missing Observations Sample**
    - For Precision1 failures bad observations, use
        - **Largest Differences Before 1950** (if available)
        - **Largest Differences** (otherwise)

## Task 2: edit `do` file so that it nicely outputs information on the bad observations

- Read the `Code/Predictors/-.do` file
- If a script is very slow, keep only data before 1950 early in the do file
    - Slow scripts are: ZZ2_BetaFP, ZZ2_IdioVolAHT, TrendFactor, ZZ1_IntanBM_IntanSP_IntanCFP_IntanEP, CoskewnessACX, ZZ2_betaVIX, ZZ2_AnnouncementReturn, Frontier, ZZ2_PriceDelaySlope_PriceDelayRsq_PriceDelayTstat, ZZ0_RealizedVol_IdioVol3F_ReturnSkew3F
    - Mark this debug mode clearly with `DEBUG_MODE` comment
- Think about the key lines of code where the calculations may be hard to translate
- Add checkpoints at these key lines
    - use `list` to print data on the bad observations
    - if `fastxtile` or `xtile` is used, print the related quantiles    
    - if industries (sic codes) are used, tabulate the number of observations in each industry for key observations
    - clearly mark these debug lines with a comment `- CHECKPOINT N` where N is the checkpoint number
    - ensure the checkpoints work with pre-1950 data if `DEBUG_MODE` is enabled

## Task 3: edit the `py` script to match the updated `do` file

- Edit the `py` script to match the updated `do` file
  - For each checkpoint in the `do` file, make the corresponding console output in the `py` script.

STOP HERE. Do not run the scripts.

# Stata Syntax
- `time_avail_m` is a monthly date. To filter, use `if time_avail_m == tm(2007m4)`
  - Do NOT use `if time_avail_m >= 200704`
- `permno` is an integer. To filter, use `if permno == 10051`

# Progress Tracking

## Group 1
- Recomm_ShortInterest: TBC
- Mom6mJunk: TBC
- CitationsRD: TBC
- ZZ1_RIO_MB_RIO_Disp_RIO_Turnover_RIO_Volatility: TBC

## Group 2
- TrendFactor: TBC
- AbnormalAccruals: TBC
- MS: TBC
- PS: TBC
- RDAbility: TBC

## Group 3
- ZZ1_OrgCap_OrgCapNoAdj: TBC
- ZZ2_BetaFP: TBC
- ZZ1_ResidualMomentum6m_ResidualMomentum: TBC
- ZZ0_RealizedVol_IdioVol3F_ReturnSkew3F: TBC
- ZZ2_PriceDelaySlope_PriceDelayRsq_PriceDelayTstat: TBC
