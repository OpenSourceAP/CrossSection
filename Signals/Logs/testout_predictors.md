# Predictor Validation Results

**Generated**: 2025-08-20 09:08:48

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
| AbnormalAccruals          | ✅         | ✅       | ❌ (10.58%)  | ❌ (29.28%)   | ❌ (99.900th diff 9.7E-01) |
| CitationsRD               | ✅         | ✅       | ❌ (4.69%)   | ❌ (6.16%)    | ❌ (99.900th diff 2.4E+00) |
| TrendFactor               | ✅         | ✅       | ✅ (0.12%)   | ❌ (97.14%)   | ❌ (99.900th diff 2.9E+00) |
| BetaFP                    | ✅         | ✅       | ✅ (0.24%)   | ❌ (6.26%)    | ❌ (99.900th diff 8.8E-01) |
| RDAbility                 | ✅         | ✅       | ✅ (0.02%)   | ❌ (4.34%)    | ❌ (99.900th diff 2.2E+00) |
| ResidualMomentum          | ✅         | ✅       | ✅ (0.00%)   | ❌ (2.85%)    | ❌ (99.900th diff 9.2E-01) |
| CredRatDG                 | ✅         | ✅       | ✅ (0.00%)   | ❌ (2.80%)    | ❌ (99.900th diff 6.6E+00) |
| ReturnSkew3F              | ✅         | ✅       | ✅ (0.00%)   | ❌ (2.57%)    | ❌ (99.900th diff 1.4E+00) |
| PriceDelayRsq             | ✅         | ✅       | ✅ (0.00%)   | ❌ (1.21%)    | ❌ (99.900th diff 1.9E+00) |
| OrgCap                    | ✅         | ✅       | ✅ (0.00%)   | ✅ (0.19%)    | ✅ (99.900th diff 1.4E-02) |

**Overall**: 1/10 available predictors passed validation
  - Natural passes: 1
  - Overridden passes: 0
**Python CSVs**: 10/10 predictors have Python implementation
\* = Manual override applied (see Predictors/overrides.yaml for details)

## Detailed Results

### AbnormalAccruals

**Status**: ❌ FAILED

**Test Results**:
- Test 1 - Column names: ✅ PASSED
- Test 2 - Superset check: ❌ FAILED (Python missing 271908 Stata observations)
- Test 3 - Precision1 check: ❌ FAILED
- Test 4 - Precision2 check: ❌ FAILED

**Columns**: ['AbnormalAccruals']

**Observations**:
- Stata:  2,570,664
- Python: 2,311,196
- Common: 2,298,756

**Precision1**: 29.278% obs with std_diff >= 1.00e-02 (tolerance: < 1%)

**Precision2**: 100th percentile diff = 9.73e-01 (tolerance: < 1.00e-01)

**Summary Statistics** (Common Observations):

| Statistic  |          Stata |         Python |     Difference | Std Difference |
|------------|----------------|----------------|----------------|----------------|
| count      |       2.30e+06 |       2.30e+06 |       2.30e+06 |       2.30e+06 |
| mean       |       1.08e-04 |       1.23e-04 |       1.48e-05 |       9.76e-05 |
| std        |         0.1514 |         0.1515 |         0.0132 |         0.0873 |
| min        |        -8.2957 |        -8.2790 |        -1.2879 |        -8.5051 |
| 25%        |        -0.0407 |        -0.0407 |      -2.46e-04 |        -0.0016 |
| 50%        |         0.0064 |         0.0063 |      -2.66e-10 |      -1.76e-09 |
| 75%        |         0.0515 |         0.0514 |       5.76e-05 |       3.80e-04 |
| max        |         2.7043 |         2.7040 |         1.4356 |         9.4807 |

**Regression Analysis** (Python ~ Stata):

- **Model**: python = 0.0000 + 0.9966 * stata
- **R-squared**: 0.9924
- **N observations**: 2,298,756

| Coefficient |     Estimate |    Std Error | t-statistic |   p-value |
|-------------|--------------|--------------|-------------|----------|
| Intercept   |     1.51e-05 |     8.71e-06 |      1.7385 |     0.082 |
| Slope       |       0.9966 |     5.75e-05 |  17326.6438 |     0.000 |

**Missing Observations Sample**:
```
 index  permno  yyyymm  AbnormalAccruals
     0   10001  199812         -0.020354
     1   10001  199901         -0.020354
     2   10001  199902         -0.020354
     3   10001  199903         -0.020354
     4   10001  199904         -0.020354
     5   10001  199905         -0.020354
     6   10001  199906         -0.020354
     7   10001  199907         -0.020354
     8   10001  199908         -0.020354
     9   10001  199909         -0.020354
```

**Feedback**:
- Num observations with std_diff >= TOL_DIFF_1: 673031/2298756 (29.278%)
- Stata standard deviation: 1.51e-01

**Most Recent Bad Observations**:
```
   permno  yyyymm    python     stata      diff
0   29946  202609  0.108293  0.092957  0.015336
1   12366  202608  0.139485  0.146414 -0.006929
2   13142  202608 -0.125493 -0.145704  0.020211
3   14033  202608  1.382135  1.391868 -0.009733
4   15623  202608 -0.091212 -0.093782  0.002570
5   16632  202608 -0.026517 -0.029087  0.002570
6   19655  202608 -0.036532 -0.038729  0.002197
7   22092  202608  0.014588  0.016372 -0.001784
8   23681  202608 -0.003675 -0.001505 -0.002170
9   24252  202608  0.088683  0.090385 -0.001702
```

**Largest Differences**:
```
   permno  yyyymm    python     stata      diff
0   84005  200106  0.148008 -1.287609  1.435617
1   84005  200107  0.148008 -1.287609  1.435617
2   84005  200108  0.148008 -1.287609  1.435617
3   85712  200103  0.237234  1.525127 -1.287893
4   85712  200104  0.237234  1.525127 -1.287893
5   85712  200105  0.237234  1.525127 -1.287893
6   77649  199709 -0.307171  0.603173 -0.910344
7   77649  199710 -0.307171  0.603173 -0.910344
8   77649  199711 -0.307171  0.603173 -0.910344
9   77649  199712 -0.307171  0.603173 -0.910344
```

**Largest Differences Before 1950**:
```
No data before 1950
```

---

### BetaFP

**Status**: ❌ FAILED

**Test Results**:
- Test 1 - Column names: ✅ PASSED
- Test 2 - Superset check: ✅ PASSED
- Test 3 - Precision1 check: ❌ FAILED
- Test 4 - Precision2 check: ❌ FAILED

**Columns**: ['BetaFP']

**Observations**:
- Stata:  3,794,018
- Python: 4,156,049
- Common: 3,784,837

**Precision1**: 6.256% obs with std_diff >= 1.00e-02 (tolerance: < 1%)

**Precision2**: 100th percentile diff = 8.77e-01 (tolerance: < 1.00e-01)

**Summary Statistics** (Common Observations):

| Statistic  |          Stata |         Python |     Difference | Std Difference |
|------------|----------------|----------------|----------------|----------------|
| count      |       3.78e+06 |       3.78e+06 |       3.78e+06 |       3.78e+06 |
| mean       |         0.9809 |         0.9797 |        -0.0012 |        -0.0019 |
| std        |         0.6411 |         0.6407 |         0.0384 |         0.0599 |
| min        |       7.25e-07 |         0.0000 |        -3.9823 |        -6.2115 |
| 25%        |         0.5198 |         0.5188 |        -0.0018 |        -0.0028 |
| 50%        |         0.8964 |         0.8954 |        -0.0010 |        -0.0016 |
| 75%        |         1.3175 |         1.3161 |      -4.94e-04 |      -7.70e-04 |
| max        |        12.6047 |        12.5623 |         4.7939 |         7.4774 |

**Regression Analysis** (Python ~ Stata):

- **Model**: python = 0.0012 + 0.9976 * stata
- **R-squared**: 0.9964
- **N observations**: 3,784,837

| Coefficient |     Estimate |    Std Error | t-statistic |   p-value |
|-------------|--------------|--------------|-------------|----------|
| Intercept   |       0.0012 |     3.61e-05 |     32.2317 |     0.000 |
| Slope       |       0.9976 |     3.08e-05 |  32422.5473 |     0.000 |

**Feedback**:
- Num observations with std_diff >= TOL_DIFF_1: 236770/3784837 (6.256%)
- Stata standard deviation: 6.41e-01

**Most Recent Bad Observations**:
```
   permno  yyyymm    python     stata      diff
0   10066  202412  0.366776  0.247929  0.118848
1   11153  202412  0.194148  0.253281 -0.059133
2   11379  202412  1.593719  1.445916  0.147803
3   12928  202412  0.551779  0.931920 -0.380141
4   13563  202412  0.903798  0.608259  0.295539
5   13828  202412  0.846968  0.970209 -0.123241
6   13878  202412  0.978277  0.966509  0.011768
7   13947  202412  2.605158  2.657374 -0.052215
8   14051  202412  3.479917  3.465529  0.014388
9   14469  202412  2.212209  1.759658  0.452551
```

**Largest Differences**:
```
   permno  yyyymm    python     stata      diff
0   11453  199312  7.664115  2.870236  4.793879
1   65622  199401  0.593349  4.575622 -3.982273
2   65622  199402  0.930784  4.732967 -3.802183
3   65622  199312  0.867006  4.276299 -3.409292
4   10872  199403  0.647807  4.045698 -3.397891
5   10216  199301  0.659991  4.034531 -3.374539
6   10872  199404  0.422160  3.782309 -3.360148
7   10216  199304  0.823704  4.174334 -3.350630
8   10216  199212  0.615237  3.899257 -3.284020
9   10872  199405  0.912626  4.134042 -3.221416
```

**Largest Differences Before 1950**:
```
   permno  yyyymm    python     stata      diff
0   14269  194112  4.258444  5.277860 -1.019417
1   13389  194108  3.766282  2.927140  0.839142
2   14269  194201  3.999881  4.830401 -0.830520
3   11797  193702  2.478371  1.648720  0.829651
4   11252  194112  4.024742  4.843852 -0.819109
5   20271  194408  1.522680  2.332971 -0.810292
6   18649  193710  1.339925  2.143693 -0.803768
7   11797  193701  2.275098  1.506865  0.768232
8   12677  192910  0.713803  1.460106 -0.746303
9   14269  194202  4.036062  4.760625 -0.724563
```

---

### CitationsRD

**Status**: ❌ FAILED

**Test Results**:
- Test 1 - Column names: ✅ PASSED
- Test 2 - Superset check: ❌ FAILED (Python missing 30252 Stata observations)
- Test 3 - Precision1 check: ❌ FAILED
- Test 4 - Precision2 check: ❌ FAILED

**Columns**: ['CitationsRD']

**Observations**:
- Stata:  645,360
- Python: 654,588
- Common: 615,108

**Precision1**: 6.157% obs with std_diff >= 1.00e-02 (tolerance: < 1%)

**Precision2**: 100th percentile diff = 2.42e+00 (tolerance: < 1.00e-01)

**Summary Statistics** (Common Observations):

| Statistic  |          Stata |         Python |     Difference | Std Difference |
|------------|----------------|----------------|----------------|----------------|
| count      |    615108.0000 |    615108.0000 |    615108.0000 |    615108.0000 |
| mean       |         0.2175 |         0.1560 |        -0.0616 |        -0.1492 |
| std        |         0.4126 |         0.3628 |         0.2404 |         0.5826 |
| min        |         0.0000 |         0.0000 |        -1.0000 |        -2.4238 |
| 25%        |         0.0000 |         0.0000 |         0.0000 |         0.0000 |
| 50%        |         0.0000 |         0.0000 |         0.0000 |         0.0000 |
| 75%        |         0.0000 |         0.0000 |         0.0000 |         0.0000 |
| max        |         1.0000 |         1.0000 |         0.0000 |         0.0000 |

**Regression Analysis** (Python ~ Stata):

- **Model**: python = 0.0000 + 0.7170 * stata
- **R-squared**: 0.6647
- **N observations**: 615,108

| Coefficient |     Estimate |    Std Error | t-statistic |   p-value |
|-------------|--------------|--------------|-------------|----------|
| Intercept   |     3.36e-13 |     3.03e-04 |    1.11e-09 |     1.000 |
| Slope       |       0.7170 |     6.49e-04 |   1104.1960 |     0.000 |

**Missing Observations Sample**:
```
 index  permno  yyyymm  CitationsRD
     0   10026  199206            0
     1   10026  199207            0
     2   10026  199208            0
     3   10026  199209            0
     4   10026  199210            0
     5   10026  199211            0
     6   10026  199212            0
     7   10026  199301            0
     8   10026  199302            0
     9   10026  199303            0
```

**Feedback**:
- Num observations with std_diff >= TOL_DIFF_1: 37872/615108 (6.157%)
- Stata standard deviation: 4.13e-01

**Most Recent Bad Observations**:
```
   permno  yyyymm  python  stata  diff
0   10163  201105     0.0      1  -1.0
1   10259  201105     0.0      1  -1.0
2   10272  201105     0.0      1  -1.0
3   10302  201105     0.0      1  -1.0
4   10382  201105     0.0      1  -1.0
5   10463  201105     0.0      1  -1.0
6   10644  201105     0.0      1  -1.0
7   10874  201105     0.0      1  -1.0
8   11038  201105     0.0      1  -1.0
9   11077  201105     0.0      1  -1.0
```

**Largest Differences**:
```
   permno  yyyymm  python  stata  diff
0   10010  199206     0.0      1  -1.0
1   10010  199207     0.0      1  -1.0
2   10010  199208     0.0      1  -1.0
3   10010  199209     0.0      1  -1.0
4   10010  199210     0.0      1  -1.0
5   10010  199211     0.0      1  -1.0
6   10010  199212     0.0      1  -1.0
7   10010  199301     0.0      1  -1.0
8   10010  199302     0.0      1  -1.0
9   10010  199303     0.0      1  -1.0
```

**Largest Differences Before 1950**:
```
No data before 1950
```

---

### CredRatDG

**Status**: ❌ FAILED

**Test Results**:
- Test 1 - Column names: ✅ PASSED
- Test 2 - Superset check: ✅ PASSED
- Test 3 - Precision1 check: ❌ FAILED
- Test 4 - Precision2 check: ❌ FAILED

**Columns**: ['CredRatDG']

**Observations**:
- Stata:  2,559,713
- Python: 2,559,715
- Common: 2,559,713

**Precision1**: 2.805% obs with std_diff >= 1.00e-02 (tolerance: < 1%)

**Precision2**: 100th percentile diff = 6.63e+00 (tolerance: < 1.00e-01)

**Summary Statistics** (Common Observations):

| Statistic  |          Stata |         Python |     Difference | Std Difference |
|------------|----------------|----------------|----------------|----------------|
| count      |       2.56e+06 |       2.56e+06 |       2.56e+06 |       2.56e+06 |
| mean       |         0.0233 |         0.0513 |         0.0280 |         0.1855 |
| std        |         0.1508 |         0.2205 |         0.1651 |         1.0949 |
| min        |         0.0000 |         0.0000 |        -1.0000 |        -6.6310 |
| 25%        |         0.0000 |         0.0000 |         0.0000 |         0.0000 |
| 50%        |         0.0000 |         0.0000 |         0.0000 |         0.0000 |
| 75%        |         0.0000 |         0.0000 |         0.0000 |         0.0000 |
| max        |         1.0000 |         1.0000 |         1.0000 |         6.6310 |

**Regression Analysis** (Python ~ Stata):

- **Model**: python = 0.0287 + 0.9698 * stata
- **R-squared**: 0.4398
- **N observations**: 2,559,713

| Coefficient |     Estimate |    Std Error | t-statistic |   p-value |
|-------------|--------------|--------------|-------------|----------|
| Intercept   |       0.0287 |     1.04e-04 |    274.7469 |     0.000 |
| Slope       |       0.9698 |     6.84e-04 |   1417.6237 |     0.000 |

**Feedback**:
- Num observations with std_diff >= TOL_DIFF_1: 71796/2559713 (2.805%)
- Stata standard deviation: 1.51e-01

**Most Recent Bad Observations**:
```
   permno  yyyymm  python  stata  diff
0   10890  202412     1.0      0   1.0
1   11600  202412     1.0      0   1.0
2   11644  202412     1.0      0   1.0
3   12060  202412     1.0      0   1.0
4   12781  202412     1.0      0   1.0
5   12877  202412     1.0      0   1.0
6   12880  202412     1.0      0   1.0
7   13168  202412     1.0      0   1.0
8   13622  202412     1.0      0   1.0
9   14239  202412     1.0      0   1.0
```

**Largest Differences**:
```
   permno  yyyymm  python  stata  diff
0   10006  198312     1.0      0   1.0
1   10006  198401     1.0      0   1.0
2   10006  198402     1.0      0   1.0
3   10006  198403     1.0      0   1.0
4   10006  198404     1.0      0   1.0
5   10006  198405     1.0      0   1.0
6   10016  199409     1.0      0   1.0
7   10016  199410     1.0      0   1.0
8   10016  199411     1.0      0   1.0
9   10016  199412     1.0      0   1.0
```

**Largest Differences Before 1950**:
```
No data before 1950
```

---

### OrgCap

**Status**: ✅ PASSED

**Test Results**:
- Test 1 - Column names: ✅ PASSED
- Test 2 - Superset check: ✅ PASSED
- Test 3 - Precision1 check: ✅ PASSED
- Test 4 - Precision2 check: ✅ PASSED

**Columns**: ['OrgCap']

**Observations**:
- Stata:  1,243,383
- Python: 1,243,528
- Common: 1,243,383

**Precision1**: 0.186% obs with std_diff >= 1.00e-02 (tolerance: < 1%)

**Precision2**: 100th percentile diff = 1.37e-02 (tolerance: < 1.00e-01)

**Summary Statistics** (Common Observations):

| Statistic  |          Stata |         Python |     Difference | Std Difference |
|------------|----------------|----------------|----------------|----------------|
| count      |       1.24e+06 |       1.24e+06 |       1.24e+06 |       1.24e+06 |
| mean       |       2.37e-10 |       2.76e-05 |       2.76e-05 |       2.78e-05 |
| std        |         0.9941 |         0.9941 |         0.0010 |         0.0010 |
| min        |        -2.3446 |        -2.3446 |        -0.1559 |        -0.1569 |
| 25%        |        -0.6402 |        -0.6402 |      -4.24e-08 |      -4.26e-08 |
| 50%        |        -0.2736 |        -0.2736 |       6.01e-10 |       6.05e-10 |
| 75%        |         0.3358 |         0.3359 |       4.52e-08 |       4.54e-08 |
| max        |        10.1323 |        10.1323 |         0.0870 |         0.0875 |

**Regression Analysis** (Python ~ Stata):

- **Model**: python = 0.0000 + 1.0000 * stata
- **R-squared**: 1.0000
- **N observations**: 1,243,383

| Coefficient |     Estimate |    Std Error | t-statistic |   p-value |
|-------------|--------------|--------------|-------------|----------|
| Intercept   |     2.76e-05 |     9.26e-07 |     29.8506 |     0.000 |
| Slope       |       1.0000 |     9.32e-07 |    1.07e+06 |     0.000 |

**Feedback**:
- Num observations with std_diff >= TOL_DIFF_1: 2310/1243383 (0.186%)
- Stata standard deviation: 9.94e-01

---

### PriceDelayRsq

**Status**: ❌ FAILED

**Test Results**:
- Test 1 - Column names: ✅ PASSED
- Test 2 - Superset check: ✅ PASSED
- Test 3 - Precision1 check: ❌ FAILED
- Test 4 - Precision2 check: ❌ FAILED

**Columns**: ['PriceDelayRsq']

**Observations**:
- Stata:  4,630,424
- Python: 4,636,840
- Common: 4,630,424

**Precision1**: 1.210% obs with std_diff >= 1.00e-02 (tolerance: < 1%)

**Precision2**: 100th percentile diff = 1.94e+00 (tolerance: < 1.00e-01)

**Summary Statistics** (Common Observations):

| Statistic  |          Stata |         Python |     Difference | Std Difference |
|------------|----------------|----------------|----------------|----------------|
| count      |       4.63e+06 |       4.63e+06 |       4.63e+06 |       4.63e+06 |
| mean       |         0.3626 |         0.3636 |         0.0010 |         0.0032 |
| std        |         0.3266 |         0.3273 |         0.0385 |         0.1179 |
| min        |       5.86e-06 |       5.86e-06 |        -0.9410 |        -2.8811 |
| 25%        |         0.0727 |         0.0727 |      -7.16e-09 |      -2.19e-08 |
| 50%        |         0.2485 |         0.2494 |      -2.94e-11 |      -9.02e-11 |
| 75%        |         0.6262 |         0.6293 |       6.55e-09 |       2.01e-08 |
| max        |         1.0000 |         1.0000 |         0.9574 |         2.9313 |

**Regression Analysis** (Python ~ Stata):

- **Model**: python = 0.0028 + 0.9952 * stata
- **R-squared**: 0.9862
- **N observations**: 4,630,424

| Coefficient |     Estimate |    Std Error | t-statistic |   p-value |
|-------------|--------------|--------------|-------------|----------|
| Intercept   |       0.0028 |     2.67e-05 |    104.3648 |     0.000 |
| Slope       |       0.9952 |     5.48e-05 |  18174.8448 |     0.000 |

**Feedback**:
- Num observations with std_diff >= TOL_DIFF_1: 56040/4630424 (1.210%)
- Stata standard deviation: 3.27e-01

**Most Recent Bad Observations**:
```
   permno  yyyymm    python     stata      diff
0   20665  202406  0.885442  0.656071  0.229371
1   20665  202405  0.885442  0.656071  0.229371
2   20665  202404  0.885442  0.656071  0.229371
3   20665  202403  0.885442  0.656071  0.229371
4   20665  202402  0.885442  0.656071  0.229371
5   20665  202401  0.885442  0.656071  0.229371
6   20665  202312  0.885442  0.656071  0.229371
7   20665  202311  0.885442  0.656071  0.229371
8   20665  202310  0.885442  0.656071  0.229371
9   20665  202309  0.885442  0.656071  0.229371
```

**Largest Differences**:
```
   permno  yyyymm    python     stata      diff
0   10066  199007  0.990682  0.033295  0.957386
1   10066  199008  0.990682  0.033295  0.957386
2   10066  199009  0.990682  0.033295  0.957386
3   10066  199010  0.990682  0.033295  0.957386
4   10066  199011  0.990682  0.033295  0.957386
5   10066  199012  0.990682  0.033295  0.957386
6   10066  199101  0.990682  0.033295  0.957386
7   10066  199102  0.990682  0.033295  0.957386
8   10066  199103  0.990682  0.033295  0.957386
9   10066  199104  0.990682  0.033295  0.957386
```

**Largest Differences Before 1950**:
```
   permno  yyyymm    python     stata      diff
0   17283  193007  0.995758  0.236111  0.759647
1   17283  193008  0.995758  0.236111  0.759647
2   17283  193009  0.995758  0.236111  0.759647
3   17283  193010  0.995758  0.236111  0.759647
4   17283  193011  0.995758  0.236111  0.759647
5   17283  193012  0.995758  0.236111  0.759647
6   17283  193101  0.995758  0.236111  0.759647
7   17283  193102  0.995758  0.236111  0.759647
8   17283  193103  0.995758  0.236111  0.759647
9   17283  193104  0.995758  0.236111  0.759647
```

---

### RDAbility

**Status**: ❌ FAILED

**Test Results**:
- Test 1 - Column names: ✅ PASSED
- Test 2 - Superset check: ✅ PASSED
- Test 3 - Precision1 check: ❌ FAILED
- Test 4 - Precision2 check: ❌ FAILED

**Columns**: ['RDAbility']

**Observations**:
- Stata:  173,266
- Python: 180,944
- Common: 173,240

**Precision1**: 4.336% obs with std_diff >= 1.00e-02 (tolerance: < 1%)

**Precision2**: 100th percentile diff = 2.17e+00 (tolerance: < 1.00e-01)

**Summary Statistics** (Common Observations):

| Statistic  |          Stata |         Python |     Difference | Std Difference |
|------------|----------------|----------------|----------------|----------------|
| count      |    173240.0000 |    173240.0000 |    173240.0000 |    173240.0000 |
| mean       |         0.4685 |         0.4644 |        -0.0040 |      -7.50e-04 |
| std        |         5.3534 |         5.2908 |         0.7769 |         0.1451 |
| min        |      -170.7315 |      -170.7315 |       -25.1031 |        -4.6892 |
| 25%        |        -0.2961 |        -0.2951 |      -1.56e-07 |      -2.91e-08 |
| 50%        |         0.4038 |         0.4001 |       5.57e-10 |       1.04e-10 |
| 75%        |         1.3891 |         1.3673 |       1.58e-07 |       2.94e-08 |
| max        |        83.8592 |        83.8592 |        35.2219 |         6.5793 |

**Regression Analysis** (Python ~ Stata):

- **Model**: python = 0.0064 + 0.9778 * stata
- **R-squared**: 0.9789
- **N observations**: 173,240

| Coefficient |     Estimate |    Std Error | t-statistic |   p-value |
|-------------|--------------|--------------|-------------|----------|
| Intercept   |       0.0064 |       0.0019 |      3.4395 |     0.001 |
| Slope       |       0.9778 |     3.45e-04 |   2837.9578 |     0.000 |

**Feedback**:
- Num observations with std_diff >= TOL_DIFF_1: 7512/173240 (4.336%)
- Stata standard deviation: 5.35e+00

**Most Recent Bad Observations**:
```
   permno  yyyymm    python     stata      diff
0   14033  202608  0.379405  0.192091  0.187314
1   14033  202607  0.379405  0.192091  0.187314
2   14033  202606  0.379405  0.192091  0.187314
3   14033  202605  0.379405  0.192091  0.187314
4   14245  202605  0.943359  0.997209 -0.053850
5   14432  202605  0.304188  0.448311 -0.144123
6   14668  202605  0.619375  0.359465  0.259910
7   15059  202605  0.805267 -4.663055  5.468322
8   16533  202605 -0.130891 -0.232203  0.101312
9   82670  202605  0.300767  0.394679 -0.093913
```

**Largest Differences**:
```
   permno  yyyymm     python      stata       diff
0   79283  200206 -24.396323 -59.618244  35.221921
1   79283  200207 -24.396323 -59.618244  35.221921
2   79283  200208 -24.396323 -59.618244  35.221921
3   79283  200209 -24.396323 -59.618244  35.221921
4   79283  200210 -24.396323 -59.618244  35.221921
5   79283  200211 -24.396323 -59.618244  35.221921
6   79283  200212 -24.396323 -59.618244  35.221921
7   79283  200301 -24.396323 -59.618244  35.221921
8   79283  200302 -24.396323 -59.618244  35.221921
9   79283  200303 -24.396323 -59.618244  35.221921
```

**Largest Differences Before 1950**:
```
No data before 1950
```

---

### ResidualMomentum

**Status**: ❌ FAILED

**Test Results**:
- Test 1 - Column names: ✅ PASSED
- Test 2 - Superset check: ✅ PASSED
- Test 3 - Precision1 check: ❌ FAILED
- Test 4 - Precision2 check: ❌ FAILED

**Columns**: ['ResidualMomentum']

**Observations**:
- Stata:  3,458,422
- Python: 3,517,891
- Common: 3,458,422

**Precision1**: 2.854% obs with std_diff >= 1.00e-02 (tolerance: < 1%)

**Precision2**: 100th percentile diff = 9.17e-01 (tolerance: < 1.00e-01)

**Summary Statistics** (Common Observations):

| Statistic  |          Stata |         Python |     Difference | Std Difference |
|------------|----------------|----------------|----------------|----------------|
| count      |       3.46e+06 |       3.46e+06 |       3.46e+06 |       3.46e+06 |
| mean       |        -0.0384 |        -0.0387 |      -3.09e-04 |      -9.38e-04 |
| std        |         0.3299 |         0.3297 |         0.0196 |         0.0593 |
| min        |        -4.1338 |        -4.1338 |        -1.4918 |        -4.5214 |
| 25%        |        -0.2366 |        -0.2368 |      -1.08e-08 |      -3.27e-08 |
| 50%        |        -0.0220 |        -0.0222 |       6.05e-10 |       1.83e-09 |
| 75%        |         0.1765 |         0.1761 |       1.26e-08 |       3.83e-08 |
| max        |         2.8989 |         2.8989 |         1.8220 |         5.5221 |

**Regression Analysis** (Python ~ Stata):

- **Model**: python = -0.0004 + 0.9976 * stata
- **R-squared**: 0.9965
- **N observations**: 3,458,422

| Coefficient |     Estimate |    Std Error | t-statistic |   p-value |
|-------------|--------------|--------------|-------------|----------|
| Intercept   |    -4.01e-04 |     1.06e-05 |    -37.9242 |     0.000 |
| Slope       |       0.9976 |     3.19e-05 |  31320.8539 |     0.000 |

**Feedback**:
- Num observations with std_diff >= TOL_DIFF_1: 98694/3458422 (2.854%)
- Stata standard deviation: 3.30e-01

**Most Recent Bad Observations**:
```
   permno  yyyymm    python     stata      diff
0   10028  202412  0.289036  0.283338  0.005699
1   10066  202412  0.502859  0.460886  0.041973
2   10107  202412 -0.795068 -0.786140 -0.008928
3   10252  202412  0.283345  0.277829  0.005516
4   10294  202412 -0.792843 -0.800530  0.007688
5   10308  202412  0.409725  0.405028  0.004697
6   10318  202412 -0.092833 -0.098400  0.005568
7   10397  202412 -0.336479 -0.339856  0.003377
8   10606  202412 -0.643135 -0.647104  0.003969
9   10629  202412  0.348657  0.343000  0.005657
```

**Largest Differences**:
```
   permno  yyyymm    python     stata      diff
0   43880  199301  1.350366 -0.471662  1.822028
1   79490  200801  0.170608 -1.534872  1.705480
2   79490  200712  0.183492 -1.389287  1.572779
3   85570  200801  0.073226  1.565069 -1.491844
4   77893  199012 -1.022008  0.420065 -1.442073
5   79490  200802 -0.083602 -1.520945  1.437344
6   79490  200803  0.000506 -1.406803  1.407309
7   43880  199303  0.941700 -0.449004  1.390704
8   84351  200603 -0.964103  0.425841 -1.389944
9   85570  200712  0.155851  1.525028 -1.369177
```

**Largest Differences Before 1950**:
```
   permno  yyyymm    python     stata      diff
0   13725  193509 -0.456978 -1.085686  0.628708
1   13725  193508 -0.570527 -1.109849  0.539321
2   13725  193506 -0.562432 -1.099878  0.537445
3   13725  193504 -0.451700 -0.988842  0.537142
4   13725  193505 -0.572521 -1.096676  0.524155
5   13725  193507 -0.594041 -1.081490  0.487448
6   13725  193503 -0.363179 -0.843710  0.480531
7   13725  193501 -0.504955 -0.972825  0.467870
8   13725  193502 -0.470708 -0.929486  0.458779
9   13725  193512 -0.732965 -1.179525  0.446559
```

---

### ReturnSkew3F

**Status**: ❌ FAILED

**Test Results**:
- Test 1 - Column names: ✅ PASSED
- Test 2 - Superset check: ✅ PASSED
- Test 3 - Precision1 check: ❌ FAILED
- Test 4 - Precision2 check: ❌ FAILED

**Columns**: ['ReturnSkew3F']

**Observations**:
- Stata:  4,978,948
- Python: 4,980,592
- Common: 4,978,741

**Precision1**: 2.575% obs with std_diff >= 1.00e-02 (tolerance: < 1%)

**Precision2**: 100th percentile diff = 1.40e+00 (tolerance: < 1.00e-01)

**Summary Statistics** (Common Observations):

| Statistic  |          Stata |         Python |     Difference | Std Difference |
|------------|----------------|----------------|----------------|----------------|
| count      |       4.98e+06 |       4.98e+06 |       4.98e+06 |       4.98e+06 |
| mean       |         0.1540 |         0.1536 |      -4.19e-04 |      -4.93e-04 |
| std        |         0.8499 |         0.8487 |         0.0940 |         0.1106 |
| min        |        -4.8206 |        -4.8206 |        -8.7287 |       -10.2706 |
| 25%        |        -0.2811 |        -0.2808 |      -2.22e-15 |      -2.61e-15 |
| 50%        |         0.1296 |         0.1295 |         0.0000 |         0.0000 |
| 75%        |         0.5701 |         0.5700 |       2.22e-15 |       2.61e-15 |
| max        |         4.7150 |         4.7150 |         5.1167 |         6.0205 |

**Regression Analysis** (Python ~ Stata):

- **Model**: python = 0.0007 + 0.9925 * stata
- **R-squared**: 0.9878
- **N observations**: 4,978,741

| Coefficient |     Estimate |    Std Error | t-statistic |   p-value |
|-------------|--------------|--------------|-------------|----------|
| Intercept   |     7.32e-04 |     4.27e-05 |     17.1416 |     0.000 |
| Slope       |       0.9925 |     4.95e-05 |  20063.9485 |     0.000 |

**Feedback**:
- Num observations with std_diff >= TOL_DIFF_1: 128182/4978741 (2.575%)
- Stata standard deviation: 8.50e-01

**Most Recent Bad Observations**:
```
   permno  yyyymm    python     stata      diff
0   10777  202412 -0.081862 -0.091706  0.009843
1   10890  202412 -2.034009 -2.020654 -0.013356
2   11369  202412 -0.138541 -0.147520  0.008979
3   11404  202412 -0.595165 -0.604012  0.008846
4   11674  202412 -0.248130 -0.262484  0.014354
5   12397  202412  0.255910  0.246951  0.008959
6   12476  202412 -1.112346 -1.139055  0.026710
7   12558  202412 -0.473364 -0.491103  0.017739
8   12680  202412  1.581095  1.593038 -0.011943
9   12753  202412 -0.725019 -0.734683  0.009664
```

**Largest Differences**:
```
   permno  yyyymm    python     stata      diff
0   10568  198212 -4.364358  4.364358 -8.728716
1   11253  198212 -4.364358  4.364358 -8.728716
2   12213  198212 -4.364358  4.364358 -8.728716
3   12491  198212 -4.364358  4.364358 -8.728716
4   13515  198212 -4.364358  4.364358 -8.728716
5   14462  198212 -4.364358  4.364358 -8.728716
6   14796  198212 -4.364358  4.364358 -8.728716
7   14964  198212 -4.364358  4.364358 -8.728716
8   15115  198212 -4.364358  4.364358 -8.728716
9   15545  198212 -4.364358  4.364358 -8.728716
```

**Largest Differences Before 1950**:
```
   permno  yyyymm    python     stata      diff
0   10284  193108 -0.043656 -4.694855  4.651200
1   15632  192904 -0.366716 -4.800000  4.433284
2   15923  193809  0.684782  4.694855 -4.010073
3   20431  194502 -4.129483 -0.185154 -3.944329
4   11738  192802 -0.664669 -4.364358  3.699689
5   15923  194208  0.000000  3.175426 -3.175426
6   15632  192903 -1.812385 -4.587317  2.774932
7   21717  194307  1.559323 -1.205178  2.764501
8   10903  193303  0.000000  2.715344 -2.715344
9   13899  193303  0.000000  2.715344 -2.715344
```

---

### TrendFactor

**Status**: ❌ FAILED

**Test Results**:
- Test 1 - Column names: ✅ PASSED
- Test 2 - Superset check: ✅ PASSED
- Test 3 - Precision1 check: ❌ FAILED
- Test 4 - Precision2 check: ❌ FAILED

**Columns**: ['TrendFactor']

**Observations**:
- Stata:  2,058,231
- Python: 2,056,292
- Common: 2,055,856

**Precision1**: 97.137% obs with std_diff >= 1.00e-02 (tolerance: < 1%)

**Precision2**: 100th percentile diff = 2.87e+00 (tolerance: < 1.00e-01)

**Summary Statistics** (Common Observations):

| Statistic  |          Stata |         Python |     Difference | Std Difference |
|------------|----------------|----------------|----------------|----------------|
| count      |       2.06e+06 |       2.06e+06 |       2.06e+06 |       2.06e+06 |
| mean       |         0.2096 |         0.1784 |        -0.0312 |        -0.2029 |
| std        |         0.1540 |         0.1465 |         0.0635 |         0.4122 |
| min        |        -1.0711 |        -1.0712 |        -0.7739 |        -5.0250 |
| 25%        |         0.1242 |         0.1041 |        -0.0599 |        -0.3890 |
| 50%        |         0.2187 |         0.1842 |        -0.0240 |        -0.1558 |
| 75%        |         0.3000 |         0.2615 |         0.0043 |         0.0276 |
| max        |         3.2757 |         3.2813 |         2.7034 |        17.5546 |

**Regression Analysis** (Python ~ Stata):

- **Model**: python = -0.0035 + 0.8675 * stata
- **R-squared**: 0.8316
- **N observations**: 2,055,856

| Coefficient |     Estimate |    Std Error | t-statistic |   p-value |
|-------------|--------------|--------------|-------------|----------|
| Intercept   |      -0.0035 |     7.08e-05 |    -48.9602 |     0.000 |
| Slope       |       0.8675 |     2.72e-04 |   3186.6579 |     0.000 |

**Feedback**:
- Num observations with std_diff >= TOL_DIFF_1: 1997005/2055856 (97.137%)
- Stata standard deviation: 1.54e-01

**Most Recent Bad Observations**:
```
   permno  yyyymm    python     stata      diff
0   10026  202412 -0.034304  0.032569 -0.066873
1   10032  202412 -0.029687  0.035968 -0.065654
2   10104  202412 -0.031745  0.034036 -0.065780
3   10107  202412 -0.030432  0.038111 -0.068543
4   10138  202412 -0.027677  0.037830 -0.065507
5   10145  202412 -0.030371  0.036421 -0.066792
6   10158  202412 -0.029219  0.032967 -0.062187
7   10200  202412 -0.029422  0.036853 -0.066275
8   10220  202412 -0.035664  0.030636 -0.066300
9   10252  202412 -0.031521  0.033475 -0.064996
```

**Largest Differences**:
```
   permno  yyyymm    python     stata      diff
0   89901  202010  3.053600  0.350159  2.703441
1   89901  202009  2.889721  0.484879  2.404842
2   91040  201802  2.698260  0.729334  1.968925
3   91040  201803  2.514423  0.577583  1.936839
4   91040  201801  2.339864  0.533972  1.805892
5   91040  201710  0.944249 -0.810950  1.755198
6   89901  202011  1.883874  0.261689  1.622186
7   91040  201711  1.758396  0.145073  1.613322
8   66800  200907  3.200631  1.620982  1.579649
9   91040  201709  0.771731 -0.776422  1.548153
```

**Largest Differences Before 1950**:
```
   permno  yyyymm  python     stata      diff
0   15683  192802     0.0  0.624997 -0.624997
1   25486  192802     0.0  0.585620 -0.585620
2   14787  192602     0.0  0.580582 -0.580582
3   19123  192802     0.0  0.571866 -0.571866
4   11690  192802     0.0  0.571848 -0.571848
5   12722  192802     0.0  0.570393 -0.570393
6   16598  192802     0.0  0.561133 -0.561133
7   13856  192808     0.0  0.554285 -0.554285
8   10057  192802     0.0  0.553838 -0.553838
9   10751  192802     0.0  0.553429 -0.553429
```

---

