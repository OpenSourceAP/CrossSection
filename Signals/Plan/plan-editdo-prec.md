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

## Progress Tracking

# Done 
BetaTailRisk ChForecastAccrual CredRatDG DivSeason EarnSupBig Herf HerfAsset IndMom IndRetBig Investment 

# Group 2

MRreversal MS Mom12mOffSeason MomOffSeason MomOffSeason06YrPlus MomOffSeason11YrPlus MomOffSeason16YrPlus MomVol NumEarnIncrease 

# Group 3

PS Tax TrendFactor VolumeTrend realestate retConglomerate 

# Group 4

ZZ0_RealizedVol_IdioVol3F_ReturnSkew3F 
ZZ1_OrgCap_OrgCapNoAdj 
ZZ1_RIO_MB_RIO_Disp_RIO_Turnover_RIO_Volatility 
ZZ1_ResidualMomentum6m_ResidualMomentum 
ZZ2_AbnormalAccruals_AbnormalAccrualsPercent 
ZZ2_BetaFP 
ZZ2_IdioVolAHT 
ZZ2_PriceDelaySlope_PriceDelayRsq_PriceDelayTstat 
