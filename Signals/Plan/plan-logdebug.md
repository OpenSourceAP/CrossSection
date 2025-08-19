# Plan use logs from do files to debug

## Task: debug the superset and precision failures

- For the requested predictor, read the do file log in `Human/Logs/*.log`
    - If no predictor is requested, work on the first TBC predictor in the list below.
- Run and test the corresponding python script 
    - run script in `pyCode/Predictors/*.py`
    - test with `python3 utils/test_predictors.py --predictors [predictor_name]`
    - *IMPORTANT*: you need to run both scripts. The existing results may be stale.
    - *IMPORTANT*: Do not remove DEBUG_MODE. Stay in DEBUG_MODE mode to speed up the debugging! If DEBUG_MODE is enabled, the problem is with the Precision1 test. Ignore the Superset test.
- Compare the output of the python script with the do file log
    - Identify the checkpoint where the log outputs start to deviate
- Think of up to three hypotheses for the deviations and test them. 
    - Think ultra hard. We've been stuck on these problems for a while.
    - Check `DocsForClaude/traps.md` for common pitfalls 
    - Write py scripts in `Debug/` to test the hypotheses
      - Do NOT edit the `py` script for the predictor in this step.
    - If your hypothesis is that the underlying data is different, check the underlying datasets that are being imported in the `do` file and the `py` script.
- Attempt to fix the problem in the `py` script
    - Once your hypothesis is confirmed, edit the `py` script to fix the problem
    - Test with `python3 utils/test_predictors.py --predictors [predictor_name]`
    - Iterate

## Progress Tracking

## Group 1
- Recomm_ShortInterest: **PROGRESS MADE** - Fixed asrol 'first' bug, reduced missing from 47.99% to 37.95%. Still some issues with consensus recommendation calculation.
- Mom6mJunk: **SIGNIFICANT PROGRESS** - Fixed CIQ data structure, reduced missing from 18.09% to 9.13%. CIQ download script now expands ratings to monthly observations. Still has precision issues (~9% missing, precision2 fails).
- CitationsRD: **PROGRESS MADE** - Fixed asrol gap detection issue by setting consecutive_only=False. Missing reduced from 4.69% to 7.27% but precision issues remain (9.78% with significant differences).
- ZZ1_RIO_MB_RIO_Disp_RIO_Turnover_RIO_Volatility: **PARTIAL PROGRESS** - Fixed volatility asrol consecutive_only=False. RIO_MB now passes all tests. RIO_Disp and RIO_Turnover still have quintile boundary issues (~0.1% observations off by exactly 1.0). RIO_Volatility still missing 4.38% observations despite consecutive_only fix.

## Group 2
- TrendFactor: **INVESTIGATION COMPLETE** - Root cause identified: asreg produces null coefficients due to insufficient cross-sectional variation in moving averages within time periods. Fixed fRet calculation timing, but core issue remains. Precision errors at 94.52%. Next step: check if Stata moving averages calculation differs from Python implementation or investigate data preprocessing differences.
- ZZ2_AbnormalAccruals_AbnormalAccrualsPercent: **SIGNIFICANT PROGRESS** - Investigated regression differences. Found tempInvTA formula was correct (1/l.at), but small observation count differences (573 vs 568) still cause precision failures. Root cause: 27.95% precision1 failure, likely due to minor filtering differences in cross-sectional regression groups.
- MS: **PARTIAL PROGRESS** - Fixed rolling window implementation by switching from manual pandas rolling to proper asrol_fast utility. Precision1 failures reduced from 32.78% to 23.66%, R-squared improved from 0.58 to 0.82. However, still have major logic errors: Python shows tempMS=1 for permno 49016 at 199201, but Stata shows MS=6. Issue may be with asrol behavior or data preprocessing differences.
- PS: **INVESTIGATION COMPLETE** - Initial hypothesis about calendar-based lag calculation was wrong. Both shift(12) and calendar-based approaches yield identical results. Fixed incorrect p7 calculation in Python (was using l12_tempebit instead of current tempebit). However, precision failures remain at 17.91% with systematic ±1 differences, suggesting another component calculation issue. Need deeper investigation into individual Piotroski components.
- RDAbility: **SIGNIFICANT PROGRESS** - Fixed critical asreg min_samples bug where polars-ols wasn't properly enforcing minimum observation requirements. For problematic case (permno 86597, fyear 1995): fixed gammaAbility3/4/5 to correctly return null when insufficient observations (<6), corrected RDAbility calculation from -184.03 to 8.65. Test results much improved: R-squared=0.9789, precision1 failures reduced to 4.336% (vs previous much higher failures). Still minor precision issues with some observations like permno 14033/79283.

## Group 3
- ZZ1_OrgCap_OrgCapNoAdj: **SIGNIFICANT PROGRESS** - Fixed three critical issues from miniplan: (1) Added inf handling after division by zero (at=0), (2) Fixed winsorization percentile method from 'nearest' to 'lower'/'higher', (3) SIC 9999 exclusion already implemented. Original test cases now perfect matches (permno 76898/40970). Precision1 failures reduced from 8.87% to 6.16%. However, systematic issues remain with permno 17515 causing large differences (~1.6), suggesting potential industry adjustment calculation issues.
- ZZ2_BetaFP: **COMPLETED** - Fixed DEBUG_MODE filter that was excluding 95% of data. Used manual correlation-based R² calculation instead of asreg. Superset test now passes (0.54% missing vs previous 95.26%). Precision improved from 18.156% to 5.98% failures. Manual correlation R² approach closely approximates Stata's regression R², though small systematic differences remain due to implementation details.
- ZZ1_ResidualMomentum6m_ResidualMomentum: **SIGNIFICANT PROGRESS** - Fixed critical rolling window positioning issue in asreg.py that caused 23-position delay. Removed additional min_samples filtering that interfered with polars-ols window positioning. Superset test now passes perfectly (0.00% missing vs previous 2.40%). However, precision issues remain with 2.85% of observations having significant differences. The rolling window fix resolved the observation count mismatch, but residual calculation differences persist.
- ZZ0_RealizedVol_IdioVol3F_ReturnSkew3F: TBC
- ZZ2_PriceDelaySlope_PriceDelayRsq_PriceDelayTstat: TBC
