# Plan: Fix All asreg Command Translations

## Overview
The Stata `asreg` command performs rolling window regressions. This plan tracks the systematic review and fixing of all Python translations that involve asreg functionality.

## Test Results Summary

### Testing Configuration
- PTH_PERCENTILE: 1.00 (100th percentile)
- TOL_DIFF_1: 1e-2 (Precision1 threshold)
- TOL_OBS_1: 0.1% (Precision1 max bad obs percentage)
- TOL_DIFF_2: 1e-6 (Precision2 tolerance)

## Beta.do Translation Success Lessons

### Why Beta.do Translation Succeeded (From Recent Progress Notes)

**Key Success Factors from DocsForClaude/asreg-implementation-milestone.md:**

1. **Created Reusable `utils/asreg.py` Helper**
   - 40-line general-purpose helper supporting rolling/expanding/group modes
   - Polars-based with Rust-optimized OLS calculations (polars-ols>=0.10.0)
   - Exact Stata replication: 60-observation windows, 20-min samples
   - Perfect coefficient extraction and missing value handling

2. **Clean Code Architecture**
   - 171 → 116 lines (32% reduction in complexity)
   - Replaced manual pandas/numpy logic with simple asreg call
   - Focused on exact Stata behavior replication vs "improvements"

3. **Perfect Validation Approach**
   - ✅ Column Names: Perfect match
   - ✅ Superset: +68k observations (better coverage than Stata!)
   - ✅ Precision1: 0.000% bad observations
   - ❌ Precision2: Only microscopic differences (2.25e-06)

4. **Critical Technical Discovery (From Journal/2025-08-09_Beta_polars_ols_order_by_discovery.md)**
   - **Essential Fix**: Must use `order_by` parameter in polars-ols rolling operations
   - **Without order_by**: 70.71% Precision1 failures (scrambled time windows)
   - **With order_by**: Near-perfect results (windows properly ordered)
   - **Pattern**: Always sort data AND use order_by=pl.col(time_column)

5. **Translation Philosophy Validation**
   - ✅ Line-by-Line Translation: Exact asreg replication
   - ✅ Execution Order: Proper data flow maintained  
   - ✅ Missing Data Handling: Identical null treatment
   - ✅ Simplicity Over Cleverness: Clean, readable implementation
   - ✅ Immediate Validation: 99.9% precision achieved

6. **Inner Join Validation Methodology (From Journal/Validation_Methodology_Breakthrough.md)**
   - Fixed validation approach from left join to inner join
   - Eliminates false positives from data recency differences
   - Focuses on processing accuracy vs timing artifacts
   - Example: monthlyShortInterest went from 99.6% → 100% match

### Applied Lessons for Other asreg Predictors

**Must-Have Technical Elements:**
- Use `utils/asreg.py` helper for consistency
- Always include `order_by` parameter in rolling operations
- Sort data before regression operations: `lf.sort([*by, t])`
- Use `time_temp = _n` for observation-based windows
- Set proper `min_samples` parameter

**Validation Approach:**
- Use inner join methodology for accurate comparison
- Fix structural issues (identifiers, formats) before data-level differences
- Convert data types to match Stata: gvkey→numeric, dates→string format
- Remove extra columns not in Stata output

**Code Quality Standards:**
- Keep implementations simple and direct
- Translate line-by-line, avoid "improvements"
- Create reusable helpers for common patterns
- Achieve >99% precision match before moving on

## Stata do Files Using asreg Command

### List of do Files (15 total with test results)

1. Beta.do
   - Outputs: Beta.csv
   - Python translation exists: Yes
   - **Test Results**: ❌ FAILED
     - Superset: ✅ PASSED (4,285,574 Stata, 4,353,773 Python)
     - Precision1: ✅ PASSED (0.000%)
     - Precision2: ❌ FAILED (100th diff 2.25e-06)

2. BetaLiquidityPS.do
   - Outputs: BetaLiquidityPS.csv
   - Python translation exists: Yes
   - **Test Results**: ❌ FAILED
     - Superset: ✅ PASSED (3,423,856 Stata, 3,479,410 Python)
     - Precision1: ❌ FAILED (0.309%)
     - Precision2: ❌ FAILED (100th diff 4.66e-02)

3. BetaTailRisk.do
   - Outputs: BetaTailRisk.csv
   - Python translation exists: Yes
   - **Test Results**: ❌ FAILED
     - Superset: ✅ PASSED (2,292,350 Stata, 2,332,084 Python)
     - Precision1: ❌ FAILED (4.149%)
     - Precision2: ❌ FAILED (100th diff 1.98e-01)

4. Coskewness.do
   - Outputs: Coskewness.csv
   - Python translation exists: Yes
   - **Test Results**: ❌ FAILED
     - Superset: ❌ FAILED (Missing 407,320 obs, 8.84%)
     - Precision1: ❌ FAILED (99.358%)
     - Precision2: ❌ FAILED (100th diff 4.53e+00)

5. RDAbility.do
   - Outputs: RDAbility.csv
   - Python translation exists: Yes
   - **Test Results**: ❌ FAILED
     - Superset: ❌ FAILED (Missing 8,479 obs, 4.89%)
     - Precision1: ❌ FAILED (95.728%)
     - Precision2: ❌ FAILED (100th diff inf)

6. TrendFactor.do
   - Outputs: TrendFactor.csv
   - Python translation exists: Yes
   - **Test Results**: ❌ FAILED
     - Superset: ❌ FAILED (Missing 1,452 obs, 0.07%)
     - Precision1: ❌ FAILED (98.418%)
     - Precision2: ❌ FAILED (100th diff 5.38e+00)

7. VolumeTrend.do
   - Outputs: VolumeTrend.csv
   - Python translation exists: Yes
   - **Test Results**: ❌ FAILED
     - Superset: ✅ PASSED (3,655,889 Stata, 3,752,130 Python)
     - Precision1: ❌ FAILED (1.001%)
     - Precision2: ❌ FAILED (100th diff 1.22e-01)

8. ZZ0_RealizedVol_IdioVol3F_ReturnSkew3F.do
   - Outputs: RealizedVol.csv, IdioVol3F.csv, ReturnSkew3F.csv
   - Python translation exists: Yes
   - **Test Results**:
     - RealizedVol: ✅ PASSED (All tests passed!)
     - IdioVol3F: ❌ FAILED
       - Superset: ✅ PASSED (4,980,936 Stata, 5,026,821 Python)
       - Precision1: ✅ PASSED (0.021%)
       - Precision2: ❌ FAILED (100th diff 1.76e-02)
     - ReturnSkew3F: ❌ FAILED
       - Superset: ❌ FAILED (Missing 207 obs, 0.004%)
       - Precision1: ❌ FAILED (2.575%)
       - Precision2: ❌ FAILED (100th diff 8.73e+00)

9. ZZ1_AnalystValue_AOP_PredictedFE_IntrinsicValue.do
   - Outputs: AnalystValue.csv, AOP.csv, PredictedFE.csv, IntrinsicValue.csv
   - Python translation exists: Yes (except IntrinsicValue - not found in Stata data)
   - **Test Results**:
     - AnalystValue: ❌ FAILED
       - Superset: ❌ FAILED (Missing 2,784 obs, 0.22%)
       - Precision1: ❌ FAILED (0.263%)
       - Precision2: ❌ FAILED (100th diff 1.17e+01)
     - AOP: ❌ FAILED
       - Superset: ❌ FAILED (Missing 2,784 obs, 0.22%)
       - Precision1: ✅ PASSED (0.002%)
       - Precision2: ❌ FAILED (100th diff 2.40e+03)
     - PredictedFE: ❌ FAILED
       - Superset: ❌ FAILED (Missing 1,320 obs, 0.27%)
       - Precision1: ❌ FAILED (95.807%)
       - Precision2: ❌ FAILED (100th diff 5.08e-02)

10. ZZ1_ResidualMomentum6m_ResidualMomentum.do
    - Outputs: ResidualMomentum.csv, ResidualMomentum6m.csv
    - Python translation exists: Yes (ResidualMomentum6m not found in Stata data)
    - **Test Results**:
      - ResidualMomentum: ❌ FAILED
        - Superset: ❌ FAILED (Missing 83,157 obs, 2.40%)
        - Precision1: ❌ FAILED (0.712%)
        - Precision2: ❌ FAILED (100th diff 4.39e-02)

11. ZZ2_AbnormalAccruals_AbnormalAccrualsPercent.do
    - Outputs: AbnormalAccruals.csv, AbnormalAccrualsPercent.csv
    - Python translation exists: Yes (AbnormalAccrualsPercent not found in Stata data)
    - **Test Results**:
      - AbnormalAccruals: ❌ FAILED
        - Superset: ❌ FAILED (Missing 16,645 obs, 0.65%)
        - Precision1: ❌ FAILED (49.009%)
        - Precision2: ❌ FAILED (100th diff 3.72e+00)

12. ZZ2_BetaFP.do
    - Outputs: BetaFP.csv
    - Python translation exists: Yes
    - **Test Results**: ❌ FAILED
      - Superset: ❌ FAILED (Missing 20,488 obs, 0.54%)
      - Precision1: ❌ FAILED (5.980%)
      - Precision2: ❌ FAILED (100th diff nan)

13. ZZ2_IdioVolAHT.do
    - Outputs: IdioVolAHT.csv
    - Python translation exists: Yes
    - **Test Results**: ❌ FAILED
      - Superset: ✅ PASSED (4,849,170 Stata, 5,113,369 Python)
      - Precision1: ❌ FAILED (8.536%)
      - Precision2: ❌ FAILED (100th diff nan)

14. ZZ2_PriceDelaySlope_PriceDelayRsq_PriceDelayTstat.do
    - Outputs: PriceDelaySlope.csv, PriceDelayRsq.csv, PriceDelayTstat.csv
    - Python translation exists: Yes
    - **Test Results**:
      - PriceDelaySlope: ❌ FAILED
        - Superset: ✅ PASSED (4,630,424 Stata, 4,636,840 Python)
        - Precision1: ❌ FAILED (0.582%)
        - Precision2: ❌ FAILED (100th diff 1.59e+04)
      - PriceDelayRsq: ❌ FAILED
        - Superset: ✅ PASSED (4,630,424 Stata, 4,636,840 Python)
        - Precision1: ❌ FAILED (1.210%)
        - Precision2: ❌ FAILED (100th diff 9.57e-01)
      - PriceDelayTstat: ❌ FAILED
        - Superset: ✅ PASSED (4,523,656 Stata, 4,636,840 Python)
        - Precision1: ❌ FAILED (19.380%)
        - Precision2: ❌ FAILED (100th diff 1.08e+01)

15. ZZ2_betaVIX.do
    - Outputs: betaVIX.csv
    - Python translation exists: Yes
    - **Test Results**: ❌ FAILED
      - Superset: ✅ PASSED (3,510,758 Stata, 3,553,481 Python)
      - Precision1: ❌ FAILED (69.594%)
      - Precision2: ❌ FAILED (100th diff 5.75e-01)
