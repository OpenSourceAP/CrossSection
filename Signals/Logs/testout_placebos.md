# Placebo Validation Results

**Generated**: 2025-08-19 16:36:09

**Configuration**:
- TOL_SUPERSET: 1.0%
- TOL_DIFF_1: 0.01
- TOL_OBS_1: 10%
- EXTREME_Q: 0.99
- TOL_DIFF_2: 1.0
- INDEX_COLS: ['permno', 'yyyymm']

## Summary

| Placebo                   | Python CSV | Columns  | Superset  | Precision1   | Precision2              |
|---------------------------|------------|----------|-----------|--------------|-------------------------|
| AMq                       | ✅         | ✅       | ✅ (0.00%)   | ✅ (0.00%)    | ✅ (99th diff 3.9E-08)   |

**Overall**: 1/1 available placebos passed validation
**Python CSVs**: 1/1 placebos have Python implementation

## Detailed Results

### AMq

**Status**: ✅ PASSED

**Test Results**:
- Test 1 - Column names: ✅ PASSED
- Test 2 - Superset check: ✅ PASSED
- Test 3 - Precision1 check: ✅ PASSED
- Test 4 - Precision2 check: ✅ PASSED

**Columns**: ['AMq']

**Observations**:
- Stata:  2,584,378
- Python: 2,584,345
- Common: 2,584,335

**Precision1**: 0.000% obs with std_diff >= 1.00e-02 (tolerance: < 10%)

**Precision2**: 99th percentile diff = 3.91e-08 (tolerance: < 1.00e+00)

**Summary Statistics** (Common Observations):

| Statistic  |          Stata |         Python |     Difference | Std Difference |
|------------|----------------|----------------|----------------|----------------|
| count      |       2.58e+06 |       2.58e+06 |       2.58e+06 |       2.58e+06 |
| mean       |         3.7379 |         3.7379 |      -1.42e-05 |      -6.09e-07 |
| std        |        23.2697 |        23.2697 |         0.0149 |       6.42e-04 |
| min        |       -33.6391 |       -33.6391 |       -14.6042 |        -0.6276 |
| 25%        |         0.6615 |         0.6615 |      -2.52e-08 |      -1.08e-09 |
| 50%        |         1.4017 |         1.4017 |       9.83e-12 |       4.22e-13 |
| 75%        |         3.2088 |         3.2088 |       2.53e-08 |       1.09e-09 |
| max        |     11549.4230 |     11549.4229 |         3.4533 |         0.1484 |

**Regression Analysis** (Python ~ Stata):

- **Model**: python = -0.0000 + 1.0000 * stata
- **R-squared**: 1.0000
- **N observations**: 2,584,335

| Coefficient |     Estimate |    Std Error | t-statistic |   p-value |
|-------------|--------------|--------------|-------------|----------|
| Intercept   |    -1.30e-05 |     9.41e-06 |     -1.3758 |     0.169 |
| Slope       |       1.0000 |     3.99e-07 |    2.50e+06 |     0.000 |

**Feedback**:
- Num observations with std_diff >= TOL_DIFF_1: 12/2584335 (0.000%)
- Stata standard deviation: 2.33e+01

---

