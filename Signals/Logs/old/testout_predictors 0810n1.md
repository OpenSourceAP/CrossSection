# Predictor Validation Results

**Generated**: 2025-08-10 20:17:33

**Configuration**:
- PTH_PERCENTILE: 1.0
- TOL_DIFF_1: 0.01
- TOL_OBS_1: 0.1%
- TOL_DIFF_2: 1e-06
- INDEX_COLS: ['permno', 'yyyymm']

## Summary

| Predictor                 | Python CSV | Columns  | Superset  | Precision1   | Precision2              |
|---------------------------|------------|----------|-----------|--------------|-------------------------|
| Coskewness                | ✅         | ✅       | ❌ (8.84%)   | ❌ (99.36%)   | ❌ (100th diff 4.5E+00)  |
| RDAbility                 | ✅         | ✅       | ❌ (4.89%)   | ❌ (95.73%)   | ❌ (100th diff INF)      |
| ResidualMomentum          | ✅         | ✅       | ❌ (2.40%)   | ❌ (0.71%)    | ❌ (100th diff 4.4E-02)  |
| AbnormalAccruals          | ✅         | ✅       | ❌ (0.65%)   | ❌ (49.01%)   | ❌ (100th diff 3.7E+00)  |
| BetaFP                    | ✅         | ✅       | ❌ (0.54%)   | ❌ (5.98%)    | ❌ (100th diff NAN)      |
| PredictedFE               | ✅         | ✅       | ❌ (0.27%)   | ❌ (95.81%)   | ❌ (100th diff 5.1E-02)  |
| AnalystValue              | ✅         | ✅       | ❌ (0.22%)   | ❌ (0.26%)    | ❌ (100th diff 1.2E+01)  |
| AOP                       | ✅         | ✅       | ❌ (0.22%)   | ✅ (0.00%)    | ❌ (100th diff 2.4E+03)  |
| TrendFactor               | ✅         | ✅       | ❌ (0.07%)   | ❌ (98.42%)   | ❌ (100th diff 5.4E+00)  |
| ReturnSkew3F              | ✅         | ✅       | ❌ (0.00%)   | ❌ (2.57%)    | ❌ (100th diff 8.7E+00)  |
| betaVIX                   | ✅         | ✅       | ✅           | ❌ (69.59%)   | ❌ (100th diff 5.7E-01)  |
| PriceDelayTstat           | ✅         | ✅       | ✅           | ❌ (19.38%)   | ❌ (100th diff 1.1E+01)  |
| IdioVolAHT                | ✅         | ✅       | ✅           | ❌ (8.54%)    | ❌ (100th diff NAN)      |
| BetaTailRisk              | ✅         | ✅       | ✅           | ❌ (4.15%)    | ❌ (100th diff 2.0E-01)  |
| PriceDelayRsq             | ✅         | ✅       | ✅           | ❌ (1.21%)    | ❌ (100th diff 9.6E-01)  |
| VolumeTrend               | ✅         | ✅       | ✅           | ❌ (1.00%)    | ❌ (100th diff 1.2E-01)  |
| PriceDelaySlope           | ✅         | ✅       | ✅           | ❌ (0.58%)    | ❌ (100th diff 1.6E+04)  |
| BetaLiquidityPS           | ✅         | ✅       | ✅           | ❌ (0.31%)    | ❌ (100th diff 4.7E-02)  |
| IdioVol3F                 | ✅         | ✅       | ✅           | ✅ (0.02%)    | ❌ (100th diff 1.8E-02)  |
| Beta                      | ✅         | ✅       | ✅           | ✅ (0.00%)    | ❌ (100th diff 2.2E-06)  |
| RealizedVol               | ✅         | ✅       | ✅           | ✅ (0.00%)    | ✅ (100th diff 3.6E-15)  |

**Overall**: 1/21 available predictors passed validation
**Python CSVs**: 21/21 predictors have Python implementation

## Detailed Results

### AOP

**Status**: ❌ FAILED

**Test Results**:
- Test 1 - Column names: ✅ PASSED
- Test 2 - Superset check: ❌ FAILED (Python missing 2784 Stata observations)
- Test 3 - Precision1 check: ✅ PASSED
- Test 4 - Precision2 check: ❌ FAILED

**Columns**: ['AOP']

**Observations**:
- Stata:  1,244,664
- Python: 1,299,504
- Common: 1,241,880

**Precision1**: 0.002% obs with std_diff >= 1.00e-02 (tolerance: < 0.1%)

**Precision2**: 100th percentile diff = 2.40e+03 (tolerance: < 1.00e-06)

**Missing Observations Sample**:
```
 index  permno  yyyymm       AOP
     0   10411  199606 33.973907
     1   10411  199607 33.973907
     2   10411  199608 33.973907
     3   10411  199609 33.973907
     4   10411  199610 33.973907
     5   10411  199611 33.973907
     6   10411  199612 33.973907
     7   10411  199701 33.973907
     8   10411  199702 33.973907
     9   10411  199703 33.973907
```

**Feedback**:
- Num observations with std_diff >= TOL_DIFF_1: 24/1241880 (0.002%)
- Stata standard deviation: 4.75e+04

**Most Recent Bad Observations**:
```
   permno  yyyymm       python      stata         diff
0   77851  199605  2422.684918  22.909092  2399.775826
1   77851  199604  2422.684918  22.909092  2399.775826
2   77851  199603  2422.684918  22.909092  2399.775826
3   77851  199602  2422.684918  22.909092  2399.775826
4   77851  199601  2422.684918  22.909092  2399.775826
5   77851  199512  2422.684918  22.909092  2399.775826
6   77851  199511  2422.684918  22.909092  2399.775826
7   77851  199510  2422.684918  22.909092  2399.775826
8   77851  199509  2422.684918  22.909092  2399.775826
9   77851  199508  2422.684918  22.909092  2399.775826
```

**Largest Differences**:
```
   permno  yyyymm       python      stata         diff
0   77851  199506  2422.684918  22.909092  2399.775826
1   77851  199507  2422.684918  22.909092  2399.775826
2   77851  199508  2422.684918  22.909092  2399.775826
3   77851  199509  2422.684918  22.909092  2399.775826
4   77851  199510  2422.684918  22.909092  2399.775826
5   77851  199511  2422.684918  22.909092  2399.775826
6   77851  199512  2422.684918  22.909092  2399.775826
7   77851  199601  2422.684918  22.909092  2399.775826
8   77851  199602  2422.684918  22.909092  2399.775826
9   77851  199603  2422.684918  22.909092  2399.775826
```

---

### AbnormalAccruals

**Status**: ❌ FAILED

**Test Results**:
- Test 1 - Column names: ✅ PASSED
- Test 2 - Superset check: ❌ FAILED (Python missing 16645 Stata observations)
- Test 3 - Precision1 check: ❌ FAILED
- Test 4 - Precision2 check: ❌ FAILED

**Columns**: ['AbnormalAccruals']

**Observations**:
- Stata:  2,570,664
- Python: 2,581,079
- Common: 2,554,019

**Precision1**: 49.009% obs with std_diff >= 1.00e-02 (tolerance: < 0.1%)

**Precision2**: 100th percentile diff = 3.72e+00 (tolerance: < 1.00e-06)

**Missing Observations Sample**:
```
 index  permno  yyyymm  AbnormalAccruals
     0   10102  197806          0.039469
     1   10102  197807          0.039469
     2   10102  197808          0.039469
     3   10102  197809          0.039469
     4   10102  197810          0.039469
     5   10102  197811          0.039469
     6   10102  197812          0.039469
     7   10102  197901          0.039469
     8   10102  197902          0.039469
     9   10102  197903          0.039469
```

**Feedback**:
- Num observations with std_diff >= TOL_DIFF_1: 1251699/2554019 (49.009%)
- Stata standard deviation: 1.61e-01

**Most Recent Bad Observations**:
```
   permno  yyyymm    python     stata      diff
0   18136  202609 -0.044470 -0.028342 -0.016129
1   29946  202609  0.108293  0.092957  0.015336
2   12366  202608  0.186167  0.146414  0.039753
3   12783  202608  0.034595  0.028171  0.006424
4   13142  202608 -0.125493 -0.145704  0.020211
5   14033  202608  1.354882  1.391868 -0.036986
6   15623  202608 -0.091212 -0.093782  0.002570
7   16318  202608  0.053173  0.051154  0.002019
8   16632  202608 -0.026517 -0.029087  0.002570
9   17920  202608  0.052339  0.064850 -0.012511
```

**Largest Differences**:
```
   permno  yyyymm    python    stata      diff
0   77200  200106 -3.701572  0.01571 -3.717283
1   77200  200107 -3.701572  0.01571 -3.717283
2   77200  200108 -3.701572  0.01571 -3.717283
3   77200  200109 -3.701572  0.01571 -3.717283
4   77200  200110 -3.701572  0.01571 -3.717283
5   77200  200111 -3.701572  0.01571 -3.717283
6   77200  200112 -3.701572  0.01571 -3.717283
7   77200  200201 -3.701572  0.01571 -3.717283
8   77200  200202 -3.701572  0.01571 -3.717283
9   77200  200203 -3.701572  0.01571 -3.717283
```

---

### AnalystValue

**Status**: ❌ FAILED

**Test Results**:
- Test 1 - Column names: ✅ PASSED
- Test 2 - Superset check: ❌ FAILED (Python missing 2784 Stata observations)
- Test 3 - Precision1 check: ❌ FAILED
- Test 4 - Precision2 check: ❌ FAILED

**Columns**: ['AnalystValue']

**Observations**:
- Stata:  1,244,664
- Python: 1,299,504
- Common: 1,241,880

**Precision1**: 0.263% obs with std_diff >= 1.00e-02 (tolerance: < 0.1%)

**Precision2**: 100th percentile diff = 1.17e+01 (tolerance: < 1.00e-06)

**Missing Observations Sample**:
```
 index  permno  yyyymm  AnalystValue
     0   10411  199606      4.547985
     1   10411  199607      4.547985
     2   10411  199608      4.547985
     3   10411  199609      4.547985
     4   10411  199610      4.547985
     5   10411  199611      4.547985
     6   10411  199612      4.547985
     7   10411  199701      4.547985
     8   10411  199702      4.547985
     9   10411  199703      4.547985
```

**Feedback**:
- Num observations with std_diff >= TOL_DIFF_1: 3264/1241880 (0.263%)
- Stata standard deviation: 1.05e+01

**Most Recent Bad Observations**:
```
   permno  yyyymm       python        stata       diff
0   21783  202505     1.230213     1.028611   0.201602
1   22793  202505  3326.578149  3338.297600 -11.719451
2   23033  202505    11.374458     9.866216   1.508243
3   23316  202505     1.854150     1.746798   0.107352
4   23426  202505    -1.539445    -1.210400  -0.329045
5   91575  202505     0.009558     1.261121  -1.251564
6   21783  202504     1.230213     1.028611   0.201602
7   22793  202504  3326.578149  3338.297600 -11.719451
8   23033  202504    11.374458     9.866216   1.508243
9   23316  202504     1.854150     1.746798   0.107352
```

**Largest Differences**:
```
   permno  yyyymm       python      stata       diff
0   22793  202406  3326.578149  3338.2976 -11.719451
1   22793  202407  3326.578149  3338.2976 -11.719451
2   22793  202408  3326.578149  3338.2976 -11.719451
3   22793  202409  3326.578149  3338.2976 -11.719451
4   22793  202410  3326.578149  3338.2976 -11.719451
5   22793  202411  3326.578149  3338.2976 -11.719451
6   22793  202412  3326.578149  3338.2976 -11.719451
7   22793  202501  3326.578149  3338.2976 -11.719451
8   22793  202502  3326.578149  3338.2976 -11.719451
9   22793  202503  3326.578149  3338.2976 -11.719451
```

---

### Beta

**Status**: ❌ FAILED

**Test Results**:
- Test 1 - Column names: ✅ PASSED
- Test 2 - Superset check: ✅ PASSED
- Test 3 - Precision1 check: ✅ PASSED
- Test 4 - Precision2 check: ❌ FAILED

**Columns**: ['Beta']

**Observations**:
- Stata:  4,285,574
- Python: 4,353,773
- Common: 4,285,574

**Precision1**: 0.000% obs with std_diff >= 1.00e-02 (tolerance: < 0.1%)

**Precision2**: 100th percentile diff = 2.25e-06 (tolerance: < 1.00e-06)

**Feedback**:
- Num observations with std_diff >= TOL_DIFF_1: 0/4285574 (0.000%)
- Stata standard deviation: 7.46e-01

---

### BetaFP

**Status**: ❌ FAILED

**Test Results**:
- Test 1 - Column names: ✅ PASSED
- Test 2 - Superset check: ❌ FAILED (Python missing 20488 Stata observations)
- Test 3 - Precision1 check: ❌ FAILED
- Test 4 - Precision2 check: ❌ FAILED

**Columns**: ['BetaFP']

**Observations**:
- Stata:  3,794,018
- Python: 3,779,957
- Common: 3,773,530

**Precision1**: 5.980% obs with std_diff >= 1.00e-02 (tolerance: < 0.1%)

**Precision2**: 100th percentile diff = nan (tolerance: < 1.00e-06)

**Missing Observations Sample**:
```
 index  permno  yyyymm   BetaFP
     0   10051  201903 0.810570
     1   10051  201904 0.802326
     2   10051  201905 0.838970
     3   10051  201906 0.780897
     4   10051  201907 0.803848
     5   10051  201908 0.844066
     6   10051  201909 0.844055
     7   10051  201910 0.906686
     8   10051  201911 0.934303
     9   10051  201912 1.063378
```

**Feedback**:
- Num observations with std_diff >= TOL_DIFF_1: 225656/3773530 (5.980%)
- Stata standard deviation: 6.41e-01

**Most Recent Bad Observations**:
```
   permno  yyyymm    python     stata      diff
0   10066  202412  0.366776  0.247929  0.118848
1   11153  202412  0.194148  0.253281 -0.059133
2   11379  202412  1.593719  1.445916  0.147803
3   13563  202412  0.903798  0.608259  0.295539
4   13828  202412  0.846968  0.970209 -0.123241
5   13878  202412  0.978277  0.966509  0.011768
6   13947  202412  2.605158  2.657374 -0.052215
7   14051  202412  3.479917  3.465529  0.014388
8   14469  202412  2.212209  1.759658  0.452551
9   14720  202412  4.574750  4.556220  0.018530
```

**Largest Differences**:
```
   permno  yyyymm    python     stata      diff
0   78301  198510       NaN  0.000378       NaN
1   78301  198511       NaN  0.000365       NaN
2   78301  198512       NaN  0.000359       NaN
3   78301  198601       NaN  0.000377       NaN
4   78301  198602       NaN  0.000447       NaN
5   78301  198603       NaN  0.000468       NaN
6   11453  199312  7.664115  2.870236  4.793879
7   65622  199401  0.593349  4.575622 -3.982273
8   65622  199402  0.930784  4.732967 -3.802183
9   65622  199312  0.867006  4.276299 -3.409292
```

---

### BetaLiquidityPS

**Status**: ❌ FAILED

**Test Results**:
- Test 1 - Column names: ✅ PASSED
- Test 2 - Superset check: ✅ PASSED
- Test 3 - Precision1 check: ❌ FAILED
- Test 4 - Precision2 check: ❌ FAILED

**Columns**: ['BetaLiquidityPS']

**Observations**:
- Stata:  3,423,856
- Python: 3,479,410
- Common: 3,423,856

**Precision1**: 0.309% obs with std_diff >= 1.00e-02 (tolerance: < 0.1%)

**Precision2**: 100th percentile diff = 4.66e-02 (tolerance: < 1.00e-06)

**Feedback**:
- Num observations with std_diff >= TOL_DIFF_1: 10596/3423856 (0.309%)
- Stata standard deviation: 4.52e-01

**Most Recent Bad Observations**:
```
   permno  yyyymm    python     stata      diff
0   12527  202412  3.114748  3.110062  0.004685
1   13812  202412 -0.279861 -0.285009  0.005148
2   14280  202412 -0.195891 -0.200836  0.004945
3   14328  202412  2.075094  2.067611  0.007482
4   14720  202412 -0.783082 -0.788315  0.005233
5   14791  202412 -2.796831 -2.804661  0.007830
6   14813  202412  0.574480  0.568289  0.006190
7   15172  202412  0.858918  0.854361  0.004557
8   15489  202412  0.114074  0.101456  0.012619
9   15775  202412  0.905586  0.899805  0.005782
```

**Largest Differences**:
```
   permno  yyyymm    python     stata      diff
0   48072  202311  2.920068  2.873500  0.046568
1   89301  202311  1.966508  1.923020  0.043488
2   48072  202310  3.102564  3.060607  0.041957
3   48072  202403  4.981330  4.941999  0.039331
4   48072  202402  4.975391  4.936378  0.039014
5   89301  202310  2.094525  2.055533  0.038992
6   48072  202401  4.069945  4.032388  0.037557
7   89301  202403  3.828060  3.791143  0.036917
8   48072  202312  4.056726  4.019963  0.036763
9   89301  202402  3.823554  3.786863  0.036692
```

---

### BetaTailRisk

**Status**: ❌ FAILED

**Test Results**:
- Test 1 - Column names: ✅ PASSED
- Test 2 - Superset check: ✅ PASSED
- Test 3 - Precision1 check: ❌ FAILED
- Test 4 - Precision2 check: ❌ FAILED

**Columns**: ['BetaTailRisk']

**Observations**:
- Stata:  2,292,350
- Python: 2,332,084
- Common: 2,292,350

**Precision1**: 4.149% obs with std_diff >= 1.00e-02 (tolerance: < 0.1%)

**Precision2**: 100th percentile diff = 1.98e-01 (tolerance: < 1.00e-06)

**Feedback**:
- Num observations with std_diff >= TOL_DIFF_1: 95107/2292350 (4.149%)
- Stata standard deviation: 5.11e-01

**Most Recent Bad Observations**:
```
   permno  yyyymm    python     stata      diff
0   16099  202412  0.288367  0.293937 -0.005571
1   16400  202412  1.372777  1.339924  0.032854
2   18148  202412  0.111011  0.116482 -0.005471
3   77437  202412  1.854679  1.846069  0.008610
4   84411  202412  0.911352  0.901888  0.009464
5   89029  202412  0.608437  0.614334 -0.005897
6   89169  202412  1.567852  1.606029 -0.038177
7   16099  202411  0.323722  0.329289 -0.005567
8   16400  202411  1.385534  1.352590  0.032944
9   18148  202411  0.147289  0.152762 -0.005473
```

**Largest Differences**:
```
   permno  yyyymm    python     stata      diff
0   78050  199811 -0.557545 -0.755131  0.197586
1   78050  199812 -0.396312 -0.593467  0.197155
2   78050  199901 -0.158898 -0.349701  0.190803
3   78050  199902 -0.069994 -0.254714  0.184720
4   78050  199903  0.069028 -0.111589  0.180616
5   78050  199904  0.224322  0.047509  0.176813
6   78050  199905  0.378144  0.209011  0.169132
7   78050  199906  0.461683  0.294377  0.167306
8   78050  199907  0.347299  0.188068  0.159231
9   78050  199908  0.386259  0.234870  0.151388
```

---

### Coskewness

**Status**: ❌ FAILED

**Test Results**:
- Test 1 - Column names: ✅ PASSED
- Test 2 - Superset check: ❌ FAILED (Python missing 407320 Stata observations)
- Test 3 - Precision1 check: ❌ FAILED
- Test 4 - Precision2 check: ❌ FAILED

**Columns**: ['Coskewness']

**Observations**:
- Stata:  4,609,158
- Python: 4,684,891
- Common: 4,201,838

**Precision1**: 99.358% obs with std_diff >= 1.00e-02 (tolerance: < 0.1%)

**Precision2**: 100th percentile diff = 4.53e+00 (tolerance: < 1.00e-06)

**Missing Observations Sample**:
```
 index  permno  yyyymm  Coskewness
     0   10000  198701   -0.080541
     1   10000  198702   -0.115902
     2   10000  198703   -0.027634
     3   10000  198704   -0.055297
     4   10000  198705   -0.086010
     5   10000  198706   -0.081288
     6   10001  201610   -0.023566
     7   10001  201611   -0.018342
     8   10001  201612   -0.010124
     9   10001  201701   -0.011009
```

**Feedback**:
- Num observations with std_diff >= TOL_DIFF_1: 4174867/4201838 (99.358%)
- Stata standard deviation: 3.87e-01

**Most Recent Bad Observations**:
```
   permno  yyyymm    python     stata      diff
0   10026  202401 -0.281231 -0.352961  0.071730
1   10028  202401  0.150770  0.192499 -0.041729
2   10032  202401  0.157133 -0.264077  0.421210
3   10044  202401  0.166441 -0.194824  0.361266
4   10065  202401 -0.428818 -0.293021 -0.135798
5   10066  202401 -0.008205  0.162496 -0.170701
6   10104  202401 -0.668330 -0.175856 -0.492473
7   10107  202401 -0.381137 -0.297508 -0.083628
8   10113  202401  0.011056 -0.360982  0.372038
9   10138  202401 -0.271320 -0.362331  0.091011
```

**Largest Differences**:
```
   permno  yyyymm    python     stata      diff
0   84521  200810  0.041675 -4.491474  4.533149
1   84521  200811  0.379757 -3.951515  4.331272
2   84521  200812  0.404184 -3.922149  4.326333
3   68320  200810 -0.521594 -4.472239  3.950645
4   38790  200810 -0.284738 -4.137259  3.852521
5   38520  199110  0.151898 -3.587333  3.739231
6   38520  199109  0.164027 -3.555150  3.719177
7   68320  200811 -0.144712 -3.845352  3.700640
8   38520  199111  0.160851 -3.481031  3.641881
9   68320  200812 -0.146651 -3.748868  3.602217
```

---

### IdioVol3F

**Status**: ❌ FAILED

**Test Results**:
- Test 1 - Column names: ✅ PASSED
- Test 2 - Superset check: ✅ PASSED
- Test 3 - Precision1 check: ✅ PASSED
- Test 4 - Precision2 check: ❌ FAILED

**Columns**: ['IdioVol3F']

**Observations**:
- Stata:  4,980,936
- Python: 5,026,821
- Common: 4,980,936

**Precision1**: 0.021% obs with std_diff >= 1.00e-02 (tolerance: < 0.1%)

**Precision2**: 100th percentile diff = 1.76e-02 (tolerance: < 1.00e-06)

**Feedback**:
- Num observations with std_diff >= TOL_DIFF_1: 1055/4980936 (0.021%)
- Stata standard deviation: 2.85e-02

**Most Recent Bad Observations**:
```
   permno  yyyymm    python     stata      diff
0   15846  202412  0.331909  0.332326 -0.000417
1   20882  202412  0.477703  0.476938  0.000765
2   21286  202412  0.780673  0.781551 -0.000878
3   23513  202412  0.159032  0.159369 -0.000336
4   25724  202412  0.259004  0.259346 -0.000343
5   25741  202412  1.170279  1.169952  0.000327
6   84819  202412  0.169069  0.168768  0.000302
7   14551  202411  0.142603  0.142889 -0.000286
8   16111  202411  0.190392  0.190785 -0.000393
9   18457  202411  0.724134  0.724934 -0.000800
```

**Largest Differences**:
```
   permno  yyyymm    python     stata      diff
0   13883  202310  7.799678  7.817299 -0.017621
1   16400  202401  0.982255  0.986626 -0.004372
2   17105  201811  0.520284  0.516678  0.003606
3   20439  202301  1.389258  1.386151  0.003107
4   18363  201901  1.182937  1.179979  0.002958
5   90926  201809  0.474128  0.471342  0.002786
6   22793  202204  0.346254  0.343756  0.002499
7   16070  202308  1.042644  1.045074 -0.002429
8   16903  202406  0.874303  0.876677 -0.002375
9   16568  201903  0.875490  0.873197  0.002293
```

---

### IdioVolAHT

**Status**: ❌ FAILED

**Test Results**:
- Test 1 - Column names: ✅ PASSED
- Test 2 - Superset check: ✅ PASSED
- Test 3 - Precision1 check: ❌ FAILED
- Test 4 - Precision2 check: ❌ FAILED

**Columns**: ['IdioVolAHT']

**Observations**:
- Stata:  4,849,170
- Python: 5,113,369
- Common: 4,849,170

**Precision1**: 8.536% obs with std_diff >= 1.00e-02 (tolerance: < 0.1%)

**Precision2**: 100th percentile diff = nan (tolerance: < 1.00e-06)

**Feedback**:
- Num observations with std_diff >= TOL_DIFF_1: 413907/4849170 (8.536%)
- Stata standard deviation: 2.64e-02

**Most Recent Bad Observations**:
```
   permno  yyyymm    python     stata      diff
0   12049  202412  0.074624  0.074922 -0.000298
1   12350  202412  0.118474  0.118947 -0.000473
2   12360  202412  0.069522  0.069799 -0.000278
3   12495  202412  0.071052  0.071336 -0.000284
4   12527  202412  0.130749  0.131271 -0.000522
5   12579  202412  0.068835  0.069110 -0.000275
6   12680  202412  0.100397  0.100798 -0.000401
7   12751  202412  0.069704  0.069982 -0.000278
8   12799  202412       NaN  0.048552       NaN
9   12840  202412  0.071510  0.071796 -0.000285
```

**Largest Differences**:
```
   permno  yyyymm  python     stata  diff
0   10007  198902     NaN  0.054694   NaN
1   10007  198903     NaN  0.055225   NaN
2   10007  198904     NaN  0.054111   NaN
3   10007  198905     NaN  0.054717   NaN
4   10007  198906     NaN  0.054713   NaN
5   10051  201809     NaN  0.018538   NaN
6   10051  201810     NaN  0.018122   NaN
7   10051  201811     NaN  0.019433   NaN
8   10051  201812     NaN  0.019570   NaN
9   10051  201901     NaN  0.019574   NaN
```

---

### PredictedFE

**Status**: ❌ FAILED

**Test Results**:
- Test 1 - Column names: ✅ PASSED
- Test 2 - Superset check: ❌ FAILED (Python missing 1320 Stata observations)
- Test 3 - Precision1 check: ❌ FAILED
- Test 4 - Precision2 check: ❌ FAILED

**Columns**: ['PredictedFE']

**Observations**:
- Stata:  491,508
- Python: 635,292
- Common: 490,188

**Precision1**: 95.807% obs with std_diff >= 1.00e-02 (tolerance: < 0.1%)

**Precision2**: 100th percentile diff = 5.08e-02 (tolerance: < 1.00e-06)

**Missing Observations Sample**:
```
 index  permno  yyyymm  PredictedFE
     0   12473  201806    -0.041659
     1   12473  201807    -0.041659
     2   12473  201808    -0.041659
     3   12473  201809    -0.041659
     4   12473  201810    -0.041659
     5   12473  201811    -0.041659
     6   12473  201812    -0.041659
     7   12473  201901    -0.041659
     8   12473  201902    -0.041659
     9   12473  201903    -0.041659
```

**Feedback**:
- Num observations with std_diff >= TOL_DIFF_1: 469632/490188 (95.807%)
- Stata standard deviation: 3.16e-02

**Most Recent Bad Observations**:
```
   permno  yyyymm    python     stata      diff
0   10107  202505  0.074906  0.078498 -0.003592
1   10145  202505  0.028429  0.040432 -0.012003
2   10200  202505  0.121830  0.113642  0.008188
3   10397  202505  0.063543  0.049793  0.013750
4   10606  202505  0.042676  0.044046 -0.001370
5   10693  202505  0.034107  0.036774 -0.002667
6   10696  202505  0.116063  0.105464  0.010598
7   11308  202505  0.059996  0.072780 -0.012784
8   11403  202505  0.086531  0.090274 -0.003744
9   11547  202505  0.088011  0.076702  0.011310
```

**Largest Differences**:
```
   permno  yyyymm    python     stata      diff
0   77496  202306  0.035265  0.086091 -0.050826
1   77496  202307  0.035265  0.086091 -0.050826
2   77496  202308  0.035265  0.086091 -0.050826
3   77496  202309  0.035265  0.086091 -0.050826
4   77496  202310  0.035265  0.086091 -0.050826
5   77496  202311  0.035265  0.086091 -0.050826
6   77496  202312  0.035265  0.086091 -0.050826
7   77496  202401  0.035265  0.086091 -0.050826
8   77496  202402  0.035265  0.086091 -0.050826
9   77496  202403  0.035265  0.086091 -0.050826
```

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

**Precision1**: 1.210% obs with std_diff >= 1.00e-02 (tolerance: < 0.1%)

**Precision2**: 100th percentile diff = 9.57e-01 (tolerance: < 1.00e-06)

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

---

### PriceDelaySlope

**Status**: ❌ FAILED

**Test Results**:
- Test 1 - Column names: ✅ PASSED
- Test 2 - Superset check: ✅ PASSED
- Test 3 - Precision1 check: ❌ FAILED
- Test 4 - Precision2 check: ❌ FAILED

**Columns**: ['PriceDelaySlope']

**Observations**:
- Stata:  4,630,424
- Python: 4,636,840
- Common: 4,630,424

**Precision1**: 0.582% obs with std_diff >= 1.00e-02 (tolerance: < 0.1%)

**Precision2**: 100th percentile diff = 1.59e+04 (tolerance: < 1.00e-06)

**Feedback**:
- Num observations with std_diff >= TOL_DIFF_1: 26952/4630424 (0.582%)
- Stata standard deviation: 2.52e+02

**Most Recent Bad Observations**:
```
   permno  yyyymm       python       stata        diff
0   12339  202406  1048.987343  1173.92500 -124.937657
1   12920  202406   138.447590   141.02330   -2.575710
2   14296  202406 -1739.165320 -1360.86080 -378.304520
3   16765  202406  -285.457178  -312.93927   27.482092
4   21288  202406   195.744273   189.23006    6.514213
5   22758  202406   277.802905   283.31763   -5.514725
6   24441  202406   396.015800   381.69559   14.320210
7   82171  202406  -115.272269  -123.27301    8.000741
8   90562  202406  -368.401832  -371.83365    3.431818
9   12339  202405  1048.987343  1173.92500 -124.937657
```

**Largest Differences**:
```
   permno  yyyymm       python     stata          diff
0   22356  202207  1525.894901  17467.24 -15941.345099
1   22356  202208  1525.894901  17467.24 -15941.345099
2   22356  202209  1525.894901  17467.24 -15941.345099
3   22356  202210  1525.894901  17467.24 -15941.345099
4   22356  202211  1525.894901  17467.24 -15941.345099
5   22356  202212  1525.894901  17467.24 -15941.345099
6   22356  202301  1525.894901  17467.24 -15941.345099
7   22356  202302  1525.894901  17467.24 -15941.345099
8   22356  202303  1525.894901  17467.24 -15941.345099
9   22356  202304  1525.894901  17467.24 -15941.345099
```

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

**Precision1**: 19.380% obs with std_diff >= 1.00e-02 (tolerance: < 0.1%)

**Precision2**: 100th percentile diff = 1.08e+01 (tolerance: < 1.00e-06)

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
- Test 2 - Superset check: ❌ FAILED (Python missing 8479 Stata observations)
- Test 3 - Precision1 check: ❌ FAILED
- Test 4 - Precision2 check: ❌ FAILED

**Columns**: ['RDAbility']

**Observations**:
- Stata:  173,266
- Python: 232,981
- Common: 164,787

**Precision1**: 95.728% obs with std_diff >= 1.00e-02 (tolerance: < 0.1%)

**Precision2**: 100th percentile diff = inf (tolerance: < 1.00e-06)

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
- Num observations with std_diff >= TOL_DIFF_1: 157748/164787 (95.728%)
- Stata standard deviation: 5.48e+00

**Most Recent Bad Observations**:
```
   permno  yyyymm    python     stata      diff
0   20117  202608  0.384144  2.244096 -1.859952
1   63125  202608  0.439429  1.052814 -0.613385
2   75603  202608  0.145414  1.657931 -1.512517
3   75828  202608  0.213916 -0.489681  0.703597
4   78987  202608  0.245592  3.648803 -3.403211
5   84761  202608  1.457716 -1.036981  2.494696
6   85035  202608  0.184039  1.323436 -1.139397
7   85177  202608  0.840426 -1.963602  2.804028
8   87179  202608 -0.219607  1.526995 -1.746602
9   20117  202607  0.384144  2.244096 -1.859952
```

**Largest Differences**:
```
   permno  yyyymm  python     stata  diff
0   75853  200106    -inf -0.107289  -inf
1   75853  200107    -inf -0.107289  -inf
2   75853  200108    -inf -0.107289  -inf
3   75853  200109    -inf -0.107289  -inf
4   75853  200110    -inf -0.107289  -inf
5   75853  200111    -inf -0.107289  -inf
6   75853  200112    -inf -0.107289  -inf
7   75853  200201    -inf -0.107289  -inf
8   75853  200202    -inf -0.107289  -inf
9   75853  200203    -inf -0.107289  -inf
```

---

### RealizedVol

**Status**: ✅ PASSED

**Test Results**:
- Test 1 - Column names: ✅ PASSED
- Test 2 - Superset check: ✅ PASSED
- Test 3 - Precision1 check: ✅ PASSED
- Test 4 - Precision2 check: ✅ PASSED

**Columns**: ['RealizedVol']

**Observations**:
- Stata:  4,987,397
- Python: 5,026,821
- Common: 4,987,397

**Precision1**: 0.000% obs with std_diff >= 1.00e-02 (tolerance: < 0.1%)

**Precision2**: 100th percentile diff = 3.55e-15 (tolerance: < 1.00e-06)

**Feedback**:
- Num observations with std_diff >= TOL_DIFF_1: 0/4987397 (0.000%)
- Stata standard deviation: 3.13e-02

---

### ResidualMomentum

**Status**: ❌ FAILED

**Test Results**:
- Test 1 - Column names: ✅ PASSED
- Test 2 - Superset check: ❌ FAILED (Python missing 83157 Stata observations)
- Test 3 - Precision1 check: ❌ FAILED
- Test 4 - Precision2 check: ❌ FAILED

**Columns**: ['ResidualMomentum']

**Observations**:
- Stata:  3,458,422
- Python: 3,375,265
- Common: 3,375,265

**Precision1**: 0.712% obs with std_diff >= 1.00e-02 (tolerance: < 0.1%)

**Precision2**: 100th percentile diff = 4.39e-02 (tolerance: < 1.00e-06)

**Missing Observations Sample**:
```
 index  permno  yyyymm  ResidualMomentum
     0   10012  199003          0.206273
     1   10012  199004          0.265448
     2   10012  199005          0.295592
     3   10012  199006          0.366329
     4   10012  199007          0.144718
     5   10012  199008          0.195028
     6   10012  199009          0.289079
     7   10012  199010          0.262496
     8   10012  199011          0.117379
     9   10012  199012          0.134704
```

**Feedback**:
- Num observations with std_diff >= TOL_DIFF_1: 24033/3375265 (0.712%)
- Stata standard deviation: 3.30e-01

**Most Recent Bad Observations**:
```
   permno  yyyymm    python     stata      diff
0   10028  202412  0.289036  0.283338  0.005699
1   10107  202412 -0.795068 -0.786140 -0.008928
2   10252  202412  0.283345  0.277829  0.005516
3   10294  202412 -0.792843 -0.800530  0.007688
4   10308  202412  0.409725  0.405028  0.004697
5   10318  202412 -0.092833 -0.098400  0.005568
6   10397  202412 -0.336479 -0.339856  0.003377
7   10606  202412 -0.643135 -0.647104  0.003969
8   10629  202412  0.348657  0.343000  0.005657
9   10892  202412  0.370519  0.366241  0.004278
```

**Largest Differences**:
```
   permno  yyyymm    python     stata      diff
0   88406  202408 -0.411009 -0.454921  0.043912
1   12975  201911  1.415373  1.371636  0.043736
2   12296  202408 -0.388452 -0.431406  0.042954
3   12975  201912  1.335915  1.294238  0.041677
4   88406  202407 -0.435183 -0.475339  0.040156
5   14081  202409 -0.658667 -0.698220  0.039553
6   88608  202408 -0.349476 -0.387996  0.038521
7   12296  202407 -0.389629 -0.427586  0.037957
8   88608  202407 -0.409801 -0.447592  0.037791
9   92816  202406  1.158787  1.124535  0.034252
```

---

### ReturnSkew3F

**Status**: ❌ FAILED

**Test Results**:
- Test 1 - Column names: ✅ PASSED
- Test 2 - Superset check: ❌ FAILED (Python missing 207 Stata observations)
- Test 3 - Precision1 check: ❌ FAILED
- Test 4 - Precision2 check: ❌ FAILED

**Columns**: ['ReturnSkew3F']

**Observations**:
- Stata:  4,978,948
- Python: 5,026,283
- Common: 4,978,741

**Precision1**: 2.575% obs with std_diff >= 1.00e-02 (tolerance: < 0.1%)

**Precision2**: 100th percentile diff = 8.73e+00 (tolerance: < 1.00e-06)

**Missing Observations Sample**:
```
 index  permno  yyyymm  ReturnSkew3F
     0   10058  198205      0.179042
     1   10074  198205      0.179042
     2   10656  198205      0.179042
     3   10699  198205      0.179042
     4   11236  193003     -0.638568
     5   11683  197301     -0.336802
     6   11712  198205      0.179042
     7   11712  198310     -0.225000
     8   11851  197301     -0.336802
     9   11894  198205      0.179042
```

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

---

### TrendFactor

**Status**: ❌ FAILED

**Test Results**:
- Test 1 - Column names: ✅ PASSED
- Test 2 - Superset check: ❌ FAILED (Python missing 1452 Stata observations)
- Test 3 - Precision1 check: ❌ FAILED
- Test 4 - Precision2 check: ❌ FAILED

**Columns**: ['TrendFactor']

**Observations**:
- Stata:  2,058,231
- Python: 2,057,228
- Common: 2,056,779

**Precision1**: 98.418% obs with std_diff >= 1.00e-02 (tolerance: < 0.1%)

**Precision2**: 100th percentile diff = 5.38e+00 (tolerance: < 1.00e-06)

**Missing Observations Sample**:
```
 index  permno  yyyymm  TrendFactor
     0   10010  199505     0.402793
     1   10025  198905     0.183533
     2   10070  198610     0.164795
     3   10086  199110     0.285178
     4   10087  198610     0.158854
     5   10115  198610     0.162526
     6   10116  199110     0.288732
     7   10122  198812     0.313713
     8   10122  199604     0.156208
     9   10123  198812     0.314046
```

**Feedback**:
- Num observations with std_diff >= TOL_DIFF_1: 2024236/2056779 (98.418%)
- Stata standard deviation: 1.54e-01

**Most Recent Bad Observations**:
```
   permno  yyyymm    python     stata      diff
0   10026  202412 -0.094924  0.032569 -0.127493
1   10032  202412 -0.092298  0.035968 -0.128266
2   10104  202412 -0.093959  0.034036 -0.127994
3   10107  202412 -0.093766  0.038111 -0.131876
4   10138  202412 -0.090847  0.037830 -0.128677
5   10145  202412 -0.094344  0.036421 -0.130765
6   10158  202412 -0.091837  0.032967 -0.124805
7   10200  202412 -0.091831  0.036853 -0.128684
8   10220  202412 -0.095402  0.030636 -0.126038
9   10252  202412 -0.093153  0.033475 -0.126628
```

**Largest Differences**:
```
   permno  yyyymm    python     stata      diff
0   18104  193203 -4.538915  0.837169 -5.376084
1   15536  193207 -3.247791  0.539885 -3.787676
2   13418  193207 -3.202128  0.525939 -3.728067
3   13725  193207 -3.202128  0.502853 -3.704981
4   17873  193207 -3.147391  0.522079 -3.669470
5   15499  193206 -3.204386  0.441662 -3.646048
6   14883  193207 -3.106826  0.520245 -3.627072
7   13725  193206 -3.068029  0.529304 -3.597333
8   10188  193202 -3.070908  0.499869 -3.570777
9   15544  193203 -3.062227  0.497286 -3.559513
```

---

### VolumeTrend

**Status**: ❌ FAILED

**Test Results**:
- Test 1 - Column names: ✅ PASSED
- Test 2 - Superset check: ✅ PASSED
- Test 3 - Precision1 check: ❌ FAILED
- Test 4 - Precision2 check: ❌ FAILED

**Columns**: ['VolumeTrend']

**Observations**:
- Stata:  3,655,889
- Python: 3,752,130
- Common: 3,655,889

**Precision1**: 1.001% obs with std_diff >= 1.00e-02 (tolerance: < 0.1%)

**Precision2**: 100th percentile diff = 1.22e-01 (tolerance: < 1.00e-06)

**Feedback**:
- Num observations with std_diff >= TOL_DIFF_1: 36580/3655889 (1.001%)
- Stata standard deviation: 2.07e-02

**Most Recent Bad Observations**:
```
   permno  yyyymm    python     stata      diff
0   10066  202412 -0.042738 -0.007268 -0.035470
1   11153  202412 -0.056518  0.001885 -0.058404
2   11379  202412 -0.036342 -0.014016 -0.022326
3   12928  202412  0.066959 -0.000076  0.067035
4   13563  202412 -0.019177 -0.051617  0.032440
5   13828  202412 -0.056518 -0.036236 -0.020282
6   13878  202412 -0.002076 -0.044578  0.042502
7   14051  202412 -0.046306 -0.042498 -0.003808
8   14469  202412  0.066959  0.012960  0.054000
9   15294  202412 -0.046056 -0.022408 -0.023648
```

**Largest Differences**:
```
   permno  yyyymm    python     stata      diff
0   76188  199207  0.066959 -0.055106  0.122065
1   81331  199212  0.066959 -0.053937  0.120896
2   83622  201706  0.063452 -0.052244  0.115697
3   83622  201707  0.059125 -0.050653  0.109778
4   11161  200602  0.053628 -0.054415  0.108043
5   27204  201810  0.060988 -0.047022  0.108011
6   27204  201811  0.060954 -0.045956  0.106910
7   76188  199212  0.054548 -0.050417  0.104965
8   83630  201203  0.066959 -0.037886  0.104845
9   27204  201812  0.060880 -0.043556  0.104436
```

---

### betaVIX

**Status**: ❌ FAILED

**Test Results**:
- Test 1 - Column names: ✅ PASSED
- Test 2 - Superset check: ✅ PASSED
- Test 3 - Precision1 check: ❌ FAILED
- Test 4 - Precision2 check: ❌ FAILED

**Columns**: ['betaVIX']

**Observations**:
- Stata:  3,510,758
- Python: 3,553,481
- Common: 3,510,758

**Precision1**: 69.594% obs with std_diff >= 1.00e-02 (tolerance: < 0.1%)

**Precision2**: 100th percentile diff = 5.75e-01 (tolerance: < 1.00e-06)

**Feedback**:
- Num observations with std_diff >= TOL_DIFF_1: 2443284/3510758 (69.594%)
- Stata standard deviation: 1.72e-02

**Most Recent Bad Observations**:
```
   permno  yyyymm    python     stata      diff
0   10026  202412 -0.001024 -0.001558  0.000534
1   10028  202412  0.006798  0.007623 -0.000824
2   10044  202412  0.001192  0.000739  0.000454
3   10066  202412 -0.005787 -0.005536 -0.000251
4   10104  202412  0.000797  0.000471  0.000326
5   10113  202412 -0.001220 -0.001042 -0.000178
6   10138  202412 -0.002827 -0.003156  0.000329
7   10158  202412 -0.000214 -0.000904  0.000690
8   10207  202412 -0.001134 -0.001502  0.000368
9   10220  202412  0.000411 -0.000230  0.000641
```

**Largest Differences**:
```
   permno  yyyymm    python     stata      diff
0   13958  201406  0.855439  0.280629  0.574810
1   19831  202012 -0.039200 -0.555196  0.515996
2   13883  202310 -1.660559 -1.237186 -0.423373
3   87776  199503  0.089535 -0.307695  0.397230
4   22298  202410 -0.360627 -0.747243  0.386616
5   67117  199012  0.028636 -0.351113  0.379749
6   86070  200201  0.126315  0.405910 -0.279595
7   18777  201911  0.215048 -0.054327  0.269375
8   24094  202407 -0.345860 -0.609205  0.263345
9   77733  199707  0.060667 -0.199686  0.260354
```

---

