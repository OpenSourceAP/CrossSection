# Predictor Validation Results

**Generated**: 2025-08-08 19:26:29

**Configuration**:
- PTH_PERCENTILE: 1.0
- TOL_DIFF_1: 0.0001
- TOL_OBS_1: 0.1%
- TOL_DIFF_2: 1e-06
- INDEX_COLS: ['permno', 'yyyymm']

## Summary

| Predictor                 | Python CSV | Columns  | Superset  | Precision1   | Precision2              |
|---------------------------|------------|----------|-----------|--------------|-------------------------|
| Recomm_ShortInterest      | ✅         | ✅       | ❌ (87.39%)  | ✅ (0.00%)    | ✅ (100th diff 0.0E+00)  |
| retConglomerate           | ✅         | ✅       | ❌ (23.24%)  | ❌ (96.72%)   | ❌ (100th diff 3.9E+00)  |
| Mom6mJunk                 | ✅         | ✅       | ❌ (18.09%)  | ❌ (0.28%)    | ❌ (100th diff 1.2E+00)  |
| Coskewness                | ✅         | ✅       | ❌ (8.59%)   | ❌ (99.98%)   | ❌ (100th diff 8.6E+00)  |
| RDAbility                 | ✅         | ✅       | ❌ (4.88%)   | ❌ (100.00%)  | ❌ (100th diff NAN)      |
| RIO_Volatility            | ✅         | ✅       | ❌ (4.40%)   | ❌ (26.58%)   | ❌ (100th diff 4.0E+00)  |
| ResidualMomentum          | ✅         | ✅       | ❌ (2.40%)   | ❌ (12.49%)   | ❌ (100th diff 4.4E-02)  |
| MomRev                    | ✅         | ✅       | ❌ (1.26%)   | ✅ (0.00%)    | ✅ (100th diff 0.0E+00)  |
| CPVolSpread               | ✅         | ✅       | ❌ (0.74%)   | ✅ (0.05%)    | ❌ (100th diff 5.3E-01)  |
| OptionVolume2             | ✅         | ✅       | ❌ (0.72%)   | ✅ (0.07%)    | ❌ (100th diff 1.2E+02)  |
| OptionVolume1             | ✅         | ✅       | ❌ (0.72%)   | ❌ (3.33%)    | ❌ (100th diff 5.4E+03)  |
| dVolPut                   | ✅         | ✅       | ❌ (0.71%)   | ✅ (0.04%)    | ❌ (100th diff 1.6E+00)  |
| dCPVolSpread              | ✅         | ✅       | ❌ (0.71%)   | ✅ (0.04%)    | ❌ (100th diff 1.5E+00)  |
| dVolCall                  | ✅         | ✅       | ❌ (0.71%)   | ✅ (0.04%)    | ❌ (100th diff 9.7E-01)  |
| skew1                     | ✅         | ✅       | ❌ (0.71%)   | ✅ (0.04%)    | ❌ (100th diff 5.3E-01)  |
| SmileSlope                | ✅         | ✅       | ❌ (0.71%)   | ✅ (0.05%)    | ❌ (100th diff 2.5E+00)  |
| RIVolSpread               | ✅         | ✅       | ❌ (0.71%)   | ✅ (0.05%)    | ❌ (100th diff 8.3E-01)  |
| AbnormalAccruals          | ✅         | ✅       | ❌ (0.65%)   | ❌ (64.27%)   | ❌ (100th diff 3.7E+00)  |
| BetaFP                    | ✅         | ✅       | ❌ (0.54%)   | ❌ (96.65%)   | ❌ (100th diff NAN)      |
| IntanBM                   | ✅         | ✅       | ❌ (0.39%)   | ❌ (99.49%)   | ❌ (100th diff 4.0E+00)  |
| IntanSP                   | ✅         | ✅       | ❌ (0.31%)   | ❌ (99.47%)   | ❌ (100th diff 1.1E+01)  |
| IntanCFP                  | ✅         | ✅       | ❌ (0.31%)   | ❌ (97.56%)   | ❌ (100th diff 9.6E+00)  |
| IntanEP                   | ✅         | ✅       | ❌ (0.31%)   | ❌ (96.53%)   | ❌ (100th diff 1.5E+01)  |
| PredictedFE               | ✅         | ✅       | ❌ (0.27%)   | ❌ (98.70%)   | ❌ (100th diff 5.1E-02)  |
| RIO_Disp                  | ✅         | ✅       | ❌ (0.24%)   | ❌ (6.72%)    | ❌ (100th diff 4.0E+00)  |
| ConsRecomm                | ✅         | ✅       | ❌ (0.23%)   | ✅ (0.01%)    | ❌ (100th diff 1.0E+00)  |
| AOP                       | ✅         | ✅       | ❌ (0.22%)   | ❌ (3.16%)    | ❌ (100th diff 2.4E+03)  |
| AnalystValue              | ✅         | ✅       | ❌ (0.22%)   | ❌ (2.66%)    | ❌ (100th diff 1.2E+01)  |
| fgr5yrLag                 | ✅         | ✅       | ❌ (0.22%)   | ✅ (0.07%)    | ❌ (100th diff 4.5E+01)  |
| sfe                       | ✅         | ✅       | ❌ (0.20%)   | ✅ (0.07%)    | ❌ (100th diff 1.0E+01)  |
| RIO_MB                    | ✅         | ✅       | ❌ (0.18%)   | ❌ (17.07%)   | ❌ (100th diff 4.0E+00)  |
| AnalystRevision           | ✅         | ✅       | ❌ (0.16%)   | ✅ (0.08%)    | ❌ (100th diff 5.4E+01)  |
| RIO_Turnover              | ✅         | ✅       | ❌ (0.15%)   | ❌ (23.71%)   | ❌ (100th diff 4.0E+00)  |
| ExclExp                   | ✅         | ✅       | ❌ (0.12%)   | ❌ (0.11%)    | ❌ (100th diff 3.7E+00)  |
| ChNAnalyst                | ✅         | ✅       | ❌ (0.11%)   | ✅ (0.01%)    | ❌ (100th diff 1.0E+00)  |
| MS                        | ✅         | ✅       | ❌ (0.07%)   | ❌ (63.49%)   | ❌ (100th diff 5.0E+00)  |
| TrendFactor               | ✅         | ✅       | ❌ (0.07%)   | ❌ (99.90%)   | ❌ (100th diff 5.4E+00)  |
| OScore                    | ✅         | ✅       | ❌ (0.04%)   | ✅ (0.00%)    | ✅ (100th diff 0.0E+00)  |
| CustomerMomentum          | ✅         | ✅       | ❌ (0.04%)   | ✅ (0.01%)    | ❌ (100th diff 2.0E-01)  |
| std_turn                  | ✅         | ✅       | ❌ (0.04%)   | ✅ (0.00%)    | ❌ (100th diff 1.9E-05)  |
| ShareVol                  | ✅         | ✅       | ❌ (0.03%)   | ❌ (14.38%)   | ❌ (100th diff 1.0E+00)  |
| VolSD                     | ✅         | ✅       | ❌ (0.02%)   | ❌ (0.31%)    | ❌ (100th diff 3.0E+01)  |
| tang                      | ✅         | ✅       | ❌ (0.02%)   | ✅ (0.00%)    | ❌ (100th diff 2.4E-03)  |
| VolMkt                    | ✅         | ✅       | ❌ (0.02%)   | ✅ (0.10%)    | ❌ (100th diff 5.3E+00)  |
| ReturnSkew3F              | ✅         | ✅       | ❌ (0.00%)   | ❌ (13.29%)   | ❌ (100th diff 8.7E+00)  |
| AnnouncementReturn        | ✅         | ✅       | ❌ (0.00%)   | ❌ (0.35%)    | ❌ (100th diff 3.2E-01)  |
| MomOffSeason11YrPlus      | ✅         | ✅       | ❌ (0.00%)   | ❌ (26.20%)   | ❌ (100th diff 4.4E+00)  |
| MomVol                    | ✅         | ✅       | ❌ (0.00%)   | ❌ (0.42%)    | ❌ (100th diff 1.0E+00)  |
| ChTax                     | ✅         | ✅       | ❌ (0.00%)   | ✅ (0.01%)    | ❌ (100th diff 6.9E-01)  |
| PS                        | ✅         | ✅       | ❌ (0.00%)   | ❌ (17.88%)   | ❌ (100th diff 5.0E+00)  |
| InvGrowth                 | ✅         | ✅       | ❌ (0.00%)   | ❌ (0.32%)    | ❌ (100th diff 3.6E-01)  |
| EntMult                   | ✅         | ✅       | ❌ (0.00%)   | ✅ (0.05%)    | ❌ (100th diff 2.2E+00)  |
| DivSeason                 | ✅         | ✅       | ❌ (0.00%)   | ❌ (5.21%)    | ❌ (100th diff 1.0E+00)  |
| NetDebtPrice              | ✅         | ✅       | ❌ (0.00%)   | ✅ (0.00%)    | ❌ (100th diff 4.2E-02)  |
| BetaTailRisk              | ✅         | ✅       | ✅           | ❌ (99.99%)   | ❌ (100th diff 1.1E+01)  |
| CompEquIss                | ✅         | ✅       | ✅           | ❌ (99.88%)   | ❌ (100th diff 2.0E+03)  |
| Frontier                  | ✅         | ✅       | ✅           | ❌ (99.81%)   | ❌ (100th diff 6.0E+00)  |
| BetaLiquidityPS           | ✅         | ✅       | ✅           | ❌ (99.22%)   | ❌ (100th diff 6.4E+00)  |
| Beta                      | ✅         | ✅       | ✅           | ❌ (99.02%)   | ❌ (100th diff 7.3E+00)  |
| Mom12mOffSeason           | ✅         | ✅       | ✅           | ❌ (95.89%)   | ❌ (100th diff 2.4E+00)  |
| DivYieldST                | ✅         | ✅       | ✅           | ❌ (89.46%)   | ❌ (100th diff 2.0E+00)  |
| betaVIX                   | ✅         | ✅       | ✅           | ❌ (77.90%)   | ❌ (100th diff 5.7E-01)  |
| IdioVolAHT                | ✅         | ✅       | ✅           | ❌ (45.95%)   | ❌ (100th diff NAN)      |
| PriceDelayTstat           | ✅         | ✅       | ✅           | ❌ (28.09%)   | ❌ (100th diff 1.1E+01)  |
| MomOffSeason06YrPlus      | ✅         | ✅       | ✅           | ❌ (27.03%)   | ❌ (100th diff 1.1E+01)  |
| REV6                      | ✅         | ✅       | ✅           | ❌ (25.74%)   | ❌ (100th diff 8.4E+03)  |
| MomOffSeason              | ✅         | ✅       | ✅           | ❌ (23.11%)   | ❌ (100th diff 4.1E+00)  |
| MomOffSeason16YrPlus      | ✅         | ✅       | ✅           | ❌ (14.63%)   | ❌ (100th diff 2.2E-01)  |
| IndMom                    | ✅         | ✅       | ✅           | ❌ (12.95%)   | ❌ (100th diff 1.3E+00)  |
| MeanRankRevGrowth         | ✅         | ✅       | ✅           | ❌ (12.20%)   | ❌ (100th diff 1.3E+01)  |
| PriceDelaySlope           | ✅         | ✅       | ✅           | ❌ (11.66%)   | ❌ (100th diff 1.6E+04)  |
| BrandInvest               | ✅         | ✅       | ✅           | ❌ (11.28%)   | ❌ (100th diff 6.9E+01)  |
| CoskewACX                 | ✅         | ✅       | ✅           | ❌ (5.38%)    | ❌ (100th diff 4.7E-03)  |
| PriceDelayRsq             | ✅         | ✅       | ✅           | ❌ (4.25%)    | ❌ (100th diff 9.6E-01)  |
| iomom_supp                | ✅         | ✅       | ✅           | ❌ (4.11%)    | ❌ (100th diff 6.3E+00)  |
| iomom_cust                | ✅         | ✅       | ✅           | ❌ (2.99%)    | ❌ (100th diff 1.4E+01)  |
| HerfBE                    | ✅         | ✅       | ✅           | ❌ (2.40%)    | ❌ (100th diff 6.4E+02)  |
| HerfAsset                 | ✅         | ✅       | ✅           | ❌ (2.18%)    | ❌ (100th diff 6.4E-01)  |
| Investment                | ✅         | ✅       | ✅           | ❌ (1.50%)    | ❌ (100th diff 3.1E+01)  |
| Tax                       | ✅         | ✅       | ✅           | ❌ (1.34%)    | ❌ (100th diff 2.0E+03)  |
| Herf                      | ✅         | ✅       | ✅           | ❌ (1.02%)    | ❌ (100th diff 2.2E+00)  |
| VolumeTrend               | ✅         | ✅       | ✅           | ❌ (1.02%)    | ❌ (100th diff 1.2E-01)  |
| CredRatDG                 | ✅         | ✅       | ✅           | ❌ (0.94%)    | ❌ (100th diff 1.0E+00)  |
| RDS                       | ✅         | ✅       | ✅           | ❌ (0.76%)    | ❌ (100th diff 7.1E+01)  |
| ChInvIA                   | ✅         | ✅       | ✅           | ❌ (0.58%)    | ❌ (100th diff 1.7E+09)  |
| realestate                | ✅         | ✅       | ✅           | ❌ (0.30%)    | ❌ (100th diff INF)      |
| BPEBM                     | ✅         | ✅       | ✅           | ❌ (0.27%)    | ❌ (100th diff 4.0E+03)  |
| EBM                       | ✅         | ✅       | ✅           | ❌ (0.27%)    | ❌ (100th diff 4.0E+03)  |
| IdioVol3F                 | ✅         | ✅       | ✅           | ❌ (0.25%)    | ❌ (100th diff 1.8E-02)  |
| CashProd                  | ✅         | ✅       | ✅           | ❌ (0.17%)    | ❌ (100th diff 2.0E-01)  |
| EquityDuration            | ✅         | ✅       | ✅           | ❌ (0.17%)    | ❌ (100th diff 3.3E+05)  |
| MRreversal                | ✅         | ✅       | ✅           | ❌ (0.15%)    | ❌ (100th diff 1.2E+01)  |
| LRreversal                | ✅         | ✅       | ✅           | ❌ (0.13%)    | ❌ (100th diff 2.7E+01)  |
| ChForecastAccrual         | ✅         | ✅       | ✅           | ❌ (0.12%)    | ❌ (100th diff 1.0E+00)  |
| ChAssetTurnover           | ✅         | ✅       | ✅           | ✅ (0.09%)    | ❌ (100th diff 1.3E+01)  |
| Cash                      | ✅         | ✅       | ✅           | ✅ (0.06%)    | ❌ (100th diff 6.8E-01)  |
| BookLeverage              | ✅         | ✅       | ✅           | ✅ (0.06%)    | ❌ (100th diff 9.9E-01)  |
| ExchSwitch                | ✅         | ✅       | ✅           | ✅ (0.05%)    | ❌ (100th diff 1.0E+00)  |
| BM                        | ✅         | ✅       | ✅           | ✅ (0.03%)    | ❌ (100th diff 3.7E+00)  |
| OperProf                  | ✅         | ✅       | ✅           | ✅ (0.02%)    | ❌ (100th diff 2.5E-01)  |
| GP                        | ✅         | ✅       | ✅           | ✅ (0.02%)    | ❌ (100th diff 1.1E+00)  |
| Accruals                  | ✅         | ✅       | ✅           | ✅ (0.02%)    | ❌ (100th diff 5.5E-01)  |
| DelNetFin                 | ✅         | ✅       | ✅           | ✅ (0.02%)    | ❌ (100th diff 7.5E-01)  |
| PctTotAcc                 | ✅         | ✅       | ✅           | ✅ (0.01%)    | ❌ (100th diff 2.8E+00)  |
| CBOperProf                | ✅         | ✅       | ✅           | ✅ (0.01%)    | ❌ (100th diff 4.3E-02)  |
| DelDRC                    | ✅         | ✅       | ✅           | ✅ (0.01%)    | ❌ (100th diff 1.4E-02)  |
| ChNNCOA                   | ✅         | ✅       | ✅           | ✅ (0.01%)    | ❌ (100th diff 7.5E-01)  |
| VarCF                     | ✅         | ✅       | ✅           | ✅ (0.01%)    | ❌ (100th diff 1.8E-02)  |
| roaq                      | ✅         | ✅       | ✅           | ✅ (0.01%)    | ❌ (100th diff 1.4E+01)  |
| sinAlgo                   | ✅         | ✅       | ✅           | ✅ (0.01%)    | ❌ (100th diff 1.0E+00)  |
| OperProfRD                | ✅         | ✅       | ✅           | ✅ (0.01%)    | ❌ (100th diff 4.4E-02)  |
| dNoa                      | ✅         | ✅       | ✅           | ✅ (0.01%)    | ❌ (100th diff 6.6E-01)  |
| BMdec                     | ✅         | ✅       | ✅           | ✅ (0.01%)    | ❌ (100th diff 1.2E-01)  |
| hire                      | ✅         | ✅       | ✅           | ✅ (0.01%)    | ❌ (100th diff 1.6E+00)  |
| DelLTI                    | ✅         | ✅       | ✅           | ✅ (0.01%)    | ❌ (100th diff 7.5E-01)  |
| CompositeDebtIssuance     | ✅         | ✅       | ✅           | ✅ (0.01%)    | ❌ (100th diff 6.5E-01)  |
| DivInit                   | ✅         | ✅       | ✅           | ✅ (0.01%)    | ❌ (100th diff 1.0E+00)  |
| ChNWC                     | ✅         | ✅       | ✅           | ✅ (0.01%)    | ❌ (100th diff 4.8E-01)  |
| DelFINL                   | ✅         | ✅       | ✅           | ✅ (0.01%)    | ❌ (100th diff 4.9E-02)  |
| DelCOL                    | ✅         | ✅       | ✅           | ✅ (0.01%)    | ❌ (100th diff 5.5E-01)  |
| CF                        | ✅         | ✅       | ✅           | ✅ (0.01%)    | ❌ (100th diff 2.3E-01)  |
| SurpriseRD                | ✅         | ✅       | ✅           | ✅ (0.01%)    | ❌ (100th diff 1.0E+00)  |
| SP                        | ✅         | ✅       | ✅           | ✅ (0.00%)    | ❌ (100th diff 9.2E-03)  |
| DivOmit                   | ✅         | ✅       | ✅           | ✅ (0.00%)    | ❌ (100th diff 1.0E+00)  |
| XFIN                      | ✅         | ✅       | ✅           | ✅ (0.00%)    | ❌ (100th diff 8.8E-02)  |
| PctAcc                    | ✅         | ✅       | ✅           | ✅ (0.00%)    | ❌ (100th diff 1.0E+01)  |
| DelCOA                    | ✅         | ✅       | ✅           | ✅ (0.00%)    | ❌ (100th diff 1.8E-02)  |
| ChEQ                      | ✅         | ✅       | ✅           | ✅ (0.00%)    | ❌ (100th diff 1.7E-01)  |
| CitationsRD               | ✅         | ✅       | ✅           | ✅ (0.00%)    | ❌ (100th diff 1.0E+00)  |
| ChInv                     | ✅         | ✅       | ✅           | ✅ (0.00%)    | ❌ (100th diff 2.0E-02)  |
| RoE                       | ✅         | ✅       | ✅           | ✅ (0.00%)    | ❌ (100th diff 3.4E-01)  |
| DelEqu                    | ✅         | ✅       | ✅           | ✅ (0.00%)    | ❌ (100th diff 5.5E-01)  |
| TotalAccruals             | ✅         | ✅       | ✅           | ✅ (0.00%)    | ❌ (100th diff 9.0E-02)  |
| AM                        | ✅         | ✅       | ✅           | ✅ (0.00%)    | ❌ (100th diff 2.5E-01)  |
| AssetGrowth               | ✅         | ✅       | ✅           | ✅ (0.00%)    | ❌ (100th diff 1.1E-01)  |
| OrderBacklogChg           | ✅         | ✅       | ✅           | ✅ (0.00%)    | ❌ (100th diff 4.4E-02)  |
| ConvDebt                  | ✅         | ✅       | ✅           | ✅ (0.00%)    | ❌ (100th diff 1.0E+00)  |
| Leverage                  | ✅         | ✅       | ✅           | ✅ (0.00%)    | ❌ (100th diff 5.1E-02)  |
| RD                        | ✅         | ✅       | ✅           | ✅ (0.00%)    | ❌ (100th diff 1.3E-02)  |
| cfp                       | ✅         | ✅       | ✅           | ✅ (0.00%)    | ❌ (100th diff 1.9E-01)  |
| zerotrade12M              | ✅         | ✅       | ✅           | ✅ (0.00%)    | ❌ (100th diff 1.3E-05)  |
| zerotrade6M               | ✅         | ✅       | ✅           | ✅ (0.00%)    | ❌ (100th diff 8.8E-06)  |
| EP                        | ✅         | ✅       | ✅           | ✅ (0.00%)    | ❌ (100th diff 8.7E-06)  |
| Mom12m                    | ✅         | ✅       | ✅           | ✅ (0.00%)    | ❌ (100th diff 4.3E-06)  |
| AdExp                     | ✅         | ✅       | ✅           | ✅ (0.00%)    | ❌ (100th diff 3.8E-06)  |
| OrderBacklog              | ✅         | ✅       | ✅           | ✅ (0.00%)    | ❌ (100th diff 2.7E-06)  |
| IntMom                    | ✅         | ✅       | ✅           | ✅ (0.00%)    | ❌ (100th diff 2.2E-06)  |
| DelBreadth                | ✅         | ✅       | ✅           | ✅ (0.00%)    | ❌ (100th diff 2.0E-06)  |
| Mom6m                     | ✅         | ✅       | ✅           | ✅ (0.00%)    | ❌ (100th diff 1.7E-06)  |
| zerotrade1M               | ✅         | ✅       | ✅           | ✅ (0.00%)    | ❌ (100th diff 1.4E-06)  |
| RDcap                     | ✅         | ✅       | ✅           | ✅ (0.00%)    | ❌ (100th diff 1.3E-06)  |
| DolVol                    | ✅         | ✅       | ✅           | ✅ (0.00%)    | ✅ (100th diff 9.6E-07)  |
| Price                     | ✅         | ✅       | ✅           | ✅ (0.00%)    | ✅ (100th diff 9.1E-07)  |
| MomSeason                 | ✅         | ✅       | ✅           | ✅ (0.00%)    | ✅ (100th diff 6.0E-07)  |
| MomSeasonShort            | ✅         | ✅       | ✅           | ✅ (0.00%)    | ✅ (100th diff 5.0E-07)  |
| STreversal                | ✅         | ✅       | ✅           | ✅ (0.00%)    | ✅ (100th diff 5.0E-07)  |
| Size                      | ✅         | ✅       | ✅           | ✅ (0.00%)    | ✅ (100th diff 5.0E-07)  |
| MomSeason06YrPlus         | ✅         | ✅       | ✅           | ✅ (0.00%)    | ✅ (100th diff 3.7E-07)  |
| MomSeason11YrPlus         | ✅         | ✅       | ✅           | ✅ (0.00%)    | ✅ (100th diff 2.0E-07)  |
| MomSeason16YrPlus         | ✅         | ✅       | ✅           | ✅ (0.00%)    | ✅ (100th diff 2.0E-07)  |
| BidAskSpread              | ✅         | ✅       | ✅           | ✅ (0.00%)    | ✅ (100th diff 1.0E-07)  |
| ProbInformedTrading       | ✅         | ✅       | ✅           | ✅ (0.00%)    | ✅ (100th diff 5.0E-08)  |
| Illiquidity               | ✅         | ✅       | ✅           | ✅ (0.00%)    | ✅ (100th diff 4.0E-09)  |
| ReturnSkew                | ✅         | ✅       | ✅           | ✅ (0.00%)    | ✅ (100th diff 1.6E-14)  |
| RealizedVol               | ✅         | ✅       | ✅           | ✅ (0.00%)    | ✅ (100th diff 3.6E-15)  |
| AccrualsBM                | ✅         | ✅       | ✅           | ✅ (0.00%)    | ✅ (100th diff 0.0E+00)  |
| DebtIssuance              | ✅         | ✅       | ✅           | ✅ (0.00%)    | ✅ (100th diff 0.0E+00)  |
| FirmAge                   | ✅         | ✅       | ✅           | ✅ (0.00%)    | ✅ (100th diff 0.0E+00)  |
| Governance                | ✅         | ✅       | ✅           | ✅ (0.00%)    | ✅ (100th diff 0.0E+00)  |
| MaxRet                    | ✅         | ✅       | ✅           | ✅ (0.00%)    | ✅ (100th diff 0.0E+00)  |
| Spinoff                   | ✅         | ✅       | ✅           | ✅ (0.00%)    | ✅ (100th diff 0.0E+00)  |
| Activism1                 | ❌         | NA      | NA          | NA           | NA                      |
| Activism2                 | ❌         | NA      | NA          | NA           | NA                      |
| ChangeInRecommendation    | ❌         | NA      | NA          | NA           | NA                      |
| DownRecomm                | ❌         | NA      | NA          | NA           | NA                      |
| EarnSupBig                | ❌         | NA      | NA          | NA           | NA                      |
| EarningsConsistency       | ❌         | NA      | NA          | NA           | NA                      |
| EarningsForecastDisparity | ❌         | NA      | NA          | NA           | NA                      |
| EarningsStreak            | ❌         | NA      | NA          | NA           | NA                      |
| EarningsSurprise          | ❌         | NA      | NA          | NA           | NA                      |
| FEPS                      | ❌         | NA      | NA          | NA           | NA                      |
| FR                        | ❌         | NA      | NA          | NA           | NA                      |
| FirmAgeMom                | ❌         | NA      | NA          | NA           | NA                      |
| ForecastDispersion        | ❌         | NA      | NA          | NA           | NA                      |
| GrAdExp                   | ❌         | NA      | NA          | NA           | NA                      |
| GrLTNOA                   | ❌         | NA      | NA          | NA           | NA                      |
| GrSaleToGrInv             | ❌         | NA      | NA          | NA           | NA                      |
| GrSaleToGrOverhead        | ❌         | NA      | NA          | NA           | NA                      |
| High52                    | ❌         | NA      | NA          | NA           | NA                      |
| IO_ShortInterest          | ❌         | NA      | NA          | NA           | NA                      |
| IndRetBig                 | ❌         | NA      | NA          | NA           | NA                      |
| InvestPPEInv              | ❌         | NA      | NA          | NA           | NA                      |
| NOA                       | ❌         | NA      | NA          | NA           | NA                      |
| NetDebtFinance            | ❌         | NA      | NA          | NA           | NA                      |
| NetEquityFinance          | ❌         | NA      | NA          | NA           | NA                      |
| NetPayoutYield            | ❌         | NA      | NA          | NA           | NA                      |
| NumEarnIncrease           | ❌         | NA      | NA          | NA           | NA                      |
| OPLeverage                | ❌         | NA      | NA          | NA           | NA                      |
| OrgCap                    | ❌         | NA      | NA          | NA           | NA                      |
| PatentsRD                 | ❌         | NA      | NA          | NA           | NA                      |
| PayoutYield               | ❌         | NA      | NA          | NA           | NA                      |
| RevenueSurprise           | ❌         | NA      | NA          | NA           | NA                      |
| ShareIss1Y                | ❌         | NA      | NA          | NA           | NA                      |
| ShareIss5Y                | ❌         | NA      | NA          | NA           | NA                      |
| ShareRepurchase           | ❌         | NA      | NA          | NA           | NA                      |
| ShortInterest             | ❌         | NA      | NA          | NA           | NA                      |
| UpRecomm                  | ❌         | NA      | NA          | NA           | NA                      |
| grcapx                    | ❌         | NA      | NA          | NA           | NA                      |
| grcapx3y                  | ❌         | NA      | NA          | NA           | NA                      |

**Overall**: 20/171 available predictors passed validation
**Python CSVs**: 171/209 predictors have Python implementation

## Detailed Results

### AM

**Status**: ❌ FAILED

**Test Results**:
- Test 1 - Column names: ✅ PASSED
- Test 2 - Superset check: ✅ PASSED
- Test 3 - Precision1 check: ✅ PASSED
- Test 4 - Precision2 check: ❌ FAILED

**Columns**: ['AM']

**Observations**:
- Stata:  3,038,206
- Python: 3,038,208
- Common: 3,038,206

**Precision1**: 0.001% obs with diff >= 1.00e-04 (tolerance: < 0.1%)

**Precision2**: 100th percentile diff = 2.46e-01 (tolerance: < 1.00e-06)

**Feedback**:
- Num observations with diff >= TOL_DIFF_1: 26/3038206 (0.001%)

**Most Recent Bad Observations**:
```
   permno  yyyymm       python        stata      diff
0   23033  202412     0.480255     0.552987 -0.072731
1   23033  202411     1.303550     1.500963 -0.197414
2   23033  202410     1.622966     1.868752 -0.245787
3   23033  202409     1.568126     1.805608 -0.237482
4   23033  202408     0.925244     1.065365 -0.140122
5   23033  202407     0.829768     0.955430 -0.125663
6   23033  202406     0.762962     0.878507 -0.115545
7   51043  201006  2271.095324  2271.095200  0.000124
8   51043  200903  1155.376402  1155.376300  0.000102
9   75162  200902  2111.211042  2111.210900  0.000142
```

**Largest Differences**:
```
   permno  yyyymm        python         stata      diff
0   23033  202410      1.622966      1.868752 -0.245787
1   23033  202409      1.568126      1.805608 -0.237482
2   23033  202411      1.303550      1.500963 -0.197414
3   23033  202408      0.925244      1.065365 -0.140122
4   23033  202407      0.829768      0.955430 -0.125663
5   23033  202406      0.762962      0.878507 -0.115545
6   23033  202412      0.480255      0.552987 -0.072731
7   46084  199002   8839.512298   8839.512700 -0.000402
8   42359  199006  10597.538348  10597.538000  0.000348
9   89045  200811   4178.757001   4178.756800  0.000201
```

---

### AOP

**Status**: ❌ FAILED

**Test Results**:
- Test 1 - Column names: ✅ PASSED
- Test 2 - Superset check: ❌ FAILED (Python missing 2784 Stata observations)
- Test 3 - Precision1 check: ❌ FAILED
- Test 4 - Precision2 check: ❌ FAILED

**Columns**: ['AOP']

**Observations**:
- Stata:  1,244,664
- Python: 1,299,504
- Common: 1,241,880

**Precision1**: 3.156% obs with diff >= 1.00e-04 (tolerance: < 0.1%)

**Precision2**: 100th percentile diff = 2.40e+03 (tolerance: < 1.00e-06)

**Missing Observations Sample**:
```
 index  permno  yyyymm       AOP
     0   10411  199606 33.973907
     1   10411  199607 33.973907
     2   10411  199608 33.973907
     3   10411  199609 33.973907
     4   10411  199610 33.973907
     5   10411  199611 33.973907
     6   10411  199612 33.973907
     7   10411  199701 33.973907
     8   10411  199702 33.973907
     9   10411  199703 33.973907
```

**Feedback**:
- Num observations with diff >= TOL_DIFF_1: 39192/1241880 (3.156%)

**Most Recent Bad Observations**:
```
   permno  yyyymm       python        stata      diff
0   12480  202505    -0.192610    -0.141603 -0.051007
1   12497  202505    40.122021    40.121864  0.000157
2   13410  202505    98.790368    98.790611 -0.000243
3   14452  202505   240.140212   240.140080  0.000132
4   15826  202505   409.201373   409.199550  0.001823
5   15909  202505  6608.902094  6608.899400  0.002694
6   17122  202505  6903.632464  6904.143600 -0.511136
7   17262  202505    60.579496    60.579834 -0.000338
8   19231  202505    -0.015543     0.055677 -0.071220
9   19996  202505   411.877900   411.878970 -0.001070
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
- Test 2 - Superset check: ❌ FAILED (Python missing 16645 Stata observations)
- Test 3 - Precision1 check: ❌ FAILED
- Test 4 - Precision2 check: ❌ FAILED

**Columns**: ['AbnormalAccruals']

**Observations**:
- Stata:  2,570,664
- Python: 2,581,079
- Common: 2,554,019

**Precision1**: 64.273% obs with diff >= 1.00e-04 (tolerance: < 0.1%)

**Precision2**: 100th percentile diff = 3.72e+00 (tolerance: < 1.00e-06)

**Missing Observations Sample**:
```
 index  permno  yyyymm  AbnormalAccruals
     0   10102  197806          0.039469
     1   10102  197807          0.039469
     2   10102  197808          0.039469
     3   10102  197809          0.039469
     4   10102  197810          0.039469
     5   10102  197811          0.039469
     6   10102  197812          0.039469
     7   10102  197901          0.039469
     8   10102  197902          0.039469
     9   10102  197903          0.039469
```

**Feedback**:
- Num observations with diff >= TOL_DIFF_1: 1641539/2554019 (64.273%)

**Most Recent Bad Observations**:
```
   permno  yyyymm    python     stata      diff
0   18136  202609 -0.044470 -0.028342 -0.016129
1   29946  202609  0.108293  0.092957  0.015336
2   82598  202609  0.005841  0.004917  0.000924
3   12366  202608  0.186167  0.146414  0.039753
4   12783  202608  0.034595  0.028171  0.006424
5   13142  202608 -0.125493 -0.145704  0.020211
6   14033  202608  1.354882  1.391868 -0.036986
7   14759  202608  0.022311  0.023689 -0.001378
8   15623  202608 -0.091212 -0.093782  0.002570
9   15651  202608 -0.004074 -0.003788 -0.000287
```

**Largest Differences**:
```
   permno  yyyymm    python    stata      diff
0   77200  200106 -3.701572  0.01571 -3.717283
1   77200  200107 -3.701572  0.01571 -3.717283
2   77200  200108 -3.701572  0.01571 -3.717283
3   77200  200109 -3.701572  0.01571 -3.717283
4   77200  200110 -3.701572  0.01571 -3.717283
5   77200  200111 -3.701572  0.01571 -3.717283
6   77200  200112 -3.701572  0.01571 -3.717283
7   77200  200201 -3.701572  0.01571 -3.717283
8   77200  200202 -3.701572  0.01571 -3.717283
9   77200  200203 -3.701572  0.01571 -3.717283
```

---

### Accruals

**Status**: ❌ FAILED

**Test Results**:
- Test 1 - Column names: ✅ PASSED
- Test 2 - Superset check: ✅ PASSED
- Test 3 - Precision1 check: ✅ PASSED
- Test 4 - Precision2 check: ❌ FAILED

**Columns**: ['Accruals']

**Observations**:
- Stata:  3,259,701
- Python: 3,276,202
- Common: 3,259,701

**Precision1**: 0.017% obs with diff >= 1.00e-04 (tolerance: < 0.1%)

**Precision2**: 100th percentile diff = 5.53e-01 (tolerance: < 1.00e-06)

**Feedback**:
- Num observations with diff >= TOL_DIFF_1: 540/3259701 (0.017%)

**Most Recent Bad Observations**:
```
   permno  yyyymm    python     stata      diff
0   10104  202610 -0.053359 -0.067396  0.014036
1   10104  202609 -0.053359 -0.067396  0.014036
2   20193  202609 -0.028867 -0.036670  0.007803
3   21742  202609 -0.059450 -0.061463  0.002013
4   42585  202609 -0.011005 -0.011232  0.000227
5   60097  202609 -0.024364 -0.026478  0.002114
6   10104  202608 -0.053359 -0.067396  0.014036
7   14888  202608  0.001022  0.000355  0.000666
8   18298  202608 -0.048885 -0.053217  0.004332
9   20193  202608 -0.028867 -0.036670  0.007803
```

**Largest Differences**:
```
   permno  yyyymm   python     stata      diff
0   18405  202506 -4.54592 -5.098427  0.552507
1   18405  202507 -4.54592 -5.098427  0.552507
2   18405  202508 -4.54592 -5.098427  0.552507
3   18405  202509 -4.54592 -5.098427  0.552507
4   18405  202510 -4.54592 -5.098427  0.552507
5   18405  202511 -4.54592 -5.098427  0.552507
6   18405  202512 -4.54592 -5.098427  0.552507
7   18405  202601 -4.54592 -5.098427  0.552507
8   18405  202602 -4.54592 -5.098427  0.552507
9   18405  202603 -4.54592 -5.098427  0.552507
```

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
- Python: 1,511,502
- Common: 220,066

**Precision1**: 0.000% obs with diff >= 1.00e-04 (tolerance: < 0.1%)

**Precision2**: 100th percentile diff = 0.00e+00 (tolerance: < 1.00e-06)

**Feedback**:
- Num observations with diff >= TOL_DIFF_1: 0/220066 (0.000%)

---

### AdExp

**Status**: ❌ FAILED

**Test Results**:
- Test 1 - Column names: ✅ PASSED
- Test 2 - Superset check: ✅ PASSED
- Test 3 - Precision1 check: ✅ PASSED
- Test 4 - Precision2 check: ❌ FAILED

**Columns**: ['AdExp']

**Observations**:
- Stata:  1,049,030
- Python: 1,049,037
- Common: 1,049,030

**Precision1**: 0.000% obs with diff >= 1.00e-04 (tolerance: < 0.1%)

**Precision2**: 100th percentile diff = 3.84e-06 (tolerance: < 1.00e-06)

**Feedback**:
- Num observations with diff >= TOL_DIFF_1: 0/1049030 (0.000%)

---

### AnalystRevision

**Status**: ❌ FAILED

**Test Results**:
- Test 1 - Column names: ✅ PASSED
- Test 2 - Superset check: ❌ FAILED (Python missing 3046 Stata observations)
- Test 3 - Precision1 check: ✅ PASSED
- Test 4 - Precision2 check: ❌ FAILED

**Columns**: ['AnalystRevision']

**Observations**:
- Stata:  1,920,473
- Python: 1,923,490
- Common: 1,917,427

**Precision1**: 0.082% obs with diff >= 1.00e-04 (tolerance: < 0.1%)

**Precision2**: 100th percentile diff = 5.44e+01 (tolerance: < 1.00e-06)

**Missing Observations Sample**:
```
 index  permno  yyyymm  AnalystRevision
     0   11406  199009         1.000000
     1   11406  199010         1.000000
     2   11406  199011         1.000000
     3   11406  199012         1.000000
     4   11406  199101         1.000000
     5   11406  199102         1.000000
     6   11406  199103         1.333333
     7   11406  199104         1.000000
     8   11406  199105         0.750000
     9   11406  199106         1.000000
```

**Feedback**:
- Num observations with diff >= TOL_DIFF_1: 1569/1917427 (0.082%)

**Most Recent Bad Observations**:
```
   permno  yyyymm    python     stata      diff
0   91575  202412  1.025316  1.013393  0.011924
1   27618  202411  1.011765  1.012048 -0.000283
2   91575  202411  0.970516  1.008252 -0.037736
3   27618  202410  1.062500  0.976471  0.086029
4   91575  202410  1.012438  0.985218  0.027220
5   91575  202409  0.990148  1.000000 -0.009852
6   27618  202408  1.142857  1.036585  0.106272
7   91575  202408  1.804444  0.968504  0.835940
8   91575  202407  1.890756  1.000000  0.890756
9   27618  202406  1.000000  1.025000 -0.025000
```

**Largest Differences**:
```
   permno  yyyymm     python      stata       diff
0   91575  201703   1.413333 -53.000000  54.413333
1   77883  199707 -21.222222   1.000000 -22.222222
2   75382  199208  20.000000   0.937500  19.062500
3   63781  200003   1.000000  20.000000 -19.000000
4   63781  201702  19.000000   0.978261  18.021739
5   76110  199103  19.333333   1.444444  17.888889
6   77883  199611  14.692308   0.913044  13.779264
7   76110  199309 -11.000000   1.000000 -12.000000
8   75382  199105  10.000000   1.000000   9.000000
9   77883  199809   1.000000   9.125000  -8.125000
```

---

### AnalystValue

**Status**: ❌ FAILED

**Test Results**:
- Test 1 - Column names: ✅ PASSED
- Test 2 - Superset check: ❌ FAILED (Python missing 2784 Stata observations)
- Test 3 - Precision1 check: ❌ FAILED
- Test 4 - Precision2 check: ❌ FAILED

**Columns**: ['AnalystValue']

**Observations**:
- Stata:  1,244,664
- Python: 1,299,504
- Common: 1,241,880

**Precision1**: 2.662% obs with diff >= 1.00e-04 (tolerance: < 0.1%)

**Precision2**: 100th percentile diff = 1.17e+01 (tolerance: < 1.00e-06)

**Missing Observations Sample**:
```
 index  permno  yyyymm  AnalystValue
     0   10411  199606      4.547985
     1   10411  199607      4.547985
     2   10411  199608      4.547985
     3   10411  199609      4.547985
     4   10411  199610      4.547985
     5   10411  199611      4.547985
     6   10411  199612      4.547985
     7   10411  199701      4.547985
     8   10411  199702      4.547985
     9   10411  199703      4.547985
```

**Feedback**:
- Num observations with diff >= TOL_DIFF_1: 33060/1241880 (2.662%)

**Most Recent Bad Observations**:
```
   permno  yyyymm       python        stata       diff
0   12480  202505     0.792628     0.786408   0.006220
1   19231  202505     0.924282     0.914931   0.009350
2   20338  202505    -0.104549    -0.111456   0.006907
3   21228  202505    -0.187005    -0.186681  -0.000323
4   21519  202505     1.434437     1.452814  -0.018377
5   21783  202505     1.230213     1.028611   0.201602
6   21830  202505     0.053666     0.053769  -0.000103
7   22311  202505     2.383150     2.351018   0.032132
8   22793  202505  3326.578149  3338.297600 -11.719451
9   23033  202505    11.374458     9.866216   1.508243
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

**Status**: ❌ FAILED

**Test Results**:
- Test 1 - Column names: ✅ PASSED
- Test 2 - Superset check: ❌ FAILED (Python missing 83 Stata observations)
- Test 3 - Precision1 check: ❌ FAILED
- Test 4 - Precision2 check: ❌ FAILED

**Columns**: ['AnnouncementReturn']

**Observations**:
- Stata:  2,922,373
- Python: 2,922,354
- Common: 2,922,290

**Precision1**: 0.351% obs with diff >= 1.00e-04 (tolerance: < 0.1%)

**Precision2**: 100th percentile diff = 3.18e-01 (tolerance: < 1.00e-06)

**Missing Observations Sample**:
```
 index  permno  yyyymm  AnnouncementReturn
     0   10543  198809           -0.115678
     1   10543  198810           -0.115678
     2   10543  198811           -0.115678
     3   10543  198812           -0.115678
     4   10543  198901           -0.115678
     5   10986  199007           -0.078410
     6   10986  199008           -0.078410
     7   10986  199009           -0.078410
     8   10986  199010           -0.078410
     9   10986  199011           -0.078410
```

**Feedback**:
- Num observations with diff >= TOL_DIFF_1: 10267/2922290 (0.351%)

**Most Recent Bad Observations**:
```
   permno  yyyymm    python     stata    diff
0   18571  202302  0.119845  0.119945 -0.0001
1   12886  202301 -0.205975 -0.205875 -0.0001
2   14987  202301  0.079512  0.079612 -0.0001
3   18571  202301  0.119845  0.119945 -0.0001
4   21520  202301  0.070402  0.070502 -0.0001
5   59504  202301 -0.028961 -0.028861 -0.0001
6   76221  202301  0.013980  0.014080 -0.0001
7   81046  202301  0.002922  0.003022 -0.0001
8   12886  202212 -0.205975 -0.205875 -0.0001
9   14987  202212  0.079512  0.079612 -0.0001
```

**Largest Differences**:
```
   permno  yyyymm    python     stata      diff
0   12113  200009  0.246096 -0.072393  0.318489
1   12113  200010  0.246096 -0.072393  0.318489
2   50059  199202 -0.093115  0.165428 -0.258543
3   50059  199203 -0.093115  0.165428 -0.258543
4   50059  199204 -0.093115  0.165428 -0.258543
5   83887  199807 -0.349580 -0.095198 -0.254382
6   82551  199711  0.123004 -0.101968  0.224972
7   82551  199712  0.123004 -0.101968  0.224972
8   82551  199710  0.123004 -0.101968  0.224972
9   45911  200202 -0.126567  0.083369 -0.209936
```

---

### AssetGrowth

**Status**: ❌ FAILED

**Test Results**:
- Test 1 - Column names: ✅ PASSED
- Test 2 - Superset check: ✅ PASSED
- Test 3 - Precision1 check: ✅ PASSED
- Test 4 - Precision2 check: ❌ FAILED

**Columns**: ['AssetGrowth']

**Observations**:
- Stata:  3,295,125
- Python: 3,311,751
- Common: 3,295,125

**Precision1**: 0.001% obs with diff >= 1.00e-04 (tolerance: < 0.1%)

**Precision2**: 100th percentile diff = 1.08e-01 (tolerance: < 1.00e-06)

**Feedback**:
- Num observations with diff >= TOL_DIFF_1: 24/3295125 (0.001%)

**Most Recent Bad Observations**:
```
   permno  yyyymm   python   stata     diff
0   23033  202605 -0.17856 -0.2866  0.10804
1   23033  202604 -0.17856 -0.2866  0.10804
2   23033  202603 -0.17856 -0.2866  0.10804
3   23033  202602 -0.17856 -0.2866  0.10804
4   23033  202601 -0.17856 -0.2866  0.10804
5   23033  202512 -0.17856 -0.2866  0.10804
6   23033  202511 -0.17856 -0.2866  0.10804
7   23033  202510 -0.17856 -0.2866  0.10804
8   23033  202509 -0.17856 -0.2866  0.10804
9   23033  202508 -0.17856 -0.2866  0.10804
```

**Largest Differences**:
```
   permno  yyyymm   python   stata     diff
0   23033  202506 -0.17856 -0.2866  0.10804
1   23033  202507 -0.17856 -0.2866  0.10804
2   23033  202508 -0.17856 -0.2866  0.10804
3   23033  202509 -0.17856 -0.2866  0.10804
4   23033  202510 -0.17856 -0.2866  0.10804
5   23033  202511 -0.17856 -0.2866  0.10804
6   23033  202512 -0.17856 -0.2866  0.10804
7   23033  202601 -0.17856 -0.2866  0.10804
8   23033  202602 -0.17856 -0.2866  0.10804
9   23033  202603 -0.17856 -0.2866  0.10804
```

---

### BM

**Status**: ❌ FAILED

**Test Results**:
- Test 1 - Column names: ✅ PASSED
- Test 2 - Superset check: ✅ PASSED
- Test 3 - Precision1 check: ✅ PASSED
- Test 4 - Precision2 check: ❌ FAILED

**Columns**: ['BM']

**Observations**:
- Stata:  2,715,090
- Python: 2,715,252
- Common: 2,715,090

**Precision1**: 0.034% obs with diff >= 1.00e-04 (tolerance: < 0.1%)

**Precision2**: 100th percentile diff = 3.69e+00 (tolerance: < 1.00e-06)

**Feedback**:
- Num observations with diff >= TOL_DIFF_1: 915/2715090 (0.034%)

**Most Recent Bad Observations**:
```
   permno  yyyymm    python     stata      diff
0   14051  202412  1.058469  0.418529  0.639940
1   23033  202412 -0.791014 -0.552329 -0.238685
2   23046  202412 -0.261006 -0.260873 -0.000133
3   14051  202411  1.058469  0.418529  0.639940
4   23033  202411 -0.791014 -0.552329 -0.238685
5   23046  202411 -0.261006 -0.260873 -0.000133
6   14051  202410  1.058469  0.418529  0.639940
7   23033  202410 -0.791014 -0.552329 -0.238685
8   23046  202410 -0.261006 -0.260873 -0.000133
9   14051  202409  1.058469  0.418529  0.639940
```

**Largest Differences**:
```
   permno  yyyymm    python     stata      diff
0   37496  199107  3.293632 -0.394846  3.688478
1   37496  199108  3.293632 -0.394846  3.688478
2   37496  199109  3.293632 -0.394846  3.688478
3   37496  199110  3.293632 -0.394846  3.688478
4   37496  199111  3.293632 -0.394846  3.688478
5   17901  202306 -2.934926  0.574377 -3.509303
6   11039  199106 -5.281017 -2.148211 -3.132806
7   82168  199804 -0.942150 -3.424312  2.482163
8   82168  199805 -0.942150 -3.424312  2.482163
9   87637  199209 -4.944558 -2.609507 -2.335051
```

---

### BMdec

**Status**: ❌ FAILED

**Test Results**:
- Test 1 - Column names: ✅ PASSED
- Test 2 - Superset check: ✅ PASSED
- Test 3 - Precision1 check: ✅ PASSED
- Test 4 - Precision2 check: ❌ FAILED

**Columns**: ['BMdec']

**Observations**:
- Stata:  2,996,716
- Python: 2,998,697
- Common: 2,996,716

**Precision1**: 0.009% obs with diff >= 1.00e-04 (tolerance: < 0.1%)

**Precision2**: 100th percentile diff = 1.22e-01 (tolerance: < 1.00e-06)

**Feedback**:
- Num observations with diff >= TOL_DIFF_1: 259/2996716 (0.009%)

**Most Recent Bad Observations**:
```
   permno  yyyymm       python        stata      diff
0   23033  202412     0.453385     0.575607 -0.122223
1   23033  202411     0.453385     0.575607 -0.122223
2   23033  202410     0.453385     0.575607 -0.122223
3   23033  202409     0.453385     0.575607 -0.122223
4   23033  202408     0.453385     0.575607 -0.122223
5   23033  202407     0.453385     0.575607 -0.122223
6   23033  202406     0.453385     0.575607 -0.122223
7   90432  202311  1524.305553  1524.305700 -0.000147
8   90432  202310  1524.305553  1524.305700 -0.000147
9   90432  202309  1524.305553  1524.305700 -0.000147
```

**Largest Differences**:
```
   permno  yyyymm        python         stata      diff
0   23033  202406      0.453385      0.575607 -0.122223
1   23033  202407      0.453385      0.575607 -0.122223
2   23033  202408      0.453385      0.575607 -0.122223
3   23033  202409      0.453385      0.575607 -0.122223
4   23033  202410      0.453385      0.575607 -0.122223
5   23033  202411      0.453385      0.575607 -0.122223
6   23033  202412      0.453385      0.575607 -0.122223
7   28303  200106  13961.466667  13961.466000  0.000667
8   28303  200107  13961.466667  13961.466000  0.000667
9   87279  201506  13106.937430  13106.938000 -0.000570
```

---

### BPEBM

**Status**: ❌ FAILED

**Test Results**:
- Test 1 - Column names: ✅ PASSED
- Test 2 - Superset check: ✅ PASSED
- Test 3 - Precision1 check: ❌ FAILED
- Test 4 - Precision2 check: ❌ FAILED

**Columns**: ['BPEBM']

**Observations**:
- Stata:  2,924,820
- Python: 2,924,826
- Common: 2,924,820

**Precision1**: 0.268% obs with diff >= 1.00e-04 (tolerance: < 0.1%)

**Precision2**: 100th percentile diff = 4.03e+03 (tolerance: < 1.00e-06)

**Feedback**:
- Num observations with diff >= TOL_DIFF_1: 7845/2924820 (0.268%)

**Most Recent Bad Observations**:
```
   permno  yyyymm      python       stata      diff
0   13188  202412  -91.590240  -91.590820  0.000580
1   15014  202412   -1.251460   -1.274214  0.022754
2   20137  202412   -0.034973   -0.034757 -0.000216
3   22767  202412 -105.047356 -105.047500  0.000144
4   23033  202412   -0.165379   -0.141344 -0.024035
5   23340  202412    0.208067    0.106085  0.101982
6   77182  202412  820.871812  820.819640  0.052172
7   83856  202412  122.127651  122.127460  0.000191
8   84172  202412 -158.697979 -158.698380  0.000401
9   89139  202412   55.573720   55.573433  0.000287
```

**Largest Differences**:
```
   permno  yyyymm         python          stata         diff
0   86685  200408 -467702.638008 -471732.060000  4029.421992
1   46017  199403 -121691.983325 -118542.310000 -3149.673325
2   16063  202307   79268.709273   78957.195000   311.514273
3   17806  198508   46483.047851   46679.918000  -196.870149
4   79322  200912   52984.030015   52893.781000    90.249015
5   62026  198508   68483.587132   68567.227000   -83.639868
6   37161  200701  -28762.704293  -28721.467000   -41.237293
7   50091  197204  -19075.606063  -19043.207000   -32.399063
8   13370  197612   46435.238240   46460.758000   -25.519760
9   23340  202308      24.935795       0.694577    24.241218
```

---

### Beta

**Status**: ❌ FAILED

**Test Results**:
- Test 1 - Column names: ✅ PASSED
- Test 2 - Superset check: ✅ PASSED
- Test 3 - Precision1 check: ❌ FAILED
- Test 4 - Precision2 check: ❌ FAILED

**Columns**: ['Beta']

**Observations**:
- Stata:  4,285,574
- Python: 5,072,338
- Common: 4,285,574

**Precision1**: 99.016% obs with diff >= 1.00e-04 (tolerance: < 0.1%)

**Precision2**: 100th percentile diff = 7.27e+00 (tolerance: < 1.00e-06)

**Feedback**:
- Num observations with diff >= TOL_DIFF_1: 4243391/4285574 (99.016%)

**Most Recent Bad Observations**:
```
   permno  yyyymm    python     stata      diff
0   10026  202412  0.574731  0.578857 -0.004126
1   10028  202412  0.980554  0.935156  0.045397
2   10032  202412  0.772370  0.760410  0.011959
3   10044  202412  1.084690  1.109201 -0.024511
4   10065  202412  0.737840  0.728035  0.009805
5   10066  202412  1.299571  1.215831  0.083739
6   10104  202412  0.603324  0.579425  0.023899
7   10107  202412  0.519840  0.501399  0.018441
8   10113  202412  0.826110  0.824631  0.001478
9   10138  202412  1.141184  1.142964 -0.001780
```

**Largest Differences**:
```
   permno  yyyymm     python      stata      diff
0   92012  200903  14.727441  22.000491 -7.273050
1   13643  201406   3.392522  -2.584796  5.977318
2   13621  201408  -0.638886  -5.888610  5.249724
3   13621  201407  -0.979878  -5.988304  5.008426
4   13643  201408   3.435966  -1.087147  4.523113
5   13643  201407   3.208480  -1.124818  4.333299
6   16067  201801   2.440643   6.633473 -4.192830
7   80471  199605  -0.152592  -4.186435  4.033843
8   80471  199604  -0.460823  -4.390349  3.929526
9   80471  199603  -1.046208  -4.770010  3.723802
```

---

### BetaFP

**Status**: ❌ FAILED

**Test Results**:
- Test 1 - Column names: ✅ PASSED
- Test 2 - Superset check: ❌ FAILED (Python missing 20488 Stata observations)
- Test 3 - Precision1 check: ❌ FAILED
- Test 4 - Precision2 check: ❌ FAILED

**Columns**: ['BetaFP']

**Observations**:
- Stata:  3,794,018
- Python: 3,779,957
- Common: 3,773,530

**Precision1**: 96.651% obs with diff >= 1.00e-04 (tolerance: < 0.1%)

**Precision2**: 100th percentile diff = nan (tolerance: < 1.00e-06)

**Missing Observations Sample**:
```
 index  permno  yyyymm   BetaFP
     0   10051  201903 0.810570
     1   10051  201904 0.802326
     2   10051  201905 0.838970
     3   10051  201906 0.780897
     4   10051  201907 0.803848
     5   10051  201908 0.844066
     6   10051  201909 0.844055
     7   10051  201910 0.906686
     8   10051  201911 0.934303
     9   10051  201912 1.063378
```

**Feedback**:
- Num observations with diff >= TOL_DIFF_1: 3647171/3773530 (96.651%)

**Most Recent Bad Observations**:
```
   permno  yyyymm    python     stata      diff
0   10026  202412  0.831054  0.831751 -0.000698
1   10028  202412  0.785613  0.786336 -0.000723
2   10032  202412  1.375082  1.376459 -0.001376
3   10044  202412  1.125466  1.126132 -0.000666
4   10065  202412  1.040226  1.041356 -0.001131
5   10066  202412  0.366776  0.247929  0.118848
6   10104  202412  1.307977  1.309455 -0.001479
7   10107  202412  1.150874  1.151919 -0.001045
8   10113  202412  1.087929  1.089314 -0.001385
9   10138  202412  1.333543  1.334771 -0.001228
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
- Test 3 - Precision1 check: ❌ FAILED
- Test 4 - Precision2 check: ❌ FAILED

**Columns**: ['BetaLiquidityPS']

**Observations**:
- Stata:  3,423,856
- Python: 4,574,505
- Common: 3,423,856

**Precision1**: 99.222% obs with diff >= 1.00e-04 (tolerance: < 0.1%)

**Precision2**: 100th percentile diff = 6.35e+00 (tolerance: < 1.00e-06)

**Feedback**:
- Num observations with diff >= TOL_DIFF_1: 3397228/3423856 (99.222%)

**Most Recent Bad Observations**:
```
   permno  yyyymm    python     stata      diff
0   10026  202412  0.019552  0.013834  0.005717
1   10028  202412 -0.294992 -0.258921 -0.036071
2   10032  202412  0.140774  0.146161 -0.005386
3   10044  202412  0.356851  0.337279  0.019572
4   10065  202412  0.002233  0.002836 -0.000603
5   10066  202412  0.280660  0.344168 -0.063507
6   10104  202412 -0.050344 -0.041437 -0.008906
7   10107  202412  0.015080  0.021103 -0.006022
8   10113  202412 -0.017947 -0.022844  0.004897
9   10138  202412  0.023165  0.013537  0.009628
```

**Largest Differences**:
```
   permno  yyyymm     python      stata      diff
0   13755  202011 -12.452115 -18.804134  6.352019
1   13755  202101 -13.016154 -19.151345  6.135191
2   13755  202012 -12.366073 -18.474695  6.108622
3   10349  198309  10.920025  15.680155 -4.760130
4   16400  201910 -14.135623 -18.708413  4.572790
5   16400  202002 -13.947204 -18.496625  4.549421
6   13755  202102 -12.151586 -16.677923  4.526337
7   13755  202103 -12.388607 -16.886392  4.497785
8   16400  201911 -14.338342 -18.750074  4.411732
9   16400  201912 -14.449057 -18.754869  4.305813
```

---

### BetaTailRisk

**Status**: ❌ FAILED

**Test Results**:
- Test 1 - Column names: ✅ PASSED
- Test 2 - Superset check: ✅ PASSED
- Test 3 - Precision1 check: ❌ FAILED
- Test 4 - Precision2 check: ❌ FAILED

**Columns**: ['BetaTailRisk']

**Observations**:
- Stata:  2,292,350
- Python: 3,839,453
- Common: 2,292,350

**Precision1**: 99.993% obs with diff >= 1.00e-04 (tolerance: < 0.1%)

**Precision2**: 100th percentile diff = 1.10e+01 (tolerance: < 1.00e-06)

**Feedback**:
- Num observations with diff >= TOL_DIFF_1: 2292198/2292350 (99.993%)

**Most Recent Bad Observations**:
```
   permno  yyyymm    python     stata      diff
0   10026  202412  0.016994  0.324815 -0.307821
1   10028  202412  0.073846 -0.427242  0.501088
2   10032  202412  0.035983  0.523027 -0.487044
3   10044  202412 -0.009575  0.422344 -0.431918
4   10066  202412 -0.092147  0.979996 -1.072143
5   10104  202412  0.036456  0.434910 -0.398454
6   10107  202412  0.051836  0.453598 -0.401762
7   10138  202412  0.024252  0.651162 -0.626910
8   10145  202412  0.028329  0.496783 -0.468454
9   10158  202412  0.057916  0.560077 -0.502161
```

**Largest Differences**:
```
   permno  yyyymm    python      stata       diff
0   79006  200002  0.274322 -10.737284  11.011607
1   79006  200003  0.261645  -8.409476   8.671121
2   15489  202405  0.616246   8.570222  -7.953976
3   15489  202407  0.597969   8.296404  -7.698435
4   15489  202408  0.596744   8.289177  -7.692433
5   15489  202406  0.589828   8.276302  -7.686475
6   15489  202409  0.584055   8.143326  -7.559271
7   15489  202410  0.577615   8.004680  -7.427066
8   15489  202411  0.574300   7.718734  -7.144434
9   15489  202412  0.567009   7.672620  -7.105611
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

**Precision1**: 0.000% obs with diff >= 1.00e-04 (tolerance: < 0.1%)

**Precision2**: 100th percentile diff = 1.00e-07 (tolerance: < 1.00e-06)

**Feedback**:
- Num observations with diff >= TOL_DIFF_1: 0/4481622 (0.000%)

---

### BookLeverage

**Status**: ❌ FAILED

**Test Results**:
- Test 1 - Column names: ✅ PASSED
- Test 2 - Superset check: ✅ PASSED
- Test 3 - Precision1 check: ✅ PASSED
- Test 4 - Precision2 check: ❌ FAILED

**Columns**: ['BookLeverage']

**Observations**:
- Stata:  3,606,159
- Python: 3,607,287
- Common: 3,606,159

**Precision1**: 0.057% obs with diff >= 1.00e-04 (tolerance: < 0.1%)

**Precision2**: 100th percentile diff = 9.91e-01 (tolerance: < 1.00e-06)

**Feedback**:
- Num observations with diff >= TOL_DIFF_1: 2044/3606159 (0.057%)

**Most Recent Bad Observations**:
```
   permno  yyyymm     python      stata      diff
0   10104  202610   7.625045   8.029043 -0.403998
1   10104  202609   7.625045   8.029043 -0.403998
2   42585  202609   2.301512   2.887466 -0.585954
3   10104  202608   7.625045   8.029043 -0.403998
4   42585  202608   2.301512   2.887466 -0.585954
5   86349  202608   3.654331   4.123998 -0.469667
6   86776  202608   1.527045   1.554574 -0.027529
7   89256  202608  15.845768  16.365347 -0.519579
8   10104  202607   7.625045   8.029043 -0.403998
9   42585  202607   2.301512   2.887466 -0.585954
```

**Largest Differences**:
```
   permno  yyyymm        python      stata      diff
0   82812  201306  33972.090909  33973.082 -0.991091
1   82812  201307  33972.090909  33973.082 -0.991091
2   82812  201308  33972.090909  33973.082 -0.991091
3   82812  201309  33972.090909  33973.082 -0.991091
4   82812  201310  33972.090909  33973.082 -0.991091
5   82812  201311  33972.090909  33973.082 -0.991091
6   82812  201312  33972.090909  33973.082 -0.991091
7   82812  201401  33972.090909  33973.082 -0.991091
8   82812  201402  33972.090909  33973.082 -0.991091
9   82812  201403  33972.090909  33973.082 -0.991091
```

---

### BrandInvest

**Status**: ❌ FAILED

**Test Results**:
- Test 1 - Column names: ✅ PASSED
- Test 2 - Superset check: ✅ PASSED
- Test 3 - Precision1 check: ❌ FAILED
- Test 4 - Precision2 check: ❌ FAILED

**Columns**: ['BrandInvest']

**Observations**:
- Stata:  485,304
- Python: 509,472
- Common: 485,304

**Precision1**: 11.275% obs with diff >= 1.00e-04 (tolerance: < 0.1%)

**Precision2**: 100th percentile diff = 6.93e+01 (tolerance: < 1.00e-06)

**Feedback**:
- Num observations with diff >= TOL_DIFF_1: 54720/485304 (11.275%)

**Most Recent Bad Observations**:
```
   permno  yyyymm         python        stata      diff
0   10693  202605    2944.246372    2944.2466 -0.000228
1   11308  202605   55513.836307   55513.8360  0.000307
2   11891  202605   33246.902797   33246.9020  0.000797
3   12449  202605    9815.870853    9815.8711 -0.000247
4   12490  202605   60093.309257   60093.3090  0.000257
5   12886  202605   11923.810262   11923.8110 -0.000738
6   13168  202605    1625.515859    1625.5157  0.000159
7   13315  202605    3393.704131    3393.7039  0.000231
8   13407  202605  104731.952372  104731.9500  0.002372
9   13447  202605   12720.465547   12720.4660 -0.000453
```

**Largest Differences**:
```
   permno  yyyymm     python  stata       diff
0   22158  202306  69.299403    0.0  69.299403
1   22158  202307  69.299403    0.0  69.299403
2   22158  202308  69.299403    0.0  69.299403
3   22158  202309  69.299403    0.0  69.299403
4   22158  202310  69.299403    0.0  69.299403
5   22158  202311  69.299403    0.0  69.299403
6   22158  202312  69.299403    0.0  69.299403
7   22158  202401  69.299403    0.0  69.299403
8   22158  202402  69.299403    0.0  69.299403
9   22158  202403  69.299403    0.0  69.299403
```

---

### CBOperProf

**Status**: ❌ FAILED

**Test Results**:
- Test 1 - Column names: ✅ PASSED
- Test 2 - Superset check: ✅ PASSED
- Test 3 - Precision1 check: ✅ PASSED
- Test 4 - Precision2 check: ❌ FAILED

**Columns**: ['CBOperProf']

**Observations**:
- Stata:  2,283,861
- Python: 2,283,897
- Common: 2,283,861

**Precision1**: 0.013% obs with diff >= 1.00e-04 (tolerance: < 0.1%)

**Precision2**: 100th percentile diff = 4.28e-02 (tolerance: < 1.00e-06)

**Feedback**:
- Num observations with diff >= TOL_DIFF_1: 300/2283861 (0.013%)

**Most Recent Bad Observations**:
```
   permno  yyyymm    python     stata      diff
0   12049  202412  0.020980 -0.001626  0.022606
1   15203  202412  0.036677  0.037948 -0.001270
2   16070  202412 -0.091118 -0.087551 -0.003566
3   18302  202412 -0.880991 -0.871779 -0.009212
4   18368  202412  0.133447  0.134490 -0.001043
5   18643  202412 -0.661646 -0.645055 -0.016590
6   18649  202412  0.120497  0.120906 -0.000409
7   19316  202412 -0.001001 -0.000827 -0.000174
8   20196  202412 -0.015870 -0.023231  0.007361
9   22096  202412  0.148657  0.149272 -0.000615
```

**Largest Differences**:
```
   permno  yyyymm    python     stata      diff
0   90177  202406  0.276960  0.319773 -0.042813
1   90177  202407  0.276960  0.319773 -0.042813
2   90177  202408  0.276960  0.319773 -0.042813
3   90177  202409  0.276960  0.319773 -0.042813
4   90177  202410  0.276960  0.319773 -0.042813
5   90177  202411  0.276960  0.319773 -0.042813
6   90177  202412  0.276960  0.319773 -0.042813
7   11664  202006  0.070004  0.038399  0.031605
8   11664  202007  0.070004  0.038399  0.031605
9   11664  202008  0.070004  0.038399  0.031605
```

---

### CF

**Status**: ❌ FAILED

**Test Results**:
- Test 1 - Column names: ✅ PASSED
- Test 2 - Superset check: ✅ PASSED
- Test 3 - Precision1 check: ✅ PASSED
- Test 4 - Precision2 check: ❌ FAILED

**Columns**: ['CF']

**Observations**:
- Stata:  3,038,206
- Python: 3,053,133
- Common: 3,038,206

**Precision1**: 0.006% obs with diff >= 1.00e-04 (tolerance: < 0.1%)

**Precision2**: 100th percentile diff = 2.33e-01 (tolerance: < 1.00e-06)

**Feedback**:
- Num observations with diff >= TOL_DIFF_1: 185/3038206 (0.006%)

**Most Recent Bad Observations**:
```
   permno  yyyymm    python     stata      diff
0   12373  202412 -0.143072 -0.087034 -0.056038
1   12500  202412  3.658760  3.686649 -0.027889
2   15203  202412  0.140786  0.143626 -0.002840
3   16070  202412 -0.355930 -0.350561 -0.005369
4   18643  202412 -2.251289 -2.214773 -0.036516
5   22096  202412  0.132051  0.130278  0.001773
6   23033  202412 -0.313925 -0.244849 -0.069076
7   82702  202412  0.061280  0.059254  0.002026
8   87471  202412  0.258615  0.257600  0.001015
9   87532  202412 -0.446453 -0.447366  0.000913
```

**Largest Differences**:
```
   permno  yyyymm    python     stata      diff
0   23033  202410 -1.060873 -0.827440 -0.233433
1   23033  202409 -1.025026 -0.799481 -0.225546
2   23033  202411 -0.852082 -0.664591 -0.187491
3   23033  202408 -0.604798 -0.471719 -0.133079
4   22096  202304  0.375524  0.245144  0.130380
5   22096  202303  0.350457  0.228780  0.121677
6   23033  202407 -0.542389 -0.423042 -0.119347
7   23033  202406 -0.498720 -0.388982 -0.109738
8   22096  202305  0.297058  0.193921  0.103137
9   22096  202209  0.252254  0.164673  0.087581
```

---

### CPVolSpread

**Status**: ❌ FAILED

**Test Results**:
- Test 1 - Column names: ✅ PASSED
- Test 2 - Superset check: ❌ FAILED (Python missing 5079 Stata observations)
- Test 3 - Precision1 check: ✅ PASSED
- Test 4 - Precision2 check: ❌ FAILED

**Columns**: ['CPVolSpread']

**Observations**:
- Stata:  684,140
- Python: 682,114
- Common: 679,061

**Precision1**: 0.050% obs with diff >= 1.00e-04 (tolerance: < 0.1%)

**Precision2**: 100th percentile diff = 5.31e-01 (tolerance: < 1.00e-06)

**Missing Observations Sample**:
```
 index  permno  yyyymm  CPVolSpread
     0   10353  199601     0.019172
     1   10353  199602     0.004079
     2   10353  199603     0.026653
     3   10353  199604     0.009082
     4   10353  199605     0.003221
     5   10353  199606     0.014537
     6   10353  199607     0.007193
     7   10353  199608     0.007460
     8   10353  199609    -0.013064
     9   10353  199610     0.004250
```

**Feedback**:
- Num observations with diff >= TOL_DIFF_1: 342/679061 (0.050%)

**Most Recent Bad Observations**:
```
   permno  yyyymm    python     stata      diff
0   21534  202208  0.224561 -0.018411  0.242972
1   19347  202202 -0.065156  0.067700 -0.132856
2   20142  202112  0.254262  0.333837 -0.079575
3   21277  202112  0.567551  0.036920  0.530630
4   20171  202110  0.320672 -0.128619  0.449291
5   20399  202109  0.114003 -0.020055  0.134059
6   19295  202108 -0.117846 -0.383800  0.265954
7   20178  202108 -0.057170  0.015512 -0.072682
8   20310  202108  0.220534 -0.015775  0.236309
9   20136  202106 -0.015650 -0.041612  0.025962
```

**Largest Differences**:
```
   permno  yyyymm    python     stata      diff
0   21277  202112  0.567551  0.036920  0.530630
1   20171  202110  0.320672 -0.128619  0.449291
2   19295  202108 -0.117846 -0.383800  0.265954
3   21534  202208  0.224561 -0.018411  0.242972
4   20310  202108  0.220534 -0.015775  0.236309
5   12473  201406 -0.002726  0.195028 -0.197754
6   42083  200810 -0.053449  0.108287 -0.161736
7   42083  200803 -0.014954  0.134779 -0.149733
8   12473  201702 -0.003259  0.143326 -0.146584
9   20399  202109  0.114003 -0.020055  0.134059
```

---

### Cash

**Status**: ❌ FAILED

**Test Results**:
- Test 1 - Column names: ✅ PASSED
- Test 2 - Superset check: ✅ PASSED
- Test 3 - Precision1 check: ✅ PASSED
- Test 4 - Precision2 check: ❌ FAILED

**Columns**: ['Cash']

**Observations**:
- Stata:  2,096,350
- Python: 2,572,551
- Common: 2,096,350

**Precision1**: 0.062% obs with diff >= 1.00e-04 (tolerance: < 0.1%)

**Precision2**: 100th percentile diff = 6.78e-01 (tolerance: < 1.00e-06)

**Feedback**:
- Num observations with diff >= TOL_DIFF_1: 1304/2096350 (0.062%)

**Most Recent Bad Observations**:
```
   permno  yyyymm    python     stata      diff
0   19018  202412  0.647435  0.642192  0.005243
1   23033  202412  0.466572  0.400684  0.065888
2   23265  202412  0.061508  0.052691  0.008817
3   85272  202412  0.264154  0.259355  0.004799
4   19018  202411  0.647435  0.642192  0.005243
5   23033  202411  0.466572  0.400684  0.065888
6   23265  202411  0.061508  0.052691  0.008817
7   85272  202411  0.264154  0.259355  0.004799
8   19018  202410  0.685832  0.681144  0.004688
9   22771  202410  0.014211  0.006017  0.008194
```

**Largest Differences**:
```
   permno  yyyymm    python     stata      diff
0   87502  200008  0.762129  0.084345  0.677785
1   88785  200406  0.595064  0.079574  0.515490
2   88785  200407  0.595064  0.079574  0.515490
3   22221  202405  0.550878  0.065452  0.485426
4   22221  202406  0.550878  0.065452  0.485426
5   10659  199402  0.448293  0.000000  0.448293
6   10659  199403  0.448293  0.000000  0.448293
7   10659  199404  0.448293  0.000000  0.448293
8   77211  199207  0.036987  0.481465 -0.444478
9   11545  199610  0.146931  0.580267 -0.433336
```

---

### CashProd

**Status**: ❌ FAILED

**Test Results**:
- Test 1 - Column names: ✅ PASSED
- Test 2 - Superset check: ✅ PASSED
- Test 3 - Precision1 check: ❌ FAILED
- Test 4 - Precision2 check: ❌ FAILED

**Columns**: ['CashProd']

**Observations**:
- Stata:  3,002,825
- Python: 3,038,208
- Common: 3,002,825

**Precision1**: 0.174% obs with diff >= 1.00e-04 (tolerance: < 0.1%)

**Precision2**: 100th percentile diff = 2.00e-01 (tolerance: < 1.00e-06)

**Feedback**:
- Num observations with diff >= TOL_DIFF_1: 5236/3002825 (0.174%)

**Most Recent Bad Observations**:
```
   permno  yyyymm         python          stata      diff
0   16738  202412   23114.563625   23114.564000 -0.000375
1   20137  202412       5.918505       5.929099 -0.010594
2   23033  202412       1.402203       1.201785  0.200417
3   24440  202412  -22507.972656  -22507.973000  0.000344
4   27991  202412   -3031.847501   -3031.847400 -0.000101
5   88857  202412 -117887.708740 -117887.710000  0.001260
6   89134  202412   -3147.959310   -3147.959200 -0.000110
7   14137  202411   -3625.865310   -3625.865200 -0.000110
8   16738  202411   29532.214252   29532.215000 -0.000748
9   20137  202411       5.130377       5.139561 -0.009183
```

**Largest Differences**:
```
   permno  yyyymm        python         stata      diff
0   23033  202412  1.402203e+00  1.201785e+00  0.200417
1   23033  202406  4.025395e-01  2.056019e-01  0.196938
2   23033  202407  2.658141e-01  6.935240e-02  0.196462
3   23033  202408  1.046853e-01 -9.121558e-02  0.195901
4   23033  202411 -3.017135e-01 -4.961998e-01  0.194486
5   23033  202409 -4.694144e-01 -6.633170e-01  0.193903
6   23033  202410 -4.973331e-01 -6.911384e-01  0.193805
7   19224  202109  1.441479e+06  1.441479e+06 -0.073828
8   19224  202107  1.608809e+06  1.608809e+06  0.060156
9   19224  202106  1.991461e+06  1.991461e+06 -0.040234
```

---

### ChAssetTurnover

**Status**: ❌ FAILED

**Test Results**:
- Test 1 - Column names: ✅ PASSED
- Test 2 - Superset check: ✅ PASSED
- Test 3 - Precision1 check: ✅ PASSED
- Test 4 - Precision2 check: ❌ FAILED

**Columns**: ['ChAssetTurnover']

**Observations**:
- Stata:  2,503,228
- Python: 2,517,970
- Common: 2,503,228

**Precision1**: 0.088% obs with diff >= 1.00e-04 (tolerance: < 0.1%)

**Precision2**: 100th percentile diff = 1.25e+01 (tolerance: < 1.00e-06)

**Feedback**:
- Num observations with diff >= TOL_DIFF_1: 2193/2503228 (0.088%)

**Most Recent Bad Observations**:
```
   permno  yyyymm    python     stata      diff
0   10104  202610 -0.059191  0.022443 -0.081635
1   10104  202609 -0.059191  0.022443 -0.081635
2   10501  202609 -0.116572 -0.114599 -0.001973
3   20193  202609  0.441993 -0.127634  0.569627
4   21742  202609 -0.419473 -0.395818 -0.023655
5   22620  202609  0.831389  0.570717  0.260671
6   42585  202609 -0.028020  0.001892 -0.029912
7   60097  202609  0.020237  0.029507 -0.009269
8   10104  202608 -0.059191  0.022443 -0.081635
9   10501  202608 -0.116572 -0.114599 -0.001973
```

**Largest Differences**:
```
   permno  yyyymm    python     stata       diff
0   23033  202506 -14.28323 -1.742444 -12.540786
1   23033  202507 -14.28323 -1.742444 -12.540786
2   23033  202508 -14.28323 -1.742444 -12.540786
3   23033  202509 -14.28323 -1.742444 -12.540786
4   23033  202510 -14.28323 -1.742444 -12.540786
5   23033  202511 -14.28323 -1.742444 -12.540786
6   23033  202512 -14.28323 -1.742444 -12.540786
7   23033  202601 -14.28323 -1.742444 -12.540786
8   23033  202602 -14.28323 -1.742444 -12.540786
9   23033  202603 -14.28323 -1.742444 -12.540786
```

---

### ChEQ

**Status**: ❌ FAILED

**Test Results**:
- Test 1 - Column names: ✅ PASSED
- Test 2 - Superset check: ✅ PASSED
- Test 3 - Precision1 check: ✅ PASSED
- Test 4 - Precision2 check: ❌ FAILED

**Columns**: ['ChEQ']

**Observations**:
- Stata:  3,047,458
- Python: 3,060,165
- Common: 3,047,458

**Precision1**: 0.002% obs with diff >= 1.00e-04 (tolerance: < 0.1%)

**Precision2**: 100th percentile diff = 1.66e-01 (tolerance: < 1.00e-06)

**Feedback**:
- Num observations with diff >= TOL_DIFF_1: 60/3047458 (0.002%)

**Most Recent Bad Observations**:
```
   permno  yyyymm    python     stata      diff
0   10104  202610  2.349609  2.409122 -0.059513
1   10104  202609  2.349609  2.409122 -0.059513
2   10104  202608  2.349609  2.409122 -0.059513
3   10104  202607  2.349609  2.409122 -0.059513
4   10104  202606  2.349609  2.409122 -0.059513
5   10104  202605  2.349609  2.409122 -0.059513
6   23033  202605  0.538941  0.424504  0.114437
7   10104  202604  2.349609  2.409122 -0.059513
8   23033  202604  0.538941  0.424504  0.114437
9   10104  202603  2.349609  2.409122 -0.059513
```

**Largest Differences**:
```
   permno  yyyymm    python     stata      diff
0   23033  202406  0.614003  0.779524 -0.165522
1   23033  202407  0.614003  0.779524 -0.165522
2   23033  202408  0.614003  0.779524 -0.165522
3   23033  202409  0.614003  0.779524 -0.165522
4   23033  202410  0.614003  0.779524 -0.165522
5   23033  202411  0.614003  0.779524 -0.165522
6   23033  202412  0.614003  0.779524 -0.165522
7   23033  202501  0.614003  0.779524 -0.165522
8   23033  202502  0.614003  0.779524 -0.165522
9   23033  202503  0.614003  0.779524 -0.165522
```

---

### ChForecastAccrual

**Status**: ❌ FAILED

**Test Results**:
- Test 1 - Column names: ✅ PASSED
- Test 2 - Superset check: ✅ PASSED
- Test 3 - Precision1 check: ❌ FAILED
- Test 4 - Precision2 check: ❌ FAILED

**Columns**: ['ChForecastAccrual']

**Observations**:
- Stata:  628,022
- Python: 2,222,361
- Common: 628,022

**Precision1**: 0.118% obs with diff >= 1.00e-04 (tolerance: < 0.1%)

**Precision2**: 100th percentile diff = 1.00e+00 (tolerance: < 1.00e-06)

**Feedback**:
- Num observations with diff >= TOL_DIFF_1: 741/628022 (0.118%)

**Most Recent Bad Observations**:
```
   permno  yyyymm  python  stata  diff
0   91575  202412     0.0      1  -1.0
1   69032  202411     0.0      1  -1.0
2   69032  202410     0.0      1  -1.0
3   69032  202408     0.0      1  -1.0
4   69032  202407     0.0      1  -1.0
5   21889  202406     1.0      0   1.0
6   21186  202405     0.0      1  -1.0
7   69032  202405     0.0      1  -1.0
8   91575  202405     0.0      1  -1.0
9   69032  202404     0.0      1  -1.0
```

**Largest Differences**:
```
   permno  yyyymm  python  stata  diff
0   11406  199508     0.0      1  -1.0
1   11406  199509     0.0      1  -1.0
2   11406  199605     0.0      1  -1.0
3   11406  199709     0.0      1  -1.0
4   12473  201111     1.0      0   1.0
5   12473  201212     1.0      0   1.0
6   12473  201308     1.0      0   1.0
7   12473  201311     1.0      0   1.0
8   12473  201404     0.0      1  -1.0
9   12473  201405     0.0      1  -1.0
```

---

### ChInv

**Status**: ❌ FAILED

**Test Results**:
- Test 1 - Column names: ✅ PASSED
- Test 2 - Superset check: ✅ PASSED
- Test 3 - Precision1 check: ✅ PASSED
- Test 4 - Precision2 check: ❌ FAILED

**Columns**: ['ChInv']

**Observations**:
- Stata:  3,295,155
- Python: 3,311,811
- Common: 3,295,155

**Precision1**: 0.002% obs with diff >= 1.00e-04 (tolerance: < 0.1%)

**Precision2**: 100th percentile diff = 1.98e-02 (tolerance: < 1.00e-06)

**Feedback**:
- Num observations with diff >= TOL_DIFF_1: 60/3295155 (0.002%)

**Most Recent Bad Observations**:
```
   permno  yyyymm    python     stata      diff
0   10104  202610 -0.000200 -0.002159  0.001959
1   10104  202609 -0.000200 -0.002159  0.001959
2   10104  202608 -0.000200 -0.002159  0.001959
3   14888  202608 -0.003745 -0.014303  0.010558
4   86349  202608 -0.001626 -0.021423  0.019798
5   10104  202607 -0.000200 -0.002159  0.001959
6   14888  202607 -0.003745 -0.014303  0.010558
7   86349  202607 -0.001626 -0.021423  0.019798
8   10104  202606 -0.000200 -0.002159  0.001959
9   14888  202606 -0.003745 -0.014303  0.010558
```

**Largest Differences**:
```
   permno  yyyymm    python     stata      diff
0   86349  202509 -0.001626 -0.021423  0.019798
1   86349  202510 -0.001626 -0.021423  0.019798
2   86349  202511 -0.001626 -0.021423  0.019798
3   86349  202512 -0.001626 -0.021423  0.019798
4   86349  202601 -0.001626 -0.021423  0.019798
5   86349  202602 -0.001626 -0.021423  0.019798
6   86349  202603 -0.001626 -0.021423  0.019798
7   86349  202604 -0.001626 -0.021423  0.019798
8   86349  202605 -0.001626 -0.021423  0.019798
9   86349  202606 -0.001626 -0.021423  0.019798
```

---

### ChInvIA

**Status**: ❌ FAILED

**Test Results**:
- Test 1 - Column names: ✅ PASSED
- Test 2 - Superset check: ✅ PASSED
- Test 3 - Precision1 check: ❌ FAILED
- Test 4 - Precision2 check: ❌ FAILED

**Columns**: ['ChInvIA']

**Observations**:
- Stata:  2,678,515
- Python: 2,678,515
- Common: 2,678,515

**Precision1**: 0.583% obs with diff >= 1.00e-04 (tolerance: < 0.1%)

**Precision2**: 100th percentile diff = 1.74e+09 (tolerance: < 1.00e-06)

**Feedback**:
- Num observations with diff >= TOL_DIFF_1: 15628/2678515 (0.583%)

**Most Recent Bad Observations**:
```
   permno  yyyymm    python     stata      diff
0   12082  202412 -0.505779 -0.550892  0.045113
1   12084  202412 -0.735565 -0.780678  0.045113
2   12350  202412 -0.371068 -0.416181  0.045113
3   12360  202412 -0.841232 -0.886345  0.045113
4   12363  202412 -1.071761 -1.116874  0.045113
5   12373  202412 -2.855479 -1.962170 -0.893309
6   12397  202412 -1.240702 -1.285815  0.045113
7   12400  202412 -0.077571 -0.122683  0.045113
8   12411  202412 -0.094887 -0.140000  0.045113
9   12477  202412 -1.817053 -1.861719  0.044665
```

**Largest Differences**:
```
   permno  yyyymm        python         stata          diff
0   25048  196904  2.194466e+16  2.194466e+16 -1.738786e+09
1   25048  196806  2.193833e+16  2.193833e+16 -1.102314e+09
2   25048  196807  2.193833e+16  2.193833e+16 -1.102314e+09
3   25048  196808  2.193833e+16  2.193833e+16 -1.102314e+09
4   25048  196809  2.194259e+16  2.194259e+16  7.669865e+08
5   25048  196810  2.194259e+16  2.194259e+16  7.669865e+08
6   25048  196811  2.194259e+16  2.194259e+16  7.669865e+08
7   25048  196812  2.194259e+16  2.194259e+16  7.669865e+08
8   25048  196901  2.194259e+16  2.194259e+16  7.669865e+08
9   25048  196902  2.194259e+16  2.194259e+16  7.669865e+08
```

---

### ChNAnalyst

**Status**: ❌ FAILED

**Test Results**:
- Test 1 - Column names: ✅ PASSED
- Test 2 - Superset check: ❌ FAILED (Python missing 232 Stata observations)
- Test 3 - Precision1 check: ✅ PASSED
- Test 4 - Precision2 check: ❌ FAILED

**Columns**: ['ChNAnalyst']

**Observations**:
- Stata:  210,988
- Python: 210,931
- Common: 210,756

**Precision1**: 0.007% obs with diff >= 1.00e-04 (tolerance: < 0.1%)

**Precision2**: 100th percentile diff = 1.00e+00 (tolerance: < 1.00e-06)

**Missing Observations Sample**:
```
 index  permno  yyyymm  ChNAnalyst
     0   11406  199011           0
     1   11406  199012           0
     2   11406  199101           0
     3   11406  199108           0
     4   11406  199110           0
     5   12265  199002           0
     6   16249  200911           0
     7   16249  200912           0
     8   16249  201001           0
     9   16249  201002           0
```

**Feedback**:
- Num observations with diff >= TOL_DIFF_1: 14/210756 (0.007%)

**Most Recent Bad Observations**:
```
   permno  yyyymm  python  stata  diff
0   63781  202004     0.0      1  -1.0
1   63781  202003     0.0      1  -1.0
2   63781  202001     1.0      0   1.0
3   77883  199811     0.0      1  -1.0
4   77883  199810     0.0      1  -1.0
5   77883  199809     0.0      1  -1.0
6   77883  199808     0.0      1  -1.0
7   63781  199301     1.0      0   1.0
8   63781  199207     0.0      1  -1.0
9   63781  199206     0.0      1  -1.0
```

**Largest Differences**:
```
   permno  yyyymm  python  stata  diff
0   63781  199111     0.0      1  -1.0
1   63781  199201     1.0      0   1.0
2   63781  199202     1.0      0   1.0
3   63781  199203     1.0      0   1.0
4   63781  199206     0.0      1  -1.0
5   63781  199207     0.0      1  -1.0
6   63781  199301     1.0      0   1.0
7   63781  202001     1.0      0   1.0
8   63781  202003     0.0      1  -1.0
9   63781  202004     0.0      1  -1.0
```

---

### ChNNCOA

**Status**: ❌ FAILED

**Test Results**:
- Test 1 - Column names: ✅ PASSED
- Test 2 - Superset check: ✅ PASSED
- Test 3 - Precision1 check: ✅ PASSED
- Test 4 - Precision2 check: ❌ FAILED

**Columns**: ['ChNNCOA']

**Observations**:
- Stata:  3,246,170
- Python: 3,262,618
- Common: 3,246,170

**Precision1**: 0.012% obs with diff >= 1.00e-04 (tolerance: < 0.1%)

**Precision2**: 100th percentile diff = 7.53e-01 (tolerance: < 1.00e-06)

**Feedback**:
- Num observations with diff >= TOL_DIFF_1: 396/3246170 (0.012%)

**Most Recent Bad Observations**:
```
   permno  yyyymm    python     stata      diff
0   10104  202610  0.051883  0.035424  0.016459
1   10104  202609  0.051883  0.035424  0.016459
2   21742  202609  0.062380  0.060596  0.001784
3   42585  202609 -0.035784 -0.043419  0.007635
4   60097  202609 -0.011947 -0.013496  0.001549
5   10104  202608  0.051883  0.035424  0.016459
6   18298  202608 -0.006720 -0.046958  0.040238
7   21742  202608  0.062380  0.060596  0.001784
8   42585  202608 -0.035784 -0.043419  0.007635
9   51131  202608  0.037610 -0.023132  0.060742
```

**Largest Differences**:
```
   permno  yyyymm    python     stata     diff
0   12373  202406 -0.749837  0.003303 -0.75314
1   12373  202407 -0.749837  0.003303 -0.75314
2   12373  202408 -0.749837  0.003303 -0.75314
3   12373  202409 -0.749837  0.003303 -0.75314
4   12373  202410 -0.749837  0.003303 -0.75314
5   12373  202411 -0.749837  0.003303 -0.75314
6   12373  202412 -0.749837  0.003303 -0.75314
7   12373  202501 -0.749837  0.003303 -0.75314
8   12373  202502 -0.749837  0.003303 -0.75314
9   12373  202503 -0.749837  0.003303 -0.75314
```

---

### ChNWC

**Status**: ❌ FAILED

**Test Results**:
- Test 1 - Column names: ✅ PASSED
- Test 2 - Superset check: ✅ PASSED
- Test 3 - Precision1 check: ✅ PASSED
- Test 4 - Precision2 check: ❌ FAILED

**Columns**: ['ChNWC']

**Observations**:
- Stata:  3,259,599
- Python: 3,275,986
- Common: 3,259,599

**Precision1**: 0.007% obs with diff >= 1.00e-04 (tolerance: < 0.1%)

**Precision2**: 100th percentile diff = 4.75e-01 (tolerance: < 1.00e-06)

**Feedback**:
- Num observations with diff >= TOL_DIFF_1: 228/3259599 (0.007%)

**Most Recent Bad Observations**:
```
   permno  yyyymm    python     stata      diff
0   10104  202610 -0.003411 -0.016306  0.012895
1   10104  202609 -0.003411 -0.016306  0.012895
2   20193  202609 -0.019291 -0.023965  0.004674
3   21742  202609  0.006354  0.004570  0.001784
4   42585  202609  0.014991  0.014803  0.000188
5   60097  202609  0.005853  0.003759  0.002094
6   10104  202608 -0.003411 -0.016306  0.012895
7   14888  202608  0.023202  0.021016  0.002186
8   18298  202608  0.002414 -0.002109  0.004523
9   20193  202608 -0.019291 -0.023965  0.004674
```

**Largest Differences**:
```
   permno  yyyymm    python     stata      diff
0   18405  202506 -3.583221 -4.058363  0.475142
1   18405  202507 -3.583221 -4.058363  0.475142
2   18405  202508 -3.583221 -4.058363  0.475142
3   18405  202509 -3.583221 -4.058363  0.475142
4   18405  202510 -3.583221 -4.058363  0.475142
5   18405  202511 -3.583221 -4.058363  0.475142
6   18405  202512 -3.583221 -4.058363  0.475142
7   18405  202601 -3.583221 -4.058363  0.475142
8   18405  202602 -3.583221 -4.058363  0.475142
9   18405  202603 -3.583221 -4.058363  0.475142
```

---

### ChTax

**Status**: ❌ FAILED

**Test Results**:
- Test 1 - Column names: ✅ PASSED
- Test 2 - Superset check: ❌ FAILED (Python missing 59 Stata observations)
- Test 3 - Precision1 check: ✅ PASSED
- Test 4 - Precision2 check: ❌ FAILED

**Columns**: ['ChTax']

**Observations**:
- Stata:  2,827,726
- Python: 3,146,764
- Common: 2,827,667

**Precision1**: 0.013% obs with diff >= 1.00e-04 (tolerance: < 0.1%)

**Precision2**: 100th percentile diff = 6.85e-01 (tolerance: < 1.00e-06)

**Missing Observations Sample**:
```
 index  permno  yyyymm     ChTax
     0   12837  198004 -0.001686
     1   12837  198005 -0.001686
     2   12837  198104  0.017560
     3   12837  198105  0.017560
     4   16536  202103 -0.009110
     5   16536  202104 -0.009110
     6   16536  202105 -0.009110
     7   17559  198612 -0.002798
     8   17559  198701 -0.002798
     9   17559  198702 -0.002798
```

**Feedback**:
- Num observations with diff >= TOL_DIFF_1: 367/2827667 (0.013%)

**Most Recent Bad Observations**:
```
   permno  yyyymm    python     stata      diff
0   16975  202508  0.000000 -0.000821  0.000821
1   23033  202508 -0.005075 -0.004407 -0.000667
2   23265  202508 -0.024632  0.000000 -0.024632
3   14296  202507  0.003940 -0.004770  0.008710
4   16975  202507  0.000000 -0.000821  0.000821
5   21788  202507  0.007887  0.035246 -0.027360
6   23033  202507 -0.005075 -0.004407 -0.000667
7   23265  202507 -0.024632  0.000000 -0.024632
8   82745  202507  0.010807  0.001679  0.009128
9   85399  202507  0.018543  0.003298  0.015245
```

**Largest Differences**:
```
   permno  yyyymm    python     stata      diff
0   23193  202506  0.000000  0.685459 -0.685459
1   38295  201203  0.029513  0.258727 -0.229214
2   38295  201204  0.029513  0.258727 -0.229214
3   38295  201205  0.029513  0.258727 -0.229214
4   38295  201103  0.206277 -0.007358  0.213635
5   38295  201104  0.206277 -0.007358  0.213635
6   38295  201105  0.206277 -0.007358  0.213635
7   83887  199907 -0.076393  0.019724 -0.096118
8   83887  199908 -0.076393  0.019724 -0.096118
9   92052  202507  0.048724 -0.028332  0.077055
```

---

### CitationsRD

**Status**: ❌ FAILED

**Test Results**:
- Test 1 - Column names: ✅ PASSED
- Test 2 - Superset check: ✅ PASSED
- Test 3 - Precision1 check: ✅ PASSED
- Test 4 - Precision2 check: ❌ FAILED

**Columns**: ['CitationsRD']

**Observations**:
- Stata:  645,360
- Python: 701,940
- Common: 645,360

**Precision1**: 0.002% obs with diff >= 1.00e-04 (tolerance: < 0.1%)

**Precision2**: 100th percentile diff = 1.00e+00 (tolerance: < 1.00e-06)

**Feedback**:
- Num observations with diff >= TOL_DIFF_1: 12/645360 (0.002%)

**Most Recent Bad Observations**:
```
   permno  yyyymm  python  stata  diff
0   84136  200105     0.0      1  -1.0
1   84136  200104     0.0      1  -1.0
2   84136  200103     0.0      1  -1.0
3   84136  200102     0.0      1  -1.0
4   84136  200101     0.0      1  -1.0
5   84136  200012     0.0      1  -1.0
6   84136  200011     0.0      1  -1.0
7   84136  200010     0.0      1  -1.0
8   84136  200009     0.0      1  -1.0
9   84136  200008     0.0      1  -1.0
```

**Largest Differences**:
```
   permno  yyyymm  python  stata  diff
0   84136  200006     0.0      1  -1.0
1   84136  200007     0.0      1  -1.0
2   84136  200008     0.0      1  -1.0
3   84136  200009     0.0      1  -1.0
4   84136  200010     0.0      1  -1.0
5   84136  200011     0.0      1  -1.0
6   84136  200012     0.0      1  -1.0
7   84136  200101     0.0      1  -1.0
8   84136  200102     0.0      1  -1.0
9   84136  200103     0.0      1  -1.0
```

---

### CompEquIss

**Status**: ❌ FAILED

**Test Results**:
- Test 1 - Column names: ✅ PASSED
- Test 2 - Superset check: ✅ PASSED
- Test 3 - Precision1 check: ❌ FAILED
- Test 4 - Precision2 check: ❌ FAILED

**Columns**: ['CompEquIss']

**Observations**:
- Stata:  2,172,395
- Python: 4,043,273
- Common: 2,172,395

**Precision1**: 99.881% obs with diff >= 1.00e-04 (tolerance: < 0.1%)

**Precision2**: 100th percentile diff = 1.96e+03 (tolerance: < 1.00e-06)

**Feedback**:
- Num observations with diff >= TOL_DIFF_1: 2169816/2172395 (99.881%)

**Most Recent Bad Observations**:
```
   permno  yyyymm    python     stata      diff
0   10026  202412 -0.142015 -0.061804 -0.080211
1   10032  202412  0.633364 -0.400428  1.033791
2   10044  202412 -1.098442 -0.365838 -0.732604
3   10104  202412  1.008915 -1.387315  2.396229
4   10107  202412  0.959713 -0.835437  1.795150
5   10138  202412 -0.131627 -0.259832  0.128205
6   10145  202412  0.149622 -0.263066  0.412688
7   10158  202412  0.464821  0.123109  0.341712
8   10200  202412  0.515279 -0.040833  0.556112
9   10220  202412  0.543835 -0.374860  0.918696
```

**Largest Differences**:
```
   permno  yyyymm    python       stata         diff
0   69681  200002  7.333129 -1948.37740  1955.710529
1   69681  200003  7.054681 -1473.09190  1480.146581
2   69681  200004  6.438723  -792.56262   799.001343
3   69681  200006  6.340743  -717.99396   724.334703
4   69681  200001  6.238836  -647.82153   654.060366
5   69681  200005  5.950148  -483.85089   489.801038
6   80114  199904  6.372611  -450.23285   456.605461
7   77103  200002  6.568435  -341.93201   348.500445
8   69681  199912  5.567645  -328.23318   333.800825
9   80114  199906  6.011644  -311.94040   317.952044
```

---

### CompositeDebtIssuance

**Status**: ❌ FAILED

**Test Results**:
- Test 1 - Column names: ✅ PASSED
- Test 2 - Superset check: ✅ PASSED
- Test 3 - Precision1 check: ✅ PASSED
- Test 4 - Precision2 check: ❌ FAILED

**Columns**: ['CompositeDebtIssuance']

**Observations**:
- Stata:  1,898,755
- Python: 2,157,897
- Common: 1,898,755

**Precision1**: 0.008% obs with diff >= 1.00e-04 (tolerance: < 0.1%)

**Precision2**: 100th percentile diff = 6.53e-01 (tolerance: < 1.00e-06)

**Feedback**:
- Num observations with diff >= TOL_DIFF_1: 144/1898755 (0.008%)

**Most Recent Bad Observations**:
```
   permno  yyyymm    python     stata      diff
0   10104  202610  0.391184  0.345455  0.045728
1   10104  202609  0.391184  0.345455  0.045728
2   21742  202609  0.744597  0.739633  0.004964
3   42585  202609  0.300614  0.283298  0.017316
4   60097  202609  0.140528  0.102306  0.038222
5   10104  202608  0.391184  0.345455  0.045728
6   21742  202608  0.744597  0.739633  0.004964
7   42585  202608  0.300614  0.283298  0.017316
8   60097  202608  0.140528  0.102306  0.038222
9   86349  202608 -0.038588 -0.079037  0.040448
```

**Largest Differences**:
```
   permno  yyyymm    python     stata      diff
0   13930  202506  0.654838  1.307349 -0.652512
1   13930  202507  0.654838  1.307349 -0.652512
2   13930  202508  0.654838  1.307349 -0.652512
3   13930  202509  0.654838  1.307349 -0.652512
4   13930  202510  0.654838  1.307349 -0.652512
5   13930  202511  0.654838  1.307349 -0.652512
6   13930  202512  0.654838  1.307349 -0.652512
7   13930  202601  0.654838  1.307349 -0.652512
8   13930  202602  0.654838  1.307349 -0.652512
9   13930  202603  0.654838  1.307349 -0.652512
```

---

### ConsRecomm

**Status**: ❌ FAILED

**Test Results**:
- Test 1 - Column names: ✅ PASSED
- Test 2 - Superset check: ❌ FAILED (Python missing 303 Stata observations)
- Test 3 - Precision1 check: ✅ PASSED
- Test 4 - Precision2 check: ❌ FAILED

**Columns**: ['ConsRecomm']

**Observations**:
- Stata:  134,102
- Python: 372,799
- Common: 133,799

**Precision1**: 0.011% obs with diff >= 1.00e-04 (tolerance: < 0.1%)

**Precision2**: 100th percentile diff = 1.00e+00 (tolerance: < 1.00e-06)

**Missing Observations Sample**:
```
 index  permno  yyyymm  ConsRecomm
     0   11406  199311           0
     1   11406  199412           0
     2   11406  199606           1
     3   11406  199609           0
     4   11406  199701           1
     5   12473  201111           1
     6   12473  201204           0
     7   12473  201304           0
     8   12473  201309           0
     9   12473  201504           0
```

**Feedback**:
- Num observations with diff >= TOL_DIFF_1: 15/133799 (0.011%)

**Most Recent Bad Observations**:
```
   permno  yyyymm  python  stata  diff
0   91575  202307     0.0      1  -1.0
1   12473  201704     1.0      0   1.0
2   91575  201609     1.0      0   1.0
3   63781  201605     1.0      0   1.0
4   63781  201507     1.0      0   1.0
5   12473  201505     0.0      1  -1.0
6   63781  201410     1.0      0   1.0
7   21186  201206     1.0      0   1.0
8   63781  200912     1.0      0   1.0
9   63781  200411     0.0      1  -1.0
```

**Largest Differences**:
```
   permno  yyyymm  python  stata  diff
0   12473  201505     0.0      1  -1.0
1   12473  201704     1.0      0   1.0
2   21186  199404     1.0      0   1.0
3   21186  201206     1.0      0   1.0
4   51633  199403     0.0      1  -1.0
5   51633  199408     0.0      1  -1.0
6   51633  199608     0.0      1  -1.0
7   63781  200411     0.0      1  -1.0
8   63781  200912     1.0      0   1.0
9   63781  201410     1.0      0   1.0
```

---

### ConvDebt

**Status**: ❌ FAILED

**Test Results**:
- Test 1 - Column names: ✅ PASSED
- Test 2 - Superset check: ✅ PASSED
- Test 3 - Precision1 check: ✅ PASSED
- Test 4 - Precision2 check: ❌ FAILED

**Columns**: ['ConvDebt']

**Observations**:
- Stata:  3,624,363
- Python: 3,625,491
- Common: 3,624,363

**Precision1**: 0.001% obs with diff >= 1.00e-04 (tolerance: < 0.1%)

**Precision2**: 100th percentile diff = 1.00e+00 (tolerance: < 1.00e-06)

**Feedback**:
- Num observations with diff >= TOL_DIFF_1: 24/3624363 (0.001%)

**Most Recent Bad Observations**:
```
   permno  yyyymm  python  stata  diff
0   14888  202608       1      0     1
1   14888  202607       1      0     1
2   14888  202606       1      0     1
3   14888  202605       1      0     1
4   88807  202605       0      1    -1
5   14888  202604       1      0     1
6   88807  202604       0      1    -1
7   14888  202603       1      0     1
8   88807  202603       0      1    -1
9   14888  202602       1      0     1
```

**Largest Differences**:
```
   permno  yyyymm  python  stata  diff
0   14888  202509       1      0     1
1   14888  202510       1      0     1
2   14888  202511       1      0     1
3   14888  202512       1      0     1
4   14888  202601       1      0     1
5   14888  202602       1      0     1
6   14888  202603       1      0     1
7   14888  202604       1      0     1
8   14888  202605       1      0     1
9   14888  202606       1      0     1
```

---

### CoskewACX

**Status**: ❌ FAILED

**Test Results**:
- Test 1 - Column names: ✅ PASSED
- Test 2 - Superset check: ✅ PASSED
- Test 3 - Precision1 check: ❌ FAILED
- Test 4 - Precision2 check: ❌ FAILED

**Columns**: ['CoskewACX']

**Observations**:
- Stata:  4,179,145
- Python: 4,179,145
- Common: 4,179,145

**Precision1**: 5.381% obs with diff >= 1.00e-04 (tolerance: < 0.1%)

**Precision2**: 100th percentile diff = 4.72e-03 (tolerance: < 1.00e-06)

**Feedback**:
- Num observations with diff >= TOL_DIFF_1: 224890/4179145 (5.381%)

**Most Recent Bad Observations**:
```
   permno  yyyymm    python     stata      diff
0   10158  202306  0.183443  0.183342  0.000101
1   10397  202306  0.123795  0.123659  0.000136
2   10781  202306  0.175453  0.175576 -0.000123
3   10933  202306  0.373697  0.373817 -0.000121
4   11018  202306  0.174025  0.174125 -0.000100
5   11547  202306  0.188006  0.188154 -0.000148
6   11748  202306  0.037010  0.037117 -0.000107
7   11955  202306  0.089979  0.089859  0.000120
8   12308  202306  0.122692  0.122931 -0.000239
9   12338  202306  0.123348  0.123230  0.000118
```

**Largest Differences**:
```
   permno  yyyymm    python     stata      diff
0   77259  202002  1.302187  1.297471  0.004716
1   75336  202002 -1.280440 -1.275764 -0.004677
2   12451  202002  0.919600  0.915094  0.004506
3   91801  202002 -1.220347 -1.216037 -0.004310
4   90400  202002 -1.043684 -1.039521 -0.004163
5   72611  202002  0.774908  0.770880  0.004028
6   18207  202002 -1.011072 -1.007070 -0.004002
7   87832  202002  1.331384  1.327384  0.004000
8   79265  202002 -1.382725 -1.378762 -0.003963
9   93325  202002 -0.915231 -0.911357 -0.003874
```

---

### Coskewness

**Status**: ❌ FAILED

**Test Results**:
- Test 1 - Column names: ✅ PASSED
- Test 2 - Superset check: ❌ FAILED (Python missing 395931 Stata observations)
- Test 3 - Precision1 check: ❌ FAILED
- Test 4 - Precision2 check: ❌ FAILED

**Columns**: ['Coskewness']

**Observations**:
- Stata:  4,609,158
- Python: 4,702,412
- Common: 4,213,227

**Precision1**: 99.983% obs with diff >= 1.00e-04 (tolerance: < 0.1%)

**Precision2**: 100th percentile diff = 8.65e+00 (tolerance: < 1.00e-06)

**Missing Observations Sample**:
```
 index  permno  yyyymm  Coskewness
     0   10000  198701   -0.080541
     1   10000  198702   -0.115902
     2   10000  198703   -0.027634
     3   10000  198704   -0.055297
     4   10000  198705   -0.086010
     5   10000  198706   -0.081288
     6   10001  201610   -0.023566
     7   10001  201611   -0.018342
     8   10001  201612   -0.010124
     9   10001  201701   -0.011009
```

**Feedback**:
- Num observations with diff >= TOL_DIFF_1: 4212517/4213227 (99.983%)

**Most Recent Bad Observations**:
```
   permno  yyyymm    python     stata      diff
0   10026  202401 -0.281231 -0.352961  0.071730
1   10028  202401  0.150770  0.192499 -0.041729
2   10032  202401  0.157133 -0.264077  0.421210
3   10044  202401  0.166441 -0.194824  0.361266
4   10065  202401 -0.428818 -0.293021 -0.135798
5   10066  202401 -0.008205  0.162496 -0.170701
6   10104  202401 -0.668330 -0.175856 -0.492473
7   10107  202401 -0.381137 -0.297508 -0.083628
8   10113  202401  0.011056 -0.360982  0.372038
9   10138  202401 -0.271320 -0.362331  0.091011
```

**Largest Differences**:
```
   permno  yyyymm    python     stata      diff
0   43167  199310 -8.866053 -0.218651 -8.647402
1   77865  200311 -8.301243 -0.043189 -8.258055
2   83704  200311  7.531086 -0.101360  7.632446
3   84185  200311  7.560394 -0.013554  7.573948
4   43167  199311 -7.413536 -0.229222 -7.184314
5   77865  200312 -6.335477 -0.037056 -6.298422
6   12045  198211 -6.530525 -0.307492 -6.223033
7   84185  200312  6.212200  0.000967  6.211233
8   10772  200208 -6.104407 -0.149531 -5.954875
9   84321  200311 -5.613792  0.054930 -5.668722
```

---

### CredRatDG

**Status**: ❌ FAILED

**Test Results**:
- Test 1 - Column names: ✅ PASSED
- Test 2 - Superset check: ✅ PASSED
- Test 3 - Precision1 check: ❌ FAILED
- Test 4 - Precision2 check: ❌ FAILED

**Columns**: ['CredRatDG']

**Observations**:
- Stata:  2,559,713
- Python: 2,559,715
- Common: 2,559,713

**Precision1**: 0.941% obs with diff >= 1.00e-04 (tolerance: < 0.1%)

**Precision2**: 100th percentile diff = 1.00e+00 (tolerance: < 1.00e-06)

**Feedback**:
- Num observations with diff >= TOL_DIFF_1: 24086/2559713 (0.941%)

**Most Recent Bad Observations**:
```
   permno  yyyymm  python  stata  diff
0   11990  202412     0.0      1  -1.0
1   13103  202412     0.0      1  -1.0
2   14328  202412     0.0      1  -1.0
3   15395  202412     0.0      1  -1.0
4   16086  202412     0.0      1  -1.0
5   16554  202412     0.0      1  -1.0
6   17672  202412     0.0      1  -1.0
7   18046  202412     0.0      1  -1.0
8   18048  202412     0.0      1  -1.0
9   18368  202412     0.0      1  -1.0
```

**Largest Differences**:
```
   permno  yyyymm  python  stata  diff
0   10006  198312     1.0      0   1.0
1   10006  198401     1.0      0   1.0
2   10006  198402     1.0      0   1.0
3   10006  198403     1.0      0   1.0
4   10006  198404     1.0      0   1.0
5   10006  198405     1.0      0   1.0
6   10025  200906     0.0      1  -1.0
7   10025  200907     0.0      1  -1.0
8   10025  200908     0.0      1  -1.0
9   10025  200909     0.0      1  -1.0
```

---

### CustomerMomentum

**Status**: ❌ FAILED

**Test Results**:
- Test 1 - Column names: ✅ PASSED
- Test 2 - Superset check: ❌ FAILED (Python missing 138 Stata observations)
- Test 3 - Precision1 check: ✅ PASSED
- Test 4 - Precision2 check: ❌ FAILED

**Columns**: ['CustomerMomentum']

**Observations**:
- Stata:  356,600
- Python: 356,510
- Common: 356,462

**Precision1**: 0.006% obs with diff >= 1.00e-04 (tolerance: < 0.1%)

**Precision2**: 100th percentile diff = 1.96e-01 (tolerance: < 1.00e-06)

**Missing Observations Sample**:
```
 index  permno  yyyymm  CustomerMomentum
     0   93436  201306          0.026457
     1   93436  201307          0.010277
     2   93436  201308         -0.009106
     3   93436  201309          0.070478
     4   93436  201310          0.010857
     5   93436  201311         -0.033766
     6   93436  201312         -0.025030
     7   93436  201401         -0.058727
     8   93436  201402          0.004705
     9   93436  201403         -0.003854
```

**Feedback**:
- Num observations with diff >= TOL_DIFF_1: 23/356462 (0.006%)

**Most Recent Bad Observations**:
```
   permno  yyyymm    python     stata      diff
0   65307  202010 -0.029265 -0.043112  0.013847
1   65307  202009 -0.022076 -0.011378 -0.010697
2   65307  202008  0.074049  0.089574 -0.015526
3   65307  202007  0.073459  0.056715  0.016744
4   65307  202005  0.129537  0.132980 -0.003442
5   65307  202004  0.143180  0.072385  0.070796
6   65307  202003 -0.120326 -0.078163 -0.042162
7   65307  202002 -0.061625 -0.063068  0.001443
8   65307  202001 -0.030696 -0.031811  0.001115
9   65307  201912  0.032281  0.027364  0.004918
```

**Largest Differences**:
```
   permno  yyyymm    python     stata      diff
0   75700  199705  0.216129  0.019663  0.196466
1   75700  199701 -0.060318  0.104568 -0.164886
2   75700  199610 -0.052288  0.111081 -0.163369
3   75700  199608  0.024735 -0.115854  0.140589
4   75700  199612  0.093750  0.003096  0.090654
5   75700  199703 -0.014737 -0.101333  0.086596
6   65307  202004  0.143180  0.072385  0.070796
7   75700  199702 -0.013514  0.056338 -0.069852
8   65307  201911 -0.014529  0.035459 -0.049988
9   65307  202003 -0.120326 -0.078163 -0.042162
```

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

**Precision1**: 0.000% obs with diff >= 1.00e-04 (tolerance: < 0.1%)

**Precision2**: 100th percentile diff = 0.00e+00 (tolerance: < 1.00e-06)

**Feedback**:
- Num observations with diff >= TOL_DIFF_1: 0/2725997 (0.000%)

---

### DelBreadth

**Status**: ❌ FAILED

**Test Results**:
- Test 1 - Column names: ✅ PASSED
- Test 2 - Superset check: ✅ PASSED
- Test 3 - Precision1 check: ✅ PASSED
- Test 4 - Precision2 check: ❌ FAILED

**Columns**: ['DelBreadth']

**Observations**:
- Stata:  1,062,671
- Python: 1,570,777
- Common: 1,062,671

**Precision1**: 0.000% obs with diff >= 1.00e-04 (tolerance: < 0.1%)

**Precision2**: 100th percentile diff = 2.00e-06 (tolerance: < 1.00e-06)

**Feedback**:
- Num observations with diff >= TOL_DIFF_1: 0/1062671 (0.000%)

---

### DelCOA

**Status**: ❌ FAILED

**Test Results**:
- Test 1 - Column names: ✅ PASSED
- Test 2 - Superset check: ✅ PASSED
- Test 3 - Precision1 check: ✅ PASSED
- Test 4 - Precision2 check: ❌ FAILED

**Columns**: ['DelCOA']

**Observations**:
- Stata:  3,295,155
- Python: 3,311,811
- Common: 3,295,155

**Precision1**: 0.002% obs with diff >= 1.00e-04 (tolerance: < 0.1%)

**Precision2**: 100th percentile diff = 1.77e-02 (tolerance: < 1.00e-06)

**Feedback**:
- Num observations with diff >= TOL_DIFF_1: 72/3295155 (0.002%)

**Most Recent Bad Observations**:
```
   permno  yyyymm    python     stata      diff
0   42585  202609  0.007199  0.009181 -0.001982
1   42585  202608  0.007199  0.009181 -0.001982
2   86349  202608 -0.005197 -0.002151 -0.003046
3   89256  202608  0.017889  0.024761 -0.006872
4   42585  202607  0.007199  0.009181 -0.001982
5   86349  202607 -0.005197 -0.002151 -0.003046
6   89256  202607  0.017889  0.024761 -0.006872
7   42585  202606  0.007199  0.009181 -0.001982
8   86349  202606 -0.005197 -0.002151 -0.003046
9   89256  202606  0.017889  0.024761 -0.006872
```

**Largest Differences**:
```
   permno  yyyymm   python     stata      diff
0   23033  202506  0.23089  0.213166  0.017724
1   23033  202507  0.23089  0.213166  0.017724
2   23033  202508  0.23089  0.213166  0.017724
3   23033  202509  0.23089  0.213166  0.017724
4   23033  202510  0.23089  0.213166  0.017724
5   23033  202511  0.23089  0.213166  0.017724
6   23033  202512  0.23089  0.213166  0.017724
7   23033  202601  0.23089  0.213166  0.017724
8   23033  202602  0.23089  0.213166  0.017724
9   23033  202603  0.23089  0.213166  0.017724
```

---

### DelCOL

**Status**: ❌ FAILED

**Test Results**:
- Test 1 - Column names: ✅ PASSED
- Test 2 - Superset check: ✅ PASSED
- Test 3 - Precision1 check: ✅ PASSED
- Test 4 - Precision2 check: ❌ FAILED

**Columns**: ['DelCOL']

**Observations**:
- Stata:  3,259,701
- Python: 3,276,202
- Common: 3,259,701

**Precision1**: 0.007% obs with diff >= 1.00e-04 (tolerance: < 0.1%)

**Precision2**: 100th percentile diff = 5.53e-01 (tolerance: < 1.00e-06)

**Feedback**:
- Num observations with diff >= TOL_DIFF_1: 216/3259701 (0.007%)

**Most Recent Bad Observations**:
```
   permno  yyyymm    python     stata      diff
0   10104  202610  0.023030  0.037066 -0.014036
1   10104  202609  0.023030  0.037066 -0.014036
2   20193  202609  0.027111  0.031757 -0.004646
3   21742  202609  0.012619  0.014631 -0.002013
4   42585  202609 -0.008304 -0.006147 -0.002157
5   60097  202609  0.003292  0.005406 -0.002114
6   10104  202608  0.023030  0.037066 -0.014036
7   14888  202608  0.011330  0.013535 -0.002205
8   18298  202608  0.002204  0.006616 -0.004413
9   20193  202608  0.027111  0.031757 -0.004646
```

**Largest Differences**:
```
   permno  yyyymm    python     stata      diff
0   18405  202506  3.901207  4.453714 -0.552506
1   18405  202507  3.901207  4.453714 -0.552506
2   18405  202508  3.901207  4.453714 -0.552506
3   18405  202509  3.901207  4.453714 -0.552506
4   18405  202510  3.901207  4.453714 -0.552506
5   18405  202511  3.901207  4.453714 -0.552506
6   18405  202512  3.901207  4.453714 -0.552506
7   18405  202601  3.901207  4.453714 -0.552506
8   18405  202602  3.901207  4.453714 -0.552506
9   18405  202603  3.901207  4.453714 -0.552506
```

---

### DelDRC

**Status**: ❌ FAILED

**Test Results**:
- Test 1 - Column names: ✅ PASSED
- Test 2 - Superset check: ✅ PASSED
- Test 3 - Precision1 check: ✅ PASSED
- Test 4 - Precision2 check: ❌ FAILED

**Columns**: ['DelDRC']

**Observations**:
- Stata:  460,159
- Python: 462,430
- Common: 460,159

**Precision1**: 0.013% obs with diff >= 1.00e-04 (tolerance: < 0.1%)

**Precision2**: 100th percentile diff = 1.37e-02 (tolerance: < 1.00e-06)

**Feedback**:
- Num observations with diff >= TOL_DIFF_1: 60/460159 (0.013%)

**Most Recent Bad Observations**:
```
   permno  yyyymm    python     stata      diff
0   21742  202609 -0.000940 -0.009745  0.008804
1   60097  202609  0.000022 -0.003875  0.003897
2   21742  202608 -0.000940 -0.009745  0.008804
3   51131  202608  0.000597 -0.004655  0.005251
4   59555  202608  0.004059 -0.009614  0.013673
5   60097  202608  0.000022 -0.003875  0.003897
6   21742  202607 -0.000940 -0.009745  0.008804
7   51131  202607  0.000597 -0.004655  0.005251
8   59555  202607  0.004059 -0.009614  0.013673
9   60097  202607  0.000022 -0.003875  0.003897
```

**Largest Differences**:
```
   permno  yyyymm    python     stata      diff
0   59555  202509  0.004059 -0.009614  0.013673
1   59555  202510  0.004059 -0.009614  0.013673
2   59555  202511  0.004059 -0.009614  0.013673
3   59555  202512  0.004059 -0.009614  0.013673
4   59555  202601  0.004059 -0.009614  0.013673
5   59555  202602  0.004059 -0.009614  0.013673
6   59555  202603  0.004059 -0.009614  0.013673
7   59555  202604  0.004059 -0.009614  0.013673
8   59555  202605  0.004059 -0.009614  0.013673
9   59555  202606  0.004059 -0.009614  0.013673
```

---

### DelEqu

**Status**: ❌ FAILED

**Test Results**:
- Test 1 - Column names: ✅ PASSED
- Test 2 - Superset check: ✅ PASSED
- Test 3 - Precision1 check: ✅ PASSED
- Test 4 - Precision2 check: ❌ FAILED

**Columns**: ['DelEqu']

**Observations**:
- Stata:  3,194,475
- Python: 3,195,504
- Common: 3,194,475

**Precision1**: 0.002% obs with diff >= 1.00e-04 (tolerance: < 0.1%)

**Precision2**: 100th percentile diff = 5.53e-01 (tolerance: < 1.00e-06)

**Feedback**:
- Num observations with diff >= TOL_DIFF_1: 48/3194475 (0.002%)

**Most Recent Bad Observations**:
```
   permno  yyyymm    python     stata      diff
0   10104  202610  0.075950  0.079299 -0.003349
1   10104  202609  0.075950  0.079299 -0.003349
2   10104  202608  0.075950  0.079299 -0.003349
3   10104  202607  0.075950  0.079299 -0.003349
4   10104  202606  0.075950  0.079299 -0.003349
5   10104  202605  0.075950  0.079299 -0.003349
6   18405  202605 -3.575558 -4.128064  0.552506
7   23033  202605 -0.373150 -0.545937  0.172787
8   10104  202604  0.075950  0.079299 -0.003349
9   18405  202604 -3.575558 -4.128064  0.552506
```

**Largest Differences**:
```
   permno  yyyymm    python     stata      diff
0   18405  202506 -3.575558 -4.128064  0.552506
1   18405  202507 -3.575558 -4.128064  0.552506
2   18405  202508 -3.575558 -4.128064  0.552506
3   18405  202509 -3.575558 -4.128064  0.552506
4   18405  202510 -3.575558 -4.128064  0.552506
5   18405  202511 -3.575558 -4.128064  0.552506
6   18405  202512 -3.575558 -4.128064  0.552506
7   18405  202601 -3.575558 -4.128064  0.552506
8   18405  202602 -3.575558 -4.128064  0.552506
9   18405  202603 -3.575558 -4.128064  0.552506
```

---

### DelFINL

**Status**: ❌ FAILED

**Test Results**:
- Test 1 - Column names: ✅ PASSED
- Test 2 - Superset check: ✅ PASSED
- Test 3 - Precision1 check: ✅ PASSED
- Test 4 - Precision2 check: ❌ FAILED

**Columns**: ['DelFINL']

**Observations**:
- Stata:  3,250,876
- Python: 3,251,941
- Common: 3,250,876

**Precision1**: 0.007% obs with diff >= 1.00e-04 (tolerance: < 0.1%)

**Precision2**: 100th percentile diff = 4.90e-02 (tolerance: < 1.00e-06)

**Feedback**:
- Num observations with diff >= TOL_DIFF_1: 216/3250876 (0.007%)

**Most Recent Bad Observations**:
```
   permno  yyyymm    python     stata      diff
0   10104  202610  0.093788  0.062295  0.031493
1   10104  202609  0.093788  0.062295  0.031493
2   21742  202609  0.181643  0.179631  0.002013
3   42585  202609 -0.039506 -0.046595  0.007088
4   60097  202609  0.039403  0.027171  0.012232
5   10104  202608  0.093788  0.062295  0.031493
6   18298  202608 -0.021946 -0.061206  0.039260
7   21742  202608  0.181643  0.179631  0.002013
8   42585  202608 -0.039506 -0.046595  0.007088
9   60097  202608  0.039403  0.027171  0.012232
```

**Largest Differences**:
```
   permno  yyyymm   python     stata      diff
0   16392  202506 -0.01293  0.036046 -0.048976
1   16392  202507 -0.01293  0.036046 -0.048976
2   16392  202508 -0.01293  0.036046 -0.048976
3   16392  202509 -0.01293  0.036046 -0.048976
4   16392  202510 -0.01293  0.036046 -0.048976
5   16392  202511 -0.01293  0.036046 -0.048976
6   16392  202512 -0.01293  0.036046 -0.048976
7   16392  202601 -0.01293  0.036046 -0.048976
8   16392  202602 -0.01293  0.036046 -0.048976
9   16392  202603 -0.01293  0.036046 -0.048976
```

---

### DelLTI

**Status**: ❌ FAILED

**Test Results**:
- Test 1 - Column names: ✅ PASSED
- Test 2 - Superset check: ✅ PASSED
- Test 3 - Precision1 check: ✅ PASSED
- Test 4 - Precision2 check: ❌ FAILED

**Columns**: ['DelLTI']

**Observations**:
- Stata:  3,295,155
- Python: 3,296,136
- Common: 3,295,155

**Precision1**: 0.008% obs with diff >= 1.00e-04 (tolerance: < 0.1%)

**Precision2**: 100th percentile diff = 7.52e-01 (tolerance: < 1.00e-06)

**Feedback**:
- Num observations with diff >= TOL_DIFF_1: 252/3295155 (0.008%)

**Most Recent Bad Observations**:
```
   permno  yyyymm    python     stata      diff
0   10104  202610  0.000647 -0.012931  0.013577
1   10104  202609  0.000647 -0.012931  0.013577
2   60097  202609 -0.004107 -0.014775  0.010668
3   10104  202608  0.000647 -0.012931  0.013577
4   51131  202608 -0.015757  0.046326 -0.062083
5   60097  202608 -0.004107 -0.014775  0.010668
6   86349  202608  0.003993  0.007076 -0.003083
7   86776  202608 -0.015026 -0.029933  0.014908
8   89256  202608  0.003404 -0.015238  0.018642
9   10104  202607  0.000647 -0.012931  0.013577
```

**Largest Differences**:
```
   permno  yyyymm    python  stata      diff
0   12373  202406  0.752101    0.0  0.752101
1   12373  202407  0.752101    0.0  0.752101
2   12373  202408  0.752101    0.0  0.752101
3   12373  202409  0.752101    0.0  0.752101
4   12373  202410  0.752101    0.0  0.752101
5   12373  202411  0.752101    0.0  0.752101
6   12373  202412  0.752101    0.0  0.752101
7   12373  202501  0.752101    0.0  0.752101
8   12373  202502  0.752101    0.0  0.752101
9   12373  202503  0.752101    0.0  0.752101
```

---

### DelNetFin

**Status**: ❌ FAILED

**Test Results**:
- Test 1 - Column names: ✅ PASSED
- Test 2 - Superset check: ✅ PASSED
- Test 3 - Precision1 check: ✅ PASSED
- Test 4 - Precision2 check: ❌ FAILED

**Columns**: ['DelNetFin']

**Observations**:
- Stata:  3,250,876
- Python: 3,251,941
- Common: 3,250,876

**Precision1**: 0.016% obs with diff >= 1.00e-04 (tolerance: < 0.1%)

**Precision2**: 100th percentile diff = 7.52e-01 (tolerance: < 1.00e-06)

**Feedback**:
- Num observations with diff >= TOL_DIFF_1: 504/3250876 (0.016%)

**Most Recent Bad Observations**:
```
   permno  yyyymm    python     stata      diff
0   10104  202610 -0.091783 -0.073868 -0.017916
1   10104  202609 -0.091783 -0.073868 -0.017916
2   21742  202609 -0.181643 -0.179631 -0.002013
3   42585  202609  0.041388  0.046494 -0.005106
4   60097  202609 -0.043223 -0.041660 -0.001563
5   10104  202608 -0.091783 -0.073868 -0.017916
6   18298  202608  0.015186  0.044080 -0.028894
7   21742  202608 -0.181643 -0.179631 -0.002013
8   42585  202608  0.041388  0.046494 -0.005106
9   51131  202608 -0.018392  0.043691 -0.062083
```

**Largest Differences**:
```
   permno  yyyymm    python     stata      diff
0   12373  202406  0.688862 -0.063239  0.752101
1   12373  202407  0.688862 -0.063239  0.752101
2   12373  202408  0.688862 -0.063239  0.752101
3   12373  202409  0.688862 -0.063239  0.752101
4   12373  202410  0.688862 -0.063239  0.752101
5   12373  202411  0.688862 -0.063239  0.752101
6   12373  202412  0.688862 -0.063239  0.752101
7   12373  202501  0.688862 -0.063239  0.752101
8   12373  202502  0.688862 -0.063239  0.752101
9   12373  202503  0.688862 -0.063239  0.752101
```

---

### DivInit

**Status**: ❌ FAILED

**Test Results**:
- Test 1 - Column names: ✅ PASSED
- Test 2 - Superset check: ✅ PASSED
- Test 3 - Precision1 check: ✅ PASSED
- Test 4 - Precision2 check: ❌ FAILED

**Columns**: ['DivInit']

**Observations**:
- Stata:  4,047,630
- Python: 4,047,630
- Common: 4,047,630

**Precision1**: 0.007% obs with diff >= 1.00e-04 (tolerance: < 0.1%)

**Precision2**: 100th percentile diff = 1.00e+00 (tolerance: < 1.00e-06)

**Feedback**:
- Num observations with diff >= TOL_DIFF_1: 287/4047630 (0.007%)

**Most Recent Bad Observations**:
```
   permno  yyyymm  python  stata  diff
0   13563  202204       0      1    -1
1   13563  202203       0      1    -1
2   13563  202202       0      1    -1
3   13563  202201       0      1    -1
4   13563  202112       0      1    -1
5   13563  202111       0      1    -1
6   79996  201910       0      1    -1
7   79996  201909       0      1    -1
8   79996  201908       0      1    -1
9   79996  201907       0      1    -1
```

**Largest Differences**:
```
   permno  yyyymm  python  stata  diff
0   10234  197906       1      0     1
1   10234  197907       1      0     1
2   10234  197908       1      0     1
3   10234  197909       1      0     1
4   10234  197910       1      0     1
5   10234  197911       1      0     1
6   10286  199008       1      0     1
7   10286  199009       1      0     1
8   10286  199010       1      0     1
9   10286  199011       1      0     1
```

---

### DivOmit

**Status**: ❌ FAILED

**Test Results**:
- Test 1 - Column names: ✅ PASSED
- Test 2 - Superset check: ✅ PASSED
- Test 3 - Precision1 check: ✅ PASSED
- Test 4 - Precision2 check: ❌ FAILED

**Columns**: ['DivOmit']

**Observations**:
- Stata:  4,047,630
- Python: 4,047,630
- Common: 4,047,630

**Precision1**: 0.003% obs with diff >= 1.00e-04 (tolerance: < 0.1%)

**Precision2**: 100th percentile diff = 1.00e+00 (tolerance: < 1.00e-06)

**Feedback**:
- Num observations with diff >= TOL_DIFF_1: 123/4047630 (0.003%)

**Most Recent Bad Observations**:
```
   permno  yyyymm  python  stata  diff
0   13007  202406       0      1    -1
1   13007  202405       0      1    -1
2   12362  201807       1      0     1
3   12362  201806       1      0     1
4   28222  201710       0      1    -1
5   28222  201709       0      1    -1
6   92893  201706       1      0     1
7   92893  201705       1      0     1
8   81593  201511       1      0     1
9   81593  201510       1      0     1
```

**Largest Differences**:
```
   permno  yyyymm  python  stata  diff
0   10172  198803       0      1    -1
1   10172  198804       0      1    -1
2   10209  195006       0      1    -1
3   10209  195007       0      1    -1
4   11287  197212       1      0     1
5   11470  199307       0      1    -1
6   11470  199308       0      1    -1
7   11565  200306       0      1    -1
8   11565  200307       0      1    -1
9   11748  201404       0      1    -1
```

---

### DivSeason

**Status**: ❌ FAILED

**Test Results**:
- Test 1 - Column names: ✅ PASSED
- Test 2 - Superset check: ❌ FAILED (Python missing 2 Stata observations)
- Test 3 - Precision1 check: ❌ FAILED
- Test 4 - Precision2 check: ❌ FAILED

**Columns**: ['DivSeason']

**Observations**:
- Stata:  1,775,339
- Python: 4,041,685
- Common: 1,775,337

**Precision1**: 5.214% obs with diff >= 1.00e-04 (tolerance: < 0.1%)

**Precision2**: 100th percentile diff = 1.00e+00 (tolerance: < 1.00e-06)

**Missing Observations Sample**:
```
 index  permno  yyyymm  DivSeason
     0   92823  198510          1
     1   92823  198511          1
```

**Feedback**:
- Num observations with diff >= TOL_DIFF_1: 92565/1775337 (5.214%)

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

**Status**: ❌ FAILED

**Test Results**:
- Test 1 - Column names: ✅ PASSED
- Test 2 - Superset check: ✅ PASSED
- Test 3 - Precision1 check: ❌ FAILED
- Test 4 - Precision2 check: ❌ FAILED

**Columns**: ['DivYieldST']

**Observations**:
- Stata:  1,591,700
- Python: 4,047,630
- Common: 1,591,700

**Precision1**: 89.464% obs with diff >= 1.00e-04 (tolerance: < 0.1%)

**Precision2**: 100th percentile diff = 2.00e+00 (tolerance: < 1.00e-06)

**Feedback**:
- Num observations with diff >= TOL_DIFF_1: 1423999/1591700 (89.464%)

**Most Recent Bad Observations**:
```
   permno  yyyymm  python  stata  diff
0   10026  202412     1.0      0   1.0
1   10107  202412     1.0      0   1.0
2   10138  202412     1.0      0   1.0
3   10145  202412     1.0      0   1.0
4   10220  202412     1.0      0   1.0
5   10252  202412     1.0      0   1.0
6   10294  202412     1.0      0   1.0
7   10308  202412     1.0      0   1.0
8   10318  202412     1.0      0   1.0
9   10382  202412     1.0      0   1.0
```

**Largest Differences**:
```
   permno  yyyymm  python  stata  diff
0   10001  198605     1.0      3  -2.0
1   10001  198608     1.0      3  -2.0
2   10001  198611     1.0      3  -2.0
3   10001  198702     1.0      3  -2.0
4   10001  198705     1.0      3  -2.0
5   10001  198708     1.0      3  -2.0
6   10001  198711     1.0      3  -2.0
7   10001  198802     1.0      3  -2.0
8   10001  198805     1.0      3  -2.0
9   10001  198808     1.0      3  -2.0
```

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

**Precision1**: 0.000% obs with diff >= 1.00e-04 (tolerance: < 0.1%)

**Precision2**: 100th percentile diff = 9.62e-07 (tolerance: < 1.00e-06)

**Feedback**:
- Num observations with diff >= TOL_DIFF_1: 0/4640493 (0.000%)

---

### EBM

**Status**: ❌ FAILED

**Test Results**:
- Test 1 - Column names: ✅ PASSED
- Test 2 - Superset check: ✅ PASSED
- Test 3 - Precision1 check: ❌ FAILED
- Test 4 - Precision2 check: ❌ FAILED

**Columns**: ['EBM']

**Observations**:
- Stata:  2,924,820
- Python: 2,924,826
- Common: 2,924,820

**Precision1**: 0.268% obs with diff >= 1.00e-04 (tolerance: < 0.1%)

**Precision2**: 100th percentile diff = 4.03e+03 (tolerance: < 1.00e-06)

**Feedback**:
- Num observations with diff >= TOL_DIFF_1: 7833/2924820 (0.268%)

**Most Recent Bad Observations**:
```
   permno  yyyymm      python       stata      diff
0   13188  202412   92.167184   92.167763 -0.000579
1   15014  202412    1.474967    1.497721 -0.022754
2   20137  202412    0.057356    0.057139  0.000216
3   22767  202412  103.975378  103.975520 -0.000142
4   23033  202412    0.519364    0.590755 -0.071392
5   23340  202412    0.482983    0.584964 -0.101982
6   77182  202412 -819.512493 -819.460330 -0.052163
7   83856  202412 -121.842373 -121.842190 -0.000183
8   84172  202412  161.097824  161.098220 -0.000396
9   89139  202412  -54.852668  -54.852383 -0.000285
```

**Largest Differences**:
```
   permno  yyyymm         python          stata         diff
0   86685  200408  467703.097020  471732.530000 -4029.432980
1   46017  199403  121692.753619  118543.090000  3149.663619
2   16063  202307  -79267.440326  -78955.930000  -311.510326
3   17806  198508  -46481.794441  -46678.664000   196.869559
4   79322  200912  -52981.539718  -52891.289000   -90.250718
5   62026  198508  -68482.022080  -68565.664000    83.641920
6   37161  200701   28763.152908   28721.916000    41.236908
7   50091  197204   19076.862866   19044.463000    32.399866
8   13370  197612  -46433.000000  -46458.520000    25.520000
9   23340  202308     -24.211752       0.029465   -24.241218
```

---

### EP

**Status**: ❌ FAILED

**Test Results**:
- Test 1 - Column names: ✅ PASSED
- Test 2 - Superset check: ✅ PASSED
- Test 3 - Precision1 check: ✅ PASSED
- Test 4 - Precision2 check: ❌ FAILED

**Columns**: ['EP']

**Observations**:
- Stata:  2,203,166
- Python: 2,203,166
- Common: 2,203,166

**Precision1**: 0.000% obs with diff >= 1.00e-04 (tolerance: < 0.1%)

**Precision2**: 100th percentile diff = 8.71e-06 (tolerance: < 1.00e-06)

**Feedback**:
- Num observations with diff >= TOL_DIFF_1: 0/2203166 (0.000%)

---

### EntMult

**Status**: ❌ FAILED

**Test Results**:
- Test 1 - Column names: ✅ PASSED
- Test 2 - Superset check: ❌ FAILED (Python missing 7 Stata observations)
- Test 3 - Precision1 check: ✅ PASSED
- Test 4 - Precision2 check: ❌ FAILED

**Columns**: ['EntMult']

**Observations**:
- Stata:  2,407,850
- Python: 2,408,497
- Common: 2,407,843

**Precision1**: 0.049% obs with diff >= 1.00e-04 (tolerance: < 0.1%)

**Precision2**: 100th percentile diff = 2.24e+00 (tolerance: < 1.00e-06)

**Missing Observations Sample**:
```
 index  permno  yyyymm   EntMult
     0   12373  202406 22.466608
     1   12373  202407 23.858236
     2   12373  202408 24.015013
     3   12373  202409 24.344990
     4   12373  202410 24.137447
     5   12373  202411 25.709810
     6   12373  202412 24.246437
```

**Feedback**:
- Num observations with diff >= TOL_DIFF_1: 1182/2407843 (0.049%)

**Most Recent Bad Observations**:
```
   permno  yyyymm     python      stata      diff
0   12500  202412   0.142548   0.141332  0.001215
1   15014  202412   7.763593   7.603958  0.159635
2   15203  202412   8.272568   8.162786  0.109782
3   15862  202412   2.937521   2.944510 -0.006990
4   18368  202412   9.810341   9.714308  0.096034
5   18649  202412   8.868280   8.836927  0.031353
6   22096  202412   7.307931   7.367719 -0.059787
7   23340  202412  19.734115  17.667999  2.066116
8   57817  202412   6.990977   6.796951  0.194026
9   82702  202412  11.016960  11.136445 -0.119485
```

**Largest Differences**:
```
   permno  yyyymm     python      stata      diff
0   22096  202207   6.874053   9.112578 -2.238526
1   22096  202210   6.604562   8.755329 -2.150767
2   22096  202208   6.597968   8.746587 -2.148619
3   22096  202211   6.475874   8.584734 -2.108860
4   22096  202301   6.400471   8.484775 -2.084304
5   23340  202412  19.734115  17.667999  2.066116
6   23340  202411  20.881258  18.815142  2.066116
7   23340  202407  20.521722  18.455606  2.066116
8   23340  202409  19.929859  17.863743  2.066116
9   23340  202410  21.206847  19.140732  2.066115
```

---

### EquityDuration

**Status**: ❌ FAILED

**Test Results**:
- Test 1 - Column names: ✅ PASSED
- Test 2 - Superset check: ✅ PASSED
- Test 3 - Precision1 check: ❌ FAILED
- Test 4 - Precision2 check: ❌ FAILED

**Columns**: ['EquityDuration']

**Observations**:
- Stata:  3,124,663
- Python: 3,201,768
- Common: 3,124,663

**Precision1**: 0.167% obs with diff >= 1.00e-04 (tolerance: < 0.1%)

**Precision2**: 100th percentile diff = 3.26e+05 (tolerance: < 1.00e-06)

**Feedback**:
- Num observations with diff >= TOL_DIFF_1: 5207/3124663 (0.167%)

**Most Recent Bad Observations**:
```
   permno  yyyymm     python      stata      diff
0   10104  202610  17.975254  17.938868  0.036386
1   10104  202609  17.975254  17.938868  0.036386
2   10501  202609  12.612647  12.799109 -0.186462
3   20193  202609  20.300457  20.312025 -0.011568
4   22620  202609  19.244924  19.244158  0.000766
5   10104  202608  17.975254  17.938868  0.036386
6   10501  202608  12.612647  12.799109 -0.186462
7   12082  202608  18.814461  18.808577  0.005884
8   14888  202608  16.474692  16.481756 -0.007064
9   20193  202608  20.300457  20.312025 -0.011568
```

**Largest Differences**:
```
   permno  yyyymm        python         stata          diff
0   92032  201906  2.881426e+12  2.881426e+12  325978.65332
1   92032  201907  2.881426e+12  2.881426e+12  325978.65332
2   92032  201908  2.881426e+12  2.881426e+12  325978.65332
3   92032  201909  2.881426e+12  2.881426e+12  325978.65332
4   92032  201910  2.881426e+12  2.881426e+12  325978.65332
5   92032  201911  2.881426e+12  2.881426e+12  325978.65332
6   92032  201912  2.881426e+12  2.881426e+12  325978.65332
7   92032  202001  2.881426e+12  2.881426e+12  325978.65332
8   92032  202002  2.881426e+12  2.881426e+12  325978.65332
9   92032  202003  2.881426e+12  2.881426e+12  325978.65332
```

---

### ExchSwitch

**Status**: ❌ FAILED

**Test Results**:
- Test 1 - Column names: ✅ PASSED
- Test 2 - Superset check: ✅ PASSED
- Test 3 - Precision1 check: ✅ PASSED
- Test 4 - Precision2 check: ❌ FAILED

**Columns**: ['ExchSwitch']

**Observations**:
- Stata:  4,047,630
- Python: 4,047,630
- Common: 4,047,630

**Precision1**: 0.047% obs with diff >= 1.00e-04 (tolerance: < 0.1%)

**Precision2**: 100th percentile diff = 1.00e+00 (tolerance: < 1.00e-06)

**Feedback**:
- Num observations with diff >= TOL_DIFF_1: 1899/4047630 (0.047%)

**Most Recent Bad Observations**:
```
   permno  yyyymm  python  stata  diff
0   78690  202304       1      0     1
1   78690  202303       1      0     1
2   78690  202302       1      0     1
3   12928  202301       1      0     1
4   78690  202301       1      0     1
5   12928  202212       1      0     1
6   78690  202212       1      0     1
7   12928  202211       1      0     1
8   78690  202211       1      0     1
9   12928  202210       1      0     1
```

**Largest Differences**:
```
   permno  yyyymm  python  stata  diff
0   10066  199903       1      0     1
1   10066  199904       1      0     1
2   10066  199905       1      0     1
3   10066  199906       1      0     1
4   10066  199907       1      0     1
5   10066  199908       1      0     1
6   10066  199909       1      0     1
7   10066  199910       1      0     1
8   10066  199911       1      0     1
9   10066  199912       1      0     1
```

---

### ExclExp

**Status**: ❌ FAILED

**Test Results**:
- Test 1 - Column names: ✅ PASSED
- Test 2 - Superset check: ❌ FAILED (Python missing 2029 Stata observations)
- Test 3 - Precision1 check: ❌ FAILED
- Test 4 - Precision2 check: ❌ FAILED

**Columns**: ['ExclExp']

**Observations**:
- Stata:  1,726,232
- Python: 1,762,541
- Common: 1,724,203

**Precision1**: 0.108% obs with diff >= 1.00e-04 (tolerance: < 0.1%)

**Precision2**: 100th percentile diff = 3.69e+00 (tolerance: < 1.00e-06)

**Missing Observations Sample**:
```
 index  permno  yyyymm  ExclExp
     0   10515  199604    0.000
     1   10515  199605    0.000
     2   10515  199606   -0.075
     3   11406  199008    0.050
     4   11406  199009    0.000
     5   11406  199010    0.000
     6   11406  199011   -0.020
     7   11406  199012    0.000
     8   11406  199101    0.000
     9   11406  199102    0.000
```

**Feedback**:
- Num observations with diff >= TOL_DIFF_1: 1864/1724203 (0.108%)

**Most Recent Bad Observations**:
```
   permno  yyyymm  python  stata  diff
0   19018  202412    0.00   0.02 -0.02
1   21091  202412   -0.49  -0.46 -0.03
2   86115  202412    0.26   0.41 -0.15
3   91575  202412   -1.80   0.05 -1.85
4   91575  202411   -1.80   1.89 -3.69
5   23033  202410   -0.20  -0.21  0.01
6   91575  202410   -1.80   0.14 -1.94
7   23033  202409   -0.20  -0.21  0.01
8   89606  202409   -0.62  -0.59 -0.03
9   91575  202409   -1.80   0.14 -1.94
```

**Largest Differences**:
```
   permno  yyyymm  python  stata  diff
0   91575  202411   -1.80   1.89 -3.69
1   91575  202311   -1.80   1.32 -3.12
2   51633  198903   -1.80   0.93 -2.73
3   51633  198904   -1.80   0.93 -2.73
4   66157  198709    2.69  -0.01  2.70
5   21091  202406    2.69   0.04  2.65
6   21091  202407    2.69   0.04  2.65
7   21091  202408    2.69   0.13  2.56
8   66157  198903    2.69   0.14  2.55
9   91575  202211   -1.34   1.00 -2.34
```

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

**Precision1**: 0.000% obs with diff >= 1.00e-04 (tolerance: < 0.1%)

**Precision2**: 100th percentile diff = 0.00e+00 (tolerance: < 1.00e-06)

**Feedback**:
- Num observations with diff >= TOL_DIFF_1: 0/4045796 (0.000%)

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

**Precision1**: 99.813% obs with diff >= 1.00e-04 (tolerance: < 0.1%)

**Precision2**: 100th percentile diff = 5.95e+00 (tolerance: < 1.00e-06)

**Feedback**:
- Num observations with diff >= TOL_DIFF_1: 1218880/1221161 (99.813%)

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
9   10258  202412 -0.459465 -0.454809 -0.004656
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

**Status**: ❌ FAILED

**Test Results**:
- Test 1 - Column names: ✅ PASSED
- Test 2 - Superset check: ✅ PASSED
- Test 3 - Precision1 check: ✅ PASSED
- Test 4 - Precision2 check: ❌ FAILED

**Columns**: ['GP']

**Observations**:
- Stata:  2,970,775
- Python: 2,972,251
- Common: 2,970,775

**Precision1**: 0.017% obs with diff >= 1.00e-04 (tolerance: < 0.1%)

**Precision2**: 100th percentile diff = 1.07e+00 (tolerance: < 1.00e-06)

**Feedback**:
- Num observations with diff >= TOL_DIFF_1: 516/2970775 (0.017%)

**Most Recent Bad Observations**:
```
   permno  yyyymm    python     stata      diff
0   22620  202609  0.376700  0.349591  0.027109
1   12082  202608  0.292990  0.297504 -0.004514
2   14888  202608  0.238370  0.236845  0.001525
3   18298  202608  0.227520  0.225605  0.001915
4   22620  202608  0.376700  0.349591  0.027109
5   51131  202608  0.063143  0.072499 -0.009355
6   86776  202608  0.369769  0.337103  0.032665
7   12082  202607  0.292990  0.297504 -0.004514
8   12339  202607  0.227611  0.218107  0.009503
9   14888  202607  0.238370  0.236845  0.001525
```

**Largest Differences**:
```
   permno  yyyymm    python     stata      diff
0   18643  202409  0.011815 -1.054809  1.066625
1   18643  202410  0.011815 -1.054809  1.066625
2   18643  202411  0.011815 -1.054809  1.066625
3   18643  202412  0.011815 -1.054809  1.066625
4   18643  202501  0.011815 -1.054809  1.066625
5   18643  202502  0.011815 -1.054809  1.066625
6   18643  202503  0.011815 -1.054809  1.066625
7   18643  202504  0.011815 -1.054809  1.066625
8   18643  202505  0.011815 -1.054809  1.066625
9   18643  202506  0.011815 -1.054809  1.066625
```

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

**Precision1**: 0.000% obs with diff >= 1.00e-04 (tolerance: < 0.1%)

**Precision2**: 100th percentile diff = 0.00e+00 (tolerance: < 1.00e-06)

**Feedback**:
- Num observations with diff >= TOL_DIFF_1: 0/334058 (0.000%)

---

### Herf

**Status**: ❌ FAILED

**Test Results**:
- Test 1 - Column names: ✅ PASSED
- Test 2 - Superset check: ✅ PASSED
- Test 3 - Precision1 check: ❌ FAILED
- Test 4 - Precision2 check: ❌ FAILED

**Columns**: ['Herf']

**Observations**:
- Stata:  3,158,336
- Python: 3,165,145
- Common: 3,158,336

**Precision1**: 1.023% obs with diff >= 1.00e-04 (tolerance: < 0.1%)

**Precision2**: 100th percentile diff = 2.20e+00 (tolerance: < 1.00e-06)

**Feedback**:
- Num observations with diff >= TOL_DIFF_1: 32315/3158336 (1.023%)

**Most Recent Bad Observations**:
```
   permno  yyyymm    python     stata      diff
0   12373  202412  0.663389  0.663996 -0.000607
1   12928  202412  0.396959  0.406861 -0.009902
2   14051  202412  0.132628  0.139513 -0.006885
3   16773  202412  0.016906  0.016373  0.000533
4   19920  202412  0.205427  0.210144 -0.004717
5   20665  202412  0.165612  0.170717 -0.005105
6   38746  202412  0.565780  0.566387 -0.000607
7   77263  202412  0.638889  0.500000  0.138889
8   77790  202412  0.565780  0.566387 -0.000607
9   77900  202412  0.260348  0.264657 -0.004309
```

**Largest Differences**:
```
   permno  yyyymm    python     stata      diff
0   64785  200902  2.598195  4.801324 -2.203130
1   64785  200903  2.878780  5.074786 -2.196006
2   64785  200901  2.316989  4.496621 -2.179632
3   64785  200904  3.159325  5.322203 -2.162878
4   64785  200812  2.035793  4.156070 -2.120277
5   64785  200905  3.439983  5.547128 -2.107145
6   64785  200811  1.777768  3.825085 -2.047317
7   64785  200810  1.519743  3.449967 -1.930225
8   64785  200906  3.515275  5.430809 -1.915533
9   64785  200809  1.261732  3.021262 -1.759530
```

---

### HerfAsset

**Status**: ❌ FAILED

**Test Results**:
- Test 1 - Column names: ✅ PASSED
- Test 2 - Superset check: ✅ PASSED
- Test 3 - Precision1 check: ❌ FAILED
- Test 4 - Precision2 check: ❌ FAILED

**Columns**: ['HerfAsset']

**Observations**:
- Stata:  2,547,057
- Python: 2,553,214
- Common: 2,547,057

**Precision1**: 2.175% obs with diff >= 1.00e-04 (tolerance: < 0.1%)

**Precision2**: 100th percentile diff = 6.45e-01 (tolerance: < 1.00e-06)

**Feedback**:
- Num observations with diff >= TOL_DIFF_1: 55407/2547057 (2.175%)

**Most Recent Bad Observations**:
```
   permno  yyyymm    python     stata      diff
0   11153  202412  0.332202  0.372792 -0.040590
1   11379  202412  0.626341  0.635870 -0.009529
2   12350  202412  0.023186  0.021049  0.002136
3   12928  202412  0.261507  0.459600 -0.198092
4   13563  202412  0.022453  0.019441  0.003012
5   13798  202412  0.430744  0.437600 -0.006856
6   14051  202412  0.132821  0.139013 -0.006191
7   14469  202412  0.026686  0.019441  0.007244
8   15294  202412  0.021884  0.019441  0.002443
9   15793  202412  0.022510  0.019441  0.003069
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
- Test 3 - Precision1 check: ❌ FAILED
- Test 4 - Precision2 check: ❌ FAILED

**Columns**: ['HerfBE']

**Observations**:
- Stata:  2,547,057
- Python: 2,553,214
- Common: 2,547,057

**Precision1**: 2.398% obs with diff >= 1.00e-04 (tolerance: < 0.1%)

**Precision2**: 100th percentile diff = 6.37e+02 (tolerance: < 1.00e-06)

**Feedback**:
- Num observations with diff >= TOL_DIFF_1: 61069/2547057 (2.398%)

**Most Recent Bad Observations**:
```
   permno  yyyymm    python     stata      diff
0   11153  202412  0.331422  0.367457 -0.036035
1   11379  202412  0.569445  0.569160  0.000285
2   12350  202412  0.020664  0.019198  0.001466
3   12928  202412  0.276350  0.493899 -0.217549
4   13563  202412  0.020155  0.017095  0.003059
5   13798  202412  0.528626  0.550402 -0.021775
6   14051  202412  0.163510  0.171811 -0.008301
7   14469  202412  0.022487  0.017095  0.005391
8   15294  202412  0.019332  0.017095  0.002236
9   15793  202412  0.020173  0.017095  0.003078
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

### IdioVol3F

**Status**: ❌ FAILED

**Test Results**:
- Test 1 - Column names: ✅ PASSED
- Test 2 - Superset check: ✅ PASSED
- Test 3 - Precision1 check: ❌ FAILED
- Test 4 - Precision2 check: ❌ FAILED

**Columns**: ['IdioVol3F']

**Observations**:
- Stata:  4,980,936
- Python: 5,026,821
- Common: 4,980,936

**Precision1**: 0.248% obs with diff >= 1.00e-04 (tolerance: < 0.1%)

**Precision2**: 100th percentile diff = 1.76e-02 (tolerance: < 1.00e-06)

**Feedback**:
- Num observations with diff >= TOL_DIFF_1: 12365/4980936 (0.248%)

**Most Recent Bad Observations**:
```
   permno  yyyymm    python     stata      diff
0   15789  202412  0.108269  0.108433 -0.000164
1   15846  202412  0.331909  0.332326 -0.000417
2   17685  202412  0.055334  0.055209  0.000125
3   18427  202412  0.610097  0.610257 -0.000160
4   19065  202412  0.084925  0.084774  0.000150
5   19391  202412  0.160329  0.160166  0.000163
6   19479  202412  0.046020  0.045898  0.000122
7   19549  202412  1.470855  1.471110 -0.000255
8   19746  202412  0.085125  0.084907  0.000218
9   19978  202412  0.230907  0.230635  0.000272
```

**Largest Differences**:
```
   permno  yyyymm    python     stata      diff
0   13883  202310  7.799678  7.817299 -0.017621
1   16400  202401  0.982255  0.986626 -0.004372
2   17105  201811  0.520284  0.516678  0.003606
3   20439  202301  1.389258  1.386151  0.003107
4   18363  201901  1.182937  1.179979  0.002958
5   90926  201809  0.474128  0.471342  0.002786
6   22793  202204  0.346254  0.343756  0.002499
7   16070  202308  1.042644  1.045074 -0.002429
8   16903  202406  0.874303  0.876677 -0.002375
9   16568  201903  0.875490  0.873197  0.002293
```

---

### IdioVolAHT

**Status**: ❌ FAILED

**Test Results**:
- Test 1 - Column names: ✅ PASSED
- Test 2 - Superset check: ✅ PASSED
- Test 3 - Precision1 check: ❌ FAILED
- Test 4 - Precision2 check: ❌ FAILED

**Columns**: ['IdioVolAHT']

**Observations**:
- Stata:  4,849,170
- Python: 5,113,369
- Common: 4,849,170

**Precision1**: 45.952% obs with diff >= 1.00e-04 (tolerance: < 0.1%)

**Precision2**: 100th percentile diff = nan (tolerance: < 1.00e-06)

**Feedback**:
- Num observations with diff >= TOL_DIFF_1: 2228295/4849170 (45.952%)

**Most Recent Bad Observations**:
```
   permno  yyyymm    python     stata      diff
0   10044  202412  0.038180  0.038332 -0.000152
1   10158  202412  0.043653  0.043827 -0.000174
2   10200  202412  0.027470  0.027580 -0.000110
3   10253  202412  0.039032  0.039188 -0.000156
4   10258  202412  0.035483  0.035624 -0.000142
5   10294  202412  0.025494  0.025595 -0.000102
6   10333  202412  0.034217  0.034353 -0.000137
7   10463  202412  0.043316  0.043489 -0.000173
8   10517  202412  0.025909  0.026013 -0.000103
9   10550  202412  0.038080  0.038232 -0.000152
```

**Largest Differences**:
```
   permno  yyyymm  python     stata  diff
0   10007  198902     NaN  0.054694   NaN
1   10007  198903     NaN  0.055225   NaN
2   10007  198904     NaN  0.054111   NaN
3   10007  198905     NaN  0.054717   NaN
4   10007  198906     NaN  0.054713   NaN
5   10051  201809     NaN  0.018538   NaN
6   10051  201810     NaN  0.018122   NaN
7   10051  201811     NaN  0.019433   NaN
8   10051  201812     NaN  0.019570   NaN
9   10051  201901     NaN  0.019574   NaN
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

**Precision1**: 0.000% obs with diff >= 1.00e-04 (tolerance: < 0.1%)

**Precision2**: 100th percentile diff = 4.04e-09 (tolerance: < 1.00e-06)

**Feedback**:
- Num observations with diff >= TOL_DIFF_1: 0/4278152 (0.000%)

---

### IndMom

**Status**: ❌ FAILED

**Test Results**:
- Test 1 - Column names: ✅ PASSED
- Test 2 - Superset check: ✅ PASSED
- Test 3 - Precision1 check: ❌ FAILED
- Test 4 - Precision2 check: ❌ FAILED

**Columns**: ['IndMom']

**Observations**:
- Stata:  4,043,138
- Python: 4,044,574
- Common: 4,043,138

**Precision1**: 12.945% obs with diff >= 1.00e-04 (tolerance: < 0.1%)

**Precision2**: 100th percentile diff = 1.27e+00 (tolerance: < 1.00e-06)

**Feedback**:
- Num observations with diff >= TOL_DIFF_1: 523392/4043138 (12.945%)

**Most Recent Bad Observations**:
```
   permno  yyyymm    python     stata      diff
0   10606  202412  0.221829  0.362349 -0.140520
1   11404  202412  0.268826  0.301823 -0.032996
2   11674  202412  0.268826  0.301823 -0.032996
3   11762  202412  0.167474  0.167149  0.000325
4   11809  202412  0.268826  0.301823 -0.032996
5   11955  202412  0.268826  0.301823 -0.032996
6   12082  202412  0.399020  0.400071 -0.001051
7   12084  202412  0.399020  0.400071 -0.001051
8   12350  202412  0.399020  0.400071 -0.001051
9   12360  202412  0.399020  0.400071 -0.001051
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

### IntMom

**Status**: ❌ FAILED

**Test Results**:
- Test 1 - Column names: ✅ PASSED
- Test 2 - Superset check: ✅ PASSED
- Test 3 - Precision1 check: ✅ PASSED
- Test 4 - Precision2 check: ❌ FAILED

**Columns**: ['IntMom']

**Observations**:
- Stata:  3,686,625
- Python: 4,047,630
- Common: 3,686,625

**Precision1**: 0.000% obs with diff >= 1.00e-04 (tolerance: < 0.1%)

**Precision2**: 100th percentile diff = 2.15e-06 (tolerance: < 1.00e-06)

**Feedback**:
- Num observations with diff >= TOL_DIFF_1: 0/3686625 (0.000%)

---

### IntanBM

**Status**: ❌ FAILED

**Test Results**:
- Test 1 - Column names: ✅ PASSED
- Test 2 - Superset check: ❌ FAILED (Python missing 6708 Stata observations)
- Test 3 - Precision1 check: ❌ FAILED
- Test 4 - Precision2 check: ❌ FAILED

**Columns**: ['IntanBM']

**Observations**:
- Stata:  1,728,575
- Python: 1,745,102
- Common: 1,721,867

**Precision1**: 99.489% obs with diff >= 1.00e-04 (tolerance: < 0.1%)

**Precision2**: 100th percentile diff = 3.98e+00 (tolerance: < 1.00e-06)

**Missing Observations Sample**:
```
 index  permno  yyyymm   IntanBM
     0   10031  198906 -1.452560
     1   10051  199203  3.137398
     2   10051  199204  3.482056
     3   10051  199205  3.315531
     4   10066  198911 -0.067446
     5   10082  199402  1.767595
     6   10082  199403  2.291165
     7   10082  199404  2.240274
     8   10082  199405  1.983207
     9   10082  199406  1.555254
```

**Feedback**:
- Num observations with diff >= TOL_DIFF_1: 1713074/1721867 (99.489%)

**Most Recent Bad Observations**:
```
   permno  yyyymm    python     stata      diff
0   10026  202412 -0.029442 -0.032523  0.003081
1   10028  202412  1.083997  0.863343  0.220653
2   10032  202412  0.481317  0.485618 -0.004301
3   10044  202412 -0.437437 -0.441253  0.003817
4   10104  202412  2.460790  2.456047  0.004743
5   10107  202412  0.899143  0.902072 -0.002929
6   10138  202412 -0.195015 -0.194707 -0.000308
7   10145  202412  0.721868  0.715202  0.006666
8   10158  202412 -0.503026 -0.490164 -0.012863
9   10200  202412  0.007900  0.008795 -0.000894
```

**Largest Differences**:
```
   permno  yyyymm    python     stata      diff
0   76995  200003  0.544785 -3.435120  3.979905
1   76995  200002  0.317854 -3.593434  3.911288
2   90170  202407 -3.370588  0.481798 -3.852386
3   90170  202408 -3.062880  0.742377 -3.805256
4   13751  202101 -4.115171 -0.481746 -3.633425
5   90170  202312 -0.779426 -4.321275  3.541850
6   76995  200001 -0.539534 -4.074275  3.534741
7   90170  202401 -1.331707 -4.824741  3.493033
8   65541  199912  1.087601 -2.354047  3.441648
9   90170  202406 -2.883440  0.532473 -3.415913
```

---

### IntanCFP

**Status**: ❌ FAILED

**Test Results**:
- Test 1 - Column names: ✅ PASSED
- Test 2 - Superset check: ❌ FAILED (Python missing 5862 Stata observations)
- Test 3 - Precision1 check: ❌ FAILED
- Test 4 - Precision2 check: ❌ FAILED

**Columns**: ['IntanCFP']

**Observations**:
- Stata:  1,881,254
- Python: 1,899,552
- Common: 1,875,392

**Precision1**: 97.562% obs with diff >= 1.00e-04 (tolerance: < 0.1%)

**Precision2**: 100th percentile diff = 9.57e+00 (tolerance: < 1.00e-06)

**Missing Observations Sample**:
```
 index  permno  yyyymm  IntanCFP
     0   10031  198906 -0.467256
     1   10051  199203 -0.077828
     2   10051  199204  0.117282
     3   10051  199205 -0.010084
     4   10057  197006 -0.014668
     5   10057  197007 -0.037554
     6   10057  197008 -0.037103
     7   10057  197009 -0.060326
     8   10057  197010 -0.063337
     9   10057  197011 -0.073378
```

**Feedback**:
- Num observations with diff >= TOL_DIFF_1: 1829662/1875392 (97.562%)

**Most Recent Bad Observations**:
```
   permno  yyyymm    python     stata      diff
0   10026  202412 -0.188506 -0.171818 -0.016688
1   10028  202412  0.740787  0.679321  0.061466
2   10032  202412  0.042084  0.040258  0.001826
3   10044  202412 -0.114935 -0.082300 -0.032635
4   10104  202412  0.343113  0.322640  0.020473
5   10107  202412  0.214476  0.201555  0.012921
6   10138  202412 -0.173831 -0.159747 -0.014084
7   10145  202412 -0.081892 -0.072032 -0.009860
8   10158  202412 -0.180332 -0.167753 -0.012579
9   10200  202412 -0.031344 -0.026040 -0.005304
```

**Largest Differences**:
```
   permno  yyyymm     python      stata      diff
0   78041  199910  11.580927  21.148239 -9.567312
1   18286  200106  27.697047  34.733170 -7.036123
2   20968  199512   7.139837   0.166095  6.973742
3   20968  199601   7.082126   1.889605  5.192520
4   11887  199910   5.024956   9.897124 -4.872168
5   78881  200209   4.652081   0.300865  4.351216
6   78971  200801  -0.229538  -4.235927  4.006389
7   75899  199910   3.907606   7.891233 -3.983627
8   68339  199006  30.283925  34.174980 -3.891055
9   18278  199203  15.088095  18.956718 -3.868623
```

---

### IntanEP

**Status**: ❌ FAILED

**Test Results**:
- Test 1 - Column names: ✅ PASSED
- Test 2 - Superset check: ❌ FAILED (Python missing 5862 Stata observations)
- Test 3 - Precision1 check: ❌ FAILED
- Test 4 - Precision2 check: ❌ FAILED

**Columns**: ['IntanEP']

**Observations**:
- Stata:  1,881,254
- Python: 1,899,552
- Common: 1,875,392

**Precision1**: 96.530% obs with diff >= 1.00e-04 (tolerance: < 0.1%)

**Precision2**: 100th percentile diff = 1.53e+01 (tolerance: < 1.00e-06)

**Missing Observations Sample**:
```
 index  permno  yyyymm   IntanEP
     0   10031  198906 -0.774279
     1   10051  199203 -0.210539
     2   10051  199204  0.106389
     3   10051  199205 -0.074725
     4   10057  197006 -0.060351
     5   10057  197007 -0.077210
     6   10057  197008 -0.078048
     7   10057  197009 -0.087054
     8   10057  197010 -0.093895
     9   10057  197011 -0.101754
```

**Feedback**:
- Num observations with diff >= TOL_DIFF_1: 1810315/1875392 (96.530%)

**Most Recent Bad Observations**:
```
   permno  yyyymm    python     stata      diff
0   10026  202412 -0.240116 -0.224882 -0.015234
1   10028  202412  0.852046  0.798814  0.053232
2   10032  202412  0.030790  0.029433  0.001357
3   10044  202412 -0.212717 -0.184353 -0.028364
4   10104  202412  0.382565  0.363849  0.018716
5   10107  202412  0.226079  0.214817  0.011263
6   10138  202412 -0.219474 -0.206796 -0.012679
7   10145  202412 -0.124812 -0.116019 -0.008793
8   10158  202412 -0.169487 -0.160120 -0.009367
9   10200  202412 -0.067140 -0.061401 -0.005739
```

**Largest Differences**:
```
   permno  yyyymm     python      stata       diff
0   68339  199006  17.903236  33.174107 -15.270871
1   20968  199512  11.409520   1.054386  10.355134
2   65445  199808  19.646535  29.729954 -10.083419
3   20968  199601  11.296138   3.814879   7.481258
4   18286  200106  26.751456  32.776867  -6.025411
5   20968  199103   4.302338   9.887170  -5.584832
6   65955  199103   4.001510   9.291549  -5.290039
7   48047  199103   3.968767   9.184343  -5.215576
8   78881  200209   5.286460   0.286337   5.000123
9   69075  199103   3.575570   8.431818  -4.856248
```

---

### IntanSP

**Status**: ❌ FAILED

**Test Results**:
- Test 1 - Column names: ✅ PASSED
- Test 2 - Superset check: ❌ FAILED (Python missing 5861 Stata observations)
- Test 3 - Precision1 check: ❌ FAILED
- Test 4 - Precision2 check: ❌ FAILED

**Columns**: ['IntanSP']

**Observations**:
- Stata:  1,876,810
- Python: 1,895,046
- Common: 1,870,949

**Precision1**: 99.469% obs with diff >= 1.00e-04 (tolerance: < 0.1%)

**Precision2**: 100th percentile diff = 1.09e+01 (tolerance: < 1.00e-06)

**Missing Observations Sample**:
```
 index  permno  yyyymm   IntanSP
     0   10031  198906 -1.643571
     1   10051  199203 -0.498943
     2   10051  199204  0.295998
     3   10051  199205 -0.098516
     4   10057  197006 -0.229430
     5   10057  197007 -0.418658
     6   10057  197008 -0.386506
     7   10057  197009 -0.624340
     8   10057  197010 -0.600878
     9   10057  197011 -0.647544
```

**Feedback**:
- Num observations with diff >= TOL_DIFF_1: 1861007/1870949 (99.469%)

**Most Recent Bad Observations**:
```
   permno  yyyymm    python     stata      diff
0   10026  202412 -0.457794 -0.477482  0.019688
1   10028  202412  3.507525  3.531562 -0.024038
2   10032  202412  0.512642  0.502865  0.009777
3   10044  202412 -1.144034 -1.159631  0.015597
4   10104  202412  1.870738  1.835441  0.035298
5   10107  202412  1.319656  1.285797  0.033859
6   10138  202412 -0.241620 -0.263961  0.022341
7   10145  202412  0.018534 -0.002560  0.021094
8   10158  202412 -0.188997 -0.192551  0.003554
9   10200  202412  0.172517  0.145393  0.027125
```

**Largest Differences**:
```
   permno  yyyymm     python      stata       diff
0   81288  200709 -21.845115 -32.751595  10.906480
1   81288  200707 -15.742404 -25.690916   9.948512
2   59483  202103   7.107208  -2.339768   9.446976
3   59483  202102   5.129913  -4.188400   9.318313
4   10785  199703   8.095767  -0.876610   8.972376
5   77042  200707 -12.379881 -20.649414   8.269533
6   77393  200104   9.224737   0.967575   8.257162
7   83161  200709  -1.711984   6.531930  -8.243913
8   59483  202101   3.401558  -4.754353   8.155911
9   68320  199512  -0.951288   7.122103  -8.073391
```

---

### InvGrowth

**Status**: ❌ FAILED

**Test Results**:
- Test 1 - Column names: ✅ PASSED
- Test 2 - Superset check: ❌ FAILED (Python missing 12 Stata observations)
- Test 3 - Precision1 check: ❌ FAILED
- Test 4 - Precision2 check: ❌ FAILED

**Columns**: ['InvGrowth']

**Observations**:
- Stata:  1,973,756
- Python: 1,996,001
- Common: 1,973,744

**Precision1**: 0.316% obs with diff >= 1.00e-04 (tolerance: < 0.1%)

**Precision2**: 100th percentile diff = 3.56e-01 (tolerance: < 1.00e-06)

**Missing Observations Sample**:
```
 index  permno  yyyymm  InvGrowth
     0   93346  201206   2.103999
     1   93346  201207   2.113518
     2   93346  201208   2.113518
     3   93346  201209   2.113518
     4   93346  201210   2.110552
     5   93346  201211   2.110552
     6   93346  201212   2.110552
     7   93346  201301   2.100679
     8   93346  201302   2.100679
     9   93346  201303   2.100679
```

**Feedback**:
- Num observations with diff >= TOL_DIFF_1: 6240/1973744 (0.316%)

**Most Recent Bad Observations**:
```
   permno  yyyymm    python     stata      diff
0   10026  202506 -0.016586 -0.016432 -0.000154
1   10028  202506  0.082076  0.082246 -0.000170
2   10032  202506 -0.181998 -0.181870 -0.000129
3   10044  202506  0.166821  0.167004 -0.000183
4   10104  202506  0.092017  0.092188 -0.000172
5   10145  202506  0.015949  0.016109 -0.000160
6   10158  202506 -0.016898 -0.016743 -0.000154
7   10200  202506 -0.311530 -0.311422 -0.000108
8   10220  202506  0.074239  0.074408 -0.000169
9   10253  202506 -0.155986 -0.155853 -0.000133
```

**Largest Differences**:
```
   permno  yyyymm       python        stata      diff
0   23636  202506  2268.827824  2269.184300 -0.356476
1   23430  202504   166.582080   166.608410 -0.026330
2   23430  202505   166.582080   166.608410 -0.026330
3   21041  202504    95.303288    95.318420 -0.015132
4   21041  202505    95.303288    95.318420 -0.015132
5   88240  202506    38.725456    38.731697 -0.006241
6   14815  202504    29.532736    29.537533 -0.004797
7   14815  202505    29.532736    29.537533 -0.004797
8   14300  202506    22.319446    22.323111 -0.003665
9   23193  202506    21.111946    21.115419 -0.003473
```

---

### Investment

**Status**: ❌ FAILED

**Test Results**:
- Test 1 - Column names: ✅ PASSED
- Test 2 - Superset check: ✅ PASSED
- Test 3 - Precision1 check: ❌ FAILED
- Test 4 - Precision2 check: ❌ FAILED

**Columns**: ['Investment']

**Observations**:
- Stata:  2,411,862
- Python: 2,419,987
- Common: 2,411,862

**Precision1**: 1.504% obs with diff >= 1.00e-04 (tolerance: < 0.1%)

**Precision2**: 100th percentile diff = 3.13e+01 (tolerance: < 1.00e-06)

**Feedback**:
- Num observations with diff >= TOL_DIFF_1: 36282/2411862 (1.504%)

**Most Recent Bad Observations**:
```
   permno  yyyymm    python     stata      diff
0   22092  202607  0.917400  0.915275  0.002125
1   90979  202607  1.099284  1.081154  0.018130
2   22092  202606  0.917365  0.913000  0.004365
3   90979  202606  1.120645  1.083741  0.036904
4   12373  202605  0.000000  0.684501 -0.684501
5   12799  202605  2.904973  1.971440  0.933533
6   13534  202605  0.920208  0.918241  0.001967
7   14607  202605  0.419918  0.396650  0.023267
8   19912  202605  0.737917  0.925279 -0.187362
9   20700  202605  0.721331  0.707821  0.013510
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

**Status**: ❌ FAILED

**Test Results**:
- Test 1 - Column names: ✅ PASSED
- Test 2 - Superset check: ✅ PASSED
- Test 3 - Precision1 check: ❌ FAILED
- Test 4 - Precision2 check: ❌ FAILED

**Columns**: ['LRreversal']

**Observations**:
- Stata:  3,059,782
- Python: 4,047,630
- Common: 3,059,782

**Precision1**: 0.132% obs with diff >= 1.00e-04 (tolerance: < 0.1%)

**Precision2**: 100th percentile diff = 2.68e+01 (tolerance: < 1.00e-06)

**Feedback**:
- Num observations with diff >= TOL_DIFF_1: 4048/3059782 (0.132%)

**Most Recent Bad Observations**:
```
   permno  yyyymm    python     stata      diff
0   14051  202412 -0.911428 -0.922049  0.010620
1   18103  202412 -0.738849 -0.904301  0.165452
2   19920  202412 -0.964417 -0.982262  0.017845
3   14051  202411 -0.913693 -0.931067  0.017375
4   18103  202411 -0.676166 -0.871259  0.195093
5   19920  202411 -0.960041 -0.968153  0.008112
6   14051  202410 -0.889415 -0.911428  0.022013
7   14093  202410 -0.951807 -0.958077  0.006270
8   18103  202410 -0.571823 -0.835805  0.263982
9   19920  202410 -0.937220 -0.964417  0.027197
```

**Largest Differences**:
```
   permno  yyyymm     python      stata       diff
0   20670  200112  30.809571   4.022735  26.786837
1   15017  201803   1.640003  27.351471 -25.711468
2   20670  200109   7.517651  30.809572 -23.291921
3   15017  201802   1.119483  23.851751 -22.732268
4   15017  201801   0.610392  17.145193 -16.534801
5   15017  201712   0.349612  14.850408 -14.500796
6   20670  200107   8.919996  23.400019 -14.480023
7   32352  196704   0.249998  14.666653 -14.416655
8   63239  199407  30.272707  16.461525  13.811182
9   15017  201806  14.850408   1.161886  13.688522
```

---

### Leverage

**Status**: ❌ FAILED

**Test Results**:
- Test 1 - Column names: ✅ PASSED
- Test 2 - Superset check: ✅ PASSED
- Test 3 - Precision1 check: ✅ PASSED
- Test 4 - Precision2 check: ❌ FAILED

**Columns**: ['Leverage']

**Observations**:
- Stata:  3,014,665
- Python: 3,014,667
- Common: 3,014,665

**Precision1**: 0.001% obs with diff >= 1.00e-04 (tolerance: < 0.1%)

**Precision2**: 100th percentile diff = 5.12e-02 (tolerance: < 1.00e-06)

**Feedback**:
- Num observations with diff >= TOL_DIFF_1: 17/3014665 (0.001%)

**Most Recent Bad Observations**:
```
   permno  yyyymm       python        stata      diff
0   23033  202412     0.126271     0.111115  0.015156
1   23033  202411     0.342735     0.301598  0.041136
2   23033  202410     0.426717     0.375501  0.051216
3   23033  202409     0.412298     0.362813  0.049486
4   23033  202408     0.243269     0.214071  0.029198
5   23033  202407     0.218166     0.191981  0.026185
6   23033  202406     0.200601     0.176524  0.024077
7   13923  201511  1349.350892  1349.351000 -0.000108
8   91282  201209  4530.172220  4530.172400 -0.000180
9   91282  201208  2652.184930  2652.184800  0.000130
```

**Largest Differences**:
```
   permno  yyyymm       python        stata      diff
0   23033  202410     0.426717     0.375501  0.051216
1   23033  202409     0.412298     0.362813  0.049486
2   23033  202411     0.342735     0.301598  0.041136
3   23033  202408     0.243269     0.214071  0.029198
4   23033  202407     0.218166     0.191981  0.026185
5   23033  202406     0.200601     0.176524  0.024077
6   23033  202412     0.126271     0.111115  0.015156
7   56120  199004  4548.191088  4548.190900  0.000188
8   56120  199005  4548.191088  4548.190900  0.000188
9   91282  201209  4530.172220  4530.172400 -0.000180
```

---

### MRreversal

**Status**: ❌ FAILED

**Test Results**:
- Test 1 - Column names: ✅ PASSED
- Test 2 - Superset check: ✅ PASSED
- Test 3 - Precision1 check: ❌ FAILED
- Test 4 - Precision2 check: ❌ FAILED

**Columns**: ['MRreversal']

**Observations**:
- Stata:  3,518,261
- Python: 4,047,630
- Common: 3,518,261

**Precision1**: 0.150% obs with diff >= 1.00e-04 (tolerance: < 0.1%)

**Precision2**: 100th percentile diff = 1.16e+01 (tolerance: < 1.00e-06)

**Feedback**:
- Num observations with diff >= TOL_DIFF_1: 5267/3518261 (0.150%)

**Most Recent Bad Observations**:
```
   permno  yyyymm    python     stata      diff
0   14051  202412 -0.397438 -0.477612  0.080173
1   18103  202412  0.124620 -0.832065  0.956685
2   19920  202412 -0.869663 -0.751032 -0.118631
3   22888  202412  0.047891  0.039847  0.008044
4   14051  202411 -0.321738 -0.442272  0.120534
5   18103  202411  1.976194 -0.717398  2.693592
6   19920  202411 -0.912735 -0.671266 -0.241469
7   22888  202411  0.048214  0.047891  0.000323
8   14051  202410 -0.406779 -0.397438 -0.009341
9   14093  202410 -0.814414 -0.845252  0.030838
```

**Largest Differences**:
```
   permno  yyyymm        python      stata       diff
0   15017  201806  1.074442e+01  -0.864316  11.608738
1   91201  201910 -6.217646e-03  10.517862 -10.524080
2   15017  201712  2.673172e-01  10.744422 -10.477105
3   15017  201801  2.916670e-01  10.612906 -10.321239
4   15017  201802  6.702154e-01  10.871568 -10.201353
5   75302  199310  8.500000e+00  -0.933400   9.433400
6   15017  201803  1.209567e+00   9.984651  -8.775083
7   32352  196704 -2.538463e-07   8.400002  -8.400003
8   76442  199206  1.000001e+00   9.166671  -8.166670
9   77562  199309  6.120002e+00  -0.775281   6.895283
```

---

### MS

**Status**: ❌ FAILED

**Test Results**:
- Test 1 - Column names: ✅ PASSED
- Test 2 - Superset check: ❌ FAILED (Python missing 337 Stata observations)
- Test 3 - Precision1 check: ❌ FAILED
- Test 4 - Precision2 check: ❌ FAILED

**Columns**: ['MS']

**Observations**:
- Stata:  473,079
- Python: 473,026
- Common: 472,742

**Precision1**: 63.487% obs with diff >= 1.00e-04 (tolerance: < 0.1%)

**Precision2**: 100th percentile diff = 5.00e+00 (tolerance: < 1.00e-06)

**Missing Observations Sample**:
```
 index  permno  yyyymm  MS
     0   10145  199711   5
     1   10530  201509   6
     2   10696  199911   5
     3   10989  196610   1
     4   11017  196701   1
     5   11040  199502   4
     6   11081  201108   5
     7   11370  201301   5
     8   11403  200305   6
     9   11481  201608   3
```

**Feedback**:
- Num observations with diff >= TOL_DIFF_1: 300131/472742 (63.487%)

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
8   12060  202412       2      4    -2
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

**Precision1**: 0.000% obs with diff >= 1.00e-04 (tolerance: < 0.1%)

**Precision2**: 100th percentile diff = 0.00e+00 (tolerance: < 1.00e-06)

**Feedback**:
- Num observations with diff >= TOL_DIFF_1: 0/5033574 (0.000%)

---

### MeanRankRevGrowth

**Status**: ❌ FAILED

**Test Results**:
- Test 1 - Column names: ✅ PASSED
- Test 2 - Superset check: ✅ PASSED
- Test 3 - Precision1 check: ❌ FAILED
- Test 4 - Precision2 check: ❌ FAILED

**Columns**: ['MeanRankRevGrowth']

**Observations**:
- Stata:  2,028,817
- Python: 2,029,426
- Common: 2,028,817

**Precision1**: 12.199% obs with diff >= 1.00e-04 (tolerance: < 0.1%)

**Precision2**: 100th percentile diff = 1.33e+01 (tolerance: < 1.00e-06)

**Feedback**:
- Num observations with diff >= TOL_DIFF_1: 247486/2028817 (12.199%)

**Most Recent Bad Observations**:
```
   permno  yyyymm       python       stata       diff
0   10104  202610  2175.733333  2166.80000   8.933333
1   10104  202609  2176.933333  2169.00000   7.933333
2   10501  202609  2787.600000  2774.33330  13.266700
3   18136  202609   882.133333   878.73334   3.399993
4   21742  202609  2074.400000  2064.66670   9.733300
5   29946  202609  2499.666667  2489.73340   9.933267
6   42585  202609  2910.400000  2899.13330  11.266700
7   60097  202609  2727.866667  2719.53340   8.333267
8   82598  202609  2814.266667  2804.60010   9.666567
9   10104  202608  2175.533333  2173.60010   1.933233
```

**Largest Differences**:
```
   permno  yyyymm       python      stata       diff
0   10501  202609  2787.600000  2774.3333  13.266700
1   42585  202609  2910.400000  2899.1333  11.266700
2   29946  202609  2499.666667  2489.7334   9.933267
3   21742  202609  2074.400000  2064.6667   9.733300
4   82598  202609  2814.266667  2804.6001   9.666567
5   10104  202610  2175.733333  2166.8000   8.933333
6   60097  202609  2727.866667  2719.5334   8.333267
7   10104  202609  2176.933333  2169.0000   7.933333
8   12373  202506  2688.133333  2682.4666   5.666733
9   12373  202507  2676.600000  2670.9333   5.666700
```

---

### Mom12m

**Status**: ❌ FAILED

**Test Results**:
- Test 1 - Column names: ✅ PASSED
- Test 2 - Superset check: ✅ PASSED
- Test 3 - Precision1 check: ✅ PASSED
- Test 4 - Precision2 check: ❌ FAILED

**Columns**: ['Mom12m']

**Observations**:
- Stata:  3,713,622
- Python: 3,730,107
- Common: 3,713,622

**Precision1**: 0.000% obs with diff >= 1.00e-04 (tolerance: < 0.1%)

**Precision2**: 100th percentile diff = 4.31e-06 (tolerance: < 1.00e-06)

**Feedback**:
- Num observations with diff >= TOL_DIFF_1: 0/3713622 (0.000%)

---

### Mom12mOffSeason

**Status**: ❌ FAILED

**Test Results**:
- Test 1 - Column names: ✅ PASSED
- Test 2 - Superset check: ✅ PASSED
- Test 3 - Precision1 check: ❌ FAILED
- Test 4 - Precision2 check: ❌ FAILED

**Columns**: ['Mom12mOffSeason']

**Observations**:
- Stata:  3,865,561
- Python: 3,872,777
- Common: 3,865,561

**Precision1**: 95.893% obs with diff >= 1.00e-04 (tolerance: < 0.1%)

**Precision2**: 100th percentile diff = 2.41e+00 (tolerance: < 1.00e-06)

**Feedback**:
- Num observations with diff >= TOL_DIFF_1: 3706809/3865561 (95.893%)

**Most Recent Bad Observations**:
```
   permno  yyyymm    python     stata      diff
0   10026  202412  0.012609  0.023884 -0.011275
1   10028  202412  0.048512  0.055180 -0.006667
2   10032  202412  0.059734  0.066746 -0.007012
3   10044  202412 -0.027687 -0.032152  0.004465
4   10066  202412  0.045816  0.049737 -0.003921
5   10104  202412  0.056671  0.062988 -0.006317
6   10107  202412  0.008458  0.004700  0.003758
7   10138  202412  0.018862  0.015938  0.002924
8   10145  202412  0.017729  0.021045 -0.003316
9   10158  202412  0.061113  0.065021 -0.003908
```

**Largest Differences**:
```
   permno  yyyymm    python     stata      diff
0   58748  199211  2.324494 -0.083895  2.408390
1   16400  201911  1.681095 -0.341405  2.022499
2   53154  199406  2.140353  0.267058  1.873294
3   23199  202402  1.642566 -0.210839  1.853405
4   48072  202111  1.695673 -0.071991  1.767664
5   89301  202111  1.654405  0.032613  1.621792
6   13755  202106  1.686759  0.098126  1.588633
7   13755  202105  1.682764  0.104096  1.578668
8   23007  202311  1.428378 -0.141880  1.570258
9   13755  202104  1.672026  0.117770  1.554255
```

---

### Mom6m

**Status**: ❌ FAILED

**Test Results**:
- Test 1 - Column names: ✅ PASSED
- Test 2 - Superset check: ✅ PASSED
- Test 3 - Precision1 check: ✅ PASSED
- Test 4 - Precision2 check: ❌ FAILED

**Columns**: ['Mom6m']

**Observations**:
- Stata:  3,893,591
- Python: 3,901,671
- Common: 3,893,591

**Precision1**: 0.000% obs with diff >= 1.00e-04 (tolerance: < 0.1%)

**Precision2**: 100th percentile diff = 1.69e-06 (tolerance: < 1.00e-06)

**Feedback**:
- Num observations with diff >= TOL_DIFF_1: 0/3893591 (0.000%)

---

### Mom6mJunk

**Status**: ❌ FAILED

**Test Results**:
- Test 1 - Column names: ✅ PASSED
- Test 2 - Superset check: ❌ FAILED (Python missing 70860 Stata observations)
- Test 3 - Precision1 check: ❌ FAILED
- Test 4 - Precision2 check: ❌ FAILED

**Columns**: ['Mom6mJunk']

**Observations**:
- Stata:  391,738
- Python: 328,709
- Common: 320,878

**Precision1**: 0.284% obs with diff >= 1.00e-04 (tolerance: < 0.1%)

**Precision2**: 100th percentile diff = 1.25e+00 (tolerance: < 1.00e-06)

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
- Num observations with diff >= TOL_DIFF_1: 911/320878 (0.284%)

**Most Recent Bad Observations**:
```
   permno  yyyymm    python     stata      diff
0   90979  202401 -0.064794  0.150524 -0.215318
1   90979  202312 -0.190532  0.065445 -0.255977
2   90979  202311 -0.348997 -0.103403 -0.245594
3   90353  202310  0.379207  0.206912  0.172295
4   90756  202310  0.153710  0.297667 -0.143957
5   90979  202310 -0.478251 -0.271199 -0.207052
6   90353  202309  0.537673  0.248826  0.288847
7   90756  202309  0.434465  0.411892  0.022573
8   90979  202309 -0.290354 -0.240253 -0.050101
9   90353  202308  0.491526  0.339849  0.151677
```

**Largest Differences**:
```
   permno  yyyymm    python     stata      diff
0   10342  200001  1.736612  0.487289  1.249323
1   86360  200106 -0.469291  0.685000 -1.154291
2   69075  199304 -0.312500  0.833333 -1.145833
3   90352  201210 -0.685484  0.426830 -1.112313
4   80658  200110  1.066668  0.000000  1.066668
5   48565  199307  1.333332  0.272727  1.060605
6   24731  198604 -0.459091  0.545455 -1.004546
7   67126  199002  1.821039  0.829268  0.991771
8   83161  200409  0.763565 -0.222222  0.985787
9   79338  200206  0.933027 -0.043428  0.976455
```

---

### MomOffSeason

**Status**: ❌ FAILED

**Test Results**:
- Test 1 - Column names: ✅ PASSED
- Test 2 - Superset check: ✅ PASSED
- Test 3 - Precision1 check: ❌ FAILED
- Test 4 - Precision2 check: ❌ FAILED

**Columns**: ['MomOffSeason']

**Observations**:
- Stata:  3,396,704
- Python: 3,786,609
- Common: 3,396,704

**Precision1**: 23.110% obs with diff >= 1.00e-04 (tolerance: < 0.1%)

**Precision2**: 100th percentile diff = 4.11e+00 (tolerance: < 1.00e-06)

**Feedback**:
- Num observations with diff >= TOL_DIFF_1: 784983/3396704 (23.110%)

**Most Recent Bad Observations**:
```
   permno  yyyymm    python     stata      diff
0   10066  202412 -0.042677 -0.048228  0.005551
1   11153  202412  0.031101  0.040138 -0.009037
2   11379  202412  0.016542  0.014271  0.002272
3   12799  202412  0.025892  0.074968 -0.049076
4   12928  202412 -0.042901 -0.024719 -0.018182
5   13563  202412  0.001611  0.005397 -0.003785
6   13828  202412  0.109483  0.023601  0.085882
7   13878  202412  0.012121  0.022194 -0.010073
8   14051  202412  0.010921 -0.003499  0.014420
9   14469  202412  0.009002 -0.012774  0.021776
```

**Largest Differences**:
```
   permno  yyyymm    python     stata      diff
0   89169  202105 -0.057384 -4.171327  4.113943
1   44230  198407  0.003680 -1.585526  1.589206
2   92161  199008 -0.022376 -1.574922  1.552546
3   82810  200509  0.111008 -1.145503  1.256511
4   79704  200304  0.014714  1.166667 -1.151953
5   77324  200102 -0.019919  1.086957 -1.106876
6   10685  199512  0.059764 -1.021461  1.081225
7   10097  199202 -0.069398  1.000000 -1.069398
8   78414  198610  0.260000  1.300000 -1.040000
9   80054  200306  0.012536 -1.002423  1.014959
```

---

### MomOffSeason06YrPlus

**Status**: ❌ FAILED

**Test Results**:
- Test 1 - Column names: ✅ PASSED
- Test 2 - Superset check: ✅ PASSED
- Test 3 - Precision1 check: ❌ FAILED
- Test 4 - Precision2 check: ❌ FAILED

**Columns**: ['MomOffSeason06YrPlus']

**Observations**:
- Stata:  2,425,319
- Python: 2,674,726
- Common: 2,425,319

**Precision1**: 27.031% obs with diff >= 1.00e-04 (tolerance: < 0.1%)

**Precision2**: 100th percentile diff = 1.06e+01 (tolerance: < 1.00e-06)

**Feedback**:
- Num observations with diff >= TOL_DIFF_1: 655599/2425319 (27.031%)

**Most Recent Bad Observations**:
```
   permno  yyyymm    python     stata      diff
0   11379  202412 -0.015023 -0.019014  0.003992
1   11990  202412  0.020602  0.006271  0.014331
2   12146  202412  0.004069  0.004235 -0.000166
3   12592  202412 -0.016859 -0.028323  0.011464
4   12799  202412  0.012784  0.023379 -0.010595
5   13563  202412 -0.069195 -0.048507 -0.020688
6   13828  202412 -0.006820 -0.008100  0.001281
7   13878  202412  0.015936  0.019389 -0.003452
8   14051  202412 -0.052086 -0.051790 -0.000296
9   14617  202412  0.001636  0.019434 -0.017798
```

**Largest Differences**:
```
   permno  yyyymm     python      stata       diff
0   13755  202011   5.298622  15.892301 -10.593679
1   13755  202111  10.641539  15.892301  -5.250762
2   13755  202211  10.641539  15.892301  -5.250762
3   83382  200510  -0.123874  -4.872470   4.748596
4   10685  199412  -0.122235  -3.649201   3.526966
5   86237  201012  -0.231136   3.244835  -3.475970
6   81728  200612  -0.273135  -3.352354   3.079219
7   76356  198510   0.022956  -2.300340   2.323296
8   12715  198603  -0.064209   2.214316  -2.278525
9   76356  198509   0.023664  -2.158295   2.181959
```

---

### MomOffSeason11YrPlus

**Status**: ❌ FAILED

**Test Results**:
- Test 1 - Column names: ✅ PASSED
- Test 2 - Superset check: ❌ FAILED (Python missing 45 Stata observations)
- Test 3 - Precision1 check: ❌ FAILED
- Test 4 - Precision2 check: ❌ FAILED

**Columns**: ['MomOffSeason11YrPlus']

**Observations**:
- Stata:  1,677,532
- Python: 1,830,162
- Common: 1,677,487

**Precision1**: 26.203% obs with diff >= 1.00e-04 (tolerance: < 0.1%)

**Precision2**: 100th percentile diff = 4.45e+00 (tolerance: < 1.00e-06)

**Missing Observations Sample**:
```
 index  permno  yyyymm  MomOffSeason11YrPlus
     0   10116  201506             -0.272727
     1   11803  201902             -0.177570
     2   12221  200405             -0.400000
     3   14154  199105             -0.111111
     4   14761  201507             -0.136364
     5   17814  198311              0.034759
     6   19828  198208             -0.165289
     7   22074  199308             -0.181818
     8   23595  197203             -0.150000
     9   24918  199102              0.115789
```

**Feedback**:
- Num observations with diff >= TOL_DIFF_1: 439557/1677487 (26.203%)

**Most Recent Bad Observations**:
```
   permno  yyyymm    python     stata      diff
0   10028  202412 -0.018208  0.011574 -0.029782
1   10158  202412 -0.002198 -0.002330  0.000132
2   10220  202412  0.004441  0.004713 -0.000272
3   10966  202412  0.031195  0.024496  0.006699
4   11379  202412  0.041162  0.029216  0.011945
5   11636  202412 -0.077253 -0.064470 -0.012784
6   11664  202412 -0.004556 -0.004829  0.000273
7   11803  202412 -0.012306 -0.000875 -0.011431
8   12009  202412  0.006002  0.006362 -0.000360
9   12049  202412 -0.013314 -0.014129  0.000815
```

**Largest Differences**:
```
   permno  yyyymm    python     stata      diff
0   78892  201708  4.972035  0.525000  4.447035
1   82848  202308 -3.450183 -0.381590 -3.068593
2   12221  200404 -3.039837 -0.265218 -2.774619
3   11803  201112  0.032250 -2.611104  2.643353
4   77729  200404  0.016219 -2.373474  2.389693
5   82163  202008 -2.650554 -0.317919 -2.332635
6   78892  201707  2.583296  0.294444  2.288852
7   82621  202105 -1.917791  0.363989 -2.281780
8   33136  197712 -0.022672  2.247807 -2.270478
9   30744  200511  2.796191  0.541667  2.254524
```

---

### MomOffSeason16YrPlus

**Status**: ❌ FAILED

**Test Results**:
- Test 1 - Column names: ✅ PASSED
- Test 2 - Superset check: ✅ PASSED
- Test 3 - Precision1 check: ❌ FAILED
- Test 4 - Precision2 check: ❌ FAILED

**Columns**: ['MomOffSeason16YrPlus']

**Observations**:
- Stata:  1,027,449
- Python: 1,049,061
- Common: 1,027,449

**Precision1**: 14.632% obs with diff >= 1.00e-04 (tolerance: < 0.1%)

**Precision2**: 100th percentile diff = 2.15e-01 (tolerance: < 1.00e-06)

**Feedback**:
- Num observations with diff >= TOL_DIFF_1: 150337/1027449 (14.632%)

**Most Recent Bad Observations**:
```
   permno  yyyymm    python     stata      diff
0   10028  202412  0.001283  0.008196 -0.006914
1   10693  202412  0.003905  0.008496 -0.004591
2   10779  202412  0.013452  0.013265  0.000187
3   11379  202412  0.001526  0.014200 -0.012674
4   11636  202412 -0.005848 -0.029687  0.023838
5   21020  202412  0.022419  0.025402 -0.002983
6   32791  202412  0.014337 -0.002500  0.016837
7   48072  202412  0.000331 -0.002034  0.002365
8   52231  202412 -0.018406 -0.045180  0.026774
9   68145  202412 -0.101777 -0.091793 -0.009984
```

**Largest Differences**:
```
   permno  yyyymm    python     stata      diff
0   41515  199310  0.217161  0.001904  0.215256
1   41515  199008  0.180211 -0.025009  0.205220
2   41515  198908  0.135280 -0.066358  0.201638
3   41515  199108  0.172863 -0.017675  0.190538
4   41515  199309  0.222858  0.038549  0.184308
5   41515  199308  0.202055  0.033127  0.168928
6   41515  199208  0.153092 -0.015305  0.168397
7   41515  199210  0.178610  0.013972  0.164639
8   41515  199107  0.179346  0.024637  0.154709
9   41515  199007  0.181810  0.029118  0.152692
```

---

### MomRev

**Status**: ❌ FAILED

**Test Results**:
- Test 1 - Column names: ✅ PASSED
- Test 2 - Superset check: ❌ FAILED (Python missing 3313 Stata observations)
- Test 3 - Precision1 check: ✅ PASSED
- Test 4 - Precision2 check: ✅ PASSED

**Columns**: ['MomRev']

**Observations**:
- Stata:  262,210
- Python: 266,161
- Common: 258,897

**Precision1**: 0.000% obs with diff >= 1.00e-04 (tolerance: < 0.1%)

**Precision2**: 100th percentile diff = 0.00e+00 (tolerance: < 1.00e-06)

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
- Num observations with diff >= TOL_DIFF_1: 0/258897 (0.000%)

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

**Precision1**: 0.000% obs with diff >= 1.00e-04 (tolerance: < 0.1%)

**Precision2**: 100th percentile diff = 6.00e-07 (tolerance: < 1.00e-06)

**Feedback**:
- Num observations with diff >= TOL_DIFF_1: 0/3398424 (0.000%)

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

**Precision1**: 0.000% obs with diff >= 1.00e-04 (tolerance: < 0.1%)

**Precision2**: 100th percentile diff = 3.67e-07 (tolerance: < 1.00e-06)

**Feedback**:
- Num observations with diff >= TOL_DIFF_1: 0/2432862 (0.000%)

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

**Precision1**: 0.000% obs with diff >= 1.00e-04 (tolerance: < 0.1%)

**Precision2**: 100th percentile diff = 2.00e-07 (tolerance: < 1.00e-06)

**Feedback**:
- Num observations with diff >= TOL_DIFF_1: 0/1680518 (0.000%)

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

**Precision1**: 0.000% obs with diff >= 1.00e-04 (tolerance: < 0.1%)

**Precision2**: 100th percentile diff = 2.00e-07 (tolerance: < 1.00e-06)

**Feedback**:
- Num observations with diff >= TOL_DIFF_1: 0/1194902 (0.000%)

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

**Precision1**: 0.000% obs with diff >= 1.00e-04 (tolerance: < 0.1%)

**Precision2**: 100th percentile diff = 5.00e-07 (tolerance: < 1.00e-06)

**Feedback**:
- Num observations with diff >= TOL_DIFF_1: 0/3718320 (0.000%)

---

### MomVol

**Status**: ❌ FAILED

**Test Results**:
- Test 1 - Column names: ✅ PASSED
- Test 2 - Superset check: ❌ FAILED (Python missing 28 Stata observations)
- Test 3 - Precision1 check: ❌ FAILED
- Test 4 - Precision2 check: ❌ FAILED

**Columns**: ['MomVol']

**Observations**:
- Stata:  1,095,615
- Python: 1,098,011
- Common: 1,095,587

**Precision1**: 0.417% obs with diff >= 1.00e-04 (tolerance: < 0.1%)

**Precision2**: 100th percentile diff = 1.00e+00 (tolerance: < 1.00e-06)

**Missing Observations Sample**:
```
 index  permno  yyyymm  MomVol
     0   11795  199011       5
     1   18365  202303       2
     2   21055  196909       5
     3   23683  196512       1
     4   27078  197208       5
     5   27860  198309       3
     6   29532  196906       6
     7   33478  196908      10
     8   36767  196906       1
     9   39810  197312       8
```

**Feedback**:
- Num observations with diff >= TOL_DIFF_1: 4567/1095587 (0.417%)

**Most Recent Bad Observations**:
```
   permno  yyyymm  python  stata  diff
0   19495  202412     9.0      8   1.0
1   20867  202412     6.0      5   1.0
2   22293  202412     8.0      7   1.0
3   46886  202412     3.0      2   1.0
4   85035  202412     2.0      1   1.0
5   90386  202412     4.0      3   1.0
6   90993  202412     7.0      6   1.0
7   13586  202411     9.0      8   1.0
8   34817  202411     4.0      3   1.0
9   93289  202411     3.0      2   1.0
```

**Largest Differences**:
```
   permno  yyyymm  python  stata  diff
0   10006  194301     4.0      3   1.0
1   10006  195503     8.0      7   1.0
2   10014  196802    10.0      9   1.0
3   10064  198901     4.0      3   1.0
4   10066  198710     2.0      1   1.0
5   10071  199204     4.0      3   1.0
6   10078  200911     3.0      2   1.0
7   10089  198908     8.0      7   1.0
8   10102  193202     8.0      7   1.0
9   10102  193210     7.0      6   1.0
```

---

### NetDebtPrice

**Status**: ❌ FAILED

**Test Results**:
- Test 1 - Column names: ✅ PASSED
- Test 2 - Superset check: ❌ FAILED (Python missing 1 Stata observations)
- Test 3 - Precision1 check: ✅ PASSED
- Test 4 - Precision2 check: ❌ FAILED

**Columns**: ['NetDebtPrice']

**Observations**:
- Stata:  1,425,163
- Python: 1,426,019
- Common: 1,425,162

**Precision1**: 0.001% obs with diff >= 1.00e-04 (tolerance: < 0.1%)

**Precision2**: 100th percentile diff = 4.24e-02 (tolerance: < 1.00e-06)

**Missing Observations Sample**:
```
 index  permno  yyyymm  NetDebtPrice
     0   23033  202412     -0.345379
```

**Feedback**:
- Num observations with diff >= TOL_DIFF_1: 8/1425162 (0.001%)

**Most Recent Bad Observations**:
```
   permno  yyyymm    python     stata      diff
0   23033  202411 -0.933942 -0.937456  0.003514
1   23033  202410 -1.162791 -1.167166  0.004375
2   23033  202409 -1.123501 -1.127728  0.004227
3   23033  202408 -0.662900 -0.665395  0.002494
4   23033  202407 -0.594496 -0.596733  0.002237
5   23033  202406 -0.546632 -0.548689  0.002057
6   15075  202207  1.858736  1.901128 -0.042391
7   15075  202206  1.451804  1.484914 -0.033110
```

**Largest Differences**:
```
   permno  yyyymm    python     stata      diff
0   15075  202207  1.858736  1.901128 -0.042391
1   15075  202206  1.451804  1.484914 -0.033110
2   23033  202410 -1.162791 -1.167166  0.004375
3   23033  202409 -1.123501 -1.127728  0.004227
4   23033  202411 -0.933942 -0.937456  0.003514
5   23033  202408 -0.662900 -0.665395  0.002494
6   23033  202407 -0.594496 -0.596733  0.002237
7   23033  202406 -0.546632 -0.548689  0.002057
```

---

### OScore

**Status**: ❌ FAILED

**Test Results**:
- Test 1 - Column names: ✅ PASSED
- Test 2 - Superset check: ❌ FAILED (Python missing 522 Stata observations)
- Test 3 - Precision1 check: ✅ PASSED
- Test 4 - Precision2 check: ✅ PASSED

**Columns**: ['OScore']

**Observations**:
- Stata:  1,197,546
- Python: 1,197,639
- Common: 1,197,024

**Precision1**: 0.000% obs with diff >= 1.00e-04 (tolerance: < 0.1%)

**Precision2**: 100th percentile diff = 0.00e+00 (tolerance: < 1.00e-06)

**Missing Observations Sample**:
```
 index  permno  yyyymm  OScore
     0   10103  198008       0
     1   10302  201603       0
     2   10371  200905       0
     3   10513  199802       0
     4   10645  200203       0
     5   10779  200206       0
     6   11038  201102       0
     7   11607  200301       0
     8   11995  201610       0
     9   12030  201301       0
```

**Feedback**:
- Num observations with diff >= TOL_DIFF_1: 0/1197024 (0.000%)

---

### OperProf

**Status**: ❌ FAILED

**Test Results**:
- Test 1 - Column names: ✅ PASSED
- Test 2 - Superset check: ✅ PASSED
- Test 3 - Precision1 check: ✅ PASSED
- Test 4 - Precision2 check: ❌ FAILED

**Columns**: ['OperProf']

**Observations**:
- Stata:  1,407,636
- Python: 1,714,647
- Common: 1,407,636

**Precision1**: 0.024% obs with diff >= 1.00e-04 (tolerance: < 0.1%)

**Precision2**: 100th percentile diff = 2.51e-01 (tolerance: < 1.00e-06)

**Feedback**:
- Num observations with diff >= TOL_DIFF_1: 333/1407636 (0.024%)

**Most Recent Bad Observations**:
```
   permno  yyyymm     python      stata      diff
0   12373  202412  -0.062563   0.019658 -0.082221
1   15862  202412   0.351910   0.350951  0.000958
2   18649  202412   1.402114   1.408908 -0.006794
3   20558  202412   0.070054   0.070885 -0.000831
4   22096  202412   0.381122   0.377095  0.004026
5   57817  202412   1.145047   1.182783 -0.037736
6   82702  202412  12.779030  12.527678  0.251352
7   85627  202412   0.430317   0.428187  0.002130
8   87077  202412   0.126221   0.121154  0.005068
9   87471  202412   0.493898   0.492247  0.001651
```

**Largest Differences**:
```
   permno  yyyymm     python      stata      diff
0   82702  202406  12.779030  12.527678  0.251352
1   82702  202407  12.779030  12.527678  0.251352
2   82702  202408  12.779030  12.527678  0.251352
3   82702  202409  12.779030  12.527678  0.251352
4   82702  202410  12.779030  12.527678  0.251352
5   82702  202411  12.779030  12.527678  0.251352
6   82702  202412  12.779030  12.527678  0.251352
7   22096  202206   0.412338   0.278429  0.133909
8   22096  202207   0.412338   0.278429  0.133909
9   22096  202208   0.412338   0.278429  0.133909
```

---

### OperProfRD

**Status**: ❌ FAILED

**Test Results**:
- Test 1 - Column names: ✅ PASSED
- Test 2 - Superset check: ✅ PASSED
- Test 3 - Precision1 check: ✅ PASSED
- Test 4 - Precision2 check: ❌ FAILED

**Columns**: ['OperProfRD']

**Observations**:
- Stata:  2,097,471
- Python: 2,389,629
- Common: 2,097,471

**Precision1**: 0.009% obs with diff >= 1.00e-04 (tolerance: < 0.1%)

**Precision2**: 100th percentile diff = 4.41e-02 (tolerance: < 1.00e-06)

**Feedback**:
- Num observations with diff >= TOL_DIFF_1: 190/2097471 (0.009%)

**Most Recent Bad Observations**:
```
   permno  yyyymm    python     stata      diff
0   15203  202412  0.102819  0.104090 -0.001270
1   18649  202412  0.115272  0.115681 -0.000409
2   22096  202412  0.122114  0.121142  0.000972
3   23033  202412 -0.511259 -0.467153 -0.044106
4   23415  202412 -0.173433 -0.186789  0.013356
5   57817  202412  0.132757  0.136547 -0.003790
6   82702  202412  0.189531  0.188100  0.001432
7   85627  202412  0.105842  0.105488  0.000354
8   87471  202412  0.257437  0.256701  0.000736
9   90177  202412  0.261965  0.304778 -0.042813
```

**Largest Differences**:
```
   permno  yyyymm    python     stata      diff
0   23033  202406 -0.511259 -0.467153 -0.044106
1   23033  202407 -0.511259 -0.467153 -0.044106
2   23033  202408 -0.511259 -0.467153 -0.044106
3   23033  202409 -0.511259 -0.467153 -0.044106
4   23033  202410 -0.511259 -0.467153 -0.044106
5   23033  202411 -0.511259 -0.467153 -0.044106
6   23033  202412 -0.511259 -0.467153 -0.044106
7   90177  202406  0.261965  0.304778 -0.042813
8   90177  202407  0.261965  0.304778 -0.042813
9   90177  202408  0.261965  0.304778 -0.042813
```

---

### OptionVolume1

**Status**: ❌ FAILED

**Test Results**:
- Test 1 - Column names: ✅ PASSED
- Test 2 - Superset check: ❌ FAILED (Python missing 6151 Stata observations)
- Test 3 - Precision1 check: ❌ FAILED
- Test 4 - Precision2 check: ❌ FAILED

**Columns**: ['OptionVolume1']

**Observations**:
- Stata:  855,113
- Python: 852,949
- Common: 848,962

**Precision1**: 3.332% obs with diff >= 1.00e-04 (tolerance: < 0.1%)

**Precision2**: 100th percentile diff = 5.42e+03 (tolerance: < 1.00e-06)

**Missing Observations Sample**:
```
 index  permno  yyyymm  OptionVolume1
     0   10353  199602      398.64133
     1   10353  199603      391.94232
     2   10353  199604      739.59509
     3   10353  199605      573.88220
     4   10353  199606      579.58887
     5   10353  199607      638.34601
     6   10353  199608      395.64926
     7   10353  199609      912.85107
     8   10353  199610      811.50128
     9   10353  199611      545.16467
```

**Feedback**:
- Num observations with diff >= TOL_DIFF_1: 28285/848962 (3.332%)

**Most Recent Bad Observations**:
```
   permno  yyyymm        python       stata      diff
0   10066  202308   6985.365854   6985.3657  0.000154
1   10104  202308   7407.255092   7407.2549  0.000192
2   10516  202308   2153.763010   2153.7629  0.000110
3   11481  202308  10743.031203  10743.0310  0.000203
4   12076  202308   3009.445408   3009.4453  0.000108
5   12369  202308   5063.518855   5063.5190 -0.000145
6   12490  202308   8942.986110   8942.9863 -0.000190
7   12919  202308  21867.801781  21867.8030 -0.001219
8   13108  202308   9870.928357   9870.9287 -0.000343
9   13303  202308   2148.541114   2148.5410  0.000114
```

**Largest Differences**:
```
   permno  yyyymm      python      stata         diff
0   48506  200712    9.991014  5434.7178 -5424.726786
1   48506  201105    7.529478  5349.4653 -5341.935822
2   48506  200706   38.071940  5158.9268 -5120.854860
3   89644  200503  256.329917  5119.5859 -4863.255983
4   89644  200511   84.272591  4918.0000 -4833.727409
5   48506  200804    2.983534  4770.9453 -4767.961766
6   89644  200412  296.809774  4398.9888 -4102.179026
7   48506  200710    9.286592  4057.5178 -4048.231208
8   48506  200805    6.384982  3965.9922 -3959.607218
9   89644  200410  104.604516  4031.5183 -3926.913784
```

---

### OptionVolume2

**Status**: ❌ FAILED

**Test Results**:
- Test 1 - Column names: ✅ PASSED
- Test 2 - Superset check: ❌ FAILED (Python missing 6070 Stata observations)
- Test 3 - Precision1 check: ✅ PASSED
- Test 4 - Precision2 check: ❌ FAILED

**Columns**: ['OptionVolume2']

**Observations**:
- Stata:  843,512
- Python: 841,828
- Common: 837,442

**Precision1**: 0.068% obs with diff >= 1.00e-04 (tolerance: < 0.1%)

**Precision2**: 100th percentile diff = 1.24e+02 (tolerance: < 1.00e-06)

**Missing Observations Sample**:
```
 index  permno  yyyymm  OptionVolume2
     0   10353  199603       0.983195
     1   10353  199604       1.871010
     2   10353  199605       1.125128
     3   10353  199606       1.101848
     4   10353  199607       1.189324
     5   10353  199608       0.714599
     6   10353  199609       1.650226
     7   10353  199610       1.268000
     8   10353  199611       0.836181
     9   10353  199612       0.884687
```

**Feedback**:
- Num observations with diff >= TOL_DIFF_1: 569/837442 (0.068%)

**Most Recent Bad Observations**:
```
   permno  yyyymm        python         stata      diff
0   17901  202308      0.002809      0.002142  0.000668
1   20548  202308      0.034696      0.026375  0.008321
2   20548  202307      2.427039      1.766302  0.660737
3   21369  202307  17723.535343  17723.535000  0.000343
4   91135  202307      1.260762      1.013812  0.246951
5   20548  202306     12.532131     11.516562  1.015569
6   91135  202306      0.967417      0.507153  0.460264
7   20548  202305      0.531441      0.552066 -0.020626
8   20548  202304      1.384088      2.127048 -0.742960
9   12789  202212      0.653939      1.692765 -1.038826
```

**Largest Differences**:
```
   permno  yyyymm     python       stata        diff
0   87043  202004   0.154464  124.352980 -124.198516
1   10942  201112   0.047394   53.250633  -53.203239
2   77763  202002   0.634055   21.281256  -20.647201
3   89397  201012   1.535987   19.085653  -17.549666
4   48506  201801  18.401057    0.882653   17.518404
5   12473  201706   0.084918   15.179537  -15.094619
6   90352  201301  31.025911   16.048969   14.976942
7   48506  201208  15.819309    1.329106   14.490203
8   10051  201902   1.491168   13.382537  -11.891369
9   51596  199905   0.129471   11.443895  -11.314424
```

---

### OrderBacklog

**Status**: ❌ FAILED

**Test Results**:
- Test 1 - Column names: ✅ PASSED
- Test 2 - Superset check: ✅ PASSED
- Test 3 - Precision1 check: ✅ PASSED
- Test 4 - Precision2 check: ❌ FAILED

**Columns**: ['OrderBacklog']

**Observations**:
- Stata:  634,164
- Python: 637,317
- Common: 634,164

**Precision1**: 0.000% obs with diff >= 1.00e-04 (tolerance: < 0.1%)

**Precision2**: 100th percentile diff = 2.71e-06 (tolerance: < 1.00e-06)

**Feedback**:
- Num observations with diff >= TOL_DIFF_1: 0/634164 (0.000%)

---

### OrderBacklogChg

**Status**: ❌ FAILED

**Test Results**:
- Test 1 - Column names: ✅ PASSED
- Test 2 - Superset check: ✅ PASSED
- Test 3 - Precision1 check: ✅ PASSED
- Test 4 - Precision2 check: ❌ FAILED

**Columns**: ['OrderBacklogChg']

**Observations**:
- Stata:  564,785
- Python: 569,589
- Common: 564,785

**Precision1**: 0.001% obs with diff >= 1.00e-04 (tolerance: < 0.1%)

**Precision2**: 100th percentile diff = 4.44e-02 (tolerance: < 1.00e-06)

**Feedback**:
- Num observations with diff >= TOL_DIFF_1: 4/564785 (0.001%)

**Most Recent Bad Observations**:
```
   permno  yyyymm    python     stata      diff
0   79901  198611 -0.891559 -0.847121 -0.044438
1   79901  198610 -0.891559 -0.847121 -0.044438
2   79901  198609 -0.891559 -0.847121 -0.044438
3   79901  198608 -0.891559 -0.847121 -0.044438
```

**Largest Differences**:
```
   permno  yyyymm    python     stata      diff
0   79901  198608 -0.891559 -0.847121 -0.044438
1   79901  198609 -0.891559 -0.847121 -0.044438
2   79901  198610 -0.891559 -0.847121 -0.044438
3   79901  198611 -0.891559 -0.847121 -0.044438
```

---

### PS

**Status**: ❌ FAILED

**Test Results**:
- Test 1 - Column names: ✅ PASSED
- Test 2 - Superset check: ❌ FAILED (Python missing 3 Stata observations)
- Test 3 - Precision1 check: ❌ FAILED
- Test 4 - Precision2 check: ❌ FAILED

**Columns**: ['PS']

**Observations**:
- Stata:  463,944
- Python: 464,340
- Common: 463,941

**Precision1**: 17.876% obs with diff >= 1.00e-04 (tolerance: < 0.1%)

**Precision2**: 100th percentile diff = 5.00e+00 (tolerance: < 1.00e-06)

**Missing Observations Sample**:
```
 index  permno  yyyymm  PS
     0   23033  202409   5
     1   23033  202410   5
     2   23033  202411   5
```

**Feedback**:
- Num observations with diff >= TOL_DIFF_1: 82936/463941 (17.876%)

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

### PctAcc

**Status**: ❌ FAILED

**Test Results**:
- Test 1 - Column names: ✅ PASSED
- Test 2 - Superset check: ✅ PASSED
- Test 3 - Precision1 check: ✅ PASSED
- Test 4 - Precision2 check: ❌ FAILED

**Columns**: ['PctAcc']

**Observations**:
- Stata:  3,174,456
- Python: 3,179,478
- Common: 3,174,456

**Precision1**: 0.003% obs with diff >= 1.00e-04 (tolerance: < 0.1%)

**Precision2**: 100th percentile diff = 1.01e+01 (tolerance: < 1.00e-06)

**Feedback**:
- Num observations with diff >= TOL_DIFF_1: 84/3174456 (0.003%)

**Most Recent Bad Observations**:
```
   permno  yyyymm    python     stata       diff
0   87381  202605 -4.900082  5.162455 -10.062537
1   90490  202605 -0.046488 -0.055116   0.008628
2   87381  202604 -4.900082  5.162455 -10.062537
3   90490  202604 -0.046488 -0.055116   0.008628
4   87381  202603 -4.900082  5.162455 -10.062537
5   90490  202603 -0.046488 -0.055116   0.008628
6   87381  202602 -4.900082  5.162455 -10.062537
7   90490  202602 -0.046488 -0.055116   0.008628
8   87381  202601 -4.900082  5.162455 -10.062537
9   90490  202601 -0.046488 -0.055116   0.008628
```

**Largest Differences**:
```
   permno  yyyymm    python     stata       diff
0   87381  202506 -4.900082  5.162455 -10.062537
1   87381  202507 -4.900082  5.162455 -10.062537
2   87381  202508 -4.900082  5.162455 -10.062537
3   87381  202509 -4.900082  5.162455 -10.062537
4   87381  202510 -4.900082  5.162455 -10.062537
5   87381  202511 -4.900082  5.162455 -10.062537
6   87381  202512 -4.900082  5.162455 -10.062537
7   87381  202601 -4.900082  5.162455 -10.062537
8   87381  202602 -4.900082  5.162455 -10.062537
9   87381  202603 -4.900082  5.162455 -10.062537
```

---

### PctTotAcc

**Status**: ❌ FAILED

**Test Results**:
- Test 1 - Column names: ✅ PASSED
- Test 2 - Superset check: ✅ PASSED
- Test 3 - Precision1 check: ✅ PASSED
- Test 4 - Precision2 check: ❌ FAILED

**Columns**: ['PctTotAcc']

**Observations**:
- Stata:  2,412,359
- Python: 2,413,703
- Common: 2,412,359

**Precision1**: 0.015% obs with diff >= 1.00e-04 (tolerance: < 0.1%)

**Precision2**: 100th percentile diff = 2.81e+00 (tolerance: < 1.00e-06)

**Feedback**:
- Num observations with diff >= TOL_DIFF_1: 360/2412359 (0.015%)

**Most Recent Bad Observations**:
```
   permno  yyyymm    python     stata      diff
0   10104  202610  0.654585  1.035763 -0.381178
1   10104  202609  0.654585  1.035763 -0.381178
2   21742  202609  0.642167  0.780100 -0.137933
3   42585  202609 -1.375853 -1.004469 -0.371384
4   60097  202609  0.179108  0.948949 -0.769841
5   10104  202608  0.654585  1.035763 -0.381178
6   12082  202608 -0.911967 -0.985668  0.073701
7   14888  202608  1.531328  1.757867 -0.226539
8   18298  202608 -1.240911  1.567999 -2.808910
9   21742  202608  0.642167  0.780100 -0.137933
```

**Largest Differences**:
```
   permno  yyyymm    python     stata     diff
0   18298  202509 -1.240911  1.567999 -2.80891
1   18298  202510 -1.240911  1.567999 -2.80891
2   18298  202511 -1.240911  1.567999 -2.80891
3   18298  202512 -1.240911  1.567999 -2.80891
4   18298  202601 -1.240911  1.567999 -2.80891
5   18298  202602 -1.240911  1.567999 -2.80891
6   18298  202603 -1.240911  1.567999 -2.80891
7   18298  202604 -1.240911  1.567999 -2.80891
8   18298  202605 -1.240911  1.567999 -2.80891
9   18298  202606 -1.240911  1.567999 -2.80891
```

---

### PredictedFE

**Status**: ❌ FAILED

**Test Results**:
- Test 1 - Column names: ✅ PASSED
- Test 2 - Superset check: ❌ FAILED (Python missing 1320 Stata observations)
- Test 3 - Precision1 check: ❌ FAILED
- Test 4 - Precision2 check: ❌ FAILED

**Columns**: ['PredictedFE']

**Observations**:
- Stata:  491,508
- Python: 635,292
- Common: 490,188

**Precision1**: 98.703% obs with diff >= 1.00e-04 (tolerance: < 0.1%)

**Precision2**: 100th percentile diff = 5.08e-02 (tolerance: < 1.00e-06)

**Missing Observations Sample**:
```
 index  permno  yyyymm  PredictedFE
     0   12473  201806    -0.041659
     1   12473  201807    -0.041659
     2   12473  201808    -0.041659
     3   12473  201809    -0.041659
     4   12473  201810    -0.041659
     5   12473  201811    -0.041659
     6   12473  201812    -0.041659
     7   12473  201901    -0.041659
     8   12473  201902    -0.041659
     9   12473  201903    -0.041659
```

**Feedback**:
- Num observations with diff >= TOL_DIFF_1: 483828/490188 (98.703%)

**Most Recent Bad Observations**:
```
   permno  yyyymm    python     stata      diff
0   10107  202505  0.074906  0.078498 -0.003592
1   10145  202505  0.028429  0.040432 -0.012003
2   10200  202505  0.121830  0.113642  0.008188
3   10397  202505  0.063543  0.049793  0.013750
4   10606  202505  0.042676  0.044046 -0.001370
5   10693  202505  0.034107  0.036774 -0.002667
6   10696  202505  0.116063  0.105464  0.010598
7   11308  202505  0.059996  0.072780 -0.012784
8   11403  202505  0.086531  0.090274 -0.003744
9   11547  202505  0.088011  0.076702  0.011310
```

**Largest Differences**:
```
   permno  yyyymm    python     stata      diff
0   77496  202306  0.035265  0.086091 -0.050826
1   77496  202307  0.035265  0.086091 -0.050826
2   77496  202308  0.035265  0.086091 -0.050826
3   77496  202309  0.035265  0.086091 -0.050826
4   77496  202310  0.035265  0.086091 -0.050826
5   77496  202311  0.035265  0.086091 -0.050826
6   77496  202312  0.035265  0.086091 -0.050826
7   77496  202401  0.035265  0.086091 -0.050826
8   77496  202402  0.035265  0.086091 -0.050826
9   77496  202403  0.035265  0.086091 -0.050826
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

**Precision1**: 0.000% obs with diff >= 1.00e-04 (tolerance: < 0.1%)

**Precision2**: 100th percentile diff = 9.12e-07 (tolerance: < 1.00e-06)

**Feedback**:
- Num observations with diff >= TOL_DIFF_1: 0/4029252 (0.000%)

---

### PriceDelayRsq

**Status**: ❌ FAILED

**Test Results**:
- Test 1 - Column names: ✅ PASSED
- Test 2 - Superset check: ✅ PASSED
- Test 3 - Precision1 check: ❌ FAILED
- Test 4 - Precision2 check: ❌ FAILED

**Columns**: ['PriceDelayRsq']

**Observations**:
- Stata:  4,630,424
- Python: 4,636,840
- Common: 4,630,424

**Precision1**: 4.251% obs with diff >= 1.00e-04 (tolerance: < 0.1%)

**Precision2**: 100th percentile diff = 9.57e-01 (tolerance: < 1.00e-06)

**Feedback**:
- Num observations with diff >= TOL_DIFF_1: 196832/4630424 (4.251%)

**Most Recent Bad Observations**:
```
   permno  yyyymm    python     stata      diff
0   10044  202406  0.296513  0.296391  0.000121
1   12017  202406  0.331738  0.331886 -0.000148
2   12059  202406  0.192970  0.193290 -0.000321
3   12064  202406  0.570412  0.570834 -0.000422
4   12078  202406  0.505508  0.505373  0.000135
5   12367  202406  0.272814  0.272923 -0.000109
6   12397  202406  0.352673  0.352791 -0.000118
7   12487  202406  0.569529  0.569774 -0.000245
8   12488  202406  0.382174  0.382441 -0.000267
9   12500  202406  0.283914  0.284215 -0.000301
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
- Test 3 - Precision1 check: ❌ FAILED
- Test 4 - Precision2 check: ❌ FAILED

**Columns**: ['PriceDelaySlope']

**Observations**:
- Stata:  4,630,424
- Python: 4,636,840
- Common: 4,630,424

**Precision1**: 11.659% obs with diff >= 1.00e-04 (tolerance: < 0.1%)

**Precision2**: 100th percentile diff = 1.59e+04 (tolerance: < 1.00e-06)

**Feedback**:
- Num observations with diff >= TOL_DIFF_1: 539854/4630424 (11.659%)

**Most Recent Bad Observations**:
```
   permno  yyyymm      python       stata      diff
0   12211  202407 -208.767746 -208.766630 -0.001116
1   14822  202407  736.877984  736.881100 -0.003116
2   16670  202407   96.854357   96.854492 -0.000135
3   18253  202407   73.445587   73.445900 -0.000313
4   18303  202407  143.441861  143.442230 -0.000369
5   19506  202407  151.978196  151.978500 -0.000304
6   19948  202407  167.521873  167.522000 -0.000127
7   20147  202407  954.716299  954.706420  0.009879
8   20238  202407 -218.851210 -218.852420  0.001210
9   21178  202407   97.716947   97.716812  0.000135
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

**Precision1**: 28.092% obs with diff >= 1.00e-04 (tolerance: < 0.1%)

**Precision2**: 100th percentile diff = 1.08e+01 (tolerance: < 1.00e-06)

**Feedback**:
- Num observations with diff >= TOL_DIFF_1: 1270775/4523656 (28.092%)

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

**Precision1**: 0.000% obs with diff >= 1.00e-04 (tolerance: < 0.1%)

**Precision2**: 100th percentile diff = 5.00e-08 (tolerance: < 1.00e-06)

**Feedback**:
- Num observations with diff >= TOL_DIFF_1: 0/24028 (0.000%)

---

### RD

**Status**: ❌ FAILED

**Test Results**:
- Test 1 - Column names: ✅ PASSED
- Test 2 - Superset check: ✅ PASSED
- Test 3 - Precision1 check: ✅ PASSED
- Test 4 - Precision2 check: ❌ FAILED

**Columns**: ['RD']

**Observations**:
- Stata:  1,419,136
- Python: 1,419,157
- Common: 1,419,136

**Precision1**: 0.000% obs with diff >= 1.00e-04 (tolerance: < 0.1%)

**Precision2**: 100th percentile diff = 1.32e-02 (tolerance: < 1.00e-06)

**Feedback**:
- Num observations with diff >= TOL_DIFF_1: 7/1419136 (0.000%)

**Most Recent Bad Observations**:
```
   permno  yyyymm    python     stata      diff
0   90177  202412  0.086494  0.096998 -0.010504
1   90177  202411  0.097252  0.109063 -0.011811
2   90177  202410  0.108784  0.121995 -0.013211
3   90177  202409  0.103196  0.115729 -0.012533
4   90177  202408  0.096002  0.107661 -0.011659
5   90177  202407  0.083686  0.093850 -0.010163
6   90177  202406  0.097965  0.109863 -0.011897
```

**Largest Differences**:
```
   permno  yyyymm    python     stata      diff
0   90177  202410  0.108784  0.121995 -0.013211
1   90177  202409  0.103196  0.115729 -0.012533
2   90177  202406  0.097965  0.109863 -0.011897
3   90177  202411  0.097252  0.109063 -0.011811
4   90177  202408  0.096002  0.107661 -0.011659
5   90177  202412  0.086494  0.096998 -0.010504
6   90177  202407  0.083686  0.093850 -0.010163
```

---

### RDAbility

**Status**: ❌ FAILED

**Test Results**:
- Test 1 - Column names: ✅ PASSED
- Test 2 - Superset check: ❌ FAILED (Python missing 8455 Stata observations)
- Test 3 - Precision1 check: ❌ FAILED
- Test 4 - Precision2 check: ❌ FAILED

**Columns**: ['RDAbility']

**Observations**:
- Stata:  173,266
- Python: 233,497
- Common: 164,811

**Precision1**: 100.000% obs with diff >= 1.00e-04 (tolerance: < 0.1%)

**Precision2**: 100th percentile diff = nan (tolerance: < 1.00e-06)

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
- Num observations with diff >= TOL_DIFF_1: 164811/164811 (100.000%)

**Most Recent Bad Observations**:
```
   permno  yyyymm    python     stata      diff
0   20117  202608  0.384144  2.244096 -1.859952
1   63125  202608  0.439429  1.052814 -0.613385
2   75603  202608  0.145414  1.657931 -1.512517
3   75828  202608  0.213916 -0.489681  0.703597
4   78987  202608  0.245592  3.648803 -3.403211
5   84761  202608  1.457716 -1.036981  2.494696
6   85035  202608  0.184039  1.323436 -1.139397
7   85177  202608  0.840426 -1.963602  2.804028
8   87179  202608 -0.219607  1.526995 -1.746602
9   20117  202607  0.384144  2.244096 -1.859952
```

**Largest Differences**:
```
   permno  yyyymm  python     stata  diff
0   84666  200406     NaN  2.125255   NaN
1   84666  200407     NaN  2.125255   NaN
2   84666  200408     NaN  2.125255   NaN
3   84666  200409     NaN  2.125255   NaN
4   84666  200410     NaN  2.125255   NaN
5   84666  200411     NaN  2.125255   NaN
6   84666  200412     NaN  2.125255   NaN
7   84666  200501     NaN  2.125255   NaN
8   84666  200502     NaN  2.125255   NaN
9   84666  200503     NaN  2.125255   NaN
```

---

### RDS

**Status**: ❌ FAILED

**Test Results**:
- Test 1 - Column names: ✅ PASSED
- Test 2 - Superset check: ✅ PASSED
- Test 3 - Precision1 check: ❌ FAILED
- Test 4 - Precision2 check: ❌ FAILED

**Columns**: ['RDS']

**Observations**:
- Stata:  2,725,375
- Python: 3,169,667
- Common: 2,725,375

**Precision1**: 0.756% obs with diff >= 1.00e-04 (tolerance: < 0.1%)

**Precision2**: 100th percentile diff = 7.13e+01 (tolerance: < 1.00e-06)

**Feedback**:
- Num observations with diff >= TOL_DIFF_1: 20601/2725375 (0.756%)

**Most Recent Bad Observations**:
```
   permno  yyyymm       python       stata      diff
0   24252  202608   -974.28936  -1026.1893  51.89994
1   76721  202608  -3853.67007  -3853.6702   0.00013
2   79686  202608 -14492.46148 -14492.4620   0.00052
3   86349  202608 -19043.16677 -19114.4650  71.29823
4   88683  202608 -16118.85870 -16118.8580  -0.00070
5   88957  202608  -8821.84906  -8821.8486  -0.00046
6   24252  202607   -974.28936  -1026.1893  51.89994
7   76721  202607  -3853.67007  -3853.6702   0.00013
8   79686  202607 -14492.46148 -14492.4620   0.00052
9   86349  202607 -19043.16677 -19114.4650  71.29823
```

**Largest Differences**:
```
   permno  yyyymm       python      stata      diff
0   86349  202509 -19043.16677 -19114.465  71.29823
1   86349  202510 -19043.16677 -19114.465  71.29823
2   86349  202511 -19043.16677 -19114.465  71.29823
3   86349  202512 -19043.16677 -19114.465  71.29823
4   86349  202601 -19043.16677 -19114.465  71.29823
5   86349  202602 -19043.16677 -19114.465  71.29823
6   86349  202603 -19043.16677 -19114.465  71.29823
7   86349  202604 -19043.16677 -19114.465  71.29823
8   86349  202605 -19043.16677 -19114.465  71.29823
9   86349  202606 -19043.16677 -19114.465  71.29823
```

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

**Precision1**: 0.000% obs with diff >= 1.00e-04 (tolerance: < 0.1%)

**Precision2**: 100th percentile diff = 1.32e-06 (tolerance: < 1.00e-06)

**Feedback**:
- Num observations with diff >= TOL_DIFF_1: 0/517737 (0.000%)

---

### REV6

**Status**: ❌ FAILED

**Test Results**:
- Test 1 - Column names: ✅ PASSED
- Test 2 - Superset check: ✅ PASSED
- Test 3 - Precision1 check: ❌ FAILED
- Test 4 - Precision2 check: ❌ FAILED

**Columns**: ['REV6']

**Observations**:
- Stata:  1,762,090
- Python: 4,003,555
- Common: 1,762,090

**Precision1**: 25.737% obs with diff >= 1.00e-04 (tolerance: < 0.1%)

**Precision2**: 100th percentile diff = 8.42e+03 (tolerance: < 1.00e-06)

**Feedback**:
- Num observations with diff >= TOL_DIFF_1: 453508/1762090 (25.737%)

**Most Recent Bad Observations**:
```
   permno  yyyymm    python     stata      diff
0   10501  202412 -0.016730 -0.017195  0.000465
1   11174  202412  0.093741  0.099217 -0.005475
2   12146  202412  0.178963  0.144146  0.034816
3   12266  202412  0.000732 -0.000090  0.000822
4   12473  202412  0.000000 -0.004113  0.004113
5   13547  202412 -0.135159 -0.133172 -0.001986
6   13750  202412  0.148053  0.137300  0.010753
7   13777  202412 -0.006271 -0.005297 -0.000975
8   13825  202412  0.111010  0.110418  0.000593
9   13947  202412  0.753591  0.957144 -0.203553
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
- Test 2 - Superset check: ❌ FAILED (Python missing 1211 Stata observations)
- Test 3 - Precision1 check: ❌ FAILED
- Test 4 - Precision2 check: ❌ FAILED

**Columns**: ['RIO_Disp']

**Observations**:
- Stata:  497,437
- Python: 513,660
- Common: 496,226

**Precision1**: 6.716% obs with diff >= 1.00e-04 (tolerance: < 0.1%)

**Precision2**: 100th percentile diff = 4.00e+00 (tolerance: < 1.00e-06)

**Missing Observations Sample**:
```
 index  permno  yyyymm  RIO_Disp
     0   10149  199605         5
     1   10149  199606         4
     2   10299  199403         2
     3   10325  199403         5
     4   10353  200006         2
     5   10363  198903         4
     6   10371  200110         5
     7   10386  199704         3
     8   10421  199605         5
     9   10501  199108         5
```

**Feedback**:
- Num observations with diff >= TOL_DIFF_1: 33325/496226 (6.716%)

**Most Recent Bad Observations**:
```
   permno  yyyymm  python  stata  diff
0   12008  202412       3      4    -1
1   13954  202412       4      5    -1
2   14317  202412       3      4    -1
3   17812  202412       2      3    -1
4   18452  202412       2      3    -1
5   18784  202412       4      5    -1
6   18808  202412       4      5    -1
7   19076  202412       2      3    -1
8   20295  202412       2      3    -1
9   20751  202412       3      4    -1
```

**Largest Differences**:
```
   permno  yyyymm  python  stata  diff
0   11379  198901       1      5    -4
1   11453  198808       1      5    -4
2   11554  199101       1      5    -4
3   11981  198002       5      1     4
4   11981  198004       5      1     4
5   12088  201304       1      5    -4
6   12402  201107       1      5    -4
7   12706  198002       5      1     4
8   12706  198003       5      1     4
9   12706  198005       5      1     4
```

---

### RIO_MB

**Status**: ❌ FAILED

**Test Results**:
- Test 1 - Column names: ✅ PASSED
- Test 2 - Superset check: ❌ FAILED (Python missing 624 Stata observations)
- Test 3 - Precision1 check: ❌ FAILED
- Test 4 - Precision2 check: ❌ FAILED

**Columns**: ['RIO_MB']

**Observations**:
- Stata:  354,170
- Python: 367,163
- Common: 353,546

**Precision1**: 17.066% obs with diff >= 1.00e-04 (tolerance: < 0.1%)

**Precision2**: 100th percentile diff = 4.00e+00 (tolerance: < 1.00e-06)

**Missing Observations Sample**:
```
 index  permno  yyyymm  RIO_MB
     0   10051  199111       5
     1   10116  198911       3
     2   10116  199001       3
     3   10125  198911       3
     4   10152  198703       1
     5   10253  200511       1
     6   10281  198802       3
     7   10285  198712       2
     8   10287  198701       3
     9   10316  198801       1
```

**Feedback**:
- Num observations with diff >= TOL_DIFF_1: 60337/353546 (17.066%)

**Most Recent Bad Observations**:
```
   permno  yyyymm  python  stata  diff
0   11955  202412       1      2    -1
1   15400  202412       3      4    -1
2   16066  202412       2      3    -1
3   17812  202412       2      3    -1
4   18452  202412       2      3    -1
5   18649  202412       3      4    -1
6   19076  202412       2      3    -1
7   51925  202412       3      4    -1
8   70578  202412       1      2    -1
9   81540  202412       2      3    -1
```

**Largest Differences**:
```
   permno  yyyymm  python  stata  diff
0   10400  197706       1      5    -4
1   10400  197707       1      5    -4
2   10400  197708       1      5    -4
3   10400  197709       1      5    -4
4   10400  197710       1      5    -4
5   10400  197711       1      5    -4
6   10875  197311       1      5    -4
7   10875  197402       1      5    -4
8   10971  197309       1      5    -4
9   10971  197404       1      5    -4
```

---

### RIO_Turnover

**Status**: ❌ FAILED

**Test Results**:
- Test 1 - Column names: ✅ PASSED
- Test 2 - Superset check: ❌ FAILED (Python missing 659 Stata observations)
- Test 3 - Precision1 check: ❌ FAILED
- Test 4 - Precision2 check: ❌ FAILED

**Columns**: ['RIO_Turnover']

**Observations**:
- Stata:  445,546
- Python: 462,744
- Common: 444,887

**Precision1**: 23.712% obs with diff >= 1.00e-04 (tolerance: < 0.1%)

**Precision2**: 100th percentile diff = 4.00e+00 (tolerance: < 1.00e-06)

**Missing Observations Sample**:
```
 index  permno  yyyymm  RIO_Turnover
     0   10051  199111             5
     1   10066  199909             1
     2   10125  198911             3
     3   10276  193309             5
     4   10281  198802             3
     5   10341  198708             4
     6   10350  199002             1
     7   10358  198707             5
     8   10371  198807             4
     9   10380  193010             5
```

**Feedback**:
- Num observations with diff >= TOL_DIFF_1: 105493/444887 (23.712%)

**Most Recent Bad Observations**:
```
   permno  yyyymm  python  stata  diff
0   12008  202412       3      4    -1
1   13730  202412       2      3    -1
2   13954  202412       4      5    -1
3   15585  202412       3      4    -1
4   18452  202412       2      3    -1
5   18784  202412       4      5    -1
6   19076  202412       2      3    -1
7   20295  202412       2      3    -1
8   20751  202412       3      4    -1
9   21124  202412       2      3    -1
```

**Largest Differences**:
```
   permno  yyyymm  python  stata  diff
0   10014  192908       1      5    -4
1   10014  193010       1      5    -4
2   10014  193012       1      5    -4
3   10014  193101       1      5    -4
4   10014  193103       1      5    -4
5   10014  194205       1      5    -4
6   10014  194206       1      5    -4
7   10014  194211       1      5    -4
8   10014  194212       1      5    -4
9   10014  194301       1      5    -4
```

---

### RIO_Volatility

**Status**: ❌ FAILED

**Test Results**:
- Test 1 - Column names: ✅ PASSED
- Test 2 - Superset check: ❌ FAILED (Python missing 20672 Stata observations)
- Test 3 - Precision1 check: ❌ FAILED
- Test 4 - Precision2 check: ❌ FAILED

**Columns**: ['RIO_Volatility']

**Observations**:
- Stata:  470,062
- Python: 493,775
- Common: 449,390

**Precision1**: 26.583% obs with diff >= 1.00e-04 (tolerance: < 0.1%)

**Precision2**: 100th percentile diff = 4.00e+00 (tolerance: < 1.00e-06)

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
- Num observations with diff >= TOL_DIFF_1: 119462/449390 (26.583%)

**Most Recent Bad Observations**:
```
   permno  yyyymm  python  stata  diff
0   13954  202412       4      5    -1
1   15585  202412       3      4    -1
2   16066  202412       2      3    -1
3   17812  202412       2      3    -1
4   18062  202412       3      4    -1
5   18452  202412       2      3    -1
6   18784  202412       4      5    -1
7   19076  202412       2      3    -1
8   20295  202412       2      3    -1
9   20751  202412       3      4    -1
```

**Largest Differences**:
```
   permno  yyyymm  python  stata  diff
0   10014  192904       1      5    -4
1   10014  192905       1      5    -4
2   10014  192906       1      5    -4
3   10014  192907       1      5    -4
4   10014  192908       1      5    -4
5   10014  192909       1      5    -4
6   10014  192910       1      5    -4
7   10014  192911       1      5    -4
8   10014  192912       1      5    -4
9   10014  193001       1      5    -4
```

---

### RIVolSpread

**Status**: ❌ FAILED

**Test Results**:
- Test 1 - Column names: ✅ PASSED
- Test 2 - Superset check: ❌ FAILED (Python missing 5337 Stata observations)
- Test 3 - Precision1 check: ✅ PASSED
- Test 4 - Precision2 check: ❌ FAILED

**Columns**: ['RIVolSpread']

**Observations**:
- Stata:  750,937
- Python: 749,192
- Common: 745,600

**Precision1**: 0.053% obs with diff >= 1.00e-04 (tolerance: < 0.1%)

**Precision2**: 100th percentile diff = 8.32e-01 (tolerance: < 1.00e-06)

**Missing Observations Sample**:
```
 index  permno  yyyymm  RIVolSpread
     0   10353  199601     0.244927
     1   10353  199602     0.106554
     2   10353  199603     0.242911
     3   10353  199604    -0.014088
     4   10353  199605    -0.151875
     5   10353  199606    -0.134579
     6   10353  199607     0.208258
     7   10353  199608     0.026554
     8   10353  199609    -0.149417
     9   10353  199610    -0.195715
```

**Feedback**:
- Num observations with diff >= TOL_DIFF_1: 392/745600 (0.053%)

**Most Recent Bad Observations**:
```
   permno  yyyymm    python     stata      diff
0   21534  202208  0.492814  1.230890 -0.738076
1   19347  202202  1.319371  1.102670  0.216701
2   20142  202112  0.315672  0.201082  0.114590
3   21277  202112  0.126028  0.223227 -0.097199
4   20171  202110  3.698565  3.637709  0.060855
5   20399  202109 -0.161713 -0.186181  0.024469
6   19295  202108  0.054789 -0.374740  0.429529
7   20178  202108 -0.476564 -0.321246 -0.155317
8   20310  202108  0.223605 -0.092755  0.316360
9   20354  202107 -0.168526 -0.353121  0.184595
```

**Largest Differences**:
```
   permno  yyyymm    python     stata      diff
0   48506  200811  0.874520  0.042460  0.832060
1   21534  202208  0.492814  1.230890 -0.738076
2   42083  200812 -0.112869 -0.842906  0.730036
3   48506  200810  0.834305  0.162663  0.671642
4   42083  200810  0.245837 -0.412422  0.658259
5   42083  200811 -0.064122 -0.648126  0.584004
6   48506  200812  0.337302 -0.197359  0.534662
7   12473  201111 -0.124758  0.370471 -0.495229
8   42083  200901 -0.091850 -0.560106  0.468256
9   48506  200903  0.408234 -0.056874  0.465108
```

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
- Python: 5,026,821
- Common: 4,987,397

**Precision1**: 0.000% obs with diff >= 1.00e-04 (tolerance: < 0.1%)

**Precision2**: 100th percentile diff = 3.55e-15 (tolerance: < 1.00e-06)

**Feedback**:
- Num observations with diff >= TOL_DIFF_1: 0/4987397 (0.000%)

---

### Recomm_ShortInterest

**Status**: ❌ FAILED

**Test Results**:
- Test 1 - Column names: ✅ PASSED
- Test 2 - Superset check: ❌ FAILED (Python missing 30254 Stata observations)
- Test 3 - Precision1 check: ✅ PASSED
- Test 4 - Precision2 check: ✅ PASSED

**Columns**: ['Recomm_ShortInterest']

**Observations**:
- Stata:  34,619
- Python: 14,630
- Common: 4,365

**Precision1**: 0.000% obs with diff >= 1.00e-04 (tolerance: < 0.1%)

**Precision2**: 100th percentile diff = 0.00e+00 (tolerance: < 1.00e-06)

**Missing Observations Sample**:
```
 index  permno  yyyymm  Recomm_ShortInterest
     0   10044  201107                     1
     1   10044  201108                     1
     2   10044  201109                     1
     3   10044  201110                     1
     4   10044  201111                     1
     5   10044  201112                     1
     6   10044  201201                     1
     7   10044  201202                     1
     8   10044  201203                     1
     9   10051  200704                     1
```

**Feedback**:
- Num observations with diff >= TOL_DIFF_1: 0/4365 (0.000%)

---

### ResidualMomentum

**Status**: ❌ FAILED

**Test Results**:
- Test 1 - Column names: ✅ PASSED
- Test 2 - Superset check: ❌ FAILED (Python missing 83157 Stata observations)
- Test 3 - Precision1 check: ❌ FAILED
- Test 4 - Precision2 check: ❌ FAILED

**Columns**: ['ResidualMomentum']

**Observations**:
- Stata:  3,458,422
- Python: 3,375,265
- Common: 3,375,265

**Precision1**: 12.492% obs with diff >= 1.00e-04 (tolerance: < 0.1%)

**Precision2**: 100th percentile diff = 4.39e-02 (tolerance: < 1.00e-06)

**Missing Observations Sample**:
```
 index  permno  yyyymm  ResidualMomentum
     0   10012  199003          0.206273
     1   10012  199004          0.265448
     2   10012  199005          0.295592
     3   10012  199006          0.366329
     4   10012  199007          0.144718
     5   10012  199008          0.195028
     6   10012  199009          0.289079
     7   10012  199010          0.262496
     8   10012  199011          0.117379
     9   10012  199012          0.134704
```

**Feedback**:
- Num observations with diff >= TOL_DIFF_1: 421625/3375265 (12.492%)

**Most Recent Bad Observations**:
```
   permno  yyyymm    python     stata      diff
0   10026  202412 -0.066509 -0.067570  0.001061
1   10028  202412  0.289036  0.283338  0.005699
2   10032  202412  0.241125  0.238950  0.002175
3   10044  202412 -0.144792 -0.145371  0.000579
4   10065  202412 -0.059084 -0.058484 -0.000600
5   10104  202412  0.191858  0.193927 -0.002068
6   10107  202412 -0.795068 -0.786140 -0.008928
7   10113  202412  0.195732  0.195336  0.000396
8   10138  202412  0.033803  0.033584  0.000219
9   10145  202412 -0.015552 -0.013983 -0.001569
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

**Precision1**: 0.000% obs with diff >= 1.00e-04 (tolerance: < 0.1%)

**Precision2**: 100th percentile diff = 1.60e-14 (tolerance: < 1.00e-06)

**Feedback**:
- Num observations with diff >= TOL_DIFF_1: 0/4952730 (0.000%)

---

### ReturnSkew3F

**Status**: ❌ FAILED

**Test Results**:
- Test 1 - Column names: ✅ PASSED
- Test 2 - Superset check: ❌ FAILED (Python missing 207 Stata observations)
- Test 3 - Precision1 check: ❌ FAILED
- Test 4 - Precision2 check: ❌ FAILED

**Columns**: ['ReturnSkew3F']

**Observations**:
- Stata:  4,978,948
- Python: 5,026,283
- Common: 4,978,741

**Precision1**: 13.286% obs with diff >= 1.00e-04 (tolerance: < 0.1%)

**Precision2**: 100th percentile diff = 8.73e+00 (tolerance: < 1.00e-06)

**Missing Observations Sample**:
```
 index  permno  yyyymm  ReturnSkew3F
     0   10058  198205      0.179042
     1   10074  198205      0.179042
     2   10656  198205      0.179042
     3   10699  198205      0.179042
     4   11236  193003     -0.638568
     5   11683  197301     -0.336802
     6   11712  198205      0.179042
     7   11712  198310     -0.225000
     8   11851  197301     -0.336802
     9   11894  198205      0.179042
```

**Feedback**:
- Num observations with diff >= TOL_DIFF_1: 661495/4978741 (13.286%)

**Most Recent Bad Observations**:
```
   permno  yyyymm    python     stata      diff
0   10026  202412  1.168809  1.169489 -0.000680
1   10028  202412  0.082237  0.081354  0.000883
2   10032  202412  0.598195  0.596837  0.001358
3   10044  202412  0.125341  0.127810 -0.002469
4   10066  202412  0.298563  0.297286  0.001278
5   10104  202412 -1.567851 -1.571426  0.003575
6   10107  202412  0.675241  0.673097  0.002144
7   10113  202412 -0.137912 -0.137762 -0.000150
8   10138  202412 -0.157415 -0.157695  0.000280
9   10145  202412  0.751342  0.753168 -0.001826
```

**Largest Differences**:
```
   permno  yyyymm    python     stata      diff
0   10568  198212 -4.364358  4.364358 -8.728716
1   11253  198212 -4.364358  4.364358 -8.728716
2   12213  198212 -4.364358  4.364358 -8.728716
3   12491  198212 -4.364358  4.364358 -8.728716
4   13515  198212 -4.364358  4.364358 -8.728716
5   14462  198212 -4.364358  4.364358 -8.728716
6   14796  198212 -4.364358  4.364358 -8.728716
7   14964  198212 -4.364358  4.364358 -8.728716
8   15115  198212 -4.364358  4.364358 -8.728716
9   15545  198212 -4.364358  4.364358 -8.728716
```

---

### RoE

**Status**: ❌ FAILED

**Test Results**:
- Test 1 - Column names: ✅ PASSED
- Test 2 - Superset check: ✅ PASSED
- Test 3 - Precision1 check: ✅ PASSED
- Test 4 - Precision2 check: ❌ FAILED

**Columns**: ['RoE']

**Observations**:
- Stata:  3,527,662
- Python: 3,528,982
- Common: 3,527,662

**Precision1**: 0.002% obs with diff >= 1.00e-04 (tolerance: < 0.1%)

**Precision2**: 100th percentile diff = 3.43e-01 (tolerance: < 1.00e-06)

**Feedback**:
- Num observations with diff >= TOL_DIFF_1: 60/3527662 (0.002%)

**Most Recent Bad Observations**:
```
   permno  yyyymm    python     stata      diff
0   10104  202610  0.608430  0.593400  0.015030
1   10104  202609  0.608430  0.593400  0.015030
2   10104  202608  0.608430  0.593400  0.015030
3   10104  202607  0.608430  0.593400  0.015030
4   10104  202606  0.608430  0.593400  0.015030
5   10104  202605  0.608430  0.593400  0.015030
6   18405  202605  1.604185  1.414764  0.189421
7   10104  202604  0.608430  0.593400  0.015030
8   18405  202604  1.604185  1.414764  0.189421
9   10104  202603  0.608430  0.593400  0.015030
```

**Largest Differences**:
```
   permno  yyyymm    python     stata      diff
0   23033  202406 -0.891136 -0.548212 -0.342924
1   23033  202407 -0.891136 -0.548212 -0.342924
2   23033  202408 -0.891136 -0.548212 -0.342924
3   23033  202409 -0.891136 -0.548212 -0.342924
4   23033  202410 -0.891136 -0.548212 -0.342924
5   23033  202411 -0.891136 -0.548212 -0.342924
6   23033  202412 -0.891136 -0.548212 -0.342924
7   23033  202501 -0.891136 -0.548212 -0.342924
8   23033  202502 -0.891136 -0.548212 -0.342924
9   23033  202503 -0.891136 -0.548212 -0.342924
```

---

### SP

**Status**: ❌ FAILED

**Test Results**:
- Test 1 - Column names: ✅ PASSED
- Test 2 - Superset check: ✅ PASSED
- Test 3 - Precision1 check: ✅ PASSED
- Test 4 - Precision2 check: ❌ FAILED

**Columns**: ['SP']

**Observations**:
- Stata:  3,030,926
- Python: 3,030,928
- Common: 3,030,926

**Precision1**: 0.003% obs with diff >= 1.00e-04 (tolerance: < 0.1%)

**Precision2**: 100th percentile diff = 9.20e-03 (tolerance: < 1.00e-06)

**Feedback**:
- Num observations with diff >= TOL_DIFF_1: 98/3030926 (0.003%)

**Most Recent Bad Observations**:
```
   permno  yyyymm    python     stata      diff
0   12373  202412  0.257776  0.265544 -0.007768
1   87077  202412  1.084568  1.080374  0.004194
2   12373  202411  0.228593  0.235482 -0.006889
3   87077  202411  1.053366  1.049293  0.004073
4   12373  202410  0.260251  0.268093 -0.007843
5   87077  202410  1.134190  1.129805  0.004385
6   12373  202409  0.255579  0.263281 -0.007702
7   87077  202409  1.096040  1.091802  0.004238
8   12373  202408  0.263088  0.271016 -0.007928
9   87077  202408  1.034541  1.030541  0.004000
```

**Largest Differences**:
```
   permno  yyyymm    python     stata      diff
0   12373  202406  0.305159  0.314355 -0.009196
1   12373  202407  0.266812  0.274853 -0.008040
2   12373  202408  0.263088  0.271016 -0.007928
3   12373  202410  0.260251  0.268093 -0.007843
4   12373  202412  0.257776  0.265544 -0.007768
5   12373  202409  0.255579  0.263281 -0.007702
6   12373  202411  0.228593  0.235482 -0.006889
7   87077  201812  1.640556  1.635548  0.005008
8   87077  202406  1.241548  1.236748  0.004801
9   87077  201810  1.518814  1.514177  0.004637
```

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

**Precision1**: 0.000% obs with diff >= 1.00e-04 (tolerance: < 0.1%)

**Precision2**: 100th percentile diff = 5.00e-07 (tolerance: < 1.00e-06)

**Feedback**:
- Num observations with diff >= TOL_DIFF_1: 0/4047630 (0.000%)

---

### ShareVol

**Status**: ❌ FAILED

**Test Results**:
- Test 1 - Column names: ✅ PASSED
- Test 2 - Superset check: ❌ FAILED (Python missing 418 Stata observations)
- Test 3 - Precision1 check: ❌ FAILED
- Test 4 - Precision2 check: ❌ FAILED

**Columns**: ['ShareVol']

**Observations**:
- Stata:  1,660,340
- Python: 1,660,875
- Common: 1,659,922

**Precision1**: 14.381% obs with diff >= 1.00e-04 (tolerance: < 0.1%)

**Precision2**: 100th percentile diff = 1.00e+00 (tolerance: < 1.00e-06)

**Missing Observations Sample**:
```
 index  permno  yyyymm  ShareVol
     0   10006  192602         1
     1   10137  192602         1
     2   10153  192602         1
     3   10268  192602         1
     4   10276  192602         1
     5   10436  192602         1
     6   10444  192602         1
     7   10639  192602         1
     8   10647  192602         1
     9   10727  192602         1
```

**Feedback**:
- Num observations with diff >= TOL_DIFF_1: 238708/1659922 (14.381%)

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

**Precision1**: 0.000% obs with diff >= 1.00e-04 (tolerance: < 0.1%)

**Precision2**: 100th percentile diff = 5.00e-07 (tolerance: < 1.00e-06)

**Feedback**:
- Num observations with diff >= TOL_DIFF_1: 0/4029130 (0.000%)

---

### SmileSlope

**Status**: ❌ FAILED

**Test Results**:
- Test 1 - Column names: ✅ PASSED
- Test 2 - Superset check: ❌ FAILED (Python missing 6146 Stata observations)
- Test 3 - Precision1 check: ✅ PASSED
- Test 4 - Precision2 check: ❌ FAILED

**Columns**: ['SmileSlope']

**Observations**:
- Stata:  862,230
- Python: 859,994
- Common: 856,084

**Precision1**: 0.048% obs with diff >= 1.00e-04 (tolerance: < 0.1%)

**Precision2**: 100th percentile diff = 2.51e+00 (tolerance: < 1.00e-06)

**Missing Observations Sample**:
```
 index  permno  yyyymm  SmileSlope
     0   10353  199601   -0.005213
     1   10353  199602    0.015477
     2   10353  199603   -0.035393
     3   10353  199604   -0.001036
     4   10353  199605   -0.000847
     5   10353  199606   -0.000553
     6   10353  199607    0.003536
     7   10353  199608   -0.023927
     8   10353  199609   -0.001470
     9   10353  199610    0.009965
```

**Feedback**:
- Num observations with diff >= TOL_DIFF_1: 407/856084 (0.048%)

**Most Recent Bad Observations**:
```
   permno  yyyymm    python     stata      diff
0   21534  202208  0.217100 -0.177240  0.394340
1   19347  202202  0.065221  0.068518 -0.003297
2   20142  202112  0.298879 -0.282450  0.581329
3   21277  202112  0.078872  1.738224 -1.659352
4   20171  202110 -0.272499  0.150525 -0.423024
5   20399  202109 -0.046154  0.009590 -0.055744
6   19295  202108  0.524126  0.511221  0.012905
7   20178  202108  0.042702 -0.022107  0.064809
8   20310  202108 -0.028377  1.294111 -1.322488
9   20354  202107  1.938081 -0.567183  2.505264
```

**Largest Differences**:
```
   permno  yyyymm    python     stata      diff
0   20354  202107  1.938081 -0.567183  2.505264
1   21277  202112  0.078872  1.738224 -1.659352
2   48506  200009  1.513003  0.010710  1.502293
3   20310  202108 -0.028377  1.294111 -1.322488
4   14831  201710 -1.251451  0.001846 -1.253297
5   24360  199805  1.702718  0.495195  1.207523
6   12473  201310 -0.009274 -0.695612  0.686338
7   20142  202112  0.298879 -0.282450  0.581329
8   42083  201006  0.011312  0.536802 -0.525490
9   12473  201505 -0.077450  0.397714 -0.475164
```

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

**Precision1**: 0.000% obs with diff >= 1.00e-04 (tolerance: < 0.1%)

**Precision2**: 100th percentile diff = 0.00e+00 (tolerance: < 1.00e-06)

**Feedback**:
- Num observations with diff >= TOL_DIFF_1: 0/4047630 (0.000%)

---

### SurpriseRD

**Status**: ❌ FAILED

**Test Results**:
- Test 1 - Column names: ✅ PASSED
- Test 2 - Superset check: ✅ PASSED
- Test 3 - Precision1 check: ✅ PASSED
- Test 4 - Precision2 check: ❌ FAILED

**Columns**: ['SurpriseRD']

**Observations**:
- Stata:  1,545,193
- Python: 1,552,503
- Common: 1,545,193

**Precision1**: 0.005% obs with diff >= 1.00e-04 (tolerance: < 0.1%)

**Precision2**: 100th percentile diff = 1.00e+00 (tolerance: < 1.00e-06)

**Feedback**:
- Num observations with diff >= TOL_DIFF_1: 84/1545193 (0.005%)

**Most Recent Bad Observations**:
```
   permno  yyyymm  python  stata  diff
0   16668  202605     1.0      0   1.0
1   16668  202604     1.0      0   1.0
2   16668  202603     1.0      0   1.0
3   16668  202602     1.0      0   1.0
4   16668  202601     1.0      0   1.0
5   16668  202512     1.0      0   1.0
6   16668  202511     1.0      0   1.0
7   16668  202510     1.0      0   1.0
8   16668  202509     1.0      0   1.0
9   16668  202508     1.0      0   1.0
```

**Largest Differences**:
```
   permno  yyyymm  python  stata  diff
0   16668  202506     1.0      0   1.0
1   16668  202507     1.0      0   1.0
2   16668  202508     1.0      0   1.0
3   16668  202509     1.0      0   1.0
4   16668  202510     1.0      0   1.0
5   16668  202511     1.0      0   1.0
6   16668  202512     1.0      0   1.0
7   16668  202601     1.0      0   1.0
8   16668  202602     1.0      0   1.0
9   16668  202603     1.0      0   1.0
```

---

### Tax

**Status**: ❌ FAILED

**Test Results**:
- Test 1 - Column names: ✅ PASSED
- Test 2 - Superset check: ✅ PASSED
- Test 3 - Precision1 check: ❌ FAILED
- Test 4 - Precision2 check: ❌ FAILED

**Columns**: ['Tax']

**Observations**:
- Stata:  3,211,651
- Python: 3,213,292
- Common: 3,211,651

**Precision1**: 1.343% obs with diff >= 1.00e-04 (tolerance: < 0.1%)

**Precision2**: 100th percentile diff = 2.02e+03 (tolerance: < 1.00e-06)

**Feedback**:
- Num observations with diff >= TOL_DIFF_1: 43145/3211651 (1.343%)

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

**Status**: ❌ FAILED

**Test Results**:
- Test 1 - Column names: ✅ PASSED
- Test 2 - Superset check: ✅ PASSED
- Test 3 - Precision1 check: ✅ PASSED
- Test 4 - Precision2 check: ❌ FAILED

**Columns**: ['TotalAccruals']

**Observations**:
- Stata:  3,141,468
- Python: 3,157,473
- Common: 3,141,468

**Precision1**: 0.001% obs with diff >= 1.00e-04 (tolerance: < 0.1%)

**Precision2**: 100th percentile diff = 9.02e-02 (tolerance: < 1.00e-06)

**Feedback**:
- Num observations with diff >= TOL_DIFF_1: 36/3141468 (0.001%)

**Most Recent Bad Observations**:
```
   permno  yyyymm    python     stata      diff
0   18047  202605  0.256704  0.211225  0.045479
1   23033  202605 -0.021250 -0.018455 -0.002795
2   18047  202604  0.256704  0.211225  0.045479
3   23033  202604 -0.021250 -0.018455 -0.002795
4   18047  202603  0.256704  0.211225  0.045479
5   23033  202603 -0.021250 -0.018455 -0.002795
6   18047  202602  0.256704  0.211225  0.045479
7   23033  202602 -0.021250 -0.018455 -0.002795
8   18047  202601  0.256704  0.211225  0.045479
9   23033  202601 -0.021250 -0.018455 -0.002795
```

**Largest Differences**:
```
   permno  yyyymm    python     stata      diff
0   23033  202406 -0.024739  0.065497 -0.090236
1   23033  202407 -0.024739  0.065497 -0.090236
2   23033  202408 -0.024739  0.065497 -0.090236
3   23033  202409 -0.024739  0.065497 -0.090236
4   23033  202410 -0.024739  0.065497 -0.090236
5   23033  202411 -0.024739  0.065497 -0.090236
6   23033  202412 -0.024739  0.065497 -0.090236
7   23033  202501 -0.024739  0.065497 -0.090236
8   23033  202502 -0.024739  0.065497 -0.090236
9   23033  202503 -0.024739  0.065497 -0.090236
```

---

### TrendFactor

**Status**: ❌ FAILED

**Test Results**:
- Test 1 - Column names: ✅ PASSED
- Test 2 - Superset check: ❌ FAILED (Python missing 1452 Stata observations)
- Test 3 - Precision1 check: ❌ FAILED
- Test 4 - Precision2 check: ❌ FAILED

**Columns**: ['TrendFactor']

**Observations**:
- Stata:  2,058,231
- Python: 2,057,228
- Common: 2,056,779

**Precision1**: 99.898% obs with diff >= 1.00e-04 (tolerance: < 0.1%)

**Precision2**: 100th percentile diff = 5.38e+00 (tolerance: < 1.00e-06)

**Missing Observations Sample**:
```
 index  permno  yyyymm  TrendFactor
     0   10010  199505     0.402793
     1   10025  198905     0.183533
     2   10070  198610     0.164795
     3   10086  199110     0.285178
     4   10087  198610     0.158854
     5   10115  198610     0.162526
     6   10116  199110     0.288732
     7   10122  198812     0.313713
     8   10122  199604     0.156208
     9   10123  198812     0.314046
```

**Feedback**:
- Num observations with diff >= TOL_DIFF_1: 2054676/2056779 (99.898%)

**Most Recent Bad Observations**:
```
   permno  yyyymm    python     stata      diff
0   10026  202412 -0.094924  0.032569 -0.127493
1   10032  202412 -0.092298  0.035968 -0.128266
2   10104  202412 -0.093959  0.034036 -0.127994
3   10107  202412 -0.093766  0.038111 -0.131876
4   10138  202412 -0.090847  0.037830 -0.128677
5   10145  202412 -0.094344  0.036421 -0.130765
6   10158  202412 -0.091837  0.032967 -0.124805
7   10200  202412 -0.091831  0.036853 -0.128684
8   10220  202412 -0.095402  0.030636 -0.126038
9   10252  202412 -0.093153  0.033475 -0.126628
```

**Largest Differences**:
```
   permno  yyyymm    python     stata      diff
0   18104  193203 -4.538915  0.837169 -5.376084
1   15536  193207 -3.247791  0.539885 -3.787676
2   13418  193207 -3.202128  0.525939 -3.728067
3   13725  193207 -3.202128  0.502853 -3.704981
4   17873  193207 -3.147391  0.522079 -3.669470
5   15499  193206 -3.204386  0.441662 -3.646048
6   14883  193207 -3.106826  0.520245 -3.627072
7   13725  193206 -3.068029  0.529304 -3.597333
8   10188  193202 -3.070908  0.499869 -3.570777
9   15544  193203 -3.062227  0.497286 -3.559513
```

---

### VarCF

**Status**: ❌ FAILED

**Test Results**:
- Test 1 - Column names: ✅ PASSED
- Test 2 - Superset check: ✅ PASSED
- Test 3 - Precision1 check: ✅ PASSED
- Test 4 - Precision2 check: ❌ FAILED

**Columns**: ['VarCF']

**Observations**:
- Stata:  2,547,003
- Python: 2,547,003
- Common: 2,547,003

**Precision1**: 0.010% obs with diff >= 1.00e-04 (tolerance: < 0.1%)

**Precision2**: 100th percentile diff = 1.79e-02 (tolerance: < 1.00e-06)

**Feedback**:
- Num observations with diff >= TOL_DIFF_1: 260/2547003 (0.010%)

**Most Recent Bad Observations**:
```
   permno  yyyymm        python         stata      diff
0   12373  202412      0.005322      0.003112  0.002210
1   12500  202412      3.109142      3.126994 -0.017852
2   15203  202412      0.013390      0.013548 -0.000158
3   16070  202412      0.536968      0.537207 -0.000239
4   18558  202412  83168.859434  83168.867000 -0.007566
5   18643  202412      0.451443      0.445233  0.006210
6   19978  202412   2184.386381   2184.386200  0.000181
7   22096  202412      0.004558      0.002626  0.001932
8   82702  202412      0.130095      0.127309  0.002785
9   87532  202412      0.233044      0.233193 -0.000149
```

**Largest Differences**:
```
   permno  yyyymm         python          stata      diff
0   12500  202412       3.109142       3.126994 -0.017852
1   12500  202411       3.002607       3.018015 -0.015408
2   18558  202404   97391.354204   97391.367000 -0.012796
3   12500  202410       2.949449       2.962090 -0.012642
4   18558  202403   99512.199103   99512.211000 -0.011897
5   18558  202312  106471.418375  106471.430000 -0.011625
6   18558  202402  101726.468758  101726.480000 -0.011242
7   18558  202408   89742.005093   89742.016000 -0.010907
8   12500  202409       2.900720       2.911244 -0.010524
9   18558  202411   84738.038519   84738.047000 -0.008481
```

---

### VolMkt

**Status**: ❌ FAILED

**Test Results**:
- Test 1 - Column names: ✅ PASSED
- Test 2 - Superset check: ❌ FAILED (Python missing 924 Stata observations)
- Test 3 - Precision1 check: ✅ PASSED
- Test 4 - Precision2 check: ❌ FAILED

**Columns**: ['VolMkt']

**Observations**:
- Stata:  4,359,237
- Python: 4,361,398
- Common: 4,358,313

**Precision1**: 0.096% obs with diff >= 1.00e-04 (tolerance: < 0.1%)

**Precision2**: 100th percentile diff = 5.26e+00 (tolerance: < 1.00e-06)

**Missing Observations Sample**:
```
 index  permno  yyyymm   VolMkt
     0   10006  193810 0.031958
     1   10025  199410 0.033900
     2   10057  198106 0.044378
     3   10057  198107 0.043731
     4   10057  198108 0.043489
     5   10057  198109 0.045174
     6   10057  198110 0.049235
     7   10100  198810 0.031230
     8   10100  198811 0.031312
     9   10100  198812 0.027437
```

**Feedback**:
- Num observations with diff >= TOL_DIFF_1: 4201/4358313 (0.096%)

**Most Recent Bad Observations**:
```
   permno  yyyymm      python       stata      diff
0   22284  202412  104.286501  104.530980 -0.244479
1   23951  202412    0.511061    4.270252 -3.759191
2   88195  202412    0.746704    0.734517  0.012187
3   22284  202411  140.847941  141.164660 -0.316719
4   23951  202411    0.492016    3.418793 -2.926777
5   88195  202411    0.315917    0.298627  0.017290
6   22818  202410    0.089680    0.059361  0.030319
7   23226  202410    1.848226    1.841104  0.007122
8   23951  202410    0.524777    3.571736 -3.046959
9   88195  202410    0.349446    0.316797  0.032649
```

**Largest Differences**:
```
   permno  yyyymm    python     stata      diff
0   81593  198312  5.399981  0.140067  5.259914
1   20639  202211  5.517778  1.367406  4.150372
2   20639  202212  5.100497  1.245716  3.854781
3   23951  202412  0.511061  4.270252 -3.759191
4   23951  202410  0.524777  3.571736 -3.046959
5   23951  202411  0.492016  3.418793 -2.926777
6   23226  202407  5.830292  3.155770  2.674522
7   20639  202301  3.644561  1.043433  2.601128
8   20639  202302  3.649246  1.647085  2.002160
9   23951  202409  1.451245  3.231171 -1.779926
```

---

### VolSD

**Status**: ❌ FAILED

**Test Results**:
- Test 1 - Column names: ✅ PASSED
- Test 2 - Superset check: ❌ FAILED (Python missing 900 Stata observations)
- Test 3 - Precision1 check: ❌ FAILED
- Test 4 - Precision2 check: ❌ FAILED

**Columns**: ['VolSD']

**Observations**:
- Stata:  3,922,498
- Python: 3,922,399
- Common: 3,921,598

**Precision1**: 0.306% obs with diff >= 1.00e-04 (tolerance: < 0.1%)

**Precision2**: 100th percentile diff = 3.02e+01 (tolerance: < 1.00e-06)

**Missing Observations Sample**:
```
 index  permno  yyyymm    VolSD
     0   10006  193810 0.018818
     1   10025  199410 0.159270
     2   10057  198106 0.128160
     3   10057  198107 0.128708
     4   10057  198108 0.129991
     5   10057  198109 0.130397
     6   10057  198110 0.131344
     7   10100  198810 0.075436
     8   10100  198811 0.074772
     9   10100  198812 0.074379
```

**Feedback**:
- Num observations with diff >= TOL_DIFF_1: 12019/3921598 (0.306%)

**Most Recent Bad Observations**:
```
   permno  yyyymm      python       stata      diff
0   20825  202412   21.181566   21.141668  0.039898
1   22284  202412  152.222852  152.369722 -0.146870
2   88195  202412  103.393789  102.550261  0.843528
3   88937  202412  392.397476  386.251600  6.145875
4   89986  202412  115.855956  115.432855  0.423101
5   20639  202411   15.835309   15.122232  0.713077
6   20825  202411   21.138931   21.144521 -0.005590
7   22284  202411  154.404017  152.428349  1.975668
8   88195  202411  101.321385  100.480995  0.840390
9   88937  202411   41.695585   41.009479  0.686106
```

**Largest Differences**:
```
   permno  yyyymm     python     stata       diff
0   81593  198502  30.606246  0.431475  30.174771
1   81593  198503  30.206970  0.424974  29.781996
2   81593  198504  29.820917  0.417886  29.403031
3   81593  198505  29.445100  0.409862  29.035238
4   81593  198506  29.067081  0.465744  28.601337
5   81593  198507  28.712341  0.463053  28.249288
6   81593  198508  28.141546  0.464398  27.677148
7   81593  198509  26.795173  0.457377  26.337797
8   81593  198510  21.586430  0.450649  21.135780
9   81593  198511  19.299315  0.446451  18.852864
```

---

### VolumeTrend

**Status**: ❌ FAILED

**Test Results**:
- Test 1 - Column names: ✅ PASSED
- Test 2 - Superset check: ✅ PASSED
- Test 3 - Precision1 check: ❌ FAILED
- Test 4 - Precision2 check: ❌ FAILED

**Columns**: ['VolumeTrend']

**Observations**:
- Stata:  3,655,889
- Python: 3,752,130
- Common: 3,655,889

**Precision1**: 1.018% obs with diff >= 1.00e-04 (tolerance: < 0.1%)

**Precision2**: 100th percentile diff = 1.22e-01 (tolerance: < 1.00e-06)

**Feedback**:
- Num observations with diff >= TOL_DIFF_1: 37222/3655889 (1.018%)

**Most Recent Bad Observations**:
```
   permno  yyyymm    python     stata      diff
0   10066  202412 -0.042738 -0.007268 -0.035470
1   11153  202412 -0.056518  0.001885 -0.058404
2   11379  202412 -0.036342 -0.014016 -0.022326
3   12928  202412  0.066959 -0.000076  0.067035
4   13563  202412 -0.019177 -0.051617  0.032440
5   13828  202412 -0.056518 -0.036236 -0.020282
6   13878  202412 -0.002076 -0.044578  0.042502
7   14051  202412 -0.046306 -0.042498 -0.003808
8   14469  202412  0.066959  0.012960  0.054000
9   15294  202412 -0.046056 -0.022408 -0.023648
```

**Largest Differences**:
```
   permno  yyyymm    python     stata      diff
0   76188  199207  0.066959 -0.055106  0.122065
1   81331  199212  0.066959 -0.053937  0.120896
2   83622  201706  0.063452 -0.052244  0.115697
3   83622  201707  0.059125 -0.050653  0.109778
4   11161  200602  0.053628 -0.054415  0.108043
5   27204  201810  0.060988 -0.047022  0.108011
6   27204  201811  0.060954 -0.045956  0.106910
7   76188  199212  0.054548 -0.050417  0.104965
8   83630  201203  0.066959 -0.037886  0.104845
9   27204  201812  0.060880 -0.043556  0.104436
```

---

### XFIN

**Status**: ❌ FAILED

**Test Results**:
- Test 1 - Column names: ✅ PASSED
- Test 2 - Superset check: ✅ PASSED
- Test 3 - Precision1 check: ✅ PASSED
- Test 4 - Precision2 check: ❌ FAILED

**Columns**: ['XFIN']

**Observations**:
- Stata:  3,022,290
- Python: 3,023,550
- Common: 3,022,290

**Precision1**: 0.003% obs with diff >= 1.00e-04 (tolerance: < 0.1%)

**Precision2**: 100th percentile diff = 8.76e-02 (tolerance: < 1.00e-06)

**Feedback**:
- Num observations with diff >= TOL_DIFF_1: 84/3022290 (0.003%)

**Most Recent Bad Observations**:
```
   permno  yyyymm    python     stata      diff
0   15014  202606  0.050924  0.005180  0.045744
1   15014  202605  0.050924  0.005180  0.045744
2   17134  202605  1.121611  1.209258 -0.087647
3   18047  202605 -0.169421 -0.220764  0.051343
4   20927  202605  0.005846  0.013601 -0.007755
5   15014  202604  0.050924  0.005180  0.045744
6   17134  202604  1.121611  1.209258 -0.087647
7   18047  202604 -0.169421 -0.220764  0.051343
8   20927  202604  0.005846  0.013601 -0.007755
9   15014  202603  0.050924  0.005180  0.045744
```

**Largest Differences**:
```
   permno  yyyymm    python     stata      diff
0   17134  202506  1.121611  1.209258 -0.087647
1   17134  202507  1.121611  1.209258 -0.087647
2   17134  202508  1.121611  1.209258 -0.087647
3   17134  202509  1.121611  1.209258 -0.087647
4   17134  202510  1.121611  1.209258 -0.087647
5   17134  202511  1.121611  1.209258 -0.087647
6   17134  202512  1.121611  1.209258 -0.087647
7   17134  202601  1.121611  1.209258 -0.087647
8   17134  202602  1.121611  1.209258 -0.087647
9   17134  202603  1.121611  1.209258 -0.087647
```

---

### betaVIX

**Status**: ❌ FAILED

**Test Results**:
- Test 1 - Column names: ✅ PASSED
- Test 2 - Superset check: ✅ PASSED
- Test 3 - Precision1 check: ❌ FAILED
- Test 4 - Precision2 check: ❌ FAILED

**Columns**: ['betaVIX']

**Observations**:
- Stata:  3,510,758
- Python: 3,553,481
- Common: 3,510,758

**Precision1**: 77.898% obs with diff >= 1.00e-04 (tolerance: < 0.1%)

**Precision2**: 100th percentile diff = 5.75e-01 (tolerance: < 1.00e-06)

**Feedback**:
- Num observations with diff >= TOL_DIFF_1: 2734804/3510758 (77.898%)

**Most Recent Bad Observations**:
```
   permno  yyyymm    python     stata      diff
0   10026  202412 -0.001024 -0.001558  0.000534
1   10028  202412  0.006798  0.007623 -0.000824
2   10032  202412 -0.000224 -0.000388  0.000164
3   10044  202412  0.001192  0.000739  0.000454
4   10066  202412 -0.005787 -0.005536 -0.000251
5   10104  202412  0.000797  0.000471  0.000326
6   10107  202412  0.000816  0.000974 -0.000158
7   10113  202412 -0.001220 -0.001042 -0.000178
8   10138  202412 -0.002827 -0.003156  0.000329
9   10158  202412 -0.000214 -0.000904  0.000690
```

**Largest Differences**:
```
   permno  yyyymm    python     stata      diff
0   13958  201406  0.855439  0.280629  0.574810
1   19831  202012 -0.039200 -0.555196  0.515996
2   13883  202310 -1.660559 -1.237186 -0.423373
3   87776  199503  0.089535 -0.307695  0.397230
4   22298  202410 -0.360627 -0.747243  0.386616
5   67117  199012  0.028636 -0.351113  0.379749
6   86070  200201  0.126315  0.405910 -0.279595
7   18777  201911  0.215048 -0.054327  0.269375
8   24094  202407 -0.345860 -0.609205  0.263345
9   77733  199707  0.060667 -0.199686  0.260354
```

---

### cfp

**Status**: ❌ FAILED

**Test Results**:
- Test 1 - Column names: ✅ PASSED
- Test 2 - Superset check: ✅ PASSED
- Test 3 - Precision1 check: ✅ PASSED
- Test 4 - Precision2 check: ❌ FAILED

**Columns**: ['cfp']

**Observations**:
- Stata:  2,613,997
- Python: 2,614,930
- Common: 2,613,997

**Precision1**: 0.000% obs with diff >= 1.00e-04 (tolerance: < 0.1%)

**Precision2**: 100th percentile diff = 1.88e-01 (tolerance: < 1.00e-06)

**Feedback**:
- Num observations with diff >= TOL_DIFF_1: 7/2613997 (0.000%)

**Most Recent Bad Observations**:
```
   permno  yyyymm    python     stata      diff
0   23033  202412 -0.253836 -0.198317 -0.055520
1   23033  202411 -0.688984 -0.538288 -0.150696
2   23033  202410 -0.857809 -0.670187 -0.187622
3   23033  202409 -0.828824 -0.647542 -0.181282
4   23033  202408 -0.489032 -0.382070 -0.106962
5   23033  202407 -0.438569 -0.342644 -0.095925
6   23033  202406 -0.403259 -0.315057 -0.088202
```

**Largest Differences**:
```
   permno  yyyymm    python     stata      diff
0   23033  202410 -0.857809 -0.670187 -0.187622
1   23033  202409 -0.828824 -0.647542 -0.181282
2   23033  202411 -0.688984 -0.538288 -0.150696
3   23033  202408 -0.489032 -0.382070 -0.106962
4   23033  202407 -0.438569 -0.342644 -0.095925
5   23033  202406 -0.403259 -0.315057 -0.088202
6   23033  202412 -0.253836 -0.198317 -0.055520
```

---

### dCPVolSpread

**Status**: ❌ FAILED

**Test Results**:
- Test 1 - Column names: ✅ PASSED
- Test 2 - Superset check: ❌ FAILED (Python missing 6088 Stata observations)
- Test 3 - Precision1 check: ✅ PASSED
- Test 4 - Precision2 check: ❌ FAILED

**Columns**: ['dCPVolSpread']

**Observations**:
- Stata:  851,720
- Python: 851,001
- Common: 845,632

**Precision1**: 0.045% obs with diff >= 1.00e-04 (tolerance: < 0.1%)

**Precision2**: 100th percentile diff = 1.50e+00 (tolerance: < 1.00e-06)

**Missing Observations Sample**:
```
 index  permno  yyyymm  dCPVolSpread
     0   10353  199602      0.020690
     1   10353  199603     -0.050870
     2   10353  199604      0.034357
     3   10353  199605      0.000189
     4   10353  199606      0.000294
     5   10353  199607      0.004089
     6   10353  199608     -0.027463
     7   10353  199609      0.022457
     8   10353  199610      0.011435
     9   10353  199611     -0.019399
```

**Feedback**:
- Num observations with diff >= TOL_DIFF_1: 379/845632 (0.045%)

**Most Recent Bad Observations**:
```
   permno  yyyymm    python     stata      diff
0   48506  201902 -0.066158  0.003310 -0.069468
1   48506  201901  0.029743  0.000919  0.028824
2   48506  201812  0.046524  0.007354  0.039170
3   48506  201811 -0.073446 -0.003467 -0.069979
4   48506  201810  0.085790  0.002080  0.083710
5   48506  201809 -0.078920 -0.002996 -0.075924
6   48506  201808  0.035969  0.023903  0.012066
7   48506  201807 -0.010291 -0.015977  0.005686
8   48506  201806 -0.001945 -0.006631  0.004686
9   48506  201805 -0.005135  0.009018 -0.014153
```

**Largest Differences**:
```
   permno  yyyymm    python     stata      diff
0   48506  200009  1.513305  0.009363  1.503942
1   48506  200010 -1.520504 -0.024254 -1.496250
2   24360  199805  1.700953  0.494501  1.206452
3   12473  201310 -0.017465 -0.756767  0.739302
4   12473  201402  0.011813 -0.691477  0.703290
5   42083  201007  0.124765 -0.533505  0.658270
6   12473  201311  0.003317  0.621303 -0.617986
7   12473  201107  0.011764 -0.589288  0.601052
8   42083  201006  0.037763  0.580042 -0.542279
9   42083  201011  0.260913 -0.275174  0.536087
```

---

### dNoa

**Status**: ❌ FAILED

**Test Results**:
- Test 1 - Column names: ✅ PASSED
- Test 2 - Superset check: ✅ PASSED
- Test 3 - Precision1 check: ✅ PASSED
- Test 4 - Precision2 check: ❌ FAILED

**Columns**: ['dNoa']

**Observations**:
- Stata:  3,194,445
- Python: 3,195,426
- Common: 3,194,445

**Precision1**: 0.009% obs with diff >= 1.00e-04 (tolerance: < 0.1%)

**Precision2**: 100th percentile diff = 6.60e-01 (tolerance: < 1.00e-06)

**Feedback**:
- Num observations with diff >= TOL_DIFF_1: 288/3194445 (0.009%)

**Most Recent Bad Observations**:
```
   permno  yyyymm    python     stata      diff
0   10104  202610  0.182379  0.151501  0.030878
1   10104  202609  0.182379  0.151501  0.030878
2   20193  202609 -0.024952 -0.083022  0.058070
3   21742  202609  0.267048  0.264740  0.002308
4   22620  202609  0.203030  0.197477  0.005552
5   42585  202609 -0.118488 -0.123253  0.004765
6   60097  202609  0.004768 -0.007579  0.012347
7   10104  202608  0.182379  0.151501  0.030878
8   14888  202608  0.113481 -0.013684  0.127165
9   18298  202608 -0.034645 -0.072972  0.038327
```

**Largest Differences**:
```
   permno  yyyymm    python     stata      diff
0   18405  202506 -4.517483 -5.177447  0.659965
1   18405  202507 -4.517483 -5.177447  0.659965
2   18405  202508 -4.517483 -5.177447  0.659965
3   18405  202509 -4.517483 -5.177447  0.659965
4   18405  202510 -4.517483 -5.177447  0.659965
5   18405  202511 -4.517483 -5.177447  0.659965
6   18405  202512 -4.517483 -5.177447  0.659965
7   18405  202601 -4.517483 -5.177447  0.659965
8   18405  202602 -4.517483 -5.177447  0.659965
9   18405  202603 -4.517483 -5.177447  0.659965
```

---

### dVolCall

**Status**: ❌ FAILED

**Test Results**:
- Test 1 - Column names: ✅ PASSED
- Test 2 - Superset check: ❌ FAILED (Python missing 6088 Stata observations)
- Test 3 - Precision1 check: ✅ PASSED
- Test 4 - Precision2 check: ❌ FAILED

**Columns**: ['dVolCall']

**Observations**:
- Stata:  851,720
- Python: 851,001
- Common: 845,632

**Precision1**: 0.045% obs with diff >= 1.00e-04 (tolerance: < 0.1%)

**Precision2**: 100th percentile diff = 9.74e-01 (tolerance: < 1.00e-06)

**Missing Observations Sample**:
```
 index  permno  yyyymm  dVolCall
     0   10353  199602 -0.017705
     1   10353  199603  0.019631
     2   10353  199604 -0.002152
     3   10353  199605 -0.081103
     4   10353  199606  0.149277
     5   10353  199607  0.002172
     6   10353  199608 -0.118033
     7   10353  199609  0.063709
     8   10353  199610 -0.046337
     9   10353  199611 -0.016560
```

**Feedback**:
- Num observations with diff >= TOL_DIFF_1: 379/845632 (0.045%)

**Most Recent Bad Observations**:
```
   permno  yyyymm    python     stata      diff
0   48506  201902  0.013125 -0.056301  0.069426
1   48506  201901 -0.057422 -0.076824  0.019402
2   48506  201812 -0.051481  0.071987 -0.123468
3   48506  201811  0.113744 -0.030567  0.144311
4   48506  201810 -0.130027  0.071206 -0.201233
5   48506  201809  0.158002  0.052461  0.105541
6   48506  201808 -0.244535 -0.058556 -0.185979
7   48506  201807  0.026748 -0.004886  0.031634
8   48506  201806  0.067291  0.007015  0.060276
9   48506  201805 -0.115736 -0.005210 -0.110526
```

**Largest Differences**:
```
   permno  yyyymm    python     stata      diff
0   12473  201403  0.067889 -0.905995  0.973884
1   12473  201310 -0.085515  0.629341 -0.714856
2   12473  201311  0.020645 -0.658292  0.678937
3   42083  201011 -0.375889  0.241222 -0.617111
4   12473  201402 -0.038522  0.531310 -0.569832
5   42083  200810  0.118373  0.681291 -0.562918
6   12473  201304 -0.044820  0.515738 -0.560558
7   12473  201305  0.002583 -0.542193  0.544776
8   12473  201108  0.371836 -0.160242  0.532078
9   42083  201012  0.230120 -0.299206  0.529326
```

---

### dVolPut

**Status**: ❌ FAILED

**Test Results**:
- Test 1 - Column names: ✅ PASSED
- Test 2 - Superset check: ❌ FAILED (Python missing 6088 Stata observations)
- Test 3 - Precision1 check: ✅ PASSED
- Test 4 - Precision2 check: ❌ FAILED

**Columns**: ['dVolPut']

**Observations**:
- Stata:  851,720
- Python: 851,001
- Common: 845,632

**Precision1**: 0.045% obs with diff >= 1.00e-04 (tolerance: < 0.1%)

**Precision2**: 100th percentile diff = 1.59e+00 (tolerance: < 1.00e-06)

**Missing Observations Sample**:
```
 index  permno  yyyymm   dVolPut
     0   10353  199602  0.002985
     1   10353  199603 -0.031239
     2   10353  199604  0.032205
     3   10353  199605 -0.080914
     4   10353  199606  0.149571
     5   10353  199607  0.006261
     6   10353  199608 -0.145496
     7   10353  199609  0.086166
     8   10353  199610 -0.034902
     9   10353  199611 -0.035959
```

**Feedback**:
- Num observations with diff >= TOL_DIFF_1: 379/845632 (0.045%)

**Most Recent Bad Observations**:
```
   permno  yyyymm    python     stata      diff
0   48506  201901 -0.027679 -0.075905  0.048226
1   48506  201812 -0.004957  0.079341 -0.084298
2   48506  201811  0.040298 -0.034034  0.074332
3   48506  201810 -0.044237  0.073286 -0.117523
4   48506  201809  0.079082  0.049465  0.029617
5   48506  201808 -0.208566 -0.034653 -0.173913
6   48506  201807  0.016457 -0.020863  0.037320
7   48506  201806  0.065346  0.000384  0.064962
8   48506  201805 -0.120871  0.003808 -0.124679
9   48506  201804  0.035389 -0.052907  0.088296
```

**Largest Differences**:
```
   permno  yyyymm    python     stata      diff
0   48506  200009  1.663070  0.069768  1.593302
1   48506  200010 -1.554566  0.021324 -1.575890
2   24360  199805  1.954683  1.134295  0.820388
3   12473  201401 -0.016189  0.667019 -0.683208
4   12473  201403  0.038115 -0.453083  0.491198
5   12473  201506  0.106315 -0.347245  0.453560
6   12473  201408 -0.035560 -0.485828  0.450268
7   12473  201407 -0.004486  0.436444 -0.440930
8   12473  201404 -0.047960  0.369293 -0.417253
9   12473  201505 -0.024799  0.375258 -0.400057
```

---

### fgr5yrLag

**Status**: ❌ FAILED

**Test Results**:
- Test 1 - Column names: ✅ PASSED
- Test 2 - Superset check: ❌ FAILED (Python missing 1920 Stata observations)
- Test 3 - Precision1 check: ✅ PASSED
- Test 4 - Precision2 check: ❌ FAILED

**Columns**: ['fgr5yrLag']

**Observations**:
- Stata:  875,784
- Python: 875,652
- Common: 873,864

**Precision1**: 0.069% obs with diff >= 1.00e-04 (tolerance: < 0.1%)

**Precision2**: 100th percentile diff = 4.50e+01 (tolerance: < 1.00e-06)

**Missing Observations Sample**:
```
 index  permno  yyyymm  fgr5yrLag
     0   11406  199306       15.0
     1   11406  199307       15.0
     2   11406  199308       15.0
     3   11406  199309       15.0
     4   11406  199310       15.0
     5   11406  199311       15.0
     6   11406  199312       15.0
     7   11406  199401       15.0
     8   11406  199402       15.0
     9   11406  199403       15.0
```

**Feedback**:
- Num observations with diff >= TOL_DIFF_1: 600/873864 (0.069%)

**Most Recent Bad Observations**:
```
   permno  yyyymm  python  stata   diff
0   12473  201805    7.78   7.27   0.51
1   91575  201805   40.40  -4.60  45.00
2   12473  201804    7.78   7.27   0.51
3   91575  201804   40.40  -4.60  45.00
4   12473  201803    7.78   7.27   0.51
5   91575  201803   40.40  -4.60  45.00
6   12473  201802    7.78   7.27   0.51
7   91575  201802   40.40  -4.60  45.00
8   12473  201801    7.78   7.27   0.51
9   91575  201801   40.40  -4.60  45.00
```

**Largest Differences**:
```
   permno  yyyymm  python  stata  diff
0   91575  201706    40.4   -4.6  45.0
1   91575  201707    40.4   -4.6  45.0
2   91575  201708    40.4   -4.6  45.0
3   91575  201709    40.4   -4.6  45.0
4   91575  201710    40.4   -4.6  45.0
5   91575  201711    40.4   -4.6  45.0
6   91575  201712    40.4   -4.6  45.0
7   91575  201801    40.4   -4.6  45.0
8   91575  201802    40.4   -4.6  45.0
9   91575  201803    40.4   -4.6  45.0
```

---

### hire

**Status**: ❌ FAILED

**Test Results**:
- Test 1 - Column names: ✅ PASSED
- Test 2 - Superset check: ✅ PASSED
- Test 3 - Precision1 check: ✅ PASSED
- Test 4 - Precision2 check: ❌ FAILED

**Columns**: ['hire']

**Observations**:
- Stata:  3,496,899
- Python: 3,498,027
- Common: 3,496,899

**Precision1**: 0.008% obs with diff >= 1.00e-04 (tolerance: < 0.1%)

**Precision2**: 100th percentile diff = 1.65e+00 (tolerance: < 1.00e-06)

**Feedback**:
- Num observations with diff >= TOL_DIFF_1: 288/3496899 (0.008%)

**Most Recent Bad Observations**:
```
   permno  yyyymm    python  stata      diff
0   10104  202610  0.018692    0.0  0.018692
1   10104  202609  0.018692    0.0  0.018692
2   20193  202609  0.279923    0.0  0.279923
3   21742  202609  0.082700    0.0  0.082700
4   22620  202609  0.217469    0.0  0.217469
5   42585  202609 -0.117647    0.0 -0.117647
6   10104  202608  0.018692    0.0  0.018692
7   12082  202608  0.112601    0.0  0.112601
8   18298  202608 -0.037752    0.0 -0.037752
9   20193  202608  0.279923    0.0  0.279923
```

**Largest Differences**:
```
   permno  yyyymm    python     stata     diff
0   90490  202506  0.018325 -1.630696  1.64902
1   90490  202507  0.018325 -1.630696  1.64902
2   90490  202508  0.018325 -1.630696  1.64902
3   90490  202509  0.018325 -1.630696  1.64902
4   90490  202510  0.018325 -1.630696  1.64902
5   90490  202511  0.018325 -1.630696  1.64902
6   90490  202512  0.018325 -1.630696  1.64902
7   90490  202601  0.018325 -1.630696  1.64902
8   90490  202602  0.018325 -1.630696  1.64902
9   90490  202603  0.018325 -1.630696  1.64902
```

---

### iomom_cust

**Status**: ❌ FAILED

**Test Results**:
- Test 1 - Column names: ✅ PASSED
- Test 2 - Superset check: ✅ PASSED
- Test 3 - Precision1 check: ❌ FAILED
- Test 4 - Precision2 check: ❌ FAILED

**Columns**: ['iomom_cust']

**Observations**:
- Stata:  1,637,670
- Python: 1,637,670
- Common: 1,637,670

**Precision1**: 2.985% obs with diff >= 1.00e-04 (tolerance: < 0.1%)

**Precision2**: 100th percentile diff = 1.36e+01 (tolerance: < 1.00e-06)

**Feedback**:
- Num observations with diff >= TOL_DIFF_1: 48891/1637670 (2.985%)

**Most Recent Bad Observations**:
```
   permno  yyyymm     python      stata      diff
0   10032  202412  -5.031135  -5.033023  0.001889
1   10066  202412  -5.031135  -5.033023  0.001889
2   10138  202412  -8.827527  -8.816810 -0.010717
3   10158  202412  -7.438546  -7.438358 -0.000189
4   10253  202412  -7.028764  -7.028272 -0.000492
5   10397  202412 -13.003320 -12.734732 -0.268588
6   10501  202412  -9.718640  -9.718749  0.000109
7   10547  202412  -5.031135  -5.033023  0.001889
8   10550  202412  -4.018180  -4.018359  0.000179
9   10606  202412  -4.869991  -4.873832  0.003841
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

**Status**: ❌ FAILED

**Test Results**:
- Test 1 - Column names: ✅ PASSED
- Test 2 - Superset check: ✅ PASSED
- Test 3 - Precision1 check: ❌ FAILED
- Test 4 - Precision2 check: ❌ FAILED

**Columns**: ['iomom_supp']

**Observations**:
- Stata:  1,639,842
- Python: 1,639,842
- Common: 1,639,842

**Precision1**: 4.107% obs with diff >= 1.00e-04 (tolerance: < 0.1%)

**Precision2**: 100th percentile diff = 6.32e+00 (tolerance: < 1.00e-06)

**Feedback**:
- Num observations with diff >= TOL_DIFF_1: 67347/1639842 (4.107%)

**Most Recent Bad Observations**:
```
   permno  yyyymm    python     stata      diff
0   10032  202412 -5.114922 -5.115264  0.000342
1   10066  202412 -5.114922 -5.115264  0.000342
2   10107  202412 -7.572168 -7.567256 -0.004912
3   10138  202412 -5.618958 -5.615217 -0.003742
4   10158  202412 -7.575939 -7.572555 -0.003384
5   10220  202412 -4.970276 -4.968610 -0.001665
6   10253  202412 -7.325556 -7.324492 -0.001064
7   10355  202412 -7.572168 -7.567256 -0.004912
8   10382  202412 -4.970276 -4.968610 -0.001665
9   10397  202412 -6.796173 -6.790234 -0.005939
```

**Largest Differences**:
```
   permno  yyyymm     python      stata      diff
0   16750  202110  12.903336   6.586491  6.316845
1   16750  202102   3.063027   7.339647 -4.276620
2   16750  202301  14.153852   9.965115  4.188737
3   16750  202401  -4.807053  -0.741561 -4.065492
4   16750  202407   9.283813   5.682468  3.601345
5   16750  202101   4.211531   0.761633  3.449898
6   16750  202210   8.952262  11.995730 -3.043468
7   16750  202112   4.209660   7.195751 -2.986091
8   16750  202411  12.704890   9.985145  2.719745
9   16750  202410  -2.308664   0.369747 -2.678412
```

---

### realestate

**Status**: ❌ FAILED

**Test Results**:
- Test 1 - Column names: ✅ PASSED
- Test 2 - Superset check: ✅ PASSED
- Test 3 - Precision1 check: ❌ FAILED
- Test 4 - Precision2 check: ❌ FAILED

**Columns**: ['realestate']

**Observations**:
- Stata:  1,448,154
- Python: 1,448,163
- Common: 1,448,154

**Precision1**: 0.302% obs with diff >= 1.00e-04 (tolerance: < 0.1%)

**Precision2**: 100th percentile diff = inf (tolerance: < 1.00e-06)

**Feedback**:
- Num observations with diff >= TOL_DIFF_1: 4367/1448154 (0.302%)

**Most Recent Bad Observations**:
```
   permno  yyyymm    python     stata      diff
0   12540  202412 -0.225637 -0.229901  0.004265
1   13142  202412  0.279480  0.275215  0.004265
2   13599  202412 -0.015268 -0.019533  0.004265
3   13760  202412 -0.441574 -0.445839  0.004265
4   14221  202412  0.228272  0.224007  0.004265
5   14339  202412  0.036196  0.031932  0.004265
6   14785  202412 -0.030344 -0.034609  0.004265
7   14985  202412 -0.078596 -0.082861  0.004265
8   15113  202412  0.148575  0.144310  0.004265
9   15802  202412  0.514576  0.510311  0.004265
```

**Largest Differences**:
```
   permno  yyyymm  python     stata  diff
0   10018  198704    -inf -0.186210  -inf
1   10018  198705    -inf -0.183145  -inf
2   10083  198612    -inf -0.145091  -inf
3   10083  198701    -inf -0.137382  -inf
4   10083  198702    -inf -0.133630  -inf
5   10083  198703    -inf -0.123486  -inf
6   10083  198704    -inf -0.121291  -inf
7   10083  198705    -inf -0.118227  -inf
8   10089  198704    -inf  0.018986  -inf
9   10089  198705    -inf  0.022050  -inf
```

---

### retConglomerate

**Status**: ❌ FAILED

**Test Results**:
- Test 1 - Column names: ✅ PASSED
- Test 2 - Superset check: ❌ FAILED (Python missing 176244 Stata observations)
- Test 3 - Precision1 check: ❌ FAILED
- Test 4 - Precision2 check: ❌ FAILED

**Columns**: ['retConglomerate']

**Observations**:
- Stata:  758,394
- Python: 582,783
- Common: 582,150

**Precision1**: 96.720% obs with diff >= 1.00e-04 (tolerance: < 0.1%)

**Precision2**: 100th percentile diff = 3.94e+00 (tolerance: < 1.00e-06)

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
- Num observations with diff >= TOL_DIFF_1: 563056/582150 (96.720%)

**Most Recent Bad Observations**:
```
   permno  yyyymm    python     stata      diff
0   10104  202412  0.000803  0.054399 -0.053596
1   10253  202412  0.000803  0.054399 -0.053596
2   10318  202412  0.039110 -0.068694  0.107804
3   10516  202412  0.009091 -0.030640  0.039731
4   11308  202412  0.009091 -0.030640  0.039731
5   11654  202412  0.039110 -0.068694  0.107804
6   11845  202412  0.000803  0.054399 -0.053596
7   11995  202412  0.009091 -0.030640  0.039731
8   13930  202412  0.039110 -0.068694  0.107804
9   15056  202412  0.039110 -0.068694  0.107804
```

**Largest Differences**:
```
   permno  yyyymm    python     stata      diff
0   14274  202101  0.441381  4.377937 -3.936556
1   89908  202101  0.441381  4.377937 -3.936556
2   19002  202311  4.121830  0.234556  3.887274
3   19357  202311  4.121830  0.234556  3.887274
4   21249  202311  4.121830  0.234556  3.887274
5   61735  202311  4.121830  0.234556  3.887274
6   13142  201806  3.540630  0.683659  2.856971
7   13936  201806  3.540630  0.683659  2.856971
8   34948  201806  3.540630  0.683659  2.856971
9   65306  201806  3.540630  0.683659  2.856971
```

---

### roaq

**Status**: ❌ FAILED

**Test Results**:
- Test 1 - Column names: ✅ PASSED
- Test 2 - Superset check: ✅ PASSED
- Test 3 - Precision1 check: ✅ PASSED
- Test 4 - Precision2 check: ❌ FAILED

**Columns**: ['roaq']

**Observations**:
- Stata:  2,490,858
- Python: 2,714,809
- Common: 2,490,858

**Precision1**: 0.010% obs with diff >= 1.00e-04 (tolerance: < 0.1%)

**Precision2**: 100th percentile diff = 1.35e+01 (tolerance: < 1.00e-06)

**Feedback**:
- Num observations with diff >= TOL_DIFF_1: 247/2490858 (0.010%)

**Most Recent Bad Observations**:
```
   permno  yyyymm    python     stata      diff
0   19018  202412 -0.188469 -0.194915  0.006447
1   21091  202412 -0.258318 -0.272419  0.014101
2   23033  202412 -0.105406 -0.082161 -0.023245
3   23265  202412 -0.050184 -0.040984 -0.009200
4   86115  202412  0.015589  0.012750  0.002839
5   19018  202411 -0.121299 -0.120578 -0.000721
6   22290  202411 -0.296588 -0.268591 -0.027996
7   23033  202411 -0.109607 -0.074826 -0.034781
8   23265  202411  0.012720 -0.050918  0.063638
9   85399  202411 -0.001992 -0.036622  0.034629
```

**Largest Differences**:
```
   permno  yyyymm     python     stata       diff
0   45911  200210 -14.090064 -0.575559 -13.514506
1   75233  199006   1.854555  0.013837   1.840717
2   75233  199007   1.854555  0.013837   1.840717
3   75233  199008   1.854555  0.013837   1.840717
4   88316  200302  -1.522167  0.000000  -1.522167
5   83887  199807   0.252900 -0.629234   0.882135
6   83887  199808   0.252900 -0.629234   0.882135
7   88316  200301  -0.650862  0.000000  -0.650862
8   45911  200209  -0.022090 -0.575559   0.553468
9   45911  200211  -0.042213 -0.575559   0.533346
```

---

### sfe

**Status**: ❌ FAILED

**Test Results**:
- Test 1 - Column names: ✅ PASSED
- Test 2 - Superset check: ❌ FAILED (Python missing 1200 Stata observations)
- Test 3 - Precision1 check: ✅ PASSED
- Test 4 - Precision2 check: ❌ FAILED

**Columns**: ['sfe']

**Observations**:
- Stata:  611,076
- Python: 611,100
- Common: 609,876

**Precision1**: 0.069% obs with diff >= 1.00e-04 (tolerance: < 0.1%)

**Precision2**: 100th percentile diff = 9.99e+00 (tolerance: < 1.00e-06)

**Missing Observations Sample**:
```
 index  permno  yyyymm      sfe
     0   11406  199103 0.195122
     1   11406  199104 0.195122
     2   11406  199105 0.195122
     3   11406  199106 0.195122
     4   11406  199107 0.195122
     5   11406  199108 0.195122
     6   11406  199109 0.195122
     7   11406  199110 0.195122
     8   11406  199111 0.195122
     9   11406  199112 0.195122
```

**Feedback**:
- Num observations with diff >= TOL_DIFF_1: 420/609876 (0.069%)

**Most Recent Bad Observations**:
```
   permno  yyyymm       python      stata      diff
0   14107  202602 -4241.419042 -4241.4189 -0.000142
1   14107  202601 -4241.419042 -4241.4189 -0.000142
2   14107  202512 -4241.419042 -4241.4189 -0.000142
3   14107  202511 -4241.419042 -4241.4189 -0.000142
4   14107  202510 -4241.419042 -4241.4189 -0.000142
5   14107  202509 -4241.419042 -4241.4189 -0.000142
6   14107  202508 -4241.419042 -4241.4189 -0.000142
7   14107  202507 -4241.419042 -4241.4189 -0.000142
8   14107  202506 -4241.419042 -4241.4189 -0.000142
9   14107  202505 -4241.419042 -4241.4189 -0.000142
```

**Largest Differences**:
```
   permno  yyyymm    python     stata      diff
0   63781  202003  8.625647 -1.365727  9.991374
1   63781  202004  8.625647 -1.365727  9.991374
2   63781  202005  8.625647 -1.365727  9.991374
3   63781  202006  8.625647 -1.365727  9.991374
4   63781  202007  8.625647 -1.365727  9.991374
5   63781  202008  8.625647 -1.365727  9.991374
6   63781  202009  8.625647 -1.365727  9.991374
7   63781  202010  8.625647 -1.365727  9.991374
8   63781  202011  8.625647 -1.365727  9.991374
9   63781  202012  8.625647 -1.365727  9.991374
```

---

### sinAlgo

**Status**: ❌ FAILED

**Test Results**:
- Test 1 - Column names: ✅ PASSED
- Test 2 - Superset check: ✅ PASSED
- Test 3 - Precision1 check: ✅ PASSED
- Test 4 - Precision2 check: ❌ FAILED

**Columns**: ['sinAlgo']

**Observations**:
- Stata:  233,503
- Python: 1,001,032
- Common: 233,503

**Precision1**: 0.010% obs with diff >= 1.00e-04 (tolerance: < 0.1%)

**Precision2**: 100th percentile diff = 1.00e+00 (tolerance: < 1.00e-06)

**Feedback**:
- Num observations with diff >= TOL_DIFF_1: 23/233503 (0.010%)

**Most Recent Bad Observations**:
```
   permno  yyyymm  python  stata  diff
0   76597  200011     1.0      0   1.0
1   76597  200010     1.0      0   1.0
2   76597  200009     1.0      0   1.0
3   76597  200008     1.0      0   1.0
4   76597  200007     1.0      0   1.0
5   76597  200006     1.0      0   1.0
6   76597  200005     1.0      0   1.0
7   76597  200004     1.0      0   1.0
8   76597  200003     1.0      0   1.0
9   76597  200002     1.0      0   1.0
```

**Largest Differences**:
```
   permno  yyyymm  python  stata  diff
0   76597  199901     1.0      0   1.0
1   76597  199902     1.0      0   1.0
2   76597  199903     1.0      0   1.0
3   76597  199904     1.0      0   1.0
4   76597  199905     1.0      0   1.0
5   76597  199906     1.0      0   1.0
6   76597  199907     1.0      0   1.0
7   76597  199908     1.0      0   1.0
8   76597  199909     1.0      0   1.0
9   76597  199910     1.0      0   1.0
```

---

### skew1

**Status**: ❌ FAILED

**Test Results**:
- Test 1 - Column names: ✅ PASSED
- Test 2 - Superset check: ❌ FAILED (Python missing 3384 Stata observations)
- Test 3 - Precision1 check: ✅ PASSED
- Test 4 - Precision2 check: ❌ FAILED

**Columns**: ['skew1']

**Observations**:
- Stata:  473,447
- Python: 472,444
- Common: 470,063

**Precision1**: 0.043% obs with diff >= 1.00e-04 (tolerance: < 0.1%)

**Precision2**: 100th percentile diff = 5.31e-01 (tolerance: < 1.00e-06)

**Missing Observations Sample**:
```
 index  permno  yyyymm     skew1
     0   10353  199601 -0.045004
     1   10353  199602 -0.005674
     2   10353  199603 -0.037583
     3   10353  199604  0.020861
     4   10353  199605  0.051236
     5   10353  199606  0.003154
     6   10353  199607  0.000625
     7   10353  199608 -0.007445
     8   10353  199609  0.023247
     9   10353  199610 -0.003927
```

**Feedback**:
- Num observations with diff >= TOL_DIFF_1: 204/470063 (0.043%)

**Most Recent Bad Observations**:
```
   permno  yyyymm    python     stata      diff
0   48506  201901  0.291545  0.042801  0.248744
1   48506  201812  0.054645  0.052503  0.002142
2   48506  201811  0.028139  0.041141 -0.013002
3   48506  201810  0.097273  0.060441  0.036832
4   48506  201809  0.082095  0.054128  0.027967
5   48506  201808  0.178415  0.049405  0.129010
6   48506  201807  0.001187  0.031469 -0.030282
7   48506  201806  0.007241  0.039920 -0.032679
8   48506  201805  0.038740  0.047691 -0.008950
9   48506  201804  0.002635  0.044318 -0.041683
```

**Largest Differences**:
```
   permno  yyyymm    python     stata      diff
0   12473  201402  0.054192  0.585175 -0.530983
1   89644  200601  0.363308  0.010588  0.352720
2   12473  201310  0.056940  0.355176 -0.298236
3   12473  201311  0.056319  0.345101 -0.288782
4   48506  200207  0.341782  0.077776  0.264006
5   48506  200701  0.289741  0.032849  0.256892
6   48506  201901  0.291545  0.042801  0.248744
7   12473  201608  0.077200  0.324817 -0.247617
8   89644  200410  0.286270  0.050412  0.235858
9   48506  200702  0.261152  0.026513  0.234640
```

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

**Precision1**: 0.000% obs with diff >= 1.00e-04 (tolerance: < 0.1%)

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
- Num observations with diff >= TOL_DIFF_1: 0/2165791 (0.000%)

---

### tang

**Status**: ❌ FAILED

**Test Results**:
- Test 1 - Column names: ✅ PASSED
- Test 2 - Superset check: ❌ FAILED (Python missing 324 Stata observations)
- Test 3 - Precision1 check: ✅ PASSED
- Test 4 - Precision2 check: ❌ FAILED

**Columns**: ['tang']

**Observations**:
- Stata:  1,517,431
- Python: 1,517,875
- Common: 1,517,107

**Precision1**: 0.005% obs with diff >= 1.00e-04 (tolerance: < 0.1%)

**Precision2**: 100th percentile diff = 2.35e-03 (tolerance: < 1.00e-06)

**Missing Observations Sample**:
```
 index  permno  yyyymm     tang
     0   87016  200006 0.925292
     1   87016  200007 0.925292
     2   87016  200008 0.925292
     3   87016  200009 0.925292
     4   87016  200010 0.925292
     5   87016  200011 0.925292
     6   87016  200012 0.925292
     7   87016  200101 0.925292
     8   87016  200102 0.925292
     9   87016  200103 0.925292
```

**Feedback**:
- Num observations with diff >= TOL_DIFF_1: 72/1517107 (0.005%)

**Most Recent Bad Observations**:
```
   permno  yyyymm    python     stata      diff
0   20137  202605  0.616611  0.615567  0.001044
1   79362  202605  1.109873  1.107870  0.002002
2   20137  202604  0.616611  0.615567  0.001044
3   79362  202604  1.109873  1.107870  0.002002
4   20137  202603  0.616611  0.615567  0.001044
5   79362  202603  1.109873  1.107870  0.002002
6   20137  202602  0.616611  0.615567  0.001044
7   79362  202602  1.109873  1.107870  0.002002
8   20137  202601  0.616611  0.615567  0.001044
9   79362  202601  1.109873  1.107870  0.002002
```

**Largest Differences**:
```
   permno  yyyymm    python     stata      diff
0   79362  202406  1.711112  1.708761  0.002351
1   79362  202407  1.711112  1.708761  0.002351
2   79362  202408  1.711112  1.708761  0.002351
3   79362  202409  1.711112  1.708761  0.002351
4   79362  202410  1.711112  1.708761  0.002351
5   79362  202411  1.711112  1.708761  0.002351
6   79362  202412  1.711112  1.708761  0.002351
7   79362  202501  1.711112  1.708761  0.002351
8   79362  202502  1.711112  1.708761  0.002351
9   79362  202503  1.711112  1.708761  0.002351
```

---

### zerotrade12M

**Status**: ❌ FAILED

**Test Results**:
- Test 1 - Column names: ✅ PASSED
- Test 2 - Superset check: ✅ PASSED
- Test 3 - Precision1 check: ✅ PASSED
- Test 4 - Precision2 check: ❌ FAILED

**Columns**: ['zerotrade12M']

**Observations**:
- Stata:  4,342,889
- Python: 4,661,610
- Common: 4,342,889

**Precision1**: 0.000% obs with diff >= 1.00e-04 (tolerance: < 0.1%)

**Precision2**: 100th percentile diff = 1.26e-05 (tolerance: < 1.00e-06)

**Feedback**:
- Num observations with diff >= TOL_DIFF_1: 0/4342889 (0.000%)

---

### zerotrade1M

**Status**: ❌ FAILED

**Test Results**:
- Test 1 - Column names: ✅ PASSED
- Test 2 - Superset check: ✅ PASSED
- Test 3 - Precision1 check: ✅ PASSED
- Test 4 - Precision2 check: ❌ FAILED

**Columns**: ['zerotrade1M']

**Observations**:
- Stata:  4,680,231
- Python: 5,077,699
- Common: 4,680,231

**Precision1**: 0.000% obs with diff >= 1.00e-04 (tolerance: < 0.1%)

**Precision2**: 100th percentile diff = 1.44e-06 (tolerance: < 1.00e-06)

**Feedback**:
- Num observations with diff >= TOL_DIFF_1: 0/4680231 (0.000%)

---

### zerotrade6M

**Status**: ❌ FAILED

**Test Results**:
- Test 1 - Column names: ✅ PASSED
- Test 2 - Superset check: ✅ PASSED
- Test 3 - Precision1 check: ✅ PASSED
- Test 4 - Precision2 check: ❌ FAILED

**Columns**: ['zerotrade6M']

**Observations**:
- Stata:  4,530,678
- Python: 4,885,711
- Common: 4,530,678

**Precision1**: 0.000% obs with diff >= 1.00e-04 (tolerance: < 0.1%)

**Precision2**: 100th percentile diff = 8.78e-06 (tolerance: < 1.00e-06)

**Feedback**:
- Num observations with diff >= TOL_DIFF_1: 0/4530678 (0.000%)

---

### Activism1

**Status**: ❌ MISSING PYTHON CSV

**Error**: Python CSV file not found: ../pyData/Predictors/Activism1.csv

---

### Activism2

**Status**: ❌ MISSING PYTHON CSV

**Error**: Python CSV file not found: ../pyData/Predictors/Activism2.csv

---

### ChangeInRecommendation

**Status**: ❌ MISSING PYTHON CSV

**Error**: Python CSV file not found: ../pyData/Predictors/ChangeInRecommendation.csv

---

### DownRecomm

**Status**: ❌ MISSING PYTHON CSV

**Error**: Python CSV file not found: ../pyData/Predictors/DownRecomm.csv

---

### EarnSupBig

**Status**: ❌ MISSING PYTHON CSV

**Error**: Python CSV file not found: ../pyData/Predictors/EarnSupBig.csv

---

### EarningsConsistency

**Status**: ❌ MISSING PYTHON CSV

**Error**: Python CSV file not found: ../pyData/Predictors/EarningsConsistency.csv

---

### EarningsForecastDisparity

**Status**: ❌ MISSING PYTHON CSV

**Error**: Python CSV file not found: ../pyData/Predictors/EarningsForecastDisparity.csv

---

### EarningsStreak

**Status**: ❌ MISSING PYTHON CSV

**Error**: Python CSV file not found: ../pyData/Predictors/EarningsStreak.csv

---

### EarningsSurprise

**Status**: ❌ MISSING PYTHON CSV

**Error**: Python CSV file not found: ../pyData/Predictors/EarningsSurprise.csv

---

### FEPS

**Status**: ❌ MISSING PYTHON CSV

**Error**: Python CSV file not found: ../pyData/Predictors/FEPS.csv

---

### FR

**Status**: ❌ MISSING PYTHON CSV

**Error**: Python CSV file not found: ../pyData/Predictors/FR.csv

---

### FirmAgeMom

**Status**: ❌ MISSING PYTHON CSV

**Error**: Python CSV file not found: ../pyData/Predictors/FirmAgeMom.csv

---

### ForecastDispersion

**Status**: ❌ MISSING PYTHON CSV

**Error**: Python CSV file not found: ../pyData/Predictors/ForecastDispersion.csv

---

### GrAdExp

**Status**: ❌ MISSING PYTHON CSV

**Error**: Python CSV file not found: ../pyData/Predictors/GrAdExp.csv

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

### High52

**Status**: ❌ MISSING PYTHON CSV

**Error**: Python CSV file not found: ../pyData/Predictors/High52.csv

---

### IO_ShortInterest

**Status**: ❌ MISSING PYTHON CSV

**Error**: Python CSV file not found: ../pyData/Predictors/IO_ShortInterest.csv

---

### IndRetBig

**Status**: ❌ MISSING PYTHON CSV

**Error**: Python CSV file not found: ../pyData/Predictors/IndRetBig.csv

---

### InvestPPEInv

**Status**: ❌ MISSING PYTHON CSV

**Error**: Python CSV file not found: ../pyData/Predictors/InvestPPEInv.csv

---

### NOA

**Status**: ❌ MISSING PYTHON CSV

**Error**: Python CSV file not found: ../pyData/Predictors/NOA.csv

---

### NetDebtFinance

**Status**: ❌ MISSING PYTHON CSV

**Error**: Python CSV file not found: ../pyData/Predictors/NetDebtFinance.csv

---

### NetEquityFinance

**Status**: ❌ MISSING PYTHON CSV

**Error**: Python CSV file not found: ../pyData/Predictors/NetEquityFinance.csv

---

### NetPayoutYield

**Status**: ❌ MISSING PYTHON CSV

**Error**: Python CSV file not found: ../pyData/Predictors/NetPayoutYield.csv

---

### NumEarnIncrease

**Status**: ❌ MISSING PYTHON CSV

**Error**: Python CSV file not found: ../pyData/Predictors/NumEarnIncrease.csv

---

### OPLeverage

**Status**: ❌ MISSING PYTHON CSV

**Error**: Python CSV file not found: ../pyData/Predictors/OPLeverage.csv

---

### OrgCap

**Status**: ❌ MISSING PYTHON CSV

**Error**: Python CSV file not found: ../pyData/Predictors/OrgCap.csv

---

### PatentsRD

**Status**: ❌ MISSING PYTHON CSV

**Error**: Python CSV file not found: ../pyData/Predictors/PatentsRD.csv

---

### PayoutYield

**Status**: ❌ MISSING PYTHON CSV

**Error**: Python CSV file not found: ../pyData/Predictors/PayoutYield.csv

---

### RevenueSurprise

**Status**: ❌ MISSING PYTHON CSV

**Error**: Python CSV file not found: ../pyData/Predictors/RevenueSurprise.csv

---

### ShareIss1Y

**Status**: ❌ MISSING PYTHON CSV

**Error**: Python CSV file not found: ../pyData/Predictors/ShareIss1Y.csv

---

### ShareIss5Y

**Status**: ❌ MISSING PYTHON CSV

**Error**: Python CSV file not found: ../pyData/Predictors/ShareIss5Y.csv

---

### ShareRepurchase

**Status**: ❌ MISSING PYTHON CSV

**Error**: Python CSV file not found: ../pyData/Predictors/ShareRepurchase.csv

---

### ShortInterest

**Status**: ❌ MISSING PYTHON CSV

**Error**: Python CSV file not found: ../pyData/Predictors/ShortInterest.csv

---

### UpRecomm

**Status**: ❌ MISSING PYTHON CSV

**Error**: Python CSV file not found: ../pyData/Predictors/UpRecomm.csv

---

### grcapx

**Status**: ❌ MISSING PYTHON CSV

**Error**: Python CSV file not found: ../pyData/Predictors/grcapx.csv

---

### grcapx3y

**Status**: ❌ MISSING PYTHON CSV

**Error**: Python CSV file not found: ../pyData/Predictors/grcapx3y.csv

---

