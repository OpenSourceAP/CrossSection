# 0811-n3-fastxtile-usage-survey

## Overview
Survey of all Stata .do files in Code/Predictors/ that use the `fastxtile` command.

## Results
Found 26 files using fastxtile:

1. AccrualsBM.do ❌
2. ChForecastAccrual.do ❌
3. ChNAnalyst.do ❌
4. CitationsRD.do ❌
5. ConsRecomm.do ❌
6. DivYieldST.do ✅
7. EquityDuration.do ❌
8. FirmAgeMom.do ❌
9. GrAdExp.do ❌
10. MS.do ✅
11. MomRev.do ❌
12. MomVol.do ❌
13. NetDebtPrice.do ✅
14. OScore.do ❌
15. OperProf.do ❌
16. PS.do ✅
17. PatentsRD.do ❌
18. ProbInformedTrading.do ❌
19. RDAbility.do ✅
20. RDcap.do ❌
21. ZZ1_Activism1_Activism2.do ❌
22. ZZ1_AnalystValue_AOP_PredictedFE_IntrinsicValue.do ❌
23. ZZ1_RIO_MB_RIO_Disp_RIO_Turnover_RIO_Volatility.do ❌
24. sfe.do ❌
25. std_turn.do ❌
26. tang.do ❌

## Notes
- Total: 26 out of ~180 predictor files use fastxtile
- This represents about 14% of all predictor files
- fastxtile is used for creating quantile-based rankings/groups in Stata

## Python Implementation Status
- ✅ = Uses standardized `stata_fastxtile` function from utils/ (5 files)
- ❌ = Uses inline fastxtile implementation instead of standardized function (21 files)

**Standardized Implementation**: DivYieldST, MS, NetDebtPrice, PS, RDAbility
**Needs Standardization**: AccrualsBM, ChForecastAccrual, ChNAnalyst, CitationsRD, ConsRecomm, EquityDuration, FirmAgeMom, GrAdExp, MomRev, MomVol, OScore, OperProf, PatentsRD, ProbInformedTrading, RDcap, ZZ1_Activism1_Activism2, ZZ1_AnalystValue_AOP_PredictedFE_IntrinsicValue, ZZ1_RIO_MB_RIO_Disp_RIO_Turnover_RIO_Volatility, sfe, std_turn, tang

# Predictor Validation Results

**Generated**: 2025-08-11 18:37:43

**Configuration**:
- PTH_PERCENTILE: 1.0
- TOL_DIFF_1: 0.01
- TOL_OBS_1: 0.1%
- TOL_DIFF_2: 1e-06
- INDEX_COLS: ['permno', 'yyyymm']

## Summary

| Predictor                 | Python CSV | Columns  | Superset  | Precision1   | Precision2              |
|---------------------------|------------|----------|-----------|--------------|-------------------------|
| PatentsRD                 | ✅         | ✅       | ❌ (58.66%)  | ❌ (15.70%)   | ❌ (100th diff 1.0E+00)  |
| RDAbility                 | ✅         | ✅       | ❌ (4.95%)   | ❌ (9.52%)    | ❌ (100th diff 1.9E+02)  |
| FirmAgeMom                | ✅         | ✅       | ❌ (1.85%)   | ❌ (0.39%)    | ❌ (100th diff 2.0E+00)  |
| MomRev                    | ✅         | ✅       | ❌ (1.26%)   | ✅ (0.00%)    | ✅ (100th diff 0.0E+00)  |
| ConsRecomm                | ✅         | ✅       | ❌ (0.23%)   | ✅ (0.01%)    | ❌ (100th diff 1.0E+00)  |
| sfe                       | ✅         | ✅       | ❌ (0.20%)   | ✅ (0.02%)    | ❌ (100th diff 1.0E+01)  |
| ChNAnalyst                | ✅         | ✅       | ❌ (0.11%)   | ✅ (0.01%)    | ❌ (100th diff 1.0E+00)  |
| std_turn                  | ✅         | ✅       | ❌ (0.04%)   | ✅ (0.00%)    | ❌ (100th diff 1.9E-05)  |
| tang                      | ✅         | ✅       | ❌ (0.02%)   | ✅ (0.00%)    | ❌ (100th diff 2.4E-03)  |
| PS                        | ✅         | ✅       | ❌ (0.00%)   | ❌ (17.90%)   | ❌ (100th diff 5.0E+00)  |
| MomVol                    | ✅         | ✅       | ❌ (0.00%)   | ❌ (0.42%)    | ❌ (100th diff 1.0E+00)  |
| DivYieldST                | ✅         | ✅       | ❌ (0.00%)   | ❌ (0.13%)    | ❌ (100th diff 3.0E+00)  |
| NetDebtPrice              | ✅         | ✅       | ❌ (0.00%)   | ✅ (0.00%)    | ❌ (100th diff 4.2E-02)  |
| MS                        | ✅         | ✅       | ✅           | ❌ (63.45%)   | ❌ (100th diff 5.0E+00)  |
| ChForecastAccrual         | ✅         | ✅       | ✅           | ❌ (0.12%)    | ❌ (100th diff 1.0E+00)  |
| CitationsRD               | ✅         | ✅       | ✅           | ✅ (0.00%)    | ❌ (100th diff 1.0E+00)  |
| OperProf                  | ✅         | ✅       | ✅           | ✅ (0.00%)    | ❌ (100th diff 2.5E-01)  |
| EquityDuration            | ✅         | ✅       | ✅           | ✅ (0.00%)    | ❌ (100th diff 3.3E+05)  |
| RDcap                     | ✅         | ✅       | ✅           | ✅ (0.00%)    | ❌ (100th diff 1.3E-06)  |
| ProbInformedTrading       | ✅         | ✅       | ✅           | ✅ (0.00%)    | ✅ (100th diff 5.0E-08)  |
| AccrualsBM                | ✅         | ✅       | ✅           | ✅ (0.00%)    | ✅ (100th diff 0.0E+00)  |

**Overall**: 2/21 available predictors passed validation
**Python CSVs**: 21/21 predictors have Python implementation

## Detailed Results

### AccrualsBM

**Status**: ✅ PASSED

**Test Results**:
- Test 1 - Column names: ✅ PASSED
- Test 2 - Superset check: ✅ PASSED
- Test 3 - Precision1 check: ✅ PASSED
- Test 4 - Precision2 check: ✅ PASSED

**Columns**: ['AccrualsBM']

**Observations**:
- Stata:  220,066
- Python: 1,511,502
- Common: 220,066

**Precision1**: 0.000% obs with std_diff >= 1.00e-02 (tolerance: < 0.1%)

**Precision2**: 100th percentile diff = 0.00e+00 (tolerance: < 1.00e-06)

**Feedback**:
- Num observations with std_diff >= TOL_DIFF_1: 0/220066 (0.000%)
- Stata standard deviation: 5.00e-01

---

### ChForecastAccrual

**Status**: ❌ FAILED

**Test Results**:
- Test 1 - Column names: ✅ PASSED
- Test 2 - Superset check: ✅ PASSED
- Test 3 - Precision1 check: ❌ FAILED
- Test 4 - Precision2 check: ❌ FAILED

**Columns**: ['ChForecastAccrual']

**Observations**:
- Stata:  628,022
- Python: 2,222,361
- Common: 628,022

**Precision1**: 0.118% obs with std_diff >= 1.00e-02 (tolerance: < 0.1%)

**Precision2**: 100th percentile diff = 1.00e+00 (tolerance: < 1.00e-06)

**Feedback**:
- Num observations with std_diff >= TOL_DIFF_1: 741/628022 (0.118%)
- Stata standard deviation: 4.99e-01

**Most Recent Bad Observations**:
```
   permno  yyyymm  python  stata  diff
0   91575  202412     0.0      1  -1.0
1   69032  202411     0.0      1  -1.0
2   69032  202410     0.0      1  -1.0
3   69032  202408     0.0      1  -1.0
4   69032  202407     0.0      1  -1.0
5   21889  202406     1.0      0   1.0
6   21186  202405     0.0      1  -1.0
7   69032  202405     0.0      1  -1.0
8   91575  202405     0.0      1  -1.0
9   69032  202404     0.0      1  -1.0
```

**Largest Differences**:
```
   permno  yyyymm  python  stata  diff
0   11406  199508     0.0      1  -1.0
1   11406  199509     0.0      1  -1.0
2   11406  199605     0.0      1  -1.0
3   11406  199709     0.0      1  -1.0
4   12473  201111     1.0      0   1.0
5   12473  201212     1.0      0   1.0
6   12473  201308     1.0      0   1.0
7   12473  201311     1.0      0   1.0
8   12473  201404     0.0      1  -1.0
9   12473  201405     0.0      1  -1.0
```

---

### ChNAnalyst

**Status**: ❌ FAILED

**Test Results**:
- Test 1 - Column names: ✅ PASSED
- Test 2 - Superset check: ❌ FAILED (Python missing 232 Stata observations)
- Test 3 - Precision1 check: ✅ PASSED
- Test 4 - Precision2 check: ❌ FAILED

**Columns**: ['ChNAnalyst']

**Observations**:
- Stata:  210,988
- Python: 210,931
- Common: 210,756

**Precision1**: 0.007% obs with std_diff >= 1.00e-02 (tolerance: < 0.1%)

**Precision2**: 100th percentile diff = 1.00e+00 (tolerance: < 1.00e-06)

**Missing Observations Sample**:
```
 index  permno  yyyymm  ChNAnalyst
     0   11406  199011           0
     1   11406  199012           0
     2   11406  199101           0
     3   11406  199108           0
     4   11406  199110           0
     5   12265  199002           0
     6   16249  200911           0
     7   16249  200912           0
     8   16249  201001           0
     9   16249  201002           0
```

**Feedback**:
- Num observations with std_diff >= TOL_DIFF_1: 14/210756 (0.007%)
- Stata standard deviation: 3.56e-01

**Most Recent Bad Observations**:
```
   permno  yyyymm  python  stata  diff
0   63781  202004     0.0      1  -1.0
1   63781  202003     0.0      1  -1.0
2   63781  202001     1.0      0   1.0
3   77883  199811     0.0      1  -1.0
4   77883  199810     0.0      1  -1.0
5   77883  199809     0.0      1  -1.0
6   77883  199808     0.0      1  -1.0
7   63781  199301     1.0      0   1.0
8   63781  199207     0.0      1  -1.0
9   63781  199206     0.0      1  -1.0
```

**Largest Differences**:
```
   permno  yyyymm  python  stata  diff
0   63781  199111     0.0      1  -1.0
1   63781  199201     1.0      0   1.0
2   63781  199202     1.0      0   1.0
3   63781  199203     1.0      0   1.0
4   63781  199206     0.0      1  -1.0
5   63781  199207     0.0      1  -1.0
6   63781  199301     1.0      0   1.0
7   63781  202001     1.0      0   1.0
8   63781  202003     0.0      1  -1.0
9   63781  202004     0.0      1  -1.0
```

---

### CitationsRD

**Status**: ❌ FAILED

**Test Results**:
- Test 1 - Column names: ✅ PASSED
- Test 2 - Superset check: ✅ PASSED
- Test 3 - Precision1 check: ✅ PASSED
- Test 4 - Precision2 check: ❌ FAILED

**Columns**: ['CitationsRD']

**Observations**:
- Stata:  645,360
- Python: 701,940
- Common: 645,360

**Precision1**: 0.002% obs with std_diff >= 1.00e-02 (tolerance: < 0.1%)

**Precision2**: 100th percentile diff = 1.00e+00 (tolerance: < 1.00e-06)

**Feedback**:
- Num observations with std_diff >= TOL_DIFF_1: 12/645360 (0.002%)
- Stata standard deviation: 4.11e-01

**Most Recent Bad Observations**:
```
   permno  yyyymm  python  stata  diff
0   84136  200105     0.0      1  -1.0
1   84136  200104     0.0      1  -1.0
2   84136  200103     0.0      1  -1.0
3   84136  200102     0.0      1  -1.0
4   84136  200101     0.0      1  -1.0
5   84136  200012     0.0      1  -1.0
6   84136  200011     0.0      1  -1.0
7   84136  200010     0.0      1  -1.0
8   84136  200009     0.0      1  -1.0
9   84136  200008     0.0      1  -1.0
```

**Largest Differences**:
```
   permno  yyyymm  python  stata  diff
0   84136  200006     0.0      1  -1.0
1   84136  200007     0.0      1  -1.0
2   84136  200008     0.0      1  -1.0
3   84136  200009     0.0      1  -1.0
4   84136  200010     0.0      1  -1.0
5   84136  200011     0.0      1  -1.0
6   84136  200012     0.0      1  -1.0
7   84136  200101     0.0      1  -1.0
8   84136  200102     0.0      1  -1.0
9   84136  200103     0.0      1  -1.0
```

---

### ConsRecomm

**Status**: ❌ FAILED

**Test Results**:
- Test 1 - Column names: ✅ PASSED
- Test 2 - Superset check: ❌ FAILED (Python missing 303 Stata observations)
- Test 3 - Precision1 check: ✅ PASSED
- Test 4 - Precision2 check: ❌ FAILED

**Columns**: ['ConsRecomm']

**Observations**:
- Stata:  134,102
- Python: 372,799
- Common: 133,799

**Precision1**: 0.011% obs with std_diff >= 1.00e-02 (tolerance: < 0.1%)

**Precision2**: 100th percentile diff = 1.00e+00 (tolerance: < 1.00e-06)

**Missing Observations Sample**:
```
 index  permno  yyyymm  ConsRecomm
     0   11406  199311           0
     1   11406  199412           0
     2   11406  199606           1
     3   11406  199609           0
     4   11406  199701           1
     5   12473  201111           1
     6   12473  201204           0
     7   12473  201304           0
     8   12473  201309           0
     9   12473  201504           0
```

**Feedback**:
- Num observations with std_diff >= TOL_DIFF_1: 15/133799 (0.011%)
- Stata standard deviation: 4.41e-01

**Most Recent Bad Observations**:
```
   permno  yyyymm  python  stata  diff
0   91575  202307     0.0      1  -1.0
1   12473  201704     1.0      0   1.0
2   91575  201609     1.0      0   1.0
3   63781  201605     1.0      0   1.0
4   63781  201507     1.0      0   1.0
5   12473  201505     0.0      1  -1.0
6   63781  201410     1.0      0   1.0
7   21186  201206     1.0      0   1.0
8   63781  200912     1.0      0   1.0
9   63781  200411     0.0      1  -1.0
```

**Largest Differences**:
```
   permno  yyyymm  python  stata  diff
0   12473  201505     0.0      1  -1.0
1   12473  201704     1.0      0   1.0
2   21186  199404     1.0      0   1.0
3   21186  201206     1.0      0   1.0
4   51633  199403     0.0      1  -1.0
5   51633  199408     0.0      1  -1.0
6   51633  199608     0.0      1  -1.0
7   63781  200411     0.0      1  -1.0
8   63781  200912     1.0      0   1.0
9   63781  201410     1.0      0   1.0
```

---

### DivYieldST

**Status**: ❌ FAILED

**Test Results**:
- Test 1 - Column names: ✅ PASSED
- Test 2 - Superset check: ❌ FAILED (Python missing 3 Stata observations)
- Test 3 - Precision1 check: ❌ FAILED
- Test 4 - Precision2 check: ❌ FAILED

**Columns**: ['DivYieldST']

**Observations**:
- Stata:  1,591,700
- Python: 1,601,392
- Common: 1,591,697

**Precision1**: 0.132% obs with std_diff >= 1.00e-02 (tolerance: < 0.1%)

**Precision2**: 100th percentile diff = 3.00e+00 (tolerance: < 1.00e-06)

**Missing Observations Sample**:
```
 index  permno  yyyymm  DivYieldST
     0   84735  199001           0
     1   84735  199002           0
     2   84735  199003           0
```

**Feedback**:
- Num observations with std_diff >= TOL_DIFF_1: 2100/1591697 (0.132%)
- Stata standard deviation: 1.03e+00

**Most Recent Bad Observations**:
```
   permno  yyyymm  python  stata  diff
0   12515  202412     3.0      2   1.0
1   21594  202412     2.0      1   1.0
2   76224  202411     2.0      1   1.0
3   90868  202411     3.0      2   1.0
4   45911  202410     3.0      2   1.0
5   90454  202410     2.0      1   1.0
6   20913  202407     3.0      2   1.0
7   91902  202407     2.0      1   1.0
8   77117  202406     2.0      1   1.0
9   91403  202406     3.0      2   1.0
```

**Largest Differences**:
```
   permno  yyyymm  python  stata  diff
0   12072  199109     3.0      0   3.0
1   13007  202303     3.0      0   3.0
2   16620  197306     3.0      0   3.0
3   17742  193701     3.0      0   3.0
4   19393  201609     3.0      0   3.0
5   25590  199209     3.0      0   3.0
6   36396  196503     3.0      0   3.0
7   39483  199703     3.0      0   3.0
8   47571  198403     3.0      0   3.0
9   50956  197402     3.0      0   3.0
```

---

### EquityDuration

**Status**: ❌ FAILED

**Test Results**:
- Test 1 - Column names: ✅ PASSED
- Test 2 - Superset check: ✅ PASSED
- Test 3 - Precision1 check: ✅ PASSED
- Test 4 - Precision2 check: ❌ FAILED

**Columns**: ['EquityDuration']

**Observations**:
- Stata:  3,124,663
- Python: 3,201,768
- Common: 3,124,663

**Precision1**: 0.000% obs with std_diff >= 1.00e-02 (tolerance: < 0.1%)

**Precision2**: 100th percentile diff = 3.26e+05 (tolerance: < 1.00e-06)

**Feedback**:
- Num observations with std_diff >= TOL_DIFF_1: 0/3124663 (0.000%)
- Stata standard deviation: 5.69e+09

---

### FirmAgeMom

**Status**: ❌ FAILED

**Test Results**:
- Test 1 - Column names: ✅ PASSED
- Test 2 - Superset check: ❌ FAILED (Python missing 10169 Stata observations)
- Test 3 - Precision1 check: ❌ FAILED
- Test 4 - Precision2 check: ❌ FAILED

**Columns**: ['FirmAgeMom']

**Observations**:
- Stata:  550,434
- Python: 570,774
- Common: 540,265

**Precision1**: 0.388% obs with std_diff >= 1.00e-02 (tolerance: < 0.1%)

**Precision2**: 100th percentile diff = 2.03e+00 (tolerance: < 1.00e-06)

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

**Most Recent Bad Observations**:
```
   permno  yyyymm    python     stata      diff
0   15266  201805  0.007699 -0.000955  0.008654
1   15266  201804  0.028985  0.025023  0.003962
2   15266  201803  0.007218  0.011110 -0.003893
3   15266  201802  0.012596  0.005774  0.006822
4   15280  201703  0.365385  0.352381  0.013003
5   15266  201702  0.032934  0.024753  0.008182
6   15280  201702 -0.020187 -0.043269  0.023082
7   15280  201701 -0.074111 -0.052684 -0.021426
8   15525  201701  0.011735  0.019014 -0.007279
9   15280  201612 -0.042553 -0.047161  0.004608
```

**Largest Differences**:
```
   permno  yyyymm    python     stata      diff
0   22270  198106  2.029051  0.000000  2.029051
1   22270  198108  1.740113 -0.237288  1.977401
2   22270  198105  1.914746  0.000000  1.914746
3   22270  198107  1.506913 -0.237288  1.744201
4   11236  192901  1.281258  0.000000  1.281258
5   11236  192904  1.221746  0.000000  1.221746
6   47846  197905  1.000000  0.000000  1.000000
7   20271  194207  1.428178  0.468201  0.959977
8   18577  193207 -0.019230  0.888889 -0.908119
9   17865  193211  0.118470  1.007253 -0.888784
```

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

**Precision1**: 63.453% obs with std_diff >= 1.00e-02 (tolerance: < 0.1%)

**Precision2**: 100th percentile diff = 5.00e+00 (tolerance: < 1.00e-06)

**Feedback**:
- Num observations with std_diff >= TOL_DIFF_1: 300181/473079 (63.453%)
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
9   12082  202412       4      5    -1
```

**Largest Differences**:
```
   permno  yyyymm  python  stata  diff
0   10051  199206       1      6    -5
1   10051  199207       1      6    -5
2   10051  199208       1      6    -5
3   10051  199209       1      6    -5
4   10051  199210       1      6    -5
5   10051  199211       1      6    -5
6   10051  199212       1      6    -5
7   10051  199301       1      6    -5
8   10051  199304       1      6    -5
9   10051  199305       1      6    -5
```

---

### MomRev

**Status**: ❌ FAILED

**Test Results**:
- Test 1 - Column names: ✅ PASSED
- Test 2 - Superset check: ❌ FAILED (Python missing 3313 Stata observations)
- Test 3 - Precision1 check: ✅ PASSED
- Test 4 - Precision2 check: ✅ PASSED

**Columns**: ['MomRev']

**Observations**:
- Stata:  262,210
- Python: 266,161
- Common: 258,897

**Precision1**: 0.000% obs with std_diff >= 1.00e-02 (tolerance: < 0.1%)

**Precision2**: 100th percentile diff = 0.00e+00 (tolerance: < 1.00e-06)

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
- Num observations with std_diff >= TOL_DIFF_1: 0/258897 (0.000%)
- Stata standard deviation: 4.97e-01

---

### MomVol

**Status**: ❌ FAILED

**Test Results**:
- Test 1 - Column names: ✅ PASSED
- Test 2 - Superset check: ❌ FAILED (Python missing 28 Stata observations)
- Test 3 - Precision1 check: ❌ FAILED
- Test 4 - Precision2 check: ❌ FAILED

**Columns**: ['MomVol']

**Observations**:
- Stata:  1,095,615
- Python: 1,098,011
- Common: 1,095,587

**Precision1**: 0.417% obs with std_diff >= 1.00e-02 (tolerance: < 0.1%)

**Precision2**: 100th percentile diff = 1.00e+00 (tolerance: < 1.00e-06)

**Missing Observations Sample**:
```
 index  permno  yyyymm  MomVol
     0   11795  199011       5
     1   18365  202303       2
     2   21055  196909       5
     3   23683  196512       1
     4   27078  197208       5
     5   27860  198309       3
     6   29532  196906       6
     7   33478  196908      10
     8   36767  196906       1
     9   39810  197312       8
```

**Feedback**:
- Num observations with std_diff >= TOL_DIFF_1: 4567/1095587 (0.417%)
- Stata standard deviation: 2.88e+00

**Most Recent Bad Observations**:
```
   permno  yyyymm  python  stata  diff
0   19495  202412     9.0      8   1.0
1   20867  202412     6.0      5   1.0
2   22293  202412     8.0      7   1.0
3   46886  202412     3.0      2   1.0
4   85035  202412     2.0      1   1.0
5   90386  202412     4.0      3   1.0
6   90993  202412     7.0      6   1.0
7   13586  202411     9.0      8   1.0
8   34817  202411     4.0      3   1.0
9   93289  202411     3.0      2   1.0
```

**Largest Differences**:
```
   permno  yyyymm  python  stata  diff
0   10006  194301     4.0      3   1.0
1   10006  195503     8.0      7   1.0
2   10014  196802    10.0      9   1.0
3   10064  198901     4.0      3   1.0
4   10066  198710     2.0      1   1.0
5   10071  199204     4.0      3   1.0
6   10078  200911     3.0      2   1.0
7   10089  198908     8.0      7   1.0
8   10102  193202     8.0      7   1.0
9   10102  193210     7.0      6   1.0
```

---

### NetDebtPrice

**Status**: ❌ FAILED

**Test Results**:
- Test 1 - Column names: ✅ PASSED
- Test 2 - Superset check: ❌ FAILED (Python missing 1 Stata observations)
- Test 3 - Precision1 check: ✅ PASSED
- Test 4 - Precision2 check: ❌ FAILED

**Columns**: ['NetDebtPrice']

**Observations**:
- Stata:  1,425,163
- Python: 1,426,019
- Common: 1,425,162

**Precision1**: 0.000% obs with std_diff >= 1.00e-02 (tolerance: < 0.1%)

**Precision2**: 100th percentile diff = 4.24e-02 (tolerance: < 1.00e-06)

**Missing Observations Sample**:
```
 index  permno  yyyymm  NetDebtPrice
     0   23033  202412     -0.345379
```

**Feedback**:
- Num observations with std_diff >= TOL_DIFF_1: 0/1425162 (0.000%)
- Stata standard deviation: 7.00e+00

---

### OperProf

**Status**: ❌ FAILED

**Test Results**:
- Test 1 - Column names: ✅ PASSED
- Test 2 - Superset check: ✅ PASSED
- Test 3 - Precision1 check: ✅ PASSED
- Test 4 - Precision2 check: ❌ FAILED

**Columns**: ['OperProf']

**Observations**:
- Stata:  1,407,636
- Python: 1,714,647
- Common: 1,407,636

**Precision1**: 0.000% obs with std_diff >= 1.00e-02 (tolerance: < 0.1%)

**Precision2**: 100th percentile diff = 2.51e-01 (tolerance: < 1.00e-06)

**Feedback**:
- Num observations with std_diff >= TOL_DIFF_1: 7/1407636 (0.000%)
- Stata standard deviation: 1.62e+01

**Most Recent Bad Observations**:
```
   permno  yyyymm    python      stata      diff
0   82702  202412  12.77903  12.527678  0.251352
1   82702  202411  12.77903  12.527678  0.251352
2   82702  202410  12.77903  12.527678  0.251352
3   82702  202409  12.77903  12.527678  0.251352
4   82702  202408  12.77903  12.527678  0.251352
5   82702  202407  12.77903  12.527678  0.251352
6   82702  202406  12.77903  12.527678  0.251352
```

**Largest Differences**:
```
   permno  yyyymm    python      stata      diff
0   82702  202406  12.77903  12.527678  0.251352
1   82702  202407  12.77903  12.527678  0.251352
2   82702  202408  12.77903  12.527678  0.251352
3   82702  202409  12.77903  12.527678  0.251352
4   82702  202410  12.77903  12.527678  0.251352
5   82702  202411  12.77903  12.527678  0.251352
6   82702  202412  12.77903  12.527678  0.251352
```

---

### PS

**Status**: ❌ FAILED

**Test Results**:
- Test 1 - Column names: ✅ PASSED
- Test 2 - Superset check: ❌ FAILED (Python missing 3 Stata observations)
- Test 3 - Precision1 check: ❌ FAILED
- Test 4 - Precision2 check: ❌ FAILED

**Columns**: ['PS']

**Observations**:
- Stata:  463,944
- Python: 464,239
- Common: 463,941

**Precision1**: 17.896% obs with std_diff >= 1.00e-02 (tolerance: < 0.1%)

**Precision2**: 100th percentile diff = 5.00e+00 (tolerance: < 1.00e-06)

**Missing Observations Sample**:
```
 index  permno  yyyymm  PS
     0   23033  202409   5
     1   23033  202410   5
     2   23033  202411   5
```

**Feedback**:
- Num observations with std_diff >= TOL_DIFF_1: 83027/463941 (17.896%)
- Stata standard deviation: 1.70e+00

**Most Recent Bad Observations**:
```
   permno  yyyymm  python  stata  diff
0   11593  202412     5.0      6  -1.0
1   12641  202412     6.0      7  -1.0
2   13583  202412     2.0      7  -5.0
3   13919  202412     5.0      6  -1.0
4   14419  202412     3.0      4  -1.0
5   14468  202412     3.0      4  -1.0
6   14540  202412     5.0      6  -1.0
7   14601  202412     5.0      6  -1.0
8   14826  202412     2.0      3  -1.0
9   15133  202412     6.0      7  -1.0
```

**Largest Differences**:
```
   permno  yyyymm  python  stata  diff
0   10001  198705     3.0      8  -5.0
1   10001  198706     3.0      8  -5.0
2   10001  198707     3.0      8  -5.0
3   10001  198709     3.0      8  -5.0
4   10005  198706     1.0      6  -5.0
5   10005  198707     1.0      6  -5.0
6   10005  198708     1.0      6  -5.0
7   10005  198709     1.0      6  -5.0
8   10005  198710     1.0      6  -5.0
9   10005  198711     1.0      6  -5.0
```

---

### PatentsRD

**Status**: ❌ FAILED

**Test Results**:
- Test 1 - Column names: ✅ PASSED
- Test 2 - Superset check: ❌ FAILED (Python missing 394114 Stata observations)
- Test 3 - Precision1 check: ❌ FAILED
- Test 4 - Precision2 check: ❌ FAILED

**Columns**: ['PatentsRD']

**Observations**:
- Stata:  671,832
- Python: 479,052
- Common: 277,718

**Precision1**: 15.700% obs with std_diff >= 1.00e-02 (tolerance: < 0.1%)

**Precision2**: 100th percentile diff = 1.00e+00 (tolerance: < 1.00e-06)

**Missing Observations Sample**:
```
 index  permno  yyyymm  PatentsRD
     0   10006  198401          1
     1   10006  198402          1
     2   10006  198403          1
     3   10006  198404          1
     4   10006  198405          1
     5   10010  198906          0
     6   10010  198907          0
     7   10010  198908          0
     8   10010  198909          0
     9   10010  198910          0
```

**Feedback**:
- Num observations with std_diff >= TOL_DIFF_1: 43603/277718 (15.700%)
- Stata standard deviation: 4.56e-01

**Most Recent Bad Observations**:
```
   permno  yyyymm  python  stata  diff
0   10026  202412     1.0      0   1.0
1   10258  202412     1.0      0   1.0
2   10333  202412     1.0      0   1.0
3   10382  202412     1.0      0   1.0
4   10645  202412     1.0      0   1.0
5   10860  202412     1.0      0   1.0
6   11154  202412     1.0      0   1.0
7   11275  202412     1.0      0   1.0
8   11292  202412     1.0      0   1.0
9   11581  202412     1.0      0   1.0
```

**Largest Differences**:
```
   permno  yyyymm  python  stata  diff
0   10025  200806     1.0      0   1.0
1   10025  200807     1.0      0   1.0
2   10025  200808     1.0      0   1.0
3   10025  200809     1.0      0   1.0
4   10025  200810     1.0      0   1.0
5   10025  200811     1.0      0   1.0
6   10025  200812     1.0      0   1.0
7   10025  201606     1.0      0   1.0
8   10025  201607     1.0      0   1.0
9   10025  201608     1.0      0   1.0
```

---

### ProbInformedTrading

**Status**: ✅ PASSED

**Test Results**:
- Test 1 - Column names: ✅ PASSED
- Test 2 - Superset check: ✅ PASSED
- Test 3 - Precision1 check: ✅ PASSED
- Test 4 - Precision2 check: ✅ PASSED

**Columns**: ['ProbInformedTrading']

**Observations**:
- Stata:  24,028
- Python: 24,028
- Common: 24,028

**Precision1**: 0.000% obs with std_diff >= 1.00e-02 (tolerance: < 0.1%)

**Precision2**: 100th percentile diff = 5.00e-08 (tolerance: < 1.00e-06)

**Feedback**:
- Num observations with std_diff >= TOL_DIFF_1: 0/24028 (0.000%)
- Stata standard deviation: 6.67e-02

---

### RDAbility

**Status**: ❌ FAILED

**Test Results**:
- Test 1 - Column names: ✅ PASSED
- Test 2 - Superset check: ❌ FAILED (Python missing 8575 Stata observations)
- Test 3 - Precision1 check: ❌ FAILED
- Test 4 - Precision2 check: ❌ FAILED

**Columns**: ['RDAbility']

**Observations**:
- Stata:  173,266
- Python: 231,277
- Common: 164,691

**Precision1**: 9.523% obs with std_diff >= 1.00e-02 (tolerance: < 0.1%)

**Precision2**: 100th percentile diff = 1.93e+02 (tolerance: < 1.00e-06)

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

**Most Recent Bad Observations**:
```
   permno  yyyymm     python      stata      diff
0   16968  202606   2.676225   4.362977 -1.686752
1   13918  202605   0.010309   0.838733 -0.828424
2   14551  202605   0.181759   0.240248 -0.058489
3   14708  202605  -0.071227   0.093842 -0.165069
4   15171  202605   0.227063   0.049347  0.177717
5   15186  202605   0.681919   0.779686 -0.097767
6   15269  202605   0.045002   0.172714 -0.127712
7   15272  202605 -16.648409 -17.745199  1.096790
8   15284  202605   0.523626   0.227037  0.296588
9   15361  202605   0.370782   0.464217 -0.093434
```

**Largest Differences**:
```
   permno  yyyymm      python     stata       diff
0   86597  199512 -184.028411  8.653519 -192.68193
1   86597  199601 -184.028411  8.653519 -192.68193
2   86597  199602 -184.028411  8.653519 -192.68193
3   86597  199603 -184.028411  8.653519 -192.68193
4   86597  199604 -184.028411  8.653519 -192.68193
5   86597  199605 -184.028411  8.653519 -192.68193
6   86597  199606 -184.028411  8.653519 -192.68193
7   86597  199607 -184.028411  8.653519 -192.68193
8   86597  199608 -184.028411  8.653519 -192.68193
9   86597  199609 -184.028411  8.653519 -192.68193
```

---

### RDcap

**Status**: ❌ FAILED

**Test Results**:
- Test 1 - Column names: ✅ PASSED
- Test 2 - Superset check: ✅ PASSED
- Test 3 - Precision1 check: ✅ PASSED
- Test 4 - Precision2 check: ❌ FAILED

**Columns**: ['RDcap']

**Observations**:
- Stata:  517,737
- Python: 1,404,631
- Common: 517,737

**Precision1**: 0.000% obs with std_diff >= 1.00e-02 (tolerance: < 0.1%)

**Precision2**: 100th percentile diff = 1.32e-06 (tolerance: < 1.00e-06)

**Feedback**:
- Num observations with std_diff >= TOL_DIFF_1: 0/517737 (0.000%)
- Stata standard deviation: 6.98e-01

---

### sfe

**Status**: ❌ FAILED

**Test Results**:
- Test 1 - Column names: ✅ PASSED
- Test 2 - Superset check: ❌ FAILED (Python missing 1200 Stata observations)
- Test 3 - Precision1 check: ✅ PASSED
- Test 4 - Precision2 check: ❌ FAILED

**Columns**: ['sfe']

**Observations**:
- Stata:  611,076
- Python: 611,100
- Common: 609,876

**Precision1**: 0.022% obs with std_diff >= 1.00e-02 (tolerance: < 0.1%)

**Precision2**: 100th percentile diff = 9.99e+00 (tolerance: < 1.00e-06)

**Missing Observations Sample**:
```
 index  permno  yyyymm      sfe
     0   11406  199103 0.195122
     1   11406  199104 0.195122
     2   11406  199105 0.195122
     3   11406  199106 0.195122
     4   11406  199107 0.195122
     5   11406  199108 0.195122
     6   11406  199109 0.195122
     7   11406  199110 0.195122
     8   11406  199111 0.195122
     9   11406  199112 0.195122
```

**Feedback**:
- Num observations with std_diff >= TOL_DIFF_1: 132/609876 (0.022%)
- Stata standard deviation: 1.89e+01

**Most Recent Bad Observations**:
```
   permno  yyyymm    python     stata      diff
0   63781  202102  8.625647 -1.365727  9.991374
1   63781  202101  8.625647 -1.365727  9.991374
2   63781  202012  8.625647 -1.365727  9.991374
3   63781  202011  8.625647 -1.365727  9.991374
4   63781  202010  8.625647 -1.365727  9.991374
5   63781  202009  8.625647 -1.365727  9.991374
6   63781  202008  8.625647 -1.365727  9.991374
7   63781  202007  8.625647 -1.365727  9.991374
8   63781  202006  8.625647 -1.365727  9.991374
9   63781  202005  8.625647 -1.365727  9.991374
```

**Largest Differences**:
```
   permno  yyyymm    python     stata      diff
0   63781  202003  8.625647 -1.365727  9.991374
1   63781  202004  8.625647 -1.365727  9.991374
2   63781  202005  8.625647 -1.365727  9.991374
3   63781  202006  8.625647 -1.365727  9.991374
4   63781  202007  8.625647 -1.365727  9.991374
5   63781  202008  8.625647 -1.365727  9.991374
6   63781  202009  8.625647 -1.365727  9.991374
7   63781  202010  8.625647 -1.365727  9.991374
8   63781  202011  8.625647 -1.365727  9.991374
9   63781  202012  8.625647 -1.365727  9.991374
```

---

### std_turn

**Status**: ❌ FAILED

**Test Results**:
- Test 1 - Column names: ✅ PASSED
- Test 2 - Superset check: ❌ FAILED (Python missing 793 Stata observations)
- Test 3 - Precision1 check: ✅ PASSED
- Test 4 - Precision2 check: ❌ FAILED

**Columns**: ['std_turn']

**Observations**:
- Stata:  2,166,584
- Python: 2,202,032
- Common: 2,165,791

**Precision1**: 0.000% obs with std_diff >= 1.00e-02 (tolerance: < 0.1%)

**Precision2**: 100th percentile diff = 1.89e-05 (tolerance: < 1.00e-06)

**Missing Observations Sample**:
```
 index  permno  yyyymm  std_turn
     0   10006  193903  0.019967
     1   10026  199904  0.025622
     2   10030  195312  0.006631
     3   10065  195008  0.006558
     4   10065  195408  0.002951
     5   10075  199403  0.018339
     6   10185  199607  0.057514
     7   10200  198907  0.082999
     8   10209  195311  0.002715
     9   10268  193009  0.096162
```

**Feedback**:
- Num observations with std_diff >= TOL_DIFF_1: 0/2165791 (0.000%)
- Stata standard deviation: 3.51e+00

---

### tang

**Status**: ❌ FAILED

**Test Results**:
- Test 1 - Column names: ✅ PASSED
- Test 2 - Superset check: ❌ FAILED (Python missing 324 Stata observations)
- Test 3 - Precision1 check: ✅ PASSED
- Test 4 - Precision2 check: ❌ FAILED

**Columns**: ['tang']

**Observations**:
- Stata:  1,517,431
- Python: 1,517,875
- Common: 1,517,107

**Precision1**: 0.002% obs with std_diff >= 1.00e-02 (tolerance: < 0.1%)

**Precision2**: 100th percentile diff = 2.35e-03 (tolerance: < 1.00e-06)

**Missing Observations Sample**:
```
 index  permno  yyyymm     tang
     0   87016  200006 0.925292
     1   87016  200007 0.925292
     2   87016  200008 0.925292
     3   87016  200009 0.925292
     4   87016  200010 0.925292
     5   87016  200011 0.925292
     6   87016  200012 0.925292
     7   87016  200101 0.925292
     8   87016  200102 0.925292
     9   87016  200103 0.925292
```

**Feedback**:
- Num observations with std_diff >= TOL_DIFF_1: 36/1517107 (0.002%)
- Stata standard deviation: 1.89e-01

**Most Recent Bad Observations**:
```
   permno  yyyymm    python    stata      diff
0   79362  202605  1.109873  1.10787  0.002002
1   79362  202604  1.109873  1.10787  0.002002
2   79362  202603  1.109873  1.10787  0.002002
3   79362  202602  1.109873  1.10787  0.002002
4   79362  202601  1.109873  1.10787  0.002002
5   79362  202512  1.109873  1.10787  0.002002
6   79362  202511  1.109873  1.10787  0.002002
7   79362  202510  1.109873  1.10787  0.002002
8   79362  202509  1.109873  1.10787  0.002002
9   79362  202508  1.109873  1.10787  0.002002
```

**Largest Differences**:
```
   permno  yyyymm    python     stata      diff
0   79362  202406  1.711112  1.708761  0.002351
1   79362  202407  1.711112  1.708761  0.002351
2   79362  202408  1.711112  1.708761  0.002351
3   79362  202409  1.711112  1.708761  0.002351
4   79362  202410  1.711112  1.708761  0.002351
5   79362  202411  1.711112  1.708761  0.002351
6   79362  202412  1.711112  1.708761  0.002351
7   79362  202501  1.711112  1.708761  0.002351
8   79362  202502  1.711112  1.708761  0.002351
9   79362  202503  1.711112  1.708761  0.002351
```

---

