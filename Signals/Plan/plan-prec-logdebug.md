# Plan use logs from do files to debug precision failures

## Task: use the do file logs to debug the precision failures

- For the requested predictor, read the do file log in `Human/Logs/*.log`
    - If no predictor is requested, work on the first TBC predictor in the list below.
- Run and test the corresponding python script 
    - run script in `pyCode/Predictors/*.py`
    - test with `python3 utils/test_predictors.py --predictors [predictor_name]`
    - *IMPORTANT*: you need to run both scripts. The existing results may be stale.
- Compare the output of the python script with the do file log
    - Identify the checkpoint where the bad observations start to deviate
- Think of up to three hypotheses for the problems and test them. 
    - Think ultra hard. We've been stuck on this for a while.
    - Check `DocsForClaude/traps.md` for common pitfalls 
    - Write py scripts in `Debug/` to test the hypotheses
      - Do NOT edit the `py` script for the predictor in this step.
    - If your hypothesis is that the underlying data is different, check the underlying datasets that are being imported in the `do` file and the `py` script.
- Attempt to fix the problem in the `py` script
    - Once your hypothesis is confirmed, edit the `py` script to fix the problem
    - Test with `python3 utils/test_predictors.py --predictors [predictor_name]`
    - Iterate

## Progress Tracking

List of scripts to debug is below.

### Group 1

- BetaTailRisk: ✅ COMPLETED
- DivSeason: ATTEMPTED
  - no improvement in tests despite improved logic.
- EarnSupBig: ATTEMPTED
  - no improvement
- IndMom: ✅ COMPLETED
- IndRetBig: ✅ COMPLETED

## Group 2

- MS: IMPROVED
  - Issue: Position-based vs time-based rolling windows in quarterly aggregations and volatility measures
  - Root cause: Stata's `asrol window(time_avail_m 12)` uses calendar-based windows, Python's `rolling(12)` uses consecutive observations
  - Fix: Implemented time-based rolling using pandas `rolling('366D')` for 12-month and `rolling('1470D')` for 48-month windows
  - Result: Precision improved from 32.967% to 19.575% failure (40.6% improvement)
  - Bias improvement: Slope from 0.7565 to 0.9252 (22.4% closer to perfect correlation)
  - R-squared improvement: 0.5782 to 0.8765 (51.6% better model fit)
  - Status: Remaining 19.575% failures likely due to industry median calculations, missing data edge cases, or timing logic
- NumEarnIncrease: ✅ COMPLETED
  - Issue: Missing chearn values treated differently in Stata vs Python
  - Root cause: Stata treats missing values as positive infinity in comparisons (chearn > 0 = TRUE when missing)
  - Fix: Modified all nincr assignment conditions to include `| df['chearn'].isna()` to treat missing chearn as positive
  - Result: Precision improved from 1.010% failure to 0.009% success (all tests passed)
- PS: TBC
- Tax: TBC
- VolumeTrend: TBC
- retConglomerate: TBC