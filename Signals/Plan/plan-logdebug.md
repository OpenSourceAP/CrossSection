# Plan: use logs from do files to debug

## Instructions

- For the requested predictor, read the do file log in `Human/StataLogs/*.log`
    - If no predictor is specified, work on the first TBC script in the list below.
- Generate the log for the corresponding python script 
    - run `cd pyCode && python3 Predictors/PREDICTOR_SCRIPT.py > ../Logs/temp-python.log`
- Compare `temp-python.log` with the do file log
    - Focus on the checkpoints that provide numerical values for specific permnos and dates
    - For these checkpoints, identify the lines of code where the log outputs start to deviate
- Think of up to three hypotheses for the deviations and test them. 
    - Think hard. We've been stuck on these problems for a long time.
    - Check `DocsForClaude/traps.md` for common pitfalls 
    - Write py scripts in `Debug/` to test the hypotheses
      - Do NOT edit the `py` script for the predictor in this step.
    - If your hypothesis is that the underlying data is different, check the underlying datasets that are being imported in the `do` file and the `py` script.
- Document your findings in `Journal/`

## Progress Tracking

- TrendFactor: DONE
    - Journal entry created
    - This is a problem with asreg edge cases where the sample size is very small (early in the permno's history)
- ZZ1_OrgCap_OrgCapNoAdj: DONE
    - The log edit didn't work.
- RDAbility: TBC    
- ZZ2_AbnormalAccruals_AbnormalAccrualsPercent: TBC
- CitationsRD: TBC
- ZZ2_BetaFP: TBC
- ZZ1_ResidualMomentum6m_ResidualMomentum: TBC
- ZZ2_PriceDelaySlope_PriceDelayRsq_PriceDelayTstat: TBC
