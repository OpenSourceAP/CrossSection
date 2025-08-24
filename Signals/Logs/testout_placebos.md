# Placebo Validation Results

**Generated**: 2025-08-24 00:43:02

**Configuration**:
- TOL_SUPERSET: 0.0%
- TOL_DIFF_1: 0.01
- TOL_OBS_1: 10%
- EXTREME_Q: 0.99
- TOL_DIFF_2: 1.0
- INDEX_COLS: ['permno', 'yyyymm']

## Summary

| Placebo                   | Python CSV | Columns  | Superset  | Precision1   | Precision2              |
|---------------------------|------------|----------|-----------|--------------|-------------------------|
| fgr5yrNoLag               | ✅         | ✅       | ❌ (0.21%)   | ✅ (0.08%)    | ✅ (99th diff 1.4E-07)   |
| DivYield                  | ✅         | ✅       | ❌ (0.01%)   | ✅ (0.00%)    | ✅ (99th diff 1.2E-08)   |
| pchquick                  | ✅         | ✅       | ❌ (0.01%)   | ✅ (0.24%)    | ✅ (99th diff 2.8E-09)   |
| cfpq                      | ✅         | ✅       | ❌ (0.00%)   | ✅ (0.02%)    | ✅ (99th diff 3.7E-08)   |
| EPq                       | ✅         | ✅       | ❌ (0.00%)   | ✅ (0.74%)    | ✅ (99th diff 2.9E-03)   |
| RD_q                      | ✅         | ✅       | ❌ (0.00%)   | ✅ (0.00%)    | ✅ (99th diff 5.2E-08)   |
| rd_sale_q                 | ✅         | ✅       | ❌ (0.00%)   | ✅ (0.00%)    | ✅ (99th diff 6.7E-09)   |
| NetDebtPrice_q            | ✅         | ✅       | ❌ (0.00%)   | ✅ (0.00%)    | ✅ (99th diff 4.8E-08)   |
| PayoutYield_q             | ✅         | ✅       | ❌ (0.00%)   | ✅ (0.01%)    | ✅ (99th diff 3.4E-08)   |
| ChangeRoE                 | ✅         | ✅       | ❌ (0.00%)   | ✅ (0.00%)    | ✅ (99th diff 3.2E-09)   |
| RetNOA_q                  | ✅         | ✅       | ❌ (0.00%)   | ✅ (0.00%)    | ✅ (99th diff 3.8E-11)   |
| ChangeRoA                 | ✅         | ✅       | ❌ (0.00%)   | ✅ (0.01%)    | ✅ (99th diff 6.6E-08)   |
| Tax_q                     | ✅         | ✅       | ❌ (0.00%)   | ✅ (0.00%)    | ✅ (99th diff 8.6E-09)   |
| Leverage_q                | ✅         | ✅       | ❌ (0.00%)   | ✅ (0.00%)    | ✅ (99th diff 4.5E-08)   |
| OPLeverage_q              | ✅         | ✅       | ❌ (0.00%)   | ✅ (0.01%)    | ✅ (99th diff 7.7E-08)   |
| EBM_q                     | ✅         | ✅       | ❌ (0.00%)   | ✅ (0.00%)    | ✅ (99th diff 3.4E-08)   |
| AssetGrowth_q             | ✅         | ✅       | ❌ (0.00%)   | ✅ (0.00%)    | ✅ (99th diff 1.9E-08)   |
| AssetLiquidityMarketQuart | ✅         | ✅       | ❌ (0.00%)   | ✅ (0.00%)    | ✅ (99th diff 1.5E-07)   |
| CapTurnover_q             | ✅         | ✅       | ❌ (0.00%)   | ✅ (0.00%)    | ✅ (99th diff 1.0E-08)   |
| CBOperProfLagAT_q         | ✅         | ✅       | ❌ (0.00%)   | ✅ (0.02%)    | ✅ (99th diff 8.5E-08)   |
| PM_q                      | ✅         | ✅       | ❌ (0.00%)   | ✅ (0.00%)    | ✅ (99th diff 2.9E-09)   |
| AssetLiquidityBookQuart   | ✅         | ✅       | ❌ (0.00%)   | ✅ (0.00%)    | ✅ (99th diff 2.4E-08)   |
| SP_q                      | ✅         | ✅       | ❌ (0.00%)   | ✅ (0.00%)    | ✅ (99th diff 8.0E-08)   |
| CFq                       | ✅         | ✅       | ❌ (0.00%)   | ✅ (0.01%)    | ✅ (99th diff 1.5E-08)   |
| AssetTurnover             | ✅         | ✅       | ❌ (0.00%)   | ✅ (0.00%)    | ✅ (99th diff 3.9E-09)   |
| pchdepr                   | ✅         | ✅       | ❌ (0.00%)   | ✅ (0.00%)    | ✅ (99th diff 2.3E-09)   |
| AssetTurnover_q           | ✅         | ✅       | ❌ (0.00%)   | ✅ (0.00%)    | ✅ (99th diff 5.5E-09)   |
| EntMult_q                 | ✅         | ✅       | ❌ (0.00%)   | ✅ (0.00%)    | ✅ (99th diff 4.7E-09)   |
| depr                      | ✅         | ✅       | ❌ (0.00%)   | ✅ (0.00%)    | ✅ (99th diff 8.7E-09)   |
| sgr_q                     | ✅         | ✅       | ❌ (0.00%)   | ✅ (0.00%)    | ✅ (99th diff 3.0E-10)   |
| tang_q                    | ✅         | ✅       | ❌ (0.00%)   | ✅ (0.01%)    | ✅ (99th diff 1.5E-07)   |
| DivYieldAnn               | ✅         | ✅       | ✅ (0.00%)   | ✅ (0.03%)    | ✅ (99th diff 2.1E-08)   |
| NetPayoutYield_q          | ✅         | ✅       | ✅ (0.00%)   | ✅ (0.02%)    | ✅ (99th diff 3.5E-08)   |
| roic                      | ✅         | ✅       | ✅ (0.00%)   | ✅ (0.01%)    | ✅ (99th diff 3.4E-23)   |
| EarningsSmoothness        | ✅         | ✅       | ✅ (0.00%)   | ✅ (0.00%)    | ✅ (99th diff 3.1E-07)   |
| salerec                   | ✅         | ✅       | ✅ (0.00%)   | ✅ (0.00%)    | ✅ (99th diff 2.1E-08)   |
| secured                   | ✅         | ✅       | ✅ (0.00%)   | ✅ (0.00%)    | ✅ (99th diff 8.4E-08)   |
| securedind                | ✅         | ✅       | ✅ (0.00%)   | ✅ (0.00%)    | ✅ (99th diff 0.0E+00)   |
| CBOperProfLagAT           | ✅         | ✅       | ✅ (0.00%)   | ✅ (0.00%)    | ✅ (99th diff 6.6E-08)   |
| ChNCOL                    | ✅         | ✅       | ✅ (0.00%)   | ✅ (0.00%)    | ✅ (99th diff 5.8E-08)   |
| DelSTI                    | ✅         | ✅       | ✅ (0.00%)   | ✅ (0.00%)    | ✅ (99th diff 2.0E-07)   |
| ZScore_q                  | ✅         | ✅       | ✅ (0.00%)   | ✅ (0.00%)    | ✅ (99th diff 7.2E-08)   |
| BMq                       | ✅         | ✅       | ✅ (0.00%)   | ✅ (0.00%)    | ✅ (99th diff 1.2E-07)   |
| ChNCOA                    | ✅         | ✅       | ✅ (0.00%)   | ✅ (0.00%)    | ✅ (99th diff 8.5E-08)   |
| AssetLiquidityMarket      | ✅         | ✅       | ✅ (0.00%)   | ✅ (0.00%)    | ✅ (99th diff 1.7E-07)   |
| AssetLiquidityBook        | ✅         | ✅       | ✅ (0.00%)   | ✅ (0.00%)    | ✅ (99th diff 8.5E-08)   |
| ETR                       | ✅         | ✅       | ✅ (0.00%)   | ✅ (0.00%)    | ✅ (99th diff 6.2E-12)   |
| sgr                       | ✅         | ✅       | ✅ (0.00%)   | ✅ (0.00%)    | ✅ (99th diff 1.9E-09)   |
| BookLeverageQuarterly     | ✅         | ✅       | ✅ (0.00%)   | ✅ (0.00%)    | ✅ (99th diff 4.1E-13)   |
| AMq                       | ✅         | ✅       | ✅ (0.00%)   | ✅ (0.00%)    | ✅ (99th diff 3.9E-08)   |
| LaborforceEfficiency      | ✅         | ✅       | ✅ (0.00%)   | ✅ (0.00%)    | ✅ (99th diff 4.3E-09)   |
| CapTurnover               | ✅         | ✅       | ✅ (0.00%)   | ✅ (0.00%)    | ✅ (99th diff 8.5E-08)   |
| salecash                  | ✅         | ✅       | ✅ (0.00%)   | ✅ (0.00%)    | ✅ (99th diff 6.5E-09)   |
| ZScore                    | ✅         | ✅       | ✅ (0.00%)   | ✅ (0.00%)    | ✅ (99th diff 8.3E-08)   |
| quick                     | ✅         | ✅       | ✅ (0.00%)   | ✅ (0.00%)    | ✅ (99th diff 1.1E-08)   |
| rd_sale                   | ✅         | ✅       | ✅ (0.00%)   | ✅ (0.00%)    | ✅ (99th diff 4.1E-09)   |
| cashdebt                  | ✅         | ✅       | ✅ (0.00%)   | ✅ (0.00%)    | ✅ (99th diff 3.2E-09)   |
| saleinv                   | ✅         | ✅       | ✅ (0.00%)   | ✅ (0.00%)    | ✅ (99th diff 3.1E-09)   |
| AbnormalAccrualsPercent   | ❌         | NA      | NA          | NA           | NA                      |
| AccrualQuality            | ❌         | NA      | NA          | NA           | NA                      |
| AccrualQualityJune        | ❌         | NA      | NA          | NA           | NA                      |
| BetaBDLeverage            | ❌         | NA      | NA          | NA           | NA                      |
| BetaDimson                | ❌         | NA      | NA          | NA           | NA                      |
| BetaSquared               | ❌         | NA      | NA          | NA           | NA                      |
| BidAskTAQ                 | ❌         | NA      | NA          | NA           | NA                      |
| BrandCapital              | ❌         | NA      | NA          | NA           | NA                      |
| ChPM                      | ❌         | NA      | NA          | NA           | NA                      |
| DelayAcct                 | ❌         | NA      | NA          | NA           | NA                      |
| DelayNonAcct              | ❌         | NA      | NA          | NA           | NA                      |
| DownsideBeta              | ❌         | NA      | NA          | NA           | NA                      |
| EarningsConservatism      | ❌         | NA      | NA          | NA           | NA                      |
| EarningsPersistence       | ❌         | NA      | NA          | NA           | NA                      |
| EarningsPredictability    | ❌         | NA      | NA          | NA           | NA                      |
| EarningsTimeliness        | ❌         | NA      | NA          | NA           | NA                      |
| EarningsValueRelevance    | ❌         | NA      | NA          | NA           | NA                      |
| FRbook                    | ❌         | NA      | NA          | NA           | NA                      |
| FailureProbability        | ❌         | NA      | NA          | NA           | NA                      |
| FailureProbabilityJune    | ❌         | NA      | NA          | NA           | NA                      |
| ForecastDispersionLT      | ❌         | NA      | NA          | NA           | NA                      |
| GPlag                     | ❌         | NA      | NA          | NA           | NA                      |
| GPlag_q                   | ❌         | NA      | NA          | NA           | NA                      |
| GrGMToGrSales             | ❌         | NA      | NA          | NA           | NA                      |
| GrSaleToGrReceivables     | ❌         | NA      | NA          | NA           | NA                      |
| IdioVolCAPM               | ❌         | NA      | NA          | NA           | NA                      |
| IdioVolQF                 | ❌         | NA      | NA          | NA           | NA                      |
| IntrinsicValue            | ❌         | NA      | NA          | NA           | NA                      |
| KZ                        | ❌         | NA      | NA          | NA           | NA                      |
| KZ_q                      | ❌         | NA      | NA          | NA           | NA                      |
| OScore_q                  | ❌         | NA      | NA          | NA           | NA                      |
| OperProfLag               | ❌         | NA      | NA          | NA           | NA                      |
| OperProfLag_q             | ❌         | NA      | NA          | NA           | NA                      |
| OperProfRDLagAT           | ❌         | NA      | NA          | NA           | NA                      |
| OperProfRDLagAT_q         | ❌         | NA      | NA          | NA           | NA                      |
| OrgCapNoAdj               | ❌         | NA      | NA          | NA           | NA                      |
| PM                        | ❌         | NA      | NA          | NA           | NA                      |
| PS_q                      | ❌         | NA      | NA          | NA           | NA                      |
| ResidualMomentum6m        | ❌         | NA      | NA          | NA           | NA                      |
| RetNOA                    | ❌         | NA      | NA          | NA           | NA                      |
| ReturnSkewCAPM            | ❌         | NA      | NA          | NA           | NA                      |
| ReturnSkewQF              | ❌         | NA      | NA          | NA           | NA                      |
| WW                        | ❌         | NA      | NA          | NA           | NA                      |
| WW_Q                      | ❌         | NA      | NA          | NA           | NA                      |
| betaCC                    | ❌         | NA      | NA          | NA           | NA                      |
| betaCR                    | ❌         | NA      | NA          | NA           | NA                      |
| betaNet                   | ❌         | NA      | NA          | NA           | NA                      |
| betaRC                    | ❌         | NA      | NA          | NA           | NA                      |
| betaRR                    | ❌         | NA      | NA          | NA           | NA                      |
| currat                    | ❌         | NA      | NA          | NA           | NA                      |
| grcapx1y                  | ❌         | NA      | NA          | NA           | NA                      |
| nanalyst                  | ❌         | NA      | NA          | NA           | NA                      |
| pchcurrat                 | ❌         | NA      | NA          | NA           | NA                      |
| pchgm_pchsale             | ❌         | NA      | NA          | NA           | NA                      |
| pchsaleinv                | ❌         | NA      | NA          | NA           | NA                      |
| roavol                    | ❌         | NA      | NA          | NA           | NA                      |

**Overall**: 27/58 available placebos passed validation
**Python CSVs**: 58/114 placebos have Python implementation

## Detailed Results

### AMq

**Status**: ✅ PASSED

**Test Results**:
- Test 1 - Column names: ✅ PASSED
- Test 2 - Superset check: ✅ PASSED
- Test 3 - Precision1 check: ✅ PASSED
- Test 4 - Precision2 check: ✅ PASSED

**Columns**: ['AMq']

**Observations**:
- Stata:  2,584,378
- Python: 2,669,375
- Common: 2,584,378

**Precision1**: 0.001% obs with std_diff >= 1.00e-02 (tolerance: < 10%)

**Precision2**: 99th percentile diff = 3.92e-08 (tolerance: < 1.00e+00)

**Summary Statistics** (Common Observations):

| Statistic  |          Stata |         Python |     Difference | Std Difference |
|------------|----------------|----------------|----------------|----------------|
| count      |       2.58e+06 |       2.58e+06 |       2.58e+06 |       2.58e+06 |
| mean       |         3.7379 |         3.7379 |      -1.45e-05 |      -6.23e-07 |
| std        |        23.2695 |        23.2695 |         0.0149 |       6.42e-04 |
| min        |       -33.6391 |       -33.6391 |       -14.6042 |        -0.6276 |
| 25%        |         0.6615 |         0.6615 |      -2.52e-08 |      -1.08e-09 |
| 50%        |         1.4017 |         1.4017 |       9.63e-12 |       4.14e-13 |
| 75%        |         3.2088 |         3.2087 |       2.53e-08 |       1.09e-09 |
| max        |     11549.4230 |     11549.4229 |         3.4533 |         0.1484 |

**Regression Analysis** (Python ~ Stata):

- **Model**: python = -0.0000 + 1.0000 * stata
- **R-squared**: 1.0000
- **N observations**: 2,584,378

| Coefficient |     Estimate |    Std Error | t-statistic |   p-value |
|-------------|--------------|--------------|-------------|----------|
| Intercept   |    -1.33e-05 |     9.42e-06 |     -1.4108 |     0.158 |
| Slope       |       1.0000 |     4.00e-07 |    2.50e+06 |     0.000 |

**Feedback**:
- Num observations with std_diff >= TOL_DIFF_1: 13/2584378 (0.001%)
- Stata standard deviation: 2.33e+01

---

### AssetGrowth_q

**Status**: ❌ FAILED

**Test Results**:
- Test 1 - Column names: ✅ PASSED
- Test 2 - Superset check: ❌ FAILED (Python missing 49 Stata observations)
- Test 3 - Precision1 check: ✅ PASSED
- Test 4 - Precision2 check: ✅ PASSED

**Columns**: ['AssetGrowth_q']

**Observations**:
- Stata:  2,303,961
- Python: 2,303,943
- Common: 2,303,912

**Precision1**: 0.002% obs with std_diff >= 1.00e-02 (tolerance: < 10%)

**Precision2**: 99th percentile diff = 1.89e-08 (tolerance: < 1.00e+00)

**Summary Statistics** (Common Observations):

| Statistic  |          Stata |         Python |     Difference | Std Difference |
|------------|----------------|----------------|----------------|----------------|
| count      |       2.30e+06 |       2.30e+06 |       2.30e+06 |       2.30e+06 |
| mean       |         0.1633 |         0.1633 |       2.84e-07 |       8.09e-08 |
| std        |         3.5114 |         3.5114 |         0.0207 |         0.0059 |
| min        |        -1.0268 |        -1.0268 |       -12.3040 |        -3.5040 |
| 25%        |        -0.0283 |        -0.0283 |      -2.02e-09 |      -5.74e-10 |
| 50%        |         0.0624 |         0.0624 |      -8.09e-13 |      -2.30e-13 |
| 75%        |         0.1821 |         0.1821 |       2.01e-09 |       5.72e-10 |
| max        |      2788.4187 |      2788.4186 |        13.1749 |         3.7521 |

**Regression Analysis** (Python ~ Stata):

- **Model**: python = 0.0000 + 1.0000 * stata
- **R-squared**: 1.0000
- **N observations**: 2,303,912

| Coefficient |     Estimate |    Std Error | t-statistic |   p-value |
|-------------|--------------|--------------|-------------|----------|
| Intercept   |     2.92e-06 |     1.37e-05 |      0.2141 |     0.830 |
| Slope       |       1.0000 |     3.88e-06 | 257423.5890 |     0.000 |

**Missing Observations Sample**:
```
 index  permno  yyyymm  AssetGrowth_q
     0   10515  199604       0.039085
     1   10515  199605       0.039085
     2   10515  199606       0.039085
     3   10515  199704      -0.161325
     4   10515  199705      -0.161325
     5   10515  199706      -0.161325
     6   11545  199706       1.051804
     7   11545  199707       1.051804
     8   11545  199708       1.051804
     9   11545  199806       0.729125
```

**Feedback**:
- Num observations with std_diff >= TOL_DIFF_1: 36/2303912 (0.002%)
- Stata standard deviation: 3.51e+00

---

### AssetLiquidityBook

**Status**: ✅ PASSED

**Test Results**:
- Test 1 - Column names: ✅ PASSED
- Test 2 - Superset check: ✅ PASSED
- Test 3 - Precision1 check: ✅ PASSED
- Test 4 - Precision2 check: ✅ PASSED

**Columns**: ['AssetLiquidityBook']

**Observations**:
- Stata:  3,595,932
- Python: 3,596,807
- Common: 3,595,932

**Precision1**: 0.001% obs with std_diff >= 1.00e-02 (tolerance: < 10%)

**Precision2**: 99th percentile diff = 8.48e-08 (tolerance: < 1.00e+00)

**Summary Statistics** (Common Observations):

| Statistic  |          Stata |         Python |     Difference | Std Difference |
|------------|----------------|----------------|----------------|----------------|
| count      |       3.60e+06 |       3.60e+06 |       3.60e+06 |       3.60e+06 |
| mean       |         0.5929 |         0.5929 |      -5.19e-07 |      -1.35e-06 |
| std        |         0.3840 |         0.3840 |       3.14e-04 |       8.19e-04 |
| min        |       -11.5597 |       -11.5597 |        -0.1662 |        -0.4329 |
| 25%        |         0.5072 |         0.5072 |      -1.24e-08 |      -3.22e-08 |
| 50%        |         0.5933 |         0.5933 |         0.0000 |         0.0000 |
| 75%        |         0.6967 |         0.6967 |       1.23e-08 |       3.20e-08 |
| max        |       491.6170 |       491.6170 |         0.0941 |         0.2450 |

**Regression Analysis** (Python ~ Stata):

- **Model**: python = -0.0000 + 1.0000 * stata
- **R-squared**: 1.0000
- **N observations**: 3,595,932

| Coefficient |     Estimate |    Std Error | t-statistic |   p-value |
|-------------|--------------|--------------|-------------|----------|
| Intercept   |    -7.59e-07 |     3.05e-07 |     -2.4882 |     0.013 |
| Slope       |       1.0000 |     4.32e-07 |    2.32e+06 |     0.000 |

**Feedback**:
- Num observations with std_diff >= TOL_DIFF_1: 49/3595932 (0.001%)
- Stata standard deviation: 3.84e-01

---

### AssetLiquidityBookQuart

**Status**: ❌ FAILED

**Test Results**:
- Test 1 - Column names: ✅ PASSED
- Test 2 - Superset check: ❌ FAILED (Python missing 44 Stata observations)
- Test 3 - Precision1 check: ✅ PASSED
- Test 4 - Precision2 check: ✅ PASSED

**Columns**: ['AssetLiquidityBookQuart']

**Observations**:
- Stata:  2,538,807
- Python: 2,538,801
- Common: 2,538,763

**Precision1**: 0.003% obs with std_diff >= 1.00e-02 (tolerance: < 10%)

**Precision2**: 99th percentile diff = 2.44e-08 (tolerance: < 1.00e+00)

**Summary Statistics** (Common Observations):

| Statistic  |          Stata |         Python |     Difference | Std Difference |
|------------|----------------|----------------|----------------|----------------|
| count      |       2.54e+06 |       2.54e+06 |       2.54e+06 |       2.54e+06 |
| mean       |         0.6036 |         0.6036 |       1.86e-06 |       1.38e-06 |
| std        |         1.3441 |         1.3441 |         0.0041 |         0.0030 |
| min        |       -10.8152 |       -10.8152 |        -0.9876 |        -0.7348 |
| 25%        |         0.5155 |         0.5155 |      -1.26e-08 |      -9.35e-09 |
| 50%        |         0.6075 |         0.6075 |         0.0000 |         0.0000 |
| 75%        |         0.7025 |         0.7025 |       1.25e-08 |       9.32e-09 |
| max        |      2003.3081 |      2003.3081 |         6.1525 |         4.5775 |

**Regression Analysis** (Python ~ Stata):

- **Model**: python = 0.0000 + 1.0000 * stata
- **R-squared**: 1.0000
- **N observations**: 2,538,763

| Coefficient |     Estimate |    Std Error | t-statistic |   p-value |
|-------------|--------------|--------------|-------------|----------|
| Intercept   |     2.15e-06 |     2.79e-06 |      0.7683 |     0.442 |
| Slope       |       1.0000 |     1.90e-06 | 527351.3128 |     0.000 |

**Missing Observations Sample**:
```
 index  permno  yyyymm  AssetLiquidityBookQuart
     0   10515  199604                 0.816307
     1   10515  199605                 0.781849
     2   10515  199606                 0.781849
     3   11545  199706                 0.818928
     4   11545  199707                 0.777539
     5   11545  199708                 0.777539
     6   12750  198212                 0.666923
     7   12750  198301                 0.695176
     8   12750  198302                 0.695176
     9   12750  198303                 0.943752
```

**Feedback**:
- Num observations with std_diff >= TOL_DIFF_1: 67/2538763 (0.003%)
- Stata standard deviation: 1.34e+00

---

### AssetLiquidityMarket

**Status**: ✅ PASSED

**Test Results**:
- Test 1 - Column names: ✅ PASSED
- Test 2 - Superset check: ✅ PASSED
- Test 3 - Precision1 check: ✅ PASSED
- Test 4 - Precision2 check: ✅ PASSED

**Columns**: ['AssetLiquidityMarket']

**Observations**:
- Stata:  3,476,318
- Python: 3,477,044
- Common: 3,476,318

**Precision1**: 0.001% obs with std_diff >= 1.00e-02 (tolerance: < 10%)

**Precision2**: 99th percentile diff = 1.65e-07 (tolerance: < 1.00e+00)

**Summary Statistics** (Common Observations):

| Statistic  |          Stata |         Python |     Difference | Std Difference |
|------------|----------------|----------------|----------------|----------------|
| count      |       3.48e+06 |       3.48e+06 |       3.48e+06 |       3.48e+06 |
| mean       |         0.4488 |         0.4488 |      -4.78e-07 |      -1.71e-06 |
| std        |         0.2802 |         0.2802 |       1.49e-04 |       5.31e-04 |
| min        |        -7.2979 |        -7.2979 |        -0.0545 |        -0.1943 |
| 25%        |         0.2655 |         0.2655 |      -7.62e-09 |      -2.72e-08 |
| 50%        |         0.4442 |         0.4442 |       1.39e-17 |       4.95e-17 |
| 75%        |         0.5694 |         0.5694 |       7.63e-09 |       2.72e-08 |
| max        |        48.9168 |        48.9168 |         0.0013 |         0.0045 |

**Regression Analysis** (Python ~ Stata):

- **Model**: python = -0.0000 + 1.0000 * stata
- **R-squared**: 1.0000
- **N observations**: 3,476,318

| Coefficient |     Estimate |    Std Error | t-statistic |   p-value |
|-------------|--------------|--------------|-------------|----------|
| Intercept   |    -4.68e-07 |     1.51e-07 |     -3.1075 |     0.002 |
| Slope       |       1.0000 |     2.85e-07 |    3.51e+06 |     0.000 |

**Feedback**:
- Num observations with std_diff >= TOL_DIFF_1: 49/3476318 (0.001%)
- Stata standard deviation: 2.80e-01

---

### AssetLiquidityMarketQuart

**Status**: ❌ FAILED

**Test Results**:
- Test 1 - Column names: ✅ PASSED
- Test 2 - Superset check: ❌ FAILED (Python missing 50 Stata observations)
- Test 3 - Precision1 check: ✅ PASSED
- Test 4 - Precision2 check: ✅ PASSED

**Columns**: ['AssetLiquidityMarketQuart']

**Observations**:
- Stata:  2,503,163
- Python: 2,503,127
- Common: 2,503,113

**Precision1**: 0.003% obs with std_diff >= 1.00e-02 (tolerance: < 10%)

**Precision2**: 99th percentile diff = 1.49e-07 (tolerance: < 1.00e+00)

**Summary Statistics** (Common Observations):

| Statistic  |          Stata |         Python |     Difference | Std Difference |
|------------|----------------|----------------|----------------|----------------|
| count      |       2.50e+06 |       2.50e+06 |       2.50e+06 |       2.50e+06 |
| mean       |         0.4482 |         0.4482 |       1.58e-06 |       5.68e-06 |
| std        |         0.2781 |         0.2781 |         0.0036 |         0.0131 |
| min        |        -6.3541 |        -6.3541 |        -1.3938 |        -5.0125 |
| 25%        |         0.2725 |         0.2725 |      -7.72e-09 |      -2.78e-08 |
| 50%        |         0.4522 |         0.4522 |       6.28e-12 |       2.26e-11 |
| 75%        |         0.5664 |         0.5664 |       7.73e-09 |       2.78e-08 |
| max        |       137.3564 |       137.3564 |         5.3448 |        19.2216 |

**Regression Analysis** (Python ~ Stata):

- **Model**: python = 0.0000 + 1.0000 * stata
- **R-squared**: 0.9998
- **N observations**: 2,503,113

| Coefficient |     Estimate |    Std Error | t-statistic |   p-value |
|-------------|--------------|--------------|-------------|----------|
| Intercept   |     6.24e-06 |     4.37e-06 |      1.4266 |     0.154 |
| Slope       |       1.0000 |     8.29e-06 | 120625.5350 |     0.000 |

**Missing Observations Sample**:
```
 index  permno  yyyymm  AssetLiquidityMarketQuart
     0   10515  199604                   0.819677
     1   10515  199605                   0.833838
     2   10515  199606                   0.833838
     3   11545  199706                   0.363298
     4   11545  199707                   0.407572
     5   11545  199708                   0.407572
     6   12750  198212                   0.349204
     7   12750  198301                   0.398642
     8   12750  198302                   0.398642
     9   12750  198303                   0.541186
```

**Feedback**:
- Num observations with std_diff >= TOL_DIFF_1: 84/2503113 (0.003%)
- Stata standard deviation: 2.78e-01

---

### AssetTurnover

**Status**: ❌ FAILED

**Test Results**:
- Test 1 - Column names: ✅ PASSED
- Test 2 - Superset check: ❌ FAILED (Python missing 24 Stata observations)
- Test 3 - Precision1 check: ✅ PASSED
- Test 4 - Precision2 check: ✅ PASSED

**Columns**: ['AssetTurnover']

**Observations**:
- Stata:  2,796,921
- Python: 2,797,974
- Common: 2,796,897

**Precision1**: 0.001% obs with std_diff >= 1.00e-02 (tolerance: < 10%)

**Precision2**: 99th percentile diff = 3.94e-09 (tolerance: < 1.00e+00)

**Summary Statistics** (Common Observations):

| Statistic  |          Stata |         Python |     Difference | Std Difference |
|------------|----------------|----------------|----------------|----------------|
| count      |       2.80e+06 |       2.80e+06 |       2.80e+06 |       2.80e+06 |
| mean       |         5.2784 |         5.2786 |       1.87e-04 |       7.15e-07 |
| std        |       261.1058 |       261.1093 |         0.0658 |       2.52e-04 |
| min        |         0.0000 |        -0.0000 |        -1.8130 |        -0.0069 |
| 25%        |         0.9854 |         0.9854 |      -3.85e-08 |      -1.47e-10 |
| 50%        |         1.8726 |         1.8726 |         0.0000 |         0.0000 |
| 75%        |         3.0805 |         3.0805 |       3.86e-08 |       1.48e-10 |
| max        |    108845.1100 |    108847.6000 |        27.7236 |         0.1062 |

**Regression Analysis** (Python ~ Stata):

- **Model**: python = 0.0001 + 1.0000 * stata
- **R-squared**: 1.0000
- **N observations**: 2,796,897

| Coefficient |     Estimate |    Std Error | t-statistic |   p-value |
|-------------|--------------|--------------|-------------|----------|
| Intercept   |     1.15e-04 |     3.93e-05 |      2.9340 |     0.003 |
| Slope       |       1.0000 |     1.50e-07 |    6.65e+06 |     0.000 |

**Missing Observations Sample**:
```
 index  permno  yyyymm  AssetTurnover
     0   12373  202406       0.145598
     1   12373  202407       0.145598
     2   12373  202408       0.145598
     3   12373  202409       0.145598
     4   12373  202410       0.145598
     5   12373  202411       0.145598
     6   12373  202412       0.145598
     7   12373  202501       0.145598
     8   12373  202502       0.145598
     9   12373  202503       0.145598
```

**Feedback**:
- Num observations with std_diff >= TOL_DIFF_1: 24/2796897 (0.001%)
- Stata standard deviation: 2.61e+02

---

### AssetTurnover_q

**Status**: ❌ FAILED

**Test Results**:
- Test 1 - Column names: ✅ PASSED
- Test 2 - Superset check: ❌ FAILED (Python missing 14 Stata observations)
- Test 3 - Precision1 check: ✅ PASSED
- Test 4 - Precision2 check: ✅ PASSED

**Columns**: ['AssetTurnover_q']

**Observations**:
- Stata:  1,963,604
- Python: 2,066,032
- Common: 1,963,590

**Precision1**: 0.002% obs with std_diff >= 1.00e-02 (tolerance: < 10%)

**Precision2**: 99th percentile diff = 5.49e-09 (tolerance: < 1.00e+00)

**Summary Statistics** (Common Observations):

| Statistic  |          Stata |         Python |     Difference | Std Difference |
|------------|----------------|----------------|----------------|----------------|
| count      |       1.96e+06 |       1.96e+06 |       1.96e+06 |       1.96e+06 |
| mean       |         1.3789 |         1.3790 |       1.51e-05 |       2.73e-07 |
| std        |        55.1413 |        55.1402 |         0.0138 |       2.49e-04 |
| min        |         0.0000 |        -0.0000 |        -3.2387 |        -0.0587 |
| 25%        |         0.2551 |         0.2551 |      -1.00e-08 |      -1.81e-10 |
| 50%        |         0.5119 |         0.5119 |         0.0000 |         0.0000 |
| 75%        |         0.8749 |         0.8749 |       1.00e-08 |       1.82e-10 |
| max        |     27068.2270 |     27068.2000 |         7.8176 |         0.1418 |

**Regression Analysis** (Python ~ Stata):

- **Model**: python = 0.0000 + 1.0000 * stata
- **R-squared**: 1.0000
- **N observations**: 1,963,590

| Coefficient |     Estimate |    Std Error | t-statistic |   p-value |
|-------------|--------------|--------------|-------------|----------|
| Intercept   |     4.15e-05 |     9.79e-06 |      4.2395 |     0.000 |
| Slope       |       1.0000 |     1.77e-07 |    5.63e+06 |     0.000 |

**Missing Observations Sample**:
```
 index  permno  yyyymm  AssetTurnover_q
     0   23033  202406         0.594178
     1   23033  202407         0.594178
     2   23033  202408         0.594178
     3   23033  202409         4.538462
     4   23033  202410         4.538462
     5   23033  202411         4.538462
     6   88316  200212         0.000000
     7   88316  200301         0.000000
     8   88316  200302         0.000000
     9   88316  200304         0.000000
```

**Feedback**:
- Num observations with std_diff >= TOL_DIFF_1: 41/1963590 (0.002%)
- Stata standard deviation: 5.51e+01

---

### BMq

**Status**: ✅ PASSED

**Test Results**:
- Test 1 - Column names: ✅ PASSED
- Test 2 - Superset check: ✅ PASSED
- Test 3 - Precision1 check: ✅ PASSED
- Test 4 - Precision2 check: ✅ PASSED

**Columns**: ['BMq']

**Observations**:
- Stata:  2,568,885
- Python: 2,717,113
- Common: 2,568,885

**Precision1**: 0.003% obs with std_diff >= 1.00e-02 (tolerance: < 10%)

**Precision2**: 99th percentile diff = 1.24e-07 (tolerance: < 1.00e+00)

**Summary Statistics** (Common Observations):

| Statistic  |          Stata |         Python |     Difference | Std Difference |
|------------|----------------|----------------|----------------|----------------|
| count      |       2.57e+06 |       2.57e+06 |       2.57e+06 |       2.57e+06 |
| mean       |        -0.5919 |        -0.5919 |      -1.30e-06 |      -1.36e-06 |
| std        |         0.9608 |         0.9608 |         0.0015 |         0.0015 |
| min        |       -13.7467 |       -13.7467 |        -0.8206 |        -0.8540 |
| 25%        |        -1.1088 |        -1.1088 |      -1.09e-08 |      -1.13e-08 |
| 50%        |        -0.5062 |        -0.5062 |      -3.87e-12 |      -4.02e-12 |
| 75%        |         0.0109 |         0.0109 |       1.09e-08 |       1.13e-08 |
| max        |         6.6128 |         6.6128 |         0.7888 |         0.8210 |

**Regression Analysis** (Python ~ Stata):

- **Model**: python = -0.0000 + 1.0000 * stata
- **R-squared**: 1.0000
- **N observations**: 2,568,885

| Coefficient |     Estimate |    Std Error | t-statistic |   p-value |
|-------------|--------------|--------------|-------------|----------|
| Intercept   |    -1.73e-06 |     1.08e-06 |     -1.6040 |     0.109 |
| Slope       |       1.0000 |     9.58e-07 |    1.04e+06 |     0.000 |

**Feedback**:
- Num observations with std_diff >= TOL_DIFF_1: 76/2568885 (0.003%)
- Stata standard deviation: 9.61e-01

---

### BookLeverageQuarterly

**Status**: ✅ PASSED

**Test Results**:
- Test 1 - Column names: ✅ PASSED
- Test 2 - Superset check: ✅ PASSED
- Test 3 - Precision1 check: ✅ PASSED
- Test 4 - Precision2 check: ✅ PASSED

**Columns**: ['BookLeverageQuarterly']

**Observations**:
- Stata:  2,572,594
- Python: 2,670,966
- Common: 2,572,594

**Precision1**: 0.001% obs with std_diff >= 1.00e-02 (tolerance: < 10%)

**Precision2**: 99th percentile diff = 4.13e-13 (tolerance: < 1.00e+00)

**Summary Statistics** (Common Observations):

| Statistic  |          Stata |         Python |     Difference | Std Difference |
|------------|----------------|----------------|----------------|----------------|
| count      |       2.57e+06 |       2.57e+06 |       2.57e+06 |       2.57e+06 |
| mean       |       945.9140 |            inf |            inf |            inf |
| std        |       3.67e+06 |            N/A |            N/A |            N/A |
| min        |      -1.62e+09 |    -34413.0000 |       -96.2367 |      -2.62e-05 |
| 25%        |         1.4348 |         1.4348 |      -6.20e-08 |      -1.69e-14 |
| 50%        |         2.0340 |         2.0340 |      -2.22e-16 |      -6.04e-23 |
| 75%        |         3.3458 |         3.3458 |       6.19e-08 |       1.68e-14 |
| max        |       2.85e+09 |            inf |            inf |            inf |

**Regression Analysis** (Python ~ Stata):

- **Model**: python = inf + nan * stata
- **R-squared**: nan
- **N observations**: 2,572,594

| Coefficient |     Estimate |    Std Error | t-statistic |   p-value |
|-------------|--------------|--------------|-------------|----------|
| Intercept   |          nan |          nan |         nan |       nan |
| Slope       |          nan |          nan |         nan |       nan |

**Feedback**:
- Num observations with std_diff >= TOL_DIFF_1: 18/2572594 (0.001%)
- Stata standard deviation: 3.67e+06

---

### CBOperProfLagAT

**Status**: ✅ PASSED

**Test Results**:
- Test 1 - Column names: ✅ PASSED
- Test 2 - Superset check: ✅ PASSED
- Test 3 - Precision1 check: ✅ PASSED
- Test 4 - Precision2 check: ✅ PASSED

**Columns**: ['CBOperProfLagAT']

**Observations**:
- Stata:  2,103,518
- Python: 2,171,034
- Common: 2,103,518

**Precision1**: 0.004% obs with std_diff >= 1.00e-02 (tolerance: < 10%)

**Precision2**: 99th percentile diff = 6.60e-08 (tolerance: < 1.00e+00)

**Summary Statistics** (Common Observations):

| Statistic  |          Stata |         Python |     Difference | Std Difference |
|------------|----------------|----------------|----------------|----------------|
| count      |       2.10e+06 |       2.10e+06 |       2.10e+06 |       2.10e+06 |
| mean       |         0.1168 |         0.1168 |       4.30e-09 |       8.53e-09 |
| std        |         0.5041 |         0.5041 |       2.96e-04 |       5.88e-04 |
| min        |      -162.6901 |      -162.6901 |        -0.2216 |        -0.4396 |
| 25%        |         0.0533 |         0.0533 |      -3.47e-09 |      -6.89e-09 |
| 50%        |         0.1320 |         0.1320 |       4.66e-12 |       9.24e-12 |
| 75%        |         0.2129 |         0.2129 |       3.50e-09 |       6.94e-09 |
| max        |        26.7835 |        26.7835 |         0.0372 |         0.0738 |

**Regression Analysis** (Python ~ Stata):

- **Model**: python = 0.0000 + 1.0000 * stata
- **R-squared**: 1.0000
- **N observations**: 2,103,518

| Coefficient |     Estimate |    Std Error | t-statistic |   p-value |
|-------------|--------------|--------------|-------------|----------|
| Intercept   |     2.13e-07 |     2.10e-07 |      1.0172 |     0.309 |
| Slope       |       1.0000 |     4.05e-07 |    2.47e+06 |     0.000 |

**Feedback**:
- Num observations with std_diff >= TOL_DIFF_1: 82/2103518 (0.004%)
- Stata standard deviation: 5.04e-01

---

### CBOperProfLagAT_q

**Status**: ❌ FAILED

**Test Results**:
- Test 1 - Column names: ✅ PASSED
- Test 2 - Superset check: ❌ FAILED (Python missing 35 Stata observations)
- Test 3 - Precision1 check: ✅ PASSED
- Test 4 - Precision2 check: ✅ PASSED

**Columns**: ['CBOperProfLagAT_q']

**Observations**:
- Stata:  1,911,489
- Python: 1,978,664
- Common: 1,911,454

**Precision1**: 0.018% obs with std_diff >= 1.00e-02 (tolerance: < 10%)

**Precision2**: 99th percentile diff = 8.53e-08 (tolerance: < 1.00e+00)

**Summary Statistics** (Common Observations):

| Statistic  |          Stata |         Python |     Difference | Std Difference |
|------------|----------------|----------------|----------------|----------------|
| count      |       1.91e+06 |       1.91e+06 |       1.91e+06 |       1.91e+06 |
| mean       |         0.0219 |         0.0219 |      -1.65e-05 |      -9.36e-05 |
| std        |         0.1758 |         0.1761 |         0.0110 |         0.0628 |
| min        |       -89.0698 |       -89.0698 |        -8.5459 |       -48.6188 |
| 25%        |        -0.0051 |        -0.0051 |      -9.05e-10 |      -5.15e-09 |
| 50%        |         0.0278 |         0.0278 |         0.0000 |         0.0000 |
| 75%        |         0.0571 |         0.0571 |       9.11e-10 |       5.18e-09 |
| max        |        22.7565 |        22.7565 |         0.6624 |         3.7684 |

**Regression Analysis** (Python ~ Stata):

- **Model**: python = -0.0000 + 0.9999 * stata
- **R-squared**: 0.9961
- **N observations**: 1,911,454

| Coefficient |     Estimate |    Std Error | t-statistic |   p-value |
|-------------|--------------|--------------|-------------|----------|
| Intercept   |    -1.52e-05 |     8.04e-06 |     -1.8851 |     0.059 |
| Slope       |       0.9999 |     4.54e-05 |  22030.9461 |     0.000 |

**Missing Observations Sample**:
```
 index  permno  yyyymm  CBOperProfLagAT_q
     0   10515  199604           0.019881
     1   10515  199605           0.019881
     2   10515  199606           0.019881
     3   11545  199706           0.062512
     4   11545  199707           0.062512
     5   11545  199708           0.062512
     6   12750  198212          -0.046107
     7   12750  198301          -0.046107
     8   12750  198302          -0.046107
     9   12750  198303          -0.021716
```

**Feedback**:
- Num observations with std_diff >= TOL_DIFF_1: 351/1911454 (0.018%)
- Stata standard deviation: 1.76e-01

---

### CFq

**Status**: ❌ FAILED

**Test Results**:
- Test 1 - Column names: ✅ PASSED
- Test 2 - Superset check: ❌ FAILED (Python missing 31 Stata observations)
- Test 3 - Precision1 check: ✅ PASSED
- Test 4 - Precision2 check: ✅ PASSED

**Columns**: ['CFq']

**Observations**:
- Stata:  2,797,878
- Python: 2,797,875
- Common: 2,797,847

**Precision1**: 0.007% obs with std_diff >= 1.00e-02 (tolerance: < 10%)

**Precision2**: 99th percentile diff = 1.50e-08 (tolerance: < 1.00e+00)

**Summary Statistics** (Common Observations):

| Statistic  |          Stata |         Python |     Difference | Std Difference |
|------------|----------------|----------------|----------------|----------------|
| count      |       2.80e+06 |       2.80e+06 |       2.80e+06 |       2.80e+06 |
| mean       |        -0.0128 |        -0.0128 |      -2.99e-06 |      -2.55e-06 |
| std        |         1.1714 |         1.1714 |         0.0034 |         0.0029 |
| min        |      -917.6409 |      -917.6409 |        -2.7228 |        -2.3243 |
| 25%        |         0.0039 |         0.0039 |      -5.35e-10 |      -4.57e-10 |
| 50%        |         0.0195 |         0.0195 |      -1.43e-13 |      -1.22e-13 |
| 75%        |         0.0369 |         0.0369 |       5.33e-10 |       4.55e-10 |
| max        |       163.1038 |       163.1038 |         1.5098 |         1.2889 |

**Regression Analysis** (Python ~ Stata):

- **Model**: python = -0.0000 + 1.0000 * stata
- **R-squared**: 1.0000
- **N observations**: 2,797,847

| Coefficient |     Estimate |    Std Error | t-statistic |   p-value |
|-------------|--------------|--------------|-------------|----------|
| Intercept   |    -3.03e-06 |     2.05e-06 |     -1.4788 |     0.139 |
| Slope       |       1.0000 |     1.75e-06 | 570954.6173 |     0.000 |

**Missing Observations Sample**:
```
 index  permno  yyyymm      CFq
     0   11545  199706 0.013777
     1   11545  199707 0.011884
     2   11545  199708 0.010663
     3   12837  198004 0.027496
     4   12837  198005 0.016803
     5   16965  201812 0.096766
     6   16965  201901 0.083703
     7   16965  201902 0.078968
     8   21346  197001 0.026762
     9   21346  197002 0.025521
```

**Feedback**:
- Num observations with std_diff >= TOL_DIFF_1: 200/2797847 (0.007%)
- Stata standard deviation: 1.17e+00

---

### CapTurnover

**Status**: ✅ PASSED

**Test Results**:
- Test 1 - Column names: ✅ PASSED
- Test 2 - Superset check: ✅ PASSED
- Test 3 - Precision1 check: ✅ PASSED
- Test 4 - Precision2 check: ✅ PASSED

**Columns**: ['CapTurnover']

**Observations**:
- Stata:  2,985,685
- Python: 2,986,378
- Common: 2,985,685

**Precision1**: 0.000% obs with std_diff >= 1.00e-02 (tolerance: < 10%)

**Precision2**: 99th percentile diff = 8.50e-08 (tolerance: < 1.00e+00)

**Summary Statistics** (Common Observations):

| Statistic  |          Stata |         Python |     Difference | Std Difference |
|------------|----------------|----------------|----------------|----------------|
| count      |       2.99e+06 |       2.99e+06 |       2.99e+06 |       2.99e+06 |
| mean       |         1.1455 |         1.1455 |      -1.85e-07 |      -1.04e-07 |
| std        |         1.7917 |         1.7917 |       7.20e-05 |       4.02e-05 |
| min        |        -1.8804 |        -1.8804 |        -0.0353 |        -0.0197 |
| 25%        |         0.3456 |         0.3456 |      -1.39e-08 |      -7.78e-09 |
| 50%        |         0.9236 |         0.9236 |         0.0000 |         0.0000 |
| 75%        |         1.5797 |         1.5797 |       1.43e-08 |       7.97e-09 |
| max        |       392.8943 |       392.8943 |       5.00e-06 |       2.79e-06 |

**Regression Analysis** (Python ~ Stata):

- **Model**: python = -0.0000 + 1.0000 * stata
- **R-squared**: 1.0000
- **N observations**: 2,985,685

| Coefficient |     Estimate |    Std Error | t-statistic |   p-value |
|-------------|--------------|--------------|-------------|----------|
| Intercept   |    -2.44e-07 |     4.95e-08 |     -4.9341 |     0.000 |
| Slope       |       1.0000 |     2.33e-08 |    4.30e+07 |     0.000 |

**Feedback**:
- Num observations with std_diff >= TOL_DIFF_1: 12/2985685 (0.000%)
- Stata standard deviation: 1.79e+00

---

### CapTurnover_q

**Status**: ❌ FAILED

**Test Results**:
- Test 1 - Column names: ✅ PASSED
- Test 2 - Superset check: ❌ FAILED (Python missing 48 Stata observations)
- Test 3 - Precision1 check: ✅ PASSED
- Test 4 - Precision2 check: ✅ PASSED

**Columns**: ['CapTurnover_q']

**Observations**:
- Stata:  2,486,325
- Python: 2,486,315
- Common: 2,486,277

**Precision1**: 0.004% obs with std_diff >= 1.00e-02 (tolerance: < 10%)

**Precision2**: 99th percentile diff = 1.01e-08 (tolerance: < 1.00e+00)

**Summary Statistics** (Common Observations):

| Statistic  |          Stata |         Python |     Difference | Std Difference |
|------------|----------------|----------------|----------------|----------------|
| count      |       2.49e+06 |       2.49e+06 |       2.49e+06 |       2.49e+06 |
| mean       |         0.2638 |         0.2638 |       8.96e-07 |       2.86e-07 |
| std        |         3.1372 |         3.1372 |         0.0033 |         0.0011 |
| min        |        -0.9789 |        -0.9789 |        -1.4640 |        -0.4666 |
| 25%        |         0.0801 |         0.0801 |      -3.40e-09 |      -1.08e-09 |
| 50%        |         0.2127 |         0.2127 |         0.0000 |         0.0000 |
| 75%        |         0.3650 |         0.3650 |       3.40e-09 |       1.08e-09 |
| max        |      2816.9070 |      2816.9070 |         1.5684 |         0.4999 |

**Regression Analysis** (Python ~ Stata):

- **Model**: python = 0.0000 + 1.0000 * stata
- **R-squared**: 1.0000
- **N observations**: 2,486,277

| Coefficient |     Estimate |    Std Error | t-statistic |   p-value |
|-------------|--------------|--------------|-------------|----------|
| Intercept   |     1.01e-06 |     2.11e-06 |      0.4784 |     0.632 |
| Slope       |       1.0000 |     6.70e-07 |    1.49e+06 |     0.000 |

**Missing Observations Sample**:
```
 index  permno  yyyymm  CapTurnover_q
     0   10515  199607       0.068358
     1   10515  199608       0.068358
     2   10515  199609       0.068358
     3   11545  199706       0.209439
     4   11545  199707       0.209439
     5   11545  199708       0.209439
     6   12750  198303       0.359559
     7   12750  198304       0.359559
     8   12750  198305       0.359559
     9   12837  198004       0.328576
```

**Feedback**:
- Num observations with std_diff >= TOL_DIFF_1: 93/2486277 (0.004%)
- Stata standard deviation: 3.14e+00

---

### ChNCOA

**Status**: ✅ PASSED

**Test Results**:
- Test 1 - Column names: ✅ PASSED
- Test 2 - Superset check: ✅ PASSED
- Test 3 - Precision1 check: ✅ PASSED
- Test 4 - Precision2 check: ✅ PASSED

**Columns**: ['ChNCOA']

**Observations**:
- Stata:  3,295,125
- Python: 3,295,872
- Common: 3,295,125

**Precision1**: 0.003% obs with std_diff >= 1.00e-02 (tolerance: < 10%)

**Precision2**: 99th percentile diff = 8.48e-08 (tolerance: < 1.00e+00)

**Summary Statistics** (Common Observations):

| Statistic  |          Stata |         Python |     Difference | Std Difference |
|------------|----------------|----------------|----------------|----------------|
| count      |       3.30e+06 |       3.30e+06 |       3.30e+06 |       3.30e+06 |
| mean       |         0.0889 |         0.0889 |      -2.75e-06 |      -3.06e-06 |
| std        |         0.8966 |         0.8966 |         0.0015 |         0.0016 |
| min        |        -1.4114 |        -1.4114 |        -0.7511 |        -0.8377 |
| 25%        |        -0.0138 |        -0.0138 |      -9.90e-09 |      -1.10e-08 |
| 50%        |         0.0232 |         0.0232 |         0.0000 |         0.0000 |
| 75%        |         0.0917 |         0.0917 |       9.89e-09 |       1.10e-08 |
| max        |       192.5833 |       192.5833 |         0.1241 |         0.1384 |

**Regression Analysis** (Python ~ Stata):

- **Model**: python = -0.0000 + 1.0000 * stata
- **R-squared**: 1.0000
- **N observations**: 3,295,125

| Coefficient |     Estimate |    Std Error | t-statistic |   p-value |
|-------------|--------------|--------------|-------------|----------|
| Intercept   |    -2.76e-06 |     8.11e-07 |     -3.4040 |     0.001 |
| Slope       |       1.0000 |     9.00e-07 |    1.11e+06 |     0.000 |

**Feedback**:
- Num observations with std_diff >= TOL_DIFF_1: 84/3295125 (0.003%)
- Stata standard deviation: 8.97e-01

---

### ChNCOL

**Status**: ✅ PASSED

**Test Results**:
- Test 1 - Column names: ✅ PASSED
- Test 2 - Superset check: ✅ PASSED
- Test 3 - Precision1 check: ✅ PASSED
- Test 4 - Precision2 check: ✅ PASSED

**Columns**: ['ChNCOL']

**Observations**:
- Stata:  3,249,290
- Python: 3,250,061
- Common: 3,249,290

**Precision1**: 0.004% obs with std_diff >= 1.00e-02 (tolerance: < 10%)

**Precision2**: 99th percentile diff = 5.79e-08 (tolerance: < 1.00e+00)

**Summary Statistics** (Common Observations):

| Statistic  |          Stata |         Python |     Difference | Std Difference |
|------------|----------------|----------------|----------------|----------------|
| count      |       3.25e+06 |       3.25e+06 |       3.25e+06 |       3.25e+06 |
| mean       |         0.0487 |         0.0487 |      -1.48e-07 |      -1.52e-07 |
| std        |         0.9693 |         0.9693 |       1.85e-04 |       1.91e-04 |
| min        |       -23.0669 |       -23.0669 |        -0.0482 |        -0.0497 |
| 25%        |        -0.0092 |        -0.0092 |      -5.62e-09 |      -5.80e-09 |
| 50%        |         0.0187 |         0.0187 |         0.0000 |         0.0000 |
| 75%        |         0.0626 |         0.0626 |       5.61e-09 |       5.79e-09 |
| max        |       381.2545 |       381.2545 |         0.0528 |         0.0545 |

**Regression Analysis** (Python ~ Stata):

- **Model**: python = -0.0000 + 1.0000 * stata
- **R-squared**: 1.0000
- **N observations**: 3,249,290

| Coefficient |     Estimate |    Std Error | t-statistic |   p-value |
|-------------|--------------|--------------|-------------|----------|
| Intercept   |    -1.46e-07 |     1.03e-07 |     -1.4209 |     0.155 |
| Slope       |       1.0000 |     1.06e-07 |    9.42e+06 |     0.000 |

**Feedback**:
- Num observations with std_diff >= TOL_DIFF_1: 120/3249290 (0.004%)
- Stata standard deviation: 9.69e-01

---

### ChangeRoA

**Status**: ❌ FAILED

**Test Results**:
- Test 1 - Column names: ✅ PASSED
- Test 2 - Superset check: ❌ FAILED (Python missing 65 Stata observations)
- Test 3 - Precision1 check: ✅ PASSED
- Test 4 - Precision2 check: ✅ PASSED

**Columns**: ['ChangeRoA']

**Observations**:
- Stata:  2,296,769
- Python: 2,296,739
- Common: 2,296,704

**Precision1**: 0.008% obs with std_diff >= 1.00e-02 (tolerance: < 10%)

**Precision2**: 99th percentile diff = 6.60e-08 (tolerance: < 1.00e+00)

**Summary Statistics** (Common Observations):

| Statistic  |          Stata |         Python |     Difference | Std Difference |
|------------|----------------|----------------|----------------|----------------|
| count      |       2.30e+06 |       2.30e+06 |       2.30e+06 |       2.30e+06 |
| mean       |        -0.0019 |        -0.0019 |      -1.97e-07 |      -8.41e-07 |
| std        |         0.2344 |         0.2344 |         0.0014 |         0.0059 |
| min        |       -55.1174 |       -55.1174 |        -0.6578 |        -2.8059 |
| 25%        |        -0.0078 |        -0.0078 |      -4.26e-10 |      -1.82e-09 |
| 50%        |      -7.35e-05 |      -7.35e-05 |      -3.65e-13 |      -1.56e-12 |
| 75%        |         0.0058 |         0.0058 |       4.28e-10 |       1.83e-09 |
| max        |       136.3447 |       136.3447 |         0.5126 |         2.1863 |

**Regression Analysis** (Python ~ Stata):

- **Model**: python = -0.0000 + 1.0000 * stata
- **R-squared**: 1.0000
- **N observations**: 2,296,704

| Coefficient |     Estimate |    Std Error | t-statistic |   p-value |
|-------------|--------------|--------------|-------------|----------|
| Intercept   |    -2.56e-07 |     9.18e-07 |     -0.2791 |     0.780 |
| Slope       |       1.0000 |     3.92e-06 | 255361.2488 |     0.000 |

**Missing Observations Sample**:
```
 index  permno  yyyymm  ChangeRoA
     0   10515  199604  -0.004968
     1   10515  199605  -0.004968
     2   10515  199606  -0.004968
     3   10515  199704  -0.004280
     4   10515  199705  -0.004280
     5   10515  199706  -0.004280
     6   11545  199706  -0.018291
     7   11545  199707  -0.018291
     8   11545  199708  -0.018291
     9   11545  199806   0.009021
```

**Feedback**:
- Num observations with std_diff >= TOL_DIFF_1: 183/2296704 (0.008%)
- Stata standard deviation: 2.34e-01

---

### ChangeRoE

**Status**: ❌ FAILED

**Test Results**:
- Test 1 - Column names: ✅ PASSED
- Test 2 - Superset check: ❌ FAILED (Python missing 70 Stata observations)
- Test 3 - Precision1 check: ✅ PASSED
- Test 4 - Precision2 check: ✅ PASSED

**Columns**: ['ChangeRoE']

**Observations**:
- Stata:  2,360,217
- Python: 2,360,248
- Common: 2,360,147

**Precision1**: 0.002% obs with std_diff >= 1.00e-02 (tolerance: < 10%)

**Precision2**: 99th percentile diff = 3.18e-09 (tolerance: < 1.00e+00)

**Summary Statistics** (Common Observations):

| Statistic  |          Stata |         Python |     Difference | Std Difference |
|------------|----------------|----------------|----------------|----------------|
| count      |       2.36e+06 |       2.36e+06 |       2.36e+06 |       2.36e+06 |
| mean       |      -8.57e-04 |      -8.62e-04 |      -4.47e-06 |      -1.44e-07 |
| std        |        31.1267 |        31.1269 |         0.0990 |         0.0032 |
| min        |    -14927.4960 |    -14927.4966 |       -61.0000 |        -1.9597 |
| 25%        |        -0.0196 |        -0.0196 |      -1.10e-09 |      -3.53e-11 |
| 50%        |      -6.95e-04 |      -6.95e-04 |      -1.29e-12 |      -4.14e-14 |
| 75%        |         0.0130 |         0.0130 |       1.09e-09 |       3.49e-11 |
| max        |     14925.0560 |     14925.0557 |        61.0000 |         1.9597 |

**Regression Analysis** (Python ~ Stata):

- **Model**: python = -0.0000 + 1.0000 * stata
- **R-squared**: 1.0000
- **N observations**: 2,360,147

| Coefficient |     Estimate |    Std Error | t-statistic |   p-value |
|-------------|--------------|--------------|-------------|----------|
| Intercept   |    -4.47e-06 |     6.44e-05 |     -0.0693 |     0.945 |
| Slope       |       1.0000 |     2.07e-06 | 483078.1554 |     0.000 |

**Missing Observations Sample**:
```
 index  permno  yyyymm  ChangeRoE
     0   10515  199604  -0.006004
     1   10515  199605  -0.006004
     2   10515  199606  -0.006004
     3   10515  199704  -0.005122
     4   10515  199705  -0.005122
     5   10515  199706  -0.005122
     6   11545  199706  -0.054672
     7   11545  199707  -0.054672
     8   11545  199708  -0.054672
     9   11545  199806   0.021011
```

**Feedback**:
- Num observations with std_diff >= TOL_DIFF_1: 36/2360147 (0.002%)
- Stata standard deviation: 3.11e+01

---

### DelSTI

**Status**: ✅ PASSED

**Test Results**:
- Test 1 - Column names: ✅ PASSED
- Test 2 - Superset check: ✅ PASSED
- Test 3 - Precision1 check: ✅ PASSED
- Test 4 - Precision2 check: ✅ PASSED

**Columns**: ['DelSTI']

**Observations**:
- Stata:  3,295,155
- Python: 3,295,872
- Common: 3,295,155

**Precision1**: 0.003% obs with std_diff >= 1.00e-02 (tolerance: < 10%)

**Precision2**: 99th percentile diff = 2.04e-07 (tolerance: < 1.00e+00)

**Summary Statistics** (Common Observations):

| Statistic  |          Stata |         Python |     Difference | Std Difference |
|------------|----------------|----------------|----------------|----------------|
| count      |       3.30e+06 |       3.30e+06 |       3.30e+06 |       3.30e+06 |
| mean       |         0.0019 |         0.0019 |      -7.19e-07 |      -7.20e-06 |
| std        |         0.0999 |         0.0999 |       4.37e-04 |         0.0044 |
| min        |        -1.8790 |        -1.8790 |        -0.2141 |        -2.1431 |
| 25%        |      -6.70e-06 |      -6.63e-06 |      -1.32e-12 |      -1.32e-11 |
| 50%        |         0.0000 |         0.0000 |         0.0000 |         0.0000 |
| 75%        |       2.58e-04 |       2.58e-04 |       1.33e-12 |       1.34e-11 |
| max        |         1.8457 |         1.8457 |         0.0581 |         0.5818 |

**Regression Analysis** (Python ~ Stata):

- **Model**: python = -0.0000 + 1.0000 * stata
- **R-squared**: 1.0000
- **N observations**: 3,295,155

| Coefficient |     Estimate |    Std Error | t-statistic |   p-value |
|-------------|--------------|--------------|-------------|----------|
| Intercept   |    -7.46e-07 |     2.41e-07 |     -3.0985 |     0.002 |
| Slope       |       1.0000 |     2.41e-06 | 414759.9752 |     0.000 |

**Feedback**:
- Num observations with std_diff >= TOL_DIFF_1: 108/3295155 (0.003%)
- Stata standard deviation: 9.99e-02

---

### DivYield

**Status**: ❌ FAILED

**Test Results**:
- Test 1 - Column names: ✅ PASSED
- Test 2 - Superset check: ❌ FAILED (Python missing 59 Stata observations)
- Test 3 - Precision1 check: ✅ PASSED
- Test 4 - Precision2 check: ✅ PASSED

**Columns**: ['DivYield']

**Observations**:
- Stata:  421,384
- Python: 421,370
- Common: 421,325

**Precision1**: 0.004% obs with std_diff >= 1.00e-02 (tolerance: < 10%)

**Precision2**: 99th percentile diff = 1.24e-08 (tolerance: < 1.00e+00)

**Summary Statistics** (Common Observations):

| Statistic  |          Stata |         Python |     Difference | Std Difference |
|------------|----------------|----------------|----------------|----------------|
| count      |    421325.0000 |    421325.0000 |    421325.0000 |    421325.0000 |
| mean       |         0.0490 |         0.0490 |      -1.33e-05 |      -2.32e-05 |
| std        |         0.5730 |         0.5717 |         0.0043 |         0.0074 |
| min        |         0.0000 |         0.0000 |        -1.7481 |        -3.0506 |
| 25%        |         0.0201 |         0.0201 |      -1.01e-09 |      -1.77e-09 |
| 50%        |         0.0356 |         0.0356 |      -2.02e-11 |      -3.53e-11 |
| 75%        |         0.0554 |         0.0554 |       4.69e-10 |       8.19e-10 |
| max        |       154.9091 |       154.9091 |         0.0335 |         0.0584 |

**Regression Analysis** (Python ~ Stata):

- **Model**: python = 0.0001 + 0.9976 * stata
- **R-squared**: 1.0000
- **N observations**: 421,325

| Coefficient |     Estimate |    Std Error | t-statistic |   p-value |
|-------------|--------------|--------------|-------------|----------|
| Intercept   |     1.06e-04 |     6.22e-06 |     17.0093 |     0.000 |
| Slope       |       0.9976 |     1.08e-05 |  92300.7198 |     0.000 |

**Missing Observations Sample**:
```
 index  permno  yyyymm  DivYield
     0   11470  199209  0.017391
     1   11470  199212  0.014371
     2   11470  199303  0.017391
     3   11748  201504  0.022488
     4   11748  201505  0.022927
     5   11748  201506  0.023354
     6   11748  201507  0.023612
     7   11748  201508  0.023176
     8   11748  201509  0.025351
     9   11748  201510  0.023389
```

**Feedback**:
- Num observations with std_diff >= TOL_DIFF_1: 16/421325 (0.004%)
- Stata standard deviation: 5.73e-01

---

### DivYieldAnn

**Status**: ✅ PASSED

**Test Results**:
- Test 1 - Column names: ✅ PASSED
- Test 2 - Superset check: ✅ PASSED
- Test 3 - Precision1 check: ✅ PASSED
- Test 4 - Precision2 check: ✅ PASSED

**Columns**: ['DivYieldAnn']

**Observations**:
- Stata:  3,878,713
- Python: 3,883,930
- Common: 3,878,713

**Precision1**: 0.032% obs with std_diff >= 1.00e-02 (tolerance: < 10%)

**Precision2**: 99th percentile diff = 2.07e-08 (tolerance: < 1.00e+00)

**Summary Statistics** (Common Observations):

| Statistic  |          Stata |         Python |     Difference | Std Difference |
|------------|----------------|----------------|----------------|----------------|
| count      |       3.88e+06 |       3.88e+06 |       3.88e+06 |       3.88e+06 |
| mean       |         0.0239 |         0.0239 |       2.17e-05 |       1.05e-04 |
| std        |         0.2072 |         0.2075 |         0.0092 |         0.0443 |
| min        |        -0.5405 |        -0.5405 |        -1.5984 |        -7.7145 |
| 25%        |         0.0000 |         0.0000 |         0.0000 |         0.0000 |
| 50%        |         0.0000 |         0.0000 |         0.0000 |         0.0000 |
| 75%        |         0.0299 |         0.0299 |         0.0000 |         0.0000 |
| max        |        83.2000 |        83.2000 |         6.1759 |        29.8080 |

**Regression Analysis** (Python ~ Stata):

- **Model**: python = 0.0000 + 1.0004 * stata
- **R-squared**: 0.9980
- **N observations**: 3,878,713

| Coefficient |     Estimate |    Std Error | t-statistic |   p-value |
|-------------|--------------|--------------|-------------|----------|
| Intercept   |     1.26e-05 |     4.69e-06 |      2.6782 |     0.007 |
| Slope       |       1.0004 |     2.25e-05 |  44469.1835 |     0.000 |

**Feedback**:
- Num observations with std_diff >= TOL_DIFF_1: 1247/3878713 (0.032%)
- Stata standard deviation: 2.07e-01

---

### EBM_q

**Status**: ❌ FAILED

**Test Results**:
- Test 1 - Column names: ✅ PASSED
- Test 2 - Superset check: ❌ FAILED (Python missing 54 Stata observations)
- Test 3 - Precision1 check: ✅ PASSED
- Test 4 - Precision2 check: ✅ PASSED

**Columns**: ['EBM_q']

**Observations**:
- Stata:  2,497,505
- Python: 2,497,500
- Common: 2,497,451

**Precision1**: 0.002% obs with std_diff >= 1.00e-02 (tolerance: < 10%)

**Precision2**: 99th percentile diff = 3.39e-08 (tolerance: < 1.00e+00)

**Summary Statistics** (Common Observations):

| Statistic  |          Stata |         Python |     Difference | Std Difference |
|------------|----------------|----------------|----------------|----------------|
| count      |       2.50e+06 |       2.50e+06 |       2.50e+06 |       2.50e+06 |
| mean       |         0.5320 |         0.5302 |        -0.0018 |      -8.56e-06 |
| std        |       210.6166 |       207.7943 |         4.0061 |         0.0190 |
| min        |   -135089.5600 |   -134017.4161 |     -6189.2265 |       -29.3862 |
| 25%        |         0.1800 |         0.1800 |      -1.36e-08 |      -6.44e-11 |
| 50%        |         0.5004 |         0.5004 |      -1.65e-11 |      -7.81e-14 |
| 75%        |         0.9606 |         0.9606 |       1.35e-08 |       6.43e-11 |
| max        |    215285.7300 |    209096.5035 |      1072.1439 |         5.0905 |

**Regression Analysis** (Python ~ Stata):

- **Model**: python = 0.0054 + 0.9865 * stata
- **R-squared**: 0.9998
- **N observations**: 2,497,451

| Coefficient |     Estimate |    Std Error | t-statistic |   p-value |
|-------------|--------------|--------------|-------------|----------|
| Intercept   |       0.0054 |       0.0018 |      3.0083 |     0.003 |
| Slope       |       0.9865 |     8.48e-06 | 116274.9025 |     0.000 |

**Missing Observations Sample**:
```
 index  permno  yyyymm    EBM_q
     0   10515  199604 1.030155
     1   10515  199605 1.891978
     2   10515  199606 1.808921
     3   11545  199706 0.477123
     4   11545  199707 0.421310
     5   11545  199708 0.383889
     6   12750  198212 0.099635
     7   12750  198301 0.103646
     8   12750  198302 0.095039
     9   12837  198004 1.263025
```

**Feedback**:
- Num observations with std_diff >= TOL_DIFF_1: 44/2497451 (0.002%)
- Stata standard deviation: 2.11e+02

---

### EPq

**Status**: ❌ FAILED

**Test Results**:
- Test 1 - Column names: ✅ PASSED
- Test 2 - Superset check: ❌ FAILED (Python missing 85 Stata observations)
- Test 3 - Precision1 check: ✅ PASSED
- Test 4 - Precision2 check: ✅ PASSED

**Columns**: ['EPq']

**Observations**:
- Stata:  1,893,938
- Python: 1,917,581
- Common: 1,893,853

**Precision1**: 0.741% obs with std_diff >= 1.00e-02 (tolerance: < 10%)

**Precision2**: 99th percentile diff = 2.94e-03 (tolerance: < 1.00e+00)

**Summary Statistics** (Common Observations):

| Statistic  |          Stata |         Python |     Difference | Std Difference |
|------------|----------------|----------------|----------------|----------------|
| count      |       1.89e+06 |       1.89e+06 |       1.89e+06 |       1.89e+06 |
| mean       |         0.0273 |         0.0273 |       7.08e-06 |       7.08e-05 |
| std        |         0.1001 |         0.1021 |         0.0209 |         0.2086 |
| min        |         0.0000 |         0.0000 |       -14.6293 |      -146.1056 |
| 25%        |         0.0107 |         0.0107 |      -3.65e-10 |      -3.64e-09 |
| 50%        |         0.0180 |         0.0180 |         0.0000 |         0.0000 |
| 75%        |         0.0297 |         0.0297 |       3.65e-10 |       3.65e-09 |
| max        |        35.0386 |        35.0386 |        19.1968 |       191.7232 |

**Regression Analysis** (Python ~ Stata):

- **Model**: python = 0.0000 + 0.9986 * stata
- **R-squared**: 0.9582
- **N observations**: 1,893,853

| Coefficient |     Estimate |    Std Error | t-statistic |   p-value |
|-------------|--------------|--------------|-------------|----------|
| Intercept   |     4.63e-05 |     1.57e-05 |      2.9415 |     0.003 |
| Slope       |       0.9986 |     1.52e-04 |   6588.6729 |     0.000 |

**Missing Observations Sample**:
```
 index  permno  yyyymm      EPq
     0   10198  198709 0.005705
     1   10515  199604 0.005181
     2   10515  199605 0.005181
     3   10515  199606 0.005181
     4   11321  199406 0.041526
     5   11651  198902 0.000409
     6   11843  198803 0.040014
     7   11843  198804 0.081029
     8   11843  198805 0.055882
     9   11865  198906 0.000835
```

**Feedback**:
- Num observations with std_diff >= TOL_DIFF_1: 14029/1893853 (0.741%)
- Stata standard deviation: 1.00e-01

---

### ETR

**Status**: ✅ PASSED

**Test Results**:
- Test 1 - Column names: ✅ PASSED
- Test 2 - Superset check: ✅ PASSED
- Test 3 - Precision1 check: ✅ PASSED
- Test 4 - Precision2 check: ✅ PASSED

**Columns**: ['ETR']

**Observations**:
- Stata:  2,657,230
- Python: 2,658,445
- Common: 2,657,230

**Precision1**: 0.001% obs with std_diff >= 1.00e-02 (tolerance: < 10%)

**Precision2**: 99th percentile diff = 6.20e-12 (tolerance: < 1.00e+00)

**Summary Statistics** (Common Observations):

| Statistic  |          Stata |         Python |     Difference | Std Difference |
|------------|----------------|----------------|----------------|----------------|
| count      |       2.66e+06 |       2.66e+06 |       2.66e+06 |       2.66e+06 |
| mean       |       200.8662 |       199.7921 |        -1.0740 |      -1.11e-05 |
| std        |     96619.4326 |     96620.8610 |       523.6358 |         0.0054 |
| min        |      -2.82e+07 |      -2.82e+07 |   -256264.7862 |        -2.6523 |
| 25%        |      -6.25e-04 |      -6.25e-04 |      -1.44e-10 |      -1.49e-15 |
| 50%        |         0.0000 |         0.0000 |        -0.0000 |        -0.0000 |
| 75%        |         0.0010 |         0.0010 |       1.45e-10 |       1.50e-15 |
| max        |       3.75e+07 |       3.75e+07 |      8898.4587 |         0.0921 |

**Regression Analysis** (Python ~ Stata):

- **Model**: python = -1.0741 + 1.0000 * stata
- **R-squared**: 1.0000
- **N observations**: 2,657,230

| Coefficient |     Estimate |    Std Error | t-statistic |   p-value |
|-------------|--------------|--------------|-------------|----------|
| Intercept   |      -1.0741 |       0.3212 |     -3.3436 |     0.001 |
| Slope       |       1.0000 |     3.32e-06 | 300780.4586 |     0.000 |

**Feedback**:
- Num observations with std_diff >= TOL_DIFF_1: 36/2657230 (0.001%)
- Stata standard deviation: 9.66e+04

---

### EarningsSmoothness

**Status**: ✅ PASSED

**Test Results**:
- Test 1 - Column names: ✅ PASSED
- Test 2 - Superset check: ✅ PASSED
- Test 3 - Precision1 check: ✅ PASSED
- Test 4 - Precision2 check: ✅ PASSED

**Columns**: ['EarningsSmoothness']

**Observations**:
- Stata:  1,482,823
- Python: 1,538,785
- Common: 1,482,823

**Precision1**: 0.005% obs with std_diff >= 1.00e-02 (tolerance: < 10%)

**Precision2**: 99th percentile diff = 3.06e-07 (tolerance: < 1.00e+00)

**Summary Statistics** (Common Observations):

| Statistic  |          Stata |         Python |     Difference | Std Difference |
|------------|----------------|----------------|----------------|----------------|
| count      |       1.48e+06 |       1.48e+06 |       1.48e+06 |       1.48e+06 |
| mean       |         0.6548 |         0.6548 |       2.11e-07 |       5.30e-07 |
| std        |         0.3971 |         0.3971 |       2.96e-04 |       7.45e-04 |
| min        |         0.0036 |         0.0036 |        -0.0287 |        -0.0722 |
| 25%        |         0.3480 |         0.3480 |      -1.50e-08 |      -3.78e-08 |
| 50%        |         0.6297 |         0.6297 |       1.52e-11 |       3.82e-11 |
| 75%        |         0.9233 |         0.9233 |       1.51e-08 |       3.79e-08 |
| max        |         8.3146 |         8.3146 |         0.3090 |         0.7781 |

**Regression Analysis** (Python ~ Stata):

- **Model**: python = 0.0000 + 1.0000 * stata
- **R-squared**: 1.0000
- **N observations**: 1,482,823

| Coefficient |     Estimate |    Std Error | t-statistic |   p-value |
|-------------|--------------|--------------|-------------|----------|
| Intercept   |     4.16e-07 |     4.69e-07 |      0.8875 |     0.375 |
| Slope       |       1.0000 |     6.12e-07 |    1.63e+06 |     0.000 |

**Feedback**:
- Num observations with std_diff >= TOL_DIFF_1: 73/1482823 (0.005%)
- Stata standard deviation: 3.97e-01

---

### EntMult_q

**Status**: ❌ FAILED

**Test Results**:
- Test 1 - Column names: ✅ PASSED
- Test 2 - Superset check: ❌ FAILED (Python missing 12 Stata observations)
- Test 3 - Precision1 check: ✅ PASSED
- Test 4 - Precision2 check: ✅ PASSED

**Columns**: ['EntMult_q']

**Observations**:
- Stata:  1,689,737
- Python: 2,064,856
- Common: 1,689,725

**Precision1**: 0.003% obs with std_diff >= 1.00e-02 (tolerance: < 10%)

**Precision2**: 99th percentile diff = 4.68e-09 (tolerance: < 1.00e+00)

**Summary Statistics** (Common Observations):

| Statistic  |          Stata |         Python |     Difference | Std Difference |
|------------|----------------|----------------|----------------|----------------|
| count      |       1.69e+06 |       1.69e+06 |       1.69e+06 |       1.69e+06 |
| mean       |        87.8995 |        87.9010 |         0.0015 |       4.86e-07 |
| std        |      3126.3404 |      3126.3404 |         1.0557 |       3.38e-04 |
| min        |    -43431.7380 |    -43431.7397 |      -269.0794 |        -0.0861 |
| 25%        |        20.2668 |        20.2672 |      -6.42e-07 |      -2.05e-10 |
| 50%        |        32.0420 |        32.0423 |      -1.57e-09 |      -5.03e-13 |
| 75%        |        51.5116 |        51.5118 |       6.38e-07 |       2.04e-10 |
| max        |       1.43e+06 |       1.43e+06 |       523.7859 |         0.1675 |

**Regression Analysis** (Python ~ Stata):

- **Model**: python = 0.0015 + 1.0000 * stata
- **R-squared**: 1.0000
- **N observations**: 1,689,725

| Coefficient |     Estimate |    Std Error | t-statistic |   p-value |
|-------------|--------------|--------------|-------------|----------|
| Intercept   |       0.0015 |     8.12e-04 |      1.8756 |     0.061 |
| Slope       |       1.0000 |     2.60e-07 |    3.85e+06 |     0.000 |

**Missing Observations Sample**:
```
 index  permno  yyyymm  EntMult_q
     0   79352  199706  43.669903
     1   79352  199707  46.337032
     2   79352  199708  43.332870
     3   86444  200106  28.878563
     4   86444  200107  25.313938
     5   86444  200108  18.186907
     6   89887  199503 204.392670
     7   89887  199504 203.474820
     8   89887  199505 200.950740
     9   92260  199003  13.277908
```

**Feedback**:
- Num observations with std_diff >= TOL_DIFF_1: 57/1689725 (0.003%)
- Stata standard deviation: 3.13e+03

---

### LaborforceEfficiency

**Status**: ✅ PASSED

**Test Results**:
- Test 1 - Column names: ✅ PASSED
- Test 2 - Superset check: ✅ PASSED
- Test 3 - Precision1 check: ✅ PASSED
- Test 4 - Precision2 check: ✅ PASSED

**Columns**: ['LaborforceEfficiency']

**Observations**:
- Stata:  2,974,260
- Python: 3,073,530
- Common: 2,974,260

**Precision1**: 0.000% obs with std_diff >= 1.00e-02 (tolerance: < 10%)

**Precision2**: 99th percentile diff = 4.28e-09 (tolerance: < 1.00e+00)

**Summary Statistics** (Common Observations):

| Statistic  |          Stata |         Python |     Difference | Std Difference |
|------------|----------------|----------------|----------------|----------------|
| count      |       2.97e+06 |       2.97e+06 |       2.97e+06 |       2.97e+06 |
| mean       |         0.5044 |         0.5043 |      -3.97e-05 |      -1.08e-06 |
| std        |        36.7045 |        36.7045 |         0.0199 |       5.43e-04 |
| min        |      -247.4286 |      -247.4286 |        -9.9206 |        -0.2703 |
| 25%        |        -0.0439 |        -0.0439 |      -2.62e-08 |      -7.15e-10 |
| 50%        |         0.0510 |         0.0510 |         0.0000 |         0.0000 |
| 75%        |         0.1598 |         0.1598 |       2.63e-08 |       7.16e-10 |
| max        |     11615.4880 |     11615.4889 |         0.1038 |         0.0028 |

**Regression Analysis** (Python ~ Stata):

- **Model**: python = -0.0000 + 1.0000 * stata
- **R-squared**: 1.0000
- **N observations**: 2,974,260

| Coefficient |     Estimate |    Std Error | t-statistic |   p-value |
|-------------|--------------|--------------|-------------|----------|
| Intercept   |    -3.95e-05 |     1.16e-05 |     -3.4220 |     0.001 |
| Slope       |       1.0000 |     3.15e-07 |    3.18e+06 |     0.000 |

**Feedback**:
- Num observations with std_diff >= TOL_DIFF_1: 12/2974260 (0.000%)
- Stata standard deviation: 3.67e+01

---

### Leverage_q

**Status**: ❌ FAILED

**Test Results**:
- Test 1 - Column names: ✅ PASSED
- Test 2 - Superset check: ❌ FAILED (Python missing 67 Stata observations)
- Test 3 - Precision1 check: ✅ PASSED
- Test 4 - Precision2 check: ✅ PASSED

**Columns**: ['Leverage_q']

**Observations**:
- Stata:  2,571,833
- Python: 2,571,800
- Common: 2,571,766

**Precision1**: 0.000% obs with std_diff >= 1.00e-02 (tolerance: < 10%)

**Precision2**: 99th percentile diff = 4.47e-08 (tolerance: < 1.00e+00)

**Summary Statistics** (Common Observations):

| Statistic  |          Stata |         Python |     Difference | Std Difference |
|------------|----------------|----------------|----------------|----------------|
| count      |       2.57e+06 |       2.57e+06 |       2.57e+06 |       2.57e+06 |
| mean       |         2.8298 |         2.8298 |       1.84e-06 |       9.83e-08 |
| std        |        18.6726 |        18.6726 |         0.0018 |       9.66e-05 |
| min        |       -11.0632 |       -11.0632 |        -0.1521 |        -0.0081 |
| 25%        |         0.2307 |         0.2307 |      -1.17e-08 |      -6.26e-10 |
| 50%        |         0.6768 |         0.6768 |      -2.03e-12 |      -1.09e-13 |
| 75%        |         2.0022 |         2.0022 |       1.16e-08 |       6.22e-10 |
| max        |      8843.3477 |      8843.3475 |         2.0802 |         0.1114 |

**Regression Analysis** (Python ~ Stata):

- **Model**: python = 0.0000 + 1.0000 * stata
- **R-squared**: 1.0000
- **N observations**: 2,571,766

| Coefficient |     Estimate |    Std Error | t-statistic |   p-value |
|-------------|--------------|--------------|-------------|----------|
| Intercept   |     1.86e-06 |     1.14e-06 |      1.6312 |     0.103 |
| Slope       |       1.0000 |     6.02e-08 |    1.66e+07 |     0.000 |

**Missing Observations Sample**:
```
 index  permno  yyyymm  Leverage_q
     0   10515  199604    0.207634
     1   10515  199605    0.534574
     2   10515  199606    0.492051
     3   11545  199706    0.042305
     4   11545  199707    0.036492
     5   11545  199708    0.032743
     6   12750  198212    0.127148
     7   12750  198301    0.131946
     8   12750  198302    0.121620
     9   12837  198004    0.933059
```

**Feedback**:
- Num observations with std_diff >= TOL_DIFF_1: 3/2571766 (0.000%)
- Stata standard deviation: 1.87e+01

---

### NetDebtPrice_q

**Status**: ❌ FAILED

**Test Results**:
- Test 1 - Column names: ✅ PASSED
- Test 2 - Superset check: ❌ FAILED (Python missing 40 Stata observations)
- Test 3 - Precision1 check: ✅ PASSED
- Test 4 - Precision2 check: ✅ PASSED

**Columns**: ['NetDebtPrice_q']

**Observations**:
- Stata:  1,178,409
- Python: 1,219,765
- Common: 1,178,369

**Precision1**: 0.001% obs with std_diff >= 1.00e-02 (tolerance: < 10%)

**Precision2**: 99th percentile diff = 4.85e-08 (tolerance: < 1.00e+00)

**Summary Statistics** (Common Observations):

| Statistic  |          Stata |         Python |     Difference | Std Difference |
|------------|----------------|----------------|----------------|----------------|
| count      |       1.18e+06 |       1.18e+06 |       1.18e+06 |       1.18e+06 |
| mean       |         1.0138 |         1.0138 |       1.65e-06 |       2.40e-07 |
| std        |         6.8787 |         6.8787 |         0.0013 |       1.87e-04 |
| min        |      -142.3929 |      -142.3929 |        -0.0512 |        -0.0074 |
| 25%        |        -0.0768 |        -0.0768 |      -8.22e-09 |      -1.20e-09 |
| 50%        |         0.2984 |         0.2984 |       1.28e-12 |       1.86e-13 |
| 75%        |         0.9501 |         0.9501 |       8.29e-09 |       1.20e-09 |
| max        |      2492.7185 |      2492.7185 |         1.3700 |         0.1992 |

**Regression Analysis** (Python ~ Stata):

- **Model**: python = 0.0000 + 1.0000 * stata
- **R-squared**: 1.0000
- **N observations**: 1,178,369

| Coefficient |     Estimate |    Std Error | t-statistic |   p-value |
|-------------|--------------|--------------|-------------|----------|
| Intercept   |     1.66e-06 |     1.20e-06 |      1.3845 |     0.166 |
| Slope       |       1.0000 |     1.72e-07 |    5.80e+06 |     0.000 |

**Missing Observations Sample**:
```
 index  permno  yyyymm  NetDebtPrice_q
     0   10515  199604       -0.342635
     1   10515  199605       -0.882147
     2   10515  199606       -0.811976
     3   12837  198004        0.438865
     4   23033  202412       -0.213396
     5   23792  202412        0.499986
     6   23863  202412       -0.402767
     7   25786  198806       -1.045119
     8   25786  198807       -1.081157
     9   25786  198808       -1.119770
```

**Feedback**:
- Num observations with std_diff >= TOL_DIFF_1: 6/1178369 (0.001%)
- Stata standard deviation: 6.88e+00

---

### NetPayoutYield_q

**Status**: ✅ PASSED

**Test Results**:
- Test 1 - Column names: ✅ PASSED
- Test 2 - Superset check: ✅ PASSED
- Test 3 - Precision1 check: ✅ PASSED
- Test 4 - Precision2 check: ✅ PASSED

**Columns**: ['NetPayoutYield_q']

**Observations**:
- Stata:  2,520,037
- Python: 2,622,217
- Common: 2,520,037

**Precision1**: 0.016% obs with std_diff >= 1.00e-02 (tolerance: < 10%)

**Precision2**: 99th percentile diff = 3.53e-08 (tolerance: < 1.00e+00)

**Summary Statistics** (Common Observations):

| Statistic  |          Stata |         Python |     Difference | Std Difference |
|------------|----------------|----------------|----------------|----------------|
| count      |       2.52e+06 |       2.52e+06 |       2.52e+06 |       2.52e+06 |
| mean       |         0.0042 |         0.0042 |       1.30e-06 |       4.29e-06 |
| std        |         0.3030 |         0.3030 |         0.0019 |         0.0062 |
| min        |      -193.6226 |      -193.6226 |        -0.9269 |        -3.0591 |
| 25%        |      -1.53e-04 |      -1.53e-04 |      -5.93e-11 |      -1.96e-10 |
| 50%        |         0.0000 |         0.0000 |         0.0000 |         0.0000 |
| 75%        |         0.0100 |         0.0100 |       5.96e-11 |       1.97e-10 |
| max        |       195.8306 |       195.8306 |         0.8013 |         2.6445 |

**Regression Analysis** (Python ~ Stata):

- **Model**: python = 0.0000 + 1.0000 * stata
- **R-squared**: 1.0000
- **N observations**: 2,520,037

| Coefficient |     Estimate |    Std Error | t-statistic |   p-value |
|-------------|--------------|--------------|-------------|----------|
| Intercept   |     1.36e-06 |     1.18e-06 |      1.1551 |     0.248 |
| Slope       |       1.0000 |     3.89e-06 | 257308.7854 |     0.000 |

**Feedback**:
- Num observations with std_diff >= TOL_DIFF_1: 401/2520037 (0.016%)
- Stata standard deviation: 3.03e-01

---

### OPLeverage_q

**Status**: ❌ FAILED

**Test Results**:
- Test 1 - Column names: ✅ PASSED
- Test 2 - Superset check: ❌ FAILED (Python missing 65 Stata observations)
- Test 3 - Precision1 check: ✅ PASSED
- Test 4 - Precision2 check: ✅ PASSED

**Columns**: ['OPLeverage_q']

**Observations**:
- Stata:  2,546,734
- Python: 2,546,725
- Common: 2,546,669

**Precision1**: 0.009% obs with std_diff >= 1.00e-02 (tolerance: < 10%)

**Precision2**: 99th percentile diff = 7.72e-08 (tolerance: < 1.00e+00)

**Summary Statistics** (Common Observations):

| Statistic  |          Stata |         Python |     Difference | Std Difference |
|------------|----------------|----------------|----------------|----------------|
| count      |       2.55e+06 |       2.55e+06 |       2.55e+06 |       2.55e+06 |
| mean       |         0.2547 |         0.2547 |       6.51e-06 |       1.35e-05 |
| std        |         0.4836 |         0.4836 |         0.0049 |         0.0101 |
| min        |        -1.4798 |        -1.4798 |        -1.3312 |        -2.7526 |
| 25%        |         0.0824 |         0.0824 |      -3.41e-09 |      -7.06e-09 |
| 50%        |         0.1983 |         0.1983 |      -1.96e-12 |      -4.06e-12 |
| 75%        |         0.3378 |         0.3378 |       3.40e-09 |       7.03e-09 |
| max        |       280.5029 |       280.5029 |         3.8251 |         7.9096 |

**Regression Analysis** (Python ~ Stata):

- **Model**: python = 0.0000 + 1.0000 * stata
- **R-squared**: 0.9999
- **N observations**: 2,546,669

| Coefficient |     Estimate |    Std Error | t-statistic |   p-value |
|-------------|--------------|--------------|-------------|----------|
| Intercept   |     9.93e-06 |     3.46e-06 |      2.8667 |     0.004 |
| Slope       |       1.0000 |     6.34e-06 | 157786.5763 |     0.000 |

**Missing Observations Sample**:
```
 index  permno  yyyymm  OPLeverage_q
     0   10515  199604      0.205151
     1   10515  199605      0.205151
     2   10515  199606      0.205151
     3   11545  199706      0.157832
     4   11545  199707      0.157832
     5   11545  199708      0.157832
     6   12750  198212      0.294411
     7   12750  198301      0.294411
     8   12750  198302      0.294411
     9   12837  198004      0.584828
```

**Feedback**:
- Num observations with std_diff >= TOL_DIFF_1: 235/2546669 (0.009%)
- Stata standard deviation: 4.84e-01

---

### PM_q

**Status**: ❌ FAILED

**Test Results**:
- Test 1 - Column names: ✅ PASSED
- Test 2 - Superset check: ❌ FAILED (Python missing 44 Stata observations)
- Test 3 - Precision1 check: ✅ PASSED
- Test 4 - Precision2 check: ✅ PASSED

**Columns**: ['PM_q']

**Observations**:
- Stata:  2,492,083
- Python: 2,551,862
- Common: 2,492,039

**Precision1**: 0.001% obs with std_diff >= 1.00e-02 (tolerance: < 10%)

**Precision2**: 99th percentile diff = 2.85e-09 (tolerance: < 1.00e+00)

**Summary Statistics** (Common Observations):

| Statistic  |          Stata |         Python |     Difference | Std Difference |
|------------|----------------|----------------|----------------|----------------|
| count      |       2.49e+06 |       2.49e+06 |       2.49e+06 |       2.49e+06 |
| mean       |        -3.9607 |            N/A |            N/A |            N/A |
| std        |       171.1261 |            N/A |            N/A |            N/A |
| min        |    -64982.0000 |           -inf |           -inf |           -inf |
| 25%        |        -0.0250 |        -0.0250 |      -1.28e-09 |      -7.50e-12 |
| 50%        |         0.0340 |         0.0340 |         0.0000 |         0.0000 |
| 75%        |         0.0816 |         0.0816 |       1.28e-09 |       7.46e-12 |
| max        |     18403.0000 |            inf |            inf |            inf |

**Regression Analysis** (Python ~ Stata):

- **Model**: python = nan + nan * stata
- **R-squared**: nan
- **N observations**: 2,492,039

| Coefficient |     Estimate |    Std Error | t-statistic |   p-value |
|-------------|--------------|--------------|-------------|----------|
| Intercept   |          nan |          nan |         nan |       nan |
| Slope       |          nan |          nan |         nan |       nan |

**Missing Observations Sample**:
```
 index  permno  yyyymm     PM_q
     0   11545  199706 0.146023
     1   11545  199707 0.146023
     2   11545  199708 0.146023
     3   12837  198004 0.040997
     4   12837  198005 0.040997
     5   16965  201812 1.705921
     6   16965  201901 1.705921
     7   16965  201902 1.705921
     8   21346  197001 0.006683
     9   21346  197002 0.006683
```

**Feedback**:
- Num observations with std_diff >= TOL_DIFF_1: 31/2492039 (0.001%)
- Stata standard deviation: 1.71e+02

---

### PayoutYield_q

**Status**: ❌ FAILED

**Test Results**:
- Test 1 - Column names: ✅ PASSED
- Test 2 - Superset check: ❌ FAILED (Python missing 40 Stata observations)
- Test 3 - Precision1 check: ✅ PASSED
- Test 4 - Precision2 check: ✅ PASSED

**Columns**: ['PayoutYield_q']

**Observations**:
- Stata:  1,310,000
- Python: 1,361,419
- Common: 1,309,960

**Precision1**: 0.014% obs with std_diff >= 1.00e-02 (tolerance: < 10%)

**Precision2**: 99th percentile diff = 3.45e-08 (tolerance: < 1.00e+00)

**Summary Statistics** (Common Observations):

| Statistic  |          Stata |         Python |     Difference | Std Difference |
|------------|----------------|----------------|----------------|----------------|
| count      |       1.31e+06 |       1.31e+06 |       1.31e+06 |       1.31e+06 |
| mean       |         0.0309 |         0.0309 |       2.34e-06 |       6.80e-06 |
| std        |         0.3442 |         0.3442 |       8.19e-04 |         0.0024 |
| min        |       1.15e-17 |       1.15e-17 |        -0.2764 |        -0.8031 |
| 25%        |         0.0045 |         0.0045 |      -2.39e-10 |      -6.95e-10 |
| 50%        |         0.0106 |         0.0106 |      -1.28e-14 |      -3.71e-14 |
| 75%        |         0.0230 |         0.0230 |       2.40e-10 |       6.97e-10 |
| max        |       217.7060 |       217.7060 |         0.3121 |         0.9067 |

**Regression Analysis** (Python ~ Stata):

- **Model**: python = 0.0000 + 1.0000 * stata
- **R-squared**: 1.0000
- **N observations**: 1,309,960

| Coefficient |     Estimate |    Std Error | t-statistic |   p-value |
|-------------|--------------|--------------|-------------|----------|
| Intercept   |     2.37e-06 |     7.18e-07 |      3.2990 |     0.001 |
| Slope       |       1.0000 |     2.08e-06 | 481071.4981 |     0.000 |

**Missing Observations Sample**:
```
 index  permno  yyyymm  PayoutYield_q
     0   14548  201703       0.054862
     1   14548  201704       0.051537
     2   14548  201705       0.051008
     3   16564  199506       0.002486
     4   16564  199507       0.002983
     5   16564  199508       0.003277
     6   19749  199903       0.001771
     7   19749  199904       0.001898
     8   19749  199905       0.001898
     9   49736  199104       0.000165
```

**Feedback**:
- Num observations with std_diff >= TOL_DIFF_1: 185/1309960 (0.014%)
- Stata standard deviation: 3.44e-01

---

### RD_q

**Status**: ❌ FAILED

**Test Results**:
- Test 1 - Column names: ✅ PASSED
- Test 2 - Superset check: ❌ FAILED (Python missing 35 Stata observations)
- Test 3 - Precision1 check: ✅ PASSED
- Test 4 - Precision2 check: ✅ PASSED

**Columns**: ['RD_q']

**Observations**:
- Stata:  833,583
- Python: 833,614
- Common: 833,548

**Precision1**: 0.004% obs with std_diff >= 1.00e-02 (tolerance: < 10%)

**Precision2**: 99th percentile diff = 5.18e-08 (tolerance: < 1.00e+00)

**Summary Statistics** (Common Observations):

| Statistic  |          Stata |         Python |     Difference | Std Difference |
|------------|----------------|----------------|----------------|----------------|
| count      |    833548.0000 |    833548.0000 |    833548.0000 |    833548.0000 |
| mean       |         0.0298 |         0.0298 |      -4.10e-07 |      -2.48e-06 |
| std        |         0.1656 |         0.1656 |       3.24e-04 |         0.0020 |
| min        |        -1.5270 |        -1.5270 |        -0.2269 |        -1.3700 |
| 25%        |         0.0024 |         0.0024 |      -1.71e-10 |      -1.03e-09 |
| 50%        |         0.0105 |         0.0105 |         0.0000 |         0.0000 |
| 75%        |         0.0278 |         0.0278 |       1.71e-10 |       1.03e-09 |
| max        |        98.7289 |        98.7289 |         0.0221 |         0.1332 |

**Regression Analysis** (Python ~ Stata):

- **Model**: python = -0.0000 + 1.0000 * stata
- **R-squared**: 1.0000
- **N observations**: 833,548

| Coefficient |     Estimate |    Std Error | t-statistic |   p-value |
|-------------|--------------|--------------|-------------|----------|
| Intercept   |    -2.58e-07 |     3.61e-07 |     -0.7162 |     0.474 |
| Slope       |       1.0000 |     2.14e-06 | 466334.4846 |     0.000 |

**Missing Observations Sample**:
```
 index  permno  yyyymm     RD_q
     0   11874  199706 0.008630
     1   11874  199707 0.007477
     2   11874  199708 0.006426
     3   15203  199708 0.029732
     4   15203  199709 0.020131
     5   15203  199710 0.024157
     6   23792  202412 0.036093
     7   23863  202412 0.015423
     8   77671  199903 0.012925
     9   77671  199904 0.014587
```

**Feedback**:
- Num observations with std_diff >= TOL_DIFF_1: 34/833548 (0.004%)
- Stata standard deviation: 1.66e-01

---

### RetNOA_q

**Status**: ❌ FAILED

**Test Results**:
- Test 1 - Column names: ✅ PASSED
- Test 2 - Superset check: ❌ FAILED (Python missing 69 Stata observations)
- Test 3 - Precision1 check: ✅ PASSED
- Test 4 - Precision2 check: ✅ PASSED

**Columns**: ['RetNOA_q']

**Observations**:
- Stata:  2,413,581
- Python: 2,413,603
- Common: 2,413,512

**Precision1**: 0.000% obs with std_diff >= 1.00e-02 (tolerance: < 10%)

**Precision2**: 99th percentile diff = 3.84e-11 (tolerance: < 1.00e+00)

**Summary Statistics** (Common Observations):

| Statistic  |          Stata |         Python |     Difference | Std Difference |
|------------|----------------|----------------|----------------|----------------|
| count      |       2.41e+06 |       2.41e+06 |       2.41e+06 |       2.41e+06 |
| mean       |       -46.8899 |       1.39e+10 |       1.39e+10 |    301349.5028 |
| std        |     46097.8677 |       1.23e+13 |       1.23e+13 |       2.68e+08 |
| min        |      -4.12e+07 |     -7057.0000 |       -22.7626 |      -4.94e-04 |
| 25%        |      -9.84e-04 |      -9.85e-04 |      -1.55e-09 |      -3.37e-14 |
| 50%        |         0.0288 |         0.0288 |      -4.68e-13 |      -1.02e-17 |
| 75%        |         0.0609 |         0.0609 |       1.54e-09 |       3.34e-14 |
| max        |       3.43e+06 |       1.11e+16 |       1.11e+16 |       2.40e+11 |

**Regression Analysis** (Python ~ Stata):

- **Model**: python = 1401917865.6421 + -266360970.0089 * stata
- **R-squared**: 0.9913
- **N observations**: 2,413,512

| Coefficient |     Estimate |    Std Error | t-statistic |   p-value |
|-------------|--------------|--------------|-------------|----------|
| Intercept   |     1.40e+09 |     7.40e+08 |      1.8942 |     0.058 |
| Slope       |    -2.66e+08 |   16055.4966 | -16590.0175 |     0.000 |

**Missing Observations Sample**:
```
 index  permno  yyyymm  RetNOA_q
     0   10515  199607  0.013844
     1   10515  199608  0.013844
     2   10515  199609  0.013844
     3   11545  199706  0.085007
     4   11545  199707  0.085007
     5   11545  199708  0.085007
     6   12750  198303  0.020093
     7   12750  198304  0.020093
     8   12750  198305  0.020093
     9   12837  198007  0.040307
```

**Feedback**:
- Num observations with std_diff >= TOL_DIFF_1: 6/2413512 (0.000%)
- Stata standard deviation: 4.61e+04

---

### SP_q

**Status**: ❌ FAILED

**Test Results**:
- Test 1 - Column names: ✅ PASSED
- Test 2 - Superset check: ❌ FAILED (Python missing 31 Stata observations)
- Test 3 - Precision1 check: ✅ PASSED
- Test 4 - Precision2 check: ✅ PASSED

**Columns**: ['SP_q']

**Observations**:
- Stata:  2,790,383
- Python: 2,790,383
- Common: 2,790,352

**Precision1**: 0.005% obs with std_diff >= 1.00e-02 (tolerance: < 10%)

**Precision2**: 99th percentile diff = 7.95e-08 (tolerance: < 1.00e+00)

**Summary Statistics** (Common Observations):

| Statistic  |          Stata |         Python |     Difference | Std Difference |
|------------|----------------|----------------|----------------|----------------|
| count      |       2.79e+06 |       2.79e+06 |       2.79e+06 |       2.79e+06 |
| mean       |         0.6076 |         0.6076 |      -7.85e-06 |      -4.34e-06 |
| std        |         1.8101 |         1.8101 |         0.0073 |         0.0040 |
| min        |       -31.7352 |       -31.7352 |        -4.6447 |        -2.5660 |
| 25%        |         0.1051 |         0.1051 |      -4.68e-09 |      -2.59e-09 |
| 50%        |         0.2523 |         0.2523 |         0.0000 |         0.0000 |
| 75%        |         0.5972 |         0.5972 |       4.67e-09 |       2.58e-09 |
| max        |       537.3825 |       537.3825 |         3.2442 |         1.7923 |

**Regression Analysis** (Python ~ Stata):

- **Model**: python = -0.0000 + 1.0000 * stata
- **R-squared**: 1.0000
- **N observations**: 2,790,352

| Coefficient |     Estimate |    Std Error | t-statistic |   p-value |
|-------------|--------------|--------------|-------------|----------|
| Intercept   |    -1.60e-06 |     4.61e-06 |     -0.3480 |     0.728 |
| Slope       |       1.0000 |     2.41e-06 | 414132.4540 |     0.000 |

**Missing Observations Sample**:
```
 index  permno  yyyymm     SP_q
     0   11545  199706 0.082241
     1   11545  199707 0.070940
     2   11545  199708 0.063652
     3   12837  198004 0.717490
     4   12837  198005 0.438482
     5   21346  197001 4.004309
     6   21346  197002 3.818679
     7   21346  197003 4.271263
     8   23792  202412 6.755312
     9   23863  202412 0.866520
```

**Feedback**:
- Num observations with std_diff >= TOL_DIFF_1: 127/2790352 (0.005%)
- Stata standard deviation: 1.81e+00

---

### Tax_q

**Status**: ❌ FAILED

**Test Results**:
- Test 1 - Column names: ✅ PASSED
- Test 2 - Superset check: ❌ FAILED (Python missing 52 Stata observations)
- Test 3 - Precision1 check: ✅ PASSED
- Test 4 - Precision2 check: ✅ PASSED

**Columns**: ['Tax_q']

**Observations**:
- Stata:  1,906,647
- Python: 1,906,650
- Common: 1,906,595

**Precision1**: 0.002% obs with std_diff >= 1.00e-02 (tolerance: < 10%)

**Precision2**: 99th percentile diff = 8.61e-09 (tolerance: < 1.00e+00)

**Summary Statistics** (Common Observations):

| Statistic  |          Stata |         Python |     Difference | Std Difference |
|------------|----------------|----------------|----------------|----------------|
| count      |       1.91e+06 |       1.91e+06 |       1.91e+06 |       1.91e+06 |
| mean       |         1.7501 |         1.7501 |       1.28e-05 |       7.96e-07 |
| std        |        16.1404 |        16.1405 |         0.0100 |       6.20e-04 |
| min        |       2.00e-06 |       2.00e-06 |        -0.8325 |        -0.0516 |
| 25%        |         1.2937 |         1.2936 |      -3.00e-08 |      -1.86e-09 |
| 50%        |         1.5463 |         1.5463 |         0.0000 |         0.0000 |
| 75%        |         1.7239 |         1.7239 |       3.03e-08 |       1.87e-09 |
| max        |     10630.3370 |     10630.3365 |         7.0000 |         0.4337 |

**Regression Analysis** (Python ~ Stata):

- **Model**: python = 0.0000 + 1.0000 * stata
- **R-squared**: 1.0000
- **N observations**: 1,906,595

| Coefficient |     Estimate |    Std Error | t-statistic |   p-value |
|-------------|--------------|--------------|-------------|----------|
| Intercept   |     8.44e-06 |     7.29e-06 |      1.1579 |     0.247 |
| Slope       |       1.0000 |     4.49e-07 |    2.23e+06 |     0.000 |

**Missing Observations Sample**:
```
 index  permno  yyyymm    Tax_q
     0   10515  199604 1.604096
     1   10515  199605 1.604096
     2   10515  199606 1.604096
     3   11545  199706 1.449165
     4   11545  199707 1.449165
     5   11545  199708 1.449165
     6   11843  198803 0.940294
     7   11843  198804 0.940294
     8   11843  198805 0.940294
     9   12837  198004 1.881661
```

**Feedback**:
- Num observations with std_diff >= TOL_DIFF_1: 40/1906595 (0.002%)
- Stata standard deviation: 1.61e+01

---

### ZScore

**Status**: ✅ PASSED

**Test Results**:
- Test 1 - Column names: ✅ PASSED
- Test 2 - Superset check: ✅ PASSED
- Test 3 - Precision1 check: ✅ PASSED
- Test 4 - Precision2 check: ✅ PASSED

**Columns**: ['ZScore']

**Observations**:
- Stata:  1,669,459
- Python: 1,669,861
- Common: 1,669,459

**Precision1**: 0.000% obs with std_diff >= 1.00e-02 (tolerance: < 10%)

**Precision2**: 99th percentile diff = 8.31e-08 (tolerance: < 1.00e+00)

**Summary Statistics** (Common Observations):

| Statistic  |          Stata |         Python |     Difference | Std Difference |
|------------|----------------|----------------|----------------|----------------|
| count      |       1.67e+06 |       1.67e+06 |       1.67e+06 |       1.67e+06 |
| mean       |         5.9418 |         5.9418 |       1.93e-07 |       5.67e-09 |
| std        |        33.9664 |        33.9665 |       2.23e-06 |       6.56e-08 |
| min        |      -353.7195 |      -353.7195 |      -1.69e-04 |      -4.96e-06 |
| 25%        |         2.1706 |         2.1706 |      -1.81e-08 |      -5.34e-10 |
| 50%        |         3.4987 |         3.4987 |       5.01e-08 |       1.47e-09 |
| 75%        |         5.4589 |         5.4589 |       1.57e-07 |       4.63e-09 |
| max        |      8802.6084 |      8802.6093 |       8.92e-04 |       2.63e-05 |

**Regression Analysis** (Python ~ Stata):

- **Model**: python = -0.0000 + 1.0000 * stata
- **R-squared**: 1.0000
- **N observations**: 1,669,459

| Coefficient |     Estimate |    Std Error | t-statistic |   p-value |
|-------------|--------------|--------------|-------------|----------|
| Intercept   |    -4.75e-08 |     1.38e-09 |    -34.3687 |     0.000 |
| Slope       |       1.0000 |     4.00e-11 |    2.50e+10 |     0.000 |

**Feedback**:
- Num observations with std_diff >= TOL_DIFF_1: 0/1669459 (0.000%)
- Stata standard deviation: 3.40e+01

---

### ZScore_q

**Status**: ✅ PASSED

**Test Results**:
- Test 1 - Column names: ✅ PASSED
- Test 2 - Superset check: ✅ PASSED
- Test 3 - Precision1 check: ✅ PASSED
- Test 4 - Precision2 check: ✅ PASSED

**Columns**: ['ZScore_q']

**Observations**:
- Stata:  1,214,174
- Python: 1,490,451
- Common: 1,214,174

**Precision1**: 0.003% obs with std_diff >= 1.00e-02 (tolerance: < 10%)

**Precision2**: 99th percentile diff = 7.18e-08 (tolerance: < 1.00e+00)

**Summary Statistics** (Common Observations):

| Statistic  |          Stata |         Python |     Difference | Std Difference |
|------------|----------------|----------------|----------------|----------------|
| count      |       1.21e+06 |       1.21e+06 |       1.21e+06 |       1.21e+06 |
| mean       |         4.2873 |         4.2873 |      -1.95e-06 |      -5.68e-08 |
| std        |        34.3037 |        34.3037 |         0.0081 |       2.36e-04 |
| min        |     -9318.5010 |     -9318.5014 |        -3.3394 |        -0.0973 |
| 25%        |         1.1057 |         1.1057 |      -2.51e-09 |      -7.32e-11 |
| 50%        |         1.9844 |         1.9844 |       3.75e-08 |       1.09e-09 |
| 75%        |         3.4886 |         3.4886 |       1.19e-07 |       3.47e-09 |
| max        |      9482.0879 |      9482.0889 |         2.9884 |         0.0871 |

**Regression Analysis** (Python ~ Stata):

- **Model**: python = -0.0000 + 1.0000 * stata
- **R-squared**: 1.0000
- **N observations**: 1,214,174

| Coefficient |     Estimate |    Std Error | t-statistic |   p-value |
|-------------|--------------|--------------|-------------|----------|
| Intercept   |    -2.07e-06 |     7.40e-06 |     -0.2799 |     0.780 |
| Slope       |       1.0000 |     2.14e-07 |    4.67e+06 |     0.000 |

**Feedback**:
- Num observations with std_diff >= TOL_DIFF_1: 38/1214174 (0.003%)
- Stata standard deviation: 3.43e+01

---

### cashdebt

**Status**: ✅ PASSED

**Test Results**:
- Test 1 - Column names: ✅ PASSED
- Test 2 - Superset check: ✅ PASSED
- Test 3 - Precision1 check: ✅ PASSED
- Test 4 - Precision2 check: ✅ PASSED

**Columns**: ['cashdebt']

**Observations**:
- Stata:  3,267,782
- Python: 3,284,937
- Common: 3,267,782

**Precision1**: 0.000% obs with std_diff >= 1.00e-02 (tolerance: < 10%)

**Precision2**: 99th percentile diff = 3.21e-09 (tolerance: < 1.00e+00)

**Summary Statistics** (Common Observations):

| Statistic  |          Stata |         Python |     Difference | Std Difference |
|------------|----------------|----------------|----------------|----------------|
| count      |       3.27e+06 |       3.27e+06 |       3.27e+06 |       3.27e+06 |
| mean       |         0.3051 |         0.3051 |      -1.49e-06 |      -3.25e-08 |
| std        |        45.8671 |        45.8671 |       7.58e-04 |       1.65e-05 |
| min        |    -10248.0000 |    -10248.0000 |        -0.3728 |        -0.0081 |
| 25%        |         0.0096 |         0.0096 |      -3.26e-09 |      -7.11e-11 |
| 50%        |         0.1142 |         0.1142 |         0.0000 |         0.0000 |
| 75%        |         0.2625 |         0.2625 |       3.26e-09 |       7.11e-11 |
| max        |     13971.0000 |     13971.0000 |         0.0877 |         0.0019 |

**Regression Analysis** (Python ~ Stata):

- **Model**: python = -0.0000 + 1.0000 * stata
- **R-squared**: 1.0000
- **N observations**: 3,267,782

| Coefficient |     Estimate |    Std Error | t-statistic |   p-value |
|-------------|--------------|--------------|-------------|----------|
| Intercept   |    -1.49e-06 |     4.19e-07 |     -3.5652 |     0.000 |
| Slope       |       1.0000 |     9.14e-09 |    1.09e+08 |     0.000 |

**Feedback**:
- Num observations with std_diff >= TOL_DIFF_1: 0/3267782 (0.000%)
- Stata standard deviation: 4.59e+01

---

### cfpq

**Status**: ❌ FAILED

**Test Results**:
- Test 1 - Column names: ✅ PASSED
- Test 2 - Superset check: ❌ FAILED (Python missing 108 Stata observations)
- Test 3 - Precision1 check: ✅ PASSED
- Test 4 - Precision2 check: ✅ PASSED

**Columns**: ['cfpq']

**Observations**:
- Stata:  2,252,622
- Python: 2,268,677
- Common: 2,252,514

**Precision1**: 0.018% obs with std_diff >= 1.00e-02 (tolerance: < 10%)

**Precision2**: 99th percentile diff = 3.70e-08 (tolerance: < 1.00e+00)

**Summary Statistics** (Common Observations):

| Statistic  |          Stata |         Python |     Difference | Std Difference |
|------------|----------------|----------------|----------------|----------------|
| count      |       2.25e+06 |       2.25e+06 |       2.25e+06 |       2.25e+06 |
| mean       |       2.38e-04 |       2.33e-04 |      -5.21e-06 |      -7.26e-06 |
| std        |         0.7177 |         0.7177 |         0.0083 |         0.0115 |
| min        |      -306.2332 |      -306.2333 |        -2.4322 |        -3.3889 |
| 25%        |        -0.0228 |        -0.0228 |      -2.92e-10 |      -4.07e-10 |
| 50%        |         0.0110 |         0.0110 |      -6.36e-14 |      -8.86e-14 |
| 75%        |         0.0389 |         0.0389 |       2.92e-10 |       4.07e-10 |
| max        |       250.7536 |       250.7536 |         7.8358 |        10.9181 |

**Regression Analysis** (Python ~ Stata):

- **Model**: python = -0.0000 + 1.0000 * stata
- **R-squared**: 0.9999
- **N observations**: 2,252,514

| Coefficient |     Estimate |    Std Error | t-statistic |   p-value |
|-------------|--------------|--------------|-------------|----------|
| Intercept   |    -5.20e-06 |     5.51e-06 |     -0.9437 |     0.345 |
| Slope       |       1.0000 |     7.68e-06 | 130210.0985 |     0.000 |

**Missing Observations Sample**:
```
 index  permno  yyyymm      cfpq
     0   11545  199706  0.005822
     1   11545  199707  0.005022
     2   11545  199708  0.004506
     3   12750  198312  0.063750
     4   12750  198401  0.057955
     5   12750  198402  0.057212
     6   12837  198004  0.174127
     7   12837  198005  0.106415
     8   13014  201403 -0.042416
     9   13014  201404 -0.041711
```

**Feedback**:
- Num observations with std_diff >= TOL_DIFF_1: 416/2252514 (0.018%)
- Stata standard deviation: 7.18e-01

---

### depr

**Status**: ❌ FAILED

**Test Results**:
- Test 1 - Column names: ✅ PASSED
- Test 2 - Superset check: ❌ FAILED (Python missing 24 Stata observations)
- Test 3 - Precision1 check: ✅ PASSED
- Test 4 - Precision2 check: ✅ PASSED

**Columns**: ['depr']

**Observations**:
- Stata:  3,462,713
- Python: 3,547,200
- Common: 3,462,689

**Precision1**: 0.001% obs with std_diff >= 1.00e-02 (tolerance: < 10%)

**Precision2**: 99th percentile diff = 8.67e-09 (tolerance: < 1.00e+00)

**Summary Statistics** (Common Observations):

| Statistic  |          Stata |         Python |     Difference | Std Difference |
|------------|----------------|----------------|----------------|----------------|
| count      |       3.46e+06 |       3.46e+06 |       3.46e+06 |       3.46e+06 |
| mean       |         0.4261 |         0.4261 |      -5.28e-06 |      -5.91e-07 |
| std        |         8.9356 |         8.9356 |         0.0028 |       3.14e-04 |
| min        |        -2.3523 |        -2.3523 |        -1.4752 |        -0.1651 |
| 25%        |         0.0910 |         0.0910 |      -3.06e-09 |      -3.43e-10 |
| 50%        |         0.1480 |         0.1480 |         0.0000 |         0.0000 |
| 75%        |         0.2717 |         0.2717 |       2.97e-09 |       3.32e-10 |
| max        |      2457.7500 |      2457.7500 |         0.1795 |         0.0201 |

**Regression Analysis** (Python ~ Stata):

- **Model**: python = -0.0000 + 1.0000 * stata
- **R-squared**: 1.0000
- **N observations**: 3,462,689

| Coefficient |     Estimate |    Std Error | t-statistic |   p-value |
|-------------|--------------|--------------|-------------|----------|
| Intercept   |    -5.26e-06 |     1.51e-06 |     -3.4855 |     0.000 |
| Slope       |       1.0000 |     1.69e-07 |    5.93e+06 |     0.000 |

**Missing Observations Sample**:
```
 index  permno  yyyymm     depr
     0   12373  202406 0.029963
     1   12373  202407 0.029963
     2   12373  202408 0.029963
     3   12373  202409 0.029963
     4   12373  202410 0.029963
     5   12373  202411 0.029963
     6   12373  202412 0.029963
     7   12373  202501 0.029963
     8   12373  202502 0.029963
     9   12373  202503 0.029963
```

**Feedback**:
- Num observations with std_diff >= TOL_DIFF_1: 36/3462689 (0.001%)
- Stata standard deviation: 8.94e+00

---

### fgr5yrNoLag

**Status**: ❌ FAILED

**Test Results**:
- Test 1 - Column names: ✅ PASSED
- Test 2 - Superset check: ❌ FAILED (Python missing 2116 Stata observations)
- Test 3 - Precision1 check: ✅ PASSED
- Test 4 - Precision2 check: ✅ PASSED

**Columns**: ['fgr5yrNoLag']

**Observations**:
- Stata:  996,237
- Python: 1,033,389
- Common: 994,121

**Precision1**: 0.075% obs with std_diff >= 1.00e-02 (tolerance: < 10%)

**Precision2**: 99th percentile diff = 1.43e-07 (tolerance: < 1.00e+00)

**Summary Statistics** (Common Observations):

| Statistic  |          Stata |         Python |     Difference | Std Difference |
|------------|----------------|----------------|----------------|----------------|
| count      |    994121.0000 |    994121.0000 |    994121.0000 |    994121.0000 |
| mean       |        16.8659 |        16.8658 |      -3.91e-05 |      -2.79e-06 |
| std        |        14.0128 |        14.0129 |         0.3335 |         0.0238 |
| min        |      -899.2000 |      -899.2000 |       -62.1000 |        -4.4317 |
| 25%        |        10.5000 |        10.5000 |         0.0000 |         0.0000 |
| 50%        |        15.0000 |        15.0000 |         0.0000 |         0.0000 |
| 75%        |        20.0000 |        20.0000 |         0.0000 |         0.0000 |
| max        |      2097.8000 |      2097.8000 |        90.3000 |         6.4441 |

**Regression Analysis** (Python ~ Stata):

- **Model**: python = 0.0046 + 0.9997 * stata
- **R-squared**: 0.9994
- **N observations**: 994,121

| Coefficient |     Estimate |    Std Error | t-statistic |   p-value |
|-------------|--------------|--------------|-------------|----------|
| Intercept   |       0.0046 |     5.23e-04 |      8.7028 |     0.000 |
| Slope       |       0.9997 |     2.39e-05 |  41888.2260 |     0.000 |

**Missing Observations Sample**:
```
 index  permno  yyyymm  fgr5yrNoLag
     0   11406  199204         20.0
     1   11406  199205         15.0
     2   11406  199206         15.0
     3   11406  199207         15.0
     4   11406  199208         15.0
     5   11406  199209         15.0
     6   11406  199210         15.0
     7   11406  199211         15.0
     8   11406  199212         15.0
     9   11406  199301         15.0
```

**Feedback**:
- Num observations with std_diff >= TOL_DIFF_1: 750/994121 (0.075%)
- Stata standard deviation: 1.40e+01

---

### pchdepr

**Status**: ❌ FAILED

**Test Results**:
- Test 1 - Column names: ✅ PASSED
- Test 2 - Superset check: ❌ FAILED (Python missing 24 Stata observations)
- Test 3 - Precision1 check: ✅ PASSED
- Test 4 - Precision2 check: ✅ PASSED

**Columns**: ['pchdepr']

**Observations**:
- Stata:  3,050,498
- Python: 3,235,524
- Common: 3,050,474

**Precision1**: 0.002% obs with std_diff >= 1.00e-02 (tolerance: < 10%)

**Precision2**: 99th percentile diff = 2.31e-09 (tolerance: < 1.00e+00)

**Summary Statistics** (Common Observations):

| Statistic  |          Stata |         Python |     Difference | Std Difference |
|------------|----------------|----------------|----------------|----------------|
| count      |       3.05e+06 |       3.05e+06 |       3.05e+06 |       3.05e+06 |
| mean       |         0.4972 |         0.4971 |      -8.88e-05 |      -2.30e-06 |
| std        |        38.5914 |        38.5913 |         0.0375 |       9.70e-04 |
| min        |       -75.5903 |       -75.5903 |       -18.3420 |        -0.4753 |
| 25%        |        -0.0906 |        -0.0906 |      -2.22e-09 |      -5.74e-11 |
| 50%        |         0.0251 |         0.0251 |         0.0000 |         0.0000 |
| 75%        |         0.1646 |         0.1646 |       2.22e-09 |       5.76e-11 |
| max        |     15513.7030 |     15513.7034 |         1.3903 |         0.0360 |

**Regression Analysis** (Python ~ Stata):

- **Model**: python = -0.0001 + 1.0000 * stata
- **R-squared**: 1.0000
- **N observations**: 3,050,474

| Coefficient |     Estimate |    Std Error | t-statistic |   p-value |
|-------------|--------------|--------------|-------------|----------|
| Intercept   |    -8.83e-05 |     2.14e-05 |     -4.1186 |     0.000 |
| Slope       |       1.0000 |     5.56e-07 |    1.80e+06 |     0.000 |

**Missing Observations Sample**:
```
 index  permno  yyyymm  pchdepr
     0   12373  202406 0.091209
     1   12373  202407 0.091209
     2   12373  202408 0.091209
     3   12373  202409 0.091209
     4   12373  202410 0.091209
     5   12373  202411 0.091209
     6   12373  202412 0.091209
     7   12373  202501 0.091209
     8   12373  202502 0.091209
     9   12373  202503 0.091209
```

**Feedback**:
- Num observations with std_diff >= TOL_DIFF_1: 48/3050474 (0.002%)
- Stata standard deviation: 3.86e+01

---

### pchquick

**Status**: ❌ FAILED

**Test Results**:
- Test 1 - Column names: ✅ PASSED
- Test 2 - Superset check: ❌ FAILED (Python missing 273 Stata observations)
- Test 3 - Precision1 check: ✅ PASSED
- Test 4 - Precision2 check: ✅ PASSED

**Columns**: ['pchquick']

**Observations**:
- Stata:  3,339,639
- Python: 3,619,047
- Common: 3,339,366

**Precision1**: 0.238% obs with std_diff >= 1.00e-02 (tolerance: < 10%)

**Precision2**: 99th percentile diff = 2.76e-09 (tolerance: < 1.00e+00)

**Summary Statistics** (Common Observations):

| Statistic  |          Stata |         Python |     Difference | Std Difference |
|------------|----------------|----------------|----------------|----------------|
| count      |       3.34e+06 |       3.34e+06 |       3.34e+06 |       3.34e+06 |
| mean       |         0.2976 |         0.3265 |         0.0289 |       6.74e-04 |
| std        |        42.9374 |        43.4447 |         6.6214 |         0.1542 |
| min        |      -111.5194 |      -111.5194 |        -9.9321 |        -0.2313 |
| 25%        |        -0.1626 |        -0.1643 |      -2.32e-09 |      -5.39e-11 |
| 50%        |         0.0000 |         0.0000 |         0.0000 |         0.0000 |
| 75%        |         0.1243 |         0.1265 |       2.34e-09 |       5.44e-11 |
| max        |     19726.1780 |     19726.1780 |      2879.3158 |        67.0585 |

**Regression Analysis** (Python ~ Stata):

- **Model**: python = 0.0290 + 1.0000 * stata
- **R-squared**: 0.9768
- **N observations**: 3,339,366

| Coefficient |     Estimate |    Std Error | t-statistic |   p-value |
|-------------|--------------|--------------|-------------|----------|
| Intercept   |       0.0290 |       0.0036 |      7.9896 |     0.000 |
| Slope       |       1.0000 |     8.44e-05 |  11849.9494 |     0.000 |

**Missing Observations Sample**:
```
 index  permno  yyyymm  pchquick
     0   10281  199711       0.0
     1   10281  199712       0.0
     2   10281  199801       0.0
     3   10281  199802       0.0
     4   10281  199803       0.0
     5   10281  199804       0.0
     6   10281  199805       0.0
     7   11396  199406       0.0
     8   11396  199407       0.0
     9   11396  199408       0.0
```

**Feedback**:
- Num observations with std_diff >= TOL_DIFF_1: 7959/3339366 (0.238%)
- Stata standard deviation: 4.29e+01

---

### quick

**Status**: ✅ PASSED

**Test Results**:
- Test 1 - Column names: ✅ PASSED
- Test 2 - Superset check: ✅ PASSED
- Test 3 - Precision1 check: ✅ PASSED
- Test 4 - Precision2 check: ✅ PASSED

**Columns**: ['quick']

**Observations**:
- Stata:  3,065,278
- Python: 3,625,095
- Common: 3,065,278

**Precision1**: 0.000% obs with std_diff >= 1.00e-02 (tolerance: < 10%)

**Precision2**: 99th percentile diff = 1.06e-08 (tolerance: < 1.00e+00)

**Summary Statistics** (Common Observations):

| Statistic  |          Stata |         Python |     Difference | Std Difference |
|------------|----------------|----------------|----------------|----------------|
| count      |       3.07e+06 |       3.07e+06 |       3.07e+06 |       3.07e+06 |
| mean       |         2.7309 |         2.7309 |      -2.05e-06 |      -3.62e-08 |
| std        |        56.6440 |        56.6440 |       9.36e-04 |       1.65e-05 |
| min        |       -41.2750 |       -41.2750 |        -0.4710 |        -0.0083 |
| 25%        |         0.8507 |         0.8507 |      -2.56e-08 |      -4.52e-10 |
| 50%        |         1.3264 |         1.3264 |         0.0000 |         0.0000 |
| 75%        |         2.2630 |         2.2630 |       2.57e-08 |       4.54e-10 |
| max        |     25204.0000 |     25204.0000 |       1.67e-04 |       2.94e-06 |

**Regression Analysis** (Python ~ Stata):

- **Model**: python = -0.0000 + 1.0000 * stata
- **R-squared**: 1.0000
- **N observations**: 3,065,278

| Coefficient |     Estimate |    Std Error | t-statistic |   p-value |
|-------------|--------------|--------------|-------------|----------|
| Intercept   |    -2.05e-06 |     5.35e-07 |     -3.8297 |     0.000 |
| Slope       |       1.0000 |     9.44e-09 |    1.06e+08 |     0.000 |

**Feedback**:
- Num observations with std_diff >= TOL_DIFF_1: 0/3065278 (0.000%)
- Stata standard deviation: 5.66e+01

---

### rd_sale

**Status**: ✅ PASSED

**Test Results**:
- Test 1 - Column names: ✅ PASSED
- Test 2 - Superset check: ✅ PASSED
- Test 3 - Precision1 check: ✅ PASSED
- Test 4 - Precision2 check: ✅ PASSED

**Columns**: ['rd_sale']

**Observations**:
- Stata:  1,207,848
- Python: 1,254,467
- Common: 1,207,848

**Precision1**: 0.000% obs with std_diff >= 1.00e-02 (tolerance: < 10%)

**Precision2**: 99th percentile diff = 4.06e-09 (tolerance: < 1.00e+00)

**Summary Statistics** (Common Observations):

| Statistic  |          Stata |         Python |     Difference | Std Difference |
|------------|----------------|----------------|----------------|----------------|
| count      |       1.21e+06 |       1.21e+06 |       1.21e+06 |       1.21e+06 |
| mean       |         5.1262 |         5.1262 |      -5.92e-09 |      -3.17e-11 |
| std        |       186.9904 |       186.9904 |       5.03e-06 |       2.69e-08 |
| min        |     -1037.3235 |     -1037.3235 |        -0.0013 |      -7.13e-06 |
| 25%        |         0.0151 |         0.0151 |      -8.68e-10 |      -4.64e-12 |
| 50%        |         0.0509 |         0.0509 |      -5.55e-17 |      -2.97e-19 |
| 75%        |         0.1546 |         0.1546 |       8.73e-10 |       4.67e-12 |
| max        |     42070.6680 |     42070.6667 |       7.27e-04 |       3.89e-06 |

**Regression Analysis** (Python ~ Stata):

- **Model**: python = 0.0000 + 1.0000 * stata
- **R-squared**: 1.0000
- **N observations**: 1,207,848

| Coefficient |     Estimate |    Std Error | t-statistic |   p-value |
|-------------|--------------|--------------|-------------|----------|
| Intercept   |     6.41e-08 |     3.94e-09 |     16.2719 |     0.000 |
| Slope       |       1.0000 |     2.11e-11 |    4.75e+10 |     0.000 |

**Feedback**:
- Num observations with std_diff >= TOL_DIFF_1: 0/1207848 (0.000%)
- Stata standard deviation: 1.87e+02

---

### rd_sale_q

**Status**: ❌ FAILED

**Test Results**:
- Test 1 - Column names: ✅ PASSED
- Test 2 - Superset check: ❌ FAILED (Python missing 20 Stata observations)
- Test 3 - Precision1 check: ✅ PASSED
- Test 4 - Precision2 check: ✅ PASSED

**Columns**: ['rd_sale_q']

**Observations**:
- Stata:  566,115
- Python: 598,403
- Common: 566,095

**Precision1**: 0.001% obs with std_diff >= 1.00e-02 (tolerance: < 10%)

**Precision2**: 99th percentile diff = 6.67e-09 (tolerance: < 1.00e+00)

**Summary Statistics** (Common Observations):

| Statistic  |          Stata |         Python |     Difference | Std Difference |
|------------|----------------|----------------|----------------|----------------|
| count      |    566095.0000 |    566095.0000 |    566095.0000 |    566095.0000 |
| mean       |         7.6749 |         7.6750 |       1.35e-04 |       7.35e-07 |
| std        |       183.2099 |       183.2100 |         0.1055 |       5.76e-04 |
| min        |     -3937.0000 |     -3937.0000 |       -29.0278 |        -0.1584 |
| 25%        |         0.0468 |         0.0468 |      -2.04e-09 |      -1.11e-11 |
| 50%        |         0.1117 |         0.1117 |      -2.22e-16 |      -1.21e-18 |
| 75%        |         0.2509 |         0.2509 |       1.93e-09 |       1.05e-11 |
| max        |     31684.3340 |     31684.3333 |        52.2216 |         0.2850 |

**Regression Analysis** (Python ~ Stata):

- **Model**: python = 0.0001 + 1.0000 * stata
- **R-squared**: 1.0000
- **N observations**: 566,095

| Coefficient |     Estimate |    Std Error | t-statistic |   p-value |
|-------------|--------------|--------------|-------------|----------|
| Intercept   |     1.34e-04 |     1.40e-04 |      0.9560 |     0.339 |
| Slope       |       1.0000 |     7.65e-07 |    1.31e+06 |     0.000 |

**Missing Observations Sample**:
```
 index  permno  yyyymm  rd_sale_q
     0   11874  199806   0.008565
     1   11874  199807   0.008565
     2   11874  199808   0.008565
     3   15203  199808   0.065449
     4   15203  199809   0.065449
     5   15203  199810   0.065449
     6   77671  200003   0.039044
     7   77671  200004   0.039044
     8   77671  200005   0.039044
     9   79117  199803   0.056410
```

**Feedback**:
- Num observations with std_diff >= TOL_DIFF_1: 3/566095 (0.001%)
- Stata standard deviation: 1.83e+02

---

### roic

**Status**: ✅ PASSED

**Test Results**:
- Test 1 - Column names: ✅ PASSED
- Test 2 - Superset check: ✅ PASSED
- Test 3 - Precision1 check: ✅ PASSED
- Test 4 - Precision2 check: ✅ PASSED

**Columns**: ['roic']

**Observations**:
- Stata:  3,409,380
- Python: 3,410,772
- Common: 3,409,380

**Precision1**: 0.014% obs with std_diff >= 1.00e-02 (tolerance: < 10%)

**Precision2**: 99th percentile diff = 3.38e-23 (tolerance: < 1.00e+00)

**Summary Statistics** (Common Observations):

| Statistic  |          Stata |         Python |     Difference | Std Difference |
|------------|----------------|----------------|----------------|----------------|
| count      |       3.41e+06 |       3.41e+06 |       3.41e+06 |       3.41e+06 |
| mean       |       1.87e+13 |            inf |            inf |            inf |
| std        |       5.82e+15 |            N/A |            N/A |            N/A |
| min        |      -3.62e+17 |      -3.91e+16 |      -3.40e+16 |        -5.8459 |
| 25%        |        -0.0121 |        -0.0121 |      -1.87e-09 |      -3.22e-25 |
| 50%        |         0.0586 |         0.0586 |         0.0000 |         0.0000 |
| 75%        |         0.1262 |         0.1262 |       1.86e-09 |       3.20e-25 |
| max        |       1.79e+18 |            inf |            inf |            inf |

**Regression Analysis** (Python ~ Stata):

- **Model**: python = nan + nan * stata
- **R-squared**: nan
- **N observations**: 3,409,380

| Coefficient |     Estimate |    Std Error | t-statistic |   p-value |
|-------------|--------------|--------------|-------------|----------|
| Intercept   |          nan |          nan |         nan |       nan |
| Slope       |          nan |          nan |         nan |       nan |

**Feedback**:
- Num observations with std_diff >= TOL_DIFF_1: 492/3409380 (0.014%)
- Stata standard deviation: 5.82e+15

---

### salecash

**Status**: ✅ PASSED

**Test Results**:
- Test 1 - Column names: ✅ PASSED
- Test 2 - Superset check: ✅ PASSED
- Test 3 - Precision1 check: ✅ PASSED
- Test 4 - Precision2 check: ✅ PASSED

**Columns**: ['salecash']

**Observations**:
- Stata:  3,583,392
- Python: 3,616,983
- Common: 3,583,392

**Precision1**: 0.000% obs with std_diff >= 1.00e-02 (tolerance: < 10%)

**Precision2**: 99th percentile diff = 6.55e-09 (tolerance: < 1.00e+00)

**Summary Statistics** (Common Observations):

| Statistic  |          Stata |         Python |     Difference | Std Difference |
|------------|----------------|----------------|----------------|----------------|
| count      |       3.58e+06 |       3.58e+06 |       3.58e+06 |       3.58e+06 |
| mean       |       107.6003 |       107.6001 |      -1.50e-04 |      -5.72e-08 |
| std        |      2627.3839 |      2627.3839 |         0.0798 |       3.04e-05 |
| min        |     -1591.6364 |     -1591.6364 |       -43.5883 |        -0.0166 |
| 25%        |         2.2471 |         2.2471 |      -1.37e-07 |      -5.21e-11 |
| 50%        |         8.4673 |         8.4673 |         0.0000 |         0.0000 |
| 75%        |        30.7168 |        30.7168 |       1.35e-07 |       5.12e-11 |
| max        |    519704.0000 |    519704.0000 |         0.1507 |       5.74e-05 |

**Regression Analysis** (Python ~ Stata):

- **Model**: python = -0.0002 + 1.0000 * stata
- **R-squared**: 1.0000
- **N observations**: 3,583,392

| Coefficient |     Estimate |    Std Error | t-statistic |   p-value |
|-------------|--------------|--------------|-------------|----------|
| Intercept   |    -1.50e-04 |     4.22e-05 |     -3.5625 |     0.000 |
| Slope       |       1.0000 |     1.60e-08 |    6.23e+07 |     0.000 |

**Feedback**:
- Num observations with std_diff >= TOL_DIFF_1: 12/3583392 (0.000%)
- Stata standard deviation: 2.63e+03

---

### saleinv

**Status**: ✅ PASSED

**Test Results**:
- Test 1 - Column names: ✅ PASSED
- Test 2 - Superset check: ✅ PASSED
- Test 3 - Precision1 check: ✅ PASSED
- Test 4 - Precision2 check: ✅ PASSED

**Columns**: ['saleinv']

**Observations**:
- Stata:  2,730,607
- Python: 3,616,983
- Common: 2,730,607

**Precision1**: 0.000% obs with std_diff >= 1.00e-02 (tolerance: < 10%)

**Precision2**: 99th percentile diff = 3.12e-09 (tolerance: < 1.00e+00)

**Summary Statistics** (Common Observations):

| Statistic  |          Stata |         Python |     Difference | Std Difference |
|------------|----------------|----------------|----------------|----------------|
| count      |       2.73e+06 |       2.73e+06 |       2.73e+06 |       2.73e+06 |
| mean       |        61.9969 |        61.9969 |       1.38e-07 |       3.95e-11 |
| std        |      3492.9321 |      3492.9321 |       1.12e-04 |       3.22e-08 |
| min        |    -14573.0000 |    -14573.0000 |        -0.0233 |      -6.68e-06 |
| 25%        |         4.6053 |         4.6053 |      -1.57e-07 |      -4.49e-11 |
| 50%        |         7.6793 |         7.6793 |         0.0000 |         0.0000 |
| 75%        |        17.8215 |        17.8215 |       1.55e-07 |       4.45e-11 |
| max        |       1.05e+06 |       1.05e+06 |         0.0387 |       1.11e-05 |

**Regression Analysis** (Python ~ Stata):

- **Model**: python = 0.0000 + 1.0000 * stata
- **R-squared**: 1.0000
- **N observations**: 2,730,607

| Coefficient |     Estimate |    Std Error | t-statistic |   p-value |
|-------------|--------------|--------------|-------------|----------|
| Intercept   |     4.03e-07 |     6.74e-08 |      5.9744 |     0.000 |
| Slope       |       1.0000 |     1.93e-11 |    5.18e+10 |     0.000 |

**Feedback**:
- Num observations with std_diff >= TOL_DIFF_1: 0/2730607 (0.000%)
- Stata standard deviation: 3.49e+03

---

### salerec

**Status**: ✅ PASSED

**Test Results**:
- Test 1 - Column names: ✅ PASSED
- Test 2 - Superset check: ✅ PASSED
- Test 3 - Precision1 check: ✅ PASSED
- Test 4 - Precision2 check: ✅ PASSED

**Columns**: ['salerec']

**Observations**:
- Stata:  3,451,784
- Python: 3,616,983
- Common: 3,451,784

**Precision1**: 0.005% obs with std_diff >= 1.00e-02 (tolerance: < 10%)

**Precision2**: 99th percentile diff = 2.11e-08 (tolerance: < 1.00e+00)

**Summary Statistics** (Common Observations):

| Statistic  |          Stata |         Python |     Difference | Std Difference |
|------------|----------------|----------------|----------------|----------------|
| count      |       3.45e+06 |       3.45e+06 |       3.45e+06 |       3.45e+06 |
| mean       |        16.3739 |        16.3744 |       5.33e-04 |       2.54e-06 |
| std        |       209.4212 |       209.4212 |         0.0834 |       3.98e-04 |
| min        |    -21796.0000 |    -21796.0000 |        -0.6092 |        -0.0029 |
| 25%        |         3.6746 |         3.6749 |      -1.08e-07 |      -5.16e-10 |
| 50%        |         5.9289 |         5.9293 |         0.0000 |         0.0000 |
| 75%        |         9.1589 |         9.1598 |       1.08e-07 |       5.14e-10 |
| max        |     47246.0000 |     47246.0000 |        17.2986 |         0.0826 |

**Regression Analysis** (Python ~ Stata):

- **Model**: python = 0.0005 + 1.0000 * stata
- **R-squared**: 1.0000
- **N observations**: 3,451,784

| Coefficient |     Estimate |    Std Error | t-statistic |   p-value |
|-------------|--------------|--------------|-------------|----------|
| Intercept   |     5.36e-04 |     4.50e-05 |     11.8914 |     0.000 |
| Slope       |       1.0000 |     2.14e-07 |    4.66e+06 |     0.000 |

**Feedback**:
- Num observations with std_diff >= TOL_DIFF_1: 168/3451784 (0.005%)
- Stata standard deviation: 2.09e+02

---

### secured

**Status**: ✅ PASSED

**Test Results**:
- Test 1 - Column names: ✅ PASSED
- Test 2 - Superset check: ✅ PASSED
- Test 3 - Precision1 check: ✅ PASSED
- Test 4 - Precision2 check: ✅ PASSED

**Columns**: ['secured']

**Observations**:
- Stata:  3,624,363
- Python: 3,625,095
- Common: 3,624,363

**Precision1**: 0.004% obs with std_diff >= 1.00e-02 (tolerance: < 10%)

**Precision2**: 99th percentile diff = 8.39e-08 (tolerance: < 1.00e+00)

**Summary Statistics** (Common Observations):

| Statistic  |          Stata |         Python |     Difference | Std Difference |
|------------|----------------|----------------|----------------|----------------|
| count      |       3.62e+06 |       3.62e+06 |       3.62e+06 |       3.62e+06 |
| mean       |         0.1995 |         0.1995 |       3.89e-06 |       1.13e-05 |
| std        |         0.3454 |         0.3454 |         0.0015 |         0.0042 |
| min        |      -7.96e-05 |      -7.96e-05 |        -0.1626 |        -0.4709 |
| 25%        |         0.0000 |         0.0000 |         0.0000 |         0.0000 |
| 50%        |         0.0000 |         0.0000 |         0.0000 |         0.0000 |
| 75%        |         0.3028 |         0.3028 |         0.0000 |         0.0000 |
| max        |        48.7452 |        48.7452 |         0.7243 |         2.0969 |

**Regression Analysis** (Python ~ Stata):

- **Model**: python = 0.0000 + 1.0000 * stata
- **R-squared**: 1.0000
- **N observations**: 3,624,363

| Coefficient |     Estimate |    Std Error | t-statistic |   p-value |
|-------------|--------------|--------------|-------------|----------|
| Intercept   |     5.20e-06 |     8.80e-07 |      5.9060 |     0.000 |
| Slope       |       1.0000 |     2.21e-06 | 453400.1353 |     0.000 |

**Feedback**:
- Num observations with std_diff >= TOL_DIFF_1: 156/3624363 (0.004%)
- Stata standard deviation: 3.45e-01

---

### securedind

**Status**: ✅ PASSED

**Test Results**:
- Test 1 - Column names: ✅ PASSED
- Test 2 - Superset check: ✅ PASSED
- Test 3 - Precision1 check: ✅ PASSED
- Test 4 - Precision2 check: ✅ PASSED

**Columns**: ['securedind']

**Observations**:
- Stata:  3,624,363
- Python: 3,625,095
- Common: 3,624,363

**Precision1**: 0.004% obs with std_diff >= 1.00e-02 (tolerance: < 10%)

**Precision2**: 99th percentile diff = 0.00e+00 (tolerance: < 1.00e+00)

**Summary Statistics** (Common Observations):

| Statistic  |          Stata |         Python |     Difference | Std Difference |
|------------|----------------|----------------|----------------|----------------|
| count      |       3.62e+06 |       3.62e+06 |       3.62e+06 |       3.62e+06 |
| mean       |         0.4092 |         0.4092 |       2.65e-05 |       5.39e-05 |
| std        |         0.4917 |         0.4917 |         0.0063 |         0.0128 |
| min        |         0.0000 |         0.0000 |        -1.0000 |        -2.0338 |
| 25%        |         0.0000 |         0.0000 |         0.0000 |         0.0000 |
| 50%        |         0.0000 |         0.0000 |         0.0000 |         0.0000 |
| 75%        |         1.0000 |         1.0000 |         0.0000 |         0.0000 |
| max        |         1.0000 |         1.0000 |         1.0000 |         2.0338 |

**Regression Analysis** (Python ~ Stata):

- **Model**: python = 0.0001 + 0.9999 * stata
- **R-squared**: 0.9998
- **N observations**: 3,624,363

| Coefficient |     Estimate |    Std Error | t-statistic |   p-value |
|-------------|--------------|--------------|-------------|----------|
| Intercept   |     5.60e-05 |     4.31e-06 |     13.0100 |     0.000 |
| Slope       |       0.9999 |     6.73e-06 | 148495.0598 |     0.000 |

**Feedback**:
- Num observations with std_diff >= TOL_DIFF_1: 144/3624363 (0.004%)
- Stata standard deviation: 4.92e-01

---

### sgr

**Status**: ✅ PASSED

**Test Results**:
- Test 1 - Column names: ✅ PASSED
- Test 2 - Superset check: ✅ PASSED
- Test 3 - Precision1 check: ✅ PASSED
- Test 4 - Precision2 check: ✅ PASSED

**Columns**: ['sgr']

**Observations**:
- Stata:  3,231,761
- Python: 3,303,855
- Common: 3,231,761

**Precision1**: 0.001% obs with std_diff >= 1.00e-02 (tolerance: < 10%)

**Precision2**: 99th percentile diff = 1.88e-09 (tolerance: < 1.00e+00)

**Summary Statistics** (Common Observations):

| Statistic  |          Stata |         Python |     Difference | Std Difference |
|------------|----------------|----------------|----------------|----------------|
| count      |       3.23e+06 |       3.23e+06 |       3.23e+06 |       3.23e+06 |
| mean       |         0.7025 |         0.7025 |       3.84e-08 |       8.18e-10 |
| std        |        46.9281 |        46.9281 |         0.0026 |       5.61e-05 |
| min        |      -237.0000 |      -237.0000 |        -1.0899 |        -0.0232 |
| 25%        |        -0.0210 |        -0.0210 |      -2.50e-09 |      -5.32e-11 |
| 50%        |         0.0863 |         0.0863 |         0.0000 |         0.0000 |
| 75%        |         0.2252 |         0.2252 |       2.53e-09 |       5.39e-11 |
| max        |     12739.0000 |     12739.0000 |         0.7897 |         0.0168 |

**Regression Analysis** (Python ~ Stata):

- **Model**: python = 0.0000 + 1.0000 * stata
- **R-squared**: 1.0000
- **N observations**: 3,231,761

| Coefficient |     Estimate |    Std Error | t-statistic |   p-value |
|-------------|--------------|--------------|-------------|----------|
| Intercept   |     3.48e-08 |     1.46e-06 |      0.0238 |     0.981 |
| Slope       |       1.0000 |     3.12e-08 |    3.21e+07 |     0.000 |

**Feedback**:
- Num observations with std_diff >= TOL_DIFF_1: 24/3231761 (0.001%)
- Stata standard deviation: 4.69e+01

---

### sgr_q

**Status**: ❌ FAILED

**Test Results**:
- Test 1 - Column names: ✅ PASSED
- Test 2 - Superset check: ❌ FAILED (Python missing 17 Stata observations)
- Test 3 - Precision1 check: ✅ PASSED
- Test 4 - Precision2 check: ✅ PASSED

**Columns**: ['sgr_q']

**Observations**:
- Stata:  2,457,701
- Python: 2,465,942
- Common: 2,457,684

**Precision1**: 0.001% obs with std_diff >= 1.00e-02 (tolerance: < 10%)

**Precision2**: 99th percentile diff = 3.03e-10 (tolerance: < 1.00e+00)

**Summary Statistics** (Common Observations):

| Statistic  |          Stata |         Python |     Difference | Std Difference |
|------------|----------------|----------------|----------------|----------------|
| count      |       2.46e+06 |       2.46e+06 |       2.46e+06 |       2.46e+06 |
| mean       |         1.0671 |         1.0670 |      -1.32e-04 |      -4.61e-07 |
| std        |       286.5288 |       286.5288 |         0.1414 |       4.93e-04 |
| min        |     -3092.0000 |     -3092.0000 |      -146.0200 |        -0.5096 |
| 25%        |        -0.0374 |        -0.0374 |      -2.58e-09 |      -8.99e-12 |
| 50%        |         0.0794 |         0.0794 |         0.0000 |         0.0000 |
| 75%        |         0.2229 |         0.2229 |       2.55e-09 |       8.91e-12 |
| max        |    251440.0000 |    251440.0000 |        15.0962 |         0.0527 |

**Regression Analysis** (Python ~ Stata):

- **Model**: python = -0.0001 + 1.0000 * stata
- **R-squared**: 1.0000
- **N observations**: 2,457,684

| Coefficient |     Estimate |    Std Error | t-statistic |   p-value |
|-------------|--------------|--------------|-------------|----------|
| Intercept   |    -1.32e-04 |     9.02e-05 |     -1.4634 |     0.143 |
| Slope       |       1.0000 |     3.15e-07 |    3.18e+06 |     0.000 |

**Missing Observations Sample**:
```
 index  permno  yyyymm     sgr_q
     0   11545  199806  1.767560
     1   11545  199807  1.767560
     2   11545  199808  1.767560
     3   21346  197101  0.072523
     4   21346  197102  0.072523
     5   21346  197103  0.072523
     6   28855  197608 -0.145659
     7   64717  199305  7.151463
     8   79352  199806  0.654237
     9   79352  199807  0.654237
```

**Feedback**:
- Num observations with std_diff >= TOL_DIFF_1: 30/2457684 (0.001%)
- Stata standard deviation: 2.87e+02

---

### tang_q

**Status**: ❌ FAILED

**Test Results**:
- Test 1 - Column names: ✅ PASSED
- Test 2 - Superset check: ❌ FAILED (Python missing 3 Stata observations)
- Test 3 - Precision1 check: ✅ PASSED
- Test 4 - Precision2 check: ✅ PASSED

**Columns**: ['tang_q']

**Observations**:
- Stata:  1,675,098
- Python: 2,417,377
- Common: 1,675,095

**Precision1**: 0.010% obs with std_diff >= 1.00e-02 (tolerance: < 10%)

**Precision2**: 99th percentile diff = 1.54e-07 (tolerance: < 1.00e+00)

**Summary Statistics** (Common Observations):

| Statistic  |          Stata |         Python |     Difference | Std Difference |
|------------|----------------|----------------|----------------|----------------|
| count      |       1.68e+06 |       1.68e+06 |       1.68e+06 |       1.68e+06 |
| mean       |         0.6565 |         0.6565 |      -1.34e-06 |      -3.88e-06 |
| std        |         0.3446 |         0.3447 |         0.0077 |         0.0224 |
| min        |        -0.4077 |        -0.4077 |        -0.9940 |        -2.8845 |
| 25%        |         0.5451 |         0.5451 |      -1.26e-08 |      -3.66e-08 |
| 50%        |         0.6594 |         0.6594 |       2.77e-11 |       8.04e-11 |
| 75%        |         0.7667 |         0.7667 |       1.27e-08 |       3.68e-08 |
| max        |       158.7655 |       158.7656 |         5.5119 |        15.9951 |

**Regression Analysis** (Python ~ Stata):

- **Model**: python = 0.0000 + 1.0000 * stata
- **R-squared**: 0.9995
- **N observations**: 1,675,095

| Coefficient |     Estimate |    Std Error | t-statistic |   p-value |
|-------------|--------------|--------------|-------------|----------|
| Intercept   |     1.34e-06 |     1.28e-05 |      0.1040 |     0.917 |
| Slope       |       1.0000 |     1.73e-05 |  57709.4575 |     0.000 |

**Missing Observations Sample**:
```
 index  permno  yyyymm  tang_q
     0   12750  198212  0.6479
     1   12750  198301  0.6479
     2   12750  198302  0.6479
```

**Feedback**:
- Num observations with std_diff >= TOL_DIFF_1: 160/1675095 (0.010%)
- Stata standard deviation: 3.45e-01

---

### AbnormalAccrualsPercent

**Status**: ❌ MISSING PYTHON CSV

**Error**: Python CSV file not found: ../pyData/Placebos/AbnormalAccrualsPercent.csv

---

### AccrualQuality

**Status**: ❌ MISSING PYTHON CSV

**Error**: Python CSV file not found: ../pyData/Placebos/AccrualQuality.csv

---

### AccrualQualityJune

**Status**: ❌ MISSING PYTHON CSV

**Error**: Python CSV file not found: ../pyData/Placebos/AccrualQualityJune.csv

---

### BetaBDLeverage

**Status**: ❌ MISSING PYTHON CSV

**Error**: Python CSV file not found: ../pyData/Placebos/BetaBDLeverage.csv

---

### BetaDimson

**Status**: ❌ MISSING PYTHON CSV

**Error**: Python CSV file not found: ../pyData/Placebos/BetaDimson.csv

---

### BetaSquared

**Status**: ❌ MISSING PYTHON CSV

**Error**: Python CSV file not found: ../pyData/Placebos/BetaSquared.csv

---

### BidAskTAQ

**Status**: ❌ MISSING PYTHON CSV

**Error**: Python CSV file not found: ../pyData/Placebos/BidAskTAQ.csv

---

### BrandCapital

**Status**: ❌ MISSING PYTHON CSV

**Error**: Python CSV file not found: ../pyData/Placebos/BrandCapital.csv

---

### ChPM

**Status**: ❌ MISSING PYTHON CSV

**Error**: Python CSV file not found: ../pyData/Placebos/ChPM.csv

---

### DelayAcct

**Status**: ❌ MISSING PYTHON CSV

**Error**: Python CSV file not found: ../pyData/Placebos/DelayAcct.csv

---

### DelayNonAcct

**Status**: ❌ MISSING PYTHON CSV

**Error**: Python CSV file not found: ../pyData/Placebos/DelayNonAcct.csv

---

### DownsideBeta

**Status**: ❌ MISSING PYTHON CSV

**Error**: Python CSV file not found: ../pyData/Placebos/DownsideBeta.csv

---

### EarningsConservatism

**Status**: ❌ MISSING PYTHON CSV

**Error**: Python CSV file not found: ../pyData/Placebos/EarningsConservatism.csv

---

### EarningsPersistence

**Status**: ❌ MISSING PYTHON CSV

**Error**: Python CSV file not found: ../pyData/Placebos/EarningsPersistence.csv

---

### EarningsPredictability

**Status**: ❌ MISSING PYTHON CSV

**Error**: Python CSV file not found: ../pyData/Placebos/EarningsPredictability.csv

---

### EarningsTimeliness

**Status**: ❌ MISSING PYTHON CSV

**Error**: Python CSV file not found: ../pyData/Placebos/EarningsTimeliness.csv

---

### EarningsValueRelevance

**Status**: ❌ MISSING PYTHON CSV

**Error**: Python CSV file not found: ../pyData/Placebos/EarningsValueRelevance.csv

---

### FRbook

**Status**: ❌ MISSING PYTHON CSV

**Error**: Python CSV file not found: ../pyData/Placebos/FRbook.csv

---

### FailureProbability

**Status**: ❌ MISSING PYTHON CSV

**Error**: Python CSV file not found: ../pyData/Placebos/FailureProbability.csv

---

### FailureProbabilityJune

**Status**: ❌ MISSING PYTHON CSV

**Error**: Python CSV file not found: ../pyData/Placebos/FailureProbabilityJune.csv

---

### ForecastDispersionLT

**Status**: ❌ MISSING PYTHON CSV

**Error**: Python CSV file not found: ../pyData/Placebos/ForecastDispersionLT.csv

---

### GPlag

**Status**: ❌ MISSING PYTHON CSV

**Error**: Python CSV file not found: ../pyData/Placebos/GPlag.csv

---

### GPlag_q

**Status**: ❌ MISSING PYTHON CSV

**Error**: Python CSV file not found: ../pyData/Placebos/GPlag_q.csv

---

### GrGMToGrSales

**Status**: ❌ MISSING PYTHON CSV

**Error**: Python CSV file not found: ../pyData/Placebos/GrGMToGrSales.csv

---

### GrSaleToGrReceivables

**Status**: ❌ MISSING PYTHON CSV

**Error**: Python CSV file not found: ../pyData/Placebos/GrSaleToGrReceivables.csv

---

### IdioVolCAPM

**Status**: ❌ MISSING PYTHON CSV

**Error**: Python CSV file not found: ../pyData/Placebos/IdioVolCAPM.csv

---

### IdioVolQF

**Status**: ❌ MISSING PYTHON CSV

**Error**: Python CSV file not found: ../pyData/Placebos/IdioVolQF.csv

---

### IntrinsicValue

**Status**: ❌ MISSING PYTHON CSV

**Error**: Python CSV file not found: ../pyData/Placebos/IntrinsicValue.csv

---

### KZ

**Status**: ❌ MISSING PYTHON CSV

**Error**: Python CSV file not found: ../pyData/Placebos/KZ.csv

---

### KZ_q

**Status**: ❌ MISSING PYTHON CSV

**Error**: Python CSV file not found: ../pyData/Placebos/KZ_q.csv

---

### OScore_q

**Status**: ❌ MISSING PYTHON CSV

**Error**: Python CSV file not found: ../pyData/Placebos/OScore_q.csv

---

### OperProfLag

**Status**: ❌ MISSING PYTHON CSV

**Error**: Python CSV file not found: ../pyData/Placebos/OperProfLag.csv

---

### OperProfLag_q

**Status**: ❌ MISSING PYTHON CSV

**Error**: Python CSV file not found: ../pyData/Placebos/OperProfLag_q.csv

---

### OperProfRDLagAT

**Status**: ❌ MISSING PYTHON CSV

**Error**: Python CSV file not found: ../pyData/Placebos/OperProfRDLagAT.csv

---

### OperProfRDLagAT_q

**Status**: ❌ MISSING PYTHON CSV

**Error**: Python CSV file not found: ../pyData/Placebos/OperProfRDLagAT_q.csv

---

### OrgCapNoAdj

**Status**: ❌ MISSING PYTHON CSV

**Error**: Python CSV file not found: ../pyData/Placebos/OrgCapNoAdj.csv

---

### PM

**Status**: ❌ MISSING PYTHON CSV

**Error**: Python CSV file not found: ../pyData/Placebos/PM.csv

---

### PS_q

**Status**: ❌ MISSING PYTHON CSV

**Error**: Python CSV file not found: ../pyData/Placebos/PS_q.csv

---

### ResidualMomentum6m

**Status**: ❌ MISSING PYTHON CSV

**Error**: Python CSV file not found: ../pyData/Placebos/ResidualMomentum6m.csv

---

### RetNOA

**Status**: ❌ MISSING PYTHON CSV

**Error**: Python CSV file not found: ../pyData/Placebos/RetNOA.csv

---

### ReturnSkewCAPM

**Status**: ❌ MISSING PYTHON CSV

**Error**: Python CSV file not found: ../pyData/Placebos/ReturnSkewCAPM.csv

---

### ReturnSkewQF

**Status**: ❌ MISSING PYTHON CSV

**Error**: Python CSV file not found: ../pyData/Placebos/ReturnSkewQF.csv

---

### WW

**Status**: ❌ MISSING PYTHON CSV

**Error**: Python CSV file not found: ../pyData/Placebos/WW.csv

---

### WW_Q

**Status**: ❌ MISSING PYTHON CSV

**Error**: Python CSV file not found: ../pyData/Placebos/WW_Q.csv

---

### betaCC

**Status**: ❌ MISSING PYTHON CSV

**Error**: Python CSV file not found: ../pyData/Placebos/betaCC.csv

---

### betaCR

**Status**: ❌ MISSING PYTHON CSV

**Error**: Python CSV file not found: ../pyData/Placebos/betaCR.csv

---

### betaNet

**Status**: ❌ MISSING PYTHON CSV

**Error**: Python CSV file not found: ../pyData/Placebos/betaNet.csv

---

### betaRC

**Status**: ❌ MISSING PYTHON CSV

**Error**: Python CSV file not found: ../pyData/Placebos/betaRC.csv

---

### betaRR

**Status**: ❌ MISSING PYTHON CSV

**Error**: Python CSV file not found: ../pyData/Placebos/betaRR.csv

---

### currat

**Status**: ❌ MISSING PYTHON CSV

**Error**: Python CSV file not found: ../pyData/Placebos/currat.csv

---

### grcapx1y

**Status**: ❌ MISSING PYTHON CSV

**Error**: Python CSV file not found: ../pyData/Placebos/grcapx1y.csv

---

### nanalyst

**Status**: ❌ MISSING PYTHON CSV

**Error**: Python CSV file not found: ../pyData/Placebos/nanalyst.csv

---

### pchcurrat

**Status**: ❌ MISSING PYTHON CSV

**Error**: Python CSV file not found: ../pyData/Placebos/pchcurrat.csv

---

### pchgm_pchsale

**Status**: ❌ MISSING PYTHON CSV

**Error**: Python CSV file not found: ../pyData/Placebos/pchgm_pchsale.csv

---

### pchsaleinv

**Status**: ❌ MISSING PYTHON CSV

**Error**: Python CSV file not found: ../pyData/Placebos/pchsaleinv.csv

---

### roavol

**Status**: ❌ MISSING PYTHON CSV

**Error**: Python CSV file not found: ../pyData/Placebos/roavol.csv

---

