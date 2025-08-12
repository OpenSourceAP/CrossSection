# Predictor Validation Results

**Generated**: 2025-08-12 14:12:23

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
| IndRetBig                 | ✅         | ✅       | ✅ (0.04%)   | ❌ (25.49%)   | ❌ (99th diff 1.8E-02)   |

**Overall**: 0/1 available predictors passed validation
**Python CSVs**: 1/1 predictors have Python implementation

## Detailed Results

### IndRetBig

**Status**: ❌ FAILED

**Test Results**:
- Test 1 - Column names: ✅ PASSED
- Test 2 - Superset check: ✅ PASSED
- Test 3 - Precision1 check: ❌ FAILED
- Test 4 - Precision2 check: ❌ FAILED

**Columns**: ['IndRetBig']

**Observations**:
- Stata:  2,607,795
- Python: 2,835,108
- Common: 2,606,748

**Precision1**: 25.494% obs with std_diff >= 1.00e-02 (tolerance: < 10%)

**Precision2**: 99th percentile diff = 1.83e-02 (tolerance: < 1.00e-03)

**Feedback**:
- Num observations with std_diff >= TOL_DIFF_1: 664574/2606748 (25.494%)
- Stata standard deviation: 7.04e-02

**Most Recent Bad Observations**:
```
   permno  yyyymm    python     stata      diff
0   10066  202412 -0.037555 -0.040106  0.002551
1   10158  202412 -0.143372 -0.146776  0.003404
2   10253  202412 -0.037555 -0.040106  0.002551
3   10318  202412 -0.084162 -0.088794  0.004632
4   10547  202412 -0.029300 -0.024732 -0.004568
5   10550  202412 -0.084474 -0.078000 -0.006474
6   10866  202412 -0.042621 -0.043805  0.001184
7   10890  202412 -0.037555 -0.040106  0.002551
8   11144  202412 -0.084162 -0.088794  0.004632
9   11267  202412 -0.042621 -0.043805  0.001184
```

**Largest Differences**:
```
   permno  yyyymm    python     stata      diff
0   11332  193909  1.103858  1.883087 -0.779228
1   11797  193909  1.103858  1.883087 -0.779228
2   13872  193909  1.103858  1.883087 -0.779228
3   15173  193909  1.103858  1.883087 -0.779228
4   17398  193909  1.103858  1.883087 -0.779228
5   18833  193909  1.103858  1.883087 -0.779228
6   20028  193909  1.103858  1.883087 -0.779228
7   20044  193909  1.103858  1.883087 -0.779228
8   75471  193909  1.103858  1.883087 -0.779228
9   10647  193209  0.107323  0.642977 -0.535654
```

---

