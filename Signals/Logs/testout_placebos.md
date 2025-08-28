# Placebo Validation Results

**Generated**: 2025-08-28 10:27:22

**Configuration**:
- TOL_SUPERSET: 0.0%
- TOL_DIFF_1: 0.01
- TOL_OBS_1: 10%
- EXTREME_Q: 0.99
- TOL_DIFF_2: 1.0
- INDEX_COLS: ['permno', 'yyyymm']

## Summary

| Placebo                   | Python CSV | Columns  | Superset  | Precision1   | Precision2              |
|---------------------------|------------|----------|-----------|--------------|-------------------------|
| pchquick                  | ✅         | ✅       | ❌ (0.01%)   | ✅ (0.24%)    | ✅ (99th diff 2.8E-09)   |

**Overall**: 0/1 available placebos passed validation
**Python CSVs**: 1/1 placebos have Python implementation

## Detailed Results

### pchquick

**Status**: ❌ FAILED

**Test Results**:
- Test 1 - Column names: ✅ PASSED
- Test 2 - Superset check: ❌ FAILED (Python missing 273 Stata observations)
- Test 3 - Precision1 check: ✅ PASSED
- Test 4 - Precision2 check: ✅ PASSED

**Columns**: ['pchquick']

**Observations**:
- Stata:  3,339,639
- Python: 3,619,047
- Common: 3,339,366

**Precision1**: 0.238% obs with std_diff >= 1.00e-02 (tolerance: < 10%)

**Precision2**: 99th percentile diff = 2.76e-09 (tolerance: < 1.00e+00)

**Summary Statistics** (Common Observations):

| Statistic  |          Stata |         Python |     Difference | Std Difference |
|------------|----------------|----------------|----------------|----------------|
| count      |       3.34e+06 |       3.34e+06 |       3.34e+06 |       3.34e+06 |
| mean       |         0.2976 |         0.3265 |         0.0289 |       6.74e-04 |
| std        |        42.9374 |        43.4447 |         6.6214 |         0.1542 |
| min        |      -111.5194 |      -111.5194 |        -9.9321 |        -0.2313 |
| 25%        |        -0.1626 |        -0.1643 |      -2.32e-09 |      -5.39e-11 |
| 50%        |         0.0000 |         0.0000 |         0.0000 |         0.0000 |
| 75%        |         0.1243 |         0.1265 |       2.34e-09 |       5.44e-11 |
| max        |     19726.1780 |     19726.1780 |      2879.3158 |        67.0585 |

**Regression Analysis** (Python ~ Stata):

- **Model**: python = 0.0290 + 1.0000 * stata
- **R-squared**: 0.9768
- **N observations**: 3,339,366

| Coefficient |     Estimate |    Std Error | t-statistic |   p-value |
|-------------|--------------|--------------|-------------|----------|
| Intercept   |       0.0290 |       0.0036 |      7.9896 |     0.000 |
| Slope       |       1.0000 |     8.44e-05 |  11849.9494 |     0.000 |

**Missing Observations Sample**:
```
 index  permno  yyyymm  pchquick
     0   10281  199711       0.0
     1   10281  199712       0.0
     2   10281  199801       0.0
     3   10281  199802       0.0
     4   10281  199803       0.0
     5   10281  199804       0.0
     6   10281  199805       0.0
     7   11396  199406       0.0
     8   11396  199407       0.0
     9   11396  199408       0.0
```

**Feedback**:
- Num observations with std_diff >= TOL_DIFF_1: 7959/3339366 (0.238%)
- Stata standard deviation: 4.29e+01

---

