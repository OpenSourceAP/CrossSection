# Predictor Validation Results

**Generated**: 2025-08-31 12:47:37

**Configuration**:
- TOL_SUPERSET: 1.0%
- TOL_NUMROWS: 5.0%
- TOL_DIFF_1: 0.01
- TOL_OBS_1: 1%
- EXTREME_Q: 0.999
- TOL_DIFF_2: 0.1
- TOL_TSTAT: 0.2
- INDEX_COLS: ['permno', 'yyyymm']

## Summary

Numbers report the **FAILURE** rate. ❌ (100.00%) is BAD.

| Predictor                 | Python CSV | Superset   | NumRows       | Precision1   | Precision2    | T-stat     |
|---------------------------|------------|------------|---------------|--------------|---------------|------------|
| IdioVolAHT                | ✅         | ✅ (0.00%) | ✅ (+0.0%)   | ✅ (0.0%)     | ✅ (1.3E-04)   | SKIP       |

**Overall**: 1/1 available predictors passed validation
  - Natural passes: 1
  - Overridden passes: 0
**Python CSVs**: 1/1 predictors have Python implementation
\* = Manual override applied (see Predictors/overrides.yaml for details)

## Detailed Results

### IdioVolAHT

**Status**: ✅ PASSED

**Test Results**:
- Test 1 - Superset check: ✅ PASSED
- Test 2 - NumRows check: ✅ PASSED (Python has +0.00% rows vs Stata)
- Test 3 - Precision1 check: ✅ PASSED
- Test 4 - Precision2 check: ✅ PASSED
- Test 5 - T-stat check: NA (Skipped - use --tstat to enable)

**Observations**:
- Stata:  4,849,170
- Python: 4,849,170
- Common: 4,849,170

**Precision1**: 0.000% obs with std_diff >= 1.00e-02 (tolerance: < 1%)

**Precision2**: 100th percentile diff = 1.31e-04 (tolerance: < 1.00e-01)

**Summary Statistics** (Common Observations):

| Statistic  |          Stata |         Python |     Difference | Std Difference |
|------------|----------------|----------------|----------------|----------------|
| count      |       4.85e+06 |       4.85e+06 |       4.85e+06 |       4.85e+06 |
| mean       |         0.0300 |         0.0300 |      -1.18e-08 |      -4.46e-07 |
| std        |         0.0264 |         0.0264 |       3.13e-07 |       1.19e-05 |
| min        |       1.02e-05 |       1.02e-05 |      -5.29e-05 |        -0.0020 |
| 25%        |         0.0142 |         0.0142 |      -2.78e-17 |      -1.05e-15 |
| 50%        |         0.0232 |         0.0232 |         0.0000 |         0.0000 |
| 75%        |         0.0379 |         0.0379 |       2.78e-17 |       1.05e-15 |
| max        |         2.5092 |         2.5092 |       1.31e-05 |       4.95e-04 |

**Regression Analysis** (Python ~ Stata):

- **Model**: python = -0.0000 + 1.0000 * stata
- **R-squared**: 1.0000
- **N observations**: 4,849,170

| Coefficient |     Estimate |    Std Error | t-statistic |   p-value |
|-------------|--------------|--------------|-------------|----------|
| Intercept   |    -1.74e-08 |     2.15e-10 |    -80.6055 |     0.000 |
| Slope       |       1.0000 |     5.38e-09 |    1.86e+08 |     0.000 |

**Feedback**:
- Num observations with std_diff >= TOL_DIFF_1: 0/4849170 (0.000%)
- Stata standard deviation: 2.64e-02

---

