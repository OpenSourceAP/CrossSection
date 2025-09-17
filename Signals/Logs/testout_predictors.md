# Predictor Validation Results

**Generated**: 2025-09-17 15:47:21

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
| MomOffSeason16YrPlus      | ✅ (0.00%) | ❌ (+26.6%)  | ❌ (1.7%)     | ❌ (1.2E+00)   | ❌ (+0.30)  |
| MomOffSeason*             | ✅ (0.00%) | ❌ (+10.9%)  | ❌ (1.6%)     | ❌ (2.4E+00)   | ✅ (-0.06)  |
| MomOffSeason06YrPlus*     | ✅ (0.00%) | ❌ (+10.6%)  | ❌ (2.6%)     | ❌ (3.9E+00)   | ❌ (+0.40)  |
| MomOffSeason11YrPlus*     | ✅ (0.00%) | ❌ (+9.8%)   | ❌ (3.1%)     | ❌ (5.8E+00)   | ❌ (-0.48)  |
| Mom12mOffSeason*          | ✅ (0.00%) | ❌ (+5.6%)   | ❌ (91.9%)    | ❌ (2.4E+00)   | ❌ (+0.64)  |

**Overall**: 4/5 available predictors passed validation
  - Natural passes: 0
  - Overridden passes: 4
**Python CSVs**: 5/5 predictors have Python implementation
\* = Manual override applied (see Predictors/overrides.yaml for details)

## Detailed Results

### Mom12mOffSeason

**Status**: ✅ PASSED (with override)

**Override Applied**:
- Reviewed on: 2025-09-17
- Reviewed by: ac
- Details: This script was greatly streamlined relative to Stata. We no longer use asrol. The new t-stat is 4.49 which is close to the original paper's 4.20.

**Test Results**:
- Test 1 - Superset check: ✅ PASSED
- Test 2 - NumRows check: ❌ FAILED (Python has +5.63% rows vs Stata)
- Test 3 - Precision1 check: ❌ FAILED
- Test 4 - Precision2 check: ❌ FAILED
- Test 5 - T-stat check: NA

**Observations**:
- Stata:  3,865,561
- Python: 4,083,294
- Common: 3,865,561

**Precision1**: 91.881% obs with std_diff >= 1.00e-02 (tolerance: < 1%)

**Precision2**: 100th percentile diff = 2.41e+00 (tolerance: < 1.00e-01)

**Summary Statistics** (Common Observations):

| Statistic  |          Stata |         Python |     Difference | Std Difference |
|------------|----------------|----------------|----------------|----------------|
| count      |       3.87e+06 |       3.87e+06 |       3.87e+06 |       3.87e+06 |
| mean       |         0.0113 |         0.0113 |      -1.15e-06 |      -1.97e-05 |
| std        |         0.0582 |         0.0551 |         0.0181 |         0.3115 |
| min        |        -0.5758 |        -0.5598 |        -0.4840 |        -8.3183 |
| 25%        |        -0.0153 |        -0.0140 |        -0.0076 |        -0.1308 |
| 50%        |         0.0096 |         0.0097 |      -3.51e-04 |        -0.0060 |
| 75%        |         0.0351 |         0.0340 |         0.0062 |         0.1061 |
| max        |         4.2943 |         3.9052 |         2.4084 |        41.3889 |

**Regression Analysis** (Python ~ Stata):

- **Model**: python = 0.0011 + 0.9005 * stata
- **R-squared**: 0.9030
- **N observations**: 3,865,561

| Coefficient |     Estimate |    Std Error | t-statistic |   p-value |
|-------------|--------------|--------------|-------------|----------|
| Intercept   |       0.0011 |     8.90e-06 |    126.5602 |     0.000 |
| Slope       |       0.9005 |     1.50e-04 |   5998.6294 |     0.000 |

**Feedback**:
- Num observations with std_diff >= TOL_DIFF_1: 3551724/3865561 (91.881%)
- Stata standard deviation: 5.82e-02

**Most Recent Bad Observations**:
```
   permno  yyyymm    python     stata      diff
0   10026  202412  0.012609  0.023884 -0.011275
1   10028  202412  0.048512  0.055180 -0.006667
2   10032  202412  0.059734  0.066746 -0.007012
3   10044  202412 -0.027687 -0.032152  0.004465
4   10066  202412  0.045816  0.049737 -0.003921
5   10104  202412  0.056671  0.062988 -0.006317
6   10107  202412  0.008458  0.004700  0.003758
7   10138  202412  0.018862  0.015938  0.002924
8   10145  202412  0.017729  0.021045 -0.003316
9   10158  202412  0.061113  0.065021 -0.003908
```

**Largest Differences**:
```
   permno  yyyymm    python     stata      diff
0   58748  199211  2.324494 -0.083895  2.408390
1   16400  201911  1.681095 -0.341405  2.022499
2   53154  199406  2.140353  0.267058  1.873294
3   23199  202402  1.642566 -0.210839  1.853405
4   48072  202111  1.695673 -0.071991  1.767664
5   89301  202111  1.654405  0.032613  1.621792
6   23007  202311  1.428378 -0.141880  1.570258
7   86916  202104  1.409701 -0.040112  1.449813
8   91186  201003  1.323391 -0.029015  1.352407
9   83852  199909  1.225646 -0.045579  1.271225
```

**Largest Differences Before 1950**:
```
   permno  yyyymm    python     stata      diff
0   13004  193402  0.586630 -0.002510  0.589140
1   17443  194007  0.463422 -0.040643  0.504064
2   11797  193306  0.634524  0.149471  0.485053
3   12212  194007  0.407744 -0.062102  0.469847
4   13872  194007  0.329524 -0.115344  0.444868
5   15579  193305  0.465776  0.073084  0.392692
6   11252  194211  0.492040  0.102266  0.389773
7   16336  193403  0.400635  0.028483  0.372152
8   11383  192903  0.326732 -0.044372  0.371104
9   16045  193306  0.489393  0.121548  0.367845
```

---

### MomOffSeason

**Status**: ✅ PASSED (with override)

**Override Applied**:
- Reviewed on: 2025-09-17
- Reviewed by: ac
- Details: This script was greatly streamlined relative to Stata. We no longer use asrol. The new t-stat is 4.88, which is very close to the previous t-stat.

**Test Results**:
- Test 1 - Superset check: ✅ PASSED
- Test 2 - NumRows check: ❌ FAILED (Python has +10.90% rows vs Stata)
- Test 3 - Precision1 check: ❌ FAILED
- Test 4 - Precision2 check: ❌ FAILED
- Test 5 - T-stat check: NA

**Observations**:
- Stata:  3,396,704
- Python: 3,767,024
- Common: 3,396,704

**Precision1**: 1.566% obs with std_diff >= 1.00e-02 (tolerance: < 1%)

**Precision2**: 100th percentile diff = 2.39e+00 (tolerance: < 1.00e-01)

**Summary Statistics** (Common Observations):

| Statistic  |          Stata |         Python |     Difference | Std Difference |
|------------|----------------|----------------|----------------|----------------|
| count      |       3.40e+06 |       3.40e+06 |       3.40e+06 |       3.40e+06 |
| mean       |         0.0125 |         0.0124 |      -7.25e-05 |        -0.0027 |
| std        |         0.0270 |         0.0261 |         0.0063 |         0.2334 |
| min        |        -4.1713 |        -0.3205 |        -1.2248 |       -45.3920 |
| 25%        |       3.95e-04 |       3.57e-04 |      -5.18e-10 |      -1.92e-08 |
| 50%        |         0.0119 |         0.0118 |         0.0000 |         0.0000 |
| 75%        |         0.0240 |         0.0239 |       5.07e-10 |       1.88e-08 |
| max        |         1.5150 |         1.5150 |         4.0798 |       151.1992 |

**Regression Analysis** (Python ~ Stata):

- **Model**: python = 0.0007 + 0.9407 * stata
- **R-squared**: 0.9455
- **N observations**: 3,396,704

| Coefficient |     Estimate |    Std Error | t-statistic |   p-value |
|-------------|--------------|--------------|-------------|----------|
| Intercept   |     6.66e-04 |     3.64e-06 |    183.0492 |     0.000 |
| Slope       |       0.9407 |     1.22e-04 |   7679.9565 |     0.000 |

**Feedback**:
- Num observations with std_diff >= TOL_DIFF_1: 53202/3396704 (1.566%)
- Stata standard deviation: 2.70e-02

**Most Recent Bad Observations**:
```
   permno  yyyymm    python     stata      diff
0   10066  202412 -0.035075 -0.048228  0.013153
1   11153  202412  0.024630  0.040138 -0.015508
2   11379  202412 -0.007882  0.014271 -0.022152
3   12799  202412  0.012392  0.074968 -0.062576
4   12928  202412 -0.012359 -0.024719  0.012359
5   13563  202412  0.003557  0.005397 -0.001840
6   13828  202412  0.021456  0.023601 -0.002146
7   13878  202412  0.017654  0.022194 -0.004540
8   14051  202412 -0.002322 -0.003499  0.001177
9   14469  202412 -0.007548 -0.012774  0.005226
```

**Largest Differences**:
```
   permno  yyyymm    python     stata      diff
0   89169  202105 -0.091515 -4.171327  4.079812
1   44230  198407 -0.012207 -1.585526  1.573319
2   92161  199008 -0.043818 -1.574922  1.531104
3   78414  198610  0.075186  1.300000 -1.224814
4   79704  200304 -0.024728  1.166667 -1.191395
5   82810  200509 -0.051027 -1.145503  1.094476
6   77324  200102  0.003466  1.086957 -1.083491
7   10097  199202 -0.026417  1.000000 -1.026417
8   10685  199512 -0.009902 -1.021461  1.011558
9   80054  200306 -0.050757 -1.002423  0.951666
```

**Largest Differences Before 1950**:
```
   permno  yyyymm    python     stata      diff
0   16408  193608  0.008585  0.019882 -0.011297
1   16408  193611  0.010299  0.020599 -0.010299
2   16408  193702  0.011422  0.020941 -0.009519
3   16408  193607  0.006189  0.015128 -0.008939
4   16408  193701  0.008498  0.016258 -0.007759
5   16408  193612  0.007490  0.014980 -0.007490
6   16408  193512 -0.002398 -0.009591  0.007193
7   16408  193708  0.014184  0.020803 -0.006619
8   16408  193703  0.008198  0.014429 -0.006231
9   16408  193707  0.010119  0.015353 -0.005234
```

---

### MomOffSeason06YrPlus

**Status**: ✅ PASSED (with override)

**Override Applied**:
- Reviewed on: 2025-09-17
- Reviewed by: ac
- Details: This script was greatly streamlined relative to Stata. We no longer use asrol. The new t-stat is 4.71, which is +0.40 higher than the previous t-stat, but it's very close to the original paper's 4.62.

**Test Results**:
- Test 1 - Superset check: ✅ PASSED
- Test 2 - NumRows check: ❌ FAILED (Python has +10.61% rows vs Stata)
- Test 3 - Precision1 check: ❌ FAILED
- Test 4 - Precision2 check: ❌ FAILED
- Test 5 - T-stat check: NA

**Observations**:
- Stata:  2,425,319
- Python: 2,682,540
- Common: 2,425,319

**Precision1**: 2.584% obs with std_diff >= 1.00e-02 (tolerance: < 1%)

**Precision2**: 100th percentile diff = 3.85e+00 (tolerance: < 1.00e-01)

**Summary Statistics** (Common Observations):

| Statistic  |          Stata |         Python |     Difference | Std Difference |
|------------|----------------|----------------|----------------|----------------|
| count      |       2.43e+06 |       2.43e+06 |       2.43e+06 |       2.43e+06 |
| mean       |         0.0130 |         0.0132 |       1.32e-04 |         0.0041 |
| std        |         0.0324 |         0.0224 |         0.0226 |         0.6993 |
| min        |        -4.8725 |        -0.2679 |       -15.6437 |      -483.2416 |
| 25%        |         0.0027 |         0.0027 |      -4.55e-10 |      -1.40e-08 |
| 50%        |         0.0125 |         0.0125 |         0.0000 |         0.0000 |
| 75%        |         0.0233 |         0.0232 |       4.55e-10 |       1.40e-08 |
| max        |        15.8923 |         0.7811 |         4.8320 |       149.2626 |

**Regression Analysis** (Python ~ Stata):

- **Model**: python = 0.0067 + 0.4955 * stata
- **R-squared**: 0.5115
- **N observations**: 2,425,319

| Coefficient |     Estimate |    Std Error | t-statistic |   p-value |
|-------------|--------------|--------------|-------------|----------|
| Intercept   |       0.0067 |     1.09e-05 |    618.3142 |     0.000 |
| Slope       |       0.4955 |     3.11e-04 |   1593.5930 |     0.000 |

**Feedback**:
- Num observations with std_diff >= TOL_DIFF_1: 62670/2425319 (2.584%)
- Stata standard deviation: 3.24e-02

**Most Recent Bad Observations**:
```
   permno  yyyymm    python     stata      diff
0   11379  202412 -0.016035 -0.019014  0.002980
1   12146  202412  0.003773  0.004235 -0.000462
2   12592  202412 -0.025234 -0.028323  0.003090
3   12799  202412  0.019427  0.023379 -0.003953
4   13563  202412 -0.015532 -0.048507  0.032975
5   13828  202412 -0.018145 -0.008100 -0.010045
6   13878  202412  0.005553  0.019389 -0.013836
7   14051  202412 -0.052231 -0.051790 -0.000441
8   14877  202412 -0.020449 -0.022052  0.001604
9   15294  202412 -0.048290 -0.073018  0.024727
```

**Largest Differences**:
```
   permno  yyyymm    python      stata       diff
0   13755  202211  0.248598  15.892301 -15.643703
1   13755  202111  0.310748  15.892301 -15.581553
2   13755  202011  0.414330  15.892301 -15.477971
3   83382  200510 -0.040478  -4.872470   4.831992
4   10685  199412 -0.042227  -3.649201   3.606974
5   81728  200612 -0.064663  -3.352354   3.287691
6   86237  201012 -0.013335   3.244835  -3.258170
7   88321  200611 -0.115412   2.289885  -2.405297
8   76356  198510  0.036092  -2.300340   2.336433
9   12715  198603 -0.001958   2.214316  -2.216274
```

**Largest Differences Before 1950**:
```
   permno  yyyymm    python     stata      diff
0   16408  193402  0.015001 -0.110645  0.125646
1   16408  193403  0.015493 -0.043396  0.058889
2   16408  193502  0.009108 -0.036882  0.045990
3   16408  193602  0.006539 -0.036882  0.043421
4   16408  193407  0.010819 -0.031911  0.042730
5   16408  193702  0.005100 -0.036882  0.041982
6   16408  193802  0.004434 -0.036882  0.041316
7   16408  193507  0.007213 -0.031911  0.039124
8   16408  193503  0.009616 -0.028931  0.038547
9   16408  193411  0.011496 -0.026085  0.037581
```

---

### MomOffSeason11YrPlus

**Status**: ✅ PASSED (with override)

**Override Applied**:
- Reviewed on: 2025-09-17
- Reviewed by: ac
- Details: This script was greatly streamlined relative to Stata. We no longer use asrol. The new t-stat is 1.56, which is -0.48 lower than the previous t-stat, but it's close to the original paper's 1.77. Note this was a likely predictor, not a clear predictor (obviously).

**Test Results**:
- Test 1 - Superset check: ✅ PASSED
- Test 2 - NumRows check: ❌ FAILED (Python has +9.81% rows vs Stata)
- Test 3 - Precision1 check: ❌ FAILED
- Test 4 - Precision2 check: ❌ FAILED
- Test 5 - T-stat check: NA

**Observations**:
- Stata:  1,677,532
- Python: 1,842,138
- Common: 1,677,532

**Precision1**: 3.092% obs with std_diff >= 1.00e-02 (tolerance: < 1%)

**Precision2**: 100th percentile diff = 5.76e+00 (tolerance: < 1.00e-01)

**Summary Statistics** (Common Observations):

| Statistic  |          Stata |         Python |     Difference | Std Difference |
|------------|----------------|----------------|----------------|----------------|
| count      |       1.68e+06 |       1.68e+06 |       1.68e+06 |       1.68e+06 |
| mean       |         0.0135 |         0.0136 |       1.19e-04 |         0.0047 |
| std        |         0.0254 |         0.0215 |         0.0127 |         0.4983 |
| min        |        -2.6111 |        -0.2782 |        -2.2556 |       -88.7393 |
| 25%        |         0.0034 |         0.0034 |      -4.55e-10 |      -1.79e-08 |
| 50%        |         0.0128 |         0.0128 |         0.0000 |         0.0000 |
| 75%        |         0.0235 |         0.0233 |       4.55e-10 |       1.79e-08 |
| max        |         2.2478 |         0.3816 |         2.6319 |       103.5419 |

**Regression Analysis** (Python ~ Stata):

- **Model**: python = 0.0037 + 0.7331 * stata
- **R-squared**: 0.7521
- **N observations**: 1,677,532

| Coefficient |     Estimate |    Std Error | t-statistic |   p-value |
|-------------|--------------|--------------|-------------|----------|
| Intercept   |       0.0037 |     9.35e-06 |    398.3669 |     0.000 |
| Slope       |       0.7331 |     3.25e-04 |   2256.1920 |     0.000 |

**Feedback**:
- Num observations with std_diff >= TOL_DIFF_1: 51866/1677532 (3.092%)
- Stata standard deviation: 2.54e-02

**Most Recent Bad Observations**:
```
   permno  yyyymm    python     stata      diff
0   10028  202412  0.010101  0.011574 -0.001473
1   10966  202412  0.007126  0.024496 -0.017370
2   11379  202412  0.022511  0.029216 -0.006706
3   11636  202412 -0.028132 -0.064470  0.036337
4   11803  202412 -0.000620 -0.000875  0.000255
5   12495  202412  0.040573  0.044531 -0.003958
6   12799  202412 -0.005228 -0.080205  0.074976
7   12877  202412  0.002364  0.002955 -0.000591
8   12890  202412 -0.053182 -0.118182  0.065000
9   13455  202412  0.008303  0.009632 -0.001329
```

**Largest Differences**:
```
   permno  yyyymm    python     stata      diff
0   11803  201112  0.020796 -2.611104  2.631900
1   77729  200404  0.016586 -2.373474  2.390060
2   33136  197712 -0.007831  2.247807 -2.255638
3   24110  198612 -0.046078  2.129370 -2.175448
4   65518  200005 -0.014146  1.961642 -1.975788
5   36492  197902  0.057469  1.643900 -1.586431
6   11803  201110  0.081820 -1.379478  1.461298
7   86092  201008  0.196499  1.608412 -1.411913
8   82163  201403  0.054147 -1.259050  1.313197
9   14761  200804  0.022150  1.294914 -1.272764
```

**Largest Differences Before 1950**:
```
   permno  yyyymm    python     stata      diff
0   16408  194306  0.004657  0.025613 -0.020956
1   16408  194301  0.006446  0.025323 -0.018877
2   16408  194305  0.004475  0.022376 -0.017901
3   16408  194212  0.006102  0.022374 -0.016272
4   16408  194205  0.008909  0.023610 -0.014700
5   16408  194302  0.004434  0.018760 -0.014326
6   16408  194210  0.006148  0.019892 -0.013744
7   16408  194508  0.006868  0.019882 -0.013014
8   16408  194310  0.001586  0.014541 -0.012955
9   16408  194209  0.006126  0.018718 -0.012592
```

---

### MomOffSeason16YrPlus

**Status**: ❌ FAILED

**Test Results**:
- Test 1 - Superset check: ✅ PASSED
- Test 2 - NumRows check: ❌ FAILED (Python has +26.57% rows vs Stata)
- Test 3 - Precision1 check: ❌ FAILED
- Test 4 - Precision2 check: ❌ FAILED
- Test 5 - T-stat check: NA

**Observations**:
- Stata:  1,027,449
- Python: 1,300,410
- Common: 1,027,449

**Precision1**: 1.714% obs with std_diff >= 1.00e-02 (tolerance: < 1%)

**Precision2**: 100th percentile diff = 1.18e+00 (tolerance: < 1.00e-01)

**Summary Statistics** (Common Observations):

| Statistic  |          Stata |         Python |     Difference | Std Difference |
|------------|----------------|----------------|----------------|----------------|
| count      |       1.03e+06 |       1.03e+06 |       1.03e+06 |       1.03e+06 |
| mean       |         0.0150 |         0.0149 |      -8.83e-06 |      -5.04e-04 |
| std        |         0.0175 |         0.0174 |         0.0015 |         0.0848 |
| min        |        -0.1110 |        -0.1110 |        -0.0954 |        -5.4417 |
| 25%        |         0.0053 |         0.0053 |      -4.45e-10 |      -2.54e-08 |
| 50%        |         0.0134 |         0.0134 |         0.0000 |         0.0000 |
| 75%        |         0.0230 |         0.0230 |       4.45e-10 |       2.54e-08 |
| max        |         0.3670 |         0.3670 |         0.1226 |         6.9931 |

**Regression Analysis** (Python ~ Stata):

- **Model**: python = 0.0002 + 0.9886 * stata
- **R-squared**: 0.9928
- **N observations**: 1,027,449

| Coefficient |     Estimate |    Std Error | t-statistic |   p-value |
|-------------|--------------|--------------|-------------|----------|
| Intercept   |     1.62e-04 |     1.91e-06 |     84.9566 |     0.000 |
| Slope       |       0.9886 |     8.29e-05 |  11927.8028 |     0.000 |

**Feedback**:
- Num observations with std_diff >= TOL_DIFF_1: 17614/1027449 (1.714%)
- Stata standard deviation: 1.75e-02

**Most Recent Bad Observations**:
```
   permno  yyyymm    python     stata      diff
0   10693  202412  0.005561  0.008496 -0.002935
1   10779  202412  0.011335  0.013265 -0.001929
2   11379  202412  0.023706  0.014200  0.009506
3   32791  202412  0.012446 -0.002500  0.014946
4   52231  202412 -0.033569 -0.045180  0.011611
5   68145  202412 -0.073434 -0.091793  0.018359
6   70704  202412 -0.019085 -0.030873  0.011788
7   77202  202412  0.024185  0.030232 -0.006046
8   77569  202412 -0.023574 -0.031623  0.008050
9   77660  202412  0.008532  0.009985 -0.001452
```

**Largest Differences**:
```
   permno  yyyymm    python     stata      diff
0   82848  201810  0.037143 -0.085432  0.122575
1   82848  201809  0.050950 -0.060400  0.111350
2   82848  201901  0.033924 -0.073479  0.107403
3   82848  201811  0.052141 -0.051648  0.103789
4   82848  201905  0.037850 -0.065358  0.103208
5   80577  201812  0.066467 -0.035637  0.102103
6   80577  201810  0.081964 -0.019242  0.101206
7   82848  201812  0.052138 -0.045694  0.097832
8   80577  201809  0.086215 -0.011225  0.097440
9   78066  201412 -0.011500 -0.107429  0.095929
```

**Largest Differences Before 1950**:
```
No data before 1950
```

---

