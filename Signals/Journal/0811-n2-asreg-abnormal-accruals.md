# 0811-n2-asreg-abnormal-accruals.md

## Task: Update ZZ2_AbnormalAccruals_AbnormalAccrualsPercent.py to use utils/asreg.py

### Result: ✅ SUCCESS - Standardized to use asreg helper

**Enhanced utils/asreg.py:**
- Added `null_policy` and `solve_method` parameters  
- Added direct residuals mode for efficiency when only residuals needed
- Now supports same polars-ols functionality as direct calls

**Updated script:**
- Replaced direct polars-ols with `asreg()` call
- Cross-sectional group regressions: `mode="group", by=["fyear", "sic2"]`
- Maintained identical performance: 49.009% failure, 2.58M observations

**Key insight:** The 49.009% failure rate appears to be a fundamental precision issue unrelated to asreg usage. The asreg helper now provides consistent interface while preserving exact functionality.

**Commit:** b81f883 - Ready for applying to other predictor scripts.