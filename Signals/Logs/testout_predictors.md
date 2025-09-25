# Predictor Validation Results

**Generated**: 2025-09-25 16:02:32

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

| Predictor                 | Superset   | NumRows       | Precision1   | Precision2    | T-stat     |
|---------------------------|------------|---------------|--------------|---------------|------------|
| DivInit                   | ✅ (0.00%) | ✅ (+1.6%)   | ✅ (0.0%)     | ✅ (0.0E+00)   | ✅ (+0.00)  |

**Overall**: 1/1 available predictors passed validation
  - Natural passes: 1
  - Overridden passes: 0
**Python CSVs**: 1/1 predictors have Python implementation
\* = Manual override applied (see Predictors/overrides.yaml for details)

## Detailed Results

### DivInit

**Status**: ✅ PASSED

**Test Results**:
- Test 1 - Superset check: ✅ PASSED
- Test 2 - NumRows check: ✅ PASSED (Python has +1.61% rows vs Stata)
- Test 3 - Precision1 check: ✅ PASSED
- Test 4 - Precision2 check: ✅ PASSED
- Test 5 - T-stat check: NA

**Observations**:
- Stata:  4,047,630
- Python: 4,112,633
- Common: 4,047,630

**Precision1**: 0.001% obs with std_diff >= 1.00e-02 (tolerance: < 1%)

**Precision2**: 100th percentile diff = 0.00e+00 (tolerance: < 1.00e-01)

**Summary Statistics** (Common Observations):

| Statistic  |          Stata |         Python |     Difference | Std Difference |
|------------|----------------|----------------|----------------|----------------|
| count      |       4.05e+06 |       4.05e+06 |       4.05e+06 |       4.05e+06 |
| mean       |         0.0191 |         0.0191 |      -2.47e-07 |      -1.80e-06 |
| std        |         0.1369 |         0.1369 |         0.0029 |         0.0209 |
| min        |         0.0000 |         0.0000 |        -1.0000 |        -7.3042 |
| 25%        |         0.0000 |         0.0000 |         0.0000 |         0.0000 |
| 50%        |         0.0000 |         0.0000 |         0.0000 |         0.0000 |
| 75%        |         0.0000 |         0.0000 |         0.0000 |         0.0000 |
| max        |         1.0000 |         1.0000 |         1.0000 |         7.3042 |

**Regression Analysis** (Python ~ Stata):

- **Model**: python = 0.0000 + 0.9998 * stata
- **R-squared**: 0.9996
- **N observations**: 4,047,630

| Coefficient |     Estimate |    Std Error | t-statistic |   p-value |
|-------------|--------------|--------------|-------------|----------|
| Intercept   |     4.03e-06 |     1.43e-06 |      2.8124 |     0.005 |
| Slope       |       0.9998 |     1.04e-05 |  96448.9896 |     0.000 |

**Feedback**:
- Num observations with std_diff >= TOL_DIFF_1: 33/4047630 (0.001%)
- Stata standard deviation: 1.37e-01

---

