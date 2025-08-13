# Predictor Validation Results

**Generated**: 2025-08-13 13:18:28

**Configuration**:
- TOL_SUPERSET: 1.0%
- TOL_DIFF_1: 0.01
- TOL_OBS_1: 10%
- EXTREME_Q: 0.99
- TOL_DIFF_2: 1.0
- INDEX_COLS: ['permno', 'yyyymm']

## Summary

| Predictor                 | Python CSV | Columns  | Superset  | Precision1   | Precision2              |
|---------------------------|------------|----------|-----------|--------------|-------------------------|
| Recomm_ShortInterest      | ✅         | ✅       | ❌ (55.76%)  | ✅ (0.00%)    | ✅ (99th diff 0.0E+00)   |
| PatentsRD                 | ✅         | ✅       | ❌ (21.05%)  | ✅ (0.02%)    | ✅ (99th diff 0.0E+00)   |
| Mom6mJunk                 | ✅         | ✅       | ❌ (18.09%)  | ✅ (0.28%)    | ✅ (99th diff 1.0E-07)   |
| ShareVol                  | ✅         | ✅       | ❌ (17.95%)  | ✅ (0.00%)    | ✅ (99th diff 0.0E+00)   |
| sinAlgo                   | ✅         | ✅       | ❌ (15.87%)  | ✅ (0.01%)    | ✅ (99th diff 0.0E+00)   |
| RDAbility                 | ✅         | ✅       | ❌ (4.95%)   | ✅ (9.52%)    | ✅ (99th diff 9.5E-01)   |
| RIO_Volatility            | ✅         | ✅       | ❌ (4.44%)   | ✅ (4.32%)    | ✅ (99th diff 7.5E-01)   |
| IdioVolAHT                | ✅         | ✅       | ❌ (3.82%)   | ❌ (17.59%)   | ✅ (99th diff 2.0E-01)   |
| DownRecomm                | ✅         | ✅       | ❌ (3.19%)   | ✅ (0.03%)    | ✅ (99th diff 0.0E+00)   |
| UpRecomm                  | ✅         | ✅       | ❌ (3.19%)   | ✅ (0.02%)    | ✅ (99th diff 0.0E+00)   |
| FirmAgeMom                | ✅         | ✅       | ❌ (1.85%)   | ✅ (0.39%)    | ✅ (99th diff 1.4E-07)   |
| MomRev                    | ✅         | ✅       | ❌ (1.31%)   | ✅ (0.00%)    | ✅ (99th diff 0.0E+00)   |
| TrendFactor               | ✅         | ✅       | ✅ (0.12%)   | ❌ (97.14%)   | ❌ (99th diff 1.7E+00)   |
| PredictedFE*              | ✅         | ✅       | ✅ (0.27%)   | ❌ (85.27%)   | ✅ (99th diff 2.1E-01)   |
| MS                        | ✅         | ✅       | ✅ (0.00%)   | ❌ (32.97%)   | ❌ (99th diff 2.6E+00)   |
| AbnormalAccruals          | ✅         | ✅       | ✅ (0.68%)   | ❌ (27.95%)   | ✅ (99th diff 3.2E-01)   |
| CitationsRD               | ✅         | ✅       | ✅ (0.00%)   | ❌ (21.54%)   | ❌ (99th diff 2.4E+00)   |
| PriceDelayTstat           | ✅         | ✅       | ✅ (0.00%)   | ❌ (19.38%)   | ❌ (99th diff 4.4E+00)   |
| PS                        | ✅         | ✅       | ✅ (0.00%)   | ❌ (17.93%)   | ✅ (99th diff 5.9E-01)   |
| OrgCap                    | ✅         | ✅       | ✅ (0.00%)   | ❌ (14.23%)   | ✅ (99th diff 1.3E-01)   |
| IndRetBig                 | ✅         | ✅       | ✅ (0.21%)   | ✅ (6.70%)    | ✅ (99th diff 1.0E-01)   |
| BetaFP                    | ✅         | ✅       | ✅ (0.54%)   | ✅ (5.98%)    | ✅ (99th diff 8.9E-02)   |
| DivSeason                 | ✅         | ✅       | ✅ (0.00%)   | ✅ (5.21%)    | ❌ (99th diff 2.0E+00)   |
| BetaTailRisk              | ✅         | ✅       | ✅ (0.00%)   | ✅ (4.15%)    | ✅ (99th diff 2.0E-02)   |
| RIO_Disp                  | ✅         | ✅       | ✅ (0.26%)   | ✅ (3.79%)    | ✅ (99th diff 7.9E-01)   |
| RIO_Turnover              | ✅         | ✅       | ✅ (0.15%)   | ✅ (3.65%)    | ✅ (99th diff 7.4E-01)   |
| RIO_MB                    | ✅         | ✅       | ✅ (0.18%)   | ✅ (3.45%)    | ✅ (99th diff 7.4E-01)   |
| IndMom                    | ✅         | ✅       | ✅ (0.00%)   | ✅ (3.28%)    | ✅ (99th diff 2.9E-01)   |
| ReturnSkew3F              | ✅         | ✅       | ✅ (0.00%)   | ✅ (2.68%)    | ✅ (99th diff 2.7E-02)   |
| HerfAsset                 | ✅         | ✅       | ✅ (0.00%)   | ✅ (1.44%)    | ✅ (99th diff 2.9E-02)   |
| VolumeTrend               | ✅         | ✅       | ✅ (0.00%)   | ✅ (1.36%)    | ✅ (99th diff 9.3E-02)   |
| Tax                       | ✅         | ✅       | ✅ (0.00%)   | ✅ (1.24%)    | ✅ (99th diff 3.2E-02)   |
| PriceDelayRsq             | ✅         | ✅       | ✅ (0.00%)   | ✅ (1.21%)    | ✅ (99th diff 1.9E-01)   |
| MomOffSeason              | ✅         | ✅       | ✅ (0.00%)   | ✅ (1.06%)    | ✅ (99th diff 3.5E-02)   |
| NumEarnIncrease           | ✅         | ✅       | ✅ (0.00%)   | ✅ (1.01%)    | ✅ (99th diff 5.2E-01)   |
| Investment                | ✅         | ✅       | ✅ (0.00%)   | ✅ (1.00%)    | ✅ (99th diff 1.0E-02)   |
| retConglomerate           | ✅         | ✅       | ✅ (0.00%)   | ✅ (0.94%)    | ✅ (99th diff 9.4E-03)   |

**Overall**: 17/37 available predictors passed validation
  - Natural passes: 16
  - Overridden passes: 1
**Python CSVs**: 37/37 predictors have Python implementation
\* = Manual override applied (see Predictors/overrides.yaml for details)

## Detailed Results

### AbnormalAccruals

**Status**: ❌ FAILED

**Test Results**:
- Test 1 - Column names: ✅ PASSED
- Test 2 - Superset check: ✅ PASSED
- Test 3 - Precision1 check: ❌ FAILED
- Test 4 - Precision2 check: ✅ PASSED

**Columns**: ['AbnormalAccruals']

**Observations**:
- Stata:  2,570,664
- Python: 2,567,830
- Common: 2,553,227

**Precision1**: 27.951% obs with std_diff >= 1.00e-02 (tolerance: < 10%)

**Precision2**: 99th percentile diff = 3.25e-01 (tolerance: < 1.00e+00)

**Summary Statistics** (Common Observations):

| Statistic  |          Stata |         Python |     Difference | Std Difference |
|------------|----------------|----------------|----------------|----------------|
| count      |       2.55e+06 |       2.55e+06 |       2.55e+06 |       2.55e+06 |
| mean       |       6.08e-05 |       2.43e-04 |       1.82e-04 |         0.0011 |
| std        |         0.1607 |         0.1612 |         0.0139 |         0.0862 |
| min        |        -8.2957 |        -8.2790 |        -0.8799 |        -5.4744 |
| 25%        |        -0.0405 |        -0.0407 |      -2.45e-04 |        -0.0015 |
| 50%        |         0.0069 |         0.0068 |      -3.53e-10 |      -2.20e-09 |
| 75%        |         0.0526 |         0.0526 |       3.53e-05 |       2.20e-04 |
| max        |         2.8119 |         2.8119 |         0.8710 |         5.4185 |

**Regression Analysis** (Python ~ Stata):

- **Model**: python = 0.0002 + 0.9990 * stata
- **R-squared**: 0.9926
- **N observations**: 2,553,227

| Coefficient |     Estimate |    Std Error | t-statistic |   p-value |
|-------------|--------------|--------------|-------------|----------|
| Intercept   |     1.83e-04 |     8.67e-06 |     21.0518 |     0.000 |
| Slope       |       0.9990 |     5.39e-05 |  18520.6724 |     0.000 |

**Feedback**:
- Num observations with std_diff >= TOL_DIFF_1: 713656/2553227 (27.951%)
- Stata standard deviation: 1.61e-01

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
   permno  yyyymm    python    stata      diff
0   79702  201712 -2.383081 -1.50314 -0.879941
1   79702  201801 -2.383081 -1.50314 -0.879941
2   79702  201802 -2.383081 -1.50314 -0.879941
3   79702  201803 -2.383081 -1.50314 -0.879941
4   79702  201804 -2.383081 -1.50314 -0.879941
5   79702  201805 -2.383081 -1.50314 -0.879941
6   79702  201806 -2.383081 -1.50314 -0.879941
7   79702  201807 -2.383081 -1.50314 -0.879941
8   79702  201808 -2.383081 -1.50314 -0.879941
9   79702  201809 -2.383081 -1.50314 -0.879941
```

---

### BetaFP

**Status**: ✅ PASSED

**Test Results**:
- Test 1 - Column names: ✅ PASSED
- Test 2 - Superset check: ✅ PASSED
- Test 3 - Precision1 check: ✅ PASSED
- Test 4 - Precision2 check: ✅ PASSED

**Columns**: ['BetaFP']

**Observations**:
- Stata:  3,794,018
- Python: 3,779,957
- Common: 3,773,530

**Precision1**: 5.980% obs with std_diff >= 1.00e-02 (tolerance: < 10%)

**Precision2**: 99th percentile diff = 8.93e-02 (tolerance: < 1.00e+00)

**Summary Statistics** (Common Observations):

| Statistic  |          Stata |         Python |     Difference | Std Difference |
|------------|----------------|----------------|----------------|----------------|
| count      |       3.77e+06 |       3.77e+06 |       3.77e+06 |       3.77e+06 |
| mean       |         0.9816 |         0.9803 |        -0.0013 |        -0.0020 |
| std        |         0.6411 |         0.6407 |         0.0286 |         0.0446 |
| min        |       7.25e-07 |         0.0000 |        -3.9823 |        -6.2114 |
| 25%        |         0.5206 |         0.5196 |        -0.0018 |        -0.0028 |
| 50%        |         0.8971 |         0.8960 |        -0.0010 |        -0.0016 |
| 75%        |         1.3181 |         1.3166 |      -4.96e-04 |      -7.74e-04 |
| max        |        12.6047 |        12.5623 |         4.7939 |         7.4774 |

**Regression Analysis** (Python ~ Stata):

- **Model**: python = 0.0004 + 0.9983 * stata
- **R-squared**: 0.9980
- **N observations**: 3,773,524

| Coefficient |     Estimate |    Std Error | t-statistic |   p-value |
|-------------|--------------|--------------|-------------|----------|
| Intercept   |     3.83e-04 |     2.69e-05 |     14.2406 |     0.000 |
| Slope       |       0.9983 |     2.30e-05 |  43476.8035 |     0.000 |

**Feedback**:
- Num observations with std_diff >= TOL_DIFF_1: 225656/3773530 (5.980%)
- Stata standard deviation: 6.41e-01

---

### BetaTailRisk

**Status**: ✅ PASSED

**Test Results**:
- Test 1 - Column names: ✅ PASSED
- Test 2 - Superset check: ✅ PASSED
- Test 3 - Precision1 check: ✅ PASSED
- Test 4 - Precision2 check: ✅ PASSED

**Columns**: ['BetaTailRisk']

**Observations**:
- Stata:  2,292,350
- Python: 2,332,084
- Common: 2,292,350

**Precision1**: 4.149% obs with std_diff >= 1.00e-02 (tolerance: < 10%)

**Precision2**: 99th percentile diff = 1.97e-02 (tolerance: < 1.00e+00)

**Summary Statistics** (Common Observations):

| Statistic  |          Stata |         Python |     Difference | Std Difference |
|------------|----------------|----------------|----------------|----------------|
| count      |       2.29e+06 |       2.29e+06 |       2.29e+06 |       2.29e+06 |
| mean       |         0.6390 |         0.6390 |      -3.78e-05 |      -7.39e-05 |
| std        |         0.5111 |         0.5109 |         0.0026 |         0.0052 |
| min        |       -10.7373 |       -10.7080 |        -0.0878 |        -0.1719 |
| 25%        |         0.3065 |         0.3066 |      -8.98e-04 |        -0.0018 |
| 50%        |         0.5661 |         0.5661 |      -1.37e-04 |      -2.69e-04 |
| 75%        |         0.8925 |         0.8923 |       4.95e-04 |       9.69e-04 |
| max        |         8.5702 |         8.5711 |         0.1976 |         0.3866 |

**Regression Analysis** (Python ~ Stata):

- **Model**: python = 0.0002 + 0.9996 * stata
- **R-squared**: 1.0000
- **N observations**: 2,292,350

| Coefficient |     Estimate |    Std Error | t-statistic |   p-value |
|-------------|--------------|--------------|-------------|----------|
| Intercept   |     1.99e-04 |     2.78e-06 |     71.7608 |     0.000 |
| Slope       |       0.9996 |     3.39e-06 | 294509.4351 |     0.000 |

**Feedback**:
- Num observations with std_diff >= TOL_DIFF_1: 95107/2292350 (4.149%)
- Stata standard deviation: 5.11e-01

---

### CitationsRD

**Status**: ❌ FAILED

**Test Results**:
- Test 1 - Column names: ✅ PASSED
- Test 2 - Superset check: ✅ PASSED
- Test 3 - Precision1 check: ❌ FAILED
- Test 4 - Precision2 check: ❌ FAILED

**Columns**: ['CitationsRD']

**Observations**:
- Stata:  645,360
- Python: 701,940
- Common: 645,360

**Precision1**: 21.536% obs with std_diff >= 1.00e-02 (tolerance: < 10%)

**Precision2**: 99th percentile diff = 2.43e+00 (tolerance: < 1.00e+00)

**Summary Statistics** (Common Observations):

| Statistic  |          Stata |         Python |     Difference | Std Difference |
|------------|----------------|----------------|----------------|----------------|
| count      |    645360.0000 |    645360.0000 |    645360.0000 |    645360.0000 |
| mean       |         0.2154 |         0.0000 |        -0.2154 |        -0.5239 |
| std        |         0.4111 |         0.0000 |         0.4111 |         1.0000 |
| min        |         0.0000 |         0.0000 |        -1.0000 |        -2.4327 |
| 25%        |         0.0000 |         0.0000 |         0.0000 |         0.0000 |
| 50%        |         0.0000 |         0.0000 |         0.0000 |         0.0000 |
| 75%        |         0.0000 |         0.0000 |         0.0000 |         0.0000 |
| max        |         1.0000 |         0.0000 |         0.0000 |         0.0000 |

**Regression Analysis** (Python ~ Stata):

- **Model**: python = 0.0000 + 0.0000 * stata
- **R-squared**: nan
- **N observations**: 645,360

| Coefficient |     Estimate |    Std Error | t-statistic |   p-value |
|-------------|--------------|--------------|-------------|----------|
| Intercept   |       0.0000 |       0.0000 |         nan |       nan |
| Slope       |       0.0000 |       0.0000 |         nan |       nan |

**Feedback**:
- Num observations with std_diff >= TOL_DIFF_1: 138984/645360 (21.536%)
- Stata standard deviation: 4.11e-01

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
0   10006  198306     0.0      1  -1.0
1   10006  198307     0.0      1  -1.0
2   10006  198308     0.0      1  -1.0
3   10006  198309     0.0      1  -1.0
4   10006  198310     0.0      1  -1.0
5   10006  198311     0.0      1  -1.0
6   10006  198312     0.0      1  -1.0
7   10006  198401     0.0      1  -1.0
8   10006  198402     0.0      1  -1.0
9   10006  198403     0.0      1  -1.0
```

---

### DivSeason

**Status**: ❌ FAILED

**Test Results**:
- Test 1 - Column names: ✅ PASSED
- Test 2 - Superset check: ✅ PASSED
- Test 3 - Precision1 check: ✅ PASSED
- Test 4 - Precision2 check: ❌ FAILED

**Columns**: ['DivSeason']

**Observations**:
- Stata:  1,775,339
- Python: 4,041,685
- Common: 1,775,337

**Precision1**: 5.214% obs with std_diff >= 1.00e-02 (tolerance: < 10%)

**Precision2**: 99th percentile diff = 2.01e+00 (tolerance: < 1.00e+00)

**Summary Statistics** (Common Observations):

| Statistic  |          Stata |         Python |     Difference | Std Difference |
|------------|----------------|----------------|----------------|----------------|
| count      |       1.78e+06 |       1.78e+06 |       1.78e+06 |       1.78e+06 |
| mean       |         0.4456 |         0.3935 |        -0.0520 |        -0.1047 |
| std        |         0.4970 |         0.4885 |         0.2223 |         0.4473 |
| min        |         0.0000 |         0.0000 |        -1.0000 |        -2.0120 |
| 25%        |         0.0000 |         0.0000 |         0.0000 |         0.0000 |
| 50%        |         0.0000 |         0.0000 |         0.0000 |         0.0000 |
| 75%        |         1.0000 |         1.0000 |         0.0000 |         0.0000 |
| max        |         1.0000 |         1.0000 |         1.0000 |         2.0120 |

**Regression Analysis** (Python ~ Stata):

- **Model**: python = 0.0001 + 0.8830 * stata
- **R-squared**: 0.8070
- **N observations**: 1,775,337

| Coefficient |     Estimate |    Std Error | t-statistic |   p-value |
|-------------|--------------|--------------|-------------|----------|
| Intercept   |     1.01e-04 |     2.16e-04 |      0.4650 |     0.642 |
| Slope       |       0.8830 |     3.24e-04 |   2724.9918 |     0.000 |

**Feedback**:
- Num observations with std_diff >= TOL_DIFF_1: 92565/1775337 (5.214%)
- Stata standard deviation: 4.97e-01

**Most Recent Bad Observations**:
```
   permno  yyyymm  python  stata  diff
0   13407  202412       0      1    -1
1   14542  202412       0      1    -1
2   15920  202412       0      1    -1
3   16119  202412       0      1    -1
4   16611  202412       0      1    -1
5   17036  202412       0      1    -1
6   20447  202412       0      1    -1
7   20998  202412       0      1    -1
8   21372  202412       0      1    -1
9   21605  202412       0      1    -1
```

**Largest Differences**:
```
   permno  yyyymm  python  stata  diff
0   10001  198603       0      1    -1
1   10001  198604       0      1    -1
2   10001  198606       0      1    -1
3   10001  198607       0      1    -1
4   10001  198609       0      1    -1
5   10001  198610       0      1    -1
6   10001  198612       0      1    -1
7   10001  198701       0      1    -1
8   10001  201507       0      1    -1
9   10001  201510       0      1    -1
```

---

### DownRecomm

**Status**: ❌ FAILED

**Test Results**:
- Test 1 - Column names: ✅ PASSED
- Test 2 - Superset check: ❌ FAILED (Python missing 14792 Stata observations)
- Test 3 - Precision1 check: ✅ PASSED
- Test 4 - Precision2 check: ✅ PASSED

**Columns**: ['DownRecomm']

**Observations**:
- Stata:  463,983
- Python: 450,458
- Common: 449,191

**Precision1**: 0.025% obs with std_diff >= 1.00e-02 (tolerance: < 10%)

**Precision2**: 99th percentile diff = 0.00e+00 (tolerance: < 1.00e+00)

**Summary Statistics** (Common Observations):

| Statistic  |          Stata |         Python |     Difference | Std Difference |
|------------|----------------|----------------|----------------|----------------|
| count      |    449191.0000 |    449191.0000 |    449191.0000 |    449191.0000 |
| mean       |         0.3815 |         0.3815 |         0.0000 |      -3.95e-21 |
| std        |         0.4857 |         0.4857 |         0.0159 |         0.0328 |
| min        |         0.0000 |         0.0000 |        -1.0000 |        -2.0587 |
| 25%        |         0.0000 |         0.0000 |         0.0000 |         0.0000 |
| 50%        |         0.0000 |         0.0000 |         0.0000 |         0.0000 |
| 75%        |         1.0000 |         1.0000 |         0.0000 |         0.0000 |
| max        |         1.0000 |         1.0000 |         1.0000 |         2.0587 |

**Regression Analysis** (Python ~ Stata):

- **Model**: python = 0.0002 + 0.9995 * stata
- **R-squared**: 0.9989
- **N observations**: 449,191

| Coefficient |     Estimate |    Std Error | t-statistic |   p-value |
|-------------|--------------|--------------|-------------|----------|
| Intercept   |     2.05e-04 |     3.02e-05 |      6.7888 |     0.000 |
| Slope       |       0.9995 |     4.89e-05 |  20427.2154 |     0.000 |

**Missing Observations Sample**:
```
 index  permno  yyyymm  DownRecomm
     0   10001  199311           0
     1   10002  200210           0
     2   10010  199311           0
     3   10011  199511           0
     4   10012  199402           0
     5   10016  199312           0
     6   10019  199403           0
     7   10025  199801           0
     8   10026  199311           0
     9   10028  202103           0
```

**Feedback**:
- Num observations with std_diff >= TOL_DIFF_1: 114/449191 (0.025%)
- Stata standard deviation: 4.86e-01

---

### FirmAgeMom

**Status**: ❌ FAILED

**Test Results**:
- Test 1 - Column names: ✅ PASSED
- Test 2 - Superset check: ❌ FAILED (Python missing 10169 Stata observations)
- Test 3 - Precision1 check: ✅ PASSED
- Test 4 - Precision2 check: ✅ PASSED

**Columns**: ['FirmAgeMom']

**Observations**:
- Stata:  550,434
- Python: 571,350
- Common: 540,265

**Precision1**: 0.388% obs with std_diff >= 1.00e-02 (tolerance: < 10%)

**Precision2**: 99th percentile diff = 1.44e-07 (tolerance: < 1.00e+00)

**Summary Statistics** (Common Observations):

| Statistic  |          Stata |         Python |     Difference | Std Difference |
|------------|----------------|----------------|----------------|----------------|
| count      |    540265.0000 |    540265.0000 |    540265.0000 |    540265.0000 |
| mean       |         0.0919 |         0.0920 |       8.77e-05 |       2.45e-04 |
| std        |         0.3575 |         0.3576 |         0.0111 |         0.0309 |
| min        |        -0.9374 |        -0.9374 |        -0.9081 |        -2.5403 |
| 25%        |        -0.0927 |        -0.0928 |      -2.71e-09 |      -7.57e-09 |
| 50%        |         0.0456 |         0.0457 |       5.55e-17 |       1.55e-16 |
| 75%        |         0.2152 |         0.2154 |       2.72e-09 |       7.61e-09 |
| max        |        27.4976 |        27.4976 |         2.0291 |         5.6759 |

**Regression Analysis** (Python ~ Stata):

- **Model**: python = 0.0001 + 1.0000 * stata
- **R-squared**: 0.9990
- **N observations**: 540,265

| Coefficient |     Estimate |    Std Error | t-statistic |   p-value |
|-------------|--------------|--------------|-------------|----------|
| Intercept   |     9.23e-05 |     1.55e-05 |      5.9468 |     0.000 |
| Slope       |       1.0000 |     4.21e-05 |  23775.1956 |     0.000 |

**Missing Observations Sample**:
```
 index  permno  yyyymm  FirmAgeMom
     0   10050  197411   -0.292222
     1   10058  197506    0.000000
     2   10058  197507    0.000000
     3   10058  197508    0.000000
     4   10058  197509    0.000000
     5   10058  197510    0.000000
     6   10058  197511    0.000000
     7   10161  192706    0.005882
     8   10189  198003   -0.095845
     9   10284  192801    0.204752
```

**Feedback**:
- Num observations with std_diff >= TOL_DIFF_1: 2098/540265 (0.388%)
- Stata standard deviation: 3.57e-01

---

### HerfAsset

**Status**: ✅ PASSED

**Test Results**:
- Test 1 - Column names: ✅ PASSED
- Test 2 - Superset check: ✅ PASSED
- Test 3 - Precision1 check: ✅ PASSED
- Test 4 - Precision2 check: ✅ PASSED

**Columns**: ['HerfAsset']

**Observations**:
- Stata:  2,547,057
- Python: 2,553,214
- Common: 2,547,057

**Precision1**: 1.444% obs with std_diff >= 1.00e-02 (tolerance: < 10%)

**Precision2**: 99th percentile diff = 2.94e-02 (tolerance: < 1.00e+00)

**Summary Statistics** (Common Observations):

| Statistic  |          Stata |         Python |     Difference | Std Difference |
|------------|----------------|----------------|----------------|----------------|
| count      |       2.55e+06 |       2.55e+06 |       2.55e+06 |       2.55e+06 |
| mean       |         0.3431 |         0.3429 |      -1.26e-04 |      -4.52e-04 |
| std        |         0.2778 |         0.2776 |         0.0096 |         0.0344 |
| min        |         0.0162 |         0.0162 |        -0.6447 |        -2.3206 |
| 25%        |         0.1214 |         0.1215 |      -2.52e-09 |      -9.08e-09 |
| 50%        |         0.2657 |         0.2657 |         0.0000 |         0.0000 |
| 75%        |         0.4885 |         0.4884 |       2.91e-09 |       1.05e-08 |
| max        |         1.0000 |         1.0000 |         0.6436 |         2.3165 |

**Regression Analysis** (Python ~ Stata):

- **Model**: python = 0.0004 + 0.9985 * stata
- **R-squared**: 0.9988
- **N observations**: 2,547,057

| Coefficient |     Estimate |    Std Error | t-statistic |   p-value |
|-------------|--------------|--------------|-------------|----------|
| Intercept   |     3.78e-04 |     9.50e-06 |     39.8123 |     0.000 |
| Slope       |       0.9985 |     2.15e-05 |  46398.4453 |     0.000 |

**Feedback**:
- Num observations with std_diff >= TOL_DIFF_1: 36791/2547057 (1.444%)
- Stata standard deviation: 2.78e-01

---

### IdioVolAHT

**Status**: ❌ FAILED

**Test Results**:
- Test 1 - Column names: ✅ PASSED
- Test 2 - Superset check: ❌ FAILED (Python missing 185207 Stata observations)
- Test 3 - Precision1 check: ❌ FAILED
- Test 4 - Precision2 check: ✅ PASSED

**Columns**: ['IdioVolAHT']

**Observations**:
- Stata:  4,849,170
- Python: 4,674,856
- Common: 4,663,963

**Precision1**: 17.592% obs with std_diff >= 1.00e-02 (tolerance: < 10%)

**Precision2**: 99th percentile diff = 2.02e-01 (tolerance: < 1.00e+00)

**Summary Statistics** (Common Observations):

| Statistic  |          Stata |         Python |     Difference | Std Difference |
|------------|----------------|----------------|----------------|----------------|
| count      |       4.66e+06 |       4.66e+06 |       4.66e+06 |       4.66e+06 |
| mean       |         0.0299 |         0.0299 |      -1.60e-05 |      -6.06e-04 |
| std        |         0.0263 |         0.0263 |         0.0026 |         0.0998 |
| min        |       1.02e-05 |       2.30e-05 |        -0.5549 |       -21.0921 |
| 25%        |         0.0142 |         0.0142 |      -7.80e-05 |        -0.0030 |
| 50%        |         0.0230 |         0.0230 |      -8.56e-06 |      -3.25e-04 |
| 75%        |         0.0377 |         0.0376 |       8.16e-05 |         0.0031 |
| max        |         2.5092 |         2.5089 |         0.3261 |        12.3974 |

**Regression Analysis** (Python ~ Stata):

- **Model**: python = 0.0002 + 0.9938 * stata
- **R-squared**: 0.9901
- **N observations**: 4,663,963

| Coefficient |     Estimate |    Std Error | t-statistic |   p-value |
|-------------|--------------|--------------|-------------|----------|
| Intercept   |     1.70e-04 |     1.84e-06 |     92.6742 |     0.000 |
| Slope       |       0.9938 |     4.61e-05 |  21554.2918 |     0.000 |

**Missing Observations Sample**:
```
 index  permno  yyyymm  IdioVolAHT
     0   10000  198605    0.044089
     1   10000  198606    0.040834
     2   10000  198607    0.041602
     3   10000  198608    0.053414
     4   10000  198609    0.052791
     5   10001  198606    0.007429
     6   10001  198607    0.008367
     7   10001  198608    0.008199
     8   10001  198609    0.012856
     9   10002  198606    0.017542
```

**Feedback**:
- Num observations with std_diff >= TOL_DIFF_1: 820464/4663963 (17.592%)
- Stata standard deviation: 2.63e-02

**Most Recent Bad Observations**:
```
   permno  yyyymm    python     stata      diff
0   10355  202412  0.020368  0.019840  0.000528
1   11547  202412  0.024971  0.024665  0.000306
2   12049  202412  0.074645  0.074922 -0.000278
3   12209  202412  0.055328  0.055615 -0.000287
4   12295  202412  0.004804  0.004460  0.000344
5   12355  202412  0.012702  0.012363  0.000339
6   12380  202412  0.024728  0.024445  0.000283
7   12397  202412  0.029515  0.029200  0.000315
8   12447  202412  0.035238  0.034865  0.000373
9   12462  202412  0.011098  0.010642  0.000456
```

**Largest Differences**:
```
   permno  yyyymm    python     stata      diff
0   10346  199508  0.200301  0.755186 -0.554885
1   19831  202107  0.138224  0.690156 -0.551932
2   10346  199509  0.199367  0.750348 -0.550982
3   19831  202108  0.128564  0.656875 -0.528310
4   19831  202111  0.113861  0.632297 -0.518436
5   19831  202110  0.117159  0.632683 -0.515523
6   19831  202109  0.123172  0.633176 -0.510004
7   17283  193204  0.036924  0.536495 -0.499571
8   17283  193203  0.040211  0.536824 -0.496613
9   38420  201105  0.033253  0.524829 -0.491576
```

---

### IndMom

**Status**: ✅ PASSED

**Test Results**:
- Test 1 - Column names: ✅ PASSED
- Test 2 - Superset check: ✅ PASSED
- Test 3 - Precision1 check: ✅ PASSED
- Test 4 - Precision2 check: ✅ PASSED

**Columns**: ['IndMom']

**Observations**:
- Stata:  4,043,138
- Python: 4,044,574
- Common: 4,043,138

**Precision1**: 3.278% obs with std_diff >= 1.00e-02 (tolerance: < 10%)

**Precision2**: 99th percentile diff = 2.92e-01 (tolerance: < 1.00e+00)

**Summary Statistics** (Common Observations):

| Statistic  |          Stata |         Python |     Difference | Std Difference |
|------------|----------------|----------------|----------------|----------------|
| count      |       4.04e+06 |       4.04e+06 |       4.04e+06 |       4.04e+06 |
| mean       |         0.0857 |         0.0841 |        -0.0016 |        -0.0093 |
| std        |         0.1736 |         0.1711 |         0.0184 |         0.1062 |
| min        |        -0.9265 |        -0.9265 |        -1.2736 |        -7.3369 |
| 25%        |        -0.0099 |        -0.0104 |      -3.43e-08 |      -1.97e-07 |
| 50%        |         0.0775 |         0.0767 |      -1.39e-09 |      -8.03e-09 |
| 75%        |         0.1676 |         0.1662 |       3.34e-09 |       1.92e-08 |
| max        |        10.5068 |        10.5068 |         0.1070 |         0.6162 |

**Regression Analysis** (Python ~ Stata):

- **Model**: python = 0.0001 + 0.9801 * stata
- **R-squared**: 0.9888
- **N observations**: 4,043,138

| Coefficient |     Estimate |    Std Error | t-statistic |   p-value |
|-------------|--------------|--------------|-------------|----------|
| Intercept   |     9.54e-05 |     1.00e-05 |      9.4990 |     0.000 |
| Slope       |       0.9801 |     5.19e-05 |  18889.0096 |     0.000 |

**Feedback**:
- Num observations with std_diff >= TOL_DIFF_1: 132529/4043138 (3.278%)
- Stata standard deviation: 1.74e-01

---

### IndRetBig

**Status**: ✅ PASSED

**Test Results**:
- Test 1 - Column names: ✅ PASSED
- Test 2 - Superset check: ✅ PASSED
- Test 3 - Precision1 check: ✅ PASSED
- Test 4 - Precision2 check: ✅ PASSED

**Columns**: ['IndRetBig']

**Observations**:
- Stata:  2,607,795
- Python: 2,616,695
- Common: 2,602,394

**Precision1**: 6.699% obs with std_diff >= 1.00e-02 (tolerance: < 10%)

**Precision2**: 99th percentile diff = 1.01e-01 (tolerance: < 1.00e+00)

**Summary Statistics** (Common Observations):

| Statistic  |          Stata |         Python |     Difference | Std Difference |
|------------|----------------|----------------|----------------|----------------|
| count      |       2.60e+06 |       2.60e+06 |       2.60e+06 |       2.60e+06 |
| mean       |         0.0180 |         0.0180 |       1.34e-06 |       1.90e-05 |
| std        |         0.0704 |         0.0704 |         0.0021 |         0.0299 |
| min        |        -0.4860 |        -0.4717 |        -0.1171 |        -1.6643 |
| 25%        |        -0.0206 |        -0.0206 |      -2.78e-17 |      -3.94e-16 |
| 50%        |         0.0176 |         0.0177 |         0.0000 |         0.0000 |
| 75%        |         0.0554 |         0.0554 |       2.78e-17 |       3.94e-16 |
| max        |         1.8831 |         1.8831 |         0.2476 |         3.5177 |

**Regression Analysis** (Python ~ Stata):

- **Model**: python = 0.0000 + 0.9998 * stata
- **R-squared**: 0.9991
- **N observations**: 2,602,394

| Coefficient |     Estimate |    Std Error | t-statistic |   p-value |
|-------------|--------------|--------------|-------------|----------|
| Intercept   |     5.27e-06 |     1.35e-06 |      3.9202 |     0.000 |
| Slope       |       0.9998 |     1.85e-05 |  53985.8175 |     0.000 |

**Feedback**:
- Num observations with std_diff >= TOL_DIFF_1: 174345/2602394 (6.699%)
- Stata standard deviation: 7.04e-02

---

### Investment

**Status**: ✅ PASSED

**Test Results**:
- Test 1 - Column names: ✅ PASSED
- Test 2 - Superset check: ✅ PASSED
- Test 3 - Precision1 check: ✅ PASSED
- Test 4 - Precision2 check: ✅ PASSED

**Columns**: ['Investment']

**Observations**:
- Stata:  2,411,862
- Python: 2,419,987
- Common: 2,411,862

**Precision1**: 0.999% obs with std_diff >= 1.00e-02 (tolerance: < 10%)

**Precision2**: 99th percentile diff = 9.98e-03 (tolerance: < 1.00e+00)

**Summary Statistics** (Common Observations):

| Statistic  |          Stata |         Python |     Difference | Std Difference |
|------------|----------------|----------------|----------------|----------------|
| count      |       2.41e+06 |       2.41e+06 |       2.41e+06 |       2.41e+06 |
| mean       |         1.0036 |         1.0035 |      -1.75e-04 |      -9.60e-05 |
| std        |         1.8269 |         1.8280 |         0.0448 |         0.0245 |
| min        |     -2512.3491 |     -2512.3180 |       -31.3369 |       -17.1529 |
| 25%        |         0.6665 |         0.6659 |      -2.24e-08 |      -1.22e-08 |
| 50%        |         0.9327 |         0.9323 |         0.0000 |         0.0000 |
| 75%        |         1.2036 |         1.2035 |       2.24e-08 |       1.23e-08 |
| max        |       253.6225 |       253.6223 |        12.0000 |         6.5685 |

**Regression Analysis** (Python ~ Stata):

- **Model**: python = -0.0004 + 1.0003 * stata
- **R-squared**: 0.9994
- **N observations**: 2,411,862

| Coefficient |     Estimate |    Std Error | t-statistic |   p-value |
|-------------|--------------|--------------|-------------|----------|
| Intercept   |    -4.43e-04 |     3.29e-05 |    -13.4392 |     0.000 |
| Slope       |       1.0003 |     1.58e-05 |  63297.3080 |     0.000 |

**Feedback**:
- Num observations with std_diff >= TOL_DIFF_1: 24097/2411862 (0.999%)
- Stata standard deviation: 1.83e+00

---

### MS

**Status**: ❌ FAILED

**Test Results**:
- Test 1 - Column names: ✅ PASSED
- Test 2 - Superset check: ✅ PASSED
- Test 3 - Precision1 check: ❌ FAILED
- Test 4 - Precision2 check: ❌ FAILED

**Columns**: ['MS']

**Observations**:
- Stata:  473,079
- Python: 473,079
- Common: 473,079

**Precision1**: 32.967% obs with std_diff >= 1.00e-02 (tolerance: < 10%)

**Precision2**: 99th percentile diff = 2.59e+00 (tolerance: < 1.00e+00)

**Summary Statistics** (Common Observations):

| Statistic  |          Stata |         Python |     Difference | Std Difference |
|------------|----------------|----------------|----------------|----------------|
| count      |    473079.0000 |    473079.0000 |    473079.0000 |    473079.0000 |
| mean       |         3.8814 |         3.7610 |        -0.1204 |        -0.0781 |
| std        |         1.5421 |         1.5342 |         1.0648 |         0.6905 |
| min        |         1.0000 |         1.0000 |        -5.0000 |        -3.2424 |
| 25%        |         3.0000 |         3.0000 |         0.0000 |         0.0000 |
| 50%        |         4.0000 |         4.0000 |         0.0000 |         0.0000 |
| 75%        |         5.0000 |         5.0000 |         0.0000 |         0.0000 |
| max        |         6.0000 |         6.0000 |         5.0000 |         3.2424 |

**Regression Analysis** (Python ~ Stata):

- **Model**: python = 0.8246 + 0.7565 * stata
- **R-squared**: 0.5782
- **N observations**: 473,079

| Coefficient |     Estimate |    Std Error | t-statistic |   p-value |
|-------------|--------------|--------------|-------------|----------|
| Intercept   |       0.8246 |       0.0039 |    210.1710 |     0.000 |
| Slope       |       0.7565 |     9.39e-04 |    805.2808 |     0.000 |

**Feedback**:
- Num observations with std_diff >= TOL_DIFF_1: 155962/473079 (32.967%)
- Stata standard deviation: 1.54e+00

**Most Recent Bad Observations**:
```
   permno  yyyymm  python  stata  diff
0   10104  202412       5      3     2
1   10220  202412       5      3     2
2   10693  202412       6      5     1
3   10966  202412       4      5    -1
4   11275  202412       2      5    -3
5   11308  202412       4      3     1
6   11809  202412       5      6    -1
7   11995  202412       4      5    -1
8   12060  202412       1      4    -3
9   12084  202412       5      6    -1
```

**Largest Differences**:
```
   permno  yyyymm  python  stata  diff
0   11170  199506       6      1     5
1   11170  199507       6      1     5
2   11170  199510       6      1     5
3   11170  199512       6      1     5
4   11170  199601       6      1     5
5   11170  199604       6      1     5
6   11170  199605       6      1     5
7   11170  199704       6      1     5
8   11170  199705       6      1     5
9   11233  199506       1      6    -5
```

---

### Mom6mJunk

**Status**: ❌ FAILED

**Test Results**:
- Test 1 - Column names: ✅ PASSED
- Test 2 - Superset check: ❌ FAILED (Python missing 70860 Stata observations)
- Test 3 - Precision1 check: ✅ PASSED
- Test 4 - Precision2 check: ✅ PASSED

**Columns**: ['Mom6mJunk']

**Observations**:
- Stata:  391,738
- Python: 328,709
- Common: 320,878

**Precision1**: 0.281% obs with std_diff >= 1.00e-02 (tolerance: < 10%)

**Precision2**: 99th percentile diff = 1.02e-07 (tolerance: < 1.00e+00)

**Summary Statistics** (Common Observations):

| Statistic  |          Stata |         Python |     Difference | Std Difference |
|------------|----------------|----------------|----------------|----------------|
| count      |    320878.0000 |    320878.0000 |    320878.0000 |    320878.0000 |
| mean       |         0.0545 |         0.0544 |      -1.69e-04 |      -4.38e-04 |
| std        |         0.3852 |         0.3855 |         0.0174 |         0.0452 |
| min        |        -0.9947 |        -0.9947 |        -1.1543 |        -2.9969 |
| 25%        |        -0.1332 |        -0.1335 |      -2.99e-09 |      -7.76e-09 |
| 50%        |         0.0332 |         0.0333 |       9.17e-15 |       2.38e-14 |
| 75%        |         0.2000 |         0.2000 |       2.99e-09 |       7.77e-09 |
| max        |        47.6527 |        47.6527 |         1.2493 |         3.2436 |

**Regression Analysis** (Python ~ Stata):

- **Model**: python = -0.0002 + 0.9999 * stata
- **R-squared**: 0.9980
- **N observations**: 320,878

| Coefficient |     Estimate |    Std Error | t-statistic |   p-value |
|-------------|--------------|--------------|-------------|----------|
| Intercept   |    -1.63e-04 |     3.11e-05 |     -5.2579 |     0.000 |
| Slope       |       0.9999 |     7.98e-05 |  12523.5442 |     0.000 |

**Missing Observations Sample**:
```
 index  permno  yyyymm  Mom6mJunk
     0   10026  201509   0.071515
     1   10026  201510   0.096434
     2   10026  201511   0.146379
     3   10026  201512   0.057645
     4   10026  201601  -0.007851
     5   10026  201602  -0.046296
     6   10026  201603  -0.021993
     7   10026  201604  -0.112035
     8   10026  201605  -0.127242
     9   10026  201606  -0.092484
```

**Feedback**:
- Num observations with std_diff >= TOL_DIFF_1: 903/320878 (0.281%)
- Stata standard deviation: 3.85e-01

---

### MomOffSeason

**Status**: ✅ PASSED

**Test Results**:
- Test 1 - Column names: ✅ PASSED
- Test 2 - Superset check: ✅ PASSED
- Test 3 - Precision1 check: ✅ PASSED
- Test 4 - Precision2 check: ✅ PASSED

**Columns**: ['MomOffSeason']

**Observations**:
- Stata:  3,396,704
- Python: 3,398,036
- Common: 3,396,703

**Precision1**: 1.063% obs with std_diff >= 1.00e-02 (tolerance: < 10%)

**Precision2**: 99th percentile diff = 3.53e-02 (tolerance: < 1.00e+00)

**Summary Statistics** (Common Observations):

| Statistic  |          Stata |         Python |     Difference | Std Difference |
|------------|----------------|----------------|----------------|----------------|
| count      |       3.40e+06 |       3.40e+06 |       3.40e+06 |       3.40e+06 |
| mean       |         0.0125 |         0.0124 |      -2.32e-05 |      -8.58e-04 |
| std        |         0.0270 |         0.0263 |         0.0057 |         0.2127 |
| min        |        -4.1713 |        -0.6858 |        -1.2021 |       -44.5515 |
| 25%        |       3.95e-04 |       3.88e-04 |      -5.00e-10 |      -1.85e-08 |
| 50%        |         0.0119 |         0.0118 |         0.0000 |         0.0000 |
| 75%        |         0.0240 |         0.0240 |       5.09e-10 |       1.89e-08 |
| max        |         1.5150 |         1.5150 |         3.8643 |       143.2185 |

**Regression Analysis** (Python ~ Stata):

- **Model**: python = 0.0006 + 0.9539 * stata
- **R-squared**: 0.9547
- **N observations**: 3,396,703

| Coefficient |     Estimate |    Std Error | t-statistic |   p-value |
|-------------|--------------|--------------|-------------|----------|
| Intercept   |     5.51e-04 |     3.35e-06 |    164.6263 |     0.000 |
| Slope       |       0.9539 |     1.13e-04 |   8465.5718 |     0.000 |

**Feedback**:
- Num observations with std_diff >= TOL_DIFF_1: 36098/3396703 (1.063%)
- Stata standard deviation: 2.70e-02

---

### MomRev

**Status**: ❌ FAILED

**Test Results**:
- Test 1 - Column names: ✅ PASSED
- Test 2 - Superset check: ❌ FAILED (Python missing 3435 Stata observations)
- Test 3 - Precision1 check: ✅ PASSED
- Test 4 - Precision2 check: ✅ PASSED

**Columns**: ['MomRev']

**Observations**:
- Stata:  262,210
- Python: 266,100
- Common: 258,775

**Precision1**: 0.000% obs with std_diff >= 1.00e-02 (tolerance: < 10%)

**Precision2**: 99th percentile diff = 0.00e+00 (tolerance: < 1.00e+00)

**Summary Statistics** (Common Observations):

| Statistic  |          Stata |         Python |     Difference | Std Difference |
|------------|----------------|----------------|----------------|----------------|
| count      |    258775.0000 |    258775.0000 |    258775.0000 |    258775.0000 |
| mean       |         0.5549 |         0.5549 |         0.0000 |         0.0000 |
| std        |         0.4970 |         0.4970 |         0.0000 |         0.0000 |
| min        |         0.0000 |         0.0000 |         0.0000 |         0.0000 |
| 25%        |         0.0000 |         0.0000 |         0.0000 |         0.0000 |
| 50%        |         1.0000 |         1.0000 |         0.0000 |         0.0000 |
| 75%        |         1.0000 |         1.0000 |         0.0000 |         0.0000 |
| max        |         1.0000 |         1.0000 |         0.0000 |         0.0000 |

**Regression Analysis** (Python ~ Stata):

- **Model**: python = -0.0000 + 1.0000 * stata
- **R-squared**: 1.0000
- **N observations**: 258,775

| Coefficient |     Estimate |    Std Error | t-statistic |   p-value |
|-------------|--------------|--------------|-------------|----------|
| Intercept   |    -5.37e-13 |     1.41e-15 |   -379.8265 |     0.000 |
| Slope       |       1.0000 |     1.90e-15 |    5.27e+14 |     0.000 |

**Missing Observations Sample**:
```
 index  permno  yyyymm  MomRev
     0   10028  200710       1
     1   10028  201707       1
     2   10057  197705       1
     3   10071  199007       1
     4   10087  200006       1
     5   10095  198911       1
     6   10100  200604       1
     7   10108  200504       1
     8   10142  199809       1
     9   10143  199104       1
```

**Feedback**:
- Num observations with std_diff >= TOL_DIFF_1: 0/258775 (0.000%)
- Stata standard deviation: 4.97e-01

---

### NumEarnIncrease

**Status**: ✅ PASSED

**Test Results**:
- Test 1 - Column names: ✅ PASSED
- Test 2 - Superset check: ✅ PASSED
- Test 3 - Precision1 check: ✅ PASSED
- Test 4 - Precision2 check: ✅ PASSED

**Columns**: ['NumEarnIncrease']

**Observations**:
- Stata:  2,823,456
- Python: 2,823,459
- Common: 2,823,456

**Precision1**: 1.010% obs with std_diff >= 1.00e-02 (tolerance: < 10%)

**Precision2**: 99th percentile diff = 5.18e-01 (tolerance: < 1.00e+00)

**Summary Statistics** (Common Observations):

| Statistic  |          Stata |         Python |     Difference | Std Difference |
|------------|----------------|----------------|----------------|----------------|
| count      |       2.82e+06 |       2.82e+06 |       2.82e+06 |       2.82e+06 |
| mean       |         1.2268 |         1.1965 |        -0.0303 |        -0.0157 |
| std        |         1.9293 |         1.9120 |         0.3730 |         0.1933 |
| min        |         0.0000 |         0.0000 |        -8.0000 |        -4.1465 |
| 25%        |         0.0000 |         0.0000 |         0.0000 |         0.0000 |
| 50%        |         0.0000 |         0.0000 |         0.0000 |         0.0000 |
| 75%        |         2.0000 |         2.0000 |         0.0000 |         0.0000 |
| max        |         8.0000 |         8.0000 |         8.0000 |         4.1465 |

**Regression Analysis** (Python ~ Stata):

- **Model**: python = 0.0036 + 0.9724 * stata
- **R-squared**: 0.9627
- **N observations**: 2,823,456

| Coefficient |     Estimate |    Std Error | t-statistic |   p-value |
|-------------|--------------|--------------|-------------|----------|
| Intercept   |       0.0036 |     2.60e-04 |     13.8365 |     0.000 |
| Slope       |       0.9724 |     1.14e-04 |   8538.4923 |     0.000 |

**Feedback**:
- Num observations with std_diff >= TOL_DIFF_1: 28519/2823456 (1.010%)
- Stata standard deviation: 1.93e+00

---

### OrgCap

**Status**: ❌ FAILED

**Test Results**:
- Test 1 - Column names: ✅ PASSED
- Test 2 - Superset check: ✅ PASSED
- Test 3 - Precision1 check: ❌ FAILED
- Test 4 - Precision2 check: ✅ PASSED

**Columns**: ['OrgCap']

**Observations**:
- Stata:  1,243,383
- Python: 1,327,508
- Common: 1,243,383

**Precision1**: 14.227% obs with std_diff >= 1.00e-02 (tolerance: < 10%)

**Precision2**: 99th percentile diff = 1.34e-01 (tolerance: < 1.00e+00)

**Summary Statistics** (Common Observations):

| Statistic  |          Stata |         Python |     Difference | Std Difference |
|------------|----------------|----------------|----------------|----------------|
| count      |       1.24e+06 |       1.24e+06 |       1.24e+06 |       1.24e+06 |
| mean       |       2.37e-10 |      -9.21e-04 |      -9.21e-04 |      -9.27e-04 |
| std        |         0.9941 |         0.9936 |         0.0410 |         0.0412 |
| min        |        -2.3446 |        -2.3446 |        -2.4134 |        -2.4279 |
| 25%        |        -0.6402 |        -0.6413 |      -3.04e-04 |      -3.06e-04 |
| 50%        |        -0.2736 |        -0.2745 |      -2.38e-08 |      -2.39e-08 |
| 75%        |         0.3358 |         0.3353 |       5.70e-04 |       5.74e-04 |
| max        |        10.1323 |        10.0846 |         0.5601 |         0.5634 |

**Regression Analysis** (Python ~ Stata):

- **Model**: python = -0.0009 + 0.9987 * stata
- **R-squared**: 0.9983
- **N observations**: 1,243,383

| Coefficient |     Estimate |    Std Error | t-statistic |   p-value |
|-------------|--------------|--------------|-------------|----------|
| Intercept   |    -9.21e-04 |     3.67e-05 |    -25.0657 |     0.000 |
| Slope       |       0.9987 |     3.70e-05 |  27016.1170 |     0.000 |

**Feedback**:
- Num observations with std_diff >= TOL_DIFF_1: 176895/1243383 (14.227%)
- Stata standard deviation: 9.94e-01

**Most Recent Bad Observations**:
```
   permno  yyyymm    python     stata      diff
0   10253  202412 -0.498174 -0.410555 -0.087619
1   10696  202412 -0.684260 -0.668215 -0.016045
2   10860  202412 -0.305616 -0.143933 -0.161683
3   10890  202412 -0.024218  0.245699 -0.269917
4   10966  202412  0.283315  0.671518 -0.388203
5   11275  202412  0.394461  0.825414 -0.430953
6   11403  202412 -0.114539  0.120637 -0.235176
7   11547  202412 -0.367466 -0.229573 -0.137893
8   11600  202412 -0.319548 -0.163224 -0.156324
9   11809  202412 -0.597949 -0.548706 -0.049243
```

**Largest Differences**:
```
   permno  yyyymm    python     stata      diff
0   13812  202406  4.742307  7.155751 -2.413444
1   14925  202406  4.809098  7.155751 -2.346653
2   24087  202406  4.809098  7.155751 -2.346653
3   89698  202406  4.809098  7.155751 -2.346653
4   13812  202410  4.813894  7.114257 -2.300363
5   14925  202410  4.813894  7.114257 -2.300363
6   24087  202410  4.813894  7.114257 -2.300363
7   89698  202410  4.813894  7.114257 -2.300363
8   13812  202411  4.826943  7.105795 -2.278852
9   14925  202411  4.826943  7.105795 -2.278852
```

---

### PS

**Status**: ❌ FAILED

**Test Results**:
- Test 1 - Column names: ✅ PASSED
- Test 2 - Superset check: ✅ PASSED
- Test 3 - Precision1 check: ❌ FAILED
- Test 4 - Precision2 check: ✅ PASSED

**Columns**: ['PS']

**Observations**:
- Stata:  463,944
- Python: 464,239
- Common: 463,941

**Precision1**: 17.931% obs with std_diff >= 1.00e-02 (tolerance: < 10%)

**Precision2**: 99th percentile diff = 5.90e-01 (tolerance: < 1.00e+00)

**Summary Statistics** (Common Observations):

| Statistic  |          Stata |         Python |     Difference | Std Difference |
|------------|----------------|----------------|----------------|----------------|
| count      |    463941.0000 |    463941.0000 |    463941.0000 |    463941.0000 |
| mean       |         5.0197 |         4.9729 |        -0.0468 |        -0.0276 |
| std        |         1.6958 |         1.8091 |         0.4595 |         0.2709 |
| min        |         0.0000 |         0.0000 |        -5.0000 |        -2.9484 |
| 25%        |         4.0000 |         4.0000 |         0.0000 |         0.0000 |
| 50%        |         5.0000 |         5.0000 |         0.0000 |         0.0000 |
| 75%        |         6.0000 |         6.0000 |         0.0000 |         0.0000 |
| max        |         9.0000 |         9.0000 |         6.0000 |         3.5381 |

**Regression Analysis** (Python ~ Stata):

- **Model**: python = -0.2090 + 1.0323 * stata
- **R-squared**: 0.9364
- **N observations**: 463,941

| Coefficient |     Estimate |    Std Error | t-statistic |   p-value |
|-------------|--------------|--------------|-------------|----------|
| Intercept   |      -0.2090 |       0.0021 |    -99.8754 |     0.000 |
| Slope       |       1.0323 |     3.95e-04 |   2613.7993 |     0.000 |

**Feedback**:
- Num observations with std_diff >= TOL_DIFF_1: 83191/463941 (17.931%)
- Stata standard deviation: 1.70e+00

**Most Recent Bad Observations**:
```
   permno  yyyymm  python  stata  diff
0   11593  202412     5.0      6  -1.0
1   12641  202412     6.0      7  -1.0
2   13583  202412     8.0      7   1.0
3   13919  202412     5.0      6  -1.0
4   14419  202412     3.0      4  -1.0
5   14468  202412     3.0      4  -1.0
6   14540  202412     5.0      6  -1.0
7   14601  202412     5.0      6  -1.0
8   14791  202412     6.0      5   1.0
9   14826  202412     2.0      3  -1.0
```

**Largest Differences**:
```
   permno  yyyymm  python  stata  diff
0   10193  198802     7.0      1   6.0
1   10193  198803     7.0      1   6.0
2   10193  198809     1.0      6  -5.0
3   10193  198810     1.0      6  -5.0
4   10193  198811     1.0      6  -5.0
5   11317  198304     2.0      7  -5.0
6   11484  199603     1.0      6  -5.0
7   11538  199101     0.0      5  -5.0
8   11538  199102     0.0      5  -5.0
9   11538  199103     0.0      5  -5.0
```

---

### PatentsRD

**Status**: ❌ FAILED

**Test Results**:
- Test 1 - Column names: ✅ PASSED
- Test 2 - Superset check: ❌ FAILED (Python missing 141420 Stata observations)
- Test 3 - Precision1 check: ✅ PASSED
- Test 4 - Precision2 check: ✅ PASSED

**Columns**: ['PatentsRD']

**Observations**:
- Stata:  671,832
- Python: 571,284
- Common: 530,412

**Precision1**: 0.023% obs with std_diff >= 1.00e-02 (tolerance: < 10%)

**Precision2**: 99th percentile diff = 0.00e+00 (tolerance: < 1.00e+00)

**Summary Statistics** (Common Observations):

| Statistic  |          Stata |         Python |     Difference | Std Difference |
|------------|----------------|----------------|----------------|----------------|
| count      |    530412.0000 |    530412.0000 |    530412.0000 |    530412.0000 |
| mean       |       2.26e-04 |         0.0000 |      -2.26e-04 |        -0.0150 |
| std        |         0.0150 |         0.0000 |         0.0150 |         1.0000 |
| min        |         0.0000 |         0.0000 |        -1.0000 |       -66.4913 |
| 25%        |         0.0000 |         0.0000 |         0.0000 |         0.0000 |
| 50%        |         0.0000 |         0.0000 |         0.0000 |         0.0000 |
| 75%        |         0.0000 |         0.0000 |         0.0000 |         0.0000 |
| max        |         1.0000 |         0.0000 |         0.0000 |         0.0000 |

**Regression Analysis** (Python ~ Stata):

- **Model**: python = 0.0000 + 0.0000 * stata
- **R-squared**: nan
- **N observations**: 530,412

| Coefficient |     Estimate |    Std Error | t-statistic |   p-value |
|-------------|--------------|--------------|-------------|----------|
| Intercept   |       0.0000 |       0.0000 |         nan |       nan |
| Slope       |       0.0000 |       0.0000 |         nan |       nan |

**Missing Observations Sample**:
```
 index  permno  yyyymm  PatentsRD
     0   10006  198306          1
     1   10006  198307          1
     2   10006  198308          1
     3   10006  198309          1
     4   10006  198310          1
     5   10006  198311          1
     6   10006  198312          1
     7   10006  198401          1
     8   10006  198402          1
     9   10006  198403          1
```

**Feedback**:
- Num observations with std_diff >= TOL_DIFF_1: 120/530412 (0.023%)
- Stata standard deviation: 1.50e-02

---

### PredictedFE

**Status**: ✅ PASSED (with override)

**Override Applied**:
- Reviewed on: 2025-08-13
- Reviewed by: ac
- Details: The standardized deviation is on average 1% with a sd of 7 pp. So it's above the threshold, but it's small. Sumstats and regressions show that the replication works very well. Regressing python on stata shows that the coefficient is 0.9959 and the Rsq is 0.995.

**Test Results**:
- Test 1 - Column names: ✅ PASSED
- Test 2 - Superset check: ✅ PASSED
- Test 3 - Precision1 check: ❌ FAILED
- Test 4 - Precision2 check: ✅ PASSED

**Columns**: ['PredictedFE']

**Observations**:
- Stata:  491,508
- Python: 635,124
- Common: 490,188

**Precision1**: 85.268% obs with std_diff >= 1.00e-02 (tolerance: < 10%)

**Precision2**: 99th percentile diff = 2.10e-01 (tolerance: < 1.00e+00)

**Summary Statistics** (Common Observations):

| Statistic  |          Stata |         Python |     Difference | Std Difference |
|------------|----------------|----------------|----------------|----------------|
| count      |    490188.0000 |    490188.0000 |    490188.0000 |    490188.0000 |
| mean       |         0.0519 |         0.0523 |       4.00e-04 |         0.0126 |
| std        |         0.0316 |         0.0316 |         0.0022 |         0.0695 |
| min        |        -0.1080 |        -0.1098 |        -0.0430 |        -1.3585 |
| 25%        |         0.0308 |         0.0310 |      -8.23e-04 |        -0.0260 |
| 50%        |         0.0476 |         0.0480 |       3.15e-04 |         0.0100 |
| 75%        |         0.0681 |         0.0685 |         0.0016 |         0.0519 |
| max        |         0.2809 |         0.2700 |         0.0289 |         0.9139 |

**Regression Analysis** (Python ~ Stata):

- **Model**: python = 0.0006 + 0.9959 * stata
- **R-squared**: 0.9952
- **N observations**: 490,188

| Coefficient |     Estimate |    Std Error | t-statistic |   p-value |
|-------------|--------------|--------------|-------------|----------|
| Intercept   |     6.10e-04 |     6.02e-06 |    101.2931 |     0.000 |
| Slope       |       0.9959 |     9.91e-05 |  10051.6551 |     0.000 |

**Feedback**:
- Num observations with std_diff >= TOL_DIFF_1: 417972/490188 (85.268%)
- Stata standard deviation: 3.16e-02

**Most Recent Bad Observations**:
```
   permno  yyyymm    python     stata      diff
0   10107  202505  0.083963  0.078498  0.005465
1   10145  202505  0.044157  0.040432  0.003725
2   10200  202505  0.115949  0.113642  0.002307
3   10397  202505  0.049261  0.049793 -0.000531
4   10606  202505  0.046297  0.044046  0.002251
5   10693  202505  0.042425  0.036774  0.005651
6   10696  202505  0.107327  0.105464  0.001862
7   11308  202505  0.073800  0.072780  0.001020
8   11403  202505  0.095454  0.090274  0.005179
9   11547  202505  0.080375  0.076702  0.003674
```

**Largest Differences**:
```
   permno  yyyymm    python     stata      diff
0   91575  202106  0.008267  0.051235 -0.042968
1   91575  202107  0.008267  0.051235 -0.042968
2   91575  202108  0.008267  0.051235 -0.042968
3   91575  202109  0.008267  0.051235 -0.042968
4   91575  202110  0.008267  0.051235 -0.042968
5   91575  202111  0.008267  0.051235 -0.042968
6   91575  202112  0.008267  0.051235 -0.042968
7   91575  202201  0.008267  0.051235 -0.042968
8   91575  202202  0.008267  0.051235 -0.042968
9   91575  202203  0.008267  0.051235 -0.042968
```

---

### PriceDelayRsq

**Status**: ✅ PASSED

**Test Results**:
- Test 1 - Column names: ✅ PASSED
- Test 2 - Superset check: ✅ PASSED
- Test 3 - Precision1 check: ✅ PASSED
- Test 4 - Precision2 check: ✅ PASSED

**Columns**: ['PriceDelayRsq']

**Observations**:
- Stata:  4,630,424
- Python: 4,636,840
- Common: 4,630,424

**Precision1**: 1.210% obs with std_diff >= 1.00e-02 (tolerance: < 10%)

**Precision2**: 99th percentile diff = 1.86e-01 (tolerance: < 1.00e+00)

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

---

### PriceDelayTstat

**Status**: ❌ FAILED

**Test Results**:
- Test 1 - Column names: ✅ PASSED
- Test 2 - Superset check: ✅ PASSED
- Test 3 - Precision1 check: ❌ FAILED
- Test 4 - Precision2 check: ❌ FAILED

**Columns**: ['PriceDelayTstat']

**Observations**:
- Stata:  4,523,656
- Python: 4,636,840
- Common: 4,523,656

**Precision1**: 19.380% obs with std_diff >= 1.00e-02 (tolerance: < 10%)

**Precision2**: 99th percentile diff = 4.40e+00 (tolerance: < 1.00e+00)

**Summary Statistics** (Common Observations):

| Statistic  |          Stata |         Python |     Difference | Std Difference |
|------------|----------------|----------------|----------------|----------------|
| count      |       4.52e+06 |       4.52e+06 |       4.52e+06 |       4.52e+06 |
| mean       |         1.6229 |         1.6095 |        -0.0134 |        -0.0097 |
| std        |         1.3836 |         1.9491 |         1.6083 |         1.1624 |
| min        |        -5.3533 |        -5.3261 |        -9.8548 |        -7.1223 |
| 25%        |         0.8336 |         0.5661 |      -1.57e-07 |      -1.13e-07 |
| 50%        |         1.6661 |         1.6681 |      -5.39e-10 |      -3.89e-10 |
| 75%        |         2.4069 |         2.6390 |       1.49e-07 |       1.07e-07 |
| max        |         7.5741 |         7.5741 |        10.7693 |         7.7833 |

**Regression Analysis** (Python ~ Stata):

- **Model**: python = 0.2841 + 0.8167 * stata
- **R-squared**: 0.3361
- **N observations**: 4,523,656

| Coefficient |     Estimate |    Std Error | t-statistic |   p-value |
|-------------|--------------|--------------|-------------|----------|
| Intercept   |       0.2841 |       0.0012 |    246.8524 |     0.000 |
| Slope       |       0.8167 |     5.40e-04 |   1513.3190 |     0.000 |

**Feedback**:
- Num observations with std_diff >= TOL_DIFF_1: 876673/4523656 (19.380%)
- Stata standard deviation: 1.38e+00

**Most Recent Bad Observations**:
```
   permno  yyyymm    python     stata      diff
0   10145  202407  6.102411  3.590652  2.511759
1   10252  202407 -3.251358  1.948711 -5.200069
2   10257  202407  6.102411  2.211252  3.891159
3   10308  202407 -3.251358  2.127883 -5.379241
4   10318  202407 -3.251358  1.480704 -4.732062
5   10355  202407  6.102411  2.726171  3.376240
6   10501  202407 -3.251358  0.107046 -3.358404
7   10516  202407  6.102411  3.875413  2.226998
8   10517  202407 -3.251358  1.185008 -4.436366
9   10547  202407 -3.251358  1.549714 -4.801072
```

**Largest Differences**:
```
   permno  yyyymm    python     stata       diff
0   20677  195407  6.913496 -3.855832  10.769328
1   20677  195408  6.913496 -3.855832  10.769328
2   20677  195409  6.913496 -3.855832  10.769328
3   20677  195410  6.913496 -3.855832  10.769328
4   20677  195411  6.913496 -3.855832  10.769328
5   20677  195412  6.913496 -3.855832  10.769328
6   20677  195501  6.913496 -3.855832  10.769328
7   20677  195502  6.913496 -3.855832  10.769328
8   20677  195503  6.913496 -3.855832  10.769328
9   20677  195504  6.913496 -3.855832  10.769328
```

---

### RDAbility

**Status**: ❌ FAILED

**Test Results**:
- Test 1 - Column names: ✅ PASSED
- Test 2 - Superset check: ❌ FAILED (Python missing 8575 Stata observations)
- Test 3 - Precision1 check: ✅ PASSED
- Test 4 - Precision2 check: ✅ PASSED

**Columns**: ['RDAbility']

**Observations**:
- Stata:  173,266
- Python: 231,277
- Common: 164,691

**Precision1**: 9.523% obs with std_diff >= 1.00e-02 (tolerance: < 10%)

**Precision2**: 99th percentile diff = 9.45e-01 (tolerance: < 1.00e+00)

**Summary Statistics** (Common Observations):

| Statistic  |          Stata |         Python |     Difference | Std Difference |
|------------|----------------|----------------|----------------|----------------|
| count      |    164691.0000 |    164691.0000 |    164691.0000 |    164691.0000 |
| mean       |         0.4654 |         0.4252 |        -0.0402 |        -0.0073 |
| std        |         5.4777 |         5.8771 |         2.6355 |         0.4811 |
| min        |      -170.7315 |      -184.0284 |      -192.6819 |       -35.1754 |
| 25%        |        -0.3627 |        -0.3703 |      -2.22e-07 |      -4.04e-08 |
| 50%        |         0.4073 |         0.3842 |      -9.38e-10 |      -1.71e-10 |
| 75%        |         1.4587 |         1.4107 |       1.84e-07 |       3.36e-08 |
| max        |        83.8592 |       121.3608 |       120.7873 |        22.0505 |

**Regression Analysis** (Python ~ Stata):

- **Model**: python = -0.0215 + 0.9598 * stata
- **R-squared**: 0.8003
- **N observations**: 164,691

| Coefficient |     Estimate |    Std Error | t-statistic |   p-value |
|-------------|--------------|--------------|-------------|----------|
| Intercept   |      -0.0215 |       0.0065 |     -3.3037 |     0.001 |
| Slope       |       0.9598 |       0.0012 |    812.4073 |     0.000 |

**Missing Observations Sample**:
```
 index  permno  yyyymm  RDAbility
     0   10116  201606   0.825915
     1   10116  201607   0.825915
     2   10116  201608   0.825915
     3   10116  201609   0.825915
     4   10116  201610   0.825915
     5   10116  201611   0.825915
     6   10116  201612   0.825915
     7   10116  201701   0.825915
     8   10116  201702   0.825915
     9   10116  201703   0.825915
```

**Feedback**:
- Num observations with std_diff >= TOL_DIFF_1: 15684/164691 (9.523%)
- Stata standard deviation: 5.48e+00

---

### RIO_Disp

**Status**: ✅ PASSED

**Test Results**:
- Test 1 - Column names: ✅ PASSED
- Test 2 - Superset check: ✅ PASSED
- Test 3 - Precision1 check: ✅ PASSED
- Test 4 - Precision2 check: ✅ PASSED

**Columns**: ['RIO_Disp']

**Observations**:
- Stata:  497,437
- Python: 513,429
- Common: 496,165

**Precision1**: 3.791% obs with std_diff >= 1.00e-02 (tolerance: < 10%)

**Precision2**: 99th percentile diff = 7.90e-01 (tolerance: < 1.00e+00)

**Summary Statistics** (Common Observations):

| Statistic  |          Stata |         Python |     Difference | Std Difference |
|------------|----------------|----------------|----------------|----------------|
| count      |    496165.0000 |    496165.0000 |    496165.0000 |    496165.0000 |
| mean       |         3.5899 |         3.5548 |        -0.0351 |        -0.0277 |
| std        |         1.2664 |         1.2633 |         0.1985 |         0.1567 |
| min        |         1.0000 |         1.0000 |        -4.0000 |        -3.1586 |
| 25%        |         3.0000 |         3.0000 |         0.0000 |         0.0000 |
| 50%        |         4.0000 |         4.0000 |         0.0000 |         0.0000 |
| 75%        |         5.0000 |         5.0000 |         0.0000 |         0.0000 |
| max        |         5.0000 |         5.0000 |         4.0000 |         3.1586 |

**Regression Analysis** (Python ~ Stata):

- **Model**: python = 0.0177 + 0.9853 * stata
- **R-squared**: 0.9755
- **N observations**: 496,165

| Coefficient |     Estimate |    Std Error | t-statistic |   p-value |
|-------------|--------------|--------------|-------------|----------|
| Intercept   |       0.0177 |     8.43e-04 |     21.0080 |     0.000 |
| Slope       |       0.9853 |     2.22e-04 |   4447.3615 |     0.000 |

**Feedback**:
- Num observations with std_diff >= TOL_DIFF_1: 18809/496165 (3.791%)
- Stata standard deviation: 1.27e+00

---

### RIO_MB

**Status**: ✅ PASSED

**Test Results**:
- Test 1 - Column names: ✅ PASSED
- Test 2 - Superset check: ✅ PASSED
- Test 3 - Precision1 check: ✅ PASSED
- Test 4 - Precision2 check: ✅ PASSED

**Columns**: ['RIO_MB']

**Observations**:
- Stata:  354,170
- Python: 366,984
- Common: 353,544

**Precision1**: 3.451% obs with std_diff >= 1.00e-02 (tolerance: < 10%)

**Precision2**: 99th percentile diff = 7.37e-01 (tolerance: < 1.00e+00)

**Summary Statistics** (Common Observations):

| Statistic  |          Stata |         Python |     Difference | Std Difference |
|------------|----------------|----------------|----------------|----------------|
| count      |    353544.0000 |    353544.0000 |    353544.0000 |    353544.0000 |
| mean       |         2.7894 |         2.7585 |        -0.0309 |        -0.0228 |
| std        |         1.3567 |         1.3451 |         0.1922 |         0.1417 |
| min        |         1.0000 |         1.0000 |        -4.0000 |        -2.9483 |
| 25%        |         2.0000 |         2.0000 |         0.0000 |         0.0000 |
| 50%        |         3.0000 |         3.0000 |         0.0000 |         0.0000 |
| 75%        |         4.0000 |         4.0000 |         0.0000 |         0.0000 |
| max        |         5.0000 |         5.0000 |         4.0000 |         2.9483 |

**Regression Analysis** (Python ~ Stata):

- **Model**: python = 0.0209 + 0.9814 * stata
- **R-squared**: 0.9799
- **N observations**: 353,544

| Coefficient |     Estimate |    Std Error | t-statistic |   p-value |
|-------------|--------------|--------------|-------------|----------|
| Intercept   |       0.0209 |     7.33e-04 |     28.4643 |     0.000 |
| Slope       |       0.9814 |     2.36e-04 |   4155.4612 |     0.000 |

**Feedback**:
- Num observations with std_diff >= TOL_DIFF_1: 12200/353544 (3.451%)
- Stata standard deviation: 1.36e+00

---

### RIO_Turnover

**Status**: ✅ PASSED

**Test Results**:
- Test 1 - Column names: ✅ PASSED
- Test 2 - Superset check: ✅ PASSED
- Test 3 - Precision1 check: ✅ PASSED
- Test 4 - Precision2 check: ✅ PASSED

**Columns**: ['RIO_Turnover']

**Observations**:
- Stata:  445,546
- Python: 462,513
- Common: 444,882

**Precision1**: 3.653% obs with std_diff >= 1.00e-02 (tolerance: < 10%)

**Precision2**: 99th percentile diff = 7.42e-01 (tolerance: < 1.00e+00)

**Summary Statistics** (Common Observations):

| Statistic  |          Stata |         Python |     Difference | Std Difference |
|------------|----------------|----------------|----------------|----------------|
| count      |    444882.0000 |    444882.0000 |    444882.0000 |    444882.0000 |
| mean       |         3.2508 |         3.2165 |        -0.0343 |        -0.0254 |
| std        |         1.3471 |         1.3412 |         0.1963 |         0.1457 |
| min        |         1.0000 |         1.0000 |        -4.0000 |        -2.9694 |
| 25%        |         2.0000 |         2.0000 |         0.0000 |         0.0000 |
| 50%        |         3.0000 |         3.0000 |         0.0000 |         0.0000 |
| 75%        |         4.0000 |         4.0000 |         0.0000 |         0.0000 |
| max        |         5.0000 |         5.0000 |         4.0000 |         2.9694 |

**Regression Analysis** (Python ~ Stata):

- **Model**: python = 0.0145 + 0.9850 * stata
- **R-squared**: 0.9788
- **N observations**: 444,882

| Coefficient |     Estimate |    Std Error | t-statistic |   p-value |
|-------------|--------------|--------------|-------------|----------|
| Intercept   |       0.0145 |     7.65e-04 |     18.9302 |     0.000 |
| Slope       |       0.9850 |     2.17e-04 |   4531.8908 |     0.000 |

**Feedback**:
- Num observations with std_diff >= TOL_DIFF_1: 16253/444882 (3.653%)
- Stata standard deviation: 1.35e+00

---

### RIO_Volatility

**Status**: ❌ FAILED

**Test Results**:
- Test 1 - Column names: ✅ PASSED
- Test 2 - Superset check: ❌ FAILED (Python missing 20887 Stata observations)
- Test 3 - Precision1 check: ✅ PASSED
- Test 4 - Precision2 check: ✅ PASSED

**Columns**: ['RIO_Volatility']

**Observations**:
- Stata:  470,062
- Python: 493,527
- Common: 449,175

**Precision1**: 4.316% obs with std_diff >= 1.00e-02 (tolerance: < 10%)

**Precision2**: 99th percentile diff = 7.46e-01 (tolerance: < 1.00e+00)

**Summary Statistics** (Common Observations):

| Statistic  |          Stata |         Python |     Difference | Std Difference |
|------------|----------------|----------------|----------------|----------------|
| count      |    449175.0000 |    449175.0000 |    449175.0000 |    449175.0000 |
| mean       |         3.4291 |         3.3898 |        -0.0392 |        -0.0293 |
| std        |         1.3400 |         1.3327 |         0.2186 |         0.1632 |
| min        |         1.0000 |         1.0000 |        -4.0000 |        -2.9851 |
| 25%        |         2.0000 |         2.0000 |         0.0000 |         0.0000 |
| 50%        |         4.0000 |         4.0000 |         0.0000 |         0.0000 |
| 75%        |         5.0000 |         5.0000 |         0.0000 |         0.0000 |
| max        |         5.0000 |         5.0000 |         4.0000 |         2.9851 |

**Regression Analysis** (Python ~ Stata):

- **Model**: python = 0.0250 + 0.9813 * stata
- **R-squared**: 0.9734
- **N observations**: 449,175

| Coefficient |     Estimate |    Std Error | t-statistic |   p-value |
|-------------|--------------|--------------|-------------|----------|
| Intercept   |       0.0250 |     8.90e-04 |     28.0960 |     0.000 |
| Slope       |       0.9813 |     2.42e-04 |   4057.7087 |     0.000 |

**Missing Observations Sample**:
```
 index  permno  yyyymm  RIO_Volatility
     0   10006  195405               4
     1   10006  197407               1
     2   10011  199103               3
     3   10011  199104               3
     4   10012  199602               3
     5   10012  199603               3
     6   10014  196704               5
     7   10014  197601               5
     8   10016  198610               3
     9   10019  199210               5
```

**Feedback**:
- Num observations with std_diff >= TOL_DIFF_1: 19387/449175 (4.316%)
- Stata standard deviation: 1.34e+00

---

### Recomm_ShortInterest

**Status**: ❌ FAILED

**Test Results**:
- Test 1 - Column names: ✅ PASSED
- Test 2 - Superset check: ❌ FAILED (Python missing 19305 Stata observations)
- Test 3 - Precision1 check: ✅ PASSED
- Test 4 - Precision2 check: ✅ PASSED

**Columns**: ['Recomm_ShortInterest']

**Observations**:
- Stata:  34,619
- Python: 35,419
- Common: 15,314

**Precision1**: 0.000% obs with std_diff >= 1.00e-02 (tolerance: < 10%)

**Precision2**: 99th percentile diff = 0.00e+00 (tolerance: < 1.00e+00)

**Summary Statistics** (Common Observations):

| Statistic  |          Stata |         Python |     Difference | Std Difference |
|------------|----------------|----------------|----------------|----------------|
| count      |     15314.0000 |     15314.0000 |     15314.0000 |     15314.0000 |
| mean       |         0.4465 |         0.4465 |         0.0000 |         0.0000 |
| std        |         0.4971 |         0.4971 |         0.0000 |         0.0000 |
| min        |         0.0000 |         0.0000 |         0.0000 |         0.0000 |
| 25%        |         0.0000 |         0.0000 |         0.0000 |         0.0000 |
| 50%        |         0.0000 |         0.0000 |         0.0000 |         0.0000 |
| 75%        |         1.0000 |         1.0000 |         0.0000 |         0.0000 |
| max        |         1.0000 |         1.0000 |         0.0000 |         0.0000 |

**Regression Analysis** (Python ~ Stata):

- **Model**: python = 0.0000 + 1.0000 * stata
- **R-squared**: 1.0000
- **N observations**: 15,314

| Coefficient |     Estimate |    Std Error | t-statistic |   p-value |
|-------------|--------------|--------------|-------------|----------|
| Intercept   |     5.11e-15 |     5.88e-17 |     86.8919 |     0.000 |
| Slope       |       1.0000 |     8.81e-17 |    1.14e+16 |     0.000 |

**Missing Observations Sample**:
```
 index  permno  yyyymm  Recomm_ShortInterest
     0   10051  200704                     1
     1   10104  200607                     1
     2   10104  200807                     1
     3   10104  200808                     1
     4   10104  200903                     1
     5   10104  200904                     1
     6   10104  200906                     1
     7   10104  201402                     1
     8   10104  201507                     1
     9   10104  201508                     1
```

**Feedback**:
- Num observations with std_diff >= TOL_DIFF_1: 0/15314 (0.000%)
- Stata standard deviation: 4.97e-01

---

### ReturnSkew3F

**Status**: ✅ PASSED

**Test Results**:
- Test 1 - Column names: ✅ PASSED
- Test 2 - Superset check: ✅ PASSED
- Test 3 - Precision1 check: ✅ PASSED
- Test 4 - Precision2 check: ✅ PASSED

**Columns**: ['ReturnSkew3F']

**Observations**:
- Stata:  4,978,948
- Python: 4,988,237
- Common: 4,978,948

**Precision1**: 2.676% obs with std_diff >= 1.00e-02 (tolerance: < 10%)

**Precision2**: 99th percentile diff = 2.70e-02 (tolerance: < 1.00e+00)

**Summary Statistics** (Common Observations):

| Statistic  |          Stata |         Python |     Difference | Std Difference |
|------------|----------------|----------------|----------------|----------------|
| count      |       4.98e+06 |       4.98e+06 |       4.98e+06 |       4.98e+06 |
| mean       |         0.1540 |         0.1539 |      -1.18e-04 |      -1.39e-04 |
| std        |         0.8499 |         0.8379 |         0.1564 |         0.1840 |
| min        |        -4.8206 |        -3.9998 |        -5.9063 |        -6.9498 |
| 25%        |        -0.2811 |        -0.2797 |      -2.22e-15 |      -2.61e-15 |
| 50%        |         0.1296 |         0.1302 |         0.0000 |         0.0000 |
| 75%        |         0.5700 |         0.5689 |       2.22e-15 |       2.61e-15 |
| max        |         4.7150 |         3.9999 |         5.1167 |         6.0206 |

**Regression Analysis** (Python ~ Stata):

- **Model**: python = 0.0046 + 0.9691 * stata
- **R-squared**: 0.9661
- **N observations**: 4,978,948

| Coefficient |     Estimate |    Std Error | t-statistic |   p-value |
|-------------|--------------|--------------|-------------|----------|
| Intercept   |       0.0046 |     7.02e-05 |     66.0724 |     0.000 |
| Slope       |       0.9691 |     8.13e-05 |  11919.6235 |     0.000 |

**Feedback**:
- Num observations with std_diff >= TOL_DIFF_1: 133232/4978948 (2.676%)
- Stata standard deviation: 8.50e-01

---

### ShareVol

**Status**: ❌ FAILED

**Test Results**:
- Test 1 - Column names: ✅ PASSED
- Test 2 - Superset check: ❌ FAILED (Python missing 298069 Stata observations)
- Test 3 - Precision1 check: ✅ PASSED
- Test 4 - Precision2 check: ✅ PASSED

**Columns**: ['ShareVol']

**Observations**:
- Stata:  1,660,340
- Python: 1,363,028
- Common: 1,362,271

**Precision1**: 0.000% obs with std_diff >= 1.00e-02 (tolerance: < 10%)

**Precision2**: 99th percentile diff = 0.00e+00 (tolerance: < 1.00e+00)

**Summary Statistics** (Common Observations):

| Statistic  |          Stata |         Python |     Difference | Std Difference |
|------------|----------------|----------------|----------------|----------------|
| count      |       1.36e+06 |       1.36e+06 |       1.36e+06 |       1.36e+06 |
| mean       |         0.1543 |         0.1543 |         0.0000 |         0.0000 |
| std        |         0.3612 |         0.3612 |         0.0000 |         0.0000 |
| min        |         0.0000 |         0.0000 |         0.0000 |         0.0000 |
| 25%        |         0.0000 |         0.0000 |         0.0000 |         0.0000 |
| 50%        |         0.0000 |         0.0000 |         0.0000 |         0.0000 |
| 75%        |         0.0000 |         0.0000 |         0.0000 |         0.0000 |
| max        |         1.0000 |         1.0000 |         0.0000 |         0.0000 |

**Regression Analysis** (Python ~ Stata):

- **Model**: python = 0.0000 + 1.0000 * stata
- **R-squared**: 1.0000
- **N observations**: 1,362,271

| Coefficient |     Estimate |    Std Error | t-statistic |   p-value |
|-------------|--------------|--------------|-------------|----------|
| Intercept   |     2.30e-13 |     5.05e-16 |    456.3895 |     0.000 |
| Slope       |       1.0000 |     1.29e-15 |    7.78e+14 |     0.000 |

**Missing Observations Sample**:
```
 index  permno  yyyymm  ShareVol
     0   10000  198601         1
     1   10000  198602         1
     2   10001  198601         1
     3   10001  198602         1
     4   10002  198601         1
     5   10002  198602         1
     6   10003  198601         1
     7   10003  198602         1
     8   10005  198601         1
     9   10005  198602         1
```

**Feedback**:
- Num observations with std_diff >= TOL_DIFF_1: 0/1362271 (0.000%)
- Stata standard deviation: 3.61e-01

---

### Tax

**Status**: ✅ PASSED

**Test Results**:
- Test 1 - Column names: ✅ PASSED
- Test 2 - Superset check: ✅ PASSED
- Test 3 - Precision1 check: ✅ PASSED
- Test 4 - Precision2 check: ✅ PASSED

**Columns**: ['Tax']

**Observations**:
- Stata:  3,211,651
- Python: 3,213,292
- Common: 3,211,651

**Precision1**: 1.244% obs with std_diff >= 1.00e-02 (tolerance: < 10%)

**Precision2**: 99th percentile diff = 3.22e-02 (tolerance: < 1.00e+00)

**Summary Statistics** (Common Observations):

| Statistic  |          Stata |         Python |     Difference | Std Difference |
|------------|----------------|----------------|----------------|----------------|
| count      |       3.21e+06 |       3.21e+06 |       3.21e+06 |       3.21e+06 |
| mean       |         1.1689 |         1.1833 |         0.0144 |       7.57e-04 |
| std        |        19.0252 |        19.4556 |         4.0707 |         0.2140 |
| min        |     -2742.5000 |     -2742.5000 |        -1.0000 |        -0.0526 |
| 25%        |         0.0341 |         0.0265 |      -1.74e-08 |      -9.15e-10 |
| 50%        |         1.0000 |         1.0000 |         0.0000 |         0.0000 |
| 75%        |         1.4267 |         1.4359 |       1.28e-10 |       6.75e-12 |
| max        |      4463.7114 |      4463.7113 |      2022.5294 |       106.3082 |

**Regression Analysis** (Python ~ Stata):

- **Model**: python = 0.0144 + 1.0000 * stata
- **R-squared**: 0.9562
- **N observations**: 3,211,651

| Coefficient |     Estimate |    Std Error | t-statistic |   p-value |
|-------------|--------------|--------------|-------------|----------|
| Intercept   |       0.0144 |       0.0023 |      6.3339 |     0.000 |
| Slope       |       1.0000 |     1.19e-04 |   8375.7860 |     0.000 |

**Feedback**:
- Num observations with std_diff >= TOL_DIFF_1: 39943/3211651 (1.244%)
- Stata standard deviation: 1.90e+01

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
- Python: 2,056,304
- Common: 2,055,856

**Precision1**: 97.137% obs with std_diff >= 1.00e-02 (tolerance: < 10%)

**Precision2**: 99th percentile diff = 1.69e+00 (tolerance: < 1.00e+00)

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

---

### UpRecomm

**Status**: ❌ FAILED

**Test Results**:
- Test 1 - Column names: ✅ PASSED
- Test 2 - Superset check: ❌ FAILED (Python missing 14792 Stata observations)
- Test 3 - Precision1 check: ✅ PASSED
- Test 4 - Precision2 check: ✅ PASSED

**Columns**: ['UpRecomm']

**Observations**:
- Stata:  463,983
- Python: 450,458
- Common: 449,191

**Precision1**: 0.023% obs with std_diff >= 1.00e-02 (tolerance: < 10%)

**Precision2**: 99th percentile diff = 0.00e+00 (tolerance: < 1.00e+00)

**Summary Statistics** (Common Observations):

| Statistic  |          Stata |         Python |     Difference | Std Difference |
|------------|----------------|----------------|----------------|----------------|
| count      |    449191.0000 |    449191.0000 |    449191.0000 |    449191.0000 |
| mean       |         0.3622 |         0.3622 |       2.23e-06 |       4.63e-06 |
| std        |         0.4806 |         0.4806 |         0.0153 |         0.0318 |
| min        |         0.0000 |         0.0000 |        -1.0000 |        -2.0806 |
| 25%        |         0.0000 |         0.0000 |         0.0000 |         0.0000 |
| 50%        |         0.0000 |         0.0000 |         0.0000 |         0.0000 |
| 75%        |         1.0000 |         1.0000 |         0.0000 |         0.0000 |
| max        |         1.0000 |         1.0000 |         1.0000 |         2.0806 |

**Regression Analysis** (Python ~ Stata):

- **Model**: python = 0.0002 + 0.9995 * stata
- **R-squared**: 0.9990
- **N observations**: 449,191

| Coefficient |     Estimate |    Std Error | t-statistic |   p-value |
|-------------|--------------|--------------|-------------|----------|
| Intercept   |     1.85e-04 |     2.86e-05 |      6.4772 |     0.000 |
| Slope       |       0.9995 |     4.75e-05 |  21061.2947 |     0.000 |

**Missing Observations Sample**:
```
 index  permno  yyyymm  UpRecomm
     0   10001  199311         0
     1   10002  200210         0
     2   10010  199311         0
     3   10011  199511         0
     4   10012  199402         0
     5   10016  199312         0
     6   10019  199403         0
     7   10025  199801         0
     8   10026  199311         0
     9   10028  202103         0
```

**Feedback**:
- Num observations with std_diff >= TOL_DIFF_1: 105/449191 (0.023%)
- Stata standard deviation: 4.81e-01

---

### VolumeTrend

**Status**: ✅ PASSED

**Test Results**:
- Test 1 - Column names: ✅ PASSED
- Test 2 - Superset check: ✅ PASSED
- Test 3 - Precision1 check: ✅ PASSED
- Test 4 - Precision2 check: ✅ PASSED

**Columns**: ['VolumeTrend']

**Observations**:
- Stata:  3,655,889
- Python: 5,153,763
- Common: 3,655,889

**Precision1**: 1.357% obs with std_diff >= 1.00e-02 (tolerance: < 10%)

**Precision2**: 99th percentile diff = 9.34e-02 (tolerance: < 1.00e+00)

**Summary Statistics** (Common Observations):

| Statistic  |          Stata |         Python |     Difference | Std Difference |
|------------|----------------|----------------|----------------|----------------|
| count      |       3.66e+06 |       3.66e+06 |       3.66e+06 |       3.66e+06 |
| mean       |         0.0057 |         0.0057 |       5.70e-05 |         0.0028 |
| std        |         0.0207 |         0.0208 |         0.0022 |         0.1068 |
| min        |        -0.0566 |        -0.0517 |        -0.0631 |        -3.0497 |
| 25%        |        -0.0068 |        -0.0069 |      -2.22e-10 |      -1.07e-08 |
| 50%        |         0.0052 |         0.0052 |       6.53e-13 |       3.16e-11 |
| 75%        |         0.0184 |         0.0186 |       2.32e-10 |       1.12e-08 |
| max        |         0.0664 |         0.1665 |         0.1636 |         7.9103 |

**Regression Analysis** (Python ~ Stata):

- **Model**: python = 0.0001 + 0.9983 * stata
- **R-squared**: 0.9887
- **N observations**: 3,655,889

| Coefficient |     Estimate |    Std Error | t-statistic |   p-value |
|-------------|--------------|--------------|-------------|----------|
| Intercept   |     6.67e-05 |     1.20e-06 |     55.6825 |     0.000 |
| Slope       |       0.9983 |     5.59e-05 |  17866.8269 |     0.000 |

**Feedback**:
- Num observations with std_diff >= TOL_DIFF_1: 49596/3655889 (1.357%)
- Stata standard deviation: 2.07e-02

---

### retConglomerate

**Status**: ✅ PASSED

**Test Results**:
- Test 1 - Column names: ✅ PASSED
- Test 2 - Superset check: ✅ PASSED
- Test 3 - Precision1 check: ✅ PASSED
- Test 4 - Precision2 check: ✅ PASSED

**Columns**: ['retConglomerate']

**Observations**:
- Stata:  758,394
- Python: 759,896
- Common: 758,382

**Precision1**: 0.936% obs with std_diff >= 1.00e-02 (tolerance: < 10%)

**Precision2**: 99th percentile diff = 9.35e-03 (tolerance: < 1.00e+00)

**Summary Statistics** (Common Observations):

| Statistic  |          Stata |         Python |     Difference | Std Difference |
|------------|----------------|----------------|----------------|----------------|
| count      |    758382.0000 |    758382.0000 |    758382.0000 |    758382.0000 |
| mean       |         0.0106 |         0.0106 |      -1.25e-05 |      -1.49e-04 |
| std        |         0.0841 |         0.0841 |         0.0020 |         0.0240 |
| min        |        -0.8000 |        -0.8000 |        -0.4277 |        -5.0889 |
| 25%        |        -0.0313 |        -0.0313 |      -2.78e-17 |      -3.30e-16 |
| 50%        |         0.0105 |         0.0105 |         0.0000 |         0.0000 |
| 75%        |         0.0495 |         0.0495 |       2.78e-17 |       3.30e-16 |
| max        |         4.3779 |         4.3779 |         0.4479 |         5.3290 |

**Regression Analysis** (Python ~ Stata):

- **Model**: python = -0.0000 + 0.9997 * stata
- **R-squared**: 0.9994
- **N observations**: 758,382

| Coefficient |     Estimate |    Std Error | t-statistic |   p-value |
|-------------|--------------|--------------|-------------|----------|
| Intercept   |    -9.83e-06 |     2.33e-06 |     -4.2168 |     0.000 |
| Slope       |       0.9997 |     2.75e-05 |  36318.4957 |     0.000 |

**Feedback**:
- Num observations with std_diff >= TOL_DIFF_1: 7102/758382 (0.936%)
- Stata standard deviation: 8.41e-02

---

### sinAlgo

**Status**: ❌ FAILED

**Test Results**:
- Test 1 - Column names: ✅ PASSED
- Test 2 - Superset check: ❌ FAILED (Python missing 37059 Stata observations)
- Test 3 - Precision1 check: ✅ PASSED
- Test 4 - Precision2 check: ✅ PASSED

**Columns**: ['sinAlgo']

**Observations**:
- Stata:  233,503
- Python: 908,711
- Common: 196,444

**Precision1**: 0.012% obs with std_diff >= 1.00e-02 (tolerance: < 10%)

**Precision2**: 99th percentile diff = 0.00e+00 (tolerance: < 1.00e+00)

**Summary Statistics** (Common Observations):

| Statistic  |          Stata |         Python |     Difference | Std Difference |
|------------|----------------|----------------|----------------|----------------|
| count      |    196444.0000 |    196444.0000 |    196444.0000 |    196444.0000 |
| mean       |         0.2142 |         0.2143 |       1.17e-04 |       2.85e-04 |
| std        |         0.4102 |         0.4103 |         0.0108 |         0.0264 |
| min        |         0.0000 |         0.0000 |         0.0000 |         0.0000 |
| 25%        |         0.0000 |         0.0000 |         0.0000 |         0.0000 |
| 50%        |         0.0000 |         0.0000 |         0.0000 |         0.0000 |
| 75%        |         0.0000 |         0.0000 |         0.0000 |         0.0000 |
| max        |         1.0000 |         1.0000 |         1.0000 |         2.4376 |

**Regression Analysis** (Python ~ Stata):

- **Model**: python = 0.0001 + 0.9999 * stata
- **R-squared**: 0.9993
- **N observations**: 196,444

| Coefficient |     Estimate |    Std Error | t-statistic |   p-value |
|-------------|--------------|--------------|-------------|----------|
| Intercept   |     1.49e-04 |     2.75e-05 |      5.4104 |     0.000 |
| Slope       |       0.9999 |     5.95e-05 |  16802.6819 |     0.000 |

**Missing Observations Sample**:
```
 index  permno  yyyymm  sinAlgo
     0   10021  198601        0
     1   10021  198602        0
     2   10021  198603        0
     3   10021  198604        0
     4   10021  198605        0
     5   10021  198606        0
     6   10021  198607        0
     7   10021  198608        0
     8   10021  198609        0
     9   10021  198610        0
```

**Feedback**:
- Num observations with std_diff >= TOL_DIFF_1: 23/196444 (0.012%)
- Stata standard deviation: 4.10e-01

---

