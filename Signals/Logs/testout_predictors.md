# Predictor Validation Results

**Generated**: 2025-09-17 08:44:45

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
| ChNAnalyst                | ❌ (26.34%) | ❌ (+76.3%)  | ✅ (0.0%)     | ✅ (0.0E+00)   | ✅ (+0.10)  |
| OptionVolume2             | ❌ (10.32%) | ✅ (-9.2%)   | ❌ (93.9%)    | ❌ (1.9E+01)   | ❌ (+0.51)  |

**Overall**: 0/2 available predictors passed validation
  - Natural passes: 0
  - Overridden passes: 0
**Python CSVs**: 2/2 predictors have Python implementation
\* = Manual override applied (see Predictors/overrides.yaml for details)

## Detailed Results

### ChNAnalyst

**Status**: ❌ FAILED

**Test Results**:
- Test 1 - Superset check: ❌ FAILED (Python missing 55570 Stata observations)
- Test 2 - NumRows check: ❌ FAILED (Python has +76.28% rows vs Stata)
- Test 3 - Precision1 check: ✅ PASSED
- Test 4 - Precision2 check: ✅ PASSED
- Test 5 - T-stat check: NA

**Observations**:
- Stata:  210,988
- Python: 371,936
- Common: 155,418

**Precision1**: 0.005% obs with std_diff >= 1.00e-02 (tolerance: < 1%)

**Precision2**: 100th percentile diff = 0.00e+00 (tolerance: < 1.00e-01)

**Summary Statistics** (Common Observations):

| Statistic  |          Stata |         Python |     Difference | Std Difference |
|------------|----------------|----------------|----------------|----------------|
| count      |    155418.0000 |    155418.0000 |    155418.0000 |    155418.0000 |
| mean       |         0.1566 |         0.1565 |      -2.57e-05 |      -7.08e-05 |
| std        |         0.3634 |         0.3634 |         0.0072 |         0.0197 |
| min        |         0.0000 |         0.0000 |        -1.0000 |        -2.7519 |
| 25%        |         0.0000 |         0.0000 |         0.0000 |         0.0000 |
| 50%        |         0.0000 |         0.0000 |         0.0000 |         0.0000 |
| 75%        |         0.0000 |         0.0000 |         0.0000 |         0.0000 |
| max        |         1.0000 |         1.0000 |         1.0000 |         2.7519 |

**Regression Analysis** (Python ~ Stata):

- **Model**: python = 0.0000 + 0.9997 * stata
- **R-squared**: 0.9996
- **N observations**: 155,418

| Coefficient |     Estimate |    Std Error | t-statistic |   p-value |
|-------------|--------------|--------------|-------------|----------|
| Intercept   |     1.53e-05 |     1.98e-05 |      0.7700 |     0.441 |
| Slope       |       0.9997 |     5.01e-05 |  19963.9526 |     0.000 |

**Missing Observations Sample**:
```
 index  permno  yyyymm  ChNAnalyst
     0   10003  198711         0.0
     1   10003  198712         0.0
     2   10003  198802         0.0
     3   10003  198803         0.0
     4   10003  198805         0.0
     5   10003  198809         1.0
     6   10003  198811         0.0
     7   10003  198812         0.0
     8   10003  198901         0.0
     9   10003  198902         0.0
```

**Feedback**:
- Num observations with std_diff >= TOL_DIFF_1: 8/155418 (0.005%)
- Stata standard deviation: 3.63e-01

---

### OptionVolume2

**Status**: ❌ FAILED

**Test Results**:
- Test 1 - Superset check: ❌ FAILED (Python missing 87091 Stata observations)
- Test 2 - NumRows check: ✅ PASSED (Python has -9.18% rows vs Stata)
- Test 3 - Precision1 check: ❌ FAILED
- Test 4 - Precision2 check: ❌ FAILED
- Test 5 - T-stat check: NA

**Observations**:
- Stata:  843,512
- Python: 766,055
- Common: 756,421

**Precision1**: 93.913% obs with std_diff >= 1.00e-02 (tolerance: < 1%)

**Precision2**: 100th percentile diff = 1.93e+01 (tolerance: < 1.00e-01)

**Summary Statistics** (Common Observations):

| Statistic  |          Stata |         Python |     Difference | Std Difference |
|------------|----------------|----------------|----------------|----------------|
| count      |    756421.0000 |    756421.0000 |    756421.0000 |    756421.0000 |
| mean       |         1.1995 |         1.4829 |         0.2834 |         0.1098 |
| std        |         2.5826 |        11.6045 |        11.3561 |         4.3972 |
| min        |         0.0000 |       2.97e-06 |     -1049.1393 |      -406.2357 |
| 25%        |         0.5649 |         0.4112 |        -0.2821 |        -0.1092 |
| 50%        |         0.9008 |         0.8140 |        -0.0334 |        -0.0129 |
| 75%        |         1.3604 |         1.4229 |         0.2714 |         0.1051 |
| max        |      1049.6909 |      7072.6796 |      7050.9285 |      2730.1796 |

**Regression Analysis** (Python ~ Stata):

- **Model**: python = 0.3705 + 0.9275 * stata
- **R-squared**: 0.0426
- **N observations**: 756,421

| Coefficient |     Estimate |    Std Error | t-statistic |   p-value |
|-------------|--------------|--------------|-------------|----------|
| Intercept   |       0.3705 |       0.0144 |     25.7364 |     0.000 |
| Slope       |       0.9275 |       0.0051 |    183.4665 |     0.000 |

**Feedback**:
- Num observations with std_diff >= TOL_DIFF_1: 710376/756421 (93.913%)
- Stata standard deviation: 2.58e+00

**Most Recent Bad Observations**:
```
   permno  yyyymm    python     stata      diff
0   10026  202308  2.279692  0.784778  1.494914
1   10028  202308  0.481896  0.791394 -0.309499
2   10032  202308  0.199350  0.505502 -0.306153
3   10066  202308  0.654055  1.027572 -0.373517
4   10104  202308  1.096916  1.236225 -0.139309
5   10145  202308  2.238413  1.542941  0.695471
6   10158  202308  2.489557  2.701363 -0.211806
7   10200  202308  0.582056  0.936441 -0.354385
8   10220  202308  0.462774  1.884915 -1.422141
9   10257  202308  0.714418  0.818952 -0.104534
```

**Largest Differences**:
```
   permno  yyyymm       python        stata         diff
0   31325  200702  7072.679560    21.751108  7050.928452
1   91184  201703  2760.485638     6.929793  2753.555844
2   19402  202211  2495.881829   178.229480  2317.652349
3   87601  200910  1847.323494     7.190881  1840.132613
4   83946  200502  1547.964602    14.013381  1533.951221
5   91154  201009  1271.031239     4.160315  1266.870924
6   92919  202308  1283.909067   225.710010  1058.199057
7   12356  201109     0.551604  1049.690900 -1049.139296
8   13652  201408   976.580283    11.884981   964.695302
9   31974  201212   846.547702     0.697687   845.850015
```

**Largest Differences Before 1950**:
```
No data before 1950
```

---

