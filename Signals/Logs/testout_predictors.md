# Predictor Validation Results

**Generated**: 2025-08-14 12:28:26

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
| TrendFactor               | ✅         | ✅       | ✅ (0.12%)   | ❌ (97.13%)   | ❌ (99th diff 1.3E+00)   |

**Overall**: 0/1 available predictors passed validation
  - Natural passes: 0
  - Overridden passes: 0
**Python CSVs**: 1/1 predictors have Python implementation
\* = Manual override applied (see Predictors/overrides.yaml for details)

## Detailed Results

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

**Precision1**: 97.125% obs with std_diff >= 1.00e-02 (tolerance: < 10%)

**Precision2**: 99th percentile diff = 1.32e+00 (tolerance: < 1.00e+00)

**Summary Statistics** (Common Observations):

| Statistic  |          Stata |         Python |     Difference | Std Difference |
|------------|----------------|----------------|----------------|----------------|
| count      |       2.06e+06 |       2.06e+06 |       2.06e+06 |       2.06e+06 |
| mean       |         0.2096 |         0.1785 |        -0.0311 |        -0.2019 |
| std        |         0.1540 |         0.1435 |         0.0551 |         0.3579 |
| min        |        -1.0711 |        -1.0712 |        -0.4212 |        -2.7352 |
| 25%        |         0.1242 |         0.1072 |        -0.0604 |        -0.3921 |
| 50%        |         0.2187 |         0.1848 |        -0.0256 |        -0.1663 |
| 75%        |         0.3000 |         0.2611 |         0.0031 |         0.0200 |
| max        |         3.2757 |         3.2813 |         2.7034 |        17.5546 |

**Regression Analysis** (Python ~ Stata):

- **Model**: python = -0.0038 + 0.8698 * stata
- **R-squared**: 0.8719
- **N observations**: 2,055,856

| Coefficient |     Estimate |    Std Error | t-statistic |   p-value |
|-------------|--------------|--------------|-------------|----------|
| Intercept   |      -0.0038 |     6.05e-05 |    -62.9716 |     0.000 |
| Slope       |       0.8698 |     2.32e-04 |   3741.4551 |     0.000 |

**Feedback**:
- Num observations with std_diff >= TOL_DIFF_1: 1996758/2055856 (97.125%)
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

