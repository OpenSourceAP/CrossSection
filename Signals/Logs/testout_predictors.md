# Predictor Validation Results

**Generated**: 2025-08-13 17:48:31

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
| RDAbility                 | ✅         | ✅       | ❌ (1.43%)   | ❌ (10.38%)   | ✅ (99th diff 9.4E-01)   |

**Overall**: 0/1 available predictors passed validation
  - Natural passes: 0
  - Overridden passes: 0
**Python CSVs**: 1/1 predictors have Python implementation
\* = Manual override applied (see Predictors/overrides.yaml for details)

## Detailed Results

### RDAbility

**Status**: ❌ FAILED

**Test Results**:
- Test 1 - Column names: ✅ PASSED
- Test 2 - Superset check: ❌ FAILED (Python missing 2474 Stata observations)
- Test 3 - Precision1 check: ❌ FAILED
- Test 4 - Precision2 check: ✅ PASSED

**Columns**: ['RDAbility']

**Observations**:
- Stata:  173,266
- Python: 186,735
- Common: 170,792

**Precision1**: 10.378% obs with std_diff >= 1.00e-02 (tolerance: < 10%)

**Precision2**: 99th percentile diff = 9.36e-01 (tolerance: < 1.00e+00)

**Summary Statistics** (Common Observations):

| Statistic  |          Stata |         Python |     Difference | Std Difference |
|------------|----------------|----------------|----------------|----------------|
| count      |    170792.0000 |    170792.0000 |    170792.0000 |    170792.0000 |
| mean       |         0.4665 |         0.4237 |        -0.0428 |        -0.0080 |
| std        |         5.3811 |         5.7735 |         2.5914 |         0.4816 |
| min        |      -170.7315 |      -184.0284 |      -192.6819 |       -35.8070 |
| 25%        |        -0.3170 |        -0.3265 |      -2.25e-07 |      -4.18e-08 |
| 50%        |         0.4038 |         0.3761 |      -1.85e-09 |      -3.44e-10 |
| 75%        |         1.4004 |         1.3577 |       1.72e-07 |       3.20e-08 |
| max        |        83.8592 |       121.3608 |       120.7873 |        22.4465 |

**Regression Analysis** (Python ~ Stata):

- **Model**: python = -0.0240 + 0.9596 * stata
- **R-squared**: 0.7999
- **N observations**: 170,792

| Coefficient |     Estimate |    Std Error | t-statistic |   p-value |
|-------------|--------------|--------------|-------------|----------|
| Intercept   |      -0.0240 |       0.0063 |     -3.8242 |     0.000 |
| Slope       |       0.9596 |       0.0012 |    826.4031 |     0.000 |

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
- Num observations with std_diff >= TOL_DIFF_1: 17724/170792 (10.378%)
- Stata standard deviation: 5.38e+00

**Most Recent Bad Observations**:
```
   permno  yyyymm    python     stata      diff
0   16968  202606  2.676225  4.362977 -1.686752
1   13159  202605  0.510686  0.628990 -0.118303
2   13918  202605  0.010309  0.838733 -0.828424
3   14051  202605  0.131522  0.408131 -0.276609
4   14245  202605  0.864758  0.997209 -0.132450
5   14272  202605  0.272244  0.369297 -0.097053
6   14432  202605  0.768600  0.448311  0.320289
7   14436  202605  0.224077  0.334133 -0.110056
8   14551  202605  0.181759  0.240248 -0.058489
9   14556  202605  0.203567  0.303276 -0.099709
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

