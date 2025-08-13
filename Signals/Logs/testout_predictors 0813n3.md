# Predictor Validation Results

**Generated**: 2025-08-13 15:46:38

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
| AgeIPO                    | ✅         | ❌       | NA          | NA           | NA                      |
| IndIPO                    | ✅         | ❌       | NA          | NA           | NA                      |
| RDIPO                     | ✅         | ❌       | NA          | NA           | NA                      |
| debug_PatentsRD           | ✅         | ❌       | NA          | NA           | NA                      |
| test_patentsrd            | ✅         | ❌       | NA          | NA           | NA                      |
| RIO_Volatility            | ✅         | ✅       | ❌ (68.92%)  | ❌ (61.95%)   | ❌ (99th diff 1.5E+00)   |
| Recomm_ShortInterest      | ✅         | ✅       | ❌ (57.03%)  | ✅ (0.00%)    | ✅ (99th diff 0.0E+00)   |
| RIO_Disp                  | ✅         | ✅       | ❌ (45.25%)  | ❌ (66.70%)   | ❌ (99th diff 1.6E+00)   |
| RIO_Turnover              | ✅         | ✅       | ❌ (37.18%)  | ❌ (57.48%)   | ❌ (99th diff 1.5E+00)   |
| RIO_MB                    | ✅         | ✅       | ❌ (36.27%)  | ❌ (50.70%)   | ❌ (99th diff 1.5E+00)   |
| PatentsRD                 | ✅         | ✅       | ❌ (23.11%)  | ✅ (6.65%)    | ❌ (99th diff 2.2E+00)   |
| Mom6mJunk                 | ✅         | ✅       | ❌ (17.12%)  | ✅ (0.05%)    | ✅ (99th diff 8.4E-08)   |
| DownRecomm                | ✅         | ✅       | ❌ (3.19%)   | ✅ (0.03%)    | ✅ (99th diff 0.0E+00)   |
| UpRecomm                  | ✅         | ✅       | ❌ (3.19%)   | ✅ (0.02%)    | ✅ (99th diff 0.0E+00)   |
| RDAbility                 | ✅         | ✅       | ❌ (1.43%)   | ❌ (10.38%)   | ✅ (99th diff 9.4E-01)   |
| MomRev                    | ✅         | ✅       | ❌ (1.31%)   | ✅ (0.00%)    | ✅ (99th diff 0.0E+00)   |
| TrendFactor               | ✅         | ✅       | ✅ (0.12%)   | ❌ (97.14%)   | ❌ (99th diff 1.7E+00)   |
| PredictedFE*              | ✅         | ✅       | ✅ (0.27%)   | ❌ (85.27%)   | ✅ (99th diff 2.1E-01)   |
| MS                        | ✅         | ✅       | ✅ (0.00%)   | ❌ (32.97%)   | ❌ (99th diff 2.6E+00)   |
| AbnormalAccruals          | ✅         | ✅       | ✅ (0.68%)   | ❌ (27.95%)   | ✅ (99th diff 3.2E-01)   |
| CitationsRD               | ✅         | ✅       | ✅ (0.00%)   | ❌ (21.54%)   | ❌ (99th diff 2.4E+00)   |
| PriceDelayTstat           | ✅         | ✅       | ✅ (0.00%)   | ❌ (19.38%)   | ❌ (99th diff 4.4E+00)   |
| PS                        | ✅         | ✅       | ✅ (0.00%)   | ❌ (17.93%)   | ✅ (99th diff 5.9E-01)   |
| OrgCap                    | ✅         | ✅       | ✅ (0.00%)   | ❌ (14.23%)   | ✅ (99th diff 1.3E-01)   |
| IndRetBig                 | ✅         | ✅       | ✅ (0.21%)   | ✅ (6.70%)    | ✅ (99th diff 1.0E-01)   |
| BetaFP                    | ✅         | ✅       | ✅ (0.54%)   | ✅ (5.98%)    | ✅ (99th diff 8.9E-02)   |
| DivSeason                 | ✅         | ✅       | ✅ (0.00%)   | ✅ (5.21%)    | ❌ (99th diff 2.0E+00)   |
| BetaTailRisk              | ✅         | ✅       | ✅ (0.00%)   | ✅ (4.15%)    | ✅ (99th diff 2.0E-02)   |
| IndMom                    | ✅         | ✅       | ✅ (0.00%)   | ✅ (3.28%)    | ✅ (99th diff 2.9E-01)   |
| ResidualMomentum          | ✅         | ✅       | ✅ (0.00%)   | ✅ (2.85%)    | ✅ (99th diff 1.1E-01)   |
| ReturnSkew3F              | ✅         | ✅       | ✅ (0.00%)   | ✅ (2.68%)    | ✅ (99th diff 2.7E-02)   |
| HerfAsset                 | ✅         | ✅       | ✅ (0.00%)   | ✅ (1.44%)    | ✅ (99th diff 2.9E-02)   |
| VolumeTrend               | ✅         | ✅       | ✅ (0.00%)   | ✅ (1.36%)    | ✅ (99th diff 9.3E-02)   |
| Tax                       | ✅         | ✅       | ✅ (0.00%)   | ✅ (1.24%)    | ✅ (99th diff 3.2E-02)   |
| PriceDelayRsq             | ✅         | ✅       | ✅ (0.00%)   | ✅ (1.21%)    | ✅ (99th diff 1.9E-01)   |
| IdioVolAHT                | ✅         | ✅       | ✅ (0.14%)   | ✅ (1.11%)    | ✅ (99th diff 1.2E-02)   |
| MomOffSeason              | ✅         | ✅       | ✅ (0.00%)   | ✅ (1.06%)    | ✅ (99th diff 3.5E-02)   |
| NumEarnIncrease           | ✅         | ✅       | ✅ (0.00%)   | ✅ (1.01%)    | ✅ (99th diff 5.2E-01)   |
| Investment                | ✅         | ✅       | ✅ (0.00%)   | ✅ (1.00%)    | ✅ (99th diff 1.0E-02)   |
| CredRatDG                 | ✅         | ✅       | ✅ (0.00%)   | ✅ (0.94%)    | ✅ (99th diff 0.0E+00)   |
| retConglomerate           | ✅         | ✅       | ✅ (0.00%)   | ✅ (0.94%)    | ✅ (99th diff 9.4E-03)   |
| MomOffSeason06YrPlus      | ✅         | ✅       | ✅ (0.00%)   | ✅ (0.92%)    | ✅ (99th diff 3.1E-07)   |
| MomOffSeason11YrPlus      | ✅         | ✅       | ✅ (0.00%)   | ✅ (0.88%)    | ✅ (99th diff 3.2E-07)   |
| Herf                      | ✅         | ✅       | ✅ (0.00%)   | ✅ (0.79%)    | ✅ (99th diff 7.0E-04)   |
| PriceDelaySlope           | ✅         | ✅       | ✅ (0.00%)   | ✅ (0.58%)    | ✅ (99th diff 2.9E-03)   |
| MomOffSeason16YrPlus      | ✅         | ✅       | ✅ (0.00%)   | ✅ (0.51%)    | ✅ (99th diff 1.9E-07)   |
| MomVol                    | ✅         | ✅       | ✅ (0.00%)   | ✅ (0.42%)    | ✅ (99th diff 0.0E+00)   |
| BetaLiquidityPS           | ✅         | ✅       | ✅ (0.00%)   | ✅ (0.31%)    | ✅ (99th diff 5.3E-03)   |
| AnalystValue              | ✅         | ✅       | ✅ (0.22%)   | ✅ (0.26%)    | ✅ (99th diff 1.7E-03)   |
| Mom12mOffSeason           | ✅         | ✅       | ✅ (0.00%)   | ✅ (0.17%)    | ✅ (99th diff 1.0E-15)   |
| REV6                      | ✅         | ✅       | ✅ (0.00%)   | ✅ (0.17%)    | ✅ (99th diff 1.2E-03)   |
| IntanEP                   | ✅         | ✅       | ✅ (0.00%)   | ✅ (0.15%)    | ✅ (99th diff 5.5E-07)   |
| EarnSupBig                | ✅         | ✅       | ✅ (0.16%)   | ✅ (0.15%)    | ✅ (99th diff 1.8E-13)   |
| IntanCFP                  | ✅         | ✅       | ✅ (0.00%)   | ✅ (0.15%)    | ✅ (99th diff 4.6E-05)   |
| MRreversal                | ✅         | ✅       | ✅ (0.00%)   | ✅ (0.15%)    | ✅ (99th diff 1.2E-07)   |
| realestate                | ✅         | ✅       | ✅ (0.00%)   | ✅ (0.14%)    | ✅ (99th diff 1.7E-07)   |
| LRreversal                | ✅         | ✅       | ✅ (0.00%)   | ✅ (0.12%)    | ✅ (99th diff 9.9E-08)   |
| ChForecastAccrual         | ✅         | ✅       | ✅ (0.00%)   | ✅ (0.12%)    | ✅ (99th diff 0.0E+00)   |
| ExclExp                   | ✅         | ✅       | ✅ (0.12%)   | ✅ (0.11%)    | ✅ (99th diff 8.4E-08)   |
| EarningsForecastDisparity | ✅         | ✅       | ✅ (0.22%)   | ✅ (0.08%)    | ✅ (99th diff 3.6E-08)   |
| ForecastDispersion        | ✅         | ✅       | ✅ (0.16%)   | ✅ (0.07%)    | ✅ (99th diff 4.0E-08)   |
| fgr5yrLag                 | ✅         | ✅       | ✅ (0.22%)   | ✅ (0.07%)    | ✅ (99th diff 1.6E-07)   |
| DivYieldST                | ✅         | ✅       | ✅ (0.00%)   | ✅ (0.07%)    | ✅ (99th diff 0.0E+00)   |
| Cash                      | ✅         | ✅       | ✅ (0.00%)   | ✅ (0.06%)    | ✅ (99th diff 1.3E-07)   |
| RIVolSpread               | ✅         | ✅       | ✅ (0.71%)   | ✅ (0.05%)    | ✅ (99th diff 3.3E-07)   |
| CPVolSpread               | ✅         | ✅       | ✅ (0.74%)   | ✅ (0.05%)    | ✅ (99th diff 7.3E-08)   |
| ChangeInRecommendation    | ✅         | ✅       | ✅ (0.23%)   | ✅ (0.05%)    | ✅ (99th diff 1.5E-07)   |
| OptionVolume2             | ✅         | ✅       | ✅ (0.72%)   | ✅ (0.05%)    | ✅ (99th diff 1.6E-08)   |
| ExchSwitch                | ✅         | ✅       | ✅ (0.00%)   | ✅ (0.05%)    | ✅ (99th diff 0.0E+00)   |
| grcapx                    | ✅         | ✅       | ✅ (0.74%)   | ✅ (0.04%)    | ✅ (99th diff 1.8E-09)   |
| skew1                     | ✅         | ✅       | ✅ (0.71%)   | ✅ (0.04%)    | ✅ (99th diff 1.2E-07)   |
| dVolPut                   | ✅         | ✅       | ✅ (0.71%)   | ✅ (0.04%)    | ✅ (99th diff 5.6E-08)   |
| OptionVolume1             | ✅         | ✅       | ✅ (0.72%)   | ✅ (0.04%)    | ✅ (99th diff 1.1E-07)   |
| dVolCall                  | ✅         | ✅       | ✅ (0.71%)   | ✅ (0.04%)    | ✅ (99th diff 5.7E-08)   |
| betaVIX                   | ✅         | ✅       | ✅ (0.00%)   | ✅ (0.04%)    | ✅ (99th diff 1.4E-03)   |
| GrSaleToGrInv             | ✅         | ✅       | ✅ (0.00%)   | ✅ (0.04%)    | ✅ (99th diff 2.4E-09)   |
| AnalystRevision           | ✅         | ✅       | ✅ (0.16%)   | ✅ (0.04%)    | ✅ (99th diff 2.0E-08)   |
| SmileSlope                | ✅         | ✅       | ✅ (0.71%)   | ✅ (0.04%)    | ✅ (99th diff 4.2E-08)   |
| dCPVolSpread              | ✅         | ✅       | ✅ (0.71%)   | ✅ (0.04%)    | ✅ (99th diff 5.2E-08)   |
| iomom_cust                | ✅         | ✅       | ✅ (0.00%)   | ✅ (0.03%)    | ✅ (99th diff 1.7E-04)   |
| BM                        | ✅         | ✅       | ✅ (0.00%)   | ✅ (0.03%)    | ✅ (99th diff 1.3E-07)   |
| EarningsSurprise          | ✅         | ✅       | ✅ (0.02%)   | ✅ (0.03%)    | ✅ (99th diff 4.8E-08)   |
| FEPS                      | ✅         | ✅       | ✅ (0.16%)   | ✅ (0.03%)    | ✅ (99th diff 1.0E-09)   |
| sfe                       | ✅         | ✅       | ✅ (0.20%)   | ✅ (0.02%)    | ✅ (99th diff 1.4E-09)   |
| IdioVol3F                 | ✅         | ✅       | ✅ (0.00%)   | ✅ (0.02%)    | ✅ (99th diff 1.6E-03)   |
| GrSaleToGrOverhead        | ✅         | ✅       | ✅ (0.00%)   | ✅ (0.02%)    | ✅ (99th diff 7.7E-10)   |
| iomom_supp                | ✅         | ✅       | ✅ (0.00%)   | ✅ (0.02%)    | ✅ (99th diff 1.6E-04)   |
| ConsRecomm                | ✅         | ✅       | ✅ (0.23%)   | ✅ (0.01%)    | ✅ (99th diff 0.0E+00)   |
| IntanBM                   | ✅         | ✅       | ✅ (0.00%)   | ✅ (0.01%)    | ✅ (99th diff 3.7E-07)   |
| DelDRC                    | ✅         | ✅       | ✅ (0.00%)   | ✅ (0.01%)    | ✅ (99th diff 1.2E-07)   |
| VolSD                     | ✅         | ✅       | ✅ (0.02%)   | ✅ (0.01%)    | ✅ (99th diff 8.6E-15)   |
| sinAlgo                   | ✅         | ✅       | ✅ (0.00%)   | ✅ (0.01%)    | ✅ (99th diff 0.0E+00)   |
| RevenueSurprise           | ✅         | ✅       | ✅ (0.00%)   | ✅ (0.01%)    | ✅ (99th diff 5.2E-08)   |
| DelNetFin                 | ✅         | ✅       | ✅ (0.00%)   | ✅ (0.01%)    | ✅ (99th diff 2.7E-07)   |
| Accruals                  | ✅         | ✅       | ✅ (0.00%)   | ✅ (0.01%)    | ✅ (99th diff 9.9E-08)   |
| IntanSP                   | ✅         | ✅       | ✅ (0.00%)   | ✅ (0.01%)    | ✅ (99th diff 4.6E-07)   |
| VolMkt                    | ✅         | ✅       | ✅ (0.02%)   | ✅ (0.01%)    | ✅ (99th diff 3.6E-08)   |
| hire                      | ✅         | ✅       | ✅ (0.00%)   | ✅ (0.01%)    | ✅ (99th diff 1.1E-07)   |
| GrLTNOA                   | ✅         | ✅       | ✅ (0.00%)   | ✅ (0.01%)    | ✅ (99th diff 2.8E-08)   |
| DivInit                   | ✅         | ✅       | ✅ (0.00%)   | ✅ (0.01%)    | ✅ (99th diff 0.0E+00)   |
| ChNNCOA                   | ✅         | ✅       | ✅ (0.00%)   | ✅ (0.01%)    | ✅ (99th diff 8.5E-08)   |
| EarningsStreak            | ✅         | ✅       | ✅ (0.19%)   | ✅ (0.01%)    | ✅ (99th diff 2.5E-09)   |
| roaq                      | ✅         | ✅       | ✅ (0.00%)   | ✅ (0.01%)    | ✅ (99th diff 3.3E-08)   |
| ChNAnalyst                | ✅         | ✅       | ✅ (0.11%)   | ✅ (0.01%)    | ✅ (99th diff 0.0E+00)   |
| CustomerMomentum          | ✅         | ✅       | ✅ (0.04%)   | ✅ (0.01%)    | ✅ (99th diff 9.0E-08)   |
| CompositeDebtIssuance     | ✅         | ✅       | ✅ (0.00%)   | ✅ (0.01%)    | ✅ (99th diff 1.2E-07)   |
| DelCOL                    | ✅         | ✅       | ✅ (0.00%)   | ✅ (0.01%)    | ✅ (99th diff 1.5E-07)   |
| GP                        | ✅         | ✅       | ✅ (0.00%)   | ✅ (0.01%)    | ✅ (99th diff 1.1E-07)   |
| DelFINL                   | ✅         | ✅       | ✅ (0.00%)   | ✅ (0.01%)    | ✅ (99th diff 1.8E-07)   |
| CBOperProf                | ✅         | ✅       | ✅ (0.00%)   | ✅ (0.01%)    | ✅ (99th diff 1.3E-07)   |
| DelLTI                    | ✅         | ✅       | ✅ (0.00%)   | ✅ (0.01%)    | ✅ (99th diff 1.9E-07)   |
| SurpriseRD                | ✅         | ✅       | ✅ (0.00%)   | ✅ (0.01%)    | ✅ (99th diff 0.0E+00)   |
| dNoa                      | ✅         | ✅       | ✅ (0.00%)   | ✅ (0.00%)    | ✅ (99th diff 9.1E-08)   |
| ChNWC                     | ✅         | ✅       | ✅ (0.00%)   | ✅ (0.00%)    | ✅ (99th diff 8.4E-08)   |
| NOA                       | ✅         | ✅       | ✅ (0.00%)   | ✅ (0.00%)    | ✅ (99th diff 6.8E-08)   |
| AnnouncementReturn        | ✅         | ✅       | ✅ (0.00%)   | ✅ (0.00%)    | ✅ (99th diff 1.9E-07)   |
| DivOmit                   | ✅         | ✅       | ✅ (0.00%)   | ✅ (0.00%)    | ✅ (99th diff 0.0E+00)   |
| NetDebtFinance            | ✅         | ✅       | ✅ (0.00%)   | ✅ (0.00%)    | ✅ (99th diff 1.2E-07)   |
| OperProfRD                | ✅         | ✅       | ✅ (0.00%)   | ✅ (0.00%)    | ✅ (99th diff 8.5E-08)   |
| OPLeverage                | ✅         | ✅       | ✅ (0.00%)   | ✅ (0.00%)    | ✅ (99th diff 1.2E-07)   |
| XFIN                      | ✅         | ✅       | ✅ (0.00%)   | ✅ (0.00%)    | ✅ (99th diff 5.3E-08)   |
| tang                      | ✅         | ✅       | ✅ (0.02%)   | ✅ (0.00%)    | ✅ (99th diff 2.4E-07)   |
| ShareRepurchase           | ✅         | ✅       | ✅ (0.00%)   | ✅ (0.00%)    | ✅ (99th diff 0.0E+00)   |
| AOP                       | ✅         | ✅       | ✅ (0.22%)   | ✅ (0.00%)    | ✅ (99th diff 5.0E-06)   |
| DelCOA                    | ✅         | ✅       | ✅ (0.00%)   | ✅ (0.00%)    | ✅ (99th diff 1.9E-07)   |
| ChInv                     | ✅         | ✅       | ✅ (0.00%)   | ✅ (0.00%)    | ✅ (99th diff 1.3E-07)   |
| BPEBM                     | ✅         | ✅       | ✅ (0.00%)   | ✅ (0.00%)    | ✅ (99th diff 2.2E-08)   |
| EBM                       | ✅         | ✅       | ✅ (0.00%)   | ✅ (0.00%)    | ✅ (99th diff 2.2E-08)   |
| CF                        | ✅         | ✅       | ✅ (0.00%)   | ✅ (0.00%)    | ✅ (99th diff 2.5E-08)   |
| HerfBE                    | ✅         | ✅       | ✅ (0.00%)   | ✅ (0.00%)    | ✅ (99th diff 1.4E-06)   |
| NetEquityFinance          | ✅         | ✅       | ✅ (0.00%)   | ✅ (0.00%)    | ✅ (99th diff 1.3E-07)   |
| DelEqu                    | ✅         | ✅       | ✅ (0.00%)   | ✅ (0.00%)    | ✅ (99th diff 8.3E-08)   |
| TotalAccruals             | ✅         | ✅       | ✅ (0.00%)   | ✅ (0.00%)    | ✅ (99th diff 8.2E-08)   |
| AssetGrowth               | ✅         | ✅       | ✅ (0.00%)   | ✅ (0.00%)    | ✅ (99th diff 3.6E-08)   |
| OrderBacklogChg           | ✅         | ✅       | ✅ (0.00%)   | ✅ (0.00%)    | ✅ (99th diff 2.2E-07)   |
| ConvDebt                  | ✅         | ✅       | ✅ (0.00%)   | ✅ (0.00%)    | ✅ (99th diff 0.0E+00)   |
| ChTax                     | ✅         | ✅       | ✅ (0.00%)   | ✅ (0.00%)    | ✅ (99th diff 5.0E-10)   |
| PctTotAcc                 | ✅         | ✅       | ✅ (0.00%)   | ✅ (0.00%)    | ✅ (99th diff 7.9E-09)   |
| OperProf                  | ✅         | ✅       | ✅ (0.00%)   | ✅ (0.00%)    | ✅ (99th diff 5.9E-09)   |
| ChAssetTurnover           | ✅         | ✅       | ✅ (0.00%)   | ✅ (0.00%)    | ✅ (99th diff 4.3E-09)   |
| InvestPPEInv              | ✅         | ✅       | ✅ (0.00%)   | ✅ (0.00%)    | ✅ (99th diff 4.7E-08)   |
| CoskewACX                 | ✅         | ✅       | ✅ (0.00%)   | ✅ (0.00%)    | ✅ (99th diff 1.1E-03)   |
| PctAcc                    | ✅         | ✅       | ✅ (0.00%)   | ✅ (0.00%)    | ✅ (99th diff 1.1E-08)   |
| PayoutYield               | ✅         | ✅       | ✅ (0.00%)   | ✅ (0.00%)    | ✅ (99th diff 5.9E-08)   |
| cfp                       | ✅         | ✅       | ✅ (0.00%)   | ✅ (0.00%)    | ✅ (99th diff 4.2E-08)   |
| NetPayoutYield            | ✅         | ✅       | ✅ (0.00%)   | ✅ (0.00%)    | ✅ (99th diff 3.2E-08)   |
| RD                        | ✅         | ✅       | ✅ (0.00%)   | ✅ (0.00%)    | ✅ (99th diff 2.1E-08)   |
| grcapx3y                  | ✅         | ✅       | ✅ (0.75%)   | ✅ (0.00%)    | ✅ (99th diff 5.8E-21)   |
| MeanRankRevGrowth         | ✅         | ✅       | ✅ (0.00%)   | ✅ (0.00%)    | ✅ (99th diff 3.2E-04)   |
| Coskewness                | ✅         | ✅       | ✅ (0.00%)   | ✅ (0.00%)    | ✅ (99th diff 1.3E-03)   |
| InvGrowth                 | ✅         | ✅       | ✅ (0.00%)   | ✅ (0.00%)    | ✅ (99th diff 1.5E-08)   |
| CompEquIss                | ✅         | ✅       | ✅ (0.73%)   | ✅ (0.00%)    | ✅ (99th diff 7.5E-07)   |
| Frontier                  | ✅         | ✅       | ✅ (0.00%)   | ✅ (0.00%)    | ✅ (99th diff 6.5E-07)   |
| ProbInformedTrading       | ✅         | ✅       | ✅ (0.00%)   | ✅ (0.00%)    | ✅ (99th diff 4.5E-07)   |
| High52                    | ✅         | ✅       | ✅ (0.00%)   | ✅ (0.00%)    | ✅ (99th diff 2.7E-07)   |
| Size                      | ✅         | ✅       | ✅ (0.00%)   | ✅ (0.00%)    | ✅ (99th diff 1.7E-07)   |
| zerotrade12M              | ✅         | ✅       | ✅ (0.00%)   | ✅ (0.00%)    | ✅ (99th diff 1.6E-07)   |
| Activism2                 | ✅         | ✅       | ✅ (0.00%)   | ✅ (0.00%)    | ✅ (99th diff 1.6E-07)   |
| zerotrade1M               | ✅         | ✅       | ✅ (0.00%)   | ✅ (0.00%)    | ✅ (99th diff 1.5E-07)   |
| Price                     | ✅         | ✅       | ✅ (0.00%)   | ✅ (0.00%)    | ✅ (99th diff 1.5E-07)   |
| MomSeason06YrPlus         | ✅         | ✅       | ✅ (0.00%)   | ✅ (0.00%)    | ✅ (99th diff 1.5E-07)   |
| zerotrade6M               | ✅         | ✅       | ✅ (0.00%)   | ✅ (0.00%)    | ✅ (99th diff 1.5E-07)   |
| MomSeason11YrPlus         | ✅         | ✅       | ✅ (0.00%)   | ✅ (0.00%)    | ✅ (99th diff 1.4E-07)   |
| GrAdExp                   | ✅         | ✅       | ✅ (0.00%)   | ✅ (0.00%)    | ✅ (99th diff 1.4E-07)   |
| MomSeason16YrPlus         | ✅         | ✅       | ✅ (0.00%)   | ✅ (0.00%)    | ✅ (99th diff 1.4E-07)   |
| MomSeason                 | ✅         | ✅       | ✅ (0.00%)   | ✅ (0.00%)    | ✅ (99th diff 1.3E-07)   |
| RDcap                     | ✅         | ✅       | ✅ (0.02%)   | ✅ (0.00%)    | ✅ (99th diff 1.2E-07)   |
| FR                        | ✅         | ✅       | ✅ (0.00%)   | ✅ (0.00%)    | ✅ (99th diff 1.2E-07)   |
| DelBreadth                | ✅         | ✅       | ✅ (0.00%)   | ✅ (0.00%)    | ✅ (99th diff 1.1E-07)   |
| IntMom                    | ✅         | ✅       | ✅ (0.00%)   | ✅ (0.00%)    | ✅ (99th diff 1.0E-07)   |
| OrderBacklog              | ✅         | ✅       | ✅ (0.00%)   | ✅ (0.00%)    | ✅ (99th diff 1.0E-07)   |
| Mom12m                    | ✅         | ✅       | ✅ (0.00%)   | ✅ (0.00%)    | ✅ (99th diff 1.0E-07)   |
| IO_ShortInterest          | ✅         | ✅       | ✅ (0.00%)   | ✅ (0.00%)    | ✅ (99th diff 9.9E-08)   |
| Beta                      | ✅         | ✅       | ✅ (0.00%)   | ✅ (0.00%)    | ✅ (99th diff 9.8E-08)   |
| Mom6m                     | ✅         | ✅       | ✅ (0.00%)   | ✅ (0.00%)    | ✅ (99th diff 9.4E-08)   |
| FirmAgeMom                | ✅         | ✅       | ✅ (0.00%)   | ✅ (0.00%)    | ✅ (99th diff 9.3E-08)   |
| DolVol                    | ✅         | ✅       | ✅ (0.00%)   | ✅ (0.00%)    | ✅ (99th diff 9.1E-08)   |
| EarningsConsistency       | ✅         | ✅       | ✅ (0.00%)   | ✅ (0.00%)    | ✅ (99th diff 8.8E-08)   |
| SP                        | ✅         | ✅       | ✅ (0.00%)   | ✅ (0.00%)    | ✅ (99th diff 8.2E-08)   |
| BidAskSpread              | ✅         | ✅       | ✅ (0.00%)   | ✅ (0.00%)    | ✅ (99th diff 6.4E-08)   |
| AdExp                     | ✅         | ✅       | ✅ (0.00%)   | ✅ (0.00%)    | ✅ (99th diff 5.9E-08)   |
| MomSeasonShort            | ✅         | ✅       | ✅ (0.00%)   | ✅ (0.00%)    | ✅ (99th diff 5.8E-08)   |
| STreversal                | ✅         | ✅       | ✅ (0.00%)   | ✅ (0.00%)    | ✅ (99th diff 5.4E-08)   |
| NetDebtPrice              | ✅         | ✅       | ✅ (0.00%)   | ✅ (0.00%)    | ✅ (99th diff 5.1E-08)   |
| ShortInterest             | ✅         | ✅       | ✅ (0.00%)   | ✅ (0.00%)    | ✅ (99th diff 5.1E-08)   |
| Leverage                  | ✅         | ✅       | ✅ (0.00%)   | ✅ (0.00%)    | ✅ (99th diff 4.4E-08)   |
| EP                        | ✅         | ✅       | ✅ (0.00%)   | ✅ (0.00%)    | ✅ (99th diff 3.9E-08)   |
| AM                        | ✅         | ✅       | ✅ (0.00%)   | ✅ (0.00%)    | ✅ (99th diff 3.3E-08)   |
| BrandInvest               | ✅         | ✅       | ✅ (0.00%)   | ✅ (0.00%)    | ✅ (99th diff 2.5E-08)   |
| Illiquidity               | ✅         | ✅       | ✅ (0.00%)   | ✅ (0.00%)    | ✅ (99th diff 1.9E-08)   |
| BMdec                     | ✅         | ✅       | ✅ (0.00%)   | ✅ (0.00%)    | ✅ (99th diff 1.8E-08)   |
| std_turn                  | ✅         | ✅       | ✅ (0.02%)   | ✅ (0.00%)    | ✅ (99th diff 1.3E-08)   |
| RDS                       | ✅         | ✅       | ✅ (0.00%)   | ✅ (0.00%)    | ✅ (99th diff 1.0E-08)   |
| BookLeverage              | ✅         | ✅       | ✅ (0.00%)   | ✅ (0.00%)    | ✅ (99th diff 7.7E-09)   |
| ChEQ                      | ✅         | ✅       | ✅ (0.00%)   | ✅ (0.00%)    | ✅ (99th diff 7.0E-09)   |
| EntMult                   | ✅         | ✅       | ✅ (0.00%)   | ✅ (0.00%)    | ✅ (99th diff 5.5E-09)   |
| CashProd                  | ✅         | ✅       | ✅ (0.00%)   | ✅ (0.00%)    | ✅ (99th diff 3.8E-09)   |
| RoE                       | ✅         | ✅       | ✅ (0.00%)   | ✅ (0.00%)    | ✅ (99th diff 2.6E-09)   |
| VarCF                     | ✅         | ✅       | ✅ (0.00%)   | ✅ (0.00%)    | ✅ (99th diff 4.7E-10)   |
| ShareIss1Y                | ✅         | ✅       | ✅ (0.00%)   | ✅ (0.00%)    | ✅ (99th diff 1.8E-10)   |
| ShareIss5Y                | ✅         | ✅       | ✅ (0.00%)   | ✅ (0.00%)    | ✅ (99th diff 4.7E-11)   |
| ReturnSkew                | ✅         | ✅       | ✅ (0.00%)   | ✅ (0.00%)    | ✅ (99th diff 1.8E-15)   |
| RealizedVol               | ✅         | ✅       | ✅ (0.13%)   | ✅ (0.00%)    | ✅ (99th diff 1.8E-15)   |
| EquityDuration            | ✅         | ✅       | ✅ (0.00%)   | ✅ (0.00%)    | ✅ (99th diff 1.2E-15)   |
| ChInvIA                   | ✅         | ✅       | ✅ (0.00%)   | ✅ (0.00%)    | ✅ (99th diff 4.0E-20)   |
| AccrualsBM                | ✅         | ✅       | ✅ (0.00%)   | ✅ (0.00%)    | ✅ (99th diff 0.0E+00)   |
| Activism1                 | ✅         | ✅       | ✅ (0.43%)   | ✅ (0.00%)    | ✅ (99th diff 0.0E+00)   |
| DebtIssuance              | ✅         | ✅       | ✅ (0.00%)   | ✅ (0.00%)    | ✅ (99th diff 0.0E+00)   |
| FirmAge                   | ✅         | ✅       | ✅ (0.00%)   | ✅ (0.00%)    | ✅ (99th diff 0.0E+00)   |
| Governance                | ✅         | ✅       | ✅ (0.00%)   | ✅ (0.00%)    | ✅ (99th diff 0.0E+00)   |
| MaxRet                    | ✅         | ✅       | ✅ (0.00%)   | ✅ (0.00%)    | ✅ (99th diff 0.0E+00)   |
| OScore                    | ✅         | ✅       | ✅ (0.04%)   | ✅ (0.00%)    | ✅ (99th diff 0.0E+00)   |
| ShareVol                  | ✅         | ✅       | ✅ (0.00%)   | ✅ (0.00%)    | ✅ (99th diff 0.0E+00)   |
| Spinoff                   | ✅         | ✅       | ✅ (0.00%)   | ✅ (0.00%)    | ✅ (99th diff 0.0E+00)   |

**Overall**: 190/214 available predictors passed validation
  - Natural passes: 189
  - Overridden passes: 1
**Python CSVs**: 214/214 predictors have Python implementation
\* = Manual override applied (see Predictors/overrides.yaml for details)

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

**Precision2**: 99th percentile diff = 3.34e-08 (tolerance: < 1.00e+00)

**Summary Statistics** (Common Observations):

| Statistic  |          Stata |         Python |     Difference | Std Difference |
|------------|----------------|----------------|----------------|----------------|
| count      |       3.04e+06 |       3.04e+06 |       3.04e+06 |       3.04e+06 |
| mean       |         3.6848 |         3.6848 |      -3.74e-07 |      -1.40e-08 |
| std        |        26.7559 |        26.7559 |       2.63e-04 |       9.82e-06 |
| min        |         0.0000 |         0.0000 |        -0.2458 |        -0.0092 |
| 25%        |         0.6412 |         0.6412 |      -2.47e-08 |      -9.23e-10 |
| 50%        |         1.3833 |         1.3833 |       2.24e-11 |       8.36e-13 |
| 75%        |         3.1169 |         3.1169 |       2.48e-08 |       9.27e-10 |
| max        |     12309.6130 |     12309.6128 |       3.48e-04 |       1.30e-05 |

**Regression Analysis** (Python ~ Stata):

- **Model**: python = -0.0000 + 1.0000 * stata
- **R-squared**: 1.0000
- **N observations**: 3,038,206

| Coefficient |     Estimate |    Std Error | t-statistic |   p-value |
|-------------|--------------|--------------|-------------|----------|
| Intercept   |    -3.72e-07 |     1.52e-07 |     -2.4473 |     0.014 |
| Slope       |       1.0000 |     5.64e-09 |    1.77e+08 |     0.000 |

**Feedback**:
- Num observations with std_diff >= TOL_DIFF_1: 0/3038206 (0.000%)
- Stata standard deviation: 2.68e+01

---

### AOP

**Status**: ✅ PASSED

**Test Results**:
- Test 1 - Column names: ✅ PASSED
- Test 2 - Superset check: ✅ PASSED
- Test 3 - Precision1 check: ✅ PASSED
- Test 4 - Precision2 check: ✅ PASSED

**Columns**: ['AOP']

**Observations**:
- Stata:  1,244,664
- Python: 1,299,504
- Common: 1,241,880

**Precision1**: 0.002% obs with std_diff >= 1.00e-02 (tolerance: < 10%)

**Precision2**: 99th percentile diff = 5.03e-06 (tolerance: < 1.00e+00)

**Summary Statistics** (Common Observations):

| Statistic  |          Stata |         Python |     Difference | Std Difference |
|------------|----------------|----------------|----------------|----------------|
| count      |       1.24e+06 |       1.24e+06 |       1.24e+06 |       1.24e+06 |
| mean       |       158.1360 |       158.1633 |         0.0273 |       5.75e-07 |
| std        |     47467.4186 |     47467.4174 |         8.8469 |       1.86e-04 |
| min        |    -23548.3180 |    -23547.9593 |      -231.9706 |        -0.0049 |
| 25%        |         0.0627 |         0.0611 |      -7.34e-08 |      -1.55e-12 |
| 50%        |         0.3989 |         0.3939 |      -3.63e-09 |      -7.66e-14 |
| 75%        |         1.3596 |         1.3519 |       6.21e-08 |       1.31e-12 |
| max        |       1.53e+07 |       1.53e+07 |      2399.7758 |         0.0506 |

**Regression Analysis** (Python ~ Stata):

- **Model**: python = 0.0273 + 1.0000 * stata
- **R-squared**: 1.0000
- **N observations**: 1,241,880

| Coefficient |     Estimate |    Std Error | t-statistic |   p-value |
|-------------|--------------|--------------|-------------|----------|
| Intercept   |       0.0273 |       0.0079 |      3.4367 |     0.001 |
| Slope       |       1.0000 |     1.67e-07 |    5.98e+06 |     0.000 |

**Feedback**:
- Num observations with std_diff >= TOL_DIFF_1: 24/1241880 (0.002%)
- Stata standard deviation: 4.75e+04

---

### AbnormalAccruals

**Status**: ❌ FAILED

**Test Results**:
- Test 1 - Column names: ✅ PASSED
- Test 2 - Superset check: ✅ PASSED
- Test 3 - Precision1 check: ❌ FAILED
- Test 4 - Precision2 check: ✅ PASSED

**Columns**: ['AbnormalAccruals']

**Observations**:
- Stata:  2,570,664
- Python: 2,567,830
- Common: 2,553,227

**Precision1**: 27.951% obs with std_diff >= 1.00e-02 (tolerance: < 10%)

**Precision2**: 99th percentile diff = 3.25e-01 (tolerance: < 1.00e+00)

**Summary Statistics** (Common Observations):

| Statistic  |          Stata |         Python |     Difference | Std Difference |
|------------|----------------|----------------|----------------|----------------|
| count      |       2.55e+06 |       2.55e+06 |       2.55e+06 |       2.55e+06 |
| mean       |       6.08e-05 |       2.43e-04 |       1.82e-04 |         0.0011 |
| std        |         0.1607 |         0.1612 |         0.0139 |         0.0862 |
| min        |        -8.2957 |        -8.2790 |        -0.8799 |        -5.4744 |
| 25%        |        -0.0405 |        -0.0407 |      -2.45e-04 |        -0.0015 |
| 50%        |         0.0069 |         0.0068 |      -3.53e-10 |      -2.20e-09 |
| 75%        |         0.0526 |         0.0526 |       3.53e-05 |       2.20e-04 |
| max        |         2.8119 |         2.8119 |         0.8710 |         5.4185 |

**Regression Analysis** (Python ~ Stata):

- **Model**: python = 0.0002 + 0.9990 * stata
- **R-squared**: 0.9926
- **N observations**: 2,553,227

| Coefficient |     Estimate |    Std Error | t-statistic |   p-value |
|-------------|--------------|--------------|-------------|----------|
| Intercept   |     1.83e-04 |     8.67e-06 |     21.0518 |     0.000 |
| Slope       |       0.9990 |     5.39e-05 |  18520.6724 |     0.000 |

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

**Precision2**: 99th percentile diff = 9.90e-08 (tolerance: < 1.00e+00)

**Summary Statistics** (Common Observations):

| Statistic  |          Stata |         Python |     Difference | Std Difference |
|------------|----------------|----------------|----------------|----------------|
| count      |       3.26e+06 |       3.26e+06 |       3.26e+06 |       3.26e+06 |
| mean       |        -0.0314 |        -0.0314 |       2.54e-06 |       1.81e-05 |
| std        |         0.1407 |         0.1406 |         0.0011 |         0.0077 |
| min        |       -24.3138 |       -24.3138 |        -0.0315 |        -0.2238 |
| 25%        |        -0.0723 |        -0.0723 |      -9.66e-10 |      -6.87e-09 |
| 50%        |        -0.0291 |        -0.0291 |       6.22e-13 |       4.42e-12 |
| 75%        |         0.0117 |         0.0117 |       9.77e-10 |       6.94e-09 |
| max        |         8.1853 |         8.1853 |         0.5525 |         3.9279 |

**Regression Analysis** (Python ~ Stata):

- **Model**: python = -0.0000 + 0.9995 * stata
- **R-squared**: 0.9999
- **N observations**: 3,259,701

| Coefficient |     Estimate |    Std Error | t-statistic |   p-value |
|-------------|--------------|--------------|-------------|----------|
| Intercept   |    -1.39e-05 |     6.13e-07 |    -22.6618 |     0.000 |
| Slope       |       0.9995 |     4.26e-06 | 234800.3460 |     0.000 |

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

**Precision2**: 99th percentile diff = 0.00e+00 (tolerance: < 1.00e+00)

**Summary Statistics** (Common Observations):

| Statistic  |          Stata |         Python |     Difference | Std Difference |
|------------|----------------|----------------|----------------|----------------|
| count      |    220066.0000 |    220066.0000 |    220066.0000 |    220066.0000 |
| mean       |         0.4843 |         0.4843 |         0.0000 |         0.0000 |
| std        |         0.4998 |         0.4998 |         0.0000 |         0.0000 |
| min        |         0.0000 |         0.0000 |         0.0000 |         0.0000 |
| 25%        |         0.0000 |         0.0000 |         0.0000 |         0.0000 |
| 50%        |         0.0000 |         0.0000 |         0.0000 |         0.0000 |
| 75%        |         1.0000 |         1.0000 |         0.0000 |         0.0000 |
| max        |         1.0000 |         1.0000 |         0.0000 |         0.0000 |

**Regression Analysis** (Python ~ Stata):

- **Model**: python = 0.0000 + 1.0000 * stata
- **R-squared**: 1.0000
- **N observations**: 220,066

| Coefficient |     Estimate |    Std Error | t-statistic |   p-value |
|-------------|--------------|--------------|-------------|----------|
| Intercept   |     2.22e-13 |     7.47e-16 |    297.5158 |     0.000 |
| Slope       |       1.0000 |     1.07e-15 |    9.32e+14 |     0.000 |

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
- Python: 234,173
- Common: 108,270

**Precision1**: 0.000% obs with std_diff >= 1.00e-02 (tolerance: < 10%)

**Precision2**: 99th percentile diff = 0.00e+00 (tolerance: < 1.00e+00)

**Summary Statistics** (Common Observations):

| Statistic  |          Stata |         Python |     Difference | Std Difference |
|------------|----------------|----------------|----------------|----------------|
| count      |    108270.0000 |    108270.0000 |    108270.0000 |    108270.0000 |
| mean       |        14.8879 |        14.8879 |         0.0000 |         0.0000 |
| std        |         2.7236 |         2.7236 |         0.0000 |         0.0000 |
| min        |         6.0000 |         6.0000 |         0.0000 |         0.0000 |
| 25%        |        13.0000 |        13.0000 |         0.0000 |         0.0000 |
| 50%        |        15.0000 |        15.0000 |         0.0000 |         0.0000 |
| 75%        |        17.0000 |        17.0000 |         0.0000 |         0.0000 |
| max        |        23.0000 |        23.0000 |         0.0000 |         0.0000 |

**Regression Analysis** (Python ~ Stata):

- **Model**: python = -0.0000 + 1.0000 * stata
- **R-squared**: 1.0000
- **N observations**: 108,270

| Coefficient |     Estimate |    Std Error | t-statistic |   p-value |
|-------------|--------------|--------------|-------------|----------|
| Intercept   |    -1.24e-12 |     4.43e-15 |   -279.4851 |     0.000 |
| Slope       |       1.0000 |     2.93e-16 |    3.42e+15 |     0.000 |

**Feedback**:
- Num observations with std_diff >= TOL_DIFF_1: 0/108270 (0.000%)
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

**Precision2**: 99th percentile diff = 1.58e-07 (tolerance: < 1.00e+00)

**Summary Statistics** (Common Observations):

| Statistic  |          Stata |         Python |     Difference | Std Difference |
|------------|----------------|----------------|----------------|----------------|
| count      |     30170.0000 |     30170.0000 |     30170.0000 |     30170.0000 |
| mean       |         9.2631 |         9.2631 |      -9.04e-09 |      -7.15e-10 |
| std        |        12.6421 |        12.6421 |       3.44e-07 |       2.72e-08 |
| min        |         0.0000 |         0.0000 |      -4.00e-06 |      -3.16e-07 |
| 25%        |         0.0000 |         0.0000 |         0.0000 |         0.0000 |
| 50%        |         7.4388 |         7.4388 |         0.0000 |         0.0000 |
| 75%        |        10.7284 |        10.7284 |         0.0000 |         0.0000 |
| max        |       221.2826 |       221.2826 |       4.00e-06 |       3.16e-07 |

**Regression Analysis** (Python ~ Stata):

- **Model**: python = 0.0000 + 1.0000 * stata
- **R-squared**: 1.0000
- **N observations**: 30,170

| Coefficient |     Estimate |    Std Error | t-statistic |   p-value |
|-------------|--------------|--------------|-------------|----------|
| Intercept   |     2.30e-08 |     2.44e-09 |      9.4380 |     0.000 |
| Slope       |       1.0000 |     1.56e-10 |    6.43e+09 |     0.000 |

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

**Precision2**: 99th percentile diff = 5.90e-08 (tolerance: < 1.00e+00)

**Summary Statistics** (Common Observations):

| Statistic  |          Stata |         Python |     Difference | Std Difference |
|------------|----------------|----------------|----------------|----------------|
| count      |       1.05e+06 |       1.05e+06 |       1.05e+06 |       1.05e+06 |
| mean       |         0.0758 |         0.0758 |       3.19e-13 |       8.57e-13 |
| std        |         0.3727 |         0.3727 |       1.05e-08 |       2.81e-08 |
| min        |       8.40e-07 |       8.40e-07 |      -1.30e-06 |      -3.49e-06 |
| 25%        |         0.0049 |         0.0049 |      -2.80e-10 |      -7.51e-10 |
| 50%        |         0.0161 |         0.0161 |       1.00e-13 |       2.69e-13 |
| 75%        |         0.0556 |         0.0556 |       2.81e-10 |       7.55e-10 |
| max        |        94.1189 |        94.1189 |       3.84e-06 |       1.03e-05 |

**Regression Analysis** (Python ~ Stata):

- **Model**: python = -0.0000 + 1.0000 * stata
- **R-squared**: 1.0000
- **N observations**: 1,049,030

| Coefficient |     Estimate |    Std Error | t-statistic |   p-value |
|-------------|--------------|--------------|-------------|----------|
| Intercept   |    -3.24e-11 |     1.04e-11 |     -3.1050 |     0.002 |
| Slope       |       1.0000 |     2.74e-11 |    3.65e+10 |     0.000 |

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

**Precision2**: 99th percentile diff = 1.96e-08 (tolerance: < 1.00e+00)

**Summary Statistics** (Common Observations):

| Statistic  |          Stata |         Python |     Difference | Std Difference |
|------------|----------------|----------------|----------------|----------------|
| count      |       1.92e+06 |       1.92e+06 |       1.92e+06 |       1.92e+06 |
| mean       |         1.0111 |         1.0111 |       3.70e-05 |       7.66e-06 |
| std        |         4.8381 |         4.8380 |         0.0550 |         0.0114 |
| min        |     -1046.0000 |     -1046.0000 |       -22.2222 |        -4.5932 |
| 25%        |         0.9915 |         0.9915 |      -5.38e-09 |      -1.11e-09 |
| 50%        |         1.0000 |         1.0000 |         0.0000 |         0.0000 |
| 75%        |         1.0068 |         1.0068 |       1.43e-09 |       2.95e-10 |
| max        |      5783.5542 |      5783.5544 |        54.4133 |        11.2469 |

**Regression Analysis** (Python ~ Stata):

- **Model**: python = 0.0001 + 0.9999 * stata
- **R-squared**: 0.9999
- **N observations**: 1,917,427

| Coefficient |     Estimate |    Std Error | t-statistic |   p-value |
|-------------|--------------|--------------|-------------|----------|
| Intercept   |     1.20e-04 |     4.06e-05 |      2.9512 |     0.003 |
| Slope       |       0.9999 |     8.21e-06 | 121756.8500 |     0.000 |

**Feedback**:
- Num observations with std_diff >= TOL_DIFF_1: 738/1917427 (0.038%)
- Stata standard deviation: 4.84e+00

---

### AnalystValue

**Status**: ✅ PASSED

**Test Results**:
- Test 1 - Column names: ✅ PASSED
- Test 2 - Superset check: ✅ PASSED
- Test 3 - Precision1 check: ✅ PASSED
- Test 4 - Precision2 check: ✅ PASSED

**Columns**: ['AnalystValue']

**Observations**:
- Stata:  1,244,664
- Python: 1,299,504
- Common: 1,241,880

**Precision1**: 0.263% obs with std_diff >= 1.00e-02 (tolerance: < 10%)

**Precision2**: 99th percentile diff = 1.74e-03 (tolerance: < 1.00e+00)

**Summary Statistics** (Common Observations):

| Statistic  |          Stata |         Python |     Difference | Std Difference |
|------------|----------------|----------------|----------------|----------------|
| count      |       1.24e+06 |       1.24e+06 |       1.24e+06 |       1.24e+06 |
| mean       |         0.7787 |         0.7792 |       5.50e-04 |       5.24e-05 |
| std        |        10.4895 |        10.4536 |         0.0510 |         0.0049 |
| min        |       -45.8197 |       -45.8197 |       -11.7195 |        -1.1173 |
| 25%        |         0.4419 |         0.4418 |      -4.09e-08 |      -3.90e-09 |
| 50%        |         0.6860 |         0.6861 |      -1.25e-08 |      -1.19e-09 |
| 75%        |         0.9878 |         0.9881 |       8.97e-09 |       8.55e-10 |
| max        |      3338.2976 |      3326.5781 |         5.3913 |         0.5140 |

**Regression Analysis** (Python ~ Stata):

- **Model**: python = 0.0032 + 0.9966 * stata
- **R-squared**: 1.0000
- **N observations**: 1,241,880

| Coefficient |     Estimate |    Std Error | t-statistic |   p-value |
|-------------|--------------|--------------|-------------|----------|
| Intercept   |       0.0032 |     3.26e-05 |     98.8219 |     0.000 |
| Slope       |       0.9966 |     3.10e-06 | 321904.8846 |     0.000 |

**Feedback**:
- Num observations with std_diff >= TOL_DIFF_1: 3264/1241880 (0.263%)
- Stata standard deviation: 1.05e+01

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

**Precision2**: 99th percentile diff = 1.90e-07 (tolerance: < 1.00e+00)

**Summary Statistics** (Common Observations):

| Statistic  |          Stata |         Python |     Difference | Std Difference |
|------------|----------------|----------------|----------------|----------------|
| count      |       2.92e+06 |       2.92e+06 |       2.92e+06 |       2.92e+06 |
| mean       |         0.0024 |         0.0024 |      -4.50e-08 |      -4.38e-07 |
| std        |         0.1028 |         0.1028 |       6.48e-04 |         0.0063 |
| min        |        -1.6087 |        -1.6087 |        -0.2585 |        -2.5156 |
| 25%        |        -0.0382 |        -0.0382 |      -1.09e-09 |      -1.06e-08 |
| 50%        |         0.0000 |         0.0000 |         0.0000 |         0.0000 |
| 75%        |         0.0394 |         0.0394 |       1.08e-09 |       1.05e-08 |
| max        |         9.4535 |         9.4535 |         0.3185 |         3.0989 |

**Regression Analysis** (Python ~ Stata):

- **Model**: python = -0.0000 + 1.0000 * stata
- **R-squared**: 1.0000
- **N observations**: 2,922,290

| Coefficient |     Estimate |    Std Error | t-statistic |   p-value |
|-------------|--------------|--------------|-------------|----------|
| Intercept   |    -9.65e-09 |     3.79e-07 |     -0.0254 |     0.980 |
| Slope       |       1.0000 |     3.69e-06 | 270982.0585 |     0.000 |

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

**Precision2**: 99th percentile diff = 3.59e-08 (tolerance: < 1.00e+00)

**Summary Statistics** (Common Observations):

| Statistic  |          Stata |         Python |     Difference | Std Difference |
|------------|----------------|----------------|----------------|----------------|
| count      |       3.30e+06 |       3.30e+06 |       3.30e+06 |       3.30e+06 |
| mean       |         0.1700 |         0.1700 |       4.10e-08 |       2.17e-08 |
| std        |         1.8876 |         1.8876 |       2.77e-04 |       1.47e-04 |
| min        |        -1.0000 |        -1.0000 |        -0.0968 |        -0.0513 |
| 25%        |        -0.0280 |        -0.0280 |      -2.07e-09 |      -1.10e-09 |
| 50%        |         0.0638 |         0.0638 |      -8.16e-13 |      -4.32e-13 |
| 75%        |         0.1864 |         0.1864 |       2.04e-09 |       1.08e-09 |
| max        |       679.3918 |       679.3918 |         0.1080 |         0.0572 |

**Regression Analysis** (Python ~ Stata):

- **Model**: python = 0.0000 + 1.0000 * stata
- **R-squared**: 1.0000
- **N observations**: 3,295,125

| Coefficient |     Estimate |    Std Error | t-statistic |   p-value |
|-------------|--------------|--------------|-------------|----------|
| Intercept   |     3.88e-08 |     1.53e-07 |      0.2530 |     0.800 |
| Slope       |       1.0000 |     8.08e-08 |    1.24e+07 |     0.000 |

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

**Precision2**: 99th percentile diff = 1.28e-07 (tolerance: < 1.00e+00)

**Summary Statistics** (Common Observations):

| Statistic  |          Stata |         Python |     Difference | Std Difference |
|------------|----------------|----------------|----------------|----------------|
| count      |       2.72e+06 |       2.72e+06 |       2.72e+06 |       2.72e+06 |
| mean       |        -0.7346 |        -0.7346 |       3.61e-05 |       3.45e-05 |
| std        |         1.0457 |         1.0457 |         0.0164 |         0.0156 |
| min        |       -10.1310 |       -10.1310 |        -3.5093 |        -3.3559 |
| 25%        |        -1.2856 |        -1.2856 |      -1.19e-08 |      -1.14e-08 |
| 50%        |        -0.6000 |        -0.6000 |      -2.61e-12 |      -2.50e-12 |
| 75%        |        -0.0485 |        -0.0485 |       1.18e-08 |       1.13e-08 |
| max        |         6.8214 |         6.8214 |         3.6885 |         3.5273 |

**Regression Analysis** (Python ~ Stata):

- **Model**: python = -0.0000 + 0.9999 * stata
- **R-squared**: 0.9998
- **N observations**: 2,715,090

| Coefficient |     Estimate |    Std Error | t-statistic |   p-value |
|-------------|--------------|--------------|-------------|----------|
| Intercept   |    -3.94e-05 |     1.21e-05 |     -3.2484 |     0.001 |
| Slope       |       0.9999 |     9.50e-06 | 105295.5450 |     0.000 |

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

**Precision2**: 99th percentile diff = 1.81e-08 (tolerance: < 1.00e+00)

**Summary Statistics** (Common Observations):

| Statistic  |          Stata |         Python |     Difference | Std Difference |
|------------|----------------|----------------|----------------|----------------|
| count      |       3.00e+06 |       3.00e+06 |       3.00e+06 |       3.00e+06 |
| mean       |         2.9269 |         2.9269 |      -2.83e-07 |      -5.41e-09 |
| std        |        52.4336 |        52.4336 |       1.87e-04 |       3.56e-06 |
| min        |     -4881.0220 |     -4881.0222 |        -0.1222 |        -0.0023 |
| 25%        |         0.3604 |         0.3604 |      -2.03e-08 |      -3.88e-10 |
| 50%        |         0.6804 |         0.6804 |         0.0000 |         0.0000 |
| 75%        |         1.1675 |         1.1675 |       2.03e-08 |       3.88e-10 |
| max        |     13961.4660 |     13961.4667 |       6.67e-04 |       1.27e-05 |

**Regression Analysis** (Python ~ Stata):

- **Model**: python = -0.0000 + 1.0000 * stata
- **R-squared**: 1.0000
- **N observations**: 2,996,716

| Coefficient |     Estimate |    Std Error | t-statistic |   p-value |
|-------------|--------------|--------------|-------------|----------|
| Intercept   |    -2.92e-07 |     1.08e-07 |     -2.7020 |     0.007 |
| Slope       |       1.0000 |     2.06e-09 |    4.86e+08 |     0.000 |

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

**Precision2**: 99th percentile diff = 2.18e-08 (tolerance: < 1.00e+00)

**Summary Statistics** (Common Observations):

| Statistic  |          Stata |         Python |     Difference | Std Difference |
|------------|----------------|----------------|----------------|----------------|
| count      |       2.92e+06 |       2.92e+06 |       2.92e+06 |       2.92e+06 |
| mean       |         0.0397 |         0.0400 |       3.11e-04 |       9.26e-07 |
| std        |       335.4250 |       333.8920 |         2.9995 |         0.0089 |
| min        |   -471732.0600 |   -467702.6380 |     -3149.6733 |        -9.3901 |
| 25%        |        -0.0674 |        -0.0674 |      -1.74e-08 |      -5.18e-11 |
| 50%        |         0.0164 |         0.0164 |         0.0000 |         0.0000 |
| 75%        |         0.2348 |         0.2348 |       1.73e-08 |       5.17e-11 |
| max        |    121033.5200 |    121033.5167 |      4029.4220 |        12.0129 |

**Regression Analysis** (Python ~ Stata):

- **Model**: python = 0.0005 + 0.9954 * stata
- **R-squared**: 0.9999
- **N observations**: 2,924,820

| Coefficient |     Estimate |    Std Error | t-statistic |   p-value |
|-------------|--------------|--------------|-------------|----------|
| Intercept   |     4.93e-04 |       0.0015 |      0.3278 |     0.743 |
| Slope       |       0.9954 |     4.48e-06 | 221984.3294 |     0.000 |

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

**Precision2**: 99th percentile diff = 9.82e-08 (tolerance: < 1.00e+00)

**Summary Statistics** (Common Observations):

| Statistic  |          Stata |         Python |     Difference | Std Difference |
|------------|----------------|----------------|----------------|----------------|
| count      |       4.29e+06 |       4.29e+06 |       4.29e+06 |       4.29e+06 |
| mean       |         0.9893 |         0.9893 |       1.97e-09 |       2.64e-09 |
| std        |         0.7459 |         0.7459 |       2.18e-08 |       2.92e-08 |
| min        |       -17.8663 |       -17.8663 |      -1.20e-06 |      -1.61e-06 |
| 25%        |         0.5301 |         0.5301 |      -7.41e-09 |      -9.93e-09 |
| 50%        |         0.8981 |         0.8981 |       7.08e-10 |       9.49e-10 |
| 75%        |         1.3300 |         1.3300 |       1.02e-08 |       1.37e-08 |
| max        |        52.6339 |        52.6339 |       2.25e-06 |       3.01e-06 |

**Regression Analysis** (Python ~ Stata):

- **Model**: python = -0.0000 + 1.0000 * stata
- **R-squared**: 1.0000
- **N observations**: 4,285,574

| Coefficient |     Estimate |    Std Error | t-statistic |   p-value |
|-------------|--------------|--------------|-------------|----------|
| Intercept   |    -1.53e-09 |     1.74e-11 |    -87.9658 |     0.000 |
| Slope       |       1.0000 |     1.40e-11 |    7.13e+10 |     0.000 |

**Feedback**:
- Num observations with std_diff >= TOL_DIFF_1: 0/4285574 (0.000%)
- Stata standard deviation: 7.46e-01

---

### BetaFP

**Status**: ✅ PASSED

**Test Results**:
- Test 1 - Column names: ✅ PASSED
- Test 2 - Superset check: ✅ PASSED
- Test 3 - Precision1 check: ✅ PASSED
- Test 4 - Precision2 check: ✅ PASSED

**Columns**: ['BetaFP']

**Observations**:
- Stata:  3,794,018
- Python: 3,779,957
- Common: 3,773,530

**Precision1**: 5.980% obs with std_diff >= 1.00e-02 (tolerance: < 10%)

**Precision2**: 99th percentile diff = 8.93e-02 (tolerance: < 1.00e+00)

**Summary Statistics** (Common Observations):

| Statistic  |          Stata |         Python |     Difference | Std Difference |
|------------|----------------|----------------|----------------|----------------|
| count      |       3.77e+06 |       3.77e+06 |       3.77e+06 |       3.77e+06 |
| mean       |         0.9816 |         0.9803 |        -0.0013 |        -0.0020 |
| std        |         0.6411 |         0.6407 |         0.0286 |         0.0446 |
| min        |       7.25e-07 |         0.0000 |        -3.9823 |        -6.2114 |
| 25%        |         0.5206 |         0.5196 |        -0.0018 |        -0.0028 |
| 50%        |         0.8971 |         0.8960 |        -0.0010 |        -0.0016 |
| 75%        |         1.3181 |         1.3166 |      -4.96e-04 |      -7.74e-04 |
| max        |        12.6047 |        12.5623 |         4.7939 |         7.4774 |

**Regression Analysis** (Python ~ Stata):

- **Model**: python = 0.0004 + 0.9983 * stata
- **R-squared**: 0.9980
- **N observations**: 3,773,524

| Coefficient |     Estimate |    Std Error | t-statistic |   p-value |
|-------------|--------------|--------------|-------------|----------|
| Intercept   |     3.83e-04 |     2.69e-05 |     14.2406 |     0.000 |
| Slope       |       0.9983 |     2.30e-05 |  43476.8035 |     0.000 |

**Feedback**:
- Num observations with std_diff >= TOL_DIFF_1: 225656/3773530 (5.980%)
- Stata standard deviation: 6.41e-01

---

### BetaLiquidityPS

**Status**: ✅ PASSED

**Test Results**:
- Test 1 - Column names: ✅ PASSED
- Test 2 - Superset check: ✅ PASSED
- Test 3 - Precision1 check: ✅ PASSED
- Test 4 - Precision2 check: ✅ PASSED

**Columns**: ['BetaLiquidityPS']

**Observations**:
- Stata:  3,423,856
- Python: 3,479,410
- Common: 3,423,856

**Precision1**: 0.309% obs with std_diff >= 1.00e-02 (tolerance: < 10%)

**Precision2**: 99th percentile diff = 5.31e-03 (tolerance: < 1.00e+00)

**Summary Statistics** (Common Observations):

| Statistic  |          Stata |         Python |     Difference | Std Difference |
|------------|----------------|----------------|----------------|----------------|
| count      |       3.42e+06 |       3.42e+06 |       3.42e+06 |       3.42e+06 |
| mean       |        -0.0013 |        -0.0013 |       7.64e-05 |       1.69e-04 |
| std        |         0.4525 |         0.4524 |       5.64e-04 |         0.0012 |
| min        |       -23.6664 |       -23.6664 |        -0.0357 |        -0.0789 |
| 25%        |        -0.1738 |        -0.1738 |      -6.41e-09 |      -1.42e-08 |
| 50%        |       8.48e-04 |       8.97e-04 |       3.96e-10 |       8.75e-10 |
| 75%        |         0.1792 |         0.1792 |       8.25e-09 |       1.82e-08 |
| max        |        41.3486 |        41.3530 |         0.0466 |         0.1029 |

**Regression Analysis** (Python ~ Stata):

- **Model**: python = 0.0001 + 0.9999 * stata
- **R-squared**: 1.0000
- **N observations**: 3,423,856

| Coefficient |     Estimate |    Std Error | t-statistic |   p-value |
|-------------|--------------|--------------|-------------|----------|
| Intercept   |     7.64e-05 |     3.04e-07 |    250.7688 |     0.000 |
| Slope       |       0.9999 |     6.73e-07 |    1.49e+06 |     0.000 |

**Feedback**:
- Num observations with std_diff >= TOL_DIFF_1: 10596/3423856 (0.309%)
- Stata standard deviation: 4.52e-01

---

### BetaTailRisk

**Status**: ✅ PASSED

**Test Results**:
- Test 1 - Column names: ✅ PASSED
- Test 2 - Superset check: ✅ PASSED
- Test 3 - Precision1 check: ✅ PASSED
- Test 4 - Precision2 check: ✅ PASSED

**Columns**: ['BetaTailRisk']

**Observations**:
- Stata:  2,292,350
- Python: 2,332,084
- Common: 2,292,350

**Precision1**: 4.149% obs with std_diff >= 1.00e-02 (tolerance: < 10%)

**Precision2**: 99th percentile diff = 1.97e-02 (tolerance: < 1.00e+00)

**Summary Statistics** (Common Observations):

| Statistic  |          Stata |         Python |     Difference | Std Difference |
|------------|----------------|----------------|----------------|----------------|
| count      |       2.29e+06 |       2.29e+06 |       2.29e+06 |       2.29e+06 |
| mean       |         0.6390 |         0.6390 |      -3.78e-05 |      -7.39e-05 |
| std        |         0.5111 |         0.5109 |         0.0026 |         0.0052 |
| min        |       -10.7373 |       -10.7080 |        -0.0878 |        -0.1719 |
| 25%        |         0.3065 |         0.3066 |      -8.98e-04 |        -0.0018 |
| 50%        |         0.5661 |         0.5661 |      -1.37e-04 |      -2.69e-04 |
| 75%        |         0.8925 |         0.8923 |       4.95e-04 |       9.69e-04 |
| max        |         8.5702 |         8.5711 |         0.1976 |         0.3866 |

**Regression Analysis** (Python ~ Stata):

- **Model**: python = 0.0002 + 0.9996 * stata
- **R-squared**: 1.0000
- **N observations**: 2,292,350

| Coefficient |     Estimate |    Std Error | t-statistic |   p-value |
|-------------|--------------|--------------|-------------|----------|
| Intercept   |     1.99e-04 |     2.78e-06 |     71.7608 |     0.000 |
| Slope       |       0.9996 |     3.39e-06 | 294509.4351 |     0.000 |

**Feedback**:
- Num observations with std_diff >= TOL_DIFF_1: 95107/2292350 (4.149%)
- Stata standard deviation: 5.11e-01

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

**Precision2**: 99th percentile diff = 6.45e-08 (tolerance: < 1.00e+00)

**Summary Statistics** (Common Observations):

| Statistic  |          Stata |         Python |     Difference | Std Difference |
|------------|----------------|----------------|----------------|----------------|
| count      |       4.48e+06 |       4.48e+06 |       4.48e+06 |       4.48e+06 |
| mean       |         0.0164 |         0.0164 |       2.17e-13 |       7.01e-12 |
| std        |         0.0310 |         0.0310 |       5.81e-10 |       1.87e-08 |
| min        |         0.0000 |         0.0000 |      -1.00e-07 |      -3.22e-06 |
| 25%        |         0.0046 |         0.0046 |         0.0000 |         0.0000 |
| 50%        |         0.0086 |         0.0086 |         0.0000 |         0.0000 |
| 75%        |         0.0174 |         0.0174 |         0.0000 |         0.0000 |
| max        |         1.5145 |         1.5145 |       3.00e-08 |       9.67e-07 |

**Regression Analysis** (Python ~ Stata):

- **Model**: python = 0.0000 + 1.0000 * stata
- **R-squared**: 1.0000
- **N observations**: 4,481,622

| Coefficient |     Estimate |    Std Error | t-statistic |   p-value |
|-------------|--------------|--------------|-------------|----------|
| Intercept   |     5.46e-14 |     3.11e-13 |      0.1758 |     0.860 |
| Slope       |       1.0000 |     8.85e-12 |    1.13e+11 |     0.000 |

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

**Precision2**: 99th percentile diff = 7.69e-09 (tolerance: < 1.00e+00)

**Summary Statistics** (Common Observations):

| Statistic  |          Stata |         Python |     Difference | Std Difference |
|------------|----------------|----------------|----------------|----------------|
| count      |       3.61e+06 |       3.61e+06 |       3.61e+06 |       3.61e+06 |
| mean       |         4.0992 |         4.0992 |      -1.12e-05 |      -5.55e-08 |
| std        |       201.7771 |       201.7765 |         0.0027 |       1.33e-05 |
| min        |    -11894.4540 |    -11894.3333 |        -0.9911 |        -0.0049 |
| 25%        |         1.4322 |         1.4322 |      -6.10e-08 |      -3.02e-10 |
| 50%        |         2.0021 |         2.0021 |         0.0000 |         0.0000 |
| 75%        |         3.1980 |         3.1980 |       6.11e-08 |       3.03e-10 |
| max        |     87702.4920 |     87702.5000 |         0.1436 |       7.12e-04 |

**Regression Analysis** (Python ~ Stata):

- **Model**: python = 0.0000 + 1.0000 * stata
- **R-squared**: 1.0000
- **N observations**: 3,606,159

| Coefficient |     Estimate |    Std Error | t-statistic |   p-value |
|-------------|--------------|--------------|-------------|----------|
| Intercept   |     1.97e-06 |     1.37e-06 |      1.4436 |     0.149 |
| Slope       |       1.0000 |     6.78e-09 |    1.48e+08 |     0.000 |

**Feedback**:
- Num observations with std_diff >= TOL_DIFF_1: 0/3606159 (0.000%)
- Stata standard deviation: 2.02e+02

---

### BrandInvest

**Status**: ✅ PASSED

**Test Results**:
- Test 1 - Column names: ✅ PASSED
- Test 2 - Superset check: ✅ PASSED
- Test 3 - Precision1 check: ✅ PASSED
- Test 4 - Precision2 check: ✅ PASSED

**Columns**: ['BrandInvest']

**Observations**:
- Stata:  485,304
- Python: 509,472
- Common: 485,304

**Precision1**: 0.000% obs with std_diff >= 1.00e-02 (tolerance: < 10%)

**Precision2**: 99th percentile diff = 2.54e-08 (tolerance: < 1.00e+00)

**Summary Statistics** (Common Observations):

| Statistic  |          Stata |         Python |     Difference | Std Difference |
|------------|----------------|----------------|----------------|----------------|
| count      |    485304.0000 |    485304.0000 |    485304.0000 |    485304.0000 |
| mean       |      2683.0685 |      2683.0702 |         0.0017 |       2.50e-08 |
| std        |     69010.0576 |     69010.0599 |         0.3446 |       4.99e-06 |
| min        |      -142.1329 |      -142.1329 |        -0.0201 |      -2.91e-07 |
| 25%        |        20.6215 |        20.6277 |      -3.45e-06 |      -5.01e-11 |
| 50%        |       127.2031 |       127.2031 |         0.0000 |         0.0000 |
| 75%        |       774.2914 |       774.2913 |       3.78e-06 |       5.47e-11 |
| max        |       1.36e+07 |       1.36e+07 |        69.2994 |         0.0010 |

**Regression Analysis** (Python ~ Stata):

- **Model**: python = 0.0016 + 1.0000 * stata
- **R-squared**: 1.0000
- **N observations**: 485,304

| Coefficient |     Estimate |    Std Error | t-statistic |   p-value |
|-------------|--------------|--------------|-------------|----------|
| Intercept   |       0.0016 |     4.95e-04 |      3.3014 |     0.001 |
| Slope       |       1.0000 |     7.17e-09 |    1.40e+08 |     0.000 |

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

**Precision2**: 99th percentile diff = 1.33e-07 (tolerance: < 1.00e+00)

**Summary Statistics** (Common Observations):

| Statistic  |          Stata |         Python |     Difference | Std Difference |
|------------|----------------|----------------|----------------|----------------|
| count      |       2.28e+06 |       2.28e+06 |       2.28e+06 |       2.28e+06 |
| mean       |         0.0904 |         0.0904 |       8.60e-08 |       3.91e-07 |
| std        |         0.2200 |         0.2200 |       1.41e-04 |       6.41e-04 |
| min        |       -11.3370 |       -11.3370 |        -0.0428 |        -0.1946 |
| 25%        |         0.0313 |         0.0313 |      -3.14e-09 |      -1.43e-08 |
| 50%        |         0.1154 |         0.1154 |       4.39e-12 |       2.00e-11 |
| 75%        |         0.1888 |         0.1888 |       3.20e-09 |       1.45e-08 |
| max        |        21.0025 |        21.0025 |         0.0316 |         0.1437 |

**Regression Analysis** (Python ~ Stata):

- **Model**: python = 0.0000 + 1.0000 * stata
- **R-squared**: 1.0000
- **N observations**: 2,283,861

| Coefficient |     Estimate |    Std Error | t-statistic |   p-value |
|-------------|--------------|--------------|-------------|----------|
| Intercept   |     1.14e-07 |     1.01e-07 |      1.1286 |     0.259 |
| Slope       |       1.0000 |     4.24e-07 |    2.36e+06 |     0.000 |

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

**Precision2**: 99th percentile diff = 2.53e-08 (tolerance: < 1.00e+00)

**Summary Statistics** (Common Observations):

| Statistic  |          Stata |         Python |     Difference | Std Difference |
|------------|----------------|----------------|----------------|----------------|
| count      |       3.04e+06 |       3.04e+06 |       3.04e+06 |       3.04e+06 |
| mean       |        -0.0077 |        -0.0077 |       8.06e-08 |       2.92e-08 |
| std        |         2.7569 |         2.7569 |       3.37e-04 |       1.22e-04 |
| min        |     -2140.1667 |     -2140.1666 |        -0.2334 |        -0.0847 |
| 25%        |         0.0214 |         0.0214 |      -1.99e-09 |      -7.22e-10 |
| 50%        |         0.0794 |         0.0794 |       4.07e-19 |       1.47e-19 |
| 75%        |         0.1498 |         0.1498 |       1.99e-09 |       7.22e-10 |
| max        |       221.9462 |       221.9462 |         0.1304 |         0.0473 |

**Regression Analysis** (Python ~ Stata):

- **Model**: python = 0.0000 + 1.0000 * stata
- **R-squared**: 1.0000
- **N observations**: 3,038,206

| Coefficient |     Estimate |    Std Error | t-statistic |   p-value |
|-------------|--------------|--------------|-------------|----------|
| Intercept   |     8.08e-08 |     1.94e-07 |      0.4176 |     0.676 |
| Slope       |       1.0000 |     7.02e-08 |    1.42e+07 |     0.000 |

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

**Precision2**: 99th percentile diff = 7.31e-08 (tolerance: < 1.00e+00)

**Summary Statistics** (Common Observations):

| Statistic  |          Stata |         Python |     Difference | Std Difference |
|------------|----------------|----------------|----------------|----------------|
| count      |    679061.0000 |    679061.0000 |    679061.0000 |    679061.0000 |
| mean       |         0.0131 |         0.0131 |       2.95e-06 |       5.39e-05 |
| std        |         0.0547 |         0.0547 |         0.0014 |         0.0247 |
| min        |        -3.8959 |        -3.8959 |        -0.1978 |        -3.6134 |
| 25%        |        -0.0038 |        -0.0038 |         0.0000 |         0.0000 |
| 50%        |         0.0059 |         0.0059 |         0.0000 |         0.0000 |
| 75%        |         0.0220 |         0.0220 |         0.0000 |         0.0000 |
| max        |         4.0661 |         4.0661 |         0.5306 |         9.6959 |

**Regression Analysis** (Python ~ Stata):

- **Model**: python = 0.0000 + 0.9998 * stata
- **R-squared**: 0.9994
- **N observations**: 679,061

| Coefficient |     Estimate |    Std Error | t-statistic |   p-value |
|-------------|--------------|--------------|-------------|----------|
| Intercept   |     5.87e-06 |     1.69e-06 |      3.4823 |     0.000 |
| Slope       |       0.9998 |     3.00e-05 |  33371.3419 |     0.000 |

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

**Precision2**: 99th percentile diff = 1.27e-07 (tolerance: < 1.00e+00)

**Summary Statistics** (Common Observations):

| Statistic  |          Stata |         Python |     Difference | Std Difference |
|------------|----------------|----------------|----------------|----------------|
| count      |       2.10e+06 |       2.10e+06 |       2.10e+06 |       2.10e+06 |
| mean       |         0.1672 |         0.1672 |      -4.03e-06 |      -1.88e-05 |
| std        |         0.2141 |         0.2141 |         0.0020 |         0.0092 |
| min        |        -0.1432 |        -0.1432 |        -0.4445 |        -2.0758 |
| 25%        |         0.0249 |         0.0249 |      -1.29e-09 |      -6.05e-09 |
| 50%        |         0.0754 |         0.0754 |         0.0000 |         0.0000 |
| 75%        |         0.2202 |         0.2202 |       1.29e-09 |       6.02e-09 |
| max        |         1.0000 |         1.0000 |         0.6778 |         3.1654 |

**Regression Analysis** (Python ~ Stata):

- **Model**: python = 0.0000 + 1.0000 * stata
- **R-squared**: 0.9999
- **N observations**: 2,096,350

| Coefficient |     Estimate |    Std Error | t-statistic |   p-value |
|-------------|--------------|--------------|-------------|----------|
| Intercept   |     2.39e-06 |     1.73e-06 |      1.3844 |     0.166 |
| Slope       |       1.0000 |     6.36e-06 | 157290.6074 |     0.000 |

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

**Precision2**: 99th percentile diff = 3.77e-09 (tolerance: < 1.00e+00)

**Summary Statistics** (Common Observations):

| Statistic  |          Stata |         Python |     Difference | Std Difference |
|------------|----------------|----------------|----------------|----------------|
| count      |       3.00e+06 |       3.00e+06 |       3.00e+06 |       3.00e+06 |
| mean       |       -12.6735 |       -12.6735 |       5.60e-07 |       1.47e-10 |
| std        |      3820.7124 |      3820.7124 |       3.17e-04 |       8.29e-08 |
| min        |   -921994.3800 |   -921994.3600 |        -0.0738 |      -1.93e-05 |
| 25%        |       -13.6941 |       -13.6941 |      -1.41e-07 |      -3.69e-11 |
| 50%        |        -2.1096 |        -2.1096 |         0.0000 |         0.0000 |
| 75%        |         3.5938 |         3.5938 |       1.41e-07 |       3.69e-11 |
| max        |       1.99e+06 |       1.99e+06 |         0.2004 |       5.25e-05 |

**Regression Analysis** (Python ~ Stata):

- **Model**: python = 0.0000 + 1.0000 * stata
- **R-squared**: 1.0000
- **N observations**: 3,002,825

| Coefficient |     Estimate |    Std Error | t-statistic |   p-value |
|-------------|--------------|--------------|-------------|----------|
| Intercept   |     5.30e-07 |     1.83e-07 |      2.9007 |     0.004 |
| Slope       |       1.0000 |     4.78e-11 |    2.09e+10 |     0.000 |

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

**Precision2**: 99th percentile diff = 4.27e-09 (tolerance: < 1.00e+00)

**Summary Statistics** (Common Observations):

| Statistic  |          Stata |         Python |     Difference | Std Difference |
|------------|----------------|----------------|----------------|----------------|
| count      |       2.50e+06 |       2.50e+06 |       2.50e+06 |       2.50e+06 |
| mean       |        -0.0575 |        -0.0576 |      -6.55e-05 |      -2.38e-07 |
| std        |       274.6743 |       274.6787 |         0.0281 |       1.02e-04 |
| min        |   -108816.4100 |   -108818.8964 |       -12.5408 |        -0.0457 |
| 25%        |        -0.1986 |        -0.1986 |      -4.59e-08 |      -1.67e-10 |
| 50%        |       4.34e-05 |       4.20e-05 |         0.0000 |         0.0000 |
| 75%        |         0.1868 |         0.1868 |       4.63e-08 |       1.69e-10 |
| max        |     39275.6840 |     39275.6489 |         0.6386 |         0.0023 |

**Regression Analysis** (Python ~ Stata):

- **Model**: python = -0.0001 + 1.0000 * stata
- **R-squared**: 1.0000
- **N observations**: 2,503,228

| Coefficient |     Estimate |    Std Error | t-statistic |   p-value |
|-------------|--------------|--------------|-------------|----------|
| Intercept   |    -6.46e-05 |     1.75e-05 |     -3.6829 |     0.000 |
| Slope       |       1.0000 |     6.38e-08 |    1.57e+07 |     0.000 |

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

**Precision2**: 99th percentile diff = 6.98e-09 (tolerance: < 1.00e+00)

**Summary Statistics** (Common Observations):

| Statistic  |          Stata |         Python |     Difference | Std Difference |
|------------|----------------|----------------|----------------|----------------|
| count      |       3.05e+06 |       3.05e+06 |       3.05e+06 |       3.05e+06 |
| mean       |         1.3348 |         1.3348 |      -4.36e-07 |      -2.46e-08 |
| std        |        17.7186 |        17.7186 |       4.16e-04 |       2.35e-05 |
| min        |       4.17e-05 |       4.17e-05 |        -0.1655 |        -0.0093 |
| 25%        |         0.9647 |         0.9647 |      -2.33e-08 |      -1.32e-09 |
| 50%        |         1.0716 |         1.0716 |         0.0000 |         0.0000 |
| 75%        |         1.1870 |         1.1870 |       2.33e-08 |       1.32e-09 |
| max        |      5799.5884 |      5799.5882 |         0.1144 |         0.0065 |

**Regression Analysis** (Python ~ Stata):

- **Model**: python = -0.0000 + 1.0000 * stata
- **R-squared**: 1.0000
- **N observations**: 3,047,458

| Coefficient |     Estimate |    Std Error | t-statistic |   p-value |
|-------------|--------------|--------------|-------------|----------|
| Intercept   |    -4.21e-07 |     2.39e-07 |     -1.7592 |     0.079 |
| Slope       |       1.0000 |     1.35e-08 |    7.43e+07 |     0.000 |

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

**Precision2**: 99th percentile diff = 0.00e+00 (tolerance: < 1.00e+00)

**Summary Statistics** (Common Observations):

| Statistic  |          Stata |         Python |     Difference | Std Difference |
|------------|----------------|----------------|----------------|----------------|
| count      |    628022.0000 |    628022.0000 |    628022.0000 |    628022.0000 |
| mean       |         0.4775 |         0.4774 |      -1.51e-04 |      -3.03e-04 |
| std        |         0.4995 |         0.4995 |         0.0343 |         0.0688 |
| min        |         0.0000 |         0.0000 |        -1.0000 |        -2.0020 |
| 25%        |         0.0000 |         0.0000 |         0.0000 |         0.0000 |
| 50%        |         0.0000 |         0.0000 |         0.0000 |         0.0000 |
| 75%        |         1.0000 |         1.0000 |         0.0000 |         0.0000 |
| max        |         1.0000 |         1.0000 |         1.0000 |         2.0020 |

**Regression Analysis** (Python ~ Stata):

- **Model**: python = 0.0010 + 0.9976 * stata
- **R-squared**: 0.9953
- **N observations**: 628,022

| Coefficient |     Estimate |    Std Error | t-statistic |   p-value |
|-------------|--------------|--------------|-------------|----------|
| Intercept   |     9.84e-04 |     5.99e-05 |     16.4257 |     0.000 |
| Slope       |       0.9976 |     8.67e-05 |  11503.3922 |     0.000 |

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

**Precision2**: 99th percentile diff = 1.30e-07 (tolerance: < 1.00e+00)

**Summary Statistics** (Common Observations):

| Statistic  |          Stata |         Python |     Difference | Std Difference |
|------------|----------------|----------------|----------------|----------------|
| count      |       3.30e+06 |       3.30e+06 |       3.30e+06 |       3.30e+06 |
| mean       |         0.0097 |         0.0097 |       1.04e-07 |       1.57e-06 |
| std        |         0.0664 |         0.0664 |       4.33e-05 |       6.53e-04 |
| min        |        -1.6890 |        -1.6890 |        -0.0024 |        -0.0357 |
| 25%        |        -0.0012 |        -0.0012 |      -1.12e-10 |      -1.69e-09 |
| 50%        |         0.0000 |         0.0000 |         0.0000 |         0.0000 |
| 75%        |         0.0174 |         0.0174 |       1.11e-10 |       1.67e-09 |
| max        |         1.7133 |         1.7133 |         0.0198 |         0.2984 |

**Regression Analysis** (Python ~ Stata):

- **Model**: python = 0.0000 + 1.0000 * stata
- **R-squared**: 1.0000
- **N observations**: 3,295,155

| Coefficient |     Estimate |    Std Error | t-statistic |   p-value |
|-------------|--------------|--------------|-------------|----------|
| Intercept   |     1.10e-07 |     2.41e-08 |      4.5668 |     0.000 |
| Slope       |       1.0000 |     3.59e-07 |    2.78e+06 |     0.000 |

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

**Precision2**: 99th percentile diff = 4.03e-20 (tolerance: < 1.00e+00)

**Summary Statistics** (Common Observations):

| Statistic  |          Stata |         Python |     Difference | Std Difference |
|------------|----------------|----------------|----------------|----------------|
| count      |       2.68e+06 |       2.68e+06 |       2.68e+06 |       2.68e+06 |
| mean       |     -1143.9086 |      -2.46e-05 |      1143.9086 |       1.99e-11 |
| std        |       5.76e+13 |       5.76e+13 |       2.33e+06 |       4.04e-08 |
| min        |      -7.94e+15 |      -7.94e+15 |      -1.74e+09 |      -3.02e-05 |
| 25%        |        -0.9389 |        -0.9388 |      -2.05e-08 |      -3.56e-22 |
| 50%        |        -0.3699 |        -0.3698 |       1.54e-11 |       2.67e-25 |
| 75%        |         0.1936 |         0.1936 |       2.07e-08 |       3.60e-22 |
| max        |       2.19e+16 |       2.19e+16 |       7.67e+08 |       1.33e-05 |

**Regression Analysis** (Python ~ Stata):

- **Model**: python = 1143.9039 + 1.0000 * stata
- **R-squared**: 1.0000
- **N observations**: 2,678,515

| Coefficient |     Estimate |    Std Error | t-statistic |   p-value |
|-------------|--------------|--------------|-------------|----------|
| Intercept   |    1143.9039 |    1401.5512 |      0.8162 |     0.414 |
| Slope       |       1.0000 |     2.44e-11 |    4.11e+10 |     0.000 |

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

**Precision2**: 99th percentile diff = 0.00e+00 (tolerance: < 1.00e+00)

**Summary Statistics** (Common Observations):

| Statistic  |          Stata |         Python |     Difference | Std Difference |
|------------|----------------|----------------|----------------|----------------|
| count      |    210756.0000 |    210756.0000 |    210756.0000 |    210756.0000 |
| mean       |         0.1489 |         0.1489 |      -1.90e-05 |      -5.33e-05 |
| std        |         0.3560 |         0.3560 |         0.0082 |         0.0229 |
| min        |         0.0000 |         0.0000 |        -1.0000 |        -2.8089 |
| 25%        |         0.0000 |         0.0000 |         0.0000 |         0.0000 |
| 50%        |         0.0000 |         0.0000 |         0.0000 |         0.0000 |
| 75%        |         0.0000 |         0.0000 |         0.0000 |         0.0000 |
| max        |         1.0000 |         1.0000 |         1.0000 |         2.8089 |

**Regression Analysis** (Python ~ Stata):

- **Model**: python = 0.0000 + 0.9997 * stata
- **R-squared**: 0.9995
- **N observations**: 210,756

| Coefficient |     Estimate |    Std Error | t-statistic |   p-value |
|-------------|--------------|--------------|-------------|----------|
| Intercept   |     2.79e-05 |     1.92e-05 |      1.4486 |     0.147 |
| Slope       |       0.9997 |     4.99e-05 |  20048.5212 |     0.000 |

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

**Precision2**: 99th percentile diff = 8.46e-08 (tolerance: < 1.00e+00)

**Summary Statistics** (Common Observations):

| Statistic  |          Stata |         Python |     Difference | Std Difference |
|------------|----------------|----------------|----------------|----------------|
| count      |       3.25e+06 |       3.25e+06 |       3.25e+06 |       3.25e+06 |
| mean       |        -0.0036 |        -0.0036 |       1.28e-07 |       2.29e-07 |
| std        |         0.5613 |         0.5613 |         0.0018 |         0.0033 |
| min        |      -166.4192 |      -166.4192 |        -0.7531 |        -1.3418 |
| 25%        |        -0.0412 |        -0.0412 |      -5.10e-09 |      -9.09e-09 |
| 50%        |      -8.74e-04 |      -8.74e-04 |      -5.07e-12 |      -9.02e-12 |
| 75%        |         0.0417 |         0.0417 |       5.10e-09 |       9.08e-09 |
| max        |        51.9783 |        51.9783 |         0.4751 |         0.8465 |

**Regression Analysis** (Python ~ Stata):

- **Model**: python = 0.0000 + 1.0000 * stata
- **R-squared**: 1.0000
- **N observations**: 3,246,170

| Coefficient |     Estimate |    Std Error | t-statistic |   p-value |
|-------------|--------------|--------------|-------------|----------|
| Intercept   |     6.09e-08 |     1.02e-06 |      0.0597 |     0.952 |
| Slope       |       1.0000 |     1.82e-06 | 550515.1509 |     0.000 |

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

**Precision2**: 99th percentile diff = 8.39e-08 (tolerance: < 1.00e+00)

**Summary Statistics** (Common Observations):

| Statistic  |          Stata |         Python |     Difference | Std Difference |
|------------|----------------|----------------|----------------|----------------|
| count      |       3.26e+06 |       3.26e+06 |       3.26e+06 |       3.26e+06 |
| mean       |        -0.0059 |        -0.0059 |       1.70e-06 |       3.98e-06 |
| std        |         0.4264 |         0.4263 |       9.31e-04 |         0.0022 |
| min        |      -166.1671 |      -166.1671 |        -0.0565 |        -0.1324 |
| 25%        |        -0.0307 |        -0.0307 |      -2.80e-09 |      -6.56e-09 |
| 50%        |      -5.74e-04 |      -5.73e-04 |         0.0000 |         0.0000 |
| 75%        |         0.0280 |         0.0280 |       2.81e-09 |       6.59e-09 |
| max        |        16.2765 |        16.2765 |         0.4751 |         1.1144 |

**Regression Analysis** (Python ~ Stata):

- **Model**: python = 0.0000 + 1.0000 * stata
- **R-squared**: 1.0000
- **N observations**: 3,259,599

| Coefficient |     Estimate |    Std Error | t-statistic |   p-value |
|-------------|--------------|--------------|-------------|----------|
| Intercept   |     1.47e-06 |     5.15e-07 |      2.8512 |     0.004 |
| Slope       |       1.0000 |     1.21e-06 | 827218.6121 |     0.000 |

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

**Precision2**: 99th percentile diff = 5.04e-10 (tolerance: < 1.00e+00)

**Summary Statistics** (Common Observations):

| Statistic  |          Stata |         Python |     Difference | Std Difference |
|------------|----------------|----------------|----------------|----------------|
| count      |       2.83e+06 |       2.83e+06 |       2.83e+06 |       2.83e+06 |
| mean       |         0.0017 |         0.0017 |      -2.03e-07 |      -5.25e-08 |
| std        |         3.8678 |         3.8678 |       5.49e-04 |       1.42e-04 |
| min        |      -990.0000 |      -990.0000 |        -0.6855 |        -0.1772 |
| 25%        |        -0.0013 |        -0.0013 |      -3.19e-11 |      -8.24e-12 |
| 50%        |         0.0000 |         0.0000 |         0.0000 |         0.0000 |
| 75%        |         0.0029 |         0.0029 |       3.23e-11 |       8.35e-12 |
| max        |      3440.0000 |      3440.0000 |         0.2136 |         0.0552 |

**Regression Analysis** (Python ~ Stata):

- **Model**: python = -0.0000 + 1.0000 * stata
- **R-squared**: 1.0000
- **N observations**: 2,827,667

| Coefficient |     Estimate |    Std Error | t-statistic |   p-value |
|-------------|--------------|--------------|-------------|----------|
| Intercept   |    -2.03e-07 |     3.26e-07 |     -0.6227 |     0.533 |
| Slope       |       1.0000 |     8.44e-08 |    1.19e+07 |     0.000 |

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

**Precision2**: 99th percentile diff = 1.53e-07 (tolerance: < 1.00e+00)

**Summary Statistics** (Common Observations):

| Statistic  |          Stata |         Python |     Difference | Std Difference |
|------------|----------------|----------------|----------------|----------------|
| count      |    449187.0000 |    449187.0000 |    449187.0000 |    449187.0000 |
| mean       |        -0.0238 |        -0.0238 |       2.69e-05 |       2.47e-05 |
| std        |         1.0884 |         1.0884 |         0.0355 |         0.0326 |
| min        |        -4.0000 |        -4.0000 |        -4.0000 |        -3.6751 |
| 25%        |        -1.0000 |        -1.0000 |         0.0000 |         0.0000 |
| 50%        |         0.0000 |         0.0000 |         0.0000 |         0.0000 |
| 75%        |         1.0000 |         1.0000 |         0.0000 |         0.0000 |
| max        |         4.0000 |         4.0000 |         5.0000 |         4.5938 |

**Regression Analysis** (Python ~ Stata):

- **Model**: python = 0.0000 + 0.9994 * stata
- **R-squared**: 0.9989
- **N observations**: 449,187

| Coefficient |     Estimate |    Std Error | t-statistic |   p-value |
|-------------|--------------|--------------|-------------|----------|
| Intercept   |     1.36e-05 |     5.29e-05 |      0.2579 |     0.796 |
| Slope       |       0.9994 |     4.86e-05 |  20557.0847 |     0.000 |

**Feedback**:
- Num observations with std_diff >= TOL_DIFF_1: 215/449187 (0.048%)
- Stata standard deviation: 1.09e+00

---

### CitationsRD

**Status**: ❌ FAILED

**Test Results**:
- Test 1 - Column names: ✅ PASSED
- Test 2 - Superset check: ✅ PASSED
- Test 3 - Precision1 check: ❌ FAILED
- Test 4 - Precision2 check: ❌ FAILED

**Columns**: ['CitationsRD']

**Observations**:
- Stata:  645,360
- Python: 701,940
- Common: 645,360

**Precision1**: 21.536% obs with std_diff >= 1.00e-02 (tolerance: < 10%)

**Precision2**: 99th percentile diff = 2.43e+00 (tolerance: < 1.00e+00)

**Summary Statistics** (Common Observations):

| Statistic  |          Stata |         Python |     Difference | Std Difference |
|------------|----------------|----------------|----------------|----------------|
| count      |    645360.0000 |    645360.0000 |    645360.0000 |    645360.0000 |
| mean       |         0.2154 |         0.0000 |        -0.2154 |        -0.5239 |
| std        |         0.4111 |         0.0000 |         0.4111 |         1.0000 |
| min        |         0.0000 |         0.0000 |        -1.0000 |        -2.4327 |
| 25%        |         0.0000 |         0.0000 |         0.0000 |         0.0000 |
| 50%        |         0.0000 |         0.0000 |         0.0000 |         0.0000 |
| 75%        |         0.0000 |         0.0000 |         0.0000 |         0.0000 |
| max        |         1.0000 |         0.0000 |         0.0000 |         0.0000 |

**Regression Analysis** (Python ~ Stata):

- **Model**: python = 0.0000 + 0.0000 * stata
- **R-squared**: nan
- **N observations**: 645,360

| Coefficient |     Estimate |    Std Error | t-statistic |   p-value |
|-------------|--------------|--------------|-------------|----------|
| Intercept   |       0.0000 |       0.0000 |         nan |       nan |
| Slope       |       0.0000 |       0.0000 |         nan |       nan |

**Feedback**:
- Num observations with std_diff >= TOL_DIFF_1: 138984/645360 (21.536%)
- Stata standard deviation: 4.11e-01

**Most Recent Bad Observations**:
```
   permno  yyyymm  python  stata  diff
0   10163  201105     0.0      1  -1.0
1   10259  201105     0.0      1  -1.0
2   10272  201105     0.0      1  -1.0
3   10302  201105     0.0      1  -1.0
4   10382  201105     0.0      1  -1.0
5   10463  201105     0.0      1  -1.0
6   10644  201105     0.0      1  -1.0
7   10874  201105     0.0      1  -1.0
8   11038  201105     0.0      1  -1.0
9   11077  201105     0.0      1  -1.0
```

**Largest Differences**:
```
   permno  yyyymm  python  stata  diff
0   10006  198306     0.0      1  -1.0
1   10006  198307     0.0      1  -1.0
2   10006  198308     0.0      1  -1.0
3   10006  198309     0.0      1  -1.0
4   10006  198310     0.0      1  -1.0
5   10006  198311     0.0      1  -1.0
6   10006  198312     0.0      1  -1.0
7   10006  198401     0.0      1  -1.0
8   10006  198402     0.0      1  -1.0
9   10006  198403     0.0      1  -1.0
```

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

**Precision2**: 99th percentile diff = 7.46e-07 (tolerance: < 1.00e+00)

**Summary Statistics** (Common Observations):

| Statistic  |          Stata |         Python |     Difference | Std Difference |
|------------|----------------|----------------|----------------|----------------|
| count      |       2.16e+06 |       2.16e+06 |       2.16e+06 |       2.16e+06 |
| mean       |        -0.6781 |        -0.6781 |       2.13e-10 |       7.04e-11 |
| std        |         3.0255 |         3.0255 |       6.78e-07 |       2.24e-07 |
| min        |     -1948.3774 |     -1948.3773 |      -8.87e-05 |      -2.93e-05 |
| 25%        |        -0.7631 |        -0.7631 |      -1.63e-07 |      -5.40e-08 |
| 50%        |        -0.3171 |        -0.3171 |       7.66e-10 |       2.53e-10 |
| 75%        |        -0.0574 |        -0.0574 |       1.64e-07 |       5.42e-08 |
| max        |         6.8094 |         6.8094 |       1.37e-04 |       4.53e-05 |

**Regression Analysis** (Python ~ Stata):

- **Model**: python = -0.0000 + 1.0000 * stata
- **R-squared**: 1.0000
- **N observations**: 2,156,555

| Coefficient |     Estimate |    Std Error | t-statistic |   p-value |
|-------------|--------------|--------------|-------------|----------|
| Intercept   |    -1.12e-08 |     4.72e-10 |    -23.6512 |     0.000 |
| Slope       |       1.0000 |     1.52e-10 |    6.57e+09 |     0.000 |

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

**Precision2**: 99th percentile diff = 1.24e-07 (tolerance: < 1.00e+00)

**Summary Statistics** (Common Observations):

| Statistic  |          Stata |         Python |     Difference | Std Difference |
|------------|----------------|----------------|----------------|----------------|
| count      |       1.90e+06 |       1.90e+06 |       1.90e+06 |       1.90e+06 |
| mean       |         0.5016 |         0.5016 |      -6.04e-06 |      -4.24e-06 |
| std        |         1.4262 |         1.4262 |         0.0022 |         0.0015 |
| min        |       -11.3807 |       -11.3807 |        -0.6525 |        -0.4575 |
| 25%        |        -0.1400 |        -0.1400 |      -3.01e-08 |      -2.11e-08 |
| 50%        |         0.3966 |         0.3966 |      -6.75e-11 |      -4.73e-11 |
| 75%        |         1.0520 |         1.0520 |       2.99e-08 |       2.10e-08 |
| max        |        12.3441 |        12.3441 |         0.0810 |         0.0568 |

**Regression Analysis** (Python ~ Stata):

- **Model**: python = -0.0000 + 1.0000 * stata
- **R-squared**: 1.0000
- **N observations**: 1,898,755

| Coefficient |     Estimate |    Std Error | t-statistic |   p-value |
|-------------|--------------|--------------|-------------|----------|
| Intercept   |    -5.96e-06 |     1.69e-06 |     -3.5261 |     0.000 |
| Slope       |       1.0000 |     1.12e-06 | 894235.2818 |     0.000 |

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

**Precision2**: 99th percentile diff = 0.00e+00 (tolerance: < 1.00e+00)

**Summary Statistics** (Common Observations):

| Statistic  |          Stata |         Python |     Difference | Std Difference |
|------------|----------------|----------------|----------------|----------------|
| count      |    133799.0000 |    133799.0000 |    133799.0000 |    133799.0000 |
| mean       |         0.2637 |         0.2637 |       7.47e-06 |       1.70e-05 |
| std        |         0.4407 |         0.4407 |         0.0106 |         0.0240 |
| min        |         0.0000 |         0.0000 |        -1.0000 |        -2.2693 |
| 25%        |         0.0000 |         0.0000 |         0.0000 |         0.0000 |
| 50%        |         0.0000 |         0.0000 |         0.0000 |         0.0000 |
| 75%        |         1.0000 |         1.0000 |         0.0000 |         0.0000 |
| max        |         1.0000 |         1.0000 |         1.0000 |         2.2693 |

**Regression Analysis** (Python ~ Stata):

- **Model**: python = 0.0001 + 0.9997 * stata
- **R-squared**: 0.9994
- **N observations**: 133,799

| Coefficient |     Estimate |    Std Error | t-statistic |   p-value |
|-------------|--------------|--------------|-------------|----------|
| Intercept   |     8.12e-05 |     3.37e-05 |      2.4074 |     0.016 |
| Slope       |       0.9997 |     6.57e-05 |  15220.0151 |     0.000 |

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

**Precision2**: 99th percentile diff = 0.00e+00 (tolerance: < 1.00e+00)

**Summary Statistics** (Common Observations):

| Statistic  |          Stata |         Python |     Difference | Std Difference |
|------------|----------------|----------------|----------------|----------------|
| count      |       3.62e+06 |       3.62e+06 |       3.62e+06 |       3.62e+06 |
| mean       |         0.1329 |         0.1329 |         0.0000 |         0.0000 |
| std        |         0.3394 |         0.3394 |         0.0026 |         0.0076 |
| min        |         0.0000 |         0.0000 |        -1.0000 |        -2.9460 |
| 25%        |         0.0000 |         0.0000 |         0.0000 |         0.0000 |
| 50%        |         0.0000 |         0.0000 |         0.0000 |         0.0000 |
| 75%        |         0.0000 |         0.0000 |         0.0000 |         0.0000 |
| max        |         1.0000 |         1.0000 |         1.0000 |         2.9460 |

**Regression Analysis** (Python ~ Stata):

- **Model**: python = 0.0000 + 1.0000 * stata
- **R-squared**: 0.9999
- **N observations**: 3,624,363

| Coefficient |     Estimate |    Std Error | t-statistic |   p-value |
|-------------|--------------|--------------|-------------|----------|
| Intercept   |     3.82e-06 |     1.45e-06 |      2.6305 |     0.009 |
| Slope       |       1.0000 |     3.98e-06 | 251120.2086 |     0.000 |

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

**Precision2**: 99th percentile diff = 1.14e-03 (tolerance: < 1.00e+00)

**Summary Statistics** (Common Observations):

| Statistic  |          Stata |         Python |     Difference | Std Difference |
|------------|----------------|----------------|----------------|----------------|
| count      |       4.18e+06 |       4.18e+06 |       4.18e+06 |       4.18e+06 |
| mean       |        -0.1398 |        -0.1398 |      -7.56e-06 |      -2.25e-05 |
| std        |         0.3359 |         0.3359 |       8.70e-05 |       2.59e-04 |
| min        |        -6.2761 |        -6.2761 |        -0.0047 |        -0.0139 |
| 25%        |        -0.2208 |        -0.2208 |      -1.92e-08 |      -5.71e-08 |
| 50%        |        -0.0859 |        -0.0859 |      -1.91e-09 |      -5.68e-09 |
| 75%        |         0.0207 |         0.0207 |       1.34e-08 |       3.99e-08 |
| max        |         3.5667 |         3.5667 |         0.0047 |         0.0140 |

**Regression Analysis** (Python ~ Stata):

- **Model**: python = -0.0000 + 1.0000 * stata
- **R-squared**: 1.0000
- **N observations**: 4,179,145

| Coefficient |     Estimate |    Std Error | t-statistic |   p-value |
|-------------|--------------|--------------|-------------|----------|
| Intercept   |    -6.58e-06 |     4.61e-08 |   -142.9121 |     0.000 |
| Slope       |       1.0000 |     1.27e-07 |    7.90e+06 |     0.000 |

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

**Precision2**: 99th percentile diff = 1.32e-03 (tolerance: < 1.00e+00)

**Summary Statistics** (Common Observations):

| Statistic  |          Stata |         Python |     Difference | Std Difference |
|------------|----------------|----------------|----------------|----------------|
| count      |       4.61e+06 |       4.61e+06 |       4.61e+06 |       4.61e+06 |
| mean       |        -0.2000 |        -0.2000 |       1.43e-05 |       3.75e-05 |
| std        |         0.3826 |         0.3826 |       1.07e-04 |       2.81e-04 |
| min        |        -4.4915 |        -4.4915 |        -0.0045 |        -0.0118 |
| 25%        |        -0.3848 |        -0.3848 |      -1.14e-08 |      -2.99e-08 |
| 50%        |        -0.1794 |        -0.1794 |       1.64e-09 |       4.28e-09 |
| 75%        |         0.0124 |         0.0124 |       1.68e-08 |       4.40e-08 |
| max        |         2.5369 |         2.5369 |         0.0043 |         0.0111 |

**Regression Analysis** (Python ~ Stata):

- **Model**: python = 0.0000 + 1.0000 * stata
- **R-squared**: 1.0000
- **N observations**: 4,609,158

| Coefficient |     Estimate |    Std Error | t-statistic |   p-value |
|-------------|--------------|--------------|-------------|----------|
| Intercept   |     1.28e-05 |     5.65e-08 |    226.2108 |     0.000 |
| Slope       |       1.0000 |     1.31e-07 |    7.65e+06 |     0.000 |

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

**Precision2**: 99th percentile diff = 0.00e+00 (tolerance: < 1.00e+00)

**Summary Statistics** (Common Observations):

| Statistic  |          Stata |         Python |     Difference | Std Difference |
|------------|----------------|----------------|----------------|----------------|
| count      |       2.56e+06 |       2.56e+06 |       2.56e+06 |       2.56e+06 |
| mean       |         0.0233 |         0.0155 |        -0.0077 |        -0.0514 |
| std        |         0.1508 |         0.1237 |         0.0967 |         0.6412 |
| min        |         0.0000 |         0.0000 |        -1.0000 |        -6.6310 |
| 25%        |         0.0000 |         0.0000 |         0.0000 |         0.0000 |
| 50%        |         0.0000 |         0.0000 |         0.0000 |         0.0000 |
| 75%        |         0.0000 |         0.0000 |         0.0000 |         0.0000 |
| max        |         1.0000 |         1.0000 |         1.0000 |         6.6310 |

**Regression Analysis** (Python ~ Stata):

- **Model**: python = 0.0009 + 0.6308 * stata
- **R-squared**: 0.5915
- **N observations**: 2,559,713

| Coefficient |     Estimate |    Std Error | t-statistic |   p-value |
|-------------|--------------|--------------|-------------|----------|
| Intercept   |     8.52e-04 |     5.00e-05 |     17.0407 |     0.000 |
| Slope       |       0.6308 |     3.28e-04 |   1925.2210 |     0.000 |

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

**Precision2**: 99th percentile diff = 8.97e-08 (tolerance: < 1.00e+00)

**Summary Statistics** (Common Observations):

| Statistic  |          Stata |         Python |     Difference | Std Difference |
|------------|----------------|----------------|----------------|----------------|
| count      |    356462.0000 |    356462.0000 |    356462.0000 |    356462.0000 |
| mean       |         0.0114 |         0.0114 |       4.34e-07 |       3.89e-06 |
| std        |         0.1115 |         0.1115 |       6.38e-04 |         0.0057 |
| min        |        -0.9813 |        -0.9813 |        -0.1649 |        -1.4790 |
| 25%        |        -0.0407 |        -0.0407 |      -1.00e-10 |      -8.97e-10 |
| 50%        |         0.0102 |         0.0102 |         0.0000 |         0.0000 |
| 75%        |         0.0606 |         0.0606 |       1.00e-10 |       8.97e-10 |
| max        |         8.1384 |         8.1384 |         0.1965 |         1.7623 |

**Regression Analysis** (Python ~ Stata):

- **Model**: python = 0.0000 + 1.0000 * stata
- **R-squared**: 1.0000
- **N observations**: 356,462

| Coefficient |     Estimate |    Std Error | t-statistic |   p-value |
|-------------|--------------|--------------|-------------|----------|
| Intercept   |     5.74e-07 |     1.07e-06 |      0.5345 |     0.593 |
| Slope       |       1.0000 |     9.58e-06 | 104359.4765 |     0.000 |

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

**Precision2**: 99th percentile diff = 0.00e+00 (tolerance: < 1.00e+00)

**Summary Statistics** (Common Observations):

| Statistic  |          Stata |         Python |     Difference | Std Difference |
|------------|----------------|----------------|----------------|----------------|
| count      |       2.73e+06 |       2.73e+06 |       2.73e+06 |       2.73e+06 |
| mean       |         0.5023 |         0.5023 |         0.0000 |         0.0000 |
| std        |         0.5000 |         0.5000 |         0.0000 |         0.0000 |
| min        |         0.0000 |         0.0000 |         0.0000 |         0.0000 |
| 25%        |         0.0000 |         0.0000 |         0.0000 |         0.0000 |
| 50%        |         1.0000 |         1.0000 |         0.0000 |         0.0000 |
| 75%        |         1.0000 |         1.0000 |         0.0000 |         0.0000 |
| max        |         1.0000 |         1.0000 |         0.0000 |         0.0000 |

**Regression Analysis** (Python ~ Stata):

- **Model**: python = -0.0000 + 1.0000 * stata
- **R-squared**: 1.0000
- **N observations**: 2,725,997

| Coefficient |     Estimate |    Std Error | t-statistic |   p-value |
|-------------|--------------|--------------|-------------|----------|
| Intercept   |    -1.68e-12 |     1.47e-15 |  -1143.8999 |     0.000 |
| Slope       |       1.0000 |     2.08e-15 |    4.81e+14 |     0.000 |

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

**Precision2**: 99th percentile diff = 1.13e-07 (tolerance: < 1.00e+00)

**Summary Statistics** (Common Observations):

| Statistic  |          Stata |         Python |     Difference | Std Difference |
|------------|----------------|----------------|----------------|----------------|
| count      |       1.06e+06 |       1.06e+06 |       1.06e+06 |       1.06e+06 |
| mean       |         0.1316 |         0.1316 |      -1.46e-10 |      -1.65e-10 |
| std        |         0.8888 |         0.8888 |       2.45e-08 |       2.76e-08 |
| min        |       -47.2500 |       -47.2500 |      -2.00e-06 |      -2.25e-06 |
| 25%        |        -0.1820 |        -0.1820 |      -1.00e-09 |      -1.13e-09 |
| 50%        |         0.0800 |         0.0800 |         0.0000 |         0.0000 |
| 75%        |         0.3990 |         0.3990 |         0.0000 |         0.0000 |
| max        |        48.0560 |        48.0560 |       1.00e-06 |       1.13e-06 |

**Regression Analysis** (Python ~ Stata):

- **Model**: python = 0.0000 + 1.0000 * stata
- **R-squared**: 1.0000
- **N observations**: 1,062,671

| Coefficient |     Estimate |    Std Error | t-statistic |   p-value |
|-------------|--------------|--------------|-------------|----------|
| Intercept   |     1.93e-11 |     2.40e-11 |      0.8034 |     0.422 |
| Slope       |       1.0000 |     2.67e-11 |    3.74e+10 |     0.000 |

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

**Precision2**: 99th percentile diff = 1.90e-07 (tolerance: < 1.00e+00)

**Summary Statistics** (Common Observations):

| Statistic  |          Stata |         Python |     Difference | Std Difference |
|------------|----------------|----------------|----------------|----------------|
| count      |       3.30e+06 |       3.30e+06 |       3.30e+06 |       3.30e+06 |
| mean       |         0.0221 |         0.0221 |      -9.06e-09 |      -7.46e-08 |
| std        |         0.1215 |         0.1215 |       3.96e-05 |       3.26e-04 |
| min        |        -1.8713 |        -1.8713 |        -0.0074 |        -0.0613 |
| 25%        |        -0.0140 |        -0.0140 |      -8.83e-10 |      -7.27e-09 |
| 50%        |         0.0104 |         0.0104 |         0.0000 |         0.0000 |
| 75%        |         0.0557 |         0.0557 |       8.67e-10 |       7.14e-09 |
| max        |         1.8202 |         1.8202 |         0.0177 |         0.1459 |

**Regression Analysis** (Python ~ Stata):

- **Model**: python = -0.0000 + 1.0000 * stata
- **R-squared**: 1.0000
- **N observations**: 3,295,155

| Coefficient |     Estimate |    Std Error | t-statistic |   p-value |
|-------------|--------------|--------------|-------------|----------|
| Intercept   |    -3.41e-08 |     2.22e-08 |     -1.5378 |     0.124 |
| Slope       |       1.0000 |     1.80e-07 |    5.57e+06 |     0.000 |

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

**Precision2**: 99th percentile diff = 1.48e-07 (tolerance: < 1.00e+00)

**Summary Statistics** (Common Observations):

| Statistic  |          Stata |         Python |     Difference | Std Difference |
|------------|----------------|----------------|----------------|----------------|
| count      |       3.26e+06 |       3.26e+06 |       3.26e+06 |       3.26e+06 |
| mean       |         0.0146 |         0.0146 |      -2.15e-06 |      -1.83e-05 |
| std        |         0.1171 |         0.1170 |         0.0011 |         0.0092 |
| min        |        -8.3977 |        -8.3977 |        -0.5525 |        -4.7197 |
| 25%        |        -0.0119 |        -0.0119 |      -6.63e-10 |      -5.66e-09 |
| 50%        |         0.0079 |         0.0079 |         0.0000 |         0.0000 |
| 75%        |         0.0389 |         0.0389 |       6.63e-10 |       5.67e-09 |
| max        |        25.3738 |        25.3738 |         0.0315 |         0.2689 |

**Regression Analysis** (Python ~ Stata):

- **Model**: python = 0.0000 + 0.9993 * stata
- **R-squared**: 0.9999
- **N observations**: 3,259,701

| Coefficient |     Estimate |    Std Error | t-statistic |   p-value |
|-------------|--------------|--------------|-------------|----------|
| Intercept   |     7.48e-06 |     5.97e-07 |     12.5376 |     0.000 |
| Slope       |       0.9993 |     5.06e-06 | 197472.4554 |     0.000 |

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

**Precision2**: 99th percentile diff = 1.18e-07 (tolerance: < 1.00e+00)

**Summary Statistics** (Common Observations):

| Statistic  |          Stata |         Python |     Difference | Std Difference |
|------------|----------------|----------------|----------------|----------------|
| count      |    460159.0000 |    460159.0000 |    460159.0000 |    460159.0000 |
| mean       |         0.0070 |         0.0070 |       8.26e-07 |       1.82e-05 |
| std        |         0.0453 |         0.0453 |       8.95e-05 |         0.0020 |
| min        |        -2.4175 |        -2.4175 |      -4.14e-05 |      -9.13e-04 |
| 25%        |        -0.0016 |        -0.0016 |      -8.66e-11 |      -1.91e-09 |
| 50%        |         0.0014 |         0.0014 |       8.07e-14 |       1.78e-12 |
| 75%        |         0.0099 |         0.0099 |       9.26e-11 |       2.04e-09 |
| max        |         1.1627 |         1.1627 |         0.0137 |         0.3016 |

**Regression Analysis** (Python ~ Stata):

- **Model**: python = 0.0000 + 1.0000 * stata
- **R-squared**: 1.0000
- **N observations**: 460,159

| Coefficient |     Estimate |    Std Error | t-statistic |   p-value |
|-------------|--------------|--------------|-------------|----------|
| Intercept   |     8.69e-07 |     1.34e-07 |      6.5094 |     0.000 |
| Slope       |       1.0000 |     2.91e-06 | 343541.7042 |     0.000 |

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

**Precision2**: 99th percentile diff = 8.34e-08 (tolerance: < 1.00e+00)

**Summary Statistics** (Common Observations):

| Statistic  |          Stata |         Python |     Difference | Std Difference |
|------------|----------------|----------------|----------------|----------------|
| count      |       3.19e+06 |       3.19e+06 |       3.19e+06 |       3.19e+06 |
| mean       |         0.0212 |         0.0212 |       2.09e-06 |       3.82e-06 |
| std        |         0.5462 |         0.5462 |         0.0012 |         0.0021 |
| min        |      -240.0000 |      -240.0000 |        -0.1665 |        -0.3048 |
| 25%        |        -0.0179 |        -0.0179 |      -1.39e-09 |      -2.54e-09 |
| 50%        |         0.0212 |         0.0212 |       4.36e-13 |       7.98e-13 |
| 75%        |         0.0750 |         0.0750 |       1.40e-09 |       2.56e-09 |
| max        |        24.9274 |        24.9274 |         0.5525 |         1.0115 |

**Regression Analysis** (Python ~ Stata):

- **Model**: python = 0.0000 + 1.0000 * stata
- **R-squared**: 1.0000
- **N observations**: 3,194,475

| Coefficient |     Estimate |    Std Error | t-statistic |   p-value |
|-------------|--------------|--------------|-------------|----------|
| Intercept   |     2.71e-06 |     6.54e-07 |      4.1497 |     0.000 |
| Slope       |       1.0000 |     1.20e-06 | 836225.8898 |     0.000 |

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

**Precision2**: 99th percentile diff = 1.76e-07 (tolerance: < 1.00e+00)

**Summary Statistics** (Common Observations):

| Statistic  |          Stata |         Python |     Difference | Std Difference |
|------------|----------------|----------------|----------------|----------------|
| count      |       3.25e+06 |       3.25e+06 |       3.25e+06 |       3.25e+06 |
| mean       |         0.0265 |         0.0265 |       2.83e-07 |       1.59e-06 |
| std        |         0.1773 |         0.1773 |       1.91e-04 |         0.0011 |
| min        |       -30.5807 |       -30.5807 |        -0.0490 |        -0.2763 |
| 25%        |        -0.0174 |        -0.0174 |      -8.28e-10 |      -4.67e-09 |
| 50%        |         0.0000 |         0.0000 |         0.0000 |         0.0000 |
| 75%        |         0.0538 |         0.0538 |       8.25e-10 |       4.65e-09 |
| max        |        12.4151 |        12.4151 |         0.0466 |         0.2627 |

**Regression Analysis** (Python ~ Stata):

- **Model**: python = 0.0000 + 1.0000 * stata
- **R-squared**: 1.0000
- **N observations**: 3,250,876

| Coefficient |     Estimate |    Std Error | t-statistic |   p-value |
|-------------|--------------|--------------|-------------|----------|
| Intercept   |     3.31e-07 |     1.07e-07 |      3.0886 |     0.002 |
| Slope       |       1.0000 |     5.98e-07 |    1.67e+06 |     0.000 |

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

**Precision2**: 99th percentile diff = 1.86e-07 (tolerance: < 1.00e+00)

**Summary Statistics** (Common Observations):

| Statistic  |          Stata |         Python |     Difference | Std Difference |
|------------|----------------|----------------|----------------|----------------|
| count      |       3.30e+06 |       3.30e+06 |       3.30e+06 |       3.30e+06 |
| mean       |         0.0063 |         0.0063 |       1.70e-06 |       2.19e-05 |
| std        |         0.0776 |         0.0776 |         0.0015 |         0.0196 |
| min        |        -1.8040 |        -1.8040 |        -0.2490 |        -3.2078 |
| 25%        |         0.0000 |         0.0000 |         0.0000 |         0.0000 |
| 50%        |         0.0000 |         0.0000 |         0.0000 |         0.0000 |
| 75%        |       5.23e-04 |       5.23e-04 |         0.0000 |         0.0000 |
| max        |         1.9377 |         1.9377 |         0.7521 |         9.6876 |

**Regression Analysis** (Python ~ Stata):

- **Model**: python = 0.0000 + 0.9999 * stata
- **R-squared**: 0.9996
- **N observations**: 3,295,155

| Coefficient |     Estimate |    Std Error | t-statistic |   p-value |
|-------------|--------------|--------------|-------------|----------|
| Intercept   |     2.29e-06 |     8.39e-07 |      2.7245 |     0.006 |
| Slope       |       0.9999 |     1.08e-05 |  92801.6075 |     0.000 |

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

**Precision2**: 99th percentile diff = 2.70e-07 (tolerance: < 1.00e+00)

**Summary Statistics** (Common Observations):

| Statistic  |          Stata |         Python |     Difference | Std Difference |
|------------|----------------|----------------|----------------|----------------|
| count      |       3.25e+06 |       3.25e+06 |       3.25e+06 |       3.25e+06 |
| mean       |        -0.0184 |        -0.0184 |       6.95e-07 |       3.39e-06 |
| std        |         0.2049 |         0.2049 |         0.0016 |         0.0078 |
| min        |       -12.4151 |       -12.4151 |        -0.2490 |        -1.2157 |
| 25%        |        -0.0667 |        -0.0667 |      -5.33e-09 |      -2.60e-08 |
| 50%        |        -0.0015 |        -0.0015 |         0.0000 |         0.0000 |
| 75%        |         0.0412 |         0.0412 |       5.38e-09 |       2.63e-08 |
| max        |        30.5807 |        30.5807 |         0.7521 |         3.6714 |

**Regression Analysis** (Python ~ Stata):

- **Model**: python = -0.0000 + 1.0000 * stata
- **R-squared**: 0.9999
- **N observations**: 3,250,876

| Coefficient |     Estimate |    Std Error | t-statistic |   p-value |
|-------------|--------------|--------------|-------------|----------|
| Intercept   |    -1.39e-07 |     8.91e-07 |     -0.1564 |     0.876 |
| Slope       |       1.0000 |     4.33e-06 | 230830.5221 |     0.000 |

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

**Precision2**: 99th percentile diff = 0.00e+00 (tolerance: < 1.00e+00)

**Summary Statistics** (Common Observations):

| Statistic  |          Stata |         Python |     Difference | Std Difference |
|------------|----------------|----------------|----------------|----------------|
| count      |       4.05e+06 |       4.05e+06 |       4.05e+06 |       4.05e+06 |
| mean       |         0.0191 |         0.0191 |      -4.22e-05 |      -3.09e-04 |
| std        |         0.1369 |         0.1368 |         0.0084 |         0.0615 |
| min        |         0.0000 |         0.0000 |        -1.0000 |        -7.3042 |
| 25%        |         0.0000 |         0.0000 |         0.0000 |         0.0000 |
| 50%        |         0.0000 |         0.0000 |         0.0000 |         0.0000 |
| 75%        |         0.0000 |         0.0000 |         0.0000 |         0.0000 |
| max        |         1.0000 |         1.0000 |         1.0000 |         7.3042 |

**Regression Analysis** (Python ~ Stata):

- **Model**: python = 0.0000 + 0.9970 * stata
- **R-squared**: 0.9962
- **N observations**: 4,047,630

| Coefficient |     Estimate |    Std Error | t-statistic |   p-value |
|-------------|--------------|--------------|-------------|----------|
| Intercept   |     1.46e-05 |     4.22e-06 |      3.4609 |     0.001 |
| Slope       |       0.9970 |     3.05e-05 |  32651.7180 |     0.000 |

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

**Precision2**: 99th percentile diff = 0.00e+00 (tolerance: < 1.00e+00)

**Summary Statistics** (Common Observations):

| Statistic  |          Stata |         Python |     Difference | Std Difference |
|------------|----------------|----------------|----------------|----------------|
| count      |       4.05e+06 |       4.05e+06 |       4.05e+06 |       4.05e+06 |
| mean       |         0.0039 |         0.0039 |      -2.22e-06 |      -3.57e-05 |
| std        |         0.0622 |         0.0622 |         0.0055 |         0.0886 |
| min        |         0.0000 |         0.0000 |        -1.0000 |       -16.0714 |
| 25%        |         0.0000 |         0.0000 |         0.0000 |         0.0000 |
| 50%        |         0.0000 |         0.0000 |         0.0000 |         0.0000 |
| 75%        |         0.0000 |         0.0000 |         0.0000 |         0.0000 |
| max        |         1.0000 |         1.0000 |         1.0000 |        16.0714 |

**Regression Analysis** (Python ~ Stata):

- **Model**: python = 0.0000 + 0.9958 * stata
- **R-squared**: 0.9922
- **N observations**: 4,047,630

| Coefficient |     Estimate |    Std Error | t-statistic |   p-value |
|-------------|--------------|--------------|-------------|----------|
| Intercept   |     1.41e-05 |     2.74e-06 |      5.1554 |     0.000 |
| Slope       |       0.9958 |     4.40e-05 |  22638.7735 |     0.000 |

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

**Precision2**: 99th percentile diff = 2.01e+00 (tolerance: < 1.00e+00)

**Summary Statistics** (Common Observations):

| Statistic  |          Stata |         Python |     Difference | Std Difference |
|------------|----------------|----------------|----------------|----------------|
| count      |       1.78e+06 |       1.78e+06 |       1.78e+06 |       1.78e+06 |
| mean       |         0.4456 |         0.3935 |        -0.0520 |        -0.1047 |
| std        |         0.4970 |         0.4885 |         0.2223 |         0.4473 |
| min        |         0.0000 |         0.0000 |        -1.0000 |        -2.0120 |
| 25%        |         0.0000 |         0.0000 |         0.0000 |         0.0000 |
| 50%        |         0.0000 |         0.0000 |         0.0000 |         0.0000 |
| 75%        |         1.0000 |         1.0000 |         0.0000 |         0.0000 |
| max        |         1.0000 |         1.0000 |         1.0000 |         2.0120 |

**Regression Analysis** (Python ~ Stata):

- **Model**: python = 0.0001 + 0.8830 * stata
- **R-squared**: 0.8070
- **N observations**: 1,775,337

| Coefficient |     Estimate |    Std Error | t-statistic |   p-value |
|-------------|--------------|--------------|-------------|----------|
| Intercept   |     1.01e-04 |     2.16e-04 |      0.4650 |     0.642 |
| Slope       |       0.8830 |     3.24e-04 |   2724.9918 |     0.000 |

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

**Precision2**: 99th percentile diff = 0.00e+00 (tolerance: < 1.00e+00)

**Summary Statistics** (Common Observations):

| Statistic  |          Stata |         Python |     Difference | Std Difference |
|------------|----------------|----------------|----------------|----------------|
| count      |       1.59e+06 |       1.59e+06 |       1.59e+06 |       1.59e+06 |
| mean       |         0.6292 |         0.6298 |       6.09e-04 |       5.89e-04 |
| std        |         1.0349 |         1.0358 |         0.0286 |         0.0276 |
| min        |         0.0000 |         0.0000 |        -1.0000 |        -0.9663 |
| 25%        |         0.0000 |         0.0000 |         0.0000 |         0.0000 |
| 50%        |         0.0000 |         0.0000 |         0.0000 |         0.0000 |
| 75%        |         1.0000 |         1.0000 |         0.0000 |         0.0000 |
| max        |         3.0000 |         3.0000 |         3.0000 |         2.8989 |

**Regression Analysis** (Python ~ Stata):

- **Model**: python = 0.0003 + 1.0005 * stata
- **R-squared**: 0.9992
- **N observations**: 1,591,697

| Coefficient |     Estimate |    Std Error | t-statistic |   p-value |
|-------------|--------------|--------------|-------------|----------|
| Intercept   |     3.17e-04 |     2.65e-05 |     11.9466 |     0.000 |
| Slope       |       1.0005 |     2.19e-05 |  45688.8176 |     0.000 |

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

**Precision2**: 99th percentile diff = 9.13e-08 (tolerance: < 1.00e+00)

**Summary Statistics** (Common Observations):

| Statistic  |          Stata |         Python |     Difference | Std Difference |
|------------|----------------|----------------|----------------|----------------|
| count      |       4.64e+06 |       4.64e+06 |       4.64e+06 |       4.64e+06 |
| mean       |         1.8039 |         1.8039 |       2.66e-10 |       8.56e-11 |
| std        |         3.1052 |         3.1052 |       9.44e-08 |       3.04e-08 |
| min        |       -12.2705 |       -12.2705 |      -9.62e-07 |      -3.10e-07 |
| 25%        |        -0.3808 |        -0.3808 |      -4.02e-08 |      -1.29e-08 |
| 50%        |         1.6649 |         1.6649 |       9.04e-11 |       2.91e-11 |
| 75%        |         3.9554 |         3.9554 |       4.12e-08 |       1.33e-08 |
| max        |        14.2392 |        14.2392 |       9.61e-07 |       3.10e-07 |

**Regression Analysis** (Python ~ Stata):

- **Model**: python = 0.0000 + 1.0000 * stata
- **R-squared**: 1.0000
- **N observations**: 4,640,493

| Coefficient |     Estimate |    Std Error | t-statistic |   p-value |
|-------------|--------------|--------------|-------------|----------|
| Intercept   |     5.01e-10 |     5.07e-11 |      9.8872 |     0.000 |
| Slope       |       1.0000 |     1.41e-11 |    7.09e+10 |     0.000 |

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

**Precision2**: 99th percentile diff = 0.00e+00 (tolerance: < 1.00e+00)

**Summary Statistics** (Common Observations):

| Statistic  |          Stata |         Python |     Difference | Std Difference |
|------------|----------------|----------------|----------------|----------------|
| count      |    449191.0000 |    449191.0000 |    449191.0000 |    449191.0000 |
| mean       |         0.3815 |         0.3815 |         0.0000 |      -3.95e-21 |
| std        |         0.4857 |         0.4857 |         0.0159 |         0.0328 |
| min        |         0.0000 |         0.0000 |        -1.0000 |        -2.0587 |
| 25%        |         0.0000 |         0.0000 |         0.0000 |         0.0000 |
| 50%        |         0.0000 |         0.0000 |         0.0000 |         0.0000 |
| 75%        |         1.0000 |         1.0000 |         0.0000 |         0.0000 |
| max        |         1.0000 |         1.0000 |         1.0000 |         2.0587 |

**Regression Analysis** (Python ~ Stata):

- **Model**: python = 0.0002 + 0.9995 * stata
- **R-squared**: 0.9989
- **N observations**: 449,191

| Coefficient |     Estimate |    Std Error | t-statistic |   p-value |
|-------------|--------------|--------------|-------------|----------|
| Intercept   |     2.05e-04 |     3.02e-05 |      6.7888 |     0.000 |
| Slope       |       0.9995 |     4.89e-05 |  20427.2154 |     0.000 |

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

**Precision2**: 99th percentile diff = 2.17e-08 (tolerance: < 1.00e+00)

**Summary Statistics** (Common Observations):

| Statistic  |          Stata |         Python |     Difference | Std Difference |
|------------|----------------|----------------|----------------|----------------|
| count      |       2.92e+06 |       2.92e+06 |       2.92e+06 |       2.92e+06 |
| mean       |         0.7855 |         0.7852 |      -3.11e-04 |      -9.27e-07 |
| std        |       335.4142 |       333.8812 |         2.9995 |         0.0089 |
| min        |   -121033.2100 |   -121033.2121 |     -4029.4330 |       -12.0133 |
| 25%        |         0.1588 |         0.1588 |      -1.34e-08 |      -3.99e-11 |
| 50%        |         0.4869 |         0.4869 |      -2.32e-12 |      -6.92e-15 |
| 75%        |         0.9656 |         0.9656 |       1.33e-08 |       3.98e-11 |
| max        |    471732.5300 |    467703.0970 |      3149.6636 |         9.3904 |

**Regression Analysis** (Python ~ Stata):

- **Model**: python = 0.0033 + 0.9954 * stata
- **R-squared**: 0.9999
- **N observations**: 2,924,820

| Coefficient |     Estimate |    Std Error | t-statistic |   p-value |
|-------------|--------------|--------------|-------------|----------|
| Intercept   |       0.0033 |       0.0015 |      2.1955 |     0.028 |
| Slope       |       0.9954 |     4.48e-06 | 221979.7776 |     0.000 |

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

**Precision2**: 99th percentile diff = 3.93e-08 (tolerance: < 1.00e+00)

**Summary Statistics** (Common Observations):

| Statistic  |          Stata |         Python |     Difference | Std Difference |
|------------|----------------|----------------|----------------|----------------|
| count      |       2.20e+06 |       2.20e+06 |       2.20e+06 |       2.20e+06 |
| mean       |         0.0885 |         0.0885 |      -1.56e-12 |      -5.16e-12 |
| std        |         0.3016 |         0.3016 |       9.02e-09 |       2.99e-08 |
| min        |         0.0000 |         0.0000 |      -8.71e-06 |      -2.89e-05 |
| 25%        |         0.0403 |         0.0403 |      -1.24e-09 |      -4.10e-09 |
| 50%        |         0.0666 |         0.0666 |         0.0000 |         0.0000 |
| 75%        |         0.1061 |         0.1061 |       1.23e-09 |       4.09e-09 |
| max        |       213.4789 |       213.4789 |       2.83e-06 |       9.39e-06 |

**Regression Analysis** (Python ~ Stata):

- **Model**: python = 0.0000 + 1.0000 * stata
- **R-squared**: 1.0000
- **N observations**: 2,203,166

| Coefficient |     Estimate |    Std Error | t-statistic |   p-value |
|-------------|--------------|--------------|-------------|----------|
| Intercept   |     4.99e-10 |     6.22e-12 |     80.2365 |     0.000 |
| Slope       |       1.0000 |     1.98e-11 |    5.06e+10 |     0.000 |

**Feedback**:
- Num observations with std_diff >= TOL_DIFF_1: 0/2203166 (0.000%)
- Stata standard deviation: 3.02e-01

---

### EarnSupBig

**Status**: ✅ PASSED

**Test Results**:
- Test 1 - Column names: ✅ PASSED
- Test 2 - Superset check: ✅ PASSED
- Test 3 - Precision1 check: ✅ PASSED
- Test 4 - Precision2 check: ✅ PASSED

**Columns**: ['EarnSupBig']

**Observations**:
- Stata:  2,327,518
- Python: 2,336,093
- Common: 2,323,705

**Precision1**: 0.152% obs with std_diff >= 1.00e-02 (tolerance: < 10%)

**Precision2**: 99th percentile diff = 1.83e-13 (tolerance: < 1.00e+00)

**Summary Statistics** (Common Observations):

| Statistic  |          Stata |         Python |     Difference | Std Difference |
|------------|----------------|----------------|----------------|----------------|
| count      |       2.32e+06 |       2.32e+06 |       2.32e+06 |       2.32e+06 |
| mean       |       5.45e+10 |        -0.1171 |      -5.45e+10 |        -0.0117 |
| std        |       4.64e+12 |         1.1736 |       4.64e+12 |         1.0000 |
| min        |      -6.79e+13 |       -60.7447 |      -3.58e+14 |       -77.1882 |
| 25%        |        -0.4066 |        -0.3996 |        -0.0034 |      -7.34e-16 |
| 50%        |        -0.0832 |        -0.0830 |       1.93e-09 |       4.17e-22 |
| 75%        |         0.2326 |         0.2271 |         0.0052 |       1.12e-15 |
| max        |       3.58e+14 |        60.4149 |       6.79e+13 |        14.6460 |

**Regression Analysis** (Python ~ Stata):

- **Model**: python = -0.1171 + 0.0000 * stata
- **R-squared**: 0.0000
- **N observations**: 2,323,705

| Coefficient |     Estimate |    Std Error | t-statistic |   p-value |
|-------------|--------------|--------------|-------------|----------|
| Intercept   |      -0.1171 |     7.70e-04 |   -152.1397 |     0.000 |
| Slope       |     1.53e-15 |     1.66e-16 |      9.2436 |     0.000 |

**Feedback**:
- Num observations with std_diff >= TOL_DIFF_1: 3539/2323705 (0.152%)
- Stata standard deviation: 4.64e+12

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

**Precision2**: 99th percentile diff = 8.79e-08 (tolerance: < 1.00e+00)

**Summary Statistics** (Common Observations):

| Statistic  |          Stata |         Python |     Difference | Std Difference |
|------------|----------------|----------------|----------------|----------------|
| count      |       1.39e+06 |       1.39e+06 |       1.39e+06 |       1.39e+06 |
| mean       |         0.0649 |         0.0649 |      -2.17e-10 |      -1.26e-10 |
| std        |         1.7181 |         1.7181 |       5.15e-08 |       3.00e-08 |
| min        |      -274.7972 |      -274.7972 |      -3.86e-06 |      -2.25e-06 |
| 25%        |        -0.0931 |        -0.0931 |      -7.10e-09 |      -4.13e-09 |
| 50%        |         0.1024 |         0.1024 |      -9.30e-11 |      -5.41e-11 |
| 75%        |         0.3403 |         0.3403 |       6.26e-09 |       3.65e-09 |
| max        |        82.0000 |        82.0000 |       5.00e-06 |       2.91e-06 |

**Regression Analysis** (Python ~ Stata):

- **Model**: python = -0.0000 + 1.0000 * stata
- **R-squared**: 1.0000
- **N observations**: 1,386,008

| Coefficient |     Estimate |    Std Error | t-statistic |   p-value |
|-------------|--------------|--------------|-------------|----------|
| Intercept   |    -3.44e-11 |     4.36e-11 |     -0.7901 |     0.429 |
| Slope       |       1.0000 |     2.53e-11 |    3.95e+10 |     0.000 |

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

**Precision2**: 99th percentile diff = 3.61e-08 (tolerance: < 1.00e+00)

**Summary Statistics** (Common Observations):

| Statistic  |          Stata |         Python |     Difference | Std Difference |
|------------|----------------|----------------|----------------|----------------|
| count      |    972933.0000 |    972933.0000 |    972933.0000 |    972933.0000 |
| mean       |       -35.2700 |       -35.2816 |        -0.0115 |      -2.09e-05 |
| std        |       553.4147 |       553.4348 |         8.0958 |         0.0146 |
| min        |    -87875.0000 |    -87875.0000 |     -3590.1192 |        -6.4872 |
| 25%        |       -19.5800 |       -19.5778 |      -4.39e-07 |      -7.93e-10 |
| 50%        |        -0.5030 |        -0.5022 |         0.0000 |         0.0000 |
| 75%        |        11.9556 |        11.9517 |       4.17e-07 |       7.53e-10 |
| max        |     24225.0000 |     24225.0000 |      1076.2586 |         1.9448 |

**Regression Analysis** (Python ~ Stata):

- **Model**: python = -0.0140 + 0.9999 * stata
- **R-squared**: 0.9998
- **N observations**: 972,933

| Coefficient |     Estimate |    Std Error | t-statistic |   p-value |
|-------------|--------------|--------------|-------------|----------|
| Intercept   |      -0.0140 |       0.0082 |     -1.7065 |     0.088 |
| Slope       |       0.9999 |     1.48e-05 |  67422.8889 |     0.000 |

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

**Precision2**: 99th percentile diff = 2.46e-09 (tolerance: < 1.00e+00)

**Summary Statistics** (Common Observations):

| Statistic  |          Stata |         Python |     Difference | Std Difference |
|------------|----------------|----------------|----------------|----------------|
| count      |       1.22e+06 |       1.22e+06 |       1.22e+06 |       1.22e+06 |
| mean       |        -0.0014 |            inf |            inf |            inf |
| std        |         3.1638 |            N/A |            N/A |            N/A |
| min        |      -154.1053 |      -154.1053 |        -0.4182 |        -0.1322 |
| 25%        |        -0.0024 |        -0.0024 |      -4.35e-11 |      -1.38e-11 |
| 50%        |       5.09e-04 |       5.09e-04 |         0.0000 |         0.0000 |
| 75%        |         0.0025 |         0.0025 |       4.51e-11 |       1.43e-11 |
| max        |       915.0000 |            inf |            inf |            inf |

**Regression Analysis** (Python ~ Stata):

- **Model**: python = inf + inf * stata
- **R-squared**: nan
- **N observations**: 1,222,769

| Coefficient |     Estimate |    Std Error | t-statistic |   p-value |
|-------------|--------------|--------------|-------------|----------|
| Intercept   |          nan |          nan |         nan |       nan |
| Slope       |          nan |          nan |         nan |       nan |

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

**Precision2**: 99th percentile diff = 4.75e-08 (tolerance: < 1.00e+00)

**Summary Statistics** (Common Observations):

| Statistic  |          Stata |         Python |     Difference | Std Difference |
|------------|----------------|----------------|----------------|----------------|
| count      |       2.32e+06 |       2.32e+06 |       2.32e+06 |       2.32e+06 |
| mean       |        -0.1913 |        -0.1911 |       1.93e-04 |       1.42e-05 |
| std        |        13.5569 |        13.5573 |         0.1244 |         0.0092 |
| min        |    -10442.0660 |    -10442.0669 |       -33.3274 |        -2.4583 |
| 25%        |        -0.6707 |        -0.6707 |      -2.36e-08 |      -1.74e-09 |
| 50%        |       2.18e-08 |       2.09e-16 |      -1.83e-10 |      -1.35e-11 |
| 75%        |         0.6469 |         0.6468 |       2.31e-08 |       1.70e-09 |
| max        |      1153.9985 |      1153.9983 |        92.3953 |         6.8153 |

**Regression Analysis** (Python ~ Stata):

- **Model**: python = 0.0002 + 1.0000 * stata
- **R-squared**: 0.9999
- **N observations**: 2,323,954

| Coefficient |     Estimate |    Std Error | t-statistic |   p-value |
|-------------|--------------|--------------|-------------|----------|
| Intercept   |     1.90e-04 |     8.16e-05 |      2.3234 |     0.020 |
| Slope       |       1.0000 |     6.02e-06 | 166173.7430 |     0.000 |

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

**Precision2**: 99th percentile diff = 5.53e-09 (tolerance: < 1.00e+00)

**Summary Statistics** (Common Observations):

| Statistic  |          Stata |         Python |     Difference | Std Difference |
|------------|----------------|----------------|----------------|----------------|
| count      |       2.41e+06 |       2.41e+06 |       2.41e+06 |       2.41e+06 |
| mean       |        23.3369 |        23.3368 |      -1.75e-05 |      -2.32e-08 |
| std        |       753.1756 |       753.1756 |         0.0071 |       9.38e-06 |
| min        |     -1760.3278 |     -1760.3277 |        -2.2385 |        -0.0030 |
| 25%        |         5.1076 |         5.1076 |      -1.57e-07 |      -2.09e-10 |
| 50%        |         8.0373 |         8.0372 |       2.54e-11 |       3.37e-14 |
| 75%        |        13.0989 |        13.0990 |       1.57e-07 |       2.09e-10 |
| max        |    445235.1900 |    445235.1727 |         2.0661 |         0.0027 |

**Regression Analysis** (Python ~ Stata):

- **Model**: python = -0.0000 + 1.0000 * stata
- **R-squared**: 1.0000
- **N observations**: 2,407,843

| Coefficient |     Estimate |    Std Error | t-statistic |   p-value |
|-------------|--------------|--------------|-------------|----------|
| Intercept   |    -1.74e-05 |     4.55e-06 |     -3.8232 |     0.000 |
| Slope       |       1.0000 |     6.04e-09 |    1.65e+08 |     0.000 |

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

**Precision2**: 99th percentile diff = 1.19e-15 (tolerance: < 1.00e+00)

**Summary Statistics** (Common Observations):

| Statistic  |          Stata |         Python |     Difference | Std Difference |
|------------|----------------|----------------|----------------|----------------|
| count      |       3.12e+06 |       3.12e+06 |       3.12e+06 |       3.12e+06 |
| mean       |       1.28e+07 |       1.28e+07 |         1.4629 |       2.57e-10 |
| std        |       5.69e+09 |       5.69e+09 |       644.0980 |       1.13e-07 |
| min        |      -4.06e+06 |      -4.06e+06 |     -3500.1904 |      -6.16e-07 |
| 25%        |        14.1395 |        14.1394 |      -5.84e-07 |      -1.03e-16 |
| 50%        |        16.2921 |        16.2921 |      -2.44e-10 |      -4.28e-20 |
| 75%        |        18.0605 |        18.0605 |       5.82e-07 |       1.02e-16 |
| max        |       2.88e+12 |       2.88e+12 |    325978.6533 |       5.73e-05 |

**Regression Analysis** (Python ~ Stata):

- **Model**: python = 0.0196 + 1.0000 * stata
- **R-squared**: 1.0000
- **N observations**: 3,124,663

| Coefficient |     Estimate |    Std Error | t-statistic |   p-value |
|-------------|--------------|--------------|-------------|----------|
| Intercept   |       0.0196 |       0.0166 |      1.1799 |     0.238 |
| Slope       |       1.0000 |     2.92e-12 |    3.43e+11 |     0.000 |

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

**Precision2**: 99th percentile diff = 0.00e+00 (tolerance: < 1.00e+00)

**Summary Statistics** (Common Observations):

| Statistic  |          Stata |         Python |     Difference | Std Difference |
|------------|----------------|----------------|----------------|----------------|
| count      |       4.05e+06 |       4.05e+06 |       4.05e+06 |       4.05e+06 |
| mean       |         0.0090 |         0.0095 |       4.69e-04 |         0.0050 |
| std        |         0.0946 |         0.0970 |         0.0217 |         0.2290 |
| min        |         0.0000 |         0.0000 |         0.0000 |         0.0000 |
| 25%        |         0.0000 |         0.0000 |         0.0000 |         0.0000 |
| 50%        |         0.0000 |         0.0000 |         0.0000 |         0.0000 |
| 75%        |         0.0000 |         0.0000 |         0.0000 |         0.0000 |
| max        |         1.0000 |         1.0000 |         1.0000 |        10.5750 |

**Regression Analysis** (Python ~ Stata):

- **Model**: python = 0.0005 + 0.9995 * stata
- **R-squared**: 0.9501
- **N observations**: 4,047,630

| Coefficient |     Estimate |    Std Error | t-statistic |   p-value |
|-------------|--------------|--------------|-------------|----------|
| Intercept   |     4.73e-04 |     1.08e-05 |     43.7858 |     0.000 |
| Slope       |       0.9995 |     1.14e-04 |   8781.2394 |     0.000 |

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

**Precision2**: 99th percentile diff = 8.43e-08 (tolerance: < 1.00e+00)

**Summary Statistics** (Common Observations):

| Statistic  |          Stata |         Python |     Difference | Std Difference |
|------------|----------------|----------------|----------------|----------------|
| count      |       1.72e+06 |       1.72e+06 |       1.72e+06 |       1.72e+06 |
| mean       |         0.0473 |         0.0472 |      -5.12e-05 |      -1.44e-04 |
| std        |         0.3560 |         0.3563 |         0.0224 |         0.0629 |
| min        |        -1.7990 |        -1.8000 |        -3.6900 |       -10.3663 |
| 25%        |        -0.0200 |        -0.0200 |      -5.55e-17 |      -1.56e-16 |
| 50%        |         0.0000 |         0.0000 |         0.0000 |         0.0000 |
| 75%        |         0.0700 |         0.0700 |       2.78e-17 |       7.80e-17 |
| max        |         2.6900 |         2.6900 |         2.7000 |         7.5851 |

**Regression Analysis** (Python ~ Stata):

- **Model**: python = -0.0000 + 0.9990 * stata
- **R-squared**: 0.9960
- **N observations**: 1,724,203

| Coefficient |     Estimate |    Std Error | t-statistic |   p-value |
|-------------|--------------|--------------|-------------|----------|
| Intercept   |    -2.00e-06 |     1.72e-05 |     -0.1160 |     0.908 |
| Slope       |       0.9990 |     4.79e-05 |  20848.8489 |     0.000 |

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

**Precision2**: 99th percentile diff = 1.01e-09 (tolerance: < 1.00e+00)

**Summary Statistics** (Common Observations):

| Statistic  |          Stata |         Python |     Difference | Std Difference |
|------------|----------------|----------------|----------------|----------------|
| count      |       1.95e+06 |       1.95e+06 |       1.95e+06 |       1.95e+06 |
| mean       |         2.7245 |         2.7242 |      -2.83e-04 |      -1.42e-06 |
| std        |       198.6832 |       198.6832 |         0.0805 |       4.05e-04 |
| min        |   -129751.1900 |   -129751.1900 |       -17.6700 |        -0.0889 |
| 25%        |         0.2400 |         0.2400 |         0.0000 |         0.0000 |
| 50%        |         1.0800 |         1.0800 |         0.0000 |         0.0000 |
| 75%        |         2.2600 |         2.2600 |         0.0000 |         0.0000 |
| max        |     30007.4900 |     30007.4900 |         9.2800 |         0.0467 |

**Regression Analysis** (Python ~ Stata):

- **Model**: python = -0.0003 + 1.0000 * stata
- **R-squared**: 1.0000
- **N observations**: 1,954,911

| Coefficient |     Estimate |    Std Error | t-statistic |   p-value |
|-------------|--------------|--------------|-------------|----------|
| Intercept   |    -2.82e-04 |     5.76e-05 |     -4.9012 |     0.000 |
| Slope       |       1.0000 |     2.90e-07 |    3.45e+06 |     0.000 |

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

**Precision2**: 99th percentile diff = 1.18e-07 (tolerance: < 1.00e+00)

**Summary Statistics** (Common Observations):

| Statistic  |          Stata |         Python |     Difference | Std Difference |
|------------|----------------|----------------|----------------|----------------|
| count      |    683893.0000 |    683893.0000 |    683893.0000 |    683893.0000 |
| mean       |        -0.0325 |        -0.0325 |       1.52e-10 |       1.96e-10 |
| std        |         0.7738 |         0.7738 |       7.28e-08 |       9.41e-08 |
| min        |      -334.6507 |      -334.6506 |      -1.82e-05 |      -2.36e-05 |
| 25%        |        -0.0239 |        -0.0239 |      -1.40e-09 |      -1.80e-09 |
| 50%        |        -0.0021 |        -0.0021 |         0.0000 |         0.0000 |
| 75%        |         0.0078 |         0.0078 |       1.38e-09 |       1.78e-09 |
| max        |        44.5372 |        44.5372 |       2.46e-05 |       3.18e-05 |

**Regression Analysis** (Python ~ Stata):

- **Model**: python = -0.0000 + 1.0000 * stata
- **R-squared**: 1.0000
- **N observations**: 683,893

| Coefficient |     Estimate |    Std Error | t-statistic |   p-value |
|-------------|--------------|--------------|-------------|----------|
| Intercept   |    -1.04e-09 |     8.11e-11 |    -12.8577 |     0.000 |
| Slope       |       1.0000 |     1.05e-10 |    9.55e+09 |     0.000 |

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

**Precision2**: 99th percentile diff = 0.00e+00 (tolerance: < 1.00e+00)

**Summary Statistics** (Common Observations):

| Statistic  |          Stata |         Python |     Difference | Std Difference |
|------------|----------------|----------------|----------------|----------------|
| count      |       4.05e+06 |       4.05e+06 |       4.05e+06 |       4.05e+06 |
| mean       |       158.4381 |       158.4381 |         0.0000 |         0.0000 |
| std        |       169.9697 |       169.9697 |         0.0000 |         0.0000 |
| min        |         1.0000 |         1.0000 |         0.0000 |         0.0000 |
| 25%        |        39.0000 |        39.0000 |         0.0000 |         0.0000 |
| 50%        |       100.0000 |       100.0000 |         0.0000 |         0.0000 |
| 75%        |       219.0000 |       219.0000 |         0.0000 |         0.0000 |
| max        |      1189.0000 |      1189.0000 |         0.0000 |         0.0000 |

**Regression Analysis** (Python ~ Stata):

- **Model**: python = 0.0000 + 1.0000 * stata
- **R-squared**: 1.0000
- **N observations**: 4,045,796

| Coefficient |     Estimate |    Std Error | t-statistic |   p-value |
|-------------|--------------|--------------|-------------|----------|
| Intercept   |     3.77e-11 |     2.04e-14 |   1847.3259 |     0.000 |
| Slope       |       1.0000 |     8.78e-17 |    1.14e+16 |     0.000 |

**Feedback**:
- Num observations with std_diff >= TOL_DIFF_1: 0/4045796 (0.000%)
- Stata standard deviation: 1.70e+02

---

### FirmAgeMom

**Status**: ✅ PASSED

**Test Results**:
- Test 1 - Column names: ✅ PASSED
- Test 2 - Superset check: ✅ PASSED
- Test 3 - Precision1 check: ✅ PASSED
- Test 4 - Precision2 check: ✅ PASSED

**Columns**: ['FirmAgeMom']

**Observations**:
- Stata:  550,434
- Python: 579,564
- Common: 550,434

**Precision1**: 0.000% obs with std_diff >= 1.00e-02 (tolerance: < 10%)

**Precision2**: 99th percentile diff = 9.31e-08 (tolerance: < 1.00e+00)

**Summary Statistics** (Common Observations):

| Statistic  |          Stata |         Python |     Difference | Std Difference |
|------------|----------------|----------------|----------------|----------------|
| count      |    550434.0000 |    550434.0000 |    550434.0000 |    550434.0000 |
| mean       |         0.0904 |         0.0904 |      -1.46e-12 |      -4.12e-12 |
| std        |         0.3547 |         0.3547 |       1.05e-08 |       2.97e-08 |
| min        |        -0.9374 |        -0.9374 |      -1.04e-06 |      -2.93e-06 |
| 25%        |        -0.0898 |        -0.0898 |      -2.60e-09 |      -7.33e-09 |
| 50%        |         0.0415 |         0.0415 |         0.0000 |         0.0000 |
| 75%        |         0.2113 |         0.2113 |       2.60e-09 |       7.33e-09 |
| max        |        27.4976 |        27.4976 |       9.60e-07 |       2.71e-06 |

**Regression Analysis** (Python ~ Stata):

- **Model**: python = -0.0000 + 1.0000 * stata
- **R-squared**: 1.0000
- **N observations**: 550,434

| Coefficient |     Estimate |    Std Error | t-statistic |   p-value |
|-------------|--------------|--------------|-------------|----------|
| Intercept   |    -2.83e-12 |     1.47e-11 |     -0.1927 |     0.847 |
| Slope       |       1.0000 |     4.01e-11 |    2.50e+10 |     0.000 |

**Feedback**:
- Num observations with std_diff >= TOL_DIFF_1: 0/550434 (0.000%)
- Stata standard deviation: 3.55e-01

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

**Precision2**: 99th percentile diff = 4.02e-08 (tolerance: < 1.00e+00)

**Summary Statistics** (Common Observations):

| Statistic  |          Stata |         Python |     Difference | Std Difference |
|------------|----------------|----------------|----------------|----------------|
| count      |       1.61e+06 |       1.61e+06 |       1.61e+06 |       1.61e+06 |
| mean       |         0.2221 |         0.2221 |      -7.84e-05 |      -5.52e-05 |
| std        |         1.4215 |         1.4213 |         0.0267 |         0.0188 |
| min        |         0.0000 |         0.0000 |       -14.8289 |       -10.4320 |
| 25%        |         0.0204 |         0.0204 |      -1.16e-09 |      -8.13e-10 |
| 50%        |         0.0476 |         0.0476 |      -4.84e-11 |      -3.41e-11 |
| 75%        |         0.1273 |         0.1273 |       4.62e-10 |       3.25e-10 |
| max        |       207.0000 |       207.0000 |        11.0000 |         7.7384 |

**Regression Analysis** (Python ~ Stata):

- **Model**: python = -0.0000 + 0.9997 * stata
- **R-squared**: 0.9996
- **N observations**: 1,614,371

| Coefficient |     Estimate |    Std Error | t-statistic |   p-value |
|-------------|--------------|--------------|-------------|----------|
| Intercept   |    -1.36e-05 |     2.13e-05 |     -0.6388 |     0.523 |
| Slope       |       0.9997 |     1.48e-05 |  67630.4185 |     0.000 |

**Feedback**:
- Num observations with std_diff >= TOL_DIFF_1: 1132/1614371 (0.070%)
- Stata standard deviation: 1.42e+00

---

### Frontier

**Status**: ✅ PASSED

**Test Results**:
- Test 1 - Column names: ✅ PASSED
- Test 2 - Superset check: ✅ PASSED
- Test 3 - Precision1 check: ✅ PASSED
- Test 4 - Precision2 check: ✅ PASSED

**Columns**: ['Frontier']

**Observations**:
- Stata:  1,221,161
- Python: 1,221,161
- Common: 1,221,161

**Precision1**: 0.000% obs with std_diff >= 1.00e-02 (tolerance: < 10%)

**Precision2**: 99th percentile diff = 6.48e-07 (tolerance: < 1.00e+00)

**Summary Statistics** (Common Observations):

| Statistic  |          Stata |         Python |     Difference | Std Difference |
|------------|----------------|----------------|----------------|----------------|
| count      |       1.22e+06 |      8535.0000 |      8535.0000 |      8535.0000 |
| mean       |        -0.0086 |        -0.0136 |      -3.00e-09 |      -3.07e-09 |
| std        |         0.9776 |         0.4955 |       2.11e-07 |       2.16e-07 |
| min        |       -11.5532 |        -3.1725 |      -9.81e-07 |      -1.00e-06 |
| 25%        |        -0.5722 |        -0.2924 |      -1.34e-07 |      -1.37e-07 |
| 50%        |         0.0113 |         0.0016 |       8.97e-10 |       9.18e-10 |
| 75%        |         0.5788 |         0.2874 |       1.34e-07 |       1.37e-07 |
| max        |        23.1422 |         1.8399 |       8.43e-07 |       8.63e-07 |

**Regression Analysis** (Python ~ Stata):

- **Model**: python = -0.0000 + 1.0000 * stata
- **R-squared**: 1.0000
- **N observations**: 8,535

| Coefficient |     Estimate |    Std Error | t-statistic |   p-value |
|-------------|--------------|--------------|-------------|----------|
| Intercept   |    -1.98e-09 |     2.25e-09 |     -0.8819 |     0.378 |
| Slope       |       1.0000 |     4.54e-09 |    2.20e+08 |     0.000 |

**Feedback**:
- Num observations with std_diff >= TOL_DIFF_1: 0/1221161 (0.000%)
- Stata standard deviation: 9.78e-01

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

**Precision2**: 99th percentile diff = 1.10e-07 (tolerance: < 1.00e+00)

**Summary Statistics** (Common Observations):

| Statistic  |          Stata |         Python |     Difference | Std Difference |
|------------|----------------|----------------|----------------|----------------|
| count      |       2.97e+06 |       2.97e+06 |       2.97e+06 |       2.97e+06 |
| mean       |         0.3280 |         0.3281 |       5.35e-06 |       1.15e-05 |
| std        |         0.4633 |         0.4633 |         0.0022 |         0.0047 |
| min        |      -134.2381 |      -134.2381 |        -0.0428 |        -0.0924 |
| 25%        |         0.1554 |         0.1555 |      -5.79e-09 |      -1.25e-08 |
| 50%        |         0.3051 |         0.3051 |         0.0000 |         0.0000 |
| 75%        |         0.4835 |         0.4835 |       5.76e-09 |       1.24e-08 |
| max        |        12.9441 |        12.9441 |         1.0666 |         2.3024 |

**Regression Analysis** (Python ~ Stata):

- **Model**: python = 0.0000 + 1.0000 * stata
- **R-squared**: 1.0000
- **N observations**: 2,970,775

| Coefficient |     Estimate |    Std Error | t-statistic |   p-value |
|-------------|--------------|--------------|-------------|----------|
| Intercept   |     1.50e-05 |     1.55e-06 |      9.6830 |     0.000 |
| Slope       |       1.0000 |     2.73e-06 | 366633.7773 |     0.000 |

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

**Precision2**: 99th percentile diff = 0.00e+00 (tolerance: < 1.00e+00)

**Summary Statistics** (Common Observations):

| Statistic  |          Stata |         Python |     Difference | Std Difference |
|------------|----------------|----------------|----------------|----------------|
| count      |    334058.0000 |    334058.0000 |    334058.0000 |    334058.0000 |
| mean       |         9.0443 |         9.0443 |         0.0000 |         0.0000 |
| std        |         2.5733 |         2.5733 |         0.0000 |         0.0000 |
| min        |         5.0000 |         5.0000 |         0.0000 |         0.0000 |
| 25%        |         7.0000 |         7.0000 |         0.0000 |         0.0000 |
| 50%        |         9.0000 |         9.0000 |         0.0000 |         0.0000 |
| 75%        |        11.0000 |        11.0000 |         0.0000 |         0.0000 |
| max        |        14.0000 |        14.0000 |         0.0000 |         0.0000 |

**Regression Analysis** (Python ~ Stata):

- **Model**: python = 0.0000 + 1.0000 * stata
- **R-squared**: 1.0000
- **N observations**: 334,058

| Coefficient |     Estimate |    Std Error | t-statistic |   p-value |
|-------------|--------------|--------------|-------------|----------|
| Intercept   |     2.54e-12 |     1.14e-14 |    222.5103 |     0.000 |
| Slope       |       1.0000 |     1.22e-15 |    8.23e+14 |     0.000 |

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

**Precision2**: 99th percentile diff = 1.38e-07 (tolerance: < 1.00e+00)

**Summary Statistics** (Common Observations):

| Statistic  |          Stata |         Python |     Difference | Std Difference |
|------------|----------------|----------------|----------------|----------------|
| count      |    898855.0000 |    898855.0000 |    898855.0000 |    898855.0000 |
| mean       |         0.0959 |         0.0959 |      -2.40e-11 |      -5.06e-11 |
| std        |         0.4754 |         0.4754 |       1.39e-08 |       2.92e-08 |
| min        |        -5.4159 |        -5.4159 |      -2.35e-07 |      -4.95e-07 |
| 25%        |        -0.0747 |        -0.0747 |      -3.07e-09 |      -6.46e-09 |
| 50%        |         0.0773 |         0.0773 |         0.0000 |         0.0000 |
| 75%        |         0.2478 |         0.2478 |       3.13e-09 |       6.59e-09 |
| max        |         7.6737 |         7.6737 |       2.71e-07 |       5.71e-07 |

**Regression Analysis** (Python ~ Stata):

- **Model**: python = 0.0000 + 1.0000 * stata
- **R-squared**: 1.0000
- **N observations**: 898,855

| Coefficient |     Estimate |    Std Error | t-statistic |   p-value |
|-------------|--------------|--------------|-------------|----------|
| Intercept   |     4.10e-11 |     1.50e-11 |      2.7422 |     0.006 |
| Slope       |       1.0000 |     3.08e-11 |    3.24e+10 |     0.000 |

**Feedback**:
- Num observations with std_diff >= TOL_DIFF_1: 0/898855 (0.000%)
- Stata standard deviation: 4.75e-01

---

### GrLTNOA

**Status**: ✅ PASSED

**Test Results**:
- Test 1 - Column names: ✅ PASSED
- Test 2 - Superset check: ✅ PASSED
- Test 3 - Precision1 check: ✅ PASSED
- Test 4 - Precision2 check: ✅ PASSED

**Columns**: ['GrLTNOA']

**Observations**:
- Stata:  3,219,259
- Python: 3,235,740
- Common: 3,219,235

**Precision1**: 0.008% obs with std_diff >= 1.00e-02 (tolerance: < 10%)

**Precision2**: 99th percentile diff = 2.82e-08 (tolerance: < 1.00e+00)

**Summary Statistics** (Common Observations):

| Statistic  |          Stata |         Python |     Difference | Std Difference |
|------------|----------------|----------------|----------------|----------------|
| count      |       3.22e+06 |       3.22e+06 |       3.22e+06 |       3.22e+06 |
| mean       |         0.0277 |         0.0277 |       2.42e-07 |       4.41e-07 |
| std        |         0.5488 |         0.5488 |       4.80e-04 |       8.75e-04 |
| min        |      -166.3113 |      -166.3113 |        -0.1253 |        -0.2284 |
| 25%        |        -0.0128 |        -0.0128 |      -8.67e-10 |      -1.58e-09 |
| 50%        |         0.0255 |         0.0255 |       2.96e-13 |       5.40e-13 |
| 75%        |         0.0758 |         0.0758 |       8.75e-10 |       1.59e-09 |
| max        |        51.4748 |        51.4748 |         0.1105 |         0.2013 |

**Regression Analysis** (Python ~ Stata):

- **Model**: python = 0.0000 + 1.0000 * stata
- **R-squared**: 1.0000
- **N observations**: 3,219,235

| Coefficient |     Estimate |    Std Error | t-statistic |   p-value |
|-------------|--------------|--------------|-------------|----------|
| Intercept   |     3.26e-07 |     2.68e-07 |      1.2159 |     0.224 |
| Slope       |       1.0000 |     4.88e-07 |    2.05e+06 |     0.000 |

**Feedback**:
- Num observations with std_diff >= TOL_DIFF_1: 252/3219235 (0.008%)
- Stata standard deviation: 5.49e-01

---

### GrSaleToGrInv

**Status**: ✅ PASSED

**Test Results**:
- Test 1 - Column names: ✅ PASSED
- Test 2 - Superset check: ✅ PASSED
- Test 3 - Precision1 check: ✅ PASSED
- Test 4 - Precision2 check: ✅ PASSED

**Columns**: ['GrSaleToGrInv']

**Observations**:
- Stata:  2,532,290
- Python: 2,545,662
- Common: 2,532,290

**Precision1**: 0.039% obs with std_diff >= 1.00e-02 (tolerance: < 10%)

**Precision2**: 99th percentile diff = 2.37e-09 (tolerance: < 1.00e+00)

**Summary Statistics** (Common Observations):

| Statistic  |          Stata |         Python |     Difference | Std Difference |
|------------|----------------|----------------|----------------|----------------|
| count      |       2.53e+06 |       2.53e+06 |       2.53e+06 |       2.53e+06 |
| mean       |        -0.6004 |        -0.6010 |      -5.57e-04 |      -5.64e-06 |
| std        |        98.7042 |        98.7036 |         0.3541 |         0.0036 |
| min        |    -27478.1970 |    -27478.1975 |      -142.5476 |        -1.4442 |
| 25%        |        -0.1477 |        -0.1476 |      -3.21e-09 |      -3.26e-11 |
| 50%        |         0.0238 |         0.0239 |         0.0000 |         0.0000 |
| 75%        |         0.2039 |         0.2041 |       3.26e-09 |       3.30e-11 |
| max        |     16243.9730 |     16243.9730 |        48.0774 |         0.4871 |

**Regression Analysis** (Python ~ Stata):

- **Model**: python = -0.0006 + 1.0000 * stata
- **R-squared**: 1.0000
- **N observations**: 2,532,290

| Coefficient |     Estimate |    Std Error | t-statistic |   p-value |
|-------------|--------------|--------------|-------------|----------|
| Intercept   |    -5.65e-04 |     2.23e-04 |     -2.5381 |     0.011 |
| Slope       |       1.0000 |     2.25e-06 | 443592.1695 |     0.000 |

**Feedback**:
- Num observations with std_diff >= TOL_DIFF_1: 986/2532290 (0.039%)
- Stata standard deviation: 9.87e+01

---

### GrSaleToGrOverhead

**Status**: ✅ PASSED

**Test Results**:
- Test 1 - Column names: ✅ PASSED
- Test 2 - Superset check: ✅ PASSED
- Test 3 - Precision1 check: ✅ PASSED
- Test 4 - Precision2 check: ✅ PASSED

**Columns**: ['GrSaleToGrOverhead']

**Observations**:
- Stata:  2,668,375
- Python: 2,681,589
- Common: 2,668,315

**Precision1**: 0.017% obs with std_diff >= 1.00e-02 (tolerance: < 10%)

**Precision2**: 99th percentile diff = 7.75e-10 (tolerance: < 1.00e+00)

**Summary Statistics** (Common Observations):

| Statistic  |          Stata |         Python |     Difference | Std Difference |
|------------|----------------|----------------|----------------|----------------|
| count      |       2.67e+06 |       2.67e+06 |       2.67e+06 |       2.67e+06 |
| mean       |         0.2114 |         0.2127 |         0.0013 |       9.86e-06 |
| std        |       134.4909 |       134.4930 |         0.8887 |         0.0066 |
| min        |    -35415.9490 |    -35415.9507 |      -153.7168 |        -1.1430 |
| 25%        |        -0.1013 |        -0.1012 |      -1.73e-09 |      -1.29e-11 |
| 50%        |        -0.0032 |        -0.0031 |      -1.18e-12 |      -8.76e-15 |
| 75%        |         0.0962 |         0.0965 |       1.76e-09 |       1.31e-11 |
| max        |     51774.7580 |     51774.7570 |       336.9123 |         2.5051 |

**Regression Analysis** (Python ~ Stata):

- **Model**: python = 0.0013 + 1.0000 * stata
- **R-squared**: 1.0000
- **N observations**: 2,668,315

| Coefficient |     Estimate |    Std Error | t-statistic |   p-value |
|-------------|--------------|--------------|-------------|----------|
| Intercept   |       0.0013 |     5.44e-04 |      2.4392 |     0.015 |
| Slope       |       1.0000 |     4.05e-06 | 247195.7137 |     0.000 |

**Feedback**:
- Num observations with std_diff >= TOL_DIFF_1: 466/2668315 (0.017%)
- Stata standard deviation: 1.34e+02

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

**Precision2**: 99th percentile diff = 6.98e-04 (tolerance: < 1.00e+00)

**Summary Statistics** (Common Observations):

| Statistic  |          Stata |         Python |     Difference | Std Difference |
|------------|----------------|----------------|----------------|----------------|
| count      |       3.16e+06 |       3.16e+06 |       3.16e+06 |       3.16e+06 |
| mean       |         0.3294 |         0.3293 |      -7.55e-05 |      -2.72e-04 |
| std        |         0.2778 |         0.2776 |         0.0102 |         0.0368 |
| min        |         0.0000 |         0.0000 |        -2.2031 |        -7.9297 |
| 25%        |         0.1184 |         0.1185 |      -2.41e-09 |      -8.67e-09 |
| 50%        |         0.2537 |         0.2537 |         0.0000 |         0.0000 |
| 75%        |         0.4723 |         0.4722 |       2.70e-09 |       9.73e-09 |
| max        |         5.5471 |         4.3717 |         0.6667 |         2.3995 |

**Regression Analysis** (Python ~ Stata):

- **Model**: python = 0.0005 + 0.9983 * stata
- **R-squared**: 0.9986
- **N observations**: 3,158,336

| Coefficient |     Estimate |    Std Error | t-statistic |   p-value |
|-------------|--------------|--------------|-------------|----------|
| Intercept   |     4.79e-04 |     8.91e-06 |     53.7839 |     0.000 |
| Slope       |       0.9983 |     2.07e-05 |  48282.1386 |     0.000 |

**Feedback**:
- Num observations with std_diff >= TOL_DIFF_1: 24846/3158336 (0.787%)
- Stata standard deviation: 2.78e-01

---

### HerfAsset

**Status**: ✅ PASSED

**Test Results**:
- Test 1 - Column names: ✅ PASSED
- Test 2 - Superset check: ✅ PASSED
- Test 3 - Precision1 check: ✅ PASSED
- Test 4 - Precision2 check: ✅ PASSED

**Columns**: ['HerfAsset']

**Observations**:
- Stata:  2,547,057
- Python: 2,553,214
- Common: 2,547,057

**Precision1**: 1.444% obs with std_diff >= 1.00e-02 (tolerance: < 10%)

**Precision2**: 99th percentile diff = 2.94e-02 (tolerance: < 1.00e+00)

**Summary Statistics** (Common Observations):

| Statistic  |          Stata |         Python |     Difference | Std Difference |
|------------|----------------|----------------|----------------|----------------|
| count      |       2.55e+06 |       2.55e+06 |       2.55e+06 |       2.55e+06 |
| mean       |         0.3431 |         0.3429 |      -1.26e-04 |      -4.52e-04 |
| std        |         0.2778 |         0.2776 |         0.0096 |         0.0344 |
| min        |         0.0162 |         0.0162 |        -0.6447 |        -2.3206 |
| 25%        |         0.1214 |         0.1215 |      -2.52e-09 |      -9.08e-09 |
| 50%        |         0.2657 |         0.2657 |         0.0000 |         0.0000 |
| 75%        |         0.4885 |         0.4884 |       2.91e-09 |       1.05e-08 |
| max        |         1.0000 |         1.0000 |         0.6436 |         2.3165 |

**Regression Analysis** (Python ~ Stata):

- **Model**: python = 0.0004 + 0.9985 * stata
- **R-squared**: 0.9988
- **N observations**: 2,547,057

| Coefficient |     Estimate |    Std Error | t-statistic |   p-value |
|-------------|--------------|--------------|-------------|----------|
| Intercept   |     3.78e-04 |     9.50e-06 |     39.8123 |     0.000 |
| Slope       |       0.9985 |     2.15e-05 |  46398.4453 |     0.000 |

**Feedback**:
- Num observations with std_diff >= TOL_DIFF_1: 36791/2547057 (1.444%)
- Stata standard deviation: 2.78e-01

---

### HerfBE

**Status**: ✅ PASSED

**Test Results**:
- Test 1 - Column names: ✅ PASSED
- Test 2 - Superset check: ✅ PASSED
- Test 3 - Precision1 check: ✅ PASSED
- Test 4 - Precision2 check: ✅ PASSED

**Columns**: ['HerfBE']

**Observations**:
- Stata:  2,547,057
- Python: 2,553,214
- Common: 2,547,057

**Precision1**: 0.001% obs with std_diff >= 1.00e-02 (tolerance: < 10%)

**Precision2**: 99th percentile diff = 1.38e-06 (tolerance: < 1.00e+00)

**Summary Statistics** (Common Observations):

| Statistic  |          Stata |         Python |     Difference | Std Difference |
|------------|----------------|----------------|----------------|----------------|
| count      |       2.55e+06 |       2.55e+06 |       2.55e+06 |       2.55e+06 |
| mean       |        70.1127 |        70.1093 |        -0.0034 |      -5.07e-07 |
| std        |      6716.9685 |      6717.1722 |         1.5384 |       2.29e-04 |
| min        |         0.0000 |         0.0000 |      -636.7797 |        -0.0948 |
| 25%        |         0.1251 |         0.1252 |      -2.57e-09 |      -3.82e-13 |
| 50%        |         0.2675 |         0.2675 |         0.0000 |         0.0000 |
| 75%        |         0.5118 |         0.5117 |       2.67e-09 |       3.97e-13 |
| max        |    859657.6583 |    859686.7510 |        62.9135 |         0.0094 |

**Regression Analysis** (Python ~ Stata):

- **Model**: python = -0.0055 + 1.0000 * stata
- **R-squared**: 1.0000
- **N observations**: 2,547,057

| Coefficient |     Estimate |    Std Error | t-statistic |   p-value |
|-------------|--------------|--------------|-------------|----------|
| Intercept   |      -0.0055 |     9.56e-04 |     -5.7892 |     0.000 |
| Slope       |       1.0000 |     1.42e-07 |    7.03e+06 |     0.000 |

**Feedback**:
- Num observations with std_diff >= TOL_DIFF_1: 32/2547057 (0.001%)
- Stata standard deviation: 6.72e+03

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

**Precision2**: 99th percentile diff = 2.72e-07 (tolerance: < 1.00e+00)

**Summary Statistics** (Common Observations):

| Statistic  |          Stata |         Python |     Difference | Std Difference |
|------------|----------------|----------------|----------------|----------------|
| count      |       5.00e+06 |       5.00e+06 |       5.00e+06 |       5.00e+06 |
| mean       |         0.7624 |         0.7624 |      -5.38e-10 |      -1.61e-09 |
| std        |         0.3336 |         0.3336 |       2.93e-08 |       8.80e-08 |
| min        |       1.76e-04 |       1.76e-04 |      -7.54e-06 |      -2.26e-05 |
| 25%        |         0.6090 |         0.6090 |      -1.58e-08 |      -4.72e-08 |
| 50%        |         0.8130 |         0.8130 |         0.0000 |         0.0000 |
| 75%        |         0.9416 |         0.9416 |       1.49e-08 |       4.47e-08 |
| max        |       262.3832 |       262.3832 |       1.02e-05 |       3.07e-05 |

**Regression Analysis** (Python ~ Stata):

- **Model**: python = -0.0000 + 1.0000 * stata
- **R-squared**: 1.0000
- **N observations**: 4,995,429

| Coefficient |     Estimate |    Std Error | t-statistic |   p-value |
|-------------|--------------|--------------|-------------|----------|
| Intercept   |    -8.69e-10 |     3.28e-11 |    -26.5324 |     0.000 |
| Slope       |       1.0000 |     3.94e-11 |    2.54e+10 |     0.000 |

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

**Precision2**: 99th percentile diff = 9.92e-08 (tolerance: < 1.00e+00)

**Summary Statistics** (Common Observations):

| Statistic  |          Stata |         Python |     Difference | Std Difference |
|------------|----------------|----------------|----------------|----------------|
| count      |      8842.0000 |      8842.0000 |      8842.0000 |      8842.0000 |
| mean       |        84.7349 |        84.7349 |      -3.65e-08 |      -3.62e-10 |
| std        |       100.7681 |       100.7681 |       2.76e-06 |       2.74e-08 |
| min        |         0.0000 |         0.0000 |      -1.00e-05 |      -9.92e-08 |
| 25%        |        55.0040 |        55.0040 |         0.0000 |         0.0000 |
| 50%        |        95.6820 |        95.6820 |         0.0000 |         0.0000 |
| 75%        |       114.8325 |       114.8325 |         0.0000 |         0.0000 |
| max        |      7896.3999 |      7896.4000 |       1.00e-04 |       9.92e-07 |

**Regression Analysis** (Python ~ Stata):

- **Model**: python = -0.0000 + 1.0000 * stata
- **R-squared**: 1.0000
- **N observations**: 8,842

| Coefficient |     Estimate |    Std Error | t-statistic |   p-value |
|-------------|--------------|--------------|-------------|----------|
| Intercept   |    -1.10e-06 |     3.41e-08 |    -32.3318 |     0.000 |
| Slope       |       1.0000 |     2.59e-10 |    3.86e+09 |     0.000 |

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
- Python: 4,980,936
- Common: 4,980,936

**Precision1**: 0.021% obs with std_diff >= 1.00e-02 (tolerance: < 10%)

**Precision2**: 99th percentile diff = 1.60e-03 (tolerance: < 1.00e+00)

**Summary Statistics** (Common Observations):

| Statistic  |          Stata |         Python |     Difference | Std Difference |
|------------|----------------|----------------|----------------|----------------|
| count      |       4.98e+06 |       4.98e+06 |       4.98e+06 |       4.98e+06 |
| mean       |         0.0253 |         0.0253 |      -1.29e-07 |      -4.53e-06 |
| std        |         0.0285 |         0.0285 |       1.56e-05 |       5.49e-04 |
| min        |         0.0000 |         0.0000 |        -0.0176 |        -0.6184 |
| 25%        |         0.0103 |         0.0103 |      -2.78e-17 |      -9.74e-16 |
| 50%        |         0.0180 |         0.0180 |         0.0000 |         0.0000 |
| 75%        |         0.0312 |         0.0312 |       2.78e-17 |       9.74e-16 |
| max        |         7.8173 |         7.7997 |         0.0036 |         0.1266 |

**Regression Analysis** (Python ~ Stata):

- **Model**: python = 0.0000 + 1.0000 * stata
- **R-squared**: 1.0000
- **N observations**: 4,980,936

| Coefficient |     Estimate |    Std Error | t-statistic |   p-value |
|-------------|--------------|--------------|-------------|----------|
| Intercept   |     7.08e-07 |     9.36e-09 |     75.6555 |     0.000 |
| Slope       |       1.0000 |     2.46e-07 |    4.07e+06 |     0.000 |

**Feedback**:
- Num observations with std_diff >= TOL_DIFF_1: 1055/4980936 (0.021%)
- Stata standard deviation: 2.85e-02

---

### IdioVolAHT

**Status**: ✅ PASSED

**Test Results**:
- Test 1 - Column names: ✅ PASSED
- Test 2 - Superset check: ✅ PASSED
- Test 3 - Precision1 check: ✅ PASSED
- Test 4 - Precision2 check: ✅ PASSED

**Columns**: ['IdioVolAHT']

**Observations**:
- Stata:  4,849,170
- Python: 4,853,953
- Common: 4,842,253

**Precision1**: 1.110% obs with std_diff >= 1.00e-02 (tolerance: < 10%)

**Precision2**: 99th percentile diff = 1.21e-02 (tolerance: < 1.00e+00)

**Summary Statistics** (Common Observations):

| Statistic  |          Stata |         Python |     Difference | Std Difference |
|------------|----------------|----------------|----------------|----------------|
| count      |       4.84e+06 |       4.84e+06 |       4.84e+06 |       4.84e+06 |
| mean       |         0.0300 |         0.0300 |      -2.46e-05 |      -9.34e-04 |
| std        |         0.0264 |         0.0263 |         0.0018 |         0.0675 |
| min        |       1.02e-05 |       1.02e-05 |        -0.5751 |       -21.8130 |
| 25%        |         0.0142 |         0.0142 |      -2.78e-17 |      -1.05e-15 |
| 50%        |         0.0232 |         0.0232 |         0.0000 |         0.0000 |
| 75%        |         0.0379 |         0.0378 |       3.12e-17 |       1.18e-15 |
| max        |         2.5092 |         2.5092 |         0.3178 |        12.0535 |

**Regression Analysis** (Python ~ Stata):

- **Model**: python = 0.0001 + 0.9966 * stata
- **R-squared**: 0.9954
- **N observations**: 4,842,253

| Coefficient |     Estimate |    Std Error | t-statistic |   p-value |
|-------------|--------------|--------------|-------------|----------|
| Intercept   |     7.61e-05 |     1.22e-06 |     62.1472 |     0.000 |
| Slope       |       0.9966 |     3.07e-05 |  32511.0140 |     0.000 |

**Feedback**:
- Num observations with std_diff >= TOL_DIFF_1: 53773/4842253 (1.110%)
- Stata standard deviation: 2.64e-02

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

**Precision2**: 99th percentile diff = 1.85e-08 (tolerance: < 1.00e+00)

**Summary Statistics** (Common Observations):

| Statistic  |          Stata |         Python |     Difference | Std Difference |
|------------|----------------|----------------|----------------|----------------|
| count      |       4.28e+06 |       4.28e+06 |       4.28e+06 |       4.28e+06 |
| mean       |       8.77e-06 |       8.77e-06 |       2.76e-15 |       1.68e-11 |
| std        |       1.64e-04 |       1.64e-04 |       5.46e-12 |       3.32e-08 |
| min        |         0.0000 |         0.0000 |      -4.04e-09 |      -2.46e-05 |
| 25%        |       7.73e-09 |       7.73e-09 |      -2.01e-15 |      -1.22e-11 |
| 50%        |       1.27e-07 |       1.27e-07 |      -4.76e-21 |      -2.90e-17 |
| 75%        |       1.47e-06 |       1.47e-06 |       2.01e-15 |       1.22e-11 |
| max        |         0.0761 |         0.0761 |       3.75e-09 |       2.28e-05 |

**Regression Analysis** (Python ~ Stata):

- **Model**: python = 0.0000 + 1.0000 * stata
- **R-squared**: 1.0000
- **N observations**: 4,278,152

| Coefficient |     Estimate |    Std Error | t-statistic |   p-value |
|-------------|--------------|--------------|-------------|----------|
| Intercept   |     3.71e-15 |     2.64e-15 |      1.4041 |     0.160 |
| Slope       |       1.0000 |     1.61e-11 |    6.22e+10 |     0.000 |

**Feedback**:
- Num observations with std_diff >= TOL_DIFF_1: 0/4278152 (0.000%)
- Stata standard deviation: 1.64e-04

---

### IndMom

**Status**: ✅ PASSED

**Test Results**:
- Test 1 - Column names: ✅ PASSED
- Test 2 - Superset check: ✅ PASSED
- Test 3 - Precision1 check: ✅ PASSED
- Test 4 - Precision2 check: ✅ PASSED

**Columns**: ['IndMom']

**Observations**:
- Stata:  4,043,138
- Python: 4,044,574
- Common: 4,043,138

**Precision1**: 3.278% obs with std_diff >= 1.00e-02 (tolerance: < 10%)

**Precision2**: 99th percentile diff = 2.92e-01 (tolerance: < 1.00e+00)

**Summary Statistics** (Common Observations):

| Statistic  |          Stata |         Python |     Difference | Std Difference |
|------------|----------------|----------------|----------------|----------------|
| count      |       4.04e+06 |       4.04e+06 |       4.04e+06 |       4.04e+06 |
| mean       |         0.0857 |         0.0841 |        -0.0016 |        -0.0093 |
| std        |         0.1736 |         0.1711 |         0.0184 |         0.1062 |
| min        |        -0.9265 |        -0.9265 |        -1.2736 |        -7.3369 |
| 25%        |        -0.0099 |        -0.0104 |      -3.43e-08 |      -1.97e-07 |
| 50%        |         0.0775 |         0.0767 |      -1.39e-09 |      -8.03e-09 |
| 75%        |         0.1676 |         0.1662 |       3.34e-09 |       1.92e-08 |
| max        |        10.5068 |        10.5068 |         0.1070 |         0.6162 |

**Regression Analysis** (Python ~ Stata):

- **Model**: python = 0.0001 + 0.9801 * stata
- **R-squared**: 0.9888
- **N observations**: 4,043,138

| Coefficient |     Estimate |    Std Error | t-statistic |   p-value |
|-------------|--------------|--------------|-------------|----------|
| Intercept   |     9.54e-05 |     1.00e-05 |      9.4990 |     0.000 |
| Slope       |       0.9801 |     5.19e-05 |  18889.0096 |     0.000 |

**Feedback**:
- Num observations with std_diff >= TOL_DIFF_1: 132529/4043138 (3.278%)
- Stata standard deviation: 1.74e-01

---

### IndRetBig

**Status**: ✅ PASSED

**Test Results**:
- Test 1 - Column names: ✅ PASSED
- Test 2 - Superset check: ✅ PASSED
- Test 3 - Precision1 check: ✅ PASSED
- Test 4 - Precision2 check: ✅ PASSED

**Columns**: ['IndRetBig']

**Observations**:
- Stata:  2,607,795
- Python: 2,616,695
- Common: 2,602,394

**Precision1**: 6.699% obs with std_diff >= 1.00e-02 (tolerance: < 10%)

**Precision2**: 99th percentile diff = 1.01e-01 (tolerance: < 1.00e+00)

**Summary Statistics** (Common Observations):

| Statistic  |          Stata |         Python |     Difference | Std Difference |
|------------|----------------|----------------|----------------|----------------|
| count      |       2.60e+06 |       2.60e+06 |       2.60e+06 |       2.60e+06 |
| mean       |         0.0180 |         0.0180 |       1.34e-06 |       1.90e-05 |
| std        |         0.0704 |         0.0704 |         0.0021 |         0.0299 |
| min        |        -0.4860 |        -0.4717 |        -0.1171 |        -1.6643 |
| 25%        |        -0.0206 |        -0.0206 |      -2.78e-17 |      -3.94e-16 |
| 50%        |         0.0176 |         0.0177 |         0.0000 |         0.0000 |
| 75%        |         0.0554 |         0.0554 |       2.78e-17 |       3.94e-16 |
| max        |         1.8831 |         1.8831 |         0.2476 |         3.5177 |

**Regression Analysis** (Python ~ Stata):

- **Model**: python = 0.0000 + 0.9998 * stata
- **R-squared**: 0.9991
- **N observations**: 2,602,394

| Coefficient |     Estimate |    Std Error | t-statistic |   p-value |
|-------------|--------------|--------------|-------------|----------|
| Intercept   |     5.27e-06 |     1.35e-06 |      3.9202 |     0.000 |
| Slope       |       0.9998 |     1.85e-05 |  53985.8175 |     0.000 |

**Feedback**:
- Num observations with std_diff >= TOL_DIFF_1: 174345/2602394 (6.699%)
- Stata standard deviation: 7.04e-02

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

**Precision2**: 99th percentile diff = 1.04e-07 (tolerance: < 1.00e+00)

**Summary Statistics** (Common Observations):

| Statistic  |          Stata |         Python |     Difference | Std Difference |
|------------|----------------|----------------|----------------|----------------|
| count      |       3.69e+06 |       3.69e+06 |       3.69e+06 |       3.69e+06 |
| mean       |         0.0700 |         0.0700 |      -8.55e-12 |      -1.77e-11 |
| std        |         0.4819 |         0.4819 |       1.37e-08 |       2.85e-08 |
| min        |        -1.0000 |        -1.0000 |      -2.15e-06 |      -4.47e-06 |
| 25%        |        -0.1555 |        -0.1555 |      -3.20e-09 |      -6.64e-09 |
| 50%        |         0.0226 |         0.0226 |         0.0000 |         0.0000 |
| 75%        |         0.2110 |         0.2110 |       3.21e-09 |       6.65e-09 |
| max        |        80.0474 |        80.0474 |       1.27e-06 |       2.65e-06 |

**Regression Analysis** (Python ~ Stata):

- **Model**: python = 0.0000 + 1.0000 * stata
- **R-squared**: 1.0000
- **N observations**: 3,686,625

| Coefficient |     Estimate |    Std Error | t-statistic |   p-value |
|-------------|--------------|--------------|-------------|----------|
| Intercept   |     2.92e-11 |     7.22e-12 |      4.0433 |     0.000 |
| Slope       |       1.0000 |     1.48e-11 |    6.74e+10 |     0.000 |

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

**Precision2**: 99th percentile diff = 3.74e-07 (tolerance: < 1.00e+00)

**Summary Statistics** (Common Observations):

| Statistic  |          Stata |         Python |     Difference | Std Difference |
|------------|----------------|----------------|----------------|----------------|
| count      |       1.73e+06 |       1.73e+06 |       1.73e+06 |       1.73e+06 |
| mean       |       1.02e-06 |       1.22e-06 |       2.05e-07 |       2.72e-07 |
| std        |         0.7511 |         0.7511 |       1.75e-04 |       2.33e-04 |
| min        |        -5.6063 |        -5.6063 |        -0.0179 |        -0.0238 |
| 25%        |        -0.4156 |        -0.4156 |      -2.43e-08 |      -3.23e-08 |
| 50%        |        -0.0282 |        -0.0282 |       1.42e-10 |       1.89e-10 |
| 75%        |         0.3716 |         0.3716 |       2.46e-08 |       3.27e-08 |
| max        |         8.4253 |         8.4253 |         0.0146 |         0.0194 |

**Regression Analysis** (Python ~ Stata):

- **Model**: python = 0.0000 + 1.0000 * stata
- **R-squared**: 1.0000
- **N observations**: 1,728,572

| Coefficient |     Estimate |    Std Error | t-statistic |   p-value |
|-------------|--------------|--------------|-------------|----------|
| Intercept   |     2.05e-07 |     1.33e-07 |      1.5357 |     0.125 |
| Slope       |       1.0000 |     1.77e-07 |    5.64e+06 |     0.000 |

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

**Precision2**: 99th percentile diff = 4.59e-05 (tolerance: < 1.00e+00)

**Summary Statistics** (Common Observations):

| Statistic  |          Stata |         Python |     Difference | Std Difference |
|------------|----------------|----------------|----------------|----------------|
| count      |       1.88e+06 |       1.88e+06 |       1.88e+06 |       1.88e+06 |
| mean       |      -8.00e-06 |       6.88e-08 |       8.07e-06 |       1.72e-05 |
| std        |         0.4700 |         0.4700 |         0.0019 |         0.0041 |
| min        |       -47.2334 |       -47.2334 |        -0.2540 |        -0.5403 |
| 25%        |        -0.1325 |        -0.1324 |      -1.44e-08 |      -3.06e-08 |
| 50%        |        -0.0266 |        -0.0266 |       1.34e-09 |       2.84e-09 |
| 75%        |         0.0715 |         0.0715 |       2.02e-08 |       4.29e-08 |
| max        |        40.0578 |        40.0578 |         0.3426 |         0.7289 |

**Regression Analysis** (Python ~ Stata):

- **Model**: python = 0.0000 + 1.0000 * stata
- **R-squared**: 1.0000
- **N observations**: 1,881,251

| Coefficient |     Estimate |    Std Error | t-statistic |   p-value |
|-------------|--------------|--------------|-------------|----------|
| Intercept   |     8.07e-06 |     1.40e-06 |      5.7561 |     0.000 |
| Slope       |       1.0000 |     2.98e-06 | 335124.5878 |     0.000 |

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

**Precision2**: 99th percentile diff = 5.52e-07 (tolerance: < 1.00e+00)

**Summary Statistics** (Common Observations):

| Statistic  |          Stata |         Python |     Difference | Std Difference |
|------------|----------------|----------------|----------------|----------------|
| count      |       1.88e+06 |       1.88e+06 |       1.88e+06 |       1.88e+06 |
| mean       |      -1.15e-05 |      -4.50e-08 |       1.14e-05 |       2.22e-05 |
| std        |         0.5140 |         0.5140 |         0.0045 |         0.0088 |
| min        |       -33.2328 |       -33.2328 |        -1.0573 |        -2.0569 |
| 25%        |        -0.1659 |        -0.1658 |      -1.53e-08 |      -2.97e-08 |
| 50%        |        -0.0563 |        -0.0563 |      -2.85e-11 |      -5.55e-11 |
| 75%        |         0.0607 |         0.0607 |       1.53e-08 |       2.97e-08 |
| max        |        42.0109 |        42.0109 |         0.8334 |         1.6212 |

**Regression Analysis** (Python ~ Stata):

- **Model**: python = 0.0000 + 0.9999 * stata
- **R-squared**: 0.9999
- **N observations**: 1,881,251

| Coefficient |     Estimate |    Std Error | t-statistic |   p-value |
|-------------|--------------|--------------|-------------|----------|
| Intercept   |     1.14e-05 |     3.29e-06 |      3.4723 |     0.001 |
| Slope       |       0.9999 |     6.40e-06 | 156147.6503 |     0.000 |

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

**Precision2**: 99th percentile diff = 4.65e-07 (tolerance: < 1.00e+00)

**Summary Statistics** (Common Observations):

| Statistic  |          Stata |         Python |     Difference | Std Difference |
|------------|----------------|----------------|----------------|----------------|
| count      |       1.88e+06 |       1.88e+06 |       1.88e+06 |       1.88e+06 |
| mean       |      -2.40e-06 |       7.69e-07 |       3.17e-06 |       2.21e-06 |
| std        |         1.4374 |         1.4374 |       4.14e-04 |       2.88e-04 |
| min        |       -37.6318 |       -37.6318 |        -0.2453 |        -0.1706 |
| 25%        |        -0.8289 |        -0.8289 |      -3.98e-08 |      -2.77e-08 |
| 50%        |        -0.2497 |        -0.2497 |       3.47e-09 |       2.41e-09 |
| 75%        |         0.4664 |         0.4664 |       5.00e-08 |       3.48e-08 |
| max        |        11.3881 |        11.3881 |         0.0977 |         0.0680 |

**Regression Analysis** (Python ~ Stata):

- **Model**: python = 0.0000 + 1.0000 * stata
- **R-squared**: 1.0000
- **N observations**: 1,876,807

| Coefficient |     Estimate |    Std Error | t-statistic |   p-value |
|-------------|--------------|--------------|-------------|----------|
| Intercept   |     3.17e-06 |     3.02e-07 |     10.5054 |     0.000 |
| Slope       |       1.0000 |     2.10e-07 |    4.76e+06 |     0.000 |

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

**Precision2**: 99th percentile diff = 1.48e-08 (tolerance: < 1.00e+00)

**Summary Statistics** (Common Observations):

| Statistic  |          Stata |         Python |     Difference | Std Difference |
|------------|----------------|----------------|----------------|----------------|
| count      |       1.97e+06 |       1.97e+06 |       1.97e+06 |       1.97e+06 |
| mean       |         0.3649 |         0.3649 |      -8.17e-07 |      -3.46e-08 |
| std        |        23.6298 |        23.6298 |       2.56e-04 |       1.08e-05 |
| min        |        -1.7528 |        -1.7528 |        -0.3565 |        -0.0151 |
| 25%        |        -0.1052 |        -0.1052 |      -1.09e-08 |      -4.63e-10 |
| 50%        |         0.0340 |         0.0340 |       6.85e-12 |       2.90e-13 |
| 75%        |         0.2044 |         0.2044 |       1.32e-08 |       5.58e-10 |
| max        |      8214.9326 |      8214.9323 |       8.84e-04 |       3.74e-05 |

**Regression Analysis** (Python ~ Stata):

- **Model**: python = -0.0000 + 1.0000 * stata
- **R-squared**: 1.0000
- **N observations**: 1,973,744

| Coefficient |     Estimate |    Std Error | t-statistic |   p-value |
|-------------|--------------|--------------|-------------|----------|
| Intercept   |    -5.36e-07 |     1.82e-07 |     -2.9462 |     0.003 |
| Slope       |       1.0000 |     7.69e-09 |    1.30e+08 |     0.000 |

**Feedback**:
- Num observations with std_diff >= TOL_DIFF_1: 1/1973744 (0.000%)
- Stata standard deviation: 2.36e+01

---

### InvestPPEInv

**Status**: ✅ PASSED

**Test Results**:
- Test 1 - Column names: ✅ PASSED
- Test 2 - Superset check: ✅ PASSED
- Test 3 - Precision1 check: ✅ PASSED
- Test 4 - Precision2 check: ✅ PASSED

**Columns**: ['InvestPPEInv']

**Observations**:
- Stata:  2,928,130
- Python: 2,943,499
- Common: 2,928,106

**Precision1**: 0.000% obs with std_diff >= 1.00e-02 (tolerance: < 10%)

**Precision2**: 99th percentile diff = 4.73e-08 (tolerance: < 1.00e+00)

**Summary Statistics** (Common Observations):

| Statistic  |          Stata |         Python |     Difference | Std Difference |
|------------|----------------|----------------|----------------|----------------|
| count      |       2.93e+06 |       2.93e+06 |       2.93e+06 |       2.93e+06 |
| mean       |         0.0854 |         0.0854 |       3.90e-08 |       5.44e-08 |
| std        |         0.7165 |         0.7165 |       1.89e-05 |       2.64e-05 |
| min        |       -13.0490 |       -13.0490 |        -0.0012 |        -0.0017 |
| 25%        |         0.0000 |         0.0000 |      -1.36e-09 |      -1.90e-09 |
| 50%        |         0.0422 |         0.0422 |         0.0000 |         0.0000 |
| 75%        |         0.1171 |         0.1171 |       1.35e-09 |       1.88e-09 |
| max        |       264.5906 |       264.5906 |         0.0079 |         0.0110 |

**Regression Analysis** (Python ~ Stata):

- **Model**: python = 0.0000 + 1.0000 * stata
- **R-squared**: 1.0000
- **N observations**: 2,928,106

| Coefficient |     Estimate |    Std Error | t-statistic |   p-value |
|-------------|--------------|--------------|-------------|----------|
| Intercept   |     3.82e-08 |     1.11e-08 |      3.4340 |     0.001 |
| Slope       |       1.0000 |     1.54e-08 |    6.48e+07 |     0.000 |

**Feedback**:
- Num observations with std_diff >= TOL_DIFF_1: 12/2928106 (0.000%)
- Stata standard deviation: 7.17e-01

---

### Investment

**Status**: ✅ PASSED

**Test Results**:
- Test 1 - Column names: ✅ PASSED
- Test 2 - Superset check: ✅ PASSED
- Test 3 - Precision1 check: ✅ PASSED
- Test 4 - Precision2 check: ✅ PASSED

**Columns**: ['Investment']

**Observations**:
- Stata:  2,411,862
- Python: 2,419,987
- Common: 2,411,862

**Precision1**: 0.999% obs with std_diff >= 1.00e-02 (tolerance: < 10%)

**Precision2**: 99th percentile diff = 9.98e-03 (tolerance: < 1.00e+00)

**Summary Statistics** (Common Observations):

| Statistic  |          Stata |         Python |     Difference | Std Difference |
|------------|----------------|----------------|----------------|----------------|
| count      |       2.41e+06 |       2.41e+06 |       2.41e+06 |       2.41e+06 |
| mean       |         1.0036 |         1.0035 |      -1.75e-04 |      -9.60e-05 |
| std        |         1.8269 |         1.8280 |         0.0448 |         0.0245 |
| min        |     -2512.3491 |     -2512.3180 |       -31.3369 |       -17.1529 |
| 25%        |         0.6665 |         0.6659 |      -2.24e-08 |      -1.22e-08 |
| 50%        |         0.9327 |         0.9323 |         0.0000 |         0.0000 |
| 75%        |         1.2036 |         1.2035 |       2.24e-08 |       1.23e-08 |
| max        |       253.6225 |       253.6223 |        12.0000 |         6.5685 |

**Regression Analysis** (Python ~ Stata):

- **Model**: python = -0.0004 + 1.0003 * stata
- **R-squared**: 0.9994
- **N observations**: 2,411,862

| Coefficient |     Estimate |    Std Error | t-statistic |   p-value |
|-------------|--------------|--------------|-------------|----------|
| Intercept   |    -4.43e-04 |     3.29e-05 |    -13.4392 |     0.000 |
| Slope       |       1.0003 |     1.58e-05 |  63297.3080 |     0.000 |

**Feedback**:
- Num observations with std_diff >= TOL_DIFF_1: 24097/2411862 (0.999%)
- Stata standard deviation: 1.83e+00

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

**Precision2**: 99th percentile diff = 9.88e-08 (tolerance: < 1.00e+00)

**Summary Statistics** (Common Observations):

| Statistic  |          Stata |         Python |     Difference | Std Difference |
|------------|----------------|----------------|----------------|----------------|
| count      |       3.06e+06 |       3.06e+06 |       3.06e+06 |       3.06e+06 |
| mean       |         0.3426 |         0.3427 |       3.93e-05 |       2.98e-05 |
| std        |         1.3200 |         1.3199 |         0.0458 |         0.0347 |
| min        |        -1.0000 |        -1.0000 |       -25.7115 |       -19.4790 |
| 25%        |        -0.2333 |        -0.2333 |      -7.12e-09 |      -5.40e-09 |
| 50%        |         0.1445 |         0.1445 |         0.0000 |         0.0000 |
| 75%        |         0.5972 |         0.5972 |       7.12e-09 |       5.39e-09 |
| max        |       544.3116 |       544.3116 |        26.7868 |        20.2937 |

**Regression Analysis** (Python ~ Stata):

- **Model**: python = 0.0003 + 0.9994 * stata
- **R-squared**: 0.9988
- **N observations**: 3,059,782

| Coefficient |     Estimate |    Std Error | t-statistic |   p-value |
|-------------|--------------|--------------|-------------|----------|
| Intercept   |     2.50e-04 |     2.71e-05 |      9.2456 |     0.000 |
| Slope       |       0.9994 |     1.99e-05 |  50340.0314 |     0.000 |

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

**Precision2**: 99th percentile diff = 4.42e-08 (tolerance: < 1.00e+00)

**Summary Statistics** (Common Observations):

| Statistic  |          Stata |         Python |     Difference | Std Difference |
|------------|----------------|----------------|----------------|----------------|
| count      |       3.01e+06 |       3.01e+06 |       3.01e+06 |       3.01e+06 |
| mean       |         2.6680 |         2.6680 |       7.89e-08 |       4.41e-09 |
| std        |        17.9005 |        17.9005 |       5.50e-05 |       3.07e-06 |
| min        |         0.0000 |         0.0000 |      -1.80e-04 |      -1.01e-05 |
| 25%        |         0.2228 |         0.2228 |      -1.12e-08 |      -6.24e-10 |
| 50%        |         0.6455 |         0.6455 |       6.07e-13 |       3.39e-14 |
| 75%        |         1.8667 |         1.8667 |       1.11e-08 |       6.21e-10 |
| max        |      5277.1953 |      5277.1954 |         0.0512 |         0.0029 |

**Regression Analysis** (Python ~ Stata):

- **Model**: python = 0.0000 + 1.0000 * stata
- **R-squared**: 1.0000
- **N observations**: 3,014,665

| Coefficient |     Estimate |    Std Error | t-statistic |   p-value |
|-------------|--------------|--------------|-------------|----------|
| Intercept   |     6.90e-08 |     3.20e-08 |      2.1551 |     0.031 |
| Slope       |       1.0000 |     1.77e-09 |    5.65e+08 |     0.000 |

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

**Precision2**: 99th percentile diff = 1.18e-07 (tolerance: < 1.00e+00)

**Summary Statistics** (Common Observations):

| Statistic  |          Stata |         Python |     Difference | Std Difference |
|------------|----------------|----------------|----------------|----------------|
| count      |       3.52e+06 |       3.52e+06 |       3.52e+06 |       3.52e+06 |
| mean       |         0.0735 |         0.0735 |       2.72e-05 |       5.71e-05 |
| std        |         0.4754 |         0.4753 |         0.0279 |         0.0587 |
| min        |        -1.0000 |        -1.0000 |       -10.5241 |       -22.1353 |
| 25%        |        -0.1506 |        -0.1506 |      -3.18e-09 |      -6.68e-09 |
| 50%        |         0.0249 |         0.0249 |         0.0000 |         0.0000 |
| 75%        |         0.2121 |         0.2121 |       3.19e-09 |       6.70e-09 |
| max        |        80.0474 |        80.0474 |        11.6087 |        24.4167 |

**Regression Analysis** (Python ~ Stata):

- **Model**: python = 0.0002 + 0.9979 * stata
- **R-squared**: 0.9966
- **N observations**: 3,518,261

| Coefficient |     Estimate |    Std Error | t-statistic |   p-value |
|-------------|--------------|--------------|-------------|----------|
| Intercept   |     1.82e-04 |     1.51e-05 |     12.1059 |     0.000 |
| Slope       |       0.9979 |     3.13e-05 |  31886.3042 |     0.000 |

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

**Precision1**: 32.967% obs with std_diff >= 1.00e-02 (tolerance: < 10%)

**Precision2**: 99th percentile diff = 2.59e+00 (tolerance: < 1.00e+00)

**Summary Statistics** (Common Observations):

| Statistic  |          Stata |         Python |     Difference | Std Difference |
|------------|----------------|----------------|----------------|----------------|
| count      |    473079.0000 |    473079.0000 |    473079.0000 |    473079.0000 |
| mean       |         3.8814 |         3.7610 |        -0.1204 |        -0.0781 |
| std        |         1.5421 |         1.5342 |         1.0648 |         0.6905 |
| min        |         1.0000 |         1.0000 |        -5.0000 |        -3.2424 |
| 25%        |         3.0000 |         3.0000 |         0.0000 |         0.0000 |
| 50%        |         4.0000 |         4.0000 |         0.0000 |         0.0000 |
| 75%        |         5.0000 |         5.0000 |         0.0000 |         0.0000 |
| max        |         6.0000 |         6.0000 |         5.0000 |         3.2424 |

**Regression Analysis** (Python ~ Stata):

- **Model**: python = 0.8246 + 0.7565 * stata
- **R-squared**: 0.5782
- **N observations**: 473,079

| Coefficient |     Estimate |    Std Error | t-statistic |   p-value |
|-------------|--------------|--------------|-------------|----------|
| Intercept   |       0.8246 |       0.0039 |    210.1710 |     0.000 |
| Slope       |       0.7565 |     9.39e-04 |    805.2808 |     0.000 |

**Feedback**:
- Num observations with std_diff >= TOL_DIFF_1: 155962/473079 (32.967%)
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
9   12084  202412       5      6    -1
```

**Largest Differences**:
```
   permno  yyyymm  python  stata  diff
0   11170  199506       6      1     5
1   11170  199507       6      1     5
2   11170  199510       6      1     5
3   11170  199512       6      1     5
4   11170  199601       6      1     5
5   11170  199604       6      1     5
6   11170  199605       6      1     5
7   11170  199704       6      1     5
8   11170  199705       6      1     5
9   11233  199506       1      6    -5
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

**Precision2**: 99th percentile diff = 0.00e+00 (tolerance: < 1.00e+00)

**Summary Statistics** (Common Observations):

| Statistic  |          Stata |         Python |     Difference | Std Difference |
|------------|----------------|----------------|----------------|----------------|
| count      |       5.03e+06 |       5.03e+06 |       5.03e+06 |       5.03e+06 |
| mean       |         0.0688 |         0.0688 |         0.0000 |         0.0000 |
| std        |         0.1031 |         0.1031 |         0.0000 |         0.0000 |
| min        |        -0.8696 |        -0.8696 |         0.0000 |         0.0000 |
| 25%        |         0.0248 |         0.0248 |         0.0000 |         0.0000 |
| 50%        |         0.0449 |         0.0449 |         0.0000 |         0.0000 |
| 75%        |         0.0811 |         0.0811 |         0.0000 |         0.0000 |
| max        |        39.7253 |        39.7253 |         0.0000 |         0.0000 |

**Regression Analysis** (Python ~ Stata):

- **Model**: python = 0.0000 + 1.0000 * stata
- **R-squared**: 1.0000
- **N observations**: 5,033,574

| Coefficient |     Estimate |    Std Error | t-statistic |   p-value |
|-------------|--------------|--------------|-------------|----------|
| Intercept   |     8.53e-15 |     5.31e-18 |   1606.4818 |     0.000 |
| Slope       |       1.0000 |     4.29e-17 |    2.33e+16 |     0.000 |

**Feedback**:
- Num observations with std_diff >= TOL_DIFF_1: 0/5033574 (0.000%)
- Stata standard deviation: 1.03e-01

---

### MeanRankRevGrowth

**Status**: ✅ PASSED

**Test Results**:
- Test 1 - Column names: ✅ PASSED
- Test 2 - Superset check: ✅ PASSED
- Test 3 - Precision1 check: ✅ PASSED
- Test 4 - Precision2 check: ✅ PASSED

**Columns**: ['MeanRankRevGrowth']

**Observations**:
- Stata:  2,028,817
- Python: 2,029,426
- Common: 2,028,817

**Precision1**: 0.000% obs with std_diff >= 1.00e-02 (tolerance: < 10%)

**Precision2**: 99th percentile diff = 3.19e-04 (tolerance: < 1.00e+00)

**Summary Statistics** (Common Observations):

| Statistic  |          Stata |         Python |     Difference | Std Difference |
|------------|----------------|----------------|----------------|----------------|
| count      |       2.03e+06 |       2.03e+06 |       2.03e+06 |       2.03e+06 |
| mean       |      2350.3064 |      2350.3082 |         0.0018 |       1.70e-06 |
| std        |      1044.5183 |      1044.5187 |         0.0618 |       5.91e-05 |
| min        |        10.6000 |        10.6000 |        -3.8667 |        -0.0037 |
| 25%        |      1639.9333 |      1639.9333 |      -3.33e-05 |      -3.19e-08 |
| 50%        |      2327.5334 |      2327.5333 |         0.0000 |         0.0000 |
| 75%        |      3009.8667 |      3009.8667 |       3.33e-05 |       3.19e-08 |
| max        |      6667.5332 |      6667.5333 |        13.2667 |         0.0127 |

**Regression Analysis** (Python ~ Stata):

- **Model**: python = 0.0008 + 1.0000 * stata
- **R-squared**: 1.0000
- **N observations**: 2,028,817

| Coefficient |     Estimate |    Std Error | t-statistic |   p-value |
|-------------|--------------|--------------|-------------|----------|
| Intercept   |     8.15e-04 |     1.07e-04 |      7.6305 |     0.000 |
| Slope       |       1.0000 |     4.15e-08 |    2.41e+07 |     0.000 |

**Feedback**:
- Num observations with std_diff >= TOL_DIFF_1: 2/2028817 (0.000%)
- Stata standard deviation: 1.04e+03

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

**Precision2**: 99th percentile diff = 1.02e-07 (tolerance: < 1.00e+00)

**Summary Statistics** (Common Observations):

| Statistic  |          Stata |         Python |     Difference | Std Difference |
|------------|----------------|----------------|----------------|----------------|
| count      |       3.71e+06 |       3.71e+06 |       3.71e+06 |       3.71e+06 |
| mean       |         0.1328 |         0.1328 |      -4.81e-12 |      -6.24e-12 |
| std        |         0.7707 |         0.7707 |       2.10e-08 |       2.72e-08 |
| min        |        -1.0000 |        -1.0000 |      -3.45e-06 |      -4.48e-06 |
| 25%        |        -0.2091 |        -0.2091 |      -4.67e-09 |      -6.06e-09 |
| 50%        |         0.0459 |         0.0459 |         0.0000 |         0.0000 |
| 75%        |         0.3214 |         0.3214 |       4.66e-09 |       6.05e-09 |
| max        |       436.6845 |       436.6845 |       4.31e-06 |       5.60e-06 |

**Regression Analysis** (Python ~ Stata):

- **Model**: python = 0.0000 + 1.0000 * stata
- **R-squared**: 1.0000
- **N observations**: 3,713,622

| Coefficient |     Estimate |    Std Error | t-statistic |   p-value |
|-------------|--------------|--------------|-------------|----------|
| Intercept   |     1.26e-11 |     1.10e-11 |      1.1398 |     0.254 |
| Slope       |       1.0000 |     1.41e-11 |    7.09e+10 |     0.000 |

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

**Precision2**: 99th percentile diff = 1.01e-15 (tolerance: < 1.00e+00)

**Summary Statistics** (Common Observations):

| Statistic  |          Stata |         Python |     Difference | Std Difference |
|------------|----------------|----------------|----------------|----------------|
| count      |       3.87e+06 |       3.87e+06 |       3.87e+06 |       3.87e+06 |
| mean       |         0.0113 |         0.0113 |      -9.37e-06 |      -1.61e-04 |
| std        |         0.0582 |         0.0582 |         0.0027 |         0.0468 |
| min        |        -0.5758 |        -0.5758 |        -0.5937 |       -10.2025 |
| 25%        |        -0.0153 |        -0.0153 |      -2.78e-17 |      -4.77e-16 |
| 50%        |         0.0096 |         0.0096 |         0.0000 |         0.0000 |
| 75%        |         0.0351 |         0.0351 |       2.78e-17 |       4.77e-16 |
| max        |         4.2943 |         4.2943 |         1.7645 |        30.3232 |

**Regression Analysis** (Python ~ Stata):

- **Model**: python = 0.0000 + 0.9989 * stata
- **R-squared**: 0.9978
- **N observations**: 3,865,561

| Coefficient |     Estimate |    Std Error | t-statistic |   p-value |
|-------------|--------------|--------------|-------------|----------|
| Intercept   |     3.18e-06 |     1.41e-06 |      2.2562 |     0.024 |
| Slope       |       0.9989 |     2.38e-05 |  41987.6080 |     0.000 |

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

**Precision2**: 99th percentile diff = 9.40e-08 (tolerance: < 1.00e+00)

**Summary Statistics** (Common Observations):

| Statistic  |          Stata |         Python |     Difference | Std Difference |
|------------|----------------|----------------|----------------|----------------|
| count      |       3.89e+06 |       3.89e+06 |       3.89e+06 |       3.89e+06 |
| mean       |         0.0556 |         0.0556 |       7.28e-12 |       1.67e-11 |
| std        |         0.4365 |         0.4365 |       1.24e-08 |       2.85e-08 |
| min        |        -1.0000 |        -1.0000 |      -1.69e-06 |      -3.88e-06 |
| 25%        |        -0.1471 |        -0.1471 |      -2.94e-09 |      -6.73e-09 |
| 50%        |         0.0171 |         0.0171 |         0.0000 |         0.0000 |
| 75%        |         0.1891 |         0.1891 |       2.95e-09 |       6.75e-09 |
| max        |        66.9428 |        66.9428 |       1.27e-06 |       2.91e-06 |

**Regression Analysis** (Python ~ Stata):

- **Model**: python = 0.0000 + 1.0000 * stata
- **R-squared**: 1.0000
- **N observations**: 3,893,591

| Coefficient |     Estimate |    Std Error | t-statistic |   p-value |
|-------------|--------------|--------------|-------------|----------|
| Intercept   |     1.43e-11 |     6.35e-12 |      2.2572 |     0.024 |
| Slope       |       1.0000 |     1.44e-11 |    6.93e+10 |     0.000 |

**Feedback**:
- Num observations with std_diff >= TOL_DIFF_1: 0/3893591 (0.000%)
- Stata standard deviation: 4.37e-01

---

### Mom6mJunk

**Status**: ❌ FAILED

**Test Results**:
- Test 1 - Column names: ✅ PASSED
- Test 2 - Superset check: ❌ FAILED (Python missing 67064 Stata observations)
- Test 3 - Precision1 check: ✅ PASSED
- Test 4 - Precision2 check: ✅ PASSED

**Columns**: ['Mom6mJunk']

**Observations**:
- Stata:  391,738
- Python: 343,810
- Common: 324,674

**Precision1**: 0.052% obs with std_diff >= 1.00e-02 (tolerance: < 10%)

**Precision2**: 99th percentile diff = 8.36e-08 (tolerance: < 1.00e+00)

**Summary Statistics** (Common Observations):

| Statistic  |          Stata |         Python |     Difference | Std Difference |
|------------|----------------|----------------|----------------|----------------|
| count      |    324713.0000 |    324713.0000 |    324713.0000 |    324713.0000 |
| mean       |         0.0541 |         0.0541 |      -1.87e-05 |      -4.87e-05 |
| std        |         0.3842 |         0.3842 |         0.0066 |         0.0171 |
| min        |        -0.9947 |        -0.9947 |        -2.3494 |        -6.1144 |
| 25%        |        -0.1325 |        -0.1325 |      -2.95e-09 |      -7.67e-09 |
| 50%        |         0.0319 |         0.0319 |         0.0000 |         0.0000 |
| 75%        |         0.1994 |         0.1994 |       2.96e-09 |       7.70e-09 |
| max        |        47.6527 |        47.6527 |         1.2424 |         3.2333 |

**Regression Analysis** (Python ~ Stata):

- **Model**: python = -0.0000 + 0.9998 * stata
- **R-squared**: 0.9997
- **N observations**: 324,713

| Coefficient |     Estimate |    Std Error | t-statistic |   p-value |
|-------------|--------------|--------------|-------------|----------|
| Intercept   |    -9.49e-06 |     1.16e-05 |     -0.8147 |     0.415 |
| Slope       |       0.9998 |     3.00e-05 |  33321.6294 |     0.000 |

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
- Num observations with std_diff >= TOL_DIFF_1: 170/324713 (0.052%)
- Stata standard deviation: 3.84e-01

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

**Precision2**: 99th percentile diff = 3.53e-02 (tolerance: < 1.00e+00)

**Summary Statistics** (Common Observations):

| Statistic  |          Stata |         Python |     Difference | Std Difference |
|------------|----------------|----------------|----------------|----------------|
| count      |       3.40e+06 |       3.40e+06 |       3.40e+06 |       3.40e+06 |
| mean       |         0.0125 |         0.0124 |      -2.32e-05 |      -8.58e-04 |
| std        |         0.0270 |         0.0263 |         0.0057 |         0.2127 |
| min        |        -4.1713 |        -0.6858 |        -1.2021 |       -44.5515 |
| 25%        |       3.95e-04 |       3.88e-04 |      -5.00e-10 |      -1.85e-08 |
| 50%        |         0.0119 |         0.0118 |         0.0000 |         0.0000 |
| 75%        |         0.0240 |         0.0240 |       5.09e-10 |       1.89e-08 |
| max        |         1.5150 |         1.5150 |         3.8643 |       143.2185 |

**Regression Analysis** (Python ~ Stata):

- **Model**: python = 0.0006 + 0.9539 * stata
- **R-squared**: 0.9547
- **N observations**: 3,396,703

| Coefficient |     Estimate |    Std Error | t-statistic |   p-value |
|-------------|--------------|--------------|-------------|----------|
| Intercept   |     5.51e-04 |     3.35e-06 |    164.6263 |     0.000 |
| Slope       |       0.9539 |     1.13e-04 |   8465.5718 |     0.000 |

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

**Precision2**: 99th percentile diff = 3.09e-07 (tolerance: < 1.00e+00)

**Summary Statistics** (Common Observations):

| Statistic  |          Stata |         Python |     Difference | Std Difference |
|------------|----------------|----------------|----------------|----------------|
| count      |       2.43e+06 |       2.43e+06 |       2.43e+06 |       2.43e+06 |
| mean       |         0.0130 |         0.0131 |       9.06e-05 |         0.0028 |
| std        |         0.0324 |         0.0304 |         0.0104 |         0.3215 |
| min        |        -4.8725 |        -4.8725 |        -2.4925 |       -76.9952 |
| 25%        |         0.0027 |         0.0027 |      -4.55e-10 |      -1.40e-08 |
| 50%        |         0.0125 |         0.0126 |         0.0000 |         0.0000 |
| 75%        |         0.0233 |         0.0233 |       4.55e-10 |       1.40e-08 |
| max        |        15.8923 |        15.8923 |         2.3495 |        72.5785 |

**Regression Analysis** (Python ~ Stata):

- **Model**: python = 0.0015 + 0.8905 * stata
- **R-squared**: 0.8967
- **N observations**: 2,425,318

| Coefficient |     Estimate |    Std Error | t-statistic |   p-value |
|-------------|--------------|--------------|-------------|----------|
| Intercept   |       0.0015 |     6.77e-06 |    224.1977 |     0.000 |
| Slope       |       0.8905 |     1.94e-04 |   4587.3336 |     0.000 |

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

**Precision2**: 99th percentile diff = 3.22e-07 (tolerance: < 1.00e+00)

**Summary Statistics** (Common Observations):

| Statistic  |          Stata |         Python |     Difference | Std Difference |
|------------|----------------|----------------|----------------|----------------|
| count      |       1.68e+06 |       1.68e+06 |       1.68e+06 |       1.68e+06 |
| mean       |         0.0135 |         0.0135 |       2.06e-05 |       8.09e-04 |
| std        |         0.0254 |         0.0242 |         0.0080 |         0.3162 |
| min        |        -2.6111 |        -1.0731 |        -1.4205 |       -55.8965 |
| 25%        |         0.0034 |         0.0034 |      -4.55e-10 |      -1.79e-08 |
| 50%        |         0.0128 |         0.0128 |         0.0000 |         0.0000 |
| 75%        |         0.0235 |         0.0234 |       4.55e-10 |       1.79e-08 |
| max        |         2.2478 |         2.2478 |         2.5829 |       101.6332 |

**Regression Analysis** (Python ~ Stata):

- **Model**: python = 0.0013 + 0.9028 * stata
- **R-squared**: 0.9000
- **N observations**: 1,677,526

| Coefficient |     Estimate |    Std Error | t-statistic |   p-value |
|-------------|--------------|--------------|-------------|----------|
| Intercept   |       0.0013 |     6.69e-06 |    199.5419 |     0.000 |
| Slope       |       0.9028 |     2.32e-04 |   3886.5164 |     0.000 |

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

**Precision2**: 99th percentile diff = 1.92e-07 (tolerance: < 1.00e+00)

**Summary Statistics** (Common Observations):

| Statistic  |          Stata |         Python |     Difference | Std Difference |
|------------|----------------|----------------|----------------|----------------|
| count      |       1.03e+06 |       1.03e+06 |       1.03e+06 |       1.03e+06 |
| mean       |         0.0150 |         0.0150 |       1.49e-06 |       8.52e-05 |
| std        |         0.0175 |         0.0175 |       7.06e-04 |         0.0403 |
| min        |        -0.1110 |        -0.1110 |        -0.0501 |        -2.8566 |
| 25%        |         0.0053 |         0.0053 |      -4.27e-10 |      -2.44e-08 |
| 50%        |         0.0134 |         0.0134 |         0.0000 |         0.0000 |
| 75%        |         0.0230 |         0.0230 |       4.44e-10 |       2.54e-08 |
| max        |         0.3670 |         0.3670 |         0.0498 |         2.8419 |

**Regression Analysis** (Python ~ Stata):

- **Model**: python = 0.0000 + 0.9982 * stata
- **R-squared**: 0.9984
- **N observations**: 1,027,449

| Coefficient |     Estimate |    Std Error | t-statistic |   p-value |
|-------------|--------------|--------------|-------------|----------|
| Intercept   |     2.77e-05 |     9.15e-07 |     30.3171 |     0.000 |
| Slope       |       0.9982 |     3.97e-05 |  25148.4282 |     0.000 |

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

**Precision2**: 99th percentile diff = 0.00e+00 (tolerance: < 1.00e+00)

**Summary Statistics** (Common Observations):

| Statistic  |          Stata |         Python |     Difference | Std Difference |
|------------|----------------|----------------|----------------|----------------|
| count      |    258775.0000 |    258775.0000 |    258775.0000 |    258775.0000 |
| mean       |         0.5549 |         0.5549 |         0.0000 |         0.0000 |
| std        |         0.4970 |         0.4970 |         0.0000 |         0.0000 |
| min        |         0.0000 |         0.0000 |         0.0000 |         0.0000 |
| 25%        |         0.0000 |         0.0000 |         0.0000 |         0.0000 |
| 50%        |         1.0000 |         1.0000 |         0.0000 |         0.0000 |
| 75%        |         1.0000 |         1.0000 |         0.0000 |         0.0000 |
| max        |         1.0000 |         1.0000 |         0.0000 |         0.0000 |

**Regression Analysis** (Python ~ Stata):

- **Model**: python = -0.0000 + 1.0000 * stata
- **R-squared**: 1.0000
- **N observations**: 258,775

| Coefficient |     Estimate |    Std Error | t-statistic |   p-value |
|-------------|--------------|--------------|-------------|----------|
| Intercept   |    -5.13e-13 |     1.45e-15 |   -354.3934 |     0.000 |
| Slope       |       1.0000 |     1.94e-15 |    5.15e+14 |     0.000 |

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

**Precision2**: 99th percentile diff = 1.32e-07 (tolerance: < 1.00e+00)

**Summary Statistics** (Common Observations):

| Statistic  |          Stata |         Python |     Difference | Std Difference |
|------------|----------------|----------------|----------------|----------------|
| count      |       3.40e+06 |       3.40e+06 |       3.40e+06 |       3.40e+06 |
| mean       |         0.0122 |         0.0122 |       4.37e-12 |       4.32e-11 |
| std        |         0.1011 |         0.1011 |       4.16e-09 |       4.11e-08 |
| min        |        -0.9957 |        -0.9957 |      -3.50e-07 |      -3.46e-06 |
| 25%        |        -0.0317 |        -0.0317 |      -1.00e-09 |      -9.89e-09 |
| 50%        |         0.0070 |         0.0070 |         0.0000 |         0.0000 |
| 75%        |         0.0487 |         0.0487 |       1.00e-09 |       9.89e-09 |
| max        |        15.9845 |        15.9845 |       6.00e-07 |       5.93e-06 |

**Regression Analysis** (Python ~ Stata):

- **Model**: python = -0.0000 + 1.0000 * stata
- **R-squared**: 1.0000
- **N observations**: 3,398,424

| Coefficient |     Estimate |    Std Error | t-statistic |   p-value |
|-------------|--------------|--------------|-------------|----------|
| Intercept   |    -4.34e-12 |     2.27e-12 |     -1.9124 |     0.056 |
| Slope       |       1.0000 |     2.23e-11 |    4.48e+10 |     0.000 |

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

**Precision2**: 99th percentile diff = 1.51e-07 (tolerance: < 1.00e+00)

**Summary Statistics** (Common Observations):

| Statistic  |          Stata |         Python |     Difference | Std Difference |
|------------|----------------|----------------|----------------|----------------|
| count      |       2.43e+06 |       2.43e+06 |       2.43e+06 |       2.43e+06 |
| mean       |         0.0127 |         0.0127 |       5.42e-12 |       6.14e-11 |
| std        |         0.0882 |         0.0882 |       4.07e-09 |       4.62e-08 |
| min        |        -0.9062 |        -0.9062 |      -3.00e-07 |      -3.40e-06 |
| 25%        |        -0.0260 |        -0.0260 |      -1.00e-09 |      -1.13e-08 |
| 50%        |         0.0084 |         0.0084 |         0.0000 |         0.0000 |
| 75%        |         0.0455 |         0.0455 |       1.00e-09 |       1.13e-08 |
| max        |         6.7025 |         6.7025 |       3.67e-07 |       4.16e-06 |

**Regression Analysis** (Python ~ Stata):

- **Model**: python = -0.0000 + 1.0000 * stata
- **R-squared**: 1.0000
- **N observations**: 2,432,862

| Coefficient |     Estimate |    Std Error | t-statistic |   p-value |
|-------------|--------------|--------------|-------------|----------|
| Intercept   |    -6.09e-12 |     2.64e-12 |     -2.3082 |     0.021 |
| Slope       |       1.0000 |     2.96e-11 |    3.38e+10 |     0.000 |

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

**Precision2**: 99th percentile diff = 1.43e-07 (tolerance: < 1.00e+00)

**Summary Statistics** (Common Observations):

| Statistic  |          Stata |         Python |     Difference | Std Difference |
|------------|----------------|----------------|----------------|----------------|
| count      |       1.68e+06 |       1.68e+06 |       1.68e+06 |       1.68e+06 |
| mean       |         0.0132 |         0.0132 |       5.62e-12 |       6.70e-11 |
| std        |         0.0839 |         0.0839 |       3.93e-09 |       4.69e-08 |
| min        |        -0.9062 |        -0.9062 |      -2.00e-07 |      -2.38e-06 |
| 25%        |        -0.0241 |        -0.0241 |      -1.00e-09 |      -1.19e-08 |
| 50%        |         0.0091 |         0.0091 |         0.0000 |         0.0000 |
| 75%        |         0.0450 |         0.0450 |       1.00e-09 |       1.19e-08 |
| max        |         3.7568 |         3.7568 |       2.00e-07 |       2.38e-06 |

**Regression Analysis** (Python ~ Stata):

- **Model**: python = -0.0000 + 1.0000 * stata
- **R-squared**: 1.0000
- **N observations**: 1,680,518

| Coefficient |     Estimate |    Std Error | t-statistic |   p-value |
|-------------|--------------|--------------|-------------|----------|
| Intercept   |    -5.15e-12 |     3.07e-12 |     -1.6778 |     0.093 |
| Slope       |       1.0000 |     3.61e-11 |    2.77e+10 |     0.000 |

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

**Precision2**: 99th percentile diff = 1.36e-07 (tolerance: < 1.00e+00)

**Summary Statistics** (Common Observations):

| Statistic  |          Stata |         Python |     Difference | Std Difference |
|------------|----------------|----------------|----------------|----------------|
| count      |       1.19e+06 |       1.19e+06 |       1.19e+06 |       1.19e+06 |
| mean       |         0.0134 |         0.0134 |      -4.78e-13 |      -5.92e-12 |
| std        |         0.0808 |         0.0808 |       3.79e-09 |       4.70e-08 |
| min        |        -0.9062 |        -0.9062 |      -1.00e-07 |      -1.24e-06 |
| 25%        |        -0.0223 |        -0.0223 |      -1.00e-09 |      -1.24e-08 |
| 50%        |         0.0096 |         0.0096 |         0.0000 |         0.0000 |
| 75%        |         0.0441 |         0.0441 |       1.00e-09 |       1.24e-08 |
| max        |         3.7568 |         3.7568 |       2.00e-07 |       2.48e-06 |

**Regression Analysis** (Python ~ Stata):

- **Model**: python = -0.0000 + 1.0000 * stata
- **R-squared**: 1.0000
- **N observations**: 1,194,902

| Coefficient |     Estimate |    Std Error | t-statistic |   p-value |
|-------------|--------------|--------------|-------------|----------|
| Intercept   |    -1.00e-11 |     3.52e-12 |     -2.8522 |     0.004 |
| Slope       |       1.0000 |     4.29e-11 |    2.33e+10 |     0.000 |

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

**Precision2**: 99th percentile diff = 5.78e-08 (tolerance: < 1.00e+00)

**Summary Statistics** (Common Observations):

| Statistic  |          Stata |         Python |     Difference | Std Difference |
|------------|----------------|----------------|----------------|----------------|
| count      |       3.72e+06 |       3.72e+06 |       3.72e+06 |       3.72e+06 |
| mean       |         0.0117 |         0.0117 |       1.75e-14 |       1.01e-13 |
| std        |         0.1730 |         0.1730 |       4.34e-09 |       2.51e-08 |
| min        |        -0.9957 |        -0.9957 |      -5.00e-07 |      -2.89e-06 |
| 25%        |        -0.0633 |        -0.0633 |      -1.11e-16 |      -6.42e-16 |
| 50%        |         0.0000 |         0.0000 |         0.0000 |         0.0000 |
| 75%        |         0.0690 |         0.0690 |       1.11e-16 |       6.42e-16 |
| max        |        24.0000 |        24.0000 |       4.00e-07 |       2.31e-06 |

**Regression Analysis** (Python ~ Stata):

- **Model**: python = -0.0000 + 1.0000 * stata
- **R-squared**: 1.0000
- **N observations**: 3,718,320

| Coefficient |     Estimate |    Std Error | t-statistic |   p-value |
|-------------|--------------|--------------|-------------|----------|
| Intercept   |    -9.95e-12 |     2.25e-12 |     -4.4149 |     0.000 |
| Slope       |       1.0000 |     1.30e-11 |    7.69e+10 |     0.000 |

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

**Precision2**: 99th percentile diff = 0.00e+00 (tolerance: < 1.00e+00)

**Summary Statistics** (Common Observations):

| Statistic  |          Stata |         Python |     Difference | Std Difference |
|------------|----------------|----------------|----------------|----------------|
| count      |       1.10e+06 |       1.10e+06 |       1.10e+06 |       1.10e+06 |
| mean       |         5.7085 |         5.7122 |         0.0036 |         0.0013 |
| std        |         2.8802 |         2.8790 |         0.0645 |         0.0224 |
| min        |         1.0000 |         1.0000 |        -1.0000 |        -0.3472 |
| 25%        |         3.0000 |         3.0000 |         0.0000 |         0.0000 |
| 50%        |         6.0000 |         6.0000 |         0.0000 |         0.0000 |
| 75%        |         8.0000 |         8.0000 |         0.0000 |         0.0000 |
| max        |        10.0000 |        10.0000 |         1.0000 |         0.3472 |

**Regression Analysis** (Python ~ Stata):

- **Model**: python = 0.0075 + 0.9993 * stata
- **R-squared**: 0.9995
- **N observations**: 1,095,587

| Coefficient |     Estimate |    Std Error | t-statistic |   p-value |
|-------------|--------------|--------------|-------------|----------|
| Intercept   |       0.0075 |     1.37e-04 |     54.5394 |     0.000 |
| Slope       |       0.9993 |     2.14e-05 |  46756.5279 |     0.000 |

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

**Precision2**: 99th percentile diff = 6.78e-08 (tolerance: < 1.00e+00)

**Summary Statistics** (Common Observations):

| Statistic  |          Stata |         Python |     Difference | Std Difference |
|------------|----------------|----------------|----------------|----------------|
| count      |       3.20e+06 |       3.20e+06 |       3.20e+06 |       3.20e+06 |
| mean       |         0.5611 |         0.5611 |       9.48e-07 |       5.86e-07 |
| std        |         1.6192 |         1.6192 |         0.0015 |       9.11e-04 |
| min        |      -498.1454 |      -498.1455 |        -0.3434 |        -0.2121 |
| 25%        |         0.3049 |         0.3049 |      -1.98e-08 |      -1.22e-08 |
| 50%        |         0.5864 |         0.5864 |         0.0000 |         0.0000 |
| 75%        |         0.7647 |         0.7647 |       1.97e-08 |       1.22e-08 |
| max        |       362.4152 |       362.4152 |         0.6600 |         0.4076 |

**Regression Analysis** (Python ~ Stata):

- **Model**: python = 0.0000 + 1.0000 * stata
- **R-squared**: 1.0000
- **N observations**: 3,196,825

| Coefficient |     Estimate |    Std Error | t-statistic |   p-value |
|-------------|--------------|--------------|-------------|----------|
| Intercept   |     4.27e-06 |     8.73e-07 |      4.8864 |     0.000 |
| Slope       |       1.0000 |     5.09e-07 |    1.96e+06 |     0.000 |

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

**Precision2**: 99th percentile diff = 1.21e-07 (tolerance: < 1.00e+00)

**Summary Statistics** (Common Observations):

| Statistic  |          Stata |         Python |     Difference | Std Difference |
|------------|----------------|----------------|----------------|----------------|
| count      |       2.78e+06 |       2.78e+06 |       2.78e+06 |       2.78e+06 |
| mean       |         0.0183 |         0.0183 |       6.20e-08 |       5.27e-07 |
| std        |         0.1177 |         0.1177 |       1.65e-04 |         0.0014 |
| min        |        -0.9958 |        -0.9958 |        -0.0584 |        -0.4958 |
| 25%        |        -0.0178 |        -0.0178 |      -4.01e-10 |      -3.40e-09 |
| 50%        |         0.0000 |         0.0000 |         0.0000 |         0.0000 |
| 75%        |         0.0359 |         0.0359 |       3.96e-10 |       3.36e-09 |
| max        |         0.9994 |         0.9994 |         0.0473 |         0.4016 |

**Regression Analysis** (Python ~ Stata):

- **Model**: python = -0.0000 + 1.0000 * stata
- **R-squared**: 1.0000
- **N observations**: 2,782,808

| Coefficient |     Estimate |    Std Error | t-statistic |   p-value |
|-------------|--------------|--------------|-------------|----------|
| Intercept   |    -4.71e-08 |     1.00e-07 |     -0.4712 |     0.638 |
| Slope       |       1.0000 |     8.39e-07 |    1.19e+06 |     0.000 |

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

**Precision2**: 99th percentile diff = 5.14e-08 (tolerance: < 1.00e+00)

**Summary Statistics** (Common Observations):

| Statistic  |          Stata |         Python |     Difference | Std Difference |
|------------|----------------|----------------|----------------|----------------|
| count      |       1.43e+06 |       1.43e+06 |       1.43e+06 |       1.43e+06 |
| mean       |         1.0155 |         1.0155 |      -3.99e-08 |      -5.70e-09 |
| std        |         7.0022 |         7.0022 |       4.56e-05 |       6.51e-06 |
| min        |      -185.6921 |      -185.6921 |        -0.0424 |        -0.0061 |
| 25%        |        -0.0787 |        -0.0787 |      -8.38e-09 |      -1.20e-09 |
| 50%        |         0.2917 |         0.2917 |      -1.37e-12 |      -1.96e-13 |
| 75%        |         0.9448 |         0.9448 |       8.32e-09 |       1.19e-09 |
| max        |      2387.4009 |      2387.4008 |         0.0044 |       6.25e-04 |

**Regression Analysis** (Python ~ Stata):

- **Model**: python = -0.0000 + 1.0000 * stata
- **R-squared**: 1.0000
- **N observations**: 1,425,162

| Coefficient |     Estimate |    Std Error | t-statistic |   p-value |
|-------------|--------------|--------------|-------------|----------|
| Intercept   |    -3.49e-08 |     3.86e-08 |     -0.9055 |     0.365 |
| Slope       |       1.0000 |     5.45e-09 |    1.83e+08 |     0.000 |

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

**Precision2**: 99th percentile diff = 1.29e-07 (tolerance: < 1.00e+00)

**Summary Statistics** (Common Observations):

| Statistic  |          Stata |         Python |     Difference | Std Difference |
|------------|----------------|----------------|----------------|----------------|
| count      |       2.87e+06 |       2.87e+06 |       2.87e+06 |       2.87e+06 |
| mean       |         0.0161 |         0.0161 |       3.33e-07 |       2.41e-06 |
| std        |         0.1385 |         0.1385 |       1.10e-04 |       7.96e-04 |
| min        |        -0.9976 |        -0.9976 |      -3.46e-08 |      -2.50e-07 |
| 25%        |        -0.0217 |        -0.0217 |      -2.35e-10 |      -1.70e-09 |
| 50%        |        -0.0014 |        -0.0014 |         0.0000 |         0.0000 |
| 75%        |         0.0046 |         0.0046 |       2.30e-10 |       1.66e-09 |
| max        |         0.9999 |         0.9999 |         0.0482 |         0.3482 |

**Regression Analysis** (Python ~ Stata):

- **Model**: python = 0.0000 + 1.0000 * stata
- **R-squared**: 1.0000
- **N observations**: 2,874,470

| Coefficient |     Estimate |    Std Error | t-statistic |   p-value |
|-------------|--------------|--------------|-------------|----------|
| Intercept   |     3.20e-07 |     6.55e-08 |      4.8813 |     0.000 |
| Slope       |       1.0000 |     4.70e-07 |    2.13e+06 |     0.000 |

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

**Precision2**: 99th percentile diff = 3.17e-08 (tolerance: < 1.00e+00)

**Summary Statistics** (Common Observations):

| Statistic  |          Stata |         Python |     Difference | Std Difference |
|------------|----------------|----------------|----------------|----------------|
| count      |       1.82e+06 |       1.82e+06 |       1.82e+06 |       1.82e+06 |
| mean       |        -0.0082 |        -0.0082 |       1.99e-08 |       3.69e-08 |
| std        |         0.5406 |         0.5406 |       1.35e-05 |       2.50e-05 |
| min        |      -589.1729 |      -589.1729 |      -5.92e-06 |      -1.09e-05 |
| 25%        |        -0.0054 |        -0.0054 |      -4.40e-10 |      -8.13e-10 |
| 50%        |         0.0107 |         0.0107 |       2.50e-14 |       4.62e-14 |
| 75%        |         0.0389 |         0.0389 |       4.43e-10 |       8.20e-10 |
| max        |        19.2230 |        19.2230 |         0.0102 |         0.0189 |

**Regression Analysis** (Python ~ Stata):

- **Model**: python = 0.0000 + 1.0000 * stata
- **R-squared**: 1.0000
- **N observations**: 1,817,567

| Coefficient |     Estimate |    Std Error | t-statistic |   p-value |
|-------------|--------------|--------------|-------------|----------|
| Intercept   |     2.00e-08 |     1.00e-08 |      2.0018 |     0.045 |
| Slope       |       1.0000 |     1.85e-08 |    5.40e+07 |     0.000 |

**Feedback**:
- Num observations with std_diff >= TOL_DIFF_1: 4/1817567 (0.000%)
- Stata standard deviation: 5.41e-01

---

### NumEarnIncrease

**Status**: ✅ PASSED

**Test Results**:
- Test 1 - Column names: ✅ PASSED
- Test 2 - Superset check: ✅ PASSED
- Test 3 - Precision1 check: ✅ PASSED
- Test 4 - Precision2 check: ✅ PASSED

**Columns**: ['NumEarnIncrease']

**Observations**:
- Stata:  2,823,456
- Python: 2,823,459
- Common: 2,823,456

**Precision1**: 1.010% obs with std_diff >= 1.00e-02 (tolerance: < 10%)

**Precision2**: 99th percentile diff = 5.18e-01 (tolerance: < 1.00e+00)

**Summary Statistics** (Common Observations):

| Statistic  |          Stata |         Python |     Difference | Std Difference |
|------------|----------------|----------------|----------------|----------------|
| count      |       2.82e+06 |       2.82e+06 |       2.82e+06 |       2.82e+06 |
| mean       |         1.2268 |         1.1965 |        -0.0303 |        -0.0157 |
| std        |         1.9293 |         1.9120 |         0.3730 |         0.1933 |
| min        |         0.0000 |         0.0000 |        -8.0000 |        -4.1465 |
| 25%        |         0.0000 |         0.0000 |         0.0000 |         0.0000 |
| 50%        |         0.0000 |         0.0000 |         0.0000 |         0.0000 |
| 75%        |         2.0000 |         2.0000 |         0.0000 |         0.0000 |
| max        |         8.0000 |         8.0000 |         8.0000 |         4.1465 |

**Regression Analysis** (Python ~ Stata):

- **Model**: python = 0.0036 + 0.9724 * stata
- **R-squared**: 0.9627
- **N observations**: 2,823,456

| Coefficient |     Estimate |    Std Error | t-statistic |   p-value |
|-------------|--------------|--------------|-------------|----------|
| Intercept   |       0.0036 |     2.60e-04 |     13.8365 |     0.000 |
| Slope       |       0.9724 |     1.14e-04 |   8538.4923 |     0.000 |

**Feedback**:
- Num observations with std_diff >= TOL_DIFF_1: 28519/2823456 (1.010%)
- Stata standard deviation: 1.93e+00

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

**Precision2**: 99th percentile diff = 1.17e-07 (tolerance: < 1.00e+00)

**Summary Statistics** (Common Observations):

| Statistic  |          Stata |         Python |     Difference | Std Difference |
|------------|----------------|----------------|----------------|----------------|
| count      |       3.61e+06 |       3.61e+06 |       3.61e+06 |       3.61e+06 |
| mean       |         0.9531 |         0.9531 |       1.24e-06 |       1.03e-06 |
| std        |         1.2034 |         1.2034 |       6.03e-04 |       5.01e-04 |
| min        |        -0.7604 |        -0.7604 |        -0.0327 |        -0.0271 |
| 25%        |         0.2942 |         0.2942 |      -1.23e-08 |      -1.03e-08 |
| 50%        |         0.7583 |         0.7583 |      -3.22e-13 |      -2.67e-13 |
| 75%        |         1.3112 |         1.3112 |       1.21e-08 |       1.01e-08 |
| max        |       218.0000 |       218.0000 |         0.3060 |         0.2543 |

**Regression Analysis** (Python ~ Stata):

- **Model**: python = 0.0000 + 1.0000 * stata
- **R-squared**: 1.0000
- **N observations**: 3,607,726

| Coefficient |     Estimate |    Std Error | t-statistic |   p-value |
|-------------|--------------|--------------|-------------|----------|
| Intercept   |     3.46e-07 |     4.05e-07 |      0.8558 |     0.392 |
| Slope       |       1.0000 |     2.64e-07 |    3.79e+06 |     0.000 |

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

**Precision2**: 99th percentile diff = 0.00e+00 (tolerance: < 1.00e+00)

**Summary Statistics** (Common Observations):

| Statistic  |          Stata |         Python |     Difference | Std Difference |
|------------|----------------|----------------|----------------|----------------|
| count      |       1.20e+06 |       1.20e+06 |       1.20e+06 |       1.20e+06 |
| mean       |         0.1248 |         0.1248 |         0.0000 |         0.0000 |
| std        |         0.3305 |         0.3305 |         0.0000 |         0.0000 |
| min        |         0.0000 |         0.0000 |         0.0000 |         0.0000 |
| 25%        |         0.0000 |         0.0000 |         0.0000 |         0.0000 |
| 50%        |         0.0000 |         0.0000 |         0.0000 |         0.0000 |
| 75%        |         0.0000 |         0.0000 |         0.0000 |         0.0000 |
| max        |         1.0000 |         1.0000 |         0.0000 |         0.0000 |

**Regression Analysis** (Python ~ Stata):

- **Model**: python = 0.0000 + 1.0000 * stata
- **R-squared**: 1.0000
- **N observations**: 1,197,024

| Coefficient |     Estimate |    Std Error | t-statistic |   p-value |
|-------------|--------------|--------------|-------------|----------|
| Intercept   |     5.07e-13 |     1.25e-15 |    404.1856 |     0.000 |
| Slope       |       1.0000 |     3.55e-15 |    2.82e+14 |     0.000 |

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

**Precision2**: 99th percentile diff = 5.87e-09 (tolerance: < 1.00e+00)

**Summary Statistics** (Common Observations):

| Statistic  |          Stata |         Python |     Difference | Std Difference |
|------------|----------------|----------------|----------------|----------------|
| count      |       1.41e+06 |       1.41e+06 |       1.41e+06 |       1.41e+06 |
| mean       |         0.1773 |         0.1774 |       2.86e-06 |       1.77e-07 |
| std        |        16.1888 |        16.1888 |       8.05e-04 |       4.97e-05 |
| min        |     -5640.1177 |     -5640.1176 |        -0.0947 |        -0.0059 |
| 25%        |         0.1291 |         0.1291 |      -5.13e-09 |      -3.17e-10 |
| 50%        |         0.2478 |         0.2478 |         0.0000 |         0.0000 |
| 75%        |         0.3634 |         0.3634 |       5.15e-09 |       3.18e-10 |
| max        |       861.0132 |       861.0132 |         0.2514 |         0.0155 |

**Regression Analysis** (Python ~ Stata):

- **Model**: python = 0.0000 + 1.0000 * stata
- **R-squared**: 1.0000
- **N observations**: 1,407,636

| Coefficient |     Estimate |    Std Error | t-statistic |   p-value |
|-------------|--------------|--------------|-------------|----------|
| Intercept   |     2.86e-06 |     6.79e-07 |      4.2094 |     0.000 |
| Slope       |       1.0000 |     4.19e-08 |    2.39e+07 |     0.000 |

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

**Precision2**: 99th percentile diff = 8.47e-08 (tolerance: < 1.00e+00)

**Summary Statistics** (Common Observations):

| Statistic  |          Stata |         Python |     Difference | Std Difference |
|------------|----------------|----------------|----------------|----------------|
| count      |       2.10e+06 |       2.10e+06 |       2.10e+06 |       2.10e+06 |
| mean       |         0.1110 |         0.1110 |      -3.19e-08 |      -1.17e-07 |
| std        |         0.2735 |         0.2735 |       1.35e-04 |       4.93e-04 |
| min        |       -85.0000 |       -85.0000 |        -0.0441 |        -0.1613 |
| 25%        |         0.0650 |         0.0650 |      -2.97e-09 |      -1.09e-08 |
| 50%        |         0.1351 |         0.1351 |       3.91e-12 |       1.43e-11 |
| 75%        |         0.2031 |         0.2031 |       3.00e-09 |       1.10e-08 |
| max        |        47.9633 |        47.9633 |         0.0253 |         0.0925 |

**Regression Analysis** (Python ~ Stata):

- **Model**: python = -0.0000 + 1.0000 * stata
- **R-squared**: 1.0000
- **N observations**: 2,097,471

| Coefficient |     Estimate |    Std Error | t-statistic |   p-value |
|-------------|--------------|--------------|-------------|----------|
| Intercept   |    -8.98e-08 |     1.01e-07 |     -0.8937 |     0.371 |
| Slope       |       1.0000 |     3.41e-07 |    2.94e+06 |     0.000 |

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

**Precision2**: 99th percentile diff = 1.06e-07 (tolerance: < 1.00e+00)

**Summary Statistics** (Common Observations):

| Statistic  |          Stata |         Python |     Difference | Std Difference |
|------------|----------------|----------------|----------------|----------------|
| count      |    848962.0000 |    848962.0000 |    848962.0000 |    848962.0000 |
| mean       |       805.8956 |       805.6408 |        -0.2548 |      -1.43e-04 |
| std        |      1786.2602 |      1786.1673 |        27.6010 |         0.0155 |
| min        |         0.0000 |         0.0000 |     -5424.7268 |        -3.0369 |
| 25%        |       101.9062 |       101.8366 |      -5.79e-06 |      -3.24e-09 |
| 50%        |       330.4659 |       330.2790 |         0.0000 |         0.0000 |
| 75%        |       878.6225 |       878.2292 |       5.76e-06 |       3.22e-09 |
| max        |    337066.2500 |    337066.2623 |      2393.1331 |         1.3397 |

**Regression Analysis** (Python ~ Stata):

- **Model**: python = -0.1166 + 0.9998 * stata
- **R-squared**: 0.9998
- **N observations**: 848,962

| Coefficient |     Estimate |    Std Error | t-statistic |   p-value |
|-------------|--------------|--------------|-------------|----------|
| Intercept   |      -0.1166 |       0.0329 |     -3.5497 |     0.000 |
| Slope       |       0.9998 |     1.68e-05 |  59623.3162 |     0.000 |

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

**Precision2**: 99th percentile diff = 1.60e-08 (tolerance: < 1.00e+00)

**Summary Statistics** (Common Observations):

| Statistic  |          Stata |         Python |     Difference | Std Difference |
|------------|----------------|----------------|----------------|----------------|
| count      |    837442.0000 |    837442.0000 |    837442.0000 |    837442.0000 |
| mean       |         1.3220 |         1.3217 |      -3.26e-04 |      -1.50e-05 |
| std        |        21.6500 |        21.6495 |         0.1610 |         0.0074 |
| min        |         0.0000 |         0.0000 |      -124.1985 |        -5.7366 |
| 25%        |         0.5175 |         0.5174 |      -2.49e-08 |      -1.15e-09 |
| 50%        |         0.8744 |         0.8744 |         0.0000 |         0.0000 |
| 75%        |         1.3549 |         1.3549 |       2.50e-08 |       1.16e-09 |
| max        |     17723.5350 |     17723.5353 |        17.5184 |         0.8092 |

**Regression Analysis** (Python ~ Stata):

- **Model**: python = -0.0003 + 0.9999 * stata
- **R-squared**: 0.9999
- **N observations**: 837,442

| Coefficient |     Estimate |    Std Error | t-statistic |   p-value |
|-------------|--------------|--------------|-------------|----------|
| Intercept   |    -2.59e-04 |     1.76e-04 |     -1.4709 |     0.141 |
| Slope       |       0.9999 |     8.12e-06 | 123088.1204 |     0.000 |

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

**Precision2**: 99th percentile diff = 1.04e-07 (tolerance: < 1.00e+00)

**Summary Statistics** (Common Observations):

| Statistic  |          Stata |         Python |     Difference | Std Difference |
|------------|----------------|----------------|----------------|----------------|
| count      |    634164.0000 |    634164.0000 |    634164.0000 |    634164.0000 |
| mean       |         0.5886 |         0.5886 |      -1.74e-10 |      -1.49e-10 |
| std        |         1.1620 |         1.1620 |       3.60e-08 |       3.10e-08 |
| min        |       9.96e-06 |       9.96e-06 |      -2.71e-06 |      -2.33e-06 |
| 25%        |         0.1418 |         0.1418 |      -5.76e-09 |      -4.96e-09 |
| 50%        |         0.3146 |         0.3146 |       8.80e-12 |       7.57e-12 |
| 75%        |         0.6607 |         0.6607 |       5.88e-09 |       5.06e-09 |
| max        |       102.1352 |       102.1352 |       1.24e-06 |       1.07e-06 |

**Regression Analysis** (Python ~ Stata):

- **Model**: python = 0.0000 + 1.0000 * stata
- **R-squared**: 1.0000
- **N observations**: 634,164

| Coefficient |     Estimate |    Std Error | t-statistic |   p-value |
|-------------|--------------|--------------|-------------|----------|
| Intercept   |     3.36e-09 |     4.98e-11 |     67.4346 |     0.000 |
| Slope       |       1.0000 |     3.82e-11 |    2.62e+10 |     0.000 |

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

**Precision2**: 99th percentile diff = 2.20e-07 (tolerance: < 1.00e+00)

**Summary Statistics** (Common Observations):

| Statistic  |          Stata |         Python |     Difference | Std Difference |
|------------|----------------|----------------|----------------|----------------|
| count      |    564785.0000 |    564785.0000 |    564785.0000 |    564785.0000 |
| mean       |        -0.0077 |        -0.0077 |      -3.15e-07 |      -4.26e-07 |
| std        |         0.7388 |         0.7388 |       1.18e-04 |       1.60e-04 |
| min        |       -98.8127 |       -98.8127 |        -0.0444 |        -0.0601 |
| 25%        |        -0.0733 |        -0.0733 |      -7.55e-09 |      -1.02e-08 |
| 50%        |        -0.0035 |        -0.0035 |      -9.55e-12 |      -1.29e-11 |
| 75%        |         0.0562 |         0.0562 |       7.51e-09 |       1.02e-08 |
| max        |        73.7469 |        73.7469 |       2.13e-06 |       2.88e-06 |

**Regression Analysis** (Python ~ Stata):

- **Model**: python = -0.0000 + 1.0000 * stata
- **R-squared**: 1.0000
- **N observations**: 564,785

| Coefficient |     Estimate |    Std Error | t-statistic |   p-value |
|-------------|--------------|--------------|-------------|----------|
| Intercept   |    -3.11e-07 |     1.57e-07 |     -1.9758 |     0.048 |
| Slope       |       1.0000 |     2.13e-07 |    4.70e+06 |     0.000 |

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
- Test 4 - Precision2 check: ✅ PASSED

**Columns**: ['OrgCap']

**Observations**:
- Stata:  1,243,383
- Python: 1,327,508
- Common: 1,243,383

**Precision1**: 14.227% obs with std_diff >= 1.00e-02 (tolerance: < 10%)

**Precision2**: 99th percentile diff = 1.34e-01 (tolerance: < 1.00e+00)

**Summary Statistics** (Common Observations):

| Statistic  |          Stata |         Python |     Difference | Std Difference |
|------------|----------------|----------------|----------------|----------------|
| count      |       1.24e+06 |       1.24e+06 |       1.24e+06 |       1.24e+06 |
| mean       |       2.37e-10 |      -9.21e-04 |      -9.21e-04 |      -9.27e-04 |
| std        |         0.9941 |         0.9936 |         0.0410 |         0.0412 |
| min        |        -2.3446 |        -2.3446 |        -2.4134 |        -2.4279 |
| 25%        |        -0.6402 |        -0.6413 |      -3.04e-04 |      -3.06e-04 |
| 50%        |        -0.2736 |        -0.2745 |      -2.38e-08 |      -2.39e-08 |
| 75%        |         0.3358 |         0.3353 |       5.70e-04 |       5.74e-04 |
| max        |        10.1323 |        10.0846 |         0.5601 |         0.5634 |

**Regression Analysis** (Python ~ Stata):

- **Model**: python = -0.0009 + 0.9987 * stata
- **R-squared**: 0.9983
- **N observations**: 1,243,383

| Coefficient |     Estimate |    Std Error | t-statistic |   p-value |
|-------------|--------------|--------------|-------------|----------|
| Intercept   |    -9.21e-04 |     3.67e-05 |    -25.0657 |     0.000 |
| Slope       |       0.9987 |     3.70e-05 |  27016.1170 |     0.000 |

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
- Test 4 - Precision2 check: ✅ PASSED

**Columns**: ['PS']

**Observations**:
- Stata:  463,944
- Python: 464,239
- Common: 463,941

**Precision1**: 17.931% obs with std_diff >= 1.00e-02 (tolerance: < 10%)

**Precision2**: 99th percentile diff = 5.90e-01 (tolerance: < 1.00e+00)

**Summary Statistics** (Common Observations):

| Statistic  |          Stata |         Python |     Difference | Std Difference |
|------------|----------------|----------------|----------------|----------------|
| count      |    463941.0000 |    463941.0000 |    463941.0000 |    463941.0000 |
| mean       |         5.0197 |         4.9729 |        -0.0468 |        -0.0276 |
| std        |         1.6958 |         1.8091 |         0.4595 |         0.2709 |
| min        |         0.0000 |         0.0000 |        -5.0000 |        -2.9484 |
| 25%        |         4.0000 |         4.0000 |         0.0000 |         0.0000 |
| 50%        |         5.0000 |         5.0000 |         0.0000 |         0.0000 |
| 75%        |         6.0000 |         6.0000 |         0.0000 |         0.0000 |
| max        |         9.0000 |         9.0000 |         6.0000 |         3.5381 |

**Regression Analysis** (Python ~ Stata):

- **Model**: python = -0.2090 + 1.0323 * stata
- **R-squared**: 0.9364
- **N observations**: 463,941

| Coefficient |     Estimate |    Std Error | t-statistic |   p-value |
|-------------|--------------|--------------|-------------|----------|
| Intercept   |      -0.2090 |       0.0021 |    -99.8754 |     0.000 |
| Slope       |       1.0323 |     3.95e-04 |   2613.7993 |     0.000 |

**Feedback**:
- Num observations with std_diff >= TOL_DIFF_1: 83191/463941 (17.931%)
- Stata standard deviation: 1.70e+00

**Most Recent Bad Observations**:
```
   permno  yyyymm  python  stata  diff
0   11593  202412     5.0      6  -1.0
1   12641  202412     6.0      7  -1.0
2   13583  202412     8.0      7   1.0
3   13919  202412     5.0      6  -1.0
4   14419  202412     3.0      4  -1.0
5   14468  202412     3.0      4  -1.0
6   14540  202412     5.0      6  -1.0
7   14601  202412     5.0      6  -1.0
8   14791  202412     6.0      5   1.0
9   14826  202412     2.0      3  -1.0
```

**Largest Differences**:
```
   permno  yyyymm  python  stata  diff
0   10193  198802     7.0      1   6.0
1   10193  198803     7.0      1   6.0
2   10193  198809     1.0      6  -5.0
3   10193  198810     1.0      6  -5.0
4   10193  198811     1.0      6  -5.0
5   11317  198304     2.0      7  -5.0
6   11484  199603     1.0      6  -5.0
7   11538  199101     0.0      5  -5.0
8   11538  199102     0.0      5  -5.0
9   11538  199103     0.0      5  -5.0
```

---

### PatentsRD

**Status**: ❌ FAILED

**Test Results**:
- Test 1 - Column names: ✅ PASSED
- Test 2 - Superset check: ❌ FAILED (Python missing 155256 Stata observations)
- Test 3 - Precision1 check: ✅ PASSED
- Test 4 - Precision2 check: ❌ FAILED

**Columns**: ['PatentsRD']

**Observations**:
- Stata:  671,832
- Python: 519,948
- Common: 516,576

**Precision1**: 6.651% obs with std_diff >= 1.00e-02 (tolerance: < 10%)

**Precision2**: 99th percentile diff = 2.25e+00 (tolerance: < 1.00e+00)

**Summary Statistics** (Common Observations):

| Statistic  |          Stata |         Python |     Difference | Std Difference |
|------------|----------------|----------------|----------------|----------------|
| count      |    516576.0000 |    516576.0000 |    516576.0000 |    516576.0000 |
| mean       |         0.2728 |         0.3393 |         0.0665 |         0.1493 |
| std        |         0.4454 |         0.4735 |         0.2492 |         0.5594 |
| min        |         0.0000 |         0.0000 |         0.0000 |         0.0000 |
| 25%        |         0.0000 |         0.0000 |         0.0000 |         0.0000 |
| 50%        |         0.0000 |         0.0000 |         0.0000 |         0.0000 |
| 75%        |         1.0000 |         1.0000 |         0.0000 |         0.0000 |
| max        |         1.0000 |         1.0000 |         1.0000 |         2.2451 |

**Regression Analysis** (Python ~ Stata):

- **Model**: python = 0.0915 + 0.9085 * stata
- **R-squared**: 0.7305
- **N observations**: 516,576

| Coefficient |     Estimate |    Std Error | t-statistic |   p-value |
|-------------|--------------|--------------|-------------|----------|
| Intercept   |       0.0915 |     4.01e-04 |    228.0366 |     0.000 |
| Slope       |       0.9085 |     7.68e-04 |   1183.2038 |     0.000 |

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
- Num observations with std_diff >= TOL_DIFF_1: 34356/516576 (6.651%)
- Stata standard deviation: 4.45e-01

**Most Recent Bad Observations**:
```
   permno  yyyymm  python  stata  diff
0   10258  202305     1.0      0   1.0
1   10966  202305     1.0      0   1.0
2   11370  202305     1.0      0   1.0
3   12009  202305     1.0      0   1.0
4   12078  202305     1.0      0   1.0
5   12307  202305     1.0      0   1.0
6   12358  202305     1.0      0   1.0
7   12360  202305     1.0      0   1.0
8   12411  202305     1.0      0   1.0
9   12488  202305     1.0      0   1.0
```

**Largest Differences**:
```
   permno  yyyymm  python  stata  diff
0   10158  201506     1.0      0   1.0
1   10158  201507     1.0      0   1.0
2   10158  201508     1.0      0   1.0
3   10158  201509     1.0      0   1.0
4   10158  201510     1.0      0   1.0
5   10158  201511     1.0      0   1.0
6   10158  201512     1.0      0   1.0
7   10158  201601     1.0      0   1.0
8   10158  201602     1.0      0   1.0
9   10158  201603     1.0      0   1.0
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

**Precision2**: 99th percentile diff = 5.91e-08 (tolerance: < 1.00e+00)

**Summary Statistics** (Common Observations):

| Statistic  |          Stata |         Python |     Difference | Std Difference |
|------------|----------------|----------------|----------------|----------------|
| count      |       1.42e+06 |       1.42e+06 |       1.42e+06 |       1.42e+06 |
| mean       |         0.1105 |         0.1105 |       2.55e-08 |       5.36e-08 |
| std        |         0.4766 |         0.4766 |       1.53e-05 |       3.20e-05 |
| min        |       5.47e-08 |       5.47e-08 |      -1.99e-06 |      -4.17e-06 |
| 25%        |         0.0153 |         0.0153 |      -6.85e-10 |      -1.44e-09 |
| 50%        |         0.0377 |         0.0377 |      -1.03e-14 |      -2.16e-14 |
| 75%        |         0.0825 |         0.0825 |       6.82e-10 |       1.43e-09 |
| max        |       204.5146 |       204.5146 |         0.0102 |         0.0215 |

**Regression Analysis** (Python ~ Stata):

- **Model**: python = 0.0000 + 1.0000 * stata
- **R-squared**: 1.0000
- **N observations**: 1,419,344

| Coefficient |     Estimate |    Std Error | t-statistic |   p-value |
|-------------|--------------|--------------|-------------|----------|
| Intercept   |     2.66e-08 |     1.32e-08 |      2.0239 |     0.043 |
| Slope       |       1.0000 |     2.69e-08 |    3.72e+07 |     0.000 |

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

**Precision2**: 99th percentile diff = 1.10e-08 (tolerance: < 1.00e+00)

**Summary Statistics** (Common Observations):

| Statistic  |          Stata |         Python |     Difference | Std Difference |
|------------|----------------|----------------|----------------|----------------|
| count      |       3.17e+06 |       3.17e+06 |       3.17e+06 |       3.17e+06 |
| mean       |        -1.6989 |        -1.6989 |      -3.80e-05 |      -3.96e-07 |
| std        |        95.9587 |        95.9587 |         0.0196 |       2.04e-04 |
| min        |    -22400.0000 |    -22400.0000 |       -10.0625 |        -0.1049 |
| 25%        |        -1.2865 |        -1.2865 |      -1.59e-08 |      -1.66e-10 |
| 50%        |        -0.3594 |        -0.3594 |         0.0000 |         0.0000 |
| 75%        |         0.4757 |         0.4757 |       1.60e-08 |       1.66e-10 |
| max        |     14452.5710 |     14452.5714 |         0.0086 |       8.99e-05 |

**Regression Analysis** (Python ~ Stata):

- **Model**: python = -0.0000 + 1.0000 * stata
- **R-squared**: 1.0000
- **N observations**: 3,174,456

| Coefficient |     Estimate |    Std Error | t-statistic |   p-value |
|-------------|--------------|--------------|-------------|----------|
| Intercept   |    -3.80e-05 |     1.10e-05 |     -3.4641 |     0.001 |
| Slope       |       1.0000 |     1.14e-07 |    8.74e+06 |     0.000 |

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

**Precision2**: 99th percentile diff = 7.89e-09 (tolerance: < 1.00e+00)

**Summary Statistics** (Common Observations):

| Statistic  |          Stata |         Python |     Difference | Std Difference |
|------------|----------------|----------------|----------------|----------------|
| count      |       2.41e+06 |       2.41e+06 |       2.41e+06 |       2.41e+06 |
| mean       |         2.5870 |         2.5870 |      -3.44e-05 |      -2.41e-07 |
| std        |       142.8889 |       142.8889 |         0.0070 |       4.90e-05 |
| min        |    -11719.7500 |    -11719.7500 |        -2.8089 |        -0.0197 |
| 25%        |        -0.6329 |        -0.6330 |      -1.78e-08 |      -1.24e-10 |
| 50%        |         0.4821 |         0.4820 |         0.0000 |         0.0000 |
| 75%        |         1.2312 |         1.2311 |       1.77e-08 |       1.24e-10 |
| max        |     49788.3980 |     49788.4000 |         0.2164 |         0.0015 |

**Regression Analysis** (Python ~ Stata):

- **Model**: python = -0.0000 + 1.0000 * stata
- **R-squared**: 1.0000
- **N observations**: 2,412,359

| Coefficient |     Estimate |    Std Error | t-statistic |   p-value |
|-------------|--------------|--------------|-------------|----------|
| Intercept   |    -3.45e-05 |     4.51e-06 |     -7.6530 |     0.000 |
| Slope       |       1.0000 |     3.15e-08 |    3.17e+07 |     0.000 |

**Feedback**:
- Num observations with std_diff >= TOL_DIFF_1: 12/2412359 (0.000%)
- Stata standard deviation: 1.43e+02

---

### PredictedFE

**Status**: ✅ PASSED (with override)

**Override Applied**:
- Reviewed on: 2025-08-13
- Reviewed by: ac
- Details: The standardized deviation is on average 1% with a sd of 7 pp. So it's above the threshold, but it's small. Sumstats and regressions show that the replication works very well. Regressing python on stata shows that the coefficient is 0.9959 and the Rsq is 0.995. This is a complicated file, so it makes sense that there will be some deviations later in the code, which is where PredictedFE is created.

**Test Results**:
- Test 1 - Column names: ✅ PASSED
- Test 2 - Superset check: ✅ PASSED
- Test 3 - Precision1 check: ❌ FAILED
- Test 4 - Precision2 check: ✅ PASSED

**Columns**: ['PredictedFE']

**Observations**:
- Stata:  491,508
- Python: 622,380
- Common: 490,188

**Precision1**: 85.268% obs with std_diff >= 1.00e-02 (tolerance: < 10%)

**Precision2**: 99th percentile diff = 2.10e-01 (tolerance: < 1.00e+00)

**Summary Statistics** (Common Observations):

| Statistic  |          Stata |         Python |     Difference | Std Difference |
|------------|----------------|----------------|----------------|----------------|
| count      |    490188.0000 |    490188.0000 |    490188.0000 |    490188.0000 |
| mean       |         0.0519 |         0.0523 |       4.00e-04 |         0.0126 |
| std        |         0.0316 |         0.0316 |         0.0022 |         0.0695 |
| min        |        -0.1080 |        -0.1098 |        -0.0430 |        -1.3585 |
| 25%        |         0.0308 |         0.0310 |      -8.23e-04 |        -0.0260 |
| 50%        |         0.0476 |         0.0480 |       3.15e-04 |         0.0100 |
| 75%        |         0.0681 |         0.0685 |         0.0016 |         0.0519 |
| max        |         0.2809 |         0.2700 |         0.0289 |         0.9139 |

**Regression Analysis** (Python ~ Stata):

- **Model**: python = 0.0006 + 0.9959 * stata
- **R-squared**: 0.9952
- **N observations**: 490,188

| Coefficient |     Estimate |    Std Error | t-statistic |   p-value |
|-------------|--------------|--------------|-------------|----------|
| Intercept   |     6.10e-04 |     6.02e-06 |    101.2931 |     0.000 |
| Slope       |       0.9959 |     9.91e-05 |  10051.6551 |     0.000 |

**Feedback**:
- Num observations with std_diff >= TOL_DIFF_1: 417972/490188 (85.268%)
- Stata standard deviation: 3.16e-02

**Most Recent Bad Observations**:
```
   permno  yyyymm    python     stata      diff
0   10107  202505  0.083963  0.078498  0.005465
1   10145  202505  0.044157  0.040432  0.003725
2   10200  202505  0.115949  0.113642  0.002307
3   10397  202505  0.049261  0.049793 -0.000531
4   10606  202505  0.046297  0.044046  0.002251
5   10693  202505  0.042425  0.036774  0.005651
6   10696  202505  0.107327  0.105464  0.001862
7   11308  202505  0.073800  0.072780  0.001020
8   11403  202505  0.095454  0.090274  0.005179
9   11547  202505  0.080375  0.076702  0.003674
```

**Largest Differences**:
```
   permno  yyyymm    python     stata      diff
0   91575  202106  0.008267  0.051235 -0.042968
1   91575  202107  0.008267  0.051235 -0.042968
2   91575  202108  0.008267  0.051235 -0.042968
3   91575  202109  0.008267  0.051235 -0.042968
4   91575  202110  0.008267  0.051235 -0.042968
5   91575  202111  0.008267  0.051235 -0.042968
6   91575  202112  0.008267  0.051235 -0.042968
7   91575  202201  0.008267  0.051235 -0.042968
8   91575  202202  0.008267  0.051235 -0.042968
9   91575  202203  0.008267  0.051235 -0.042968
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

**Precision2**: 99th percentile diff = 1.51e-07 (tolerance: < 1.00e+00)

**Summary Statistics** (Common Observations):

| Statistic  |          Stata |         Python |     Difference | Std Difference |
|------------|----------------|----------------|----------------|----------------|
| count      |       4.03e+06 |       4.03e+06 |       4.03e+06 |       4.03e+06 |
| mean       |         2.3896 |         2.3896 |      -5.50e-09 |      -4.14e-09 |
| std        |         1.3279 |         1.3279 |       7.22e-08 |       5.43e-08 |
| min        |        -4.8536 |        -4.8536 |      -9.12e-07 |      -6.87e-07 |
| 25%        |         1.6214 |         1.6214 |      -4.87e-08 |      -3.67e-08 |
| 50%        |         2.5887 |         2.5887 |      -3.86e-09 |      -2.91e-09 |
| 75%        |         3.3080 |         3.3080 |       4.02e-08 |       3.03e-08 |
| max        |        13.4926 |        13.4926 |       8.70e-07 |       6.55e-07 |

**Regression Analysis** (Python ~ Stata):

- **Model**: python = -0.0000 + 1.0000 * stata
- **R-squared**: 1.0000
- **N observations**: 4,029,252

| Coefficient |     Estimate |    Std Error | t-statistic |   p-value |
|-------------|--------------|--------------|-------------|----------|
| Intercept   |    -3.19e-09 |     7.40e-11 |    -43.0915 |     0.000 |
| Slope       |       1.0000 |     2.71e-11 |    3.69e+10 |     0.000 |

**Feedback**:
- Num observations with std_diff >= TOL_DIFF_1: 0/4029252 (0.000%)
- Stata standard deviation: 1.33e+00

---

### PriceDelayRsq

**Status**: ✅ PASSED

**Test Results**:
- Test 1 - Column names: ✅ PASSED
- Test 2 - Superset check: ✅ PASSED
- Test 3 - Precision1 check: ✅ PASSED
- Test 4 - Precision2 check: ✅ PASSED

**Columns**: ['PriceDelayRsq']

**Observations**:
- Stata:  4,630,424
- Python: 4,636,840
- Common: 4,630,424

**Precision1**: 1.210% obs with std_diff >= 1.00e-02 (tolerance: < 10%)

**Precision2**: 99th percentile diff = 1.86e-01 (tolerance: < 1.00e+00)

**Summary Statistics** (Common Observations):

| Statistic  |          Stata |         Python |     Difference | Std Difference |
|------------|----------------|----------------|----------------|----------------|
| count      |       4.63e+06 |       4.63e+06 |       4.63e+06 |       4.63e+06 |
| mean       |         0.3626 |         0.3636 |         0.0010 |         0.0032 |
| std        |         0.3266 |         0.3273 |         0.0385 |         0.1179 |
| min        |       5.86e-06 |       5.86e-06 |        -0.9410 |        -2.8811 |
| 25%        |         0.0727 |         0.0727 |      -7.16e-09 |      -2.19e-08 |
| 50%        |         0.2485 |         0.2494 |      -2.94e-11 |      -9.02e-11 |
| 75%        |         0.6262 |         0.6293 |       6.55e-09 |       2.01e-08 |
| max        |         1.0000 |         1.0000 |         0.9574 |         2.9313 |

**Regression Analysis** (Python ~ Stata):

- **Model**: python = 0.0028 + 0.9952 * stata
- **R-squared**: 0.9862
- **N observations**: 4,630,424

| Coefficient |     Estimate |    Std Error | t-statistic |   p-value |
|-------------|--------------|--------------|-------------|----------|
| Intercept   |       0.0028 |     2.67e-05 |    104.3648 |     0.000 |
| Slope       |       0.9952 |     5.48e-05 |  18174.8448 |     0.000 |

**Feedback**:
- Num observations with std_diff >= TOL_DIFF_1: 56040/4630424 (1.210%)
- Stata standard deviation: 3.27e-01

---

### PriceDelaySlope

**Status**: ✅ PASSED

**Test Results**:
- Test 1 - Column names: ✅ PASSED
- Test 2 - Superset check: ✅ PASSED
- Test 3 - Precision1 check: ✅ PASSED
- Test 4 - Precision2 check: ✅ PASSED

**Columns**: ['PriceDelaySlope']

**Observations**:
- Stata:  4,630,424
- Python: 4,636,840
- Common: 4,630,424

**Precision1**: 0.582% obs with std_diff >= 1.00e-02 (tolerance: < 10%)

**Precision2**: 99th percentile diff = 2.89e-03 (tolerance: < 1.00e+00)

**Summary Statistics** (Common Observations):

| Statistic  |          Stata |         Python |     Difference | Std Difference |
|------------|----------------|----------------|----------------|----------------|
| count      |       4.63e+06 |       4.63e+06 |       4.63e+06 |       4.63e+06 |
| mean       |        -0.1887 |        -0.2304 |        -0.0418 |      -1.66e-04 |
| std        |       251.9312 |       250.4707 |        28.6307 |         0.1136 |
| min        |    -85166.8980 |    -85251.4764 |    -15941.3451 |       -63.2766 |
| 25%        |        -0.2251 |        -0.2250 |      -5.97e-08 |      -2.37e-10 |
| 50%        |         0.4319 |         0.4334 |      -1.01e-09 |      -4.01e-12 |
| 75%        |         1.2235 |         1.2261 |       5.04e-08 |       2.00e-10 |
| max        |     60258.0310 |     60248.4687 |      6282.3819 |        24.9369 |

**Regression Analysis** (Python ~ Stata):

- **Model**: python = -0.0441 + 0.9878 * stata
- **R-squared**: 0.9871
- **N observations**: 4,630,424

| Coefficient |     Estimate |    Std Error | t-statistic |   p-value |
|-------------|--------------|--------------|-------------|----------|
| Intercept   |      -0.0441 |       0.0132 |     -3.3330 |     0.001 |
| Slope       |       0.9878 |     5.25e-05 |  18812.4694 |     0.000 |

**Feedback**:
- Num observations with std_diff >= TOL_DIFF_1: 26952/4630424 (0.582%)
- Stata standard deviation: 2.52e+02

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

**Precision2**: 99th percentile diff = 4.40e+00 (tolerance: < 1.00e+00)

**Summary Statistics** (Common Observations):

| Statistic  |          Stata |         Python |     Difference | Std Difference |
|------------|----------------|----------------|----------------|----------------|
| count      |       4.52e+06 |       4.52e+06 |       4.52e+06 |       4.52e+06 |
| mean       |         1.6229 |         1.6095 |        -0.0134 |        -0.0097 |
| std        |         1.3836 |         1.9491 |         1.6083 |         1.1624 |
| min        |        -5.3533 |        -5.3261 |        -9.8548 |        -7.1223 |
| 25%        |         0.8336 |         0.5661 |      -1.57e-07 |      -1.13e-07 |
| 50%        |         1.6661 |         1.6681 |      -5.39e-10 |      -3.89e-10 |
| 75%        |         2.4069 |         2.6390 |       1.49e-07 |       1.07e-07 |
| max        |         7.5741 |         7.5741 |        10.7693 |         7.7833 |

**Regression Analysis** (Python ~ Stata):

- **Model**: python = 0.2841 + 0.8167 * stata
- **R-squared**: 0.3361
- **N observations**: 4,523,656

| Coefficient |     Estimate |    Std Error | t-statistic |   p-value |
|-------------|--------------|--------------|-------------|----------|
| Intercept   |       0.2841 |       0.0012 |    246.8524 |     0.000 |
| Slope       |       0.8167 |     5.40e-04 |   1513.3190 |     0.000 |

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

**Precision2**: 99th percentile diff = 4.50e-07 (tolerance: < 1.00e+00)

**Summary Statistics** (Common Observations):

| Statistic  |          Stata |         Python |     Difference | Std Difference |
|------------|----------------|----------------|----------------|----------------|
| count      |     24028.0000 |     24028.0000 |     24028.0000 |     24028.0000 |
| mean       |         0.1930 |         0.1930 |       2.66e-10 |       3.99e-09 |
| std        |         0.0667 |         0.0667 |       1.12e-08 |       1.68e-07 |
| min        |         0.0191 |         0.0191 |      -4.00e-08 |      -5.99e-07 |
| 25%        |         0.1469 |         0.1469 |         0.0000 |         0.0000 |
| 50%        |         0.1935 |         0.1935 |         0.0000 |         0.0000 |
| 75%        |         0.2405 |         0.2405 |         0.0000 |         0.0000 |
| max        |         0.4767 |         0.4767 |       5.00e-08 |       7.49e-07 |

**Regression Analysis** (Python ~ Stata):

- **Model**: python = -0.0000 + 1.0000 * stata
- **R-squared**: 1.0000
- **N observations**: 24,028

| Coefficient |     Estimate |    Std Error | t-statistic |   p-value |
|-------------|--------------|--------------|-------------|----------|
| Intercept   |    -6.59e-10 |     2.21e-10 |     -2.9775 |     0.003 |
| Slope       |       1.0000 |     1.08e-09 |    9.23e+08 |     0.000 |

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

**Precision2**: 99th percentile diff = 2.10e-08 (tolerance: < 1.00e+00)

**Summary Statistics** (Common Observations):

| Statistic  |          Stata |         Python |     Difference | Std Difference |
|------------|----------------|----------------|----------------|----------------|
| count      |       1.42e+06 |       1.42e+06 |       1.42e+06 |       1.42e+06 |
| mean       |         0.0927 |         0.0927 |      -5.77e-08 |      -4.81e-08 |
| std        |         1.1988 |         1.1988 |       2.60e-05 |       2.17e-05 |
| min        |        -0.0744 |        -0.0744 |        -0.0132 |        -0.0110 |
| 25%        |         0.0061 |         0.0061 |      -4.62e-10 |      -3.86e-10 |
| 50%        |         0.0273 |         0.0273 |         0.0000 |         0.0000 |
| 75%        |         0.0770 |         0.0770 |       4.61e-10 |       3.85e-10 |
| max        |      1344.9330 |      1344.9330 |       2.08e-06 |       1.73e-06 |

**Regression Analysis** (Python ~ Stata):

- **Model**: python = -0.0000 + 1.0000 * stata
- **R-squared**: 1.0000
- **N observations**: 1,419,136

| Coefficient |     Estimate |    Std Error | t-statistic |   p-value |
|-------------|--------------|--------------|-------------|----------|
| Intercept   |    -5.56e-08 |     2.19e-08 |     -2.5371 |     0.011 |
| Slope       |       1.0000 |     1.82e-08 |    5.48e+07 |     0.000 |

**Feedback**:
- Num observations with std_diff >= TOL_DIFF_1: 2/1419136 (0.000%)
- Stata standard deviation: 1.20e+00

---

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

**Precision2**: 99th percentile diff = 1.01e-08 (tolerance: < 1.00e+00)

**Summary Statistics** (Common Observations):

| Statistic  |          Stata |         Python |     Difference | Std Difference |
|------------|----------------|----------------|----------------|----------------|
| count      |       2.73e+06 |       2.73e+06 |       2.73e+06 |       2.73e+06 |
| mean       |      -142.9794 |      -142.9786 |       7.27e-04 |       9.15e-08 |
| std        |      7944.9900 |      7944.9890 |         0.1932 |       2.43e-05 |
| min        |      -2.68e+06 |      -2.68e+06 |        -0.3460 |      -4.35e-05 |
| 25%        |        -6.6615 |        -6.6611 |      -1.00e-08 |      -1.26e-12 |
| 50%        |        -0.0935 |        -0.0935 |         0.0000 |         0.0000 |
| 75%        |         0.7535 |         0.7535 |       1.00e-08 |       1.26e-12 |
| max        |    692140.2500 |    692140.2477 |        71.2982 |         0.0090 |

**Regression Analysis** (Python ~ Stata):

- **Model**: python = 0.0007 + 1.0000 * stata
- **R-squared**: 1.0000
- **N observations**: 2,725,375

| Coefficient |     Estimate |    Std Error | t-statistic |   p-value |
|-------------|--------------|--------------|-------------|----------|
| Intercept   |     7.10e-04 |     1.17e-04 |      6.0629 |     0.000 |
| Slope       |       1.0000 |     1.47e-08 |    6.79e+07 |     0.000 |

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
- Python: 1,403,949
- Common: 517,652

**Precision1**: 0.000% obs with std_diff >= 1.00e-02 (tolerance: < 10%)

**Precision2**: 99th percentile diff = 1.20e-07 (tolerance: < 1.00e+00)

**Summary Statistics** (Common Observations):

| Statistic  |          Stata |         Python |     Difference | Std Difference |
|------------|----------------|----------------|----------------|----------------|
| count      |    517652.0000 |    517652.0000 |    517652.0000 |    517652.0000 |
| mean       |         0.2067 |         0.2067 |       7.47e-12 |       1.07e-11 |
| std        |         0.6976 |         0.6976 |       2.23e-08 |       3.20e-08 |
| min        |        -0.0011 |        -0.0011 |      -1.04e-06 |      -1.49e-06 |
| 25%        |         0.0000 |         0.0000 |         0.0000 |         0.0000 |
| 50%        |         0.0000 |         0.0000 |         0.0000 |         0.0000 |
| 75%        |         0.1533 |         0.1533 |         0.0000 |         0.0000 |
| max        |        34.7810 |        34.7810 |       1.32e-06 |       1.90e-06 |

**Regression Analysis** (Python ~ Stata):

- **Model**: python = -0.0000 + 1.0000 * stata
- **R-squared**: 1.0000
- **N observations**: 517,652

| Coefficient |     Estimate |    Std Error | t-statistic |   p-value |
|-------------|--------------|--------------|-------------|----------|
| Intercept   |    -1.64e-10 |     3.24e-11 |     -5.0527 |     0.000 |
| Slope       |       1.0000 |     4.45e-11 |    2.25e+10 |     0.000 |

**Feedback**:
- Num observations with std_diff >= TOL_DIFF_1: 0/517652 (0.000%)
- Stata standard deviation: 6.98e-01

---

### REV6

**Status**: ✅ PASSED

**Test Results**:
- Test 1 - Column names: ✅ PASSED
- Test 2 - Superset check: ✅ PASSED
- Test 3 - Precision1 check: ✅ PASSED
- Test 4 - Precision2 check: ✅ PASSED

**Columns**: ['REV6']

**Observations**:
- Stata:  1,762,090
- Python: 4,003,555
- Common: 1,762,090

**Precision1**: 0.166% obs with std_diff >= 1.00e-02 (tolerance: < 10%)

**Precision2**: 99th percentile diff = 1.24e-03 (tolerance: < 1.00e+00)

**Summary Statistics** (Common Observations):

| Statistic  |          Stata |         Python |     Difference | Std Difference |
|------------|----------------|----------------|----------------|----------------|
| count      |       1.76e+06 |       1.76e+06 |       1.76e+06 |       1.76e+06 |
| mean       |        -0.0684 |        -0.0644 |         0.0040 |       6.21e-05 |
| std        |        64.8335 |        65.3305 |         8.3361 |         0.1286 |
| min        |    -58190.5590 |    -58190.5598 |     -3284.2074 |       -50.6560 |
| 25%        |        -0.0119 |        -0.0122 |      -9.78e-10 |      -1.51e-11 |
| 50%        |         0.0016 |         0.0016 |         0.0000 |         0.0000 |
| 75%        |         0.0124 |         0.0126 |       9.76e-10 |       1.50e-11 |
| max        |     32747.2600 |     32748.0882 |      8424.1383 |       129.9349 |

**Regression Analysis** (Python ~ Stata):

- **Model**: python = 0.0040 + 0.9994 * stata
- **R-squared**: 0.9837
- **N observations**: 1,762,090

| Coefficient |     Estimate |    Std Error | t-statistic |   p-value |
|-------------|--------------|--------------|-------------|----------|
| Intercept   |       0.0040 |       0.0063 |      0.6348 |     0.526 |
| Slope       |       0.9994 |     9.69e-05 |  10318.2292 |     0.000 |

**Feedback**:
- Num observations with std_diff >= TOL_DIFF_1: 2923/1762090 (0.166%)
- Stata standard deviation: 6.48e+01

---

### RIO_Disp

**Status**: ❌ FAILED

**Test Results**:
- Test 1 - Column names: ✅ PASSED
- Test 2 - Superset check: ❌ FAILED (Python missing 225106 Stata observations)
- Test 3 - Precision1 check: ❌ FAILED
- Test 4 - Precision2 check: ❌ FAILED

**Columns**: ['RIO_Disp']

**Observations**:
- Stata:  497,437
- Python: 376,371
- Common: 272,331

**Precision1**: 66.702% obs with std_diff >= 1.00e-02 (tolerance: < 10%)

**Precision2**: 99th percentile diff = 1.59e+00 (tolerance: < 1.00e+00)

**Summary Statistics** (Common Observations):

| Statistic  |          Stata |         Python |     Difference | Std Difference |
|------------|----------------|----------------|----------------|----------------|
| count      |    272331.0000 |    272331.0000 |    272331.0000 |    272331.0000 |
| mean       |         3.6284 |         2.8847 |        -0.7438 |        -0.5920 |
| std        |         1.2564 |         1.1308 |         0.6718 |         0.5347 |
| min        |         1.0000 |         1.0000 |        -4.0000 |        -3.1836 |
| 25%        |         3.0000 |         2.0000 |        -1.0000 |        -0.7959 |
| 50%        |         4.0000 |         3.0000 |        -1.0000 |        -0.7959 |
| 75%        |         5.0000 |         4.0000 |         0.0000 |         0.0000 |
| max        |         5.0000 |         5.0000 |         4.0000 |         3.1836 |

**Regression Analysis** (Python ~ Stata):

- **Model**: python = 0.1197 + 0.7620 * stata
- **R-squared**: 0.7169
- **N observations**: 272,331

| Coefficient |     Estimate |    Std Error | t-statistic |   p-value |
|-------------|--------------|--------------|-------------|----------|
| Intercept   |       0.1197 |       0.0035 |     33.9746 |     0.000 |
| Slope       |       0.7620 |     9.18e-04 |    830.4437 |     0.000 |

**Missing Observations Sample**:
```
 index  permno  yyyymm  RIO_Disp
     0   10002  200603         3
     1   10002  200604         3
     2   10002  200605         3
     3   10002  200708         3
     4   10002  200803         3
     5   10002  200804         3
     6   10002  200902         4
     7   10002  200903         3
     8   10002  200904         3
     9   10008  198708         5
```

**Feedback**:
- Num observations with std_diff >= TOL_DIFF_1: 181650/272331 (66.702%)
- Stata standard deviation: 1.26e+00

**Most Recent Bad Observations**:
```
   permno  yyyymm  python  stata  diff
0   10026  202412     2.0      3  -1.0
1   10032  202412     3.0      4  -1.0
2   10501  202412     3.0      5  -2.0
3   10547  202412     3.0      4  -1.0
4   10966  202412     4.0      5  -1.0
5   11174  202412     4.0      5  -1.0
6   12211  202412     3.0      4  -1.0
7   12623  202412     2.0      3  -1.0
8   13108  202412     3.0      4  -1.0
9   13918  202412     4.0      5  -1.0
```

**Largest Differences**:
```
   permno  yyyymm  python  stata  diff
0   10353  198812     1.0      5  -4.0
1   10564  200003     1.0      5  -4.0
2   10739  198707     1.0      5  -4.0
3   10739  198708     1.0      5  -4.0
4   10745  198801     1.0      5  -4.0
5   10745  198802     1.0      5  -4.0
6   10885  198909     1.0      5  -4.0
7   10929  199709     1.0      5  -4.0
8   10929  199710     1.0      5  -4.0
9   11379  198901     1.0      5  -4.0
```

---

### RIO_MB

**Status**: ❌ FAILED

**Test Results**:
- Test 1 - Column names: ✅ PASSED
- Test 2 - Superset check: ❌ FAILED (Python missing 128451 Stata observations)
- Test 3 - Precision1 check: ❌ FAILED
- Test 4 - Precision2 check: ❌ FAILED

**Columns**: ['RIO_MB']

**Observations**:
- Stata:  354,170
- Python: 364,989
- Common: 225,719

**Precision1**: 50.696% obs with std_diff >= 1.00e-02 (tolerance: < 10%)

**Precision2**: 99th percentile diff = 1.47e+00 (tolerance: < 1.00e+00)

**Summary Statistics** (Common Observations):

| Statistic  |          Stata |         Python |     Difference | Std Difference |
|------------|----------------|----------------|----------------|----------------|
| count      |    225719.0000 |    225719.0000 |    225719.0000 |    225719.0000 |
| mean       |         2.7953 |         2.2698 |        -0.5255 |        -0.3866 |
| std        |         1.3595 |         1.1495 |         0.6765 |         0.4976 |
| min        |         1.0000 |         1.0000 |        -4.0000 |        -2.9423 |
| 25%        |         2.0000 |         1.0000 |        -1.0000 |        -0.7356 |
| 50%        |         3.0000 |         2.0000 |         0.0000 |         0.0000 |
| 75%        |         4.0000 |         3.0000 |         0.0000 |         0.0000 |
| max        |         5.0000 |         5.0000 |         4.0000 |         2.9423 |

**Regression Analysis** (Python ~ Stata):

- **Model**: python = 0.2190 + 0.7337 * stata
- **R-squared**: 0.7529
- **N observations**: 225,719

| Coefficient |     Estimate |    Std Error | t-statistic |   p-value |
|-------------|--------------|--------------|-------------|----------|
| Intercept   |       0.2190 |       0.0028 |     79.6197 |     0.000 |
| Slope       |       0.7337 |     8.85e-04 |    829.2439 |     0.000 |

**Missing Observations Sample**:
```
 index  permno  yyyymm  RIO_MB
     0   10010  199109       4
     1   10010  199203       3
     2   10010  199208       3
     3   10010  199211       4
     4   10010  199212       3
     5   10010  199301       3
     6   10010  199302       3
     7   10010  199410       4
     8   10010  199505       5
     9   10010  199507       5
```

**Feedback**:
- Num observations with std_diff >= TOL_DIFF_1: 114430/225719 (50.696%)
- Stata standard deviation: 1.36e+00

**Most Recent Bad Observations**:
```
   permno  yyyymm  python  stata  diff
0   10220  202412     2.0      3  -1.0
1   10966  202412     4.0      5  -1.0
2   11618  202412     1.0      2  -1.0
3   13600  202412     4.0      5  -1.0
4   13628  202412     1.0      2  -1.0
5   13788  202412     1.0      2  -1.0
6   13802  202412     2.0      3  -1.0
7   13878  202412     3.0      4  -1.0
8   13935  202412     3.0      4  -1.0
9   13956  202412     3.0      4  -1.0
```

**Largest Differences**:
```
   permno  yyyymm  python  stata  diff
0   10116  200809     5.0      1   4.0
1   10362  198709     1.0      5  -4.0
2   10693  198706     1.0      5  -4.0
3   10696  201909     1.0      5  -4.0
4   10739  198707     1.0      5  -4.0
5   10739  198708     1.0      5  -4.0
6   10812  198708     1.0      5  -4.0
7   10885  198909     1.0      5  -4.0
8   10987  199612     5.0      1   4.0
9   10987  199703     5.0      1   4.0
```

---

### RIO_Turnover

**Status**: ❌ FAILED

**Test Results**:
- Test 1 - Column names: ✅ PASSED
- Test 2 - Superset check: ❌ FAILED (Python missing 165651 Stata observations)
- Test 3 - Precision1 check: ❌ FAILED
- Test 4 - Precision2 check: ❌ FAILED

**Columns**: ['RIO_Turnover']

**Observations**:
- Stata:  445,546
- Python: 452,334
- Common: 279,895

**Precision1**: 57.480% obs with std_diff >= 1.00e-02 (tolerance: < 10%)

**Precision2**: 99th percentile diff = 1.49e+00 (tolerance: < 1.00e+00)

**Summary Statistics** (Common Observations):

| Statistic  |          Stata |         Python |     Difference | Std Difference |
|------------|----------------|----------------|----------------|----------------|
| count      |    279895.0000 |    279895.0000 |    279895.0000 |    279895.0000 |
| mean       |         3.2558 |         2.6428 |        -0.6130 |        -0.4553 |
| std        |         1.3463 |         1.1949 |         0.6828 |         0.5072 |
| min        |         1.0000 |         1.0000 |        -4.0000 |        -2.9710 |
| 25%        |         2.0000 |         2.0000 |        -1.0000 |        -0.7428 |
| 50%        |         3.0000 |         3.0000 |        -1.0000 |        -0.7428 |
| 75%        |         4.0000 |         3.0000 |         0.0000 |         0.0000 |
| max        |         5.0000 |         5.0000 |         4.0000 |         2.9710 |

**Regression Analysis** (Python ~ Stata):

- **Model**: python = 0.1514 + 0.7652 * stata
- **R-squared**: 0.7434
- **N observations**: 279,895

| Coefficient |     Estimate |    Std Error | t-statistic |   p-value |
|-------------|--------------|--------------|-------------|----------|
| Intercept   |       0.1514 |       0.0030 |     50.5763 |     0.000 |
| Slope       |       0.7652 |     8.50e-04 |    900.5713 |     0.000 |

**Missing Observations Sample**:
```
 index  permno  yyyymm  RIO_Turnover
     0   10003  198702             5
     1   10003  198704             5
     2   10003  198806             5
     3   10006  193112             3
     4   10006  193407             3
     5   10006  193602             3
     6   10006  193712             3
     7   10006  193807             3
     8   10006  193903             3
     9   10006  193908             3
```

**Feedback**:
- Num observations with std_diff >= TOL_DIFF_1: 160884/279895 (57.480%)
- Stata standard deviation: 1.35e+00

**Most Recent Bad Observations**:
```
   permno  yyyymm  python  stata  diff
0   12360  202412     4.0      5  -1.0
1   12788  202412     3.0      4  -1.0
2   13108  202412     3.0      4  -1.0
3   13628  202412     1.0      2  -1.0
4   13730  202412     2.0      3  -1.0
5   13954  202412     4.0      5  -1.0
6   14276  202412     3.0      4  -1.0
7   14328  202412     2.0      3  -1.0
8   14543  202412     3.0      4  -1.0
9   14773  202412     3.0      4  -1.0
```

**Largest Differences**:
```
   permno  yyyymm  python  stata  diff
0   10008  198609     1.0      5  -4.0
1   10008  198610     1.0      5  -4.0
2   10048  198610     1.0      5  -4.0
3   10066  199909     5.0      1   4.0
4   10157  198612     1.0      5  -4.0
5   10171  198612     1.0      5  -4.0
6   10202  198612     1.0      5  -4.0
7   10254  198703     1.0      5  -4.0
8   10263  198701     1.0      5  -4.0
9   10299  200712     1.0      5  -4.0
```

---

### RIO_Volatility

**Status**: ❌ FAILED

**Test Results**:
- Test 1 - Column names: ✅ PASSED
- Test 2 - Superset check: ❌ FAILED (Python missing 323960 Stata observations)
- Test 3 - Precision1 check: ❌ FAILED
- Test 4 - Precision2 check: ❌ FAILED

**Columns**: ['RIO_Volatility']

**Observations**:
- Stata:  470,062
- Python: 488,809
- Common: 146,102

**Precision1**: 61.952% obs with std_diff >= 1.00e-02 (tolerance: < 10%)

**Precision2**: 99th percentile diff = 1.51e+00 (tolerance: < 1.00e+00)

**Summary Statistics** (Common Observations):

| Statistic  |          Stata |         Python |     Difference | Std Difference |
|------------|----------------|----------------|----------------|----------------|
| count      |    146102.0000 |    146102.0000 |    146102.0000 |    146102.0000 |
| mean       |         3.4428 |         2.7747 |        -0.6680 |        -0.5029 |
| std        |         1.3284 |         1.1443 |         0.7267 |         0.5471 |
| min        |         1.0000 |         1.0000 |        -4.0000 |        -3.0111 |
| 25%        |         2.0000 |         2.0000 |        -1.0000 |        -0.7528 |
| 50%        |         4.0000 |         3.0000 |        -1.0000 |        -0.7528 |
| 75%        |         5.0000 |         4.0000 |         0.0000 |         0.0000 |
| max        |         5.0000 |         5.0000 |         4.0000 |         3.0111 |

**Regression Analysis** (Python ~ Stata):

- **Model**: python = 0.2911 + 0.7214 * stata
- **R-squared**: 0.7013
- **N observations**: 146,102

| Coefficient |     Estimate |    Std Error | t-statistic |   p-value |
|-------------|--------------|--------------|-------------|----------|
| Intercept   |       0.2911 |       0.0045 |     64.0561 |     0.000 |
| Slope       |       0.7214 |       0.0012 |    585.6882 |     0.000 |

**Missing Observations Sample**:
```
 index  permno  yyyymm  RIO_Volatility
     0   10002  200809               3
     1   10002  200810               3
     2   10002  200901               4
     3   10002  200902               4
     4   10002  200903               3
     5   10006  193208               4
     6   10006  193209               4
     7   10006  193302               3
     8   10006  193303               3
     9   10006  193405               3
```

**Feedback**:
- Num observations with std_diff >= TOL_DIFF_1: 90513/146102 (61.952%)
- Stata standard deviation: 1.33e+00

**Most Recent Bad Observations**:
```
   permno  yyyymm  python  stata  diff
0   10158  202412     4.0      5  -1.0
1   10966  202412     4.0      5  -1.0
2   12360  202412     4.0      5  -1.0
3   14823  202412     3.0      4  -1.0
4   15222  202412     2.0      3  -1.0
5   15533  202412     1.0      2  -1.0
6   16066  202412     2.0      3  -1.0
7   16086  202412     4.0      5  -1.0
8   16829  202412     3.0      4  -1.0
9   17038  202412     4.0      5  -1.0
```

**Largest Differences**:
```
   permno  yyyymm  python  stata  diff
0   10143  198704     1.0      5  -4.0
1   10263  198701     1.0      5  -4.0
2   10537  198703     1.0      5  -4.0
3   10537  198704     1.0      5  -4.0
4   10739  198707     1.0      5  -4.0
5   10739  198708     1.0      5  -4.0
6   10844  198707     1.0      5  -4.0
7   10871  198711     1.0      5  -4.0
8   10987  199612     5.0      1   4.0
9   11307  198801     1.0      5  -4.0
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

**Precision2**: 99th percentile diff = 3.28e-07 (tolerance: < 1.00e+00)

**Summary Statistics** (Common Observations):

| Statistic  |          Stata |         Python |     Difference | Std Difference |
|------------|----------------|----------------|----------------|----------------|
| count      |    745591.0000 |    745591.0000 |    745591.0000 |    745591.0000 |
| mean       |        -0.0296 |        -0.0296 |       2.18e-05 |       9.46e-05 |
| std        |         0.2302 |         0.2302 |         0.0043 |         0.0187 |
| min        |        -7.4048 |        -7.4048 |        -0.7381 |        -3.2056 |
| 25%        |        -0.1139 |        -0.1139 |      -8.68e-09 |      -3.77e-08 |
| 50%        |        -0.0453 |        -0.0453 |       2.73e-11 |       1.18e-10 |
| 75%        |         0.0295 |         0.0295 |       8.71e-09 |       3.78e-08 |
| max        |        23.6805 |        23.6805 |         0.8321 |         3.6138 |

**Regression Analysis** (Python ~ Stata):

- **Model**: python = 0.0000 + 0.9998 * stata
- **R-squared**: 0.9996
- **N observations**: 745,591

| Coefficient |     Estimate |    Std Error | t-statistic |   p-value |
|-------------|--------------|--------------|-------------|----------|
| Intercept   |     1.56e-05 |     5.03e-06 |      3.1026 |     0.002 |
| Slope       |       0.9998 |     2.17e-05 |  46137.7552 |     0.000 |

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
- Python: 4,980,936
- Common: 4,980,936

**Precision1**: 0.000% obs with std_diff >= 1.00e-02 (tolerance: < 10%)

**Precision2**: 99th percentile diff = 1.79e-15 (tolerance: < 1.00e+00)

**Summary Statistics** (Common Observations):

| Statistic  |          Stata |         Python |     Difference | Std Difference |
|------------|----------------|----------------|----------------|----------------|
| count      |       4.98e+06 |       4.98e+06 |       4.98e+06 |       4.98e+06 |
| mean       |         0.0297 |         0.0297 |       2.57e-20 |       8.27e-19 |
| std        |         0.0311 |         0.0311 |       2.95e-17 |       9.50e-16 |
| min        |         0.0000 |         0.0000 |      -6.66e-16 |      -2.14e-14 |
| 25%        |         0.0131 |         0.0131 |      -2.52e-17 |      -8.09e-16 |
| 50%        |         0.0219 |         0.0219 |         0.0000 |         0.0000 |
| 75%        |         0.0367 |         0.0367 |       2.60e-17 |       8.37e-16 |
| max        |         8.4777 |         8.4777 |       3.55e-15 |       1.14e-13 |

**Regression Analysis** (Python ~ Stata):

- **Model**: python = -0.0000 + 1.0000 * stata
- **R-squared**: 1.0000
- **N observations**: 4,980,936

| Coefficient |     Estimate |    Std Error | t-statistic |   p-value |
|-------------|--------------|--------------|-------------|----------|
| Intercept   |    -1.44e-15 |     9.16e-19 |  -1577.0941 |     0.000 |
| Slope       |       1.0000 |     2.13e-17 |    4.70e+16 |     0.000 |

**Feedback**:
- Num observations with std_diff >= TOL_DIFF_1: 0/4980936 (0.000%)
- Stata standard deviation: 3.11e-02

---

### Recomm_ShortInterest

**Status**: ❌ FAILED

**Test Results**:
- Test 1 - Column names: ✅ PASSED
- Test 2 - Superset check: ❌ FAILED (Python missing 19744 Stata observations)
- Test 3 - Precision1 check: ✅ PASSED
- Test 4 - Precision2 check: ✅ PASSED

**Columns**: ['Recomm_ShortInterest']

**Observations**:
- Stata:  34,619
- Python: 35,589
- Common: 14,875

**Precision1**: 0.000% obs with std_diff >= 1.00e-02 (tolerance: < 10%)

**Precision2**: 99th percentile diff = 0.00e+00 (tolerance: < 1.00e+00)

**Summary Statistics** (Common Observations):

| Statistic  |          Stata |         Python |     Difference | Std Difference |
|------------|----------------|----------------|----------------|----------------|
| count      |     14875.0000 |     14875.0000 |     14875.0000 |     14875.0000 |
| mean       |         0.6764 |         0.6764 |         0.0000 |         0.0000 |
| std        |         0.4679 |         0.4679 |         0.0000 |         0.0000 |
| min        |         0.0000 |         0.0000 |         0.0000 |         0.0000 |
| 25%        |         0.0000 |         0.0000 |         0.0000 |         0.0000 |
| 50%        |         1.0000 |         1.0000 |         0.0000 |         0.0000 |
| 75%        |         1.0000 |         1.0000 |         0.0000 |         0.0000 |
| max        |         1.0000 |         1.0000 |         0.0000 |         0.0000 |

**Regression Analysis** (Python ~ Stata):

- **Model**: python = 0.0000 + 1.0000 * stata
- **R-squared**: 1.0000
- **N observations**: 14,875

| Coefficient |     Estimate |    Std Error | t-statistic |   p-value |
|-------------|--------------|--------------|-------------|----------|
| Intercept   |     4.14e-15 |     3.69e-17 |    112.1720 |     0.000 |
| Slope       |       1.0000 |     4.49e-17 |    2.23e+16 |     0.000 |

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
- Num observations with std_diff >= TOL_DIFF_1: 0/14875 (0.000%)
- Stata standard deviation: 4.68e-01

---

### ResidualMomentum

**Status**: ✅ PASSED

**Test Results**:
- Test 1 - Column names: ✅ PASSED
- Test 2 - Superset check: ✅ PASSED
- Test 3 - Precision1 check: ✅ PASSED
- Test 4 - Precision2 check: ✅ PASSED

**Columns**: ['ResidualMomentum']

**Observations**:
- Stata:  3,458,422
- Python: 3,517,891
- Common: 3,458,422

**Precision1**: 2.854% obs with std_diff >= 1.00e-02 (tolerance: < 10%)

**Precision2**: 99th percentile diff = 1.14e-01 (tolerance: < 1.00e+00)

**Summary Statistics** (Common Observations):

| Statistic  |          Stata |         Python |     Difference | Std Difference |
|------------|----------------|----------------|----------------|----------------|
| count      |       3.46e+06 |       3.46e+06 |       3.46e+06 |       3.46e+06 |
| mean       |        -0.0384 |        -0.0387 |      -3.09e-04 |      -9.38e-04 |
| std        |         0.3299 |         0.3297 |         0.0196 |         0.0593 |
| min        |        -4.1338 |        -4.1338 |        -1.4918 |        -4.5214 |
| 25%        |        -0.2366 |        -0.2368 |      -1.08e-08 |      -3.27e-08 |
| 50%        |        -0.0220 |        -0.0222 |       6.05e-10 |       1.83e-09 |
| 75%        |         0.1765 |         0.1761 |       1.26e-08 |       3.83e-08 |
| max        |         2.8989 |         2.8989 |         1.8220 |         5.5221 |

**Regression Analysis** (Python ~ Stata):

- **Model**: python = -0.0004 + 0.9976 * stata
- **R-squared**: 0.9965
- **N observations**: 3,458,422

| Coefficient |     Estimate |    Std Error | t-statistic |   p-value |
|-------------|--------------|--------------|-------------|----------|
| Intercept   |    -4.01e-04 |     1.06e-05 |    -37.9242 |     0.000 |
| Slope       |       0.9976 |     3.19e-05 |  31320.8539 |     0.000 |

**Feedback**:
- Num observations with std_diff >= TOL_DIFF_1: 98694/3458422 (2.854%)
- Stata standard deviation: 3.30e-01

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

**Precision2**: 99th percentile diff = 1.81e-15 (tolerance: < 1.00e+00)

**Summary Statistics** (Common Observations):

| Statistic  |          Stata |         Python |     Difference | Std Difference |
|------------|----------------|----------------|----------------|----------------|
| count      |       4.95e+06 |       4.95e+06 |       4.95e+06 |       4.95e+06 |
| mean       |         0.1796 |         0.1796 |      -2.56e-19 |      -2.60e-19 |
| std        |         0.9830 |         0.9830 |       5.13e-16 |       5.21e-16 |
| min        |        -4.9029 |        -4.9029 |      -1.60e-14 |      -1.63e-14 |
| 25%        |        -0.2931 |        -0.2931 |      -1.39e-16 |      -1.41e-16 |
| 50%        |         0.1487 |         0.1487 |         0.0000 |         0.0000 |
| 75%        |         0.6344 |         0.6344 |       1.39e-16 |       1.41e-16 |
| max        |         4.9029 |         4.9029 |       1.60e-14 |       1.63e-14 |

**Regression Analysis** (Python ~ Stata):

- **Model**: python = -0.0000 + 1.0000 * stata
- **R-squared**: 1.0000
- **N observations**: 4,952,730

| Coefficient |     Estimate |    Std Error | t-statistic |   p-value |
|-------------|--------------|--------------|-------------|----------|
| Intercept   |    -1.30e-14 |     2.93e-17 |   -442.6160 |     0.000 |
| Slope       |       1.0000 |     2.93e-17 |    3.41e+16 |     0.000 |

**Feedback**:
- Num observations with std_diff >= TOL_DIFF_1: 0/4952730 (0.000%)
- Stata standard deviation: 9.83e-01

---

### ReturnSkew3F

**Status**: ✅ PASSED

**Test Results**:
- Test 1 - Column names: ✅ PASSED
- Test 2 - Superset check: ✅ PASSED
- Test 3 - Precision1 check: ✅ PASSED
- Test 4 - Precision2 check: ✅ PASSED

**Columns**: ['ReturnSkew3F']

**Observations**:
- Stata:  4,978,948
- Python: 4,980,936
- Common: 4,978,948

**Precision1**: 2.676% obs with std_diff >= 1.00e-02 (tolerance: < 10%)

**Precision2**: 99th percentile diff = 2.70e-02 (tolerance: < 1.00e+00)

**Summary Statistics** (Common Observations):

| Statistic  |          Stata |         Python |     Difference | Std Difference |
|------------|----------------|----------------|----------------|----------------|
| count      |       4.98e+06 |       4.98e+06 |       4.98e+06 |       4.98e+06 |
| mean       |         0.1540 |         0.1539 |      -1.18e-04 |      -1.39e-04 |
| std        |         0.8499 |         0.8379 |         0.1564 |         0.1840 |
| min        |        -4.8206 |        -3.9998 |        -5.9063 |        -6.9498 |
| 25%        |        -0.2811 |        -0.2797 |      -2.22e-15 |      -2.61e-15 |
| 50%        |         0.1296 |         0.1302 |         0.0000 |         0.0000 |
| 75%        |         0.5700 |         0.5689 |       2.22e-15 |       2.61e-15 |
| max        |         4.7150 |         3.9999 |         5.1167 |         6.0206 |

**Regression Analysis** (Python ~ Stata):

- **Model**: python = 0.0046 + 0.9691 * stata
- **R-squared**: 0.9661
- **N observations**: 4,978,948

| Coefficient |     Estimate |    Std Error | t-statistic |   p-value |
|-------------|--------------|--------------|-------------|----------|
| Intercept   |       0.0046 |     7.02e-05 |     66.0724 |     0.000 |
| Slope       |       0.9691 |     8.13e-05 |  11919.6235 |     0.000 |

**Feedback**:
- Num observations with std_diff >= TOL_DIFF_1: 133232/4978948 (2.676%)
- Stata standard deviation: 8.50e-01

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

**Precision2**: 99th percentile diff = 5.18e-08 (tolerance: < 1.00e+00)

**Summary Statistics** (Common Observations):

| Statistic  |          Stata |         Python |     Difference | Std Difference |
|------------|----------------|----------------|----------------|----------------|
| count      |       2.11e+06 |       2.11e+06 |       2.11e+06 |       2.11e+06 |
| mean       |         0.0943 |         0.0976 |         0.0033 |       2.85e-05 |
| std        |       116.2025 |       114.0863 |         2.4006 |         0.0207 |
| min        |    -86414.3670 |    -84415.3972 |       -25.5825 |        -0.2202 |
| 25%        |        -0.7785 |        -0.7785 |      -1.56e-07 |      -1.34e-09 |
| 50%        |         0.1277 |         0.1277 |         0.0000 |         0.0000 |
| 75%        |         0.8664 |         0.8663 |       1.56e-07 |       1.34e-09 |
| max        |     27665.5370 |     27665.5361 |      1998.9698 |        17.2025 |

**Regression Analysis** (Python ~ Stata):

- **Model**: python = 0.0050 + 0.9817 * stata
- **R-squared**: 0.9999
- **N observations**: 2,107,434

| Coefficient |     Estimate |    Std Error | t-statistic |   p-value |
|-------------|--------------|--------------|-------------|----------|
| Intercept   |       0.0050 |     7.73e-04 |      6.5117 |     0.000 |
| Slope       |       0.9817 |     6.66e-06 | 147489.3008 |     0.000 |

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

**Precision2**: 99th percentile diff = 2.57e-09 (tolerance: < 1.00e+00)

**Summary Statistics** (Common Observations):

| Statistic  |          Stata |         Python |     Difference | Std Difference |
|------------|----------------|----------------|----------------|----------------|
| count      |       3.53e+06 |       3.53e+06 |       3.53e+06 |       3.53e+06 |
| mean       |        -0.1424 |        -0.1424 |      -4.73e-07 |      -6.18e-09 |
| std        |        76.4924 |        76.4924 |       7.23e-04 |       9.45e-06 |
| min        |    -31837.0000 |    -31837.0000 |        -0.3429 |        -0.0045 |
| 25%        |        -0.0331 |        -0.0331 |      -2.80e-09 |      -3.66e-11 |
| 50%        |         0.0884 |         0.0884 |      -9.47e-13 |      -1.24e-14 |
| 75%        |         0.1559 |         0.1559 |       2.76e-09 |       3.61e-11 |
| max        |      7770.3335 |      7770.3333 |         0.1894 |         0.0025 |

**Regression Analysis** (Python ~ Stata):

- **Model**: python = -0.0000 + 1.0000 * stata
- **R-squared**: 1.0000
- **N observations**: 3,527,662

| Coefficient |     Estimate |    Std Error | t-statistic |   p-value |
|-------------|--------------|--------------|-------------|----------|
| Intercept   |    -4.73e-07 |     3.85e-07 |     -1.2289 |     0.219 |
| Slope       |       1.0000 |     5.03e-09 |    1.99e+08 |     0.000 |

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

**Precision2**: 99th percentile diff = 8.20e-08 (tolerance: < 1.00e+00)

**Summary Statistics** (Common Observations):

| Statistic  |          Stata |         Python |     Difference | Std Difference |
|------------|----------------|----------------|----------------|----------------|
| count      |       3.03e+06 |       3.03e+06 |       3.03e+06 |       3.03e+06 |
| mean       |         2.5432 |         2.5432 |       6.04e-08 |       6.99e-09 |
| std        |         8.6324 |         8.6324 |       1.96e-05 |       2.27e-06 |
| min        |       -61.8389 |       -61.8389 |        -0.0092 |        -0.0011 |
| 25%        |         0.3973 |         0.3973 |      -1.71e-08 |      -1.98e-09 |
| 50%        |         0.9928 |         0.9928 |         0.0000 |         0.0000 |
| 75%        |         2.4125 |         2.4125 |       1.70e-08 |       1.97e-09 |
| max        |      3668.3628 |      3668.3627 |         0.0050 |       5.80e-04 |

**Regression Analysis** (Python ~ Stata):

- **Model**: python = 0.0000 + 1.0000 * stata
- **R-squared**: 1.0000
- **N observations**: 3,030,926

| Coefficient |     Estimate |    Std Error | t-statistic |   p-value |
|-------------|--------------|--------------|-------------|----------|
| Intercept   |     6.94e-08 |     1.17e-08 |      5.9191 |     0.000 |
| Slope       |       1.0000 |     1.30e-09 |    7.67e+08 |     0.000 |

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

**Precision2**: 99th percentile diff = 5.39e-08 (tolerance: < 1.00e+00)

**Summary Statistics** (Common Observations):

| Statistic  |          Stata |         Python |     Difference | Std Difference |
|------------|----------------|----------------|----------------|----------------|
| count      |       4.05e+06 |       4.05e+06 |       4.05e+06 |       4.05e+06 |
| mean       |         0.0111 |         0.0111 |      -2.51e-12 |      -1.35e-11 |
| std        |         0.1856 |         0.1856 |       4.56e-09 |       2.46e-08 |
| min        |        -1.0000 |        -1.0000 |      -5.00e-07 |      -2.69e-06 |
| 25%        |        -0.0650 |        -0.0650 |      -1.11e-16 |      -5.98e-16 |
| 50%        |         0.0000 |         0.0000 |         0.0000 |         0.0000 |
| 75%        |         0.0690 |         0.0690 |       1.08e-16 |       5.79e-16 |
| max        |        39.0000 |        39.0000 |       5.00e-07 |       2.69e-06 |

**Regression Analysis** (Python ~ Stata):

- **Model**: python = -0.0000 + 1.0000 * stata
- **R-squared**: 1.0000
- **N observations**: 4,047,630

| Coefficient |     Estimate |    Std Error | t-statistic |   p-value |
|-------------|--------------|--------------|-------------|----------|
| Intercept   |    -1.22e-11 |     2.27e-12 |     -5.3703 |     0.000 |
| Slope       |       1.0000 |     1.22e-11 |    8.20e+10 |     0.000 |

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

**Precision2**: 99th percentile diff = 1.78e-10 (tolerance: < 1.00e+00)

**Summary Statistics** (Common Observations):

| Statistic  |          Stata |         Python |     Difference | Std Difference |
|------------|----------------|----------------|----------------|----------------|
| count      |       3.52e+06 |       3.52e+06 |       3.52e+06 |       3.52e+06 |
| mean       |         0.7841 |         0.7841 |      -3.05e-08 |      -5.13e-11 |
| std        |       593.7148 |       593.7147 |       3.01e-05 |       5.07e-08 |
| min        |        -0.9982 |        -0.9982 |        -0.0413 |      -6.95e-05 |
| 25%        |         0.0000 |         0.0000 |      -1.80e-08 |      -3.03e-11 |
| 50%        |         0.0024 |         0.0024 |         0.0000 |         0.0000 |
| 75%        |         0.0285 |         0.0285 |       1.81e-08 |       3.05e-11 |
| max        |    707720.6900 |    707720.6487 |       2.57e-04 |       4.32e-07 |

**Regression Analysis** (Python ~ Stata):

- **Model**: python = 0.0000 + 1.0000 * stata
- **R-squared**: 1.0000
- **N observations**: 3,517,326

| Coefficient |     Estimate |    Std Error | t-statistic |   p-value |
|-------------|--------------|--------------|-------------|----------|
| Intercept   |     8.19e-09 |     3.81e-09 |      2.1507 |     0.032 |
| Slope       |       1.0000 |     6.42e-12 |    1.56e+11 |     0.000 |

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

**Precision2**: 99th percentile diff = 4.73e-11 (tolerance: < 1.00e+00)

**Summary Statistics** (Common Observations):

| Statistic  |          Stata |         Python |     Difference | Std Difference |
|------------|----------------|----------------|----------------|----------------|
| count      |       2.51e+06 |       2.51e+06 |       2.51e+06 |       2.51e+06 |
| mean       |        19.3920 |        19.3920 |       1.92e-07 |       2.44e-11 |
| std        |      7858.8404 |      7858.8406 |       1.99e-04 |       2.53e-08 |
| min        |        -0.9913 |        -0.9913 |        -0.0359 |      -4.57e-06 |
| 25%        |      -1.32e-04 |      -1.32e-04 |      -2.67e-08 |      -3.40e-12 |
| 50%        |         0.0471 |         0.0471 |         0.0000 |         0.0000 |
| 75%        |         0.2961 |         0.2961 |       2.71e-08 |       3.45e-12 |
| max        |       6.54e+06 |       6.54e+06 |         0.2681 |       3.41e-05 |

**Regression Analysis** (Python ~ Stata):

- **Model**: python = -0.0000 + 1.0000 * stata
- **R-squared**: 1.0000
- **N observations**: 2,507,320

| Coefficient |     Estimate |    Std Error | t-statistic |   p-value |
|-------------|--------------|--------------|-------------|----------|
| Intercept   |    -1.55e-07 |     8.89e-08 |     -1.7387 |     0.082 |
| Slope       |       1.0000 |     1.13e-11 |    8.84e+10 |     0.000 |

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

**Precision2**: 99th percentile diff = 0.00e+00 (tolerance: < 1.00e+00)

**Summary Statistics** (Common Observations):

| Statistic  |          Stata |         Python |     Difference | Std Difference |
|------------|----------------|----------------|----------------|----------------|
| count      |       3.62e+06 |       3.62e+06 |       3.62e+06 |       3.62e+06 |
| mean       |         0.3376 |         0.3376 |       1.99e-05 |       4.20e-05 |
| std        |         0.4729 |         0.4729 |         0.0045 |         0.0094 |
| min        |         0.0000 |         0.0000 |         0.0000 |         0.0000 |
| 25%        |         0.0000 |         0.0000 |         0.0000 |         0.0000 |
| 50%        |         0.0000 |         0.0000 |         0.0000 |         0.0000 |
| 75%        |         1.0000 |         1.0000 |         0.0000 |         0.0000 |
| max        |         1.0000 |         1.0000 |         1.0000 |         2.1146 |

**Regression Analysis** (Python ~ Stata):

- **Model**: python = 0.0000 + 1.0000 * stata
- **R-squared**: 0.9999
- **N observations**: 3,624,363

| Coefficient |     Estimate |    Std Error | t-statistic |   p-value |
|-------------|--------------|--------------|-------------|----------|
| Intercept   |     3.00e-05 |     2.88e-06 |     10.4261 |     0.000 |
| Slope       |       1.0000 |     4.95e-06 | 201989.1013 |     0.000 |

**Feedback**:
- Num observations with std_diff >= TOL_DIFF_1: 72/3624363 (0.002%)
- Stata standard deviation: 4.73e-01

---

### ShareVol

**Status**: ✅ PASSED

**Test Results**:
- Test 1 - Column names: ✅ PASSED
- Test 2 - Superset check: ✅ PASSED
- Test 3 - Precision1 check: ✅ PASSED
- Test 4 - Precision2 check: ✅ PASSED

**Columns**: ['ShareVol']

**Observations**:
- Stata:  1,660,340
- Python: 1,661,295
- Common: 1,660,340

**Precision1**: 0.000% obs with std_diff >= 1.00e-02 (tolerance: < 10%)

**Precision2**: 99th percentile diff = 0.00e+00 (tolerance: < 1.00e+00)

**Summary Statistics** (Common Observations):

| Statistic  |          Stata |         Python |     Difference | Std Difference |
|------------|----------------|----------------|----------------|----------------|
| count      |       1.66e+06 |       1.66e+06 |       1.66e+06 |       1.66e+06 |
| mean       |         0.3061 |         0.3061 |         0.0000 |         0.0000 |
| std        |         0.4609 |         0.4609 |         0.0000 |         0.0000 |
| min        |         0.0000 |         0.0000 |         0.0000 |         0.0000 |
| 25%        |         0.0000 |         0.0000 |         0.0000 |         0.0000 |
| 50%        |         0.0000 |         0.0000 |         0.0000 |         0.0000 |
| 75%        |         1.0000 |         1.0000 |         0.0000 |         0.0000 |
| max        |         1.0000 |         1.0000 |         0.0000 |         0.0000 |

**Regression Analysis** (Python ~ Stata):

- **Model**: python = -0.0000 + 1.0000 * stata
- **R-squared**: 1.0000
- **N observations**: 1,660,340

| Coefficient |     Estimate |    Std Error | t-statistic |   p-value |
|-------------|--------------|--------------|-------------|----------|
| Intercept   |    -1.36e-12 |     1.89e-15 |   -717.5598 |     0.000 |
| Slope       |       1.0000 |     3.42e-15 |    2.92e+14 |     0.000 |

**Feedback**:
- Num observations with std_diff >= TOL_DIFF_1: 0/1660340 (0.000%)
- Stata standard deviation: 4.61e-01

---

### ShortInterest

**Status**: ✅ PASSED

**Test Results**:
- Test 1 - Column names: ✅ PASSED
- Test 2 - Superset check: ✅ PASSED
- Test 3 - Precision1 check: ✅ PASSED
- Test 4 - Precision2 check: ✅ PASSED

**Columns**: ['ShortInterest']

**Observations**:
- Stata:  873,175
- Python: 873,182
- Common: 873,175

**Precision1**: 0.000% obs with std_diff >= 1.00e-02 (tolerance: < 10%)

**Precision2**: 99th percentile diff = 5.09e-08 (tolerance: < 1.00e+00)

**Summary Statistics** (Common Observations):

| Statistic  |          Stata |         Python |     Difference | Std Difference |
|------------|----------------|----------------|----------------|----------------|
| count      |    873175.0000 |    873175.0000 |    873175.0000 |    873175.0000 |
| mean       |     36854.3903 |     36854.3903 |      -3.85e-05 |      -2.27e-10 |
| std        |    169080.3104 |    169080.3066 |         0.0053 |       3.14e-08 |
| min        |         0.0000 |         0.0000 |        -4.3468 |      -2.57e-05 |
| 25%        |      3359.3736 |      3359.3737 |      -2.49e-04 |      -1.47e-09 |
| 50%        |     15037.8830 |     15037.8829 |         0.0000 |         0.0000 |
| 75%        |     45982.9375 |     45982.9369 |       2.29e-04 |       1.36e-09 |
| max        |       1.34e+08 |       1.34e+08 |         0.9625 |       5.69e-06 |

**Regression Analysis** (Python ~ Stata):

- **Model**: python = 0.0008 + 1.0000 * stata
- **R-squared**: 1.0000
- **N observations**: 873,175

| Coefficient |     Estimate |    Std Error | t-statistic |   p-value |
|-------------|--------------|--------------|-------------|----------|
| Intercept   |     7.80e-04 |     4.11e-06 |    189.9077 |     0.000 |
| Slope       |       1.0000 |     2.37e-11 |    4.21e+10 |     0.000 |

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

**Precision2**: 99th percentile diff = 1.71e-07 (tolerance: < 1.00e+00)

**Summary Statistics** (Common Observations):

| Statistic  |          Stata |         Python |     Difference | Std Difference |
|------------|----------------|----------------|----------------|----------------|
| count      |       4.03e+06 |       4.03e+06 |       4.03e+06 |       4.03e+06 |
| mean       |         4.6018 |         4.6018 |       1.36e-11 |       5.81e-12 |
| std        |         2.3329 |         2.3329 |       1.00e-07 |       4.29e-08 |
| min        |        -5.9915 |        -5.9915 |      -5.00e-07 |      -2.14e-07 |
| 25%        |         2.8983 |         2.8983 |         0.0000 |         0.0000 |
| 50%        |         4.3953 |         4.3953 |         0.0000 |         0.0000 |
| 75%        |         6.1365 |         6.1365 |         0.0000 |         0.0000 |
| max        |        15.1466 |        15.1466 |       5.00e-07 |       2.14e-07 |

**Regression Analysis** (Python ~ Stata):

- **Model**: python = 0.0000 + 1.0000 * stata
- **R-squared**: 1.0000
- **N observations**: 4,029,130

| Coefficient |     Estimate |    Std Error | t-statistic |   p-value |
|-------------|--------------|--------------|-------------|----------|
| Intercept   |     4.68e-11 |     1.10e-10 |      0.4246 |     0.671 |
| Slope       |       1.0000 |     2.14e-11 |    4.68e+10 |     0.000 |

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

**Precision2**: 99th percentile diff = 4.20e-08 (tolerance: < 1.00e+00)

**Summary Statistics** (Common Observations):

| Statistic  |          Stata |         Python |     Difference | Std Difference |
|------------|----------------|----------------|----------------|----------------|
| count      |    856084.0000 |    856084.0000 |    856084.0000 |    856084.0000 |
| mean       |        -0.0373 |        -0.0373 |       9.46e-07 |       1.99e-06 |
| std        |         0.4759 |         0.4759 |         0.0048 |         0.0101 |
| min        |        -7.8254 |        -7.8254 |        -1.6594 |        -3.4867 |
| 25%        |        -0.0312 |        -0.0312 |         0.0000 |         0.0000 |
| 50%        |        -0.0066 |        -0.0066 |         0.0000 |         0.0000 |
| 75%        |         0.0022 |         0.0022 |         0.0000 |         0.0000 |
| max        |         7.7511 |         7.7511 |         2.5053 |         5.2642 |

**Regression Analysis** (Python ~ Stata):

- **Model**: python = -0.0000 + 1.0000 * stata
- **R-squared**: 0.9999
- **N observations**: 856,084

| Coefficient |     Estimate |    Std Error | t-statistic |   p-value |
|-------------|--------------|--------------|-------------|----------|
| Intercept   |    -6.84e-07 |     5.23e-06 |     -0.1309 |     0.896 |
| Slope       |       1.0000 |     1.10e-05 |  91309.3139 |     0.000 |

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

**Precision2**: 99th percentile diff = 0.00e+00 (tolerance: < 1.00e+00)

**Summary Statistics** (Common Observations):

| Statistic  |          Stata |         Python |     Difference | Std Difference |
|------------|----------------|----------------|----------------|----------------|
| count      |       4.05e+06 |       4.05e+06 |       4.05e+06 |       4.05e+06 |
| mean       |         0.0253 |         0.0253 |         0.0000 |         0.0000 |
| std        |         0.1571 |         0.1571 |         0.0000 |         0.0000 |
| min        |         0.0000 |         0.0000 |         0.0000 |         0.0000 |
| 25%        |         0.0000 |         0.0000 |         0.0000 |         0.0000 |
| 50%        |         0.0000 |         0.0000 |         0.0000 |         0.0000 |
| 75%        |         0.0000 |         0.0000 |         0.0000 |         0.0000 |
| max        |         1.0000 |         1.0000 |         0.0000 |         0.0000 |

**Regression Analysis** (Python ~ Stata):

- **Model**: python = 0.0000 + 1.0000 * stata
- **R-squared**: 1.0000
- **N observations**: 4,047,630

| Coefficient |     Estimate |    Std Error | t-statistic |   p-value |
|-------------|--------------|--------------|-------------|----------|
| Intercept   |     3.75e-13 |     1.18e-15 |    319.4918 |     0.000 |
| Slope       |       1.0000 |     7.38e-15 |    1.35e+14 |     0.000 |

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

**Precision2**: 99th percentile diff = 0.00e+00 (tolerance: < 1.00e+00)

**Summary Statistics** (Common Observations):

| Statistic  |          Stata |         Python |     Difference | Std Difference |
|------------|----------------|----------------|----------------|----------------|
| count      |       1.55e+06 |       1.55e+06 |       1.55e+06 |       1.55e+06 |
| mean       |         0.2861 |         0.2860 |      -3.88e-05 |      -8.59e-05 |
| std        |         0.4519 |         0.4519 |         0.0074 |         0.0163 |
| min        |         0.0000 |         0.0000 |        -1.0000 |        -2.2127 |
| 25%        |         0.0000 |         0.0000 |         0.0000 |         0.0000 |
| 50%        |         0.0000 |         0.0000 |         0.0000 |         0.0000 |
| 75%        |         1.0000 |         1.0000 |         0.0000 |         0.0000 |
| max        |         1.0000 |         1.0000 |         1.0000 |         2.2127 |

**Regression Analysis** (Python ~ Stata):

- **Model**: python = 0.0000 + 0.9998 * stata
- **R-squared**: 0.9997
- **N observations**: 1,545,193

| Coefficient |     Estimate |    Std Error | t-statistic |   p-value |
|-------------|--------------|--------------|-------------|----------|
| Intercept   |     1.09e-05 |     7.02e-06 |      1.5497 |     0.121 |
| Slope       |       0.9998 |     1.31e-05 |  76184.5432 |     0.000 |

**Feedback**:
- Num observations with std_diff >= TOL_DIFF_1: 84/1545193 (0.005%)
- Stata standard deviation: 4.52e-01

---

### Tax

**Status**: ✅ PASSED

**Test Results**:
- Test 1 - Column names: ✅ PASSED
- Test 2 - Superset check: ✅ PASSED
- Test 3 - Precision1 check: ✅ PASSED
- Test 4 - Precision2 check: ✅ PASSED

**Columns**: ['Tax']

**Observations**:
- Stata:  3,211,651
- Python: 3,213,292
- Common: 3,211,651

**Precision1**: 1.244% obs with std_diff >= 1.00e-02 (tolerance: < 10%)

**Precision2**: 99th percentile diff = 3.22e-02 (tolerance: < 1.00e+00)

**Summary Statistics** (Common Observations):

| Statistic  |          Stata |         Python |     Difference | Std Difference |
|------------|----------------|----------------|----------------|----------------|
| count      |       3.21e+06 |       3.21e+06 |       3.21e+06 |       3.21e+06 |
| mean       |         1.1689 |         1.1833 |         0.0144 |       7.57e-04 |
| std        |        19.0252 |        19.4556 |         4.0707 |         0.2140 |
| min        |     -2742.5000 |     -2742.5000 |        -1.0000 |        -0.0526 |
| 25%        |         0.0341 |         0.0265 |      -1.74e-08 |      -9.15e-10 |
| 50%        |         1.0000 |         1.0000 |         0.0000 |         0.0000 |
| 75%        |         1.4267 |         1.4359 |       1.28e-10 |       6.75e-12 |
| max        |      4463.7114 |      4463.7113 |      2022.5294 |       106.3082 |

**Regression Analysis** (Python ~ Stata):

- **Model**: python = 0.0144 + 1.0000 * stata
- **R-squared**: 0.9562
- **N observations**: 3,211,651

| Coefficient |     Estimate |    Std Error | t-statistic |   p-value |
|-------------|--------------|--------------|-------------|----------|
| Intercept   |       0.0144 |       0.0023 |      6.3339 |     0.000 |
| Slope       |       1.0000 |     1.19e-04 |   8375.7860 |     0.000 |

**Feedback**:
- Num observations with std_diff >= TOL_DIFF_1: 39943/3211651 (1.244%)
- Stata standard deviation: 1.90e+01

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

**Precision2**: 99th percentile diff = 8.22e-08 (tolerance: < 1.00e+00)

**Summary Statistics** (Common Observations):

| Statistic  |          Stata |         Python |     Difference | Std Difference |
|------------|----------------|----------------|----------------|----------------|
| count      |       3.14e+06 |       3.14e+06 |       3.14e+06 |       3.14e+06 |
| mean       |       9.92e-04 |       9.92e-04 |      -1.82e-07 |      -2.32e-07 |
| std        |         0.7815 |         0.7815 |       1.98e-04 |       2.53e-04 |
| min        |      -161.4356 |      -161.4356 |        -0.0902 |        -0.1155 |
| 25%        |        -0.0461 |        -0.0461 |      -2.74e-09 |      -3.51e-09 |
| 50%        |         0.0111 |         0.0111 |      -2.39e-12 |      -3.06e-12 |
| 75%        |         0.0655 |         0.0655 |       2.70e-09 |       3.46e-09 |
| max        |       190.7895 |       190.7895 |         0.0455 |         0.0582 |

**Regression Analysis** (Python ~ Stata):

- **Model**: python = -0.0000 + 1.0000 * stata
- **R-squared**: 1.0000
- **N observations**: 3,141,468

| Coefficient |     Estimate |    Std Error | t-statistic |   p-value |
|-------------|--------------|--------------|-------------|----------|
| Intercept   |    -1.82e-07 |     1.11e-07 |     -1.6300 |     0.103 |
| Slope       |       1.0000 |     1.43e-07 |    7.01e+06 |     0.000 |

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
- Python: 2,056,304
- Common: 2,055,856

**Precision1**: 97.137% obs with std_diff >= 1.00e-02 (tolerance: < 10%)

**Precision2**: 99th percentile diff = 1.69e+00 (tolerance: < 1.00e+00)

**Summary Statistics** (Common Observations):

| Statistic  |          Stata |         Python |     Difference | Std Difference |
|------------|----------------|----------------|----------------|----------------|
| count      |       2.06e+06 |       2.06e+06 |       2.06e+06 |       2.06e+06 |
| mean       |         0.2096 |         0.1784 |        -0.0312 |        -0.2029 |
| std        |         0.1540 |         0.1465 |         0.0635 |         0.4122 |
| min        |        -1.0711 |        -1.0712 |        -0.7739 |        -5.0250 |
| 25%        |         0.1242 |         0.1041 |        -0.0599 |        -0.3890 |
| 50%        |         0.2187 |         0.1842 |        -0.0240 |        -0.1558 |
| 75%        |         0.3000 |         0.2615 |         0.0043 |         0.0276 |
| max        |         3.2757 |         3.2813 |         2.7034 |        17.5546 |

**Regression Analysis** (Python ~ Stata):

- **Model**: python = -0.0035 + 0.8675 * stata
- **R-squared**: 0.8316
- **N observations**: 2,055,856

| Coefficient |     Estimate |    Std Error | t-statistic |   p-value |
|-------------|--------------|--------------|-------------|----------|
| Intercept   |      -0.0035 |     7.08e-05 |    -48.9602 |     0.000 |
| Slope       |       0.8675 |     2.72e-04 |   3186.6579 |     0.000 |

**Feedback**:
- Num observations with std_diff >= TOL_DIFF_1: 1997005/2055856 (97.137%)
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

**Precision2**: 99th percentile diff = 0.00e+00 (tolerance: < 1.00e+00)

**Summary Statistics** (Common Observations):

| Statistic  |          Stata |         Python |     Difference | Std Difference |
|------------|----------------|----------------|----------------|----------------|
| count      |    449191.0000 |    449191.0000 |    449191.0000 |    449191.0000 |
| mean       |         0.3622 |         0.3622 |       2.23e-06 |       4.63e-06 |
| std        |         0.4806 |         0.4806 |         0.0153 |         0.0318 |
| min        |         0.0000 |         0.0000 |        -1.0000 |        -2.0806 |
| 25%        |         0.0000 |         0.0000 |         0.0000 |         0.0000 |
| 50%        |         0.0000 |         0.0000 |         0.0000 |         0.0000 |
| 75%        |         1.0000 |         1.0000 |         0.0000 |         0.0000 |
| max        |         1.0000 |         1.0000 |         1.0000 |         2.0806 |

**Regression Analysis** (Python ~ Stata):

- **Model**: python = 0.0002 + 0.9995 * stata
- **R-squared**: 0.9990
- **N observations**: 449,191

| Coefficient |     Estimate |    Std Error | t-statistic |   p-value |
|-------------|--------------|--------------|-------------|----------|
| Intercept   |     1.85e-04 |     2.86e-05 |      6.4772 |     0.000 |
| Slope       |       0.9995 |     4.75e-05 |  21061.2947 |     0.000 |

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

**Precision2**: 99th percentile diff = 4.68e-10 (tolerance: < 1.00e+00)

**Summary Statistics** (Common Observations):

| Statistic  |          Stata |         Python |     Difference | Std Difference |
|------------|----------------|----------------|----------------|----------------|
| count      |       2.55e+06 |       2.55e+06 |       2.55e+06 |       2.55e+06 |
| mean       |         1.3777 |         1.3777 |      -3.72e-08 |      -1.70e-10 |
| std        |       219.5846 |       219.5846 |       3.07e-05 |       1.40e-07 |
| min        |         0.0000 |         0.0000 |        -0.0179 |      -8.13e-05 |
| 25%        |       6.28e-04 |       6.28e-04 |      -6.13e-11 |      -2.79e-13 |
| 50%        |         0.0026 |         0.0026 |       4.84e-14 |       2.20e-16 |
| 75%        |         0.0139 |         0.0139 |       6.25e-11 |       2.84e-13 |
| max        |    106471.4300 |    106471.4184 |         0.0062 |       2.83e-05 |

**Regression Analysis** (Python ~ Stata):

- **Model**: python = 0.0000 + 1.0000 * stata
- **R-squared**: 1.0000
- **N observations**: 2,547,003

| Coefficient |     Estimate |    Std Error | t-statistic |   p-value |
|-------------|--------------|--------------|-------------|----------|
| Intercept   |     8.54e-08 |     1.48e-08 |      5.7660 |     0.000 |
| Slope       |       1.0000 |     6.74e-11 |    1.48e+10 |     0.000 |

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

**Precision2**: 99th percentile diff = 3.64e-08 (tolerance: < 1.00e+00)

**Summary Statistics** (Common Observations):

| Statistic  |          Stata |         Python |     Difference | Std Difference |
|------------|----------------|----------------|----------------|----------------|
| count      |       4.36e+06 |       4.36e+06 |       4.36e+06 |       4.36e+06 |
| mean       |         0.1938 |         0.1938 |       6.37e-06 |       2.97e-06 |
| std        |         2.1410 |         2.1410 |         0.0054 |         0.0025 |
| min        |         0.0000 |      -1.56e-17 |        -3.7592 |        -1.7558 |
| 25%        |         0.0234 |         0.0234 |      -1.35e-09 |      -6.33e-10 |
| 50%        |         0.0593 |         0.0593 |      -6.41e-13 |      -3.00e-13 |
| 75%        |         0.1414 |         0.1415 |       1.36e-09 |       6.34e-10 |
| max        |      1330.3551 |      1330.3551 |         5.2599 |         2.4568 |

**Regression Analysis** (Python ~ Stata):

- **Model**: python = 0.0000 + 1.0000 * stata
- **R-squared**: 1.0000
- **N observations**: 4,358,313

| Coefficient |     Estimate |    Std Error | t-statistic |   p-value |
|-------------|--------------|--------------|-------------|----------|
| Intercept   |     7.29e-06 |     2.58e-06 |      2.8284 |     0.005 |
| Slope       |       1.0000 |     1.20e-06 | 834545.5875 |     0.000 |

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

**Precision2**: 99th percentile diff = 8.59e-15 (tolerance: < 1.00e+00)

**Summary Statistics** (Common Observations):

| Statistic  |          Stata |         Python |     Difference | Std Difference |
|------------|----------------|----------------|----------------|----------------|
| count      |       3.92e+06 |       3.92e+06 |       3.92e+06 |       3.92e+06 |
| mean       |         5.3349 |         5.3351 |       2.56e-04 |       6.62e-06 |
| std        |        38.6789 |        38.6790 |         0.0517 |         0.0013 |
| min        |         0.0000 |       4.33e-10 |        -4.1070 |        -0.1062 |
| 25%        |         0.0640 |         0.0640 |      -1.11e-16 |      -2.87e-18 |
| 50%        |         0.3696 |         0.3697 |         0.0000 |         0.0000 |
| 75%        |         2.1897 |         2.1900 |       1.25e-16 |       3.23e-18 |
| max        |      6121.4561 |      6121.4561 |        30.1748 |         0.7801 |

**Regression Analysis** (Python ~ Stata):

- **Model**: python = 0.0003 + 1.0000 * stata
- **R-squared**: 1.0000
- **N observations**: 3,921,598

| Coefficient |     Estimate |    Std Error | t-statistic |   p-value |
|-------------|--------------|--------------|-------------|----------|
| Intercept   |     2.53e-04 |     2.63e-05 |      9.6092 |     0.000 |
| Slope       |       1.0000 |     6.75e-07 |    1.48e+06 |     0.000 |

**Feedback**:
- Num observations with std_diff >= TOL_DIFF_1: 396/3921598 (0.010%)
- Stata standard deviation: 3.87e+01

---

### VolumeTrend

**Status**: ✅ PASSED

**Test Results**:
- Test 1 - Column names: ✅ PASSED
- Test 2 - Superset check: ✅ PASSED
- Test 3 - Precision1 check: ✅ PASSED
- Test 4 - Precision2 check: ✅ PASSED

**Columns**: ['VolumeTrend']

**Observations**:
- Stata:  3,655,889
- Python: 5,153,763
- Common: 3,655,889

**Precision1**: 1.357% obs with std_diff >= 1.00e-02 (tolerance: < 10%)

**Precision2**: 99th percentile diff = 9.34e-02 (tolerance: < 1.00e+00)

**Summary Statistics** (Common Observations):

| Statistic  |          Stata |         Python |     Difference | Std Difference |
|------------|----------------|----------------|----------------|----------------|
| count      |       3.66e+06 |       3.66e+06 |       3.66e+06 |       3.66e+06 |
| mean       |         0.0057 |         0.0057 |       5.70e-05 |         0.0028 |
| std        |         0.0207 |         0.0208 |         0.0022 |         0.1068 |
| min        |        -0.0566 |        -0.0517 |        -0.0631 |        -3.0497 |
| 25%        |        -0.0068 |        -0.0069 |      -2.22e-10 |      -1.07e-08 |
| 50%        |         0.0052 |         0.0052 |       6.53e-13 |       3.16e-11 |
| 75%        |         0.0184 |         0.0186 |       2.32e-10 |       1.12e-08 |
| max        |         0.0664 |         0.1665 |         0.1636 |         7.9103 |

**Regression Analysis** (Python ~ Stata):

- **Model**: python = 0.0001 + 0.9983 * stata
- **R-squared**: 0.9887
- **N observations**: 3,655,889

| Coefficient |     Estimate |    Std Error | t-statistic |   p-value |
|-------------|--------------|--------------|-------------|----------|
| Intercept   |     6.67e-05 |     1.20e-06 |     55.6825 |     0.000 |
| Slope       |       0.9983 |     5.59e-05 |  17866.8269 |     0.000 |

**Feedback**:
- Num observations with std_diff >= TOL_DIFF_1: 49596/3655889 (1.357%)
- Stata standard deviation: 2.07e-02

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

**Precision2**: 99th percentile diff = 5.33e-08 (tolerance: < 1.00e+00)

**Summary Statistics** (Common Observations):

| Statistic  |          Stata |         Python |     Difference | Std Difference |
|------------|----------------|----------------|----------------|----------------|
| count      |       3.02e+06 |       3.02e+06 |       3.02e+06 |       3.02e+06 |
| mean       |         0.0642 |         0.0642 |       2.02e-07 |       3.27e-07 |
| std        |         0.6161 |         0.6161 |       2.31e-04 |       3.75e-04 |
| min        |      -165.5014 |      -165.5014 |        -0.0876 |        -0.1423 |
| 25%        |        -0.0373 |        -0.0373 |      -8.91e-10 |      -1.45e-09 |
| 50%        |         0.0000 |         0.0000 |         0.0000 |         0.0000 |
| 75%        |         0.0785 |         0.0785 |       8.91e-10 |       1.45e-09 |
| max        |        64.3333 |        64.3333 |         0.0513 |         0.0833 |

**Regression Analysis** (Python ~ Stata):

- **Model**: python = 0.0000 + 1.0000 * stata
- **R-squared**: 1.0000
- **N observations**: 3,022,290

| Coefficient |     Estimate |    Std Error | t-statistic |   p-value |
|-------------|--------------|--------------|-------------|----------|
| Intercept   |     2.81e-07 |     1.34e-07 |      2.1052 |     0.035 |
| Slope       |       1.0000 |     2.16e-07 |    4.63e+06 |     0.000 |

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

**Precision2**: 99th percentile diff = 1.35e-03 (tolerance: < 1.00e+00)

**Summary Statistics** (Common Observations):

| Statistic  |          Stata |         Python |     Difference | Std Difference |
|------------|----------------|----------------|----------------|----------------|
| count      |       3.51e+06 |       3.51e+06 |       3.51e+06 |       3.51e+06 |
| mean       |       3.88e-04 |       3.88e-04 |       9.63e-08 |       5.60e-06 |
| std        |         0.0172 |         0.0172 |       9.88e-06 |       5.74e-04 |
| min        |        -1.5701 |        -1.5701 |        -0.0026 |        -0.1486 |
| 25%        |        -0.0039 |        -0.0039 |      -2.25e-16 |      -1.30e-14 |
| 50%        |       8.83e-05 |       8.84e-05 |       8.57e-18 |       4.98e-16 |
| 75%        |         0.0046 |         0.0046 |       3.64e-16 |       2.12e-14 |
| max        |         1.9930 |         1.9930 |         0.0031 |         0.1824 |

**Regression Analysis** (Python ~ Stata):

- **Model**: python = 0.0000 + 1.0000 * stata
- **R-squared**: 1.0000
- **N observations**: 3,510,758

| Coefficient |     Estimate |    Std Error | t-statistic |   p-value |
|-------------|--------------|--------------|-------------|----------|
| Intercept   |     9.60e-08 |     5.28e-09 |     18.1935 |     0.000 |
| Slope       |       1.0000 |     3.06e-07 |    3.26e+06 |     0.000 |

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

**Precision2**: 99th percentile diff = 4.15e-08 (tolerance: < 1.00e+00)

**Summary Statistics** (Common Observations):

| Statistic  |          Stata |         Python |     Difference | Std Difference |
|------------|----------------|----------------|----------------|----------------|
| count      |       2.61e+06 |       2.61e+06 |       2.61e+06 |       2.61e+06 |
| mean       |        -0.0066 |        -0.0066 |      -3.31e-07 |      -1.74e-07 |
| std        |         1.8996 |         1.8996 |       2.16e-04 |       1.14e-04 |
| min        |     -1800.0656 |     -1800.0656 |        -0.1876 |        -0.0988 |
| 25%        |        -0.0438 |        -0.0438 |      -1.93e-09 |      -1.02e-09 |
| 50%        |         0.0402 |         0.0402 |       3.71e-13 |       1.95e-13 |
| 75%        |         0.1136 |         0.1136 |       1.94e-09 |       1.02e-09 |
| max        |       574.5096 |       574.5097 |       2.59e-05 |       1.36e-05 |

**Regression Analysis** (Python ~ Stata):

- **Model**: python = -0.0000 + 1.0000 * stata
- **R-squared**: 1.0000
- **N observations**: 2,613,997

| Coefficient |     Estimate |    Std Error | t-statistic |   p-value |
|-------------|--------------|--------------|-------------|----------|
| Intercept   |    -3.31e-07 |     1.34e-07 |     -2.4741 |     0.013 |
| Slope       |       1.0000 |     7.04e-08 |    1.42e+07 |     0.000 |

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

**Precision2**: 99th percentile diff = 5.17e-08 (tolerance: < 1.00e+00)

**Summary Statistics** (Common Observations):

| Statistic  |          Stata |         Python |     Difference | Std Difference |
|------------|----------------|----------------|----------------|----------------|
| count      |    845632.0000 |    845632.0000 |    845632.0000 |    845632.0000 |
| mean       |      -8.19e-04 |      -8.17e-04 |       1.81e-06 |       3.11e-06 |
| std        |         0.5805 |         0.5805 |         0.0038 |         0.0066 |
| min        |       -12.5800 |       -12.5800 |        -1.4963 |        -2.5775 |
| 25%        |        -0.0233 |        -0.0233 |         0.0000 |         0.0000 |
| 50%        |      -1.50e-05 |      -1.60e-05 |         0.0000 |         0.0000 |
| 75%        |         0.0230 |         0.0230 |         0.0000 |         0.0000 |
| max        |        12.5655 |        12.5655 |         1.5039 |         2.5907 |

**Regression Analysis** (Python ~ Stata):

- **Model**: python = 0.0000 + 1.0000 * stata
- **R-squared**: 1.0000
- **N observations**: 845,632

| Coefficient |     Estimate |    Std Error | t-statistic |   p-value |
|-------------|--------------|--------------|-------------|----------|
| Intercept   |     1.79e-06 |     4.16e-06 |      0.4307 |     0.667 |
| Slope       |       1.0000 |     7.17e-06 | 139490.0986 |     0.000 |

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

**Precision2**: 99th percentile diff = 9.09e-08 (tolerance: < 1.00e+00)

**Summary Statistics** (Common Observations):

| Statistic  |          Stata |         Python |     Difference | Std Difference |
|------------|----------------|----------------|----------------|----------------|
| count      |       3.19e+06 |       3.19e+06 |       3.19e+06 |       3.19e+06 |
| mean       |         0.0925 |         0.0925 |       3.72e-06 |       2.49e-06 |
| std        |         1.4933 |         1.4933 |         0.0014 |       9.31e-04 |
| min        |      -361.9091 |      -361.9091 |        -0.1253 |        -0.0839 |
| 25%        |        -0.0325 |        -0.0325 |      -2.71e-08 |      -1.82e-08 |
| 50%        |         0.0308 |         0.0308 |      -8.04e-13 |      -5.39e-13 |
| 75%        |         0.1209 |         0.1209 |       2.71e-08 |       1.82e-08 |
| max        |       457.1988 |       457.1988 |         0.6600 |         0.4419 |

**Regression Analysis** (Python ~ Stata):

- **Model**: python = 0.0000 + 1.0000 * stata
- **R-squared**: 1.0000
- **N observations**: 3,194,445

| Coefficient |     Estimate |    Std Error | t-statistic |   p-value |
|-------------|--------------|--------------|-------------|----------|
| Intercept   |     4.27e-06 |     7.79e-07 |      5.4809 |     0.000 |
| Slope       |       1.0000 |     5.21e-07 |    1.92e+06 |     0.000 |

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

**Precision2**: 99th percentile diff = 5.68e-08 (tolerance: < 1.00e+00)

**Summary Statistics** (Common Observations):

| Statistic  |          Stata |         Python |     Difference | Std Difference |
|------------|----------------|----------------|----------------|----------------|
| count      |    845632.0000 |    845632.0000 |    845632.0000 |    845632.0000 |
| mean       |         0.0164 |         0.0164 |      -1.35e-06 |      -2.55e-06 |
| std        |         0.5281 |         0.5281 |         0.0031 |         0.0059 |
| min        |        -7.9158 |        -7.9158 |        -0.7149 |        -1.3536 |
| 25%        |        -0.0575 |        -0.0575 |         0.0000 |         0.0000 |
| 50%        |      -9.05e-04 |      -9.04e-04 |         0.0000 |         0.0000 |
| 75%        |         0.0573 |         0.0573 |         0.0000 |         0.0000 |
| max        |         8.2983 |         8.2983 |         0.9739 |         1.8440 |

**Regression Analysis** (Python ~ Stata):

- **Model**: python = -0.0000 + 1.0000 * stata
- **R-squared**: 1.0000
- **N observations**: 845,632

| Coefficient |     Estimate |    Std Error | t-statistic |   p-value |
|-------------|--------------|--------------|-------------|----------|
| Intercept   |    -8.99e-07 |     3.39e-06 |     -0.2651 |     0.791 |
| Slope       |       1.0000 |     6.42e-06 | 155699.0941 |     0.000 |

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

**Precision2**: 99th percentile diff = 5.63e-08 (tolerance: < 1.00e+00)

**Summary Statistics** (Common Observations):

| Statistic  |          Stata |         Python |     Difference | Std Difference |
|------------|----------------|----------------|----------------|----------------|
| count      |    845632.0000 |    845632.0000 |    845632.0000 |    845632.0000 |
| mean       |         0.0155 |         0.0155 |       4.58e-07 |       8.60e-07 |
| std        |         0.5329 |         0.5329 |         0.0035 |         0.0066 |
| min        |        -8.1177 |        -8.1177 |        -1.5759 |        -2.9573 |
| 25%        |        -0.0547 |        -0.0547 |         0.0000 |         0.0000 |
| 50%        |        -0.0011 |        -0.0011 |         0.0000 |         0.0000 |
| 75%        |         0.0539 |         0.0539 |         0.0000 |         0.0000 |
| max        |         8.1240 |         8.1240 |         1.5933 |         2.9900 |

**Regression Analysis** (Python ~ Stata):

- **Model**: python = 0.0000 + 1.0000 * stata
- **R-squared**: 1.0000
- **N observations**: 845,632

| Coefficient |     Estimate |    Std Error | t-statistic |   p-value |
|-------------|--------------|--------------|-------------|----------|
| Intercept   |     6.57e-07 |     3.83e-06 |      0.1713 |     0.864 |
| Slope       |       1.0000 |     7.19e-06 | 139011.9529 |     0.000 |

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

**Precision2**: 99th percentile diff = 1.61e-07 (tolerance: < 1.00e+00)

**Summary Statistics** (Common Observations):

| Statistic  |          Stata |         Python |     Difference | Std Difference |
|------------|----------------|----------------|----------------|----------------|
| count      |    873864.0000 |    873864.0000 |    873864.0000 |    873864.0000 |
| mean       |        16.7174 |        16.7174 |      -3.97e-06 |      -3.20e-07 |
| std        |        12.4128 |        12.4123 |         0.2384 |         0.0192 |
| min        |      -259.1000 |      -259.1000 |       -31.0000 |        -2.4974 |
| 25%        |        10.6000 |        10.6000 |         0.0000 |         0.0000 |
| 50%        |        15.0000 |        15.0000 |         0.0000 |         0.0000 |
| 75%        |        20.0000 |        20.0000 |         0.0000 |         0.0000 |
| max        |       473.9000 |       473.9000 |        45.0000 |         3.6253 |

**Regression Analysis** (Python ~ Stata):

- **Model**: python = 0.0037 + 0.9998 * stata
- **R-squared**: 0.9996
- **N observations**: 873,864

| Coefficient |     Estimate |    Std Error | t-statistic |   p-value |
|-------------|--------------|--------------|-------------|----------|
| Intercept   |       0.0037 |     4.28e-04 |      8.7331 |     0.000 |
| Slope       |       0.9998 |     2.05e-05 |  48669.1061 |     0.000 |

**Feedback**:
- Num observations with std_diff >= TOL_DIFF_1: 600/873864 (0.069%)
- Stata standard deviation: 1.24e+01

---

### grcapx

**Status**: ✅ PASSED

**Test Results**:
- Test 1 - Column names: ✅ PASSED
- Test 2 - Superset check: ✅ PASSED
- Test 3 - Precision1 check: ✅ PASSED
- Test 4 - Precision2 check: ✅ PASSED

**Columns**: ['grcapx']

**Observations**:
- Stata:  2,425,711
- Python: 2,444,969
- Common: 2,407,863

**Precision1**: 0.045% obs with std_diff >= 1.00e-02 (tolerance: < 10%)

**Precision2**: 99th percentile diff = 1.83e-09 (tolerance: < 1.00e+00)

**Summary Statistics** (Common Observations):

| Statistic  |          Stata |         Python |     Difference | Std Difference |
|------------|----------------|----------------|----------------|----------------|
| count      |       2.41e+06 |       2.41e+06 |       2.41e+06 |       2.41e+06 |
| mean       |         3.7307 |            inf |            inf |            inf |
| std        |       394.4875 |            N/A |            N/A |            N/A |
| min        |     -9061.0000 |     -9061.0000 |    -91202.9468 |      -231.1935 |
| 25%        |        -0.3587 |        -0.3588 |      -9.08e-09 |      -2.30e-11 |
| 50%        |         0.1307 |         0.1308 |         0.0000 |         0.0000 |
| 75%        |         0.8916 |         0.8919 |       9.27e-09 |       2.35e-11 |
| max        |    141782.2000 |            inf |            inf |            inf |

**Regression Analysis** (Python ~ Stata):

- **Model**: python = inf + nan * stata
- **R-squared**: nan
- **N observations**: 2,407,863

| Coefficient |     Estimate |    Std Error | t-statistic |   p-value |
|-------------|--------------|--------------|-------------|----------|
| Intercept   |          nan |          nan |         nan |       nan |
| Slope       |          nan |          nan |         nan |       nan |

**Feedback**:
- Num observations with std_diff >= TOL_DIFF_1: 1081/2407863 (0.045%)
- Stata standard deviation: 3.94e+02

---

### grcapx3y

**Status**: ✅ PASSED

**Test Results**:
- Test 1 - Column names: ✅ PASSED
- Test 2 - Superset check: ✅ PASSED
- Test 3 - Precision1 check: ✅ PASSED
- Test 4 - Precision2 check: ✅ PASSED

**Columns**: ['grcapx3y']

**Observations**:
- Stata:  2,214,095
- Python: 2,236,619
- Common: 2,197,381

**Precision1**: 0.000% obs with std_diff >= 1.00e-02 (tolerance: < 10%)

**Precision2**: 99th percentile diff = 5.81e-21 (tolerance: < 1.00e+00)

**Summary Statistics** (Common Observations):

| Statistic  |          Stata |         Python |     Difference | Std Difference |
|------------|----------------|----------------|----------------|----------------|
| count      |       2.20e+06 |       2.20e+06 |       2.20e+06 |       2.20e+06 |
| mean       |      -4.24e+10 |            N/A |            N/A |            N/A |
| std        |       4.50e+13 |            N/A |            N/A |            N/A |
| min        |      -2.57e+16 |           -inf |           -inf |           -inf |
| 25%        |         0.6523 |         0.6522 |      -1.95e-08 |      -4.32e-22 |
| 50%        |         1.0687 |         1.0686 |         0.0000 |         0.0000 |
| 75%        |         1.6003 |         1.6003 |       1.93e-08 |       4.28e-22 |
| max        |       1.44e+16 |            inf |            inf |            inf |

**Regression Analysis** (Python ~ Stata):

- **Model**: python = nan + nan * stata
- **R-squared**: nan
- **N observations**: 2,197,381

| Coefficient |     Estimate |    Std Error | t-statistic |   p-value |
|-------------|--------------|--------------|-------------|----------|
| Intercept   |          nan |          nan |         nan |       nan |
| Slope       |          nan |          nan |         nan |       nan |

**Feedback**:
- Num observations with std_diff >= TOL_DIFF_1: 3/2197381 (0.000%)
- Stata standard deviation: 4.50e+13

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

**Precision2**: 99th percentile diff = 1.07e-07 (tolerance: < 1.00e+00)

**Summary Statistics** (Common Observations):

| Statistic  |          Stata |         Python |     Difference | Std Difference |
|------------|----------------|----------------|----------------|----------------|
| count      |       3.50e+06 |       3.50e+06 |       3.50e+06 |       3.50e+06 |
| mean       |         0.0353 |         0.0354 |       9.71e-06 |       3.51e-05 |
| std        |         0.2767 |         0.2767 |         0.0032 |         0.0117 |
| min        |        -2.0000 |        -2.0000 |        -0.1176 |        -0.4252 |
| 25%        |        -0.0274 |        -0.0274 |      -1.10e-09 |      -3.97e-09 |
| 50%        |         0.0000 |         0.0000 |         0.0000 |         0.0000 |
| 75%        |         0.0997 |         0.0998 |       9.43e-10 |       3.41e-09 |
| max        |         2.0000 |         2.0000 |         1.6490 |         5.9598 |

**Regression Analysis** (Python ~ Stata):

- **Model**: python = 0.0000 + 0.9999 * stata
- **R-squared**: 0.9999
- **N observations**: 3,496,899

| Coefficient |     Estimate |    Std Error | t-statistic |   p-value |
|-------------|--------------|--------------|-------------|----------|
| Intercept   |     1.41e-05 |     1.75e-06 |      8.0749 |     0.000 |
| Slope       |       0.9999 |     6.28e-06 | 159334.3051 |     0.000 |

**Feedback**:
- Num observations with std_diff >= TOL_DIFF_1: 288/3496899 (0.008%)
- Stata standard deviation: 2.77e-01

---

### iomom_cust

**Status**: ✅ PASSED

**Test Results**:
- Test 1 - Column names: ✅ PASSED
- Test 2 - Superset check: ✅ PASSED
- Test 3 - Precision1 check: ✅ PASSED
- Test 4 - Precision2 check: ✅ PASSED

**Columns**: ['iomom_cust']

**Observations**:
- Stata:  1,637,670
- Python: 1,637,670
- Common: 1,637,670

**Precision1**: 0.034% obs with std_diff >= 1.00e-02 (tolerance: < 10%)

**Precision2**: 99th percentile diff = 1.75e-04 (tolerance: < 1.00e+00)

**Summary Statistics** (Common Observations):

| Statistic  |          Stata |         Python |     Difference | Std Difference |
|------------|----------------|----------------|----------------|----------------|
| count      |       1.64e+06 |       1.64e+06 |       1.64e+06 |       1.64e+06 |
| mean       |         1.7274 |         1.7274 |      -2.33e-05 |      -3.91e-06 |
| std        |         5.9574 |         5.9574 |         0.0294 |         0.0049 |
| min        |       -50.7987 |       -50.7987 |       -13.2719 |        -2.2278 |
| 25%        |        -1.4085 |        -1.4085 |      -7.07e-08 |      -1.19e-08 |
| 50%        |         1.8440 |         1.8440 |       2.36e-10 |       3.97e-11 |
| 75%        |         5.1077 |         5.1077 |       6.87e-08 |       1.15e-08 |
| max        |       147.0000 |       147.0000 |        13.5870 |         2.2807 |

**Regression Analysis** (Python ~ Stata):

- **Model**: python = -0.0000 + 1.0000 * stata
- **R-squared**: 1.0000
- **N observations**: 1,637,670

| Coefficient |     Estimate |    Std Error | t-statistic |   p-value |
|-------------|--------------|--------------|-------------|----------|
| Intercept   |    -4.44e-07 |     2.39e-05 |     -0.0186 |     0.985 |
| Slope       |       1.0000 |     3.85e-06 | 259475.9408 |     0.000 |

**Feedback**:
- Num observations with std_diff >= TOL_DIFF_1: 564/1637670 (0.034%)
- Stata standard deviation: 5.96e+00

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

**Precision2**: 99th percentile diff = 1.56e-04 (tolerance: < 1.00e+00)

**Summary Statistics** (Common Observations):

| Statistic  |          Stata |         Python |     Difference | Std Difference |
|------------|----------------|----------------|----------------|----------------|
| count      |       1.64e+06 |       1.64e+06 |       1.64e+06 |       1.64e+06 |
| mean       |         1.6156 |         1.6155 |      -1.57e-05 |      -3.00e-06 |
| std        |         5.2255 |         5.2256 |         0.0124 |         0.0024 |
| min        |       -46.2534 |       -46.2534 |        -4.2766 |        -0.8184 |
| 25%        |        -1.0228 |        -1.0228 |      -6.40e-08 |      -1.23e-08 |
| 50%        |         1.7934 |         1.7934 |      -3.98e-10 |      -7.63e-11 |
| 75%        |         4.5754 |         4.5754 |       6.12e-08 |       1.17e-08 |
| max        |       135.8487 |       135.8487 |         6.3168 |         1.2088 |

**Regression Analysis** (Python ~ Stata):

- **Model**: python = -0.0000 + 1.0000 * stata
- **R-squared**: 1.0000
- **N observations**: 1,639,842

| Coefficient |     Estimate |    Std Error | t-statistic |   p-value |
|-------------|--------------|--------------|-------------|----------|
| Intercept   |    -1.54e-05 |     1.01e-05 |     -1.5192 |     0.129 |
| Slope       |       1.0000 |     1.85e-06 | 539594.6405 |     0.000 |

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

**Precision2**: 99th percentile diff = 1.65e-07 (tolerance: < 1.00e+00)

**Summary Statistics** (Common Observations):

| Statistic  |          Stata |         Python |     Difference | Std Difference |
|------------|----------------|----------------|----------------|----------------|
| count      |       1.45e+06 |       1.45e+06 |       1.45e+06 |       1.45e+06 |
| mean       |      -9.58e-12 |           -inf |           -inf |           -inf |
| std        |         0.2476 |            N/A |            N/A |            N/A |
| min        |        -1.6407 |           -inf |           -inf |           -inf |
| 25%        |        -0.1188 |        -0.1191 |      -7.45e-09 |      -3.01e-08 |
| 50%        |        -0.0155 |        -0.0156 |         0.0000 |         0.0000 |
| 75%        |         0.0987 |         0.0986 |       7.51e-09 |       3.03e-08 |
| max        |        56.9154 |        56.9154 |         0.0043 |         0.0172 |

**Regression Analysis** (Python ~ Stata):

- **Model**: python = -inf + nan * stata
- **R-squared**: nan
- **N observations**: 1,448,154

| Coefficient |     Estimate |    Std Error | t-statistic |   p-value |
|-------------|--------------|--------------|-------------|----------|
| Intercept   |          nan |          nan |         nan |       nan |
| Slope       |          nan |          nan |         nan |       nan |

**Feedback**:
- Num observations with std_diff >= TOL_DIFF_1: 2091/1448154 (0.144%)
- Stata standard deviation: 2.48e-01

---

### retConglomerate

**Status**: ✅ PASSED

**Test Results**:
- Test 1 - Column names: ✅ PASSED
- Test 2 - Superset check: ✅ PASSED
- Test 3 - Precision1 check: ✅ PASSED
- Test 4 - Precision2 check: ✅ PASSED

**Columns**: ['retConglomerate']

**Observations**:
- Stata:  758,394
- Python: 759,896
- Common: 758,382

**Precision1**: 0.936% obs with std_diff >= 1.00e-02 (tolerance: < 10%)

**Precision2**: 99th percentile diff = 9.35e-03 (tolerance: < 1.00e+00)

**Summary Statistics** (Common Observations):

| Statistic  |          Stata |         Python |     Difference | Std Difference |
|------------|----------------|----------------|----------------|----------------|
| count      |    758382.0000 |    758382.0000 |    758382.0000 |    758382.0000 |
| mean       |         0.0106 |         0.0106 |      -1.25e-05 |      -1.49e-04 |
| std        |         0.0841 |         0.0841 |         0.0020 |         0.0240 |
| min        |        -0.8000 |        -0.8000 |        -0.4277 |        -5.0889 |
| 25%        |        -0.0313 |        -0.0313 |      -2.78e-17 |      -3.30e-16 |
| 50%        |         0.0105 |         0.0105 |         0.0000 |         0.0000 |
| 75%        |         0.0495 |         0.0495 |       2.78e-17 |       3.30e-16 |
| max        |         4.3779 |         4.3779 |         0.4479 |         5.3290 |

**Regression Analysis** (Python ~ Stata):

- **Model**: python = -0.0000 + 0.9997 * stata
- **R-squared**: 0.9994
- **N observations**: 758,382

| Coefficient |     Estimate |    Std Error | t-statistic |   p-value |
|-------------|--------------|--------------|-------------|----------|
| Intercept   |    -9.83e-06 |     2.33e-06 |     -4.2168 |     0.000 |
| Slope       |       0.9997 |     2.75e-05 |  36318.4957 |     0.000 |

**Feedback**:
- Num observations with std_diff >= TOL_DIFF_1: 7102/758382 (0.936%)
- Stata standard deviation: 8.41e-02

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

**Precision2**: 99th percentile diff = 3.34e-08 (tolerance: < 1.00e+00)

**Summary Statistics** (Common Observations):

| Statistic  |          Stata |         Python |     Difference | Std Difference |
|------------|----------------|----------------|----------------|----------------|
| count      |       2.49e+06 |       2.49e+06 |       2.49e+06 |       2.49e+06 |
| mean       |        -0.0085 |        -0.0085 |      -1.89e-06 |      -6.41e-06 |
| std        |         0.2948 |         0.2950 |         0.0090 |         0.0304 |
| min        |       -58.0917 |       -58.0917 |       -13.5145 |       -45.8400 |
| 25%        |        -0.0053 |        -0.0053 |      -2.63e-10 |      -8.91e-10 |
| 50%        |         0.0059 |         0.0059 |         0.0000 |         0.0000 |
| 75%        |         0.0184 |         0.0184 |       2.64e-10 |       8.94e-10 |
| max        |       171.9972 |       171.9972 |         1.8407 |         6.2436 |

**Regression Analysis** (Python ~ Stata):

- **Model**: python = -0.0000 + 1.0000 * stata
- **R-squared**: 0.9991
- **N observations**: 2,490,858

| Coefficient |     Estimate |    Std Error | t-statistic |   p-value |
|-------------|--------------|--------------|-------------|----------|
| Intercept   |    -1.71e-06 |     5.67e-06 |     -0.3013 |     0.763 |
| Slope       |       1.0000 |     1.92e-05 |  51975.9588 |     0.000 |

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

**Precision2**: 99th percentile diff = 1.38e-09 (tolerance: < 1.00e+00)

**Summary Statistics** (Common Observations):

| Statistic  |          Stata |         Python |     Difference | Std Difference |
|------------|----------------|----------------|----------------|----------------|
| count      |    609876.0000 |    609876.0000 |    609876.0000 |    609876.0000 |
| mean       |        -0.1056 |        -0.1052 |       3.61e-04 |       1.91e-05 |
| std        |        18.9485 |        18.9486 |         0.0463 |         0.0024 |
| min        |     -4241.4189 |     -4241.4190 |        -0.1008 |        -0.0053 |
| 25%        |         0.0258 |         0.0258 |      -1.56e-09 |      -8.21e-11 |
| 50%        |         0.0642 |         0.0642 |      -1.73e-18 |      -9.15e-20 |
| 75%        |         0.0970 |         0.0971 |       1.38e-09 |       7.29e-11 |
| max        |        12.2928 |        12.2928 |         9.9914 |         0.5273 |

**Regression Analysis** (Python ~ Stata):

- **Model**: python = 0.0004 + 1.0000 * stata
- **R-squared**: 1.0000
- **N observations**: 609,876

| Coefficient |     Estimate |    Std Error | t-statistic |   p-value |
|-------------|--------------|--------------|-------------|----------|
| Intercept   |     3.61e-04 |     5.93e-05 |      6.0906 |     0.000 |
| Slope       |       1.0000 |     3.13e-06 | 319348.4277 |     0.000 |

**Feedback**:
- Num observations with std_diff >= TOL_DIFF_1: 132/609876 (0.022%)
- Stata standard deviation: 1.89e+01

---

### sinAlgo

**Status**: ✅ PASSED

**Test Results**:
- Test 1 - Column names: ✅ PASSED
- Test 2 - Superset check: ✅ PASSED
- Test 3 - Precision1 check: ✅ PASSED
- Test 4 - Precision2 check: ✅ PASSED

**Columns**: ['sinAlgo']

**Observations**:
- Stata:  233,503
- Python: 233,996
- Common: 233,503

**Precision1**: 0.010% obs with std_diff >= 1.00e-02 (tolerance: < 10%)

**Precision2**: 99th percentile diff = 0.00e+00 (tolerance: < 1.00e+00)

**Summary Statistics** (Common Observations):

| Statistic  |          Stata |         Python |     Difference | Std Difference |
|------------|----------------|----------------|----------------|----------------|
| count      |    233503.0000 |    233503.0000 |    233503.0000 |    233503.0000 |
| mean       |         0.1802 |         0.1803 |       9.85e-05 |       2.56e-04 |
| std        |         0.3843 |         0.3844 |         0.0099 |         0.0258 |
| min        |         0.0000 |         0.0000 |         0.0000 |         0.0000 |
| 25%        |         0.0000 |         0.0000 |         0.0000 |         0.0000 |
| 50%        |         0.0000 |         0.0000 |         0.0000 |         0.0000 |
| 75%        |         0.0000 |         0.0000 |         0.0000 |         0.0000 |
| max        |         1.0000 |         1.0000 |         1.0000 |         2.6019 |

**Regression Analysis** (Python ~ Stata):

- **Model**: python = 0.0001 + 0.9999 * stata
- **R-squared**: 0.9993
- **N observations**: 233,503

| Coefficient |     Estimate |    Std Error | t-statistic |   p-value |
|-------------|--------------|--------------|-------------|----------|
| Intercept   |     1.20e-04 |     2.27e-05 |      5.2970 |     0.000 |
| Slope       |       0.9999 |     5.34e-05 |  18711.4230 |     0.000 |

**Feedback**:
- Num observations with std_diff >= TOL_DIFF_1: 23/233503 (0.010%)
- Stata standard deviation: 3.84e-01

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

**Precision2**: 99th percentile diff = 1.21e-07 (tolerance: < 1.00e+00)

**Summary Statistics** (Common Observations):

| Statistic  |          Stata |         Python |     Difference | Std Difference |
|------------|----------------|----------------|----------------|----------------|
| count      |    470063.0000 |    470063.0000 |    470063.0000 |    470063.0000 |
| mean       |         0.0515 |         0.0515 |       2.78e-06 |       3.37e-05 |
| std        |         0.0826 |         0.0826 |         0.0019 |         0.0236 |
| min        |        -1.3802 |        -1.3802 |        -0.5310 |        -6.4297 |
| 25%        |         0.0170 |         0.0170 |         0.0000 |         0.0000 |
| 50%        |         0.0381 |         0.0381 |         0.0000 |         0.0000 |
| 75%        |         0.0686 |         0.0686 |         0.0000 |         0.0000 |
| max        |         1.6481 |         1.6481 |         0.3527 |         4.2711 |

**Regression Analysis** (Python ~ Stata):

- **Model**: python = 0.0000 + 0.9998 * stata
- **R-squared**: 0.9994
- **N observations**: 470,063

| Coefficient |     Estimate |    Std Error | t-statistic |   p-value |
|-------------|--------------|--------------|-------------|----------|
| Intercept   |     1.55e-05 |     3.35e-06 |      4.6246 |     0.000 |
| Slope       |       0.9998 |     3.44e-05 |  29045.4671 |     0.000 |

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

**Precision2**: 99th percentile diff = 1.28e-08 (tolerance: < 1.00e+00)

**Summary Statistics** (Common Observations):

| Statistic  |          Stata |         Python |     Difference | Std Difference |
|------------|----------------|----------------|----------------|----------------|
| count      |       2.17e+06 |       2.17e+06 |       2.17e+06 |       2.17e+06 |
| mean       |         0.2270 |         0.2270 |       2.09e-10 |       5.96e-11 |
| std        |         3.5115 |         3.5115 |       7.13e-08 |       2.03e-08 |
| min        |       6.96e-06 |       6.96e-06 |      -1.89e-05 |      -5.37e-06 |
| 25%        |         0.0161 |         0.0161 |      -3.90e-10 |      -1.11e-10 |
| 50%        |         0.0367 |         0.0367 |      -2.34e-12 |      -6.67e-13 |
| 75%        |         0.0941 |         0.0941 |       3.74e-10 |       1.07e-10 |
| max        |       711.4860 |       711.4860 |       9.53e-06 |       2.71e-06 |

**Regression Analysis** (Python ~ Stata):

- **Model**: python = 0.0000 + 1.0000 * stata
- **R-squared**: 1.0000
- **N observations**: 2,166,204

| Coefficient |     Estimate |    Std Error | t-statistic |   p-value |
|-------------|--------------|--------------|-------------|----------|
| Intercept   |     3.73e-10 |     4.85e-11 |      7.6862 |     0.000 |
| Slope       |       1.0000 |     1.38e-11 |    7.25e+10 |     0.000 |

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

**Precision2**: 99th percentile diff = 2.40e-07 (tolerance: < 1.00e+00)

**Summary Statistics** (Common Observations):

| Statistic  |          Stata |         Python |     Difference | Std Difference |
|------------|----------------|----------------|----------------|----------------|
| count      |       1.52e+06 |       1.52e+06 |       1.52e+06 |       1.52e+06 |
| mean       |         0.6912 |         0.6912 |       7.94e-08 |       4.21e-07 |
| std        |         0.1888 |         0.1888 |       1.21e-05 |       6.43e-05 |
| min        |         0.0000 |         0.0000 |      -1.37e-07 |      -7.25e-07 |
| 25%        |         0.5956 |         0.5956 |      -1.35e-08 |      -7.14e-08 |
| 50%        |         0.6959 |         0.6959 |      -2.19e-11 |      -1.16e-10 |
| 75%        |         0.7978 |         0.7978 |       1.34e-08 |       7.12e-08 |
| max        |         7.1460 |         7.1460 |         0.0024 |         0.0125 |

**Regression Analysis** (Python ~ Stata):

- **Model**: python = -0.0000 + 1.0000 * stata
- **R-squared**: 1.0000
- **N observations**: 1,517,107

| Coefficient |     Estimate |    Std Error | t-statistic |   p-value |
|-------------|--------------|--------------|-------------|----------|
| Intercept   |    -7.18e-07 |     3.74e-08 |    -19.2099 |     0.000 |
| Slope       |       1.0000 |     5.22e-08 |    1.92e+07 |     0.000 |

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

**Precision2**: 99th percentile diff = 1.59e-07 (tolerance: < 1.00e+00)

**Summary Statistics** (Common Observations):

| Statistic  |          Stata |         Python |     Difference | Std Difference |
|------------|----------------|----------------|----------------|----------------|
| count      |       4.34e+06 |       4.34e+06 |       4.34e+06 |       4.34e+06 |
| mean       |        17.8741 |        17.8741 |       4.12e-08 |       1.02e-09 |
| std        |        40.3912 |        40.3912 |       1.19e-06 |       2.94e-08 |
| min        |       1.49e-11 |       1.49e-11 |      -1.26e-05 |      -3.11e-07 |
| 25%        |       6.15e-08 |       6.15e-08 |      -3.76e-15 |      -9.31e-17 |
| 50%        |       2.22e-07 |       2.22e-07 |       3.08e-16 |       7.63e-18 |
| 75%        |        10.8837 |        10.8837 |       2.37e-14 |       5.87e-16 |
| max        |       251.0160 |       251.0160 |       1.25e-05 |       3.09e-07 |

**Regression Analysis** (Python ~ Stata):

- **Model**: python = 0.0000 + 1.0000 * stata
- **R-squared**: 1.0000
- **N observations**: 4,342,889

| Coefficient |     Estimate |    Std Error | t-statistic |   p-value |
|-------------|--------------|--------------|-------------|----------|
| Intercept   |     7.81e-09 |     6.22e-10 |     12.5575 |     0.000 |
| Slope       |       1.0000 |     1.41e-11 |    7.10e+10 |     0.000 |

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

**Precision2**: 99th percentile diff = 1.53e-07 (tolerance: < 1.00e+00)

**Summary Statistics** (Common Observations):

| Statistic  |          Stata |         Python |     Difference | Std Difference |
|------------|----------------|----------------|----------------|----------------|
| count      |       4.68e+06 |       4.68e+06 |       4.68e+06 |       4.68e+06 |
| mean       |         1.5093 |         1.5093 |       8.03e-10 |       2.21e-10 |
| std        |         3.6329 |         3.6329 |       1.17e-07 |       3.22e-08 |
| min        |       7.34e-13 |       7.34e-13 |      -1.44e-06 |      -3.97e-07 |
| 25%        |       1.65e-08 |       1.65e-08 |      -9.05e-16 |      -2.49e-16 |
| 50%        |       4.69e-08 |       4.69e-08 |       1.09e-17 |       2.99e-18 |
| 75%        |         0.9130 |         0.9130 |       1.08e-15 |       2.96e-16 |
| max        |        20.2225 |        20.2225 |       1.44e-06 |       3.98e-07 |

**Regression Analysis** (Python ~ Stata):

- **Model**: python = 0.0000 + 1.0000 * stata
- **R-squared**: 1.0000
- **N observations**: 4,680,231

| Coefficient |     Estimate |    Std Error | t-statistic |   p-value |
|-------------|--------------|--------------|-------------|----------|
| Intercept   |     1.71e-10 |     5.85e-11 |      2.9209 |     0.003 |
| Slope       |       1.0000 |     1.49e-11 |    6.72e+10 |     0.000 |

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

**Precision2**: 99th percentile diff = 1.48e-07 (tolerance: < 1.00e+00)

**Summary Statistics** (Common Observations):

| Statistic  |          Stata |         Python |     Difference | Std Difference |
|------------|----------------|----------------|----------------|----------------|
| count      |       4.53e+06 |       4.53e+06 |       4.53e+06 |       4.53e+06 |
| mean       |         9.1074 |         9.1074 |       1.65e-08 |       7.91e-10 |
| std        |        20.8086 |        20.8086 |       6.23e-07 |       3.00e-08 |
| min        |       2.14e-11 |       2.14e-11 |      -8.78e-06 |      -4.22e-07 |
| 25%        |       1.21e-07 |       1.21e-07 |      -9.31e-15 |      -4.47e-16 |
| 50%        |       3.90e-07 |       3.90e-07 |       1.93e-16 |       9.25e-18 |
| 75%        |         5.0000 |         5.0000 |       1.45e-14 |       6.97e-16 |
| max        |       125.1831 |       125.1831 |       8.73e-06 |       4.19e-07 |

**Regression Analysis** (Python ~ Stata):

- **Model**: python = 0.0000 + 1.0000 * stata
- **R-squared**: 1.0000
- **N observations**: 4,530,678

| Coefficient |     Estimate |    Std Error | t-statistic |   p-value |
|-------------|--------------|--------------|-------------|----------|
| Intercept   |     2.42e-09 |     3.19e-10 |      7.5938 |     0.000 |
| Slope       |       1.0000 |     1.41e-11 |    7.11e+10 |     0.000 |

**Feedback**:
- Num observations with std_diff >= TOL_DIFF_1: 0/4530678 (0.000%)
- Stata standard deviation: 2.08e+01

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

### IndIPO

**Status**: ❌ FAILED

**Test Results**:
- Test 1 - Column names: ❌ FAILED
- Test 2 - Superset check: ❌ FAILED (Python missing 0 Stata observations)
- Test 3 - Precision1 check: ❌ FAILED
- Test 4 - Precision2 check: ❌ FAILED

**Columns**: []

**Observations**:
- Stata:  0
- Python: 4,047,630
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

### debug_PatentsRD

**Status**: ❌ FAILED

**Test Results**:
- Test 1 - Column names: ❌ FAILED
- Test 2 - Superset check: ❌ FAILED (Python missing 0 Stata observations)
- Test 3 - Precision1 check: ❌ FAILED
- Test 4 - Precision2 check: ❌ FAILED

**Columns**: []

**Observations**:
- Stata:  0
- Python: 519,948
- Common: 0

---

### test_patentsrd

**Status**: ❌ FAILED

**Test Results**:
- Test 1 - Column names: ❌ FAILED
- Test 2 - Superset check: ❌ FAILED (Python missing 0 Stata observations)
- Test 3 - Precision1 check: ❌ FAILED
- Test 4 - Precision2 check: ❌ FAILED

**Columns**: []

**Observations**:
- Stata:  0
- Python: 12
- Common: 0

---

