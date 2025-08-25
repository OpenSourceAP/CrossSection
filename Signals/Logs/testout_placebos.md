# Placebo Validation Results

**Generated**: 2025-08-25 00:00:13

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
| DelayAcct                 | ✅         | ✅       | ❌ (100.00%) | ❌ (0.00%)    | ❌ (99th diff 0.0E+00)   |
| DelayNonAcct              | ✅         | ✅       | ❌ (100.00%) | ❌ (0.00%)    | ❌ (99th diff 0.0E+00)   |
| DownsideBeta              | ✅         | ✅       | ❌ (100.00%) | ❌ (0.00%)    | ❌ (99th diff 0.0E+00)   |
| IdioVolCAPM               | ✅         | ✅       | ❌ (100.00%) | ❌ (0.00%)    | ❌ (99th diff 0.0E+00)   |
| IdioVolQF                 | ✅         | ✅       | ❌ (100.00%) | ❌ (0.00%)    | ❌ (99th diff 0.0E+00)   |
| ReturnSkewCAPM            | ✅         | ✅       | ❌ (100.00%) | ❌ (0.00%)    | ❌ (99th diff 0.0E+00)   |
| ReturnSkewQF              | ✅         | ✅       | ❌ (100.00%) | ❌ (0.00%)    | ❌ (99th diff 0.0E+00)   |
| betaCC                    | ✅         | ✅       | ❌ (100.00%) | ❌ (0.00%)    | ❌ (99th diff 0.0E+00)   |
| betaCR                    | ✅         | ✅       | ❌ (100.00%) | ❌ (0.00%)    | ❌ (99th diff 0.0E+00)   |
| betaNet                   | ✅         | ✅       | ❌ (100.00%) | ❌ (0.00%)    | ❌ (99th diff 0.0E+00)   |
| betaRC                    | ✅         | ✅       | ❌ (100.00%) | ❌ (0.00%)    | ❌ (99th diff 0.0E+00)   |
| betaRR                    | ✅         | ✅       | ❌ (100.00%) | ❌ (0.00%)    | ❌ (99th diff 0.0E+00)   |
| AccrualQualityJune        | ✅         | ✅       | ❌ (3.88%)   | ❌ (60.03%)   | ✅ (99th diff 5.6E-01)   |
| AccrualQuality            | ✅         | ✅       | ❌ (0.96%)   | ❌ (59.96%)   | ✅ (99th diff 4.1E-01)   |
| FailureProbability        | ✅         | ✅       | ❌ (0.69%)   | ✅ (0.11%)    | ✅ (99th diff 3.2E-06)   |
| OScore_q                  | ✅         | ✅       | ❌ (0.36%)   | ✅ (0.00%)    | ✅ (99th diff 0.0E+00)   |
| FailureProbabilityJune    | ✅         | ✅       | ❌ (0.26%)   | ✅ (0.26%)    | ✅ (99th diff 3.6E-06)   |
| ForecastDispersionLT      | ✅         | ✅       | ❌ (0.21%)   | ✅ (0.09%)    | ✅ (99th diff 1.5E-07)   |
| fgr5yrNoLag               | ✅         | ✅       | ❌ (0.21%)   | ✅ (0.08%)    | ✅ (99th diff 1.4E-07)   |
| nanalyst                  | ✅         | ✅       | ❌ (0.03%)   | ✅ (0.26%)    | ✅ (99th diff 0.0E+00)   |
| PS_q                      | ✅         | ✅       | ❌ (0.02%)   | ❌ (53.97%)   | ❌ (99th diff 3.2E+00)   |
| DivYield                  | ✅         | ✅       | ❌ (0.01%)   | ✅ (0.00%)    | ✅ (99th diff 1.2E-08)   |
| KZ_q                      | ✅         | ✅       | ❌ (0.01%)   | ✅ (0.00%)    | ✅ (99th diff 3.1E-09)   |
| pchquick                  | ✅         | ✅       | ❌ (0.01%)   | ✅ (0.24%)    | ✅ (99th diff 2.8E-09)   |
| OperProfRDLagAT_q         | ✅         | ✅       | ❌ (0.01%)   | ✅ (0.02%)    | ✅ (99th diff 6.6E-08)   |
| OperProfLag               | ✅         | ✅       | ❌ (0.00%)   | ✅ (0.01%)    | ✅ (99th diff 1.5E-08)   |
| cfpq                      | ✅         | ✅       | ❌ (0.00%)   | ✅ (0.02%)    | ✅ (99th diff 3.7E-08)   |
| EPq                       | ✅         | ✅       | ❌ (0.00%)   | ✅ (0.74%)    | ✅ (99th diff 2.9E-03)   |
| RD_q                      | ✅         | ✅       | ❌ (0.00%)   | ✅ (0.00%)    | ✅ (99th diff 5.2E-08)   |
| WW                        | ✅         | ✅       | ❌ (0.00%)   | ✅ (0.00%)    | ✅ (99th diff 4.7E-10)   |
| GPlag_q                   | ✅         | ✅       | ❌ (0.00%)   | ✅ (0.01%)    | ✅ (99th diff 1.8E-08)   |
| rd_sale_q                 | ✅         | ✅       | ❌ (0.00%)   | ✅ (0.00%)    | ✅ (99th diff 6.7E-09)   |
| NetDebtPrice_q            | ✅         | ✅       | ❌ (0.00%)   | ✅ (0.00%)    | ✅ (99th diff 4.8E-08)   |
| PayoutYield_q             | ✅         | ✅       | ❌ (0.00%)   | ✅ (0.01%)    | ✅ (99th diff 3.4E-08)   |
| ChangeRoE                 | ✅         | ✅       | ❌ (0.00%)   | ✅ (0.00%)    | ✅ (99th diff 3.2E-09)   |
| RetNOA_q                  | ✅         | ✅       | ❌ (0.00%)   | ✅ (0.00%)    | ✅ (99th diff 3.8E-11)   |
| ChangeRoA                 | ✅         | ✅       | ❌ (0.00%)   | ✅ (0.01%)    | ✅ (99th diff 6.6E-08)   |
| Tax_q                     | ✅         | ✅       | ❌ (0.00%)   | ✅ (0.00%)    | ✅ (99th diff 8.6E-09)   |
| Leverage_q                | ✅         | ✅       | ❌ (0.00%)   | ✅ (0.00%)    | ✅ (99th diff 4.5E-08)   |
| OPLeverage_q              | ✅         | ✅       | ❌ (0.00%)   | ✅ (0.01%)    | ✅ (99th diff 7.7E-08)   |
| OperProfRDLagAT           | ✅         | ✅       | ❌ (0.00%)   | ✅ (0.00%)    | ✅ (99th diff 2.3E-08)   |
| OperProfLag_q             | ✅         | ✅       | ❌ (0.00%)   | ✅ (0.00%)    | ✅ (99th diff 9.2E-13)   |
| EBM_q                     | ✅         | ✅       | ❌ (0.00%)   | ✅ (0.00%)    | ✅ (99th diff 3.4E-08)   |
| AssetGrowth_q             | ✅         | ✅       | ❌ (0.00%)   | ✅ (0.00%)    | ✅ (99th diff 1.9E-08)   |
| AssetLiquidityMarketQuart | ✅         | ✅       | ❌ (0.00%)   | ✅ (0.00%)    | ✅ (99th diff 1.5E-07)   |
| CapTurnover_q             | ✅         | ✅       | ❌ (0.00%)   | ✅ (0.00%)    | ✅ (99th diff 1.0E-08)   |
| CBOperProfLagAT_q         | ✅         | ✅       | ❌ (0.00%)   | ✅ (0.02%)    | ✅ (99th diff 8.5E-08)   |
| WW_Q                      | ✅         | ✅       | ❌ (0.00%)   | ✅ (0.00%)    | ✅ (99th diff 2.6E-07)   |
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
| roavol                    | ✅         | ✅       | ❌ (0.00%)   | ✅ (4.52%)    | ✅ (99th diff 7.5E-02)   |
| KZ                        | ✅         | ✅       | ❌ (0.00%)   | ✅ (0.00%)    | ✅ (99th diff 2.0E-09)   |
| tang_q                    | ✅         | ✅       | ❌ (0.00%)   | ✅ (0.01%)    | ✅ (99th diff 1.5E-07)   |
| RetNOA                    | ✅         | ✅       | ❌ (0.00%)   | ✅ (0.00%)    | ✅ (99th diff 1.4E-19)   |
| pchcurrat                 | ✅         | ✅       | ✅ (0.00%)   | ❌ (15.54%)   | ❌ (99th diff NAN)       |
| BrandCapital              | ✅         | ✅       | ✅ (0.00%)   | ✅ (5.88%)    | ✅ (99th diff 8.2E-02)   |
| GrGMToGrSales             | ✅         | ✅       | ✅ (0.00%)   | ✅ (0.04%)    | ✅ (99th diff 4.5E-09)   |
| DivYieldAnn               | ✅         | ✅       | ✅ (0.00%)   | ✅ (0.03%)    | ✅ (99th diff 2.1E-08)   |
| NetPayoutYield_q          | ✅         | ✅       | ✅ (0.00%)   | ✅ (0.02%)    | ✅ (99th diff 3.5E-08)   |
| roic                      | ✅         | ✅       | ✅ (0.00%)   | ✅ (0.01%)    | ✅ (99th diff 3.4E-23)   |
| GrSaleToGrReceivables     | ✅         | ✅       | ✅ (0.00%)   | ✅ (0.01%)    | ✅ (99th diff 8.0E-10)   |
| GPlag                     | ✅         | ✅       | ✅ (0.00%)   | ✅ (0.01%)    | ✅ (99th diff 5.6E-08)   |
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
| pchgm_pchsale             | ✅         | ✅       | ✅ (0.00%)   | ✅ (0.00%)    | ✅ (99th diff 2.6E-09)   |
| sgr                       | ✅         | ✅       | ✅ (0.00%)   | ✅ (0.00%)    | ✅ (99th diff 1.9E-09)   |
| BookLeverageQuarterly     | ✅         | ✅       | ✅ (0.00%)   | ✅ (0.00%)    | ✅ (99th diff 4.1E-13)   |
| AMq                       | ✅         | ✅       | ✅ (0.00%)   | ✅ (0.00%)    | ✅ (99th diff 3.9E-08)   |
| LaborforceEfficiency      | ✅         | ✅       | ✅ (0.00%)   | ✅ (0.00%)    | ✅ (99th diff 4.3E-09)   |
| CapTurnover               | ✅         | ✅       | ✅ (0.00%)   | ✅ (0.00%)    | ✅ (99th diff 8.5E-08)   |
| salecash                  | ✅         | ✅       | ✅ (0.00%)   | ✅ (0.00%)    | ✅ (99th diff 6.5E-09)   |
| ZScore                    | ✅         | ✅       | ✅ (0.00%)   | ✅ (0.00%)    | ✅ (99th diff 8.3E-08)   |
| BidAskTAQ                 | ✅         | ✅       | ✅ (0.00%)   | ✅ (0.00%)    | ✅ (99th diff 8.0E-08)   |
| BetaSquared               | ✅         | ✅       | ✅ (0.00%)   | ✅ (0.00%)    | ✅ (99th diff 7.0E-08)   |
| currat                    | ✅         | ✅       | ✅ (0.00%)   | ✅ (0.00%)    | ✅ (99th diff 1.4E-08)   |
| quick                     | ✅         | ✅       | ✅ (0.00%)   | ✅ (0.00%)    | ✅ (99th diff 1.1E-08)   |
| ChPM                      | ✅         | ✅       | ✅ (0.00%)   | ✅ (0.00%)    | ✅ (99th diff 5.2E-09)   |
| rd_sale                   | ✅         | ✅       | ✅ (0.00%)   | ✅ (0.00%)    | ✅ (99th diff 4.1E-09)   |
| cashdebt                  | ✅         | ✅       | ✅ (0.00%)   | ✅ (0.00%)    | ✅ (99th diff 3.2E-09)   |
| saleinv                   | ✅         | ✅       | ✅ (0.00%)   | ✅ (0.00%)    | ✅ (99th diff 3.1E-09)   |
| PM                        | ✅         | ✅       | ✅ (0.00%)   | ✅ (0.00%)    | ✅ (99th diff 2.3E-09)   |
| pchsaleinv                | ✅         | ✅       | ✅ (0.00%)   | ✅ (0.00%)    | ✅ (99th diff 1.7E-09)   |
| AbnormalAccrualsPercent   | ❌         | NA      | NA          | NA           | NA                      |
| BetaBDLeverage            | ❌         | NA      | NA          | NA           | NA                      |
| BetaDimson                | ❌         | NA      | NA          | NA           | NA                      |
| EarningsConservatism      | ❌         | NA      | NA          | NA           | NA                      |
| EarningsPersistence       | ❌         | NA      | NA          | NA           | NA                      |
| EarningsPredictability    | ❌         | NA      | NA          | NA           | NA                      |
| EarningsTimeliness        | ❌         | NA      | NA          | NA           | NA                      |
| EarningsValueRelevance    | ❌         | NA      | NA          | NA           | NA                      |
| FRbook                    | ❌         | NA      | NA          | NA           | NA                      |
| IntrinsicValue            | ❌         | NA      | NA          | NA           | NA                      |
| OrgCapNoAdj               | ❌         | NA      | NA          | NA           | NA                      |
| ResidualMomentum6m        | ❌         | NA      | NA          | NA           | NA                      |
| grcapx1y                  | ❌         | NA      | NA          | NA           | NA                      |

**Overall**: 38/101 available placebos passed validation
**Python CSVs**: 101/114 placebos have Python implementation

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

### AccrualQuality

**Status**: ❌ FAILED

**Test Results**:
- Test 1 - Column names: ✅ PASSED
- Test 2 - Superset check: ❌ FAILED (Python missing 16721 Stata observations)
- Test 3 - Precision1 check: ❌ FAILED
- Test 4 - Precision2 check: ✅ PASSED

**Columns**: ['AccrualQuality']

**Observations**:
- Stata:  1,740,065
- Python: 1,772,372
- Common: 1,723,344

**Precision1**: 59.956% obs with std_diff >= 1.00e-02 (tolerance: < 10%)

**Precision2**: 99th percentile diff = 4.11e-01 (tolerance: < 1.00e+00)

**Summary Statistics** (Common Observations):

| Statistic  |          Stata |         Python |     Difference | Std Difference |
|------------|----------------|----------------|----------------|----------------|
| count      |       1.72e+06 |       1.72e+06 |       1.72e+06 |       1.72e+06 |
| mean       |         0.0460 |         0.0463 |       3.24e-04 |         0.0065 |
| std        |         0.0495 |         0.0498 |         0.0053 |         0.1061 |
| min        |       4.17e-04 |       4.58e-04 |        -0.1265 |        -2.5557 |
| 25%        |         0.0179 |         0.0180 |      -6.90e-04 |        -0.0139 |
| 50%        |         0.0316 |         0.0318 |       7.99e-10 |       1.61e-08 |
| 75%        |         0.0562 |         0.0567 |       9.51e-04 |         0.0192 |
| max        |         1.6265 |         1.6229 |         0.5466 |        11.0413 |

**Regression Analysis** (Python ~ Stata):

- **Model**: python = 0.0003 + 1.0008 * stata
- **R-squared**: 0.9889
- **N observations**: 1,723,344

| Coefficient |     Estimate |    Std Error | t-statistic |   p-value |
|-------------|--------------|--------------|-------------|----------|
| Intercept   |     2.85e-04 |     5.46e-06 |     52.2289 |     0.000 |
| Slope       |       1.0008 |     8.08e-05 |  12389.1528 |     0.000 |

**Missing Observations Sample**:
```
 index  permno  yyyymm  AccrualQuality
     0   10080  200006        0.026711
     1   10080  200007        0.026711
     2   10080  200008        0.026711
     3   10080  200009        0.026711
     4   10080  200010        0.026711
     5   10080  200011        0.026711
     6   10080  200012        0.026711
     7   10080  200101        0.026711
     8   10080  200102        0.026711
     9   10080  200103        0.026711
```

**Feedback**:
- Num observations with std_diff >= TOL_DIFF_1: 1033246/1723344 (59.956%)
- Stata standard deviation: 4.95e-02

**Most Recent Bad Observations**:
```
   permno  yyyymm    python     stata      diff
0   10104  202610  0.017492  0.018274 -0.000782
1   10104  202609  0.017492  0.018274 -0.000782
2   42585  202609  0.021855  0.041185 -0.019330
3   60097  202609  0.020834  0.019858  0.000976
4   82598  202609  0.014516  0.015714 -0.001199
5   10104  202608  0.017492  0.018274 -0.000782
6   12082  202608  0.086767  0.085591  0.001176
7   12783  202608  0.031212  0.031918 -0.000707
8   13142  202608  0.018200  0.017444  0.000756
9   14888  202608  0.020935  0.019089  0.001846
```

**Largest Differences**:
```
   permno  yyyymm    python     stata      diff
0   11665  199807  0.708231  0.161608  0.546622
1   11665  199808  0.708231  0.161608  0.546622
2   11665  199809  0.708231  0.161608  0.546622
3   11665  199810  0.708231  0.161608  0.546622
4   11665  199811  0.708231  0.161608  0.546622
5   11665  199812  0.708231  0.161608  0.546622
6   11665  199901  0.708231  0.161608  0.546622
7   11665  199902  0.708231  0.161608  0.546622
8   11665  199903  0.708231  0.161608  0.546622
9   11665  199904  0.708231  0.161608  0.546622
```

---

### AccrualQualityJune

**Status**: ❌ FAILED

**Test Results**:
- Test 1 - Column names: ✅ PASSED
- Test 2 - Superset check: ❌ FAILED (Python missing 69316 Stata observations)
- Test 3 - Precision1 check: ❌ FAILED
- Test 4 - Precision2 check: ✅ PASSED

**Columns**: ['AccrualQualityJune']

**Observations**:
- Stata:  1,784,388
- Python: 1,744,543
- Common: 1,715,072

**Precision1**: 60.028% obs with std_diff >= 1.00e-02 (tolerance: < 10%)

**Precision2**: 99th percentile diff = 5.56e-01 (tolerance: < 1.00e+00)

**Summary Statistics** (Common Observations):

| Statistic  |          Stata |         Python |     Difference | Std Difference |
|------------|----------------|----------------|----------------|----------------|
| count      |       1.72e+06 |       1.72e+06 |       1.72e+06 |       1.72e+06 |
| mean       |         0.0462 |         0.0467 |       5.01e-04 |         0.0100 |
| std        |         0.0500 |         0.0506 |         0.0095 |         0.1905 |
| min        |       4.17e-04 |       4.58e-04 |        -0.5295 |       -10.5847 |
| 25%        |         0.0179 |         0.0180 |      -6.93e-04 |        -0.0138 |
| 50%        |         0.0316 |         0.0319 |       8.58e-10 |       1.71e-08 |
| 75%        |         0.0565 |         0.0571 |       9.77e-04 |         0.0195 |
| max        |         1.6265 |         1.6229 |         0.5466 |        10.9260 |

**Regression Analysis** (Python ~ Stata):

- **Model**: python = 0.0008 + 0.9938 * stata
- **R-squared**: 0.9646
- **N observations**: 1,715,072

| Coefficient |     Estimate |    Std Error | t-statistic |   p-value |
|-------------|--------------|--------------|-------------|----------|
| Intercept   |     7.86e-04 |     9.90e-06 |     79.4311 |     0.000 |
| Slope       |       0.9938 |     1.45e-04 |   6837.5039 |     0.000 |

**Missing Observations Sample**:
```
 index  permno  yyyymm  AccrualQualityJune
     0   10025  201104            0.026843
     1   10025  201105            0.026843
     2   10025  201106            0.026843
     3   10025  201107            0.026843
     4   10025  201108            0.026843
     5   10025  201109            0.026843
     6   10025  201110            0.026843
     7   10025  201111            0.026843
     8   10025  201112            0.026843
     9   10025  201201            0.026843
```

**Feedback**:
- Num observations with std_diff >= TOL_DIFF_1: 1029517/1715072 (60.028%)
- Stata standard deviation: 5.00e-02

**Most Recent Bad Observations**:
```
   permno  yyyymm    python     stata      diff
0   10104  202610  0.017492  0.018274 -0.000782
1   10104  202609  0.017492  0.018274 -0.000782
2   42585  202609  0.021855  0.041185 -0.019330
3   60097  202609  0.020834  0.019858  0.000976
4   82598  202609  0.014516  0.015714 -0.001199
5   10104  202608  0.017492  0.018274 -0.000782
6   12082  202608  0.086767  0.085591  0.001176
7   12783  202608  0.031212  0.031918 -0.000707
8   13142  202608  0.018200  0.017444  0.000756
9   14888  202608  0.020935  0.019089  0.001846
```

**Largest Differences**:
```
   permno  yyyymm    python     stata      diff
0   11665  199906  0.708231  0.161608  0.546622
1   11665  199907  0.708231  0.161608  0.546622
2   11665  199908  0.708231  0.161608  0.546622
3   11665  199909  0.708231  0.161608  0.546622
4   11665  199910  0.708231  0.161608  0.546622
5   11665  199911  0.708231  0.161608  0.546622
6   11665  199912  0.708231  0.161608  0.546622
7   11665  200001  0.708231  0.161608  0.546622
8   11665  200002  0.708231  0.161608  0.546622
9   11665  200003  0.708231  0.161608  0.546622
```

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

### BetaSquared

**Status**: ✅ PASSED

**Test Results**:
- Test 1 - Column names: ✅ PASSED
- Test 2 - Superset check: ✅ PASSED
- Test 3 - Precision1 check: ✅ PASSED
- Test 4 - Precision2 check: ✅ PASSED

**Columns**: ['BetaSquared']

**Observations**:
- Stata:  4,285,574
- Python: 4,353,773
- Common: 4,285,574

**Precision1**: 0.000% obs with std_diff >= 1.00e-02 (tolerance: < 10%)

**Precision2**: 99th percentile diff = 7.04e-08 (tolerance: < 1.00e+00)

**Summary Statistics** (Common Observations):

| Statistic  |          Stata |         Python |     Difference | Std Difference |
|------------|----------------|----------------|----------------|----------------|
| count      |       4.29e+06 |       4.29e+06 |       4.29e+06 |       4.29e+06 |
| mean       |         1.5351 |         1.5351 |       7.77e-09 |       1.17e-09 |
| std        |         6.6568 |         6.6568 |       4.67e-07 |       7.02e-08 |
| min        |       5.10e-13 |       5.13e-13 |      -4.38e-05 |      -6.58e-06 |
| 25%        |         0.2920 |         0.2920 |      -1.62e-08 |      -2.43e-09 |
| 50%        |         0.8168 |         0.8168 |       4.33e-10 |       6.51e-11 |
| 75%        |         1.7846 |         1.7846 |       2.33e-08 |       3.50e-09 |
| max        |      2770.3259 |      2770.3261 |       3.03e-04 |       4.55e-05 |

**Regression Analysis** (Python ~ Stata):

- **Model**: python = -0.0000 + 1.0000 * stata
- **R-squared**: 1.0000
- **N observations**: 4,285,574

| Coefficient |     Estimate |    Std Error | t-statistic |   p-value |
|-------------|--------------|--------------|-------------|----------|
| Intercept   |    -6.95e-08 |     1.61e-10 |   -430.8821 |     0.000 |
| Slope       |       1.0000 |     2.36e-11 |    4.24e+10 |     0.000 |

**Feedback**:
- Num observations with std_diff >= TOL_DIFF_1: 0/4285574 (0.000%)
- Stata standard deviation: 6.66e+00

---

### BidAskTAQ

**Status**: ✅ PASSED

**Test Results**:
- Test 1 - Column names: ✅ PASSED
- Test 2 - Superset check: ✅ PASSED
- Test 3 - Precision1 check: ✅ PASSED
- Test 4 - Precision2 check: ✅ PASSED

**Columns**: ['BidAskTAQ']

**Observations**:
- Stata:  3,262,927
- Python: 3,262,927
- Common: 3,262,927

**Precision1**: 0.000% obs with std_diff >= 1.00e-02 (tolerance: < 10%)

**Precision2**: 99th percentile diff = 7.96e-08 (tolerance: < 1.00e+00)

**Summary Statistics** (Common Observations):

| Statistic  |          Stata |         Python |     Difference | Std Difference |
|------------|----------------|----------------|----------------|----------------|
| count      |       3.26e+06 |       3.26e+06 |       3.26e+06 |       3.26e+06 |
| mean       |         1.5559 |         1.5559 |      -7.71e-12 |      -3.07e-12 |
| std        |         2.5110 |         2.5110 |       4.90e-08 |       1.95e-08 |
| min        |         0.0000 |         0.0000 |      -2.00e-06 |      -7.96e-07 |
| 25%        |         0.1774 |         0.1774 |         0.0000 |         0.0000 |
| 50%        |         0.6136 |         0.6136 |         0.0000 |         0.0000 |
| 75%        |         1.8032 |         1.8032 |         0.0000 |         0.0000 |
| max        |        39.9582 |        39.9582 |       2.00e-06 |       7.96e-07 |

**Regression Analysis** (Python ~ Stata):

- **Model**: python = -0.0000 + 1.0000 * stata
- **R-squared**: 1.0000
- **N observations**: 3,262,927

| Coefficient |     Estimate |    Std Error | t-statistic |   p-value |
|-------------|--------------|--------------|-------------|----------|
| Intercept   |    -1.86e-12 |     3.19e-11 |     -0.0584 |     0.953 |
| Slope       |       1.0000 |     1.08e-11 |    9.26e+10 |     0.000 |

**Feedback**:
- Num observations with std_diff >= TOL_DIFF_1: 0/3262927 (0.000%)
- Stata standard deviation: 2.51e+00

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

### BrandCapital

**Status**: ✅ PASSED

**Test Results**:
- Test 1 - Column names: ✅ PASSED
- Test 2 - Superset check: ✅ PASSED
- Test 3 - Precision1 check: ✅ PASSED
- Test 4 - Precision2 check: ✅ PASSED

**Columns**: ['BrandCapital']

**Observations**:
- Stata:  1,231,460
- Python: 1,280,000
- Common: 1,231,460

**Precision1**: 5.877% obs with std_diff >= 1.00e-02 (tolerance: < 10%)

**Precision2**: 99th percentile diff = 8.25e-02 (tolerance: < 1.00e+00)

**Summary Statistics** (Common Observations):

| Statistic  |          Stata |         Python |     Difference | Std Difference |
|------------|----------------|----------------|----------------|----------------|
| count      |       1.23e+06 |       1.23e+06 |       1.23e+06 |       1.23e+06 |
| mean       |         0.0642 |         0.0656 |         0.0014 |         0.0040 |
| std        |         0.3504 |         0.3545 |         0.0239 |         0.0683 |
| min        |        -0.0066 |        -0.0066 |        -0.0211 |        -0.0603 |
| 25%        |         0.0043 |         0.0045 |      -1.01e-10 |      -2.88e-10 |
| 50%        |         0.0228 |         0.0238 |       2.62e-10 |       7.47e-10 |
| 75%        |         0.0651 |         0.0669 |       1.75e-07 |       5.00e-07 |
| max        |        86.0362 |        86.0362 |         6.8422 |        19.5254 |

**Regression Analysis** (Python ~ Stata):

- **Model**: python = 0.0008 + 1.0094 * stata
- **R-squared**: 0.9955
- **N observations**: 1,231,460

| Coefficient |     Estimate |    Std Error | t-statistic |   p-value |
|-------------|--------------|--------------|-------------|----------|
| Intercept   |     8.07e-04 |     2.17e-05 |     37.1912 |     0.000 |
| Slope       |       1.0094 |     6.09e-05 |  16562.8102 |     0.000 |

**Feedback**:
- Num observations with std_diff >= TOL_DIFF_1: 72379/1231460 (5.877%)
- Stata standard deviation: 3.50e-01

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

### ChPM

**Status**: ✅ PASSED

**Test Results**:
- Test 1 - Column names: ✅ PASSED
- Test 2 - Superset check: ✅ PASSED
- Test 3 - Precision1 check: ✅ PASSED
- Test 4 - Precision2 check: ✅ PASSED

**Columns**: ['ChPM']

**Observations**:
- Stata:  3,222,277
- Python: 3,303,855
- Common: 3,222,277

**Precision1**: 0.000% obs with std_diff >= 1.00e-02 (tolerance: < 10%)

**Precision2**: 99th percentile diff = 5.23e-09 (tolerance: < 1.00e+00)

**Summary Statistics** (Common Observations):

| Statistic  |          Stata |         Python |     Difference | Std Difference |
|------------|----------------|----------------|----------------|----------------|
| count      |       3.22e+06 |       3.22e+06 |       3.22e+06 |       3.22e+06 |
| mean       |        -0.3833 |        -0.3833 |      -4.11e-08 |      -2.71e-10 |
| std        |       151.4586 |       151.4586 |       7.13e-04 |       4.71e-06 |
| min        |    -30903.6450 |    -30903.6451 |        -0.2284 |        -0.0015 |
| 25%        |        -0.0312 |        -0.0312 |      -2.22e-09 |      -1.47e-11 |
| 50%        |      -1.17e-04 |      -1.17e-04 |       6.86e-12 |       4.53e-14 |
| 75%        |         0.0251 |         0.0251 |       2.23e-09 |       1.48e-11 |
| max        |     24410.3810 |     24410.3806 |         0.2069 |         0.0014 |

**Regression Analysis** (Python ~ Stata):

- **Model**: python = -0.0000 + 1.0000 * stata
- **R-squared**: 1.0000
- **N observations**: 3,222,277

| Coefficient |     Estimate |    Std Error | t-statistic |   p-value |
|-------------|--------------|--------------|-------------|----------|
| Intercept   |    -4.21e-08 |     3.97e-07 |     -0.1059 |     0.916 |
| Slope       |       1.0000 |     2.62e-09 |    3.81e+08 |     0.000 |

**Feedback**:
- Num observations with std_diff >= TOL_DIFF_1: 0/3222277 (0.000%)
- Stata standard deviation: 1.51e+02

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

### DelayAcct

**Status**: ❌ FAILED

**Test Results**:
- Test 1 - Column names: ✅ PASSED
- Test 2 - Superset check: ❌ FAILED (Python missing 674090 Stata observations)
- Test 3 - Precision1 check: ❌ FAILED
- Test 4 - Precision2 check: ❌ FAILED

**Columns**: ['DelayAcct']

**Observations**:
- Stata:  674,090
- Python: 0
- Common: 0

**Missing Observations Sample**:
```
 index  permno  yyyymm  DelayAcct
     0   10001  199212   0.307460
     1   10001  199301   0.329167
     2   10001  199302   0.293849
     3   10001  199303   0.308783
     4   10001  199304   0.314104
     5   10001  199305   0.313442
     6   10001  199309   0.339221
     7   10001  199310   0.334278
     8   10001  199311   0.336795
     9   10001  199312   0.363150
```

---

### DelayNonAcct

**Status**: ❌ FAILED

**Test Results**:
- Test 1 - Column names: ✅ PASSED
- Test 2 - Superset check: ❌ FAILED (Python missing 674090 Stata observations)
- Test 3 - Precision1 check: ❌ FAILED
- Test 4 - Precision2 check: ❌ FAILED

**Columns**: ['DelayNonAcct']

**Observations**:
- Stata:  674,090
- Python: 0
- Common: 0

**Missing Observations Sample**:
```
 index  permno  yyyymm  DelayNonAcct
     0   10001  199212      0.539160
     1   10001  199301      0.517452
     2   10001  199302      0.552770
     3   10001  199303      0.537836
     4   10001  199304      0.532516
     5   10001  199305      0.533177
     6   10001  199309      0.659154
     7   10001  199310      0.664098
     8   10001  199311      0.661581
     9   10001  199312      0.635226
```

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

### DownsideBeta

**Status**: ❌ FAILED

**Test Results**:
- Test 1 - Column names: ✅ PASSED
- Test 2 - Superset check: ❌ FAILED (Python missing 4848559 Stata observations)
- Test 3 - Precision1 check: ❌ FAILED
- Test 4 - Precision2 check: ❌ FAILED

**Columns**: ['DownsideBeta']

**Observations**:
- Stata:  4,848,559
- Python: 0
- Common: 0

**Missing Observations Sample**:
```
 index  permno  yyyymm  DownsideBeta
     0   10000  198606      1.107329
     1   10000  198607      1.720590
     2   10000  198608      1.294280
     3   10000  198609      1.466464
     4   10000  198610      1.333412
     5   10000  198611      1.000356
     6   10000  198612      0.970582
     7   10000  198701      0.946452
     8   10000  198702      0.946339
     9   10000  198703      0.864751
```

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

### FailureProbability

**Status**: ❌ FAILED

**Test Results**:
- Test 1 - Column names: ✅ PASSED
- Test 2 - Superset check: ❌ FAILED (Python missing 13426 Stata observations)
- Test 3 - Precision1 check: ✅ PASSED
- Test 4 - Precision2 check: ✅ PASSED

**Columns**: ['FailureProbability']

**Observations**:
- Stata:  1,958,798
- Python: 2,235,710
- Common: 1,945,372

**Precision1**: 0.105% obs with std_diff >= 1.00e-02 (tolerance: < 10%)

**Precision2**: 99th percentile diff = 3.17e-06 (tolerance: < 1.00e+00)

**Summary Statistics** (Common Observations):

| Statistic  |          Stata |         Python |     Difference | Std Difference |
|------------|----------------|----------------|----------------|----------------|
| count      |       1.95e+06 |       1.95e+06 |       1.95e+06 |       1.95e+06 |
| mean       |       1.08e+06 |       1.10e+06 |     12854.8334 |       6.00e-04 |
| std        |       2.14e+07 |       4.98e+07 |       4.48e+07 |         2.0904 |
| min        |       -10.0057 |       -10.1657 |      -6.77e+08 |       -31.5742 |
| 25%        |        -5.9321 |         2.5649 |         7.7889 |       3.63e-07 |
| 50%        |        -4.5454 |         7.8521 |        11.8532 |       5.53e-07 |
| 75%        |        -2.1108 |        16.1749 |        18.1207 |       8.46e-07 |
| max        |       6.77e+08 |       1.05e+10 |       9.83e+09 |       458.7189 |

**Regression Analysis** (Python ~ Stata):

- **Model**: python = -7819.8276 + 1.0191 * stata
- **R-squared**: 0.1920
- **N observations**: 1,945,372

| Coefficient |     Estimate |    Std Error | t-statistic |   p-value |
|-------------|--------------|--------------|-------------|----------|
| Intercept   |   -7819.8276 |   32159.1322 |     -0.2432 |     0.808 |
| Slope       |       1.0191 |       0.0015 |    679.9809 |     0.000 |

**Missing Observations Sample**:
```
 index  permno  yyyymm  FailureProbability
     0   10001  198711           -3.110158
     1   10005  198805           -2.359228
     2   10007  198711            2.222355
     3   10008  198802           -2.768568
     4   10010  198803           -2.333784
     5   10012  198810           -2.782152
     6   10015  198505           -2.312654
     7   10016  198805           -6.327080
     8   10017  198712           -2.855397
     9   10018  198803           -3.369524
```

**Feedback**:
- Num observations with std_diff >= TOL_DIFF_1: 2049/1945372 (0.105%)
- Stata standard deviation: 2.14e+07

---

### FailureProbabilityJune

**Status**: ❌ FAILED

**Test Results**:
- Test 1 - Column names: ✅ PASSED
- Test 2 - Superset check: ❌ FAILED (Python missing 5397 Stata observations)
- Test 3 - Precision1 check: ✅ PASSED
- Test 4 - Precision2 check: ✅ PASSED

**Columns**: ['FailureProbabilityJune']

**Observations**:
- Stata:  2,090,935
- Python: 2,255,542
- Common: 2,085,538

**Precision1**: 0.258% obs with std_diff >= 1.00e-02 (tolerance: < 10%)

**Precision2**: 99th percentile diff = 3.58e-06 (tolerance: < 1.00e+00)

**Summary Statistics** (Common Observations):

| Statistic  |          Stata |         Python |     Difference | Std Difference |
|------------|----------------|----------------|----------------|----------------|
| count      |       2.09e+06 |       2.09e+06 |       2.09e+06 |       2.09e+06 |
| mean       |       1.03e+06 |       1.07e+06 |     40599.5039 |         0.0020 |
| std        |       2.07e+07 |       5.00e+07 |       4.53e+07 |         2.1878 |
| min        |        -9.7055 |        -9.2736 |      -6.77e+08 |       -32.6970 |
| 25%        |        -5.9405 |         2.6210 |         7.8772 |       3.81e-07 |
| 50%        |        -4.5904 |         7.9704 |        12.0623 |       5.83e-07 |
| 75%        |        -2.2199 |        16.4387 |        18.5606 |       8.97e-07 |
| max        |       6.77e+08 |       1.05e+10 |       9.83e+09 |       475.0311 |

**Regression Analysis** (Python ~ Stata):

- **Model**: python = 19485.6769 + 1.0204 * stata
- **R-squared**: 0.1787
- **N observations**: 2,085,538

| Coefficient |     Estimate |    Std Error | t-statistic |   p-value |
|-------------|--------------|--------------|-------------|----------|
| Intercept   |   19485.6769 |   31388.6013 |      0.6208 |     0.535 |
| Slope       |       1.0204 |       0.0015 |    673.6121 |     0.000 |

**Missing Observations Sample**:
```
 index  permno  yyyymm  FailureProbabilityJune
     0   10077  198806               -3.205529
     1   10077  198807               -3.205529
     2   10077  198808               -3.205529
     3   10077  198809               -3.205529
     4   10077  198810               -3.205529
     5   10077  198811               -3.205529
     6   10077  198812               -3.205529
     7   10077  198901               -3.205529
     8   10077  198902               -3.205529
     9   10077  198903               -3.205529
```

**Feedback**:
- Num observations with std_diff >= TOL_DIFF_1: 5372/2085538 (0.258%)
- Stata standard deviation: 2.07e+07

---

### ForecastDispersionLT

**Status**: ❌ FAILED

**Test Results**:
- Test 1 - Column names: ✅ PASSED
- Test 2 - Superset check: ❌ FAILED (Python missing 1774 Stata observations)
- Test 3 - Precision1 check: ✅ PASSED
- Test 4 - Precision2 check: ✅ PASSED

**Columns**: ['ForecastDispersionLT']

**Observations**:
- Stata:  828,578
- Python: 828,784
- Common: 826,804

**Precision1**: 0.087% obs with std_diff >= 1.00e-02 (tolerance: < 10%)

**Precision2**: 99th percentile diff = 1.49e-07 (tolerance: < 1.00e+00)

**Summary Statistics** (Common Observations):

| Statistic  |          Stata |         Python |     Difference | Std Difference |
|------------|----------------|----------------|----------------|----------------|
| count      |    826804.0000 |    826804.0000 |    826804.0000 |    826804.0000 |
| mean       |         4.5453 |         4.5451 |      -1.46e-04 |      -2.17e-05 |
| std        |         6.7281 |         6.7286 |         0.1312 |         0.0195 |
| min        |         0.0000 |         0.0000 |       -18.1600 |        -2.6991 |
| 25%        |         1.7100 |         1.7100 |         0.0000 |         0.0000 |
| 50%        |         3.0000 |         3.0000 |         0.0000 |         0.0000 |
| 75%        |         5.2000 |         5.2000 |       2.00e-08 |       2.97e-09 |
| max        |       623.7400 |       623.7400 |        41.1800 |         6.1206 |

**Regression Analysis** (Python ~ Stata):

- **Model**: python = 0.0004 + 0.9999 * stata
- **R-squared**: 0.9996
- **N observations**: 826,804

| Coefficient |     Estimate |    Std Error | t-statistic |   p-value |
|-------------|--------------|--------------|-------------|----------|
| Intercept   |     3.70e-04 |     1.74e-04 |      2.1263 |     0.033 |
| Slope       |       0.9999 |     2.14e-05 |  46632.5512 |     0.000 |

**Missing Observations Sample**:
```
 index  permno  yyyymm  ForecastDispersionLT
     0   11406  199609                  1.41
     1   11406  199610                  1.41
     2   12473  201012                  5.13
     3   12473  201101                  6.10
     4   12473  201710                  6.83
     5   12473  201711                  4.03
     6   12473  201712                  4.03
     7   12473  201801                  6.77
     8   12473  201802                  7.78
     9   12473  201803                  7.75
```

**Feedback**:
- Num observations with std_diff >= TOL_DIFF_1: 717/826804 (0.087%)
- Stata standard deviation: 6.73e+00

---

### GPlag

**Status**: ✅ PASSED

**Test Results**:
- Test 1 - Column names: ✅ PASSED
- Test 2 - Superset check: ✅ PASSED
- Test 3 - Precision1 check: ✅ PASSED
- Test 4 - Precision2 check: ✅ PASSED

**Columns**: ['GPlag']

**Observations**:
- Stata:  3,281,500
- Python: 3,297,874
- Common: 3,281,500

**Precision1**: 0.006% obs with std_diff >= 1.00e-02 (tolerance: < 10%)

**Precision2**: 99th percentile diff = 5.55e-08 (tolerance: < 1.00e+00)

**Summary Statistics** (Common Observations):

| Statistic  |          Stata |         Python |     Difference | Std Difference |
|------------|----------------|----------------|----------------|----------------|
| count      |       3.28e+06 |       3.28e+06 |       3.28e+06 |       3.28e+06 |
| mean       |         0.3420 |         0.3420 |      -2.68e-07 |      -2.36e-07 |
| std        |         1.1339 |         1.1339 |         0.0020 |         0.0018 |
| min        |       -28.7301 |       -28.7301 |        -0.2811 |        -0.2479 |
| 25%        |         0.0981 |         0.0981 |      -4.83e-09 |      -4.26e-09 |
| 50%        |         0.2774 |         0.2774 |         0.0000 |         0.0000 |
| 75%        |         0.4978 |         0.4978 |       4.90e-09 |       4.32e-09 |
| max        |       282.3216 |       282.3216 |         0.8837 |         0.7794 |

**Regression Analysis** (Python ~ Stata):

- **Model**: python = 0.0000 + 1.0000 * stata
- **R-squared**: 1.0000
- **N observations**: 3,281,500

| Coefficient |     Estimate |    Std Error | t-statistic |   p-value |
|-------------|--------------|--------------|-------------|----------|
| Intercept   |     2.14e-06 |     1.17e-06 |      1.8357 |     0.066 |
| Slope       |       1.0000 |     9.85e-07 |    1.02e+06 |     0.000 |

**Feedback**:
- Num observations with std_diff >= TOL_DIFF_1: 192/3281500 (0.006%)
- Stata standard deviation: 1.13e+00

---

### GPlag_q

**Status**: ❌ FAILED

**Test Results**:
- Test 1 - Column names: ✅ PASSED
- Test 2 - Superset check: ❌ FAILED (Python missing 81 Stata observations)
- Test 3 - Precision1 check: ✅ PASSED
- Test 4 - Precision2 check: ✅ PASSED

**Columns**: ['GPlag_q']

**Observations**:
- Stata:  2,216,580
- Python: 2,236,734
- Common: 2,216,499

**Precision1**: 0.015% obs with std_diff >= 1.00e-02 (tolerance: < 10%)

**Precision2**: 99th percentile diff = 1.78e-08 (tolerance: < 1.00e+00)

**Summary Statistics** (Common Observations):

| Statistic  |          Stata |         Python |     Difference | Std Difference |
|------------|----------------|----------------|----------------|----------------|
| count      |       2.22e+06 |       2.22e+06 |       2.22e+06 |       2.22e+06 |
| mean       |         0.0808 |         0.0808 |      -2.46e-07 |      -3.47e-07 |
| std        |         0.7089 |         0.7089 |         0.0017 |         0.0025 |
| min        |        -9.0482 |        -9.0482 |        -0.5642 |        -0.7959 |
| 25%        |         0.0314 |         0.0314 |      -1.36e-09 |      -1.92e-09 |
| 50%        |         0.0731 |         0.0731 |         0.0000 |         0.0000 |
| 75%        |         0.1240 |         0.1240 |       1.36e-09 |       1.92e-09 |
| max        |       598.7442 |       598.7442 |         0.7397 |         1.0434 |

**Regression Analysis** (Python ~ Stata):

- **Model**: python = -0.0000 + 1.0000 * stata
- **R-squared**: 1.0000
- **N observations**: 2,216,499

| Coefficient |     Estimate |    Std Error | t-statistic |   p-value |
|-------------|--------------|--------------|-------------|----------|
| Intercept   |    -7.93e-08 |     1.18e-06 |     -0.0672 |     0.946 |
| Slope       |       1.0000 |     1.65e-06 | 604773.0311 |     0.000 |

**Missing Observations Sample**:
```
 index  permno  yyyymm   GPlag_q
     0   10031  198607  0.248821
     1   10515  199607  0.024224
     2   10515  199608  0.024224
     3   10515  199609  0.024224
     4   10535  198805 -0.034978
     5   10536  199707  0.064386
     6   10824  198606  0.210711
     7   11362  199412  0.022848
     8   11545  199706  0.043206
     9   11545  199707  0.043206
```

**Feedback**:
- Num observations with std_diff >= TOL_DIFF_1: 325/2216499 (0.015%)
- Stata standard deviation: 7.09e-01

---

### GrGMToGrSales

**Status**: ✅ PASSED

**Test Results**:
- Test 1 - Column names: ✅ PASSED
- Test 2 - Superset check: ✅ PASSED
- Test 3 - Precision1 check: ✅ PASSED
- Test 4 - Precision2 check: ✅ PASSED

**Columns**: ['GrGMToGrSales']

**Observations**:
- Stata:  3,229,675
- Python: 3,294,865
- Common: 3,229,675

**Precision1**: 0.036% obs with std_diff >= 1.00e-02 (tolerance: < 10%)

**Precision2**: 99th percentile diff = 4.50e-09 (tolerance: < 1.00e+00)

**Summary Statistics** (Common Observations):

| Statistic  |          Stata |         Python |     Difference | Std Difference |
|------------|----------------|----------------|----------------|----------------|
| count      |       3.23e+06 |       3.23e+06 |       3.23e+06 |       3.23e+06 |
| mean       |        -1.0320 |            inf |            inf |            inf |
| std        |       213.3399 |            N/A |            N/A |            N/A |
| min        |    -90231.3050 |    -89952.2742 |     -4992.8331 |       -23.4032 |
| 25%        |        -0.0941 |        -0.0941 |      -2.51e-08 |      -1.18e-10 |
| 50%        |        -0.0024 |        -0.0024 |         0.0000 |         0.0000 |
| 75%        |         0.0784 |         0.0787 |       2.50e-08 |       1.17e-10 |
| max        |      7383.3198 |            inf |            inf |            inf |

**Regression Analysis** (Python ~ Stata):

- **Model**: python = inf + nan * stata
- **R-squared**: nan
- **N observations**: 3,229,675

| Coefficient |     Estimate |    Std Error | t-statistic |   p-value |
|-------------|--------------|--------------|-------------|----------|
| Intercept   |          nan |          nan |         nan |       nan |
| Slope       |          nan |          nan |         nan |       nan |

**Feedback**:
- Num observations with std_diff >= TOL_DIFF_1: 1161/3229675 (0.036%)
- Stata standard deviation: 2.13e+02

---

### GrSaleToGrReceivables

**Status**: ✅ PASSED

**Test Results**:
- Test 1 - Column names: ✅ PASSED
- Test 2 - Superset check: ✅ PASSED
- Test 3 - Precision1 check: ✅ PASSED
- Test 4 - Precision2 check: ✅ PASSED

**Columns**: ['GrSaleToGrReceivables']

**Observations**:
- Stata:  3,134,552
- Python: 3,303,855
- Common: 3,134,552

**Precision1**: 0.012% obs with std_diff >= 1.00e-02 (tolerance: < 10%)

**Precision2**: 99th percentile diff = 8.03e-10 (tolerance: < 1.00e+00)

**Summary Statistics** (Common Observations):

| Statistic  |          Stata |         Python |     Difference | Std Difference |
|------------|----------------|----------------|----------------|----------------|
| count      |       3.13e+06 |       3.13e+06 |       3.13e+06 |       3.13e+06 |
| mean       |        -0.7276 |        -0.7208 |         0.0068 |       2.50e-05 |
| std        |       272.2844 |       272.2685 |         2.4935 |         0.0092 |
| min        |    -93814.8910 |    -93814.8917 |      -122.8291 |        -0.4511 |
| 25%        |        -0.1435 |        -0.1435 |      -2.75e-09 |      -1.01e-11 |
| 50%        |         0.0056 |         0.0057 |       1.92e-12 |       7.06e-15 |
| 75%        |         0.1566 |         0.1568 |       2.77e-09 |       1.02e-11 |
| max        |     51770.8950 |     51770.8949 |      1176.6455 |         4.3214 |

**Regression Analysis** (Python ~ Stata):

- **Model**: python = 0.0067 + 0.9999 * stata
- **R-squared**: 0.9999
- **N observations**: 3,134,552

| Coefficient |     Estimate |    Std Error | t-statistic |   p-value |
|-------------|--------------|--------------|-------------|----------|
| Intercept   |       0.0067 |       0.0014 |      4.7865 |     0.000 |
| Slope       |       0.9999 |     5.17e-06 | 193323.0863 |     0.000 |

**Feedback**:
- Num observations with std_diff >= TOL_DIFF_1: 364/3134552 (0.012%)
- Stata standard deviation: 2.72e+02

---

### IdioVolCAPM

**Status**: ❌ FAILED

**Test Results**:
- Test 1 - Column names: ✅ PASSED
- Test 2 - Superset check: ❌ FAILED (Python missing 5026821 Stata observations)
- Test 3 - Precision1 check: ❌ FAILED
- Test 4 - Precision2 check: ❌ FAILED

**Columns**: ['IdioVolCAPM']

**Observations**:
- Stata:  5,026,821
- Python: 0
- Common: 0

**Missing Observations Sample**:
```
 index  permno  yyyymm  IdioVolCAPM
     0   10000  198601     0.061439
     1   10000  198602     0.031004
     2   10000  198603     0.044539
     3   10000  198604     0.011246
     4   10000  198605     0.038560
     5   10000  198606     0.019216
     6   10000  198607     0.046018
     7   10000  198608     0.096259
     8   10000  198609     0.047863
     9   10000  198610     0.040414
```

---

### IdioVolQF

**Status**: ❌ FAILED

**Test Results**:
- Test 1 - Column names: ✅ PASSED
- Test 2 - Superset check: ❌ FAILED (Python missing 3986461 Stata observations)
- Test 3 - Precision1 check: ❌ FAILED
- Test 4 - Precision2 check: ❌ FAILED

**Columns**: ['IdioVolQF']

**Observations**:
- Stata:  3,986,461
- Python: 0
- Common: 0

**Missing Observations Sample**:
```
 index  permno  yyyymm  IdioVolQF
     0   10000  198601   0.060926
     1   10000  198602   0.029838
     2   10000  198603   0.042672
     3   10000  198604   0.010589
     4   10000  198605   0.037976
     5   10000  198606   0.018890
     6   10000  198607   0.043929
     7   10000  198608   0.089077
     8   10000  198609   0.046870
     9   10000  198610   0.038371
```

---

### KZ

**Status**: ❌ FAILED

**Test Results**:
- Test 1 - Column names: ✅ PASSED
- Test 2 - Superset check: ❌ FAILED (Python missing 7 Stata observations)
- Test 3 - Precision1 check: ✅ PASSED
- Test 4 - Precision2 check: ✅ PASSED

**Columns**: ['KZ']

**Observations**:
- Stata:  2,630,499
- Python: 2,653,592
- Common: 2,630,492

**Precision1**: 0.000% obs with std_diff >= 1.00e-02 (tolerance: < 10%)

**Precision2**: 99th percentile diff = 2.04e-09 (tolerance: < 1.00e+00)

**Summary Statistics** (Common Observations):

| Statistic  |          Stata |         Python |     Difference | Std Difference |
|------------|----------------|----------------|----------------|----------------|
| count      |       2.63e+06 |       2.63e+06 |       2.63e+06 |       2.63e+06 |
| mean       |       -34.2551 |       -34.2551 |      -4.85e-05 |      -1.56e-08 |
| std        |      3118.1808 |      3118.1808 |         0.0315 |       1.01e-05 |
| min        |      -1.23e+06 |      -1.23e+06 |       -19.2429 |        -0.0062 |
| 25%        |        -5.2581 |        -5.2582 |      -4.09e-08 |      -1.31e-11 |
| 50%        |        -0.6982 |        -0.6982 |       1.23e-11 |       3.95e-15 |
| 75%        |         1.0179 |         1.0179 |       4.08e-08 |       1.31e-11 |
| max        |    205925.8400 |    205925.8463 |         3.3978 |         0.0011 |

**Regression Analysis** (Python ~ Stata):

- **Model**: python = -0.0000 + 1.0000 * stata
- **R-squared**: 1.0000
- **N observations**: 2,630,492

| Coefficient |     Estimate |    Std Error | t-statistic |   p-value |
|-------------|--------------|--------------|-------------|----------|
| Intercept   |    -4.85e-05 |     1.94e-05 |     -2.4938 |     0.013 |
| Slope       |       1.0000 |     6.23e-09 |    1.60e+08 |     0.000 |

**Missing Observations Sample**:
```
 index  permno  yyyymm       KZ
     0   12373  202406 2.156376
     1   12373  202407 2.170212
     2   12373  202408 2.171770
     3   12373  202409 2.175051
     4   12373  202410 2.172988
     5   12373  202411 2.188620
     6   12373  202412 2.174071
```

**Feedback**:
- Num observations with std_diff >= TOL_DIFF_1: 0/2630492 (0.000%)
- Stata standard deviation: 3.12e+03

---

### KZ_q

**Status**: ❌ FAILED

**Test Results**:
- Test 1 - Column names: ✅ PASSED
- Test 2 - Superset check: ❌ FAILED (Python missing 255 Stata observations)
- Test 3 - Precision1 check: ✅ PASSED
- Test 4 - Precision2 check: ✅ PASSED

**Columns**: ['KZ_q']

**Observations**:
- Stata:  1,936,942
- Python: 1,953,037
- Common: 1,936,687

**Precision1**: 0.001% obs with std_diff >= 1.00e-02 (tolerance: < 10%)

**Precision2**: 99th percentile diff = 3.12e-09 (tolerance: < 1.00e+00)

**Summary Statistics** (Common Observations):

| Statistic  |          Stata |         Python |     Difference | Std Difference |
|------------|----------------|----------------|----------------|----------------|
| count      |       1.94e+06 |       1.94e+06 |       1.94e+06 |       1.94e+06 |
| mean       |       -26.0737 |       -26.0742 |      -5.17e-04 |      -2.91e-07 |
| std        |      1776.1958 |      1776.1958 |         0.3830 |       2.16e-04 |
| min        |      -1.23e+06 |      -1.23e+06 |      -256.0814 |        -0.1442 |
| 25%        |        -4.8604 |        -4.8607 |      -3.96e-08 |      -2.23e-11 |
| 50%        |        -0.2486 |        -0.2486 |      -5.06e-12 |      -2.85e-15 |
| 75%        |         1.2951 |         1.2951 |       3.94e-08 |       2.22e-11 |
| max        |     26732.3870 |     26732.3858 |       130.4051 |         0.0734 |

**Regression Analysis** (Python ~ Stata):

- **Model**: python = -0.0005 + 1.0000 * stata
- **R-squared**: 1.0000
- **N observations**: 1,936,687

| Coefficient |     Estimate |    Std Error | t-statistic |   p-value |
|-------------|--------------|--------------|-------------|----------|
| Intercept   |    -5.18e-04 |     2.75e-04 |     -1.8810 |     0.060 |
| Slope       |       1.0000 |     1.55e-07 |    6.45e+06 |     0.000 |

**Missing Observations Sample**:
```
 index  permno  yyyymm      KZ_q
     0   10515  199604 -4.790903
     1   10515  199605 -4.929575
     2   10515  199606 -4.921965
     3   10986  199008  8.309092
     4   10994  199204  5.937374
     5   10994  199205  6.358468
     6   11212  199008 -1.955831
     7   11545  199612 -1.467011
     8   11545  199701 -1.472400
     9   11545  199702 -1.472400
```

**Feedback**:
- Num observations with std_diff >= TOL_DIFF_1: 20/1936687 (0.001%)
- Stata standard deviation: 1.78e+03

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

### OScore_q

**Status**: ❌ FAILED

**Test Results**:
- Test 1 - Column names: ✅ PASSED
- Test 2 - Superset check: ❌ FAILED (Python missing 3198 Stata observations)
- Test 3 - Precision1 check: ✅ PASSED
- Test 4 - Precision2 check: ✅ PASSED

**Columns**: ['OScore_q']

**Observations**:
- Stata:  877,922
- Python: 886,880
- Common: 874,724

**Precision1**: 0.000% obs with std_diff >= 1.00e-02 (tolerance: < 10%)

**Precision2**: 99th percentile diff = 0.00e+00 (tolerance: < 1.00e+00)

**Summary Statistics** (Common Observations):

| Statistic  |          Stata |         Python |     Difference | Std Difference |
|------------|----------------|----------------|----------------|----------------|
| count      |    874724.0000 |    874724.0000 |    874724.0000 |    874724.0000 |
| mean       |         0.1226 |         0.1226 |         0.0000 |         0.0000 |
| std        |         0.3280 |         0.3280 |         0.0000 |         0.0000 |
| min        |         0.0000 |         0.0000 |         0.0000 |         0.0000 |
| 25%        |         0.0000 |         0.0000 |         0.0000 |         0.0000 |
| 50%        |         0.0000 |         0.0000 |         0.0000 |         0.0000 |
| 75%        |         0.0000 |         0.0000 |         0.0000 |         0.0000 |
| max        |         1.0000 |         1.0000 |         0.0000 |         0.0000 |

**Regression Analysis** (Python ~ Stata):

- **Model**: python = 0.0000 + 1.0000 * stata
- **R-squared**: 1.0000
- **N observations**: 874,724

| Coefficient |     Estimate |    Std Error | t-statistic |   p-value |
|-------------|--------------|--------------|-------------|----------|
| Intercept   |     1.16e-13 |     3.64e-16 |    318.9745 |     0.000 |
| Slope       |       1.0000 |     1.04e-15 |    9.62e+14 |     0.000 |

**Missing Observations Sample**:
```
 index  permno  yyyymm  OScore_q
     0   10012  199303         1
     1   10028  200109         1
     2   10028  201906         0
     3   10028  201912         0
     4   10031  198610         0
     5   10035  200108         0
     6   10042  198806         0
     7   10051  199703         1
     8   10062  199309         1
     9   10074  198911         1
```

**Feedback**:
- Num observations with std_diff >= TOL_DIFF_1: 0/874724 (0.000%)
- Stata standard deviation: 3.28e-01

---

### OperProfLag

**Status**: ❌ FAILED

**Test Results**:
- Test 1 - Column names: ✅ PASSED
- Test 2 - Superset check: ❌ FAILED (Python missing 64 Stata observations)
- Test 3 - Precision1 check: ✅ PASSED
- Test 4 - Precision2 check: ✅ PASSED

**Columns**: ['OperProfLag']

**Observations**:
- Stata:  1,292,263
- Python: 1,297,970
- Common: 1,292,199

**Precision1**: 0.009% obs with std_diff >= 1.00e-02 (tolerance: < 10%)

**Precision2**: 99th percentile diff = 1.45e-08 (tolerance: < 1.00e+00)

**Summary Statistics** (Common Observations):

| Statistic  |          Stata |         Python |     Difference | Std Difference |
|------------|----------------|----------------|----------------|----------------|
| count      |       1.29e+06 |       1.29e+06 |       1.29e+06 |       1.29e+06 |
| mean       |         0.2731 |         0.2727 |      -4.19e-04 |      -5.99e-05 |
| std        |         6.9921 |         6.9710 |         0.5401 |         0.0772 |
| min        |     -1594.7000 |     -1594.7000 |      -609.1517 |       -87.1201 |
| 25%        |         0.1432 |         0.1432 |      -5.76e-09 |      -8.24e-10 |
| 50%        |         0.2804 |         0.2804 |       3.33e-16 |       4.76e-17 |
| 75%        |         0.4266 |         0.4266 |       5.79e-09 |       8.28e-10 |
| max        |      1096.4845 |      1096.4845 |        66.9652 |         9.5773 |

**Regression Analysis** (Python ~ Stata):

- **Model**: python = 0.0012 + 0.9940 * stata
- **R-squared**: 0.9940
- **N observations**: 1,292,199

| Coefficient |     Estimate |    Std Error | t-statistic |   p-value |
|-------------|--------------|--------------|-------------|----------|
| Intercept   |       0.0012 |     4.74e-04 |      2.5684 |     0.010 |
| Slope       |       0.9940 |     6.77e-05 |  14671.7650 |     0.000 |

**Missing Observations Sample**:
```
 index  permno  yyyymm  OperProfLag
     0   10264  198803    -0.553213
     1   10517  202106     1.199436
     2   10517  202107     1.199436
     3   10517  202108     1.199436
     4   10517  202109     1.199436
     5   10517  202110     1.199436
     6   10517  202111     1.199436
     7   10517  202112     1.199436
     8   10517  202201     1.199436
     9   10517  202202     1.199436
```

**Feedback**:
- Num observations with std_diff >= TOL_DIFF_1: 117/1292199 (0.009%)
- Stata standard deviation: 6.99e+00

---

### OperProfLag_q

**Status**: ❌ FAILED

**Test Results**:
- Test 1 - Column names: ✅ PASSED
- Test 2 - Superset check: ❌ FAILED (Python missing 52 Stata observations)
- Test 3 - Precision1 check: ✅ PASSED
- Test 4 - Precision2 check: ✅ PASSED

**Columns**: ['OperProfLag_q']

**Observations**:
- Stata:  2,395,707
- Python: 2,407,547
- Common: 2,395,655

**Precision1**: 0.001% obs with std_diff >= 1.00e-02 (tolerance: < 10%)

**Precision2**: 99th percentile diff = 9.22e-13 (tolerance: < 1.00e+00)

**Summary Statistics** (Common Observations):

| Statistic  |          Stata |         Python |     Difference | Std Difference |
|------------|----------------|----------------|----------------|----------------|
| count      |       2.40e+06 |       2.40e+06 |       2.40e+06 |       2.40e+06 |
| mean       |       -70.1493 |            N/A |            N/A |            N/A |
| std        |    252627.2555 |            N/A |            N/A |            N/A |
| min        |      -3.48e+08 |           -inf |           -inf |           -inf |
| 25%        |        -0.0048 |        -0.0048 |      -6.83e-09 |      -2.70e-14 |
| 50%        |         0.0444 |         0.0444 |         0.0000 |         0.0000 |
| 75%        |         0.0849 |         0.0849 |       6.85e-09 |       2.71e-14 |
| max        |       9.52e+07 |            inf |            inf |            inf |

**Regression Analysis** (Python ~ Stata):

- **Model**: python = nan + nan * stata
- **R-squared**: nan
- **N observations**: 2,395,655

| Coefficient |     Estimate |    Std Error | t-statistic |   p-value |
|-------------|--------------|--------------|-------------|----------|
| Intercept   |          nan |          nan |         nan |       nan |
| Slope       |          nan |          nan |         nan |       nan |

**Missing Observations Sample**:
```
 index  permno  yyyymm  OperProfLag_q
     0   10515  199604       0.002818
     1   10515  199605       0.002818
     2   10515  199606       0.002818
     3   11545  199706       0.044945
     4   11545  199707       0.044945
     5   11545  199708       0.044945
     6   12750  198212       0.014304
     7   12750  198301       0.014304
     8   12750  198302       0.014304
     9   12837  198004      -0.470808
```

**Feedback**:
- Num observations with std_diff >= TOL_DIFF_1: 12/2395655 (0.001%)
- Stata standard deviation: 2.53e+05

---

### OperProfRDLagAT

**Status**: ❌ FAILED

**Test Results**:
- Test 1 - Column names: ✅ PASSED
- Test 2 - Superset check: ❌ FAILED (Python missing 60 Stata observations)
- Test 3 - Precision1 check: ✅ PASSED
- Test 4 - Precision2 check: ✅ PASSED

**Columns**: ['OperProfRDLagAT']

**Observations**:
- Stata:  2,742,767
- Python: 2,756,887
- Common: 2,742,707

**Precision1**: 0.003% obs with std_diff >= 1.00e-02 (tolerance: < 10%)

**Precision2**: 99th percentile diff = 2.29e-08 (tolerance: < 1.00e+00)

**Summary Statistics** (Common Observations):

| Statistic  |          Stata |         Python |     Difference | Std Difference |
|------------|----------------|----------------|----------------|----------------|
| count      |       2.74e+06 |       2.74e+06 |       2.74e+06 |       2.74e+06 |
| mean       |         0.1294 |         0.1294 |      -5.41e-07 |      -4.56e-07 |
| std        |         1.1878 |         1.1878 |       2.24e-04 |       1.89e-04 |
| min        |      -200.7273 |      -200.7273 |        -0.0766 |        -0.0645 |
| 25%        |         0.0319 |         0.0319 |      -2.70e-09 |      -2.27e-09 |
| 50%        |         0.1280 |         0.1281 |      -3.79e-12 |      -3.19e-12 |
| 75%        |         0.2154 |         0.2154 |       2.68e-09 |       2.26e-09 |
| max        |       226.5365 |       226.5365 |         0.0170 |         0.0143 |

**Regression Analysis** (Python ~ Stata):

- **Model**: python = -0.0000 + 1.0000 * stata
- **R-squared**: 1.0000
- **N observations**: 2,742,707

| Coefficient |     Estimate |    Std Error | t-statistic |   p-value |
|-------------|--------------|--------------|-------------|----------|
| Intercept   |    -5.99e-07 |     1.36e-07 |     -4.4054 |     0.000 |
| Slope       |       1.0000 |     1.14e-07 |    8.78e+06 |     0.000 |

**Missing Observations Sample**:
```
 index  permno  yyyymm  OperProfRDLagAT
     0   10517  202106         0.631911
     1   10517  202107         0.631911
     2   10517  202108         0.631911
     3   10517  202109         0.631911
     4   10517  202110         0.631911
     5   10517  202111         0.631911
     6   10517  202112         0.631911
     7   10517  202201         0.631911
     8   10517  202202         0.631911
     9   10517  202203         0.631911
```

**Feedback**:
- Num observations with std_diff >= TOL_DIFF_1: 72/2742707 (0.003%)
- Stata standard deviation: 1.19e+00

---

### OperProfRDLagAT_q

**Status**: ❌ FAILED

**Test Results**:
- Test 1 - Column names: ✅ PASSED
- Test 2 - Superset check: ❌ FAILED (Python missing 144 Stata observations)
- Test 3 - Precision1 check: ✅ PASSED
- Test 4 - Precision2 check: ✅ PASSED

**Columns**: ['OperProfRDLagAT_q']

**Observations**:
- Stata:  1,800,025
- Python: 1,816,859
- Common: 1,799,881

**Precision1**: 0.019% obs with std_diff >= 1.00e-02 (tolerance: < 10%)

**Precision2**: 99th percentile diff = 6.60e-08 (tolerance: < 1.00e+00)

**Summary Statistics** (Common Observations):

| Statistic  |          Stata |         Python |     Difference | Std Difference |
|------------|----------------|----------------|----------------|----------------|
| count      |       1.80e+06 |       1.80e+06 |       1.80e+06 |       1.80e+06 |
| mean       |         0.0249 |         0.0249 |       6.70e-07 |       5.09e-06 |
| std        |         0.1317 |         0.1317 |         0.0014 |         0.0107 |
| min        |       -10.0000 |       -10.0000 |        -0.4914 |        -3.7306 |
| 25%        |         0.0110 |         0.0110 |      -7.24e-10 |      -5.50e-09 |
| 50%        |         0.0317 |         0.0317 |         0.0000 |         0.0000 |
| 75%        |         0.0522 |         0.0522 |       7.22e-10 |       5.48e-09 |
| max        |        54.3953 |        54.3953 |         0.6825 |         5.1816 |

**Regression Analysis** (Python ~ Stata):

- **Model**: python = 0.0000 + 0.9999 * stata
- **R-squared**: 0.9999
- **N observations**: 1,799,881

| Coefficient |     Estimate |    Std Error | t-statistic |   p-value |
|-------------|--------------|--------------|-------------|----------|
| Intercept   |     3.19e-06 |     1.07e-06 |      2.9886 |     0.003 |
| Slope       |       0.9999 |     7.97e-06 | 125428.7784 |     0.000 |

**Missing Observations Sample**:
```
 index  permno  yyyymm  OperProfRDLagAT_q
     0   10031  198607           0.030236
     1   10515  199607           0.007740
     2   10515  199608           0.007740
     3   10515  199609           0.007740
     4   10517  202006           0.168328
     5   10517  202007           0.168328
     6   10517  202008           0.168328
     7   10517  202009           0.160288
     8   10517  202010           0.160288
     9   10517  202011           0.160288
```

**Feedback**:
- Num observations with std_diff >= TOL_DIFF_1: 345/1799881 (0.019%)
- Stata standard deviation: 1.32e-01

---

### PM

**Status**: ✅ PASSED

**Test Results**:
- Test 1 - Column names: ✅ PASSED
- Test 2 - Superset check: ✅ PASSED
- Test 3 - Precision1 check: ✅ PASSED
- Test 4 - Precision2 check: ✅ PASSED

**Columns**: ['PM']

**Observations**:
- Stata:  3,547,773
- Python: 3,616,983
- Common: 3,547,773

**Precision1**: 0.000% obs with std_diff >= 1.00e-02 (tolerance: < 10%)

**Precision2**: 99th percentile diff = 2.31e-09 (tolerance: < 1.00e+00)

**Summary Statistics** (Common Observations):

| Statistic  |          Stata |         Python |     Difference | Std Difference |
|------------|----------------|----------------|----------------|----------------|
| count      |       3.55e+06 |       3.55e+06 |       3.55e+06 |       3.55e+06 |
| mean       |        -4.0283 |        -4.0283 |      -1.02e-06 |      -4.83e-09 |
| std        |       211.9918 |       211.9919 |       4.41e-04 |       2.08e-06 |
| min        |    -84221.6640 |    -84221.6667 |        -0.1893 |      -8.93e-04 |
| 25%        |        -0.0177 |        -0.0177 |      -1.41e-09 |      -6.64e-12 |
| 50%        |         0.0398 |         0.0398 |         0.0000 |         0.0000 |
| 75%        |         0.0957 |         0.0957 |       1.42e-09 |       6.69e-12 |
| max        |     10418.0800 |     10418.0800 |         0.0391 |       1.85e-04 |

**Regression Analysis** (Python ~ Stata):

- **Model**: python = -0.0000 + 1.0000 * stata
- **R-squared**: 1.0000
- **N observations**: 3,547,773

| Coefficient |     Estimate |    Std Error | t-statistic |   p-value |
|-------------|--------------|--------------|-------------|----------|
| Intercept   |    -9.60e-07 |     2.34e-07 |     -4.1007 |     0.000 |
| Slope       |       1.0000 |     1.10e-09 |    9.05e+08 |     0.000 |

**Feedback**:
- Num observations with std_diff >= TOL_DIFF_1: 0/3547773 (0.000%)
- Stata standard deviation: 2.12e+02

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

### PS_q

**Status**: ❌ FAILED

**Test Results**:
- Test 1 - Column names: ✅ PASSED
- Test 2 - Superset check: ❌ FAILED (Python missing 60 Stata observations)
- Test 3 - Precision1 check: ❌ FAILED
- Test 4 - Precision2 check: ❌ FAILED

**Columns**: ['PS_q']

**Observations**:
- Stata:  310,650
- Python: 310,826
- Common: 310,590

**Precision1**: 53.974% obs with std_diff >= 1.00e-02 (tolerance: < 10%)

**Precision2**: 99th percentile diff = 3.16e+00 (tolerance: < 1.00e+00)

**Summary Statistics** (Common Observations):

| Statistic  |          Stata |         Python |     Difference | Std Difference |
|------------|----------------|----------------|----------------|----------------|
| count      |    310590.0000 |    310590.0000 |    310590.0000 |    310590.0000 |
| mean       |         5.2219 |         4.7472 |        -0.4747 |        -0.3003 |
| std        |         1.5810 |         1.7853 |         1.4651 |         0.9267 |
| min        |         1.0000 |         1.0000 |        -6.0000 |        -3.7951 |
| 25%        |         4.0000 |         3.0000 |        -1.0000 |        -0.6325 |
| 50%        |         5.0000 |         5.0000 |         0.0000 |         0.0000 |
| 75%        |         6.0000 |         6.0000 |         0.0000 |         0.0000 |
| max        |         9.0000 |         9.0000 |         4.0000 |         2.5301 |

**Regression Analysis** (Python ~ Stata):

- **Model**: python = 1.0490 + 0.7082 * stata
- **R-squared**: 0.3933
- **N observations**: 310,590

| Coefficient |     Estimate |    Std Error | t-statistic |   p-value |
|-------------|--------------|--------------|-------------|----------|
| Intercept   |       1.0490 |       0.0086 |    121.8142 |     0.000 |
| Slope       |       0.7082 |       0.0016 |    448.7187 |     0.000 |

**Missing Observations Sample**:
```
 index  permno  yyyymm  PS_q
     0   10515  199604     5
     1   10515  199605     6
     2   10515  199606     6
     3   11394  201803     5
     4   11394  201804     5
     5   11394  201805     5
     6   11874  199706     5
     7   11874  199707     5
     8   11874  199708     5
     9   14011  201703     5
```

**Feedback**:
- Num observations with std_diff >= TOL_DIFF_1: 167637/310590 (53.974%)
- Stata standard deviation: 1.58e+00

**Most Recent Bad Observations**:
```
   permno  yyyymm  python  stata  diff
0   11174  202412     2.0      3  -1.0
1   11593  202412     8.0      7   1.0
2   11701  202412     5.0      6  -1.0
3   11775  202412     6.0      7  -1.0
4   11790  202412     4.0      5  -1.0
5   12880  202412     5.0      6  -1.0
6   13116  202412     6.0      5   1.0
7   13124  202412     6.0      5   1.0
8   13337  202412     4.0      5  -1.0
9   13583  202412     3.0      8  -5.0
```

**Largest Differences**:
```
   permno  yyyymm  python  stata  diff
0   10005  198706     1.0      7  -6.0
1   10005  198707     1.0      7  -6.0
2   10005  198708     1.0      7  -6.0
3   10005  198709     1.0      7  -6.0
4   10005  198710     1.0      7  -6.0
5   10005  198711     1.0      7  -6.0
6   10005  198712     2.0      8  -6.0
7   10005  198801     2.0      8  -6.0
8   10005  198802     2.0      8  -6.0
9   10005  198803     1.0      7  -6.0
```

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

### RetNOA

**Status**: ❌ FAILED

**Test Results**:
- Test 1 - Column names: ✅ PASSED
- Test 2 - Superset check: ❌ FAILED (Python missing 1 Stata observations)
- Test 3 - Precision1 check: ✅ PASSED
- Test 4 - Precision2 check: ✅ PASSED

**Columns**: ['RetNOA']

**Observations**:
- Stata:  2,892,942
- Python: 2,921,223
- Common: 2,892,941

**Precision1**: 0.001% obs with std_diff >= 1.00e-02 (tolerance: < 10%)

**Precision2**: 99th percentile diff = 1.40e-19 (tolerance: < 1.00e+00)

**Summary Statistics** (Common Observations):

| Statistic  |          Stata |         Python |     Difference | Std Difference |
|------------|----------------|----------------|----------------|----------------|
| count      |       2.89e+06 |       2.89e+06 |       2.89e+06 |       2.89e+06 |
| mean       |       2.31e+11 |            inf |            inf |            inf |
| std        |       1.27e+14 |            N/A |            N/A |            N/A |
| min        |      -5.90e+15 |      -5.90e+15 |      -1.75e+09 |      -1.37e-05 |
| 25%        |        -0.0320 |        -0.0320 |      -6.74e-09 |      -5.29e-23 |
| 50%        |         0.1203 |         0.1203 |      -1.19e-12 |      -9.33e-27 |
| 75%        |         0.2648 |         0.2648 |       6.73e-09 |       5.28e-23 |
| max        |       6.23e+16 |            inf |            inf |            inf |

**Regression Analysis** (Python ~ Stata):

- **Model**: python = inf + inf * stata
- **R-squared**: nan
- **N observations**: 2,892,941

| Coefficient |     Estimate |    Std Error | t-statistic |   p-value |
|-------------|--------------|--------------|-------------|----------|
| Intercept   |          nan |          nan |         nan |       nan |
| Slope       |          nan |          nan |         nan |       nan |

**Missing Observations Sample**:
```
 index  permno  yyyymm   RetNOA
     0   23800  196507 0.041734
```

**Feedback**:
- Num observations with std_diff >= TOL_DIFF_1: 24/2892941 (0.001%)
- Stata standard deviation: 1.27e+14

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

### ReturnSkewCAPM

**Status**: ❌ FAILED

**Test Results**:
- Test 1 - Column names: ✅ PASSED
- Test 2 - Superset check: ❌ FAILED (Python missing 4997359 Stata observations)
- Test 3 - Precision1 check: ❌ FAILED
- Test 4 - Precision2 check: ❌ FAILED

**Columns**: ['ReturnSkewCAPM']

**Observations**:
- Stata:  4,997,359
- Python: 0
- Common: 0

**Missing Observations Sample**:
```
 index  permno  yyyymm  ReturnSkewCAPM
     0   10000  198601        2.244703
     1   10000  198602       -0.730520
     2   10000  198603        1.687384
     3   10000  198604       -0.274580
     4   10000  198605        1.245450
     5   10000  198606       -0.110014
     6   10000  198607        0.877926
     7   10000  198608       -1.039173
     8   10000  198609        0.639478
     9   10000  198610       -1.519597
```

---

### ReturnSkewQF

**Status**: ❌ FAILED

**Test Results**:
- Test 1 - Column names: ✅ PASSED
- Test 2 - Superset check: ❌ FAILED (Python missing 3985016 Stata observations)
- Test 3 - Precision1 check: ❌ FAILED
- Test 4 - Precision2 check: ❌ FAILED

**Columns**: ['ReturnSkewQF']

**Observations**:
- Stata:  3,985,016
- Python: 0
- Common: 0

**Missing Observations Sample**:
```
 index  permno  yyyymm  ReturnSkewQF
     0   10000  198601      2.136304
     1   10000  198602     -0.730719
     2   10000  198603      1.318269
     3   10000  198604      0.291021
     4   10000  198605      1.151838
     5   10000  198606     -0.198608
     6   10000  198607      0.503765
     7   10000  198608     -0.426768
     8   10000  198609      0.589325
     9   10000  198610     -1.740994
```

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

### WW

**Status**: ❌ FAILED

**Test Results**:
- Test 1 - Column names: ✅ PASSED
- Test 2 - Superset check: ❌ FAILED (Python missing 101 Stata observations)
- Test 3 - Precision1 check: ✅ PASSED
- Test 4 - Precision2 check: ✅ PASSED

**Columns**: ['WW']

**Observations**:
- Stata:  2,702,805
- Python: 2,758,348
- Common: 2,702,704

**Precision1**: 0.002% obs with std_diff >= 1.00e-02 (tolerance: < 10%)

**Precision2**: 99th percentile diff = 4.65e-10 (tolerance: < 1.00e+00)

**Summary Statistics** (Common Observations):

| Statistic  |          Stata |         Python |     Difference | Std Difference |
|------------|----------------|----------------|----------------|----------------|
| count      |       2.70e+06 |       2.70e+06 |       2.70e+06 |       2.70e+06 |
| mean       |        -0.1112 |            inf |            inf |            inf |
| std        |        54.8169 |            N/A |            N/A |            N/A |
| min        |      -111.6833 |      -111.6833 |        -4.4987 |        -0.0821 |
| 25%        |        -0.3470 |        -0.3470 |      -5.05e-09 |      -9.20e-11 |
| 50%        |        -0.2572 |        -0.2572 |       7.59e-12 |       1.39e-13 |
| 75%        |        -0.1745 |        -0.1745 |       5.05e-09 |       9.21e-11 |
| max        |     76241.1800 |            inf |            inf |            inf |

**Regression Analysis** (Python ~ Stata):

- **Model**: python = inf + inf * stata
- **R-squared**: nan
- **N observations**: 2,702,704

| Coefficient |     Estimate |    Std Error | t-statistic |   p-value |
|-------------|--------------|--------------|-------------|----------|
| Intercept   |          nan |          nan |         nan |       nan |
| Slope       |          nan |          nan |         nan |       nan |

**Missing Observations Sample**:
```
 index  permno  yyyymm        WW
     0   10193  198803 -0.070419
     1   10193  198804 -0.071916
     2   10264  198803 -0.070417
     3   10274  198806  0.199467
     4   10274  198807  0.195080
     5   10274  198808  0.197029
     6   10274  198809  0.194967
     7   10535  198902 -0.057308
     8   10544  198811 -0.114865
     9   10544  198812 -0.114869
```

**Feedback**:
- Num observations with std_diff >= TOL_DIFF_1: 41/2702704 (0.002%)
- Stata standard deviation: 5.48e+01

---

### WW_Q

**Status**: ❌ FAILED

**Test Results**:
- Test 1 - Column names: ✅ PASSED
- Test 2 - Superset check: ❌ FAILED (Python missing 44 Stata observations)
- Test 3 - Precision1 check: ✅ PASSED
- Test 4 - Precision2 check: ✅ PASSED

**Columns**: ['WW_Q']

**Observations**:
- Stata:  2,406,602
- Python: 2,493,801
- Common: 2,406,558

**Precision1**: 0.001% obs with std_diff >= 1.00e-02 (tolerance: < 10%)

**Precision2**: 99th percentile diff = 2.62e-07 (tolerance: < 1.00e+00)

**Summary Statistics** (Common Observations):

| Statistic  |          Stata |         Python |     Difference | Std Difference |
|------------|----------------|----------------|----------------|----------------|
| count      |       2.41e+06 |       2.41e+06 |       2.41e+06 |       2.41e+06 |
| mean       |        -0.0942 |           -inf |           -inf |           -inf |
| std        |        80.9101 |            N/A |            N/A |            N/A |
| min        |     -1099.2520 |           -inf |           -inf |           -inf |
| 25%        |        -0.3578 |        -0.3578 |      -6.01e-09 |      -7.42e-11 |
| 50%        |        -0.2663 |        -0.2663 |      -3.11e-12 |      -3.84e-14 |
| 75%        |        -0.1791 |        -0.1791 |       6.00e-09 |       7.41e-11 |
| max        |     75674.3520 |     75674.3568 |        15.5945 |         0.1927 |

**Regression Analysis** (Python ~ Stata):

- **Model**: python = -inf + inf * stata
- **R-squared**: nan
- **N observations**: 2,406,551

| Coefficient |     Estimate |    Std Error | t-statistic |   p-value |
|-------------|--------------|--------------|-------------|----------|
| Intercept   |          nan |          nan |         nan |       nan |
| Slope       |          nan |          nan |         nan |       nan |

**Missing Observations Sample**:
```
 index  permno  yyyymm      WW_Q
     0   10515  199604 -0.192867
     1   10515  199605 -0.198629
     2   10515  199606 -0.190664
     3   10535  198805  0.097225
     4   11545  199706 -0.169969
     5   11545  199707 -0.161824
     6   11545  199708 -0.155090
     7   12750  198212 -0.038403
     8   12750  198301 -0.042673
     9   12750  198302 -0.043110
```

**Feedback**:
- Num observations with std_diff >= TOL_DIFF_1: 33/2406558 (0.001%)
- Stata standard deviation: 8.09e+01

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

### betaCC

**Status**: ❌ FAILED

**Test Results**:
- Test 1 - Column names: ✅ PASSED
- Test 2 - Superset check: ❌ FAILED (Python missing 3459006 Stata observations)
- Test 3 - Precision1 check: ❌ FAILED
- Test 4 - Precision2 check: ❌ FAILED

**Columns**: ['betaCC']

**Observations**:
- Stata:  3,459,006
- Python: 0
- Common: 0

**Missing Observations Sample**:
```
 index  permno  yyyymm    betaCC
     0   10001  198912 96.556709
     1   10001  199001 78.446892
     2   10001  199002 81.491409
     3   10001  199003 77.058983
     4   10001  199004 69.123657
     5   10001  199005 65.499115
     6   10001  199006 62.682751
     7   10001  199007 54.436337
     8   10001  199008 59.355011
     9   10001  199009 56.830456
```

---

### betaCR

**Status**: ❌ FAILED

**Test Results**:
- Test 1 - Column names: ✅ PASSED
- Test 2 - Superset check: ❌ FAILED (Python missing 3459006 Stata observations)
- Test 3 - Precision1 check: ❌ FAILED
- Test 4 - Precision2 check: ❌ FAILED

**Columns**: ['betaCR']

**Observations**:
- Stata:  3,459,006
- Python: 0
- Common: 0

**Missing Observations Sample**:
```
 index  permno  yyyymm    betaCR
     0   10001  198912 -4.462341
     1   10001  199001  7.927080
     2   10001  199002 10.556782
     3   10001  199003 10.227539
     4   10001  199004 17.441637
     5   10001  199005 14.496083
     6   10001  199006  7.174622
     7   10001  199007  8.668968
     8   10001  199008 -8.670435
     9   10001  199009 -8.461947
```

---

### betaNet

**Status**: ❌ FAILED

**Test Results**:
- Test 1 - Column names: ✅ PASSED
- Test 2 - Superset check: ❌ FAILED (Python missing 3420591 Stata observations)
- Test 3 - Precision1 check: ❌ FAILED
- Test 4 - Precision2 check: ❌ FAILED

**Columns**: ['betaNet']

**Observations**:
- Stata:  3,420,591
- Python: 0
- Common: 0

**Missing Observations Sample**:
```
 index  permno  yyyymm    betaNet
     0   10001  198912 101.080060
     1   10001  199001  70.609283
     2   10001  199002  71.023659
     3   10001  199003  66.917381
     4   10001  199004  51.771923
     5   10001  199005  51.066372
     6   10001  199006  55.570599
     7   10001  199007  45.826405
     8   10001  199008  68.131134
     9   10001  199009  65.379723
```

---

### betaRC

**Status**: ❌ FAILED

**Test Results**:
- Test 1 - Column names: ✅ PASSED
- Test 2 - Superset check: ❌ FAILED (Python missing 3421560 Stata observations)
- Test 3 - Precision1 check: ❌ FAILED
- Test 4 - Precision2 check: ❌ FAILED

**Columns**: ['betaRC']

**Observations**:
- Stata:  3,421,560
- Python: 0
- Common: 0

**Missing Observations Sample**:
```
 index  permno  yyyymm    betaRC
     0   10001  198912 -0.037640
     1   10001  199001 -0.049183
     2   10001  199002 -0.051516
     3   10001  199003 -0.049271
     4   10001  199004 -0.050521
     5   10001  199005 -0.039892
     6   10001  199006 -0.039184
     7   10001  199007 -0.036623
     8   10001  199008 -0.052458
     9   10001  199009 -0.042971
```

---

### betaRR

**Status**: ❌ FAILED

**Test Results**:
- Test 1 - Column names: ✅ PASSED
- Test 2 - Superset check: ❌ FAILED (Python missing 3421560 Stata observations)
- Test 3 - Precision1 check: ❌ FAILED
- Test 4 - Precision2 check: ❌ FAILED

**Columns**: ['betaRR']

**Observations**:
- Stata:  3,421,560
- Python: 0
- Common: 0

**Missing Observations Sample**:
```
 index  permno  yyyymm   betaRR
     0   10001  198912 0.023374
     1   10001  199001 0.040286
     2   10001  199002 0.037514
     3   10001  199003 0.036667
     4   10001  199004 0.039381
     5   10001  199005 0.023447
     6   10001  199006 0.023286
     7   10001  199007 0.022415
     8   10001  199008 0.053231
     9   10001  199009 0.044351
```

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

### currat

**Status**: ✅ PASSED

**Test Results**:
- Test 1 - Column names: ✅ PASSED
- Test 2 - Superset check: ✅ PASSED
- Test 3 - Precision1 check: ✅ PASSED
- Test 4 - Precision2 check: ✅ PASSED

**Columns**: ['currat']

**Observations**:
- Stata:  3,065,278
- Python: 3,625,095
- Common: 3,065,278

**Precision1**: 0.000% obs with std_diff >= 1.00e-02 (tolerance: < 10%)

**Precision2**: 99th percentile diff = 1.40e-08 (tolerance: < 1.00e+00)

**Summary Statistics** (Common Observations):

| Statistic  |          Stata |         Python |     Difference | Std Difference |
|------------|----------------|----------------|----------------|----------------|
| count      |       3.07e+06 |       3.07e+06 |       3.07e+06 |       3.07e+06 |
| mean       |         3.3803 |         3.3803 |      -1.95e-06 |      -3.44e-08 |
| std        |        56.6989 |        56.6989 |       9.85e-04 |       1.74e-05 |
| min        |         0.0000 |         0.0000 |        -0.4978 |        -0.0088 |
| 25%        |         1.2859 |         1.2859 |      -5.02e-08 |      -8.85e-10 |
| 50%        |         2.0125 |         2.0125 |         0.0000 |         0.0000 |
| 75%        |         3.1813 |         3.1813 |       5.05e-08 |       8.91e-10 |
| max        |     25204.0000 |     25204.0000 |       1.67e-04 |       2.94e-06 |

**Regression Analysis** (Python ~ Stata):

- **Model**: python = -0.0000 + 1.0000 * stata
- **R-squared**: 1.0000
- **N observations**: 3,065,278

| Coefficient |     Estimate |    Std Error | t-statistic |   p-value |
|-------------|--------------|--------------|-------------|----------|
| Intercept   |    -1.95e-06 |     5.64e-07 |     -3.4584 |     0.001 |
| Slope       |       1.0000 |     9.92e-09 |    1.01e+08 |     0.000 |

**Feedback**:
- Num observations with std_diff >= TOL_DIFF_1: 0/3065278 (0.000%)
- Stata standard deviation: 5.67e+01

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

### nanalyst

**Status**: ❌ FAILED

**Test Results**:
- Test 1 - Column names: ✅ PASSED
- Test 2 - Superset check: ❌ FAILED (Python missing 716 Stata observations)
- Test 3 - Precision1 check: ✅ PASSED
- Test 4 - Precision2 check: ✅ PASSED

**Columns**: ['nanalyst']

**Observations**:
- Stata:  2,700,302
- Python: 2,699,967
- Common: 2,699,586

**Precision1**: 0.259% obs with std_diff >= 1.00e-02 (tolerance: < 10%)

**Precision2**: 99th percentile diff = 0.00e+00 (tolerance: < 1.00e+00)

**Summary Statistics** (Common Observations):

| Statistic  |          Stata |         Python |     Difference | Std Difference |
|------------|----------------|----------------|----------------|----------------|
| count      |       2.70e+06 |       2.70e+06 |       2.70e+06 |       2.70e+06 |
| mean       |         5.1507 |         5.1529 |         0.0022 |       3.29e-04 |
| std        |         6.7165 |         6.7171 |         0.5838 |         0.0869 |
| min        |         0.0000 |         0.0000 |       -29.0000 |        -4.3177 |
| 25%        |         0.0000 |         0.0000 |         0.0000 |         0.0000 |
| 50%        |         3.0000 |         3.0000 |         0.0000 |         0.0000 |
| 75%        |         7.0000 |         7.0000 |         0.0000 |         0.0000 |
| max        |        62.0000 |        62.0000 |        35.0000 |         5.2111 |

**Regression Analysis** (Python ~ Stata):

- **Model**: python = 0.0212 + 0.9963 * stata
- **R-squared**: 0.9925
- **N observations**: 2,699,586

| Coefficient |     Estimate |    Std Error | t-statistic |   p-value |
|-------------|--------------|--------------|-------------|----------|
| Intercept   |       0.0212 |     4.47e-04 |     47.3288 |     0.000 |
| Slope       |       0.9963 |     5.29e-05 |  18848.5715 |     0.000 |

**Missing Observations Sample**:
```
 index  permno  yyyymm  nanalyst
     0   19289  197807         1
     1   19289  197808         1
     2   19289  197809         1
     3   19289  197810         1
     4   19289  197811         1
     5   19289  197812         1
     6   19289  197901         1
     7   19289  197902         1
     8   19289  197903         1
     9   19289  197904         1
```

**Feedback**:
- Num observations with std_diff >= TOL_DIFF_1: 6994/2699586 (0.259%)
- Stata standard deviation: 6.72e+00

---

### pchcurrat

**Status**: ❌ FAILED

**Test Results**:
- Test 1 - Column names: ✅ PASSED
- Test 2 - Superset check: ✅ PASSED
- Test 3 - Precision1 check: ❌ FAILED
- Test 4 - Precision2 check: ❌ FAILED

**Columns**: ['pchcurrat']

**Observations**:
- Stata:  3,624,363
- Python: 3,625,095
- Common: 3,624,363

**Precision1**: 15.542% obs with std_diff >= 1.00e-02 (tolerance: < 10%)

**Precision2**: 99th percentile diff = nan (tolerance: < 1.00e+00)

**Summary Statistics** (Common Observations):

| Statistic  |          Stata |         Python |     Difference | Std Difference |
|------------|----------------|----------------|----------------|----------------|
| count      |       3.62e+06 |       3.07e+06 |       3.07e+06 |       3.07e+06 |
| mean       |         0.1878 |            inf |            inf |            inf |
| std        |        20.4050 |            N/A |            N/A |            N/A |
| min        |        -1.0000 |        -1.0000 |        -1.0000 |        -0.0490 |
| 25%        |        -0.1194 |        -0.1581 |      -2.87e-08 |      -1.41e-09 |
| 50%        |         0.0000 |         0.0000 |         0.0000 |         0.0000 |
| 75%        |         0.0786 |         0.1213 |       2.87e-08 |       1.41e-09 |
| max        |      8289.6123 |            inf |            inf |            inf |

**Regression Analysis** (Python ~ Stata):

- **Model**: python = inf + -inf * stata
- **R-squared**: nan
- **N observations**: 3,072,640

| Coefficient |     Estimate |    Std Error | t-statistic |   p-value |
|-------------|--------------|--------------|-------------|----------|
| Intercept   |          nan |          nan |         nan |       nan |
| Slope       |          nan |          nan |         nan |       nan |

**Feedback**:
- Num observations with std_diff >= TOL_DIFF_1: 563297/3624363 (15.542%)
- Stata standard deviation: 2.04e+01

**Most Recent Bad Observations**:
```
   permno  yyyymm  python  stata  diff
0   12385  202608     NaN    0.0   NaN
1   15623  202608     NaN    0.0   NaN
2   16632  202608     NaN    0.0   NaN
3   19655  202608     NaN    0.0   NaN
4   21259  202608     NaN    0.0   NaN
5   77114  202608     NaN    0.0   NaN
6   81073  202608     NaN    0.0   NaN
7   86349  202608     NaN    0.0   NaN
8   89056  202608     NaN    0.0   NaN
9   89256  202608     NaN    0.0   NaN
```

**Largest Differences**:
```
   permno  yyyymm  python  stata  diff
0   10002  199506     NaN    0.0   NaN
1   10002  199507     NaN    0.0   NaN
2   10002  199508     NaN    0.0   NaN
3   10002  199509     NaN    0.0   NaN
4   10002  199510     NaN    0.0   NaN
5   10002  199511     NaN    0.0   NaN
6   10002  199512     NaN    0.0   NaN
7   10002  199601     NaN    0.0   NaN
8   10002  199602     NaN    0.0   NaN
9   10002  199603     NaN    0.0   NaN
```

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

### pchgm_pchsale

**Status**: ✅ PASSED

**Test Results**:
- Test 1 - Column names: ✅ PASSED
- Test 2 - Superset check: ✅ PASSED
- Test 3 - Precision1 check: ✅ PASSED
- Test 4 - Precision2 check: ✅ PASSED

**Columns**: ['pchgm_pchsale']

**Observations**:
- Stata:  3,222,544
- Python: 3,294,865
- Common: 3,222,544

**Precision1**: 0.001% obs with std_diff >= 1.00e-02 (tolerance: < 10%)

**Precision2**: 99th percentile diff = 2.59e-09 (tolerance: < 1.00e+00)

**Summary Statistics** (Common Observations):

| Statistic  |          Stata |         Python |     Difference | Std Difference |
|------------|----------------|----------------|----------------|----------------|
| count      |       3.22e+06 |       3.22e+06 |       3.22e+06 |       3.22e+06 |
| mean       |        -0.7243 |        -0.7243 |       9.70e-06 |       1.23e-07 |
| std        |        78.7275 |        78.7275 |         0.0038 |       4.82e-05 |
| min        |    -27624.8850 |    -27624.8841 |        -0.4564 |        -0.0058 |
| 25%        |        -0.0812 |        -0.0812 |      -1.27e-09 |      -1.62e-11 |
| 50%        |        -0.0029 |        -0.0029 |         0.0000 |         0.0000 |
| 75%        |         0.0636 |         0.0636 |       1.29e-09 |       1.63e-11 |
| max        |      5139.5205 |      5139.5206 |         1.4141 |         0.0180 |

**Regression Analysis** (Python ~ Stata):

- **Model**: python = 0.0000 + 1.0000 * stata
- **R-squared**: 1.0000
- **N observations**: 3,222,544

| Coefficient |     Estimate |    Std Error | t-statistic |   p-value |
|-------------|--------------|--------------|-------------|----------|
| Intercept   |     9.69e-06 |     2.12e-06 |      4.5821 |     0.000 |
| Slope       |       1.0000 |     2.69e-08 |    3.72e+07 |     0.000 |

**Feedback**:
- Num observations with std_diff >= TOL_DIFF_1: 24/3222544 (0.001%)
- Stata standard deviation: 7.87e+01

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

### pchsaleinv

**Status**: ✅ PASSED

**Test Results**:
- Test 1 - Column names: ✅ PASSED
- Test 2 - Superset check: ✅ PASSED
- Test 3 - Precision1 check: ✅ PASSED
- Test 4 - Precision2 check: ✅ PASSED

**Columns**: ['pchsaleinv']

**Observations**:
- Stata:  2,465,425
- Python: 3,303,855
- Common: 2,465,425

**Precision1**: 0.000% obs with std_diff >= 1.00e-02 (tolerance: < 10%)

**Precision2**: 99th percentile diff = 1.66e-09 (tolerance: < 1.00e+00)

**Summary Statistics** (Common Observations):

| Statistic  |          Stata |         Python |     Difference | Std Difference |
|------------|----------------|----------------|----------------|----------------|
| count      |       2.47e+06 |       2.47e+06 |       2.47e+06 |       2.47e+06 |
| mean       |         0.7658 |         0.7658 |       9.89e-08 |       1.35e-09 |
| std        |        73.4020 |        73.4020 |       4.81e-05 |       6.55e-07 |
| min        |     -3126.2041 |     -3126.2041 |      -6.97e-04 |      -9.50e-06 |
| 25%        |        -0.1224 |        -0.1224 |      -2.63e-09 |      -3.59e-11 |
| 50%        |         0.0114 |         0.0114 |       1.70e-12 |       2.31e-14 |
| 75%        |         0.1759 |         0.1759 |       2.67e-09 |       3.63e-11 |
| max        |     28764.0310 |     28764.0303 |         0.0218 |       2.97e-04 |

**Regression Analysis** (Python ~ Stata):

- **Model**: python = 0.0000 + 1.0000 * stata
- **R-squared**: 1.0000
- **N observations**: 2,465,425

| Coefficient |     Estimate |    Std Error | t-statistic |   p-value |
|-------------|--------------|--------------|-------------|----------|
| Intercept   |     1.17e-07 |     3.06e-08 |      3.8251 |     0.000 |
| Slope       |       1.0000 |     4.17e-10 |    2.40e+09 |     0.000 |

**Feedback**:
- Num observations with std_diff >= TOL_DIFF_1: 0/2465425 (0.000%)
- Stata standard deviation: 7.34e+01

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

### roavol

**Status**: ❌ FAILED

**Test Results**:
- Test 1 - Column names: ✅ PASSED
- Test 2 - Superset check: ❌ FAILED (Python missing 9 Stata observations)
- Test 3 - Precision1 check: ✅ PASSED
- Test 4 - Precision2 check: ✅ PASSED

**Columns**: ['roavol']

**Observations**:
- Stata:  2,039,901
- Python: 2,058,816
- Common: 2,039,892

**Precision1**: 4.523% obs with std_diff >= 1.00e-02 (tolerance: < 10%)

**Precision2**: 99th percentile diff = 7.54e-02 (tolerance: < 1.00e+00)

**Summary Statistics** (Common Observations):

| Statistic  |          Stata |         Python |     Difference | Std Difference |
|------------|----------------|----------------|----------------|----------------|
| count      |       2.04e+06 |       2.04e+06 |       2.04e+06 |       2.04e+06 |
| mean       |         0.0305 |         0.0314 |       9.42e-04 |         0.0062 |
| std        |         0.1527 |         0.1699 |         0.0757 |         0.4955 |
| min        |       3.49e-05 |       3.49e-05 |        -0.7907 |        -5.1792 |
| 25%        |         0.0056 |         0.0056 |      -1.96e-10 |      -1.28e-09 |
| 50%        |         0.0124 |         0.0125 |      -5.37e-12 |      -3.52e-11 |
| 75%        |         0.0295 |         0.0298 |       1.36e-10 |       8.91e-10 |
| max        |        49.8304 |        49.8304 |        21.5355 |       141.0592 |

**Regression Analysis** (Python ~ Stata):

- **Model**: python = 0.0011 + 0.9963 * stata
- **R-squared**: 0.8016
- **N observations**: 2,039,772

| Coefficient |     Estimate |    Std Error | t-statistic |   p-value |
|-------------|--------------|--------------|-------------|----------|
| Intercept   |       0.0011 |     5.40e-05 |     19.5295 |     0.000 |
| Slope       |       0.9963 |     3.47e-04 |   2870.9738 |     0.000 |

**Missing Observations Sample**:
```
 index  permno  yyyymm   roavol
     0   16965  202011 0.020348
     1   16965  202012 0.019920
     2   16965  202101 0.019519
     3   44580  197607 0.008090
     4   48013  197702 0.003290
     5   50518  197609 0.009734
     6   52572  197710 0.039755
     7   52572  197711 0.039759
     8   52572  197712 0.039723
```

**Feedback**:
- Num observations with std_diff >= TOL_DIFF_1: 92257/2039892 (4.523%)
- Stata standard deviation: 1.53e-01

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

### BetaBDLeverage

**Status**: ❌ MISSING PYTHON CSV

**Error**: Python CSV file not found: ../pyData/Placebos/BetaBDLeverage.csv

---

### BetaDimson

**Status**: ❌ MISSING PYTHON CSV

**Error**: Python CSV file not found: ../pyData/Placebos/BetaDimson.csv

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

### IntrinsicValue

**Status**: ❌ MISSING PYTHON CSV

**Error**: Python CSV file not found: ../pyData/Placebos/IntrinsicValue.csv

---

### OrgCapNoAdj

**Status**: ❌ MISSING PYTHON CSV

**Error**: Python CSV file not found: ../pyData/Placebos/OrgCapNoAdj.csv

---

### ResidualMomentum6m

**Status**: ❌ MISSING PYTHON CSV

**Error**: Python CSV file not found: ../pyData/Placebos/ResidualMomentum6m.csv

---

### grcapx1y

**Status**: ❌ MISSING PYTHON CSV

**Error**: Python CSV file not found: ../pyData/Placebos/grcapx1y.csv

---

