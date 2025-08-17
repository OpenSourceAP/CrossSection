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
- PS: ATTEMPTED
  - Issue: Dataset composition differences causing BM quintile threshold shifts
  - Root cause: Python has 295 extra observations vs Stata, shifting BM quintile thresholds and changing which observations appear in final output
  - Analysis: Verified that individual Piotroski components (p1-p9) are calculated correctly and match Stata checkpoints
  - Key finding: For permno 10193, Python gives PS=7 for Feb 1988 and PS=1 for Sep 1988, but Stata gives PS=1 for Feb and PS=6 for Sep
  - This occurs because different quintile thresholds put different months in quintile 5 (highest BM), completely changing final output composition
  - Status: Requires fixing dataset composition to exactly match Stata's 463,944 observations vs Python's 464,239 observations
- Tax: ✅ COMPLETED
  - Issue: Missing value handling in Step 3 condition `(txfo + txfed > 0 | txt > txdi) & ib <=0`
  - Root cause: When txfed is missing but txfo > 0, `txfo + txfed = NaN` and `NaN > 0 = False`, failing to trigger Tax = 1
  - Additional issue: When both txfo and txfed are missing but there's tax activity (txt, txdi) and ib <= 0, should default to Tax = 1
  - Fix: Modified condition to handle missing values separately: check if txfed missing & txfo > 0, OR if both missing with tax activity & ib <= 0
  - Result: Precision improved from 1.244% failure to 0.357% success (all tests passed)
- VolumeTrend: IMPROVED
  - Issue: Stata `winsor2 VolumeTrend, cut(1 99) replace trim` behavior differs from Python `clip()`
  - Root cause: Stata `winsor2` with `trim` option removes outliers completely (sets to missing), while Python `clip()` caps them at cutoff values
  - Additional issue: NaN/infinite values in VolumeTrend caused quantile calculation to return NaN, breaking trimming logic
  - Fix: Replaced `clip()` with proper trimming logic that sets outliers to None, and filtered infinite values before quantile calculation
  - Result: Precision improved from 1.357% to 0.963% failure (29.0% improvement)
  - Status: Very close to 1% passing threshold, remaining failures likely due to edge cases in rolling window calculations
- retConglomerate: ✅ COMPLETED
  - Issue: Missing sics1 values handled differently when converting to string in Stata vs Python
  - Root cause: In Stata, missing numeric values become "." when converted to string, but in Python NaN becomes "nan"
  - Impact: Missing sics1 → "nan" → sic2D = "na", creating 133,315 spurious industry groups that weren't dropped by the `!= '.'` filter
  - Fix: Added `segments_df['sics1'] = segments_df['sics1'].replace('nan', '.')` after string conversion to match Stata behavior
  - Result: Precision improved from 0.936% failure to 0.886% success (all tests passed, 100th percentile diff: 7.59e-02 < 1.00e-01)
  - Impact: Reduced spurious industry groups, properly dropped 276 missing SIC records, cleaner final dataset (759,500 vs 759,896 rows)

## Group 3

complicated scripts

- TrendFactor: ✅ COMPLETED
- ZZ1_OrgCap_OrgCapNoAdj: ✅ COMPLETED
- ZZ2_AbnormalAccruals_AbnormalAccrualsPercent: ✅ COMPLETED
- ZZ2_BetaFP: ✅ COMPLETED
- CitationsRD: ✅ COMPLETED

## Group 4

complicated scripts with small errors

- ZZ1_RIO_MB_RIO_Disp_RIO_Turnover_RIO_Volatility: ✅ COMPLETED
- ZZ0_RealizedVol_IdioVol3F_ReturnSkew3F: ✅ COMPLETED
- ZZ1_ResidualMomentum6m_ResidualMomentum: ✅ COMPLETED
- ZZ2_IdioVolAHT: ✅ COMPLETED


## Group 5

very small errors

- realestate: ✅ COMPLETED
- MRreversal: ✅ COMPLETED
- Mom12mOffSeason: ✅ COMPLETED
- MomOffSeason: ✅ COMPLETED
- MomOffSeason06YrPlus: ✅ COMPLETED
- MomOffSeason11YrPlus: ✅ COMPLETED
- MomVol: ✅ COMPLETED
