# Predictor Validation Results

**Generated**: 2025-09-13 19:26:38

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
| iomom_supp                | ✅ (0.00%) | ✅ (-0.0%)   | ❌ (1.2%)     | ✅ (6.1E-02)   | SKIP       |
| iomom_cust                | ✅ (0.00%) | ✅ (-0.0%)   | ✅ (0.8%)     | ✅ (3.4E-02)   | SKIP       |

**Overall**: 1/2 available predictors passed validation
  - Natural passes: 1
  - Overridden passes: 0
**Python CSVs**: 2/2 predictors have Python implementation
\* = Manual override applied (see Predictors/overrides.yaml for details)

## Detailed Results

### iomom_cust

**Status**: ✅ PASSED

**Test Results**:
- Test 1 - Superset check: ✅ PASSED
- Test 2 - NumRows check: ✅ PASSED (Python has -0.00% rows vs Stata)
- Test 3 - Precision1 check: ✅ PASSED
- Test 4 - Precision2 check: ✅ PASSED
- Test 5 - T-stat check: NA (Skipped - use --tstat to enable)

**Observations**:
- Stata:  1,637,670
- Python: 1,637,617
- Common: 1,637,610

**Precision1**: 0.773% obs with std_diff >= 1.00e-02 (tolerance: < 1%)

**Precision2**: 100th percentile diff = 3.35e-02 (tolerance: < 1.00e-01)

**Summary Statistics** (Common Observations):

| Statistic  |          Stata |         Python |     Difference | Std Difference |
|------------|----------------|----------------|----------------|----------------|
| count      |       1.64e+06 |       1.64e+06 |       1.64e+06 |       1.64e+06 |
| mean       |         1.7274 |         1.7273 |      -1.29e-04 |      -2.16e-05 |
| std        |         5.9574 |         5.9570 |         0.0466 |         0.0078 |
| min        |       -50.7987 |       -50.7987 |       -13.2564 |        -2.2252 |
| 25%        |        -1.4085 |        -1.4112 |      -2.40e-07 |      -4.02e-08 |
| 50%        |         1.8440 |         1.8444 |       1.10e-08 |       1.84e-09 |
| 75%        |         5.1077 |         5.1077 |       4.98e-06 |       8.35e-07 |
| max        |       147.0000 |       147.0000 |        17.8713 |         2.9999 |

**Regression Analysis** (Python ~ Stata):

- **Model**: python = 0.0000 + 0.9999 * stata
- **R-squared**: 0.9999
- **N observations**: 1,637,610

| Coefficient |     Estimate |    Std Error | t-statistic |   p-value |
|-------------|--------------|--------------|-------------|----------|
| Intercept   |     4.51e-05 |     3.79e-05 |      1.1906 |     0.234 |
| Slope       |       0.9999 |     6.11e-06 | 163672.2941 |     0.000 |

**Feedback**:
- Num observations with std_diff >= TOL_DIFF_1: 12659/1637610 (0.773%)
- Stata standard deviation: 5.96e+00

---

### iomom_supp

**Status**: ❌ FAILED

**Test Results**:
- Test 1 - Superset check: ✅ PASSED
- Test 2 - NumRows check: ✅ PASSED (Python has -0.00% rows vs Stata)
- Test 3 - Precision1 check: ❌ FAILED
- Test 4 - Precision2 check: ✅ PASSED
- Test 5 - T-stat check: NA (Skipped - use --tstat to enable)

**Observations**:
- Stata:  1,639,842
- Python: 1,639,789
- Common: 1,639,782

**Precision1**: 1.234% obs with std_diff >= 1.00e-02 (tolerance: < 1%)

**Precision2**: 100th percentile diff = 6.14e-02 (tolerance: < 1.00e-01)

**Summary Statistics** (Common Observations):

| Statistic  |          Stata |         Python |     Difference | Std Difference |
|------------|----------------|----------------|----------------|----------------|
| count      |       1.64e+06 |       1.64e+06 |       1.64e+06 |       1.64e+06 |
| mean       |         1.6156 |         1.6148 |      -7.10e-04 |      -1.36e-04 |
| std        |         5.2255 |         5.2245 |         0.0340 |         0.0065 |
| min        |       -46.2534 |       -46.2534 |        -5.1255 |        -0.9809 |
| 25%        |        -1.0213 |        -1.0241 |      -3.73e-05 |      -7.14e-06 |
| 50%        |         1.7934 |         1.7825 |       1.38e-07 |       2.65e-08 |
| 75%        |         4.5754 |         4.5728 |       1.46e-04 |       2.79e-05 |
| max        |       135.8487 |       135.8487 |         6.3098 |         1.2075 |

**Regression Analysis** (Python ~ Stata):

- **Model**: python = -0.0004 + 0.9998 * stata
- **R-squared**: 1.0000
- **N observations**: 1,639,782

| Coefficient |     Estimate |    Std Error | t-statistic |   p-value |
|-------------|--------------|--------------|-------------|----------|
| Intercept   |    -3.53e-04 |     2.78e-05 |    -12.7117 |     0.000 |
| Slope       |       0.9998 |     5.08e-06 | 196898.2754 |     0.000 |

**Feedback**:
- Num observations with std_diff >= TOL_DIFF_1: 20232/1639782 (1.234%)
- Stata standard deviation: 5.23e+00

**Most Recent Bad Observations**:
```
   permno  yyyymm    python     stata      diff
0   11618  202412 -6.406334 -6.345796 -0.060539
1   12913  202412 -6.406334 -6.345796 -0.060539
2   13343  202412 -6.406334 -6.345796 -0.060539
3   13766  202412 -6.406334 -6.345796 -0.060539
4   13949  202412 -6.406334 -6.345796 -0.060539
5   14169  202412 -6.406334 -6.345796 -0.060539
6   14532  202412 -6.406334 -6.345796 -0.060539
7   14632  202412 -6.406334 -6.345796 -0.060539
8   14715  202412 -7.633868 -6.017747 -1.616122
9   14855  202412 -6.406334 -6.345796 -0.060539
```

**Largest Differences**:
```
   permno  yyyymm     python      stata      diff
0   16750  202110  12.896252   6.586491  6.309761
1   22089  202411   3.868967   8.994449 -5.125481
2   22089  202307  -0.980245   3.988476 -4.968720
3   22089  202402   4.050644   8.943476 -4.892832
4   14715  202305  -4.716198   0.167605 -4.883802
5   22089  202311   8.992454  13.634898 -4.642444
6   22089  202301   7.213364  11.727923 -4.514559
7   14715  202102   6.839592   2.440022  4.399570
8   16750  202102   3.062342   7.339647 -4.277306
9   16750  202301  14.155701   9.965115  4.190586
```

**Largest Differences Before 1950**:
```
No data before 1950
```

---

