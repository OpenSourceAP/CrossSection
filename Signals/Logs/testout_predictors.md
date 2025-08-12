# Predictor Validation Results

**Generated**: 2025-08-12 09:57:21

**Configuration**:
- PTH_PERCENTILE: 1.0
- TOL_DIFF_1: 0.01
- TOL_OBS_1: 0.1%
- TOL_DIFF_2: 1e-06
- INDEX_COLS: ['permno', 'yyyymm']

## Summary

| Predictor                 | Python CSV | Columns  | Superset  | Precision1   | Precision2              |
|---------------------------|------------|----------|-----------|--------------|-------------------------|
| FirmAgeMom                | ✅         | ✅       | ❌ (26.99%)  | ✅ (0.00%)    | ❌ (100th diff 1.0E-06)  |
| std_turn                  | ✅         | ✅       | ❌ (0.04%)   | ✅ (0.00%)    | ❌ (100th diff 1.9E-05)  |
| RDcap                     | ✅         | ✅       | ✅           | ✅ (0.00%)    | ❌ (100th diff 1.3E-06)  |
| GrAdExp                   | ✅         | ✅       | ✅           | ✅ (0.00%)    | ✅ (100th diff 2.7E-07)  |

**Overall**: 1/4 available predictors passed validation
**Python CSVs**: 4/4 predictors have Python implementation

## Detailed Results

### FirmAgeMom

**Status**: ❌ FAILED

**Test Results**:
- Test 1 - Column names: ✅ PASSED
- Test 2 - Superset check: ❌ FAILED (Python missing 148535 Stata observations)
- Test 3 - Precision1 check: ✅ PASSED
- Test 4 - Precision2 check: ❌ FAILED

**Columns**: ['FirmAgeMom']

**Observations**:
- Stata:  550,434
- Python: 440,809
- Common: 401,899

**Precision1**: 0.000% obs with std_diff >= 1.00e-02 (tolerance: < 0.1%)

**Precision2**: 100th percentile diff = 1.04e-06 (tolerance: < 1.00e-06)

**Missing Observations Sample**:
```
 index  permno  yyyymm  FirmAgeMom
     0   10001  198805    0.057086
     1   10002  198805   -0.037038
     2   10003  198805    0.240245
     3   10006  192804    0.100632
     4   10006  192805    0.037833
     5   10006  192806   -0.065188
     6   10006  192807   -0.101982
     7   10006  192808   -0.125491
     8   10006  192809   -0.099370
     9   10006  192810   -0.058148
```

**Feedback**:
- Num observations with std_diff >= TOL_DIFF_1: 0/401899 (0.000%)
- Stata standard deviation: 3.76e-01

---

### GrAdExp

**Status**: ✅ PASSED

**Test Results**:
- Test 1 - Column names: ✅ PASSED
- Test 2 - Superset check: ✅ PASSED
- Test 3 - Precision1 check: ✅ PASSED
- Test 4 - Precision2 check: ✅ PASSED

**Columns**: ['GrAdExp']

**Observations**:
- Stata:  898,855
- Python: 905,831
- Common: 898,855

**Precision1**: 0.000% obs with std_diff >= 1.00e-02 (tolerance: < 0.1%)

**Precision2**: 100th percentile diff = 2.71e-07 (tolerance: < 1.00e-06)

**Feedback**:
- Num observations with std_diff >= TOL_DIFF_1: 0/898855 (0.000%)
- Stata standard deviation: 4.75e-01

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

