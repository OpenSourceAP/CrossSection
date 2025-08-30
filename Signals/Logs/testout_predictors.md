# Predictor Validation Results

**Generated**: 2025-08-30 09:26:47

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

| Predictor                 | Python CSV | Superset   | NumRows       | Precision1   | Precision2              | T-stat     |
|---------------------------|------------|------------|---------------|--------------|-------------------------|------------|
| FirmAgeMom                | ✅         | ✅ (0.00%) | ✅ (+0.0%)   | ✅ (0.0%)     | ✅ (2.7E-07)             | SKIP       |

**Overall**: 1/1 available predictors passed validation
  - Natural passes: 1
  - Overridden passes: 0
**Python CSVs**: 1/1 predictors have Python implementation
\* = Manual override applied (see Predictors/overrides.yaml for details)

## Detailed Results

### FirmAgeMom

**Status**: ✅ PASSED

**Test Results**:
- Test 1 - Superset check: ✅ PASSED
- Test 2 - NumRows check: ✅ PASSED (Python has +0.00% rows vs Stata)
- Test 3 - Precision1 check: ✅ PASSED
- Test 4 - Precision2 check: ✅ PASSED
- Test 5 - T-stat check: NA (Skipped - use --tstat to enable)

**Observations**:
- Stata:  550,434
- Python: 550,434
- Common: 550,434

**Precision1**: 0.000% obs with std_diff >= 1.00e-02 (tolerance: < 1%)

**Precision2**: 100th percentile diff = 2.70e-07 (tolerance: < 1.00e-01)

**Summary Statistics** (Common Observations):

| Statistic  |          Stata |         Python |     Difference | Std Difference |
|------------|----------------|----------------|----------------|----------------|
| count      |    550434.0000 |    550434.0000 |    550434.0000 |    550434.0000 |
| mean       |         0.0904 |         0.0904 |      -1.46e-12 |      -4.12e-12 |
| std        |         0.3547 |         0.3547 |       1.05e-08 |       2.97e-08 |
| min        |        -0.9374 |        -0.9374 |      -1.04e-06 |      -2.93e-06 |
| 25%        |        -0.0898 |        -0.0898 |      -2.60e-09 |      -7.33e-09 |
| 50%        |         0.0415 |         0.0415 |         0.0000 |         0.0000 |
| 75%        |         0.2113 |         0.2113 |       2.60e-09 |       7.33e-09 |
| max        |        27.4976 |        27.4976 |       9.60e-07 |       2.71e-06 |

**Regression Analysis** (Python ~ Stata):

- **Model**: python = -0.0000 + 1.0000 * stata
- **R-squared**: 1.0000
- **N observations**: 550,434

| Coefficient |     Estimate |    Std Error | t-statistic |   p-value |
|-------------|--------------|--------------|-------------|----------|
| Intercept   |    -2.83e-12 |     1.47e-11 |     -0.1927 |     0.847 |
| Slope       |       1.0000 |     4.01e-11 |    2.50e+10 |     0.000 |

**Feedback**:
- Num observations with std_diff >= TOL_DIFF_1: 0/550434 (0.000%)
- Stata standard deviation: 3.55e-01

---

