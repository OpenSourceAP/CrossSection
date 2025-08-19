# Plan: use logs from do files to debug

## Instructions

- For the requested predictor, read the do file log in `Human/StataLogs/*.log`
    - If no predictor is requested, work on the first TBC predictor in the list below.
- Generate the log for the corresponding python script 
    - run `cd pyCode && python3 Predictors/PREDICTOR_SCRIPT.py > ../Logs/temp-python.log`
- Compare `temp-python.log` with the do file log
    - Identify the checkpoint where the log outputs start to deviate
- Think of up to three hypotheses for the deviations and test them. 
    - Think ultra hard. We've been stuck on these problems for a while.
    - Check `DocsForClaude/traps.md` for common pitfalls 
    - Write py scripts in `Debug/` to test the hypotheses
      - Do NOT edit the `py` script for the predictor in this step.
    - If your hypothesis is that the underlying data is different, check the underlying datasets that are being imported in the `do` file and the `py` script.
- Document your findings in `Journal/`

## Progress Tracking

## Group 1
- Recomm_ShortInterest: ATTEMPTED. Do file log output is not helpful.
- Mom6mJunk: ATTEMPTED. Do filelog output is broken.
- CitationsRD: ATTEMPTED. Claude found the problem to be asrol and missing value handling. But once again the checkpoint output is not helpful.
- ZZ1_RIO_MB_RIO_Disp_RIO_Turnover_RIO_Volatility: ATTEMPTED. Do file log output is broken.

## Group 2
- TrendFactor: ATTEMPTED. The problem is with asrol edge cases that are very difficult to fix. Needs either manual intervention or a high quality set of do file outputs to match.
- ZZ2_AbnormalAccruals_AbnormalAccrualsPercent: SKIP. Prec1 differences look large, but the file is very long and has many steps and the regression test looks great. The difference is likely due to small differences in sic2 columns, combined with the long file and machine precision differences over these steps. 
- MS: ATTEMPTED. Do file log is not detailed enough, though it does show what the deviations happen before SIGNAL CONSTRUCTION, and likely happen with the asrol calls
- PS: ATTEMPTED. The do file log hinted that the problem was with position vs time based lags, and missing value handling with inequalities. Strangely, when Claude fixed these problems, the test results got worse, particularly in the regression test.
- RDAbility: IMPROVED. by enforcing minimum obs for the asreg. 

## Group 3
- ZZ1_OrgCap_OrgCapNoAdj: IMPROVED. The problem was with the tie breakers in the winsorization. Crazy how detailed this is. Also seems to be sic code issues.
- ZZ2_BetaFP: SKIP. do log failed.
- ZZ1_ResidualMomentum6m_ResidualMomentum: TBC
- ZZ0_RealizedVol_IdioVol3F_ReturnSkew3F: SKIP log failed
- ZZ2_PriceDelaySlope_PriceDelayRsq_PriceDelayTstat: SKIP do log failed
