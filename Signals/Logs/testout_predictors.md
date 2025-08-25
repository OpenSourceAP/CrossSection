# Predictor Validation Results

**Generated**: 2025-08-24 22:56:05

**Configuration**:
- TOL_SUPERSET: 1.0%
- TOL_DIFF_1: 0.01
- TOL_OBS_1: 1%
- EXTREME_Q: 0.999
- TOL_DIFF_2: 0.1
- INDEX_COLS: ['permno', 'yyyymm']

## Summary

Numbers report the **FAILURE** rate. ❌ (100.00%) is BAD.

| Predictor                 | Python CSV | Columns  | Superset  | Precision1   | Precision2              |
|---------------------------|------------|----------|-----------|--------------|-------------------------|
| MomSeasonShort            | ✅         | ✅       | ✅ (0.13%)   | ✅ (0.00%)    | ✅ (99.900th diff 1.7E-07) |

**Overall**: 1/1 available predictors passed validation
  - Natural passes: 1
  - Overridden passes: 0
**Python CSVs**: 1/1 predictors have Python implementation
\* = Manual override applied (see Predictors/overrides.yaml for details)

## Detailed Results

### MomSeasonShort

**Status**: ✅ PASSED

**Test Results**:
- Test 1 - Column names: ✅ PASSED
- Test 2 - Superset check: ✅ PASSED
- Test 3 - Precision1 check: ✅ PASSED
- Test 4 - Precision2 check: ✅ PASSED

**Columns**: ['MomSeasonShort']

**Observations**:
- Stata:  3,718,320
- Python: 3,713,622
- Common: 3,713,622

**Precision1**: 0.000% obs with std_diff >= 1.00e-02 (tolerance: < 1%)

**Precision2**: 100th percentile diff = 1.74e-07 (tolerance: < 1.00e-01)

**Summary Statistics** (Common Observations):

| Statistic  |          Stata |         Python |     Difference | Std Difference |
|------------|----------------|----------------|----------------|----------------|
| count      |       3.71e+06 |       3.71e+06 |       3.71e+06 |       3.71e+06 |
| mean       |         0.0117 |         0.0117 |       1.25e-13 |       7.23e-13 |
| std        |         0.1728 |         0.1728 |       4.34e-09 |       2.51e-08 |
| min        |        -0.9957 |        -0.9957 |      -5.00e-07 |      -2.89e-06 |
| 25%        |        -0.0633 |        -0.0633 |      -1.11e-16 |      -6.43e-16 |
| 50%        |         0.0000 |         0.0000 |         0.0000 |         0.0000 |
| 75%        |         0.0690 |         0.0690 |       1.11e-16 |       6.43e-16 |
| max        |        24.0000 |        24.0000 |       4.00e-07 |       2.32e-06 |

**Regression Analysis** (Python ~ Stata):

- **Model**: python = -0.0000 + 1.0000 * stata
- **R-squared**: 1.0000
- **N observations**: 3,713,622

| Coefficient |     Estimate |    Std Error | t-statistic |   p-value |
|-------------|--------------|--------------|-------------|----------|
| Intercept   |    -9.79e-12 |     2.25e-12 |     -4.3400 |     0.000 |
| Slope       |       1.0000 |     1.30e-11 |    7.68e+10 |     0.000 |

**Feedback**:
- Num observations with std_diff >= TOL_DIFF_1: 0/3713622 (0.000%)
- Stata standard deviation: 1.73e-01

---

