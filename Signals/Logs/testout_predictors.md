# Predictor Validation Results

**Generated**: 2025-08-21 22:09:13

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
| DivSeason                 | ✅         | ✅       | ✅ (0.00%)   | ✅ (0.78%)    | ❌ (99.900th diff 2.0E+00) |

**Overall**: 0/1 available predictors passed validation
  - Natural passes: 0
  - Overridden passes: 0
**Python CSVs**: 1/1 predictors have Python implementation
\* = Manual override applied (see Predictors/overrides.yaml for details)

## Detailed Results

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
- Python: 1,775,674
- Common: 1,775,335

**Precision1**: 0.782% obs with std_diff >= 1.00e-02 (tolerance: < 1%)

**Precision2**: 100th percentile diff = 2.01e+00 (tolerance: < 1.00e-01)

**Summary Statistics** (Common Observations):

| Statistic  |          Stata |         Python |     Difference | Std Difference |
|------------|----------------|----------------|----------------|----------------|
| count      |       1.78e+06 |       1.78e+06 |       1.78e+06 |       1.78e+06 |
| mean       |         0.4456 |         0.4379 |        -0.0077 |        -0.0155 |
| std        |         0.4970 |         0.4961 |         0.0881 |         0.1773 |
| min        |         0.0000 |         0.0000 |        -1.0000 |        -2.0120 |
| 25%        |         0.0000 |         0.0000 |         0.0000 |         0.0000 |
| 50%        |         0.0000 |         0.0000 |         0.0000 |         0.0000 |
| 75%        |         1.0000 |         1.0000 |         0.0000 |         0.0000 |
| max        |         1.0000 |         1.0000 |         1.0000 |         2.0120 |

**Regression Analysis** (Python ~ Stata):

- **Model**: python = 0.0001 + 0.9825 * stata
- **R-squared**: 0.9688
- **N observations**: 1,775,335

| Coefficient |     Estimate |    Std Error | t-statistic |   p-value |
|-------------|--------------|--------------|-------------|----------|
| Intercept   |     1.01e-04 |     8.84e-05 |      1.1381 |     0.255 |
| Slope       |       0.9825 |     1.32e-04 |   7420.5350 |     0.000 |

**Feedback**:
- Num observations with std_diff >= TOL_DIFF_1: 13889/1775335 (0.782%)
- Stata standard deviation: 4.97e-01

**Most Recent Bad Observations**:
```
   permno  yyyymm  python  stata  diff
0   16611  202412       0      1    -1
1   21372  202412       0      1    -1
2   22515  202412       0      1    -1
3   32791  202412       0      1    -1
4   79033  202412       0      1    -1
5   81134  202412       0      1    -1
6   84411  202412       0      1    -1
7   86578  202412       0      1    -1
8   89597  202412       0      1    -1
9   89857  202412       0      1    -1
```

**Largest Differences**:
```
   permno  yyyymm  python  stata  diff
0   10001  201601       0      1    -1
1   10001  201604       0      1    -1
2   10002  199707       0      1    -1
3   10002  199710       0      1    -1
4   10002  199801       0      1    -1
5   10002  199804       0      1    -1
6   10014  193501       0      1    -1
7   10014  193504       0      1    -1
8   10014  193507       0      1    -1
9   10014  193510       0      1    -1
```

**Largest Differences Before 1950**:
```
   permno  yyyymm  python  stata  diff
0   10014  193501       0      1    -1
1   10014  193504       0      1    -1
2   10014  193507       0      1    -1
3   10014  193510       0      1    -1
4   10014  193511       0      1    -1
5   10022  194304       0      1    -1
6   10022  194307       0      1    -1
7   10022  194310       0      1    -1
8   10022  194401       0      1    -1
9   10022  194402       0      1    -1
```

---

