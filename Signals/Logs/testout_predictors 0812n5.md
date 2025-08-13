# Predictor Validation Results

**Generated**: 2025-08-12 19:43:16

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
| Recomm_ShortInterest      | ✅         | ✅       | ❌ (55.76%)  | ✅ (0.00%)    | ✅ (99th diff 0.0E+00)   |
| PatentsRD                 | ✅         | ✅       | ❌ (29.14%)  | ❌ (15.70%)   | ❌ (99th diff 1.0E+00)   |
| FirmAgeMom                | ✅         | ✅       | ❌ (26.99%)  | ✅ (0.00%)    | ✅ (99th diff 3.6E-08)   |
| retConglomerate           | ✅         | ✅       | ❌ (22.32%)  | ❌ (94.06%)   | ❌ (99th diff 1.7E-01)   |
| Mom6mJunk                 | ✅         | ✅       | ❌ (18.09%)  | ✅ (0.28%)    | ✅ (99th diff 3.9E-08)   |
| sinAlgo                   | ✅         | ✅       | ❌ (15.87%)  | ✅ (0.01%)    | ✅ (99th diff 0.0E+00)   |
| RDAbility                 | ✅         | ✅       | ❌ (4.95%)   | ✅ (9.52%)    | ❌ (99th diff 5.2E+00)   |
| RIO_Volatility            | ✅         | ✅       | ❌ (4.44%)   | ✅ (4.32%)    | ❌ (99th diff 1.0E+00)   |
| IdioVolAHT                | ✅         | ✅       | ❌ (3.82%)   | ❌ (17.59%)   | ❌ (99th diff 5.3E-03)   |
| EarnSupBig                | ✅         | ✅       | ❌ (3.76%)   | ✅ (0.16%)    | ❌ (99th diff 6.5E+00)   |
| DownRecomm                | ✅         | ✅       | ❌ (3.19%)   | ✅ (0.03%)    | ✅ (99th diff 0.0E+00)   |
| UpRecomm                  | ✅         | ✅       | ❌ (3.19%)   | ✅ (0.02%)    | ✅ (99th diff 0.0E+00)   |
| MomRev                    | ✅         | ✅       | ❌ (1.31%)   | ✅ (0.00%)    | ✅ (99th diff 0.0E+00)   |
| TrendFactor               | ✅         | ✅       | ✅ (0.07%)   | ❌ (97.15%)   | ❌ (99th diff 2.6E-01)   |
| PredictedFE               | ✅         | ✅       | ✅ (0.27%)   | ❌ (93.91%)   | ❌ (99th diff 1.4E-02)   |
| Frontier                  | ✅         | ✅       | ✅ (0.00%)   | ❌ (84.22%)   | ❌ (99th diff 5.4E-01)   |
| MS                        | ✅         | ✅       | ✅ (0.00%)   | ❌ (63.45%)   | ❌ (99th diff 4.0E+00)   |
| AbnormalAccruals          | ✅         | ✅       | ✅ (0.68%)   | ❌ (27.95%)   | ❌ (99th diff 5.2E-02)   |
| PriceDelayTstat           | ✅         | ✅       | ✅ (0.00%)   | ❌ (19.38%)   | ❌ (99th diff 6.1E+00)   |
| PS                        | ✅         | ✅       | ✅ (0.00%)   | ❌ (17.90%)   | ❌ (99th diff 5.0E+00)   |
| ShareVol                  | ✅         | ✅       | ✅ (0.03%)   | ❌ (14.38%)   | ❌ (99th diff 1.0E+00)   |
| OrgCap                    | ✅         | ✅       | ✅ (0.00%)   | ❌ (14.23%)   | ❌ (99th diff 1.3E-01)   |
| IndRetBig                 | ✅         | ✅       | ✅ (0.25%)   | ✅ (7.12%)    | ❌ (99th diff 8.8E-03)   |
| BetaFP                    | ✅         | ✅       | ✅ (0.54%)   | ✅ (5.98%)    | ❌ (99th diff 5.7E-02)   |
| DivSeason                 | ✅         | ✅       | ✅ (0.00%)   | ✅ (5.21%)    | ❌ (99th diff 1.0E+00)   |
| BetaTailRisk              | ✅         | ✅       | ✅ (0.00%)   | ✅ (4.15%)    | ❌ (99th diff 1.0E-02)   |
| RIO_Disp                  | ✅         | ✅       | ✅ (0.26%)   | ✅ (3.79%)    | ❌ (99th diff 1.0E+00)   |
| RIO_Turnover              | ✅         | ✅       | ✅ (0.15%)   | ✅ (3.65%)    | ❌ (99th diff 1.0E+00)   |
| RIO_MB                    | ✅         | ✅       | ✅ (0.18%)   | ✅ (3.45%)    | ❌ (99th diff 1.0E+00)   |
| IndMom                    | ✅         | ✅       | ✅ (0.00%)   | ✅ (3.28%)    | ❌ (99th diff 5.1E-02)   |
| ReturnSkew3F              | ✅         | ✅       | ✅ (0.00%)   | ✅ (2.68%)    | ❌ (99th diff 2.3E-02)   |
| HerfAsset                 | ✅         | ✅       | ✅ (0.00%)   | ✅ (1.44%)    | ❌ (99th diff 8.2E-03)   |
| VolumeTrend               | ✅         | ✅       | ✅ (0.00%)   | ✅ (1.36%)    | ❌ (99th diff 1.9E-03)   |
| Tax                       | ✅         | ✅       | ✅ (0.00%)   | ✅ (1.24%)    | ❌ (99th diff 6.1E-01)   |
| PriceDelayRsq             | ✅         | ✅       | ✅ (0.00%)   | ✅ (1.21%)    | ❌ (99th diff 6.1E-02)   |
| MomOffSeason              | ✅         | ✅       | ✅ (0.00%)   | ✅ (1.06%)    | ✅ (99th diff 9.5E-04)   |
| NumEarnIncrease           | ✅         | ✅       | ✅ (0.00%)   | ✅ (1.01%)    | ❌ (99th diff 1.0E+00)   |
| Investment                | ✅         | ✅       | ✅ (0.00%)   | ✅ (1.00%)    | ❌ (99th diff 1.8E-02)   |
| CredRatDG                 | ✅         | ✅       | ✅ (0.00%)   | ✅ (0.94%)    | ✅ (99th diff 0.0E+00)   |
| MomOffSeason06YrPlus      | ✅         | ✅       | ✅ (0.00%)   | ✅ (0.92%)    | ✅ (99th diff 1.0E-08)   |
| MomOffSeason11YrPlus      | ✅         | ✅       | ✅ (0.00%)   | ✅ (0.88%)    | ✅ (99th diff 8.2E-09)   |
| Herf                      | ✅         | ✅       | ✅ (0.00%)   | ✅ (0.79%)    | ✅ (99th diff 1.9E-04)   |
| ResidualMomentum          | ✅         | ✅       | ✅ (0.00%)   | ✅ (0.70%)    | ❌ (99th diff 2.8E-03)   |
| PriceDelaySlope           | ✅         | ✅       | ✅ (0.00%)   | ✅ (0.58%)    | ❌ (99th diff 7.3E-01)   |
| MomOffSeason16YrPlus      | ✅         | ✅       | ✅ (0.00%)   | ✅ (0.51%)    | ✅ (99th diff 3.4E-09)   |
| MomVol                    | ✅         | ✅       | ✅ (0.00%)   | ✅ (0.42%)    | ✅ (99th diff 0.0E+00)   |
| BetaLiquidityPS           | ✅         | ✅       | ✅ (0.00%)   | ✅ (0.31%)    | ❌ (99th diff 2.4E-03)   |
| AnalystValue              | ✅         | ✅       | ✅ (0.22%)   | ✅ (0.26%)    | ❌ (99th diff 1.8E-02)   |
| Mom12mOffSeason           | ✅         | ✅       | ✅ (0.00%)   | ✅ (0.17%)    | ✅ (99th diff 5.9E-17)   |
| REV6                      | ✅         | ✅       | ✅ (0.00%)   | ✅ (0.17%)    | ❌ (99th diff 8.0E-02)   |
| IntanEP                   | ✅         | ✅       | ✅ (0.00%)   | ✅ (0.15%)    | ✅ (99th diff 2.8E-07)   |
| IntanCFP                  | ✅         | ✅       | ✅ (0.00%)   | ✅ (0.15%)    | ✅ (99th diff 2.2E-05)   |
| MRreversal                | ✅         | ✅       | ✅ (0.00%)   | ✅ (0.15%)    | ✅ (99th diff 5.6E-08)   |
| realestate                | ✅         | ✅       | ✅ (0.00%)   | ✅ (0.14%)    | ✅ (99th diff 4.1E-08)   |
| LRreversal                | ✅         | ✅       | ✅ (0.00%)   | ✅ (0.12%)    | ✅ (99th diff 1.3E-07)   |
| ChForecastAccrual         | ✅         | ✅       | ✅ (0.00%)   | ✅ (0.12%)    | ✅ (99th diff 0.0E+00)   |
| ExclExp                   | ✅         | ✅       | ✅ (0.12%)   | ✅ (0.11%)    | ✅ (99th diff 3.0E-08)   |
| EarningsForecastDisparity | ✅         | ✅       | ✅ (0.22%)   | ✅ (0.08%)    | ✅ (99th diff 2.0E-05)   |
| ForecastDispersion        | ✅         | ✅       | ✅ (0.16%)   | ✅ (0.07%)    | ✅ (99th diff 5.7E-08)   |
| fgr5yrLag                 | ✅         | ✅       | ✅ (0.22%)   | ✅ (0.07%)    | ✅ (99th diff 2.0E-06)   |
| DivYieldST                | ✅         | ✅       | ✅ (0.00%)   | ✅ (0.07%)    | ✅ (99th diff 0.0E+00)   |
| Cash                      | ✅         | ✅       | ✅ (0.00%)   | ✅ (0.06%)    | ✅ (99th diff 2.7E-08)   |
| RIVolSpread               | ✅         | ✅       | ✅ (0.71%)   | ✅ (0.05%)    | ✅ (99th diff 7.5E-08)   |
| CPVolSpread               | ✅         | ✅       | ✅ (0.74%)   | ✅ (0.05%)    | ✅ (99th diff 4.0E-09)   |
| ChangeInRecommendation    | ✅         | ✅       | ✅ (0.23%)   | ✅ (0.05%)    | ✅ (99th diff 1.7E-07)   |
| OptionVolume2             | ✅         | ✅       | ✅ (0.72%)   | ✅ (0.05%)    | ✅ (99th diff 3.5E-07)   |
| ExchSwitch                | ✅         | ✅       | ✅ (0.00%)   | ✅ (0.05%)    | ✅ (99th diff 0.0E+00)   |
| skew1                     | ✅         | ✅       | ✅ (0.71%)   | ✅ (0.04%)    | ✅ (99th diff 1.0E-08)   |
| dVolPut                   | ✅         | ✅       | ✅ (0.71%)   | ✅ (0.04%)    | ✅ (99th diff 3.0E-08)   |
| OptionVolume1             | ✅         | ✅       | ✅ (0.72%)   | ✅ (0.04%)    | ✅ (99th diff 1.9E-04)   |
| dVolCall                  | ✅         | ✅       | ✅ (0.71%)   | ✅ (0.04%)    | ✅ (99th diff 3.0E-08)   |
| betaVIX                   | ✅         | ✅       | ✅ (0.00%)   | ✅ (0.04%)    | ✅ (99th diff 2.3E-05)   |
| AnalystRevision           | ✅         | ✅       | ✅ (0.16%)   | ✅ (0.04%)    | ✅ (99th diff 9.5E-08)   |
| SmileSlope                | ✅         | ✅       | ✅ (0.71%)   | ✅ (0.04%)    | ✅ (99th diff 2.0E-08)   |
| dCPVolSpread              | ✅         | ✅       | ✅ (0.71%)   | ✅ (0.04%)    | ✅ (99th diff 3.0E-08)   |
| iomom_cust                | ✅         | ✅       | ✅ (0.00%)   | ✅ (0.03%)    | ❌ (99th diff 1.0E-03)   |
| BM                        | ✅         | ✅       | ✅ (0.00%)   | ✅ (0.03%)    | ✅ (99th diff 1.3E-07)   |
| EarningsSurprise          | ✅         | ✅       | ✅ (0.02%)   | ✅ (0.03%)    | ✅ (99th diff 6.4E-07)   |
| FEPS                      | ✅         | ✅       | ✅ (0.16%)   | ✅ (0.03%)    | ✅ (99th diff 2.0E-07)   |
| sfe                       | ✅         | ✅       | ✅ (0.20%)   | ✅ (0.02%)    | ✅ (99th diff 2.6E-08)   |
| IdioVol3F                 | ✅         | ✅       | ✅ (0.00%)   | ✅ (0.02%)    | ✅ (99th diff 4.6E-05)   |
| iomom_supp                | ✅         | ✅       | ✅ (0.00%)   | ✅ (0.02%)    | ✅ (99th diff 8.1E-04)   |
| ConsRecomm                | ✅         | ✅       | ✅ (0.23%)   | ✅ (0.01%)    | ✅ (99th diff 0.0E+00)   |
| IntanBM                   | ✅         | ✅       | ✅ (0.00%)   | ✅ (0.01%)    | ✅ (99th diff 2.8E-07)   |
| DelDRC                    | ✅         | ✅       | ✅ (0.00%)   | ✅ (0.01%)    | ✅ (99th diff 5.4E-09)   |
| VolSD                     | ✅         | ✅       | ✅ (0.02%)   | ✅ (0.01%)    | ✅ (99th diff 3.3E-13)   |
| RevenueSurprise           | ✅         | ✅       | ✅ (0.00%)   | ✅ (0.01%)    | ✅ (99th diff 6.0E-06)   |
| DelNetFin                 | ✅         | ✅       | ✅ (0.00%)   | ✅ (0.01%)    | ✅ (99th diff 5.5E-08)   |
| Accruals                  | ✅         | ✅       | ✅ (0.00%)   | ✅ (0.01%)    | ✅ (99th diff 1.4E-08)   |
| IntanSP                   | ✅         | ✅       | ✅ (0.00%)   | ✅ (0.01%)    | ✅ (99th diff 6.7E-07)   |
| VolMkt                    | ✅         | ✅       | ✅ (0.02%)   | ✅ (0.01%)    | ✅ (99th diff 7.8E-08)   |
| hire                      | ✅         | ✅       | ✅ (0.00%)   | ✅ (0.01%)    | ✅ (99th diff 3.0E-08)   |
| DivInit                   | ✅         | ✅       | ✅ (0.00%)   | ✅ (0.01%)    | ✅ (99th diff 0.0E+00)   |
| ChNNCOA                   | ✅         | ✅       | ✅ (0.00%)   | ✅ (0.01%)    | ✅ (99th diff 4.7E-08)   |
| EarningsStreak            | ✅         | ✅       | ✅ (0.19%)   | ✅ (0.01%)    | ✅ (99th diff 7.8E-09)   |
| roaq                      | ✅         | ✅       | ✅ (0.00%)   | ✅ (0.01%)    | ✅ (99th diff 9.8E-09)   |
| ChNAnalyst                | ✅         | ✅       | ✅ (0.11%)   | ✅ (0.01%)    | ✅ (99th diff 0.0E+00)   |
| CustomerMomentum          | ✅         | ✅       | ✅ (0.04%)   | ✅ (0.01%)    | ✅ (99th diff 1.0E-08)   |
| CompositeDebtIssuance     | ✅         | ✅       | ✅ (0.00%)   | ✅ (0.01%)    | ✅ (99th diff 1.8E-07)   |
| DelCOL                    | ✅         | ✅       | ✅ (0.00%)   | ✅ (0.01%)    | ✅ (99th diff 1.7E-08)   |
| GP                        | ✅         | ✅       | ✅ (0.00%)   | ✅ (0.01%)    | ✅ (99th diff 5.1E-08)   |
| DelFINL                   | ✅         | ✅       | ✅ (0.00%)   | ✅ (0.01%)    | ✅ (99th diff 3.1E-08)   |
| CBOperProf                | ✅         | ✅       | ✅ (0.00%)   | ✅ (0.01%)    | ✅ (99th diff 2.9E-08)   |
| DelLTI                    | ✅         | ✅       | ✅ (0.00%)   | ✅ (0.01%)    | ✅ (99th diff 1.4E-08)   |
| SurpriseRD                | ✅         | ✅       | ✅ (0.00%)   | ✅ (0.01%)    | ✅ (99th diff 0.0E+00)   |
| dNoa                      | ✅         | ✅       | ✅ (0.00%)   | ✅ (0.00%)    | ✅ (99th diff 1.4E-07)   |
| ChNWC                     | ✅         | ✅       | ✅ (0.00%)   | ✅ (0.00%)    | ✅ (99th diff 3.6E-08)   |
| NOA                       | ✅         | ✅       | ✅ (0.00%)   | ✅ (0.00%)    | ✅ (99th diff 1.1E-07)   |
| AnnouncementReturn        | ✅         | ✅       | ✅ (0.00%)   | ✅ (0.00%)    | ✅ (99th diff 2.0E-08)   |
| DivOmit                   | ✅         | ✅       | ✅ (0.00%)   | ✅ (0.00%)    | ✅ (99th diff 0.0E+00)   |
| NetDebtFinance            | ✅         | ✅       | ✅ (0.00%)   | ✅ (0.00%)    | ✅ (99th diff 1.4E-08)   |
| OperProfRD                | ✅         | ✅       | ✅ (0.00%)   | ✅ (0.00%)    | ✅ (99th diff 2.3E-08)   |
| OPLeverage                | ✅         | ✅       | ✅ (0.00%)   | ✅ (0.00%)    | ✅ (99th diff 1.4E-07)   |
| XFIN                      | ✅         | ✅       | ✅ (0.00%)   | ✅ (0.00%)    | ✅ (99th diff 3.3E-08)   |
| tang                      | ✅         | ✅       | ✅ (0.02%)   | ✅ (0.00%)    | ✅ (99th diff 4.5E-08)   |
| ShareRepurchase           | ✅         | ✅       | ✅ (0.00%)   | ✅ (0.00%)    | ✅ (99th diff 0.0E+00)   |
| AOP                       | ✅         | ✅       | ✅ (0.22%)   | ✅ (0.00%)    | ❌ (99th diff 2.4E-01)   |
| CitationsRD               | ✅         | ✅       | ✅ (0.00%)   | ✅ (0.00%)    | ✅ (99th diff 0.0E+00)   |
| DelCOA                    | ✅         | ✅       | ✅ (0.00%)   | ✅ (0.00%)    | ✅ (99th diff 2.3E-08)   |
| ChInv                     | ✅         | ✅       | ✅ (0.00%)   | ✅ (0.00%)    | ✅ (99th diff 8.6E-09)   |
| BPEBM                     | ✅         | ✅       | ✅ (0.00%)   | ✅ (0.00%)    | ✅ (99th diff 7.3E-06)   |
| EBM                       | ✅         | ✅       | ✅ (0.00%)   | ✅ (0.00%)    | ✅ (99th diff 7.3E-06)   |
| CF                        | ✅         | ✅       | ✅ (0.00%)   | ✅ (0.00%)    | ✅ (99th diff 7.0E-08)   |
| HerfBE                    | ✅         | ✅       | ✅ (0.00%)   | ✅ (0.00%)    | ❌ (99th diff 9.3E-03)   |
| NetEquityFinance          | ✅         | ✅       | ✅ (0.00%)   | ✅ (0.00%)    | ✅ (99th diff 1.8E-08)   |
| DelEqu                    | ✅         | ✅       | ✅ (0.00%)   | ✅ (0.00%)    | ✅ (99th diff 4.6E-08)   |
| TotalAccruals             | ✅         | ✅       | ✅ (0.00%)   | ✅ (0.00%)    | ✅ (99th diff 6.4E-08)   |
| AssetGrowth               | ✅         | ✅       | ✅ (0.00%)   | ✅ (0.00%)    | ✅ (99th diff 6.8E-08)   |
| OrderBacklogChg           | ✅         | ✅       | ✅ (0.00%)   | ✅ (0.00%)    | ✅ (99th diff 1.6E-07)   |
| ConvDebt                  | ✅         | ✅       | ✅ (0.00%)   | ✅ (0.00%)    | ✅ (99th diff 0.0E+00)   |
| ChTax                     | ✅         | ✅       | ✅ (0.00%)   | ✅ (0.00%)    | ✅ (99th diff 1.9E-09)   |
| PctTotAcc                 | ✅         | ✅       | ✅ (0.00%)   | ✅ (0.00%)    | ✅ (99th diff 1.1E-06)   |
| OperProf                  | ✅         | ✅       | ✅ (0.00%)   | ✅ (0.00%)    | ✅ (99th diff 9.5E-08)   |
| ChAssetTurnover           | ✅         | ✅       | ✅ (0.00%)   | ✅ (0.00%)    | ✅ (99th diff 1.2E-06)   |
| CoskewACX                 | ✅         | ✅       | ✅ (0.00%)   | ✅ (0.00%)    | ✅ (99th diff 3.8E-04)   |
| PctAcc                    | ✅         | ✅       | ✅ (0.00%)   | ✅ (0.00%)    | ✅ (99th diff 1.1E-06)   |
| PayoutYield               | ✅         | ✅       | ✅ (0.00%)   | ✅ (0.00%)    | ✅ (99th diff 2.8E-08)   |
| cfp                       | ✅         | ✅       | ✅ (0.00%)   | ✅ (0.00%)    | ✅ (99th diff 7.9E-08)   |
| NetPayoutYield            | ✅         | ✅       | ✅ (0.00%)   | ✅ (0.00%)    | ✅ (99th diff 1.7E-08)   |
| RD                        | ✅         | ✅       | ✅ (0.00%)   | ✅ (0.00%)    | ✅ (99th diff 2.5E-08)   |
| MeanRankRevGrowth         | ✅         | ✅       | ✅ (0.00%)   | ✅ (0.00%)    | ❌ (99th diff 3.3E-01)   |
| Coskewness                | ✅         | ✅       | ✅ (0.00%)   | ✅ (0.00%)    | ✅ (99th diff 5.0E-04)   |
| InvGrowth                 | ✅         | ✅       | ✅ (0.00%)   | ✅ (0.00%)    | ✅ (99th diff 3.5E-07)   |
| ShortInterest             | ✅         | ✅       | ✅ (0.00%)   | ✅ (0.00%)    | ❌ (99th diff 8.6E-03)   |
| BrandInvest               | ✅         | ✅       | ✅ (0.00%)   | ✅ (0.00%)    | ❌ (99th diff 1.8E-03)   |
| RDS                       | ✅         | ✅       | ✅ (0.00%)   | ✅ (0.00%)    | ✅ (99th diff 8.0E-05)   |
| CashProd                  | ✅         | ✅       | ✅ (0.00%)   | ✅ (0.00%)    | ✅ (99th diff 1.4E-05)   |
| IO_ShortInterest          | ✅         | ✅       | ✅ (0.00%)   | ✅ (0.00%)    | ✅ (99th diff 1.0E-05)   |
| EquityDuration            | ✅         | ✅       | ✅ (0.00%)   | ✅ (0.00%)    | ✅ (99th diff 6.8E-06)   |
| zerotrade12M              | ✅         | ✅       | ✅ (0.00%)   | ✅ (0.00%)    | ✅ (99th diff 6.4E-06)   |
| EntMult                   | ✅         | ✅       | ✅ (0.00%)   | ✅ (0.00%)    | ✅ (99th diff 4.2E-06)   |
| zerotrade6M               | ✅         | ✅       | ✅ (0.00%)   | ✅ (0.00%)    | ✅ (99th diff 3.1E-06)   |
| ChInvIA                   | ✅         | ✅       | ✅ (0.00%)   | ✅ (0.00%)    | ✅ (99th diff 2.3E-06)   |
| CompEquIss                | ✅         | ✅       | ✅ (0.73%)   | ✅ (0.00%)    | ✅ (99th diff 2.3E-06)   |
| Activism2                 | ✅         | ✅       | ✅ (0.00%)   | ✅ (0.00%)    | ✅ (99th diff 2.0E-06)   |
| BookLeverage              | ✅         | ✅       | ✅ (0.00%)   | ✅ (0.00%)    | ✅ (99th diff 1.6E-06)   |
| BMdec                     | ✅         | ✅       | ✅ (0.00%)   | ✅ (0.00%)    | ✅ (99th diff 9.5E-07)   |
| AM                        | ✅         | ✅       | ✅ (0.00%)   | ✅ (0.00%)    | ✅ (99th diff 8.9E-07)   |
| Leverage                  | ✅         | ✅       | ✅ (0.00%)   | ✅ (0.00%)    | ✅ (99th diff 7.9E-07)   |
| SP                        | ✅         | ✅       | ✅ (0.00%)   | ✅ (0.00%)    | ✅ (99th diff 7.1E-07)   |
| zerotrade1M               | ✅         | ✅       | ✅ (0.00%)   | ✅ (0.00%)    | ✅ (99th diff 5.6E-07)   |
| Size                      | ✅         | ✅       | ✅ (0.00%)   | ✅ (0.00%)    | ✅ (99th diff 4.0E-07)   |
| ShareIss5Y                | ✅         | ✅       | ✅ (0.00%)   | ✅ (0.00%)    | ✅ (99th diff 3.7E-07)   |
| NetDebtPrice              | ✅         | ✅       | ✅ (0.00%)   | ✅ (0.00%)    | ✅ (99th diff 3.6E-07)   |
| DolVol                    | ✅         | ✅       | ✅ (0.00%)   | ✅ (0.00%)    | ✅ (99th diff 2.8E-07)   |
| Price                     | ✅         | ✅       | ✅ (0.00%)   | ✅ (0.00%)    | ✅ (99th diff 2.0E-07)   |
| RoE                       | ✅         | ✅       | ✅ (0.00%)   | ✅ (0.00%)    | ✅ (99th diff 2.0E-07)   |
| EarningsConsistency       | ✅         | ✅       | ✅ (0.00%)   | ✅ (0.00%)    | ✅ (99th diff 1.5E-07)   |
| ChEQ                      | ✅         | ✅       | ✅ (0.00%)   | ✅ (0.00%)    | ✅ (99th diff 1.2E-07)   |
| OrderBacklog              | ✅         | ✅       | ✅ (0.00%)   | ✅ (0.00%)    | ✅ (99th diff 1.2E-07)   |
| ShareIss1Y                | ✅         | ✅       | ✅ (0.00%)   | ✅ (0.00%)    | ✅ (99th diff 1.1E-07)   |
| VarCF                     | ✅         | ✅       | ✅ (0.00%)   | ✅ (0.00%)    | ✅ (99th diff 1.0E-07)   |
| DelBreadth                | ✅         | ✅       | ✅ (0.00%)   | ✅ (0.00%)    | ✅ (99th diff 1.0E-07)   |
| FR                        | ✅         | ✅       | ✅ (0.00%)   | ✅ (0.00%)    | ✅ (99th diff 9.2E-08)   |
| High52                    | ✅         | ✅       | ✅ (0.00%)   | ✅ (0.00%)    | ✅ (99th diff 9.1E-08)   |
| RDcap                     | ✅         | ✅       | ✅ (0.00%)   | ✅ (0.00%)    | ✅ (99th diff 8.4E-08)   |
| Mom12m                    | ✅         | ✅       | ✅ (0.00%)   | ✅ (0.00%)    | ✅ (99th diff 7.9E-08)   |
| Beta                      | ✅         | ✅       | ✅ (0.00%)   | ✅ (0.00%)    | ✅ (99th diff 7.3E-08)   |
| GrAdExp                   | ✅         | ✅       | ✅ (0.00%)   | ✅ (0.00%)    | ✅ (99th diff 6.6E-08)   |
| IntMom                    | ✅         | ✅       | ✅ (0.00%)   | ✅ (0.00%)    | ✅ (99th diff 5.0E-08)   |
| std_turn                  | ✅         | ✅       | ✅ (0.02%)   | ✅ (0.00%)    | ✅ (99th diff 4.5E-08)   |
| Mom6m                     | ✅         | ✅       | ✅ (0.00%)   | ✅ (0.00%)    | ✅ (99th diff 4.1E-08)   |
| ProbInformedTrading       | ✅         | ✅       | ✅ (0.00%)   | ✅ (0.00%)    | ✅ (99th diff 3.0E-08)   |
| AdExp                     | ✅         | ✅       | ✅ (0.00%)   | ✅ (0.00%)    | ✅ (99th diff 2.2E-08)   |
| MomSeason                 | ✅         | ✅       | ✅ (0.00%)   | ✅ (0.00%)    | ✅ (99th diff 1.3E-08)   |
| MomSeason06YrPlus         | ✅         | ✅       | ✅ (0.00%)   | ✅ (0.00%)    | ✅ (99th diff 1.3E-08)   |
| MomSeason11YrPlus         | ✅         | ✅       | ✅ (0.00%)   | ✅ (0.00%)    | ✅ (99th diff 1.2E-08)   |
| EP                        | ✅         | ✅       | ✅ (0.00%)   | ✅ (0.00%)    | ✅ (99th diff 1.2E-08)   |
| MomSeason16YrPlus         | ✅         | ✅       | ✅ (0.00%)   | ✅ (0.00%)    | ✅ (99th diff 1.1E-08)   |
| MomSeasonShort            | ✅         | ✅       | ✅ (0.00%)   | ✅ (0.00%)    | ✅ (99th diff 1.0E-08)   |
| STreversal                | ✅         | ✅       | ✅ (0.00%)   | ✅ (0.00%)    | ✅ (99th diff 1.0E-08)   |
| BidAskSpread              | ✅         | ✅       | ✅ (0.00%)   | ✅ (0.00%)    | ✅ (99th diff 2.0E-09)   |
| Illiquidity               | ✅         | ✅       | ✅ (0.00%)   | ✅ (0.00%)    | ✅ (99th diff 3.0E-12)   |
| ReturnSkew                | ✅         | ✅       | ✅ (0.00%)   | ✅ (0.00%)    | ✅ (99th diff 1.8E-15)   |
| RealizedVol               | ✅         | ✅       | ✅ (0.12%)   | ✅ (0.00%)    | ✅ (99th diff 5.6E-17)   |
| AccrualsBM                | ✅         | ✅       | ✅ (0.00%)   | ✅ (0.00%)    | ✅ (99th diff 0.0E+00)   |
| Activism1                 | ✅         | ✅       | ✅ (0.00%)   | ✅ (0.00%)    | ✅ (99th diff 0.0E+00)   |
| DebtIssuance              | ✅         | ✅       | ✅ (0.00%)   | ✅ (0.00%)    | ✅ (99th diff 0.0E+00)   |
| FirmAge                   | ✅         | ✅       | ✅ (0.00%)   | ✅ (0.00%)    | ✅ (99th diff 0.0E+00)   |
| Governance                | ✅         | ✅       | ✅ (0.00%)   | ✅ (0.00%)    | ✅ (99th diff 0.0E+00)   |
| MaxRet                    | ✅         | ✅       | ✅ (0.00%)   | ✅ (0.00%)    | ✅ (99th diff 0.0E+00)   |
| OScore                    | ✅         | ✅       | ✅ (0.04%)   | ✅ (0.00%)    | ✅ (99th diff 0.0E+00)   |
| Spinoff                   | ✅         | ✅       | ✅ (0.00%)   | ✅ (0.00%)    | ✅ (99th diff 0.0E+00)   |
| GrLTNOA                   | ❌         | NA      | NA          | NA           | NA                      |
| GrSaleToGrInv             | ❌         | NA      | NA          | NA           | NA                      |
| GrSaleToGrOverhead        | ❌         | NA      | NA          | NA           | NA                      |
| InvestPPEInv              | ❌         | NA      | NA          | NA           | NA                      |
| grcapx                    | ❌         | NA      | NA          | NA           | NA                      |
| grcapx3y                  | ❌         | NA      | NA          | NA           | NA                      |

**Overall**: 155/203 available predictors passed validation
**Python CSVs**: 203/209 predictors have Python implementation

## Detailed Results

### AM

**Status**: ✅ PASSED

**Test Results**:
- Test 1 - Column names: ✅ PASSED
- Test 2 - Superset check: ✅ PASSED
- Test 3 - Precision1 check: ✅ PASSED
- Test 4 - Precision2 check: ✅ PASSED

**Columns**: ['AM']

**Observations**:
- Stata:  3,038,206
- Python: 3,038,208
- Common: 3,038,206

**Precision1**: 0.000% obs with std_diff >= 1.00e-02 (tolerance: < 10%)

**Precision2**: 99th percentile diff = 8.94e-07 (tolerance: < 1.00e-03)

**Feedback**:
- Num observations with std_diff >= TOL_DIFF_1: 0/3038206 (0.000%)
- Stata standard deviation: 2.68e+01

---

### AOP

**Status**: ❌ FAILED

**Test Results**:
- Test 1 - Column names: ✅ PASSED
- Test 2 - Superset check: ✅ PASSED
- Test 3 - Precision1 check: ✅ PASSED
- Test 4 - Precision2 check: ❌ FAILED

**Columns**: ['AOP']

**Observations**:
- Stata:  1,244,664
- Python: 1,299,504
- Common: 1,241,880

**Precision1**: 0.002% obs with std_diff >= 1.00e-02 (tolerance: < 10%)

**Precision2**: 99th percentile diff = 2.39e-01 (tolerance: < 1.00e-03)

**Feedback**:
- Num observations with std_diff >= TOL_DIFF_1: 24/1241880 (0.002%)
- Stata standard deviation: 4.75e+04

**Most Recent Bad Observations**:
```
   permno  yyyymm       python      stata         diff
0   77851  199605  2422.684918  22.909092  2399.775826
1   77851  199604  2422.684918  22.909092  2399.775826
2   77851  199603  2422.684918  22.909092  2399.775826
3   77851  199602  2422.684918  22.909092  2399.775826
4   77851  199601  2422.684918  22.909092  2399.775826
5   77851  199512  2422.684918  22.909092  2399.775826
6   77851  199511  2422.684918  22.909092  2399.775826
7   77851  199510  2422.684918  22.909092  2399.775826
8   77851  199509  2422.684918  22.909092  2399.775826
9   77851  199508  2422.684918  22.909092  2399.775826
```

**Largest Differences**:
```
   permno  yyyymm       python      stata         diff
0   77851  199506  2422.684918  22.909092  2399.775826
1   77851  199507  2422.684918  22.909092  2399.775826
2   77851  199508  2422.684918  22.909092  2399.775826
3   77851  199509  2422.684918  22.909092  2399.775826
4   77851  199510  2422.684918  22.909092  2399.775826
5   77851  199511  2422.684918  22.909092  2399.775826
6   77851  199512  2422.684918  22.909092  2399.775826
7   77851  199601  2422.684918  22.909092  2399.775826
8   77851  199602  2422.684918  22.909092  2399.775826
9   77851  199603  2422.684918  22.909092  2399.775826
```

---

### AbnormalAccruals

**Status**: ❌ FAILED

**Test Results**:
- Test 1 - Column names: ✅ PASSED
- Test 2 - Superset check: ✅ PASSED
- Test 3 - Precision1 check: ❌ FAILED
- Test 4 - Precision2 check: ❌ FAILED

**Columns**: ['AbnormalAccruals']

**Observations**:
- Stata:  2,570,664
- Python: 2,567,830
- Common: 2,553,227

**Precision1**: 27.951% obs with std_diff >= 1.00e-02 (tolerance: < 10%)

**Precision2**: 99th percentile diff = 5.22e-02 (tolerance: < 1.00e-03)

**Feedback**:
- Num observations with std_diff >= TOL_DIFF_1: 713656/2553227 (27.951%)
- Stata standard deviation: 1.61e-01

**Most Recent Bad Observations**:
```
   permno  yyyymm    python     stata      diff
0   29946  202609  0.108293  0.092957  0.015336
1   12366  202608  0.139485  0.146414 -0.006929
2   13142  202608 -0.125493 -0.145704  0.020211
3   14033  202608  1.382135  1.391868 -0.009733
4   15623  202608 -0.091212 -0.093782  0.002570
5   16632  202608 -0.026517 -0.029087  0.002570
6   19655  202608 -0.036532 -0.038729  0.002197
7   22092  202608  0.014588  0.016372 -0.001784
8   23681  202608 -0.003675 -0.001505 -0.002170
9   24252  202608  0.088683  0.090385 -0.001702
```

**Largest Differences**:
```
   permno  yyyymm    python    stata      diff
0   79702  201712 -2.383081 -1.50314 -0.879941
1   79702  201801 -2.383081 -1.50314 -0.879941
2   79702  201802 -2.383081 -1.50314 -0.879941
3   79702  201803 -2.383081 -1.50314 -0.879941
4   79702  201804 -2.383081 -1.50314 -0.879941
5   79702  201805 -2.383081 -1.50314 -0.879941
6   79702  201806 -2.383081 -1.50314 -0.879941
7   79702  201807 -2.383081 -1.50314 -0.879941
8   79702  201808 -2.383081 -1.50314 -0.879941
9   79702  201809 -2.383081 -1.50314 -0.879941
```

---

### Accruals

**Status**: ✅ PASSED

**Test Results**:
- Test 1 - Column names: ✅ PASSED
- Test 2 - Superset check: ✅ PASSED
- Test 3 - Precision1 check: ✅ PASSED
- Test 4 - Precision2 check: ✅ PASSED

**Columns**: ['Accruals']

**Observations**:
- Stata:  3,259,701
- Python: 3,276,202
- Common: 3,259,701

**Precision1**: 0.009% obs with std_diff >= 1.00e-02 (tolerance: < 10%)

**Precision2**: 99th percentile diff = 1.39e-08 (tolerance: < 1.00e-03)

**Feedback**:
- Num observations with std_diff >= TOL_DIFF_1: 300/3259701 (0.009%)
- Stata standard deviation: 1.41e-01

---

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
- Python: 1,511,521
- Common: 220,066

**Precision1**: 0.000% obs with std_diff >= 1.00e-02 (tolerance: < 10%)

**Precision2**: 99th percentile diff = 0.00e+00 (tolerance: < 1.00e-03)

**Feedback**:
- Num observations with std_diff >= TOL_DIFF_1: 0/220066 (0.000%)
- Stata standard deviation: 5.00e-01

---

### Activism1

**Status**: ✅ PASSED

**Test Results**:
- Test 1 - Column names: ✅ PASSED
- Test 2 - Superset check: ✅ PASSED
- Test 3 - Precision1 check: ✅ PASSED
- Test 4 - Precision2 check: ✅ PASSED

**Columns**: ['Activism1']

**Observations**:
- Stata:  108,733
- Python: 235,090
- Common: 108,733

**Precision1**: 0.000% obs with std_diff >= 1.00e-02 (tolerance: < 10%)

**Precision2**: 99th percentile diff = 0.00e+00 (tolerance: < 1.00e-03)

**Feedback**:
- Num observations with std_diff >= TOL_DIFF_1: 0/108733 (0.000%)
- Stata standard deviation: 2.72e+00

---

### Activism2

**Status**: ✅ PASSED

**Test Results**:
- Test 1 - Column names: ✅ PASSED
- Test 2 - Superset check: ✅ PASSED
- Test 3 - Precision1 check: ✅ PASSED
- Test 4 - Precision2 check: ✅ PASSED

**Columns**: ['Activism2']

**Observations**:
- Stata:  30,170
- Python: 30,170
- Common: 30,170

**Precision1**: 0.000% obs with std_diff >= 1.00e-02 (tolerance: < 10%)

**Precision2**: 99th percentile diff = 2.00e-06 (tolerance: < 1.00e-03)

**Feedback**:
- Num observations with std_diff >= TOL_DIFF_1: 0/30170 (0.000%)
- Stata standard deviation: 1.26e+01

---

### AdExp

**Status**: ✅ PASSED

**Test Results**:
- Test 1 - Column names: ✅ PASSED
- Test 2 - Superset check: ✅ PASSED
- Test 3 - Precision1 check: ✅ PASSED
- Test 4 - Precision2 check: ✅ PASSED

**Columns**: ['AdExp']

**Observations**:
- Stata:  1,049,030
- Python: 1,049,037
- Common: 1,049,030

**Precision1**: 0.000% obs with std_diff >= 1.00e-02 (tolerance: < 10%)

**Precision2**: 99th percentile diff = 2.20e-08 (tolerance: < 1.00e-03)

**Feedback**:
- Num observations with std_diff >= TOL_DIFF_1: 0/1049030 (0.000%)
- Stata standard deviation: 3.73e-01

---

### AnalystRevision

**Status**: ✅ PASSED

**Test Results**:
- Test 1 - Column names: ✅ PASSED
- Test 2 - Superset check: ✅ PASSED
- Test 3 - Precision1 check: ✅ PASSED
- Test 4 - Precision2 check: ✅ PASSED

**Columns**: ['AnalystRevision']

**Observations**:
- Stata:  1,920,473
- Python: 1,923,490
- Common: 1,917,427

**Precision1**: 0.038% obs with std_diff >= 1.00e-02 (tolerance: < 10%)

**Precision2**: 99th percentile diff = 9.47e-08 (tolerance: < 1.00e-03)

**Feedback**:
- Num observations with std_diff >= TOL_DIFF_1: 738/1917427 (0.038%)
- Stata standard deviation: 4.84e+00

---

### AnalystValue

**Status**: ❌ FAILED

**Test Results**:
- Test 1 - Column names: ✅ PASSED
- Test 2 - Superset check: ✅ PASSED
- Test 3 - Precision1 check: ✅ PASSED
- Test 4 - Precision2 check: ❌ FAILED

**Columns**: ['AnalystValue']

**Observations**:
- Stata:  1,244,664
- Python: 1,299,504
- Common: 1,241,880

**Precision1**: 0.263% obs with std_diff >= 1.00e-02 (tolerance: < 10%)

**Precision2**: 99th percentile diff = 1.82e-02 (tolerance: < 1.00e-03)

**Feedback**:
- Num observations with std_diff >= TOL_DIFF_1: 3264/1241880 (0.263%)
- Stata standard deviation: 1.05e+01

**Most Recent Bad Observations**:
```
   permno  yyyymm       python        stata       diff
0   21783  202505     1.230213     1.028611   0.201602
1   22793  202505  3326.578149  3338.297600 -11.719451
2   23033  202505    11.374458     9.866216   1.508243
3   23316  202505     1.854150     1.746798   0.107352
4   23426  202505    -1.539445    -1.210400  -0.329045
5   91575  202505     0.009558     1.261121  -1.251564
6   21783  202504     1.230213     1.028611   0.201602
7   22793  202504  3326.578149  3338.297600 -11.719451
8   23033  202504    11.374458     9.866216   1.508243
9   23316  202504     1.854150     1.746798   0.107352
```

**Largest Differences**:
```
   permno  yyyymm       python      stata       diff
0   22793  202406  3326.578149  3338.2976 -11.719451
1   22793  202407  3326.578149  3338.2976 -11.719451
2   22793  202408  3326.578149  3338.2976 -11.719451
3   22793  202409  3326.578149  3338.2976 -11.719451
4   22793  202410  3326.578149  3338.2976 -11.719451
5   22793  202411  3326.578149  3338.2976 -11.719451
6   22793  202412  3326.578149  3338.2976 -11.719451
7   22793  202501  3326.578149  3338.2976 -11.719451
8   22793  202502  3326.578149  3338.2976 -11.719451
9   22793  202503  3326.578149  3338.2976 -11.719451
```

---

### AnnouncementReturn

**Status**: ✅ PASSED

**Test Results**:
- Test 1 - Column names: ✅ PASSED
- Test 2 - Superset check: ✅ PASSED
- Test 3 - Precision1 check: ✅ PASSED
- Test 4 - Precision2 check: ✅ PASSED

**Columns**: ['AnnouncementReturn']

**Observations**:
- Stata:  2,922,373
- Python: 2,922,354
- Common: 2,922,290

**Precision1**: 0.003% obs with std_diff >= 1.00e-02 (tolerance: < 10%)

**Precision2**: 99th percentile diff = 1.95e-08 (tolerance: < 1.00e-03)

**Feedback**:
- Num observations with std_diff >= TOL_DIFF_1: 90/2922290 (0.003%)
- Stata standard deviation: 1.03e-01

---

### AssetGrowth

**Status**: ✅ PASSED

**Test Results**:
- Test 1 - Column names: ✅ PASSED
- Test 2 - Superset check: ✅ PASSED
- Test 3 - Precision1 check: ✅ PASSED
- Test 4 - Precision2 check: ✅ PASSED

**Columns**: ['AssetGrowth']

**Observations**:
- Stata:  3,295,125
- Python: 3,311,751
- Common: 3,295,125

**Precision1**: 0.001% obs with std_diff >= 1.00e-02 (tolerance: < 10%)

**Precision2**: 99th percentile diff = 6.77e-08 (tolerance: < 1.00e-03)

**Feedback**:
- Num observations with std_diff >= TOL_DIFF_1: 24/3295125 (0.001%)
- Stata standard deviation: 1.89e+00

---

### BM

**Status**: ✅ PASSED

**Test Results**:
- Test 1 - Column names: ✅ PASSED
- Test 2 - Superset check: ✅ PASSED
- Test 3 - Precision1 check: ✅ PASSED
- Test 4 - Precision2 check: ✅ PASSED

**Columns**: ['BM']

**Observations**:
- Stata:  2,715,090
- Python: 2,715,252
- Common: 2,715,090

**Precision1**: 0.032% obs with std_diff >= 1.00e-02 (tolerance: < 10%)

**Precision2**: 99th percentile diff = 1.34e-07 (tolerance: < 1.00e-03)

**Feedback**:
- Num observations with std_diff >= TOL_DIFF_1: 882/2715090 (0.032%)
- Stata standard deviation: 1.05e+00

---

### BMdec

**Status**: ✅ PASSED

**Test Results**:
- Test 1 - Column names: ✅ PASSED
- Test 2 - Superset check: ✅ PASSED
- Test 3 - Precision1 check: ✅ PASSED
- Test 4 - Precision2 check: ✅ PASSED

**Columns**: ['BMdec']

**Observations**:
- Stata:  2,996,716
- Python: 2,998,697
- Common: 2,996,716

**Precision1**: 0.000% obs with std_diff >= 1.00e-02 (tolerance: < 10%)

**Precision2**: 99th percentile diff = 9.52e-07 (tolerance: < 1.00e-03)

**Feedback**:
- Num observations with std_diff >= TOL_DIFF_1: 0/2996716 (0.000%)
- Stata standard deviation: 5.24e+01

---

### BPEBM

**Status**: ✅ PASSED

**Test Results**:
- Test 1 - Column names: ✅ PASSED
- Test 2 - Superset check: ✅ PASSED
- Test 3 - Precision1 check: ✅ PASSED
- Test 4 - Precision2 check: ✅ PASSED

**Columns**: ['BPEBM']

**Observations**:
- Stata:  2,924,820
- Python: 2,924,826
- Common: 2,924,820

**Precision1**: 0.001% obs with std_diff >= 1.00e-02 (tolerance: < 10%)

**Precision2**: 99th percentile diff = 7.32e-06 (tolerance: < 1.00e-03)

**Feedback**:
- Num observations with std_diff >= TOL_DIFF_1: 43/2924820 (0.001%)
- Stata standard deviation: 3.35e+02

---

### Beta

**Status**: ✅ PASSED

**Test Results**:
- Test 1 - Column names: ✅ PASSED
- Test 2 - Superset check: ✅ PASSED
- Test 3 - Precision1 check: ✅ PASSED
- Test 4 - Precision2 check: ✅ PASSED

**Columns**: ['Beta']

**Observations**:
- Stata:  4,285,574
- Python: 4,353,773
- Common: 4,285,574

**Precision1**: 0.000% obs with std_diff >= 1.00e-02 (tolerance: < 10%)

**Precision2**: 99th percentile diff = 7.33e-08 (tolerance: < 1.00e-03)

**Feedback**:
- Num observations with std_diff >= TOL_DIFF_1: 0/4285574 (0.000%)
- Stata standard deviation: 7.46e-01

---

### BetaFP

**Status**: ❌ FAILED

**Test Results**:
- Test 1 - Column names: ✅ PASSED
- Test 2 - Superset check: ✅ PASSED
- Test 3 - Precision1 check: ✅ PASSED
- Test 4 - Precision2 check: ❌ FAILED

**Columns**: ['BetaFP']

**Observations**:
- Stata:  3,794,018
- Python: 3,779,957
- Common: 3,773,530

**Precision1**: 5.980% obs with std_diff >= 1.00e-02 (tolerance: < 10%)

**Precision2**: 99th percentile diff = 5.72e-02 (tolerance: < 1.00e-03)

**Feedback**:
- Num observations with std_diff >= TOL_DIFF_1: 225656/3773530 (5.980%)
- Stata standard deviation: 6.41e-01

**Most Recent Bad Observations**:
```
   permno  yyyymm    python     stata      diff
0   10066  202412  0.366776  0.247929  0.118848
1   11153  202412  0.194148  0.253281 -0.059133
2   11379  202412  1.593719  1.445916  0.147803
3   13563  202412  0.903798  0.608259  0.295539
4   13828  202412  0.846968  0.970209 -0.123241
5   13878  202412  0.978277  0.966509  0.011768
6   13947  202412  2.605158  2.657374 -0.052215
7   14051  202412  3.479917  3.465529  0.014388
8   14469  202412  2.212209  1.759658  0.452551
9   14720  202412  4.574750  4.556220  0.018530
```

**Largest Differences**:
```
   permno  yyyymm    python     stata      diff
0   78301  198510       NaN  0.000378       NaN
1   78301  198511       NaN  0.000365       NaN
2   78301  198512       NaN  0.000359       NaN
3   78301  198601       NaN  0.000377       NaN
4   78301  198602       NaN  0.000447       NaN
5   78301  198603       NaN  0.000468       NaN
6   11453  199312  7.664115  2.870236  4.793879
7   65622  199401  0.593349  4.575622 -3.982273
8   65622  199402  0.930784  4.732967 -3.802183
9   65622  199312  0.867006  4.276299 -3.409292
```

---

### BetaLiquidityPS

**Status**: ❌ FAILED

**Test Results**:
- Test 1 - Column names: ✅ PASSED
- Test 2 - Superset check: ✅ PASSED
- Test 3 - Precision1 check: ✅ PASSED
- Test 4 - Precision2 check: ❌ FAILED

**Columns**: ['BetaLiquidityPS']

**Observations**:
- Stata:  3,423,856
- Python: 3,479,410
- Common: 3,423,856

**Precision1**: 0.309% obs with std_diff >= 1.00e-02 (tolerance: < 10%)

**Precision2**: 99th percentile diff = 2.40e-03 (tolerance: < 1.00e-03)

**Feedback**:
- Num observations with std_diff >= TOL_DIFF_1: 10596/3423856 (0.309%)
- Stata standard deviation: 4.52e-01

**Most Recent Bad Observations**:
```
   permno  yyyymm    python     stata      diff
0   12527  202412  3.114748  3.110062  0.004685
1   13812  202412 -0.279861 -0.285009  0.005148
2   14280  202412 -0.195891 -0.200836  0.004945
3   14328  202412  2.075094  2.067611  0.007482
4   14720  202412 -0.783082 -0.788315  0.005233
5   14791  202412 -2.796831 -2.804661  0.007830
6   14813  202412  0.574480  0.568289  0.006190
7   15172  202412  0.858918  0.854361  0.004557
8   15489  202412  0.114074  0.101456  0.012619
9   15775  202412  0.905586  0.899805  0.005782
```

**Largest Differences**:
```
   permno  yyyymm    python     stata      diff
0   48072  202311  2.920068  2.873500  0.046568
1   89301  202311  1.966508  1.923020  0.043488
2   48072  202310  3.102564  3.060607  0.041957
3   48072  202403  4.981330  4.941999  0.039331
4   48072  202402  4.975391  4.936378  0.039014
5   89301  202310  2.094525  2.055533  0.038992
6   48072  202401  4.069945  4.032388  0.037557
7   89301  202403  3.828060  3.791143  0.036917
8   48072  202312  4.056726  4.019963  0.036763
9   89301  202402  3.823554  3.786863  0.036692
```

---

### BetaTailRisk

**Status**: ❌ FAILED

**Test Results**:
- Test 1 - Column names: ✅ PASSED
- Test 2 - Superset check: ✅ PASSED
- Test 3 - Precision1 check: ✅ PASSED
- Test 4 - Precision2 check: ❌ FAILED

**Columns**: ['BetaTailRisk']

**Observations**:
- Stata:  2,292,350
- Python: 2,332,084
- Common: 2,292,350

**Precision1**: 4.149% obs with std_diff >= 1.00e-02 (tolerance: < 10%)

**Precision2**: 99th percentile diff = 1.01e-02 (tolerance: < 1.00e-03)

**Feedback**:
- Num observations with std_diff >= TOL_DIFF_1: 95107/2292350 (4.149%)
- Stata standard deviation: 5.11e-01

**Most Recent Bad Observations**:
```
   permno  yyyymm    python     stata      diff
0   16099  202412  0.288367  0.293937 -0.005571
1   16400  202412  1.372777  1.339924  0.032854
2   18148  202412  0.111011  0.116482 -0.005471
3   77437  202412  1.854679  1.846069  0.008610
4   84411  202412  0.911352  0.901888  0.009464
5   89029  202412  0.608437  0.614334 -0.005897
6   89169  202412  1.567852  1.606029 -0.038177
7   16099  202411  0.323722  0.329289 -0.005567
8   16400  202411  1.385534  1.352590  0.032944
9   18148  202411  0.147289  0.152762 -0.005473
```

**Largest Differences**:
```
   permno  yyyymm    python     stata      diff
0   78050  199811 -0.557545 -0.755131  0.197586
1   78050  199812 -0.396312 -0.593467  0.197155
2   78050  199901 -0.158898 -0.349701  0.190803
3   78050  199902 -0.069994 -0.254714  0.184720
4   78050  199903  0.069028 -0.111589  0.180616
5   78050  199904  0.224322  0.047509  0.176813
6   78050  199905  0.378144  0.209011  0.169132
7   78050  199906  0.461683  0.294377  0.167306
8   78050  199907  0.347299  0.188068  0.159231
9   78050  199908  0.386259  0.234870  0.151388
```

---

### BidAskSpread

**Status**: ✅ PASSED

**Test Results**:
- Test 1 - Column names: ✅ PASSED
- Test 2 - Superset check: ✅ PASSED
- Test 3 - Precision1 check: ✅ PASSED
- Test 4 - Precision2 check: ✅ PASSED

**Columns**: ['BidAskSpread']

**Observations**:
- Stata:  4,481,622
- Python: 4,481,622
- Common: 4,481,622

**Precision1**: 0.000% obs with std_diff >= 1.00e-02 (tolerance: < 10%)

**Precision2**: 99th percentile diff = 2.00e-09 (tolerance: < 1.00e-03)

**Feedback**:
- Num observations with std_diff >= TOL_DIFF_1: 0/4481622 (0.000%)
- Stata standard deviation: 3.10e-02

---

### BookLeverage

**Status**: ✅ PASSED

**Test Results**:
- Test 1 - Column names: ✅ PASSED
- Test 2 - Superset check: ✅ PASSED
- Test 3 - Precision1 check: ✅ PASSED
- Test 4 - Precision2 check: ✅ PASSED

**Columns**: ['BookLeverage']

**Observations**:
- Stata:  3,606,159
- Python: 3,607,287
- Common: 3,606,159

**Precision1**: 0.000% obs with std_diff >= 1.00e-02 (tolerance: < 10%)

**Precision2**: 99th percentile diff = 1.55e-06 (tolerance: < 1.00e-03)

**Feedback**:
- Num observations with std_diff >= TOL_DIFF_1: 0/3606159 (0.000%)
- Stata standard deviation: 2.02e+02

---

### BrandInvest

**Status**: ❌ FAILED

**Test Results**:
- Test 1 - Column names: ✅ PASSED
- Test 2 - Superset check: ✅ PASSED
- Test 3 - Precision1 check: ✅ PASSED
- Test 4 - Precision2 check: ❌ FAILED

**Columns**: ['BrandInvest']

**Observations**:
- Stata:  485,304
- Python: 509,472
- Common: 485,304

**Precision1**: 0.000% obs with std_diff >= 1.00e-02 (tolerance: < 10%)

**Precision2**: 99th percentile diff = 1.75e-03 (tolerance: < 1.00e-03)

**Feedback**:
- Num observations with std_diff >= TOL_DIFF_1: 0/485304 (0.000%)
- Stata standard deviation: 6.90e+04

---

### CBOperProf

**Status**: ✅ PASSED

**Test Results**:
- Test 1 - Column names: ✅ PASSED
- Test 2 - Superset check: ✅ PASSED
- Test 3 - Precision1 check: ✅ PASSED
- Test 4 - Precision2 check: ✅ PASSED

**Columns**: ['CBOperProf']

**Observations**:
- Stata:  2,283,861
- Python: 2,283,897
- Common: 2,283,861

**Precision1**: 0.006% obs with std_diff >= 1.00e-02 (tolerance: < 10%)

**Precision2**: 99th percentile diff = 2.92e-08 (tolerance: < 1.00e-03)

**Feedback**:
- Num observations with std_diff >= TOL_DIFF_1: 127/2283861 (0.006%)
- Stata standard deviation: 2.20e-01

---

### CF

**Status**: ✅ PASSED

**Test Results**:
- Test 1 - Column names: ✅ PASSED
- Test 2 - Superset check: ✅ PASSED
- Test 3 - Precision1 check: ✅ PASSED
- Test 4 - Precision2 check: ✅ PASSED

**Columns**: ['CF']

**Observations**:
- Stata:  3,038,206
- Python: 3,053,133
- Common: 3,038,206

**Precision1**: 0.001% obs with std_diff >= 1.00e-02 (tolerance: < 10%)

**Precision2**: 99th percentile diff = 6.97e-08 (tolerance: < 1.00e-03)

**Feedback**:
- Num observations with std_diff >= TOL_DIFF_1: 43/3038206 (0.001%)
- Stata standard deviation: 2.76e+00

---

### CPVolSpread

**Status**: ✅ PASSED

**Test Results**:
- Test 1 - Column names: ✅ PASSED
- Test 2 - Superset check: ✅ PASSED
- Test 3 - Precision1 check: ✅ PASSED
- Test 4 - Precision2 check: ✅ PASSED

**Columns**: ['CPVolSpread']

**Observations**:
- Stata:  684,140
- Python: 682,114
- Common: 679,061

**Precision1**: 0.050% obs with std_diff >= 1.00e-02 (tolerance: < 10%)

**Precision2**: 99th percentile diff = 4.00e-09 (tolerance: < 1.00e-03)

**Feedback**:
- Num observations with std_diff >= TOL_DIFF_1: 337/679061 (0.050%)
- Stata standard deviation: 5.47e-02

---

### Cash

**Status**: ✅ PASSED

**Test Results**:
- Test 1 - Column names: ✅ PASSED
- Test 2 - Superset check: ✅ PASSED
- Test 3 - Precision1 check: ✅ PASSED
- Test 4 - Precision2 check: ✅ PASSED

**Columns**: ['Cash']

**Observations**:
- Stata:  2,096,350
- Python: 2,572,551
- Common: 2,096,350

**Precision1**: 0.058% obs with std_diff >= 1.00e-02 (tolerance: < 10%)

**Precision2**: 99th percentile diff = 2.72e-08 (tolerance: < 1.00e-03)

**Feedback**:
- Num observations with std_diff >= TOL_DIFF_1: 1206/2096350 (0.058%)
- Stata standard deviation: 2.14e-01

---

### CashProd

**Status**: ✅ PASSED

**Test Results**:
- Test 1 - Column names: ✅ PASSED
- Test 2 - Superset check: ✅ PASSED
- Test 3 - Precision1 check: ✅ PASSED
- Test 4 - Precision2 check: ✅ PASSED

**Columns**: ['CashProd']

**Observations**:
- Stata:  3,002,825
- Python: 3,038,208
- Common: 3,002,825

**Precision1**: 0.000% obs with std_diff >= 1.00e-02 (tolerance: < 10%)

**Precision2**: 99th percentile diff = 1.44e-05 (tolerance: < 1.00e-03)

**Feedback**:
- Num observations with std_diff >= TOL_DIFF_1: 0/3002825 (0.000%)
- Stata standard deviation: 3.82e+03

---

### ChAssetTurnover

**Status**: ✅ PASSED

**Test Results**:
- Test 1 - Column names: ✅ PASSED
- Test 2 - Superset check: ✅ PASSED
- Test 3 - Precision1 check: ✅ PASSED
- Test 4 - Precision2 check: ✅ PASSED

**Columns**: ['ChAssetTurnover']

**Observations**:
- Stata:  2,503,228
- Python: 2,517,970
- Common: 2,503,228

**Precision1**: 0.000% obs with std_diff >= 1.00e-02 (tolerance: < 10%)

**Precision2**: 99th percentile diff = 1.17e-06 (tolerance: < 1.00e-03)

**Feedback**:
- Num observations with std_diff >= TOL_DIFF_1: 12/2503228 (0.000%)
- Stata standard deviation: 2.75e+02

---

### ChEQ

**Status**: ✅ PASSED

**Test Results**:
- Test 1 - Column names: ✅ PASSED
- Test 2 - Superset check: ✅ PASSED
- Test 3 - Precision1 check: ✅ PASSED
- Test 4 - Precision2 check: ✅ PASSED

**Columns**: ['ChEQ']

**Observations**:
- Stata:  3,047,458
- Python: 3,060,165
- Common: 3,047,458

**Precision1**: 0.000% obs with std_diff >= 1.00e-02 (tolerance: < 10%)

**Precision2**: 99th percentile diff = 1.24e-07 (tolerance: < 1.00e-03)

**Feedback**:
- Num observations with std_diff >= TOL_DIFF_1: 0/3047458 (0.000%)
- Stata standard deviation: 1.77e+01

---

### ChForecastAccrual

**Status**: ✅ PASSED

**Test Results**:
- Test 1 - Column names: ✅ PASSED
- Test 2 - Superset check: ✅ PASSED
- Test 3 - Precision1 check: ✅ PASSED
- Test 4 - Precision2 check: ✅ PASSED

**Columns**: ['ChForecastAccrual']

**Observations**:
- Stata:  628,022
- Python: 2,222,319
- Common: 628,022

**Precision1**: 0.118% obs with std_diff >= 1.00e-02 (tolerance: < 10%)

**Precision2**: 99th percentile diff = 0.00e+00 (tolerance: < 1.00e-03)

**Feedback**:
- Num observations with std_diff >= TOL_DIFF_1: 741/628022 (0.118%)
- Stata standard deviation: 4.99e-01

---

### ChInv

**Status**: ✅ PASSED

**Test Results**:
- Test 1 - Column names: ✅ PASSED
- Test 2 - Superset check: ✅ PASSED
- Test 3 - Precision1 check: ✅ PASSED
- Test 4 - Precision2 check: ✅ PASSED

**Columns**: ['ChInv']

**Observations**:
- Stata:  3,295,155
- Python: 3,311,811
- Common: 3,295,155

**Precision1**: 0.002% obs with std_diff >= 1.00e-02 (tolerance: < 10%)

**Precision2**: 99th percentile diff = 8.61e-09 (tolerance: < 1.00e-03)

**Feedback**:
- Num observations with std_diff >= TOL_DIFF_1: 60/3295155 (0.002%)
- Stata standard deviation: 6.64e-02

---

### ChInvIA

**Status**: ✅ PASSED

**Test Results**:
- Test 1 - Column names: ✅ PASSED
- Test 2 - Superset check: ✅ PASSED
- Test 3 - Precision1 check: ✅ PASSED
- Test 4 - Precision2 check: ✅ PASSED

**Columns**: ['ChInvIA']

**Observations**:
- Stata:  2,678,515
- Python: 2,678,515
- Common: 2,678,515

**Precision1**: 0.000% obs with std_diff >= 1.00e-02 (tolerance: < 10%)

**Precision2**: 99th percentile diff = 2.32e-06 (tolerance: < 1.00e-03)

**Feedback**:
- Num observations with std_diff >= TOL_DIFF_1: 0/2678515 (0.000%)
- Stata standard deviation: 5.76e+13

---

### ChNAnalyst

**Status**: ✅ PASSED

**Test Results**:
- Test 1 - Column names: ✅ PASSED
- Test 2 - Superset check: ✅ PASSED
- Test 3 - Precision1 check: ✅ PASSED
- Test 4 - Precision2 check: ✅ PASSED

**Columns**: ['ChNAnalyst']

**Observations**:
- Stata:  210,988
- Python: 210,931
- Common: 210,756

**Precision1**: 0.007% obs with std_diff >= 1.00e-02 (tolerance: < 10%)

**Precision2**: 99th percentile diff = 0.00e+00 (tolerance: < 1.00e-03)

**Feedback**:
- Num observations with std_diff >= TOL_DIFF_1: 14/210756 (0.007%)
- Stata standard deviation: 3.56e-01

---

### ChNNCOA

**Status**: ✅ PASSED

**Test Results**:
- Test 1 - Column names: ✅ PASSED
- Test 2 - Superset check: ✅ PASSED
- Test 3 - Precision1 check: ✅ PASSED
- Test 4 - Precision2 check: ✅ PASSED

**Columns**: ['ChNNCOA']

**Observations**:
- Stata:  3,246,170
- Python: 3,262,618
- Common: 3,246,170

**Precision1**: 0.007% obs with std_diff >= 1.00e-02 (tolerance: < 10%)

**Precision2**: 99th percentile diff = 4.75e-08 (tolerance: < 1.00e-03)

**Feedback**:
- Num observations with std_diff >= TOL_DIFF_1: 228/3246170 (0.007%)
- Stata standard deviation: 5.61e-01

---

### ChNWC

**Status**: ✅ PASSED

**Test Results**:
- Test 1 - Column names: ✅ PASSED
- Test 2 - Superset check: ✅ PASSED
- Test 3 - Precision1 check: ✅ PASSED
- Test 4 - Precision2 check: ✅ PASSED

**Columns**: ['ChNWC']

**Observations**:
- Stata:  3,259,599
- Python: 3,275,986
- Common: 3,259,599

**Precision1**: 0.004% obs with std_diff >= 1.00e-02 (tolerance: < 10%)

**Precision2**: 99th percentile diff = 3.58e-08 (tolerance: < 1.00e-03)

**Feedback**:
- Num observations with std_diff >= TOL_DIFF_1: 132/3259599 (0.004%)
- Stata standard deviation: 4.26e-01

---

### ChTax

**Status**: ✅ PASSED

**Test Results**:
- Test 1 - Column names: ✅ PASSED
- Test 2 - Superset check: ✅ PASSED
- Test 3 - Precision1 check: ✅ PASSED
- Test 4 - Precision2 check: ✅ PASSED

**Columns**: ['ChTax']

**Observations**:
- Stata:  2,827,726
- Python: 3,146,764
- Common: 2,827,667

**Precision1**: 0.001% obs with std_diff >= 1.00e-02 (tolerance: < 10%)

**Precision2**: 99th percentile diff = 1.95e-09 (tolerance: < 1.00e-03)

**Feedback**:
- Num observations with std_diff >= TOL_DIFF_1: 16/2827667 (0.001%)
- Stata standard deviation: 3.87e+00

---

### ChangeInRecommendation

**Status**: ✅ PASSED

**Test Results**:
- Test 1 - Column names: ✅ PASSED
- Test 2 - Superset check: ✅ PASSED
- Test 3 - Precision1 check: ✅ PASSED
- Test 4 - Precision2 check: ✅ PASSED

**Columns**: ['ChangeInRecommendation']

**Observations**:
- Stata:  450,217
- Python: 450,458
- Common: 449,187

**Precision1**: 0.048% obs with std_diff >= 1.00e-02 (tolerance: < 10%)

**Precision2**: 99th percentile diff = 1.67e-07 (tolerance: < 1.00e-03)

**Feedback**:
- Num observations with std_diff >= TOL_DIFF_1: 215/449187 (0.048%)
- Stata standard deviation: 1.09e+00

---

### CitationsRD

**Status**: ✅ PASSED

**Test Results**:
- Test 1 - Column names: ✅ PASSED
- Test 2 - Superset check: ✅ PASSED
- Test 3 - Precision1 check: ✅ PASSED
- Test 4 - Precision2 check: ✅ PASSED

**Columns**: ['CitationsRD']

**Observations**:
- Stata:  645,360
- Python: 701,940
- Common: 645,360

**Precision1**: 0.002% obs with std_diff >= 1.00e-02 (tolerance: < 10%)

**Precision2**: 99th percentile diff = 0.00e+00 (tolerance: < 1.00e-03)

**Feedback**:
- Num observations with std_diff >= TOL_DIFF_1: 12/645360 (0.002%)
- Stata standard deviation: 4.11e-01

---

### CompEquIss

**Status**: ✅ PASSED

**Test Results**:
- Test 1 - Column names: ✅ PASSED
- Test 2 - Superset check: ✅ PASSED
- Test 3 - Precision1 check: ✅ PASSED
- Test 4 - Precision2 check: ✅ PASSED

**Columns**: ['CompEquIss']

**Observations**:
- Stata:  2,172,395
- Python: 2,581,962
- Common: 2,156,555

**Precision1**: 0.000% obs with std_diff >= 1.00e-02 (tolerance: < 10%)

**Precision2**: 99th percentile diff = 2.26e-06 (tolerance: < 1.00e-03)

**Feedback**:
- Num observations with std_diff >= TOL_DIFF_1: 0/2156555 (0.000%)
- Stata standard deviation: 3.03e+00

---

### CompositeDebtIssuance

**Status**: ✅ PASSED

**Test Results**:
- Test 1 - Column names: ✅ PASSED
- Test 2 - Superset check: ✅ PASSED
- Test 3 - Precision1 check: ✅ PASSED
- Test 4 - Precision2 check: ✅ PASSED

**Columns**: ['CompositeDebtIssuance']

**Observations**:
- Stata:  1,898,755
- Python: 2,157,897
- Common: 1,898,755

**Precision1**: 0.006% obs with std_diff >= 1.00e-02 (tolerance: < 10%)

**Precision2**: 99th percentile diff = 1.77e-07 (tolerance: < 1.00e-03)

**Feedback**:
- Num observations with std_diff >= TOL_DIFF_1: 120/1898755 (0.006%)
- Stata standard deviation: 1.43e+00

---

### ConsRecomm

**Status**: ✅ PASSED

**Test Results**:
- Test 1 - Column names: ✅ PASSED
- Test 2 - Superset check: ✅ PASSED
- Test 3 - Precision1 check: ✅ PASSED
- Test 4 - Precision2 check: ✅ PASSED

**Columns**: ['ConsRecomm']

**Observations**:
- Stata:  134,102
- Python: 372,799
- Common: 133,799

**Precision1**: 0.011% obs with std_diff >= 1.00e-02 (tolerance: < 10%)

**Precision2**: 99th percentile diff = 0.00e+00 (tolerance: < 1.00e-03)

**Feedback**:
- Num observations with std_diff >= TOL_DIFF_1: 15/133799 (0.011%)
- Stata standard deviation: 4.41e-01

---

### ConvDebt

**Status**: ✅ PASSED

**Test Results**:
- Test 1 - Column names: ✅ PASSED
- Test 2 - Superset check: ✅ PASSED
- Test 3 - Precision1 check: ✅ PASSED
- Test 4 - Precision2 check: ✅ PASSED

**Columns**: ['ConvDebt']

**Observations**:
- Stata:  3,624,363
- Python: 3,625,491
- Common: 3,624,363

**Precision1**: 0.001% obs with std_diff >= 1.00e-02 (tolerance: < 10%)

**Precision2**: 99th percentile diff = 0.00e+00 (tolerance: < 1.00e-03)

**Feedback**:
- Num observations with std_diff >= TOL_DIFF_1: 24/3624363 (0.001%)
- Stata standard deviation: 3.39e-01

---

### CoskewACX

**Status**: ✅ PASSED

**Test Results**:
- Test 1 - Column names: ✅ PASSED
- Test 2 - Superset check: ✅ PASSED
- Test 3 - Precision1 check: ✅ PASSED
- Test 4 - Precision2 check: ✅ PASSED

**Columns**: ['CoskewACX']

**Observations**:
- Stata:  4,179,145
- Python: 4,179,145
- Common: 4,179,145

**Precision1**: 0.000% obs with std_diff >= 1.00e-02 (tolerance: < 10%)

**Precision2**: 99th percentile diff = 3.83e-04 (tolerance: < 1.00e-03)

**Feedback**:
- Num observations with std_diff >= TOL_DIFF_1: 16/4179145 (0.000%)
- Stata standard deviation: 3.36e-01

---

### Coskewness

**Status**: ✅ PASSED

**Test Results**:
- Test 1 - Column names: ✅ PASSED
- Test 2 - Superset check: ✅ PASSED
- Test 3 - Precision1 check: ✅ PASSED
- Test 4 - Precision2 check: ✅ PASSED

**Columns**: ['Coskewness']

**Observations**:
- Stata:  4,609,158
- Python: 4,609,158
- Common: 4,609,158

**Precision1**: 0.000% obs with std_diff >= 1.00e-02 (tolerance: < 10%)

**Precision2**: 99th percentile diff = 5.05e-04 (tolerance: < 1.00e-03)

**Feedback**:
- Num observations with std_diff >= TOL_DIFF_1: 4/4609158 (0.000%)
- Stata standard deviation: 3.83e-01

---

### CredRatDG

**Status**: ✅ PASSED

**Test Results**:
- Test 1 - Column names: ✅ PASSED
- Test 2 - Superset check: ✅ PASSED
- Test 3 - Precision1 check: ✅ PASSED
- Test 4 - Precision2 check: ✅ PASSED

**Columns**: ['CredRatDG']

**Observations**:
- Stata:  2,559,713
- Python: 2,559,715
- Common: 2,559,713

**Precision1**: 0.941% obs with std_diff >= 1.00e-02 (tolerance: < 10%)

**Precision2**: 99th percentile diff = 0.00e+00 (tolerance: < 1.00e-03)

**Feedback**:
- Num observations with std_diff >= TOL_DIFF_1: 24086/2559713 (0.941%)
- Stata standard deviation: 1.51e-01

---

### CustomerMomentum

**Status**: ✅ PASSED

**Test Results**:
- Test 1 - Column names: ✅ PASSED
- Test 2 - Superset check: ✅ PASSED
- Test 3 - Precision1 check: ✅ PASSED
- Test 4 - Precision2 check: ✅ PASSED

**Columns**: ['CustomerMomentum']

**Observations**:
- Stata:  356,600
- Python: 356,510
- Common: 356,462

**Precision1**: 0.006% obs with std_diff >= 1.00e-02 (tolerance: < 10%)

**Precision2**: 99th percentile diff = 1.00e-08 (tolerance: < 1.00e-03)

**Feedback**:
- Num observations with std_diff >= TOL_DIFF_1: 23/356462 (0.006%)
- Stata standard deviation: 1.11e-01

---

### DebtIssuance

**Status**: ✅ PASSED

**Test Results**:
- Test 1 - Column names: ✅ PASSED
- Test 2 - Superset check: ✅ PASSED
- Test 3 - Precision1 check: ✅ PASSED
- Test 4 - Precision2 check: ✅ PASSED

**Columns**: ['DebtIssuance']

**Observations**:
- Stata:  2,725,997
- Python: 2,726,038
- Common: 2,725,997

**Precision1**: 0.000% obs with std_diff >= 1.00e-02 (tolerance: < 10%)

**Precision2**: 99th percentile diff = 0.00e+00 (tolerance: < 1.00e-03)

**Feedback**:
- Num observations with std_diff >= TOL_DIFF_1: 0/2725997 (0.000%)
- Stata standard deviation: 5.00e-01

---

### DelBreadth

**Status**: ✅ PASSED

**Test Results**:
- Test 1 - Column names: ✅ PASSED
- Test 2 - Superset check: ✅ PASSED
- Test 3 - Precision1 check: ✅ PASSED
- Test 4 - Precision2 check: ✅ PASSED

**Columns**: ['DelBreadth']

**Observations**:
- Stata:  1,062,671
- Python: 1,570,777
- Common: 1,062,671

**Precision1**: 0.000% obs with std_diff >= 1.00e-02 (tolerance: < 10%)

**Precision2**: 99th percentile diff = 1.00e-07 (tolerance: < 1.00e-03)

**Feedback**:
- Num observations with std_diff >= TOL_DIFF_1: 0/1062671 (0.000%)
- Stata standard deviation: 8.89e-01

---

### DelCOA

**Status**: ✅ PASSED

**Test Results**:
- Test 1 - Column names: ✅ PASSED
- Test 2 - Superset check: ✅ PASSED
- Test 3 - Precision1 check: ✅ PASSED
- Test 4 - Precision2 check: ✅ PASSED

**Columns**: ['DelCOA']

**Observations**:
- Stata:  3,295,155
- Python: 3,311,811
- Common: 3,295,155

**Precision1**: 0.002% obs with std_diff >= 1.00e-02 (tolerance: < 10%)

**Precision2**: 99th percentile diff = 2.31e-08 (tolerance: < 1.00e-03)

**Feedback**:
- Num observations with std_diff >= TOL_DIFF_1: 60/3295155 (0.002%)
- Stata standard deviation: 1.21e-01

---

### DelCOL

**Status**: ✅ PASSED

**Test Results**:
- Test 1 - Column names: ✅ PASSED
- Test 2 - Superset check: ✅ PASSED
- Test 3 - Precision1 check: ✅ PASSED
- Test 4 - Precision2 check: ✅ PASSED

**Columns**: ['DelCOL']

**Observations**:
- Stata:  3,259,701
- Python: 3,276,202
- Common: 3,259,701

**Precision1**: 0.006% obs with std_diff >= 1.00e-02 (tolerance: < 10%)

**Precision2**: 99th percentile diff = 1.73e-08 (tolerance: < 1.00e-03)

**Feedback**:
- Num observations with std_diff >= TOL_DIFF_1: 204/3259701 (0.006%)
- Stata standard deviation: 1.17e-01

---

### DelDRC

**Status**: ✅ PASSED

**Test Results**:
- Test 1 - Column names: ✅ PASSED
- Test 2 - Superset check: ✅ PASSED
- Test 3 - Precision1 check: ✅ PASSED
- Test 4 - Precision2 check: ✅ PASSED

**Columns**: ['DelDRC']

**Observations**:
- Stata:  460,159
- Python: 462,430
- Common: 460,159

**Precision1**: 0.010% obs with std_diff >= 1.00e-02 (tolerance: < 10%)

**Precision2**: 99th percentile diff = 5.36e-09 (tolerance: < 1.00e-03)

**Feedback**:
- Num observations with std_diff >= TOL_DIFF_1: 48/460159 (0.010%)
- Stata standard deviation: 4.53e-02

---

### DelEqu

**Status**: ✅ PASSED

**Test Results**:
- Test 1 - Column names: ✅ PASSED
- Test 2 - Superset check: ✅ PASSED
- Test 3 - Precision1 check: ✅ PASSED
- Test 4 - Precision2 check: ✅ PASSED

**Columns**: ['DelEqu']

**Observations**:
- Stata:  3,194,475
- Python: 3,195,504
- Common: 3,194,475

**Precision1**: 0.001% obs with std_diff >= 1.00e-02 (tolerance: < 10%)

**Precision2**: 99th percentile diff = 4.56e-08 (tolerance: < 1.00e-03)

**Feedback**:
- Num observations with std_diff >= TOL_DIFF_1: 36/3194475 (0.001%)
- Stata standard deviation: 5.46e-01

---

### DelFINL

**Status**: ✅ PASSED

**Test Results**:
- Test 1 - Column names: ✅ PASSED
- Test 2 - Superset check: ✅ PASSED
- Test 3 - Precision1 check: ✅ PASSED
- Test 4 - Precision2 check: ✅ PASSED

**Columns**: ['DelFINL']

**Observations**:
- Stata:  3,250,876
- Python: 3,251,941
- Common: 3,250,876

**Precision1**: 0.006% obs with std_diff >= 1.00e-02 (tolerance: < 10%)

**Precision2**: 99th percentile diff = 3.11e-08 (tolerance: < 1.00e-03)

**Feedback**:
- Num observations with std_diff >= TOL_DIFF_1: 192/3250876 (0.006%)
- Stata standard deviation: 1.77e-01

---

### DelLTI

**Status**: ✅ PASSED

**Test Results**:
- Test 1 - Column names: ✅ PASSED
- Test 2 - Superset check: ✅ PASSED
- Test 3 - Precision1 check: ✅ PASSED
- Test 4 - Precision2 check: ✅ PASSED

**Columns**: ['DelLTI']

**Observations**:
- Stata:  3,295,155
- Python: 3,296,136
- Common: 3,295,155

**Precision1**: 0.005% obs with std_diff >= 1.00e-02 (tolerance: < 10%)

**Precision2**: 99th percentile diff = 1.44e-08 (tolerance: < 1.00e-03)

**Feedback**:
- Num observations with std_diff >= TOL_DIFF_1: 180/3295155 (0.005%)
- Stata standard deviation: 7.76e-02

---

### DelNetFin

**Status**: ✅ PASSED

**Test Results**:
- Test 1 - Column names: ✅ PASSED
- Test 2 - Superset check: ✅ PASSED
- Test 3 - Precision1 check: ✅ PASSED
- Test 4 - Precision2 check: ✅ PASSED

**Columns**: ['DelNetFin']

**Observations**:
- Stata:  3,250,876
- Python: 3,251,941
- Common: 3,250,876

**Precision1**: 0.009% obs with std_diff >= 1.00e-02 (tolerance: < 10%)

**Precision2**: 99th percentile diff = 5.53e-08 (tolerance: < 1.00e-03)

**Feedback**:
- Num observations with std_diff >= TOL_DIFF_1: 300/3250876 (0.009%)
- Stata standard deviation: 2.05e-01

---

### DivInit

**Status**: ✅ PASSED

**Test Results**:
- Test 1 - Column names: ✅ PASSED
- Test 2 - Superset check: ✅ PASSED
- Test 3 - Precision1 check: ✅ PASSED
- Test 4 - Precision2 check: ✅ PASSED

**Columns**: ['DivInit']

**Observations**:
- Stata:  4,047,630
- Python: 4,047,630
- Common: 4,047,630

**Precision1**: 0.007% obs with std_diff >= 1.00e-02 (tolerance: < 10%)

**Precision2**: 99th percentile diff = 0.00e+00 (tolerance: < 1.00e-03)

**Feedback**:
- Num observations with std_diff >= TOL_DIFF_1: 287/4047630 (0.007%)
- Stata standard deviation: 1.37e-01

---

### DivOmit

**Status**: ✅ PASSED

**Test Results**:
- Test 1 - Column names: ✅ PASSED
- Test 2 - Superset check: ✅ PASSED
- Test 3 - Precision1 check: ✅ PASSED
- Test 4 - Precision2 check: ✅ PASSED

**Columns**: ['DivOmit']

**Observations**:
- Stata:  4,047,630
- Python: 4,047,630
- Common: 4,047,630

**Precision1**: 0.003% obs with std_diff >= 1.00e-02 (tolerance: < 10%)

**Precision2**: 99th percentile diff = 0.00e+00 (tolerance: < 1.00e-03)

**Feedback**:
- Num observations with std_diff >= TOL_DIFF_1: 123/4047630 (0.003%)
- Stata standard deviation: 6.22e-02

---

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
- Python: 4,041,685
- Common: 1,775,337

**Precision1**: 5.214% obs with std_diff >= 1.00e-02 (tolerance: < 10%)

**Precision2**: 99th percentile diff = 1.00e+00 (tolerance: < 1.00e-03)

**Feedback**:
- Num observations with std_diff >= TOL_DIFF_1: 92565/1775337 (5.214%)
- Stata standard deviation: 4.97e-01

**Most Recent Bad Observations**:
```
   permno  yyyymm  python  stata  diff
0   13407  202412       0      1    -1
1   14542  202412       0      1    -1
2   15920  202412       0      1    -1
3   16119  202412       0      1    -1
4   16611  202412       0      1    -1
5   17036  202412       0      1    -1
6   20447  202412       0      1    -1
7   20998  202412       0      1    -1
8   21372  202412       0      1    -1
9   21605  202412       0      1    -1
```

**Largest Differences**:
```
   permno  yyyymm  python  stata  diff
0   10001  198603       0      1    -1
1   10001  198604       0      1    -1
2   10001  198606       0      1    -1
3   10001  198607       0      1    -1
4   10001  198609       0      1    -1
5   10001  198610       0      1    -1
6   10001  198612       0      1    -1
7   10001  198701       0      1    -1
8   10001  201507       0      1    -1
9   10001  201510       0      1    -1
```

---

### DivYieldST

**Status**: ✅ PASSED

**Test Results**:
- Test 1 - Column names: ✅ PASSED
- Test 2 - Superset check: ✅ PASSED
- Test 3 - Precision1 check: ✅ PASSED
- Test 4 - Precision2 check: ✅ PASSED

**Columns**: ['DivYieldST']

**Observations**:
- Stata:  1,591,700
- Python: 1,601,392
- Common: 1,591,697

**Precision1**: 0.069% obs with std_diff >= 1.00e-02 (tolerance: < 10%)

**Precision2**: 99th percentile diff = 0.00e+00 (tolerance: < 1.00e-03)

**Feedback**:
- Num observations with std_diff >= TOL_DIFF_1: 1092/1591697 (0.069%)
- Stata standard deviation: 1.03e+00

---

### DolVol

**Status**: ✅ PASSED

**Test Results**:
- Test 1 - Column names: ✅ PASSED
- Test 2 - Superset check: ✅ PASSED
- Test 3 - Precision1 check: ✅ PASSED
- Test 4 - Precision2 check: ✅ PASSED

**Columns**: ['DolVol']

**Observations**:
- Stata:  4,640,493
- Python: 4,650,572
- Common: 4,640,493

**Precision1**: 0.000% obs with std_diff >= 1.00e-02 (tolerance: < 10%)

**Precision2**: 99th percentile diff = 2.84e-07 (tolerance: < 1.00e-03)

**Feedback**:
- Num observations with std_diff >= TOL_DIFF_1: 0/4640493 (0.000%)
- Stata standard deviation: 3.11e+00

---

### DownRecomm

**Status**: ❌ FAILED

**Test Results**:
- Test 1 - Column names: ✅ PASSED
- Test 2 - Superset check: ❌ FAILED (Python missing 14792 Stata observations)
- Test 3 - Precision1 check: ✅ PASSED
- Test 4 - Precision2 check: ✅ PASSED

**Columns**: ['DownRecomm']

**Observations**:
- Stata:  463,983
- Python: 450,458
- Common: 449,191

**Precision1**: 0.025% obs with std_diff >= 1.00e-02 (tolerance: < 10%)

**Precision2**: 99th percentile diff = 0.00e+00 (tolerance: < 1.00e-03)

**Missing Observations Sample**:
```
 index  permno  yyyymm  DownRecomm
     0   10001  199311           0
     1   10002  200210           0
     2   10010  199311           0
     3   10011  199511           0
     4   10012  199402           0
     5   10016  199312           0
     6   10019  199403           0
     7   10025  199801           0
     8   10026  199311           0
     9   10028  202103           0
```

**Feedback**:
- Num observations with std_diff >= TOL_DIFF_1: 114/449191 (0.025%)
- Stata standard deviation: 4.86e-01

---

### EBM

**Status**: ✅ PASSED

**Test Results**:
- Test 1 - Column names: ✅ PASSED
- Test 2 - Superset check: ✅ PASSED
- Test 3 - Precision1 check: ✅ PASSED
- Test 4 - Precision2 check: ✅ PASSED

**Columns**: ['EBM']

**Observations**:
- Stata:  2,924,820
- Python: 2,924,826
- Common: 2,924,820

**Precision1**: 0.001% obs with std_diff >= 1.00e-02 (tolerance: < 10%)

**Precision2**: 99th percentile diff = 7.27e-06 (tolerance: < 1.00e-03)

**Feedback**:
- Num observations with std_diff >= TOL_DIFF_1: 43/2924820 (0.001%)
- Stata standard deviation: 3.35e+02

---

### EP

**Status**: ✅ PASSED

**Test Results**:
- Test 1 - Column names: ✅ PASSED
- Test 2 - Superset check: ✅ PASSED
- Test 3 - Precision1 check: ✅ PASSED
- Test 4 - Precision2 check: ✅ PASSED

**Columns**: ['EP']

**Observations**:
- Stata:  2,203,166
- Python: 2,203,166
- Common: 2,203,166

**Precision1**: 0.000% obs with std_diff >= 1.00e-02 (tolerance: < 10%)

**Precision2**: 99th percentile diff = 1.18e-08 (tolerance: < 1.00e-03)

**Feedback**:
- Num observations with std_diff >= TOL_DIFF_1: 0/2203166 (0.000%)
- Stata standard deviation: 3.02e-01

---

### EarnSupBig

**Status**: ❌ FAILED

**Test Results**:
- Test 1 - Column names: ✅ PASSED
- Test 2 - Superset check: ❌ FAILED (Python missing 87621 Stata observations)
- Test 3 - Precision1 check: ✅ PASSED
- Test 4 - Precision2 check: ❌ FAILED

**Columns**: ['EarnSupBig']

**Observations**:
- Stata:  2,327,518
- Python: 2,533,035
- Common: 2,239,897

**Precision1**: 0.156% obs with std_diff >= 1.00e-02 (tolerance: < 10%)

**Precision2**: 99th percentile diff = 6.51e+00 (tolerance: < 1.00e-03)

**Missing Observations Sample**:
```
 index  permno  yyyymm  EarnSupBig
     0   10002  200811   -0.755143
     1   10002  200812   -1.854773
     2   10003  198806   -0.001391
     3   10003  198807   -0.060459
     4   10003  198808   -0.047608
     5   10006  197804   -2.586295
     6   10006  197805   -2.586295
     7   10006  197806    0.224887
     8   10006  197807    0.224887
     9   10006  197808    0.224887
```

**Feedback**:
- Num observations with std_diff >= TOL_DIFF_1: 3489/2239897 (0.156%)
- Stata standard deviation: 4.73e+12

**Most Recent Bad Observations**:
```
   permno  yyyymm    python         stata          diff
0   10100  200105 -0.382466 -5.363412e+13  5.363412e+13
1   10488  200105 -0.382466 -5.363412e+13  5.363412e+13
2   10680  200105 -0.382466 -5.363412e+13  5.363412e+13
3   11833  200105 -0.382466 -5.363412e+13  5.363412e+13
4   20248  200105 -0.382466 -5.363412e+13  5.363412e+13
5   39773  200105 -0.382466 -5.363412e+13  5.363412e+13
6   62296  200105 -0.382466 -5.363412e+13  5.363412e+13
7   69200  200105 -0.382466 -5.363412e+13  5.363412e+13
8   75526  200105 -0.382466 -5.363412e+13  5.363412e+13
9   75609  200105 -0.382466 -5.363412e+13  5.363412e+13
```

**Largest Differences**:
```
   permno  yyyymm    python         stata          diff
0   10613  197309  0.188875  3.580440e+14 -3.580440e+14
1   11165  197309  0.188875  3.580440e+14 -3.580440e+14
2   12141  197309  0.188875  3.580440e+14 -3.580440e+14
3   14227  197309  0.188875  3.580440e+14 -3.580440e+14
4   14569  197309  0.188875  3.580440e+14 -3.580440e+14
5   14702  197309  0.188875  3.580440e+14 -3.580440e+14
6   15078  197309  0.188875  3.580440e+14 -3.580440e+14
7   15457  197309  0.188875  3.580440e+14 -3.580440e+14
8   16986  197309  0.188875  3.580440e+14 -3.580440e+14
9   17523  197309  0.188875  3.580440e+14 -3.580440e+14
```

---

### EarningsConsistency

**Status**: ✅ PASSED

**Test Results**:
- Test 1 - Column names: ✅ PASSED
- Test 2 - Superset check: ✅ PASSED
- Test 3 - Precision1 check: ✅ PASSED
- Test 4 - Precision2 check: ✅ PASSED

**Columns**: ['EarningsConsistency']

**Observations**:
- Stata:  1,386,008
- Python: 1,521,466
- Common: 1,386,008

**Precision1**: 0.000% obs with std_diff >= 1.00e-02 (tolerance: < 10%)

**Precision2**: 99th percentile diff = 1.51e-07 (tolerance: < 1.00e-03)

**Feedback**:
- Num observations with std_diff >= TOL_DIFF_1: 0/1386008 (0.000%)
- Stata standard deviation: 1.72e+00

---

### EarningsForecastDisparity

**Status**: ✅ PASSED

**Test Results**:
- Test 1 - Column names: ✅ PASSED
- Test 2 - Superset check: ✅ PASSED
- Test 3 - Precision1 check: ✅ PASSED
- Test 4 - Precision2 check: ✅ PASSED

**Columns**: ['EarningsForecastDisparity']

**Observations**:
- Stata:  975,097
- Python: 975,050
- Common: 972,933

**Precision1**: 0.079% obs with std_diff >= 1.00e-02 (tolerance: < 10%)

**Precision2**: 99th percentile diff = 2.00e-05 (tolerance: < 1.00e-03)

**Feedback**:
- Num observations with std_diff >= TOL_DIFF_1: 766/972933 (0.079%)
- Stata standard deviation: 5.53e+02

---

### EarningsStreak

**Status**: ✅ PASSED

**Test Results**:
- Test 1 - Column names: ✅ PASSED
- Test 2 - Superset check: ✅ PASSED
- Test 3 - Precision1 check: ✅ PASSED
- Test 4 - Precision2 check: ✅ PASSED

**Columns**: ['EarningsStreak']

**Observations**:
- Stata:  1,225,060
- Python: 1,225,437
- Common: 1,222,769

**Precision1**: 0.007% obs with std_diff >= 1.00e-02 (tolerance: < 10%)

**Precision2**: 99th percentile diff = 7.78e-09 (tolerance: < 1.00e-03)

**Feedback**:
- Num observations with std_diff >= TOL_DIFF_1: 84/1222769 (0.007%)
- Stata standard deviation: 3.16e+00

---

### EarningsSurprise

**Status**: ✅ PASSED

**Test Results**:
- Test 1 - Column names: ✅ PASSED
- Test 2 - Superset check: ✅ PASSED
- Test 3 - Precision1 check: ✅ PASSED
- Test 4 - Precision2 check: ✅ PASSED

**Columns**: ['EarningsSurprise']

**Observations**:
- Stata:  2,324,394
- Python: 2,324,021
- Common: 2,323,954

**Precision1**: 0.031% obs with std_diff >= 1.00e-02 (tolerance: < 10%)

**Precision2**: 99th percentile diff = 6.44e-07 (tolerance: < 1.00e-03)

**Feedback**:
- Num observations with std_diff >= TOL_DIFF_1: 714/2323954 (0.031%)
- Stata standard deviation: 1.36e+01

---

### EntMult

**Status**: ✅ PASSED

**Test Results**:
- Test 1 - Column names: ✅ PASSED
- Test 2 - Superset check: ✅ PASSED
- Test 3 - Precision1 check: ✅ PASSED
- Test 4 - Precision2 check: ✅ PASSED

**Columns**: ['EntMult']

**Observations**:
- Stata:  2,407,850
- Python: 2,408,497
- Common: 2,407,843

**Precision1**: 0.000% obs with std_diff >= 1.00e-02 (tolerance: < 10%)

**Precision2**: 99th percentile diff = 4.17e-06 (tolerance: < 1.00e-03)

**Feedback**:
- Num observations with std_diff >= TOL_DIFF_1: 0/2407843 (0.000%)
- Stata standard deviation: 7.53e+02

---

### EquityDuration

**Status**: ✅ PASSED

**Test Results**:
- Test 1 - Column names: ✅ PASSED
- Test 2 - Superset check: ✅ PASSED
- Test 3 - Precision1 check: ✅ PASSED
- Test 4 - Precision2 check: ✅ PASSED

**Columns**: ['EquityDuration']

**Observations**:
- Stata:  3,124,663
- Python: 3,201,768
- Common: 3,124,663

**Precision1**: 0.000% obs with std_diff >= 1.00e-02 (tolerance: < 10%)

**Precision2**: 99th percentile diff = 6.79e-06 (tolerance: < 1.00e-03)

**Feedback**:
- Num observations with std_diff >= TOL_DIFF_1: 0/3124663 (0.000%)
- Stata standard deviation: 5.69e+09

---

### ExchSwitch

**Status**: ✅ PASSED

**Test Results**:
- Test 1 - Column names: ✅ PASSED
- Test 2 - Superset check: ✅ PASSED
- Test 3 - Precision1 check: ✅ PASSED
- Test 4 - Precision2 check: ✅ PASSED

**Columns**: ['ExchSwitch']

**Observations**:
- Stata:  4,047,630
- Python: 4,047,630
- Common: 4,047,630

**Precision1**: 0.047% obs with std_diff >= 1.00e-02 (tolerance: < 10%)

**Precision2**: 99th percentile diff = 0.00e+00 (tolerance: < 1.00e-03)

**Feedback**:
- Num observations with std_diff >= TOL_DIFF_1: 1899/4047630 (0.047%)
- Stata standard deviation: 9.46e-02

---

### ExclExp

**Status**: ✅ PASSED

**Test Results**:
- Test 1 - Column names: ✅ PASSED
- Test 2 - Superset check: ✅ PASSED
- Test 3 - Precision1 check: ✅ PASSED
- Test 4 - Precision2 check: ✅ PASSED

**Columns**: ['ExclExp']

**Observations**:
- Stata:  1,726,232
- Python: 1,762,541
- Common: 1,724,203

**Precision1**: 0.108% obs with std_diff >= 1.00e-02 (tolerance: < 10%)

**Precision2**: 99th percentile diff = 3.00e-08 (tolerance: < 1.00e-03)

**Feedback**:
- Num observations with std_diff >= TOL_DIFF_1: 1864/1724203 (0.108%)
- Stata standard deviation: 3.56e-01

---

### FEPS

**Status**: ✅ PASSED

**Test Results**:
- Test 1 - Column names: ✅ PASSED
- Test 2 - Superset check: ✅ PASSED
- Test 3 - Precision1 check: ✅ PASSED
- Test 4 - Precision2 check: ✅ PASSED

**Columns**: ['FEPS']

**Observations**:
- Stata:  1,957,995
- Python: 1,958,211
- Common: 1,954,911

**Precision1**: 0.026% obs with std_diff >= 1.00e-02 (tolerance: < 10%)

**Precision2**: 99th percentile diff = 2.00e-07 (tolerance: < 1.00e-03)

**Feedback**:
- Num observations with std_diff >= TOL_DIFF_1: 513/1954911 (0.026%)
- Stata standard deviation: 1.99e+02

---

### FR

**Status**: ✅ PASSED

**Test Results**:
- Test 1 - Column names: ✅ PASSED
- Test 2 - Superset check: ✅ PASSED
- Test 3 - Precision1 check: ✅ PASSED
- Test 4 - Precision2 check: ✅ PASSED

**Columns**: ['FR']

**Observations**:
- Stata:  683,893
- Python: 683,893
- Common: 683,893

**Precision1**: 0.000% obs with std_diff >= 1.00e-02 (tolerance: < 10%)

**Precision2**: 99th percentile diff = 9.16e-08 (tolerance: < 1.00e-03)

**Feedback**:
- Num observations with std_diff >= TOL_DIFF_1: 0/683893 (0.000%)
- Stata standard deviation: 7.74e-01

---

### FirmAge

**Status**: ✅ PASSED

**Test Results**:
- Test 1 - Column names: ✅ PASSED
- Test 2 - Superset check: ✅ PASSED
- Test 3 - Precision1 check: ✅ PASSED
- Test 4 - Precision2 check: ✅ PASSED

**Columns**: ['FirmAge']

**Observations**:
- Stata:  4,045,796
- Python: 4,045,796
- Common: 4,045,796

**Precision1**: 0.000% obs with std_diff >= 1.00e-02 (tolerance: < 10%)

**Precision2**: 99th percentile diff = 0.00e+00 (tolerance: < 1.00e-03)

**Feedback**:
- Num observations with std_diff >= TOL_DIFF_1: 0/4045796 (0.000%)
- Stata standard deviation: 1.70e+02

---

### FirmAgeMom

**Status**: ❌ FAILED

**Test Results**:
- Test 1 - Column names: ✅ PASSED
- Test 2 - Superset check: ❌ FAILED (Python missing 148535 Stata observations)
- Test 3 - Precision1 check: ✅ PASSED
- Test 4 - Precision2 check: ✅ PASSED

**Columns**: ['FirmAgeMom']

**Observations**:
- Stata:  550,434
- Python: 440,809
- Common: 401,899

**Precision1**: 0.000% obs with std_diff >= 1.00e-02 (tolerance: < 10%)

**Precision2**: 99th percentile diff = 3.64e-08 (tolerance: < 1.00e-03)

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

### ForecastDispersion

**Status**: ✅ PASSED

**Test Results**:
- Test 1 - Column names: ✅ PASSED
- Test 2 - Superset check: ✅ PASSED
- Test 3 - Precision1 check: ✅ PASSED
- Test 4 - Precision2 check: ✅ PASSED

**Columns**: ['ForecastDispersion']

**Observations**:
- Stata:  1,616,983
- Python: 1,620,034
- Common: 1,614,371

**Precision1**: 0.070% obs with std_diff >= 1.00e-02 (tolerance: < 10%)

**Precision2**: 99th percentile diff = 5.71e-08 (tolerance: < 1.00e-03)

**Feedback**:
- Num observations with std_diff >= TOL_DIFF_1: 1132/1614371 (0.070%)
- Stata standard deviation: 1.42e+00

---

### Frontier

**Status**: ❌ FAILED

**Test Results**:
- Test 1 - Column names: ✅ PASSED
- Test 2 - Superset check: ✅ PASSED
- Test 3 - Precision1 check: ❌ FAILED
- Test 4 - Precision2 check: ❌ FAILED

**Columns**: ['Frontier']

**Observations**:
- Stata:  1,221,161
- Python: 1,308,554
- Common: 1,221,161

**Precision1**: 84.223% obs with std_diff >= 1.00e-02 (tolerance: < 10%)

**Precision2**: 99th percentile diff = 5.44e-01 (tolerance: < 1.00e-03)

**Feedback**:
- Num observations with std_diff >= TOL_DIFF_1: 1028495/1221161 (84.223%)
- Stata standard deviation: 9.78e-01

**Most Recent Bad Observations**:
```
   permno  yyyymm    python     stata      diff
0   10026  202412 -0.677199 -0.780603  0.103404
1   10028  202412 -0.391396 -0.520535  0.129139
2   10066  202412  0.443135  0.568824 -0.125689
3   10104  202412 -2.215219 -1.953049 -0.262170
4   10107  202412 -1.635750 -1.238720 -0.397031
5   10145  202412 -1.328160 -0.719358 -0.608802
6   10200  202412 -0.170885 -0.101468 -0.069417
7   10220  202412 -1.211545 -1.234168  0.022623
8   10253  202412  3.311301  3.423937 -0.112636
9   10318  202412 -0.545215 -0.670803  0.125587
```

**Largest Differences**:
```
   permno  yyyymm        python      stata      diff
0   49315  197306  4.874287e+00  10.828367 -5.954080
1   49315  197307  2.170007e+00   7.243619 -5.073612
2   49315  197308  1.256226e+00   5.702786 -4.446560
3   49315  197309  6.350514e-01   4.663649 -4.028598
4   49315  197310  3.600313e-01   4.100815 -3.740783
5   49315  197311  6.525662e-01   4.171880 -3.519314
6   89631  200406 -2.398082e-14  -3.468813  3.468813
7   12111  199211 -3.463358e-01  -3.732341  3.386005
8   12111  199212 -2.203209e-01  -3.593663  3.373342
9   49315  197312  2.136465e-01   3.569990 -3.356343
```

---

### GP

**Status**: ✅ PASSED

**Test Results**:
- Test 1 - Column names: ✅ PASSED
- Test 2 - Superset check: ✅ PASSED
- Test 3 - Precision1 check: ✅ PASSED
- Test 4 - Precision2 check: ✅ PASSED

**Columns**: ['GP']

**Observations**:
- Stata:  2,970,775
- Python: 2,972,251
- Common: 2,970,775

**Precision1**: 0.006% obs with std_diff >= 1.00e-02 (tolerance: < 10%)

**Precision2**: 99th percentile diff = 5.12e-08 (tolerance: < 1.00e-03)

**Feedback**:
- Num observations with std_diff >= TOL_DIFF_1: 180/2970775 (0.006%)
- Stata standard deviation: 4.63e-01

---

### Governance

**Status**: ✅ PASSED

**Test Results**:
- Test 1 - Column names: ✅ PASSED
- Test 2 - Superset check: ✅ PASSED
- Test 3 - Precision1 check: ✅ PASSED
- Test 4 - Precision2 check: ✅ PASSED

**Columns**: ['Governance']

**Observations**:
- Stata:  334,058
- Python: 334,058
- Common: 334,058

**Precision1**: 0.000% obs with std_diff >= 1.00e-02 (tolerance: < 10%)

**Precision2**: 99th percentile diff = 0.00e+00 (tolerance: < 1.00e-03)

**Feedback**:
- Num observations with std_diff >= TOL_DIFF_1: 0/334058 (0.000%)
- Stata standard deviation: 2.57e+00

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

**Precision1**: 0.000% obs with std_diff >= 1.00e-02 (tolerance: < 10%)

**Precision2**: 99th percentile diff = 6.57e-08 (tolerance: < 1.00e-03)

**Feedback**:
- Num observations with std_diff >= TOL_DIFF_1: 0/898855 (0.000%)
- Stata standard deviation: 4.75e-01

---

### Herf

**Status**: ✅ PASSED

**Test Results**:
- Test 1 - Column names: ✅ PASSED
- Test 2 - Superset check: ✅ PASSED
- Test 3 - Precision1 check: ✅ PASSED
- Test 4 - Precision2 check: ✅ PASSED

**Columns**: ['Herf']

**Observations**:
- Stata:  3,158,336
- Python: 3,165,145
- Common: 3,158,336

**Precision1**: 0.787% obs with std_diff >= 1.00e-02 (tolerance: < 10%)

**Precision2**: 99th percentile diff = 1.94e-04 (tolerance: < 1.00e-03)

**Feedback**:
- Num observations with std_diff >= TOL_DIFF_1: 24846/3158336 (0.787%)
- Stata standard deviation: 2.78e-01

---

### HerfAsset

**Status**: ❌ FAILED

**Test Results**:
- Test 1 - Column names: ✅ PASSED
- Test 2 - Superset check: ✅ PASSED
- Test 3 - Precision1 check: ✅ PASSED
- Test 4 - Precision2 check: ❌ FAILED

**Columns**: ['HerfAsset']

**Observations**:
- Stata:  2,547,057
- Python: 2,553,214
- Common: 2,547,057

**Precision1**: 1.444% obs with std_diff >= 1.00e-02 (tolerance: < 10%)

**Precision2**: 99th percentile diff = 8.16e-03 (tolerance: < 1.00e-03)

**Feedback**:
- Num observations with std_diff >= TOL_DIFF_1: 36791/2547057 (1.444%)
- Stata standard deviation: 2.78e-01

**Most Recent Bad Observations**:
```
   permno  yyyymm    python     stata      diff
0   11153  202412  0.332202  0.372792 -0.040590
1   11379  202412  0.626341  0.635870 -0.009529
2   12928  202412  0.261507  0.459600 -0.198092
3   13563  202412  0.022453  0.019441  0.003012
4   13798  202412  0.430744  0.437600 -0.006856
5   14051  202412  0.132821  0.139013 -0.006191
6   14469  202412  0.026686  0.019441  0.007244
7   15793  202412  0.022510  0.019441  0.003069
8   16773  202412  0.033162  0.019419  0.013743
9   18065  202412  0.583155  0.542521  0.040635
```

**Largest Differences**:
```
   permno  yyyymm    python     stata      diff
0   11511  201705  0.355296  1.000000 -0.644704
1   53137  198208  0.678208  0.034624  0.643584
2   57015  200705  0.376106  1.000000 -0.623894
3   12715  198407  0.376506  1.000000 -0.623494
4   11511  201706  0.382062  1.000000 -0.617938
5   53137  198209  0.651516  0.034969  0.616548
6   57015  200706  0.403188  1.000000 -0.596812
7   12715  198408  0.403625  1.000000 -0.596375
8   73091  199705  0.372989  0.964393 -0.591403
9   11511  201707  0.408854  1.000000 -0.591145
```

---

### HerfBE

**Status**: ❌ FAILED

**Test Results**:
- Test 1 - Column names: ✅ PASSED
- Test 2 - Superset check: ✅ PASSED
- Test 3 - Precision1 check: ✅ PASSED
- Test 4 - Precision2 check: ❌ FAILED

**Columns**: ['HerfBE']

**Observations**:
- Stata:  2,547,057
- Python: 2,553,214
- Common: 2,547,057

**Precision1**: 0.001% obs with std_diff >= 1.00e-02 (tolerance: < 10%)

**Precision2**: 99th percentile diff = 9.28e-03 (tolerance: < 1.00e-03)

**Feedback**:
- Num observations with std_diff >= TOL_DIFF_1: 32/2547057 (0.001%)
- Stata standard deviation: 6.72e+03

**Most Recent Bad Observations**:
```
   permno  yyyymm      python        stata        diff
0   91612  201612  801.701333   874.567580  -72.866247
1   91612  201611  798.777117   898.602302  -99.825186
2   91612  201610  798.330272   927.064597 -128.734325
3   91612  201609  797.882863   957.424379 -159.541516
4   91612  201608  797.428832   989.871658 -192.442826
5   91612  201607  796.974802  1024.636600 -227.661798
6   91612  201606  796.520771  1061.976722 -265.455951
7   91612  201605  796.125962  1102.271162 -306.145200
8   91612  201604  796.122825  1146.353163 -350.230338
9   91612  201603  796.119986  1194.108664 -397.988679
```

**Largest Differences**:
```
   permno  yyyymm      python        stata        diff
0   91612  201509  796.102889  1432.882624 -636.779735
1   91612  201508  796.101336  1432.880842 -636.779507
2   91612  201507  796.099783  1432.879061 -636.779278
3   91612  201506  796.098230  1432.877280 -636.779050
4   91612  201510  796.105744  1432.884398 -636.778654
5   91612  201511  796.108599  1432.886171 -636.777573
6   91612  201505  795.901241  1432.522698 -636.621456
7   91612  201504  740.245737  1332.339838 -592.094101
8   91612  201512  796.111454  1364.664026 -568.552573
9   91612  201503  684.589898  1232.156979 -547.567081
```

---

### High52

**Status**: ✅ PASSED

**Test Results**:
- Test 1 - Column names: ✅ PASSED
- Test 2 - Superset check: ✅ PASSED
- Test 3 - Precision1 check: ✅ PASSED
- Test 4 - Precision2 check: ✅ PASSED

**Columns**: ['High52']

**Observations**:
- Stata:  4,995,429
- Python: 4,995,429
- Common: 4,995,429

**Precision1**: 0.000% obs with std_diff >= 1.00e-02 (tolerance: < 10%)

**Precision2**: 99th percentile diff = 9.09e-08 (tolerance: < 1.00e-03)

**Feedback**:
- Num observations with std_diff >= TOL_DIFF_1: 0/4995429 (0.000%)
- Stata standard deviation: 3.34e-01

---

### IO_ShortInterest

**Status**: ✅ PASSED

**Test Results**:
- Test 1 - Column names: ✅ PASSED
- Test 2 - Superset check: ✅ PASSED
- Test 3 - Precision1 check: ✅ PASSED
- Test 4 - Precision2 check: ✅ PASSED

**Columns**: ['IO_ShortInterest']

**Observations**:
- Stata:  8,842
- Python: 3,051,307
- Common: 8,842

**Precision1**: 0.000% obs with std_diff >= 1.00e-02 (tolerance: < 10%)

**Precision2**: 99th percentile diff = 1.00e-05 (tolerance: < 1.00e-03)

**Feedback**:
- Num observations with std_diff >= TOL_DIFF_1: 0/8842 (0.000%)
- Stata standard deviation: 1.01e+02

---

### IdioVol3F

**Status**: ✅ PASSED

**Test Results**:
- Test 1 - Column names: ✅ PASSED
- Test 2 - Superset check: ✅ PASSED
- Test 3 - Precision1 check: ✅ PASSED
- Test 4 - Precision2 check: ✅ PASSED

**Columns**: ['IdioVol3F']

**Observations**:
- Stata:  4,980,936
- Python: 4,987,890
- Common: 4,980,936

**Precision1**: 0.021% obs with std_diff >= 1.00e-02 (tolerance: < 10%)

**Precision2**: 99th percentile diff = 4.57e-05 (tolerance: < 1.00e-03)

**Feedback**:
- Num observations with std_diff >= TOL_DIFF_1: 1055/4980936 (0.021%)
- Stata standard deviation: 2.85e-02

---

### IdioVolAHT

**Status**: ❌ FAILED

**Test Results**:
- Test 1 - Column names: ✅ PASSED
- Test 2 - Superset check: ❌ FAILED (Python missing 185207 Stata observations)
- Test 3 - Precision1 check: ❌ FAILED
- Test 4 - Precision2 check: ❌ FAILED

**Columns**: ['IdioVolAHT']

**Observations**:
- Stata:  4,849,170
- Python: 4,674,856
- Common: 4,663,963

**Precision1**: 17.592% obs with std_diff >= 1.00e-02 (tolerance: < 10%)

**Precision2**: 99th percentile diff = 5.31e-03 (tolerance: < 1.00e-03)

**Missing Observations Sample**:
```
 index  permno  yyyymm  IdioVolAHT
     0   10000  198605    0.044089
     1   10000  198606    0.040834
     2   10000  198607    0.041602
     3   10000  198608    0.053414
     4   10000  198609    0.052791
     5   10001  198606    0.007429
     6   10001  198607    0.008367
     7   10001  198608    0.008199
     8   10001  198609    0.012856
     9   10002  198606    0.017542
```

**Feedback**:
- Num observations with std_diff >= TOL_DIFF_1: 820464/4663963 (17.592%)
- Stata standard deviation: 2.63e-02

**Most Recent Bad Observations**:
```
   permno  yyyymm    python     stata      diff
0   10355  202412  0.020368  0.019840  0.000528
1   11547  202412  0.024971  0.024665  0.000306
2   12049  202412  0.074645  0.074922 -0.000278
3   12209  202412  0.055328  0.055615 -0.000287
4   12295  202412  0.004804  0.004460  0.000344
5   12355  202412  0.012702  0.012363  0.000339
6   12380  202412  0.024728  0.024445  0.000283
7   12397  202412  0.029515  0.029200  0.000315
8   12447  202412  0.035238  0.034865  0.000373
9   12462  202412  0.011098  0.010642  0.000456
```

**Largest Differences**:
```
   permno  yyyymm    python     stata      diff
0   10346  199508  0.200301  0.755186 -0.554885
1   19831  202107  0.138224  0.690156 -0.551932
2   10346  199509  0.199367  0.750348 -0.550982
3   19831  202108  0.128564  0.656875 -0.528310
4   19831  202111  0.113861  0.632297 -0.518436
5   19831  202110  0.117159  0.632683 -0.515523
6   19831  202109  0.123172  0.633176 -0.510004
7   17283  193204  0.036924  0.536495 -0.499571
8   17283  193203  0.040211  0.536824 -0.496613
9   38420  201105  0.033253  0.524829 -0.491576
```

---

### Illiquidity

**Status**: ✅ PASSED

**Test Results**:
- Test 1 - Column names: ✅ PASSED
- Test 2 - Superset check: ✅ PASSED
- Test 3 - Precision1 check: ✅ PASSED
- Test 4 - Precision2 check: ✅ PASSED

**Columns**: ['Illiquidity']

**Observations**:
- Stata:  4,278,152
- Python: 4,739,556
- Common: 4,278,152

**Precision1**: 0.000% obs with std_diff >= 1.00e-02 (tolerance: < 10%)

**Precision2**: 99th percentile diff = 3.04e-12 (tolerance: < 1.00e-03)

**Feedback**:
- Num observations with std_diff >= TOL_DIFF_1: 0/4278152 (0.000%)
- Stata standard deviation: 1.64e-04

---

### IndMom

**Status**: ❌ FAILED

**Test Results**:
- Test 1 - Column names: ✅ PASSED
- Test 2 - Superset check: ✅ PASSED
- Test 3 - Precision1 check: ✅ PASSED
- Test 4 - Precision2 check: ❌ FAILED

**Columns**: ['IndMom']

**Observations**:
- Stata:  4,043,138
- Python: 4,044,574
- Common: 4,043,138

**Precision1**: 3.278% obs with std_diff >= 1.00e-02 (tolerance: < 10%)

**Precision2**: 99th percentile diff = 5.07e-02 (tolerance: < 1.00e-03)

**Feedback**:
- Num observations with std_diff >= TOL_DIFF_1: 132529/4043138 (3.278%)
- Stata standard deviation: 1.74e-01

**Most Recent Bad Observations**:
```
   permno  yyyymm    python     stata      diff
0   10606  202412  0.221829  0.362349 -0.140520
1   11404  202412  0.268826  0.301823 -0.032996
2   11674  202412  0.268826  0.301823 -0.032996
3   11809  202412  0.268826  0.301823 -0.032996
4   11955  202412  0.268826  0.301823 -0.032996
5   12476  202412  0.268826  0.301823 -0.032996
6   12558  202412  0.268826  0.301823 -0.032996
7   12781  202412  0.268826  0.301823 -0.032996
8   12981  202412  0.221829  0.362349 -0.140520
9   13019  202412  0.268826  0.301823 -0.032996
```

**Largest Differences**:
```
   permno  yyyymm    python     stata      diff
0   11362  200003 -0.086561  1.187011 -1.273572
1   11694  200003 -0.086561  1.187011 -1.273572
2   26650  200003 -0.086561  1.187011 -1.273572
3   38746  200003 -0.086561  1.187011 -1.273572
4   48565  200003 -0.086561  1.187011 -1.273572
5   53831  200003 -0.086561  1.187011 -1.273572
6   54148  200003 -0.086561  1.187011 -1.273572
7   54439  200003 -0.086561  1.187011 -1.273572
8   55036  200003 -0.086561  1.187011 -1.273572
9   62383  200003 -0.086561  1.187011 -1.273572
```

---

### IndRetBig

**Status**: ❌ FAILED

**Test Results**:
- Test 1 - Column names: ✅ PASSED
- Test 2 - Superset check: ✅ PASSED
- Test 3 - Precision1 check: ✅ PASSED
- Test 4 - Precision2 check: ❌ FAILED

**Columns**: ['IndRetBig']

**Observations**:
- Stata:  2,607,795
- Python: 2,808,360
- Common: 2,601,282

**Precision1**: 7.120% obs with std_diff >= 1.00e-02 (tolerance: < 10%)

**Precision2**: 99th percentile diff = 8.82e-03 (tolerance: < 1.00e-03)

**Feedback**:
- Num observations with std_diff >= TOL_DIFF_1: 185206/2601282 (7.120%)
- Stata standard deviation: 7.04e-02

**Most Recent Bad Observations**:
```
   permno  yyyymm    python     stata      diff
0   10032  202412 -0.033698 -0.032256 -0.001442
1   10463  202412 -0.033698 -0.032256 -0.001442
2   10779  202412 -0.033698 -0.032256 -0.001442
3   11154  202412 -0.033698 -0.032256 -0.001442
4   12629  202412 -0.033698 -0.032256 -0.001442
5   13577  202412 -0.061087 -0.064159  0.003072
6   13704  202412 -0.033698 -0.032256 -0.001442
7   14185  202412 -0.061087 -0.064159  0.003072
8   16432  202412 -0.061087 -0.064159  0.003072
9   16560  202412 -0.061087 -0.064159  0.003072
```

**Largest Differences**:
```
   permno  yyyymm    python     stata      diff
0   19183  197409 -0.075931  0.210256 -0.286188
1   56371  197409 -0.075931  0.210256 -0.286188
2   69287  197409 -0.075931  0.210256 -0.286188
3   81649  197409 -0.075931  0.210256 -0.286188
4   13784  193207  0.923912  0.676327  0.247585
5   14381  193207  0.923912  0.676327  0.247585
6   14859  193207  0.923912  0.676327  0.247585
7   16352  193207  0.923912  0.676327  0.247585
8   18083  193207  0.923912  0.676327  0.247585
9   19297  193207  0.923912  0.676327  0.247585
```

---

### IntMom

**Status**: ✅ PASSED

**Test Results**:
- Test 1 - Column names: ✅ PASSED
- Test 2 - Superset check: ✅ PASSED
- Test 3 - Precision1 check: ✅ PASSED
- Test 4 - Precision2 check: ✅ PASSED

**Columns**: ['IntMom']

**Observations**:
- Stata:  3,686,625
- Python: 4,047,630
- Common: 3,686,625

**Precision1**: 0.000% obs with std_diff >= 1.00e-02 (tolerance: < 10%)

**Precision2**: 99th percentile diff = 5.01e-08 (tolerance: < 1.00e-03)

**Feedback**:
- Num observations with std_diff >= TOL_DIFF_1: 0/3686625 (0.000%)
- Stata standard deviation: 4.82e-01

---

### IntanBM

**Status**: ✅ PASSED

**Test Results**:
- Test 1 - Column names: ✅ PASSED
- Test 2 - Superset check: ✅ PASSED
- Test 3 - Precision1 check: ✅ PASSED
- Test 4 - Precision2 check: ✅ PASSED

**Columns**: ['IntanBM']

**Observations**:
- Stata:  1,728,575
- Python: 1,728,573
- Common: 1,728,572

**Precision1**: 0.011% obs with std_diff >= 1.00e-02 (tolerance: < 10%)

**Precision2**: 99th percentile diff = 2.81e-07 (tolerance: < 1.00e-03)

**Feedback**:
- Num observations with std_diff >= TOL_DIFF_1: 192/1728572 (0.011%)
- Stata standard deviation: 7.51e-01

---

### IntanCFP

**Status**: ✅ PASSED

**Test Results**:
- Test 1 - Column names: ✅ PASSED
- Test 2 - Superset check: ✅ PASSED
- Test 3 - Precision1 check: ✅ PASSED
- Test 4 - Precision2 check: ✅ PASSED

**Columns**: ['IntanCFP']

**Observations**:
- Stata:  1,881,254
- Python: 1,881,252
- Common: 1,881,251

**Precision1**: 0.149% obs with std_diff >= 1.00e-02 (tolerance: < 10%)

**Precision2**: 99th percentile diff = 2.16e-05 (tolerance: < 1.00e-03)

**Feedback**:
- Num observations with std_diff >= TOL_DIFF_1: 2807/1881251 (0.149%)
- Stata standard deviation: 4.70e-01

---

### IntanEP

**Status**: ✅ PASSED

**Test Results**:
- Test 1 - Column names: ✅ PASSED
- Test 2 - Superset check: ✅ PASSED
- Test 3 - Precision1 check: ✅ PASSED
- Test 4 - Precision2 check: ✅ PASSED

**Columns**: ['IntanEP']

**Observations**:
- Stata:  1,881,254
- Python: 1,881,252
- Common: 1,881,251

**Precision1**: 0.155% obs with std_diff >= 1.00e-02 (tolerance: < 10%)

**Precision2**: 99th percentile diff = 2.84e-07 (tolerance: < 1.00e-03)

**Feedback**:
- Num observations with std_diff >= TOL_DIFF_1: 2907/1881251 (0.155%)
- Stata standard deviation: 5.14e-01

---

### IntanSP

**Status**: ✅ PASSED

**Test Results**:
- Test 1 - Column names: ✅ PASSED
- Test 2 - Superset check: ✅ PASSED
- Test 3 - Precision1 check: ✅ PASSED
- Test 4 - Precision2 check: ✅ PASSED

**Columns**: ['IntanSP']

**Observations**:
- Stata:  1,876,810
- Python: 1,876,808
- Common: 1,876,807

**Precision1**: 0.009% obs with std_diff >= 1.00e-02 (tolerance: < 10%)

**Precision2**: 99th percentile diff = 6.68e-07 (tolerance: < 1.00e-03)

**Feedback**:
- Num observations with std_diff >= TOL_DIFF_1: 164/1876807 (0.009%)
- Stata standard deviation: 1.44e+00

---

### InvGrowth

**Status**: ✅ PASSED

**Test Results**:
- Test 1 - Column names: ✅ PASSED
- Test 2 - Superset check: ✅ PASSED
- Test 3 - Precision1 check: ✅ PASSED
- Test 4 - Precision2 check: ✅ PASSED

**Columns**: ['InvGrowth']

**Observations**:
- Stata:  1,973,756
- Python: 1,996,001
- Common: 1,973,744

**Precision1**: 0.000% obs with std_diff >= 1.00e-02 (tolerance: < 10%)

**Precision2**: 99th percentile diff = 3.50e-07 (tolerance: < 1.00e-03)

**Feedback**:
- Num observations with std_diff >= TOL_DIFF_1: 1/1973744 (0.000%)
- Stata standard deviation: 2.36e+01

---

### Investment

**Status**: ❌ FAILED

**Test Results**:
- Test 1 - Column names: ✅ PASSED
- Test 2 - Superset check: ✅ PASSED
- Test 3 - Precision1 check: ✅ PASSED
- Test 4 - Precision2 check: ❌ FAILED

**Columns**: ['Investment']

**Observations**:
- Stata:  2,411,862
- Python: 2,419,987
- Common: 2,411,862

**Precision1**: 0.999% obs with std_diff >= 1.00e-02 (tolerance: < 10%)

**Precision2**: 99th percentile diff = 1.82e-02 (tolerance: < 1.00e-03)

**Feedback**:
- Num observations with std_diff >= TOL_DIFF_1: 24097/2411862 (0.999%)
- Stata standard deviation: 1.83e+00

**Most Recent Bad Observations**:
```
   permno  yyyymm    python     stata      diff
0   90979  202606  1.120645  1.083741  0.036904
1   12373  202605  0.000000  0.684501 -0.684501
2   12799  202605  2.904973  1.971440  0.933533
3   14607  202605  0.419918  0.396650  0.023267
4   19912  202605  0.737917  0.925279 -0.187362
5   22899  202605  2.858161  2.718322  0.139839
6   88937  202605  0.563974  0.822234 -0.258260
7   90979  202605  1.142852  1.086498  0.056354
8   12373  202604  0.000000  0.681080 -0.681080
9   12799  202604  3.155432  2.144376  1.011055
```

**Largest Differences**:
```
   permno  yyyymm     python      stata       diff
0   82215  202006   0.267506  31.604452 -31.336946
1   82215  202007   0.291701  14.516804 -14.225103
2   50139  198108  36.000000  24.000000  12.000000
3   50817  198004  36.000000  24.000000  12.000000
4   51692  198102  36.000000  24.000000  12.000000
5   55335  198506  36.000000  24.000000  12.000000
6   82215  202008   0.320708   9.673856  -9.353148
7   87759  202306  30.158196  21.692593   8.465603
8   82215  202005  -0.016379   7.615222  -7.631601
9   82215  202009   0.356120   7.385860  -7.029740
```

---

### LRreversal

**Status**: ✅ PASSED

**Test Results**:
- Test 1 - Column names: ✅ PASSED
- Test 2 - Superset check: ✅ PASSED
- Test 3 - Precision1 check: ✅ PASSED
- Test 4 - Precision2 check: ✅ PASSED

**Columns**: ['LRreversal']

**Observations**:
- Stata:  3,059,782
- Python: 4,047,630
- Common: 3,059,782

**Precision1**: 0.123% obs with std_diff >= 1.00e-02 (tolerance: < 10%)

**Precision2**: 99th percentile diff = 1.30e-07 (tolerance: < 1.00e-03)

**Feedback**:
- Num observations with std_diff >= TOL_DIFF_1: 3755/3059782 (0.123%)
- Stata standard deviation: 1.32e+00

---

### Leverage

**Status**: ✅ PASSED

**Test Results**:
- Test 1 - Column names: ✅ PASSED
- Test 2 - Superset check: ✅ PASSED
- Test 3 - Precision1 check: ✅ PASSED
- Test 4 - Precision2 check: ✅ PASSED

**Columns**: ['Leverage']

**Observations**:
- Stata:  3,014,665
- Python: 3,014,667
- Common: 3,014,665

**Precision1**: 0.000% obs with std_diff >= 1.00e-02 (tolerance: < 10%)

**Precision2**: 99th percentile diff = 7.92e-07 (tolerance: < 1.00e-03)

**Feedback**:
- Num observations with std_diff >= TOL_DIFF_1: 0/3014665 (0.000%)
- Stata standard deviation: 1.79e+01

---

### MRreversal

**Status**: ✅ PASSED

**Test Results**:
- Test 1 - Column names: ✅ PASSED
- Test 2 - Superset check: ✅ PASSED
- Test 3 - Precision1 check: ✅ PASSED
- Test 4 - Precision2 check: ✅ PASSED

**Columns**: ['MRreversal']

**Observations**:
- Stata:  3,518,261
- Python: 4,047,630
- Common: 3,518,261

**Precision1**: 0.147% obs with std_diff >= 1.00e-02 (tolerance: < 10%)

**Precision2**: 99th percentile diff = 5.62e-08 (tolerance: < 1.00e-03)

**Feedback**:
- Num observations with std_diff >= TOL_DIFF_1: 5170/3518261 (0.147%)
- Stata standard deviation: 4.75e-01

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

**Precision1**: 63.453% obs with std_diff >= 1.00e-02 (tolerance: < 10%)

**Precision2**: 99th percentile diff = 4.00e+00 (tolerance: < 1.00e-03)

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

### MaxRet

**Status**: ✅ PASSED

**Test Results**:
- Test 1 - Column names: ✅ PASSED
- Test 2 - Superset check: ✅ PASSED
- Test 3 - Precision1 check: ✅ PASSED
- Test 4 - Precision2 check: ✅ PASSED

**Columns**: ['MaxRet']

**Observations**:
- Stata:  5,033,574
- Python: 5,033,574
- Common: 5,033,574

**Precision1**: 0.000% obs with std_diff >= 1.00e-02 (tolerance: < 10%)

**Precision2**: 99th percentile diff = 0.00e+00 (tolerance: < 1.00e-03)

**Feedback**:
- Num observations with std_diff >= TOL_DIFF_1: 0/5033574 (0.000%)
- Stata standard deviation: 1.03e-01

---

### MeanRankRevGrowth

**Status**: ❌ FAILED

**Test Results**:
- Test 1 - Column names: ✅ PASSED
- Test 2 - Superset check: ✅ PASSED
- Test 3 - Precision1 check: ✅ PASSED
- Test 4 - Precision2 check: ❌ FAILED

**Columns**: ['MeanRankRevGrowth']

**Observations**:
- Stata:  2,028,817
- Python: 2,029,426
- Common: 2,028,817

**Precision1**: 0.000% obs with std_diff >= 1.00e-02 (tolerance: < 10%)

**Precision2**: 99th percentile diff = 3.33e-01 (tolerance: < 1.00e-03)

**Feedback**:
- Num observations with std_diff >= TOL_DIFF_1: 2/2028817 (0.000%)
- Stata standard deviation: 1.04e+03

**Most Recent Bad Observations**:
```
   permno  yyyymm  python      stata     diff
0   10501  202609  2787.6  2774.3333  13.2667
1   42585  202609  2910.4  2899.1333  11.2667
```

**Largest Differences**:
```
   permno  yyyymm  python      stata     diff
0   10501  202609  2787.6  2774.3333  13.2667
1   42585  202609  2910.4  2899.1333  11.2667
```

---

### Mom12m

**Status**: ✅ PASSED

**Test Results**:
- Test 1 - Column names: ✅ PASSED
- Test 2 - Superset check: ✅ PASSED
- Test 3 - Precision1 check: ✅ PASSED
- Test 4 - Precision2 check: ✅ PASSED

**Columns**: ['Mom12m']

**Observations**:
- Stata:  3,713,622
- Python: 3,730,107
- Common: 3,713,622

**Precision1**: 0.000% obs with std_diff >= 1.00e-02 (tolerance: < 10%)

**Precision2**: 99th percentile diff = 7.89e-08 (tolerance: < 1.00e-03)

**Feedback**:
- Num observations with std_diff >= TOL_DIFF_1: 0/3713622 (0.000%)
- Stata standard deviation: 7.71e-01

---

### Mom12mOffSeason

**Status**: ✅ PASSED

**Test Results**:
- Test 1 - Column names: ✅ PASSED
- Test 2 - Superset check: ✅ PASSED
- Test 3 - Precision1 check: ✅ PASSED
- Test 4 - Precision2 check: ✅ PASSED

**Columns**: ['Mom12mOffSeason']

**Observations**:
- Stata:  3,865,561
- Python: 3,872,777
- Common: 3,865,561

**Precision1**: 0.174% obs with std_diff >= 1.00e-02 (tolerance: < 10%)

**Precision2**: 99th percentile diff = 5.90e-17 (tolerance: < 1.00e-03)

**Feedback**:
- Num observations with std_diff >= TOL_DIFF_1: 6707/3865561 (0.174%)
- Stata standard deviation: 5.82e-02

---

### Mom6m

**Status**: ✅ PASSED

**Test Results**:
- Test 1 - Column names: ✅ PASSED
- Test 2 - Superset check: ✅ PASSED
- Test 3 - Precision1 check: ✅ PASSED
- Test 4 - Precision2 check: ✅ PASSED

**Columns**: ['Mom6m']

**Observations**:
- Stata:  3,893,591
- Python: 3,901,671
- Common: 3,893,591

**Precision1**: 0.000% obs with std_diff >= 1.00e-02 (tolerance: < 10%)

**Precision2**: 99th percentile diff = 4.10e-08 (tolerance: < 1.00e-03)

**Feedback**:
- Num observations with std_diff >= TOL_DIFF_1: 0/3893591 (0.000%)
- Stata standard deviation: 4.37e-01

---

### Mom6mJunk

**Status**: ❌ FAILED

**Test Results**:
- Test 1 - Column names: ✅ PASSED
- Test 2 - Superset check: ❌ FAILED (Python missing 70860 Stata observations)
- Test 3 - Precision1 check: ✅ PASSED
- Test 4 - Precision2 check: ✅ PASSED

**Columns**: ['Mom6mJunk']

**Observations**:
- Stata:  391,738
- Python: 328,709
- Common: 320,878

**Precision1**: 0.281% obs with std_diff >= 1.00e-02 (tolerance: < 10%)

**Precision2**: 99th percentile diff = 3.93e-08 (tolerance: < 1.00e-03)

**Missing Observations Sample**:
```
 index  permno  yyyymm  Mom6mJunk
     0   10026  201509   0.071515
     1   10026  201510   0.096434
     2   10026  201511   0.146379
     3   10026  201512   0.057645
     4   10026  201601  -0.007851
     5   10026  201602  -0.046296
     6   10026  201603  -0.021993
     7   10026  201604  -0.112035
     8   10026  201605  -0.127242
     9   10026  201606  -0.092484
```

**Feedback**:
- Num observations with std_diff >= TOL_DIFF_1: 903/320878 (0.281%)
- Stata standard deviation: 3.85e-01

---

### MomOffSeason

**Status**: ✅ PASSED

**Test Results**:
- Test 1 - Column names: ✅ PASSED
- Test 2 - Superset check: ✅ PASSED
- Test 3 - Precision1 check: ✅ PASSED
- Test 4 - Precision2 check: ✅ PASSED

**Columns**: ['MomOffSeason']

**Observations**:
- Stata:  3,396,704
- Python: 3,398,036
- Common: 3,396,703

**Precision1**: 1.063% obs with std_diff >= 1.00e-02 (tolerance: < 10%)

**Precision2**: 99th percentile diff = 9.53e-04 (tolerance: < 1.00e-03)

**Feedback**:
- Num observations with std_diff >= TOL_DIFF_1: 36098/3396703 (1.063%)
- Stata standard deviation: 2.70e-02

---

### MomOffSeason06YrPlus

**Status**: ✅ PASSED

**Test Results**:
- Test 1 - Column names: ✅ PASSED
- Test 2 - Superset check: ✅ PASSED
- Test 3 - Precision1 check: ✅ PASSED
- Test 4 - Precision2 check: ✅ PASSED

**Columns**: ['MomOffSeason06YrPlus']

**Observations**:
- Stata:  2,425,319
- Python: 2,429,450
- Common: 2,425,318

**Precision1**: 0.924% obs with std_diff >= 1.00e-02 (tolerance: < 10%)

**Precision2**: 99th percentile diff = 1.00e-08 (tolerance: < 1.00e-03)

**Feedback**:
- Num observations with std_diff >= TOL_DIFF_1: 22415/2425318 (0.924%)
- Stata standard deviation: 3.24e-02

---

### MomOffSeason11YrPlus

**Status**: ✅ PASSED

**Test Results**:
- Test 1 - Column names: ✅ PASSED
- Test 2 - Superset check: ✅ PASSED
- Test 3 - Precision1 check: ✅ PASSED
- Test 4 - Precision2 check: ✅ PASSED

**Columns**: ['MomOffSeason11YrPlus']

**Observations**:
- Stata:  1,677,532
- Python: 1,678,292
- Common: 1,677,526

**Precision1**: 0.880% obs with std_diff >= 1.00e-02 (tolerance: < 10%)

**Precision2**: 99th percentile diff = 8.18e-09 (tolerance: < 1.00e-03)

**Feedback**:
- Num observations with std_diff >= TOL_DIFF_1: 14757/1677526 (0.880%)
- Stata standard deviation: 2.54e-02

---

### MomOffSeason16YrPlus

**Status**: ✅ PASSED

**Test Results**:
- Test 1 - Column names: ✅ PASSED
- Test 2 - Superset check: ✅ PASSED
- Test 3 - Precision1 check: ✅ PASSED
- Test 4 - Precision2 check: ✅ PASSED

**Columns**: ['MomOffSeason16YrPlus']

**Observations**:
- Stata:  1,027,449
- Python: 1,029,940
- Common: 1,027,449

**Precision1**: 0.510% obs with std_diff >= 1.00e-02 (tolerance: < 10%)

**Precision2**: 99th percentile diff = 3.36e-09 (tolerance: < 1.00e-03)

**Feedback**:
- Num observations with std_diff >= TOL_DIFF_1: 5240/1027449 (0.510%)
- Stata standard deviation: 1.75e-02

---

### MomRev

**Status**: ❌ FAILED

**Test Results**:
- Test 1 - Column names: ✅ PASSED
- Test 2 - Superset check: ❌ FAILED (Python missing 3435 Stata observations)
- Test 3 - Precision1 check: ✅ PASSED
- Test 4 - Precision2 check: ✅ PASSED

**Columns**: ['MomRev']

**Observations**:
- Stata:  262,210
- Python: 266,100
- Common: 258,775

**Precision1**: 0.000% obs with std_diff >= 1.00e-02 (tolerance: < 10%)

**Precision2**: 99th percentile diff = 0.00e+00 (tolerance: < 1.00e-03)

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
- Num observations with std_diff >= TOL_DIFF_1: 0/258775 (0.000%)
- Stata standard deviation: 4.97e-01

---

### MomSeason

**Status**: ✅ PASSED

**Test Results**:
- Test 1 - Column names: ✅ PASSED
- Test 2 - Superset check: ✅ PASSED
- Test 3 - Precision1 check: ✅ PASSED
- Test 4 - Precision2 check: ✅ PASSED

**Columns**: ['MomSeason']

**Observations**:
- Stata:  3,398,424
- Python: 3,398,424
- Common: 3,398,424

**Precision1**: 0.000% obs with std_diff >= 1.00e-02 (tolerance: < 10%)

**Precision2**: 99th percentile diff = 1.33e-08 (tolerance: < 1.00e-03)

**Feedback**:
- Num observations with std_diff >= TOL_DIFF_1: 0/3398424 (0.000%)
- Stata standard deviation: 1.01e-01

---

### MomSeason06YrPlus

**Status**: ✅ PASSED

**Test Results**:
- Test 1 - Column names: ✅ PASSED
- Test 2 - Superset check: ✅ PASSED
- Test 3 - Precision1 check: ✅ PASSED
- Test 4 - Precision2 check: ✅ PASSED

**Columns**: ['MomSeason06YrPlus']

**Observations**:
- Stata:  2,432,862
- Python: 2,432,862
- Common: 2,432,862

**Precision1**: 0.000% obs with std_diff >= 1.00e-02 (tolerance: < 10%)

**Precision2**: 99th percentile diff = 1.33e-08 (tolerance: < 1.00e-03)

**Feedback**:
- Num observations with std_diff >= TOL_DIFF_1: 0/2432862 (0.000%)
- Stata standard deviation: 8.82e-02

---

### MomSeason11YrPlus

**Status**: ✅ PASSED

**Test Results**:
- Test 1 - Column names: ✅ PASSED
- Test 2 - Superset check: ✅ PASSED
- Test 3 - Precision1 check: ✅ PASSED
- Test 4 - Precision2 check: ✅ PASSED

**Columns**: ['MomSeason11YrPlus']

**Observations**:
- Stata:  1,680,518
- Python: 1,680,518
- Common: 1,680,518

**Precision1**: 0.000% obs with std_diff >= 1.00e-02 (tolerance: < 10%)

**Precision2**: 99th percentile diff = 1.20e-08 (tolerance: < 1.00e-03)

**Feedback**:
- Num observations with std_diff >= TOL_DIFF_1: 0/1680518 (0.000%)
- Stata standard deviation: 8.39e-02

---

### MomSeason16YrPlus

**Status**: ✅ PASSED

**Test Results**:
- Test 1 - Column names: ✅ PASSED
- Test 2 - Superset check: ✅ PASSED
- Test 3 - Precision1 check: ✅ PASSED
- Test 4 - Precision2 check: ✅ PASSED

**Columns**: ['MomSeason16YrPlus']

**Observations**:
- Stata:  1,194,902
- Python: 1,194,902
- Common: 1,194,902

**Precision1**: 0.000% obs with std_diff >= 1.00e-02 (tolerance: < 10%)

**Precision2**: 99th percentile diff = 1.10e-08 (tolerance: < 1.00e-03)

**Feedback**:
- Num observations with std_diff >= TOL_DIFF_1: 0/1194902 (0.000%)
- Stata standard deviation: 8.08e-02

---

### MomSeasonShort

**Status**: ✅ PASSED

**Test Results**:
- Test 1 - Column names: ✅ PASSED
- Test 2 - Superset check: ✅ PASSED
- Test 3 - Precision1 check: ✅ PASSED
- Test 4 - Precision2 check: ✅ PASSED

**Columns**: ['MomSeasonShort']

**Observations**:
- Stata:  3,718,320
- Python: 3,718,320
- Common: 3,718,320

**Precision1**: 0.000% obs with std_diff >= 1.00e-02 (tolerance: < 10%)

**Precision2**: 99th percentile diff = 1.00e-08 (tolerance: < 1.00e-03)

**Feedback**:
- Num observations with std_diff >= TOL_DIFF_1: 0/3718320 (0.000%)
- Stata standard deviation: 1.73e-01

---

### MomVol

**Status**: ✅ PASSED

**Test Results**:
- Test 1 - Column names: ✅ PASSED
- Test 2 - Superset check: ✅ PASSED
- Test 3 - Precision1 check: ✅ PASSED
- Test 4 - Precision2 check: ✅ PASSED

**Columns**: ['MomVol']

**Observations**:
- Stata:  1,095,615
- Python: 1,098,011
- Common: 1,095,587

**Precision1**: 0.417% obs with std_diff >= 1.00e-02 (tolerance: < 10%)

**Precision2**: 99th percentile diff = 0.00e+00 (tolerance: < 1.00e-03)

**Feedback**:
- Num observations with std_diff >= TOL_DIFF_1: 4567/1095587 (0.417%)
- Stata standard deviation: 2.88e+00

---

### NOA

**Status**: ✅ PASSED

**Test Results**:
- Test 1 - Column names: ✅ PASSED
- Test 2 - Superset check: ✅ PASSED
- Test 3 - Precision1 check: ✅ PASSED
- Test 4 - Precision2 check: ✅ PASSED

**Columns**: ['NOA']

**Observations**:
- Stata:  3,196,825
- Python: 3,213,348
- Common: 3,196,825

**Precision1**: 0.003% obs with std_diff >= 1.00e-02 (tolerance: < 10%)

**Precision2**: 99th percentile diff = 1.10e-07 (tolerance: < 1.00e-03)

**Feedback**:
- Num observations with std_diff >= TOL_DIFF_1: 108/3196825 (0.003%)
- Stata standard deviation: 1.62e+00

---

### NetDebtFinance

**Status**: ✅ PASSED

**Test Results**:
- Test 1 - Column names: ✅ PASSED
- Test 2 - Superset check: ✅ PASSED
- Test 3 - Precision1 check: ✅ PASSED
- Test 4 - Precision2 check: ✅ PASSED

**Columns**: ['NetDebtFinance']

**Observations**:
- Stata:  2,782,808
- Python: 2,797,645
- Common: 2,782,808

**Precision1**: 0.003% obs with std_diff >= 1.00e-02 (tolerance: < 10%)

**Precision2**: 99th percentile diff = 1.42e-08 (tolerance: < 1.00e-03)

**Feedback**:
- Num observations with std_diff >= TOL_DIFF_1: 84/2782808 (0.003%)
- Stata standard deviation: 1.18e-01

---

### NetDebtPrice

**Status**: ✅ PASSED

**Test Results**:
- Test 1 - Column names: ✅ PASSED
- Test 2 - Superset check: ✅ PASSED
- Test 3 - Precision1 check: ✅ PASSED
- Test 4 - Precision2 check: ✅ PASSED

**Columns**: ['NetDebtPrice']

**Observations**:
- Stata:  1,425,163
- Python: 1,425,639
- Common: 1,425,162

**Precision1**: 0.000% obs with std_diff >= 1.00e-02 (tolerance: < 10%)

**Precision2**: 99th percentile diff = 3.60e-07 (tolerance: < 1.00e-03)

**Feedback**:
- Num observations with std_diff >= TOL_DIFF_1: 0/1425162 (0.000%)
- Stata standard deviation: 7.00e+00

---

### NetEquityFinance

**Status**: ✅ PASSED

**Test Results**:
- Test 1 - Column names: ✅ PASSED
- Test 2 - Superset check: ✅ PASSED
- Test 3 - Precision1 check: ✅ PASSED
- Test 4 - Precision2 check: ✅ PASSED

**Columns**: ['NetEquityFinance']

**Observations**:
- Stata:  2,874,470
- Python: 2,889,052
- Common: 2,874,470

**Precision1**: 0.001% obs with std_diff >= 1.00e-02 (tolerance: < 10%)

**Precision2**: 99th percentile diff = 1.78e-08 (tolerance: < 1.00e-03)

**Feedback**:
- Num observations with std_diff >= TOL_DIFF_1: 36/2874470 (0.001%)
- Stata standard deviation: 1.39e-01

---

### NetPayoutYield

**Status**: ✅ PASSED

**Test Results**:
- Test 1 - Column names: ✅ PASSED
- Test 2 - Superset check: ✅ PASSED
- Test 3 - Precision1 check: ✅ PASSED
- Test 4 - Precision2 check: ✅ PASSED

**Columns**: ['NetPayoutYield']

**Observations**:
- Stata:  1,817,567
- Python: 1,818,920
- Common: 1,817,567

**Precision1**: 0.000% obs with std_diff >= 1.00e-02 (tolerance: < 10%)

**Precision2**: 99th percentile diff = 1.72e-08 (tolerance: < 1.00e-03)

**Feedback**:
- Num observations with std_diff >= TOL_DIFF_1: 4/1817567 (0.000%)
- Stata standard deviation: 5.41e-01

---

### NumEarnIncrease

**Status**: ❌ FAILED

**Test Results**:
- Test 1 - Column names: ✅ PASSED
- Test 2 - Superset check: ✅ PASSED
- Test 3 - Precision1 check: ✅ PASSED
- Test 4 - Precision2 check: ❌ FAILED

**Columns**: ['NumEarnIncrease']

**Observations**:
- Stata:  2,823,456
- Python: 2,823,459
- Common: 2,823,456

**Precision1**: 1.010% obs with std_diff >= 1.00e-02 (tolerance: < 10%)

**Precision2**: 99th percentile diff = 1.00e+00 (tolerance: < 1.00e-03)

**Feedback**:
- Num observations with std_diff >= TOL_DIFF_1: 28519/2823456 (1.010%)
- Stata standard deviation: 1.93e+00

**Most Recent Bad Observations**:
```
   permno  yyyymm  python  stata  diff
0   13919  202412       0      3    -3
1   14987  202412       0      1    -1
2   15065  202412       0      5    -5
3   15129  202412       0      1    -1
4   15433  202412       0      4    -4
5   16048  202412       0      1    -1
6   16310  202412       0      1    -1
7   16536  202412       0      7    -7
8   16541  202412       0      4    -4
9   17809  202412       0      3    -3
```

**Largest Differences**:
```
   permno  yyyymm  python  stata  diff
0   10056  200103       0      8    -8
1   10056  200104       0      8    -8
2   10056  200105       0      8    -8
3   10072  199209       0      8    -8
4   10082  199212       0      8    -8
5   10082  199304       0      8    -8
6   10082  199305       0      8    -8
7   10083  199006       0      8    -8
8   10083  199007       0      8    -8
9   10083  199008       0      8    -8
```

---

### OPLeverage

**Status**: ✅ PASSED

**Test Results**:
- Test 1 - Column names: ✅ PASSED
- Test 2 - Superset check: ✅ PASSED
- Test 3 - Precision1 check: ✅ PASSED
- Test 4 - Precision2 check: ✅ PASSED

**Columns**: ['OPLeverage']

**Observations**:
- Stata:  3,607,726
- Python: 3,609,010
- Common: 3,607,726

**Precision1**: 0.003% obs with std_diff >= 1.00e-02 (tolerance: < 10%)

**Precision2**: 99th percentile diff = 1.41e-07 (tolerance: < 1.00e-03)

**Feedback**:
- Num observations with std_diff >= TOL_DIFF_1: 108/3607726 (0.003%)
- Stata standard deviation: 1.20e+00

---

### OScore

**Status**: ✅ PASSED

**Test Results**:
- Test 1 - Column names: ✅ PASSED
- Test 2 - Superset check: ✅ PASSED
- Test 3 - Precision1 check: ✅ PASSED
- Test 4 - Precision2 check: ✅ PASSED

**Columns**: ['OScore']

**Observations**:
- Stata:  1,197,546
- Python: 1,197,639
- Common: 1,197,024

**Precision1**: 0.000% obs with std_diff >= 1.00e-02 (tolerance: < 10%)

**Precision2**: 99th percentile diff = 0.00e+00 (tolerance: < 1.00e-03)

**Feedback**:
- Num observations with std_diff >= TOL_DIFF_1: 0/1197024 (0.000%)
- Stata standard deviation: 3.30e-01

---

### OperProf

**Status**: ✅ PASSED

**Test Results**:
- Test 1 - Column names: ✅ PASSED
- Test 2 - Superset check: ✅ PASSED
- Test 3 - Precision1 check: ✅ PASSED
- Test 4 - Precision2 check: ✅ PASSED

**Columns**: ['OperProf']

**Observations**:
- Stata:  1,407,636
- Python: 1,714,647
- Common: 1,407,636

**Precision1**: 0.000% obs with std_diff >= 1.00e-02 (tolerance: < 10%)

**Precision2**: 99th percentile diff = 9.50e-08 (tolerance: < 1.00e-03)

**Feedback**:
- Num observations with std_diff >= TOL_DIFF_1: 7/1407636 (0.000%)
- Stata standard deviation: 1.62e+01

---

### OperProfRD

**Status**: ✅ PASSED

**Test Results**:
- Test 1 - Column names: ✅ PASSED
- Test 2 - Superset check: ✅ PASSED
- Test 3 - Precision1 check: ✅ PASSED
- Test 4 - Precision2 check: ✅ PASSED

**Columns**: ['OperProfRD']

**Observations**:
- Stata:  2,097,471
- Python: 2,389,629
- Common: 2,097,471

**Precision1**: 0.003% obs with std_diff >= 1.00e-02 (tolerance: < 10%)

**Precision2**: 99th percentile diff = 2.32e-08 (tolerance: < 1.00e-03)

**Feedback**:
- Num observations with std_diff >= TOL_DIFF_1: 63/2097471 (0.003%)
- Stata standard deviation: 2.74e-01

---

### OptionVolume1

**Status**: ✅ PASSED

**Test Results**:
- Test 1 - Column names: ✅ PASSED
- Test 2 - Superset check: ✅ PASSED
- Test 3 - Precision1 check: ✅ PASSED
- Test 4 - Precision2 check: ✅ PASSED

**Columns**: ['OptionVolume1']

**Observations**:
- Stata:  855,113
- Python: 852,949
- Common: 848,962

**Precision1**: 0.042% obs with std_diff >= 1.00e-02 (tolerance: < 10%)

**Precision2**: 99th percentile diff = 1.89e-04 (tolerance: < 1.00e-03)

**Feedback**:
- Num observations with std_diff >= TOL_DIFF_1: 353/848962 (0.042%)
- Stata standard deviation: 1.79e+03

---

### OptionVolume2

**Status**: ✅ PASSED

**Test Results**:
- Test 1 - Column names: ✅ PASSED
- Test 2 - Superset check: ✅ PASSED
- Test 3 - Precision1 check: ✅ PASSED
- Test 4 - Precision2 check: ✅ PASSED

**Columns**: ['OptionVolume2']

**Observations**:
- Stata:  843,512
- Python: 841,828
- Common: 837,442

**Precision1**: 0.047% obs with std_diff >= 1.00e-02 (tolerance: < 10%)

**Precision2**: 99th percentile diff = 3.47e-07 (tolerance: < 1.00e-03)

**Feedback**:
- Num observations with std_diff >= TOL_DIFF_1: 397/837442 (0.047%)
- Stata standard deviation: 2.17e+01

---

### OrderBacklog

**Status**: ✅ PASSED

**Test Results**:
- Test 1 - Column names: ✅ PASSED
- Test 2 - Superset check: ✅ PASSED
- Test 3 - Precision1 check: ✅ PASSED
- Test 4 - Precision2 check: ✅ PASSED

**Columns**: ['OrderBacklog']

**Observations**:
- Stata:  634,164
- Python: 637,317
- Common: 634,164

**Precision1**: 0.000% obs with std_diff >= 1.00e-02 (tolerance: < 10%)

**Precision2**: 99th percentile diff = 1.21e-07 (tolerance: < 1.00e-03)

**Feedback**:
- Num observations with std_diff >= TOL_DIFF_1: 0/634164 (0.000%)
- Stata standard deviation: 1.16e+00

---

### OrderBacklogChg

**Status**: ✅ PASSED

**Test Results**:
- Test 1 - Column names: ✅ PASSED
- Test 2 - Superset check: ✅ PASSED
- Test 3 - Precision1 check: ✅ PASSED
- Test 4 - Precision2 check: ✅ PASSED

**Columns**: ['OrderBacklogChg']

**Observations**:
- Stata:  564,785
- Python: 569,589
- Common: 564,785

**Precision1**: 0.001% obs with std_diff >= 1.00e-02 (tolerance: < 10%)

**Precision2**: 99th percentile diff = 1.63e-07 (tolerance: < 1.00e-03)

**Feedback**:
- Num observations with std_diff >= TOL_DIFF_1: 4/564785 (0.001%)
- Stata standard deviation: 7.39e-01

---

### OrgCap

**Status**: ❌ FAILED

**Test Results**:
- Test 1 - Column names: ✅ PASSED
- Test 2 - Superset check: ✅ PASSED
- Test 3 - Precision1 check: ❌ FAILED
- Test 4 - Precision2 check: ❌ FAILED

**Columns**: ['OrgCap']

**Observations**:
- Stata:  1,243,383
- Python: 1,327,508
- Common: 1,243,383

**Precision1**: 14.227% obs with std_diff >= 1.00e-02 (tolerance: < 10%)

**Precision2**: 99th percentile diff = 1.33e-01 (tolerance: < 1.00e-03)

**Feedback**:
- Num observations with std_diff >= TOL_DIFF_1: 176895/1243383 (14.227%)
- Stata standard deviation: 9.94e-01

**Most Recent Bad Observations**:
```
   permno  yyyymm    python     stata      diff
0   10253  202412 -0.498174 -0.410555 -0.087619
1   10696  202412 -0.684260 -0.668215 -0.016045
2   10860  202412 -0.305616 -0.143933 -0.161683
3   10890  202412 -0.024218  0.245699 -0.269917
4   10966  202412  0.283315  0.671518 -0.388203
5   11275  202412  0.394461  0.825414 -0.430953
6   11403  202412 -0.114539  0.120637 -0.235176
7   11547  202412 -0.367466 -0.229573 -0.137893
8   11600  202412 -0.319548 -0.163224 -0.156324
9   11809  202412 -0.597949 -0.548706 -0.049243
```

**Largest Differences**:
```
   permno  yyyymm    python     stata      diff
0   13812  202406  4.742307  7.155751 -2.413444
1   14925  202406  4.809098  7.155751 -2.346653
2   24087  202406  4.809098  7.155751 -2.346653
3   89698  202406  4.809098  7.155751 -2.346653
4   13812  202410  4.813894  7.114257 -2.300363
5   14925  202410  4.813894  7.114257 -2.300363
6   24087  202410  4.813894  7.114257 -2.300363
7   89698  202410  4.813894  7.114257 -2.300363
8   13812  202411  4.826943  7.105795 -2.278852
9   14925  202411  4.826943  7.105795 -2.278852
```

---

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

### PatentsRD

**Status**: ❌ FAILED

**Test Results**:
- Test 1 - Column names: ✅ PASSED
- Test 2 - Superset check: ❌ FAILED (Python missing 195744 Stata observations)
- Test 3 - Precision1 check: ❌ FAILED
- Test 4 - Precision2 check: ❌ FAILED

**Columns**: ['PatentsRD']

**Observations**:
- Stata:  671,832
- Python: 479,052
- Common: 476,088

**Precision1**: 15.700% obs with std_diff >= 1.00e-02 (tolerance: < 10%)

**Precision2**: 99th percentile diff = 1.00e+00 (tolerance: < 1.00e-03)

**Missing Observations Sample**:
```
 index  permno  yyyymm  PatentsRD
     0   10010  198906          0
     1   10010  198907          0
     2   10010  198908          0
     3   10010  198909          0
     4   10010  198910          0
     5   10010  198911          0
     6   10010  198912          0
     7   10010  199001          0
     8   10010  199002          0
     9   10010  199003          0
```

**Feedback**:
- Num observations with std_diff >= TOL_DIFF_1: 74748/476088 (15.700%)
- Stata standard deviation: 4.56e-01

**Most Recent Bad Observations**:
```
   permno  yyyymm  python  stata  diff
0   10026  202505     1.0      0   1.0
1   10258  202505     1.0      0   1.0
2   10333  202505     1.0      0   1.0
3   10382  202505     1.0      0   1.0
4   10645  202505     1.0      0   1.0
5   10860  202505     1.0      0   1.0
6   11154  202505     1.0      0   1.0
7   11275  202505     1.0      0   1.0
8   11292  202505     1.0      0   1.0
9   11581  202505     1.0      0   1.0
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
7   10025  200901     1.0      0   1.0
8   10025  200902     1.0      0   1.0
9   10025  200903     1.0      0   1.0
```

---

### PayoutYield

**Status**: ✅ PASSED

**Test Results**:
- Test 1 - Column names: ✅ PASSED
- Test 2 - Superset check: ✅ PASSED
- Test 3 - Precision1 check: ✅ PASSED
- Test 4 - Precision2 check: ✅ PASSED

**Columns**: ['PayoutYield']

**Observations**:
- Stata:  1,419,344
- Python: 1,419,513
- Common: 1,419,344

**Precision1**: 0.000% obs with std_diff >= 1.00e-02 (tolerance: < 10%)

**Precision2**: 99th percentile diff = 2.82e-08 (tolerance: < 1.00e-03)

**Feedback**:
- Num observations with std_diff >= TOL_DIFF_1: 4/1419344 (0.000%)
- Stata standard deviation: 4.77e-01

---

### PctAcc

**Status**: ✅ PASSED

**Test Results**:
- Test 1 - Column names: ✅ PASSED
- Test 2 - Superset check: ✅ PASSED
- Test 3 - Precision1 check: ✅ PASSED
- Test 4 - Precision2 check: ✅ PASSED

**Columns**: ['PctAcc']

**Observations**:
- Stata:  3,174,456
- Python: 3,179,478
- Common: 3,174,456

**Precision1**: 0.000% obs with std_diff >= 1.00e-02 (tolerance: < 10%)

**Precision2**: 99th percentile diff = 1.05e-06 (tolerance: < 1.00e-03)

**Feedback**:
- Num observations with std_diff >= TOL_DIFF_1: 12/3174456 (0.000%)
- Stata standard deviation: 9.60e+01

---

### PctTotAcc

**Status**: ✅ PASSED

**Test Results**:
- Test 1 - Column names: ✅ PASSED
- Test 2 - Superset check: ✅ PASSED
- Test 3 - Precision1 check: ✅ PASSED
- Test 4 - Precision2 check: ✅ PASSED

**Columns**: ['PctTotAcc']

**Observations**:
- Stata:  2,412,359
- Python: 2,413,703
- Common: 2,412,359

**Precision1**: 0.000% obs with std_diff >= 1.00e-02 (tolerance: < 10%)

**Precision2**: 99th percentile diff = 1.13e-06 (tolerance: < 1.00e-03)

**Feedback**:
- Num observations with std_diff >= TOL_DIFF_1: 12/2412359 (0.000%)
- Stata standard deviation: 1.43e+02

---

### PredictedFE

**Status**: ❌ FAILED

**Test Results**:
- Test 1 - Column names: ✅ PASSED
- Test 2 - Superset check: ✅ PASSED
- Test 3 - Precision1 check: ❌ FAILED
- Test 4 - Precision2 check: ❌ FAILED

**Columns**: ['PredictedFE']

**Observations**:
- Stata:  491,508
- Python: 635,124
- Common: 490,188

**Precision1**: 93.912% obs with std_diff >= 1.00e-02 (tolerance: < 10%)

**Precision2**: 99th percentile diff = 1.44e-02 (tolerance: < 1.00e-03)

**Feedback**:
- Num observations with std_diff >= TOL_DIFF_1: 460344/490188 (93.912%)
- Stata standard deviation: 3.16e-02

**Most Recent Bad Observations**:
```
   permno  yyyymm    python     stata      diff
0   10107  202505  0.079630  0.078498  0.001132
1   10145  202505  0.045430  0.040432  0.004997
2   10200  202505  0.108685  0.113642 -0.004957
3   10397  202505  0.055039  0.049793  0.005246
4   10606  202505  0.049590  0.044046  0.005543
5   10693  202505  0.045114  0.036774  0.008340
6   10696  202505  0.102107  0.105464 -0.003357
7   11308  202505  0.070800  0.072780 -0.001979
8   11403  202505  0.089096  0.090274 -0.001179
9   11547  202505  0.079154  0.076702  0.002452
```

**Largest Differences**:
```
   permno  yyyymm    python     stata      diff
0   66093  202306  0.025659  0.066932 -0.041273
1   66093  202307  0.025659  0.066932 -0.041273
2   66093  202308  0.025659  0.066932 -0.041273
3   66093  202309  0.025659  0.066932 -0.041273
4   66093  202310  0.025659  0.066932 -0.041273
5   66093  202311  0.025659  0.066932 -0.041273
6   66093  202312  0.025659  0.066932 -0.041273
7   66093  202401  0.025659  0.066932 -0.041273
8   66093  202402  0.025659  0.066932 -0.041273
9   66093  202403  0.025659  0.066932 -0.041273
```

---

### Price

**Status**: ✅ PASSED

**Test Results**:
- Test 1 - Column names: ✅ PASSED
- Test 2 - Superset check: ✅ PASSED
- Test 3 - Precision1 check: ✅ PASSED
- Test 4 - Precision2 check: ✅ PASSED

**Columns**: ['Price']

**Observations**:
- Stata:  4,029,252
- Python: 4,029,252
- Common: 4,029,252

**Precision1**: 0.000% obs with std_diff >= 1.00e-02 (tolerance: < 10%)

**Precision2**: 99th percentile diff = 2.01e-07 (tolerance: < 1.00e-03)

**Feedback**:
- Num observations with std_diff >= TOL_DIFF_1: 0/4029252 (0.000%)
- Stata standard deviation: 1.33e+00

---

### PriceDelayRsq

**Status**: ❌ FAILED

**Test Results**:
- Test 1 - Column names: ✅ PASSED
- Test 2 - Superset check: ✅ PASSED
- Test 3 - Precision1 check: ✅ PASSED
- Test 4 - Precision2 check: ❌ FAILED

**Columns**: ['PriceDelayRsq']

**Observations**:
- Stata:  4,630,424
- Python: 4,636,840
- Common: 4,630,424

**Precision1**: 1.210% obs with std_diff >= 1.00e-02 (tolerance: < 10%)

**Precision2**: 99th percentile diff = 6.07e-02 (tolerance: < 1.00e-03)

**Feedback**:
- Num observations with std_diff >= TOL_DIFF_1: 56040/4630424 (1.210%)
- Stata standard deviation: 3.27e-01

**Most Recent Bad Observations**:
```
   permno  yyyymm    python     stata      diff
0   20665  202406  0.885442  0.656071  0.229371
1   20665  202405  0.885442  0.656071  0.229371
2   20665  202404  0.885442  0.656071  0.229371
3   20665  202403  0.885442  0.656071  0.229371
4   20665  202402  0.885442  0.656071  0.229371
5   20665  202401  0.885442  0.656071  0.229371
6   20665  202312  0.885442  0.656071  0.229371
7   20665  202311  0.885442  0.656071  0.229371
8   20665  202310  0.885442  0.656071  0.229371
9   20665  202309  0.885442  0.656071  0.229371
```

**Largest Differences**:
```
   permno  yyyymm    python     stata      diff
0   10066  199007  0.990682  0.033295  0.957386
1   10066  199008  0.990682  0.033295  0.957386
2   10066  199009  0.990682  0.033295  0.957386
3   10066  199010  0.990682  0.033295  0.957386
4   10066  199011  0.990682  0.033295  0.957386
5   10066  199012  0.990682  0.033295  0.957386
6   10066  199101  0.990682  0.033295  0.957386
7   10066  199102  0.990682  0.033295  0.957386
8   10066  199103  0.990682  0.033295  0.957386
9   10066  199104  0.990682  0.033295  0.957386
```

---

### PriceDelaySlope

**Status**: ❌ FAILED

**Test Results**:
- Test 1 - Column names: ✅ PASSED
- Test 2 - Superset check: ✅ PASSED
- Test 3 - Precision1 check: ✅ PASSED
- Test 4 - Precision2 check: ❌ FAILED

**Columns**: ['PriceDelaySlope']

**Observations**:
- Stata:  4,630,424
- Python: 4,636,840
- Common: 4,630,424

**Precision1**: 0.582% obs with std_diff >= 1.00e-02 (tolerance: < 10%)

**Precision2**: 99th percentile diff = 7.27e-01 (tolerance: < 1.00e-03)

**Feedback**:
- Num observations with std_diff >= TOL_DIFF_1: 26952/4630424 (0.582%)
- Stata standard deviation: 2.52e+02

**Most Recent Bad Observations**:
```
   permno  yyyymm       python       stata        diff
0   12339  202406  1048.987343  1173.92500 -124.937657
1   12920  202406   138.447590   141.02330   -2.575710
2   14296  202406 -1739.165320 -1360.86080 -378.304520
3   16765  202406  -285.457178  -312.93927   27.482092
4   21288  202406   195.744273   189.23006    6.514213
5   22758  202406   277.802905   283.31763   -5.514725
6   24441  202406   396.015800   381.69559   14.320210
7   82171  202406  -115.272269  -123.27301    8.000741
8   90562  202406  -368.401832  -371.83365    3.431818
9   12339  202405  1048.987343  1173.92500 -124.937657
```

**Largest Differences**:
```
   permno  yyyymm       python     stata          diff
0   22356  202207  1525.894901  17467.24 -15941.345099
1   22356  202208  1525.894901  17467.24 -15941.345099
2   22356  202209  1525.894901  17467.24 -15941.345099
3   22356  202210  1525.894901  17467.24 -15941.345099
4   22356  202211  1525.894901  17467.24 -15941.345099
5   22356  202212  1525.894901  17467.24 -15941.345099
6   22356  202301  1525.894901  17467.24 -15941.345099
7   22356  202302  1525.894901  17467.24 -15941.345099
8   22356  202303  1525.894901  17467.24 -15941.345099
9   22356  202304  1525.894901  17467.24 -15941.345099
```

---

### PriceDelayTstat

**Status**: ❌ FAILED

**Test Results**:
- Test 1 - Column names: ✅ PASSED
- Test 2 - Superset check: ✅ PASSED
- Test 3 - Precision1 check: ❌ FAILED
- Test 4 - Precision2 check: ❌ FAILED

**Columns**: ['PriceDelayTstat']

**Observations**:
- Stata:  4,523,656
- Python: 4,636,840
- Common: 4,523,656

**Precision1**: 19.380% obs with std_diff >= 1.00e-02 (tolerance: < 10%)

**Precision2**: 99th percentile diff = 6.09e+00 (tolerance: < 1.00e-03)

**Feedback**:
- Num observations with std_diff >= TOL_DIFF_1: 876673/4523656 (19.380%)
- Stata standard deviation: 1.38e+00

**Most Recent Bad Observations**:
```
   permno  yyyymm    python     stata      diff
0   10145  202407  6.102411  3.590652  2.511759
1   10252  202407 -3.251358  1.948711 -5.200069
2   10257  202407  6.102411  2.211252  3.891159
3   10308  202407 -3.251358  2.127883 -5.379241
4   10318  202407 -3.251358  1.480704 -4.732062
5   10355  202407  6.102411  2.726171  3.376240
6   10501  202407 -3.251358  0.107046 -3.358404
7   10516  202407  6.102411  3.875413  2.226998
8   10517  202407 -3.251358  1.185008 -4.436366
9   10547  202407 -3.251358  1.549714 -4.801072
```

**Largest Differences**:
```
   permno  yyyymm    python     stata       diff
0   20677  195407  6.913496 -3.855832  10.769328
1   20677  195408  6.913496 -3.855832  10.769328
2   20677  195409  6.913496 -3.855832  10.769328
3   20677  195410  6.913496 -3.855832  10.769328
4   20677  195411  6.913496 -3.855832  10.769328
5   20677  195412  6.913496 -3.855832  10.769328
6   20677  195501  6.913496 -3.855832  10.769328
7   20677  195502  6.913496 -3.855832  10.769328
8   20677  195503  6.913496 -3.855832  10.769328
9   20677  195504  6.913496 -3.855832  10.769328
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

**Precision1**: 0.000% obs with std_diff >= 1.00e-02 (tolerance: < 10%)

**Precision2**: 99th percentile diff = 3.00e-08 (tolerance: < 1.00e-03)

**Feedback**:
- Num observations with std_diff >= TOL_DIFF_1: 0/24028 (0.000%)
- Stata standard deviation: 6.67e-02

---

### RD

**Status**: ✅ PASSED

**Test Results**:
- Test 1 - Column names: ✅ PASSED
- Test 2 - Superset check: ✅ PASSED
- Test 3 - Precision1 check: ✅ PASSED
- Test 4 - Precision2 check: ✅ PASSED

**Columns**: ['RD']

**Observations**:
- Stata:  1,419,136
- Python: 1,419,157
- Common: 1,419,136

**Precision1**: 0.000% obs with std_diff >= 1.00e-02 (tolerance: < 10%)

**Precision2**: 99th percentile diff = 2.52e-08 (tolerance: < 1.00e-03)

**Feedback**:
- Num observations with std_diff >= TOL_DIFF_1: 2/1419136 (0.000%)
- Stata standard deviation: 1.20e+00

---

### RDAbility

**Status**: ❌ FAILED

**Test Results**:
- Test 1 - Column names: ✅ PASSED
- Test 2 - Superset check: ❌ FAILED (Python missing 8575 Stata observations)
- Test 3 - Precision1 check: ✅ PASSED
- Test 4 - Precision2 check: ❌ FAILED

**Columns**: ['RDAbility']

**Observations**:
- Stata:  173,266
- Python: 231,277
- Common: 164,691

**Precision1**: 9.523% obs with std_diff >= 1.00e-02 (tolerance: < 10%)

**Precision2**: 99th percentile diff = 5.18e+00 (tolerance: < 1.00e-03)

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

### RDS

**Status**: ✅ PASSED

**Test Results**:
- Test 1 - Column names: ✅ PASSED
- Test 2 - Superset check: ✅ PASSED
- Test 3 - Precision1 check: ✅ PASSED
- Test 4 - Precision2 check: ✅ PASSED

**Columns**: ['RDS']

**Observations**:
- Stata:  2,725,375
- Python: 3,169,667
- Common: 2,725,375

**Precision1**: 0.000% obs with std_diff >= 1.00e-02 (tolerance: < 10%)

**Precision2**: 99th percentile diff = 8.00e-05 (tolerance: < 1.00e-03)

**Feedback**:
- Num observations with std_diff >= TOL_DIFF_1: 0/2725375 (0.000%)
- Stata standard deviation: 7.94e+03

---

### RDcap

**Status**: ✅ PASSED

**Test Results**:
- Test 1 - Column names: ✅ PASSED
- Test 2 - Superset check: ✅ PASSED
- Test 3 - Precision1 check: ✅ PASSED
- Test 4 - Precision2 check: ✅ PASSED

**Columns**: ['RDcap']

**Observations**:
- Stata:  517,737
- Python: 1,404,631
- Common: 517,737

**Precision1**: 0.000% obs with std_diff >= 1.00e-02 (tolerance: < 10%)

**Precision2**: 99th percentile diff = 8.38e-08 (tolerance: < 1.00e-03)

**Feedback**:
- Num observations with std_diff >= TOL_DIFF_1: 0/517737 (0.000%)
- Stata standard deviation: 6.98e-01

---

### REV6

**Status**: ❌ FAILED

**Test Results**:
- Test 1 - Column names: ✅ PASSED
- Test 2 - Superset check: ✅ PASSED
- Test 3 - Precision1 check: ✅ PASSED
- Test 4 - Precision2 check: ❌ FAILED

**Columns**: ['REV6']

**Observations**:
- Stata:  1,762,090
- Python: 4,003,555
- Common: 1,762,090

**Precision1**: 0.166% obs with std_diff >= 1.00e-02 (tolerance: < 10%)

**Precision2**: 99th percentile diff = 8.04e-02 (tolerance: < 1.00e-03)

**Feedback**:
- Num observations with std_diff >= TOL_DIFF_1: 2923/1762090 (0.166%)
- Stata standard deviation: 6.48e+01

**Most Recent Bad Observations**:
```
   permno  yyyymm     python      stata       diff
0   15057  202412  42.345788  46.219757  -3.873969
1   16104  202412  -0.021401  -0.731138   0.709738
2   19314  202412   4.558442   1.077922   3.480519
3   23185  202412  -1.112128  -2.441614   1.329486
4   23235  202412 -79.185532 -83.947433   4.761901
5   23814  202412 -21.099760 -20.018442  -1.081318
6   92230  202412  -0.344130  10.191999 -10.536129
7   92986  202412  11.819759   9.268723   2.551036
8   13455  202411  -2.946154  -0.547843  -2.398311
9   15057  202411   1.824911   0.639749   1.185162
```

**Largest Differences**:
```
   permno  yyyymm       python        stata         diff
0   18301  201908  8805.823583   381.685240  8424.138343
1   18301  201909  4581.855241   381.637540  4200.217701
2   21794  202401 -2397.665488   886.541870 -3284.207358
3   21794  202404 -1671.221128   925.533940 -2596.755068
4   15010  201603   884.435320 -1009.113200  1893.548520
5   21794  202403  -860.749078   945.197630 -1805.946708
6   21794  202402  -919.128318   886.541870 -1805.670188
7   18301  201907  -912.078018   381.693760 -1293.771778
8   15010  201602  1060.302442    61.477833   998.824609
9   13013  201808  -809.949554    -0.136150  -809.813404
```

---

### RIO_Disp

**Status**: ❌ FAILED

**Test Results**:
- Test 1 - Column names: ✅ PASSED
- Test 2 - Superset check: ✅ PASSED
- Test 3 - Precision1 check: ✅ PASSED
- Test 4 - Precision2 check: ❌ FAILED

**Columns**: ['RIO_Disp']

**Observations**:
- Stata:  497,437
- Python: 513,429
- Common: 496,165

**Precision1**: 3.791% obs with std_diff >= 1.00e-02 (tolerance: < 10%)

**Precision2**: 99th percentile diff = 1.00e+00 (tolerance: < 1.00e-03)

**Feedback**:
- Num observations with std_diff >= TOL_DIFF_1: 18809/496165 (3.791%)
- Stata standard deviation: 1.27e+00

**Most Recent Bad Observations**:
```
   permno  yyyymm  python  stata  diff
0   12008  202412     3.0      4  -1.0
1   13954  202412     4.0      5  -1.0
2   14317  202412     3.0      4  -1.0
3   17812  202412     2.0      3  -1.0
4   18452  202412     2.0      3  -1.0
5   18784  202412     4.0      5  -1.0
6   18808  202412     4.0      5  -1.0
7   19076  202412     2.0      3  -1.0
8   20295  202412     2.0      3  -1.0
9   20751  202412     3.0      4  -1.0
```

**Largest Differences**:
```
   permno  yyyymm  python  stata  diff
0   11379  198901     1.0      5  -4.0
1   11453  198808     1.0      5  -4.0
2   11554  199101     1.0      5  -4.0
3   12088  201304     1.0      5  -4.0
4   12402  201107     1.0      5  -4.0
5   12916  201507     1.0      5  -4.0
6   12916  201509     1.0      5  -4.0
7   13041  201207     1.0      5  -4.0
8   14423  202005     1.0      5  -4.0
9   14423  202006     1.0      5  -4.0
```

---

### RIO_MB

**Status**: ❌ FAILED

**Test Results**:
- Test 1 - Column names: ✅ PASSED
- Test 2 - Superset check: ✅ PASSED
- Test 3 - Precision1 check: ✅ PASSED
- Test 4 - Precision2 check: ❌ FAILED

**Columns**: ['RIO_MB']

**Observations**:
- Stata:  354,170
- Python: 366,984
- Common: 353,544

**Precision1**: 3.451% obs with std_diff >= 1.00e-02 (tolerance: < 10%)

**Precision2**: 99th percentile diff = 1.00e+00 (tolerance: < 1.00e-03)

**Feedback**:
- Num observations with std_diff >= TOL_DIFF_1: 12200/353544 (3.451%)
- Stata standard deviation: 1.36e+00

**Most Recent Bad Observations**:
```
   permno  yyyymm  python  stata  diff
0   11955  202412     1.0      2  -1.0
1   15400  202412     3.0      4  -1.0
2   16066  202412     2.0      3  -1.0
3   17812  202412     2.0      3  -1.0
4   18452  202412     2.0      3  -1.0
5   18649  202412     3.0      4  -1.0
6   19076  202412     2.0      3  -1.0
7   51925  202412     3.0      4  -1.0
8   70578  202412     1.0      2  -1.0
9   81540  202412     2.0      3  -1.0
```

**Largest Differences**:
```
   permno  yyyymm  python  stata  diff
0   16827  201809     1.0      5  -4.0
1   19002  202007     1.0      5  -4.0
2   22321  202206     1.0      5  -4.0
3   22802  202209     1.0      5  -4.0
4   25698  198302     1.0      5  -4.0
5   28258  198010     1.0      5  -4.0
6   39757  198012     1.0      5  -4.0
7   50172  198010     1.0      5  -4.0
8   50172  198012     1.0      5  -4.0
9   51079  198112     1.0      5  -4.0
```

---

### RIO_Turnover

**Status**: ❌ FAILED

**Test Results**:
- Test 1 - Column names: ✅ PASSED
- Test 2 - Superset check: ✅ PASSED
- Test 3 - Precision1 check: ✅ PASSED
- Test 4 - Precision2 check: ❌ FAILED

**Columns**: ['RIO_Turnover']

**Observations**:
- Stata:  445,546
- Python: 462,513
- Common: 444,882

**Precision1**: 3.653% obs with std_diff >= 1.00e-02 (tolerance: < 10%)

**Precision2**: 99th percentile diff = 1.00e+00 (tolerance: < 1.00e-03)

**Feedback**:
- Num observations with std_diff >= TOL_DIFF_1: 16253/444882 (3.653%)
- Stata standard deviation: 1.35e+00

**Most Recent Bad Observations**:
```
   permno  yyyymm  python  stata  diff
0   12008  202412     3.0      4  -1.0
1   13730  202412     2.0      3  -1.0
2   13954  202412     4.0      5  -1.0
3   15585  202412     3.0      4  -1.0
4   18452  202412     2.0      3  -1.0
5   18784  202412     4.0      5  -1.0
6   19076  202412     2.0      3  -1.0
7   20295  202412     2.0      3  -1.0
8   20751  202412     3.0      4  -1.0
9   21124  202412     2.0      3  -1.0
```

**Largest Differences**:
```
   permno  yyyymm  python  stata  diff
0   10342  199107     1.0      5  -4.0
1   11202  198712     1.0      5  -4.0
2   11269  198712     1.0      5  -4.0
3   11701  198807     1.0      5  -4.0
4   14423  202005     1.0      5  -4.0
5   16827  201809     1.0      5  -4.0
6   17695  202012     1.0      5  -4.0
7   17949  201904     1.0      5  -4.0
8   17949  201905     1.0      5  -4.0
9   19828  198010     1.0      5  -4.0
```

---

### RIO_Volatility

**Status**: ❌ FAILED

**Test Results**:
- Test 1 - Column names: ✅ PASSED
- Test 2 - Superset check: ❌ FAILED (Python missing 20887 Stata observations)
- Test 3 - Precision1 check: ✅ PASSED
- Test 4 - Precision2 check: ❌ FAILED

**Columns**: ['RIO_Volatility']

**Observations**:
- Stata:  470,062
- Python: 493,527
- Common: 449,175

**Precision1**: 4.316% obs with std_diff >= 1.00e-02 (tolerance: < 10%)

**Precision2**: 99th percentile diff = 1.00e+00 (tolerance: < 1.00e-03)

**Missing Observations Sample**:
```
 index  permno  yyyymm  RIO_Volatility
     0   10006  195405               4
     1   10006  197407               1
     2   10011  199103               3
     3   10011  199104               3
     4   10012  199602               3
     5   10012  199603               3
     6   10014  196704               5
     7   10014  197601               5
     8   10016  198610               3
     9   10019  199210               5
```

**Feedback**:
- Num observations with std_diff >= TOL_DIFF_1: 19387/449175 (4.316%)
- Stata standard deviation: 1.34e+00

**Most Recent Bad Observations**:
```
   permno  yyyymm  python  stata  diff
0   13954  202412     4.0      5  -1.0
1   15585  202412     3.0      4  -1.0
2   16066  202412     2.0      3  -1.0
3   17812  202412     2.0      3  -1.0
4   18062  202412     3.0      4  -1.0
5   18452  202412     2.0      3  -1.0
6   18784  202412     4.0      5  -1.0
7   19076  202412     2.0      3  -1.0
8   20295  202412     2.0      3  -1.0
9   20751  202412     3.0      4  -1.0
```

**Largest Differences**:
```
   permno  yyyymm  python  stata  diff
0   10026  198701     1.0      5  -4.0
1   10537  198703     1.0      5  -4.0
2   10948  198709     1.0      5  -4.0
3   11212  198801     1.0      5  -4.0
4   11212  198802     1.0      5  -4.0
5   11277  198803     1.0      5  -4.0
6   11379  198901     1.0      5  -4.0
7   11453  198808     1.0      5  -4.0
8   11701  198807     1.0      5  -4.0
9   12402  201107     1.0      5  -4.0
```

---

### RIVolSpread

**Status**: ✅ PASSED

**Test Results**:
- Test 1 - Column names: ✅ PASSED
- Test 2 - Superset check: ✅ PASSED
- Test 3 - Precision1 check: ✅ PASSED
- Test 4 - Precision2 check: ✅ PASSED

**Columns**: ['RIVolSpread']

**Observations**:
- Stata:  750,937
- Python: 748,979
- Common: 745,591

**Precision1**: 0.051% obs with std_diff >= 1.00e-02 (tolerance: < 10%)

**Precision2**: 99th percentile diff = 7.54e-08 (tolerance: < 1.00e-03)

**Feedback**:
- Num observations with std_diff >= TOL_DIFF_1: 381/745591 (0.051%)
- Stata standard deviation: 2.30e-01

---

### RealizedVol

**Status**: ✅ PASSED

**Test Results**:
- Test 1 - Column names: ✅ PASSED
- Test 2 - Superset check: ✅ PASSED
- Test 3 - Precision1 check: ✅ PASSED
- Test 4 - Precision2 check: ✅ PASSED

**Columns**: ['RealizedVol']

**Observations**:
- Stata:  4,987,397
- Python: 4,987,890
- Common: 4,981,661

**Precision1**: 0.000% obs with std_diff >= 1.00e-02 (tolerance: < 10%)

**Precision2**: 99th percentile diff = 5.55e-17 (tolerance: < 1.00e-03)

**Feedback**:
- Num observations with std_diff >= TOL_DIFF_1: 0/4981661 (0.000%)
- Stata standard deviation: 3.12e-02

---

### Recomm_ShortInterest

**Status**: ❌ FAILED

**Test Results**:
- Test 1 - Column names: ✅ PASSED
- Test 2 - Superset check: ❌ FAILED (Python missing 19305 Stata observations)
- Test 3 - Precision1 check: ✅ PASSED
- Test 4 - Precision2 check: ✅ PASSED

**Columns**: ['Recomm_ShortInterest']

**Observations**:
- Stata:  34,619
- Python: 35,419
- Common: 15,314

**Precision1**: 0.000% obs with std_diff >= 1.00e-02 (tolerance: < 10%)

**Precision2**: 99th percentile diff = 0.00e+00 (tolerance: < 1.00e-03)

**Missing Observations Sample**:
```
 index  permno  yyyymm  Recomm_ShortInterest
     0   10051  200704                     1
     1   10104  200607                     1
     2   10104  200807                     1
     3   10104  200808                     1
     4   10104  200903                     1
     5   10104  200904                     1
     6   10104  200906                     1
     7   10104  201402                     1
     8   10104  201507                     1
     9   10104  201508                     1
```

**Feedback**:
- Num observations with std_diff >= TOL_DIFF_1: 0/15314 (0.000%)
- Stata standard deviation: 4.97e-01

---

### ResidualMomentum

**Status**: ❌ FAILED

**Test Results**:
- Test 1 - Column names: ✅ PASSED
- Test 2 - Superset check: ✅ PASSED
- Test 3 - Precision1 check: ✅ PASSED
- Test 4 - Precision2 check: ❌ FAILED

**Columns**: ['ResidualMomentum']

**Observations**:
- Stata:  3,458,422
- Python: 3,458,602
- Common: 3,458,422

**Precision1**: 0.697% obs with std_diff >= 1.00e-02 (tolerance: < 10%)

**Precision2**: 99th percentile diff = 2.77e-03 (tolerance: < 1.00e-03)

**Feedback**:
- Num observations with std_diff >= TOL_DIFF_1: 24112/3458422 (0.697%)
- Stata standard deviation: 3.30e-01

**Most Recent Bad Observations**:
```
   permno  yyyymm    python     stata      diff
0   10028  202412  0.289036  0.283338  0.005699
1   10107  202412 -0.795068 -0.786140 -0.008928
2   10252  202412  0.283345  0.277829  0.005516
3   10294  202412 -0.792843 -0.800530  0.007688
4   10308  202412  0.409725  0.405028  0.004697
5   10318  202412 -0.092833 -0.098400  0.005568
6   10397  202412 -0.336479 -0.339856  0.003377
7   10606  202412 -0.643135 -0.647104  0.003969
8   10629  202412  0.348657  0.343000  0.005657
9   10892  202412  0.370519  0.366241  0.004278
```

**Largest Differences**:
```
   permno  yyyymm    python     stata      diff
0   88406  202408 -0.411009 -0.454921  0.043912
1   12975  201911  1.415373  1.371636  0.043736
2   12296  202408 -0.388452 -0.431406  0.042954
3   12975  201912  1.335915  1.294238  0.041677
4   88406  202407 -0.435183 -0.475339  0.040156
5   14081  202409 -0.658667 -0.698220  0.039553
6   88608  202408 -0.349476 -0.387996  0.038521
7   12296  202407 -0.389629 -0.427586  0.037957
8   88608  202407 -0.409801 -0.447592  0.037791
9   92816  202406  1.158787  1.124535  0.034252
```

---

### ReturnSkew

**Status**: ✅ PASSED

**Test Results**:
- Test 1 - Column names: ✅ PASSED
- Test 2 - Superset check: ✅ PASSED
- Test 3 - Precision1 check: ✅ PASSED
- Test 4 - Precision2 check: ✅ PASSED

**Columns**: ['ReturnSkew']

**Observations**:
- Stata:  4,952,730
- Python: 4,952,730
- Common: 4,952,730

**Precision1**: 0.000% obs with std_diff >= 1.00e-02 (tolerance: < 10%)

**Precision2**: 99th percentile diff = 1.78e-15 (tolerance: < 1.00e-03)

**Feedback**:
- Num observations with std_diff >= TOL_DIFF_1: 0/4952730 (0.000%)
- Stata standard deviation: 9.83e-01

---

### ReturnSkew3F

**Status**: ❌ FAILED

**Test Results**:
- Test 1 - Column names: ✅ PASSED
- Test 2 - Superset check: ✅ PASSED
- Test 3 - Precision1 check: ✅ PASSED
- Test 4 - Precision2 check: ❌ FAILED

**Columns**: ['ReturnSkew3F']

**Observations**:
- Stata:  4,978,948
- Python: 4,988,237
- Common: 4,978,948

**Precision1**: 2.676% obs with std_diff >= 1.00e-02 (tolerance: < 10%)

**Precision2**: 99th percentile diff = 2.30e-02 (tolerance: < 1.00e-03)

**Feedback**:
- Num observations with std_diff >= TOL_DIFF_1: 133232/4978948 (2.676%)
- Stata standard deviation: 8.50e-01

**Most Recent Bad Observations**:
```
   permno  yyyymm    python     stata      diff
0   10777  202412 -0.081862 -0.091706  0.009843
1   10890  202412 -2.034009 -2.020654 -0.013356
2   11369  202412 -0.138541 -0.147520  0.008979
3   11404  202412 -0.595165 -0.604012  0.008846
4   11674  202412 -0.248130 -0.262484  0.014354
5   12397  202412  0.255910  0.246951  0.008959
6   12476  202412 -1.112346 -1.139055  0.026710
7   12558  202412 -0.473364 -0.491103  0.017739
8   12680  202412  1.581095  1.593038 -0.011943
9   12753  202412 -0.725019 -0.734683  0.009664
```

**Largest Differences**:
```
   permno  yyyymm    python     stata      diff
0   11651  198709 -1.776812  4.129483 -5.906295
1   21232  197411 -1.811528  3.474396 -5.285924
2   31317  196511  0.987175 -4.129483  5.116658
3   36169  196511  0.987175 -4.129483  5.116658
4   24994  198601 -0.834719  4.248529 -5.083248
5   92954  198601 -0.834719  4.248529 -5.083248
6   10072  199207  0.641259 -4.364358  5.005617
7   10245  199207  0.641259 -4.364358  5.005617
8   26551  199207  0.641259 -4.364358  5.005617
9   28864  199207  0.641259 -4.364358  5.005617
```

---

### RevenueSurprise

**Status**: ✅ PASSED

**Test Results**:
- Test 1 - Column names: ✅ PASSED
- Test 2 - Superset check: ✅ PASSED
- Test 3 - Precision1 check: ✅ PASSED
- Test 4 - Precision2 check: ✅ PASSED

**Columns**: ['RevenueSurprise']

**Observations**:
- Stata:  2,107,489
- Python: 2,107,507
- Common: 2,107,434

**Precision1**: 0.009% obs with std_diff >= 1.00e-02 (tolerance: < 10%)

**Precision2**: 99th percentile diff = 6.01e-06 (tolerance: < 1.00e-03)

**Feedback**:
- Num observations with std_diff >= TOL_DIFF_1: 200/2107434 (0.009%)
- Stata standard deviation: 1.16e+02

---

### RoE

**Status**: ✅ PASSED

**Test Results**:
- Test 1 - Column names: ✅ PASSED
- Test 2 - Superset check: ✅ PASSED
- Test 3 - Precision1 check: ✅ PASSED
- Test 4 - Precision2 check: ✅ PASSED

**Columns**: ['RoE']

**Observations**:
- Stata:  3,527,662
- Python: 3,528,982
- Common: 3,527,662

**Precision1**: 0.000% obs with std_diff >= 1.00e-02 (tolerance: < 10%)

**Precision2**: 99th percentile diff = 1.97e-07 (tolerance: < 1.00e-03)

**Feedback**:
- Num observations with std_diff >= TOL_DIFF_1: 0/3527662 (0.000%)
- Stata standard deviation: 7.65e+01

---

### SP

**Status**: ✅ PASSED

**Test Results**:
- Test 1 - Column names: ✅ PASSED
- Test 2 - Superset check: ✅ PASSED
- Test 3 - Precision1 check: ✅ PASSED
- Test 4 - Precision2 check: ✅ PASSED

**Columns**: ['SP']

**Observations**:
- Stata:  3,030,926
- Python: 3,030,928
- Common: 3,030,926

**Precision1**: 0.000% obs with std_diff >= 1.00e-02 (tolerance: < 10%)

**Precision2**: 99th percentile diff = 7.08e-07 (tolerance: < 1.00e-03)

**Feedback**:
- Num observations with std_diff >= TOL_DIFF_1: 0/3030926 (0.000%)
- Stata standard deviation: 8.63e+00

---

### STreversal

**Status**: ✅ PASSED

**Test Results**:
- Test 1 - Column names: ✅ PASSED
- Test 2 - Superset check: ✅ PASSED
- Test 3 - Precision1 check: ✅ PASSED
- Test 4 - Precision2 check: ✅ PASSED

**Columns**: ['STreversal']

**Observations**:
- Stata:  4,047,630
- Python: 4,047,630
- Common: 4,047,630

**Precision1**: 0.000% obs with std_diff >= 1.00e-02 (tolerance: < 10%)

**Precision2**: 99th percentile diff = 1.00e-08 (tolerance: < 1.00e-03)

**Feedback**:
- Num observations with std_diff >= TOL_DIFF_1: 0/4047630 (0.000%)
- Stata standard deviation: 1.86e-01

---

### ShareIss1Y

**Status**: ✅ PASSED

**Test Results**:
- Test 1 - Column names: ✅ PASSED
- Test 2 - Superset check: ✅ PASSED
- Test 3 - Precision1 check: ✅ PASSED
- Test 4 - Precision2 check: ✅ PASSED

**Columns**: ['ShareIss1Y']

**Observations**:
- Stata:  3,517,326
- Python: 3,517,511
- Common: 3,517,326

**Precision1**: 0.000% obs with std_diff >= 1.00e-02 (tolerance: < 10%)

**Precision2**: 99th percentile diff = 1.06e-07 (tolerance: < 1.00e-03)

**Feedback**:
- Num observations with std_diff >= TOL_DIFF_1: 0/3517326 (0.000%)
- Stata standard deviation: 5.94e+02

---

### ShareIss5Y

**Status**: ✅ PASSED

**Test Results**:
- Test 1 - Column names: ✅ PASSED
- Test 2 - Superset check: ✅ PASSED
- Test 3 - Precision1 check: ✅ PASSED
- Test 4 - Precision2 check: ✅ PASSED

**Columns**: ['ShareIss5Y']

**Observations**:
- Stata:  2,507,320
- Python: 2,508,021
- Common: 2,507,320

**Precision1**: 0.000% obs with std_diff >= 1.00e-02 (tolerance: < 10%)

**Precision2**: 99th percentile diff = 3.72e-07 (tolerance: < 1.00e-03)

**Feedback**:
- Num observations with std_diff >= TOL_DIFF_1: 0/2507320 (0.000%)
- Stata standard deviation: 7.86e+03

---

### ShareRepurchase

**Status**: ✅ PASSED

**Test Results**:
- Test 1 - Column names: ✅ PASSED
- Test 2 - Superset check: ✅ PASSED
- Test 3 - Precision1 check: ✅ PASSED
- Test 4 - Precision2 check: ✅ PASSED

**Columns**: ['ShareRepurchase']

**Observations**:
- Stata:  3,624,363
- Python: 3,625,491
- Common: 3,624,363

**Precision1**: 0.002% obs with std_diff >= 1.00e-02 (tolerance: < 10%)

**Precision2**: 99th percentile diff = 0.00e+00 (tolerance: < 1.00e-03)

**Feedback**:
- Num observations with std_diff >= TOL_DIFF_1: 72/3624363 (0.002%)
- Stata standard deviation: 4.73e-01

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

### ShortInterest

**Status**: ❌ FAILED

**Test Results**:
- Test 1 - Column names: ✅ PASSED
- Test 2 - Superset check: ✅ PASSED
- Test 3 - Precision1 check: ✅ PASSED
- Test 4 - Precision2 check: ❌ FAILED

**Columns**: ['ShortInterest']

**Observations**:
- Stata:  873,175
- Python: 873,182
- Common: 873,175

**Precision1**: 0.000% obs with std_diff >= 1.00e-02 (tolerance: < 10%)

**Precision2**: 99th percentile diff = 8.61e-03 (tolerance: < 1.00e-03)

**Feedback**:
- Num observations with std_diff >= TOL_DIFF_1: 0/873175 (0.000%)
- Stata standard deviation: 1.69e+05

---

### Size

**Status**: ✅ PASSED

**Test Results**:
- Test 1 - Column names: ✅ PASSED
- Test 2 - Superset check: ✅ PASSED
- Test 3 - Precision1 check: ✅ PASSED
- Test 4 - Precision2 check: ✅ PASSED

**Columns**: ['Size']

**Observations**:
- Stata:  4,029,130
- Python: 4,029,252
- Common: 4,029,130

**Precision1**: 0.000% obs with std_diff >= 1.00e-02 (tolerance: < 10%)

**Precision2**: 99th percentile diff = 4.00e-07 (tolerance: < 1.00e-03)

**Feedback**:
- Num observations with std_diff >= TOL_DIFF_1: 0/4029130 (0.000%)
- Stata standard deviation: 2.33e+00

---

### SmileSlope

**Status**: ✅ PASSED

**Test Results**:
- Test 1 - Column names: ✅ PASSED
- Test 2 - Superset check: ✅ PASSED
- Test 3 - Precision1 check: ✅ PASSED
- Test 4 - Precision2 check: ✅ PASSED

**Columns**: ['SmileSlope']

**Observations**:
- Stata:  862,230
- Python: 859,994
- Common: 856,084

**Precision1**: 0.038% obs with std_diff >= 1.00e-02 (tolerance: < 10%)

**Precision2**: 99th percentile diff = 2.00e-08 (tolerance: < 1.00e-03)

**Feedback**:
- Num observations with std_diff >= TOL_DIFF_1: 327/856084 (0.038%)
- Stata standard deviation: 4.76e-01

---

### Spinoff

**Status**: ✅ PASSED

**Test Results**:
- Test 1 - Column names: ✅ PASSED
- Test 2 - Superset check: ✅ PASSED
- Test 3 - Precision1 check: ✅ PASSED
- Test 4 - Precision2 check: ✅ PASSED

**Columns**: ['Spinoff']

**Observations**:
- Stata:  4,047,630
- Python: 4,047,630
- Common: 4,047,630

**Precision1**: 0.000% obs with std_diff >= 1.00e-02 (tolerance: < 10%)

**Precision2**: 99th percentile diff = 0.00e+00 (tolerance: < 1.00e-03)

**Feedback**:
- Num observations with std_diff >= TOL_DIFF_1: 0/4047630 (0.000%)
- Stata standard deviation: 1.57e-01

---

### SurpriseRD

**Status**: ✅ PASSED

**Test Results**:
- Test 1 - Column names: ✅ PASSED
- Test 2 - Superset check: ✅ PASSED
- Test 3 - Precision1 check: ✅ PASSED
- Test 4 - Precision2 check: ✅ PASSED

**Columns**: ['SurpriseRD']

**Observations**:
- Stata:  1,545,193
- Python: 1,552,503
- Common: 1,545,193

**Precision1**: 0.005% obs with std_diff >= 1.00e-02 (tolerance: < 10%)

**Precision2**: 99th percentile diff = 0.00e+00 (tolerance: < 1.00e-03)

**Feedback**:
- Num observations with std_diff >= TOL_DIFF_1: 84/1545193 (0.005%)
- Stata standard deviation: 4.52e-01

---

### Tax

**Status**: ❌ FAILED

**Test Results**:
- Test 1 - Column names: ✅ PASSED
- Test 2 - Superset check: ✅ PASSED
- Test 3 - Precision1 check: ✅ PASSED
- Test 4 - Precision2 check: ❌ FAILED

**Columns**: ['Tax']

**Observations**:
- Stata:  3,211,651
- Python: 3,213,292
- Common: 3,211,651

**Precision1**: 1.244% obs with std_diff >= 1.00e-02 (tolerance: < 10%)

**Precision2**: 99th percentile diff = 6.12e-01 (tolerance: < 1.00e-03)

**Feedback**:
- Num observations with std_diff >= TOL_DIFF_1: 39943/3211651 (1.244%)
- Stata standard deviation: 1.90e+01

**Most Recent Bad Observations**:
```
   permno  yyyymm     python  stata       diff
0   22084  202606  29.805790    1.0  28.805790
1   55984  202606  -0.000000    1.0  -1.000000
2   12751  202605   0.121108    1.0  -0.878892
3   13332  202605   0.001470    1.0  -0.998530
4   14618  202605   0.004255    1.0  -0.995745
5   14734  202605  -0.000000    1.0  -1.000000
6   15305  202605   0.002373    1.0  -0.997627
7   15636  202605   0.153538    1.0  -0.846462
8   16401  202605   0.212764    1.0  -0.787236
9   17036  202605   0.077854    1.0  -0.922146
```

**Largest Differences**:
```
   permno  yyyymm       python  stata         diff
0   26542  198906  2023.529412    1.0  2022.529412
1   26542  198907  2023.529412    1.0  2022.529412
2   26542  198908  2023.529412    1.0  2022.529412
3   26542  198909  2023.529412    1.0  2022.529412
4   26542  198910  2023.529412    1.0  2022.529412
5   26542  198911  2023.529412    1.0  2022.529412
6   26542  198912  2023.529412    1.0  2022.529412
7   26542  199001  2023.529412    1.0  2022.529412
8   26542  199002  2023.529412    1.0  2022.529412
9   26542  199003  2023.529412    1.0  2022.529412
```

---

### TotalAccruals

**Status**: ✅ PASSED

**Test Results**:
- Test 1 - Column names: ✅ PASSED
- Test 2 - Superset check: ✅ PASSED
- Test 3 - Precision1 check: ✅ PASSED
- Test 4 - Precision2 check: ✅ PASSED

**Columns**: ['TotalAccruals']

**Observations**:
- Stata:  3,141,468
- Python: 3,157,473
- Common: 3,141,468

**Precision1**: 0.001% obs with std_diff >= 1.00e-02 (tolerance: < 10%)

**Precision2**: 99th percentile diff = 6.42e-08 (tolerance: < 1.00e-03)

**Feedback**:
- Num observations with std_diff >= TOL_DIFF_1: 24/3141468 (0.001%)
- Stata standard deviation: 7.82e-01

---

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
- Python: 2,057,228
- Common: 2,056,779

**Precision1**: 97.153% obs with std_diff >= 1.00e-02 (tolerance: < 10%)

**Precision2**: 99th percentile diff = 2.63e-01 (tolerance: < 1.00e-03)

**Feedback**:
- Num observations with std_diff >= TOL_DIFF_1: 1998225/2056779 (97.153%)
- Stata standard deviation: 1.54e-01

**Most Recent Bad Observations**:
```
   permno  yyyymm    python     stata      diff
0   10026  202412 -0.034347  0.032569 -0.066916
1   10032  202412 -0.029719  0.035968 -0.065687
2   10104  202412 -0.031795  0.034036 -0.065831
3   10107  202412 -0.030447  0.038111 -0.068558
4   10138  202412 -0.027720  0.037830 -0.065549
5   10145  202412 -0.030421  0.036421 -0.066841
6   10158  202412 -0.029272  0.032967 -0.062240
7   10200  202412 -0.029451  0.036853 -0.066304
8   10220  202412 -0.035748  0.030636 -0.066384
9   10252  202412 -0.031573  0.033475 -0.065049
```

**Largest Differences**:
```
   permno  yyyymm    python     stata      diff
0   89901  202010  3.046132  0.350159  2.695973
1   89901  202009  2.886221  0.484879  2.401342
2   91040  201802  2.489060  0.729334  1.759726
3   91040  201803  2.278041  0.577583  1.700457
4   89901  202011  1.880780  0.261689  1.619091
5   91040  201710  0.785790 -0.810950  1.596739
6   66800  200907  3.193169  1.620982  1.572186
7   91040  201801  2.064963  0.533972  1.530991
8   91040  201709  0.712680 -0.776422  1.489103
9   86173  200103  1.641341  0.196553  1.444788
```

---

### UpRecomm

**Status**: ❌ FAILED

**Test Results**:
- Test 1 - Column names: ✅ PASSED
- Test 2 - Superset check: ❌ FAILED (Python missing 14792 Stata observations)
- Test 3 - Precision1 check: ✅ PASSED
- Test 4 - Precision2 check: ✅ PASSED

**Columns**: ['UpRecomm']

**Observations**:
- Stata:  463,983
- Python: 450,458
- Common: 449,191

**Precision1**: 0.023% obs with std_diff >= 1.00e-02 (tolerance: < 10%)

**Precision2**: 99th percentile diff = 0.00e+00 (tolerance: < 1.00e-03)

**Missing Observations Sample**:
```
 index  permno  yyyymm  UpRecomm
     0   10001  199311         0
     1   10002  200210         0
     2   10010  199311         0
     3   10011  199511         0
     4   10012  199402         0
     5   10016  199312         0
     6   10019  199403         0
     7   10025  199801         0
     8   10026  199311         0
     9   10028  202103         0
```

**Feedback**:
- Num observations with std_diff >= TOL_DIFF_1: 105/449191 (0.023%)
- Stata standard deviation: 4.81e-01

---

### VarCF

**Status**: ✅ PASSED

**Test Results**:
- Test 1 - Column names: ✅ PASSED
- Test 2 - Superset check: ✅ PASSED
- Test 3 - Precision1 check: ✅ PASSED
- Test 4 - Precision2 check: ✅ PASSED

**Columns**: ['VarCF']

**Observations**:
- Stata:  2,547,003
- Python: 2,547,003
- Common: 2,547,003

**Precision1**: 0.000% obs with std_diff >= 1.00e-02 (tolerance: < 10%)

**Precision2**: 99th percentile diff = 1.03e-07 (tolerance: < 1.00e-03)

**Feedback**:
- Num observations with std_diff >= TOL_DIFF_1: 0/2547003 (0.000%)
- Stata standard deviation: 2.20e+02

---

### VolMkt

**Status**: ✅ PASSED

**Test Results**:
- Test 1 - Column names: ✅ PASSED
- Test 2 - Superset check: ✅ PASSED
- Test 3 - Precision1 check: ✅ PASSED
- Test 4 - Precision2 check: ✅ PASSED

**Columns**: ['VolMkt']

**Observations**:
- Stata:  4,359,237
- Python: 4,361,398
- Common: 4,358,313

**Precision1**: 0.008% obs with std_diff >= 1.00e-02 (tolerance: < 10%)

**Precision2**: 99th percentile diff = 7.79e-08 (tolerance: < 1.00e-03)

**Feedback**:
- Num observations with std_diff >= TOL_DIFF_1: 368/4358313 (0.008%)
- Stata standard deviation: 2.14e+00

---

### VolSD

**Status**: ✅ PASSED

**Test Results**:
- Test 1 - Column names: ✅ PASSED
- Test 2 - Superset check: ✅ PASSED
- Test 3 - Precision1 check: ✅ PASSED
- Test 4 - Precision2 check: ✅ PASSED

**Columns**: ['VolSD']

**Observations**:
- Stata:  3,922,498
- Python: 3,922,399
- Common: 3,921,598

**Precision1**: 0.010% obs with std_diff >= 1.00e-02 (tolerance: < 10%)

**Precision2**: 99th percentile diff = 3.32e-13 (tolerance: < 1.00e-03)

**Feedback**:
- Num observations with std_diff >= TOL_DIFF_1: 396/3921598 (0.010%)
- Stata standard deviation: 3.87e+01

---

### VolumeTrend

**Status**: ❌ FAILED

**Test Results**:
- Test 1 - Column names: ✅ PASSED
- Test 2 - Superset check: ✅ PASSED
- Test 3 - Precision1 check: ✅ PASSED
- Test 4 - Precision2 check: ❌ FAILED

**Columns**: ['VolumeTrend']

**Observations**:
- Stata:  3,655,889
- Python: 5,153,763
- Common: 3,655,889

**Precision1**: 1.357% obs with std_diff >= 1.00e-02 (tolerance: < 10%)

**Precision2**: 99th percentile diff = 1.93e-03 (tolerance: < 1.00e-03)

**Feedback**:
- Num observations with std_diff >= TOL_DIFF_1: 49596/3655889 (1.357%)
- Stata standard deviation: 2.07e-02

**Most Recent Bad Observations**:
```
   permno  yyyymm    python     stata      diff
0   10066  202412 -0.042738 -0.007268 -0.035470
1   10253  202412 -0.051729 -0.054648  0.002919
2   11153  202412 -0.051729  0.001885 -0.053615
3   11379  202412 -0.036342 -0.014016 -0.022326
4   12828  202412 -0.051729 -0.054894  0.003165
5   12839  202412 -0.051729 -0.055632  0.003903
6   12928  202412  0.108894 -0.000076  0.108969
7   13563  202412 -0.019177 -0.051617  0.032440
8   13779  202412 -0.051729 -0.052743  0.001014
9   13828  202412 -0.051729 -0.036236 -0.015493
```

**Largest Differences**:
```
   permno  yyyymm    python     stata      diff
0   83630  201203  0.125749 -0.037886  0.163634
1   88937  202412  0.166484  0.006299  0.160185
2   83630  201204  0.119393 -0.032068  0.151461
3   30744  200111  0.155265  0.008748  0.146517
4   84521  201001  0.130462 -0.014673  0.145135
5   27167  201712  0.147492  0.003482  0.144010
6   83630  201205  0.112769 -0.029291  0.142060
7   84757  202003  0.145373  0.004022  0.141350
8   30744  200112  0.146678  0.008842  0.137836
9   27167  201801  0.141298  0.003938  0.137359
```

---

### XFIN

**Status**: ✅ PASSED

**Test Results**:
- Test 1 - Column names: ✅ PASSED
- Test 2 - Superset check: ✅ PASSED
- Test 3 - Precision1 check: ✅ PASSED
- Test 4 - Precision2 check: ✅ PASSED

**Columns**: ['XFIN']

**Observations**:
- Stata:  3,022,290
- Python: 3,023,550
- Common: 3,022,290

**Precision1**: 0.002% obs with std_diff >= 1.00e-02 (tolerance: < 10%)

**Precision2**: 99th percentile diff = 3.29e-08 (tolerance: < 1.00e-03)

**Feedback**:
- Num observations with std_diff >= TOL_DIFF_1: 72/3022290 (0.002%)
- Stata standard deviation: 6.16e-01

---

### betaVIX

**Status**: ✅ PASSED

**Test Results**:
- Test 1 - Column names: ✅ PASSED
- Test 2 - Superset check: ✅ PASSED
- Test 3 - Precision1 check: ✅ PASSED
- Test 4 - Precision2 check: ✅ PASSED

**Columns**: ['betaVIX']

**Observations**:
- Stata:  3,510,758
- Python: 3,553,481
- Common: 3,510,758

**Precision1**: 0.041% obs with std_diff >= 1.00e-02 (tolerance: < 10%)

**Precision2**: 99th percentile diff = 2.33e-05 (tolerance: < 1.00e-03)

**Feedback**:
- Num observations with std_diff >= TOL_DIFF_1: 1443/3510758 (0.041%)
- Stata standard deviation: 1.72e-02

---

### cfp

**Status**: ✅ PASSED

**Test Results**:
- Test 1 - Column names: ✅ PASSED
- Test 2 - Superset check: ✅ PASSED
- Test 3 - Precision1 check: ✅ PASSED
- Test 4 - Precision2 check: ✅ PASSED

**Columns**: ['cfp']

**Observations**:
- Stata:  2,613,997
- Python: 2,614,930
- Common: 2,613,997

**Precision1**: 0.000% obs with std_diff >= 1.00e-02 (tolerance: < 10%)

**Precision2**: 99th percentile diff = 7.89e-08 (tolerance: < 1.00e-03)

**Feedback**:
- Num observations with std_diff >= TOL_DIFF_1: 7/2613997 (0.000%)
- Stata standard deviation: 1.90e+00

---

### dCPVolSpread

**Status**: ✅ PASSED

**Test Results**:
- Test 1 - Column names: ✅ PASSED
- Test 2 - Superset check: ✅ PASSED
- Test 3 - Precision1 check: ✅ PASSED
- Test 4 - Precision2 check: ✅ PASSED

**Columns**: ['dCPVolSpread']

**Observations**:
- Stata:  851,720
- Python: 851,001
- Common: 845,632

**Precision1**: 0.037% obs with std_diff >= 1.00e-02 (tolerance: < 10%)

**Precision2**: 99th percentile diff = 3.00e-08 (tolerance: < 1.00e-03)

**Feedback**:
- Num observations with std_diff >= TOL_DIFF_1: 316/845632 (0.037%)
- Stata standard deviation: 5.81e-01

---

### dNoa

**Status**: ✅ PASSED

**Test Results**:
- Test 1 - Column names: ✅ PASSED
- Test 2 - Superset check: ✅ PASSED
- Test 3 - Precision1 check: ✅ PASSED
- Test 4 - Precision2 check: ✅ PASSED

**Columns**: ['dNoa']

**Observations**:
- Stata:  3,194,445
- Python: 3,195,426
- Common: 3,194,445

**Precision1**: 0.005% obs with std_diff >= 1.00e-02 (tolerance: < 10%)

**Precision2**: 99th percentile diff = 1.36e-07 (tolerance: < 1.00e-03)

**Feedback**:
- Num observations with std_diff >= TOL_DIFF_1: 156/3194445 (0.005%)
- Stata standard deviation: 1.49e+00

---

### dVolCall

**Status**: ✅ PASSED

**Test Results**:
- Test 1 - Column names: ✅ PASSED
- Test 2 - Superset check: ✅ PASSED
- Test 3 - Precision1 check: ✅ PASSED
- Test 4 - Precision2 check: ✅ PASSED

**Columns**: ['dVolCall']

**Observations**:
- Stata:  851,720
- Python: 851,001
- Common: 845,632

**Precision1**: 0.042% obs with std_diff >= 1.00e-02 (tolerance: < 10%)

**Precision2**: 99th percentile diff = 3.00e-08 (tolerance: < 1.00e-03)

**Feedback**:
- Num observations with std_diff >= TOL_DIFF_1: 351/845632 (0.042%)
- Stata standard deviation: 5.28e-01

---

### dVolPut

**Status**: ✅ PASSED

**Test Results**:
- Test 1 - Column names: ✅ PASSED
- Test 2 - Superset check: ✅ PASSED
- Test 3 - Precision1 check: ✅ PASSED
- Test 4 - Precision2 check: ✅ PASSED

**Columns**: ['dVolPut']

**Observations**:
- Stata:  851,720
- Python: 851,001
- Common: 845,632

**Precision1**: 0.042% obs with std_diff >= 1.00e-02 (tolerance: < 10%)

**Precision2**: 99th percentile diff = 3.00e-08 (tolerance: < 1.00e-03)

**Feedback**:
- Num observations with std_diff >= TOL_DIFF_1: 352/845632 (0.042%)
- Stata standard deviation: 5.33e-01

---

### fgr5yrLag

**Status**: ✅ PASSED

**Test Results**:
- Test 1 - Column names: ✅ PASSED
- Test 2 - Superset check: ✅ PASSED
- Test 3 - Precision1 check: ✅ PASSED
- Test 4 - Precision2 check: ✅ PASSED

**Columns**: ['fgr5yrLag']

**Observations**:
- Stata:  875,784
- Python: 875,652
- Common: 873,864

**Precision1**: 0.069% obs with std_diff >= 1.00e-02 (tolerance: < 10%)

**Precision2**: 99th percentile diff = 2.00e-06 (tolerance: < 1.00e-03)

**Feedback**:
- Num observations with std_diff >= TOL_DIFF_1: 600/873864 (0.069%)
- Stata standard deviation: 1.24e+01

---

### hire

**Status**: ✅ PASSED

**Test Results**:
- Test 1 - Column names: ✅ PASSED
- Test 2 - Superset check: ✅ PASSED
- Test 3 - Precision1 check: ✅ PASSED
- Test 4 - Precision2 check: ✅ PASSED

**Columns**: ['hire']

**Observations**:
- Stata:  3,496,899
- Python: 3,498,027
- Common: 3,496,899

**Precision1**: 0.008% obs with std_diff >= 1.00e-02 (tolerance: < 10%)

**Precision2**: 99th percentile diff = 2.96e-08 (tolerance: < 1.00e-03)

**Feedback**:
- Num observations with std_diff >= TOL_DIFF_1: 288/3496899 (0.008%)
- Stata standard deviation: 2.77e-01

---

### iomom_cust

**Status**: ❌ FAILED

**Test Results**:
- Test 1 - Column names: ✅ PASSED
- Test 2 - Superset check: ✅ PASSED
- Test 3 - Precision1 check: ✅ PASSED
- Test 4 - Precision2 check: ❌ FAILED

**Columns**: ['iomom_cust']

**Observations**:
- Stata:  1,637,670
- Python: 1,637,670
- Common: 1,637,670

**Precision1**: 0.034% obs with std_diff >= 1.00e-02 (tolerance: < 10%)

**Precision2**: 99th percentile diff = 1.04e-03 (tolerance: < 1.00e-03)

**Feedback**:
- Num observations with std_diff >= TOL_DIFF_1: 564/1637670 (0.034%)
- Stata standard deviation: 5.96e+00

**Most Recent Bad Observations**:
```
   permno  yyyymm     python      stata      diff
0   10397  202412 -13.003320 -12.734732 -0.268588
1   10649  202412 -13.003320 -12.734732 -0.268588
2   10812  202412 -13.003320 -12.734732 -0.268588
3   11174  202412 -15.468398 -15.407539 -0.060859
4   12473  202412 -13.003320 -12.734732 -0.268588
5   16437  202412 -15.468398 -15.407539 -0.060859
6   16648  202412 -13.003320 -12.734732 -0.268588
7   16655  202412 -15.468398 -15.407539 -0.060859
8   16750  202412  -1.753785  -5.290940  3.537155
9   16999  202412 -15.468398 -15.407539 -0.060859
```

**Largest Differences**:
```
   permno  yyyymm     python      stata       diff
0   16750  202209  -8.947296 -22.534321  13.587025
1   16750  202201  -7.162393   6.109506 -13.271899
2   16750  202301  16.562568   6.781145   9.781423
3   16750  202310  -7.419968   1.362881  -8.782849
4   16750  202306  17.105154   8.611089   8.494065
5   16750  202210   7.598268  15.977790  -8.379522
6   16750  202401  -4.940950   3.165166  -8.106116
7   16750  202112   3.049989  11.134679  -8.084690
8   16750  202304  -4.408209   2.674375  -7.082583
9   16750  202110  11.566769   4.621628   6.945141
```

---

### iomom_supp

**Status**: ✅ PASSED

**Test Results**:
- Test 1 - Column names: ✅ PASSED
- Test 2 - Superset check: ✅ PASSED
- Test 3 - Precision1 check: ✅ PASSED
- Test 4 - Precision2 check: ✅ PASSED

**Columns**: ['iomom_supp']

**Observations**:
- Stata:  1,639,842
- Python: 1,639,842
- Common: 1,639,842

**Precision1**: 0.016% obs with std_diff >= 1.00e-02 (tolerance: < 10%)

**Precision2**: 99th percentile diff = 8.13e-04 (tolerance: < 1.00e-03)

**Feedback**:
- Num observations with std_diff >= TOL_DIFF_1: 258/1639842 (0.016%)
- Stata standard deviation: 5.23e+00

---

### realestate

**Status**: ✅ PASSED

**Test Results**:
- Test 1 - Column names: ✅ PASSED
- Test 2 - Superset check: ✅ PASSED
- Test 3 - Precision1 check: ✅ PASSED
- Test 4 - Precision2 check: ✅ PASSED

**Columns**: ['realestate']

**Observations**:
- Stata:  1,448,154
- Python: 1,448,163
- Common: 1,448,154

**Precision1**: 0.144% obs with std_diff >= 1.00e-02 (tolerance: < 10%)

**Precision2**: 99th percentile diff = 4.09e-08 (tolerance: < 1.00e-03)

**Feedback**:
- Num observations with std_diff >= TOL_DIFF_1: 2091/1448154 (0.144%)
- Stata standard deviation: 2.48e-01

---

### retConglomerate

**Status**: ❌ FAILED

**Test Results**:
- Test 1 - Column names: ✅ PASSED
- Test 2 - Superset check: ❌ FAILED (Python missing 169303 Stata observations)
- Test 3 - Precision1 check: ❌ FAILED
- Test 4 - Precision2 check: ❌ FAILED

**Columns**: ['retConglomerate']

**Observations**:
- Stata:  758,394
- Python: 591,884
- Common: 589,091

**Precision1**: 94.057% obs with std_diff >= 1.00e-02 (tolerance: < 10%)

**Precision2**: 99th percentile diff = 1.70e-01 (tolerance: < 1.00e-03)

**Missing Observations Sample**:
```
 index  permno  yyyymm  retConglomerate
     0   10001  201401         0.011739
     1   10001  201402         0.018180
     2   10001  201403         0.027526
     3   10001  201404         0.016493
     4   10001  201405         0.015747
     5   10001  201406         0.048119
     6   10001  201407        -0.042713
     7   10001  201408         0.036581
     8   10001  201409        -0.058244
     9   10001  201410         0.037713
```

**Feedback**:
- Num observations with std_diff >= TOL_DIFF_1: 554083/589091 (94.057%)
- Stata standard deviation: 8.20e-02

**Most Recent Bad Observations**:
```
   permno  yyyymm    python     stata      diff
0   10104  202412  0.000803  0.054399 -0.053596
1   10253  202412  0.000803  0.054399 -0.053596
2   10318  202412  0.039110 -0.068694  0.107804
3   10516  202412  0.009091 -0.030640  0.039731
4   11308  202412  0.009091 -0.030640  0.039731
5   11654  202412  0.039110 -0.068694  0.107804
6   11701  202412  0.009091 -0.119622  0.128713
7   11845  202412  0.000803  0.054399 -0.053596
8   11850  202412  0.039110 -0.077714  0.116824
9   11995  202412  0.009091 -0.030640  0.039731
```

**Largest Differences**:
```
   permno  yyyymm    python     stata      diff
0   89908  202101  0.342324  4.377937 -4.035613
1   18781  202311  4.121830  0.098565  4.023265
2   14274  202101  0.412303  4.377937 -3.965633
3   19002  202311  4.121830  0.234556  3.887274
4   21249  202311  3.685644  0.234556  3.451088
5   61735  202311  3.550788  0.234556  3.316232
6   75905  202101  2.991671  0.004319  2.987353
7   91416  202101  2.991671  0.004319  2.987353
8   19357  202311  3.110927  0.234556  2.876371
9   13142  201806  3.540630  0.683659  2.856971
```

---

### roaq

**Status**: ✅ PASSED

**Test Results**:
- Test 1 - Column names: ✅ PASSED
- Test 2 - Superset check: ✅ PASSED
- Test 3 - Precision1 check: ✅ PASSED
- Test 4 - Precision2 check: ✅ PASSED

**Columns**: ['roaq']

**Observations**:
- Stata:  2,490,858
- Python: 2,714,809
- Common: 2,490,858

**Precision1**: 0.007% obs with std_diff >= 1.00e-02 (tolerance: < 10%)

**Precision2**: 99th percentile diff = 9.85e-09 (tolerance: < 1.00e-03)

**Feedback**:
- Num observations with std_diff >= TOL_DIFF_1: 169/2490858 (0.007%)
- Stata standard deviation: 2.95e-01

---

### sfe

**Status**: ✅ PASSED

**Test Results**:
- Test 1 - Column names: ✅ PASSED
- Test 2 - Superset check: ✅ PASSED
- Test 3 - Precision1 check: ✅ PASSED
- Test 4 - Precision2 check: ✅ PASSED

**Columns**: ['sfe']

**Observations**:
- Stata:  611,076
- Python: 611,100
- Common: 609,876

**Precision1**: 0.022% obs with std_diff >= 1.00e-02 (tolerance: < 10%)

**Precision2**: 99th percentile diff = 2.62e-08 (tolerance: < 1.00e-03)

**Feedback**:
- Num observations with std_diff >= TOL_DIFF_1: 132/609876 (0.022%)
- Stata standard deviation: 1.89e+01

---

### sinAlgo

**Status**: ❌ FAILED

**Test Results**:
- Test 1 - Column names: ✅ PASSED
- Test 2 - Superset check: ❌ FAILED (Python missing 37059 Stata observations)
- Test 3 - Precision1 check: ✅ PASSED
- Test 4 - Precision2 check: ✅ PASSED

**Columns**: ['sinAlgo']

**Observations**:
- Stata:  233,503
- Python: 908,711
- Common: 196,444

**Precision1**: 0.012% obs with std_diff >= 1.00e-02 (tolerance: < 10%)

**Precision2**: 99th percentile diff = 0.00e+00 (tolerance: < 1.00e-03)

**Missing Observations Sample**:
```
 index  permno  yyyymm  sinAlgo
     0   10021  198601        0
     1   10021  198602        0
     2   10021  198603        0
     3   10021  198604        0
     4   10021  198605        0
     5   10021  198606        0
     6   10021  198607        0
     7   10021  198608        0
     8   10021  198609        0
     9   10021  198610        0
```

**Feedback**:
- Num observations with std_diff >= TOL_DIFF_1: 23/196444 (0.012%)
- Stata standard deviation: 4.10e-01

---

### skew1

**Status**: ✅ PASSED

**Test Results**:
- Test 1 - Column names: ✅ PASSED
- Test 2 - Superset check: ✅ PASSED
- Test 3 - Precision1 check: ✅ PASSED
- Test 4 - Precision2 check: ✅ PASSED

**Columns**: ['skew1']

**Observations**:
- Stata:  473,447
- Python: 472,444
- Common: 470,063

**Precision1**: 0.043% obs with std_diff >= 1.00e-02 (tolerance: < 10%)

**Precision2**: 99th percentile diff = 1.00e-08 (tolerance: < 1.00e-03)

**Feedback**:
- Num observations with std_diff >= TOL_DIFF_1: 200/470063 (0.043%)
- Stata standard deviation: 8.26e-02

---

### std_turn

**Status**: ✅ PASSED

**Test Results**:
- Test 1 - Column names: ✅ PASSED
- Test 2 - Superset check: ✅ PASSED
- Test 3 - Precision1 check: ✅ PASSED
- Test 4 - Precision2 check: ✅ PASSED

**Columns**: ['std_turn']

**Observations**:
- Stata:  2,166,584
- Python: 2,200,763
- Common: 2,166,204

**Precision1**: 0.000% obs with std_diff >= 1.00e-02 (tolerance: < 10%)

**Precision2**: 99th percentile diff = 4.50e-08 (tolerance: < 1.00e-03)

**Feedback**:
- Num observations with std_diff >= TOL_DIFF_1: 0/2166204 (0.000%)
- Stata standard deviation: 3.51e+00

---

### tang

**Status**: ✅ PASSED

**Test Results**:
- Test 1 - Column names: ✅ PASSED
- Test 2 - Superset check: ✅ PASSED
- Test 3 - Precision1 check: ✅ PASSED
- Test 4 - Precision2 check: ✅ PASSED

**Columns**: ['tang']

**Observations**:
- Stata:  1,517,431
- Python: 1,517,875
- Common: 1,517,107

**Precision1**: 0.002% obs with std_diff >= 1.00e-02 (tolerance: < 10%)

**Precision2**: 99th percentile diff = 4.52e-08 (tolerance: < 1.00e-03)

**Feedback**:
- Num observations with std_diff >= TOL_DIFF_1: 36/1517107 (0.002%)
- Stata standard deviation: 1.89e-01

---

### zerotrade12M

**Status**: ✅ PASSED

**Test Results**:
- Test 1 - Column names: ✅ PASSED
- Test 2 - Superset check: ✅ PASSED
- Test 3 - Precision1 check: ✅ PASSED
- Test 4 - Precision2 check: ✅ PASSED

**Columns**: ['zerotrade12M']

**Observations**:
- Stata:  4,342,889
- Python: 4,661,610
- Common: 4,342,889

**Precision1**: 0.000% obs with std_diff >= 1.00e-02 (tolerance: < 10%)

**Precision2**: 99th percentile diff = 6.40e-06 (tolerance: < 1.00e-03)

**Feedback**:
- Num observations with std_diff >= TOL_DIFF_1: 0/4342889 (0.000%)
- Stata standard deviation: 4.04e+01

---

### zerotrade1M

**Status**: ✅ PASSED

**Test Results**:
- Test 1 - Column names: ✅ PASSED
- Test 2 - Superset check: ✅ PASSED
- Test 3 - Precision1 check: ✅ PASSED
- Test 4 - Precision2 check: ✅ PASSED

**Columns**: ['zerotrade1M']

**Observations**:
- Stata:  4,680,231
- Python: 5,077,699
- Common: 4,680,231

**Precision1**: 0.000% obs with std_diff >= 1.00e-02 (tolerance: < 10%)

**Precision2**: 99th percentile diff = 5.56e-07 (tolerance: < 1.00e-03)

**Feedback**:
- Num observations with std_diff >= TOL_DIFF_1: 0/4680231 (0.000%)
- Stata standard deviation: 3.63e+00

---

### zerotrade6M

**Status**: ✅ PASSED

**Test Results**:
- Test 1 - Column names: ✅ PASSED
- Test 2 - Superset check: ✅ PASSED
- Test 3 - Precision1 check: ✅ PASSED
- Test 4 - Precision2 check: ✅ PASSED

**Columns**: ['zerotrade6M']

**Observations**:
- Stata:  4,530,678
- Python: 4,885,711
- Common: 4,530,678

**Precision1**: 0.000% obs with std_diff >= 1.00e-02 (tolerance: < 10%)

**Precision2**: 99th percentile diff = 3.08e-06 (tolerance: < 1.00e-03)

**Feedback**:
- Num observations with std_diff >= TOL_DIFF_1: 0/4530678 (0.000%)
- Stata standard deviation: 2.08e+01

---

### GrLTNOA

**Status**: ❌ MISSING PYTHON CSV

**Error**: Python CSV file not found: ../pyData/Predictors/GrLTNOA.csv

---

### GrSaleToGrInv

**Status**: ❌ MISSING PYTHON CSV

**Error**: Python CSV file not found: ../pyData/Predictors/GrSaleToGrInv.csv

---

### GrSaleToGrOverhead

**Status**: ❌ MISSING PYTHON CSV

**Error**: Python CSV file not found: ../pyData/Predictors/GrSaleToGrOverhead.csv

---

### InvestPPEInv

**Status**: ❌ MISSING PYTHON CSV

**Error**: Python CSV file not found: ../pyData/Predictors/InvestPPEInv.csv

---

### grcapx

**Status**: ❌ MISSING PYTHON CSV

**Error**: Python CSV file not found: ../pyData/Predictors/grcapx.csv

---

### grcapx3y

**Status**: ❌ MISSING PYTHON CSV

**Error**: Python CSV file not found: ../pyData/Predictors/grcapx3y.csv

---

