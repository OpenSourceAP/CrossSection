# Placebo Validation Results

**Generated**: 2025-08-26 13:21:52

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
| cfpq                      | ✅         | ✅       | ❌ (0.00%)   | ✅ (0.02%)    | ✅ (99th diff 3.7E-08)   |

**Overall**: 0/1 available placebos passed validation
**Python CSVs**: 1/1 placebos have Python implementation

## Detailed Results

### cfpq

**Status**: ❌ FAILED

**Test Results**:
- Test 1 - Column names: ✅ PASSED
- Test 2 - Superset check: ❌ FAILED (Python missing 108 Stata observations)
- Test 3 - Precision1 check: ✅ PASSED
- Test 4 - Precision2 check: ✅ PASSED

**Columns**: ['cfpq']

**Observations**:
- Stata:  2,252,622
- Python: 2,268,677
- Common: 2,252,514

**Precision1**: 0.018% obs with std_diff >= 1.00e-02 (tolerance: < 10%)

**Precision2**: 99th percentile diff = 3.70e-08 (tolerance: < 1.00e+00)

**Summary Statistics** (Common Observations):

| Statistic  |          Stata |         Python |     Difference | Std Difference |
|------------|----------------|----------------|----------------|----------------|
| count      |       2.25e+06 |       2.25e+06 |       2.25e+06 |       2.25e+06 |
| mean       |       2.38e-04 |       2.33e-04 |      -5.21e-06 |      -7.26e-06 |
| std        |         0.7177 |         0.7177 |         0.0083 |         0.0115 |
| min        |      -306.2332 |      -306.2333 |        -2.4322 |        -3.3889 |
| 25%        |        -0.0228 |        -0.0228 |      -2.92e-10 |      -4.07e-10 |
| 50%        |         0.0110 |         0.0110 |      -6.36e-14 |      -8.86e-14 |
| 75%        |         0.0389 |         0.0389 |       2.92e-10 |       4.07e-10 |
| max        |       250.7536 |       250.7536 |         7.8358 |        10.9181 |

**Regression Analysis** (Python ~ Stata):

- **Model**: python = -0.0000 + 1.0000 * stata
- **R-squared**: 0.9999
- **N observations**: 2,252,514

| Coefficient |     Estimate |    Std Error | t-statistic |   p-value |
|-------------|--------------|--------------|-------------|----------|
| Intercept   |    -5.20e-06 |     5.51e-06 |     -0.9437 |     0.345 |
| Slope       |       1.0000 |     7.68e-06 | 130210.0985 |     0.000 |

**Missing Observations Sample**:
```
 index  permno  yyyymm      cfpq
     0   11545  199706  0.005822
     1   11545  199707  0.005022
     2   11545  199708  0.004506
     3   12750  198312  0.063750
     4   12750  198401  0.057955
     5   12750  198402  0.057212
     6   12837  198004  0.174127
     7   12837  198005  0.106415
     8   13014  201403 -0.042416
     9   13014  201404 -0.041711
```

**Feedback**:
- Num observations with std_diff >= TOL_DIFF_1: 416/2252514 (0.018%)
- Stata standard deviation: 7.18e-01

---

