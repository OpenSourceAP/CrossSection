# Predictor Validation Results

**Generated**: 2025-08-11 18:24:19

**Configuration**:
- PTH_PERCENTILE: 1.0
- TOL_DIFF_1: 0.01
- TOL_OBS_1: 0.1%
- TOL_DIFF_2: 1e-06
- INDEX_COLS: ['permno', 'yyyymm']

## Summary

| Predictor                 | Python CSV | Columns  | Superset  | Precision1   | Precision2              |
|---------------------------|------------|----------|-----------|--------------|-------------------------|
| PredictedFE               | ✅         | ✅       | ❌ (0.27%)   | ❌ (95.81%)   | ❌ (100th diff 5.1E-02)  |
| AnalystValue              | ✅         | ✅       | ❌ (0.22%)   | ❌ (0.26%)    | ❌ (100th diff 1.2E+01)  |
| AOP                       | ✅         | ✅       | ❌ (0.22%)   | ✅ (0.00%)    | ❌ (100th diff 2.4E+03)  |
| RealizedVol               | ✅         | ✅       | ❌ (0.12%)   | ✅ (0.00%)    | ✅ (100th diff 3.6E-15)  |
| BetaTailRisk              | ✅         | ✅       | ✅           | ❌ (4.15%)    | ❌ (100th diff 2.0E-01)  |
| ReturnSkew3F              | ✅         | ✅       | ✅           | ❌ (2.68%)    | ❌ (100th diff 5.9E+00)  |
| VolumeTrend               | ✅         | ✅       | ✅           | ❌ (1.36%)    | ❌ (100th diff 1.6E-01)  |
| ResidualMomentum          | ✅         | ✅       | ✅           | ❌ (0.70%)    | ❌ (100th diff 4.4E-02)  |
| BetaLiquidityPS           | ✅         | ✅       | ✅           | ❌ (0.31%)    | ❌ (100th diff 4.7E-02)  |
| IdioVol3F                 | ✅         | ✅       | ✅           | ✅ (0.02%)    | ❌ (100th diff 1.8E-02)  |

**Overall**: 0/10 available predictors passed validation
**Python CSVs**: 10/10 predictors have Python implementation

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
- Python: 4,987,890
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

### RealizedVol

**Status**: ❌ FAILED

**Test Results**:
- Test 1 - Column names: ✅ PASSED
- Test 2 - Superset check: ❌ FAILED (Python missing 5736 Stata observations)
- Test 3 - Precision1 check: ✅ PASSED
- Test 4 - Precision2 check: ✅ PASSED

**Columns**: ['RealizedVol']

**Observations**:
- Stata:  4,987,397
- Python: 4,987,890
- Common: 4,981,661

**Precision1**: 0.000% obs with std_diff >= 1.00e-02 (tolerance: < 0.1%)

**Precision2**: 100th percentile diff = 3.55e-15 (tolerance: < 1.00e-06)

**Missing Observations Sample**:
```
 index  permno  yyyymm  RealizedVol
     0   10001  201708     0.003861
     1   10004  198601     0.011756
     2   10009  200011     0.001091
     3   10012  200508     0.120162
     4   10016  200105     0.018682
     5   10022  196005     0.000000
     6   10023  197306     0.000000
     7   10024  198601     0.017678
     8   10057  199607     0.000000
     9   10084  199403     0.054101
```

**Feedback**:
- Num observations with std_diff >= TOL_DIFF_1: 0/4981661 (0.000%)
- Stata standard deviation: 3.12e-02

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
- Python: 3,458,602
- Common: 3,458,422

**Precision1**: 0.697% obs with std_diff >= 1.00e-02 (tolerance: < 0.1%)

**Precision2**: 100th percentile diff = 4.39e-02 (tolerance: < 1.00e-06)

**Feedback**:
- Num observations with std_diff >= TOL_DIFF_1: 24112/3458422 (0.697%)
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
- Test 2 - Superset check: ✅ PASSED
- Test 3 - Precision1 check: ❌ FAILED
- Test 4 - Precision2 check: ❌ FAILED

**Columns**: ['ReturnSkew3F']

**Observations**:
- Stata:  4,978,948
- Python: 4,988,237
- Common: 4,978,948

**Precision1**: 2.676% obs with std_diff >= 1.00e-02 (tolerance: < 0.1%)

**Precision2**: 100th percentile diff = 5.91e+00 (tolerance: < 1.00e-06)

**Feedback**:
- Num observations with std_diff >= TOL_DIFF_1: 133232/4978948 (2.676%)
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
0   11651  198709 -1.776812  4.129483 -5.906295
1   21232  197411 -1.811528  3.474396 -5.285924
2   31317  196511  0.987175 -4.129483  5.116658
3   36169  196511  0.987175 -4.129483  5.116658
4   24994  198601 -0.834719  4.248529 -5.083248
5   92954  198601 -0.834719  4.248529 -5.083248
6   10072  199207  0.641259 -4.364358  5.005617
7   10245  199207  0.641259 -4.364358  5.005617
8   26551  199207  0.641259 -4.364358  5.005617
9   28864  199207  0.641259 -4.364358  5.005617
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
- Python: 5,153,763
- Common: 3,655,889

**Precision1**: 1.357% obs with std_diff >= 1.00e-02 (tolerance: < 0.1%)

**Precision2**: 100th percentile diff = 1.64e-01 (tolerance: < 1.00e-06)

**Feedback**:
- Num observations with std_diff >= TOL_DIFF_1: 49596/3655889 (1.357%)
- Stata standard deviation: 2.07e-02

**Most Recent Bad Observations**:
```
   permno  yyyymm    python     stata      diff
0   10066  202412 -0.042738 -0.007268 -0.035470
1   10253  202412 -0.051729 -0.054648  0.002919
2   11153  202412 -0.051729  0.001885 -0.053615
3   11379  202412 -0.036342 -0.014016 -0.022326
4   12828  202412 -0.051729 -0.054894  0.003165
5   12839  202412 -0.051729 -0.055632  0.003903
6   12928  202412  0.108894 -0.000076  0.108969
7   13563  202412 -0.019177 -0.051617  0.032440
8   13779  202412 -0.051729 -0.052743  0.001014
9   13828  202412 -0.051729 -0.036236 -0.015493
```

**Largest Differences**:
```
   permno  yyyymm    python     stata      diff
0   83630  201203  0.125749 -0.037886  0.163634
1   88937  202412  0.166484  0.006299  0.160185
2   83630  201204  0.119393 -0.032068  0.151461
3   30744  200111  0.155265  0.008748  0.146517
4   84521  201001  0.130462 -0.014673  0.145135
5   27167  201712  0.147492  0.003482  0.144010
6   83630  201205  0.112769 -0.029291  0.142060
7   84757  202003  0.145373  0.004022  0.141350
8   30744  200112  0.146678  0.008842  0.137836
9   27167  201801  0.141298  0.003938  0.137359
```

---

