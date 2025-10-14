# Placebo Validation Results

**Generated**: 2025-10-14 16:20:11

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
| EarningsSmoothness        | ✅         | ✅       | ❌ (100.00%) | ❌ (0.00%)    | ❌ (99th diff 0.0E+00)   |
| AccrualQuality            | ✅         | ✅       | ❌ (8.51%)   | ❌ (90.95%)   | ❌ (99th diff 1.7E+00)   |
| betaCR                    | ✅         | ✅       | ❌ (8.34%)   | ❌ (65.92%)   | ❌ (99th diff 3.6E+00)   |
| betaCC                    | ✅         | ✅       | ❌ (8.34%)   | ❌ (77.09%)   | ❌ (99th diff 1.3E+01)   |
| AccrualQualityJune        | ✅         | ✅       | ❌ (8.22%)   | ❌ (89.82%)   | ❌ (99th diff 1.8E+00)   |
| betaNet                   | ✅         | ✅       | ❌ (7.32%)   | ❌ (78.49%)   | ❌ (99th diff 8.1E+00)   |
| EarningsConservatism      | ✅         | ✅       | ❌ (2.52%)   | ✅ (3.56%)    | ✅ (99th diff 6.4E-02)   |
| EarningsTimeliness        | ✅         | ✅       | ❌ (2.52%)   | ✅ (0.00%)    | ✅ (99th diff 4.8E-07)   |
| OrgCapNoAdj               | ✅         | ✅       | ❌ (2.05%)   | ✅ (0.02%)    | ✅ (99th diff 3.0E-05)   |
| AbnormalAccrualsPercent   | ✅         | ✅       | ❌ (1.39%)   | ✅ (1.13%)    | ✅ (99th diff 1.1E-02)   |
| DelayAcct                 | ✅         | ✅       | ❌ (1.34%)   | ❌ (89.49%)   | ✅ (99th diff 6.2E-01)   |
| DelayNonAcct              | ✅         | ✅       | ❌ (1.34%)   | ❌ (78.22%)   | ✅ (99th diff 2.9E-01)   |
| grcapx1y                  | ✅         | ✅       | ❌ (1.09%)   | ✅ (0.01%)    | ✅ (99th diff 1.8E-09)   |
| pchcurrat                 | ✅         | ✅       | ❌ (0.99%)   | ✅ (0.05%)    | ✅ (99th diff 9.7E-09)   |
| ForecastDispersionLT      | ✅         | ✅       | ❌ (0.92%)   | ✅ (0.08%)    | ✅ (99th diff 1.5E-07)   |
| IdioVolCAPM               | ✅         | ✅       | ❌ (0.77%)   | ✅ (0.00%)    | ✅ (99th diff 1.0E-03)   |
| IdioVolQF                 | ✅         | ✅       | ❌ (0.77%)   | ✅ (0.00%)    | ✅ (99th diff 3.4E-08)   |
| ReturnSkewQF              | ✅         | ✅       | ❌ (0.77%)   | ✅ (0.89%)    | ✅ (99th diff 3.2E-07)   |
| ReturnSkewCAPM            | ✅         | ✅       | ❌ (0.75%)   | ✅ (0.81%)    | ✅ (99th diff 9.0E-03)   |
| IntrinsicValue            | ✅         | ✅       | ❌ (0.71%)   | ✅ (2.12%)    | ✅ (99th diff 6.3E-02)   |
| OScore_q                  | ✅         | ✅       | ❌ (0.66%)   | ✅ (0.00%)    | ✅ (99th diff 0.0E+00)   |
| fgr5yrNoLag               | ✅         | ✅       | ❌ (0.49%)   | ✅ (0.08%)    | ✅ (99th diff 1.4E-07)   |
| ZScore                    | ✅         | ✅       | ❌ (0.08%)   | ✅ (0.00%)    | ✅ (99th diff 5.6E-08)   |
| KZ_q                      | ✅         | ✅       | ❌ (0.01%)   | ✅ (0.00%)    | ✅ (99th diff 3.4E-09)   |
| PS_q                      | ✅         | ✅       | ❌ (0.01%)   | ❌ (53.37%)   | ❌ (99th diff 3.2E+00)   |
| OperProfRDLagAT_q         | ✅         | ✅       | ❌ (0.01%)   | ✅ (0.05%)    | ✅ (99th diff 6.8E-08)   |
| EntMult_q                 | ✅         | ✅       | ❌ (0.01%)   | ✅ (0.01%)    | ✅ (99th diff 6.4E-09)   |
| NetDebtPrice_q            | ✅         | ✅       | ❌ (0.01%)   | ✅ (0.00%)    | ✅ (99th diff 6.4E-08)   |
| BrandCapital              | ✅         | ✅       | ❌ (0.00%)   | ✅ (5.88%)    | ✅ (99th diff 8.2E-02)   |
| Tax_q                     | ✅         | ✅       | ❌ (0.00%)   | ✅ (0.01%)    | ✅ (99th diff 8.7E-09)   |
| WW_Q                      | ✅         | ✅       | ❌ (0.00%)   | ✅ (0.00%)    | ✅ (99th diff 1.9E-06)   |
| OPLeverage_q              | ✅         | ✅       | ❌ (0.00%)   | ✅ (0.03%)    | ✅ (99th diff 8.1E-08)   |
| EBM_q                     | ✅         | ✅       | ❌ (0.00%)   | ✅ (0.00%)    | ✅ (99th diff 4.9E-08)   |
| Leverage_q                | ✅         | ✅       | ❌ (0.00%)   | ✅ (0.00%)    | ✅ (99th diff 5.7E-08)   |
| EPq                       | ✅         | ✅       | ❌ (0.00%)   | ✅ (0.01%)    | ✅ (99th diff 6.2E-08)   |
| AssetGrowth_q             | ✅         | ✅       | ❌ (0.00%)   | ✅ (0.00%)    | ✅ (99th diff 1.9E-08)   |
| CapTurnover_q             | ✅         | ✅       | ❌ (0.00%)   | ✅ (0.01%)    | ✅ (99th diff 1.0E-08)   |
| AssetLiquidityMarketQuart | ✅         | ✅       | ❌ (0.00%)   | ✅ (0.01%)    | ✅ (99th diff 1.5E-07)   |
| AssetTurnover_q           | ✅         | ✅       | ❌ (0.00%)   | ✅ (0.00%)    | ✅ (99th diff 5.7E-09)   |
| AssetLiquidityBookQuart   | ✅         | ✅       | ❌ (0.00%)   | ✅ (0.00%)    | ✅ (99th diff 2.4E-08)   |
| sgr_q                     | ✅         | ✅       | ❌ (0.00%)   | ✅ (0.00%)    | ✅ (99th diff 3.1E-10)   |
| SP_q                      | ✅         | ✅       | ❌ (0.00%)   | ✅ (0.02%)    | ✅ (99th diff 1.1E-07)   |
| DivYield                  | ✅         | ✅       | ❌ (0.00%)   | ✅ (0.01%)    | ✅ (99th diff 1.2E-08)   |
| tang_q                    | ✅         | ✅       | ❌ (0.00%)   | ✅ (0.01%)    | ✅ (99th diff 1.6E-07)   |
| DownsideBeta              | ✅         | ✅       | ❌ (0.00%)   | ❌ (19.35%)   | ✅ (99th diff 1.7E-01)   |
| CBOperProfLagAT_q         | ✅         | ✅       | ❌ (0.00%)   | ❌ (26.69%)   | ❌ (99th diff 2.5E+00)   |
| FailureProbability        | ✅         | ✅       | ❌ (0.00%)   | ✅ (0.11%)    | ✅ (99th diff 6.1E-08)   |
| roavol                    | ✅         | ✅       | ❌ (0.00%)   | ✅ (2.95%)    | ✅ (99th diff 3.5E-02)   |
| FailureProbabilityJune    | ✅         | ✅       | ❌ (0.00%)   | ✅ (0.21%)    | ✅ (99th diff 1.7E-07)   |
| GPlag_q                   | ✅         | ✅       | ❌ (0.00%)   | ✅ (0.04%)    | ✅ (99th diff 1.8E-08)   |
| cfpq                      | ✅         | ✅       | ❌ (0.00%)   | ❌ (11.98%)   | ✅ (99th diff 8.8E-01)   |
| ChangeRoA                 | ✅         | ✅       | ❌ (0.00%)   | ✅ (0.03%)    | ✅ (99th diff 6.7E-08)   |
| ChangeRoE                 | ✅         | ✅       | ❌ (0.00%)   | ✅ (0.00%)    | ✅ (99th diff 3.3E-09)   |
| OperProfLag_q             | ✅         | ✅       | ❌ (0.00%)   | ✅ (0.00%)    | ✅ (99th diff 1.1E-05)   |
| PM_q                      | ✅         | ✅       | ❌ (0.00%)   | ✅ (0.00%)    | ✅ (99th diff 3.1E-09)   |
| NetPayoutYield_q          | ✅         | ✅       | ❌ (0.00%)   | ✅ (0.04%)    | ✅ (99th diff 4.9E-08)   |
| BMq                       | ✅         | ✅       | ❌ (0.00%)   | ✅ (0.00%)    | ✅ (99th diff 1.3E-07)   |
| BookLeverageQuarterly     | ✅         | ✅       | ❌ (0.00%)   | ✅ (0.00%)    | ✅ (99th diff 4.1E-13)   |
| AMq                       | ✅         | ✅       | ❌ (0.00%)   | ✅ (0.00%)    | ✅ (99th diff 5.1E-08)   |
| betaRC                    | ✅         | ✅       | ✅ (0.00%)   | ❌ (98.79%)   | ❌ (99th diff 3.5E+00)   |
| betaRR                    | ✅         | ✅       | ✅ (0.00%)   | ❌ (98.48%)   | ❌ (99th diff 2.9E+00)   |
| OperProfRDLagAT           | ✅         | ✅       | ✅ (0.00%)   | ✅ (4.55%)    | ✅ (99th diff 8.2E-02)   |
| BetaDimson                | ✅         | ✅       | ✅ (0.00%)   | ✅ (2.94%)    | ✅ (99th diff 1.9E-02)   |
| BetaBDLeverage            | ✅         | ✅       | ✅ (0.00%)   | ✅ (2.21%)    | ✅ (99th diff 2.3E-01)   |
| nanalyst                  | ✅         | ✅       | ✅ (0.00%)   | ✅ (1.25%)    | ✅ (99th diff 3.0E-01)   |
| ResidualMomentum6m        | ✅         | ✅       | ✅ (0.00%)   | ✅ (0.93%)    | ✅ (99th diff 9.6E-03)   |
| PayoutYield_q             | ✅         | ✅       | ✅ (0.00%)   | ✅ (0.06%)    | ✅ (99th diff 4.4E-08)   |
| EarningsPredictability    | ✅         | ✅       | ✅ (0.00%)   | ✅ (0.06%)    | ✅ (99th diff 7.4E-10)   |
| DivYieldAnn               | ✅         | ✅       | ✅ (0.00%)   | ✅ (0.05%)    | ✅ (99th diff 2.1E-08)   |
| ETR                       | ✅         | ✅       | ✅ (0.00%)   | ✅ (0.03%)    | ✅ (99th diff 1.2E-11)   |
| RD_q                      | ✅         | ✅       | ✅ (0.00%)   | ✅ (0.02%)    | ✅ (99th diff 6.8E-08)   |
| GPlag                     | ✅         | ✅       | ✅ (0.00%)   | ✅ (0.02%)    | ✅ (99th diff 5.7E-08)   |
| CFq                       | ✅         | ✅       | ✅ (0.00%)   | ✅ (0.02%)    | ✅ (99th diff 2.1E-08)   |
| roic                      | ✅         | ✅       | ✅ (0.00%)   | ✅ (0.01%)    | ✅ (99th diff 3.6E-23)   |
| GrSaleToGrReceivables     | ✅         | ✅       | ✅ (0.00%)   | ✅ (0.01%)    | ✅ (99th diff 8.3E-10)   |
| secured                   | ✅         | ✅       | ✅ (0.00%)   | ✅ (0.01%)    | ✅ (99th diff 8.4E-08)   |
| CBOperProfLagAT           | ✅         | ✅       | ✅ (0.00%)   | ✅ (0.01%)    | ✅ (99th diff 6.6E-08)   |
| DelSTI                    | ✅         | ✅       | ✅ (0.00%)   | ✅ (0.01%)    | ✅ (99th diff 2.0E-07)   |
| salerec                   | ✅         | ✅       | ✅ (0.00%)   | ✅ (0.01%)    | ✅ (99th diff 2.1E-08)   |
| ChNCOA                    | ✅         | ✅       | ✅ (0.00%)   | ✅ (0.01%)    | ✅ (99th diff 8.5E-08)   |
| EarningsPersistence       | ✅         | ✅       | ✅ (0.00%)   | ✅ (0.01%)    | ✅ (99th diff 2.1E-07)   |
| AssetLiquidityMarket      | ✅         | ✅       | ✅ (0.00%)   | ✅ (0.01%)    | ✅ (99th diff 1.7E-07)   |
| securedind                | ✅         | ✅       | ✅ (0.00%)   | ✅ (0.01%)    | ✅ (99th diff 0.0E+00)   |
| ChNCOL                    | ✅         | ✅       | ✅ (0.00%)   | ✅ (0.01%)    | ✅ (99th diff 5.8E-08)   |
| ZScore_q                  | ✅         | ✅       | ✅ (0.00%)   | ✅ (0.01%)    | ✅ (99th diff 5.0E-08)   |
| pchdepr                   | ✅         | ✅       | ✅ (0.00%)   | ✅ (0.00%)    | ✅ (99th diff 2.3E-09)   |
| OperProfLag               | ✅         | ✅       | ✅ (0.00%)   | ✅ (0.00%)    | ✅ (99th diff 1.5E-08)   |
| pchgm_pchsale             | ✅         | ✅       | ✅ (0.00%)   | ✅ (0.00%)    | ✅ (99th diff 2.8E-09)   |
| AssetLiquidityBook        | ✅         | ✅       | ✅ (0.00%)   | ✅ (0.00%)    | ✅ (99th diff 8.5E-08)   |
| depr                      | ✅         | ✅       | ✅ (0.00%)   | ✅ (0.00%)    | ✅ (99th diff 8.8E-09)   |
| GrGMToGrSales             | ✅         | ✅       | ✅ (0.00%)   | ✅ (0.00%)    | ✅ (99th diff 2.3E-09)   |
| LaborforceEfficiency      | ✅         | ✅       | ✅ (0.00%)   | ✅ (0.00%)    | ✅ (99th diff 4.3E-09)   |
| RetNOA_q                  | ✅         | ✅       | ✅ (0.00%)   | ✅ (0.00%)    | ✅ (99th diff 4.3E-11)   |
| sgr                       | ✅         | ✅       | ✅ (0.00%)   | ✅ (0.00%)    | ✅ (99th diff 1.9E-09)   |
| AssetTurnover             | ✅         | ✅       | ✅ (0.00%)   | ✅ (0.00%)    | ✅ (99th diff 4.0E-09)   |
| CapTurnover               | ✅         | ✅       | ✅ (0.00%)   | ✅ (0.00%)    | ✅ (99th diff 8.5E-08)   |
| WW                        | ✅         | ✅       | ✅ (0.00%)   | ✅ (0.00%)    | ✅ (99th diff 5.2E-10)   |
| EarningsValueRelevance    | ✅         | ✅       | ✅ (0.00%)   | ✅ (0.00%)    | ✅ (99th diff 4.4E-07)   |
| BetaSquared               | ✅         | ✅       | ✅ (0.00%)   | ✅ (0.00%)    | ✅ (99th diff 1.2E-04)   |
| saleinv                   | ✅         | ✅       | ✅ (0.00%)   | ✅ (0.00%)    | ✅ (99th diff 3.1E-09)   |
| RetNOA                    | ✅         | ✅       | ✅ (0.00%)   | ✅ (0.00%)    | ✅ (99th diff 1.5E-19)   |
| ChPM                      | ✅         | ✅       | ✅ (0.00%)   | ✅ (0.00%)    | ✅ (99th diff 5.3E-09)   |
| rd_sale_q                 | ✅         | ✅       | ✅ (0.00%)   | ✅ (0.00%)    | ✅ (99th diff 6.7E-09)   |
| pchsaleinv                | ✅         | ✅       | ✅ (0.00%)   | ✅ (0.00%)    | ✅ (99th diff 1.7E-09)   |
| PM                        | ✅         | ✅       | ✅ (0.00%)   | ✅ (0.00%)    | ✅ (99th diff 2.4E-09)   |
| salecash                  | ✅         | ✅       | ✅ (0.00%)   | ✅ (0.00%)    | ✅ (99th diff 6.6E-09)   |
| FRbook                    | ✅         | ✅       | ✅ (0.00%)   | ✅ (0.00%)    | ✅ (99th diff 2.1E-07)   |
| BidAskTAQ                 | ✅         | ✅       | ✅ (0.00%)   | ✅ (0.00%)    | ✅ (99th diff 1.6E-07)   |
| currat                    | ✅         | ✅       | ✅ (0.00%)   | ✅ (0.00%)    | ✅ (99th diff 1.4E-08)   |
| quick                     | ✅         | ✅       | ✅ (0.00%)   | ✅ (0.00%)    | ✅ (99th diff 1.1E-08)   |
| rd_sale                   | ✅         | ✅       | ✅ (0.00%)   | ✅ (0.00%)    | ✅ (99th diff 4.1E-09)   |
| cashdebt                  | ✅         | ✅       | ✅ (0.00%)   | ✅ (0.00%)    | ✅ (99th diff 3.2E-09)   |
| KZ                        | ✅         | ✅       | ✅ (0.00%)   | ✅ (0.00%)    | ✅ (99th diff 2.1E-09)   |
| pchquick                  | ✅         | ✅       | ✅ (0.00%)   | ✅ (0.00%)    | ✅ (99th diff 2.0E-09)   |

**Overall**: 53/114 available placebos passed validation
**Python CSVs**: 114/114 placebos have Python implementation

## Detailed Results

### AMq

**Status**: ❌ FAILED

**Test Results**:
- Test 1 - Column names: ✅ PASSED
- Test 2 - Superset check: ❌ FAILED (Python missing 1 Stata observations)
- Test 3 - Precision1 check: ✅ PASSED
- Test 4 - Precision2 check: ✅ PASSED

**Columns**: ['AMq']

**Observations**:
- Stata:  2,584,378
- Python: 2,809,481
- Common: 2,584,377

**Precision1**: 0.001% obs with std_diff >= 1.00e-02 (tolerance: < 10%)

**Precision2**: 99th percentile diff = 5.15e-08 (tolerance: < 1.00e+00)

**Summary Statistics** (Common Observations):

| Statistic  |          Stata |         Python |     Difference | Std Difference |
|------------|----------------|----------------|----------------|----------------|
| count      |       2.58e+06 |       2.58e+06 |       2.58e+06 |       2.58e+06 |
| mean       |         3.7379 |         3.7379 |       2.79e-08 |       1.20e-09 |
| std        |        23.2695 |        23.2695 |         0.0018 |       7.59e-05 |
| min        |       -33.6391 |       -33.6391 |        -0.7715 |        -0.0332 |
| 25%        |         0.6615 |         0.6615 |      -3.34e-08 |      -1.44e-09 |
| 50%        |         1.4017 |         1.4017 |         0.0000 |         0.0000 |
| 75%        |         3.2088 |         3.2088 |       3.35e-08 |       1.44e-09 |
| max        |     11549.4230 |     11549.4231 |         1.3032 |         0.0560 |

**Regression Analysis** (Python ~ Stata):

- **Model**: python = 0.0000 + 1.0000 * stata
- **R-squared**: 1.0000
- **N observations**: 2,584,377

| Coefficient |     Estimate |    Std Error | t-statistic |   p-value |
|-------------|--------------|--------------|-------------|----------|
| Intercept   |     9.99e-08 |     1.11e-06 |      0.0898 |     0.928 |
| Slope       |       1.0000 |     4.72e-08 |    2.12e+07 |     0.000 |

**Missing Observations Sample**:
```
 index  permno  yyyymm      AMq
     0   19316  202412 3.937687
```

**Feedback**:
- Num observations with std_diff >= TOL_DIFF_1: 16/2584377 (0.001%)
- Stata standard deviation: 2.33e+01

---

### AbnormalAccrualsPercent

**Status**: ❌ FAILED

**Test Results**:
- Test 1 - Column names: ✅ PASSED
- Test 2 - Superset check: ❌ FAILED (Python missing 35314 Stata observations)
- Test 3 - Precision1 check: ✅ PASSED
- Test 4 - Precision2 check: ✅ PASSED

**Columns**: ['AbnormalAccrualsPercent']

**Observations**:
- Stata:  2,535,621
- Python: 2,629,956
- Common: 2,500,307

**Precision1**: 1.131% obs with std_diff >= 1.00e-02 (tolerance: < 10%)

**Precision2**: 99th percentile diff = 1.13e-02 (tolerance: < 1.00e+00)

**Summary Statistics** (Common Observations):

| Statistic  |          Stata |         Python |     Difference | Std Difference |
|------------|----------------|----------------|----------------|----------------|
| count      |       2.50e+06 |       2.50e+06 |       2.50e+06 |       2.50e+06 |
| mean       |         1.0533 |         1.0446 |        -0.0088 |      -1.06e-04 |
| std        |        82.5142 |        82.3364 |         3.0917 |         0.0375 |
| min        |     -5995.7578 |     -5995.7576 |      -879.1455 |       -10.6545 |
| 25%        |        -0.4816 |        -0.4808 |      -4.53e-07 |      -5.49e-09 |
| 50%        |         0.0802 |         0.0807 |      -4.27e-09 |      -5.17e-11 |
| 75%        |         0.7854 |         0.7846 |       1.34e-07 |       1.63e-09 |
| max        |     22304.4650 |     22304.4471 |       369.1171 |         4.4734 |

**Regression Analysis** (Python ~ Stata):

- **Model**: python = -0.0057 + 0.9971 * stata
- **R-squared**: 0.9986
- **N observations**: 2,500,307

| Coefficient |     Estimate |    Std Error | t-statistic |   p-value |
|-------------|--------------|--------------|-------------|----------|
| Intercept   |      -0.0057 |       0.0019 |     -2.9461 |     0.003 |
| Slope       |       0.9971 |     2.36e-05 |  42203.8582 |     0.000 |

**Missing Observations Sample**:
```
 index  permno  yyyymm  AbnormalAccrualsPercent
     0   10006  197206                 1.094513
     1   10006  197207                 1.094513
     2   10006  197208                 1.094513
     3   10006  197209                 1.094513
     4   10006  197210                 1.094513
     5   10006  197211                 1.094513
     6   10006  197212                 1.094513
     7   10006  197301                 1.094513
     8   10006  197302                 1.094513
     9   10006  197303                 1.094513
```

**Feedback**:
- Num observations with std_diff >= TOL_DIFF_1: 28273/2500307 (1.131%)
- Stata standard deviation: 8.25e+01

---

### AccrualQuality

**Status**: ❌ FAILED

**Test Results**:
- Test 1 - Column names: ✅ PASSED
- Test 2 - Superset check: ❌ FAILED (Python missing 148124 Stata observations)
- Test 3 - Precision1 check: ❌ FAILED
- Test 4 - Precision2 check: ❌ FAILED

**Columns**: ['AccrualQuality']

**Observations**:
- Stata:  1,740,065
- Python: 1,790,065
- Common: 1,591,941

**Precision1**: 90.947% obs with std_diff >= 1.00e-02 (tolerance: < 10%)

**Precision2**: 99th percentile diff = 1.68e+00 (tolerance: < 1.00e+00)

**Summary Statistics** (Common Observations):

| Statistic  |          Stata |         Python |     Difference | Std Difference |
|------------|----------------|----------------|----------------|----------------|
| count      |       1.59e+06 |       1.59e+06 |       1.59e+06 |       1.59e+06 |
| mean       |         0.0449 |         0.0453 |       4.91e-04 |         0.0102 |
| std        |         0.0482 |         0.0483 |         0.0208 |         0.4305 |
| min        |       4.17e-04 |       4.58e-04 |        -1.2531 |       -25.9759 |
| 25%        |         0.0175 |         0.0179 |        -0.0044 |        -0.0902 |
| 50%        |         0.0309 |         0.0314 |       4.54e-05 |       9.42e-04 |
| 75%        |         0.0548 |         0.0555 |         0.0049 |         0.1010 |
| max        |         1.6265 |         1.6228 |         1.3339 |        27.6500 |

**Regression Analysis** (Python ~ Stata):

- **Model**: python = 0.0046 + 0.9088 * stata
- **R-squared**: 0.8235
- **N observations**: 1,591,941

| Coefficient |     Estimate |    Std Error | t-statistic |   p-value |
|-------------|--------------|--------------|-------------|----------|
| Intercept   |       0.0046 |     2.20e-05 |    208.5618 |     0.000 |
| Slope       |       0.9088 |     3.33e-04 |   2725.7018 |     0.000 |

**Missing Observations Sample**:
```
 index  permno  yyyymm  AccrualQuality
     0   10001  200712        0.028371
     1   10001  200801        0.028371
     2   10001  200802        0.028371
     3   10001  200803        0.028371
     4   10001  200804        0.028371
     5   10001  200805        0.028371
     6   10001  201706        0.007970
     7   10001  201707        0.007970
     8   10001  201708        0.007970
     9   10001  201709        0.007970
```

**Feedback**:
- Num observations with std_diff >= TOL_DIFF_1: 1447817/1591941 (90.947%)
- Stata standard deviation: 4.82e-02

**Most Recent Bad Observations**:
```
   permno  yyyymm    python     stata      diff
0   10104  202510  0.016547  0.017300 -0.000752
1   16431  202510  0.013722  0.031955 -0.018234
2   17144  202510  0.004580  0.007341 -0.002762
3   23660  202510  0.033724  0.025741  0.007983
4   54114  202510  0.028960  0.028468  0.000493
5   54594  202510  0.022022  0.013264  0.008758
6   55862  202510  0.209078  0.203164  0.005914
7   56274  202510  0.010395  0.013914 -0.003519
8   57665  202510  0.022031  0.026395 -0.004363
9   61621  202510  0.019110  0.021003 -0.001893
```

**Largest Differences**:
```
   permno  yyyymm    python     stata      diff
0   79703  200406  1.405766  0.071864  1.333902
1   79703  200407  1.405766  0.071864  1.333902
2   79703  200408  1.405766  0.071864  1.333902
3   79703  200409  1.405766  0.071864  1.333902
4   79703  200410  1.405766  0.071864  1.333902
5   79703  200411  1.405766  0.071864  1.333902
6   79703  200412  1.405766  0.071864  1.333902
7   79703  200501  1.405766  0.071864  1.333902
8   79703  200502  1.405766  0.071864  1.333902
9   79703  200503  1.405766  0.071864  1.333902
```

---

### AccrualQualityJune

**Status**: ❌ FAILED

**Test Results**:
- Test 1 - Column names: ✅ PASSED
- Test 2 - Superset check: ❌ FAILED (Python missing 146692 Stata observations)
- Test 3 - Precision1 check: ❌ FAILED
- Test 4 - Precision2 check: ❌ FAILED

**Columns**: ['AccrualQualityJune']

**Observations**:
- Stata:  1,784,388
- Python: 1,815,930
- Common: 1,637,696

**Precision1**: 89.823% obs with std_diff >= 1.00e-02 (tolerance: < 10%)

**Precision2**: 99th percentile diff = 1.77e+00 (tolerance: < 1.00e+00)

**Summary Statistics** (Common Observations):

| Statistic  |          Stata |         Python |     Difference | Std Difference |
|------------|----------------|----------------|----------------|----------------|
| count      |       1.64e+06 |       1.64e+06 |       1.64e+06 |       1.64e+06 |
| mean       |         0.0455 |         0.0461 |       6.43e-04 |         0.0130 |
| std        |         0.0495 |         0.0500 |         0.0222 |         0.4487 |
| min        |       4.17e-04 |       4.58e-04 |        -1.2531 |       -25.3016 |
| 25%        |         0.0175 |         0.0179 |        -0.0042 |        -0.0849 |
| 50%        |         0.0311 |         0.0316 |       1.24e-05 |       2.50e-04 |
| 75%        |         0.0555 |         0.0563 |         0.0048 |         0.0959 |
| max        |         1.6265 |         1.6228 |         1.3339 |        26.9323 |

**Regression Analysis** (Python ~ Stata):

- **Model**: python = 0.0048 + 0.9094 * stata
- **R-squared**: 0.8107
- **N observations**: 1,637,696

| Coefficient |     Estimate |    Std Error | t-statistic |   p-value |
|-------------|--------------|--------------|-------------|----------|
| Intercept   |       0.0048 |     2.31e-05 |    206.3658 |     0.000 |
| Slope       |       0.9094 |     3.43e-04 |   2648.2108 |     0.000 |

**Missing Observations Sample**:
```
 index  permno  yyyymm  AccrualQualityJune
     0   10001  200712            0.028488
     1   10001  200801            0.028488
     2   10001  200802            0.028488
     3   10001  200803            0.028488
     4   10001  200804            0.028488
     5   10001  200805            0.028488
     6   10001  201706            0.007970
     7   10001  201707            0.007970
     8   10001  201708            0.007970
     9   10001  201709            0.007970
```

**Feedback**:
- Num observations with std_diff >= TOL_DIFF_1: 1471033/1637696 (89.823%)
- Stata standard deviation: 4.95e-02

**Most Recent Bad Observations**:
```
   permno  yyyymm    python     stata      diff
0   10104  202510  0.016547  0.017300 -0.000752
1   16431  202510  0.013722  0.031955 -0.018234
2   17144  202510  0.004580  0.007341 -0.002762
3   23660  202510  0.033724  0.025741  0.007983
4   54594  202510  0.022022  0.013264  0.008758
5   55862  202510  0.209078  0.203164  0.005914
6   56274  202510  0.010395  0.013914 -0.003519
7   57665  202510  0.022031  0.026395 -0.004363
8   61621  202510  0.019110  0.021003 -0.001893
9   65307  202510  0.033541  0.028258  0.005282
```

**Largest Differences**:
```
   permno  yyyymm    python     stata      diff
0   79703  200406  1.405766  0.071864  1.333902
1   79703  200407  1.405766  0.071864  1.333902
2   79703  200408  1.405766  0.071864  1.333902
3   79703  200409  1.405766  0.071864  1.333902
4   79703  200410  1.405766  0.071864  1.333902
5   79703  200411  1.405766  0.071864  1.333902
6   79703  200412  1.405766  0.071864  1.333902
7   79703  200501  1.405766  0.071864  1.333902
8   79703  200502  1.405766  0.071864  1.333902
9   79703  200503  1.405766  0.071864  1.333902
```

---

### AssetGrowth_q

**Status**: ❌ FAILED

**Test Results**:
- Test 1 - Column names: ✅ PASSED
- Test 2 - Superset check: ❌ FAILED (Python missing 69 Stata observations)
- Test 3 - Precision1 check: ✅ PASSED
- Test 4 - Precision2 check: ✅ PASSED

**Columns**: ['AssetGrowth_q']

**Observations**:
- Stata:  2,303,961
- Python: 2,303,964
- Common: 2,303,892

**Precision1**: 0.001% obs with std_diff >= 1.00e-02 (tolerance: < 10%)

**Precision2**: 99th percentile diff = 1.89e-08 (tolerance: < 1.00e+00)

**Summary Statistics** (Common Observations):

| Statistic  |          Stata |         Python |     Difference | Std Difference |
|------------|----------------|----------------|----------------|----------------|
| count      |       2.30e+06 |       2.30e+06 |       2.30e+06 |       2.30e+06 |
| mean       |         0.1633 |         0.1633 |      -1.24e-05 |      -3.55e-06 |
| std        |         3.5114 |         3.5114 |         0.0143 |         0.0041 |
| min        |        -1.0268 |        -1.0268 |       -12.1084 |        -3.4483 |
| 25%        |        -0.0283 |        -0.0283 |      -2.02e-09 |      -5.74e-10 |
| 50%        |         0.0624 |         0.0624 |      -8.11e-13 |      -2.31e-13 |
| 75%        |         0.1821 |         0.1822 |       2.01e-09 |       5.72e-10 |
| max        |      2788.4187 |      2788.4186 |         3.0812 |         0.8775 |

**Regression Analysis** (Python ~ Stata):

- **Model**: python = -0.0000 + 1.0000 * stata
- **R-squared**: 1.0000
- **N observations**: 2,303,892

| Coefficient |     Estimate |    Std Error | t-statistic |   p-value |
|-------------|--------------|--------------|-------------|----------|
| Intercept   |    -9.76e-06 |     9.41e-06 |     -1.0379 |     0.299 |
| Slope       |       1.0000 |     2.68e-06 | 373736.5368 |     0.000 |

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
- Num observations with std_diff >= TOL_DIFF_1: 32/2303892 (0.001%)
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
- Python: 3,600,497
- Common: 3,595,932

**Precision1**: 0.004% obs with std_diff >= 1.00e-02 (tolerance: < 10%)

**Precision2**: 99th percentile diff = 8.49e-08 (tolerance: < 1.00e+00)

**Summary Statistics** (Common Observations):

| Statistic  |          Stata |         Python |     Difference | Std Difference |
|------------|----------------|----------------|----------------|----------------|
| count      |       3.60e+06 |       3.60e+06 |       3.60e+06 |       3.60e+06 |
| mean       |         0.5929 |         0.5929 |      -8.44e-07 |      -2.20e-06 |
| std        |         0.3840 |         0.3840 |       3.41e-04 |       8.87e-04 |
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
| Intercept   |    -9.38e-07 |     3.30e-07 |     -2.8411 |     0.004 |
| Slope       |       1.0000 |     4.68e-07 |    2.14e+06 |     0.000 |

**Feedback**:
- Num observations with std_diff >= TOL_DIFF_1: 158/3595932 (0.004%)
- Stata standard deviation: 3.84e-01

---

### AssetLiquidityBookQuart

**Status**: ❌ FAILED

**Test Results**:
- Test 1 - Column names: ✅ PASSED
- Test 2 - Superset check: ❌ FAILED (Python missing 62 Stata observations)
- Test 3 - Precision1 check: ✅ PASSED
- Test 4 - Precision2 check: ✅ PASSED

**Columns**: ['AssetLiquidityBookQuart']

**Observations**:
- Stata:  2,538,807
- Python: 2,553,352
- Common: 2,538,745

**Precision1**: 0.003% obs with std_diff >= 1.00e-02 (tolerance: < 10%)

**Precision2**: 99th percentile diff = 2.44e-08 (tolerance: < 1.00e+00)

**Summary Statistics** (Common Observations):

| Statistic  |          Stata |         Python |     Difference | Std Difference |
|------------|----------------|----------------|----------------|----------------|
| count      |       2.54e+06 |       2.54e+06 |       2.54e+06 |       2.54e+06 |
| mean       |         0.6036 |         0.6036 |      -1.28e-06 |      -9.52e-07 |
| std        |         1.3441 |         1.3441 |         0.0034 |         0.0025 |
| min        |       -10.8152 |       -10.8152 |        -4.2936 |        -3.1944 |
| 25%        |         0.5155 |         0.5155 |      -1.26e-08 |      -9.35e-09 |
| 50%        |         0.6075 |         0.6075 |         0.0000 |         0.0000 |
| 75%        |         0.7025 |         0.7025 |       1.25e-08 |       9.33e-09 |
| max        |      2003.3081 |      2003.3081 |         3.0063 |         2.2367 |

**Regression Analysis** (Python ~ Stata):

- **Model**: python = 0.0000 + 1.0000 * stata
- **R-squared**: 1.0000
- **N observations**: 2,538,745

| Coefficient |     Estimate |    Std Error | t-statistic |   p-value |
|-------------|--------------|--------------|-------------|----------|
| Intercept   |     1.13e-06 |     2.31e-06 |      0.4882 |     0.625 |
| Slope       |       1.0000 |     1.57e-06 | 637822.1012 |     0.000 |

**Missing Observations Sample**:
```
 index  permno  yyyymm  AssetLiquidityBookQuart
     0   10515  199604                 0.816307
     1   10515  199605                 0.781849
     2   10515  199606                 0.781849
     3   10872  199403                 0.519552
     4   10872  199404                 0.503846
     5   11545  199706                 0.818928
     6   11545  199707                 0.777539
     7   11545  199708                 0.777539
     8   12113  200006                 0.588284
     9   12113  200007                 0.651822
```

**Feedback**:
- Num observations with std_diff >= TOL_DIFF_1: 69/2538745 (0.003%)
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
- Python: 3,478,711
- Common: 3,476,318

**Precision1**: 0.006% obs with std_diff >= 1.00e-02 (tolerance: < 10%)

**Precision2**: 99th percentile diff = 1.68e-07 (tolerance: < 1.00e+00)

**Summary Statistics** (Common Observations):

| Statistic  |          Stata |         Python |     Difference | Std Difference |
|------------|----------------|----------------|----------------|----------------|
| count      |       3.48e+06 |       3.48e+06 |       3.48e+06 |       3.48e+06 |
| mean       |         0.4488 |         0.4488 |      -4.60e-07 |      -1.64e-06 |
| std        |         0.2802 |         0.2802 |       2.06e-04 |       7.35e-04 |
| min        |        -7.2979 |        -7.2979 |        -0.0545 |        -0.1943 |
| 25%        |         0.2655 |         0.2655 |      -7.62e-09 |      -2.72e-08 |
| 50%        |         0.4442 |         0.4442 |       1.05e-13 |       3.76e-13 |
| 75%        |         0.5694 |         0.5694 |       7.64e-09 |       2.73e-08 |
| max        |        48.9168 |        48.9168 |         0.0444 |         0.1583 |

**Regression Analysis** (Python ~ Stata):

- **Model**: python = -0.0000 + 1.0000 * stata
- **R-squared**: 1.0000
- **N observations**: 3,476,318

| Coefficient |     Estimate |    Std Error | t-statistic |   p-value |
|-------------|--------------|--------------|-------------|----------|
| Intercept   |    -4.89e-07 |     2.09e-07 |     -2.3445 |     0.019 |
| Slope       |       1.0000 |     3.94e-07 |    2.54e+06 |     0.000 |

**Feedback**:
- Num observations with std_diff >= TOL_DIFF_1: 225/3476318 (0.006%)
- Stata standard deviation: 2.80e-01

---

### AssetLiquidityMarketQuart

**Status**: ❌ FAILED

**Test Results**:
- Test 1 - Column names: ✅ PASSED
- Test 2 - Superset check: ❌ FAILED (Python missing 67 Stata observations)
- Test 3 - Precision1 check: ✅ PASSED
- Test 4 - Precision2 check: ✅ PASSED

**Columns**: ['AssetLiquidityMarketQuart']

**Observations**:
- Stata:  2,503,163
- Python: 2,503,153
- Common: 2,503,096

**Precision1**: 0.005% obs with std_diff >= 1.00e-02 (tolerance: < 10%)

**Precision2**: 99th percentile diff = 1.50e-07 (tolerance: < 1.00e+00)

**Summary Statistics** (Common Observations):

| Statistic  |          Stata |         Python |     Difference | Std Difference |
|------------|----------------|----------------|----------------|----------------|
| count      |       2.50e+06 |       2.50e+06 |       2.50e+06 |       2.50e+06 |
| mean       |         0.4482 |         0.4482 |      -1.00e-06 |      -3.60e-06 |
| std        |         0.2781 |         0.2781 |       6.86e-04 |         0.0025 |
| min        |        -6.3541 |        -6.3541 |        -0.3661 |        -1.3166 |
| 25%        |         0.2725 |         0.2725 |      -7.72e-09 |      -2.78e-08 |
| 50%        |         0.4522 |         0.4522 |       6.25e-12 |       2.25e-11 |
| 75%        |         0.5664 |         0.5664 |       7.73e-09 |       2.78e-08 |
| max        |       137.3564 |       137.3564 |         0.2938 |         1.0567 |

**Regression Analysis** (Python ~ Stata):

- **Model**: python = -0.0000 + 1.0000 * stata
- **R-squared**: 1.0000
- **N observations**: 2,503,096

| Coefficient |     Estimate |    Std Error | t-statistic |   p-value |
|-------------|--------------|--------------|-------------|----------|
| Intercept   |    -2.85e-07 |     8.22e-07 |     -0.3471 |     0.729 |
| Slope       |       1.0000 |     1.56e-06 | 641375.6907 |     0.000 |

**Missing Observations Sample**:
```
 index  permno  yyyymm  AssetLiquidityMarketQuart
     0   10515  199604                   0.819677
     1   10515  199605                   0.833838
     2   10515  199606                   0.833838
     3   10872  199403                   0.429908
     4   10872  199404                   0.470614
     5   11545  199706                   0.363298
     6   11545  199707                   0.407572
     7   11545  199708                   0.407572
     8   12113  200006                   0.683969
     9   12113  200007                   0.820795
```

**Feedback**:
- Num observations with std_diff >= TOL_DIFF_1: 128/2503096 (0.005%)
- Stata standard deviation: 2.78e-01

---

### AssetTurnover

**Status**: ✅ PASSED

**Test Results**:
- Test 1 - Column names: ✅ PASSED
- Test 2 - Superset check: ✅ PASSED
- Test 3 - Precision1 check: ✅ PASSED
- Test 4 - Precision2 check: ✅ PASSED

**Columns**: ['AssetTurnover']

**Observations**:
- Stata:  2,796,921
- Python: 2,817,397
- Common: 2,796,921

**Precision1**: 0.001% obs with std_diff >= 1.00e-02 (tolerance: < 10%)

**Precision2**: 99th percentile diff = 4.00e-09 (tolerance: < 1.00e+00)

**Summary Statistics** (Common Observations):

| Statistic  |          Stata |         Python |     Difference | Std Difference |
|------------|----------------|----------------|----------------|----------------|
| count      |       2.80e+06 |       2.80e+06 |       2.80e+06 |       2.80e+06 |
| mean       |         5.2784 |         5.2785 |       1.08e-04 |       4.15e-07 |
| std        |       261.1047 |       261.1082 |         0.0761 |       2.92e-04 |
| min        |         0.0000 |        -0.0000 |       -18.4493 |        -0.0707 |
| 25%        |         0.9854 |         0.9854 |      -3.85e-08 |      -1.47e-10 |
| 50%        |         1.8726 |         1.8726 |         0.0000 |         0.0000 |
| 75%        |         3.0805 |         3.0805 |       3.86e-08 |       1.48e-10 |
| max        |    108845.1100 |    108847.6000 |        27.7236 |         0.1062 |

**Regression Analysis** (Python ~ Stata):

- **Model**: python = 0.0000 + 1.0000 * stata
- **R-squared**: 1.0000
- **N observations**: 2,796,921

| Coefficient |     Estimate |    Std Error | t-statistic |   p-value |
|-------------|--------------|--------------|-------------|----------|
| Intercept   |     3.73e-05 |     4.55e-05 |      0.8195 |     0.412 |
| Slope       |       1.0000 |     1.74e-07 |    5.74e+06 |     0.000 |

**Feedback**:
- Num observations with std_diff >= TOL_DIFF_1: 36/2796921 (0.001%)
- Stata standard deviation: 2.61e+02

---

### AssetTurnover_q

**Status**: ❌ FAILED

**Test Results**:
- Test 1 - Column names: ✅ PASSED
- Test 2 - Superset check: ❌ FAILED (Python missing 50 Stata observations)
- Test 3 - Precision1 check: ✅ PASSED
- Test 4 - Precision2 check: ✅ PASSED

**Columns**: ['AssetTurnover_q']

**Observations**:
- Stata:  1,963,604
- Python: 2,183,944
- Common: 1,963,554

**Precision1**: 0.004% obs with std_diff >= 1.00e-02 (tolerance: < 10%)

**Precision2**: 99th percentile diff = 5.69e-09 (tolerance: < 1.00e+00)

**Summary Statistics** (Common Observations):

| Statistic  |          Stata |         Python |     Difference | Std Difference |
|------------|----------------|----------------|----------------|----------------|
| count      |       1.96e+06 |       1.96e+06 |       1.96e+06 |       1.96e+06 |
| mean       |         1.3789 |         1.3789 |       1.97e-05 |       3.57e-07 |
| std        |        55.1418 |        55.1407 |         0.0140 |       2.54e-04 |
| min        |         0.0000 |        -0.0000 |        -2.2891 |        -0.0415 |
| 25%        |         0.2551 |         0.2550 |      -1.00e-08 |      -1.82e-10 |
| 50%        |         0.5119 |         0.5119 |         0.0000 |         0.0000 |
| 75%        |         0.8749 |         0.8749 |       1.00e-08 |       1.82e-10 |
| max        |     27068.2270 |     27068.2000 |         5.1241 |         0.0929 |

**Regression Analysis** (Python ~ Stata):

- **Model**: python = 0.0000 + 1.0000 * stata
- **R-squared**: 1.0000
- **N observations**: 1,963,554

| Coefficient |     Estimate |    Std Error | t-statistic |   p-value |
|-------------|--------------|--------------|-------------|----------|
| Intercept   |     4.61e-05 |     9.98e-06 |      4.6213 |     0.000 |
| Slope       |       1.0000 |     1.81e-07 |    5.53e+06 |     0.000 |

**Missing Observations Sample**:
```
 index  permno  yyyymm  AssetTurnover_q
     0   11545  199706         0.546037
     1   11545  199707         0.546037
     2   11545  199708         0.546037
     3   12113  200006         0.655086
     4   12113  200007         0.655086
     5   12113  200008         0.655086
     6   12373  202406         0.021631
     7   12373  202407         0.021631
     8   12373  202408         0.021631
     9   12373  202409         0.038419
```

**Feedback**:
- Num observations with std_diff >= TOL_DIFF_1: 82/1963554 (0.004%)
- Stata standard deviation: 5.51e+01

---

### BMq

**Status**: ❌ FAILED

**Test Results**:
- Test 1 - Column names: ✅ PASSED
- Test 2 - Superset check: ❌ FAILED (Python missing 1 Stata observations)
- Test 3 - Precision1 check: ✅ PASSED
- Test 4 - Precision2 check: ✅ PASSED

**Columns**: ['BMq']

**Observations**:
- Stata:  2,568,885
- Python: 2,631,810
- Common: 2,568,884

**Precision1**: 0.004% obs with std_diff >= 1.00e-02 (tolerance: < 10%)

**Precision2**: 99th percentile diff = 1.35e-07 (tolerance: < 1.00e+00)

**Summary Statistics** (Common Observations):

| Statistic  |          Stata |         Python |     Difference | Std Difference |
|------------|----------------|----------------|----------------|----------------|
| count      |       2.57e+06 |       2.57e+06 |       2.57e+06 |       2.57e+06 |
| mean       |        -0.5919 |        -0.5919 |       1.50e-06 |       1.56e-06 |
| std        |         0.9608 |         0.9608 |         0.0029 |         0.0030 |
| min        |       -13.7467 |       -13.7467 |        -0.8206 |        -0.8540 |
| 25%        |        -1.1088 |        -1.1088 |      -2.50e-08 |      -2.61e-08 |
| 50%        |        -0.5062 |        -0.5062 |      -1.45e-11 |      -1.51e-11 |
| 75%        |         0.0109 |         0.0109 |       2.51e-08 |       2.61e-08 |
| max        |         6.6128 |         6.6128 |         2.3152 |         2.4096 |

**Regression Analysis** (Python ~ Stata):

- **Model**: python = -0.0000 + 1.0000 * stata
- **R-squared**: 1.0000
- **N observations**: 2,568,884

| Coefficient |     Estimate |    Std Error | t-statistic |   p-value |
|-------------|--------------|--------------|-------------|----------|
| Intercept   |    -2.95e-06 |     2.11e-06 |     -1.3967 |     0.163 |
| Slope       |       1.0000 |     1.87e-06 | 533921.2755 |     0.000 |

**Missing Observations Sample**:
```
 index  permno  yyyymm      BMq
     0   19316  202412 0.685185
```

**Feedback**:
- Num observations with std_diff >= TOL_DIFF_1: 97/2568884 (0.004%)
- Stata standard deviation: 9.61e-01

---

### BetaBDLeverage

**Status**: ✅ PASSED

**Test Results**:
- Test 1 - Column names: ✅ PASSED
- Test 2 - Superset check: ✅ PASSED
- Test 3 - Precision1 check: ✅ PASSED
- Test 4 - Precision2 check: ✅ PASSED

**Columns**: ['BetaBDLeverage']

**Observations**:
- Stata:  2,116,539
- Python: 2,130,495
- Common: 2,116,539

**Precision1**: 2.206% obs with std_diff >= 1.00e-02 (tolerance: < 10%)

**Precision2**: 99th percentile diff = 2.31e-01 (tolerance: < 1.00e+00)

**Summary Statistics** (Common Observations):

| Statistic  |          Stata |         Python |     Difference | Std Difference |
|------------|----------------|----------------|----------------|----------------|
| count      |       2.12e+06 |       2.12e+06 |       2.12e+06 |       2.12e+06 |
| mean       |         0.2175 |         0.2194 |         0.0019 |         0.0019 |
| std        |         0.9765 |         0.9681 |         0.1224 |         0.1254 |
| min        |       -29.5917 |       -29.5915 |        -5.8416 |        -5.9822 |
| 25%        |        -0.1353 |        -0.1334 |      -5.37e-06 |      -5.50e-06 |
| 50%        |         0.2846 |         0.2856 |       4.28e-05 |       4.38e-05 |
| 75%        |         0.6641 |         0.6649 |       7.60e-05 |       7.78e-05 |
| max        |        25.2977 |        25.2978 |        16.0268 |        16.4126 |

**Regression Analysis** (Python ~ Stata):

- **Model**: python = 0.0054 + 0.9836 * stata
- **R-squared**: 0.9843
- **N observations**: 2,116,539

| Coefficient |     Estimate |    Std Error | t-statistic |   p-value |
|-------------|--------------|--------------|-------------|----------|
| Intercept   |       0.0054 |     8.55e-05 |     63.7188 |     0.000 |
| Slope       |       0.9836 |     8.54e-05 |  11514.0790 |     0.000 |

**Feedback**:
- Num observations with std_diff >= TOL_DIFF_1: 46683/2116539 (2.206%)
- Stata standard deviation: 9.76e-01

---

### BetaDimson

**Status**: ✅ PASSED

**Test Results**:
- Test 1 - Column names: ✅ PASSED
- Test 2 - Superset check: ✅ PASSED
- Test 3 - Precision1 check: ✅ PASSED
- Test 4 - Precision2 check: ✅ PASSED

**Columns**: ['BetaDimson']

**Observations**:
- Stata:  5,002,680
- Python: 5,083,747
- Common: 5,002,680

**Precision1**: 2.944% obs with std_diff >= 1.00e-02 (tolerance: < 10%)

**Precision2**: 99th percentile diff = 1.90e-02 (tolerance: < 1.00e+00)

**Summary Statistics** (Common Observations):

| Statistic  |          Stata |         Python |     Difference | Std Difference |
|------------|----------------|----------------|----------------|----------------|
| count      |       5.00e+06 |       5.00e+06 |       5.00e+06 |       5.00e+06 |
| mean       |         0.7973 |         0.7978 |       4.79e-04 |       2.00e-04 |
| std        |         2.3944 |         2.3967 |         0.0133 |         0.0056 |
| min        |      -286.1514 |      -285.0655 |        -3.0642 |        -1.2797 |
| 25%        |        -0.0184 |        -0.0184 |      -4.30e-04 |      -1.79e-04 |
| 50%        |         0.6958 |         0.6962 |       1.02e-08 |       4.25e-09 |
| 75%        |         1.5830 |         1.5838 |         0.0013 |       5.26e-04 |
| max        |       301.7971 |       302.8436 |         1.6407 |         0.6852 |

**Regression Analysis** (Python ~ Stata):

- **Model**: python = -0.0003 + 1.0009 * stata
- **R-squared**: 1.0000
- **N observations**: 5,002,680

| Coefficient |     Estimate |    Std Error | t-statistic |   p-value |
|-------------|--------------|--------------|-------------|----------|
| Intercept   |    -2.63e-04 |     6.19e-06 |    -42.4922 |     0.000 |
| Slope       |       1.0009 |     2.45e-06 | 408024.9645 |     0.000 |

**Feedback**:
- Num observations with std_diff >= TOL_DIFF_1: 147265/5002680 (2.944%)
- Stata standard deviation: 2.39e+00

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

**Precision1**: 0.001% obs with std_diff >= 1.00e-02 (tolerance: < 10%)

**Precision2**: 99th percentile diff = 1.16e-04 (tolerance: < 1.00e+00)

**Summary Statistics** (Common Observations):

| Statistic  |          Stata |         Python |     Difference | Std Difference |
|------------|----------------|----------------|----------------|----------------|
| count      |       4.29e+06 |       4.29e+06 |       4.29e+06 |       4.29e+06 |
| mean       |         1.5351 |         1.5351 |      -4.90e-06 |      -7.36e-07 |
| std        |         6.6568 |         6.6566 |       5.54e-04 |       8.33e-05 |
| min        |       5.10e-13 |       5.13e-13 |        -0.3036 |        -0.0456 |
| 25%        |         0.2920 |         0.2920 |      -2.20e-08 |      -3.31e-09 |
| 50%        |         0.8168 |         0.8168 |       5.22e-10 |       7.84e-11 |
| 75%        |         1.7846 |         1.7846 |       3.14e-08 |       4.71e-09 |
| max        |      2770.3259 |      2770.1126 |         0.1280 |         0.0192 |

**Regression Analysis** (Python ~ Stata):

- **Model**: python = 0.0000 + 1.0000 * stata
- **R-squared**: 1.0000
- **N observations**: 4,285,574

| Coefficient |     Estimate |    Std Error | t-statistic |   p-value |
|-------------|--------------|--------------|-------------|----------|
| Intercept   |     4.16e-05 |     2.56e-07 |    162.4728 |     0.000 |
| Slope       |       1.0000 |     3.75e-08 |    2.67e+07 |     0.000 |

**Feedback**:
- Num observations with std_diff >= TOL_DIFF_1: 40/4285574 (0.001%)
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

**Precision2**: 99th percentile diff = 1.59e-07 (tolerance: < 1.00e+00)

**Summary Statistics** (Common Observations):

| Statistic  |          Stata |         Python |     Difference | Std Difference |
|------------|----------------|----------------|----------------|----------------|
| count      |       3.26e+06 |       3.26e+06 |       3.26e+06 |       3.26e+06 |
| mean       |         1.5559 |         1.5559 |       1.00e-10 |       3.99e-11 |
| std        |         2.5110 |         2.5110 |       8.73e-08 |       3.48e-08 |
| min        |         0.0000 |         0.0000 |      -2.27e-06 |      -9.05e-07 |
| 25%        |         0.1774 |         0.1774 |      -1.00e-08 |      -3.98e-09 |
| 50%        |         0.6136 |         0.6136 |         0.0000 |         0.0000 |
| 75%        |         1.8032 |         1.8032 |       1.00e-08 |       3.98e-09 |
| max        |        39.9582 |        39.9582 |       2.22e-06 |       8.83e-07 |

**Regression Analysis** (Python ~ Stata):

- **Model**: python = -0.0000 + 1.0000 * stata
- **R-squared**: 1.0000
- **N observations**: 3,262,927

| Coefficient |     Estimate |    Std Error | t-statistic |   p-value |
|-------------|--------------|--------------|-------------|----------|
| Intercept   |    -4.95e-10 |     5.69e-11 |     -8.7096 |     0.000 |
| Slope       |       1.0000 |     1.93e-11 |    5.19e+10 |     0.000 |

**Feedback**:
- Num observations with std_diff >= TOL_DIFF_1: 0/3262927 (0.000%)
- Stata standard deviation: 2.51e+00

---

### BookLeverageQuarterly

**Status**: ❌ FAILED

**Test Results**:
- Test 1 - Column names: ✅ PASSED
- Test 2 - Superset check: ❌ FAILED (Python missing 1 Stata observations)
- Test 3 - Precision1 check: ✅ PASSED
- Test 4 - Precision2 check: ✅ PASSED

**Columns**: ['BookLeverageQuarterly']

**Observations**:
- Stata:  2,572,594
- Python: 2,670,974
- Common: 2,572,593

**Precision1**: 0.001% obs with std_diff >= 1.00e-02 (tolerance: < 10%)

**Precision2**: 99th percentile diff = 4.13e-13 (tolerance: < 1.00e+00)

**Summary Statistics** (Common Observations):

| Statistic  |          Stata |         Python |     Difference | Std Difference |
|------------|----------------|----------------|----------------|----------------|
| count      |       2.57e+06 |       2.57e+06 |       2.57e+06 |       2.57e+06 |
| mean       |       945.9143 |            inf |            inf |            inf |
| std        |       3.67e+06 |            N/A |            N/A |            N/A |
| min        |      -1.62e+09 |    -34413.0000 |       -96.2367 |      -2.62e-05 |
| 25%        |         1.4348 |         1.4348 |      -6.20e-08 |      -1.69e-14 |
| 50%        |         2.0340 |         2.0341 |      -2.22e-16 |      -6.04e-23 |
| 75%        |         3.3458 |         3.3459 |       6.19e-08 |       1.68e-14 |
| max        |       2.85e+09 |            inf |            inf |            inf |

**Regression Analysis** (Python ~ Stata):

- **Model**: python = inf + nan * stata
- **R-squared**: nan
- **N observations**: 2,572,593

| Coefficient |     Estimate |    Std Error | t-statistic |   p-value |
|-------------|--------------|--------------|-------------|----------|
| Intercept   |          nan |          nan |         nan |       nan |
| Slope       |          nan |          nan |         nan |       nan |

**Missing Observations Sample**:
```
 index  permno  yyyymm  BookLeverageQuarterly
     0   19316  202412               1.832112
```

**Feedback**:
- Num observations with std_diff >= TOL_DIFF_1: 18/2572593 (0.001%)
- Stata standard deviation: 3.67e+06

---

### BrandCapital

**Status**: ❌ FAILED

**Test Results**:
- Test 1 - Column names: ✅ PASSED
- Test 2 - Superset check: ❌ FAILED (Python missing 48 Stata observations)
- Test 3 - Precision1 check: ✅ PASSED
- Test 4 - Precision2 check: ✅ PASSED

**Columns**: ['BrandCapital']

**Observations**:
- Stata:  1,231,460
- Python: 1,280,672
- Common: 1,231,412

**Precision1**: 5.878% obs with std_diff >= 1.00e-02 (tolerance: < 10%)

**Precision2**: 99th percentile diff = 8.25e-02 (tolerance: < 1.00e+00)

**Summary Statistics** (Common Observations):

| Statistic  |          Stata |         Python |     Difference | Std Difference |
|------------|----------------|----------------|----------------|----------------|
| count      |       1.23e+06 |       1.23e+06 |       1.23e+06 |       1.23e+06 |
| mean       |         0.0642 |         0.0656 |         0.0014 |         0.0040 |
| std        |         0.3504 |         0.3545 |         0.0239 |         0.0683 |
| min        |        -0.0066 |        -0.0066 |        -0.0211 |        -0.0603 |
| 25%        |         0.0043 |         0.0045 |      -1.01e-10 |      -2.88e-10 |
| 50%        |         0.0228 |         0.0238 |       2.62e-10 |       7.46e-10 |
| 75%        |         0.0651 |         0.0669 |       1.75e-07 |       4.99e-07 |
| max        |        86.0362 |        86.0362 |         6.8422 |        19.5251 |

**Regression Analysis** (Python ~ Stata):

- **Model**: python = 0.0008 + 1.0094 * stata
- **R-squared**: 0.9955
- **N observations**: 1,231,412

| Coefficient |     Estimate |    Std Error | t-statistic |   p-value |
|-------------|--------------|--------------|-------------|----------|
| Intercept   |     8.07e-04 |     2.17e-05 |     37.1894 |     0.000 |
| Slope       |       1.0094 |     6.09e-05 |  16562.4815 |     0.000 |

**Missing Observations Sample**:
```
 index  permno  yyyymm  BrandCapital
     0   16981  202206      0.017015
     1   16981  202207      0.017015
     2   16981  202208      0.017015
     3   16981  202209      0.017015
     4   16981  202210      0.017015
     5   16981  202211      0.017015
     6   16981  202212      0.017015
     7   16981  202301      0.017015
     8   16981  202302      0.017015
     9   16981  202303      0.017015
```

**Feedback**:
- Num observations with std_diff >= TOL_DIFF_1: 72379/1231412 (5.878%)
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

**Precision1**: 0.008% obs with std_diff >= 1.00e-02 (tolerance: < 10%)

**Precision2**: 99th percentile diff = 6.65e-08 (tolerance: < 1.00e+00)

**Summary Statistics** (Common Observations):

| Statistic  |          Stata |         Python |     Difference | Std Difference |
|------------|----------------|----------------|----------------|----------------|
| count      |       2.10e+06 |       2.10e+06 |       2.10e+06 |       2.10e+06 |
| mean       |         0.1168 |         0.1168 |       1.23e-07 |       2.43e-07 |
| std        |         0.5041 |         0.5040 |       3.71e-04 |       7.35e-04 |
| min        |      -162.6901 |      -162.6901 |        -0.2216 |        -0.4396 |
| 25%        |         0.0533 |         0.0533 |      -3.47e-09 |      -6.89e-09 |
| 50%        |         0.1320 |         0.1320 |       4.61e-12 |       9.15e-12 |
| 75%        |         0.2129 |         0.2129 |       3.50e-09 |       6.94e-09 |
| max        |        26.7835 |        26.7835 |         0.0800 |         0.1586 |

**Regression Analysis** (Python ~ Stata):

- **Model**: python = 0.0000 + 1.0000 * stata
- **R-squared**: 1.0000
- **N observations**: 2,103,518

| Coefficient |     Estimate |    Std Error | t-statistic |   p-value |
|-------------|--------------|--------------|-------------|----------|
| Intercept   |     4.01e-07 |     2.62e-07 |      1.5282 |     0.126 |
| Slope       |       1.0000 |     5.07e-07 |    1.97e+06 |     0.000 |

**Feedback**:
- Num observations with std_diff >= TOL_DIFF_1: 172/2103518 (0.008%)
- Stata standard deviation: 5.04e-01

---

### CBOperProfLagAT_q

**Status**: ❌ FAILED

**Test Results**:
- Test 1 - Column names: ✅ PASSED
- Test 2 - Superset check: ❌ FAILED (Python missing 1 Stata observations)
- Test 3 - Precision1 check: ❌ FAILED
- Test 4 - Precision2 check: ❌ FAILED

**Columns**: ['CBOperProfLagAT_q']

**Observations**:
- Stata:  1,911,489
- Python: 2,183,955
- Common: 1,911,488

**Precision1**: 26.694% obs with std_diff >= 1.00e-02 (tolerance: < 10%)

**Precision2**: 99th percentile diff = 2.54e+00 (tolerance: < 1.00e+00)

**Summary Statistics** (Common Observations):

| Statistic  |          Stata |         Python |     Difference | Std Difference |
|------------|----------------|----------------|----------------|----------------|
| count      |       1.91e+06 |       1.91e+06 |       1.91e+06 |       1.91e+06 |
| mean       |         0.0219 |         0.0116 |        -0.0103 |        -0.0584 |
| std        |         0.1758 |         0.2598 |         0.2067 |         1.1760 |
| min        |       -89.0698 |       -89.0698 |       -38.9822 |      -221.7759 |
| 25%        |        -0.0051 |        -0.0079 |      -1.18e-09 |      -6.69e-09 |
| 50%        |         0.0278 |         0.0285 |       1.14e-10 |       6.50e-10 |
| 75%        |         0.0571 |         0.0598 |       2.69e-09 |       1.53e-08 |
| max        |        22.7565 |        23.8488 |        23.8496 |       135.6843 |

**Regression Analysis** (Python ~ Stata):

- **Model**: python = -0.0081 + 0.9011 * stata
- **R-squared**: 0.3716
- **N observations**: 1,911,488

| Coefficient |     Estimate |    Std Error | t-statistic |   p-value |
|-------------|--------------|--------------|-------------|----------|
| Intercept   |      -0.0081 |     1.50e-04 |    -53.9541 |     0.000 |
| Slope       |       0.9011 |     8.48e-04 |   1063.2238 |     0.000 |

**Missing Observations Sample**:
```
 index  permno  yyyymm  CBOperProfLagAT_q
     0   19316  202412           0.009463
```

**Feedback**:
- Num observations with std_diff >= TOL_DIFF_1: 510261/1911488 (26.694%)
- Stata standard deviation: 1.76e-01

**Most Recent Bad Observations**:
```
   permno  yyyymm    python     stata      diff
0   10333  202412 -0.138080 -0.068818 -0.069262
1   10382  202412  0.042999  0.023126  0.019874
2   10516  202412  0.023663  0.018805  0.004858
3   10517  202412 -0.097929  0.305647 -0.403575
4   11144  202412  0.066241  0.050950  0.015291
5   11654  202412 -0.018806 -0.030510  0.011704
6   11731  202412  0.049574  0.026383  0.023191
7   11850  202412  0.045113  0.043205  0.001908
8   12009  202412  0.019519  0.017253  0.002266
9   12017  202412 -0.085506 -0.091540  0.006035
```

**Largest Differences**:
```
   permno  yyyymm     python         stata       diff
0   85002  200003 -38.982167  4.432618e-17 -38.982167
1   85002  200004 -38.982167  4.432618e-17 -38.982167
2   85002  200005 -38.982167  4.432618e-17 -38.982167
3   25778  198212 -32.869907 -1.559557e-01 -32.713951
4   25778  198301 -32.869907 -1.559557e-01 -32.713951
5   25778  198302 -32.869907 -1.559557e-01 -32.713951
6   79906  199412 -31.007524 -1.504778e-03 -31.006019
7   79906  199501 -31.007524 -1.504778e-03 -31.006019
8   79906  199502 -31.007524 -1.504778e-03 -31.006019
9   79906  199409 -26.832238 -2.543420e-02 -26.806804
```

---

### CFq

**Status**: ✅ PASSED

**Test Results**:
- Test 1 - Column names: ✅ PASSED
- Test 2 - Superset check: ✅ PASSED
- Test 3 - Precision1 check: ✅ PASSED
- Test 4 - Precision2 check: ✅ PASSED

**Columns**: ['CFq']

**Observations**:
- Stata:  2,797,878
- Python: 3,041,660
- Common: 2,797,878

**Precision1**: 0.021% obs with std_diff >= 1.00e-02 (tolerance: < 10%)

**Precision2**: 99th percentile diff = 2.14e-08 (tolerance: < 1.00e+00)

**Summary Statistics** (Common Observations):

| Statistic  |          Stata |         Python |     Difference | Std Difference |
|------------|----------------|----------------|----------------|----------------|
| count      |       2.80e+06 |       2.80e+06 |       2.80e+06 |       2.80e+06 |
| mean       |        -0.0128 |        -0.0128 |       1.15e-05 |       9.81e-06 |
| std        |         1.1714 |         1.1714 |         0.0088 |         0.0075 |
| min        |      -917.6409 |      -917.6410 |        -2.7228 |        -2.3243 |
| 25%        |         0.0039 |         0.0039 |      -6.64e-10 |      -5.67e-10 |
| 50%        |         0.0195 |         0.0195 |      -4.32e-14 |      -3.69e-14 |
| 75%        |         0.0369 |         0.0369 |       6.62e-10 |       5.65e-10 |
| max        |       163.1038 |       163.1038 |         8.6011 |         7.3423 |

**Regression Analysis** (Python ~ Stata):

- **Model**: python = 0.0000 + 1.0000 * stata
- **R-squared**: 0.9999
- **N observations**: 2,797,878

| Coefficient |     Estimate |    Std Error | t-statistic |   p-value |
|-------------|--------------|--------------|-------------|----------|
| Intercept   |     1.10e-05 |     5.24e-06 |      2.0908 |     0.037 |
| Slope       |       1.0000 |     4.47e-06 | 223574.4849 |     0.000 |

**Feedback**:
- Num observations with std_diff >= TOL_DIFF_1: 576/2797878 (0.021%)
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
- Python: 2,987,356
- Common: 2,985,685

**Precision1**: 0.001% obs with std_diff >= 1.00e-02 (tolerance: < 10%)

**Precision2**: 99th percentile diff = 8.51e-08 (tolerance: < 1.00e+00)

**Summary Statistics** (Common Observations):

| Statistic  |          Stata |         Python |     Difference | Std Difference |
|------------|----------------|----------------|----------------|----------------|
| count      |       2.99e+06 |       2.99e+06 |       2.99e+06 |       2.99e+06 |
| mean       |         1.1455 |         1.1455 |       3.07e-07 |       1.71e-07 |
| std        |         1.7917 |         1.7917 |       2.21e-04 |       1.23e-04 |
| min        |        -1.8804 |        -1.8804 |        -0.0353 |        -0.0197 |
| 25%        |         0.3456 |         0.3456 |      -1.39e-08 |      -7.78e-09 |
| 50%        |         0.9236 |         0.9236 |         0.0000 |         0.0000 |
| 75%        |         1.5797 |         1.5797 |       1.43e-08 |       7.98e-09 |
| max        |       392.8943 |       392.8943 |         0.0736 |         0.0411 |

**Regression Analysis** (Python ~ Stata):

- **Model**: python = 0.0000 + 1.0000 * stata
- **R-squared**: 1.0000
- **N observations**: 2,985,685

| Coefficient |     Estimate |    Std Error | t-statistic |   p-value |
|-------------|--------------|--------------|-------------|----------|
| Intercept   |     4.43e-07 |     1.52e-07 |      2.9220 |     0.003 |
| Slope       |       1.0000 |     7.14e-08 |    1.40e+07 |     0.000 |

**Feedback**:
- Num observations with std_diff >= TOL_DIFF_1: 36/2985685 (0.001%)
- Stata standard deviation: 1.79e+00

---

### CapTurnover_q

**Status**: ❌ FAILED

**Test Results**:
- Test 1 - Column names: ✅ PASSED
- Test 2 - Superset check: ❌ FAILED (Python missing 69 Stata observations)
- Test 3 - Precision1 check: ✅ PASSED
- Test 4 - Precision2 check: ✅ PASSED

**Columns**: ['CapTurnover_q']

**Observations**:
- Stata:  2,486,325
- Python: 2,486,376
- Common: 2,486,256

**Precision1**: 0.013% obs with std_diff >= 1.00e-02 (tolerance: < 10%)

**Precision2**: 99th percentile diff = 1.01e-08 (tolerance: < 1.00e+00)

**Summary Statistics** (Common Observations):

| Statistic  |          Stata |         Python |     Difference | Std Difference |
|------------|----------------|----------------|----------------|----------------|
| count      |       2.49e+06 |       2.49e+06 |       2.49e+06 |       2.49e+06 |
| mean       |         0.2638 |         0.2638 |       1.09e-05 |       3.47e-06 |
| std        |         3.1372 |         3.1373 |         0.0099 |         0.0032 |
| min        |        -0.9789 |        -0.9789 |        -1.8341 |        -0.5846 |
| 25%        |         0.0801 |         0.0801 |      -3.40e-09 |      -1.08e-09 |
| 50%        |         0.2127 |         0.2127 |         0.0000 |         0.0000 |
| 75%        |         0.3650 |         0.3650 |       3.40e-09 |       1.08e-09 |
| max        |      2816.9070 |      2816.9070 |         6.0506 |         1.9286 |

**Regression Analysis** (Python ~ Stata):

- **Model**: python = 0.0000 + 1.0000 * stata
- **R-squared**: 1.0000
- **N observations**: 2,486,256

| Coefficient |     Estimate |    Std Error | t-statistic |   p-value |
|-------------|--------------|--------------|-------------|----------|
| Intercept   |     1.11e-05 |     6.31e-06 |      1.7544 |     0.079 |
| Slope       |       1.0000 |     2.00e-06 | 499062.8595 |     0.000 |

**Missing Observations Sample**:
```
 index  permno  yyyymm  CapTurnover_q
     0   10515  199607       0.068358
     1   10515  199608       0.068358
     2   10515  199609       0.068358
     3   10872  199403       0.087038
     4   10872  199404       0.087038
     5   11545  199706       0.209439
     6   11545  199707       0.209439
     7   11545  199708       0.209439
     8   12113  200006       0.428770
     9   12113  200007       0.428770
```

**Feedback**:
- Num observations with std_diff >= TOL_DIFF_1: 326/2486256 (0.013%)
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
- Python: 3,297,084
- Common: 3,295,125

**Precision1**: 0.007% obs with std_diff >= 1.00e-02 (tolerance: < 10%)

**Precision2**: 99th percentile diff = 8.50e-08 (tolerance: < 1.00e+00)

**Summary Statistics** (Common Observations):

| Statistic  |          Stata |         Python |     Difference | Std Difference |
|------------|----------------|----------------|----------------|----------------|
| count      |       3.30e+06 |       3.30e+06 |       3.30e+06 |       3.30e+06 |
| mean       |         0.0889 |         0.0889 |      -2.05e-06 |      -2.29e-06 |
| std        |         0.8966 |         0.8966 |         0.0016 |         0.0018 |
| min        |        -1.4114 |        -1.4114 |        -0.7511 |        -0.8377 |
| 25%        |        -0.0138 |        -0.0138 |      -9.90e-09 |      -1.10e-08 |
| 50%        |         0.0232 |         0.0232 |         0.0000 |         0.0000 |
| 75%        |         0.0917 |         0.0917 |       9.89e-09 |       1.10e-08 |
| max        |       192.5833 |       192.5833 |         0.3378 |         0.3768 |

**Regression Analysis** (Python ~ Stata):

- **Model**: python = -0.0000 + 1.0000 * stata
- **R-squared**: 1.0000
- **N observations**: 3,295,125

| Coefficient |     Estimate |    Std Error | t-statistic |   p-value |
|-------------|--------------|--------------|-------------|----------|
| Intercept   |    -2.03e-06 |     8.99e-07 |     -2.2611 |     0.024 |
| Slope       |       1.0000 |     9.97e-07 |    1.00e+06 |     0.000 |

**Feedback**:
- Num observations with std_diff >= TOL_DIFF_1: 228/3295125 (0.007%)
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
- Python: 3,251,333
- Common: 3,249,290

**Precision1**: 0.006% obs with std_diff >= 1.00e-02 (tolerance: < 10%)

**Precision2**: 99th percentile diff = 5.80e-08 (tolerance: < 1.00e+00)

**Summary Statistics** (Common Observations):

| Statistic  |          Stata |         Python |     Difference | Std Difference |
|------------|----------------|----------------|----------------|----------------|
| count      |       3.25e+06 |       3.25e+06 |       3.25e+06 |       3.25e+06 |
| mean       |         0.0487 |         0.0487 |      -2.83e-06 |      -2.92e-06 |
| std        |         0.9693 |         0.9693 |         0.0013 |         0.0013 |
| min        |       -23.0669 |       -23.0669 |        -0.6600 |        -0.6808 |
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
| Intercept   |    -2.16e-06 |     7.15e-07 |     -3.0266 |     0.002 |
| Slope       |       1.0000 |     7.36e-07 |    1.36e+06 |     0.000 |

**Feedback**:
- Num observations with std_diff >= TOL_DIFF_1: 192/3249290 (0.006%)
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
- Python: 3,250,331
- Common: 3,222,277

**Precision1**: 0.001% obs with std_diff >= 1.00e-02 (tolerance: < 10%)

**Precision2**: 99th percentile diff = 5.32e-09 (tolerance: < 1.00e+00)

**Summary Statistics** (Common Observations):

| Statistic  |          Stata |         Python |     Difference | Std Difference |
|------------|----------------|----------------|----------------|----------------|
| count      |       3.22e+06 |       3.22e+06 |       3.22e+06 |       3.22e+06 |
| mean       |        -0.3833 |        -0.3833 |       3.53e-06 |       2.33e-08 |
| std        |       151.4586 |       151.4586 |         0.0089 |       5.87e-05 |
| min        |    -30903.6450 |    -30903.6451 |        -3.1309 |        -0.0207 |
| 25%        |        -0.0312 |        -0.0312 |      -2.22e-09 |      -1.47e-11 |
| 50%        |      -1.17e-04 |      -1.17e-04 |       6.89e-12 |       4.55e-14 |
| 75%        |         0.0251 |         0.0251 |       2.23e-09 |       1.48e-11 |
| max        |     24410.3810 |     24410.3806 |         3.2878 |         0.0217 |

**Regression Analysis** (Python ~ Stata):

- **Model**: python = 0.0000 + 1.0000 * stata
- **R-squared**: 1.0000
- **N observations**: 3,222,277

| Coefficient |     Estimate |    Std Error | t-statistic |   p-value |
|-------------|--------------|--------------|-------------|----------|
| Intercept   |     3.53e-06 |     4.95e-06 |      0.7126 |     0.476 |
| Slope       |       1.0000 |     3.27e-08 |    3.06e+07 |     0.000 |

**Feedback**:
- Num observations with std_diff >= TOL_DIFF_1: 24/3222277 (0.001%)
- Stata standard deviation: 1.51e+02

---

### ChangeRoA

**Status**: ❌ FAILED

**Test Results**:
- Test 1 - Column names: ✅ PASSED
- Test 2 - Superset check: ❌ FAILED (Python missing 1 Stata observations)
- Test 3 - Precision1 check: ✅ PASSED
- Test 4 - Precision2 check: ✅ PASSED

**Columns**: ['ChangeRoA']

**Observations**:
- Stata:  2,296,769
- Python: 2,526,839
- Common: 2,296,768

**Precision1**: 0.026% obs with std_diff >= 1.00e-02 (tolerance: < 10%)

**Precision2**: 99th percentile diff = 6.71e-08 (tolerance: < 1.00e+00)

**Summary Statistics** (Common Observations):

| Statistic  |          Stata |         Python |     Difference | Std Difference |
|------------|----------------|----------------|----------------|----------------|
| count      |       2.30e+06 |       2.30e+06 |       2.30e+06 |       2.30e+06 |
| mean       |        -0.0019 |        -0.0019 |       8.04e-07 |       3.43e-06 |
| std        |         0.2344 |         0.2345 |         0.0037 |         0.0160 |
| min        |       -55.1174 |       -55.1174 |        -1.7846 |        -7.6119 |
| 25%        |        -0.0078 |        -0.0078 |      -4.27e-10 |      -1.82e-09 |
| 50%        |      -7.35e-05 |      -7.33e-05 |      -3.71e-13 |      -1.58e-12 |
| 75%        |         0.0058 |         0.0058 |       4.28e-10 |       1.83e-09 |
| max        |       136.3447 |       136.3447 |         1.7846 |         7.6119 |

**Regression Analysis** (Python ~ Stata):

- **Model**: python = 0.0000 + 0.9999 * stata
- **R-squared**: 0.9997
- **N observations**: 2,296,768

| Coefficient |     Estimate |    Std Error | t-statistic |   p-value |
|-------------|--------------|--------------|-------------|----------|
| Intercept   |     6.52e-07 |     2.47e-06 |      0.2641 |     0.792 |
| Slope       |       0.9999 |     1.05e-05 |  94900.9351 |     0.000 |

**Missing Observations Sample**:
```
 index  permno  yyyymm  ChangeRoA
     0   19316  202412  -0.036712
```

**Feedback**:
- Num observations with std_diff >= TOL_DIFF_1: 590/2296768 (0.026%)
- Stata standard deviation: 2.34e-01

---

### ChangeRoE

**Status**: ❌ FAILED

**Test Results**:
- Test 1 - Column names: ✅ PASSED
- Test 2 - Superset check: ❌ FAILED (Python missing 1 Stata observations)
- Test 3 - Precision1 check: ✅ PASSED
- Test 4 - Precision2 check: ✅ PASSED

**Columns**: ['ChangeRoE']

**Observations**:
- Stata:  2,360,217
- Python: 2,535,910
- Common: 2,360,216

**Precision1**: 0.004% obs with std_diff >= 1.00e-02 (tolerance: < 10%)

**Precision2**: 99th percentile diff = 3.26e-09 (tolerance: < 1.00e+00)

**Summary Statistics** (Common Observations):

| Statistic  |          Stata |         Python |     Difference | Std Difference |
|------------|----------------|----------------|----------------|----------------|
| count      |       2.36e+06 |       2.36e+06 |       2.36e+06 |       2.36e+06 |
| mean       |      -8.46e-04 |      -8.51e-04 |      -5.45e-06 |      -1.75e-07 |
| std        |        31.1263 |        31.1265 |         0.0979 |         0.0031 |
| min        |    -14927.4960 |    -14927.4966 |       -61.0000 |        -1.9598 |
| 25%        |        -0.0196 |        -0.0196 |      -1.10e-09 |      -3.53e-11 |
| 50%        |      -6.95e-04 |      -6.94e-04 |      -1.28e-12 |      -4.11e-14 |
| 75%        |         0.0130 |         0.0130 |       1.09e-09 |       3.50e-11 |
| max        |     14925.0560 |     14925.0557 |        61.0000 |         1.9598 |

**Regression Analysis** (Python ~ Stata):

- **Model**: python = -0.0000 + 1.0000 * stata
- **R-squared**: 1.0000
- **N observations**: 2,360,216

| Coefficient |     Estimate |    Std Error | t-statistic |   p-value |
|-------------|--------------|--------------|-------------|----------|
| Intercept   |    -5.45e-06 |     6.37e-05 |     -0.0855 |     0.932 |
| Slope       |       1.0000 |     2.05e-06 | 488534.9625 |     0.000 |

**Missing Observations Sample**:
```
 index  permno  yyyymm  ChangeRoE
     0   19316  202412  -0.070941
```

**Feedback**:
- Num observations with std_diff >= TOL_DIFF_1: 99/2360216 (0.004%)
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
- Python: 3,297,084
- Common: 3,295,155

**Precision1**: 0.008% obs with std_diff >= 1.00e-02 (tolerance: < 10%)

**Precision2**: 99th percentile diff = 2.05e-07 (tolerance: < 1.00e+00)

**Summary Statistics** (Common Observations):

| Statistic  |          Stata |         Python |     Difference | Std Difference |
|------------|----------------|----------------|----------------|----------------|
| count      |       3.30e+06 |       3.30e+06 |       3.30e+06 |       3.30e+06 |
| mean       |         0.0019 |         0.0019 |      -2.37e-07 |      -2.37e-06 |
| std        |         0.0999 |         0.0999 |       4.29e-04 |         0.0043 |
| min        |        -1.8790 |        -1.8790 |        -0.2141 |        -2.1431 |
| 25%        |      -6.70e-06 |      -6.63e-06 |      -1.32e-12 |      -1.32e-11 |
| 50%        |         0.0000 |         0.0000 |         0.0000 |         0.0000 |
| 75%        |       2.58e-04 |       2.59e-04 |       1.35e-12 |       1.35e-11 |
| max        |         1.8457 |         1.8457 |         0.0605 |         0.6054 |

**Regression Analysis** (Python ~ Stata):

- **Model**: python = -0.0000 + 1.0000 * stata
- **R-squared**: 1.0000
- **N observations**: 3,295,155

| Coefficient |     Estimate |    Std Error | t-statistic |   p-value |
|-------------|--------------|--------------|-------------|----------|
| Intercept   |    -2.68e-07 |     2.36e-07 |     -1.1333 |     0.257 |
| Slope       |       1.0000 |     2.37e-06 | 422581.7802 |     0.000 |

**Feedback**:
- Num observations with std_diff >= TOL_DIFF_1: 264/3295155 (0.008%)
- Stata standard deviation: 9.99e-02

---

### DelayAcct

**Status**: ❌ FAILED

**Test Results**:
- Test 1 - Column names: ✅ PASSED
- Test 2 - Superset check: ❌ FAILED (Python missing 9051 Stata observations)
- Test 3 - Precision1 check: ❌ FAILED
- Test 4 - Precision2 check: ✅ PASSED

**Columns**: ['DelayAcct']

**Observations**:
- Stata:  674,090
- Python: 723,510
- Common: 665,039

**Precision1**: 89.487% obs with std_diff >= 1.00e-02 (tolerance: < 10%)

**Precision2**: 99th percentile diff = 6.15e-01 (tolerance: < 1.00e+00)

**Summary Statistics** (Common Observations):

| Statistic  |          Stata |         Python |     Difference | Std Difference |
|------------|----------------|----------------|----------------|----------------|
| count      |    665039.0000 |    665039.0000 |    665039.0000 |    665039.0000 |
| mean       |         0.1912 |         0.1932 |         0.0020 |         0.0210 |
| std        |         0.0958 |         0.0967 |         0.0160 |         0.1666 |
| min        |        -0.4104 |        -0.3776 |        -0.6145 |        -6.4119 |
| 25%        |         0.1116 |         0.1121 |        -0.0035 |        -0.0370 |
| 50%        |         0.1721 |         0.1755 |         0.0015 |         0.0158 |
| 75%        |         0.2701 |         0.2726 |         0.0072 |         0.0750 |
| max        |         1.3192 |         1.4278 |         0.6530 |         6.8130 |

**Regression Analysis** (Python ~ Stata):

- **Model**: python = 0.0030 + 0.9950 * stata
- **R-squared**: 0.9728
- **N observations**: 665,039

| Coefficient |     Estimate |    Std Error | t-statistic |   p-value |
|-------------|--------------|--------------|-------------|----------|
| Intercept   |       0.0030 |     4.37e-05 |     67.8178 |     0.000 |
| Slope       |       0.9950 |     2.04e-04 |   4873.6337 |     0.000 |

**Missing Observations Sample**:
```
 index  permno  yyyymm  DelayAcct
     0   10001  199311   0.336795
     1   10012  200208   0.207148
     2   10012  200209   0.217094
     3   10016  199805   0.390521
     4   10062  199311   0.366439
     5   10114  200306   0.405294
     6   10114  200307   0.400538
     7   10116  201508   0.121925
     8   10119  199706   0.367174
     9   10119  199707   0.350161
```

**Feedback**:
- Num observations with std_diff >= TOL_DIFF_1: 595126/665039 (89.487%)
- Stata standard deviation: 9.58e-02

**Most Recent Bad Observations**:
```
   permno  yyyymm    python     stata      diff
0   10026  202407  0.150854  0.155085 -0.004231
1   10028  202407  0.230718  0.220374  0.010344
2   10032  202407  0.141829  0.142951 -0.001122
3   10138  202407  0.163082  0.161488  0.001594
4   10158  202407  0.156650  0.158672 -0.002022
5   10200  202407  0.145193  0.144167  0.001025
6   10220  202407  0.170459  0.171523 -0.001065
7   10257  202407  0.222328  0.231531 -0.009203
8   10258  202407  0.148280  0.151306 -0.003026
9   10318  202407  0.139412  0.138319  0.001094
```

**Largest Differences**:
```
   permno  yyyymm    python     stata      diff
0   90285  201804  0.908272  0.255317  0.652955
1   85705  200706  0.793233  0.169225  0.624007
2   90285  201805  0.861148  0.242163  0.618985
3   87084  201508  0.335759  0.950278 -0.614519
4   87084  201507  0.308805  0.916879 -0.608074
5   90285  201711  0.782073  0.177341  0.604732
6   90285  201708  0.779079  0.190940  0.588138
7   87084  201510  0.215498  0.801547 -0.586049
8   87084  201511  0.231609  0.815343 -0.583734
9   87084  201509  0.204048  0.770471 -0.566423
```

---

### DelayNonAcct

**Status**: ❌ FAILED

**Test Results**:
- Test 1 - Column names: ✅ PASSED
- Test 2 - Superset check: ❌ FAILED (Python missing 9051 Stata observations)
- Test 3 - Precision1 check: ❌ FAILED
- Test 4 - Precision2 check: ✅ PASSED

**Columns**: ['DelayNonAcct']

**Observations**:
- Stata:  674,090
- Python: 723,510
- Common: 665,039

**Precision1**: 78.220% obs with std_diff >= 1.00e-02 (tolerance: < 10%)

**Precision2**: 99th percentile diff = 2.89e-01 (tolerance: < 1.00e+00)

**Summary Statistics** (Common Observations):

| Statistic  |          Stata |         Python |     Difference | Std Difference |
|------------|----------------|----------------|----------------|----------------|
| count      |    665039.0000 |    665039.0000 |    665039.0000 |    665039.0000 |
| mean       |      -7.96e-04 |        -0.0028 |        -0.0020 |        -0.0099 |
| std        |         0.2044 |         0.2043 |         0.0160 |         0.0783 |
| min        |        -0.7815 |        -0.8607 |        -0.6524 |        -3.1923 |
| 25%        |        -0.1140 |        -0.1156 |        -0.0072 |        -0.0352 |
| 50%        |        -0.0510 |        -0.0524 |        -0.0015 |        -0.0075 |
| 75%        |         0.0442 |         0.0420 |         0.0035 |         0.0174 |
| max        |         0.9457 |         0.9560 |         0.6150 |         3.0092 |

**Regression Analysis** (Python ~ Stata):

- **Model**: python = -0.0020 + 0.9966 * stata
- **R-squared**: 0.9939
- **N observations**: 665,039

| Coefficient |     Estimate |    Std Error | t-statistic |   p-value |
|-------------|--------------|--------------|-------------|----------|
| Intercept   |      -0.0020 |     1.96e-05 |   -102.8771 |     0.000 |
| Slope       |       0.9966 |     9.59e-05 |  10392.6002 |     0.000 |

**Missing Observations Sample**:
```
 index  permno  yyyymm  DelayNonAcct
     0   10001  199311      0.661581
     1   10012  200208     -0.166785
     2   10012  200209     -0.176730
     3   10016  199805      0.158209
     4   10062  199311      0.215670
     5   10114  200306     -0.267660
     6   10114  200307     -0.114482
     7   10116  201508      0.689750
     8   10119  199706     -0.277600
     9   10119  199707      0.003510
```

**Feedback**:
- Num observations with std_diff >= TOL_DIFF_1: 520194/665039 (78.220%)
- Stata standard deviation: 2.04e-01

**Most Recent Bad Observations**:
```
   permno  yyyymm    python     stata      diff
0   10026  202407  0.337480  0.333248  0.004232
1   10028  202407 -0.180375 -0.170063 -0.010312
2   10158  202407 -0.144593 -0.146786  0.002193
3   10257  202407  0.222467  0.213249  0.009218
4   10258  202407  0.053840  0.051251  0.002588
5   10382  202407 -0.020147 -0.033574  0.013427
6   10397  202407 -0.124998 -0.128800  0.003803
7   10516  202407  0.217879  0.219996 -0.002118
8   10517  202407 -0.179300 -0.191732  0.012432
9   10547  202407 -0.266692 -0.276424  0.009732
```

**Largest Differences**:
```
   permno  yyyymm    python     stata      diff
0   90285  201804 -0.742640 -0.090245 -0.652394
1   85705  200706  0.165988  0.790008 -0.624020
2   90285  201805 -0.695515 -0.077091 -0.618424
3   87084  201508 -0.166488 -0.781468  0.614980
4   87084  201507 -0.139534 -0.748070  0.608535
5   90285  201711 -0.616440 -0.012269 -0.604171
6   90285  201708 -0.613446 -0.025869 -0.587577
7   87084  201510 -0.046227 -0.632738  0.586510
8   87084  201511 -0.062338 -0.646533  0.584195
9   87084  201509 -0.034777 -0.601661  0.566884
```

---

### DivYield

**Status**: ❌ FAILED

**Test Results**:
- Test 1 - Column names: ✅ PASSED
- Test 2 - Superset check: ❌ FAILED (Python missing 1 Stata observations)
- Test 3 - Precision1 check: ✅ PASSED
- Test 4 - Precision2 check: ✅ PASSED

**Columns**: ['DivYield']

**Observations**:
- Stata:  421,384
- Python: 2,014,930
- Common: 421,383

**Precision1**: 0.007% obs with std_diff >= 1.00e-02 (tolerance: < 10%)

**Precision2**: 99th percentile diff = 1.24e-08 (tolerance: < 1.00e+00)

**Summary Statistics** (Common Observations):

| Statistic  |          Stata |         Python |     Difference | Std Difference |
|------------|----------------|----------------|----------------|----------------|
| count      |    421383.0000 |    421383.0000 |    421383.0000 |    421383.0000 |
| mean       |         0.0490 |         0.0490 |       4.91e-05 |       8.57e-05 |
| std        |         0.5731 |         0.5726 |         0.0269 |         0.0469 |
| min        |         0.0000 |         0.0000 |        -1.7481 |        -3.0501 |
| 25%        |         0.0201 |         0.0201 |      -1.01e-09 |      -1.77e-09 |
| 50%        |         0.0356 |         0.0356 |      -1.99e-11 |      -3.48e-11 |
| 75%        |         0.0554 |         0.0554 |       4.69e-10 |       8.19e-10 |
| max        |       154.9091 |       154.9091 |        13.8577 |        24.1787 |

**Regression Analysis** (Python ~ Stata):

- **Model**: python = 0.0001 + 0.9979 * stata
- **R-squared**: 0.9978
- **N observations**: 421,383

| Coefficient |     Estimate |    Std Error | t-statistic |   p-value |
|-------------|--------------|--------------|-------------|----------|
| Intercept   |     1.50e-04 |     4.15e-05 |      3.6065 |     0.000 |
| Slope       |       0.9979 |     7.22e-05 |  13830.8506 |     0.000 |

**Missing Observations Sample**:
```
 index  permno  yyyymm  DivYield
     0   21119  196012  0.031068
```

**Feedback**:
- Num observations with std_diff >= TOL_DIFF_1: 30/421383 (0.007%)
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

**Precision1**: 0.053% obs with std_diff >= 1.00e-02 (tolerance: < 10%)

**Precision2**: 99th percentile diff = 2.12e-08 (tolerance: < 1.00e+00)

**Summary Statistics** (Common Observations):

| Statistic  |          Stata |         Python |     Difference | Std Difference |
|------------|----------------|----------------|----------------|----------------|
| count      |       3.88e+06 |       3.88e+06 |       3.88e+06 |       3.88e+06 |
| mean       |         0.0239 |         0.0239 |       3.73e-05 |       1.80e-04 |
| std        |         0.2072 |         0.2076 |         0.0101 |         0.0488 |
| min        |        -0.5405 |        -0.5405 |        -1.5984 |        -7.7145 |
| 25%        |         0.0000 |         0.0000 |         0.0000 |         0.0000 |
| 50%        |         0.0000 |         0.0000 |         0.0000 |         0.0000 |
| 75%        |         0.0299 |         0.0299 |         0.0000 |         0.0000 |
| max        |        83.2000 |        83.2000 |         6.1759 |        29.8080 |

**Regression Analysis** (Python ~ Stata):

- **Model**: python = 0.0000 + 1.0008 * stata
- **R-squared**: 0.9976
- **N observations**: 3,878,713

| Coefficient |     Estimate |    Std Error | t-statistic |   p-value |
|-------------|--------------|--------------|-------------|----------|
| Intercept   |     1.90e-05 |     5.17e-06 |      3.6702 |     0.000 |
| Slope       |       1.0008 |     2.48e-05 |  40370.3962 |     0.000 |

**Feedback**:
- Num observations with std_diff >= TOL_DIFF_1: 2060/3878713 (0.053%)
- Stata standard deviation: 2.07e-01

---

### DownsideBeta

**Status**: ❌ FAILED

**Test Results**:
- Test 1 - Column names: ✅ PASSED
- Test 2 - Superset check: ❌ FAILED (Python missing 7 Stata observations)
- Test 3 - Precision1 check: ❌ FAILED
- Test 4 - Precision2 check: ✅ PASSED

**Columns**: ['DownsideBeta']

**Observations**:
- Stata:  4,848,559
- Python: 5,072,351
- Common: 4,848,552

**Precision1**: 19.351% obs with std_diff >= 1.00e-02 (tolerance: < 10%)

**Precision2**: 99th percentile diff = 1.74e-01 (tolerance: < 1.00e+00)

**Summary Statistics** (Common Observations):

| Statistic  |          Stata |         Python |     Difference | Std Difference |
|------------|----------------|----------------|----------------|----------------|
| count      |       4.85e+06 |       4.85e+06 |       4.85e+06 |       4.85e+06 |
| mean       |         0.8537 |         0.8543 |       6.00e-04 |       8.34e-04 |
| std        |         0.7191 |         0.7201 |         0.0530 |         0.0737 |
| min        |       -43.6149 |       -43.6034 |       -17.8849 |       -24.8725 |
| 25%        |         0.4076 |         0.4080 |      -6.43e-04 |      -8.95e-04 |
| 50%        |         0.8185 |         0.8190 |       9.52e-05 |       1.32e-04 |
| 75%        |         1.2309 |         1.2316 |         0.0012 |         0.0016 |
| max        |        16.0159 |        22.7108 |        22.2480 |        30.9402 |

**Regression Analysis** (Python ~ Stata):

- **Model**: python = 0.0017 + 0.9988 * stata
- **R-squared**: 0.9946
- **N observations**: 4,848,552

| Coefficient |     Estimate |    Std Error | t-statistic |   p-value |
|-------------|--------------|--------------|-------------|----------|
| Intercept   |       0.0017 |     3.73e-05 |     44.3783 |     0.000 |
| Slope       |       0.9988 |     3.35e-05 |  29855.7059 |     0.000 |

**Missing Observations Sample**:
```
 index  permno  yyyymm  DownsideBeta
     0   11746  192608      0.712000
     1   12909  192608      0.917963
     2   13127  192608      0.547239
     3   13629  192612      0.354627
     4   13960  192608     -1.756058
     5   18593  192608      0.171028
     6   33718  196310      0.944770
```

**Feedback**:
- Num observations with std_diff >= TOL_DIFF_1: 938264/4848552 (19.351%)
- Stata standard deviation: 7.19e-01

**Most Recent Bad Observations**:
```
   permno  yyyymm    python     stata      diff
0   16680  202412 -0.288771 -0.279329 -0.009443
1   19014  202412  1.500611  1.490741  0.009870
2   19066  202412  2.207404  2.217591 -0.010187
3   19146  202412  0.962848  0.955032  0.007816
4   19147  202412  3.032554  3.016006  0.016548
5   20292  202412  1.655575  1.647555  0.008019
6   20334  202412  1.157843  1.165704 -0.007861
7   20638  202412 -0.351702 -0.362992  0.011289
8   21114  202412  9.236139  9.247963 -0.011824
9   21539  202412  1.794273  1.785916  0.008357
```

**Largest Differences**:
```
   permno  yyyymm     python     stata       diff
0   11818  192608  19.061026 -3.186927  22.247954
1   11412  192608  22.710776  3.952252  18.758523
2   10815  192608  15.747186 -2.698489  18.445674
3   10583  192608 -15.932580  1.952304 -17.884885
4   11383  192609 -15.923443 -2.731694 -13.191749
5   14648  192608  15.302066  2.676733  12.625333
6   11818  192609   8.157301 -1.672886   9.830186
7   12714  192609   8.802288 -0.983153   9.785441
8   10655  192608  -8.780685  0.721612  -9.502297
9   10655  192612  -8.503854  0.846114  -9.349969
```

---

### EBM_q

**Status**: ❌ FAILED

**Test Results**:
- Test 1 - Column names: ✅ PASSED
- Test 2 - Superset check: ❌ FAILED (Python missing 89 Stata observations)
- Test 3 - Precision1 check: ✅ PASSED
- Test 4 - Precision2 check: ✅ PASSED

**Columns**: ['EBM_q']

**Observations**:
- Stata:  2,497,505
- Python: 2,497,530
- Common: 2,497,416

**Precision1**: 0.003% obs with std_diff >= 1.00e-02 (tolerance: < 10%)

**Precision2**: 99th percentile diff = 4.89e-08 (tolerance: < 1.00e+00)

**Summary Statistics** (Common Observations):

| Statistic  |          Stata |         Python |     Difference | Std Difference |
|------------|----------------|----------------|----------------|----------------|
| count      |       2.50e+06 |       2.50e+06 |       2.50e+06 |       2.50e+06 |
| mean       |         0.5320 |         0.5336 |         0.0016 |       7.71e-06 |
| std        |       210.6181 |       212.5570 |         2.5521 |         0.0121 |
| min        |   -135089.5600 |   -136046.0000 |      -956.4400 |        -4.5411 |
| 25%        |         0.1800 |         0.1800 |      -1.71e-08 |      -8.14e-11 |
| 50%        |         0.5004 |         0.5004 |      -1.01e-11 |      -4.81e-14 |
| 75%        |         0.9606 |         0.9606 |       1.71e-08 |       8.14e-11 |
| max        |    215285.7300 |    219000.0000 |      3714.2700 |        17.6351 |

**Regression Analysis** (Python ~ Stata):

- **Model**: python = -0.0033 + 1.0092 * stata
- **R-squared**: 0.9999
- **N observations**: 2,497,416

| Coefficient |     Estimate |    Std Error | t-statistic |   p-value |
|-------------|--------------|--------------|-------------|----------|
| Intercept   |      -0.0033 |       0.0011 |     -3.0868 |     0.002 |
| Slope       |       1.0092 |     5.01e-06 | 201493.0403 |     0.000 |

**Missing Observations Sample**:
```
 index  permno  yyyymm      EBM_q
     0   10515  199604   1.030155
     1   10515  199605   1.891978
     2   10515  199606   1.808921
     3   10872  199403   0.956019
     4   10872  199404   0.972510
     5   11545  199706   0.477123
     6   11545  199707   0.421310
     7   11545  199708   0.383889
     8   12113  200006   9.675225
     9   12113  200007 164.975690
```

**Feedback**:
- Num observations with std_diff >= TOL_DIFF_1: 63/2497416 (0.003%)
- Stata standard deviation: 2.11e+02

---

### EPq

**Status**: ❌ FAILED

**Test Results**:
- Test 1 - Column names: ✅ PASSED
- Test 2 - Superset check: ❌ FAILED (Python missing 58 Stata observations)
- Test 3 - Precision1 check: ✅ PASSED
- Test 4 - Precision2 check: ✅ PASSED

**Columns**: ['EPq']

**Observations**:
- Stata:  1,893,938
- Python: 1,893,955
- Common: 1,893,880

**Precision1**: 0.010% obs with std_diff >= 1.00e-02 (tolerance: < 10%)

**Precision2**: 99th percentile diff = 6.17e-08 (tolerance: < 1.00e+00)

**Summary Statistics** (Common Observations):

| Statistic  |          Stata |         Python |     Difference | Std Difference |
|------------|----------------|----------------|----------------|----------------|
| count      |       1.89e+06 |       1.89e+06 |       1.89e+06 |       1.89e+06 |
| mean       |         0.0273 |         0.0273 |       3.13e-06 |       3.13e-05 |
| std        |         0.1001 |         0.1002 |         0.0022 |         0.0223 |
| min        |         0.0000 |         0.0000 |        -0.0441 |        -0.4401 |
| 25%        |         0.0107 |         0.0107 |      -4.38e-10 |      -4.38e-09 |
| 50%        |         0.0180 |         0.0180 |         0.0000 |         0.0000 |
| 75%        |         0.0297 |         0.0297 |       4.39e-10 |       4.39e-09 |
| max        |        35.0386 |        35.0386 |         1.8565 |        18.5412 |

**Regression Analysis** (Python ~ Stata):

- **Model**: python = 0.0000 + 1.0000 * stata
- **R-squared**: 0.9995
- **N observations**: 1,893,880

| Coefficient |     Estimate |    Std Error | t-statistic |   p-value |
|-------------|--------------|--------------|-------------|----------|
| Intercept   |     3.37e-06 |     1.68e-06 |      2.0053 |     0.045 |
| Slope       |       1.0000 |     1.62e-05 |  61824.5581 |     0.000 |

**Missing Observations Sample**:
```
 index  permno  yyyymm      EPq
     0   10515  199604 0.005181
     1   10515  199605 0.005181
     2   10515  199606 0.005181
     3   11545  199706 0.014092
     4   11545  199707 0.014227
     5   11545  199708 0.014227
     6   11843  198803 0.040014
     7   11843  198804 0.081029
     8   11843  198805 0.055882
     9   12113  200006 0.076754
```

**Feedback**:
- Num observations with std_diff >= TOL_DIFF_1: 197/1893880 (0.010%)
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
- Python: 2,659,309
- Common: 2,657,230

**Precision1**: 0.026% obs with std_diff >= 1.00e-02 (tolerance: < 10%)

**Precision2**: 99th percentile diff = 1.17e-11 (tolerance: < 1.00e+00)

**Summary Statistics** (Common Observations):

| Statistic  |          Stata |         Python |     Difference | Std Difference |
|------------|----------------|----------------|----------------|----------------|
| count      |       2.66e+06 |       2.66e+06 |       2.66e+06 |       2.66e+06 |
| mean       |       200.8662 |       310.3177 |       109.4515 |         0.0011 |
| std        |     96619.4326 |    148863.3909 |     89150.5529 |         0.9227 |
| min        |      -2.82e+07 |      -7.90e+07 |      -7.13e+07 |      -738.0394 |
| 25%        |      -6.25e-04 |      -6.26e-04 |      -1.44e-10 |      -1.49e-15 |
| 50%        |         0.0000 |         0.0000 |        -0.0000 |        -0.0000 |
| 75%        |         0.0010 |         0.0010 |       1.45e-10 |       1.50e-15 |
| max        |       3.75e+07 |       5.07e+07 |       3.69e+07 |       381.9033 |

**Regression Analysis** (Python ~ Stata):

- **Model**: python = 56.9809 + 1.2612 * stata
- **R-squared**: 0.6701
- **N observations**: 2,657,230

| Coefficient |     Estimate |    Std Error | t-statistic |   p-value |
|-------------|--------------|--------------|-------------|----------|
| Intercept   |      56.9809 |      52.4529 |      1.0863 |     0.277 |
| Slope       |       1.2612 |     5.43e-04 |   2323.2053 |     0.000 |

**Feedback**:
- Num observations with std_diff >= TOL_DIFF_1: 689/2657230 (0.026%)
- Stata standard deviation: 9.66e+04

---

### EarningsConservatism

**Status**: ❌ FAILED

**Test Results**:
- Test 1 - Column names: ✅ PASSED
- Test 2 - Superset check: ❌ FAILED (Python missing 36945 Stata observations)
- Test 3 - Precision1 check: ✅ PASSED
- Test 4 - Precision2 check: ✅ PASSED

**Columns**: ['EarningsConservatism']

**Observations**:
- Stata:  1,467,671
- Python: 1,503,418
- Common: 1,430,726

**Precision1**: 3.563% obs with std_diff >= 1.00e-02 (tolerance: < 10%)

**Precision2**: 99th percentile diff = 6.39e-02 (tolerance: < 1.00e+00)

**Summary Statistics** (Common Observations):

| Statistic  |          Stata |         Python |     Difference | Std Difference |
|------------|----------------|----------------|----------------|----------------|
| count      |       1.43e+06 |       1.43e+06 |       1.43e+06 |       1.43e+06 |
| mean       |       -58.8950 |         0.2690 |        59.1640 |         0.0030 |
| std        |     19715.2905 |        36.3067 |     19714.2874 |         0.9999 |
| min        |      -6.48e+06 |      -100.0000 |   -872029.2500 |       -44.2311 |
| 25%        |        -5.1398 |        -5.1886 |      -1.17e-06 |      -5.91e-11 |
| 50%        |         0.9102 |         0.6719 |         0.0000 |         0.0000 |
| 75%        |         5.4525 |         5.5536 |       9.13e-07 |       4.63e-11 |
| max        |    872129.2500 |       100.0000 |       6.48e+06 |       328.6320 |

**Regression Analysis** (Python ~ Stata):

- **Model**: python = 0.2721 + 0.0001 * stata
- **R-squared**: 0.0008
- **N observations**: 1,430,726

| Coefficient |     Estimate |    Std Error | t-statistic |   p-value |
|-------------|--------------|--------------|-------------|----------|
| Intercept   |       0.2721 |       0.0303 |      8.9674 |     0.000 |
| Slope       |     5.26e-05 |     1.54e-06 |     34.1609 |     0.000 |

**Missing Observations Sample**:
```
 index  permno  yyyymm  EarningsConservatism
     0   10002  200306             -1.976701
     1   10002  200307             -1.976701
     2   10002  200308             -1.976701
     3   10002  200309             -1.976701
     4   10002  200310             -1.976701
     5   10002  200311             -1.976701
     6   10002  200312             -1.976701
     7   10002  200401             -1.976701
     8   10002  200402             -1.976701
     9   10002  200403             -1.976701
```

**Feedback**:
- Num observations with std_diff >= TOL_DIFF_1: 50971/1430726 (3.563%)
- Stata standard deviation: 1.97e+04

---

### EarningsPersistence

**Status**: ✅ PASSED

**Test Results**:
- Test 1 - Column names: ✅ PASSED
- Test 2 - Superset check: ✅ PASSED
- Test 3 - Precision1 check: ✅ PASSED
- Test 4 - Precision2 check: ✅ PASSED

**Columns**: ['EarningsPersistence']

**Observations**:
- Stata:  1,495,672
- Python: 1,554,071
- Common: 1,495,672

**Precision1**: 0.007% obs with std_diff >= 1.00e-02 (tolerance: < 10%)

**Precision2**: 99th percentile diff = 2.13e-07 (tolerance: < 1.00e+00)

**Summary Statistics** (Common Observations):

| Statistic  |          Stata |         Python |     Difference | Std Difference |
|------------|----------------|----------------|----------------|----------------|
| count      |       1.50e+06 |       1.50e+06 |       1.50e+06 |       1.50e+06 |
| mean       |         0.4579 |         0.4579 |      -1.18e-05 |      -1.96e-05 |
| std        |         0.5997 |         0.5997 |         0.0026 |         0.0044 |
| min        |      -119.0719 |      -119.0719 |        -0.7309 |        -1.2188 |
| 25%        |         0.1421 |         0.1421 |      -1.11e-08 |      -1.85e-08 |
| 50%        |         0.4517 |         0.4517 |      -5.28e-12 |      -8.80e-12 |
| 75%        |         0.7670 |         0.7670 |       1.08e-08 |       1.80e-08 |
| max        |        14.3520 |        14.3520 |         0.2564 |         0.4276 |

**Regression Analysis** (Python ~ Stata):

- **Model**: python = -0.0000 + 1.0000 * stata
- **R-squared**: 1.0000
- **N observations**: 1,495,672

| Coefficient |     Estimate |    Std Error | t-statistic |   p-value |
|-------------|--------------|--------------|-------------|----------|
| Intercept   |    -1.30e-05 |     2.70e-06 |     -4.8194 |     0.000 |
| Slope       |       1.0000 |     3.58e-06 | 279444.5075 |     0.000 |

**Feedback**:
- Num observations with std_diff >= TOL_DIFF_1: 99/1495672 (0.007%)
- Stata standard deviation: 6.00e-01

---

### EarningsPredictability

**Status**: ✅ PASSED

**Test Results**:
- Test 1 - Column names: ✅ PASSED
- Test 2 - Superset check: ✅ PASSED
- Test 3 - Precision1 check: ✅ PASSED
- Test 4 - Precision2 check: ✅ PASSED

**Columns**: ['EarningsPredictability']

**Observations**:
- Stata:  1,495,672
- Python: 1,554,071
- Common: 1,495,672

**Precision1**: 0.058% obs with std_diff >= 1.00e-02 (tolerance: < 10%)

**Precision2**: 99th percentile diff = 7.44e-10 (tolerance: < 1.00e+00)

**Summary Statistics** (Common Observations):

| Statistic  |          Stata |         Python |     Difference | Std Difference |
|------------|----------------|----------------|----------------|----------------|
| count      |       1.50e+06 |       1.50e+06 |       1.50e+06 |       1.50e+06 |
| mean       |       2.99e+11 |       1.27e+12 |       9.68e+11 |         0.0239 |
| std        |       4.05e+13 |       3.74e+14 |       3.39e+14 |         8.3667 |
| min        |         0.0000 |         0.0000 |      -7.45e+14 |       -18.3810 |
| 25%        |         0.0446 |         0.0356 |        -0.3570 |      -8.81e-15 |
| 50%        |         0.2784 |         0.2231 |        -0.0555 |      -1.37e-15 |
| 75%        |         1.7905 |         1.4394 |        -0.0088 |      -2.18e-16 |
| max        |       1.23e+16 |       1.32e+17 |       1.20e+17 |      2952.4210 |

**Regression Analysis** (Python ~ Stata):

- **Model**: python = -1164683045981.5442 + 8.1253 * stata
- **R-squared**: 0.7744
- **N observations**: 1,495,672

| Coefficient |     Estimate |    Std Error | t-statistic |   p-value |
|-------------|--------------|--------------|-------------|----------|
| Intercept   |    -1.16e+12 |     1.45e+11 |     -8.0166 |     0.000 |
| Slope       |       8.1253 |       0.0036 |   2265.9476 |     0.000 |

**Feedback**:
- Num observations with std_diff >= TOL_DIFF_1: 873/1495672 (0.058%)
- Stata standard deviation: 4.05e+13

---

### EarningsSmoothness

**Status**: ❌ FAILED

**Test Results**:
- Test 1 - Column names: ✅ PASSED
- Test 2 - Superset check: ❌ FAILED (Python missing 1482823 Stata observations)
- Test 3 - Precision1 check: ❌ FAILED
- Test 4 - Precision2 check: ❌ FAILED

**Columns**: ['EarningsSmoothness']

**Observations**:
- Stata:  1,482,823
- Python: 0
- Common: 0

**Missing Observations Sample**:
```
 index  permno  yyyymm  EarningsSmoothness
     0   10001  199612            0.529589
     1   10001  199701            0.529589
     2   10001  199702            0.529589
     3   10001  199703            0.529589
     4   10001  199704            0.529589
     5   10001  199705            0.529589
     6   10001  199706            0.529589
     7   10001  199707            0.529589
     8   10001  199708            0.529589
     9   10001  199709            0.529589
```

---

### EarningsTimeliness

**Status**: ❌ FAILED

**Test Results**:
- Test 1 - Column names: ✅ PASSED
- Test 2 - Superset check: ❌ FAILED (Python missing 36945 Stata observations)
- Test 3 - Precision1 check: ✅ PASSED
- Test 4 - Precision2 check: ✅ PASSED

**Columns**: ['EarningsTimeliness']

**Observations**:
- Stata:  1,467,923
- Python: 1,503,418
- Common: 1,430,978

**Precision1**: 0.002% obs with std_diff >= 1.00e-02 (tolerance: < 10%)

**Precision2**: 99th percentile diff = 4.76e-07 (tolerance: < 1.00e+00)

**Summary Statistics** (Common Observations):

| Statistic  |          Stata |         Python |     Difference | Std Difference |
|------------|----------------|----------------|----------------|----------------|
| count      |       1.43e+06 |       1.43e+06 |       1.43e+06 |       1.43e+06 |
| mean       |         0.3952 |         0.3952 |       4.08e-06 |       1.66e-05 |
| std        |         0.2458 |         0.2458 |         0.0013 |         0.0053 |
| min        |       6.46e-10 |       6.48e-10 |        -0.0101 |        -0.0409 |
| 25%        |         0.1933 |         0.1933 |      -1.34e-08 |      -5.46e-08 |
| 50%        |         0.3608 |         0.3608 |      -6.61e-11 |      -2.69e-10 |
| 75%        |         0.5729 |         0.5729 |       1.33e-08 |       5.40e-08 |
| max        |         1.0000 |         1.0000 |         0.4256 |         1.7318 |

**Regression Analysis** (Python ~ Stata):

- **Model**: python = 0.0000 + 1.0000 * stata
- **R-squared**: 1.0000
- **N observations**: 1,430,978

| Coefficient |     Estimate |    Std Error | t-statistic |   p-value |
|-------------|--------------|--------------|-------------|----------|
| Intercept   |     6.78e-06 |     2.06e-06 |      3.3005 |     0.001 |
| Slope       |       1.0000 |     4.42e-06 | 226368.9830 |     0.000 |

**Missing Observations Sample**:
```
 index  permno  yyyymm  EarningsTimeliness
     0   10002  200306            0.382373
     1   10002  200307            0.382373
     2   10002  200308            0.382373
     3   10002  200309            0.382373
     4   10002  200310            0.382373
     5   10002  200311            0.382373
     6   10002  200312            0.382373
     7   10002  200401            0.382373
     8   10002  200402            0.382373
     9   10002  200403            0.382373
```

**Feedback**:
- Num observations with std_diff >= TOL_DIFF_1: 27/1430978 (0.002%)
- Stata standard deviation: 2.46e-01

---

### EarningsValueRelevance

**Status**: ✅ PASSED

**Test Results**:
- Test 1 - Column names: ✅ PASSED
- Test 2 - Superset check: ✅ PASSED
- Test 3 - Precision1 check: ✅ PASSED
- Test 4 - Precision2 check: ✅ PASSED

**Columns**: ['EarningsValueRelevance']

**Observations**:
- Stata:  1,427,774
- Python: 1,503,418
- Common: 1,427,774

**Precision1**: 0.001% obs with std_diff >= 1.00e-02 (tolerance: < 10%)

**Precision2**: 99th percentile diff = 4.44e-07 (tolerance: < 1.00e+00)

**Summary Statistics** (Common Observations):

| Statistic  |          Stata |         Python |     Difference | Std Difference |
|------------|----------------|----------------|----------------|----------------|
| count      |       1.43e+06 |       1.43e+06 |       1.43e+06 |       1.43e+06 |
| mean       |         0.3224 |         0.3224 |       4.17e-07 |       1.95e-06 |
| std        |         0.2136 |         0.2136 |       1.36e-04 |       6.37e-04 |
| min        |       5.13e-06 |       5.13e-06 |      -3.86e-07 |      -1.81e-06 |
| 25%        |         0.1458 |         0.1458 |      -9.53e-09 |      -4.46e-08 |
| 50%        |         0.2926 |         0.2926 |       3.59e-11 |       1.68e-10 |
| 75%        |         0.4707 |         0.4707 |       9.68e-09 |       4.53e-08 |
| max        |         0.9929 |         0.9929 |         0.0671 |         0.3142 |

**Regression Analysis** (Python ~ Stata):

- **Model**: python = 0.0000 + 1.0000 * stata
- **R-squared**: 1.0000
- **N observations**: 1,427,774

| Coefficient |     Estimate |    Std Error | t-statistic |   p-value |
|-------------|--------------|--------------|-------------|----------|
| Intercept   |     9.40e-07 |     2.06e-07 |      4.5596 |     0.000 |
| Slope       |       1.0000 |     5.33e-07 |    1.88e+06 |     0.000 |

**Feedback**:
- Num observations with std_diff >= TOL_DIFF_1: 15/1427774 (0.001%)
- Stata standard deviation: 2.14e-01

---

### EntMult_q

**Status**: ❌ FAILED

**Test Results**:
- Test 1 - Column names: ✅ PASSED
- Test 2 - Superset check: ❌ FAILED (Python missing 143 Stata observations)
- Test 3 - Precision1 check: ✅ PASSED
- Test 4 - Precision2 check: ✅ PASSED

**Columns**: ['EntMult_q']

**Observations**:
- Stata:  1,689,737
- Python: 1,691,203
- Common: 1,689,594

**Precision1**: 0.006% obs with std_diff >= 1.00e-02 (tolerance: < 10%)

**Precision2**: 99th percentile diff = 6.40e-09 (tolerance: < 1.00e+00)

**Summary Statistics** (Common Observations):

| Statistic  |          Stata |         Python |     Difference | Std Difference |
|------------|----------------|----------------|----------------|----------------|
| count      |       1.69e+06 |       1.69e+06 |       1.69e+06 |       1.69e+06 |
| mean       |        87.8996 |        87.8864 |        -0.0131 |      -4.20e-06 |
| std        |      3126.4612 |      3126.4429 |        10.4351 |         0.0033 |
| min        |    -43431.7380 |    -43431.7391 |     -7731.1405 |        -2.4728 |
| 25%        |        20.2673 |        20.2677 |      -7.63e-07 |      -2.44e-10 |
| 50%        |        32.0422 |        32.0421 |      -2.84e-14 |      -9.09e-18 |
| 75%        |        51.5099 |        51.5106 |       7.53e-07 |       2.41e-10 |
| max        |       1.43e+06 |       1.43e+06 |       642.1284 |         0.2054 |

**Regression Analysis** (Python ~ Stata):

- **Model**: python = -0.0121 + 1.0000 * stata
- **R-squared**: 1.0000
- **N observations**: 1,689,594

| Coefficient |     Estimate |    Std Error | t-statistic |   p-value |
|-------------|--------------|--------------|-------------|----------|
| Intercept   |      -0.0121 |       0.0080 |     -1.5103 |     0.131 |
| Slope       |       1.0000 |     2.57e-06 | 389444.1430 |     0.000 |

**Missing Observations Sample**:
```
 index  permno  yyyymm  EntMult_q
     0   11545  199706  47.009804
     1   11545  199707  56.398899
     2   11545  199708  64.223152
     3   11843  198806  14.236789
     4   11843  198807  14.917392
     5   11843  198808  15.257691
     6   12373  202403  52.285816
     7   12373  202404  49.820324
     8   12373  202405  50.198395
     9   12750  198212 143.219590
```

**Feedback**:
- Num observations with std_diff >= TOL_DIFF_1: 106/1689594 (0.006%)
- Stata standard deviation: 3.13e+03

---

### FRbook

**Status**: ✅ PASSED

**Test Results**:
- Test 1 - Column names: ✅ PASSED
- Test 2 - Superset check: ✅ PASSED
- Test 3 - Precision1 check: ✅ PASSED
- Test 4 - Precision2 check: ✅ PASSED

**Columns**: ['FRbook']

**Observations**:
- Stata:  684,322
- Python: 684,322
- Common: 684,322

**Precision1**: 0.000% obs with std_diff >= 1.00e-02 (tolerance: < 10%)

**Precision2**: 99th percentile diff = 2.14e-07 (tolerance: < 1.00e+00)

**Summary Statistics** (Common Observations):

| Statistic  |          Stata |         Python |     Difference | Std Difference |
|------------|----------------|----------------|----------------|----------------|
| count      |    684322.0000 |    684322.0000 |    684322.0000 |    684322.0000 |
| mean       |        -0.0069 |        -0.0069 |      -1.55e-11 |      -1.29e-10 |
| std        |         0.1200 |         0.1200 |       1.52e-08 |       1.27e-07 |
| min        |       -39.0165 |       -39.0165 |      -5.02e-06 |      -4.18e-05 |
| 25%        |        -0.0158 |        -0.0158 |      -8.08e-10 |      -6.74e-09 |
| 50%        |        -0.0012 |        -0.0012 |         0.0000 |         0.0000 |
| 75%        |         0.0043 |         0.0043 |       8.16e-10 |       6.80e-09 |
| max        |         1.8105 |         1.8105 |       4.58e-07 |       3.82e-06 |

**Regression Analysis** (Python ~ Stata):

- **Model**: python = 0.0000 + 1.0000 * stata
- **R-squared**: 1.0000
- **N observations**: 684,322

| Coefficient |     Estimate |    Std Error | t-statistic |   p-value |
|-------------|--------------|--------------|-------------|----------|
| Intercept   |     6.65e-10 |     1.14e-11 |     58.1352 |     0.000 |
| Slope       |       1.0000 |     9.52e-11 |    1.05e+10 |     0.000 |

**Feedback**:
- Num observations with std_diff >= TOL_DIFF_1: 0/684322 (0.000%)
- Stata standard deviation: 1.20e-01

---

### FailureProbability

**Status**: ❌ FAILED

**Test Results**:
- Test 1 - Column names: ✅ PASSED
- Test 2 - Superset check: ❌ FAILED (Python missing 1 Stata observations)
- Test 3 - Precision1 check: ✅ PASSED
- Test 4 - Precision2 check: ✅ PASSED

**Columns**: ['FailureProbability']

**Observations**:
- Stata:  1,958,798
- Python: 2,420,936
- Common: 1,958,797

**Precision1**: 0.105% obs with std_diff >= 1.00e-02 (tolerance: < 10%)

**Precision2**: 99th percentile diff = 6.07e-08 (tolerance: < 1.00e+00)

**Summary Statistics** (Common Observations):

| Statistic  |          Stata |         Python |     Difference | Std Difference |
|------------|----------------|----------------|----------------|----------------|
| count      |       1.96e+06 |       1.96e+06 |       1.96e+06 |       1.96e+06 |
| mean       |       1.08e+06 |       1.09e+06 |     12405.6368 |       5.80e-04 |
| std        |       2.14e+07 |       4.97e+07 |       4.46e+07 |         2.0884 |
| min        |       -10.0057 |       -10.4365 |      -6.77e+08 |       -31.6501 |
| 25%        |        -5.9270 |        -5.9200 |        -0.0106 |      -4.97e-10 |
| 50%        |        -4.5351 |        -4.5382 |       3.95e-05 |       1.85e-12 |
| 75%        |        -2.0932 |        -2.1068 |         0.0198 |       9.28e-10 |
| max        |       6.77e+08 |       1.05e+10 |       9.83e+09 |       459.8210 |

**Regression Analysis** (Python ~ Stata):

- **Model**: python = -7605.8722 + 1.0185 * stata
- **R-squared**: 0.1922
- **N observations**: 1,958,797

| Coefficient |     Estimate |    Std Error | t-statistic |   p-value |
|-------------|--------------|--------------|-------------|----------|
| Intercept   |   -7605.8722 |   31940.5909 |     -0.2381 |     0.812 |
| Slope       |       1.0185 |       0.0015 |    682.6222 |     0.000 |

**Missing Observations Sample**:
```
 index  permno  yyyymm  FailureProbability
     0   19316  202412           -4.008925
```

**Feedback**:
- Num observations with std_diff >= TOL_DIFF_1: 2063/1958797 (0.105%)
- Stata standard deviation: 2.14e+07

---

### FailureProbabilityJune

**Status**: ❌ FAILED

**Test Results**:
- Test 1 - Column names: ✅ PASSED
- Test 2 - Superset check: ❌ FAILED (Python missing 1 Stata observations)
- Test 3 - Precision1 check: ✅ PASSED
- Test 4 - Precision2 check: ✅ PASSED

**Columns**: ['FailureProbabilityJune']

**Observations**:
- Stata:  2,090,935
- Python: 2,558,214
- Common: 2,090,934

**Precision1**: 0.206% obs with std_diff >= 1.00e-02 (tolerance: < 10%)

**Precision2**: 99th percentile diff = 1.70e-07 (tolerance: < 1.00e+00)

**Summary Statistics** (Common Observations):

| Statistic  |          Stata |         Python |     Difference | Std Difference |
|------------|----------------|----------------|----------------|----------------|
| count      |       2.09e+06 |       2.09e+06 |       2.09e+06 |       2.09e+06 |
| mean       |       1.03e+06 |       1.07e+06 |     38140.0838 |         0.0018 |
| std        |       2.07e+07 |       4.99e+07 |       4.52e+07 |         2.1840 |
| min        |        -9.7055 |        -9.7215 |      -6.77e+08 |       -32.6947 |
| 25%        |        -5.9385 |        -5.9355 |        -0.0147 |      -7.09e-10 |
| 50%        |        -4.5879 |        -4.5868 |       3.93e-05 |       1.90e-12 |
| 75%        |        -2.2170 |        -2.2136 |         0.0190 |       9.18e-10 |
| max        |       6.77e+08 |       1.05e+10 |       9.83e+09 |       474.9973 |

**Regression Analysis** (Python ~ Stata):

- **Model**: python = 16500.0690 + 1.0209 * stata
- **R-squared**: 0.1793
- **N observations**: 2,090,934

| Coefficient |     Estimate |    Std Error | t-statistic |   p-value |
|-------------|--------------|--------------|-------------|----------|
| Intercept   |   16500.0690 |   31295.8557 |      0.5272 |     0.598 |
| Slope       |       1.0209 |       0.0015 |    675.9849 |     0.000 |

**Missing Observations Sample**:
```
 index  permno  yyyymm  FailureProbabilityJune
     0   19316  202412               -3.903571
```

**Feedback**:
- Num observations with std_diff >= TOL_DIFF_1: 4317/2090934 (0.206%)
- Stata standard deviation: 2.07e+07

---

### ForecastDispersionLT

**Status**: ❌ FAILED

**Test Results**:
- Test 1 - Column names: ✅ PASSED
- Test 2 - Superset check: ❌ FAILED (Python missing 7604 Stata observations)
- Test 3 - Precision1 check: ✅ PASSED
- Test 4 - Precision2 check: ✅ PASSED

**Columns**: ['ForecastDispersionLT']

**Observations**:
- Stata:  828,578
- Python: 828,777
- Common: 820,974

**Precision1**: 0.085% obs with std_diff >= 1.00e-02 (tolerance: < 10%)

**Precision2**: 99th percentile diff = 1.49e-07 (tolerance: < 1.00e+00)

**Summary Statistics** (Common Observations):

| Statistic  |          Stata |         Python |     Difference | Std Difference |
|------------|----------------|----------------|----------------|----------------|
| count      |    820974.0000 |    820974.0000 |    820974.0000 |    820974.0000 |
| mean       |         4.5450 |         4.5450 |       5.39e-05 |       8.01e-06 |
| std        |         6.7258 |         6.7265 |         0.2252 |         0.0335 |
| min        |         0.0000 |         0.0000 |      -115.8600 |       -17.2262 |
| 25%        |         1.7200 |         1.7200 |         0.0000 |         0.0000 |
| 50%        |         3.0000 |         3.0000 |         0.0000 |         0.0000 |
| 75%        |         5.2000 |         5.2000 |       2.00e-08 |       2.97e-09 |
| max        |       623.7400 |       623.7400 |       115.8600 |        17.2262 |

**Regression Analysis** (Python ~ Stata):

- **Model**: python = 0.0021 + 0.9995 * stata
- **R-squared**: 0.9989
- **N observations**: 820,974

| Coefficient |     Estimate |    Std Error | t-statistic |   p-value |
|-------------|--------------|--------------|-------------|----------|
| Intercept   |       0.0021 |     3.00e-04 |      7.0081 |     0.000 |
| Slope       |       0.9995 |     3.69e-05 |  27054.3472 |     0.000 |

**Missing Observations Sample**:
```
 index  permno  yyyymm  ForecastDispersionLT
     0   10016  199805                  6.03
     1   10104  202412                  1.77
     2   10107  202412                  2.21
     3   10122  199711                  0.00
     4   10137  199709                  1.57
     5   10138  200012                  3.17
     6   10145  198403                  3.20
     7   10145  198404                  3.20
     8   10145  198405                  3.00
     9   10145  198406                  2.80
```

**Feedback**:
- Num observations with std_diff >= TOL_DIFF_1: 694/820974 (0.085%)
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
- Python: 3,299,086
- Common: 3,281,500

**Precision1**: 0.022% obs with std_diff >= 1.00e-02 (tolerance: < 10%)

**Precision2**: 99th percentile diff = 5.67e-08 (tolerance: < 1.00e+00)

**Summary Statistics** (Common Observations):

| Statistic  |          Stata |         Python |     Difference | Std Difference |
|------------|----------------|----------------|----------------|----------------|
| count      |       3.28e+06 |       3.28e+06 |       3.28e+06 |       3.28e+06 |
| mean       |         0.3420 |         0.3420 |      -6.35e-06 |      -5.60e-06 |
| std        |         1.1339 |         1.1339 |         0.0065 |         0.0057 |
| min        |       -28.7301 |       -28.7301 |        -2.7728 |        -2.4454 |
| 25%        |         0.0981 |         0.0981 |      -4.84e-09 |      -4.27e-09 |
| 50%        |         0.2774 |         0.2774 |         0.0000 |         0.0000 |
| 75%        |         0.4978 |         0.4978 |       4.90e-09 |       4.32e-09 |
| max        |       282.3216 |       282.3216 |         1.0171 |         0.8970 |

**Regression Analysis** (Python ~ Stata):

- **Model**: python = -0.0000 + 1.0000 * stata
- **R-squared**: 1.0000
- **N observations**: 3,281,500

| Coefficient |     Estimate |    Std Error | t-statistic |   p-value |
|-------------|--------------|--------------|-------------|----------|
| Intercept   |    -9.54e-07 |     3.74e-06 |     -0.2546 |     0.799 |
| Slope       |       1.0000 |     3.16e-06 | 316240.8335 |     0.000 |

**Feedback**:
- Num observations with std_diff >= TOL_DIFF_1: 720/3281500 (0.022%)
- Stata standard deviation: 1.13e+00

---

### GPlag_q

**Status**: ❌ FAILED

**Test Results**:
- Test 1 - Column names: ✅ PASSED
- Test 2 - Superset check: ❌ FAILED (Python missing 1 Stata observations)
- Test 3 - Precision1 check: ✅ PASSED
- Test 4 - Precision2 check: ✅ PASSED

**Columns**: ['GPlag_q']

**Observations**:
- Stata:  2,216,580
- Python: 2,482,785
- Common: 2,216,579

**Precision1**: 0.038% obs with std_diff >= 1.00e-02 (tolerance: < 10%)

**Precision2**: 99th percentile diff = 1.83e-08 (tolerance: < 1.00e+00)

**Summary Statistics** (Common Observations):

| Statistic  |          Stata |         Python |     Difference | Std Difference |
|------------|----------------|----------------|----------------|----------------|
| count      |       2.22e+06 |       2.22e+06 |       2.22e+06 |       2.22e+06 |
| mean       |         0.0808 |         0.0808 |       9.95e-06 |       1.40e-05 |
| std        |         0.7089 |         0.7089 |         0.0055 |         0.0077 |
| min        |        -9.0482 |        -9.0482 |        -0.5642 |        -0.7959 |
| 25%        |         0.0314 |         0.0314 |      -1.36e-09 |      -1.92e-09 |
| 50%        |         0.0731 |         0.0731 |         0.0000 |         0.0000 |
| 75%        |         0.1240 |         0.1240 |       1.36e-09 |       1.92e-09 |
| max        |       598.7442 |       598.7442 |         3.2404 |         4.5711 |

**Regression Analysis** (Python ~ Stata):

- **Model**: python = 0.0000 + 1.0000 * stata
- **R-squared**: 0.9999
- **N observations**: 2,216,579

| Coefficient |     Estimate |    Std Error | t-statistic |   p-value |
|-------------|--------------|--------------|-------------|----------|
| Intercept   |     1.01e-05 |     3.69e-06 |      2.7411 |     0.006 |
| Slope       |       1.0000 |     5.17e-06 | 193316.9874 |     0.000 |

**Missing Observations Sample**:
```
 index  permno  yyyymm  GPlag_q
     0   19316  202412 0.018425
```

**Feedback**:
- Num observations with std_diff >= TOL_DIFF_1: 835/2216579 (0.038%)
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
- Python: 3,237,974
- Common: 3,229,675

**Precision1**: 0.004% obs with std_diff >= 1.00e-02 (tolerance: < 10%)

**Precision2**: 99th percentile diff = 2.26e-09 (tolerance: < 1.00e+00)

**Summary Statistics** (Common Observations):

| Statistic  |          Stata |         Python |     Difference | Std Difference |
|------------|----------------|----------------|----------------|----------------|
| count      |       3.23e+06 |       3.23e+06 |       3.23e+06 |       3.23e+06 |
| mean       |        -1.0320 |            inf |            inf |            inf |
| std        |       213.3399 |            N/A |            N/A |            N/A |
| min        |    -90231.3050 |    -89952.2742 |        -4.6620 |        -0.0219 |
| 25%        |        -0.0941 |        -0.0941 |      -2.50e-08 |      -1.17e-10 |
| 50%        |        -0.0024 |        -0.0024 |         0.0000 |         0.0000 |
| 75%        |         0.0784 |         0.0784 |       2.49e-08 |       1.17e-10 |
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
- Num observations with std_diff >= TOL_DIFF_1: 120/3229675 (0.004%)
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
- Python: 3,172,213
- Common: 3,134,552

**Precision1**: 0.012% obs with std_diff >= 1.00e-02 (tolerance: < 10%)

**Precision2**: 99th percentile diff = 8.31e-10 (tolerance: < 1.00e+00)

**Summary Statistics** (Common Observations):

| Statistic  |          Stata |         Python |     Difference | Std Difference |
|------------|----------------|----------------|----------------|----------------|
| count      |       3.13e+06 |       3.13e+06 |       3.13e+06 |       3.13e+06 |
| mean       |        -0.7276 |        -0.7208 |         0.0068 |       2.50e-05 |
| std        |       272.2844 |       272.2685 |         2.4935 |         0.0092 |
| min        |    -93814.8910 |    -93814.8917 |      -122.8291 |        -0.4511 |
| 25%        |        -0.1435 |        -0.1436 |      -2.75e-09 |      -1.01e-11 |
| 50%        |         0.0056 |         0.0057 |       1.88e-12 |       6.92e-15 |
| 75%        |         0.1566 |         0.1568 |       2.77e-09 |       1.02e-11 |
| max        |     51770.8950 |     51770.8949 |      1176.6455 |         4.3214 |

**Regression Analysis** (Python ~ Stata):

- **Model**: python = 0.0067 + 0.9999 * stata
- **R-squared**: 0.9999
- **N observations**: 3,134,552

| Coefficient |     Estimate |    Std Error | t-statistic |   p-value |
|-------------|--------------|--------------|-------------|----------|
| Intercept   |       0.0067 |       0.0014 |      4.7854 |     0.000 |
| Slope       |       0.9999 |     5.17e-06 | 193322.5259 |     0.000 |

**Feedback**:
- Num observations with std_diff >= TOL_DIFF_1: 364/3134552 (0.012%)
- Stata standard deviation: 2.72e+02

---

### IdioVolCAPM

**Status**: ❌ FAILED

**Test Results**:
- Test 1 - Column names: ✅ PASSED
- Test 2 - Superset check: ❌ FAILED (Python missing 38931 Stata observations)
- Test 3 - Precision1 check: ✅ PASSED
- Test 4 - Precision2 check: ✅ PASSED

**Columns**: ['IdioVolCAPM']

**Observations**:
- Stata:  5,026,821
- Python: 4,987,890
- Common: 4,987,890

**Precision1**: 0.003% obs with std_diff >= 1.00e-02 (tolerance: < 10%)

**Precision2**: 99th percentile diff = 1.03e-03 (tolerance: < 1.00e+00)

**Summary Statistics** (Common Observations):

| Statistic  |          Stata |         Python |     Difference | Std Difference |
|------------|----------------|----------------|----------------|----------------|
| count      |       4.99e+06 |       4.99e+06 |       4.99e+06 |       4.99e+06 |
| mean       |         0.0273 |         0.0273 |      -1.47e-08 |      -4.86e-07 |
| std        |         0.0304 |         0.0304 |       8.55e-06 |       2.81e-04 |
| min        |         0.0000 |         0.0000 |        -0.0021 |        -0.0708 |
| 25%        |         0.0113 |         0.0113 |      -7.46e-07 |      -2.46e-05 |
| 50%        |         0.0195 |         0.0195 |      -3.47e-18 |      -1.14e-16 |
| 75%        |         0.0337 |         0.0337 |       4.90e-07 |       1.61e-05 |
| max        |         8.4129 |         8.4129 |         0.0020 |         0.0650 |

**Regression Analysis** (Python ~ Stata):

- **Model**: python = -0.0000 + 1.0000 * stata
- **R-squared**: 1.0000
- **N observations**: 4,987,890

| Coefficient |     Estimate |    Std Error | t-statistic |   p-value |
|-------------|--------------|--------------|-------------|----------|
| Intercept   |    -2.50e-09 |     5.14e-09 |     -0.4856 |     0.627 |
| Slope       |       1.0000 |     1.26e-07 |    7.93e+06 |     0.000 |

**Missing Observations Sample**:
```
 index  permno  yyyymm  IdioVolCAPM
     0   10000  198706     0.000000
     1   10001  201708     0.000898
     2   10002  201302     0.008657
     3   10003  198601     0.021412
     4   10003  199512     0.020168
     5   10004  198601     0.000000
     6   10005  198601     0.051636
     7   10005  199107     0.044184
     8   10007  198601     0.037836
     9   10007  199010     0.251540
```

**Feedback**:
- Num observations with std_diff >= TOL_DIFF_1: 152/4987890 (0.003%)
- Stata standard deviation: 3.04e-02

---

### IdioVolQF

**Status**: ❌ FAILED

**Test Results**:
- Test 1 - Column names: ✅ PASSED
- Test 2 - Superset check: ❌ FAILED (Python missing 30563 Stata observations)
- Test 3 - Precision1 check: ✅ PASSED
- Test 4 - Precision2 check: ✅ PASSED

**Columns**: ['IdioVolQF']

**Observations**:
- Stata:  3,986,461
- Python: 3,955,898
- Common: 3,955,898

**Precision1**: 0.000% obs with std_diff >= 1.00e-02 (tolerance: < 10%)

**Precision2**: 99th percentile diff = 3.43e-08 (tolerance: < 1.00e+00)

**Summary Statistics** (Common Observations):

| Statistic  |          Stata |         Python |     Difference | Std Difference |
|------------|----------------|----------------|----------------|----------------|
| count      |       3.96e+06 |       3.96e+06 |       3.96e+06 |       3.96e+06 |
| mean       |         0.0255 |         0.0255 |       2.86e-13 |       1.05e-11 |
| std        |         0.0273 |         0.0273 |       2.52e-10 |       9.25e-09 |
| min        |         0.0000 |         0.0000 |      -2.33e-08 |      -8.56e-07 |
| 25%        |         0.0106 |         0.0106 |      -6.46e-11 |      -2.37e-09 |
| 50%        |         0.0185 |         0.0185 |      -2.21e-20 |      -8.12e-19 |
| 75%        |         0.0316 |         0.0316 |       6.49e-11 |       2.38e-09 |
| max        |         3.4183 |         3.4183 |       6.27e-08 |       2.30e-06 |

**Regression Analysis** (Python ~ Stata):

- **Model**: python = -0.0000 + 1.0000 * stata
- **R-squared**: 1.0000
- **N observations**: 3,955,898

| Coefficient |     Estimate |    Std Error | t-statistic |   p-value |
|-------------|--------------|--------------|-------------|----------|
| Intercept   |    -3.50e-12 |     1.74e-13 |    -20.1372 |     0.000 |
| Slope       |       1.0000 |     4.65e-12 |    2.15e+11 |     0.000 |

**Missing Observations Sample**:
```
 index  permno  yyyymm    IdioVolQF
     0   10000  198706 5.849607e-19
     1   10002  201302 6.958739e-03
     2   10003  198601 1.861721e-02
     3   10003  199512 1.487973e-02
     4   10005  198601 4.759861e-02
     5   10005  199107 4.180065e-02
     6   10007  198601 2.829195e-02
     7   10007  199010 2.182299e-01
     8   10008  198601 1.745024e-02
     9   10009  198601 1.959985e-02
```

**Feedback**:
- Num observations with std_diff >= TOL_DIFF_1: 0/3955898 (0.000%)
- Stata standard deviation: 2.73e-02

---

### IntrinsicValue

**Status**: ❌ FAILED

**Test Results**:
- Test 1 - Column names: ✅ PASSED
- Test 2 - Superset check: ❌ FAILED (Python missing 8808 Stata observations)
- Test 3 - Precision1 check: ✅ PASSED
- Test 4 - Precision2 check: ✅ PASSED

**Columns**: ['IntrinsicValue']

**Observations**:
- Stata:  1,244,664
- Python: 1,301,064
- Common: 1,235,856

**Precision1**: 2.117% obs with std_diff >= 1.00e-02 (tolerance: < 10%)

**Precision2**: 99th percentile diff = 6.29e-02 (tolerance: < 1.00e+00)

**Summary Statistics** (Common Observations):

| Statistic  |          Stata |         Python |     Difference | Std Difference |
|------------|----------------|----------------|----------------|----------------|
| count      |       1.24e+06 |       1.24e+06 |       1.24e+06 |       1.24e+06 |
| mean       |         0.4657 |         0.4687 |         0.0031 |         0.0024 |
| std        |         1.2614 |         1.2678 |         0.0671 |         0.0532 |
| min        |       -51.3084 |       -51.3084 |        -2.7533 |        -2.1827 |
| 25%        |         0.0526 |         0.0527 |      -3.20e-08 |      -2.54e-08 |
| 50%        |         0.4591 |         0.4607 |      -4.83e-09 |      -3.83e-09 |
| 75%        |         0.7858 |         0.7888 |       1.58e-08 |       1.25e-08 |
| max        |        47.5224 |        47.5224 |         9.8992 |         7.8476 |

**Regression Analysis** (Python ~ Stata):

- **Model**: python = 0.0014 + 1.0036 * stata
- **R-squared**: 0.9972
- **N observations**: 1,235,856

| Coefficient |     Estimate |    Std Error | t-statistic |   p-value |
|-------------|--------------|--------------|-------------|----------|
| Intercept   |       0.0014 |     6.42e-05 |     21.7505 |     0.000 |
| Slope       |       1.0036 |     4.77e-05 |  21022.2773 |     0.000 |

**Missing Observations Sample**:
```
 index  permno  yyyymm  IntrinsicValue
     0   10145  197606         0.94617
     1   10145  197607         0.94617
     2   10145  197608         0.94617
     3   10145  197609         0.94617
     4   10145  197610         0.94617
     5   10145  197611         0.94617
     6   10145  197612         0.94617
     7   10145  197701         0.94617
     8   10145  197702         0.94617
     9   10145  197703         0.94617
```

**Feedback**:
- Num observations with std_diff >= TOL_DIFF_1: 26160/1235856 (2.117%)
- Stata standard deviation: 1.26e+00

---

### KZ

**Status**: ✅ PASSED

**Test Results**:
- Test 1 - Column names: ✅ PASSED
- Test 2 - Superset check: ✅ PASSED
- Test 3 - Precision1 check: ✅ PASSED
- Test 4 - Precision2 check: ✅ PASSED

**Columns**: ['KZ']

**Observations**:
- Stata:  2,630,499
- Python: 2,663,113
- Common: 2,630,499

**Precision1**: 0.000% obs with std_diff >= 1.00e-02 (tolerance: < 10%)

**Precision2**: 99th percentile diff = 2.06e-09 (tolerance: < 1.00e+00)

**Summary Statistics** (Common Observations):

| Statistic  |          Stata |         Python |     Difference | Std Difference |
|------------|----------------|----------------|----------------|----------------|
| count      |       2.63e+06 |       2.63e+06 |       2.63e+06 |       2.63e+06 |
| mean       |       -34.2550 |       -34.2551 |      -8.85e-05 |      -2.84e-08 |
| std        |      3118.1767 |      3118.1767 |         0.0395 |       1.27e-05 |
| min        |      -1.23e+06 |      -1.23e+06 |       -19.2429 |        -0.0062 |
| 25%        |        -5.2581 |        -5.2582 |      -4.30e-08 |      -1.38e-11 |
| 50%        |        -0.6982 |        -0.6982 |       2.30e-11 |       7.37e-15 |
| 75%        |         1.0179 |         1.0179 |       4.29e-08 |       1.37e-11 |
| max        |    205925.8400 |    205925.8463 |         3.3978 |         0.0011 |

**Regression Analysis** (Python ~ Stata):

- **Model**: python = -0.0001 + 1.0000 * stata
- **R-squared**: 1.0000
- **N observations**: 2,630,499

| Coefficient |     Estimate |    Std Error | t-statistic |   p-value |
|-------------|--------------|--------------|-------------|----------|
| Intercept   |    -8.84e-05 |     2.43e-05 |     -3.6340 |     0.000 |
| Slope       |       1.0000 |     7.80e-09 |    1.28e+08 |     0.000 |

**Feedback**:
- Num observations with std_diff >= TOL_DIFF_1: 0/2630499 (0.000%)
- Stata standard deviation: 3.12e+03

---

### KZ_q

**Status**: ❌ FAILED

**Test Results**:
- Test 1 - Column names: ✅ PASSED
- Test 2 - Superset check: ❌ FAILED (Python missing 258 Stata observations)
- Test 3 - Precision1 check: ✅ PASSED
- Test 4 - Precision2 check: ✅ PASSED

**Columns**: ['KZ_q']

**Observations**:
- Stata:  1,936,942
- Python: 1,940,673
- Common: 1,936,684

**Precision1**: 0.001% obs with std_diff >= 1.00e-02 (tolerance: < 10%)

**Precision2**: 99th percentile diff = 3.35e-09 (tolerance: < 1.00e+00)

**Summary Statistics** (Common Observations):

| Statistic  |          Stata |         Python |     Difference | Std Difference |
|------------|----------------|----------------|----------------|----------------|
| count      |       1.94e+06 |       1.94e+06 |       1.94e+06 |       1.94e+06 |
| mean       |       -26.0718 |       -26.0729 |        -0.0012 |      -6.56e-07 |
| std        |      1776.1967 |      1776.1966 |         0.6689 |       3.77e-04 |
| min        |      -1.23e+06 |      -1.23e+06 |      -794.1236 |        -0.4471 |
| 25%        |        -4.8599 |        -4.8603 |      -4.19e-08 |      -2.36e-11 |
| 50%        |        -0.2485 |        -0.2485 |      -2.62e-11 |      -1.48e-14 |
| 75%        |         1.2951 |         1.2951 |       4.17e-08 |       2.35e-11 |
| max        |     26732.3870 |     26732.3858 |        15.1278 |         0.0085 |

**Regression Analysis** (Python ~ Stata):

- **Model**: python = -0.0012 + 1.0000 * stata
- **R-squared**: 1.0000
- **N observations**: 1,936,684

| Coefficient |     Estimate |    Std Error | t-statistic |   p-value |
|-------------|--------------|--------------|-------------|----------|
| Intercept   |      -0.0012 |     4.81e-04 |     -2.4301 |     0.015 |
| Slope       |       1.0000 |     2.71e-07 |    3.70e+06 |     0.000 |

**Missing Observations Sample**:
```
 index  permno  yyyymm      KZ_q
     0   10515  199604 -4.790903
     1   10515  199605 -4.929575
     2   10515  199606 -4.921965
     3   10872  199403  4.016939
     4   10872  199404  4.020635
     5   10986  199008  8.309092
     6   11122  199503 -1.456571
     7   11122  199504 -1.620262
     8   11122  199505 -1.456571
     9   11212  199008 -1.955831
```

**Feedback**:
- Num observations with std_diff >= TOL_DIFF_1: 19/1936684 (0.001%)
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
- Python: 2,990,300
- Common: 2,974,260

**Precision1**: 0.002% obs with std_diff >= 1.00e-02 (tolerance: < 10%)

**Precision2**: 99th percentile diff = 4.32e-09 (tolerance: < 1.00e+00)

**Summary Statistics** (Common Observations):

| Statistic  |          Stata |         Python |     Difference | Std Difference |
|------------|----------------|----------------|----------------|----------------|
| count      |       2.97e+06 |       2.97e+06 |       2.97e+06 |       2.97e+06 |
| mean       |         0.5044 |         0.5043 |      -3.75e-05 |      -1.02e-06 |
| std        |        36.7045 |        36.7045 |         0.0230 |       6.26e-04 |
| min        |      -247.4286 |      -247.4286 |        -9.9206 |        -0.2703 |
| 25%        |        -0.0439 |        -0.0440 |      -2.63e-08 |      -7.15e-10 |
| 50%        |         0.0510 |         0.0510 |         0.0000 |         0.0000 |
| 75%        |         0.1598 |         0.1598 |       2.63e-08 |       7.16e-10 |
| max        |     11615.4880 |     11615.4889 |         3.4648 |         0.0944 |

**Regression Analysis** (Python ~ Stata):

- **Model**: python = -0.0000 + 1.0000 * stata
- **R-squared**: 1.0000
- **N observations**: 2,974,260

| Coefficient |     Estimate |    Std Error | t-statistic |   p-value |
|-------------|--------------|--------------|-------------|----------|
| Intercept   |    -3.73e-05 |     1.33e-05 |     -2.8038 |     0.005 |
| Slope       |       1.0000 |     3.63e-07 |    2.76e+06 |     0.000 |

**Feedback**:
- Num observations with std_diff >= TOL_DIFF_1: 60/2974260 (0.002%)
- Stata standard deviation: 3.67e+01

---

### Leverage_q

**Status**: ❌ FAILED

**Test Results**:
- Test 1 - Column names: ✅ PASSED
- Test 2 - Superset check: ❌ FAILED (Python missing 83 Stata observations)
- Test 3 - Precision1 check: ✅ PASSED
- Test 4 - Precision2 check: ✅ PASSED

**Columns**: ['Leverage_q']

**Observations**:
- Stata:  2,571,833
- Python: 2,571,823
- Common: 2,571,750

**Precision1**: 0.000% obs with std_diff >= 1.00e-02 (tolerance: < 10%)

**Precision2**: 99th percentile diff = 5.75e-08 (tolerance: < 1.00e+00)

**Summary Statistics** (Common Observations):

| Statistic  |          Stata |         Python |     Difference | Std Difference |
|------------|----------------|----------------|----------------|----------------|
| count      |       2.57e+06 |       2.57e+06 |       2.57e+06 |       2.57e+06 |
| mean       |         2.8298 |         2.8298 |       4.45e-07 |       2.38e-08 |
| std        |        18.6726 |        18.6726 |       5.80e-04 |       3.10e-05 |
| min        |       -11.0632 |       -11.0632 |        -0.2401 |        -0.0129 |
| 25%        |         0.2307 |         0.2307 |      -1.51e-08 |      -8.07e-10 |
| 50%        |         0.6768 |         0.6768 |         0.0000 |         0.0000 |
| 75%        |         2.0022 |         2.0022 |       1.50e-08 |       8.06e-10 |
| max        |      8843.3477 |      8843.3470 |         0.6649 |         0.0356 |

**Regression Analysis** (Python ~ Stata):

- **Model**: python = 0.0000 + 1.0000 * stata
- **R-squared**: 1.0000
- **N observations**: 2,571,750

| Coefficient |     Estimate |    Std Error | t-statistic |   p-value |
|-------------|--------------|--------------|-------------|----------|
| Intercept   |     4.49e-07 |     3.66e-07 |      1.2290 |     0.219 |
| Slope       |       1.0000 |     1.94e-08 |    5.17e+07 |     0.000 |

**Missing Observations Sample**:
```
 index  permno  yyyymm  Leverage_q
     0   10515  199604    0.207634
     1   10515  199605    0.534574
     2   10515  199606    0.492051
     3   10872  199403   23.655371
     4   10872  199404   17.741528
     5   11545  199706    0.042305
     6   11545  199707    0.036492
     7   11545  199708    0.032743
     8   12113  200006    1.927242
     9   12113  200007    2.380712
```

**Feedback**:
- Num observations with std_diff >= TOL_DIFF_1: 4/2571750 (0.000%)
- Stata standard deviation: 1.87e+01

---

### NetDebtPrice_q

**Status**: ❌ FAILED

**Test Results**:
- Test 1 - Column names: ✅ PASSED
- Test 2 - Superset check: ❌ FAILED (Python missing 90 Stata observations)
- Test 3 - Precision1 check: ✅ PASSED
- Test 4 - Precision2 check: ✅ PASSED

**Columns**: ['NetDebtPrice_q']

**Observations**:
- Stata:  1,178,409
- Python: 1,220,292
- Common: 1,178,319

**Precision1**: 0.001% obs with std_diff >= 1.00e-02 (tolerance: < 10%)

**Precision2**: 99th percentile diff = 6.40e-08 (tolerance: < 1.00e+00)

**Summary Statistics** (Common Observations):

| Statistic  |          Stata |         Python |     Difference | Std Difference |
|------------|----------------|----------------|----------------|----------------|
| count      |       1.18e+06 |       1.18e+06 |       1.18e+06 |       1.18e+06 |
| mean       |         1.0138 |         1.0138 |       1.26e-06 |       1.83e-07 |
| std        |         6.8788 |         6.8788 |       3.38e-04 |       4.91e-05 |
| min        |      -142.3929 |      -142.3930 |        -0.0642 |        -0.0093 |
| 25%        |        -0.0768 |        -0.0768 |      -1.03e-08 |      -1.50e-09 |
| 50%        |         0.2984 |         0.2984 |      -1.12e-12 |      -1.62e-13 |
| 75%        |         0.9501 |         0.9501 |       1.03e-08 |       1.50e-09 |
| max        |      2492.7185 |      2492.7184 |         0.1154 |         0.0168 |

**Regression Analysis** (Python ~ Stata):

- **Model**: python = 0.0000 + 1.0000 * stata
- **R-squared**: 1.0000
- **N observations**: 1,178,319

| Coefficient |     Estimate |    Std Error | t-statistic |   p-value |
|-------------|--------------|--------------|-------------|----------|
| Intercept   |     1.34e-06 |     3.15e-07 |      4.2533 |     0.000 |
| Slope       |       1.0000 |     4.53e-08 |    2.21e+07 |     0.000 |

**Missing Observations Sample**:
```
 index  permno  yyyymm  NetDebtPrice_q
     0   10515  199604       -0.342635
     1   10515  199605       -0.882147
     2   10515  199606       -0.811976
     3   12113  200006        0.797657
     4   12113  200007        0.985341
     5   12113  200008        0.523462
     6   12837  198004        0.438865
     7   15268  202412       -3.077925
     8   15381  201705       -0.152520
     9   15381  201801       -0.398268
```

**Feedback**:
- Num observations with std_diff >= TOL_DIFF_1: 11/1178319 (0.001%)
- Stata standard deviation: 6.88e+00

---

### NetPayoutYield_q

**Status**: ❌ FAILED

**Test Results**:
- Test 1 - Column names: ✅ PASSED
- Test 2 - Superset check: ❌ FAILED (Python missing 1 Stata observations)
- Test 3 - Precision1 check: ✅ PASSED
- Test 4 - Precision2 check: ✅ PASSED

**Columns**: ['NetPayoutYield_q']

**Observations**:
- Stata:  2,520,037
- Python: 2,622,235
- Common: 2,520,036

**Precision1**: 0.042% obs with std_diff >= 1.00e-02 (tolerance: < 10%)

**Precision2**: 99th percentile diff = 4.91e-08 (tolerance: < 1.00e+00)

**Summary Statistics** (Common Observations):

| Statistic  |          Stata |         Python |     Difference | Std Difference |
|------------|----------------|----------------|----------------|----------------|
| count      |       2.52e+06 |       2.52e+06 |       2.52e+06 |       2.52e+06 |
| mean       |         0.0042 |         0.0042 |       5.37e-06 |       1.77e-05 |
| std        |         0.3030 |         0.3030 |         0.0023 |         0.0076 |
| min        |      -193.6226 |      -193.6226 |        -0.9269 |        -3.0591 |
| 25%        |      -1.53e-04 |      -1.53e-04 |      -7.90e-11 |      -2.61e-10 |
| 50%        |         0.0000 |         0.0000 |         0.0000 |         0.0000 |
| 75%        |         0.0100 |         0.0100 |       8.07e-11 |       2.66e-10 |
| max        |       195.8306 |       195.8306 |         1.2332 |         4.0699 |

**Regression Analysis** (Python ~ Stata):

- **Model**: python = 0.0000 + 1.0000 * stata
- **R-squared**: 0.9999
- **N observations**: 2,520,036

| Coefficient |     Estimate |    Std Error | t-statistic |   p-value |
|-------------|--------------|--------------|-------------|----------|
| Intercept   |     5.41e-06 |     1.46e-06 |      3.7149 |     0.000 |
| Slope       |       1.0000 |     4.80e-06 | 208119.2325 |     0.000 |

**Missing Observations Sample**:
```
 index  permno  yyyymm  NetPayoutYield_q
     0   19316  202412          0.012858
```

**Feedback**:
- Num observations with std_diff >= TOL_DIFF_1: 1059/2520036 (0.042%)
- Stata standard deviation: 3.03e-01

---

### OPLeverage_q

**Status**: ❌ FAILED

**Test Results**:
- Test 1 - Column names: ✅ PASSED
- Test 2 - Superset check: ❌ FAILED (Python missing 94 Stata observations)
- Test 3 - Precision1 check: ✅ PASSED
- Test 4 - Precision2 check: ✅ PASSED

**Columns**: ['OPLeverage_q']

**Observations**:
- Stata:  2,546,734
- Python: 2,546,791
- Common: 2,546,640

**Precision1**: 0.034% obs with std_diff >= 1.00e-02 (tolerance: < 10%)

**Precision2**: 99th percentile diff = 8.07e-08 (tolerance: < 1.00e+00)

**Summary Statistics** (Common Observations):

| Statistic  |          Stata |         Python |     Difference | Std Difference |
|------------|----------------|----------------|----------------|----------------|
| count      |       2.55e+06 |       2.55e+06 |       2.55e+06 |       2.55e+06 |
| mean       |         0.2547 |         0.2547 |       2.52e-06 |       5.22e-06 |
| std        |         0.4836 |         0.4836 |         0.0063 |         0.0131 |
| min        |        -1.4798 |        -1.4798 |        -1.0265 |        -2.1227 |
| 25%        |         0.0824 |         0.0824 |      -3.42e-09 |      -7.07e-09 |
| 50%        |         0.1983 |         0.1983 |      -2.14e-12 |      -4.42e-12 |
| 75%        |         0.3378 |         0.3378 |       3.40e-09 |       7.04e-09 |
| max        |       280.5029 |       280.5029 |         3.8251 |         7.9099 |

**Regression Analysis** (Python ~ Stata):

- **Model**: python = 0.0000 + 1.0000 * stata
- **R-squared**: 0.9998
- **N observations**: 2,546,640

| Coefficient |     Estimate |    Std Error | t-statistic |   p-value |
|-------------|--------------|--------------|-------------|----------|
| Intercept   |     2.44e-06 |     4.49e-06 |      0.5447 |     0.586 |
| Slope       |       1.0000 |     8.21e-06 | 121768.0759 |     0.000 |

**Missing Observations Sample**:
```
 index  permno  yyyymm  OPLeverage_q
     0   10515  199604      0.205151
     1   10515  199605      0.205151
     2   10515  199606      0.205151
     3   10872  199403      0.108935
     4   10872  199404      0.108935
     5   11545  199706      0.157832
     6   11545  199707      0.157832
     7   11545  199708      0.157832
     8   12113  200006      0.443489
     9   12113  200007      0.443489
```

**Feedback**:
- Num observations with std_diff >= TOL_DIFF_1: 860/2546640 (0.034%)
- Stata standard deviation: 4.84e-01

---

### OScore_q

**Status**: ❌ FAILED

**Test Results**:
- Test 1 - Column names: ✅ PASSED
- Test 2 - Superset check: ❌ FAILED (Python missing 5820 Stata observations)
- Test 3 - Precision1 check: ✅ PASSED
- Test 4 - Precision2 check: ✅ PASSED

**Columns**: ['OScore_q']

**Observations**:
- Stata:  877,922
- Python: 1,177,521
- Common: 872,102

**Precision1**: 0.000% obs with std_diff >= 1.00e-02 (tolerance: < 10%)

**Precision2**: 99th percentile diff = 0.00e+00 (tolerance: < 1.00e+00)

**Summary Statistics** (Common Observations):

| Statistic  |          Stata |         Python |     Difference | Std Difference |
|------------|----------------|----------------|----------------|----------------|
| count      |    872102.0000 |    872102.0000 |    872102.0000 |    872102.0000 |
| mean       |         0.1194 |         0.1194 |         0.0000 |         0.0000 |
| std        |         0.3243 |         0.3243 |         0.0000 |         0.0000 |
| min        |         0.0000 |         0.0000 |         0.0000 |         0.0000 |
| 25%        |         0.0000 |         0.0000 |         0.0000 |         0.0000 |
| 50%        |         0.0000 |         0.0000 |         0.0000 |         0.0000 |
| 75%        |         0.0000 |         0.0000 |         0.0000 |         0.0000 |
| max        |         1.0000 |         1.0000 |         0.0000 |         0.0000 |

**Regression Analysis** (Python ~ Stata):

- **Model**: python = -0.0000 + 1.0000 * stata
- **R-squared**: 1.0000
- **N observations**: 872,102

| Coefficient |     Estimate |    Std Error | t-statistic |   p-value |
|-------------|--------------|--------------|-------------|----------|
| Intercept   |    -8.20e-14 |     2.64e-16 |   -311.0990 |     0.000 |
| Slope       |       1.0000 |     7.63e-16 |    1.31e+15 |     0.000 |

**Missing Observations Sample**:
```
 index  permno  yyyymm  OScore_q
     0   10010  199501       1.0
     1   10012  199002       1.0
     2   10012  199207       1.0
     3   10012  199302       1.0
     4   10012  199303       1.0
     5   10015  198511       1.0
     6   10025  199601       1.0
     7   10025  199607       1.0
     8   10025  199608       1.0
     9   10028  199902       1.0
```

**Feedback**:
- Num observations with std_diff >= TOL_DIFF_1: 0/872102 (0.000%)
- Stata standard deviation: 3.24e-01

---

### OperProfLag

**Status**: ✅ PASSED

**Test Results**:
- Test 1 - Column names: ✅ PASSED
- Test 2 - Superset check: ✅ PASSED
- Test 3 - Precision1 check: ✅ PASSED
- Test 4 - Precision2 check: ✅ PASSED

**Columns**: ['OperProfLag']

**Observations**:
- Stata:  1,292,263
- Python: 1,826,388
- Common: 1,292,263

**Precision1**: 0.005% obs with std_diff >= 1.00e-02 (tolerance: < 10%)

**Precision2**: 99th percentile diff = 1.47e-08 (tolerance: < 1.00e+00)

**Summary Statistics** (Common Observations):

| Statistic  |          Stata |         Python |     Difference | Std Difference |
|------------|----------------|----------------|----------------|----------------|
| count      |       1.29e+06 |       1.29e+06 |       1.29e+06 |       1.29e+06 |
| mean       |         0.2732 |         0.2732 |       5.34e-07 |       7.64e-08 |
| std        |         6.9919 |         6.9919 |         0.0013 |       1.84e-04 |
| min        |     -1594.7000 |     -1594.7000 |        -0.3447 |        -0.0493 |
| 25%        |         0.1432 |         0.1432 |      -5.76e-09 |      -8.24e-10 |
| 50%        |         0.2805 |         0.2805 |       5.55e-16 |       7.94e-17 |
| 75%        |         0.4266 |         0.4266 |       5.79e-09 |       8.28e-10 |
| max        |      1096.4845 |      1096.4845 |         0.3904 |         0.0558 |

**Regression Analysis** (Python ~ Stata):

- **Model**: python = 0.0000 + 1.0000 * stata
- **R-squared**: 1.0000
- **N observations**: 1,292,263

| Coefficient |     Estimate |    Std Error | t-statistic |   p-value |
|-------------|--------------|--------------|-------------|----------|
| Intercept   |     6.14e-07 |     1.13e-06 |      0.5424 |     0.588 |
| Slope       |       1.0000 |     1.62e-07 |    6.18e+06 |     0.000 |

**Feedback**:
- Num observations with std_diff >= TOL_DIFF_1: 60/1292263 (0.005%)
- Stata standard deviation: 6.99e+00

---

### OperProfLag_q

**Status**: ❌ FAILED

**Test Results**:
- Test 1 - Column names: ✅ PASSED
- Test 2 - Superset check: ❌ FAILED (Python missing 1 Stata observations)
- Test 3 - Precision1 check: ✅ PASSED
- Test 4 - Precision2 check: ✅ PASSED

**Columns**: ['OperProfLag_q']

**Observations**:
- Stata:  2,395,707
- Python: 2,579,765
- Common: 2,395,706

**Precision1**: 0.001% obs with std_diff >= 1.00e-02 (tolerance: < 10%)

**Precision2**: 99th percentile diff = 1.15e-05 (tolerance: < 1.00e+00)

**Summary Statistics** (Common Observations):

| Statistic  |          Stata |         Python |     Difference | Std Difference |
|------------|----------------|----------------|----------------|----------------|
| count      |       2.40e+06 |       2.40e+06 |       2.40e+06 |       2.40e+06 |
| mean       |       -70.1479 |            N/A |            N/A |            N/A |
| std        |    252624.5665 |            N/A |            N/A |            N/A |
| min        |      -3.48e+08 |           -inf |           -inf |           -inf |
| 25%        |        -0.0048 |        -0.0273 |      -2.71e-08 |      -1.07e-13 |
| 50%        |         0.0444 |         0.0372 |      -2.29e-09 |      -9.06e-15 |
| 75%        |         0.0849 |         0.0767 |       4.61e-09 |       1.83e-14 |
| max        |       9.52e+07 |            inf |            inf |            inf |

**Regression Analysis** (Python ~ Stata):

- **Model**: python = nan + nan * stata
- **R-squared**: nan
- **N observations**: 2,395,706

| Coefficient |     Estimate |    Std Error | t-statistic |   p-value |
|-------------|--------------|--------------|-------------|----------|
| Intercept   |          nan |          nan |         nan |       nan |
| Slope       |          nan |          nan |         nan |       nan |

**Missing Observations Sample**:
```
 index  permno  yyyymm  OperProfLag_q
     0   19316  202412      -0.021109
```

**Feedback**:
- Num observations with std_diff >= TOL_DIFF_1: 30/2395706 (0.001%)
- Stata standard deviation: 2.53e+05

---

### OperProfRDLagAT

**Status**: ✅ PASSED

**Test Results**:
- Test 1 - Column names: ✅ PASSED
- Test 2 - Superset check: ✅ PASSED
- Test 3 - Precision1 check: ✅ PASSED
- Test 4 - Precision2 check: ✅ PASSED

**Columns**: ['OperProfRDLagAT']

**Observations**:
- Stata:  2,742,767
- Python: 2,949,448
- Common: 2,742,767

**Precision1**: 4.550% obs with std_diff >= 1.00e-02 (tolerance: < 10%)

**Precision2**: 99th percentile diff = 8.21e-02 (tolerance: < 1.00e+00)

**Summary Statistics** (Common Observations):

| Statistic  |          Stata |         Python |     Difference | Std Difference |
|------------|----------------|----------------|----------------|----------------|
| count      |       2.74e+06 |       2.74e+06 |       2.74e+06 |       2.74e+06 |
| mean       |         0.1294 |         0.1345 |         0.0051 |         0.0043 |
| std        |         1.1878 |         1.1902 |         0.0736 |         0.0620 |
| min        |      -200.7273 |      -200.7273 |        -1.6015 |        -1.3483 |
| 25%        |         0.0319 |         0.0327 |      -2.15e-09 |      -1.81e-09 |
| 50%        |         0.1281 |         0.1303 |       3.09e-10 |       2.60e-10 |
| 75%        |         0.2154 |         0.2198 |       4.70e-09 |       3.96e-09 |
| max        |       226.5365 |       226.5365 |         6.8470 |         5.7642 |

**Regression Analysis** (Python ~ Stata):

- **Model**: python = 0.0051 + 1.0001 * stata
- **R-squared**: 0.9962
- **N observations**: 2,742,767

| Coefficient |     Estimate |    Std Error | t-statistic |   p-value |
|-------------|--------------|--------------|-------------|----------|
| Intercept   |       0.0051 |     4.47e-05 |    113.7673 |     0.000 |
| Slope       |       1.0001 |     3.74e-05 |  26725.3208 |     0.000 |

**Feedback**:
- Num observations with std_diff >= TOL_DIFF_1: 124794/2742767 (4.550%)
- Stata standard deviation: 1.19e+00

---

### OperProfRDLagAT_q

**Status**: ❌ FAILED

**Test Results**:
- Test 1 - Column names: ✅ PASSED
- Test 2 - Superset check: ❌ FAILED (Python missing 166 Stata observations)
- Test 3 - Precision1 check: ✅ PASSED
- Test 4 - Precision2 check: ✅ PASSED

**Columns**: ['OperProfRDLagAT_q']

**Observations**:
- Stata:  1,800,025
- Python: 1,800,118
- Common: 1,799,859

**Precision1**: 0.050% obs with std_diff >= 1.00e-02 (tolerance: < 10%)

**Precision2**: 99th percentile diff = 6.78e-08 (tolerance: < 1.00e+00)

**Summary Statistics** (Common Observations):

| Statistic  |          Stata |         Python |     Difference | Std Difference |
|------------|----------------|----------------|----------------|----------------|
| count      |       1.80e+06 |       1.80e+06 |       1.80e+06 |       1.80e+06 |
| mean       |         0.0249 |         0.0250 |       6.88e-06 |       5.22e-05 |
| std        |         0.1317 |         0.1317 |         0.0031 |         0.0234 |
| min        |       -10.0000 |       -10.0000 |        -0.4027 |        -3.0572 |
| 25%        |         0.0110 |         0.0110 |      -7.25e-10 |      -5.50e-09 |
| 50%        |         0.0317 |         0.0317 |         0.0000 |         0.0000 |
| 75%        |         0.0522 |         0.0522 |       7.23e-10 |       5.49e-09 |
| max        |        54.3953 |        54.3953 |         1.8353 |        13.9346 |

**Regression Analysis** (Python ~ Stata):

- **Model**: python = 0.0000 + 0.9997 * stata
- **R-squared**: 0.9995
- **N observations**: 1,799,859

| Coefficient |     Estimate |    Std Error | t-statistic |   p-value |
|-------------|--------------|--------------|-------------|----------|
| Intercept   |     1.41e-05 |     2.34e-06 |      6.0347 |     0.000 |
| Slope       |       0.9997 |     1.74e-05 |  57299.3876 |     0.000 |

**Missing Observations Sample**:
```
 index  permno  yyyymm  OperProfRDLagAT_q
     0   10515  199607           0.007740
     1   10515  199608           0.007740
     2   10515  199609           0.007740
     3   10517  202006           0.168328
     4   10517  202007           0.168328
     5   10517  202008           0.168328
     6   10517  202009           0.160288
     7   10517  202010           0.160288
     8   10517  202011           0.160288
     9   10517  202012           0.194064
```

**Feedback**:
- Num observations with std_diff >= TOL_DIFF_1: 907/1799859 (0.050%)
- Stata standard deviation: 1.32e-01

---

### OrgCapNoAdj

**Status**: ❌ FAILED

**Test Results**:
- Test 1 - Column names: ✅ PASSED
- Test 2 - Superset check: ❌ FAILED (Python missing 25478 Stata observations)
- Test 3 - Precision1 check: ✅ PASSED
- Test 4 - Precision2 check: ✅ PASSED

**Columns**: ['OrgCapNoAdj']

**Observations**:
- Stata:  1,243,418
- Python: 1,249,255
- Common: 1,217,940

**Precision1**: 0.022% obs with std_diff >= 1.00e-02 (tolerance: < 10%)

**Precision2**: 99th percentile diff = 3.02e-05 (tolerance: < 1.00e+00)

**Summary Statistics** (Common Observations):

| Statistic  |          Stata |         Python |     Difference | Std Difference |
|------------|----------------|----------------|----------------|----------------|
| count      |       1.22e+06 |       1.22e+06 |       1.22e+06 |       1.22e+06 |
| mean       |         2.6133 |         2.6132 |      -7.88e-05 |      -8.68e-06 |
| std        |         9.0762 |         9.0761 |         0.0277 |         0.0030 |
| min        |        -5.4577 |        -5.4577 |       -17.0922 |        -1.8832 |
| 25%        |         0.7044 |         0.7043 |      -7.19e-08 |      -7.93e-09 |
| 50%        |         1.6586 |         1.6587 |      -1.31e-09 |      -1.44e-10 |
| 75%        |         3.3211 |         3.3211 |       5.06e-08 |       5.58e-09 |
| max        |      3861.9792 |      3861.9793 |         5.7057 |         0.6286 |

**Regression Analysis** (Python ~ Stata):

- **Model**: python = -0.0000 + 1.0000 * stata
- **R-squared**: 1.0000
- **N observations**: 1,217,940

| Coefficient |     Estimate |    Std Error | t-statistic |   p-value |
|-------------|--------------|--------------|-------------|----------|
| Intercept   |    -2.95e-05 |     2.61e-05 |     -1.1300 |     0.258 |
| Slope       |       1.0000 |     2.76e-06 | 361865.7815 |     0.000 |

**Missing Observations Sample**:
```
 index  permno  yyyymm  OrgCapNoAdj
     0   10286  198806     1.863002
     1   10286  198807     1.844594
     2   10286  198808     1.844594
     3   10286  198809     1.844594
     4   10286  198810     1.822256
     5   10286  198811     1.822256
     6   10286  198812     1.822256
     7   10286  198901     1.805611
     8   10286  198902     1.805611
     9   10286  198903     1.805611
```

**Feedback**:
- Num observations with std_diff >= TOL_DIFF_1: 270/1217940 (0.022%)
- Stata standard deviation: 9.08e+00

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
- Python: 3,618,531
- Common: 3,547,773

**Precision1**: 0.000% obs with std_diff >= 1.00e-02 (tolerance: < 10%)

**Precision2**: 99th percentile diff = 2.35e-09 (tolerance: < 1.00e+00)

**Summary Statistics** (Common Observations):

| Statistic  |          Stata |         Python |     Difference | Std Difference |
|------------|----------------|----------------|----------------|----------------|
| count      |       3.55e+06 |       3.55e+06 |       3.55e+06 |       3.55e+06 |
| mean       |        -4.0283 |        -4.0283 |       1.20e-05 |       5.66e-08 |
| std        |       211.9918 |       211.9919 |         0.0059 |       2.79e-05 |
| min        |    -84221.6640 |    -84221.6667 |        -0.1893 |      -8.93e-04 |
| 25%        |        -0.0177 |        -0.0177 |      -1.41e-09 |      -6.64e-12 |
| 50%        |         0.0398 |         0.0398 |         0.0000 |         0.0000 |
| 75%        |         0.0957 |         0.0957 |       1.42e-09 |       6.69e-12 |
| max        |     10418.0800 |     10418.0800 |         3.1361 |         0.0148 |

**Regression Analysis** (Python ~ Stata):

- **Model**: python = 0.0000 + 1.0000 * stata
- **R-squared**: 1.0000
- **N observations**: 3,547,773

| Coefficient |     Estimate |    Std Error | t-statistic |   p-value |
|-------------|--------------|--------------|-------------|----------|
| Intercept   |     1.21e-05 |     3.14e-06 |      3.8447 |     0.000 |
| Slope       |       1.0000 |     1.48e-08 |    6.75e+07 |     0.000 |

**Feedback**:
- Num observations with std_diff >= TOL_DIFF_1: 12/3547773 (0.000%)
- Stata standard deviation: 2.12e+02

---

### PM_q

**Status**: ❌ FAILED

**Test Results**:
- Test 1 - Column names: ✅ PASSED
- Test 2 - Superset check: ❌ FAILED (Python missing 1 Stata observations)
- Test 3 - Precision1 check: ✅ PASSED
- Test 4 - Precision2 check: ✅ PASSED

**Columns**: ['PM_q']

**Observations**:
- Stata:  2,492,083
- Python: 2,823,485
- Common: 2,492,082

**Precision1**: 0.005% obs with std_diff >= 1.00e-02 (tolerance: < 10%)

**Precision2**: 99th percentile diff = 3.05e-09 (tolerance: < 1.00e+00)

**Summary Statistics** (Common Observations):

| Statistic  |          Stata |         Python |     Difference | Std Difference |
|------------|----------------|----------------|----------------|----------------|
| count      |       2.49e+06 |       2.49e+06 |       2.49e+06 |       2.49e+06 |
| mean       |        -3.9606 |        -4.3942 |        -0.4336 |        -0.0025 |
| std        |       171.1246 |       262.2484 |       198.8954 |         1.1623 |
| min        |    -64982.0000 |   -183220.0000 |   -183147.0040 |     -1070.2553 |
| 25%        |        -0.0250 |        -0.0250 |      -1.28e-09 |      -7.51e-12 |
| 50%        |         0.0340 |         0.0340 |         0.0000 |         0.0000 |
| 75%        |         0.0816 |         0.0816 |       1.28e-09 |       7.46e-12 |
| max        |     18403.0000 |     28930.0000 |     28930.3781 |       169.0603 |

**Regression Analysis** (Python ~ Stata):

- **Model**: python = -0.4382 + 0.9988 * stata
- **R-squared**: 0.4248
- **N observations**: 2,492,082

| Coefficient |     Estimate |    Std Error | t-statistic |   p-value |
|-------------|--------------|--------------|-------------|----------|
| Intercept   |      -0.4382 |       0.1260 |     -3.4773 |     0.001 |
| Slope       |       0.9988 |     7.36e-04 |   1356.6210 |     0.000 |

**Missing Observations Sample**:
```
 index  permno  yyyymm      PM_q
     0   19316  202412 -0.461944
```

**Feedback**:
- Num observations with std_diff >= TOL_DIFF_1: 123/2492082 (0.005%)
- Stata standard deviation: 1.71e+02

---

### PS_q

**Status**: ❌ FAILED

**Test Results**:
- Test 1 - Column names: ✅ PASSED
- Test 2 - Superset check: ❌ FAILED (Python missing 32 Stata observations)
- Test 3 - Precision1 check: ❌ FAILED
- Test 4 - Precision2 check: ❌ FAILED

**Columns**: ['PS_q']

**Observations**:
- Stata:  310,650
- Python: 371,800
- Common: 310,618

**Precision1**: 53.366% obs with std_diff >= 1.00e-02 (tolerance: < 10%)

**Precision2**: 99th percentile diff = 3.16e+00 (tolerance: < 1.00e+00)

**Summary Statistics** (Common Observations):

| Statistic  |          Stata |         Python |     Difference | Std Difference |
|------------|----------------|----------------|----------------|----------------|
| count      |    310618.0000 |    310618.0000 |    310618.0000 |    310618.0000 |
| mean       |         5.2218 |         4.7228 |        -0.4989 |        -0.3156 |
| std        |         1.5810 |         1.7964 |         1.5061 |         0.9526 |
| min        |         1.0000 |         1.0000 |        -7.0000 |        -4.4275 |
| 25%        |         4.0000 |         3.0000 |        -1.0000 |        -0.6325 |
| 50%        |         5.0000 |         5.0000 |         0.0000 |         0.0000 |
| 75%        |         6.0000 |         6.0000 |         0.0000 |         0.0000 |
| max        |         9.0000 |         9.0000 |         2.0000 |         1.2650 |

**Regression Analysis** (Python ~ Stata):

- **Model**: python = 1.1108 + 0.6917 * stata
- **R-squared**: 0.3706
- **N observations**: 310,618

| Coefficient |     Estimate |    Std Error | t-statistic |   p-value |
|-------------|--------------|--------------|-------------|----------|
| Intercept   |       1.1108 |       0.0088 |    125.8808 |     0.000 |
| Slope       |       0.6917 |       0.0016 |    427.7072 |     0.000 |

**Missing Observations Sample**:
```
 index  permno  yyyymm  PS_q
     0   10515  199604   5.0
     1   10515  199605   6.0
     2   10515  199606   6.0
     3   10872  199403   7.0
     4   10872  199404   7.0
     5   18244  199608   5.0
     6   19316  202412   6.0
     7   19483  202310   4.0
     8   19483  202311   4.0
     9   20637  202407   6.0
```

**Feedback**:
- Num observations with std_diff >= TOL_DIFF_1: 165763/310618 (53.366%)
- Stata standard deviation: 1.58e+00

**Most Recent Bad Observations**:
```
   permno  yyyymm  python  stata  diff
0   11174  202412     2.0    3.0  -1.0
1   11593  202412     8.0    7.0   1.0
2   11701  202412     5.0    6.0  -1.0
3   11775  202412     6.0    7.0  -1.0
4   11790  202412     4.0    5.0  -1.0
5   12880  202412     5.0    6.0  -1.0
6   13116  202412     6.0    5.0   1.0
7   13124  202412     6.0    5.0   1.0
8   13337  202412     4.0    5.0  -1.0
9   13583  202412     3.0    8.0  -5.0
```

**Largest Differences**:
```
   permno  yyyymm  python  stata  diff
0   11843  198806     1.0    8.0  -7.0
1   93129  201103     1.0    8.0  -7.0
2   93129  201104     1.0    8.0  -7.0
3   93129  201105     1.0    8.0  -7.0
4   10005  198706     1.0    7.0  -6.0
5   10005  198707     1.0    7.0  -6.0
6   10005  198708     1.0    7.0  -6.0
7   10005  198709     1.0    7.0  -6.0
8   10005  198710     1.0    7.0  -6.0
9   10005  198711     1.0    7.0  -6.0
```

---

### PayoutYield_q

**Status**: ✅ PASSED

**Test Results**:
- Test 1 - Column names: ✅ PASSED
- Test 2 - Superset check: ✅ PASSED
- Test 3 - Precision1 check: ✅ PASSED
- Test 4 - Precision2 check: ✅ PASSED

**Columns**: ['PayoutYield_q']

**Observations**:
- Stata:  1,310,000
- Python: 2,903,425
- Common: 1,310,000

**Precision1**: 0.064% obs with std_diff >= 1.00e-02 (tolerance: < 10%)

**Precision2**: 99th percentile diff = 4.41e-08 (tolerance: < 1.00e+00)

**Summary Statistics** (Common Observations):

| Statistic  |          Stata |         Python |     Difference | Std Difference |
|------------|----------------|----------------|----------------|----------------|
| count      |       1.31e+06 |       1.31e+06 |       1.31e+06 |       1.31e+06 |
| mean       |         0.0309 |         0.0309 |       9.60e-06 |       2.79e-05 |
| std        |         0.3442 |         0.3442 |       9.98e-04 |         0.0029 |
| min        |       1.15e-17 |      -2.10e-16 |        -0.2764 |        -0.8031 |
| 25%        |         0.0045 |         0.0045 |      -2.96e-10 |      -8.60e-10 |
| 50%        |         0.0106 |         0.0106 |      -2.09e-13 |      -6.08e-13 |
| 75%        |         0.0230 |         0.0231 |       2.97e-10 |       8.63e-10 |
| max        |       217.7060 |       217.7060 |         0.3391 |         0.9851 |

**Regression Analysis** (Python ~ Stata):

- **Model**: python = 0.0000 + 1.0000 * stata
- **R-squared**: 1.0000
- **N observations**: 1,310,000

| Coefficient |     Estimate |    Std Error | t-statistic |   p-value |
|-------------|--------------|--------------|-------------|----------|
| Intercept   |     9.56e-06 |     8.76e-07 |     10.9184 |     0.000 |
| Slope       |       1.0000 |     2.53e-06 | 394698.2846 |     0.000 |

**Feedback**:
- Num observations with std_diff >= TOL_DIFF_1: 832/1310000 (0.064%)
- Stata standard deviation: 3.44e-01

---

### RD_q

**Status**: ✅ PASSED

**Test Results**:
- Test 1 - Column names: ✅ PASSED
- Test 2 - Superset check: ✅ PASSED
- Test 3 - Precision1 check: ✅ PASSED
- Test 4 - Precision2 check: ✅ PASSED

**Columns**: ['RD_q']

**Observations**:
- Stata:  833,583
- Python: 3,038,238
- Common: 833,583

**Precision1**: 0.024% obs with std_diff >= 1.00e-02 (tolerance: < 10%)

**Precision2**: 99th percentile diff = 6.84e-08 (tolerance: < 1.00e+00)

**Summary Statistics** (Common Observations):

| Statistic  |          Stata |         Python |     Difference | Std Difference |
|------------|----------------|----------------|----------------|----------------|
| count      |    833583.0000 |    833583.0000 |    833583.0000 |    833583.0000 |
| mean       |         0.0298 |         0.0298 |      -7.40e-06 |      -4.47e-05 |
| std        |         0.1656 |         0.1656 |         0.0022 |         0.0133 |
| min        |        -1.5270 |        -1.5270 |        -1.2894 |        -7.7861 |
| 25%        |         0.0024 |         0.0024 |      -2.18e-10 |      -1.32e-09 |
| 50%        |         0.0105 |         0.0105 |         0.0000 |         0.0000 |
| 75%        |         0.0278 |         0.0278 |       2.15e-10 |       1.30e-09 |
| max        |        98.7289 |        98.7289 |         0.2419 |         1.4604 |

**Regression Analysis** (Python ~ Stata):

- **Model**: python = -0.0000 + 0.9998 * stata
- **R-squared**: 0.9998
- **N observations**: 833,583

| Coefficient |     Estimate |    Std Error | t-statistic |   p-value |
|-------------|--------------|--------------|-------------|----------|
| Intercept   |    -8.95e-07 |     2.45e-06 |     -0.3652 |     0.715 |
| Slope       |       0.9998 |     1.46e-05 |  68608.9887 |     0.000 |

**Feedback**:
- Num observations with std_diff >= TOL_DIFF_1: 197/833583 (0.024%)
- Stata standard deviation: 1.66e-01

---

### ResidualMomentum6m

**Status**: ✅ PASSED

**Test Results**:
- Test 1 - Column names: ✅ PASSED
- Test 2 - Superset check: ✅ PASSED
- Test 3 - Precision1 check: ✅ PASSED
- Test 4 - Precision2 check: ✅ PASSED

**Columns**: ['ResidualMomentum6m']

**Observations**:
- Stata:  3,601,405
- Python: 3,601,799
- Common: 3,601,405

**Precision1**: 0.926% obs with std_diff >= 1.00e-02 (tolerance: < 10%)

**Precision2**: 99th percentile diff = 9.58e-03 (tolerance: < 1.00e+00)

**Summary Statistics** (Common Observations):

| Statistic  |          Stata |         Python |     Difference | Std Difference |
|------------|----------------|----------------|----------------|----------------|
| count      |       3.60e+06 |       3.60e+06 |       3.60e+06 |       3.60e+06 |
| mean       |        -0.0597 |        -0.0597 |       5.99e-05 |       1.17e-04 |
| std        |         0.5125 |         0.5125 |         0.0014 |         0.0027 |
| min        |       -12.3925 |       -12.3887 |        -0.2201 |        -0.4294 |
| 25%        |        -0.3366 |        -0.3366 |      -3.16e-08 |      -6.17e-08 |
| 50%        |        -0.0296 |        -0.0296 |      -2.64e-09 |      -5.14e-09 |
| 75%        |         0.2494 |         0.2495 |       1.76e-08 |       3.43e-08 |
| max        |        35.4630 |        35.4663 |         0.2783 |         0.5429 |

**Regression Analysis** (Python ~ Stata):

- **Model**: python = 0.0001 + 1.0000 * stata
- **R-squared**: 1.0000
- **N observations**: 3,601,405

| Coefficient |     Estimate |    Std Error | t-statistic |   p-value |
|-------------|--------------|--------------|-------------|----------|
| Intercept   |     6.02e-05 |     7.28e-07 |     82.7564 |     0.000 |
| Slope       |       1.0000 |     1.41e-06 | 708806.2205 |     0.000 |

**Feedback**:
- Num observations with std_diff >= TOL_DIFF_1: 33366/3601405 (0.926%)
- Stata standard deviation: 5.13e-01

---

### RetNOA

**Status**: ✅ PASSED

**Test Results**:
- Test 1 - Column names: ✅ PASSED
- Test 2 - Superset check: ✅ PASSED
- Test 3 - Precision1 check: ✅ PASSED
- Test 4 - Precision2 check: ✅ PASSED

**Columns**: ['RetNOA']

**Observations**:
- Stata:  2,892,942
- Python: 3,014,004
- Common: 2,892,942

**Precision1**: 0.001% obs with std_diff >= 1.00e-02 (tolerance: < 10%)

**Precision2**: 99th percentile diff = 1.48e-19 (tolerance: < 1.00e+00)

**Summary Statistics** (Common Observations):

| Statistic  |          Stata |         Python |     Difference | Std Difference |
|------------|----------------|----------------|----------------|----------------|
| count      |       2.89e+06 |       2.89e+06 |       2.89e+06 |       2.89e+06 |
| mean       |       2.31e+11 |            inf |            inf |            inf |
| std        |       1.27e+14 |            N/A |            N/A |            N/A |
| min        |      -5.90e+15 |      -5.90e+15 |      -1.75e+09 |      -1.37e-05 |
| 25%        |        -0.0320 |        -0.0320 |      -6.74e-09 |      -5.29e-23 |
| 50%        |         0.1203 |         0.1203 |      -1.26e-12 |      -9.90e-27 |
| 75%        |         0.2648 |         0.2648 |       6.73e-09 |       5.29e-23 |
| max        |       6.23e+16 |            inf |            inf |            inf |

**Regression Analysis** (Python ~ Stata):

- **Model**: python = inf + inf * stata
- **R-squared**: nan
- **N observations**: 2,892,942

| Coefficient |     Estimate |    Std Error | t-statistic |   p-value |
|-------------|--------------|--------------|-------------|----------|
| Intercept   |          nan |          nan |         nan |       nan |
| Slope       |          nan |          nan |         nan |       nan |

**Feedback**:
- Num observations with std_diff >= TOL_DIFF_1: 24/2892942 (0.001%)
- Stata standard deviation: 1.27e+14

---

### RetNOA_q

**Status**: ✅ PASSED

**Test Results**:
- Test 1 - Column names: ✅ PASSED
- Test 2 - Superset check: ✅ PASSED
- Test 3 - Precision1 check: ✅ PASSED
- Test 4 - Precision2 check: ✅ PASSED

**Columns**: ['RetNOA_q']

**Observations**:
- Stata:  2,413,581
- Python: 2,692,945
- Common: 2,413,581

**Precision1**: 0.002% obs with std_diff >= 1.00e-02 (tolerance: < 10%)

**Precision2**: 99th percentile diff = 4.34e-11 (tolerance: < 1.00e+00)

**Summary Statistics** (Common Observations):

| Statistic  |          Stata |         Python |     Difference | Std Difference |
|------------|----------------|----------------|----------------|----------------|
| count      |       2.41e+06 |       2.41e+06 |       2.41e+06 |       2.41e+06 |
| mean       |       -46.8886 |            N/A |            N/A |            N/A |
| std        |     46097.2088 |            N/A |            N/A |            N/A |
| min        |      -4.12e+07 |           -inf |           -inf |           -inf |
| 25%        |      -9.84e-04 |      -9.81e-04 |      -1.55e-09 |      -3.37e-14 |
| 50%        |         0.0288 |         0.0288 |      -3.89e-13 |      -8.43e-18 |
| 75%        |         0.0609 |         0.0609 |       1.54e-09 |       3.34e-14 |
| max        |       3.43e+06 |            inf |            inf |            inf |

**Regression Analysis** (Python ~ Stata):

- **Model**: python = nan + nan * stata
- **R-squared**: nan
- **N observations**: 2,413,581

| Coefficient |     Estimate |    Std Error | t-statistic |   p-value |
|-------------|--------------|--------------|-------------|----------|
| Intercept   |          nan |          nan |         nan |       nan |
| Slope       |          nan |          nan |         nan |       nan |

**Feedback**:
- Num observations with std_diff >= TOL_DIFF_1: 38/2413581 (0.002%)
- Stata standard deviation: 4.61e+04

---

### ReturnSkewCAPM

**Status**: ❌ FAILED

**Test Results**:
- Test 1 - Column names: ✅ PASSED
- Test 2 - Superset check: ❌ FAILED (Python missing 37254 Stata observations)
- Test 3 - Precision1 check: ✅ PASSED
- Test 4 - Precision2 check: ✅ PASSED

**Columns**: ['ReturnSkewCAPM']

**Observations**:
- Stata:  4,997,359
- Python: 4,988,237
- Common: 4,960,105

**Precision1**: 0.808% obs with std_diff >= 1.00e-02 (tolerance: < 10%)

**Precision2**: 99th percentile diff = 8.97e-03 (tolerance: < 1.00e+00)

**Summary Statistics** (Common Observations):

| Statistic  |          Stata |         Python |     Difference | Std Difference |
|------------|----------------|----------------|----------------|----------------|
| count      |       4.96e+06 |       4.95e+06 |       4.95e+06 |       4.95e+06 |
| mean       |         0.1846 |         0.1846 |      -2.52e-04 |      -2.64e-04 |
| std        |         0.9536 |         0.9517 |         0.0706 |         0.0740 |
| min        |        -4.9022 |        -4.9022 |        -8.0139 |        -8.4041 |
| 25%        |        -0.2801 |        -0.2799 |      -2.62e-04 |      -2.75e-04 |
| 50%        |         0.1553 |         0.1556 |         0.0000 |         0.0000 |
| 75%        |         0.6325 |         0.6326 |       2.33e-04 |       2.44e-04 |
| max        |         4.8256 |         4.8258 |         7.7611 |         8.1391 |

**Regression Analysis** (Python ~ Stata):

- **Model**: python = 0.0001 + 0.9982 * stata
- **R-squared**: 0.9945
- **N observations**: 4,953,435

| Coefficient |     Estimate |    Std Error | t-statistic |   p-value |
|-------------|--------------|--------------|-------------|----------|
| Intercept   |     7.84e-05 |     3.23e-05 |      2.4269 |     0.015 |
| Slope       |       0.9982 |     3.33e-05 |  29948.1483 |     0.000 |

**Missing Observations Sample**:
```
 index  permno  yyyymm  ReturnSkewCAPM
     0   10001  201708        0.532855
     1   10002  201302        0.980123
     2   10003  198601        0.194168
     3   10003  199512        0.707874
     4   10005  198601       -1.702117
     5   10005  199107        2.265614
     6   10007  198601       -0.336022
     7   10007  199010       -1.647068
     8   10008  198601        0.808999
     9   10009  198601        1.587751
```

**Feedback**:
- Num observations with std_diff >= TOL_DIFF_1: 40095/4960105 (0.808%)
- Stata standard deviation: 9.54e-01

---

### ReturnSkewQF

**Status**: ❌ FAILED

**Test Results**:
- Test 1 - Column names: ✅ PASSED
- Test 2 - Superset check: ❌ FAILED (Python missing 30525 Stata observations)
- Test 3 - Precision1 check: ✅ PASSED
- Test 4 - Precision2 check: ✅ PASSED

**Columns**: ['ReturnSkewQF']

**Observations**:
- Stata:  3,985,016
- Python: 3,955,898
- Common: 3,954,491

**Precision1**: 0.892% obs with std_diff >= 1.00e-02 (tolerance: < 10%)

**Precision2**: 99th percentile diff = 3.16e-07 (tolerance: < 1.00e+00)

**Summary Statistics** (Common Observations):

| Statistic  |          Stata |         Python |     Difference | Std Difference |
|------------|----------------|----------------|----------------|----------------|
| count      |       3.95e+06 |       3.94e+06 |       3.94e+06 |       3.94e+06 |
| mean       |         0.1399 |         0.1401 |      -2.54e-04 |      -3.07e-04 |
| std        |         0.8265 |         0.8321 |         0.1179 |         0.1426 |
| min        |        -4.4416 |        -4.4416 |        -6.1208 |        -7.4054 |
| 25%        |        -0.2864 |        -0.2870 |      -1.92e-08 |      -2.33e-08 |
| 50%        |         0.1203 |         0.1203 |       1.76e-10 |       2.13e-10 |
| 75%        |         0.5534 |         0.5541 |       1.97e-08 |       2.38e-08 |
| max        |         4.4416 |         4.4772 |         6.0899 |         7.3679 |

**Regression Analysis** (Python ~ Stata):

- **Model**: python = 0.0003 + 0.9962 * stata
- **R-squared**: 0.9799
- **N observations**: 3,943,726

| Coefficient |     Estimate |    Std Error | t-statistic |   p-value |
|-------------|--------------|--------------|-------------|----------|
| Intercept   |     2.81e-04 |     6.02e-05 |      4.6702 |     0.000 |
| Slope       |       0.9962 |     7.18e-05 |  13883.1483 |     0.000 |

**Missing Observations Sample**:
```
 index  permno  yyyymm  ReturnSkewQF
     0   10000  198706      0.499660
     1   10002  201302      0.345465
     2   10003  198601      0.164571
     3   10003  199512      0.168800
     4   10005  198601     -1.189934
     5   10005  199107      1.837418
     6   10007  198601     -0.753537
     7   10007  199010     -1.225254
     8   10008  198601      0.281495
     9   10009  198601      0.921937
```

**Feedback**:
- Num observations with std_diff >= TOL_DIFF_1: 35283/3954491 (0.892%)
- Stata standard deviation: 8.27e-01

---

### SP_q

**Status**: ❌ FAILED

**Test Results**:
- Test 1 - Column names: ✅ PASSED
- Test 2 - Superset check: ❌ FAILED (Python missing 48 Stata observations)
- Test 3 - Precision1 check: ✅ PASSED
- Test 4 - Precision2 check: ✅ PASSED

**Columns**: ['SP_q']

**Observations**:
- Stata:  2,790,383
- Python: 2,790,458
- Common: 2,790,335

**Precision1**: 0.018% obs with std_diff >= 1.00e-02 (tolerance: < 10%)

**Precision2**: 99th percentile diff = 1.09e-07 (tolerance: < 1.00e+00)

**Summary Statistics** (Common Observations):

| Statistic  |          Stata |         Python |     Difference | Std Difference |
|------------|----------------|----------------|----------------|----------------|
| count      |       2.79e+06 |       2.79e+06 |       2.79e+06 |       2.79e+06 |
| mean       |         0.6076 |         0.6076 |      -2.41e-05 |      -1.33e-05 |
| std        |         1.8101 |         1.8101 |         0.0078 |         0.0043 |
| min        |       -31.7352 |       -31.7352 |        -3.9848 |        -2.2015 |
| 25%        |         0.1051 |         0.1051 |      -5.82e-09 |      -3.22e-09 |
| 50%        |         0.2523 |         0.2523 |         0.0000 |         0.0000 |
| 75%        |         0.5972 |         0.5972 |       5.80e-09 |       3.20e-09 |
| max        |       537.3825 |       537.3825 |         2.4458 |         1.3512 |

**Regression Analysis** (Python ~ Stata):

- **Model**: python = -0.0000 + 1.0000 * stata
- **R-squared**: 1.0000
- **N observations**: 2,790,335

| Coefficient |     Estimate |    Std Error | t-statistic |   p-value |
|-------------|--------------|--------------|-------------|----------|
| Intercept   |    -1.52e-05 |     4.90e-06 |     -3.1111 |     0.002 |
| Slope       |       1.0000 |     2.56e-06 | 390035.4285 |     0.000 |

**Missing Observations Sample**:
```
 index  permno  yyyymm     SP_q
     0   10872  199403 2.154062
     1   10872  199404 1.615547
     2   11545  199706 0.082241
     3   11545  199707 0.070940
     4   11545  199708 0.063652
     5   12113  200006 2.333926
     6   12113  200007 2.883085
     7   12113  200008 1.531639
     8   12837  198004 0.717490
     9   12837  198005 0.438482
```

**Feedback**:
- Num observations with std_diff >= TOL_DIFF_1: 491/2790335 (0.018%)
- Stata standard deviation: 1.81e+00

---

### Tax_q

**Status**: ❌ FAILED

**Test Results**:
- Test 1 - Column names: ✅ PASSED
- Test 2 - Superset check: ❌ FAILED (Python missing 74 Stata observations)
- Test 3 - Precision1 check: ✅ PASSED
- Test 4 - Precision2 check: ✅ PASSED

**Columns**: ['Tax_q']

**Observations**:
- Stata:  1,906,647
- Python: 1,906,681
- Common: 1,906,573

**Precision1**: 0.006% obs with std_diff >= 1.00e-02 (tolerance: < 10%)

**Precision2**: 99th percentile diff = 8.65e-09 (tolerance: < 1.00e+00)

**Summary Statistics** (Common Observations):

| Statistic  |          Stata |         Python |     Difference | Std Difference |
|------------|----------------|----------------|----------------|----------------|
| count      |       1.91e+06 |       1.91e+06 |       1.91e+06 |       1.91e+06 |
| mean       |         1.7501 |         1.7502 |       1.03e-04 |       6.38e-06 |
| std        |        16.1405 |        16.1419 |         0.0885 |         0.0055 |
| min        |       2.00e-06 |       2.00e-06 |       -11.3264 |        -0.7017 |
| 25%        |         1.2937 |         1.2936 |      -3.00e-08 |      -1.86e-09 |
| 50%        |         1.5463 |         1.5463 |         0.0000 |         0.0000 |
| 75%        |         1.7239 |         1.7239 |       3.03e-08 |       1.87e-09 |
| max        |     10630.3370 |     10630.3365 |        69.8003 |         4.3245 |

**Regression Analysis** (Python ~ Stata):

- **Model**: python = -0.0000 + 1.0001 * stata
- **R-squared**: 1.0000
- **N observations**: 1,906,573

| Coefficient |     Estimate |    Std Error | t-statistic |   p-value |
|-------------|--------------|--------------|-------------|----------|
| Intercept   |    -1.59e-05 |     6.45e-05 |     -0.2458 |     0.806 |
| Slope       |       1.0001 |     3.97e-06 | 251738.2130 |     0.000 |

**Missing Observations Sample**:
```
 index  permno  yyyymm    Tax_q
     0   10515  199604 1.604096
     1   10515  199605 1.604096
     2   10515  199606 1.604096
     3   11217  199212 3.416667
     4   11217  199301 3.416667
     5   11217  199302 3.416667
     6   11545  199706 1.449165
     7   11545  199707 1.449165
     8   11545  199708 1.449165
     9   11843  198803 0.940294
```

**Feedback**:
- Num observations with std_diff >= TOL_DIFF_1: 109/1906573 (0.006%)
- Stata standard deviation: 1.61e+01

---

### WW

**Status**: ✅ PASSED

**Test Results**:
- Test 1 - Column names: ✅ PASSED
- Test 2 - Superset check: ✅ PASSED
- Test 3 - Precision1 check: ✅ PASSED
- Test 4 - Precision2 check: ✅ PASSED

**Columns**: ['WW']

**Observations**:
- Stata:  2,702,805
- Python: 3,247,808
- Common: 2,702,805

**Precision1**: 0.001% obs with std_diff >= 1.00e-02 (tolerance: < 10%)

**Precision2**: 99th percentile diff = 5.20e-10 (tolerance: < 1.00e+00)

**Summary Statistics** (Common Observations):

| Statistic  |          Stata |         Python |     Difference | Std Difference |
|------------|----------------|----------------|----------------|----------------|
| count      |       2.70e+06 |       2.70e+06 |       2.70e+06 |       2.70e+06 |
| mean       |        -0.1112 |        -0.1111 |       1.11e-05 |       2.02e-07 |
| std        |        54.8159 |        54.8159 |         0.0052 |       9.44e-05 |
| min        |      -111.6833 |      -111.6833 |        -2.7503 |        -0.0502 |
| 25%        |        -0.3470 |        -0.3470 |      -5.02e-09 |      -9.17e-11 |
| 50%        |        -0.2572 |        -0.2571 |       2.66e-11 |       4.85e-13 |
| 75%        |        -0.1745 |        -0.1745 |       5.09e-09 |       9.29e-11 |
| max        |     76241.1800 |     76241.1777 |         3.7323 |         0.0681 |

**Regression Analysis** (Python ~ Stata):

- **Model**: python = 0.0000 + 1.0000 * stata
- **R-squared**: 1.0000
- **N observations**: 2,702,805

| Coefficient |     Estimate |    Std Error | t-statistic |   p-value |
|-------------|--------------|--------------|-------------|----------|
| Intercept   |     1.11e-05 |     3.15e-06 |      3.5220 |     0.000 |
| Slope       |       1.0000 |     5.74e-08 |    1.74e+07 |     0.000 |

**Feedback**:
- Num observations with std_diff >= TOL_DIFF_1: 29/2702805 (0.001%)
- Stata standard deviation: 5.48e+01

---

### WW_Q

**Status**: ❌ FAILED

**Test Results**:
- Test 1 - Column names: ✅ PASSED
- Test 2 - Superset check: ❌ FAILED (Python missing 91 Stata observations)
- Test 3 - Precision1 check: ✅ PASSED
- Test 4 - Precision2 check: ✅ PASSED

**Columns**: ['WW_Q']

**Observations**:
- Stata:  2,406,602
- Python: 2,440,911
- Common: 2,406,511

**Precision1**: 0.002% obs with std_diff >= 1.00e-02 (tolerance: < 10%)

**Precision2**: 99th percentile diff = 1.94e-06 (tolerance: < 1.00e+00)

**Summary Statistics** (Common Observations):

| Statistic  |          Stata |         Python |     Difference | Std Difference |
|------------|----------------|----------------|----------------|----------------|
| count      |       2.41e+06 |       2.41e+06 |       2.41e+06 |       2.41e+06 |
| mean       |        -0.0942 |           -inf |           -inf |           -inf |
| std        |        80.9108 |            N/A |            N/A |            N/A |
| min        |     -1099.2520 |           -inf |           -inf |           -inf |
| 25%        |        -0.3578 |        -0.3578 |      -6.07e-09 |      -7.51e-11 |
| 50%        |        -0.2663 |        -0.2663 |      -3.95e-11 |      -4.88e-13 |
| 75%        |        -0.1791 |        -0.1791 |       5.97e-09 |       7.38e-11 |
| max        |     75674.3520 |     75674.3568 |        15.5945 |         0.1927 |

**Regression Analysis** (Python ~ Stata):

- **Model**: python = -inf + nan * stata
- **R-squared**: nan
- **N observations**: 2,406,511

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
     4   10872  199403 -0.160945
     5   10872  199404 -0.163142
     6   11545  199706 -0.169969
     7   11545  199707 -0.161824
     8   11545  199708 -0.155090
     9   12113  200006 -0.146354
```

**Feedback**:
- Num observations with std_diff >= TOL_DIFF_1: 38/2406511 (0.002%)
- Stata standard deviation: 8.09e+01

---

### ZScore

**Status**: ❌ FAILED

**Test Results**:
- Test 1 - Column names: ✅ PASSED
- Test 2 - Superset check: ❌ FAILED (Python missing 1351 Stata observations)
- Test 3 - Precision1 check: ✅ PASSED
- Test 4 - Precision2 check: ✅ PASSED

**Columns**: ['ZScore']

**Observations**:
- Stata:  1,669,459
- Python: 1,669,132
- Common: 1,668,108

**Precision1**: 0.000% obs with std_diff >= 1.00e-02 (tolerance: < 10%)

**Precision2**: 99th percentile diff = 5.63e-08 (tolerance: < 1.00e+00)

**Summary Statistics** (Common Observations):

| Statistic  |          Stata |         Python |     Difference | Std Difference |
|------------|----------------|----------------|----------------|----------------|
| count      |       1.67e+06 |       1.67e+06 |       1.67e+06 |       1.67e+06 |
| mean       |         5.9429 |         5.9429 |       7.95e-07 |       2.34e-08 |
| std        |        33.9604 |        33.9604 |         0.0011 |       3.27e-05 |
| min        |      -353.7195 |      -353.7195 |        -0.1188 |        -0.0035 |
| 25%        |         2.1718 |         2.1718 |      -7.65e-08 |      -2.25e-09 |
| 50%        |         3.4992 |         3.4992 |       2.97e-11 |       8.75e-13 |
| 75%        |         5.4589 |         5.4589 |       7.67e-08 |       2.26e-09 |
| max        |      8802.6084 |      8802.6085 |         1.3375 |         0.0394 |

**Regression Analysis** (Python ~ Stata):

- **Model**: python = 0.0000 + 1.0000 * stata
- **R-squared**: 1.0000
- **N observations**: 1,668,108

| Coefficient |     Estimate |    Std Error | t-statistic |   p-value |
|-------------|--------------|--------------|-------------|----------|
| Intercept   |     9.25e-07 |     8.72e-07 |      1.0601 |     0.289 |
| Slope       |       1.0000 |     2.53e-08 |    3.95e+07 |     0.000 |

**Missing Observations Sample**:
```
 index  permno  yyyymm     ZScore
     0   15381  201606 -12.249100
     1   15381  201607 -10.749489
     2   15381  201608 -11.746960
     3   15381  201609 -11.660131
     4   15381  201610 -12.884400
     5   15381  201611 -12.757137
     6   15381  201612 -12.279421
     7   15381  201701 -12.303628
     8   15381  201702 -12.594108
     9   15381  201703 -12.051365
```

**Feedback**:
- Num observations with std_diff >= TOL_DIFF_1: 1/1668108 (0.000%)
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
- Python: 1,490,454
- Common: 1,214,174

**Precision1**: 0.006% obs with std_diff >= 1.00e-02 (tolerance: < 10%)

**Precision2**: 99th percentile diff = 5.01e-08 (tolerance: < 1.00e+00)

**Summary Statistics** (Common Observations):

| Statistic  |          Stata |         Python |     Difference | Std Difference |
|------------|----------------|----------------|----------------|----------------|
| count      |       1.21e+06 |       1.21e+06 |       1.21e+06 |       1.21e+06 |
| mean       |         4.2873 |         4.2873 |       1.84e-05 |       5.36e-07 |
| std        |        34.3037 |        34.3037 |         0.0146 |       4.26e-04 |
| min        |     -9318.5010 |     -9318.5014 |        -3.3394 |        -0.0973 |
| 25%        |         1.1057 |         1.1057 |      -4.80e-08 |      -1.40e-09 |
| 50%        |         1.9844 |         1.9844 |       3.71e-11 |       1.08e-12 |
| 75%        |         3.4886 |         3.4886 |       4.82e-08 |       1.40e-09 |
| max        |      9482.0879 |      9482.0882 |         6.7900 |         0.1979 |

**Regression Analysis** (Python ~ Stata):

- **Model**: python = 0.0000 + 1.0000 * stata
- **R-squared**: 1.0000
- **N observations**: 1,214,174

| Coefficient |     Estimate |    Std Error | t-statistic |   p-value |
|-------------|--------------|--------------|-------------|----------|
| Intercept   |     1.81e-05 |     1.34e-05 |      1.3566 |     0.175 |
| Slope       |       1.0000 |     3.87e-07 |    2.59e+06 |     0.000 |

**Feedback**:
- Num observations with std_diff >= TOL_DIFF_1: 69/1214174 (0.006%)
- Stata standard deviation: 3.43e+01

---

### betaCC

**Status**: ❌ FAILED

**Test Results**:
- Test 1 - Column names: ✅ PASSED
- Test 2 - Superset check: ❌ FAILED (Python missing 288458 Stata observations)
- Test 3 - Precision1 check: ❌ FAILED
- Test 4 - Precision2 check: ❌ FAILED

**Columns**: ['betaCC']

**Observations**:
- Stata:  3,459,006
- Python: 3,206,357
- Common: 3,170,548

**Precision1**: 77.088% obs with std_diff >= 1.00e-02 (tolerance: < 10%)

**Precision2**: 99th percentile diff = 1.35e+01 (tolerance: < 1.00e+00)

**Summary Statistics** (Common Observations):

| Statistic  |          Stata |         Python |     Difference | Std Difference |
|------------|----------------|----------------|----------------|----------------|
| count      |       3.17e+06 |       3.17e+06 |       3.17e+06 |       3.17e+06 |
| mean       |         8.6444 |        -2.7986 |       -11.4430 |        -0.5236 |
| std        |        21.8551 |        47.0464 |        54.9334 |         2.5135 |
| min        |      -349.5267 |      -824.7979 |      -842.7770 |       -38.5621 |
| 25%        |         0.0500 |        -0.0349 |        -4.9712 |        -0.2275 |
| 50%        |         0.7937 |         0.3822 |        -0.0338 |        -0.0015 |
| 75%        |         9.3539 |         5.0303 |         1.4257 |         0.0652 |
| max        |       379.4352 |       348.1181 |       368.4940 |        16.8608 |

**Regression Analysis** (Python ~ Stata):

- **Model**: python = 0.1575 + -0.3420 * stata
- **R-squared**: 0.0252
- **N observations**: 3,170,548

| Coefficient |     Estimate |    Std Error | t-statistic |   p-value |
|-------------|--------------|--------------|-------------|----------|
| Intercept   |       0.1575 |       0.0281 |      5.6132 |     0.000 |
| Slope       |      -0.3420 |       0.0012 |   -286.5032 |     0.000 |

**Missing Observations Sample**:
```
 index  permno  yyyymm    betaCC
     0   10001  198912 96.556709
     1   10002  198912 32.718147
     2   10003  198912 -2.203168
     3   10005  198912 61.053226
     4   10005  199001 53.632965
     5   10005  199002 51.967674
     6   10005  199003 51.935169
     7   10005  199004 49.527191
     8   10005  199005 47.318539
     9   10005  199006 43.358784
```

**Feedback**:
- Num observations with std_diff >= TOL_DIFF_1: 2444109/3170548 (77.088%)
- Stata standard deviation: 2.19e+01

**Most Recent Bad Observations**:
```
   permno  yyyymm     python      stata       diff
0   10028  202412  31.577045  21.920418   9.656627
1   10044  202412  18.481290  23.439190  -4.957900
2   10113  202412  25.177770  18.293459   6.884311
3   10158  202412   0.691755   0.455747   0.236008
4   10207  202412   7.418319   4.409046   3.009273
5   10253  202412  36.230914  22.687012  13.543902
6   10257  202412  22.212737  15.757562   6.455175
7   10258  202412   0.318325   1.725508  -1.407183
8   10294  202412  14.580944   1.382009  13.198935
9   10333  202412   3.054784   3.627675  -0.572891
```

**Largest Differences**:
```
   permno  yyyymm      python       stata        diff
0   82624  200806 -824.797898   17.979137 -842.777035
1   82624  200807 -796.361299   18.201847 -814.563146
2   10952  200806 -764.597438   49.578754 -814.176192
3   12209  200806 -764.641985   46.135052 -810.777037
4   10952  200807 -760.834108   49.601364 -810.435472
5   84030  200806 -707.854492  102.418100 -810.272592
6   12209  200807 -760.272723   46.859852 -807.132575
7   91287  200806 -700.429582  104.901990 -805.331572
8   83632  200806 -657.328560  147.812000 -805.140560
9   85705  200807 -753.295848   49.907070 -803.202918
```

---

### betaCR

**Status**: ❌ FAILED

**Test Results**:
- Test 1 - Column names: ✅ PASSED
- Test 2 - Superset check: ❌ FAILED (Python missing 288481 Stata observations)
- Test 3 - Precision1 check: ❌ FAILED
- Test 4 - Precision2 check: ❌ FAILED

**Columns**: ['betaCR']

**Observations**:
- Stata:  3,459,006
- Python: 3,205,749
- Common: 3,170,525

**Precision1**: 65.916% obs with std_diff >= 1.00e-02 (tolerance: < 10%)

**Precision2**: 99th percentile diff = 3.62e+00 (tolerance: < 1.00e+00)

**Summary Statistics** (Common Observations):

| Statistic  |          Stata |         Python |     Difference | Std Difference |
|------------|----------------|----------------|----------------|----------------|
| count      |       3.17e+06 |       3.17e+06 |       3.17e+06 |       3.17e+06 |
| mean       |        -8.2910 |        -3.5659 |         4.7250 |         0.1565 |
| std        |        30.1999 |        18.3752 |        24.6951 |         0.8177 |
| min        |      -453.6021 |      -534.4206 |      -509.3180 |       -16.8649 |
| 25%        |        -6.3774 |        -1.0215 |        -0.1058 |        -0.0035 |
| 50%        |        -0.4646 |        -0.0389 |         0.1468 |         0.0049 |
| 75%        |        -0.0032 |         0.0109 |         3.2185 |         0.1066 |
| max        |       491.6973 |       699.7499 |       695.3175 |        23.0238 |

**Regression Analysis** (Python ~ Stata):

- **Model**: python = -0.6577 + 0.3508 * stata
- **R-squared**: 0.3324
- **N observations**: 3,170,525

| Coefficient |     Estimate |    Std Error | t-statistic |   p-value |
|-------------|--------------|--------------|-------------|----------|
| Intercept   |      -0.6577 |       0.0087 |    -75.2163 |     0.000 |
| Slope       |       0.3508 |     2.79e-04 |   1256.2916 |     0.000 |

**Missing Observations Sample**:
```
 index  permno  yyyymm     betaCR
     0   10001  198912  -4.462341
     1   10002  198912  10.664037
     2   10003  198912  -0.254437
     3   10005  198912   0.960282
     4   10005  199001   3.320451
     5   10005  199002   2.864126
     6   10005  199003   2.835214
     7   10005  199004   3.779512
     8   10005  199005   1.537567
     9   10005  199006 -11.425655
```

**Feedback**:
- Num observations with std_diff >= TOL_DIFF_1: 2089880/3170525 (65.916%)
- Stata standard deviation: 3.02e+01

**Most Recent Bad Observations**:
```
   permno  yyyymm     python      stata      diff
0   10028  202412  19.157147  15.126258  4.030889
1   10044  202412 -54.191267 -51.162571 -3.028696
2   10113  202412 -35.443679 -33.305286 -2.138393
3   10207  202412  -4.468778  -4.013835 -0.454943
4   10253  202412  -7.740257 -14.677695  6.937438
5   10257  202412 -26.683773 -31.312153  4.628380
6   10258  202412 -21.721220 -21.035307 -0.685913
7   10294  202412  -7.055871 -12.270684  5.214813
8   10333  202412  -1.050962  -0.421896 -0.629066
9   10443  202412  -5.708680  -5.188190 -0.520490
```

**Largest Differences**:
```
   permno  yyyymm      python       stata        diff
0   14025  201707  699.749927    4.432381  695.317546
1   14025  201708  683.944779    4.391966  679.552813
2   14025  201709  669.322313    5.034044  664.288270
3   14025  201710  646.318615    4.322103  641.996512
4   14025  201711  619.398959    4.230157  615.168802
5   14377  201801  198.501219 -407.127500  605.628719
6   14025  201712  608.333593    4.049723  604.283871
7   14025  201801  592.229656    3.651663  588.577993
8   13838  201802  340.172992 -220.068920  560.241912
9   14025  201802  559.594226    3.445087  556.149139
```

---

### betaNet

**Status**: ❌ FAILED

**Test Results**:
- Test 1 - Column names: ✅ PASSED
- Test 2 - Superset check: ❌ FAILED (Python missing 250293 Stata observations)
- Test 3 - Precision1 check: ❌ FAILED
- Test 4 - Precision2 check: ❌ FAILED

**Columns**: ['betaNet']

**Observations**:
- Stata:  3,420,591
- Python: 3,205,061
- Common: 3,170,298

**Precision1**: 78.491% obs with std_diff >= 1.00e-02 (tolerance: < 10%)

**Precision2**: 99th percentile diff = 8.06e+00 (tolerance: < 1.00e+00)

**Summary Statistics** (Common Observations):

| Statistic  |          Stata |         Python |     Difference | Std Difference |
|------------|----------------|----------------|----------------|----------------|
| count      |       3.17e+06 |       3.17e+06 |       3.17e+06 |       3.17e+06 |
| mean       |        17.5911 |         1.0554 |       -16.5357 |        -0.3780 |
| std        |        43.7488 |        45.2922 |        68.6161 |         1.5684 |
| min        |      -561.5379 |      -746.7417 |      -975.7653 |       -22.3038 |
| 25%        |         0.7150 |         0.0476 |        -8.6101 |        -0.1968 |
| 50%        |         2.2951 |         1.1370 |        -0.4456 |        -0.0102 |
| 75%        |        17.3850 |         6.6491 |         0.9338 |         0.0213 |
| max        |       620.3024 |       532.7209 |       494.0089 |        11.2919 |

**Regression Analysis** (Python ~ Stata):

- **Model**: python = 4.4690 + -0.1941 * stata
- **R-squared**: 0.0351
- **N observations**: 3,170,298

| Coefficient |     Estimate |    Std Error | t-statistic |   p-value |
|-------------|--------------|--------------|-------------|----------|
| Intercept   |       4.4690 |       0.0269 |    165.9449 |     0.000 |
| Slope       |      -0.1941 |     5.71e-04 |   -339.7702 |     0.000 |

**Missing Observations Sample**:
```
 index  permno  yyyymm    betaNet
     0   10001  198912 101.080060
     1   10002  198912  22.053020
     2   10003  198912  -1.873727
     3   10005  198912  59.802097
     4   10005  199001  50.042191
     5   10005  199002  48.851650
     6   10005  199003  48.856773
     7   10005  199004  45.507900
     8   10005  199005  45.564640
     9   10005  199006  54.570499
```

**Feedback**:
- Num observations with std_diff >= TOL_DIFF_1: 2488400/3170298 (78.491%)
- Stata standard deviation: 4.37e+01

**Most Recent Bad Observations**:
```
   permno  yyyymm     python      stata      diff
0   10028  202412  12.970081   7.307667  5.662413
1   10044  202412  73.281135  75.308937 -2.027802
2   10113  202412  61.434583  52.441204  8.993379
3   10207  202412  12.668037   9.244012  3.424025
4   10253  202412  45.217181  38.610798  6.606383
5   10257  202412  49.691697  47.998154  1.693543
6   10258  202412  24.846751  25.298738 -0.451987
7   10294  202412  22.903733  14.915699  7.988034
8   10355  202412  15.473973  12.896639  2.577334
9   10443  202412   4.923517   6.205584 -1.282067
```

**Largest Differences**:
```
   permno  yyyymm      python      stata        diff
0   85356  200805 -420.415023  555.35028 -975.765303
1   87318  200805 -478.833184  474.05557 -952.888754
2   84030  200806 -587.001091  362.71936 -949.720451
3   84030  200805 -547.424104  401.09720 -948.521304
4   91287  200805 -591.499509  348.11423 -939.613739
5   84030  200804 -454.483004  479.30182 -933.784824
6   84030  200710 -346.110059  587.65570 -933.765759
7   84030  200711 -381.115119  549.00305 -930.118169
8   84030  200712 -375.446660  551.29279 -926.739450
9   85356  200806 -445.099762  481.40512 -926.504882
```

---

### betaRC

**Status**: ❌ FAILED

**Test Results**:
- Test 1 - Column names: ✅ PASSED
- Test 2 - Superset check: ✅ PASSED
- Test 3 - Precision1 check: ❌ FAILED
- Test 4 - Precision2 check: ❌ FAILED

**Columns**: ['betaRC']

**Observations**:
- Stata:  3,421,560
- Python: 3,461,692
- Common: 3,421,560

**Precision1**: 98.785% obs with std_diff >= 1.00e-02 (tolerance: < 10%)

**Precision2**: 99th percentile diff = 3.46e+00 (tolerance: < 1.00e+00)

**Summary Statistics** (Common Observations):

| Statistic  |          Stata |         Python |     Difference | Std Difference |
|------------|----------------|----------------|----------------|----------------|
| count      |       3.42e+06 |       3.42e+06 |       3.42e+06 |       3.42e+06 |
| mean       |        -0.1585 |        -0.0574 |         0.1010 |         0.4857 |
| std        |         0.2080 |         0.1708 |         0.1914 |         0.9204 |
| min        |        -8.9074 |        -6.4917 |        -5.0246 |       -24.1619 |
| 25%        |        -0.2516 |        -0.0872 |         0.0039 |         0.0189 |
| 50%        |        -0.1403 |        -0.0315 |         0.0849 |         0.4081 |
| 75%        |        -0.0465 |        -0.0017 |         0.1890 |         0.9087 |
| max        |         6.1166 |         7.9645 |         4.9314 |        23.7141 |

**Regression Analysis** (Python ~ Stata):

- **Model**: python = 0.0081 + 0.4135 * stata
- **R-squared**: 0.2537
- **N observations**: 3,421,560

| Coefficient |     Estimate |    Std Error | t-statistic |   p-value |
|-------------|--------------|--------------|-------------|----------|
| Intercept   |       0.0081 |     1.00e-04 |     80.6264 |     0.000 |
| Slope       |       0.4135 |     3.83e-04 |   1078.3722 |     0.000 |

**Feedback**:
- Num observations with std_diff >= TOL_DIFF_1: 3379994/3421560 (98.785%)
- Stata standard deviation: 2.08e-01

**Most Recent Bad Observations**:
```
   permno  yyyymm    python     stata      diff
0   10026  202412  0.014323 -0.024906  0.039229
1   10028  202412 -0.218407 -0.200618 -0.017790
2   10032  202412  0.033644 -0.044258  0.077902
3   10044  202412  0.161009  0.018604  0.142404
4   10065  202412 -0.041100 -0.104633  0.063533
5   10104  202412 -0.076381 -0.129191  0.052810
6   10107  202412 -0.110181 -0.124065  0.013884
7   10113  202412 -0.060098 -0.132289  0.072191
8   10138  202412 -0.090315 -0.152853  0.062538
9   10145  202412 -0.000101 -0.092242  0.092141
```

**Largest Differences**:
```
   permno  yyyymm    python     stata      diff
0   79006  200412 -3.535730  1.488823 -5.024553
1   79261  199705 -0.275510 -5.206944  4.931433
2   79006  200501 -3.368015  1.450752 -4.818767
3   79006  200411 -3.303724  1.490285 -4.794009
4   58748  199511 -3.626904 -8.405652  4.778748
5   89173  198808  0.741950 -3.895979  4.637929
6   79261  199706 -0.162244 -4.761354  4.599110
7   79006  200410 -2.977338  1.503812 -4.481150
8   79006  200407 -2.978096  1.437946 -4.416042
9   79006  200409 -2.913579  1.498283 -4.411862
```

---

### betaRR

**Status**: ❌ FAILED

**Test Results**:
- Test 1 - Column names: ✅ PASSED
- Test 2 - Superset check: ✅ PASSED
- Test 3 - Precision1 check: ❌ FAILED
- Test 4 - Precision2 check: ❌ FAILED

**Columns**: ['betaRR']

**Observations**:
- Stata:  3,421,560
- Python: 3,461,064
- Common: 3,421,560

**Precision1**: 98.483% obs with std_diff >= 1.00e-02 (tolerance: < 10%)

**Precision2**: 99th percentile diff = 2.89e+00 (tolerance: < 1.00e+00)

**Summary Statistics** (Common Observations):

| Statistic  |          Stata |         Python |     Difference | Std Difference |
|------------|----------------|----------------|----------------|----------------|
| count      |       3.42e+06 |       3.42e+06 |       3.42e+06 |       3.42e+06 |
| mean       |         0.4870 |         0.2149 |        -0.2721 |        -0.6196 |
| std        |         0.4391 |         0.3914 |         0.2901 |         0.6607 |
| min        |        -9.0881 |        -9.2420 |        -5.2150 |       -11.8776 |
| 25%        |         0.2195 |         0.0038 |        -0.4089 |        -0.9314 |
| 50%        |         0.4000 |         0.0172 |        -0.2296 |        -0.5230 |
| 75%        |         0.6594 |         0.3377 |        -0.0716 |        -0.1630 |
| max        |        14.4013 |        14.6229 |         6.5177 |        14.8447 |

**Regression Analysis** (Python ~ Stata):

- **Model**: python = -0.1158 + 0.6791 * stata
- **R-squared**: 0.5803
- **N observations**: 3,421,560

| Coefficient |     Estimate |    Std Error | t-statistic |   p-value |
|-------------|--------------|--------------|-------------|----------|
| Intercept   |      -0.1158 |     2.05e-04 |   -565.6637 |     0.000 |
| Slope       |       0.6791 |     3.12e-04 |   2174.9571 |     0.000 |

**Feedback**:
- Num observations with std_diff >= TOL_DIFF_1: 3369652/3421560 (98.483%)
- Stata standard deviation: 4.39e-01

**Most Recent Bad Observations**:
```
   permno  yyyymm    python     stata      diff
0   10026  202412  0.493511  0.465418  0.028093
1   10028  202412  0.331776  0.312890  0.018886
2   10032  202412  0.660508  0.622909  0.037599
3   10044  202412  0.769588  0.725779  0.043808
4   10065  202412  0.713768  0.673138  0.040631
5   10104  202412  0.697834  0.658111  0.039724
6   10107  202412  0.615829  0.580773  0.035056
7   10113  202412  0.753036  0.710170  0.042866
8   10138  202412  1.074110  1.012967  0.061143
9   10145  202412  0.726112  0.684779  0.041333
```

**Largest Differences**:
```
   permno  yyyymm    python     stata      diff
0   58748  199602 -0.500889 -7.018583  6.517694
1   58748  199606 -0.538110 -6.984344  6.446235
2   58748  199603 -0.494707 -6.933651  6.438944
3   58748  199604 -0.494017 -6.873692  6.379675
4   58748  199605 -0.498361 -6.729397  6.231036
5   58748  199601 -0.336576 -5.716923  5.380348
6   58748  199512 -0.332551 -5.681717  5.349166
7   58748  199511 -0.318695 -5.543966  5.225270
8   87588  200710  1.230044  6.445008 -5.214965
9   88336  200709  1.214242  6.276519 -5.062277
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
- Python: 3,286,173
- Common: 3,267,782

**Precision1**: 0.000% obs with std_diff >= 1.00e-02 (tolerance: < 10%)

**Precision2**: 99th percentile diff = 3.24e-09 (tolerance: < 1.00e+00)

**Summary Statistics** (Common Observations):

| Statistic  |          Stata |         Python |     Difference | Std Difference |
|------------|----------------|----------------|----------------|----------------|
| count      |       3.27e+06 |       3.27e+06 |       3.27e+06 |       3.27e+06 |
| mean       |         0.3051 |         0.3051 |       8.64e-07 |       1.88e-08 |
| std        |        45.8671 |        45.8671 |         0.0011 |       2.45e-05 |
| min        |    -10248.0000 |    -10248.0000 |        -0.3728 |        -0.0081 |
| 25%        |         0.0096 |         0.0096 |      -3.26e-09 |      -7.11e-11 |
| 50%        |         0.1142 |         0.1142 |         0.0000 |         0.0000 |
| 75%        |         0.2625 |         0.2625 |       3.26e-09 |       7.11e-11 |
| max        |     13971.0000 |     13971.0000 |         0.2960 |         0.0065 |

**Regression Analysis** (Python ~ Stata):

- **Model**: python = 0.0000 + 1.0000 * stata
- **R-squared**: 1.0000
- **N observations**: 3,267,782

| Coefficient |     Estimate |    Std Error | t-statistic |   p-value |
|-------------|--------------|--------------|-------------|----------|
| Intercept   |     8.61e-07 |     6.21e-07 |      1.3871 |     0.165 |
| Slope       |       1.0000 |     1.35e-08 |    7.39e+07 |     0.000 |

**Feedback**:
- Num observations with std_diff >= TOL_DIFF_1: 0/3267782 (0.000%)
- Stata standard deviation: 4.59e+01

---

### cfpq

**Status**: ❌ FAILED

**Test Results**:
- Test 1 - Column names: ✅ PASSED
- Test 2 - Superset check: ❌ FAILED (Python missing 1 Stata observations)
- Test 3 - Precision1 check: ❌ FAILED
- Test 4 - Precision2 check: ✅ PASSED

**Columns**: ['cfpq']

**Observations**:
- Stata:  2,252,622
- Python: 2,703,325
- Common: 2,252,621

**Precision1**: 11.981% obs with std_diff >= 1.00e-02 (tolerance: < 10%)

**Precision2**: 99th percentile diff = 8.81e-01 (tolerance: < 1.00e+00)

**Summary Statistics** (Common Observations):

| Statistic  |          Stata |         Python |     Difference | Std Difference |
|------------|----------------|----------------|----------------|----------------|
| count      |       2.25e+06 |       2.25e+06 |       2.25e+06 |       2.25e+06 |
| mean       |       2.37e-04 |         0.0061 |         0.0059 |         0.0082 |
| std        |         0.7177 |         0.8124 |         0.6330 |         0.8821 |
| min        |      -306.2332 |      -278.1893 |      -161.2249 |      -224.6477 |
| 25%        |        -0.0228 |        -0.0169 |      -9.56e-10 |      -1.33e-09 |
| 50%        |         0.0110 |         0.0132 |       2.98e-11 |       4.15e-11 |
| 75%        |         0.0389 |         0.0423 |       1.37e-09 |       1.91e-09 |
| max        |       250.7536 |       250.7536 |       307.0868 |       427.8888 |

**Regression Analysis** (Python ~ Stata):

- **Model**: python = 0.0059 + 0.7517 * stata
- **R-squared**: 0.4409
- **N observations**: 2,252,621

| Coefficient |     Estimate |    Std Error | t-statistic |   p-value |
|-------------|--------------|--------------|-------------|----------|
| Intercept   |       0.0059 |     4.05e-04 |     14.6112 |     0.000 |
| Slope       |       0.7517 |     5.64e-04 |   1332.9026 |     0.000 |

**Missing Observations Sample**:
```
 index  permno  yyyymm     cfpq
     0   19316  202412 0.029232
```

**Feedback**:
- Num observations with std_diff >= TOL_DIFF_1: 269879/2252621 (11.981%)
- Stata standard deviation: 7.18e-01

**Most Recent Bad Observations**:
```
   permno  yyyymm    python     stata      diff
0   15268  202412 -0.611130 -1.136608  0.525478
1   17330  202412 -0.271085 -0.231680 -0.039405
2   18302  202412 -0.031779  0.599014 -0.630793
3   18464  202412  0.236709 -0.015777  0.252486
4   19487  202412 -0.321679 -0.423716  0.102037
5   20801  202412 -0.375193  1.748981 -2.124173
6   22894  202412 -0.030379 -0.019062 -0.011316
7   23193  202412 -0.098279 -4.034034  3.935756
8   79571  202412  0.095949  0.076077  0.019872
9   80276  202412  0.000368  0.304700 -0.304332
```

**Largest Differences**:
```
   permno  yyyymm      python       stata        diff
0   19314  202311    0.853598 -306.233250  307.086848
1   63079  198711   -0.132030 -169.426270  169.294240
2   50518  197409 -161.705519   -0.480574 -161.224945
3   28310  197505  109.189841  -16.858906  126.048747
4   50518  197507 -122.357907   -0.110357 -122.247550
5   50518  197509 -122.357907   -0.110357 -122.247550
6   28310  197503  105.488491  -16.287418  121.775909
7   28310  197504  105.488491  -16.287418  121.775909
8   28310  197605  125.327968    6.254519  119.073449
9   28310  197703  109.315549   -9.288592  118.604142
```

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
- Python: 3,070,726
- Common: 3,065,278

**Precision1**: 0.000% obs with std_diff >= 1.00e-02 (tolerance: < 10%)

**Precision2**: 99th percentile diff = 1.40e-08 (tolerance: < 1.00e+00)

**Summary Statistics** (Common Observations):

| Statistic  |          Stata |         Python |     Difference | Std Difference |
|------------|----------------|----------------|----------------|----------------|
| count      |       3.07e+06 |       3.07e+06 |       3.07e+06 |       3.07e+06 |
| mean       |         3.3803 |         3.3803 |      -1.59e-06 |      -2.81e-08 |
| std        |        56.6989 |        56.6989 |       9.92e-04 |       1.75e-05 |
| min        |         0.0000 |         0.0000 |        -0.4978 |        -0.0088 |
| 25%        |         1.2859 |         1.2859 |      -5.02e-08 |      -8.85e-10 |
| 50%        |         2.0125 |         2.0125 |         0.0000 |         0.0000 |
| 75%        |         3.1813 |         3.1813 |       5.05e-08 |       8.91e-10 |
| max        |     25204.0000 |     25204.0000 |         0.0579 |         0.0010 |

**Regression Analysis** (Python ~ Stata):

- **Model**: python = -0.0000 + 1.0000 * stata
- **R-squared**: 1.0000
- **N observations**: 3,065,278

| Coefficient |     Estimate |    Std Error | t-statistic |   p-value |
|-------------|--------------|--------------|-------------|----------|
| Intercept   |    -1.59e-06 |     5.68e-07 |     -2.8076 |     0.005 |
| Slope       |       1.0000 |     1.00e-08 |    1.00e+08 |     0.000 |

**Feedback**:
- Num observations with std_diff >= TOL_DIFF_1: 0/3065278 (0.000%)
- Stata standard deviation: 5.67e+01

---

### depr

**Status**: ✅ PASSED

**Test Results**:
- Test 1 - Column names: ✅ PASSED
- Test 2 - Superset check: ✅ PASSED
- Test 3 - Precision1 check: ✅ PASSED
- Test 4 - Precision2 check: ✅ PASSED

**Columns**: ['depr']

**Observations**:
- Stata:  3,462,713
- Python: 3,525,488
- Common: 3,462,713

**Precision1**: 0.004% obs with std_diff >= 1.00e-02 (tolerance: < 10%)

**Precision2**: 99th percentile diff = 8.77e-09 (tolerance: < 1.00e+00)

**Summary Statistics** (Common Observations):

| Statistic  |          Stata |         Python |     Difference | Std Difference |
|------------|----------------|----------------|----------------|----------------|
| count      |       3.46e+06 |       3.46e+06 |       3.46e+06 |       3.46e+06 |
| mean       |         0.4261 |         0.4261 |      -1.05e-05 |      -1.17e-06 |
| std        |         8.9356 |         8.9356 |         0.0037 |       4.12e-04 |
| min        |        -2.3523 |        -2.3523 |        -1.4752 |        -0.1651 |
| 25%        |         0.0910 |         0.0910 |      -3.06e-09 |      -3.43e-10 |
| 50%        |         0.1480 |         0.1480 |         0.0000 |         0.0000 |
| 75%        |         0.2717 |         0.2717 |       2.97e-09 |       3.32e-10 |
| max        |      2457.7500 |      2457.7500 |         0.2782 |         0.0311 |

**Regression Analysis** (Python ~ Stata):

- **Model**: python = -0.0000 + 1.0000 * stata
- **R-squared**: 1.0000
- **N observations**: 3,462,713

| Coefficient |     Estimate |    Std Error | t-statistic |   p-value |
|-------------|--------------|--------------|-------------|----------|
| Intercept   |    -1.04e-05 |     1.98e-06 |     -5.2527 |     0.000 |
| Slope       |       1.0000 |     2.22e-07 |    4.51e+06 |     0.000 |

**Feedback**:
- Num observations with std_diff >= TOL_DIFF_1: 132/3462713 (0.004%)
- Stata standard deviation: 8.94e+00

---

### fgr5yrNoLag

**Status**: ❌ FAILED

**Test Results**:
- Test 1 - Column names: ✅ PASSED
- Test 2 - Superset check: ❌ FAILED (Python missing 4917 Stata observations)
- Test 3 - Precision1 check: ✅ PASSED
- Test 4 - Precision2 check: ✅ PASSED

**Columns**: ['fgr5yrNoLag']

**Observations**:
- Stata:  996,237
- Python: 998,737
- Common: 991,320

**Precision1**: 0.077% obs with std_diff >= 1.00e-02 (tolerance: < 10%)

**Precision2**: 99th percentile diff = 1.43e-07 (tolerance: < 1.00e+00)

**Summary Statistics** (Common Observations):

| Statistic  |          Stata |         Python |     Difference | Std Difference |
|------------|----------------|----------------|----------------|----------------|
| count      |    991320.0000 |    991320.0000 |    991320.0000 |    991320.0000 |
| mean       |        16.8629 |        16.8626 |      -3.11e-04 |      -2.22e-05 |
| std        |        14.0065 |        14.0065 |         0.1603 |         0.0114 |
| min        |      -899.2000 |      -899.2000 |       -87.7100 |        -6.2621 |
| 25%        |        10.5000 |        10.5000 |         0.0000 |         0.0000 |
| 50%        |        15.0000 |        15.0000 |         0.0000 |         0.0000 |
| 75%        |        20.0000 |        20.0000 |         0.0000 |         0.0000 |
| max        |      2097.8000 |      2097.8000 |        28.2200 |         2.0148 |

**Regression Analysis** (Python ~ Stata):

- **Model**: python = 0.0008 + 0.9999 * stata
- **R-squared**: 0.9999
- **N observations**: 991,320

| Coefficient |     Estimate |    Std Error | t-statistic |   p-value |
|-------------|--------------|--------------|-------------|----------|
| Intercept   |     8.33e-04 |     2.52e-04 |      3.3074 |     0.001 |
| Slope       |       0.9999 |     1.15e-05 |  87005.4295 |     0.000 |

**Missing Observations Sample**:
```
 index  permno  yyyymm  fgr5yrNoLag
     0   10012  200108        30.00
     1   10012  200109        30.00
     2   10104  202412        12.01
     3   10107  202412        13.95
     4   10137  199709         3.64
     5   10138  200012        15.36
     6   10138  202412         8.10
     7   10145  198403        10.30
     8   10145  198404        10.30
     9   10145  198405        10.00
```

**Feedback**:
- Num observations with std_diff >= TOL_DIFF_1: 768/991320 (0.077%)
- Stata standard deviation: 1.40e+01

---

### grcapx1y

**Status**: ❌ FAILED

**Test Results**:
- Test 1 - Column names: ✅ PASSED
- Test 2 - Superset check: ❌ FAILED (Python missing 26438 Stata observations)
- Test 3 - Precision1 check: ✅ PASSED
- Test 4 - Precision2 check: ✅ PASSED

**Columns**: ['grcapx1y']

**Observations**:
- Stata:  2,427,138
- Python: 2,440,811
- Common: 2,400,700

**Precision1**: 0.010% obs with std_diff >= 1.00e-02 (tolerance: < 10%)

**Precision2**: 99th percentile diff = 1.76e-09 (tolerance: < 1.00e+00)

**Summary Statistics** (Common Observations):

| Statistic  |          Stata |         Python |     Difference | Std Difference |
|------------|----------------|----------------|----------------|----------------|
| count      |       2.40e+06 |       2.40e+06 |       2.40e+06 |       2.40e+06 |
| mean       |         1.7653 |            inf |            inf |            inf |
| std        |       183.8807 |            N/A |            N/A |            N/A |
| min        |     -4687.0000 |     -4687.0000 |      -405.1343 |        -2.2032 |
| 25%        |        -0.2932 |        -0.2932 |      -6.90e-09 |      -3.75e-11 |
| 50%        |         0.0705 |         0.0705 |         0.0000 |         0.0000 |
| 75%        |         0.5721 |         0.5721 |       6.90e-09 |       3.75e-11 |
| max        |     91212.0000 |            inf |            inf |            inf |

**Regression Analysis** (Python ~ Stata):

- **Model**: python = inf + nan * stata
- **R-squared**: nan
- **N observations**: 2,400,700

| Coefficient |     Estimate |    Std Error | t-statistic |   p-value |
|-------------|--------------|--------------|-------------|----------|
| Intercept   |          nan |          nan |         nan |       nan |
| Slope       |          nan |          nan |         nan |       nan |

**Missing Observations Sample**:
```
 index  permno  yyyymm  grcapx1y
     0   10001  200812  0.047433
     1   10001  200901  0.047433
     2   10001  200902  0.047433
     3   10001  200903  0.047433
     4   10001  200904  0.047433
     5   10001  200905  0.047433
     6   10002  199706 19.634615
     7   10002  199707 19.634615
     8   10002  199708 19.634615
     9   10002  199709 19.634615
```

**Feedback**:
- Num observations with std_diff >= TOL_DIFF_1: 244/2400700 (0.010%)
- Stata standard deviation: 1.84e+02

---

### nanalyst

**Status**: ✅ PASSED

**Test Results**:
- Test 1 - Column names: ✅ PASSED
- Test 2 - Superset check: ✅ PASSED
- Test 3 - Precision1 check: ✅ PASSED
- Test 4 - Precision2 check: ✅ PASSED

**Columns**: ['nanalyst']

**Observations**:
- Stata:  2,700,302
- Python: 4,047,630
- Common: 2,700,302

**Precision1**: 1.246% obs with std_diff >= 1.00e-02 (tolerance: < 10%)

**Precision2**: 99th percentile diff = 2.98e-01 (tolerance: < 1.00e+00)

**Summary Statistics** (Common Observations):

| Statistic  |          Stata |         Python |     Difference | Std Difference |
|------------|----------------|----------------|----------------|----------------|
| count      |       2.70e+06 |       2.69e+06 |       2.69e+06 |       2.69e+06 |
| mean       |         5.1509 |         5.1533 |         0.0042 |       6.29e-04 |
| std        |         6.7163 |         6.7181 |         1.0988 |         0.1636 |
| min        |         0.0000 |         0.0000 |       -62.0000 |        -9.2312 |
| 25%        |         0.0000 |         0.0000 |         0.0000 |         0.0000 |
| 50%        |         3.0000 |         3.0000 |         0.0000 |         0.0000 |
| 75%        |         7.0000 |         7.0000 |         0.0000 |         0.0000 |
| max        |        62.0000 |        59.0000 |        35.0000 |         5.2112 |

**Regression Analysis** (Python ~ Stata):

- **Model**: python = 0.0734 + 0.9866 * stata
- **R-squared**: 0.9734
- **N observations**: 2,689,688

| Coefficient |     Estimate |    Std Error | t-statistic |   p-value |
|-------------|--------------|--------------|-------------|----------|
| Intercept   |       0.0734 |     8.41e-04 |     87.2427 |     0.000 |
| Slope       |       0.9866 |     9.94e-05 |   9926.3522 |     0.000 |

**Feedback**:
- Num observations with std_diff >= TOL_DIFF_1: 33637/2700302 (1.246%)
- Stata standard deviation: 6.72e+00

---

### pchcurrat

**Status**: ❌ FAILED

**Test Results**:
- Test 1 - Column names: ✅ PASSED
- Test 2 - Superset check: ❌ FAILED (Python missing 36014 Stata observations)
- Test 3 - Precision1 check: ✅ PASSED
- Test 4 - Precision2 check: ✅ PASSED

**Columns**: ['pchcurrat']

**Observations**:
- Stata:  3,624,363
- Python: 3,590,797
- Common: 3,588,349

**Precision1**: 0.049% obs with std_diff >= 1.00e-02 (tolerance: < 10%)

**Precision2**: 99th percentile diff = 9.73e-09 (tolerance: < 1.00e+00)

**Summary Statistics** (Common Observations):

| Statistic  |          Stata |         Python |     Difference | Std Difference |
|------------|----------------|----------------|----------------|----------------|
| count      |       3.59e+06 |       3.59e+06 |       3.59e+06 |       3.59e+06 |
| mean       |         0.1897 |            inf |            inf |            inf |
| std        |        20.5071 |            N/A |            N/A |            N/A |
| min        |        -1.0000 |        -1.0000 |        -0.1094 |        -0.0053 |
| 25%        |        -0.1217 |        -0.1217 |      -2.16e-08 |      -1.05e-09 |
| 50%        |         0.0000 |         0.0000 |         0.0000 |         0.0000 |
| 75%        |         0.0809 |         0.0814 |       2.16e-08 |       1.05e-09 |
| max        |      8289.6123 |            inf |            inf |            inf |

**Regression Analysis** (Python ~ Stata):

- **Model**: python = inf + -inf * stata
- **R-squared**: nan
- **N observations**: 3,588,349

| Coefficient |     Estimate |    Std Error | t-statistic |   p-value |
|-------------|--------------|--------------|-------------|----------|
| Intercept   |          nan |          nan |         nan |       nan |
| Slope       |          nan |          nan |         nan |       nan |

**Missing Observations Sample**:
```
 index  permno  yyyymm  pchcurrat
     0   10055  198910        0.0
     1   10055  198911        0.0
     2   10055  198912        0.0
     3   10055  199001        0.0
     4   10055  199002        0.0
     5   10055  199003        0.0
     6   10055  199004        0.0
     7   10055  199005        0.0
     8   10055  199006        0.0
     9   10055  199007        0.0
```

**Feedback**:
- Num observations with std_diff >= TOL_DIFF_1: 1758/3588349 (0.049%)
- Stata standard deviation: 2.05e+01

---

### pchdepr

**Status**: ✅ PASSED

**Test Results**:
- Test 1 - Column names: ✅ PASSED
- Test 2 - Superset check: ✅ PASSED
- Test 3 - Precision1 check: ✅ PASSED
- Test 4 - Precision2 check: ✅ PASSED

**Columns**: ['pchdepr']

**Observations**:
- Stata:  3,050,498
- Python: 3,269,992
- Common: 3,050,498

**Precision1**: 0.005% obs with std_diff >= 1.00e-02 (tolerance: < 10%)

**Precision2**: 99th percentile diff = 2.34e-09 (tolerance: < 1.00e+00)

**Summary Statistics** (Common Observations):

| Statistic  |          Stata |         Python |     Difference | Std Difference |
|------------|----------------|----------------|----------------|----------------|
| count      |       3.05e+06 |       3.05e+06 |       3.05e+06 |       3.05e+06 |
| mean       |         0.4972 |         0.4971 |      -9.16e-05 |      -2.37e-06 |
| std        |        38.5912 |        38.5913 |         0.0378 |       9.78e-04 |
| min        |       -75.5903 |       -75.5903 |       -18.3420 |        -0.4753 |
| 25%        |        -0.0906 |        -0.0906 |      -2.22e-09 |      -5.75e-11 |
| 50%        |         0.0251 |         0.0251 |         0.0000 |         0.0000 |
| 75%        |         0.1646 |         0.1646 |       2.22e-09 |       5.76e-11 |
| max        |     15513.7030 |     15513.7034 |         1.3903 |         0.0360 |

**Regression Analysis** (Python ~ Stata):

- **Model**: python = -0.0001 + 1.0000 * stata
- **R-squared**: 1.0000
- **N observations**: 3,050,486

| Coefficient |     Estimate |    Std Error | t-statistic |   p-value |
|-------------|--------------|--------------|-------------|----------|
| Intercept   |    -9.11e-05 |     2.16e-05 |     -4.2145 |     0.000 |
| Slope       |       1.0000 |     5.60e-07 |    1.79e+06 |     0.000 |

**Feedback**:
- Num observations with std_diff >= TOL_DIFF_1: 144/3050498 (0.005%)
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
- Python: 3,232,762
- Common: 3,222,544

**Precision1**: 0.004% obs with std_diff >= 1.00e-02 (tolerance: < 10%)

**Precision2**: 99th percentile diff = 2.76e-09 (tolerance: < 1.00e+00)

**Summary Statistics** (Common Observations):

| Statistic  |          Stata |         Python |     Difference | Std Difference |
|------------|----------------|----------------|----------------|----------------|
| count      |       3.22e+06 |       3.22e+06 |       3.22e+06 |       3.22e+06 |
| mean       |        -0.7243 |        -0.7244 |      -4.55e-05 |      -5.78e-07 |
| std        |        78.7275 |        78.7275 |         0.0451 |       5.73e-04 |
| min        |    -27624.8850 |    -27624.8841 |       -13.5667 |        -0.1723 |
| 25%        |        -0.0812 |        -0.0812 |      -1.28e-09 |      -1.62e-11 |
| 50%        |        -0.0029 |        -0.0029 |         0.0000 |         0.0000 |
| 75%        |         0.0636 |         0.0636 |       1.29e-09 |       1.63e-11 |
| max        |      5139.5205 |      5139.5206 |         7.1747 |         0.0911 |

**Regression Analysis** (Python ~ Stata):

- **Model**: python = -0.0000 + 1.0000 * stata
- **R-squared**: 1.0000
- **N observations**: 3,222,544

| Coefficient |     Estimate |    Std Error | t-statistic |   p-value |
|-------------|--------------|--------------|-------------|----------|
| Intercept   |    -4.56e-05 |     2.51e-05 |     -1.8137 |     0.070 |
| Slope       |       1.0000 |     3.19e-07 |    3.13e+06 |     0.000 |

**Feedback**:
- Num observations with std_diff >= TOL_DIFF_1: 144/3222544 (0.004%)
- Stata standard deviation: 7.87e+01

---

### pchquick

**Status**: ✅ PASSED

**Test Results**:
- Test 1 - Column names: ✅ PASSED
- Test 2 - Superset check: ✅ PASSED
- Test 3 - Precision1 check: ✅ PASSED
- Test 4 - Precision2 check: ✅ PASSED

**Columns**: ['pchquick']

**Observations**:
- Stata:  3,339,639
- Python: 3,657,513
- Common: 3,339,639

**Precision1**: 0.000% obs with std_diff >= 1.00e-02 (tolerance: < 10%)

**Precision2**: 99th percentile diff = 1.96e-09 (tolerance: < 1.00e+00)

**Summary Statistics** (Common Observations):

| Statistic  |          Stata |         Python |     Difference | Std Difference |
|------------|----------------|----------------|----------------|----------------|
| count      |       3.34e+06 |       3.34e+06 |       3.34e+06 |       3.34e+06 |
| mean       |         0.2975 |         0.2975 |      -1.56e-08 |      -3.63e-10 |
| std        |        42.9356 |        42.9356 |       2.76e-04 |       6.42e-06 |
| min        |      -111.5194 |      -111.5194 |        -0.1096 |        -0.0026 |
| 25%        |        -0.1626 |        -0.1626 |      -2.27e-09 |      -5.28e-11 |
| 50%        |         0.0000 |         0.0000 |         0.0000 |         0.0000 |
| 75%        |         0.1243 |         0.1243 |       2.28e-09 |       5.31e-11 |
| max        |     19726.1780 |     19726.1780 |         0.0773 |         0.0018 |

**Regression Analysis** (Python ~ Stata):

- **Model**: python = -0.0000 + 1.0000 * stata
- **R-squared**: 1.0000
- **N observations**: 3,339,639

| Coefficient |     Estimate |    Std Error | t-statistic |   p-value |
|-------------|--------------|--------------|-------------|----------|
| Intercept   |    -1.62e-08 |     1.51e-07 |     -0.1077 |     0.914 |
| Slope       |       1.0000 |     3.51e-09 |    2.85e+08 |     0.000 |

**Feedback**:
- Num observations with std_diff >= TOL_DIFF_1: 0/3339639 (0.000%)
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
- Python: 2,466,706
- Common: 2,465,425

**Precision1**: 0.000% obs with std_diff >= 1.00e-02 (tolerance: < 10%)

**Precision2**: 99th percentile diff = 1.67e-09 (tolerance: < 1.00e+00)

**Summary Statistics** (Common Observations):

| Statistic  |          Stata |         Python |     Difference | Std Difference |
|------------|----------------|----------------|----------------|----------------|
| count      |       2.47e+06 |       2.47e+06 |       2.47e+06 |       2.47e+06 |
| mean       |         0.7658 |         0.7199 |        -0.0459 |      -6.25e-04 |
| std        |        73.4020 |        70.3930 |        20.8029 |         0.2834 |
| min        |     -3126.2041 |     -3126.2041 |     -9429.3242 |      -128.4613 |
| 25%        |        -0.1224 |        -0.1224 |      -2.63e-09 |      -3.59e-11 |
| 50%        |         0.0114 |         0.0114 |       1.63e-12 |       2.23e-14 |
| 75%        |         0.1759 |         0.1759 |       2.67e-09 |       3.63e-11 |
| max        |     28764.0310 |     28764.0303 |         0.0597 |       8.13e-04 |

**Regression Analysis** (Python ~ Stata):

- **Model**: python = 0.0156 + 0.9197 * stata
- **R-squared**: 0.9197
- **N observations**: 2,465,425

| Coefficient |     Estimate |    Std Error | t-statistic |   p-value |
|-------------|--------------|--------------|-------------|----------|
| Intercept   |       0.0156 |       0.0127 |      1.2284 |     0.219 |
| Slope       |       0.9197 |     1.73e-04 |   5313.0942 |     0.000 |

**Feedback**:
- Num observations with std_diff >= TOL_DIFF_1: 12/2465425 (0.000%)
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
- Python: 3,359,810
- Common: 3,065,278

**Precision1**: 0.000% obs with std_diff >= 1.00e-02 (tolerance: < 10%)

**Precision2**: 99th percentile diff = 1.06e-08 (tolerance: < 1.00e+00)

**Summary Statistics** (Common Observations):

| Statistic  |          Stata |         Python |     Difference | Std Difference |
|------------|----------------|----------------|----------------|----------------|
| count      |       3.07e+06 |       3.07e+06 |       3.07e+06 |       3.07e+06 |
| mean       |         2.7309 |         2.7309 |      -1.82e-06 |      -3.21e-08 |
| std        |        56.6440 |        56.6440 |       9.57e-04 |       1.69e-05 |
| min        |       -41.2750 |       -41.2750 |        -0.4710 |        -0.0083 |
| 25%        |         0.8507 |         0.8507 |      -2.56e-08 |      -4.52e-10 |
| 50%        |         1.3264 |         1.3264 |         0.0000 |         0.0000 |
| 75%        |         2.2630 |         2.2630 |       2.57e-08 |       4.54e-10 |
| max        |     25204.0000 |     25204.0000 |         0.0579 |         0.0010 |

**Regression Analysis** (Python ~ Stata):

- **Model**: python = -0.0000 + 1.0000 * stata
- **R-squared**: 1.0000
- **N observations**: 3,065,278

| Coefficient |     Estimate |    Std Error | t-statistic |   p-value |
|-------------|--------------|--------------|-------------|----------|
| Intercept   |    -1.82e-06 |     5.47e-07 |     -3.3277 |     0.001 |
| Slope       |       1.0000 |     9.65e-09 |    1.04e+08 |     0.000 |

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
- Python: 1,253,272
- Common: 1,207,848

**Precision1**: 0.000% obs with std_diff >= 1.00e-02 (tolerance: < 10%)

**Precision2**: 99th percentile diff = 4.09e-09 (tolerance: < 1.00e+00)

**Summary Statistics** (Common Observations):

| Statistic  |          Stata |         Python |     Difference | Std Difference |
|------------|----------------|----------------|----------------|----------------|
| count      |       1.21e+06 |       1.21e+06 |       1.21e+06 |       1.21e+06 |
| mean       |         5.1262 |         5.1262 |      -9.27e-07 |      -4.96e-09 |
| std        |       186.9904 |       186.9904 |       4.62e-04 |       2.47e-06 |
| min        |     -1037.3235 |     -1037.3235 |        -0.1280 |      -6.85e-04 |
| 25%        |         0.0151 |         0.0151 |      -8.68e-10 |      -4.64e-12 |
| 50%        |         0.0509 |         0.0509 |      -2.78e-17 |      -1.48e-19 |
| 75%        |         0.1546 |         0.1546 |       8.73e-10 |       4.67e-12 |
| max        |     42070.6680 |     42070.6667 |         0.0533 |       2.85e-04 |

**Regression Analysis** (Python ~ Stata):

- **Model**: python = -0.0000 + 1.0000 * stata
- **R-squared**: 1.0000
- **N observations**: 1,207,848

| Coefficient |     Estimate |    Std Error | t-statistic |   p-value |
|-------------|--------------|--------------|-------------|----------|
| Intercept   |    -8.57e-07 |     4.21e-07 |     -2.0368 |     0.042 |
| Slope       |       1.0000 |     2.25e-09 |    4.45e+08 |     0.000 |

**Feedback**:
- Num observations with std_diff >= TOL_DIFF_1: 0/1207848 (0.000%)
- Stata standard deviation: 1.87e+02

---

### rd_sale_q

**Status**: ✅ PASSED

**Test Results**:
- Test 1 - Column names: ✅ PASSED
- Test 2 - Superset check: ✅ PASSED
- Test 3 - Precision1 check: ✅ PASSED
- Test 4 - Precision2 check: ✅ PASSED

**Columns**: ['rd_sale_q']

**Observations**:
- Stata:  566,115
- Python: 1,048,156
- Common: 566,115

**Precision1**: 0.001% obs with std_diff >= 1.00e-02 (tolerance: < 10%)

**Precision2**: 99th percentile diff = 6.67e-09 (tolerance: < 1.00e+00)

**Summary Statistics** (Common Observations):

| Statistic  |          Stata |         Python |     Difference | Std Difference |
|------------|----------------|----------------|----------------|----------------|
| count      |    566115.0000 |    566115.0000 |    566115.0000 |    566115.0000 |
| mean       |         7.6746 |         7.6747 |       1.33e-04 |       7.27e-07 |
| std        |       183.2067 |       183.2067 |         0.1055 |       5.76e-04 |
| min        |     -3937.0000 |     -3937.0000 |       -29.0278 |        -0.1584 |
| 25%        |         0.0468 |         0.0468 |      -2.04e-09 |      -1.11e-11 |
| 50%        |         0.1117 |         0.1117 |      -2.22e-16 |      -1.21e-18 |
| 75%        |         0.2509 |         0.2509 |       1.93e-09 |       1.05e-11 |
| max        |     31684.3340 |     31684.3333 |        52.2216 |         0.2850 |

**Regression Analysis** (Python ~ Stata):

- **Model**: python = 0.0001 + 1.0000 * stata
- **R-squared**: 1.0000
- **N observations**: 566,115

| Coefficient |     Estimate |    Std Error | t-statistic |   p-value |
|-------------|--------------|--------------|-------------|----------|
| Intercept   |     1.33e-04 |     1.40e-04 |      0.9462 |     0.344 |
| Slope       |       1.0000 |     7.65e-07 |    1.31e+06 |     0.000 |

**Feedback**:
- Num observations with std_diff >= TOL_DIFF_1: 3/566115 (0.001%)
- Stata standard deviation: 1.83e+02

---

### roavol

**Status**: ❌ FAILED

**Test Results**:
- Test 1 - Column names: ✅ PASSED
- Test 2 - Superset check: ❌ FAILED (Python missing 1 Stata observations)
- Test 3 - Precision1 check: ✅ PASSED
- Test 4 - Precision2 check: ✅ PASSED

**Columns**: ['roavol']

**Observations**:
- Stata:  2,039,901
- Python: 2,159,735
- Common: 2,039,900

**Precision1**: 2.952% obs with std_diff >= 1.00e-02 (tolerance: < 10%)

**Precision2**: 99th percentile diff = 3.49e-02 (tolerance: < 1.00e+00)

**Summary Statistics** (Common Observations):

| Statistic  |          Stata |         Python |     Difference | Std Difference |
|------------|----------------|----------------|----------------|----------------|
| count      |       2.04e+06 |       2.04e+06 |       2.04e+06 |       2.04e+06 |
| mean       |         0.0305 |         0.0313 |       8.67e-04 |         0.0057 |
| std        |         0.1527 |         0.1740 |         0.0828 |         0.5421 |
| min        |       3.49e-05 |       3.49e-05 |        -0.4214 |        -2.7599 |
| 25%        |         0.0056 |         0.0056 |      -2.12e-10 |      -1.39e-09 |
| 50%        |         0.0124 |         0.0125 |      -8.08e-12 |      -5.29e-11 |
| 75%        |         0.0295 |         0.0296 |       1.24e-10 |       8.14e-10 |
| max        |        49.8304 |        49.8304 |        24.9505 |       163.4275 |

**Regression Analysis** (Python ~ Stata):

- **Model**: python = 0.0008 + 1.0027 * stata
- **R-squared**: 0.7738
- **N observations**: 2,039,783

| Coefficient |     Estimate |    Std Error | t-statistic |   p-value |
|-------------|--------------|--------------|-------------|----------|
| Intercept   |     7.86e-04 |     5.91e-05 |     13.2986 |     0.000 |
| Slope       |       1.0027 |     3.80e-04 |   2641.2126 |     0.000 |

**Missing Observations Sample**:
```
 index  permno  yyyymm   roavol
     0   19316  202412 0.020575
```

**Feedback**:
- Num observations with std_diff >= TOL_DIFF_1: 60219/2039900 (2.952%)
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
- Python: 3,412,464
- Common: 3,409,380

**Precision1**: 0.014% obs with std_diff >= 1.00e-02 (tolerance: < 10%)

**Precision2**: 99th percentile diff = 3.65e-23 (tolerance: < 1.00e+00)

**Summary Statistics** (Common Observations):

| Statistic  |          Stata |         Python |     Difference | Std Difference |
|------------|----------------|----------------|----------------|----------------|
| count      |       3.41e+06 |       3.41e+06 |       3.41e+06 |       3.41e+06 |
| mean       |       1.87e+13 |            inf |            inf |            inf |
| std        |       5.82e+15 |            N/A |            N/A |            N/A |
| min        |      -3.62e+17 |      -3.91e+16 |      -3.40e+16 |        -5.8459 |
| 25%        |        -0.0121 |        -0.0121 |      -1.88e-09 |      -3.23e-25 |
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
- Python: 3,617,574
- Common: 3,583,392

**Precision1**: 0.000% obs with std_diff >= 1.00e-02 (tolerance: < 10%)

**Precision2**: 99th percentile diff = 6.63e-09 (tolerance: < 1.00e+00)

**Summary Statistics** (Common Observations):

| Statistic  |          Stata |         Python |     Difference | Std Difference |
|------------|----------------|----------------|----------------|----------------|
| count      |       3.58e+06 |       3.58e+06 |       3.58e+06 |       3.58e+06 |
| mean       |       107.6003 |       107.6001 |      -1.90e-04 |      -7.24e-08 |
| std        |      2627.3839 |      2627.3839 |         0.0830 |       3.16e-05 |
| min        |     -1591.6364 |     -1591.6364 |       -43.5883 |        -0.0166 |
| 25%        |         2.2471 |         2.2470 |      -1.37e-07 |      -5.21e-11 |
| 50%        |         8.4673 |         8.4670 |         0.0000 |         0.0000 |
| 75%        |        30.7168 |        30.7168 |       1.35e-07 |       5.12e-11 |
| max        |    519704.0000 |    519704.0000 |         4.4842 |         0.0017 |

**Regression Analysis** (Python ~ Stata):

- **Model**: python = -0.0002 + 1.0000 * stata
- **R-squared**: 1.0000
- **N observations**: 3,583,392

| Coefficient |     Estimate |    Std Error | t-statistic |   p-value |
|-------------|--------------|--------------|-------------|----------|
| Intercept   |    -1.90e-04 |     4.39e-05 |     -4.3319 |     0.000 |
| Slope       |       1.0000 |     1.67e-08 |    5.99e+07 |     0.000 |

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
- Python: 3,554,029
- Common: 2,730,607

**Precision1**: 0.001% obs with std_diff >= 1.00e-02 (tolerance: < 10%)

**Precision2**: 99th percentile diff = 3.13e-09 (tolerance: < 1.00e+00)

**Summary Statistics** (Common Observations):

| Statistic  |          Stata |         Python |     Difference | Std Difference |
|------------|----------------|----------------|----------------|----------------|
| count      |       2.73e+06 |       2.73e+06 |       2.73e+06 |       2.73e+06 |
| mean       |        61.9969 |        61.9749 |        -0.0220 |      -6.30e-06 |
| std        |      3492.9321 |      3492.9205 |         7.5822 |         0.0022 |
| min        |    -14573.0000 |    -14573.0000 |     -3081.3552 |        -0.8822 |
| 25%        |         4.6053 |         4.6053 |      -1.57e-07 |      -4.49e-11 |
| 50%        |         7.6793 |         7.6787 |         0.0000 |         0.0000 |
| 75%        |        17.8215 |        17.8207 |       1.55e-07 |       4.45e-11 |
| max        |       1.05e+06 |       1.05e+06 |         0.0919 |       2.63e-05 |

**Regression Analysis** (Python ~ Stata):

- **Model**: python = -0.0217 + 1.0000 * stata
- **R-squared**: 1.0000
- **N observations**: 2,730,607

| Coefficient |     Estimate |    Std Error | t-statistic |   p-value |
|-------------|--------------|--------------|-------------|----------|
| Intercept   |      -0.0217 |       0.0046 |     -4.7193 |     0.000 |
| Slope       |       1.0000 |     1.31e-06 | 761240.4084 |     0.000 |

**Feedback**:
- Num observations with std_diff >= TOL_DIFF_1: 24/2730607 (0.001%)
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
- Python: 3,578,875
- Common: 3,451,784

**Precision1**: 0.007% obs with std_diff >= 1.00e-02 (tolerance: < 10%)

**Precision2**: 99th percentile diff = 2.14e-08 (tolerance: < 1.00e+00)

**Summary Statistics** (Common Observations):

| Statistic  |          Stata |         Python |     Difference | Std Difference |
|------------|----------------|----------------|----------------|----------------|
| count      |       3.45e+06 |       3.45e+06 |       3.45e+06 |       3.45e+06 |
| mean       |        16.3739 |        16.3749 |       9.99e-04 |       4.77e-06 |
| std        |       209.4212 |       209.4212 |         0.5576 |         0.0027 |
| min        |    -21796.0000 |    -21796.0000 |      -121.3652 |        -0.5795 |
| 25%        |         3.6746 |         3.6748 |      -1.08e-07 |      -5.16e-10 |
| 50%        |         5.9289 |         5.9292 |         0.0000 |         0.0000 |
| 75%        |         9.1589 |         9.1597 |       1.08e-07 |       5.14e-10 |
| max        |     47246.0000 |     47246.0000 |       269.4239 |         1.2865 |

**Regression Analysis** (Python ~ Stata):

- **Model**: python = 0.0011 + 1.0000 * stata
- **R-squared**: 1.0000
- **N observations**: 3,451,784

| Coefficient |     Estimate |    Std Error | t-statistic |   p-value |
|-------------|--------------|--------------|-------------|----------|
| Intercept   |       0.0011 |     3.01e-04 |      3.4999 |     0.000 |
| Slope       |       1.0000 |     1.43e-06 | 697746.4741 |     0.000 |

**Feedback**:
- Num observations with std_diff >= TOL_DIFF_1: 240/3451784 (0.007%)
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
- Python: 3,626,811
- Common: 3,624,363

**Precision1**: 0.011% obs with std_diff >= 1.00e-02 (tolerance: < 10%)

**Precision2**: 99th percentile diff = 8.39e-08 (tolerance: < 1.00e+00)

**Summary Statistics** (Common Observations):

| Statistic  |          Stata |         Python |     Difference | Std Difference |
|------------|----------------|----------------|----------------|----------------|
| count      |       3.62e+06 |       3.62e+06 |       3.62e+06 |       3.62e+06 |
| mean       |         0.1995 |         0.1995 |       2.43e-06 |       7.03e-06 |
| std        |         0.3454 |         0.3454 |         0.0020 |         0.0059 |
| min        |      -7.96e-05 |      -7.96e-05 |        -0.3067 |        -0.8880 |
| 25%        |         0.0000 |         0.0000 |         0.0000 |         0.0000 |
| 50%        |         0.0000 |         0.0000 |         0.0000 |         0.0000 |
| 75%        |         0.3028 |         0.3029 |         0.0000 |         0.0000 |
| max        |        48.7452 |        48.7452 |         0.7243 |         2.0969 |

**Regression Analysis** (Python ~ Stata):

- **Model**: python = 0.0000 + 1.0000 * stata
- **R-squared**: 1.0000
- **N observations**: 3,624,363

| Coefficient |     Estimate |    Std Error | t-statistic |   p-value |
|-------------|--------------|--------------|-------------|----------|
| Intercept   |     8.23e-06 |     1.23e-06 |      6.7050 |     0.000 |
| Slope       |       1.0000 |     3.08e-06 | 325036.5301 |     0.000 |

**Feedback**:
- Num observations with std_diff >= TOL_DIFF_1: 384/3624363 (0.011%)
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
- Python: 3,626,811
- Common: 3,624,363

**Precision1**: 0.006% obs with std_diff >= 1.00e-02 (tolerance: < 10%)

**Precision2**: 99th percentile diff = 0.00e+00 (tolerance: < 1.00e+00)

**Summary Statistics** (Common Observations):

| Statistic  |          Stata |         Python |     Difference | Std Difference |
|------------|----------------|----------------|----------------|----------------|
| count      |       3.62e+06 |       3.62e+06 |       3.62e+06 |       3.62e+06 |
| mean       |         0.4092 |         0.4092 |       4.30e-05 |       8.75e-05 |
| std        |         0.4917 |         0.4917 |         0.0079 |         0.0161 |
| min        |         0.0000 |         0.0000 |        -1.0000 |        -2.0338 |
| 25%        |         0.0000 |         0.0000 |         0.0000 |         0.0000 |
| 50%        |         0.0000 |         0.0000 |         0.0000 |         0.0000 |
| 75%        |         1.0000 |         1.0000 |         0.0000 |         0.0000 |
| max        |         1.0000 |         1.0000 |         1.0000 |         2.0338 |

**Regression Analysis** (Python ~ Stata):

- **Model**: python = 0.0001 + 0.9999 * stata
- **R-squared**: 0.9997
- **N observations**: 3,624,363

| Coefficient |     Estimate |    Std Error | t-statistic |   p-value |
|-------------|--------------|--------------|-------------|----------|
| Intercept   |     8.97e-05 |     5.42e-06 |     16.5431 |     0.000 |
| Slope       |       0.9999 |     8.47e-06 | 118008.7505 |     0.000 |

**Feedback**:
- Num observations with std_diff >= TOL_DIFF_1: 228/3624363 (0.006%)
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
- Python: 3,233,534
- Common: 3,231,761

**Precision1**: 0.001% obs with std_diff >= 1.00e-02 (tolerance: < 10%)

**Precision2**: 99th percentile diff = 1.89e-09 (tolerance: < 1.00e+00)

**Summary Statistics** (Common Observations):

| Statistic  |          Stata |         Python |     Difference | Std Difference |
|------------|----------------|----------------|----------------|----------------|
| count      |       3.23e+06 |       3.23e+06 |       3.23e+06 |       3.23e+06 |
| mean       |         0.7025 |         0.7024 |      -9.67e-06 |      -2.06e-07 |
| std        |        46.9281 |        46.9281 |         0.0086 |       1.84e-04 |
| min        |      -237.0000 |      -237.0000 |        -4.0617 |        -0.0866 |
| 25%        |        -0.0210 |        -0.0210 |      -2.50e-09 |      -5.32e-11 |
| 50%        |         0.0863 |         0.0863 |         0.0000 |         0.0000 |
| 75%        |         0.2252 |         0.2252 |       2.53e-09 |       5.39e-11 |
| max        |     12739.0000 |     12739.0000 |         1.2280 |         0.0262 |

**Regression Analysis** (Python ~ Stata):

- **Model**: python = -0.0000 + 1.0000 * stata
- **R-squared**: 1.0000
- **N observations**: 3,231,761

| Coefficient |     Estimate |    Std Error | t-statistic |   p-value |
|-------------|--------------|--------------|-------------|----------|
| Intercept   |    -9.65e-06 |     4.79e-06 |     -2.0144 |     0.044 |
| Slope       |       1.0000 |     1.02e-07 |    9.79e+06 |     0.000 |

**Feedback**:
- Num observations with std_diff >= TOL_DIFF_1: 48/3231761 (0.001%)
- Stata standard deviation: 4.69e+01

---

### sgr_q

**Status**: ❌ FAILED

**Test Results**:
- Test 1 - Column names: ✅ PASSED
- Test 2 - Superset check: ❌ FAILED (Python missing 57 Stata observations)
- Test 3 - Precision1 check: ✅ PASSED
- Test 4 - Precision2 check: ✅ PASSED

**Columns**: ['sgr_q']

**Observations**:
- Stata:  2,457,701
- Python: 2,457,747
- Common: 2,457,644

**Precision1**: 0.002% obs with std_diff >= 1.00e-02 (tolerance: < 10%)

**Precision2**: 99th percentile diff = 3.08e-10 (tolerance: < 1.00e+00)

**Summary Statistics** (Common Observations):

| Statistic  |          Stata |         Python |     Difference | Std Difference |
|------------|----------------|----------------|----------------|----------------|
| count      |       2.46e+06 |       2.46e+06 |       2.46e+06 |       2.46e+06 |
| mean       |         1.0671 |         1.0670 |      -1.78e-04 |      -6.22e-07 |
| std        |       286.5311 |       286.5312 |         0.2027 |       7.08e-04 |
| min        |     -3092.0000 |     -3092.0000 |      -146.0200 |        -0.5096 |
| 25%        |        -0.0374 |        -0.0374 |      -2.58e-09 |      -9.00e-12 |
| 50%        |         0.0794 |         0.0794 |         0.0000 |         0.0000 |
| 75%        |         0.2229 |         0.2229 |       2.55e-09 |       8.91e-12 |
| max        |    251440.0000 |    251440.0000 |       187.2391 |         0.6535 |

**Regression Analysis** (Python ~ Stata):

- **Model**: python = -0.0002 + 1.0000 * stata
- **R-squared**: 1.0000
- **N observations**: 2,457,644

| Coefficient |     Estimate |    Std Error | t-statistic |   p-value |
|-------------|--------------|--------------|-------------|----------|
| Intercept   |    -1.78e-04 |     1.29e-04 |     -1.3772 |     0.168 |
| Slope       |       1.0000 |     4.51e-07 |    2.22e+06 |     0.000 |

**Missing Observations Sample**:
```
 index  permno  yyyymm     sgr_q
     0   11545  199706  0.241882
     1   11545  199707  0.241882
     2   11545  199708  0.241882
     3   11545  199806  1.767560
     4   11545  199807  1.767560
     5   11545  199808  1.767560
     6   12113  200006  0.008898
     7   12113  200007  0.008898
     8   12113  200008  0.008898
     9   12113  200106 -0.276953
```

**Feedback**:
- Num observations with std_diff >= TOL_DIFF_1: 47/2457644 (0.002%)
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
- Python: 2,822,888
- Common: 1,675,095

**Precision1**: 0.015% obs with std_diff >= 1.00e-02 (tolerance: < 10%)

**Precision2**: 99th percentile diff = 1.55e-07 (tolerance: < 1.00e+00)

**Summary Statistics** (Common Observations):

| Statistic  |          Stata |         Python |     Difference | Std Difference |
|------------|----------------|----------------|----------------|----------------|
| count      |       1.68e+06 |       1.68e+06 |       1.68e+06 |       1.68e+06 |
| mean       |         0.6565 |         0.6569 |       3.17e-04 |       9.20e-04 |
| std        |         0.3446 |         0.4379 |         0.2704 |         0.7846 |
| min        |        -0.4077 |        -0.4077 |        -0.8573 |        -2.4879 |
| 25%        |         0.5451 |         0.5451 |      -1.26e-08 |      -3.66e-08 |
| 50%        |         0.6594 |         0.6594 |       2.87e-11 |       8.34e-11 |
| 75%        |         0.7667 |         0.7667 |       1.27e-08 |       3.68e-08 |
| max        |       158.7655 |       339.2011 |       338.7035 |       982.8918 |

**Regression Analysis** (Python ~ Stata):

- **Model**: python = 0.0005 + 0.9996 * stata
- **R-squared**: 0.6188
- **N observations**: 1,675,095

| Coefficient |     Estimate |    Std Error | t-statistic |   p-value |
|-------------|--------------|--------------|-------------|----------|
| Intercept   |     5.48e-04 |     4.50e-04 |      1.2193 |     0.223 |
| Slope       |       0.9996 |     6.06e-04 |   1648.9844 |     0.000 |

**Missing Observations Sample**:
```
 index  permno  yyyymm   tang_q
     0   12113  200006 0.625689
     1   19316  202412 0.562276
     2   85570  199608 0.551519
```

**Feedback**:
- Num observations with std_diff >= TOL_DIFF_1: 250/1675095 (0.015%)
- Stata standard deviation: 3.45e-01

---

