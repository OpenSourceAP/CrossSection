# Plan: modify do files to provide more information on the precision failures 

Some scripts are failing the precision tests. We've been struggling to diagnose the problem using just the `do` file and the do file output in `Data/Predictors/*.csv`. The goal is to get more information.
The goal is *not* to fix the problem, just yet. First, we're just getting helpful information.

# Tasks

Unless otherwise specified, work on the first TBC script under the "Progress Tracking" section.

## Task 1: get information on bad observations

- Read `DocsForClaude/leg3-predictors.md` to understand the context.
- Run the `pyCode/Predictors/*.py` script 
- Run `python3 utils/test_predictors.py --predictors PREDICTOR_NAME`
- Check `Logs/testout_predictors.md` "**Largest Differences**" for bad permno and yyyymm combinations

## Task 2: edit `do` file so that it outputs information on the bad observations

- Read the `Code/Predictors/*.do` file
- Think about the key lines of code where the calculations may be hard to translate
- Add checkpoints at these key lines
    - use `list` to print data on the bad observations
    - if `fastxtile` or `xtile` is used, print the related quantiles    
    - if industries (sic codes) are used, tabulate the number of observations in each industry for key observations
    - clearly mark these debug lines with a comment `* CHECKPOINT N` where N is the checkpoint number

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
- BetaTailRisk: ✅ COMPLETED
- DivSeason: ✅ COMPLETED
- EarnSupBig: ✅ COMPLETED
- IndMom: ✅ COMPLETED
- IndRetBig: ✅ COMPLETED

## Group 2

- MS: ✅ COMPLETED
- NumEarnIncrease: ✅ COMPLETED
- PS: ✅ COMPLETED
- Tax: ✅ COMPLETED
- VolumeTrend: ✅ COMPLETED
- retConglomerate: ✅ COMPLETED

## Group 3

very small errors

- realestate: TBC
- MRreversal: TBC
- Mom12mOffSeason: TBC
- MomOffSeason: TBC
- MomOffSeason06YrPlus: TBC
- MomOffSeason11YrPlus: TBC
- MomVol: TBC

## Group 4

complicated scripts

- TrendFactor: TBC
- ZZ0_RealizedVol_IdioVol3F_ReturnSkew3F: TBC
- ZZ1_OrgCap_OrgCapNoAdj: TBC
- ZZ1_RIO_MB_RIO_Disp_RIO_Turnover_RIO_Volatility: TBC
- ZZ1_ResidualMomentum6m_ResidualMomentum: TBC
- ZZ2_AbnormalAccruals_AbnormalAccrualsPercent: TBC
- ZZ2_BetaFP: TBC
- ZZ2_IdioVolAHT: TBC
- ZZ2_PriceDelaySlope_PriceDelayRsq_PriceDelayTstat: TBC
