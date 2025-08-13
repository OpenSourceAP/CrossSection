# Predictor Validation Results

**Generated**: 2025-08-12 20:10:46

**Configuration**:
- TOL_SUPERSET: 1.0%
- TOL_DIFF_1: 0.01
- TOL_OBS_1: 10%
- EXTREME_Q: 0.99
- TOL_DIFF_2: 0.001
- INDEX_COLS: ['permno', 'yyyymm']

## Summary

| Predictor                 | Python CSV | Columns  | Superset  | Precision1   | Precision2              |
|---------------------------|------------|----------|-----------|--------------|-------------------------|
| AgeIPO                    | ✅         | ❌       | NA          | NA           | NA                      |
| RDIPO                     | ✅         | ❌       | NA          | NA           | NA                      |
| PS                        | ✅         | ✅       | ✅ (0.00%)   | ❌ (17.90%)   | ❌ (99th diff 5.0E+00)   |
| ShareVol                  | ✅         | ✅       | ✅ (0.03%)   | ❌ (14.38%)   | ❌ (99th diff 1.0E+00)   |
| GrLTNOA                   | ❌         | NA      | NA          | NA           | NA                      |

**Overall**: 0/4 available predictors passed validation
**Python CSVs**: 4/5 predictors have Python implementation

## Detailed Results

### PS

**Status**: ❌ FAILED

**Test Results**:
- Test 1 - Column names: ✅ PASSED
- Test 2 - Superset check: ✅ PASSED
- Test 3 - Precision1 check: ❌ FAILED
- Test 4 - Precision2 check: ❌ FAILED

**Columns**: ['PS']

**Observations**:
- Stata:  463,944
- Python: 464,239
- Common: 463,941

**Precision1**: 17.896% obs with std_diff >= 1.00e-02 (tolerance: < 10%)

**Precision2**: 99th percentile diff = 5.00e+00 (tolerance: < 1.00e-03)

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

### ShareVol

**Status**: ❌ FAILED

**Test Results**:
- Test 1 - Column names: ✅ PASSED
- Test 2 - Superset check: ✅ PASSED
- Test 3 - Precision1 check: ❌ FAILED
- Test 4 - Precision2 check: ❌ FAILED

**Columns**: ['ShareVol']

**Observations**:
- Stata:  1,660,340
- Python: 1,660,875
- Common: 1,659,922

**Precision1**: 14.381% obs with std_diff >= 1.00e-02 (tolerance: < 10%)

**Precision2**: 99th percentile diff = 1.00e+00 (tolerance: < 1.00e-03)

**Feedback**:
- Num observations with std_diff >= TOL_DIFF_1: 238708/1659922 (14.381%)
- Stata standard deviation: 4.61e-01

**Most Recent Bad Observations**:
```
   permno  yyyymm  python  stata  diff
0   91428  201605       0      1    -1
1   12877  201403       0      1    -1
2   12877  201402       0      1    -1
3   80443  200010       0      1    -1
4   80443  200009       0      1    -1
5   75549  199807       0      1    -1
6   75549  199806       0      1    -1
7   75549  199805       0      1    -1
8   75549  199804       0      1    -1
9   75549  199803       0      1    -1
```

**Largest Differences**:
```
   permno  yyyymm  python  stata  diff
0   10013  198705       0      1    -1
1   10021  198603       0      1    -1
2   10021  198604       0      1    -1
3   10023  197302       0      1    -1
4   10023  197303       0      1    -1
5   10023  197304       0      1    -1
6   10023  197305       0      1    -1
7   10049  192602       0      1    -1
8   10050  197302       0      1    -1
9   10050  197303       0      1    -1
```

---

### GrLTNOA

**Status**: ❌ MISSING PYTHON CSV

**Error**: Python CSV file not found: ../pyData/Predictors/GrLTNOA.csv

---

### AgeIPO

**Status**: ❌ FAILED

**Test Results**:
- Test 1 - Column names: ❌ FAILED
- Test 2 - Superset check: ❌ FAILED (Python missing 0 Stata observations)
- Test 3 - Precision1 check: ❌ FAILED
- Test 4 - Precision2 check: ❌ FAILED

**Columns**: []

**Observations**:
- Stata:  0
- Python: 353,486
- Common: 0

---

### RDIPO

**Status**: ❌ FAILED

**Test Results**:
- Test 1 - Column names: ❌ FAILED
- Test 2 - Superset check: ❌ FAILED (Python missing 0 Stata observations)
- Test 3 - Precision1 check: ❌ FAILED
- Test 4 - Precision2 check: ❌ FAILED

**Columns**: []

**Observations**:
- Stata:  0
- Python: 3,625,491
- Common: 0

---

