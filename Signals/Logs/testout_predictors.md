# Predictor Validation Results

**Generated**: 2025-08-27 23:55:01

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
| MomOffSeason              | ✅         | ✅ (0.00%) | ✅ (+1.2%)   | ✅ (0.9%)     | ❌ (2.2E+00)             | ❌ (+2.72)  |
| Investment                | ✅         | ✅ (0.86%) | ✅ (-0.4%)   | ✅ (0.3%)     | ❌ (1.1E-01)             | ✅ (+0.04)  |
| Herf                      | ✅         | ✅ (0.20%) | ✅ (-0.2%)   | ✅ (0.2%)     | ✅ (6.2E-02)             | ✅ (+0.01)  |
| DivInit                   | ✅         | ✅ (0.00%) | ✅ (+0.0%)   | ✅ (0.1%)     | ❌ (7.3E+00)             | ❌ (-0.29)  |

**Overall**: 1/4 available predictors passed validation
  - Natural passes: 1
  - Overridden passes: 0
**Python CSVs**: 4/4 predictors have Python implementation
\* = Manual override applied (see Predictors/overrides.yaml for details)

## Detailed Results

### DivInit

**Status**: ❌ FAILED

**Test Results**:
- Test 1 - Superset check: ✅ PASSED
- Test 2 - NumRows check: ✅ PASSED (Python has +0.00% rows vs Stata)
- Test 3 - Precision1 check: ✅ PASSED
- Test 4 - Precision2 check: ❌ FAILED
- Test 5 - T-stat check: NA

**Observations**:
- Stata:  4,047,630
- Python: 4,047,630
- Common: 4,047,630

**Precision1**: 0.103% obs with std_diff >= 1.00e-02 (tolerance: < 1%)

**Precision2**: 100th percentile diff = 7.30e+00 (tolerance: < 1.00e-01)

**Summary Statistics** (Common Observations):

| Statistic  |          Stata |         Python |     Difference | Std Difference |
|------------|----------------|----------------|----------------|----------------|
| count      |       4.05e+06 |       4.05e+06 |       4.05e+06 |       4.05e+06 |
| mean       |         0.0191 |         0.0182 |      -9.33e-04 |        -0.0068 |
| std        |         0.1369 |         0.1336 |         0.0321 |         0.2344 |
| min        |         0.0000 |         0.0000 |        -1.0000 |        -7.3042 |
| 25%        |         0.0000 |         0.0000 |         0.0000 |         0.0000 |
| 50%        |         0.0000 |         0.0000 |         0.0000 |         0.0000 |
| 75%        |         0.0000 |         0.0000 |         0.0000 |         0.0000 |
| max        |         1.0000 |         1.0000 |         1.0000 |         7.3042 |

**Regression Analysis** (Python ~ Stata):

- **Model**: python = 0.0000 + 0.9486 * stata
- **R-squared**: 0.9451
- **N observations**: 4,047,630

| Coefficient |     Estimate |    Std Error | t-statistic |   p-value |
|-------------|--------------|--------------|-------------|----------|
| Intercept   |     4.99e-05 |     1.57e-05 |      3.1734 |     0.002 |
| Slope       |       0.9486 |     1.14e-04 |   8343.8411 |     0.000 |

**Feedback**:
- Num observations with std_diff >= TOL_DIFF_1: 4173/4047630 (0.103%)
- Stata standard deviation: 1.37e-01

**Most Recent Bad Observations**:
```
   permno  yyyymm  python  stata  diff
0   79145  202412       0      1    -1
1   81784  202412       0      1    -1
2   79145  202411       0      1    -1
3   79145  202410       0      1    -1
4   79145  202409       0      1    -1
5   10517  202408       0      1    -1
6   88988  202408       0      1    -1
7   10517  202407       0      1    -1
8   12009  202407       0      1    -1
9   88988  202407       0      1    -1
```

**Largest Differences**:
```
   permno  yyyymm  python  stata  diff
0   10001  200510       0      1    -1
1   10001  200511       0      1    -1
2   10001  200512       0      1    -1
3   10001  200601       0      1    -1
4   10001  200602       0      1    -1
5   10001  200603       0      1    -1
6   10056  199410       0      1    -1
7   10056  199411       0      1    -1
8   10056  199412       0      1    -1
9   10056  199501       0      1    -1
```

**Largest Differences Before 1950**:
```
   permno  yyyymm  python  stata  diff
0   10372  193609       0      1    -1
1   10372  193610       0      1    -1
2   10372  193611       0      1    -1
3   10372  193612       0      1    -1
4   10372  193701       0      1    -1
5   10372  193702       0      1    -1
6   10751  193511       0      1    -1
7   10751  193512       0      1    -1
8   10751  193601       0      1    -1
9   10751  193602       0      1    -1
```

---

### Herf

**Status**: ✅ PASSED

**Test Results**:
- Test 1 - Superset check: ✅ PASSED
- Test 2 - NumRows check: ✅ PASSED (Python has -0.20% rows vs Stata)
- Test 3 - Precision1 check: ✅ PASSED
- Test 4 - Precision2 check: ✅ PASSED
- Test 5 - T-stat check: NA

**Observations**:
- Stata:  3,158,336
- Python: 3,152,103
- Common: 3,152,103

**Precision1**: 0.191% obs with std_diff >= 1.00e-02 (tolerance: < 1%)

**Precision2**: 100th percentile diff = 6.18e-02 (tolerance: < 1.00e-01)

**Summary Statistics** (Common Observations):

| Statistic  |          Stata |         Python |     Difference | Std Difference |
|------------|----------------|----------------|----------------|----------------|
| count      |       3.15e+06 |       3.15e+06 |       3.15e+06 |       3.15e+06 |
| mean       |         0.3294 |         0.3294 |      -6.78e-07 |      -2.44e-06 |
| std        |         0.2779 |         0.2779 |         0.0036 |         0.0131 |
| min        |         0.0000 |      -1.54e-17 |        -0.5101 |        -1.8359 |
| 25%        |         0.1184 |         0.1184 |      -2.36e-09 |      -8.48e-09 |
| 50%        |         0.2537 |         0.2537 |         0.0000 |         0.0000 |
| 75%        |         0.4723 |         0.4724 |       2.68e-09 |       9.63e-09 |
| max        |         5.5471 |         5.5471 |         0.4787 |         1.7229 |

**Regression Analysis** (Python ~ Stata):

- **Model**: python = -0.0000 + 1.0000 * stata
- **R-squared**: 0.9998
- **N observations**: 3,152,103

| Coefficient |     Estimate |    Std Error | t-statistic |   p-value |
|-------------|--------------|--------------|-------------|----------|
| Intercept   |    -3.07e-06 |     3.18e-06 |     -0.9637 |     0.335 |
| Slope       |       1.0000 |     7.38e-06 | 135450.4159 |     0.000 |

**Feedback**:
- Num observations with std_diff >= TOL_DIFF_1: 6011/3152103 (0.191%)
- Stata standard deviation: 2.78e-01

---

### Investment

**Status**: ❌ FAILED

**Test Results**:
- Test 1 - Superset check: ✅ PASSED
- Test 2 - NumRows check: ✅ PASSED (Python has -0.39% rows vs Stata)
- Test 3 - Precision1 check: ✅ PASSED
- Test 4 - Precision2 check: ❌ FAILED
- Test 5 - T-stat check: NA

**Observations**:
- Stata:  2,411,862
- Python: 2,402,502
- Common: 2,391,143

**Precision1**: 0.286% obs with std_diff >= 1.00e-02 (tolerance: < 1%)

**Precision2**: 100th percentile diff = 1.07e-01 (tolerance: < 1.00e-01)

**Summary Statistics** (Common Observations):

| Statistic  |          Stata |         Python |     Difference | Std Difference |
|------------|----------------|----------------|----------------|----------------|
| count      |       2.39e+06 |       2.39e+06 |       2.39e+06 |       2.39e+06 |
| mean       |         1.0035 |         1.0027 |      -8.02e-04 |      -4.38e-04 |
| std        |         1.8324 |         1.8321 |         0.0522 |         0.0285 |
| min        |     -2512.3491 |     -2512.3180 |       -25.0000 |       -13.6435 |
| 25%        |         0.6673 |         0.6668 |      -2.22e-08 |      -1.21e-08 |
| 50%        |         0.9330 |         0.9327 |         0.0000 |         0.0000 |
| 75%        |         1.2033 |         1.2030 |       2.20e-08 |       1.20e-08 |
| max        |       253.6225 |       253.6223 |         5.2631 |         2.8723 |

**Regression Analysis** (Python ~ Stata):

- **Model**: python = -0.0002 + 0.9994 * stata
- **R-squared**: 0.9992
- **N observations**: 2,391,143

| Coefficient |     Estimate |    Std Error | t-statistic |   p-value |
|-------------|--------------|--------------|-------------|----------|
| Intercept   |    -2.18e-04 |     3.85e-05 |     -5.6554 |     0.000 |
| Slope       |       0.9994 |     1.84e-05 |  54242.1050 |     0.000 |

**Feedback**:
- Num observations with std_diff >= TOL_DIFF_1: 6834/2391143 (0.286%)
- Stata standard deviation: 1.83e+00

**Most Recent Bad Observations**:
```
   permno  yyyymm  python     stata      diff
0   12373  202605     0.0  0.684501 -0.684501
1   12497  202605     0.0  0.053676 -0.053676
2   12912  202605     0.0  0.140886 -0.140886
3   14107  202605     0.0  0.023124 -0.023124
4   16928  202605     0.0  0.117970 -0.117970
5   17122  202605     0.0  0.328346 -0.328346
6   18961  202605     0.0  0.033693 -0.033693
7   19476  202605     0.0  0.175748 -0.175748
8   19808  202605     0.0  0.149306 -0.149306
9   20397  202605     0.0  0.080427 -0.080427
```

**Largest Differences**:
```
   permno  yyyymm  python      stata       diff
0   16705  202306     0.0  25.000000 -25.000000
1   91186  201206     0.0  25.000000 -25.000000
2   19560  202406     0.0  18.475424 -18.475424
3   86990  201912     0.0  15.609619 -15.609619
4   16705  202307     0.0  13.000000 -13.000000
5   91186  201207     0.0  13.000000 -13.000000
6   19560  202407     0.0  11.049025 -11.049025
7   86990  202001     0.0   9.993940  -9.993940
8   16705  202308     0.0   9.000000  -9.000000
9   91186  201208     0.0   9.000000  -9.000000
```

**Largest Differences Before 1950**:
```
No data before 1950
```

---

### MomOffSeason

**Status**: ❌ FAILED

**Test Results**:
- Test 1 - Superset check: ✅ PASSED
- Test 2 - NumRows check: ✅ PASSED (Python has +1.18% rows vs Stata)
- Test 3 - Precision1 check: ✅ PASSED
- Test 4 - Precision2 check: ❌ FAILED
- Test 5 - T-stat check: NA

**Observations**:
- Stata:  3,396,704
- Python: 3,436,865
- Common: 3,396,704

**Precision1**: 0.893% obs with std_diff >= 1.00e-02 (tolerance: < 1%)

**Precision2**: 100th percentile diff = 2.20e+00 (tolerance: < 1.00e-01)

**Summary Statistics** (Common Observations):

| Statistic  |          Stata |         Python |     Difference | Std Difference |
|------------|----------------|----------------|----------------|----------------|
| count      |       3.40e+06 |       3.40e+06 |       3.40e+06 |       3.40e+06 |
| mean       |         0.0125 |         0.0124 |      -6.59e-05 |        -0.0024 |
| std        |         0.0270 |         0.0264 |         0.0060 |         0.2208 |
| min        |        -4.1713 |        -0.3549 |        -1.2656 |       -46.9028 |
| 25%        |       3.95e-04 |       3.59e-04 |      -5.00e-10 |      -1.85e-08 |
| 50%        |         0.0119 |         0.0118 |         0.0000 |         0.0000 |
| 75%        |         0.0240 |         0.0240 |       5.00e-10 |       1.85e-08 |
| max        |         1.5150 |         1.5150 |         3.8837 |       143.9315 |

**Regression Analysis** (Python ~ Stata):

- **Model**: python = 0.0005 + 0.9545 * stata
- **R-squared**: 0.9513
- **N observations**: 3,396,704

| Coefficient |     Estimate |    Std Error | t-statistic |   p-value |
|-------------|--------------|--------------|-------------|----------|
| Intercept   |     5.00e-04 |     3.48e-06 |    143.6172 |     0.000 |
| Slope       |       0.9545 |     1.17e-04 |   8143.1419 |     0.000 |

**Feedback**:
- Num observations with std_diff >= TOL_DIFF_1: 30342/3396704 (0.893%)
- Stata standard deviation: 2.70e-02

**Most Recent Bad Observations**:
```
   permno  yyyymm    python     stata      diff
0   11379  202412 -0.009633  0.014271 -0.023904
1   12799  202412  0.024784  0.074968 -0.050184
2   14051  202412 -0.002322 -0.003499  0.001177
3   16086  202412 -0.064238 -0.019903 -0.044335
4   16794  202412 -0.000793  0.013392 -0.014186
5   17147  202412 -0.067903 -0.071290  0.003386
6   17901  202412 -0.031193 -0.021832 -0.009361
7   18065  202412  0.002178  0.002903 -0.000726
8   18103  202412 -0.019200  0.002476 -0.021675
9   19833  202412 -0.054061 -0.049822 -0.004239
```

**Largest Differences**:
```
   permno  yyyymm    python     stata      diff
0   89169  202105 -0.287618 -4.171327  3.883708
1   44230  198407 -0.059679 -1.585526  1.525847
2   92161  199008 -0.128534 -1.574922  1.446388
3   79704  200304 -0.098913  1.166667 -1.265580
4   10097  199202 -0.105667  1.000000 -1.105667
5   77324  200102  0.013863  1.086957 -1.073094
6   10685  199512 -0.048412 -1.021461  0.973049
7   82810  200509 -0.172706 -1.145503  0.972797
8   78414  198610  0.354448  1.300000 -0.945552
9   79704  200302  0.079939  0.960578 -0.880639
```

**Largest Differences Before 1950**:
```
No data before 1950
```

---

