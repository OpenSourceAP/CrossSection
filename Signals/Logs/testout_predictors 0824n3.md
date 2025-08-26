# Predictor Validation Results

**Generated**: 2025-08-25 23:15:13

**Configuration**:
- TOL_SUPERSET: 1.0%
- TOL_NUMROWS: 5.0%
- TOL_DIFF_1: 0.01
- TOL_OBS_1: 1%
- EXTREME_Q: 0.999
- TOL_DIFF_2: 0.1
- TOL_TSTAT: 0.2
- INDEX_COLS: ['permno', 'yyyymm']

## Summary

Numbers report the **FAILURE** rate. ❌ (100.00%) is BAD.

| Predictor                 | Python CSV | Superset   | NumRows       | Precision1   | Precision2              | T-stat     |
|---------------------------|------------|------------|---------------|--------------|-------------------------|------------|
| AgeIPO                    | ✅         | NA        | NA          | NA           | NA                      | NA         |
| IndIPO                    | ✅         | NA        | NA          | NA           | NA                      | NA         |
| RDIPO                     | ✅         | NA        | NA          | NA           | NA                      | NA         |
| CitationsRD               | ✅         | ❌ (100.00%) | ✅ (-100.0%) | ❌ (0.0%)     | ❌ (99.9th diff 0.0E+00) | SKIP       |
| Recomm_ShortInterest*     | ✅         | ❌ (61.03%) | ❌ (+39.7%)  | ✅ (0.0%)     | ✅ (99.9th diff 0.0E+00) | SKIP       |
| VarCF                     | ✅         | ❌ (27.61%) | ✅ (-27.6%)  | ✅ (0.0%)     | ✅ (99.9th diff 4.0E-08) | SKIP       |
| HerfBE                    | ✅         | ❌ (19.00%) | ✅ (-19.0%)  | ✅ (0.0%)     | ✅ (99.9th diff 2.9E-07) | SKIP       |
| HerfAsset                 | ✅         | ❌ (19.00%) | ✅ (-19.0%)  | ✅ (0.0%)     | ✅ (99.9th diff 2.9E-07) | SKIP       |
| RIO_Volatility            | ✅         | ❌ (18.34%) | ✅ (-6.1%)   | ✅ (0.1%)     | ❌ (99.9th diff 7.7E-01) | SKIP       |
| Herf                      | ✅         | ❌ (17.50%) | ✅ (-17.5%)  | ✅ (0.0%)     | ✅ (99.9th diff 2.8E-07) | SKIP       |
| Mom6mJunk*                | ✅         | ❌ (12.51%) | ✅ (-11.5%)  | ✅ (0.3%)     | ❌ (99.9th diff 5.6E-01) | SKIP       |
| AbnormalAccruals          | ✅         | ❌ (10.58%) | ✅ (-10.1%)  | ❌ (29.3%)    | ❌ (99.9th diff 9.7E-01) | SKIP       |
| Investment                | ✅         | ❌ (9.79%) | ✅ (-9.7%)   | ✅ (0.1%)     | ✅ (99.9th diff 4.3E-02) | SKIP       |
| Activism2                 | ✅         | ❌ (2.01%) | ✅ (-2.0%)   | ✅ (0.0%)     | ✅ (99.9th diff 2.4E-07) | SKIP       |
| MomOffSeason06YrPlus      | ✅         | ❌ (1.82%) | ✅ (-1.8%)   | ✅ (0.5%)     | ❌ (99.9th diff 1.7E+00) | SKIP       |
| Activism1                 | ✅         | ✅ (0.35%) | ❌ (+179.4%) | ✅ (0.0%)     | ✅ (99.9th diff 0.0E+00) | SKIP       |
| RDcap                     | ✅         | ✅ (0.02%) | ❌ (+62.3%)  | ✅ (0.5%)     | ❌ (99.9th diff 1.9E-01) | SKIP       |
| LRreversal                | ✅         | ✅ (0.00%) | ❌ (+32.3%)  | ✅ (0.1%)     | ✅ (99.9th diff 3.6E-02) | SKIP       |
| PredictedFE*              | ✅         | ✅ (0.27%) | ❌ (+26.6%)  | ❌ (85.3%)    | ❌ (99.9th diff 3.1E-01) | SKIP       |
| OperProf                  | ✅         | ✅ (0.00%) | ❌ (+21.8%)  | ✅ (0.0%)     | ✅ (99.9th diff 7.2E-08) | SKIP       |
| CompEquIss                | ✅         | ✅ (0.73%) | ❌ (+18.9%)  | ✅ (0.0%)     | ✅ (99.9th diff 2.1E-06) | SKIP       |
| CredRatDG*                | ✅         | ✅ (0.00%) | ❌ (+18.8%)  | ✅ (0.3%)     | ❌ (99.9th diff 6.6E+00) | SKIP       |
| RDS                       | ✅         | ✅ (0.00%) | ❌ (+16.3%)  | ✅ (0.0%)     | ✅ (99.9th diff 8.7E-08) | SKIP       |
| MRreversal                | ✅         | ✅ (0.00%) | ❌ (+15.0%)  | ✅ (0.0%)     | ✅ (99.9th diff 2.7E-07) | SKIP       |
| OperProfRD                | ✅         | ✅ (0.00%) | ❌ (+13.9%)  | ✅ (0.0%)     | ✅ (99.9th diff 2.9E-07) | SKIP       |
| Illiquidity               | ✅         | ✅ (0.00%) | ❌ (+10.8%)  | ✅ (0.0%)     | ✅ (99.9th diff 1.3E-07) | SKIP       |
| IntMom                    | ✅         | ✅ (0.00%) | ❌ (+9.8%)   | ✅ (0.0%)     | ✅ (99.9th diff 2.7E-07) | SKIP       |
| EarningsConsistency       | ✅         | ✅ (0.00%) | ❌ (+9.8%)   | ✅ (0.0%)     | ✅ (99.9th diff 3.2E-07) | SKIP       |
| BetaFP                    | ✅         | ✅ (0.24%) | ❌ (+9.5%)   | ❌ (6.3%)     | ❌ (99.9th diff 8.8E-01) | SKIP       |
| roaq                      | ✅         | ✅ (0.00%) | ❌ (+9.0%)   | ✅ (0.0%)     | ✅ (99.9th diff 9.6E-08) | SKIP       |
| Cash                      | ✅         | ✅ (0.02%) | ❌ (+7.3%)   | ✅ (0.0%)     | ✅ (99.9th diff 1.5E-07) | SKIP       |
| FirmAgeMom                | ✅         | ✅ (0.00%) | ❌ (+5.2%)   | ✅ (0.0%)     | ✅ (99.9th diff 2.7E-07) | SKIP       |
| MS                        | ✅         | ✅ (0.00%) | ✅ (+0.0%)   | ❌ (31.9%)    | ❌ (99.9th diff 2.6E+00) | SKIP       |
| TrendFactor               | ✅         | ✅ (0.00%) | ✅ (+0.0%)   | ❌ (25.1%)    | ❌ (99.9th diff 9.1E-01) | SKIP       |
| PriceDelayTstat*          | ✅         | ✅ (0.00%) | ✅ (+2.5%)   | ❌ (19.4%)    | ❌ (99.9th diff 5.7E+00) | SKIP       |
| PS                        | ✅         | ✅ (0.00%) | ✅ (+0.1%)   | ❌ (17.9%)    | ❌ (99.9th diff 2.4E+00) | SKIP       |
| RDAbility                 | ✅         | ✅ (0.02%) | ✅ (+4.4%)   | ❌ (4.3%)     | ❌ (99.9th diff 2.2E+00) | SKIP       |
| ResidualMomentum          | ✅         | ✅ (0.00%) | ✅ (+1.7%)   | ❌ (2.9%)     | ❌ (99.9th diff 9.2E-01) | SKIP       |
| ReturnSkew3F              | ✅         | ✅ (0.00%) | ✅ (+0.0%)   | ❌ (2.6%)     | ❌ (99.9th diff 1.4E+00) | SKIP       |
| PriceDelayRsq             | ✅         | ✅ (0.00%) | ✅ (+0.1%)   | ❌ (1.2%)     | ❌ (99.9th diff 1.9E+00) | SKIP       |
| DivInit                   | ✅         | ✅ (0.00%) | ✅ (+0.0%)   | ❌ (1.1%)     | ❌ (99.9th diff 7.3E+00) | SKIP       |
| VolumeTrend               | ✅         | ✅ (0.04%) | ✅ (+0.6%)   | ✅ (1.0%)     | ❌ (99.9th diff 1.5E+00) | SKIP       |
| retConglomerate           | ✅         | ✅ (0.00%) | ✅ (+0.1%)   | ✅ (0.9%)     | ✅ (99.9th diff 7.6E-02) | SKIP       |
| MomOffSeason11YrPlus      | ✅         | ✅ (0.00%) | ✅ (+0.0%)   | ✅ (0.9%)     | ❌ (99.9th diff 1.8E+00) | SKIP       |
| PriceDelaySlope           | ✅         | ✅ (0.00%) | ✅ (+0.1%)   | ✅ (0.6%)     | ✅ (99.9th diff 7.0E-02) | SKIP       |
| MomOffSeason16YrPlus      | ✅         | ✅ (0.00%) | ✅ (+0.2%)   | ✅ (0.5%)     | ❌ (99.9th diff 6.1E-01) | SKIP       |
| Tax                       | ✅         | ✅ (0.00%) | ✅ (+0.1%)   | ✅ (0.4%)     | ✅ (99.9th diff 5.3E-02) | SKIP       |
| BetaLiquidityPS           | ✅         | ✅ (0.00%) | ✅ (+1.6%)   | ✅ (0.3%)     | ✅ (99.9th diff 1.5E-02) | SKIP       |
| AnalystValue              | ✅         | ✅ (0.22%) | ✅ (+4.4%)   | ✅ (0.3%)     | ✅ (99.9th diff 3.1E-02) | SKIP       |
| DivSeason                 | ✅         | ✅ (0.82%) | ✅ (-0.8%)   | ✅ (0.2%)     | ❌ (99.9th diff 2.0E+00) | SKIP       |
| OrgCap                    | ✅         | ✅ (0.00%) | ✅ (+0.0%)   | ✅ (0.2%)     | ✅ (99.9th diff 1.4E-02) | SKIP       |
| REV6                      | ✅         | ✅ (0.17%) | ✅ (+0.0%)   | ✅ (0.2%)     | ✅ (99.9th diff 1.7E-02) | SKIP       |
| IntanEP                   | ✅         | ✅ (0.00%) | ✅ (-0.0%)   | ✅ (0.2%)     | ✅ (99.9th diff 8.1E-02) | SKIP       |
| EarnSupBig                | ✅         | ✅ (0.16%) | ✅ (+0.4%)   | ✅ (0.2%)     | ❌ (99.9th diff 1.5E+00) | SKIP       |
| IntanCFP                  | ✅         | ✅ (0.00%) | ✅ (-0.0%)   | ✅ (0.1%)     | ✅ (99.9th diff 4.1E-02) | SKIP       |
| RIO_Turnover              | ✅         | ✅ (0.03%) | ✅ (+0.1%)   | ✅ (0.1%)     | ❌ (99.9th diff 7.4E-01) | SKIP       |
| ExclExp                   | ✅         | ✅ (0.12%) | ✅ (+2.1%)   | ✅ (0.1%)     | ✅ (99.9th diff 5.6E-02) | SKIP       |
| RIO_Disp                  | ✅         | ✅ (0.22%) | ✅ (+0.1%)   | ✅ (0.1%)     | ❌ (99.9th diff 7.9E-01) | SKIP       |
| MomVol                    | ✅         | ✅ (0.00%) | ✅ (+0.1%)   | ✅ (0.1%)     | ✅ (99.9th diff 0.0E+00) | SKIP       |
| RIO_MB                    | ✅         | ✅ (0.03%) | ✅ (+0.1%)   | ✅ (0.1%)     | ✅ (99.9th diff 0.0E+00) | SKIP       |
| EarningsForecastDisparity | ✅         | ✅ (0.22%) | ✅ (-0.0%)   | ✅ (0.1%)     | ✅ (99.9th diff 8.0E-07) | SKIP       |
| ForecastDispersion        | ✅         | ✅ (0.16%) | ✅ (+0.0%)   | ✅ (0.1%)     | ✅ (99.9th diff 7.0E-07) | SKIP       |
| fgr5yrLag                 | ✅         | ✅ (0.22%) | ✅ (-0.0%)   | ✅ (0.1%)     | ✅ (99.9th diff 3.2E-07) | SKIP       |
| DivYieldST                | ✅         | ✅ (0.00%) | ✅ (+0.6%)   | ✅ (0.1%)     | ✅ (99.9th diff 0.0E+00) | SKIP       |
| PatentsRD                 | ✅         | ✅ (0.04%) | ✅ (+0.6%)   | ✅ (0.1%)     | ✅ (99.9th diff 0.0E+00) | SKIP       |
| RIVolSpread               | ✅         | ✅ (0.71%) | ✅ (-0.3%)   | ✅ (0.1%)     | ✅ (99.9th diff 8.1E-07) | SKIP       |
| CPVolSpread               | ✅         | ✅ (0.74%) | ✅ (-0.3%)   | ✅ (0.0%)     | ✅ (99.9th diff 1.8E-07) | SKIP       |
| ChangeInRecommendation    | ✅         | ✅ (0.23%) | ✅ (+0.1%)   | ✅ (0.0%)     | ✅ (99.9th diff 2.5E-07) | SKIP       |
| OptionVolume2             | ✅         | ✅ (0.72%) | ✅ (-0.3%)   | ✅ (0.0%)     | ✅ (99.9th diff 1.5E-07) | SKIP       |
| ExchSwitch                | ✅         | ✅ (0.00%) | ✅ (+0.0%)   | ✅ (0.0%)     | ✅ (99.9th diff 0.0E+00) | SKIP       |
| skew1                     | ✅         | ✅ (0.71%) | ✅ (-0.2%)   | ✅ (0.0%)     | ✅ (99.9th diff 3.6E-07) | SKIP       |
| grcapx                    | ✅         | ✅ (0.74%) | ✅ (+0.1%)   | ✅ (0.0%)     | ✅ (99.9th diff 2.7E-03) | SKIP       |
| dVolPut                   | ✅         | ✅ (0.71%) | ✅ (-0.1%)   | ✅ (0.0%)     | ✅ (99.9th diff 3.8E-07) | SKIP       |
| OptionVolume1             | ✅         | ✅ (0.72%) | ✅ (-0.3%)   | ✅ (0.0%)     | ✅ (99.9th diff 4.7E-07) | SKIP       |
| dVolCall                  | ✅         | ✅ (0.71%) | ✅ (-0.1%)   | ✅ (0.0%)     | ✅ (99.9th diff 3.8E-07) | SKIP       |
| betaVIX                   | ✅         | ✅ (0.00%) | ✅ (+1.2%)   | ✅ (0.0%)     | ✅ (99.9th diff 6.4E-03) | SKIP       |
| realestate                | ✅         | ✅ (0.00%) | ✅ (+0.0%)   | ✅ (0.0%)     | ✅ (99.9th diff 1.7E-03) | SKIP       |
| GrSaleToGrInv             | ✅         | ✅ (0.00%) | ✅ (+0.5%)   | ✅ (0.0%)     | ✅ (99.9th diff 4.2E-03) | SKIP       |
| AnalystRevision           | ✅         | ✅ (0.16%) | ✅ (+0.0%)   | ✅ (0.0%)     | ✅ (99.9th diff 1.4E-07) | SKIP       |
| SmileSlope                | ✅         | ✅ (0.71%) | ✅ (-0.3%)   | ✅ (0.0%)     | ✅ (99.9th diff 4.2E-07) | SKIP       |
| dCPVolSpread              | ✅         | ✅ (0.71%) | ✅ (-0.1%)   | ✅ (0.0%)     | ✅ (99.9th diff 3.4E-07) | SKIP       |
| iomom_cust                | ✅         | ✅ (0.00%) | ✅ (+0.0%)   | ✅ (0.0%)     | ✅ (99.9th diff 5.0E-03) | SKIP       |
| BM                        | ✅         | ✅ (0.00%) | ✅ (+0.0%)   | ✅ (0.0%)     | ✅ (99.9th diff 2.2E-07) | SKIP       |
| EarningsSurprise          | ✅         | ✅ (0.02%) | ✅ (-0.0%)   | ✅ (0.0%)     | ✅ (99.9th diff 3.2E-04) | SKIP       |
| ChForecastAccrual         | ✅         | ✅ (0.18%) | ✅ (+0.1%)   | ✅ (0.0%)     | ✅ (99.9th diff 0.0E+00) | SKIP       |
| FEPS                      | ✅         | ✅ (0.16%) | ✅ (+0.0%)   | ✅ (0.0%)     | ✅ (99.9th diff 5.0E-07) | SKIP       |
| DownRecomm                | ✅         | ✅ (0.23%) | ✅ (+0.1%)   | ✅ (0.0%)     | ✅ (99.9th diff 0.0E+00) | SKIP       |
| UpRecomm                  | ✅         | ✅ (0.23%) | ✅ (+0.1%)   | ✅ (0.0%)     | ✅ (99.9th diff 0.0E+00) | SKIP       |
| sfe                       | ✅         | ✅ (0.20%) | ✅ (+0.0%)   | ✅ (0.0%)     | ✅ (99.9th diff 4.4E-08) | SKIP       |
| IdioVol3F                 | ✅         | ✅ (0.00%) | ✅ (+0.0%)   | ✅ (0.0%)     | ✅ (99.9th diff 5.3E-03) | SKIP       |
| DivOmit                   | ✅         | ✅ (0.00%) | ✅ (+0.0%)   | ✅ (0.0%)     | ✅ (99.9th diff 0.0E+00) | SKIP       |
| GrSaleToGrOverhead        | ✅         | ✅ (0.00%) | ✅ (+0.5%)   | ✅ (0.0%)     | ✅ (99.9th diff 2.5E-03) | SKIP       |
| iomom_supp                | ✅         | ✅ (0.00%) | ✅ (+0.0%)   | ✅ (0.0%)     | ✅ (99.9th diff 2.0E-03) | SKIP       |
| BetaTailRisk              | ✅         | ✅ (0.00%) | ✅ (+1.7%)   | ✅ (0.0%)     | ✅ (99.9th diff 6.3E-03) | SKIP       |
| IntanBM                   | ✅         | ✅ (0.00%) | ✅ (-0.0%)   | ✅ (0.0%)     | ✅ (99.9th diff 3.1E-03) | SKIP       |
| DelDRC                    | ✅         | ✅ (0.00%) | ✅ (+0.5%)   | ✅ (0.0%)     | ✅ (99.9th diff 3.2E-07) | SKIP       |
| VolSD                     | ✅         | ✅ (0.02%) | ✅ (-0.0%)   | ✅ (0.0%)     | ✅ (99.9th diff 1.5E-04) | SKIP       |
| sinAlgo                   | ✅         | ✅ (0.00%) | ✅ (+0.2%)   | ✅ (0.0%)     | ✅ (99.9th diff 0.0E+00) | SKIP       |
| RevenueSurprise           | ✅         | ✅ (0.00%) | ✅ (+0.0%)   | ✅ (0.0%)     | ✅ (99.9th diff 2.3E-04) | SKIP       |
| DelNetFin                 | ✅         | ✅ (0.00%) | ✅ (+0.0%)   | ✅ (0.0%)     | ✅ (99.9th diff 5.8E-07) | SKIP       |
| Accruals                  | ✅         | ✅ (0.00%) | ✅ (+0.5%)   | ✅ (0.0%)     | ✅ (99.9th diff 2.4E-07) | SKIP       |
| NumEarnIncrease           | ✅         | ✅ (0.00%) | ✅ (+0.0%)   | ✅ (0.0%)     | ✅ (99.9th diff 0.0E+00) | SKIP       |
| IntanSP                   | ✅         | ✅ (0.00%) | ✅ (-0.0%)   | ✅ (0.0%)     | ✅ (99.9th diff 1.7E-03) | SKIP       |
| VolMkt                    | ✅         | ✅ (0.02%) | ✅ (-0.0%)   | ✅ (0.0%)     | ✅ (99.9th diff 2.2E-05) | SKIP       |
| hire                      | ✅         | ✅ (0.00%) | ✅ (+0.0%)   | ✅ (0.0%)     | ✅ (99.9th diff 3.0E-07) | SKIP       |
| GrLTNOA                   | ✅         | ✅ (0.00%) | ✅ (+0.5%)   | ✅ (0.0%)     | ✅ (99.9th diff 1.1E-07) | SKIP       |
| ChNNCOA                   | ✅         | ✅ (0.00%) | ✅ (+0.5%)   | ✅ (0.0%)     | ✅ (99.9th diff 1.7E-07) | SKIP       |
| EarningsStreak            | ✅         | ✅ (0.19%) | ✅ (+0.0%)   | ✅ (0.0%)     | ✅ (99.9th diff 6.4E-08) | SKIP       |
| ChNAnalyst                | ✅         | ✅ (0.11%) | ✅ (-0.0%)   | ✅ (0.0%)     | ✅ (99.9th diff 0.0E+00) | SKIP       |
| CustomerMomentum          | ✅         | ✅ (0.04%) | ✅ (-0.0%)   | ✅ (0.0%)     | ✅ (99.9th diff 1.8E-07) | SKIP       |
| CompositeDebtIssuance     | ✅         | ✅ (0.00%) | ✅ (+0.9%)   | ✅ (0.0%)     | ✅ (99.9th diff 2.0E-07) | SKIP       |
| DelCOL                    | ✅         | ✅ (0.00%) | ✅ (+0.5%)   | ✅ (0.0%)     | ✅ (99.9th diff 4.3E-07) | SKIP       |
| GP                        | ✅         | ✅ (0.00%) | ✅ (+0.0%)   | ✅ (0.0%)     | ✅ (99.9th diff 2.2E-07) | SKIP       |
| DelFINL                   | ✅         | ✅ (0.00%) | ✅ (+0.0%)   | ✅ (0.0%)     | ✅ (99.9th diff 4.7E-07) | SKIP       |
| CBOperProf                | ✅         | ✅ (0.00%) | ✅ (+0.0%)   | ✅ (0.0%)     | ✅ (99.9th diff 3.6E-07) | SKIP       |
| DelLTI                    | ✅         | ✅ (0.00%) | ✅ (+0.0%)   | ✅ (0.0%)     | ✅ (99.9th diff 5.9E-07) | SKIP       |
| SurpriseRD                | ✅         | ✅ (0.00%) | ✅ (+0.5%)   | ✅ (0.0%)     | ✅ (99.9th diff 0.0E+00) | SKIP       |
| dNoa                      | ✅         | ✅ (0.00%) | ✅ (+0.0%)   | ✅ (0.0%)     | ✅ (99.9th diff 2.5E-07) | SKIP       |
| ChNWC                     | ✅         | ✅ (0.00%) | ✅ (+0.5%)   | ✅ (0.0%)     | ✅ (99.9th diff 1.4E-07) | SKIP       |
| NOA                       | ✅         | ✅ (0.00%) | ✅ (+0.5%)   | ✅ (0.0%)     | ✅ (99.9th diff 1.9E-07) | SKIP       |
| AnnouncementReturn        | ✅         | ✅ (0.00%) | ✅ (-0.0%)   | ✅ (0.0%)     | ✅ (99.9th diff 9.7E-04) | SKIP       |
| NetDebtFinance            | ✅         | ✅ (0.00%) | ✅ (+0.5%)   | ✅ (0.0%)     | ✅ (99.9th diff 2.4E-07) | SKIP       |
| OPLeverage                | ✅         | ✅ (0.00%) | ✅ (+0.0%)   | ✅ (0.0%)     | ✅ (99.9th diff 2.3E-07) | SKIP       |
| XFIN                      | ✅         | ✅ (0.00%) | ✅ (+0.0%)   | ✅ (0.0%)     | ✅ (99.9th diff 1.6E-07) | SKIP       |
| tang                      | ✅         | ✅ (0.02%) | ✅ (+0.0%)   | ✅ (0.0%)     | ✅ (99.9th diff 4.8E-07) | SKIP       |
| ConsRecomm                | ✅         | ✅ (0.26%) | ✅ (+0.0%)   | ✅ (0.0%)     | ✅ (99.9th diff 0.0E+00) | SKIP       |
| ShareRepurchase           | ✅         | ✅ (0.00%) | ✅ (+0.0%)   | ✅ (0.0%)     | ✅ (99.9th diff 0.0E+00) | SKIP       |
| AOP                       | ✅         | ✅ (0.22%) | ✅ (+4.4%)   | ✅ (0.0%)     | ✅ (99.9th diff 8.0E-05) | SKIP       |
| DelCOA                    | ✅         | ✅ (0.00%) | ✅ (+0.5%)   | ✅ (0.0%)     | ✅ (99.9th diff 4.5E-07) | SKIP       |
| ChInv                     | ✅         | ✅ (0.00%) | ✅ (+0.5%)   | ✅ (0.0%)     | ✅ (99.9th diff 2.7E-07) | SKIP       |
| BPEBM                     | ✅         | ✅ (0.00%) | ✅ (+0.0%)   | ✅ (0.0%)     | ✅ (99.9th diff 2.2E-06) | SKIP       |
| EBM                       | ✅         | ✅ (0.00%) | ✅ (+0.0%)   | ✅ (0.0%)     | ✅ (99.9th diff 2.2E-06) | SKIP       |
| CF                        | ✅         | ✅ (0.00%) | ✅ (+0.5%)   | ✅ (0.0%)     | ✅ (99.9th diff 1.5E-07) | SKIP       |
| NetEquityFinance          | ✅         | ✅ (0.00%) | ✅ (+0.5%)   | ✅ (0.0%)     | ✅ (99.9th diff 2.2E-07) | SKIP       |
| DelEqu                    | ✅         | ✅ (0.00%) | ✅ (+0.0%)   | ✅ (0.0%)     | ✅ (99.9th diff 2.1E-07) | SKIP       |
| TotalAccruals             | ✅         | ✅ (0.00%) | ✅ (+0.5%)   | ✅ (0.0%)     | ✅ (99.9th diff 2.3E-07) | SKIP       |
| AssetGrowth               | ✅         | ✅ (0.00%) | ✅ (+0.5%)   | ✅ (0.0%)     | ✅ (99.9th diff 1.3E-07) | SKIP       |
| OrderBacklogChg           | ✅         | ✅ (0.00%) | ✅ (+0.9%)   | ✅ (0.0%)     | ✅ (99.9th diff 6.0E-07) | SKIP       |
| ConvDebt                  | ✅         | ✅ (0.00%) | ✅ (+0.0%)   | ✅ (0.0%)     | ✅ (99.9th diff 0.0E+00) | SKIP       |
| ChTax                     | ✅         | ✅ (0.00%) | ✅ (+0.0%)   | ✅ (0.0%)     | ✅ (99.9th diff 2.4E-09) | SKIP       |
| PctTotAcc                 | ✅         | ✅ (0.00%) | ✅ (+0.0%)   | ✅ (0.0%)     | ✅ (99.9th diff 7.2E-08) | SKIP       |
| ChAssetTurnover           | ✅         | ✅ (0.00%) | ✅ (+0.6%)   | ✅ (0.0%)     | ✅ (99.9th diff 2.6E-07) | SKIP       |
| InvestPPEInv              | ✅         | ✅ (0.00%) | ✅ (+0.5%)   | ✅ (0.0%)     | ✅ (99.9th diff 1.8E-07) | SKIP       |
| CoskewACX                 | ✅         | ✅ (0.00%) | ✅ (+0.0%)   | ✅ (0.0%)     | ✅ (99.9th diff 3.2E-03) | SKIP       |
| PctAcc                    | ✅         | ✅ (0.00%) | ✅ (+0.2%)   | ✅ (0.0%)     | ✅ (99.9th diff 8.8E-08) | SKIP       |
| PayoutYield               | ✅         | ✅ (0.00%) | ✅ (+0.0%)   | ✅ (0.0%)     | ✅ (99.9th diff 2.7E-07) | SKIP       |
| cfp                       | ✅         | ✅ (0.00%) | ✅ (+0.0%)   | ✅ (0.0%)     | ✅ (99.9th diff 1.8E-07) | SKIP       |
| NetPayoutYield            | ✅         | ✅ (0.00%) | ✅ (+0.1%)   | ✅ (0.0%)     | ✅ (99.9th diff 1.6E-07) | SKIP       |
| RD                        | ✅         | ✅ (0.00%) | ✅ (+0.0%)   | ✅ (0.0%)     | ✅ (99.9th diff 9.7E-08) | SKIP       |
| MeanRankRevGrowth         | ✅         | ✅ (0.00%) | ✅ (+0.0%)   | ✅ (0.0%)     | ✅ (99.9th diff 6.4E-04) | SKIP       |
| Coskewness                | ✅         | ✅ (0.00%) | ✅ (+0.0%)   | ✅ (0.0%)     | ✅ (99.9th diff 2.7E-03) | SKIP       |
| InvGrowth                 | ✅         | ✅ (0.00%) | ✅ (+0.0%)   | ✅ (0.0%)     | ✅ (99.9th diff 7.2E-06) | SKIP       |
| IdioVolAHT                | ✅         | ✅ (0.00%) | ✅ (+0.0%)   | ✅ (0.0%)     | ✅ (99.9th diff 1.3E-04) | SKIP       |
| Frontier                  | ✅         | ✅ (0.00%) | ✅ (+0.0%)   | ✅ (0.0%)     | ✅ (99.9th diff 2.2E-05) | SKIP       |
| FR                        | ✅         | ✅ (0.00%) | ✅ (+0.0%)   | ✅ (0.0%)     | ✅ (99.9th diff 7.0E-07) | SKIP       |
| ProbInformedTrading       | ✅         | ✅ (0.00%) | ✅ (+0.0%)   | ✅ (0.0%)     | ✅ (99.9th diff 6.0E-07) | SKIP       |
| High52                    | ✅         | ✅ (0.00%) | ✅ (+0.0%)   | ✅ (0.0%)     | ✅ (99.9th diff 4.1E-07) | SKIP       |
| MomSeason16YrPlus         | ✅         | ✅ (0.00%) | ✅ (+0.0%)   | ✅ (0.0%)     | ✅ (99.9th diff 3.7E-07) | SKIP       |
| MomSeason11YrPlus         | ✅         | ✅ (0.00%) | ✅ (+0.0%)   | ✅ (0.0%)     | ✅ (99.9th diff 3.6E-07) | SKIP       |
| MomSeason06YrPlus         | ✅         | ✅ (0.00%) | ✅ (+0.0%)   | ✅ (0.0%)     | ✅ (99.9th diff 3.4E-07) | SKIP       |
| BidAskSpread              | ✅         | ✅ (0.00%) | ✅ (+0.0%)   | ✅ (0.0%)     | ✅ (99.9th diff 3.2E-07) | SKIP       |
| IndMom                    | ✅         | ✅ (0.00%) | ✅ (+0.0%)   | ✅ (0.0%)     | ✅ (99.9th diff 3.2E-07) | SKIP       |
| MomOffSeason              | ✅         | ✅ (0.00%) | ✅ (+0.0%)   | ✅ (0.0%)     | ✅ (99.9th diff 3.1E-07) | SKIP       |
| BMdec                     | ✅         | ✅ (0.00%) | ✅ (+0.1%)   | ✅ (0.0%)     | ✅ (99.9th diff 3.1E-07) | SKIP       |
| MomSeason                 | ✅         | ✅ (0.00%) | ✅ (+0.0%)   | ✅ (0.0%)     | ✅ (99.9th diff 3.0E-07) | SKIP       |
| zerotrade1M               | ✅         | ✅ (0.00%) | ✅ (+0.1%)   | ✅ (0.0%)     | ✅ (99.9th diff 2.8E-07) | SKIP       |
| zerotrade6M               | ✅         | ✅ (0.00%) | ✅ (+0.1%)   | ✅ (0.0%)     | ✅ (99.9th diff 2.8E-07) | SKIP       |
| OrderBacklog              | ✅         | ✅ (0.00%) | ✅ (+0.5%)   | ✅ (0.0%)     | ✅ (99.9th diff 2.8E-07) | SKIP       |
| AdExp                     | ✅         | ✅ (0.00%) | ✅ (+0.0%)   | ✅ (0.0%)     | ✅ (99.9th diff 2.7E-07) | SKIP       |
| GrAdExp                   | ✅         | ✅ (0.00%) | ✅ (+0.4%)   | ✅ (0.0%)     | ✅ (99.9th diff 2.7E-07) | SKIP       |
| Mom6m                     | ✅         | ✅ (0.00%) | ✅ (+0.0%)   | ✅ (0.0%)     | ✅ (99.9th diff 2.6E-07) | SKIP       |
| SP                        | ✅         | ✅ (0.00%) | ✅ (+0.0%)   | ✅ (0.0%)     | ✅ (99.9th diff 2.6E-07) | SKIP       |
| zerotrade12M              | ✅         | ✅ (0.00%) | ✅ (+0.0%)   | ✅ (0.0%)     | ✅ (99.9th diff 2.6E-07) | SKIP       |
| Mom12m                    | ✅         | ✅ (0.00%) | ✅ (+0.4%)   | ✅ (0.0%)     | ✅ (99.9th diff 2.5E-07) | SKIP       |
| NetDebtPrice              | ✅         | ✅ (0.00%) | ✅ (+0.0%)   | ✅ (0.0%)     | ✅ (99.9th diff 2.3E-07) | SKIP       |
| DelBreadth                | ✅         | ✅ (0.43%) | ✅ (+4.0%)   | ✅ (0.0%)     | ✅ (99.9th diff 2.2E-07) | SKIP       |
| Size                      | ✅         | ✅ (0.00%) | ✅ (+0.0%)   | ✅ (0.0%)     | ✅ (99.9th diff 2.1E-07) | SKIP       |
| BookLeverage              | ✅         | ✅ (0.00%) | ✅ (+0.0%)   | ✅ (0.0%)     | ✅ (99.9th diff 2.0E-07) | SKIP       |
| Price                     | ✅         | ✅ (0.00%) | ✅ (+0.0%)   | ✅ (0.0%)     | ✅ (99.9th diff 2.0E-07) | SKIP       |
| Leverage                  | ✅         | ✅ (0.00%) | ✅ (+0.0%)   | ✅ (0.0%)     | ✅ (99.9th diff 1.9E-07) | SKIP       |
| Beta                      | ✅         | ✅ (0.00%) | ✅ (+1.6%)   | ✅ (0.0%)     | ✅ (99.9th diff 1.9E-07) | SKIP       |
| MomSeasonShort            | ✅         | ✅ (0.13%) | ✅ (-0.1%)   | ✅ (0.0%)     | ✅ (99.9th diff 1.7E-07) | SKIP       |
| STreversal                | ✅         | ✅ (0.00%) | ✅ (+0.0%)   | ✅ (0.0%)     | ✅ (99.9th diff 1.6E-07) | SKIP       |
| DolVol                    | ✅         | ✅ (0.00%) | ✅ (+0.0%)   | ✅ (0.0%)     | ✅ (99.9th diff 1.5E-07) | SKIP       |
| AM                        | ✅         | ✅ (0.00%) | ✅ (+0.0%)   | ✅ (0.0%)     | ✅ (99.9th diff 1.5E-07) | SKIP       |
| BrandInvest               | ✅         | ✅ (0.00%) | ✅ (+4.9%)   | ✅ (0.0%)     | ✅ (99.9th diff 1.2E-07) | SKIP       |
| EP                        | ✅         | ✅ (0.00%) | ✅ (+0.0%)   | ✅ (0.0%)     | ✅ (99.9th diff 1.0E-07) | SKIP       |
| std_turn                  | ✅         | ✅ (0.02%) | ✅ (+1.6%)   | ✅ (0.0%)     | ✅ (99.9th diff 1.0E-07) | SKIP       |
| IO_ShortInterest          | ✅         | ✅ (0.00%) | ✅ (+0.0%)   | ✅ (0.0%)     | ✅ (99.9th diff 9.9E-08) | SKIP       |
| ShortInterest             | ✅         | ✅ (0.00%) | ✅ (+0.0%)   | ✅ (0.0%)     | ✅ (99.9th diff 9.0E-08) | SKIP       |
| EntMult                   | ✅         | ✅ (0.00%) | ✅ (-0.0%)   | ✅ (0.0%)     | ✅ (99.9th diff 6.1E-08) | SKIP       |
| CashProd                  | ✅         | ✅ (0.00%) | ✅ (+0.0%)   | ✅ (0.0%)     | ✅ (99.9th diff 4.9E-08) | SKIP       |
| ChEQ                      | ✅         | ✅ (0.00%) | ✅ (+0.4%)   | ✅ (0.0%)     | ✅ (99.9th diff 4.0E-08) | SKIP       |
| ChInvIA                   | ✅         | ✅ (0.00%) | ✅ (+0.0%)   | ✅ (0.0%)     | ✅ (99.9th diff 2.3E-08) | SKIP       |
| RoE                       | ✅         | ✅ (0.00%) | ✅ (+0.0%)   | ✅ (0.0%)     | ✅ (99.9th diff 2.3E-08) | SKIP       |
| ShareIss5Y                | ✅         | ✅ (0.00%) | ✅ (+0.0%)   | ✅ (0.0%)     | ✅ (99.9th diff 7.6E-10) | SKIP       |
| ShareIss1Y                | ✅         | ✅ (0.00%) | ✅ (+0.0%)   | ✅ (0.0%)     | ✅ (99.9th diff 7.5E-10) | SKIP       |
| EquityDuration            | ✅         | ✅ (0.00%) | ✅ (+2.5%)   | ✅ (0.0%)     | ✅ (99.9th diff 4.9E-14) | SKIP       |
| ReturnSkew                | ✅         | ✅ (0.00%) | ✅ (+0.0%)   | ✅ (0.0%)     | ✅ (99.9th diff 5.4E-15) | SKIP       |
| RealizedVol               | ✅         | ✅ (0.13%) | ✅ (-0.1%)   | ✅ (0.0%)     | ✅ (99.9th diff 2.7E-15) | SKIP       |
| IndRetBig                 | ✅         | ✅ (0.21%) | ✅ (+0.3%)   | ✅ (0.0%)     | ✅ (99.9th diff 2.4E-15) | SKIP       |
| Mom12mOffSeason           | ✅         | ✅ (0.00%) | ✅ (+0.0%)   | ✅ (0.0%)     | ✅ (99.9th diff 1.4E-15) | SKIP       |
| grcapx3y                  | ✅         | ✅ (0.76%) | ✅ (+0.9%)   | ✅ (0.0%)     | ✅ (99.9th diff 9.3E-20) | SKIP       |
| AccrualsBM                | ✅         | ✅ (0.48%) | ✅ (+0.7%)   | ✅ (0.0%)     | ✅ (99.9th diff 0.0E+00) | SKIP       |
| DebtIssuance              | ✅         | ✅ (0.00%) | ✅ (+0.0%)   | ✅ (0.0%)     | ✅ (99.9th diff 0.0E+00) | SKIP       |
| FirmAge                   | ✅         | ✅ (0.00%) | ✅ (+0.0%)   | ✅ (0.0%)     | ✅ (99.9th diff 0.0E+00) | SKIP       |
| Governance                | ✅         | ✅ (0.00%) | ✅ (+0.0%)   | ✅ (0.0%)     | ✅ (99.9th diff 0.0E+00) | SKIP       |
| MaxRet                    | ✅         | ✅ (0.00%) | ✅ (+0.0%)   | ✅ (0.0%)     | ✅ (99.9th diff 0.0E+00) | SKIP       |
| MomRev                    | ✅         | ✅ (0.14%) | ✅ (+0.1%)   | ✅ (0.0%)     | ✅ (99.9th diff 0.0E+00) | SKIP       |
| OScore                    | ✅         | ✅ (0.04%) | ✅ (+0.0%)   | ✅ (0.0%)     | ✅ (99.9th diff 0.0E+00) | SKIP       |
| ShareVol                  | ✅         | ✅ (0.00%) | ✅ (+0.1%)   | ✅ (0.0%)     | ✅ (99.9th diff 0.0E+00) | SKIP       |
| Spinoff                   | ✅         | ✅ (0.00%) | ✅ (+0.0%)   | ✅ (0.0%)     | ✅ (99.9th diff 0.0E+00) | SKIP       |

**Overall**: 169/212 available predictors passed validation
  - Natural passes: 164
  - Overridden passes: 5
**Python CSVs**: 212/212 predictors have Python implementation
\* = Manual override applied (see Predictors/overrides.yaml for details)

## Detailed Results

### AM

**Status**: ✅ PASSED

**Test Results**:
- Test 1 - Superset check: ✅ PASSED
- Test 2 - NumRows check: ✅ PASSED (Python has +0.00% rows vs Stata)
- Test 3 - Precision1 check: ✅ PASSED
- Test 4 - Precision2 check: ✅ PASSED
- Test 5 - T-stat check: NA (Skipped for faster execution)

**Observations**:
- Stata:  3,038,206
- Python: 3,038,208
- Common: 3,038,206

**Precision1**: 0.000% obs with std_diff >= 1.00e-02 (tolerance: < 1%)

**Precision2**: 100th percentile diff = 1.48e-07 (tolerance: < 1.00e-01)

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
- Test 1 - Superset check: ✅ PASSED
- Test 2 - NumRows check: ✅ PASSED (Python has +4.41% rows vs Stata)
- Test 3 - Precision1 check: ✅ PASSED
- Test 4 - Precision2 check: ✅ PASSED
- Test 5 - T-stat check: NA (Skipped for faster execution)

**Observations**:
- Stata:  1,244,664
- Python: 1,299,504
- Common: 1,241,880

**Precision1**: 0.002% obs with std_diff >= 1.00e-02 (tolerance: < 1%)

**Precision2**: 100th percentile diff = 8.02e-05 (tolerance: < 1.00e-01)

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
- Test 1 - Superset check: ❌ FAILED (Python missing 271908 Stata observations)
- Test 2 - NumRows check: ✅ PASSED (Python has -10.09% rows vs Stata)
- Test 3 - Precision1 check: ❌ FAILED
- Test 4 - Precision2 check: ❌ FAILED
- Test 5 - T-stat check: NA (Skipped for faster execution)

**Observations**:
- Stata:  2,570,664
- Python: 2,311,196
- Common: 2,298,756

**Precision1**: 29.278% obs with std_diff >= 1.00e-02 (tolerance: < 1%)

**Precision2**: 100th percentile diff = 9.73e-01 (tolerance: < 1.00e-01)

**Summary Statistics** (Common Observations):

| Statistic  |          Stata |         Python |     Difference | Std Difference |
|------------|----------------|----------------|----------------|----------------|
| count      |       2.30e+06 |       2.30e+06 |       2.30e+06 |       2.30e+06 |
| mean       |       1.08e-04 |       1.23e-04 |       1.48e-05 |       9.76e-05 |
| std        |         0.1514 |         0.1515 |         0.0132 |         0.0873 |
| min        |        -8.2957 |        -8.2790 |        -1.2879 |        -8.5051 |
| 25%        |        -0.0407 |        -0.0407 |      -2.46e-04 |        -0.0016 |
| 50%        |         0.0064 |         0.0063 |      -2.66e-10 |      -1.76e-09 |
| 75%        |         0.0515 |         0.0514 |       5.76e-05 |       3.80e-04 |
| max        |         2.7043 |         2.7040 |         1.4356 |         9.4807 |

**Regression Analysis** (Python ~ Stata):

- **Model**: python = 0.0000 + 0.9966 * stata
- **R-squared**: 0.9924
- **N observations**: 2,298,756

| Coefficient |     Estimate |    Std Error | t-statistic |   p-value |
|-------------|--------------|--------------|-------------|----------|
| Intercept   |     1.51e-05 |     8.71e-06 |      1.7385 |     0.082 |
| Slope       |       0.9966 |     5.75e-05 |  17326.6438 |     0.000 |

**Feedback**:
- Num observations with std_diff >= TOL_DIFF_1: 673031/2298756 (29.278%)
- Stata standard deviation: 1.51e-01

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
   permno  yyyymm    python     stata      diff
0   84005  200106  0.148008 -1.287609  1.435617
1   84005  200107  0.148008 -1.287609  1.435617
2   84005  200108  0.148008 -1.287609  1.435617
3   85712  200103  0.237234  1.525127 -1.287893
4   85712  200104  0.237234  1.525127 -1.287893
5   85712  200105  0.237234  1.525127 -1.287893
6   77649  199709 -0.307171  0.603173 -0.910344
7   77649  199710 -0.307171  0.603173 -0.910344
8   77649  199711 -0.307171  0.603173 -0.910344
9   77649  199712 -0.307171  0.603173 -0.910344
```

**Largest Differences Before 1950**:
```
No data before 1950
```

---

### Accruals

**Status**: ✅ PASSED

**Test Results**:
- Test 1 - Superset check: ✅ PASSED
- Test 2 - NumRows check: ✅ PASSED (Python has +0.50% rows vs Stata)
- Test 3 - Precision1 check: ✅ PASSED
- Test 4 - Precision2 check: ✅ PASSED
- Test 5 - T-stat check: NA (Skipped for faster execution)

**Observations**:
- Stata:  3,259,701
- Python: 3,276,154
- Common: 3,259,701

**Precision1**: 0.009% obs with std_diff >= 1.00e-02 (tolerance: < 1%)

**Precision2**: 100th percentile diff = 2.44e-07 (tolerance: < 1.00e-01)

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
- Test 1 - Superset check: ✅ PASSED
- Test 2 - NumRows check: ✅ PASSED (Python has +0.69% rows vs Stata)
- Test 3 - Precision1 check: ✅ PASSED
- Test 4 - Precision2 check: ✅ PASSED
- Test 5 - T-stat check: NA (Skipped for faster execution)

**Observations**:
- Stata:  220,066
- Python: 221,587
- Common: 219,001

**Precision1**: 0.000% obs with std_diff >= 1.00e-02 (tolerance: < 1%)

**Precision2**: 100th percentile diff = 0.00e+00 (tolerance: < 1.00e-01)

**Summary Statistics** (Common Observations):

| Statistic  |          Stata |         Python |     Difference | Std Difference |
|------------|----------------|----------------|----------------|----------------|
| count      |    219001.0000 |    219001.0000 |    219001.0000 |    219001.0000 |
| mean       |         0.4832 |         0.4832 |         0.0000 |         0.0000 |
| std        |         0.4997 |         0.4997 |         0.0000 |         0.0000 |
| min        |         0.0000 |         0.0000 |         0.0000 |         0.0000 |
| 25%        |         0.0000 |         0.0000 |         0.0000 |         0.0000 |
| 50%        |         0.0000 |         0.0000 |         0.0000 |         0.0000 |
| 75%        |         1.0000 |         1.0000 |         0.0000 |         0.0000 |
| max        |         1.0000 |         1.0000 |         0.0000 |         0.0000 |

**Regression Analysis** (Python ~ Stata):

- **Model**: python = -0.0000 + 1.0000 * stata
- **R-squared**: 1.0000
- **N observations**: 219,001

| Coefficient |     Estimate |    Std Error | t-statistic |   p-value |
|-------------|--------------|--------------|-------------|----------|
| Intercept   |    -9.77e-15 |     1.51e-16 |    -64.5004 |     0.000 |
| Slope       |       1.0000 |     2.18e-16 |    4.59e+15 |     0.000 |

**Feedback**:
- Num observations with std_diff >= TOL_DIFF_1: 0/219001 (0.000%)
- Stata standard deviation: 5.00e-01

---

### Activism1

**Status**: ❌ FAILED

**Test Results**:
- Test 1 - Superset check: ✅ PASSED
- Test 2 - NumRows check: ❌ FAILED (Python has +179.42% rows vs Stata)
- Test 3 - Precision1 check: ✅ PASSED
- Test 4 - Precision2 check: ✅ PASSED
- Test 5 - T-stat check: NA (Skipped for faster execution)

**Observations**:
- Stata:  108,733
- Python: 303,825
- Common: 108,348

**Precision1**: 0.000% obs with std_diff >= 1.00e-02 (tolerance: < 1%)

**Precision2**: 100th percentile diff = 0.00e+00 (tolerance: < 1.00e-01)

**Summary Statistics** (Common Observations):

| Statistic  |          Stata |         Python |     Difference | Std Difference |
|------------|----------------|----------------|----------------|----------------|
| count      |    108348.0000 |    108348.0000 |    108348.0000 |    108348.0000 |
| mean       |        14.8856 |        14.8856 |         0.0000 |         0.0000 |
| std        |         2.7243 |         2.7243 |         0.0000 |         0.0000 |
| min        |         6.0000 |         6.0000 |         0.0000 |         0.0000 |
| 25%        |        13.0000 |        13.0000 |         0.0000 |         0.0000 |
| 50%        |        15.0000 |        15.0000 |         0.0000 |         0.0000 |
| 75%        |        17.0000 |        17.0000 |         0.0000 |         0.0000 |
| max        |        23.0000 |        23.0000 |         0.0000 |         0.0000 |

**Regression Analysis** (Python ~ Stata):

- **Model**: python = 0.0000 + 1.0000 * stata
- **R-squared**: 1.0000
- **N observations**: 108,348

| Coefficient |     Estimate |    Std Error | t-statistic |   p-value |
|-------------|--------------|--------------|-------------|----------|
| Intercept   |     2.88e-12 |     9.04e-15 |    318.5036 |     0.000 |
| Slope       |       1.0000 |     5.97e-16 |    1.67e+15 |     0.000 |

**Feedback**:
- Num observations with std_diff >= TOL_DIFF_1: 0/108348 (0.000%)
- Stata standard deviation: 2.72e+00

---

### Activism2

**Status**: ❌ FAILED

**Test Results**:
- Test 1 - Superset check: ❌ FAILED (Python missing 606 Stata observations)
- Test 2 - NumRows check: ✅ PASSED (Python has -2.01% rows vs Stata)
- Test 3 - Precision1 check: ✅ PASSED
- Test 4 - Precision2 check: ✅ PASSED
- Test 5 - T-stat check: NA (Skipped for faster execution)

**Observations**:
- Stata:  30,170
- Python: 29,564
- Common: 29,564

**Precision1**: 0.000% obs with std_diff >= 1.00e-02 (tolerance: < 1%)

**Precision2**: 100th percentile diff = 2.36e-07 (tolerance: < 1.00e-01)

**Summary Statistics** (Common Observations):

| Statistic  |          Stata |         Python |     Difference | Std Difference |
|------------|----------------|----------------|----------------|----------------|
| count      |     29564.0000 |     29564.0000 |     29564.0000 |     29564.0000 |
| mean       |         9.4530 |         9.4530 |      -9.22e-09 |      -7.26e-10 |
| std        |        12.7006 |        12.7006 |       3.48e-07 |       2.74e-08 |
| min        |         0.0000 |         0.0000 |      -4.00e-06 |      -3.15e-07 |
| 25%        |         0.0000 |         0.0000 |         0.0000 |         0.0000 |
| 50%        |         7.5533 |         7.5533 |         0.0000 |         0.0000 |
| 75%        |        10.8365 |        10.8365 |         0.0000 |         0.0000 |
| max        |       221.2826 |       221.2826 |       4.00e-06 |       3.15e-07 |

**Regression Analysis** (Python ~ Stata):

- **Model**: python = 0.0000 + 1.0000 * stata
- **R-squared**: 1.0000
- **N observations**: 29,564

| Coefficient |     Estimate |    Std Error | t-statistic |   p-value |
|-------------|--------------|--------------|-------------|----------|
| Intercept   |     2.37e-08 |     2.50e-09 |      9.4909 |     0.000 |
| Slope       |       1.0000 |     1.58e-10 |    6.33e+09 |     0.000 |

**Feedback**:
- Num observations with std_diff >= TOL_DIFF_1: 0/29564 (0.000%)
- Stata standard deviation: 1.27e+01

---

### AdExp

**Status**: ✅ PASSED

**Test Results**:
- Test 1 - Superset check: ✅ PASSED
- Test 2 - NumRows check: ✅ PASSED (Python has +0.00% rows vs Stata)
- Test 3 - Precision1 check: ✅ PASSED
- Test 4 - Precision2 check: ✅ PASSED
- Test 5 - T-stat check: NA (Skipped for faster execution)

**Observations**:
- Stata:  1,049,030
- Python: 1,049,037
- Common: 1,049,030

**Precision1**: 0.000% obs with std_diff >= 1.00e-02 (tolerance: < 1%)

**Precision2**: 100th percentile diff = 2.74e-07 (tolerance: < 1.00e-01)

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
- Test 1 - Superset check: ✅ PASSED
- Test 2 - NumRows check: ✅ PASSED (Python has +0.02% rows vs Stata)
- Test 3 - Precision1 check: ✅ PASSED
- Test 4 - Precision2 check: ✅ PASSED
- Test 5 - T-stat check: NA (Skipped for faster execution)

**Observations**:
- Stata:  1,920,473
- Python: 1,920,793
- Common: 1,917,427

**Precision1**: 0.038% obs with std_diff >= 1.00e-02 (tolerance: < 1%)

**Precision2**: 100th percentile diff = 1.38e-07 (tolerance: < 1.00e-01)

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
- Test 1 - Superset check: ✅ PASSED
- Test 2 - NumRows check: ✅ PASSED (Python has +4.41% rows vs Stata)
- Test 3 - Precision1 check: ✅ PASSED
- Test 4 - Precision2 check: ✅ PASSED
- Test 5 - T-stat check: NA (Skipped for faster execution)

**Observations**:
- Stata:  1,244,664
- Python: 1,299,504
- Common: 1,241,880

**Precision1**: 0.263% obs with std_diff >= 1.00e-02 (tolerance: < 1%)

**Precision2**: 100th percentile diff = 3.10e-02 (tolerance: < 1.00e-01)

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
- Test 1 - Superset check: ✅ PASSED
- Test 2 - NumRows check: ✅ PASSED (Python has -0.00% rows vs Stata)
- Test 3 - Precision1 check: ✅ PASSED
- Test 4 - Precision2 check: ✅ PASSED
- Test 5 - T-stat check: NA (Skipped for faster execution)

**Observations**:
- Stata:  2,922,373
- Python: 2,922,354
- Common: 2,922,290

**Precision1**: 0.003% obs with std_diff >= 1.00e-02 (tolerance: < 1%)

**Precision2**: 100th percentile diff = 9.73e-04 (tolerance: < 1.00e-01)

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
- Test 1 - Superset check: ✅ PASSED
- Test 2 - NumRows check: ✅ PASSED (Python has +0.50% rows vs Stata)
- Test 3 - Precision1 check: ✅ PASSED
- Test 4 - Precision2 check: ✅ PASSED
- Test 5 - T-stat check: NA (Skipped for faster execution)

**Observations**:
- Stata:  3,295,125
- Python: 3,311,751
- Common: 3,295,125

**Precision1**: 0.001% obs with std_diff >= 1.00e-02 (tolerance: < 1%)

**Precision2**: 100th percentile diff = 1.29e-07 (tolerance: < 1.00e-01)

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
- Test 1 - Superset check: ✅ PASSED
- Test 2 - NumRows check: ✅ PASSED (Python has +0.00% rows vs Stata)
- Test 3 - Precision1 check: ✅ PASSED
- Test 4 - Precision2 check: ✅ PASSED
- Test 5 - T-stat check: NA (Skipped for faster execution)

**Observations**:
- Stata:  2,715,090
- Python: 2,715,204
- Common: 2,715,090

**Precision1**: 0.032% obs with std_diff >= 1.00e-02 (tolerance: < 1%)

**Precision2**: 100th percentile diff = 2.24e-07 (tolerance: < 1.00e-01)

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
- Test 1 - Superset check: ✅ PASSED
- Test 2 - NumRows check: ✅ PASSED (Python has +0.07% rows vs Stata)
- Test 3 - Precision1 check: ✅ PASSED
- Test 4 - Precision2 check: ✅ PASSED
- Test 5 - T-stat check: NA (Skipped for faster execution)

**Observations**:
- Stata:  2,996,716
- Python: 2,998,697
- Common: 2,996,716

**Precision1**: 0.000% obs with std_diff >= 1.00e-02 (tolerance: < 1%)

**Precision2**: 100th percentile diff = 3.05e-07 (tolerance: < 1.00e-01)

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
- Test 1 - Superset check: ✅ PASSED
- Test 2 - NumRows check: ✅ PASSED (Python has +0.00% rows vs Stata)
- Test 3 - Precision1 check: ✅ PASSED
- Test 4 - Precision2 check: ✅ PASSED
- Test 5 - T-stat check: NA (Skipped for faster execution)

**Observations**:
- Stata:  2,924,820
- Python: 2,924,826
- Common: 2,924,820

**Precision1**: 0.001% obs with std_diff >= 1.00e-02 (tolerance: < 1%)

**Precision2**: 100th percentile diff = 2.19e-06 (tolerance: < 1.00e-01)

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
- Test 1 - Superset check: ✅ PASSED
- Test 2 - NumRows check: ✅ PASSED (Python has +1.59% rows vs Stata)
- Test 3 - Precision1 check: ✅ PASSED
- Test 4 - Precision2 check: ✅ PASSED
- Test 5 - T-stat check: NA (Skipped for faster execution)

**Observations**:
- Stata:  4,285,574
- Python: 4,353,773
- Common: 4,285,574

**Precision1**: 0.000% obs with std_diff >= 1.00e-02 (tolerance: < 1%)

**Precision2**: 100th percentile diff = 1.93e-07 (tolerance: < 1.00e-01)

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

**Status**: ❌ FAILED

**Test Results**:
- Test 1 - Superset check: ✅ PASSED
- Test 2 - NumRows check: ❌ FAILED (Python has +9.54% rows vs Stata)
- Test 3 - Precision1 check: ❌ FAILED
- Test 4 - Precision2 check: ❌ FAILED
- Test 5 - T-stat check: NA (Skipped for faster execution)

**Observations**:
- Stata:  3,794,018
- Python: 4,156,049
- Common: 3,784,837

**Precision1**: 6.256% obs with std_diff >= 1.00e-02 (tolerance: < 1%)

**Precision2**: 100th percentile diff = 8.77e-01 (tolerance: < 1.00e-01)

**Summary Statistics** (Common Observations):

| Statistic  |          Stata |         Python |     Difference | Std Difference |
|------------|----------------|----------------|----------------|----------------|
| count      |       3.78e+06 |       3.78e+06 |       3.78e+06 |       3.78e+06 |
| mean       |         0.9809 |         0.9797 |        -0.0012 |        -0.0019 |
| std        |         0.6411 |         0.6407 |         0.0384 |         0.0599 |
| min        |       7.25e-07 |         0.0000 |        -3.9823 |        -6.2115 |
| 25%        |         0.5198 |         0.5188 |        -0.0018 |        -0.0028 |
| 50%        |         0.8964 |         0.8954 |        -0.0010 |        -0.0016 |
| 75%        |         1.3175 |         1.3161 |      -4.94e-04 |      -7.70e-04 |
| max        |        12.6047 |        12.5623 |         4.7939 |         7.4774 |

**Regression Analysis** (Python ~ Stata):

- **Model**: python = 0.0012 + 0.9976 * stata
- **R-squared**: 0.9964
- **N observations**: 3,784,837

| Coefficient |     Estimate |    Std Error | t-statistic |   p-value |
|-------------|--------------|--------------|-------------|----------|
| Intercept   |       0.0012 |     3.61e-05 |     32.2317 |     0.000 |
| Slope       |       0.9976 |     3.08e-05 |  32422.5473 |     0.000 |

**Feedback**:
- Num observations with std_diff >= TOL_DIFF_1: 236770/3784837 (6.256%)
- Stata standard deviation: 6.41e-01

**Most Recent Bad Observations**:
```
   permno  yyyymm    python     stata      diff
0   10066  202412  0.366776  0.247929  0.118848
1   11153  202412  0.194148  0.253281 -0.059133
2   11379  202412  1.593719  1.445916  0.147803
3   12928  202412  0.551779  0.931920 -0.380141
4   13563  202412  0.903798  0.608259  0.295539
5   13828  202412  0.846968  0.970209 -0.123241
6   13878  202412  0.978277  0.966509  0.011768
7   13947  202412  2.605158  2.657374 -0.052215
8   14051  202412  3.479917  3.465529  0.014388
9   14469  202412  2.212209  1.759658  0.452551
```

**Largest Differences**:
```
   permno  yyyymm    python     stata      diff
0   11453  199312  7.664115  2.870236  4.793879
1   65622  199401  0.593349  4.575622 -3.982273
2   65622  199402  0.930784  4.732967 -3.802183
3   65622  199312  0.867006  4.276299 -3.409292
4   10872  199403  0.647807  4.045698 -3.397891
5   10216  199301  0.659991  4.034531 -3.374539
6   10872  199404  0.422160  3.782309 -3.360148
7   10216  199304  0.823704  4.174334 -3.350630
8   10216  199212  0.615237  3.899257 -3.284020
9   10872  199405  0.912626  4.134042 -3.221416
```

**Largest Differences Before 1950**:
```
   permno  yyyymm    python     stata      diff
0   14269  194112  4.258444  5.277860 -1.019417
1   13389  194108  3.766282  2.927140  0.839142
2   14269  194201  3.999881  4.830401 -0.830520
3   11797  193702  2.478371  1.648720  0.829651
4   11252  194112  4.024742  4.843852 -0.819109
5   20271  194408  1.522680  2.332971 -0.810292
6   18649  193710  1.339925  2.143693 -0.803768
7   11797  193701  2.275098  1.506865  0.768232
8   12677  192910  0.713803  1.460106 -0.746303
9   14269  194202  4.036062  4.760625 -0.724563
```

---

### BetaLiquidityPS

**Status**: ✅ PASSED

**Test Results**:
- Test 1 - Superset check: ✅ PASSED
- Test 2 - NumRows check: ✅ PASSED (Python has +1.62% rows vs Stata)
- Test 3 - Precision1 check: ✅ PASSED
- Test 4 - Precision2 check: ✅ PASSED
- Test 5 - T-stat check: NA (Skipped for faster execution)

**Observations**:
- Stata:  3,423,856
- Python: 3,479,410
- Common: 3,423,856

**Precision1**: 0.309% obs with std_diff >= 1.00e-02 (tolerance: < 1%)

**Precision2**: 100th percentile diff = 1.51e-02 (tolerance: < 1.00e-01)

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
- Test 1 - Superset check: ✅ PASSED
- Test 2 - NumRows check: ✅ PASSED (Python has +1.73% rows vs Stata)
- Test 3 - Precision1 check: ✅ PASSED
- Test 4 - Precision2 check: ✅ PASSED
- Test 5 - T-stat check: NA (Skipped for faster execution)

**Observations**:
- Stata:  2,292,350
- Python: 2,332,084
- Common: 2,292,350

**Precision1**: 0.013% obs with std_diff >= 1.00e-02 (tolerance: < 1%)

**Precision2**: 100th percentile diff = 6.31e-03 (tolerance: < 1.00e-01)

**Summary Statistics** (Common Observations):

| Statistic  |          Stata |         Python |     Difference | Std Difference |
|------------|----------------|----------------|----------------|----------------|
| count      |       2.29e+06 |       2.29e+06 |       2.29e+06 |       2.29e+06 |
| mean       |         0.6390 |         0.6390 |       1.65e-06 |       3.22e-06 |
| std        |         0.5111 |         0.5111 |       3.74e-04 |       7.32e-04 |
| min        |       -10.7373 |       -10.7363 |        -0.0114 |        -0.0224 |
| 25%        |         0.3065 |         0.3065 |      -2.17e-05 |      -4.24e-05 |
| 50%        |         0.5661 |         0.5661 |       5.54e-08 |       1.08e-07 |
| 75%        |         0.8925 |         0.8926 |       8.11e-05 |       1.59e-04 |
| max        |         8.5702 |         8.5702 |         0.0068 |         0.0133 |

**Regression Analysis** (Python ~ Stata):

- **Model**: python = -0.0000 + 1.0001 * stata
- **R-squared**: 1.0000
- **N observations**: 2,292,350

| Coefficient |     Estimate |    Std Error | t-statistic |   p-value |
|-------------|--------------|--------------|-------------|----------|
| Intercept   |    -4.64e-05 |     3.93e-07 |   -118.0172 |     0.000 |
| Slope       |       1.0001 |     4.81e-07 |    2.08e+06 |     0.000 |

**Feedback**:
- Num observations with std_diff >= TOL_DIFF_1: 307/2292350 (0.013%)
- Stata standard deviation: 5.11e-01

---

### BidAskSpread

**Status**: ✅ PASSED

**Test Results**:
- Test 1 - Superset check: ✅ PASSED
- Test 2 - NumRows check: ✅ PASSED (Python has +0.00% rows vs Stata)
- Test 3 - Precision1 check: ✅ PASSED
- Test 4 - Precision2 check: ✅ PASSED
- Test 5 - T-stat check: NA (Skipped for faster execution)

**Observations**:
- Stata:  4,481,622
- Python: 4,481,622
- Common: 4,481,622

**Precision1**: 0.000% obs with std_diff >= 1.00e-02 (tolerance: < 1%)

**Precision2**: 100th percentile diff = 3.22e-07 (tolerance: < 1.00e-01)

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
- Test 1 - Superset check: ✅ PASSED
- Test 2 - NumRows check: ✅ PASSED (Python has +0.03% rows vs Stata)
- Test 3 - Precision1 check: ✅ PASSED
- Test 4 - Precision2 check: ✅ PASSED
- Test 5 - T-stat check: NA (Skipped for faster execution)

**Observations**:
- Stata:  3,606,159
- Python: 3,607,287
- Common: 3,606,159

**Precision1**: 0.000% obs with std_diff >= 1.00e-02 (tolerance: < 1%)

**Precision2**: 100th percentile diff = 1.99e-07 (tolerance: < 1.00e-01)

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
- Test 1 - Superset check: ✅ PASSED
- Test 2 - NumRows check: ✅ PASSED (Python has +4.85% rows vs Stata)
- Test 3 - Precision1 check: ✅ PASSED
- Test 4 - Precision2 check: ✅ PASSED
- Test 5 - T-stat check: NA (Skipped for faster execution)

**Observations**:
- Stata:  485,304
- Python: 508,848
- Common: 485,304

**Precision1**: 0.000% obs with std_diff >= 1.00e-02 (tolerance: < 1%)

**Precision2**: 100th percentile diff = 1.23e-07 (tolerance: < 1.00e-01)

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
- Test 1 - Superset check: ✅ PASSED
- Test 2 - NumRows check: ✅ PASSED (Python has +0.00% rows vs Stata)
- Test 3 - Precision1 check: ✅ PASSED
- Test 4 - Precision2 check: ✅ PASSED
- Test 5 - T-stat check: NA (Skipped for faster execution)

**Observations**:
- Stata:  2,283,861
- Python: 2,283,897
- Common: 2,283,861

**Precision1**: 0.006% obs with std_diff >= 1.00e-02 (tolerance: < 1%)

**Precision2**: 100th percentile diff = 3.60e-07 (tolerance: < 1.00e-01)

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
- Test 1 - Superset check: ✅ PASSED
- Test 2 - NumRows check: ✅ PASSED (Python has +0.49% rows vs Stata)
- Test 3 - Precision1 check: ✅ PASSED
- Test 4 - Precision2 check: ✅ PASSED
- Test 5 - T-stat check: NA (Skipped for faster execution)

**Observations**:
- Stata:  3,038,206
- Python: 3,053,133
- Common: 3,038,206

**Precision1**: 0.001% obs with std_diff >= 1.00e-02 (tolerance: < 1%)

**Precision2**: 100th percentile diff = 1.50e-07 (tolerance: < 1.00e-01)

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
- Test 1 - Superset check: ✅ PASSED
- Test 2 - NumRows check: ✅ PASSED (Python has -0.30% rows vs Stata)
- Test 3 - Precision1 check: ✅ PASSED
- Test 4 - Precision2 check: ✅ PASSED
- Test 5 - T-stat check: NA (Skipped for faster execution)

**Observations**:
- Stata:  684,140
- Python: 682,114
- Common: 679,061

**Precision1**: 0.050% obs with std_diff >= 1.00e-02 (tolerance: < 1%)

**Precision2**: 100th percentile diff = 1.83e-07 (tolerance: < 1.00e-01)

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

**Status**: ❌ FAILED

**Test Results**:
- Test 1 - Superset check: ✅ PASSED
- Test 2 - NumRows check: ❌ FAILED (Python has +7.28% rows vs Stata)
- Test 3 - Precision1 check: ✅ PASSED
- Test 4 - Precision2 check: ✅ PASSED
- Test 5 - T-stat check: NA (Skipped for faster execution)

**Observations**:
- Stata:  2,096,350
- Python: 2,249,039
- Common: 2,095,954

**Precision1**: 0.048% obs with std_diff >= 1.00e-02 (tolerance: < 1%)

**Precision2**: 100th percentile diff = 1.54e-07 (tolerance: < 1.00e-01)

**Summary Statistics** (Common Observations):

| Statistic  |          Stata |         Python |     Difference | Std Difference |
|------------|----------------|----------------|----------------|----------------|
| count      |       2.10e+06 |       2.10e+06 |       2.10e+06 |       2.10e+06 |
| mean       |         0.1672 |         0.1672 |      -2.93e-06 |      -1.37e-05 |
| std        |         0.2141 |         0.2141 |         0.0017 |         0.0080 |
| min        |        -0.1432 |        -0.1432 |        -0.3351 |        -1.5649 |
| 25%        |         0.0249 |         0.0249 |      -1.29e-09 |      -6.05e-09 |
| 50%        |         0.0754 |         0.0754 |         0.0000 |         0.0000 |
| 75%        |         0.2202 |         0.2202 |       1.29e-09 |       6.02e-09 |
| max        |         1.0000 |         1.0000 |         0.6778 |         3.1653 |

**Regression Analysis** (Python ~ Stata):

- **Model**: python = 0.0000 + 1.0000 * stata
- **R-squared**: 0.9999
- **N observations**: 2,095,954

| Coefficient |     Estimate |    Std Error | t-statistic |   p-value |
|-------------|--------------|--------------|-------------|----------|
| Intercept   |     1.54e-06 |     1.50e-06 |      1.0271 |     0.304 |
| Slope       |       1.0000 |     5.53e-06 | 180808.3589 |     0.000 |

**Feedback**:
- Num observations with std_diff >= TOL_DIFF_1: 1005/2095954 (0.048%)
- Stata standard deviation: 2.14e-01

---

### CashProd

**Status**: ✅ PASSED

**Test Results**:
- Test 1 - Superset check: ✅ PASSED
- Test 2 - NumRows check: ✅ PASSED (Python has +0.00% rows vs Stata)
- Test 3 - Precision1 check: ✅ PASSED
- Test 4 - Precision2 check: ✅ PASSED
- Test 5 - T-stat check: NA (Skipped for faster execution)

**Observations**:
- Stata:  3,002,825
- Python: 3,002,827
- Common: 3,002,825

**Precision1**: 0.000% obs with std_diff >= 1.00e-02 (tolerance: < 1%)

**Precision2**: 100th percentile diff = 4.89e-08 (tolerance: < 1.00e-01)

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
- Test 1 - Superset check: ✅ PASSED
- Test 2 - NumRows check: ✅ PASSED (Python has +0.59% rows vs Stata)
- Test 3 - Precision1 check: ✅ PASSED
- Test 4 - Precision2 check: ✅ PASSED
- Test 5 - T-stat check: NA (Skipped for faster execution)

**Observations**:
- Stata:  2,503,228
- Python: 2,517,886
- Common: 2,503,228

**Precision1**: 0.000% obs with std_diff >= 1.00e-02 (tolerance: < 1%)

**Precision2**: 100th percentile diff = 2.63e-07 (tolerance: < 1.00e-01)

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
- Test 1 - Superset check: ✅ PASSED
- Test 2 - NumRows check: ✅ PASSED (Python has +0.42% rows vs Stata)
- Test 3 - Precision1 check: ✅ PASSED
- Test 4 - Precision2 check: ✅ PASSED
- Test 5 - T-stat check: NA (Skipped for faster execution)

**Observations**:
- Stata:  3,047,458
- Python: 3,060,165
- Common: 3,047,458

**Precision1**: 0.000% obs with std_diff >= 1.00e-02 (tolerance: < 1%)

**Precision2**: 100th percentile diff = 4.02e-08 (tolerance: < 1.00e-01)

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
- Test 1 - Superset check: ✅ PASSED
- Test 2 - NumRows check: ✅ PASSED (Python has +0.07% rows vs Stata)
- Test 3 - Precision1 check: ✅ PASSED
- Test 4 - Precision2 check: ✅ PASSED
- Test 5 - T-stat check: NA (Skipped for faster execution)

**Observations**:
- Stata:  628,022
- Python: 628,490
- Common: 626,889

**Precision1**: 0.030% obs with std_diff >= 1.00e-02 (tolerance: < 1%)

**Precision2**: 100th percentile diff = 0.00e+00 (tolerance: < 1.00e-01)

**Summary Statistics** (Common Observations):

| Statistic  |          Stata |         Python |     Difference | Std Difference |
|------------|----------------|----------------|----------------|----------------|
| count      |    626889.0000 |    626889.0000 |    626889.0000 |    626889.0000 |
| mean       |         0.4775 |         0.4775 |       2.55e-05 |       5.11e-05 |
| std        |         0.4995 |         0.4995 |         0.0174 |         0.0349 |
| min        |         0.0000 |         0.0000 |        -1.0000 |        -2.0020 |
| 25%        |         0.0000 |         0.0000 |         0.0000 |         0.0000 |
| 50%        |         0.0000 |         0.0000 |         0.0000 |         0.0000 |
| 75%        |         1.0000 |         1.0000 |         0.0000 |         0.0000 |
| max        |         1.0000 |         1.0000 |         1.0000 |         2.0020 |

**Regression Analysis** (Python ~ Stata):

- **Model**: python = 0.0003 + 0.9994 * stata
- **R-squared**: 0.9988
- **N observations**: 626,889

| Coefficient |     Estimate |    Std Error | t-statistic |   p-value |
|-------------|--------------|--------------|-------------|----------|
| Intercept   |     3.14e-04 |     3.04e-05 |     10.3393 |     0.000 |
| Slope       |       0.9994 |     4.40e-05 |  22706.3239 |     0.000 |

**Feedback**:
- Num observations with std_diff >= TOL_DIFF_1: 190/626889 (0.030%)
- Stata standard deviation: 4.99e-01

---

### ChInv

**Status**: ✅ PASSED

**Test Results**:
- Test 1 - Superset check: ✅ PASSED
- Test 2 - NumRows check: ✅ PASSED (Python has +0.51% rows vs Stata)
- Test 3 - Precision1 check: ✅ PASSED
- Test 4 - Precision2 check: ✅ PASSED
- Test 5 - T-stat check: NA (Skipped for faster execution)

**Observations**:
- Stata:  3,295,155
- Python: 3,311,811
- Common: 3,295,155

**Precision1**: 0.002% obs with std_diff >= 1.00e-02 (tolerance: < 1%)

**Precision2**: 100th percentile diff = 2.69e-07 (tolerance: < 1.00e-01)

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
- Test 1 - Superset check: ✅ PASSED
- Test 2 - NumRows check: ✅ PASSED (Python has +0.00% rows vs Stata)
- Test 3 - Precision1 check: ✅ PASSED
- Test 4 - Precision2 check: ✅ PASSED
- Test 5 - T-stat check: NA (Skipped for faster execution)

**Observations**:
- Stata:  2,678,515
- Python: 2,678,515
- Common: 2,678,515

**Precision1**: 0.000% obs with std_diff >= 1.00e-02 (tolerance: < 1%)

**Precision2**: 100th percentile diff = 2.33e-08 (tolerance: < 1.00e-01)

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
- Test 1 - Superset check: ✅ PASSED
- Test 2 - NumRows check: ✅ PASSED (Python has -0.03% rows vs Stata)
- Test 3 - Precision1 check: ✅ PASSED
- Test 4 - Precision2 check: ✅ PASSED
- Test 5 - T-stat check: NA (Skipped for faster execution)

**Observations**:
- Stata:  210,988
- Python: 210,931
- Common: 210,756

**Precision1**: 0.007% obs with std_diff >= 1.00e-02 (tolerance: < 1%)

**Precision2**: 100th percentile diff = 0.00e+00 (tolerance: < 1.00e-01)

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
- Test 1 - Superset check: ✅ PASSED
- Test 2 - NumRows check: ✅ PASSED (Python has +0.50% rows vs Stata)
- Test 3 - Precision1 check: ✅ PASSED
- Test 4 - Precision2 check: ✅ PASSED
- Test 5 - T-stat check: NA (Skipped for faster execution)

**Observations**:
- Stata:  3,246,170
- Python: 3,262,498
- Common: 3,246,170

**Precision1**: 0.007% obs with std_diff >= 1.00e-02 (tolerance: < 1%)

**Precision2**: 100th percentile diff = 1.69e-07 (tolerance: < 1.00e-01)

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
- Test 1 - Superset check: ✅ PASSED
- Test 2 - NumRows check: ✅ PASSED (Python has +0.50% rows vs Stata)
- Test 3 - Precision1 check: ✅ PASSED
- Test 4 - Precision2 check: ✅ PASSED
- Test 5 - T-stat check: NA (Skipped for faster execution)

**Observations**:
- Stata:  3,259,599
- Python: 3,275,986
- Common: 3,259,599

**Precision1**: 0.004% obs with std_diff >= 1.00e-02 (tolerance: < 1%)

**Precision2**: 100th percentile diff = 1.44e-07 (tolerance: < 1.00e-01)

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
- Test 1 - Superset check: ✅ PASSED
- Test 2 - NumRows check: ✅ PASSED (Python has +0.02% rows vs Stata)
- Test 3 - Precision1 check: ✅ PASSED
- Test 4 - Precision2 check: ✅ PASSED
- Test 5 - T-stat check: NA (Skipped for faster execution)

**Observations**:
- Stata:  2,827,726
- Python: 2,828,377
- Common: 2,827,667

**Precision1**: 0.001% obs with std_diff >= 1.00e-02 (tolerance: < 1%)

**Precision2**: 100th percentile diff = 2.43e-09 (tolerance: < 1.00e-01)

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
- Test 1 - Superset check: ✅ PASSED
- Test 2 - NumRows check: ✅ PASSED (Python has +0.05% rows vs Stata)
- Test 3 - Precision1 check: ✅ PASSED
- Test 4 - Precision2 check: ✅ PASSED
- Test 5 - T-stat check: NA (Skipped for faster execution)

**Observations**:
- Stata:  450,217
- Python: 450,458
- Common: 449,187

**Precision1**: 0.048% obs with std_diff >= 1.00e-02 (tolerance: < 1%)

**Precision2**: 100th percentile diff = 2.49e-07 (tolerance: < 1.00e-01)

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
- Test 1 - Superset check: ❌ FAILED (Python missing 645360 Stata observations)
- Test 2 - NumRows check: ✅ PASSED (Python has -100.00% rows vs Stata)
- Test 3 - Precision1 check: ❌ FAILED
- Test 4 - Precision2 check: ❌ FAILED
- Test 5 - T-stat check: NA (Skipped for faster execution)

**Observations**:
- Stata:  645,360
- Python: 0
- Common: 0

---

### CompEquIss

**Status**: ❌ FAILED

**Test Results**:
- Test 1 - Superset check: ✅ PASSED
- Test 2 - NumRows check: ❌ FAILED (Python has +18.85% rows vs Stata)
- Test 3 - Precision1 check: ✅ PASSED
- Test 4 - Precision2 check: ✅ PASSED
- Test 5 - T-stat check: NA (Skipped for faster execution)

**Observations**:
- Stata:  2,172,395
- Python: 2,581,962
- Common: 2,156,555

**Precision1**: 0.000% obs with std_diff >= 1.00e-02 (tolerance: < 1%)

**Precision2**: 100th percentile diff = 2.06e-06 (tolerance: < 1.00e-01)

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
- Test 1 - Superset check: ✅ PASSED
- Test 2 - NumRows check: ✅ PASSED (Python has +0.85% rows vs Stata)
- Test 3 - Precision1 check: ✅ PASSED
- Test 4 - Precision2 check: ✅ PASSED
- Test 5 - T-stat check: NA (Skipped for faster execution)

**Observations**:
- Stata:  1,898,755
- Python: 1,914,946
- Common: 1,898,755

**Precision1**: 0.006% obs with std_diff >= 1.00e-02 (tolerance: < 1%)

**Precision2**: 100th percentile diff = 2.00e-07 (tolerance: < 1.00e-01)

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
- Test 1 - Superset check: ✅ PASSED
- Test 2 - NumRows check: ✅ PASSED (Python has +0.02% rows vs Stata)
- Test 3 - Precision1 check: ✅ PASSED
- Test 4 - Precision2 check: ✅ PASSED
- Test 5 - T-stat check: NA (Skipped for faster execution)

**Observations**:
- Stata:  134,102
- Python: 134,129
- Common: 133,755

**Precision1**: 0.002% obs with std_diff >= 1.00e-02 (tolerance: < 1%)

**Precision2**: 100th percentile diff = 0.00e+00 (tolerance: < 1.00e-01)

**Summary Statistics** (Common Observations):

| Statistic  |          Stata |         Python |     Difference | Std Difference |
|------------|----------------|----------------|----------------|----------------|
| count      |    133755.0000 |    133755.0000 |    133755.0000 |    133755.0000 |
| mean       |         0.2638 |         0.2638 |      -7.48e-06 |      -1.70e-05 |
| std        |         0.4407 |         0.4407 |         0.0047 |         0.0107 |
| min        |         0.0000 |         0.0000 |        -1.0000 |        -2.2692 |
| 25%        |         0.0000 |         0.0000 |         0.0000 |         0.0000 |
| 50%        |         0.0000 |         0.0000 |         0.0000 |         0.0000 |
| 75%        |         1.0000 |         1.0000 |         0.0000 |         0.0000 |
| max        |         1.0000 |         1.0000 |         1.0000 |         2.2692 |

**Regression Analysis** (Python ~ Stata):

- **Model**: python = 0.0000 + 0.9999 * stata
- **R-squared**: 0.9999
- **N observations**: 133,755

| Coefficient |     Estimate |    Std Error | t-statistic |   p-value |
|-------------|--------------|--------------|-------------|----------|
| Intercept   |     1.02e-05 |     1.51e-05 |      0.6729 |     0.501 |
| Slope       |       0.9999 |     2.94e-05 |  34028.5403 |     0.000 |

**Feedback**:
- Num observations with std_diff >= TOL_DIFF_1: 3/133755 (0.002%)
- Stata standard deviation: 4.41e-01

---

### ConvDebt

**Status**: ✅ PASSED

**Test Results**:
- Test 1 - Superset check: ✅ PASSED
- Test 2 - NumRows check: ✅ PASSED (Python has +0.03% rows vs Stata)
- Test 3 - Precision1 check: ✅ PASSED
- Test 4 - Precision2 check: ✅ PASSED
- Test 5 - T-stat check: NA (Skipped for faster execution)

**Observations**:
- Stata:  3,624,363
- Python: 3,625,491
- Common: 3,624,363

**Precision1**: 0.001% obs with std_diff >= 1.00e-02 (tolerance: < 1%)

**Precision2**: 100th percentile diff = 0.00e+00 (tolerance: < 1.00e-01)

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
- Test 1 - Superset check: ✅ PASSED
- Test 2 - NumRows check: ✅ PASSED (Python has +0.00% rows vs Stata)
- Test 3 - Precision1 check: ✅ PASSED
- Test 4 - Precision2 check: ✅ PASSED
- Test 5 - T-stat check: NA (Skipped for faster execution)

**Observations**:
- Stata:  4,179,145
- Python: 4,179,145
- Common: 4,179,145

**Precision1**: 0.000% obs with std_diff >= 1.00e-02 (tolerance: < 1%)

**Precision2**: 100th percentile diff = 3.17e-03 (tolerance: < 1.00e-01)

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
- Test 1 - Superset check: ✅ PASSED
- Test 2 - NumRows check: ✅ PASSED (Python has +0.00% rows vs Stata)
- Test 3 - Precision1 check: ✅ PASSED
- Test 4 - Precision2 check: ✅ PASSED
- Test 5 - T-stat check: NA (Skipped for faster execution)

**Observations**:
- Stata:  4,609,158
- Python: 4,609,158
- Common: 4,609,158

**Precision1**: 0.000% obs with std_diff >= 1.00e-02 (tolerance: < 1%)

**Precision2**: 100th percentile diff = 2.69e-03 (tolerance: < 1.00e-01)

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

**Status**: ✅ PASSED (with override)

**Override Applied**:
- Reviewed on: 2025-08-20
- Reviewed by: ac
- Details: The sample deviations are all downgrades found in Python but not in Stata. I manually checked a few and found these all have CIQ downgrades. This is likely an improvement due to patching the CIQ deduplication bugs in the Stata DataDownloads code.

**Test Results**:
- Test 1 - Superset check: ✅ PASSED
- Test 2 - NumRows check: ❌ FAILED (Python has +18.83% rows vs Stata)
- Test 3 - Precision1 check: ✅ PASSED
- Test 4 - Precision2 check: ❌ FAILED
- Test 5 - T-stat check: NA (Skipped for faster execution)

**Observations**:
- Stata:  2,559,713
- Python: 3,041,661
- Common: 2,559,713

**Precision1**: 0.342% obs with std_diff >= 1.00e-02 (tolerance: < 1%)

**Precision2**: 100th percentile diff = 6.63e+00 (tolerance: < 1.00e-01)

**Summary Statistics** (Common Observations):

| Statistic  |          Stata |         Python |     Difference | Std Difference |
|------------|----------------|----------------|----------------|----------------|
| count      |       2.56e+06 |       2.56e+06 |       2.56e+06 |       2.56e+06 |
| mean       |         0.0233 |         0.0266 |         0.0033 |         0.0221 |
| std        |         0.1508 |         0.1610 |         0.0584 |         0.3873 |
| min        |         0.0000 |         0.0000 |        -1.0000 |        -6.6310 |
| 25%        |         0.0000 |         0.0000 |         0.0000 |         0.0000 |
| 50%        |         0.0000 |         0.0000 |         0.0000 |         0.0000 |
| 75%        |         0.0000 |         0.0000 |         0.0000 |         0.0000 |
| max        |         1.0000 |         1.0000 |         1.0000 |         6.6310 |

**Regression Analysis** (Python ~ Stata):

- **Model**: python = 0.0035 + 0.9945 * stata
- **R-squared**: 0.8683
- **N observations**: 2,559,713

| Coefficient |     Estimate |    Std Error | t-statistic |   p-value |
|-------------|--------------|--------------|-------------|----------|
| Intercept   |       0.0035 |     3.69e-05 |     93.5730 |     0.000 |
| Slope       |       0.9945 |     2.42e-04 |   4108.6788 |     0.000 |

**Feedback**:
- Num observations with std_diff >= TOL_DIFF_1: 8761/2559713 (0.342%)
- Stata standard deviation: 1.51e-01

**Most Recent Bad Observations**:
```
   permno  yyyymm  python  stata  diff
0   17956  202412     1.0      0   1.0
1   18144  202412     1.0      0   1.0
2   22174  202412     1.0      0   1.0
3   38703  202412     1.0      0   1.0
4   47896  202412     1.0      0   1.0
5   58318  202412     1.0      0   1.0
6   66157  202412     1.0      0   1.0
7   70519  202412     1.0      0   1.0
8   88284  202412     1.0      0   1.0
9   89199  202412     1.0      0   1.0
```

**Largest Differences**:
```
   permno  yyyymm  python  stata  diff
0   10026  198911     1.0      0   1.0
1   10026  198912     1.0      0   1.0
2   10026  199001     1.0      0   1.0
3   10026  199002     1.0      0   1.0
4   10026  199003     1.0      0   1.0
5   10026  199004     1.0      0   1.0
6   10047  199311     1.0      0   1.0
7   10047  199312     1.0      0   1.0
8   10047  199401     1.0      0   1.0
9   10047  199402     1.0      0   1.0
```

**Largest Differences Before 1950**:
```
No data before 1950
```

---

### CustomerMomentum

**Status**: ✅ PASSED

**Test Results**:
- Test 1 - Superset check: ✅ PASSED
- Test 2 - NumRows check: ✅ PASSED (Python has -0.03% rows vs Stata)
- Test 3 - Precision1 check: ✅ PASSED
- Test 4 - Precision2 check: ✅ PASSED
- Test 5 - T-stat check: NA (Skipped for faster execution)

**Observations**:
- Stata:  356,600
- Python: 356,510
- Common: 356,462

**Precision1**: 0.006% obs with std_diff >= 1.00e-02 (tolerance: < 1%)

**Precision2**: 100th percentile diff = 1.79e-07 (tolerance: < 1.00e-01)

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
- Test 1 - Superset check: ✅ PASSED
- Test 2 - NumRows check: ✅ PASSED (Python has +0.00% rows vs Stata)
- Test 3 - Precision1 check: ✅ PASSED
- Test 4 - Precision2 check: ✅ PASSED
- Test 5 - T-stat check: NA (Skipped for faster execution)

**Observations**:
- Stata:  2,725,997
- Python: 2,726,038
- Common: 2,725,997

**Precision1**: 0.000% obs with std_diff >= 1.00e-02 (tolerance: < 1%)

**Precision2**: 100th percentile diff = 0.00e+00 (tolerance: < 1.00e-01)

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
- Test 1 - Superset check: ✅ PASSED
- Test 2 - NumRows check: ✅ PASSED (Python has +4.02% rows vs Stata)
- Test 3 - Precision1 check: ✅ PASSED
- Test 4 - Precision2 check: ✅ PASSED
- Test 5 - T-stat check: NA (Skipped for faster execution)

**Observations**:
- Stata:  1,062,671
- Python: 1,105,341
- Common: 1,058,068

**Precision1**: 0.000% obs with std_diff >= 1.00e-02 (tolerance: < 1%)

**Precision2**: 100th percentile diff = 2.25e-07 (tolerance: < 1.00e-01)

**Summary Statistics** (Common Observations):

| Statistic  |          Stata |         Python |     Difference | Std Difference |
|------------|----------------|----------------|----------------|----------------|
| count      |       1.06e+06 |       1.06e+06 |       1.06e+06 |       1.06e+06 |
| mean       |         0.1320 |         0.1320 |      -1.47e-10 |      -1.65e-10 |
| std        |         0.8906 |         0.8906 |       2.45e-08 |       2.76e-08 |
| min        |       -47.2500 |       -47.2500 |      -2.00e-06 |      -2.25e-06 |
| 25%        |        -0.1820 |        -0.1820 |      -1.00e-09 |      -1.12e-09 |
| 50%        |         0.0810 |         0.0810 |         0.0000 |         0.0000 |
| 75%        |         0.4010 |         0.4010 |         0.0000 |         0.0000 |
| max        |        48.0560 |        48.0560 |       1.00e-06 |       1.12e-06 |

**Regression Analysis** (Python ~ Stata):

- **Model**: python = 0.0000 + 1.0000 * stata
- **R-squared**: 1.0000
- **N observations**: 1,058,068

| Coefficient |     Estimate |    Std Error | t-statistic |   p-value |
|-------------|--------------|--------------|-------------|----------|
| Intercept   |     1.90e-11 |     2.41e-11 |      0.7867 |     0.431 |
| Slope       |       1.0000 |     2.68e-11 |    3.74e+10 |     0.000 |

**Feedback**:
- Num observations with std_diff >= TOL_DIFF_1: 0/1058068 (0.000%)
- Stata standard deviation: 8.91e-01

---

### DelCOA

**Status**: ✅ PASSED

**Test Results**:
- Test 1 - Superset check: ✅ PASSED
- Test 2 - NumRows check: ✅ PASSED (Python has +0.51% rows vs Stata)
- Test 3 - Precision1 check: ✅ PASSED
- Test 4 - Precision2 check: ✅ PASSED
- Test 5 - T-stat check: NA (Skipped for faster execution)

**Observations**:
- Stata:  3,295,155
- Python: 3,311,811
- Common: 3,295,155

**Precision1**: 0.002% obs with std_diff >= 1.00e-02 (tolerance: < 1%)

**Precision2**: 100th percentile diff = 4.46e-07 (tolerance: < 1.00e-01)

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
- Test 1 - Superset check: ✅ PASSED
- Test 2 - NumRows check: ✅ PASSED (Python has +0.50% rows vs Stata)
- Test 3 - Precision1 check: ✅ PASSED
- Test 4 - Precision2 check: ✅ PASSED
- Test 5 - T-stat check: NA (Skipped for faster execution)

**Observations**:
- Stata:  3,259,701
- Python: 3,276,154
- Common: 3,259,701

**Precision1**: 0.006% obs with std_diff >= 1.00e-02 (tolerance: < 1%)

**Precision2**: 100th percentile diff = 4.27e-07 (tolerance: < 1.00e-01)

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
- Test 1 - Superset check: ✅ PASSED
- Test 2 - NumRows check: ✅ PASSED (Python has +0.49% rows vs Stata)
- Test 3 - Precision1 check: ✅ PASSED
- Test 4 - Precision2 check: ✅ PASSED
- Test 5 - T-stat check: NA (Skipped for faster execution)

**Observations**:
- Stata:  460,159
- Python: 462,430
- Common: 460,159

**Precision1**: 0.010% obs with std_diff >= 1.00e-02 (tolerance: < 1%)

**Precision2**: 100th percentile diff = 3.19e-07 (tolerance: < 1.00e-01)

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
- Test 1 - Superset check: ✅ PASSED
- Test 2 - NumRows check: ✅ PASSED (Python has +0.03% rows vs Stata)
- Test 3 - Precision1 check: ✅ PASSED
- Test 4 - Precision2 check: ✅ PASSED
- Test 5 - T-stat check: NA (Skipped for faster execution)

**Observations**:
- Stata:  3,194,475
- Python: 3,195,456
- Common: 3,194,475

**Precision1**: 0.001% obs with std_diff >= 1.00e-02 (tolerance: < 1%)

**Precision2**: 100th percentile diff = 2.06e-07 (tolerance: < 1.00e-01)

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
- Test 1 - Superset check: ✅ PASSED
- Test 2 - NumRows check: ✅ PASSED (Python has +0.03% rows vs Stata)
- Test 3 - Precision1 check: ✅ PASSED
- Test 4 - Precision2 check: ✅ PASSED
- Test 5 - T-stat check: NA (Skipped for faster execution)

**Observations**:
- Stata:  3,250,876
- Python: 3,251,905
- Common: 3,250,876

**Precision1**: 0.006% obs with std_diff >= 1.00e-02 (tolerance: < 1%)

**Precision2**: 100th percentile diff = 4.69e-07 (tolerance: < 1.00e-01)

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
- Test 1 - Superset check: ✅ PASSED
- Test 2 - NumRows check: ✅ PASSED (Python has +0.03% rows vs Stata)
- Test 3 - Precision1 check: ✅ PASSED
- Test 4 - Precision2 check: ✅ PASSED
- Test 5 - T-stat check: NA (Skipped for faster execution)

**Observations**:
- Stata:  3,295,155
- Python: 3,296,136
- Common: 3,295,155

**Precision1**: 0.005% obs with std_diff >= 1.00e-02 (tolerance: < 1%)

**Precision2**: 100th percentile diff = 5.93e-07 (tolerance: < 1.00e-01)

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
- Test 1 - Superset check: ✅ PASSED
- Test 2 - NumRows check: ✅ PASSED (Python has +0.03% rows vs Stata)
- Test 3 - Precision1 check: ✅ PASSED
- Test 4 - Precision2 check: ✅ PASSED
- Test 5 - T-stat check: NA (Skipped for faster execution)

**Observations**:
- Stata:  3,250,876
- Python: 3,251,905
- Common: 3,250,876

**Precision1**: 0.009% obs with std_diff >= 1.00e-02 (tolerance: < 1%)

**Precision2**: 100th percentile diff = 5.82e-07 (tolerance: < 1.00e-01)

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

**Status**: ❌ FAILED

**Test Results**:
- Test 1 - Superset check: ✅ PASSED
- Test 2 - NumRows check: ✅ PASSED (Python has +0.00% rows vs Stata)
- Test 3 - Precision1 check: ❌ FAILED
- Test 4 - Precision2 check: ❌ FAILED
- Test 5 - T-stat check: NA (Skipped for faster execution)

**Observations**:
- Stata:  4,047,630
- Python: 4,047,630
- Common: 4,047,630

**Precision1**: 1.103% obs with std_diff >= 1.00e-02 (tolerance: < 1%)

**Precision2**: 100th percentile diff = 7.30e+00 (tolerance: < 1.00e-01)

**Summary Statistics** (Common Observations):

| Statistic  |          Stata |         Python |     Difference | Std Difference |
|------------|----------------|----------------|----------------|----------------|
| count      |       4.05e+06 |       4.05e+06 |       4.05e+06 |       4.05e+06 |
| mean       |         0.0191 |         0.0081 |        -0.0110 |        -0.0805 |
| std        |         0.1369 |         0.0895 |         0.1044 |         0.7628 |
| min        |         0.0000 |         0.0000 |        -1.0000 |        -7.3042 |
| 25%        |         0.0000 |         0.0000 |         0.0000 |         0.0000 |
| 50%        |         0.0000 |         0.0000 |         0.0000 |         0.0000 |
| 75%        |         0.0000 |         0.0000 |         0.0000 |         0.0000 |
| max        |         1.0000 |         1.0000 |         1.0000 |         7.3042 |

**Regression Analysis** (Python ~ Stata):

- **Model**: python = 0.0000 + 0.4230 * stata
- **R-squared**: 0.4181
- **N observations**: 4,047,630

| Coefficient |     Estimate |    Std Error | t-statistic |   p-value |
|-------------|--------------|--------------|-------------|----------|
| Intercept   |     2.27e-06 |     3.43e-05 |      0.0661 |     0.947 |
| Slope       |       0.4230 |     2.48e-04 |   1705.5067 |     0.000 |

**Feedback**:
- Num observations with std_diff >= TOL_DIFF_1: 44640/4047630 (1.103%)
- Stata standard deviation: 1.37e-01

**Most Recent Bad Observations**:
```
   permno  yyyymm  python  stata  diff
0   23877  202412       0      1    -1
1   24878  202412       0      1    -1
2   25027  202412       0      1    -1
3   25146  202412       0      1    -1
4   25181  202412       0      1    -1
5   25244  202412       0      1    -1
6   25245  202412       0      1    -1
7   25341  202412       0      1    -1
8   25700  202412       0      1    -1
9   23877  202411       0      1    -1
```

**Largest Differences**:
```
   permno  yyyymm  python  stata  diff
0   10001  198603       0      1    -1
1   10001  198604       0      1    -1
2   10001  198605       0      1    -1
3   10001  198606       0      1    -1
4   10001  198607       0      1    -1
5   10001  198608       0      1    -1
6   10003  198708       0      1    -1
7   10003  198709       0      1    -1
8   10003  198710       0      1    -1
9   10003  198711       0      1    -1
```

**Largest Differences Before 1950**:
```
   permno  yyyymm  python  stata  diff
0   10006  192603       0      1    -1
1   10006  192604       0      1    -1
2   10006  192605       0      1    -1
3   10006  192606       0      1    -1
4   10006  192607       0      1    -1
5   10006  192608       0      1    -1
6   10022  192603       0      1    -1
7   10022  192604       0      1    -1
8   10022  192605       0      1    -1
9   10022  192606       0      1    -1
```

---

### DivOmit

**Status**: ✅ PASSED

**Test Results**:
- Test 1 - Superset check: ✅ PASSED
- Test 2 - NumRows check: ✅ PASSED (Python has +0.00% rows vs Stata)
- Test 3 - Precision1 check: ✅ PASSED
- Test 4 - Precision2 check: ✅ PASSED
- Test 5 - T-stat check: NA (Skipped for faster execution)

**Observations**:
- Stata:  4,047,630
- Python: 4,047,630
- Common: 4,047,630

**Precision1**: 0.018% obs with std_diff >= 1.00e-02 (tolerance: < 1%)

**Precision2**: 100th percentile diff = 0.00e+00 (tolerance: < 1.00e-01)

**Summary Statistics** (Common Observations):

| Statistic  |          Stata |         Python |     Difference | Std Difference |
|------------|----------------|----------------|----------------|----------------|
| count      |       4.05e+06 |       4.05e+06 |       4.05e+06 |       4.05e+06 |
| mean       |         0.0039 |         0.0037 |      -1.72e-04 |        -0.0028 |
| std        |         0.0622 |         0.0608 |         0.0132 |         0.2128 |
| min        |         0.0000 |         0.0000 |        -1.0000 |       -16.0714 |
| 25%        |         0.0000 |         0.0000 |         0.0000 |         0.0000 |
| 50%        |         0.0000 |         0.0000 |         0.0000 |         0.0000 |
| 75%        |         0.0000 |         0.0000 |         0.0000 |         0.0000 |
| max        |         1.0000 |         1.0000 |         1.0000 |        16.0714 |

**Regression Analysis** (Python ~ Stata):

- **Model**: python = 0.0000 + 0.9553 * stata
- **R-squared**: 0.9547
- **N observations**: 4,047,630

| Coefficient |     Estimate |    Std Error | t-statistic |   p-value |
|-------------|--------------|--------------|-------------|----------|
| Intercept   |     1.74e-06 |     6.45e-06 |      0.2692 |     0.788 |
| Slope       |       0.9553 |     1.03e-04 |   9236.1212 |     0.000 |

**Feedback**:
- Num observations with std_diff >= TOL_DIFF_1: 710/4047630 (0.018%)
- Stata standard deviation: 6.22e-02

---

### DivSeason

**Status**: ❌ FAILED

**Test Results**:
- Test 1 - Superset check: ✅ PASSED
- Test 2 - NumRows check: ✅ PASSED (Python has -0.80% rows vs Stata)
- Test 3 - Precision1 check: ✅ PASSED
- Test 4 - Precision2 check: ❌ FAILED
- Test 5 - T-stat check: NA (Skipped for faster execution)

**Observations**:
- Stata:  1,775,339
- Python: 1,761,068
- Common: 1,760,764

**Precision1**: 0.202% obs with std_diff >= 1.00e-02 (tolerance: < 1%)

**Precision2**: 100th percentile diff = 2.01e+00 (tolerance: < 1.00e-01)

**Summary Statistics** (Common Observations):

| Statistic  |          Stata |         Python |     Difference | Std Difference |
|------------|----------------|----------------|----------------|----------------|
| count      |       1.76e+06 |       1.76e+06 |       1.76e+06 |       1.76e+06 |
| mean       |         0.4413 |         0.4428 |         0.0015 |         0.0031 |
| std        |         0.4965 |         0.4967 |         0.0449 |         0.0904 |
| min        |         0.0000 |         0.0000 |        -1.0000 |        -2.0139 |
| 25%        |         0.0000 |         0.0000 |         0.0000 |         0.0000 |
| 50%        |         0.0000 |         0.0000 |         0.0000 |         0.0000 |
| 75%        |         1.0000 |         1.0000 |         0.0000 |         0.0000 |
| max        |         1.0000 |         1.0000 |         1.0000 |         2.0139 |

**Regression Analysis** (Python ~ Stata):

- **Model**: python = 0.0032 + 0.9963 * stata
- **R-squared**: 0.9919
- **N observations**: 1,760,764

| Coefficient |     Estimate |    Std Error | t-statistic |   p-value |
|-------------|--------------|--------------|-------------|----------|
| Intercept   |       0.0032 |     4.52e-05 |     70.4805 |     0.000 |
| Slope       |       0.9963 |     6.80e-05 |  14642.2418 |     0.000 |

**Feedback**:
- Num observations with std_diff >= TOL_DIFF_1: 3549/1760764 (0.202%)
- Stata standard deviation: 4.97e-01

**Most Recent Bad Observations**:
```
   permno  yyyymm  python  stata  diff
0   13303  202412       1      0     1
1   15802  202412       1      0     1
2   16019  202412       1      0     1
3   16560  202412       1      0     1
4   32791  202412       0      1    -1
5   85903  202412       1      0     1
6   90983  202412       1      0     1
7   32791  202411       0      1    -1
8   78981  202411       1      0     1
9   82171  202411       1      0     1
```

**Largest Differences**:
```
   permno  yyyymm  python  stata  diff
0   10057  196407       1      0     1
1   10057  196410       1      0     1
2   10172  198810       0      1    -1
3   10241  192901       1      0     1
4   10241  192904       1      0     1
5   10241  192907       1      0     1
6   10241  192910       1      0     1
7   10241  193701       1      0     1
8   10241  193704       1      0     1
9   10241  193707       1      0     1
```

**Largest Differences Before 1950**:
```
   permno  yyyymm  python  stata  diff
0   10241  192901       1      0     1
1   10241  192904       1      0     1
2   10241  192907       1      0     1
3   10241  192910       1      0     1
4   10241  193701       1      0     1
5   10241  193704       1      0     1
6   10241  193707       1      0     1
7   10241  193710       1      0     1
8   10540  192701       1      0     1
9   10698  194612       1      0     1
```

---

### DivYieldST

**Status**: ✅ PASSED

**Test Results**:
- Test 1 - Superset check: ✅ PASSED
- Test 2 - NumRows check: ✅ PASSED (Python has +0.61% rows vs Stata)
- Test 3 - Precision1 check: ✅ PASSED
- Test 4 - Precision2 check: ✅ PASSED
- Test 5 - T-stat check: NA (Skipped for faster execution)

**Observations**:
- Stata:  1,591,700
- Python: 1,601,392
- Common: 1,591,697

**Precision1**: 0.069% obs with std_diff >= 1.00e-02 (tolerance: < 1%)

**Precision2**: 100th percentile diff = 0.00e+00 (tolerance: < 1.00e-01)

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
- Test 1 - Superset check: ✅ PASSED
- Test 2 - NumRows check: ✅ PASSED (Python has +0.00% rows vs Stata)
- Test 3 - Precision1 check: ✅ PASSED
- Test 4 - Precision2 check: ✅ PASSED
- Test 5 - T-stat check: NA (Skipped for faster execution)

**Observations**:
- Stata:  4,640,493
- Python: 4,640,493
- Common: 4,640,493

**Precision1**: 0.000% obs with std_diff >= 1.00e-02 (tolerance: < 1%)

**Precision2**: 100th percentile diff = 1.54e-07 (tolerance: < 1.00e-01)

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

**Status**: ✅ PASSED

**Test Results**:
- Test 1 - Superset check: ✅ PASSED
- Test 2 - NumRows check: ✅ PASSED (Python has +0.05% rows vs Stata)
- Test 3 - Precision1 check: ✅ PASSED
- Test 4 - Precision2 check: ✅ PASSED
- Test 5 - T-stat check: NA (Skipped for faster execution)

**Observations**:
- Stata:  463,983
- Python: 464,223
- Common: 462,936

**Precision1**: 0.025% obs with std_diff >= 1.00e-02 (tolerance: < 1%)

**Precision2**: 100th percentile diff = 0.00e+00 (tolerance: < 1.00e-01)

**Summary Statistics** (Common Observations):

| Statistic  |          Stata |         Python |     Difference | Std Difference |
|------------|----------------|----------------|----------------|----------------|
| count      |    462936.0000 |    462936.0000 |    462936.0000 |    462936.0000 |
| mean       |         0.3701 |         0.3701 |      -2.16e-06 |      -4.47e-06 |
| std        |         0.4828 |         0.4828 |         0.0158 |         0.0326 |
| min        |         0.0000 |         0.0000 |        -1.0000 |        -2.0711 |
| 25%        |         0.0000 |         0.0000 |         0.0000 |         0.0000 |
| 50%        |         0.0000 |         0.0000 |         0.0000 |         0.0000 |
| 75%        |         1.0000 |         1.0000 |         0.0000 |         0.0000 |
| max        |         1.0000 |         1.0000 |         1.0000 |         2.0711 |

**Regression Analysis** (Python ~ Stata):

- **Model**: python = 0.0002 + 0.9995 * stata
- **R-squared**: 0.9989
- **N observations**: 462,936

| Coefficient |     Estimate |    Std Error | t-statistic |   p-value |
|-------------|--------------|--------------|-------------|----------|
| Intercept   |     1.95e-04 |     2.92e-05 |      6.6982 |     0.000 |
| Slope       |       0.9995 |     4.80e-05 |  20835.2921 |     0.000 |

**Feedback**:
- Num observations with std_diff >= TOL_DIFF_1: 115/462936 (0.025%)
- Stata standard deviation: 4.83e-01

---

### EBM

**Status**: ✅ PASSED

**Test Results**:
- Test 1 - Superset check: ✅ PASSED
- Test 2 - NumRows check: ✅ PASSED (Python has +0.00% rows vs Stata)
- Test 3 - Precision1 check: ✅ PASSED
- Test 4 - Precision2 check: ✅ PASSED
- Test 5 - T-stat check: NA (Skipped for faster execution)

**Observations**:
- Stata:  2,924,820
- Python: 2,924,826
- Common: 2,924,820

**Precision1**: 0.001% obs with std_diff >= 1.00e-02 (tolerance: < 1%)

**Precision2**: 100th percentile diff = 2.18e-06 (tolerance: < 1.00e-01)

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
- Test 1 - Superset check: ✅ PASSED
- Test 2 - NumRows check: ✅ PASSED (Python has +0.00% rows vs Stata)
- Test 3 - Precision1 check: ✅ PASSED
- Test 4 - Precision2 check: ✅ PASSED
- Test 5 - T-stat check: NA (Skipped for faster execution)

**Observations**:
- Stata:  2,203,166
- Python: 2,203,166
- Common: 2,203,166

**Precision1**: 0.000% obs with std_diff >= 1.00e-02 (tolerance: < 1%)

**Precision2**: 100th percentile diff = 1.03e-07 (tolerance: < 1.00e-01)

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

**Status**: ❌ FAILED

**Test Results**:
- Test 1 - Superset check: ✅ PASSED
- Test 2 - NumRows check: ✅ PASSED (Python has +0.37% rows vs Stata)
- Test 3 - Precision1 check: ✅ PASSED
- Test 4 - Precision2 check: ❌ FAILED
- Test 5 - T-stat check: NA (Skipped for faster execution)

**Observations**:
- Stata:  2,327,518
- Python: 2,336,093
- Common: 2,323,705

**Precision1**: 0.152% obs with std_diff >= 1.00e-02 (tolerance: < 1%)

**Precision2**: 100th percentile diff = 1.47e+00 (tolerance: < 1.00e-01)

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

**Most Recent Bad Observations**:
```
   permno  yyyymm    python         stata          diff
0   10100  200105  0.068662 -5.363412e+13  5.363412e+13
1   10488  200105  0.068662 -5.363412e+13  5.363412e+13
2   10680  200105  0.068662 -5.363412e+13  5.363412e+13
3   11833  200105  0.068662 -5.363412e+13  5.363412e+13
4   20248  200105  0.068662 -5.363412e+13  5.363412e+13
5   39773  200105  0.068662 -5.363412e+13  5.363412e+13
6   62296  200105  0.068662 -5.363412e+13  5.363412e+13
7   69200  200105  0.068662 -5.363412e+13  5.363412e+13
8   75526  200105  0.068662 -5.363412e+13  5.363412e+13
9   75609  200105  0.068662 -5.363412e+13  5.363412e+13
```

**Largest Differences**:
```
   permno  yyyymm    python         stata          diff
0   10613  197308  0.451178  3.580440e+14 -3.580440e+14
1   11165  197308  0.451178  3.580440e+14 -3.580440e+14
2   12141  197308  0.451178  3.580440e+14 -3.580440e+14
3   14227  197308  0.451178  3.580440e+14 -3.580440e+14
4   14569  197308  0.451178  3.580440e+14 -3.580440e+14
5   14702  197308  0.451178  3.580440e+14 -3.580440e+14
6   15078  197308  0.451178  3.580440e+14 -3.580440e+14
7   15457  197308  0.451178  3.580440e+14 -3.580440e+14
8   16986  197308  0.451178  3.580440e+14 -3.580440e+14
9   17523  197308  0.451178  3.580440e+14 -3.580440e+14
```

**Largest Differences Before 1950**:
```
No data before 1950
```

---

### EarningsConsistency

**Status**: ❌ FAILED

**Test Results**:
- Test 1 - Superset check: ✅ PASSED
- Test 2 - NumRows check: ❌ FAILED (Python has +9.77% rows vs Stata)
- Test 3 - Precision1 check: ✅ PASSED
- Test 4 - Precision2 check: ✅ PASSED
- Test 5 - T-stat check: NA (Skipped for faster execution)

**Observations**:
- Stata:  1,386,008
- Python: 1,521,466
- Common: 1,386,008

**Precision1**: 0.000% obs with std_diff >= 1.00e-02 (tolerance: < 1%)

**Precision2**: 100th percentile diff = 3.25e-07 (tolerance: < 1.00e-01)

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
- Test 1 - Superset check: ✅ PASSED
- Test 2 - NumRows check: ✅ PASSED (Python has -0.00% rows vs Stata)
- Test 3 - Precision1 check: ✅ PASSED
- Test 4 - Precision2 check: ✅ PASSED
- Test 5 - T-stat check: NA (Skipped for faster execution)

**Observations**:
- Stata:  975,097
- Python: 975,050
- Common: 972,933

**Precision1**: 0.079% obs with std_diff >= 1.00e-02 (tolerance: < 1%)

**Precision2**: 100th percentile diff = 8.03e-07 (tolerance: < 1.00e-01)

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
- Test 1 - Superset check: ✅ PASSED
- Test 2 - NumRows check: ✅ PASSED (Python has +0.03% rows vs Stata)
- Test 3 - Precision1 check: ✅ PASSED
- Test 4 - Precision2 check: ✅ PASSED
- Test 5 - T-stat check: NA (Skipped for faster execution)

**Observations**:
- Stata:  1,225,060
- Python: 1,225,413
- Common: 1,222,767

**Precision1**: 0.007% obs with std_diff >= 1.00e-02 (tolerance: < 1%)

**Precision2**: 100th percentile diff = 6.41e-08 (tolerance: < 1.00e-01)

**Summary Statistics** (Common Observations):

| Statistic  |          Stata |         Python |     Difference | Std Difference |
|------------|----------------|----------------|----------------|----------------|
| count      |       1.22e+06 |       1.22e+06 |       1.22e+06 |       1.22e+06 |
| mean       |        -0.0014 |        -0.0015 |      -3.55e-06 |      -1.12e-06 |
| std        |         3.1638 |         3.1638 |         0.0022 |       6.81e-04 |
| min        |      -154.1053 |      -154.1053 |        -0.4182 |        -0.1322 |
| 25%        |        -0.0024 |        -0.0024 |      -4.35e-11 |      -1.38e-11 |
| 50%        |       5.09e-04 |       5.09e-04 |         0.0000 |         0.0000 |
| 75%        |         0.0025 |         0.0025 |       4.51e-11 |       1.43e-11 |
| max        |       915.0000 |       915.0000 |         1.3338 |         0.4216 |

**Regression Analysis** (Python ~ Stata):

- **Model**: python = -0.0000 + 1.0000 * stata
- **R-squared**: 1.0000
- **N observations**: 1,222,767

| Coefficient |     Estimate |    Std Error | t-statistic |   p-value |
|-------------|--------------|--------------|-------------|----------|
| Intercept   |    -3.55e-06 |     1.95e-06 |     -1.8211 |     0.069 |
| Slope       |       1.0000 |     6.16e-07 |    1.62e+06 |     0.000 |

**Feedback**:
- Num observations with std_diff >= TOL_DIFF_1: 82/1222767 (0.007%)
- Stata standard deviation: 3.16e+00

---

### EarningsSurprise

**Status**: ✅ PASSED

**Test Results**:
- Test 1 - Superset check: ✅ PASSED
- Test 2 - NumRows check: ✅ PASSED (Python has -0.02% rows vs Stata)
- Test 3 - Precision1 check: ✅ PASSED
- Test 4 - Precision2 check: ✅ PASSED
- Test 5 - T-stat check: NA (Skipped for faster execution)

**Observations**:
- Stata:  2,324,394
- Python: 2,324,021
- Common: 2,323,954

**Precision1**: 0.031% obs with std_diff >= 1.00e-02 (tolerance: < 1%)

**Precision2**: 100th percentile diff = 3.24e-04 (tolerance: < 1.00e-01)

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
- Test 1 - Superset check: ✅ PASSED
- Test 2 - NumRows check: ✅ PASSED (Python has -0.00% rows vs Stata)
- Test 3 - Precision1 check: ✅ PASSED
- Test 4 - Precision2 check: ✅ PASSED
- Test 5 - T-stat check: NA (Skipped for faster execution)

**Observations**:
- Stata:  2,407,850
- Python: 2,407,843
- Common: 2,407,843

**Precision1**: 0.000% obs with std_diff >= 1.00e-02 (tolerance: < 1%)

**Precision2**: 100th percentile diff = 6.09e-08 (tolerance: < 1.00e-01)

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
- Test 1 - Superset check: ✅ PASSED
- Test 2 - NumRows check: ✅ PASSED (Python has +2.47% rows vs Stata)
- Test 3 - Precision1 check: ✅ PASSED
- Test 4 - Precision2 check: ✅ PASSED
- Test 5 - T-stat check: NA (Skipped for faster execution)

**Observations**:
- Stata:  3,124,663
- Python: 3,201,768
- Common: 3,124,663

**Precision1**: 0.000% obs with std_diff >= 1.00e-02 (tolerance: < 1%)

**Precision2**: 100th percentile diff = 4.91e-14 (tolerance: < 1.00e-01)

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
- Test 1 - Superset check: ✅ PASSED
- Test 2 - NumRows check: ✅ PASSED (Python has +0.00% rows vs Stata)
- Test 3 - Precision1 check: ✅ PASSED
- Test 4 - Precision2 check: ✅ PASSED
- Test 5 - T-stat check: NA (Skipped for faster execution)

**Observations**:
- Stata:  4,047,630
- Python: 4,047,630
- Common: 4,047,630

**Precision1**: 0.047% obs with std_diff >= 1.00e-02 (tolerance: < 1%)

**Precision2**: 100th percentile diff = 0.00e+00 (tolerance: < 1.00e-01)

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
- Test 1 - Superset check: ✅ PASSED
- Test 2 - NumRows check: ✅ PASSED (Python has +2.10% rows vs Stata)
- Test 3 - Precision1 check: ✅ PASSED
- Test 4 - Precision2 check: ✅ PASSED
- Test 5 - T-stat check: NA (Skipped for faster execution)

**Observations**:
- Stata:  1,726,232
- Python: 1,762,541
- Common: 1,724,203

**Precision1**: 0.108% obs with std_diff >= 1.00e-02 (tolerance: < 1%)

**Precision2**: 100th percentile diff = 5.62e-02 (tolerance: < 1.00e-01)

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
- Test 1 - Superset check: ✅ PASSED
- Test 2 - NumRows check: ✅ PASSED (Python has +0.01% rows vs Stata)
- Test 3 - Precision1 check: ✅ PASSED
- Test 4 - Precision2 check: ✅ PASSED
- Test 5 - T-stat check: NA (Skipped for faster execution)

**Observations**:
- Stata:  1,957,995
- Python: 1,958,211
- Common: 1,954,911

**Precision1**: 0.026% obs with std_diff >= 1.00e-02 (tolerance: < 1%)

**Precision2**: 100th percentile diff = 5.03e-07 (tolerance: < 1.00e-01)

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
- Test 1 - Superset check: ✅ PASSED
- Test 2 - NumRows check: ✅ PASSED (Python has +0.00% rows vs Stata)
- Test 3 - Precision1 check: ✅ PASSED
- Test 4 - Precision2 check: ✅ PASSED
- Test 5 - T-stat check: NA (Skipped for faster execution)

**Observations**:
- Stata:  683,893
- Python: 683,893
- Common: 683,893

**Precision1**: 0.000% obs with std_diff >= 1.00e-02 (tolerance: < 1%)

**Precision2**: 100th percentile diff = 7.02e-07 (tolerance: < 1.00e-01)

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
- Test 1 - Superset check: ✅ PASSED
- Test 2 - NumRows check: ✅ PASSED (Python has +0.00% rows vs Stata)
- Test 3 - Precision1 check: ✅ PASSED
- Test 4 - Precision2 check: ✅ PASSED
- Test 5 - T-stat check: NA (Skipped for faster execution)

**Observations**:
- Stata:  4,045,796
- Python: 4,045,796
- Common: 4,045,796

**Precision1**: 0.000% obs with std_diff >= 1.00e-02 (tolerance: < 1%)

**Precision2**: 100th percentile diff = 0.00e+00 (tolerance: < 1.00e-01)

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

**Status**: ❌ FAILED

**Test Results**:
- Test 1 - Superset check: ✅ PASSED
- Test 2 - NumRows check: ❌ FAILED (Python has +5.20% rows vs Stata)
- Test 3 - Precision1 check: ✅ PASSED
- Test 4 - Precision2 check: ✅ PASSED
- Test 5 - T-stat check: NA (Skipped for faster execution)

**Observations**:
- Stata:  550,434
- Python: 579,033
- Common: 550,434

**Precision1**: 0.000% obs with std_diff >= 1.00e-02 (tolerance: < 1%)

**Precision2**: 100th percentile diff = 2.70e-07 (tolerance: < 1.00e-01)

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
- Test 1 - Superset check: ✅ PASSED
- Test 2 - NumRows check: ✅ PASSED (Python has +0.02% rows vs Stata)
- Test 3 - Precision1 check: ✅ PASSED
- Test 4 - Precision2 check: ✅ PASSED
- Test 5 - T-stat check: NA (Skipped for faster execution)

**Observations**:
- Stata:  1,616,983
- Python: 1,617,348
- Common: 1,614,371

**Precision1**: 0.070% obs with std_diff >= 1.00e-02 (tolerance: < 1%)

**Precision2**: 100th percentile diff = 7.03e-07 (tolerance: < 1.00e-01)

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
- Test 1 - Superset check: ✅ PASSED
- Test 2 - NumRows check: ✅ PASSED (Python has +0.00% rows vs Stata)
- Test 3 - Precision1 check: ✅ PASSED
- Test 4 - Precision2 check: ✅ PASSED
- Test 5 - T-stat check: NA (Skipped for faster execution)

**Observations**:
- Stata:  1,221,161
- Python: 1,221,161
- Common: 1,221,161

**Precision1**: 0.000% obs with std_diff >= 1.00e-02 (tolerance: < 1%)

**Precision2**: 100th percentile diff = 2.24e-05 (tolerance: < 1.00e-01)

**Summary Statistics** (Common Observations):

| Statistic  |          Stata |         Python |     Difference | Std Difference |
|------------|----------------|----------------|----------------|----------------|
| count      |       1.22e+06 |       1.22e+06 |       1.22e+06 |       1.22e+06 |
| mean       |        -0.0086 |        -0.0086 |       3.50e-08 |       3.58e-08 |
| std        |         0.9776 |         0.9776 |       1.03e-05 |       1.05e-05 |
| min        |       -11.5532 |       -11.5532 |        -0.0025 |        -0.0025 |
| 25%        |        -0.5722 |        -0.5722 |      -1.09e-07 |      -1.12e-07 |
| 50%        |         0.0113 |         0.0113 |       1.98e-10 |       2.03e-10 |
| 75%        |         0.5788 |         0.5788 |       1.10e-07 |       1.13e-07 |
| max        |        23.1422 |        23.1422 |         0.0036 |         0.0036 |

**Regression Analysis** (Python ~ Stata):

- **Model**: python = 0.0000 + 1.0000 * stata
- **R-squared**: 1.0000
- **N observations**: 1,221,161

| Coefficient |     Estimate |    Std Error | t-statistic |   p-value |
|-------------|--------------|--------------|-------------|----------|
| Intercept   |     3.53e-08 |     9.29e-09 |      3.8004 |     0.000 |
| Slope       |       1.0000 |     9.51e-09 |    1.05e+08 |     0.000 |

**Feedback**:
- Num observations with std_diff >= TOL_DIFF_1: 0/1221161 (0.000%)
- Stata standard deviation: 9.78e-01

---

### GP

**Status**: ✅ PASSED

**Test Results**:
- Test 1 - Superset check: ✅ PASSED
- Test 2 - NumRows check: ✅ PASSED (Python has +0.05% rows vs Stata)
- Test 3 - Precision1 check: ✅ PASSED
- Test 4 - Precision2 check: ✅ PASSED
- Test 5 - T-stat check: NA (Skipped for faster execution)

**Observations**:
- Stata:  2,970,775
- Python: 2,972,227
- Common: 2,970,775

**Precision1**: 0.006% obs with std_diff >= 1.00e-02 (tolerance: < 1%)

**Precision2**: 100th percentile diff = 2.19e-07 (tolerance: < 1.00e-01)

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
- Test 1 - Superset check: ✅ PASSED
- Test 2 - NumRows check: ✅ PASSED (Python has +0.00% rows vs Stata)
- Test 3 - Precision1 check: ✅ PASSED
- Test 4 - Precision2 check: ✅ PASSED
- Test 5 - T-stat check: NA (Skipped for faster execution)

**Observations**:
- Stata:  334,058
- Python: 334,058
- Common: 334,058

**Precision1**: 0.000% obs with std_diff >= 1.00e-02 (tolerance: < 1%)

**Precision2**: 100th percentile diff = 0.00e+00 (tolerance: < 1.00e-01)

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
- Test 1 - Superset check: ✅ PASSED
- Test 2 - NumRows check: ✅ PASSED (Python has +0.36% rows vs Stata)
- Test 3 - Precision1 check: ✅ PASSED
- Test 4 - Precision2 check: ✅ PASSED
- Test 5 - T-stat check: NA (Skipped for faster execution)

**Observations**:
- Stata:  898,855
- Python: 902,079
- Common: 898,855

**Precision1**: 0.000% obs with std_diff >= 1.00e-02 (tolerance: < 1%)

**Precision2**: 100th percentile diff = 2.68e-07 (tolerance: < 1.00e-01)

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
- Test 1 - Superset check: ✅ PASSED
- Test 2 - NumRows check: ✅ PASSED (Python has +0.51% rows vs Stata)
- Test 3 - Precision1 check: ✅ PASSED
- Test 4 - Precision2 check: ✅ PASSED
- Test 5 - T-stat check: NA (Skipped for faster execution)

**Observations**:
- Stata:  3,219,259
- Python: 3,235,620
- Common: 3,219,235

**Precision1**: 0.008% obs with std_diff >= 1.00e-02 (tolerance: < 1%)

**Precision2**: 100th percentile diff = 1.10e-07 (tolerance: < 1.00e-01)

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
- Test 1 - Superset check: ✅ PASSED
- Test 2 - NumRows check: ✅ PASSED (Python has +0.53% rows vs Stata)
- Test 3 - Precision1 check: ✅ PASSED
- Test 4 - Precision2 check: ✅ PASSED
- Test 5 - T-stat check: NA (Skipped for faster execution)

**Observations**:
- Stata:  2,532,290
- Python: 2,545,662
- Common: 2,532,290

**Precision1**: 0.039% obs with std_diff >= 1.00e-02 (tolerance: < 1%)

**Precision2**: 100th percentile diff = 4.24e-03 (tolerance: < 1.00e-01)

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
- Test 1 - Superset check: ✅ PASSED
- Test 2 - NumRows check: ✅ PASSED (Python has +0.50% rows vs Stata)
- Test 3 - Precision1 check: ✅ PASSED
- Test 4 - Precision2 check: ✅ PASSED
- Test 5 - T-stat check: NA (Skipped for faster execution)

**Observations**:
- Stata:  2,668,375
- Python: 2,681,589
- Common: 2,668,315

**Precision1**: 0.017% obs with std_diff >= 1.00e-02 (tolerance: < 1%)

**Precision2**: 100th percentile diff = 2.46e-03 (tolerance: < 1.00e-01)

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

**Status**: ❌ FAILED

**Test Results**:
- Test 1 - Superset check: ❌ FAILED (Python missing 552785 Stata observations)
- Test 2 - NumRows check: ✅ PASSED (Python has -17.50% rows vs Stata)
- Test 3 - Precision1 check: ✅ PASSED
- Test 4 - Precision2 check: ✅ PASSED
- Test 5 - T-stat check: NA (Skipped for faster execution)

**Observations**:
- Stata:  3,158,336
- Python: 2,605,551
- Common: 2,605,551

**Precision1**: 0.000% obs with std_diff >= 1.00e-02 (tolerance: < 1%)

**Precision2**: 100th percentile diff = 2.83e-07 (tolerance: < 1.00e-01)

**Summary Statistics** (Common Observations):

| Statistic  |          Stata |         Python |     Difference | Std Difference |
|------------|----------------|----------------|----------------|----------------|
| count      |       2.61e+06 |       2.61e+06 |       2.61e+06 |       2.61e+06 |
| mean       |         0.3391 |         0.3391 |       1.53e-08 |       5.43e-08 |
| std        |         0.2809 |         0.2809 |       2.02e-06 |       7.19e-06 |
| min        |         0.0000 |         0.0000 |      -6.07e-04 |        -0.0022 |
| 25%        |         0.1260 |         0.1260 |      -2.45e-09 |      -8.70e-09 |
| 50%        |         0.2628 |         0.2628 |         0.0000 |         0.0000 |
| 75%        |         0.4834 |         0.4834 |       2.78e-09 |       9.89e-09 |
| max        |         4.3717 |         4.3717 |       2.19e-04 |       7.81e-04 |

**Regression Analysis** (Python ~ Stata):

- **Model**: python = 0.0000 + 1.0000 * stata
- **R-squared**: 1.0000
- **N observations**: 2,605,551

| Coefficient |     Estimate |    Std Error | t-statistic |   p-value |
|-------------|--------------|--------------|-------------|----------|
| Intercept   |     1.27e-08 |     1.96e-09 |      6.4990 |     0.000 |
| Slope       |       1.0000 |     4.45e-09 |    2.25e+08 |     0.000 |

**Feedback**:
- Num observations with std_diff >= TOL_DIFF_1: 0/2605551 (0.000%)
- Stata standard deviation: 2.81e-01

---

### HerfAsset

**Status**: ❌ FAILED

**Test Results**:
- Test 1 - Superset check: ❌ FAILED (Python missing 483832 Stata observations)
- Test 2 - NumRows check: ✅ PASSED (Python has -19.00% rows vs Stata)
- Test 3 - Precision1 check: ✅ PASSED
- Test 4 - Precision2 check: ✅ PASSED
- Test 5 - T-stat check: NA (Skipped for faster execution)

**Observations**:
- Stata:  2,547,057
- Python: 2,063,225
- Common: 2,063,225

**Precision1**: 0.000% obs with std_diff >= 1.00e-02 (tolerance: < 1%)

**Precision2**: 100th percentile diff = 2.86e-07 (tolerance: < 1.00e-01)

**Summary Statistics** (Common Observations):

| Statistic  |          Stata |         Python |     Difference | Std Difference |
|------------|----------------|----------------|----------------|----------------|
| count      |       2.06e+06 |       2.06e+06 |       2.06e+06 |       2.06e+06 |
| mean       |         0.3544 |         0.3544 |       2.31e-10 |       8.31e-10 |
| std        |         0.2781 |         0.2781 |       1.21e-08 |       4.35e-08 |
| min        |         0.0173 |         0.0173 |      -1.19e-07 |      -4.29e-07 |
| 25%        |         0.1337 |         0.1337 |      -2.49e-09 |      -8.97e-09 |
| 50%        |         0.2803 |         0.2803 |      -8.38e-12 |      -3.02e-11 |
| 75%        |         0.5018 |         0.5018 |       2.92e-09 |       1.05e-08 |
| max        |         1.0000 |         1.0000 |       9.93e-08 |       3.57e-07 |

**Regression Analysis** (Python ~ Stata):

- **Model**: python = -0.0000 + 1.0000 * stata
- **R-squared**: 1.0000
- **N observations**: 2,063,225

| Coefficient |     Estimate |    Std Error | t-statistic |   p-value |
|-------------|--------------|--------------|-------------|----------|
| Intercept   |    -4.47e-10 |     1.36e-11 |    -32.7861 |     0.000 |
| Slope       |       1.0000 |     3.02e-11 |    3.31e+10 |     0.000 |

**Feedback**:
- Num observations with std_diff >= TOL_DIFF_1: 0/2063225 (0.000%)
- Stata standard deviation: 2.78e-01

---

### HerfBE

**Status**: ❌ FAILED

**Test Results**:
- Test 1 - Superset check: ❌ FAILED (Python missing 483832 Stata observations)
- Test 2 - NumRows check: ✅ PASSED (Python has -19.00% rows vs Stata)
- Test 3 - Precision1 check: ✅ PASSED
- Test 4 - Precision2 check: ✅ PASSED
- Test 5 - T-stat check: NA (Skipped for faster execution)

**Observations**:
- Stata:  2,547,057
- Python: 2,063,225
- Common: 2,063,225

**Precision1**: 0.000% obs with std_diff >= 1.00e-02 (tolerance: < 1%)

**Precision2**: 100th percentile diff = 2.92e-07 (tolerance: < 1.00e-01)

**Summary Statistics** (Common Observations):

| Statistic  |          Stata |         Python |     Difference | Std Difference |
|------------|----------------|----------------|----------------|----------------|
| count      |       2.06e+06 |       2.06e+06 |       2.06e+06 |       2.06e+06 |
| mean       |        86.1299 |        86.1319 |         0.0020 |       2.73e-07 |
| std        |      7461.7358 |      7461.9629 |         0.2401 |       3.22e-05 |
| min        |         0.0000 |         0.0000 |        -0.7337 |      -9.83e-05 |
| 25%        |         0.1397 |         0.1397 |      -2.55e-09 |      -3.42e-13 |
| 50%        |         0.2823 |         0.2823 |         0.0000 |         0.0000 |
| 75%        |         0.5253 |         0.5253 |       2.66e-09 |       3.57e-13 |
| max        |    859657.6583 |    859686.7510 |        29.0949 |         0.0039 |

**Regression Analysis** (Python ~ Stata):

- **Model**: python = -0.0006 + 1.0000 * stata
- **R-squared**: 1.0000
- **N observations**: 2,063,225

| Coefficient |     Estimate |    Std Error | t-statistic |   p-value |
|-------------|--------------|--------------|-------------|----------|
| Intercept   |    -5.86e-04 |     5.45e-05 |    -10.7552 |     0.000 |
| Slope       |       1.0000 |     7.30e-09 |    1.37e+08 |     0.000 |

**Feedback**:
- Num observations with std_diff >= TOL_DIFF_1: 0/2063225 (0.000%)
- Stata standard deviation: 7.46e+03

---

### High52

**Status**: ✅ PASSED

**Test Results**:
- Test 1 - Superset check: ✅ PASSED
- Test 2 - NumRows check: ✅ PASSED (Python has +0.00% rows vs Stata)
- Test 3 - Precision1 check: ✅ PASSED
- Test 4 - Precision2 check: ✅ PASSED
- Test 5 - T-stat check: NA (Skipped for faster execution)

**Observations**:
- Stata:  4,995,429
- Python: 4,995,429
- Common: 4,995,429

**Precision1**: 0.000% obs with std_diff >= 1.00e-02 (tolerance: < 1%)

**Precision2**: 100th percentile diff = 4.11e-07 (tolerance: < 1.00e-01)

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
- Test 1 - Superset check: ✅ PASSED
- Test 2 - NumRows check: ✅ PASSED (Python has +0.00% rows vs Stata)
- Test 3 - Precision1 check: ✅ PASSED
- Test 4 - Precision2 check: ✅ PASSED
- Test 5 - T-stat check: NA (Skipped for faster execution)

**Observations**:
- Stata:  8,842
- Python: 8,842
- Common: 8,842

**Precision1**: 0.000% obs with std_diff >= 1.00e-02 (tolerance: < 1%)

**Precision2**: 100th percentile diff = 9.92e-08 (tolerance: < 1.00e-01)

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
- Test 1 - Superset check: ✅ PASSED
- Test 2 - NumRows check: ✅ PASSED (Python has +0.00% rows vs Stata)
- Test 3 - Precision1 check: ✅ PASSED
- Test 4 - Precision2 check: ✅ PASSED
- Test 5 - T-stat check: NA (Skipped for faster execution)

**Observations**:
- Stata:  4,980,936
- Python: 4,980,936
- Common: 4,980,936

**Precision1**: 0.021% obs with std_diff >= 1.00e-02 (tolerance: < 1%)

**Precision2**: 100th percentile diff = 5.31e-03 (tolerance: < 1.00e-01)

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
- Test 1 - Superset check: ✅ PASSED
- Test 2 - NumRows check: ✅ PASSED (Python has +0.00% rows vs Stata)
- Test 3 - Precision1 check: ✅ PASSED
- Test 4 - Precision2 check: ✅ PASSED
- Test 5 - T-stat check: NA (Skipped for faster execution)

**Observations**:
- Stata:  4,849,170
- Python: 4,849,170
- Common: 4,849,170

**Precision1**: 0.000% obs with std_diff >= 1.00e-02 (tolerance: < 1%)

**Precision2**: 100th percentile diff = 1.31e-04 (tolerance: < 1.00e-01)

**Summary Statistics** (Common Observations):

| Statistic  |          Stata |         Python |     Difference | Std Difference |
|------------|----------------|----------------|----------------|----------------|
| count      |       4.85e+06 |       4.85e+06 |       4.85e+06 |       4.85e+06 |
| mean       |         0.0300 |         0.0300 |      -1.18e-08 |      -4.46e-07 |
| std        |         0.0264 |         0.0264 |       3.13e-07 |       1.19e-05 |
| min        |       1.02e-05 |       1.02e-05 |      -5.29e-05 |        -0.0020 |
| 25%        |         0.0142 |         0.0142 |      -2.78e-17 |      -1.05e-15 |
| 50%        |         0.0232 |         0.0232 |         0.0000 |         0.0000 |
| 75%        |         0.0379 |         0.0379 |       2.78e-17 |       1.05e-15 |
| max        |         2.5092 |         2.5092 |       1.31e-05 |       4.95e-04 |

**Regression Analysis** (Python ~ Stata):

- **Model**: python = -0.0000 + 1.0000 * stata
- **R-squared**: 1.0000
- **N observations**: 4,849,170

| Coefficient |     Estimate |    Std Error | t-statistic |   p-value |
|-------------|--------------|--------------|-------------|----------|
| Intercept   |    -1.74e-08 |     2.15e-10 |    -80.6055 |     0.000 |
| Slope       |       1.0000 |     5.38e-09 |    1.86e+08 |     0.000 |

**Feedback**:
- Num observations with std_diff >= TOL_DIFF_1: 0/4849170 (0.000%)
- Stata standard deviation: 2.64e-02

---

### Illiquidity

**Status**: ❌ FAILED

**Test Results**:
- Test 1 - Superset check: ✅ PASSED
- Test 2 - NumRows check: ❌ FAILED (Python has +10.79% rows vs Stata)
- Test 3 - Precision1 check: ✅ PASSED
- Test 4 - Precision2 check: ✅ PASSED
- Test 5 - T-stat check: NA (Skipped for faster execution)

**Observations**:
- Stata:  4,278,152
- Python: 4,739,556
- Common: 4,278,152

**Precision1**: 0.000% obs with std_diff >= 1.00e-02 (tolerance: < 1%)

**Precision2**: 100th percentile diff = 1.29e-07 (tolerance: < 1.00e-01)

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
- Test 1 - Superset check: ✅ PASSED
- Test 2 - NumRows check: ✅ PASSED (Python has +0.00% rows vs Stata)
- Test 3 - Precision1 check: ✅ PASSED
- Test 4 - Precision2 check: ✅ PASSED
- Test 5 - T-stat check: NA (Skipped for faster execution)

**Observations**:
- Stata:  4,043,138
- Python: 4,043,138
- Common: 4,043,138

**Precision1**: 0.000% obs with std_diff >= 1.00e-02 (tolerance: < 1%)

**Precision2**: 100th percentile diff = 3.20e-07 (tolerance: < 1.00e-01)

**Summary Statistics** (Common Observations):

| Statistic  |          Stata |         Python |     Difference | Std Difference |
|------------|----------------|----------------|----------------|----------------|
| count      |       4.04e+06 |       4.04e+06 |       4.04e+06 |       4.04e+06 |
| mean       |         0.0857 |         0.0857 |      -4.84e-11 |      -2.79e-10 |
| std        |         0.1736 |         0.1736 |       5.91e-09 |       3.41e-08 |
| min        |        -0.9265 |        -0.9265 |      -2.53e-07 |      -1.46e-06 |
| 25%        |        -0.0099 |        -0.0099 |      -2.11e-09 |      -1.21e-08 |
| 50%        |         0.0775 |         0.0775 |      -2.82e-11 |      -1.62e-10 |
| 75%        |         0.1676 |         0.1676 |       2.02e-09 |       1.17e-08 |
| max        |        10.5068 |        10.5068 |       2.19e-07 |       1.26e-06 |

**Regression Analysis** (Python ~ Stata):

- **Model**: python = 0.0000 + 1.0000 * stata
- **R-squared**: 1.0000
- **N observations**: 4,043,138

| Coefficient |     Estimate |    Std Error | t-statistic |   p-value |
|-------------|--------------|--------------|-------------|----------|
| Intercept   |     2.32e-11 |     3.28e-12 |      7.0801 |     0.000 |
| Slope       |       1.0000 |     1.69e-11 |    5.90e+10 |     0.000 |

**Feedback**:
- Num observations with std_diff >= TOL_DIFF_1: 0/4043138 (0.000%)
- Stata standard deviation: 1.74e-01

---

### IndRetBig

**Status**: ✅ PASSED

**Test Results**:
- Test 1 - Superset check: ✅ PASSED
- Test 2 - NumRows check: ✅ PASSED (Python has +0.34% rows vs Stata)
- Test 3 - Precision1 check: ✅ PASSED
- Test 4 - Precision2 check: ✅ PASSED
- Test 5 - T-stat check: NA (Skipped for faster execution)

**Observations**:
- Stata:  2,607,795
- Python: 2,616,695
- Common: 2,602,394

**Precision1**: 0.000% obs with std_diff >= 1.00e-02 (tolerance: < 1%)

**Precision2**: 100th percentile diff = 2.37e-15 (tolerance: < 1.00e-01)

**Summary Statistics** (Common Observations):

| Statistic  |          Stata |         Python |     Difference | Std Difference |
|------------|----------------|----------------|----------------|----------------|
| count      |       2.60e+06 |       2.60e+06 |       2.60e+06 |       2.60e+06 |
| mean       |         0.0180 |         0.0180 |       7.40e-20 |       1.05e-18 |
| std        |         0.0704 |         0.0704 |       3.26e-17 |       4.63e-16 |
| min        |        -0.4860 |        -0.4860 |      -2.22e-16 |      -3.15e-15 |
| 25%        |        -0.0206 |        -0.0206 |      -2.52e-17 |      -3.57e-16 |
| 50%        |         0.0176 |         0.0176 |         0.0000 |         0.0000 |
| 75%        |         0.0554 |         0.0554 |       2.69e-17 |       3.82e-16 |
| max        |         1.8831 |         1.8831 |       1.94e-16 |       2.76e-15 |

**Regression Analysis** (Python ~ Stata):

- **Model**: python = 0.0000 + 1.0000 * stata
- **R-squared**: 1.0000
- **N observations**: 2,602,394

| Coefficient |     Estimate |    Std Error | t-statistic |   p-value |
|-------------|--------------|--------------|-------------|----------|
| Intercept   |     7.14e-16 |     3.80e-18 |    188.0642 |     0.000 |
| Slope       |       1.0000 |     5.23e-17 |    1.91e+16 |     0.000 |

**Feedback**:
- Num observations with std_diff >= TOL_DIFF_1: 0/2602394 (0.000%)
- Stata standard deviation: 7.04e-02

---

### IntMom

**Status**: ❌ FAILED

**Test Results**:
- Test 1 - Superset check: ✅ PASSED
- Test 2 - NumRows check: ❌ FAILED (Python has +9.79% rows vs Stata)
- Test 3 - Precision1 check: ✅ PASSED
- Test 4 - Precision2 check: ✅ PASSED
- Test 5 - T-stat check: NA (Skipped for faster execution)

**Observations**:
- Stata:  3,686,625
- Python: 4,047,630
- Common: 3,686,625

**Precision1**: 0.000% obs with std_diff >= 1.00e-02 (tolerance: < 1%)

**Precision2**: 100th percentile diff = 2.66e-07 (tolerance: < 1.00e-01)

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
- Test 1 - Superset check: ✅ PASSED
- Test 2 - NumRows check: ✅ PASSED (Python has -0.00% rows vs Stata)
- Test 3 - Precision1 check: ✅ PASSED
- Test 4 - Precision2 check: ✅ PASSED
- Test 5 - T-stat check: NA (Skipped for faster execution)

**Observations**:
- Stata:  1,728,575
- Python: 1,728,573
- Common: 1,728,572

**Precision1**: 0.011% obs with std_diff >= 1.00e-02 (tolerance: < 1%)

**Precision2**: 100th percentile diff = 3.08e-03 (tolerance: < 1.00e-01)

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
- Test 1 - Superset check: ✅ PASSED
- Test 2 - NumRows check: ✅ PASSED (Python has -0.00% rows vs Stata)
- Test 3 - Precision1 check: ✅ PASSED
- Test 4 - Precision2 check: ✅ PASSED
- Test 5 - T-stat check: NA (Skipped for faster execution)

**Observations**:
- Stata:  1,881,254
- Python: 1,881,252
- Common: 1,881,251

**Precision1**: 0.149% obs with std_diff >= 1.00e-02 (tolerance: < 1%)

**Precision2**: 100th percentile diff = 4.12e-02 (tolerance: < 1.00e-01)

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
- Test 1 - Superset check: ✅ PASSED
- Test 2 - NumRows check: ✅ PASSED (Python has -0.00% rows vs Stata)
- Test 3 - Precision1 check: ✅ PASSED
- Test 4 - Precision2 check: ✅ PASSED
- Test 5 - T-stat check: NA (Skipped for faster execution)

**Observations**:
- Stata:  1,881,254
- Python: 1,881,252
- Common: 1,881,251

**Precision1**: 0.155% obs with std_diff >= 1.00e-02 (tolerance: < 1%)

**Precision2**: 100th percentile diff = 8.14e-02 (tolerance: < 1.00e-01)

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
- Test 1 - Superset check: ✅ PASSED
- Test 2 - NumRows check: ✅ PASSED (Python has -0.00% rows vs Stata)
- Test 3 - Precision1 check: ✅ PASSED
- Test 4 - Precision2 check: ✅ PASSED
- Test 5 - T-stat check: NA (Skipped for faster execution)

**Observations**:
- Stata:  1,876,810
- Python: 1,876,808
- Common: 1,876,807

**Precision1**: 0.009% obs with std_diff >= 1.00e-02 (tolerance: < 1%)

**Precision2**: 100th percentile diff = 1.72e-03 (tolerance: < 1.00e-01)

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
- Test 1 - Superset check: ✅ PASSED
- Test 2 - NumRows check: ✅ PASSED (Python has +0.01% rows vs Stata)
- Test 3 - Precision1 check: ✅ PASSED
- Test 4 - Precision2 check: ✅ PASSED
- Test 5 - T-stat check: NA (Skipped for faster execution)

**Observations**:
- Stata:  1,973,756
- Python: 1,973,910
- Common: 1,973,744

**Precision1**: 0.000% obs with std_diff >= 1.00e-02 (tolerance: < 1%)

**Precision2**: 100th percentile diff = 7.19e-06 (tolerance: < 1.00e-01)

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
- Test 1 - Superset check: ✅ PASSED
- Test 2 - NumRows check: ✅ PASSED (Python has +0.52% rows vs Stata)
- Test 3 - Precision1 check: ✅ PASSED
- Test 4 - Precision2 check: ✅ PASSED
- Test 5 - T-stat check: NA (Skipped for faster execution)

**Observations**:
- Stata:  2,928,130
- Python: 2,943,499
- Common: 2,928,106

**Precision1**: 0.000% obs with std_diff >= 1.00e-02 (tolerance: < 1%)

**Precision2**: 100th percentile diff = 1.80e-07 (tolerance: < 1.00e-01)

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

**Status**: ❌ FAILED

**Test Results**:
- Test 1 - Superset check: ❌ FAILED (Python missing 236173 Stata observations)
- Test 2 - NumRows check: ✅ PASSED (Python has -9.68% rows vs Stata)
- Test 3 - Precision1 check: ✅ PASSED
- Test 4 - Precision2 check: ✅ PASSED
- Test 5 - T-stat check: NA (Skipped for faster execution)

**Observations**:
- Stata:  2,411,862
- Python: 2,178,399
- Common: 2,175,689

**Precision1**: 0.116% obs with std_diff >= 1.00e-02 (tolerance: < 1%)

**Precision2**: 100th percentile diff = 4.27e-02 (tolerance: < 1.00e-01)

**Summary Statistics** (Common Observations):

| Statistic  |          Stata |         Python |     Difference | Std Difference |
|------------|----------------|----------------|----------------|----------------|
| count      |       2.18e+06 |       2.18e+06 |       2.18e+06 |       2.18e+06 |
| mean       |         1.0044 |         1.0035 |      -9.52e-04 |      -5.01e-04 |
| std        |         1.9006 |         1.9003 |         0.0532 |         0.0280 |
| min        |     -2512.3491 |     -2512.3180 |       -25.0000 |       -13.1539 |
| 25%        |         0.6745 |         0.6739 |      -2.22e-08 |      -1.17e-08 |
| 50%        |         0.9356 |         0.9353 |         0.0000 |         0.0000 |
| 75%        |         1.2013 |         1.2009 |       2.20e-08 |       1.16e-08 |
| max        |       253.6225 |       253.6223 |         0.0311 |         0.0164 |

**Regression Analysis** (Python ~ Stata):

- **Model**: python = -0.0004 + 0.9995 * stata
- **R-squared**: 0.9992
- **N observations**: 2,175,689

| Coefficient |     Estimate |    Std Error | t-statistic |   p-value |
|-------------|--------------|--------------|-------------|----------|
| Intercept   |    -4.20e-04 |     4.08e-05 |    -10.2883 |     0.000 |
| Slope       |       0.9995 |     1.90e-05 |  52651.3883 |     0.000 |

**Feedback**:
- Num observations with std_diff >= TOL_DIFF_1: 2532/2175689 (0.116%)
- Stata standard deviation: 1.90e+00

---

### LRreversal

**Status**: ❌ FAILED

**Test Results**:
- Test 1 - Superset check: ✅ PASSED
- Test 2 - NumRows check: ❌ FAILED (Python has +32.28% rows vs Stata)
- Test 3 - Precision1 check: ✅ PASSED
- Test 4 - Precision2 check: ✅ PASSED
- Test 5 - T-stat check: NA (Skipped for faster execution)

**Observations**:
- Stata:  3,059,782
- Python: 4,047,630
- Common: 3,059,782

**Precision1**: 0.123% obs with std_diff >= 1.00e-02 (tolerance: < 1%)

**Precision2**: 100th percentile diff = 3.65e-02 (tolerance: < 1.00e-01)

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
- Test 1 - Superset check: ✅ PASSED
- Test 2 - NumRows check: ✅ PASSED (Python has +0.00% rows vs Stata)
- Test 3 - Precision1 check: ✅ PASSED
- Test 4 - Precision2 check: ✅ PASSED
- Test 5 - T-stat check: NA (Skipped for faster execution)

**Observations**:
- Stata:  3,014,665
- Python: 3,014,667
- Common: 3,014,665

**Precision1**: 0.000% obs with std_diff >= 1.00e-02 (tolerance: < 1%)

**Precision2**: 100th percentile diff = 1.94e-07 (tolerance: < 1.00e-01)

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

**Status**: ❌ FAILED

**Test Results**:
- Test 1 - Superset check: ✅ PASSED
- Test 2 - NumRows check: ❌ FAILED (Python has +15.05% rows vs Stata)
- Test 3 - Precision1 check: ✅ PASSED
- Test 4 - Precision2 check: ✅ PASSED
- Test 5 - T-stat check: NA (Skipped for faster execution)

**Observations**:
- Stata:  3,518,261
- Python: 4,047,630
- Common: 3,518,261

**Precision1**: 0.000% obs with std_diff >= 1.00e-02 (tolerance: < 1%)

**Precision2**: 100th percentile diff = 2.69e-07 (tolerance: < 1.00e-01)

**Summary Statistics** (Common Observations):

| Statistic  |          Stata |         Python |     Difference | Std Difference |
|------------|----------------|----------------|----------------|----------------|
| count      |       3.52e+06 |       3.52e+06 |       3.52e+06 |       3.52e+06 |
| mean       |         0.0735 |         0.0735 |      -8.46e-12 |      -1.78e-11 |
| std        |         0.4754 |         0.4754 |       1.37e-08 |       2.87e-08 |
| min        |        -1.0000 |        -1.0000 |      -2.15e-06 |      -4.53e-06 |
| 25%        |        -0.1506 |        -0.1506 |      -3.17e-09 |      -6.67e-09 |
| 50%        |         0.0249 |         0.0249 |         0.0000 |         0.0000 |
| 75%        |         0.2121 |         0.2121 |       3.18e-09 |       6.69e-09 |
| max        |        80.0474 |        80.0474 |       1.27e-06 |       2.68e-06 |

**Regression Analysis** (Python ~ Stata):

- **Model**: python = 0.0000 + 1.0000 * stata
- **R-squared**: 1.0000
- **N observations**: 3,518,261

| Coefficient |     Estimate |    Std Error | t-statistic |   p-value |
|-------------|--------------|--------------|-------------|----------|
| Intercept   |     2.89e-11 |     7.37e-12 |      3.9216 |     0.000 |
| Slope       |       1.0000 |     1.53e-11 |    6.53e+10 |     0.000 |

**Feedback**:
- Num observations with std_diff >= TOL_DIFF_1: 0/3518261 (0.000%)
- Stata standard deviation: 4.75e-01

---

### MS

**Status**: ❌ FAILED

**Test Results**:
- Test 1 - Superset check: ✅ PASSED
- Test 2 - NumRows check: ✅ PASSED (Python has +0.00% rows vs Stata)
- Test 3 - Precision1 check: ❌ FAILED
- Test 4 - Precision2 check: ❌ FAILED
- Test 5 - T-stat check: NA (Skipped for faster execution)

**Observations**:
- Stata:  473,079
- Python: 473,079
- Common: 473,079

**Precision1**: 31.919% obs with std_diff >= 1.00e-02 (tolerance: < 1%)

**Precision2**: 100th percentile diff = 2.59e+00 (tolerance: < 1.00e-01)

**Summary Statistics** (Common Observations):

| Statistic  |          Stata |         Python |     Difference | Std Difference |
|------------|----------------|----------------|----------------|----------------|
| count      |    473079.0000 |    473079.0000 |    473079.0000 |    473079.0000 |
| mean       |         3.8814 |         3.4972 |        -0.3842 |        -0.2492 |
| std        |         1.5421 |         1.4530 |         0.6865 |         0.4452 |
| min        |         1.0000 |         1.0000 |        -5.0000 |        -3.2424 |
| 25%        |         3.0000 |         2.0000 |        -1.0000 |        -0.6485 |
| 50%        |         4.0000 |         4.0000 |         0.0000 |         0.0000 |
| 75%        |         5.0000 |         5.0000 |         0.0000 |         0.0000 |
| max        |         6.0000 |         6.0000 |         2.0000 |         1.2970 |

**Regression Analysis** (Python ~ Stata):

- **Model**: python = 0.2182 + 0.8448 * stata
- **R-squared**: 0.8039
- **N observations**: 473,079

| Coefficient |     Estimate |    Std Error | t-statistic |   p-value |
|-------------|--------------|--------------|-------------|----------|
| Intercept   |       0.2182 |       0.0025 |     86.1011 |     0.000 |
| Slope       |       0.8448 |     6.07e-04 |   1392.4809 |     0.000 |

**Feedback**:
- Num observations with std_diff >= TOL_DIFF_1: 151001/473079 (31.919%)
- Stata standard deviation: 1.54e+00

**Most Recent Bad Observations**:
```
   permno  yyyymm  python  stata  diff
0   10145  202412       1      3    -2
1   10220  202412       2      3    -1
2   10966  202412       4      5    -1
3   11275  202412       4      5    -1
4   11308  202412       4      3     1
5   11809  202412       5      6    -1
6   11884  202412       2      3    -1
7   11955  202412       4      6    -2
8   11995  202412       3      5    -2
9   12084  202412       4      6    -2
```

**Largest Differences**:
```
   permno  yyyymm  python  stata  diff
0   12169  200306       1      6    -5
1   12169  200307       1      6    -5
2   12169  200309       1      6    -5
3   12169  200310       1      6    -5
4   12169  200311       1      6    -5
5   12169  200407       1      6    -5
6   12169  200408       1      6    -5
7   12169  200409       1      6    -5
8   12169  200410       1      6    -5
9   12169  200411       1      6    -5
```

**Largest Differences Before 1950**:
```
No data before 1950
```

---

### MaxRet

**Status**: ✅ PASSED

**Test Results**:
- Test 1 - Superset check: ✅ PASSED
- Test 2 - NumRows check: ✅ PASSED (Python has +0.00% rows vs Stata)
- Test 3 - Precision1 check: ✅ PASSED
- Test 4 - Precision2 check: ✅ PASSED
- Test 5 - T-stat check: NA (Skipped for faster execution)

**Observations**:
- Stata:  5,033,574
- Python: 5,033,574
- Common: 5,033,574

**Precision1**: 0.000% obs with std_diff >= 1.00e-02 (tolerance: < 1%)

**Precision2**: 100th percentile diff = 0.00e+00 (tolerance: < 1.00e-01)

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
- Test 1 - Superset check: ✅ PASSED
- Test 2 - NumRows check: ✅ PASSED (Python has +0.03% rows vs Stata)
- Test 3 - Precision1 check: ✅ PASSED
- Test 4 - Precision2 check: ✅ PASSED
- Test 5 - T-stat check: NA (Skipped for faster execution)

**Observations**:
- Stata:  2,028,817
- Python: 2,029,426
- Common: 2,028,817

**Precision1**: 0.000% obs with std_diff >= 1.00e-02 (tolerance: < 1%)

**Precision2**: 100th percentile diff = 6.38e-04 (tolerance: < 1.00e-01)

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
- Test 1 - Superset check: ✅ PASSED
- Test 2 - NumRows check: ✅ PASSED (Python has +0.44% rows vs Stata)
- Test 3 - Precision1 check: ✅ PASSED
- Test 4 - Precision2 check: ✅ PASSED
- Test 5 - T-stat check: NA (Skipped for faster execution)

**Observations**:
- Stata:  3,713,622
- Python: 3,730,107
- Common: 3,713,622

**Precision1**: 0.000% obs with std_diff >= 1.00e-02 (tolerance: < 1%)

**Precision2**: 100th percentile diff = 2.50e-07 (tolerance: < 1.00e-01)

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
- Test 1 - Superset check: ✅ PASSED
- Test 2 - NumRows check: ✅ PASSED (Python has +0.00% rows vs Stata)
- Test 3 - Precision1 check: ✅ PASSED
- Test 4 - Precision2 check: ✅ PASSED
- Test 5 - T-stat check: NA (Skipped for faster execution)

**Observations**:
- Stata:  3,865,561
- Python: 3,865,561
- Common: 3,865,561

**Precision1**: 0.000% obs with std_diff >= 1.00e-02 (tolerance: < 1%)

**Precision2**: 100th percentile diff = 1.43e-15 (tolerance: < 1.00e-01)

**Summary Statistics** (Common Observations):

| Statistic  |          Stata |         Python |     Difference | Std Difference |
|------------|----------------|----------------|----------------|----------------|
| count      |       3.87e+06 |       3.87e+06 |       3.87e+06 |       3.87e+06 |
| mean       |         0.0113 |         0.0113 |       2.56e-21 |       4.39e-20 |
| std        |         0.0582 |         0.0582 |       2.93e-17 |       5.03e-16 |
| min        |        -0.5758 |        -0.5758 |      -8.88e-16 |      -1.53e-14 |
| 25%        |        -0.0153 |        -0.0153 |      -2.78e-17 |      -4.77e-16 |
| 50%        |         0.0096 |         0.0096 |         0.0000 |         0.0000 |
| 75%        |         0.0351 |         0.0351 |       2.78e-17 |       4.77e-16 |
| max        |         4.2943 |         4.2943 |       8.88e-16 |       1.53e-14 |

**Regression Analysis** (Python ~ Stata):

- **Model**: python = -0.0000 + 1.0000 * stata
- **R-squared**: 1.0000
- **N observations**: 3,865,561

| Coefficient |     Estimate |    Std Error | t-statistic |   p-value |
|-------------|--------------|--------------|-------------|----------|
| Intercept   |    -7.00e-16 |     1.75e-18 |   -399.0188 |     0.000 |
| Slope       |       1.0000 |     2.96e-17 |    3.38e+16 |     0.000 |

**Feedback**:
- Num observations with std_diff >= TOL_DIFF_1: 0/3865561 (0.000%)
- Stata standard deviation: 5.82e-02

---

### Mom6m

**Status**: ✅ PASSED

**Test Results**:
- Test 1 - Superset check: ✅ PASSED
- Test 2 - NumRows check: ✅ PASSED (Python has +0.00% rows vs Stata)
- Test 3 - Precision1 check: ✅ PASSED
- Test 4 - Precision2 check: ✅ PASSED
- Test 5 - T-stat check: NA (Skipped for faster execution)

**Observations**:
- Stata:  3,893,591
- Python: 3,893,591
- Common: 3,893,591

**Precision1**: 0.000% obs with std_diff >= 1.00e-02 (tolerance: < 1%)

**Precision2**: 100th percentile diff = 2.63e-07 (tolerance: < 1.00e-01)

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

**Status**: ✅ PASSED (with override)

**Override Applied**:
- Reviewed on: 2025-08-21
- Reviewed by: ac
- Details: Python is missing permno 10026 (gvkey 12825) in 198907. This is because the CIQ security rating has "NR" in 1989-07, which means that it should be excluded (see Avramov et al 2007 JF Table 3). We want only not-investment-grade stocks, excluding not-rated stocks. The old CIQ data likely missed this due to the poor deduplication code. The original paper only used SP ratings, so it's unclear what to do here. But the long-short portfolio t-stat and mean return match the OP quite well, so I'm accepting this.

**Test Results**:
- Test 1 - Superset check: ❌ FAILED (Python missing 48991 Stata observations)
- Test 2 - NumRows check: ✅ PASSED (Python has -11.53% rows vs Stata)
- Test 3 - Precision1 check: ✅ PASSED
- Test 4 - Precision2 check: ❌ FAILED
- Test 5 - T-stat check: NA (Skipped for faster execution)

**Observations**:
- Stata:  391,738
- Python: 346,566
- Common: 342,747

**Precision1**: 0.282% obs with std_diff >= 1.00e-02 (tolerance: < 1%)

**Precision2**: 100th percentile diff = 5.64e-01 (tolerance: < 1.00e-01)

**Summary Statistics** (Common Observations):

| Statistic  |          Stata |         Python |     Difference | Std Difference |
|------------|----------------|----------------|----------------|----------------|
| count      |    342747.0000 |    342747.0000 |    342747.0000 |    342747.0000 |
| mean       |         0.0549 |         0.0548 |      -1.63e-04 |      -4.27e-04 |
| std        |         0.3822 |         0.3826 |         0.0172 |         0.0450 |
| min        |        -0.9947 |        -0.9947 |        -1.1543 |        -3.0200 |
| 25%        |        -0.1348 |        -0.1351 |      -3.00e-09 |      -7.85e-09 |
| 50%        |         0.0326 |         0.0327 |       1.31e-14 |       3.42e-14 |
| 75%        |         0.2011 |         0.2013 |       3.02e-09 |       7.90e-09 |
| max        |        47.6527 |        47.6527 |         1.5000 |         3.9245 |

**Regression Analysis** (Python ~ Stata):

- **Model**: python = -0.0002 + 0.9999 * stata
- **R-squared**: 0.9980
- **N observations**: 342,747

| Coefficient |     Estimate |    Std Error | t-statistic |   p-value |
|-------------|--------------|--------------|-------------|----------|
| Intercept   |    -1.59e-04 |     2.97e-05 |     -5.3608 |     0.000 |
| Slope       |       0.9999 |     7.69e-05 |  13001.7151 |     0.000 |

**Feedback**:
- Num observations with std_diff >= TOL_DIFF_1: 967/342747 (0.282%)
- Stata standard deviation: 3.82e-01

**Most Recent Bad Observations**:
```
   permno  yyyymm    python     stata      diff
0   90979  202401 -0.064794  0.150524 -0.215318
1   90979  202312 -0.190532  0.065445 -0.255977
2   90979  202311 -0.348997 -0.103403 -0.245594
3   90353  202310  0.379207  0.206912  0.172295
4   90979  202310 -0.478251 -0.271199 -0.207052
5   93338  202310  0.035490  0.263470 -0.227979
6   90353  202309  0.537673  0.248826  0.288847
7   90979  202309 -0.290354 -0.240253 -0.050101
8   93338  202309  0.500335  0.372355  0.127980
9   90353  202308  0.491526  0.339849  0.151677
```

**Largest Differences**:
```
   permno  yyyymm    python     stata      diff
0   67969  199207  1.499999  0.000000  1.499999
1   10342  200001  1.736612  0.487289  1.249323
2   86360  200106 -0.469291  0.685000 -1.154291
3   90352  201210 -0.685484  0.426830 -1.112313
4   80658  200110  1.066668  0.000000  1.066668
5   48565  199307  1.333332  0.272727  1.060605
6   24731  198604 -0.459091  0.545455 -1.004546
7   67126  199002  1.821039  0.829268  0.991771
8   83161  200409  0.763565 -0.222222  0.985787
9   79338  200206  0.933027 -0.043428  0.976455
```

**Largest Differences Before 1950**:
```
No data before 1950
```

---

### MomOffSeason

**Status**: ✅ PASSED

**Test Results**:
- Test 1 - Superset check: ✅ PASSED
- Test 2 - NumRows check: ✅ PASSED (Python has +0.00% rows vs Stata)
- Test 3 - Precision1 check: ✅ PASSED
- Test 4 - Precision2 check: ✅ PASSED
- Test 5 - T-stat check: NA (Skipped for faster execution)

**Observations**:
- Stata:  3,396,704
- Python: 3,396,704
- Common: 3,396,704

**Precision1**: 0.000% obs with std_diff >= 1.00e-02 (tolerance: < 1%)

**Precision2**: 100th percentile diff = 3.06e-07 (tolerance: < 1.00e-01)

**Summary Statistics** (Common Observations):

| Statistic  |          Stata |         Python |     Difference | Std Difference |
|------------|----------------|----------------|----------------|----------------|
| count      |       3.40e+06 |       3.40e+06 |       3.40e+06 |       3.40e+06 |
| mean       |         0.0125 |         0.0125 |       2.08e-12 |       7.69e-11 |
| std        |         0.0270 |         0.0270 |       1.13e-09 |       4.17e-08 |
| min        |        -4.1713 |        -4.1713 |      -5.45e-08 |      -2.02e-06 |
| 25%        |       3.95e-04 |       3.95e-04 |      -4.91e-10 |      -1.82e-08 |
| 50%        |         0.0119 |         0.0119 |         0.0000 |         0.0000 |
| 75%        |         0.0240 |         0.0240 |       5.00e-10 |       1.85e-08 |
| max        |         1.5150 |         1.5150 |       1.14e-07 |       4.24e-06 |

**Regression Analysis** (Python ~ Stata):

- **Model**: python = -0.0000 + 1.0000 * stata
- **R-squared**: 1.0000
- **N observations**: 3,396,704

| Coefficient |     Estimate |    Std Error | t-statistic |   p-value |
|-------------|--------------|--------------|-------------|----------|
| Intercept   |    -3.61e-12 |     6.72e-13 |     -5.3709 |     0.000 |
| Slope       |       1.0000 |     2.26e-11 |    4.42e+10 |     0.000 |

**Feedback**:
- Num observations with std_diff >= TOL_DIFF_1: 0/3396704 (0.000%)
- Stata standard deviation: 2.70e-02

---

### MomOffSeason06YrPlus

**Status**: ❌ FAILED

**Test Results**:
- Test 1 - Superset check: ❌ FAILED (Python missing 44208 Stata observations)
- Test 2 - NumRows check: ✅ PASSED (Python has -1.82% rows vs Stata)
- Test 3 - Precision1 check: ✅ PASSED
- Test 4 - Precision2 check: ❌ FAILED
- Test 5 - T-stat check: NA (Skipped for faster execution)

**Observations**:
- Stata:  2,425,319
- Python: 2,381,111
- Common: 2,381,111

**Precision1**: 0.486% obs with std_diff >= 1.00e-02 (tolerance: < 1%)

**Precision2**: 100th percentile diff = 1.68e+00 (tolerance: < 1.00e-01)

**Summary Statistics** (Common Observations):

| Statistic  |          Stata |         Python |     Difference | Std Difference |
|------------|----------------|----------------|----------------|----------------|
| count      |       2.38e+06 |       2.38e+06 |       2.38e+06 |       2.38e+06 |
| mean       |         0.0134 |         0.0135 |       5.12e-05 |         0.0023 |
| std        |         0.0223 |         0.0224 |         0.0024 |         0.1093 |
| min        |        -0.2679 |        -0.2679 |        -0.1614 |        -7.2327 |
| 25%        |         0.0030 |         0.0030 |      -4.55e-10 |      -2.04e-08 |
| 50%        |         0.0126 |         0.0127 |         0.0000 |         0.0000 |
| 75%        |         0.0233 |         0.0234 |       4.55e-10 |       2.04e-08 |
| max        |         0.7811 |         0.7811 |         0.3239 |        14.5195 |

**Regression Analysis** (Python ~ Stata):

- **Model**: python = 0.0001 + 0.9979 * stata
- **R-squared**: 0.9882
- **N observations**: 2,381,111

| Coefficient |     Estimate |    Std Error | t-statistic |   p-value |
|-------------|--------------|--------------|-------------|----------|
| Intercept   |     7.99e-05 |     1.84e-06 |     43.3771 |     0.000 |
| Slope       |       0.9979 |     7.08e-05 |  14096.2658 |     0.000 |

**Feedback**:
- Num observations with std_diff >= TOL_DIFF_1: 11581/2381111 (0.486%)
- Stata standard deviation: 2.23e-02

**Most Recent Bad Observations**:
```
   permno  yyyymm    python     stata      diff
0   12592  202412 -0.034421 -0.028323 -0.006098
1   14877  202412 -0.031057 -0.022052 -0.009005
2   15913  202412 -0.050835 -0.075277  0.024442
3   16522  202412 -0.056738 -0.020471 -0.036268
4   84833  202412  0.027149  0.014767  0.012382
5   85401  202412  0.006058  0.033507 -0.027449
6   88471  202412 -0.072621 -0.063099 -0.009521
7   89175  202412  0.129627  0.087445  0.042182
8   91366  202412 -0.012479 -0.013879  0.001400
9   92102  202412 -0.057114 -0.026740 -0.030374
```

**Largest Differences**:
```
   permno  yyyymm    python     stata      diff
0   10411  199702  0.422525  0.098611  0.323914
1   11357  199702  0.314061  0.078372  0.235689
2   10419  199609  0.237537  0.029638  0.207899
3   10411  199703  0.290480  0.085644  0.204836
4   81666  200907  0.240340  0.042914  0.197426
5   87833  200708  0.275532  0.079590  0.195941
6   10419  199608  0.210776  0.019766  0.191010
7   11357  199703  0.251247  0.067723  0.183523
8   10419  199610  0.214992  0.033143  0.181849
9   87833  200711  0.246031  0.065308  0.180724
```

**Largest Differences Before 1950**:
```
No data before 1950
```

---

### MomOffSeason11YrPlus

**Status**: ❌ FAILED

**Test Results**:
- Test 1 - Superset check: ✅ PASSED
- Test 2 - NumRows check: ✅ PASSED (Python has +0.05% rows vs Stata)
- Test 3 - Precision1 check: ✅ PASSED
- Test 4 - Precision2 check: ❌ FAILED
- Test 5 - T-stat check: NA (Skipped for faster execution)

**Observations**:
- Stata:  1,677,532
- Python: 1,678,292
- Common: 1,677,526

**Precision1**: 0.880% obs with std_diff >= 1.00e-02 (tolerance: < 1%)

**Precision2**: 100th percentile diff = 1.82e+00 (tolerance: < 1.00e-01)

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

**Most Recent Bad Observations**:
```
   permno  yyyymm    python     stata      diff
0   11379  202412  0.068397  0.029216  0.039180
1   32791  202412  0.002924 -0.009110  0.012034
2   77900  202412  0.019325  0.024432 -0.005106
3   79666  202412  0.020302  0.032062 -0.011760
4   79903  202412  0.004065  0.000592  0.003473
5   82156  202412 -0.017317 -0.023979  0.006662
6   84321  202412  0.005217 -0.102155  0.107372
7   86812  202412  0.007851  0.024643 -0.016792
8   87043  202412  0.047672  0.011518  0.036154
9   87404  202412 -0.000059 -0.010178  0.010120
```

**Largest Differences**:
```
   permno  yyyymm    python     stata      diff
0   11803  201112 -0.028211 -2.611104  2.582893
1   77729  200404 -0.040883 -2.373474  2.332591
2   82163  201403  0.352963 -1.259050  1.612013
3   11803  201110  0.048556 -1.379478  1.428034
4   29153  197908 -0.998496  0.422049 -1.420545
5   82621  201509 -0.079410  1.246043 -1.325453
6   14761  200804 -0.022644  1.294914 -1.317558
7   82621  201508 -0.171515  0.951737 -1.123252
8   77173  201108  0.014516 -1.105233  1.119749
9   79689  201809  0.024521 -1.083838  1.108359
```

**Largest Differences Before 1950**:
```
No data before 1950
```

---

### MomOffSeason16YrPlus

**Status**: ❌ FAILED

**Test Results**:
- Test 1 - Superset check: ✅ PASSED
- Test 2 - NumRows check: ✅ PASSED (Python has +0.24% rows vs Stata)
- Test 3 - Precision1 check: ✅ PASSED
- Test 4 - Precision2 check: ❌ FAILED
- Test 5 - T-stat check: NA (Skipped for faster execution)

**Observations**:
- Stata:  1,027,449
- Python: 1,029,940
- Common: 1,027,449

**Precision1**: 0.510% obs with std_diff >= 1.00e-02 (tolerance: < 1%)

**Precision2**: 100th percentile diff = 6.05e-01 (tolerance: < 1.00e-01)

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

**Most Recent Bad Observations**:
```
   permno  yyyymm    python     stata      diff
0   11379  202412  0.002448  0.014200 -0.011752
1   32791  202412  0.024257 -0.002500  0.026758
2   52231  202412 -0.018362 -0.045180  0.026818
3   77900  202412 -0.004866 -0.005192  0.000326
4   79903  202412  0.000376 -0.007966  0.008342
5   82156  202412 -0.004761 -0.002425 -0.002336
6   86812  202412  0.006006 -0.011868  0.017874
7   87043  202412  0.039561  0.040528 -0.000967
8   87404  202412  0.025389  0.019622  0.005766
9   89169  202412  0.014077  0.020761 -0.006683
```

**Largest Differences**:
```
   permno  yyyymm    python     stata      diff
0   20002  199704  0.035400  0.085470 -0.050070
1   85401  202108  0.057048  0.007236  0.049812
2   41515  199310  0.051310  0.001904  0.049405
3   85401  202208  0.085915  0.036861  0.049054
4   85401  202209  0.059197  0.010437  0.048759
5   85401  202109  0.055278  0.006877  0.048401
6   41515  199309  0.086164  0.038549  0.047615
7   52250  201011  0.013986 -0.032840  0.046826
8   20002  199705  0.033726  0.079460 -0.045734
9   21785  200602  0.047106  0.002049  0.045057
```

**Largest Differences Before 1950**:
```
No data before 1950
```

---

### MomRev

**Status**: ✅ PASSED

**Test Results**:
- Test 1 - Superset check: ✅ PASSED
- Test 2 - NumRows check: ✅ PASSED (Python has +0.06% rows vs Stata)
- Test 3 - Precision1 check: ✅ PASSED
- Test 4 - Precision2 check: ✅ PASSED
- Test 5 - T-stat check: NA (Skipped for faster execution)

**Observations**:
- Stata:  262,210
- Python: 262,365
- Common: 261,856

**Precision1**: 0.000% obs with std_diff >= 1.00e-02 (tolerance: < 1%)

**Precision2**: 100th percentile diff = 0.00e+00 (tolerance: < 1.00e-01)

**Summary Statistics** (Common Observations):

| Statistic  |          Stata |         Python |     Difference | Std Difference |
|------------|----------------|----------------|----------------|----------------|
| count      |    261856.0000 |    261856.0000 |    261856.0000 |    261856.0000 |
| mean       |         0.5591 |         0.5591 |         0.0000 |         0.0000 |
| std        |         0.4965 |         0.4965 |         0.0000 |         0.0000 |
| min        |         0.0000 |         0.0000 |         0.0000 |         0.0000 |
| 25%        |         0.0000 |         0.0000 |         0.0000 |         0.0000 |
| 50%        |         1.0000 |         1.0000 |         0.0000 |         0.0000 |
| 75%        |         1.0000 |         1.0000 |         0.0000 |         0.0000 |
| max        |         1.0000 |         1.0000 |         0.0000 |         0.0000 |

**Regression Analysis** (Python ~ Stata):

- **Model**: python = -0.0000 + 1.0000 * stata
- **R-squared**: 1.0000
- **N observations**: 261,856

| Coefficient |     Estimate |    Std Error | t-statistic |   p-value |
|-------------|--------------|--------------|-------------|----------|
| Intercept   |    -2.99e-13 |     1.00e-15 |   -297.6163 |     0.000 |
| Slope       |       1.0000 |     1.34e-15 |    7.45e+14 |     0.000 |

**Feedback**:
- Num observations with std_diff >= TOL_DIFF_1: 0/261856 (0.000%)
- Stata standard deviation: 4.96e-01

---

### MomSeason

**Status**: ✅ PASSED

**Test Results**:
- Test 1 - Superset check: ✅ PASSED
- Test 2 - NumRows check: ✅ PASSED (Python has +0.00% rows vs Stata)
- Test 3 - Precision1 check: ✅ PASSED
- Test 4 - Precision2 check: ✅ PASSED
- Test 5 - T-stat check: NA (Skipped for faster execution)

**Observations**:
- Stata:  3,398,424
- Python: 3,398,424
- Common: 3,398,424

**Precision1**: 0.000% obs with std_diff >= 1.00e-02 (tolerance: < 1%)

**Precision2**: 100th percentile diff = 2.97e-07 (tolerance: < 1.00e-01)

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
- Test 1 - Superset check: ✅ PASSED
- Test 2 - NumRows check: ✅ PASSED (Python has +0.00% rows vs Stata)
- Test 3 - Precision1 check: ✅ PASSED
- Test 4 - Precision2 check: ✅ PASSED
- Test 5 - T-stat check: NA (Skipped for faster execution)

**Observations**:
- Stata:  2,432,862
- Python: 2,432,862
- Common: 2,432,862

**Precision1**: 0.000% obs with std_diff >= 1.00e-02 (tolerance: < 1%)

**Precision2**: 100th percentile diff = 3.40e-07 (tolerance: < 1.00e-01)

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
- Test 1 - Superset check: ✅ PASSED
- Test 2 - NumRows check: ✅ PASSED (Python has +0.00% rows vs Stata)
- Test 3 - Precision1 check: ✅ PASSED
- Test 4 - Precision2 check: ✅ PASSED
- Test 5 - T-stat check: NA (Skipped for faster execution)

**Observations**:
- Stata:  1,680,518
- Python: 1,680,518
- Common: 1,680,518

**Precision1**: 0.000% obs with std_diff >= 1.00e-02 (tolerance: < 1%)

**Precision2**: 100th percentile diff = 3.58e-07 (tolerance: < 1.00e-01)

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
- Test 1 - Superset check: ✅ PASSED
- Test 2 - NumRows check: ✅ PASSED (Python has +0.00% rows vs Stata)
- Test 3 - Precision1 check: ✅ PASSED
- Test 4 - Precision2 check: ✅ PASSED
- Test 5 - T-stat check: NA (Skipped for faster execution)

**Observations**:
- Stata:  1,194,902
- Python: 1,194,902
- Common: 1,194,902

**Precision1**: 0.000% obs with std_diff >= 1.00e-02 (tolerance: < 1%)

**Precision2**: 100th percentile diff = 3.71e-07 (tolerance: < 1.00e-01)

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
- Test 1 - Superset check: ✅ PASSED
- Test 2 - NumRows check: ✅ PASSED (Python has -0.13% rows vs Stata)
- Test 3 - Precision1 check: ✅ PASSED
- Test 4 - Precision2 check: ✅ PASSED
- Test 5 - T-stat check: NA (Skipped for faster execution)

**Observations**:
- Stata:  3,718,320
- Python: 3,713,622
- Common: 3,713,622

**Precision1**: 0.000% obs with std_diff >= 1.00e-02 (tolerance: < 1%)

**Precision2**: 100th percentile diff = 1.74e-07 (tolerance: < 1.00e-01)

**Summary Statistics** (Common Observations):

| Statistic  |          Stata |         Python |     Difference | Std Difference |
|------------|----------------|----------------|----------------|----------------|
| count      |       3.71e+06 |       3.71e+06 |       3.71e+06 |       3.71e+06 |
| mean       |         0.0117 |         0.0117 |       1.25e-13 |       7.23e-13 |
| std        |         0.1728 |         0.1728 |       4.34e-09 |       2.51e-08 |
| min        |        -0.9957 |        -0.9957 |      -5.00e-07 |      -2.89e-06 |
| 25%        |        -0.0633 |        -0.0633 |      -1.11e-16 |      -6.43e-16 |
| 50%        |         0.0000 |         0.0000 |         0.0000 |         0.0000 |
| 75%        |         0.0690 |         0.0690 |       1.11e-16 |       6.43e-16 |
| max        |        24.0000 |        24.0000 |       4.00e-07 |       2.32e-06 |

**Regression Analysis** (Python ~ Stata):

- **Model**: python = -0.0000 + 1.0000 * stata
- **R-squared**: 1.0000
- **N observations**: 3,713,622

| Coefficient |     Estimate |    Std Error | t-statistic |   p-value |
|-------------|--------------|--------------|-------------|----------|
| Intercept   |    -9.79e-12 |     2.25e-12 |     -4.3400 |     0.000 |
| Slope       |       1.0000 |     1.30e-11 |    7.68e+10 |     0.000 |

**Feedback**:
- Num observations with std_diff >= TOL_DIFF_1: 0/3713622 (0.000%)
- Stata standard deviation: 1.73e-01

---

### MomVol

**Status**: ✅ PASSED

**Test Results**:
- Test 1 - Superset check: ✅ PASSED
- Test 2 - NumRows check: ✅ PASSED (Python has +0.06% rows vs Stata)
- Test 3 - Precision1 check: ✅ PASSED
- Test 4 - Precision2 check: ✅ PASSED
- Test 5 - T-stat check: NA (Skipped for faster execution)

**Observations**:
- Stata:  1,095,615
- Python: 1,096,292
- Common: 1,095,614

**Precision1**: 0.091% obs with std_diff >= 1.00e-02 (tolerance: < 1%)

**Precision2**: 100th percentile diff = 0.00e+00 (tolerance: < 1.00e-01)

**Summary Statistics** (Common Observations):

| Statistic  |          Stata |         Python |     Difference | Std Difference |
|------------|----------------|----------------|----------------|----------------|
| count      |       1.10e+06 |       1.10e+06 |       1.10e+06 |       1.10e+06 |
| mean       |         5.7085 |         5.7094 |       9.12e-04 |       3.17e-04 |
| std        |         2.8802 |         2.8808 |         0.0302 |         0.0105 |
| min        |         1.0000 |         1.0000 |         0.0000 |         0.0000 |
| 25%        |         3.0000 |         3.0000 |         0.0000 |         0.0000 |
| 50%        |         6.0000 |         6.0000 |         0.0000 |         0.0000 |
| 75%        |         8.0000 |         8.0000 |         0.0000 |         0.0000 |
| max        |        10.0000 |        10.0000 |         1.0000 |         0.3472 |

**Regression Analysis** (Python ~ Stata):

- **Model**: python = -0.0001 + 1.0002 * stata
- **R-squared**: 0.9999
- **N observations**: 1,095,614

| Coefficient |     Estimate |    Std Error | t-statistic |   p-value |
|-------------|--------------|--------------|-------------|----------|
| Intercept   |    -6.81e-05 |     6.40e-05 |     -1.0645 |     0.287 |
| Slope       |       1.0002 |     1.00e-05 |  99913.1172 |     0.000 |

**Feedback**:
- Num observations with std_diff >= TOL_DIFF_1: 999/1095614 (0.091%)
- Stata standard deviation: 2.88e+00

---

### NOA

**Status**: ✅ PASSED

**Test Results**:
- Test 1 - Superset check: ✅ PASSED
- Test 2 - NumRows check: ✅ PASSED (Python has +0.51% rows vs Stata)
- Test 3 - Precision1 check: ✅ PASSED
- Test 4 - Precision2 check: ✅ PASSED
- Test 5 - T-stat check: NA (Skipped for faster execution)

**Observations**:
- Stata:  3,196,825
- Python: 3,213,240
- Common: 3,196,825

**Precision1**: 0.003% obs with std_diff >= 1.00e-02 (tolerance: < 1%)

**Precision2**: 100th percentile diff = 1.88e-07 (tolerance: < 1.00e-01)

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
- Test 1 - Superset check: ✅ PASSED
- Test 2 - NumRows check: ✅ PASSED (Python has +0.53% rows vs Stata)
- Test 3 - Precision1 check: ✅ PASSED
- Test 4 - Precision2 check: ✅ PASSED
- Test 5 - T-stat check: NA (Skipped for faster execution)

**Observations**:
- Stata:  2,782,808
- Python: 2,797,645
- Common: 2,782,808

**Precision1**: 0.003% obs with std_diff >= 1.00e-02 (tolerance: < 1%)

**Precision2**: 100th percentile diff = 2.36e-07 (tolerance: < 1.00e-01)

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
- Test 1 - Superset check: ✅ PASSED
- Test 2 - NumRows check: ✅ PASSED (Python has +0.03% rows vs Stata)
- Test 3 - Precision1 check: ✅ PASSED
- Test 4 - Precision2 check: ✅ PASSED
- Test 5 - T-stat check: NA (Skipped for faster execution)

**Observations**:
- Stata:  1,425,163
- Python: 1,425,639
- Common: 1,425,162

**Precision1**: 0.000% obs with std_diff >= 1.00e-02 (tolerance: < 1%)

**Precision2**: 100th percentile diff = 2.31e-07 (tolerance: < 1.00e-01)

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
- Test 1 - Superset check: ✅ PASSED
- Test 2 - NumRows check: ✅ PASSED (Python has +0.51% rows vs Stata)
- Test 3 - Precision1 check: ✅ PASSED
- Test 4 - Precision2 check: ✅ PASSED
- Test 5 - T-stat check: NA (Skipped for faster execution)

**Observations**:
- Stata:  2,874,470
- Python: 2,889,052
- Common: 2,874,470

**Precision1**: 0.001% obs with std_diff >= 1.00e-02 (tolerance: < 1%)

**Precision2**: 100th percentile diff = 2.15e-07 (tolerance: < 1.00e-01)

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
- Test 1 - Superset check: ✅ PASSED
- Test 2 - NumRows check: ✅ PASSED (Python has +0.07% rows vs Stata)
- Test 3 - Precision1 check: ✅ PASSED
- Test 4 - Precision2 check: ✅ PASSED
- Test 5 - T-stat check: NA (Skipped for faster execution)

**Observations**:
- Stata:  1,817,567
- Python: 1,818,920
- Common: 1,817,567

**Precision1**: 0.000% obs with std_diff >= 1.00e-02 (tolerance: < 1%)

**Precision2**: 100th percentile diff = 1.56e-07 (tolerance: < 1.00e-01)

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
- Test 1 - Superset check: ✅ PASSED
- Test 2 - NumRows check: ✅ PASSED (Python has +0.00% rows vs Stata)
- Test 3 - Precision1 check: ✅ PASSED
- Test 4 - Precision2 check: ✅ PASSED
- Test 5 - T-stat check: NA (Skipped for faster execution)

**Observations**:
- Stata:  2,823,456
- Python: 2,823,459
- Common: 2,823,456

**Precision1**: 0.009% obs with std_diff >= 1.00e-02 (tolerance: < 1%)

**Precision2**: 100th percentile diff = 0.00e+00 (tolerance: < 1.00e-01)

**Summary Statistics** (Common Observations):

| Statistic  |          Stata |         Python |     Difference | Std Difference |
|------------|----------------|----------------|----------------|----------------|
| count      |       2.82e+06 |       2.82e+06 |       2.82e+06 |       2.82e+06 |
| mean       |         1.2268 |         1.2267 |      -3.51e-05 |      -1.82e-05 |
| std        |         1.9293 |         1.9292 |         0.0280 |         0.0145 |
| min        |         0.0000 |         0.0000 |        -8.0000 |        -4.1465 |
| 25%        |         0.0000 |         0.0000 |         0.0000 |         0.0000 |
| 50%        |         0.0000 |         0.0000 |         0.0000 |         0.0000 |
| 75%        |         2.0000 |         2.0000 |         0.0000 |         0.0000 |
| max        |         8.0000 |         8.0000 |         8.0000 |         4.1465 |

**Regression Analysis** (Python ~ Stata):

- **Model**: python = 0.0001 + 0.9999 * stata
- **R-squared**: 0.9998
- **N observations**: 2,823,456

| Coefficient |     Estimate |    Std Error | t-statistic |   p-value |
|-------------|--------------|--------------|-------------|----------|
| Intercept   |     1.41e-04 |     1.98e-05 |      7.1124 |     0.000 |
| Slope       |       0.9999 |     8.65e-06 | 115576.6191 |     0.000 |

**Feedback**:
- Num observations with std_diff >= TOL_DIFF_1: 250/2823456 (0.009%)
- Stata standard deviation: 1.93e+00

---

### OPLeverage

**Status**: ✅ PASSED

**Test Results**:
- Test 1 - Superset check: ✅ PASSED
- Test 2 - NumRows check: ✅ PASSED (Python has +0.03% rows vs Stata)
- Test 3 - Precision1 check: ✅ PASSED
- Test 4 - Precision2 check: ✅ PASSED
- Test 5 - T-stat check: NA (Skipped for faster execution)

**Observations**:
- Stata:  3,607,726
- Python: 3,608,854
- Common: 3,607,726

**Precision1**: 0.003% obs with std_diff >= 1.00e-02 (tolerance: < 1%)

**Precision2**: 100th percentile diff = 2.33e-07 (tolerance: < 1.00e-01)

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
- Test 1 - Superset check: ✅ PASSED
- Test 2 - NumRows check: ✅ PASSED (Python has +0.01% rows vs Stata)
- Test 3 - Precision1 check: ✅ PASSED
- Test 4 - Precision2 check: ✅ PASSED
- Test 5 - T-stat check: NA (Skipped for faster execution)

**Observations**:
- Stata:  1,197,546
- Python: 1,197,639
- Common: 1,197,024

**Precision1**: 0.000% obs with std_diff >= 1.00e-02 (tolerance: < 1%)

**Precision2**: 100th percentile diff = 0.00e+00 (tolerance: < 1.00e-01)

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

**Status**: ❌ FAILED

**Test Results**:
- Test 1 - Superset check: ✅ PASSED
- Test 2 - NumRows check: ❌ FAILED (Python has +21.81% rows vs Stata)
- Test 3 - Precision1 check: ✅ PASSED
- Test 4 - Precision2 check: ✅ PASSED
- Test 5 - T-stat check: NA (Skipped for faster execution)

**Observations**:
- Stata:  1,407,636
- Python: 1,714,592
- Common: 1,407,636

**Precision1**: 0.000% obs with std_diff >= 1.00e-02 (tolerance: < 1%)

**Precision2**: 100th percentile diff = 7.23e-08 (tolerance: < 1.00e-01)

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

**Status**: ❌ FAILED

**Test Results**:
- Test 1 - Superset check: ✅ PASSED
- Test 2 - NumRows check: ❌ FAILED (Python has +13.93% rows vs Stata)
- Test 3 - Precision1 check: ✅ PASSED
- Test 4 - Precision2 check: ✅ PASSED
- Test 5 - T-stat check: NA (Skipped for faster execution)

**Observations**:
- Stata:  2,097,471
- Python: 2,389,617
- Common: 2,097,471

**Precision1**: 0.003% obs with std_diff >= 1.00e-02 (tolerance: < 1%)

**Precision2**: 100th percentile diff = 2.87e-07 (tolerance: < 1.00e-01)

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
- Test 1 - Superset check: ✅ PASSED
- Test 2 - NumRows check: ✅ PASSED (Python has -0.25% rows vs Stata)
- Test 3 - Precision1 check: ✅ PASSED
- Test 4 - Precision2 check: ✅ PASSED
- Test 5 - T-stat check: NA (Skipped for faster execution)

**Observations**:
- Stata:  855,113
- Python: 852,949
- Common: 848,962

**Precision1**: 0.042% obs with std_diff >= 1.00e-02 (tolerance: < 1%)

**Precision2**: 100th percentile diff = 4.66e-07 (tolerance: < 1.00e-01)

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
- Test 1 - Superset check: ✅ PASSED
- Test 2 - NumRows check: ✅ PASSED (Python has -0.25% rows vs Stata)
- Test 3 - Precision1 check: ✅ PASSED
- Test 4 - Precision2 check: ✅ PASSED
- Test 5 - T-stat check: NA (Skipped for faster execution)

**Observations**:
- Stata:  843,512
- Python: 841,390
- Common: 837,442

**Precision1**: 0.047% obs with std_diff >= 1.00e-02 (tolerance: < 1%)

**Precision2**: 100th percentile diff = 1.46e-07 (tolerance: < 1.00e-01)

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
- Test 1 - Superset check: ✅ PASSED
- Test 2 - NumRows check: ✅ PASSED (Python has +0.50% rows vs Stata)
- Test 3 - Precision1 check: ✅ PASSED
- Test 4 - Precision2 check: ✅ PASSED
- Test 5 - T-stat check: NA (Skipped for faster execution)

**Observations**:
- Stata:  634,164
- Python: 637,317
- Common: 634,164

**Precision1**: 0.000% obs with std_diff >= 1.00e-02 (tolerance: < 1%)

**Precision2**: 100th percentile diff = 2.77e-07 (tolerance: < 1.00e-01)

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
- Test 1 - Superset check: ✅ PASSED
- Test 2 - NumRows check: ✅ PASSED (Python has +0.85% rows vs Stata)
- Test 3 - Precision1 check: ✅ PASSED
- Test 4 - Precision2 check: ✅ PASSED
- Test 5 - T-stat check: NA (Skipped for faster execution)

**Observations**:
- Stata:  564,785
- Python: 569,589
- Common: 564,785

**Precision1**: 0.001% obs with std_diff >= 1.00e-02 (tolerance: < 1%)

**Precision2**: 100th percentile diff = 6.00e-07 (tolerance: < 1.00e-01)

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

**Status**: ✅ PASSED

**Test Results**:
- Test 1 - Superset check: ✅ PASSED
- Test 2 - NumRows check: ✅ PASSED (Python has +0.01% rows vs Stata)
- Test 3 - Precision1 check: ✅ PASSED
- Test 4 - Precision2 check: ✅ PASSED
- Test 5 - T-stat check: NA (Skipped for faster execution)

**Observations**:
- Stata:  1,243,383
- Python: 1,243,528
- Common: 1,243,383

**Precision1**: 0.186% obs with std_diff >= 1.00e-02 (tolerance: < 1%)

**Precision2**: 100th percentile diff = 1.37e-02 (tolerance: < 1.00e-01)

**Summary Statistics** (Common Observations):

| Statistic  |          Stata |         Python |     Difference | Std Difference |
|------------|----------------|----------------|----------------|----------------|
| count      |       1.24e+06 |       1.24e+06 |       1.24e+06 |       1.24e+06 |
| mean       |       2.37e-10 |       2.76e-05 |       2.76e-05 |       2.78e-05 |
| std        |         0.9941 |         0.9941 |         0.0010 |         0.0010 |
| min        |        -2.3446 |        -2.3446 |        -0.1559 |        -0.1569 |
| 25%        |        -0.6402 |        -0.6402 |      -4.24e-08 |      -4.26e-08 |
| 50%        |        -0.2736 |        -0.2736 |       6.01e-10 |       6.05e-10 |
| 75%        |         0.3358 |         0.3359 |       4.52e-08 |       4.54e-08 |
| max        |        10.1323 |        10.1323 |         0.0870 |         0.0875 |

**Regression Analysis** (Python ~ Stata):

- **Model**: python = 0.0000 + 1.0000 * stata
- **R-squared**: 1.0000
- **N observations**: 1,243,383

| Coefficient |     Estimate |    Std Error | t-statistic |   p-value |
|-------------|--------------|--------------|-------------|----------|
| Intercept   |     2.76e-05 |     9.26e-07 |     29.8506 |     0.000 |
| Slope       |       1.0000 |     9.32e-07 |    1.07e+06 |     0.000 |

**Feedback**:
- Num observations with std_diff >= TOL_DIFF_1: 2310/1243383 (0.186%)
- Stata standard deviation: 9.94e-01

---

### PS

**Status**: ❌ FAILED

**Test Results**:
- Test 1 - Superset check: ✅ PASSED
- Test 2 - NumRows check: ✅ PASSED (Python has +0.06% rows vs Stata)
- Test 3 - Precision1 check: ❌ FAILED
- Test 4 - Precision2 check: ❌ FAILED
- Test 5 - T-stat check: NA (Skipped for faster execution)

**Observations**:
- Stata:  463,944
- Python: 464,239
- Common: 463,941

**Precision1**: 17.931% obs with std_diff >= 1.00e-02 (tolerance: < 1%)

**Precision2**: 100th percentile diff = 2.36e+00 (tolerance: < 1.00e-01)

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

**Largest Differences Before 1950**:
```
No data before 1950
```

---

### PatentsRD

**Status**: ✅ PASSED

**Test Results**:
- Test 1 - Superset check: ✅ PASSED
- Test 2 - NumRows check: ✅ PASSED (Python has +0.61% rows vs Stata)
- Test 3 - Precision1 check: ✅ PASSED
- Test 4 - Precision2 check: ✅ PASSED
- Test 5 - T-stat check: NA (Skipped for faster execution)

**Observations**:
- Stata:  671,832
- Python: 675,912
- Common: 671,580

**Precision1**: 0.055% obs with std_diff >= 1.00e-02 (tolerance: < 1%)

**Precision2**: 100th percentile diff = 0.00e+00 (tolerance: < 1.00e-01)

**Summary Statistics** (Common Observations):

| Statistic  |          Stata |         Python |     Difference | Std Difference |
|------------|----------------|----------------|----------------|----------------|
| count      |    671580.0000 |    671580.0000 |    671580.0000 |    671580.0000 |
| mean       |         0.2099 |         0.2104 |       5.54e-04 |         0.0014 |
| std        |         0.4072 |         0.4076 |         0.0235 |         0.0578 |
| min        |         0.0000 |         0.0000 |         0.0000 |         0.0000 |
| 25%        |         0.0000 |         0.0000 |         0.0000 |         0.0000 |
| 50%        |         0.0000 |         0.0000 |         0.0000 |         0.0000 |
| 75%        |         0.0000 |         0.0000 |         0.0000 |         0.0000 |
| max        |         1.0000 |         1.0000 |         1.0000 |         2.4557 |

**Regression Analysis** (Python ~ Stata):

- **Model**: python = 0.0007 + 0.9993 * stata
- **R-squared**: 0.9967
- **N observations**: 671,580

| Coefficient |     Estimate |    Std Error | t-statistic |   p-value |
|-------------|--------------|--------------|-------------|----------|
| Intercept   |     7.01e-04 |     3.23e-05 |     21.7059 |     0.000 |
| Slope       |       0.9993 |     7.05e-05 |  14174.4527 |     0.000 |

**Feedback**:
- Num observations with std_diff >= TOL_DIFF_1: 372/671580 (0.055%)
- Stata standard deviation: 4.07e-01

---

### PayoutYield

**Status**: ✅ PASSED

**Test Results**:
- Test 1 - Superset check: ✅ PASSED
- Test 2 - NumRows check: ✅ PASSED (Python has +0.01% rows vs Stata)
- Test 3 - Precision1 check: ✅ PASSED
- Test 4 - Precision2 check: ✅ PASSED
- Test 5 - T-stat check: NA (Skipped for faster execution)

**Observations**:
- Stata:  1,419,344
- Python: 1,419,513
- Common: 1,419,344

**Precision1**: 0.000% obs with std_diff >= 1.00e-02 (tolerance: < 1%)

**Precision2**: 100th percentile diff = 2.75e-07 (tolerance: < 1.00e-01)

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
- Test 1 - Superset check: ✅ PASSED
- Test 2 - NumRows check: ✅ PASSED (Python has +0.16% rows vs Stata)
- Test 3 - Precision1 check: ✅ PASSED
- Test 4 - Precision2 check: ✅ PASSED
- Test 5 - T-stat check: NA (Skipped for faster execution)

**Observations**:
- Stata:  3,174,456
- Python: 3,179,478
- Common: 3,174,456

**Precision1**: 0.000% obs with std_diff >= 1.00e-02 (tolerance: < 1%)

**Precision2**: 100th percentile diff = 8.80e-08 (tolerance: < 1.00e-01)

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
- Test 1 - Superset check: ✅ PASSED
- Test 2 - NumRows check: ✅ PASSED (Python has +0.05% rows vs Stata)
- Test 3 - Precision1 check: ✅ PASSED
- Test 4 - Precision2 check: ✅ PASSED
- Test 5 - T-stat check: NA (Skipped for faster execution)

**Observations**:
- Stata:  2,412,359
- Python: 2,413,499
- Common: 2,412,359

**Precision1**: 0.000% obs with std_diff >= 1.00e-02 (tolerance: < 1%)

**Precision2**: 100th percentile diff = 7.22e-08 (tolerance: < 1.00e-01)

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
- Test 1 - Superset check: ✅ PASSED
- Test 2 - NumRows check: ❌ FAILED (Python has +26.63% rows vs Stata)
- Test 3 - Precision1 check: ❌ FAILED
- Test 4 - Precision2 check: ❌ FAILED
- Test 5 - T-stat check: NA (Skipped for faster execution)

**Observations**:
- Stata:  491,508
- Python: 622,380
- Common: 490,188

**Precision1**: 85.268% obs with std_diff >= 1.00e-02 (tolerance: < 1%)

**Precision2**: 100th percentile diff = 3.14e-01 (tolerance: < 1.00e-01)

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

**Largest Differences Before 1950**:
```
No data before 1950
```

---

### Price

**Status**: ✅ PASSED

**Test Results**:
- Test 1 - Superset check: ✅ PASSED
- Test 2 - NumRows check: ✅ PASSED (Python has +0.00% rows vs Stata)
- Test 3 - Precision1 check: ✅ PASSED
- Test 4 - Precision2 check: ✅ PASSED
- Test 5 - T-stat check: NA (Skipped for faster execution)

**Observations**:
- Stata:  4,029,252
- Python: 4,029,252
- Common: 4,029,252

**Precision1**: 0.000% obs with std_diff >= 1.00e-02 (tolerance: < 1%)

**Precision2**: 100th percentile diff = 1.97e-07 (tolerance: < 1.00e-01)

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

**Status**: ❌ FAILED

**Test Results**:
- Test 1 - Superset check: ✅ PASSED
- Test 2 - NumRows check: ✅ PASSED (Python has +0.14% rows vs Stata)
- Test 3 - Precision1 check: ❌ FAILED
- Test 4 - Precision2 check: ❌ FAILED
- Test 5 - T-stat check: NA (Skipped for faster execution)

**Observations**:
- Stata:  4,630,424
- Python: 4,636,840
- Common: 4,630,424

**Precision1**: 1.210% obs with std_diff >= 1.00e-02 (tolerance: < 1%)

**Precision2**: 100th percentile diff = 1.94e+00 (tolerance: < 1.00e-01)

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

**Largest Differences Before 1950**:
```
   permno  yyyymm    python     stata      diff
0   17283  193007  0.995758  0.236111  0.759647
1   17283  193008  0.995758  0.236111  0.759647
2   17283  193009  0.995758  0.236111  0.759647
3   17283  193010  0.995758  0.236111  0.759647
4   17283  193011  0.995758  0.236111  0.759647
5   17283  193012  0.995758  0.236111  0.759647
6   17283  193101  0.995758  0.236111  0.759647
7   17283  193102  0.995758  0.236111  0.759647
8   17283  193103  0.995758  0.236111  0.759647
9   17283  193104  0.995758  0.236111  0.759647
```

---

### PriceDelaySlope

**Status**: ✅ PASSED

**Test Results**:
- Test 1 - Superset check: ✅ PASSED
- Test 2 - NumRows check: ✅ PASSED (Python has +0.14% rows vs Stata)
- Test 3 - Precision1 check: ✅ PASSED
- Test 4 - Precision2 check: ✅ PASSED
- Test 5 - T-stat check: NA (Skipped for faster execution)

**Observations**:
- Stata:  4,630,424
- Python: 4,636,840
- Common: 4,630,424

**Precision1**: 0.582% obs with std_diff >= 1.00e-02 (tolerance: < 1%)

**Precision2**: 100th percentile diff = 7.00e-02 (tolerance: < 1.00e-01)

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

**Status**: ✅ PASSED (with override)

**Override Applied**:
- Reviewed on: 2025-08-14
- Reviewed by: ac
- Details: There was a bug with the Stata code's winsorization. No way to replicate this. There's also a typo in the Stata formula for this. See https://github.com/OpenSourceAP/CrossSection/issues/177

**Test Results**:
- Test 1 - Superset check: ✅ PASSED
- Test 2 - NumRows check: ✅ PASSED (Python has +2.50% rows vs Stata)
- Test 3 - Precision1 check: ❌ FAILED
- Test 4 - Precision2 check: ❌ FAILED
- Test 5 - T-stat check: NA (Skipped for faster execution)

**Observations**:
- Stata:  4,523,656
- Python: 4,636,840
- Common: 4,523,656

**Precision1**: 19.380% obs with std_diff >= 1.00e-02 (tolerance: < 1%)

**Precision2**: 100th percentile diff = 5.70e+00 (tolerance: < 1.00e-01)

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

**Largest Differences Before 1950**:
```
   permno  yyyymm    python     stata       diff
0   17726  194607  6.742584 -3.977883  10.720467
1   17726  194608  6.742584 -3.977883  10.720467
2   17726  194609  6.742584 -3.977883  10.720467
3   17726  194610  6.742584 -3.977883  10.720467
4   17726  194611  6.742584 -3.977883  10.720467
5   17726  194612  6.742584 -3.977883  10.720467
6   17726  194701  6.742584 -3.977883  10.720467
7   17726  194702  6.742584 -3.977883  10.720467
8   17726  194703  6.742584 -3.977883  10.720467
9   17726  194704  6.742584 -3.977883  10.720467
```

---

### ProbInformedTrading

**Status**: ✅ PASSED

**Test Results**:
- Test 1 - Superset check: ✅ PASSED
- Test 2 - NumRows check: ✅ PASSED (Python has +0.00% rows vs Stata)
- Test 3 - Precision1 check: ✅ PASSED
- Test 4 - Precision2 check: ✅ PASSED
- Test 5 - T-stat check: NA (Skipped for faster execution)

**Observations**:
- Stata:  24,028
- Python: 24,028
- Common: 24,028

**Precision1**: 0.000% obs with std_diff >= 1.00e-02 (tolerance: < 1%)

**Precision2**: 100th percentile diff = 5.99e-07 (tolerance: < 1.00e-01)

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
- Test 1 - Superset check: ✅ PASSED
- Test 2 - NumRows check: ✅ PASSED (Python has +0.00% rows vs Stata)
- Test 3 - Precision1 check: ✅ PASSED
- Test 4 - Precision2 check: ✅ PASSED
- Test 5 - T-stat check: NA (Skipped for faster execution)

**Observations**:
- Stata:  1,419,136
- Python: 1,419,157
- Common: 1,419,136

**Precision1**: 0.000% obs with std_diff >= 1.00e-02 (tolerance: < 1%)

**Precision2**: 100th percentile diff = 9.73e-08 (tolerance: < 1.00e-01)

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
- Test 1 - Superset check: ✅ PASSED
- Test 2 - NumRows check: ✅ PASSED (Python has +4.40% rows vs Stata)
- Test 3 - Precision1 check: ❌ FAILED
- Test 4 - Precision2 check: ❌ FAILED
- Test 5 - T-stat check: NA (Skipped for faster execution)

**Observations**:
- Stata:  173,266
- Python: 180,884
- Common: 173,240

**Precision1**: 4.336% obs with std_diff >= 1.00e-02 (tolerance: < 1%)

**Precision2**: 100th percentile diff = 2.17e+00 (tolerance: < 1.00e-01)

**Summary Statistics** (Common Observations):

| Statistic  |          Stata |         Python |     Difference | Std Difference |
|------------|----------------|----------------|----------------|----------------|
| count      |    173240.0000 |    173240.0000 |    173240.0000 |    173240.0000 |
| mean       |         0.4685 |         0.4644 |        -0.0040 |      -7.50e-04 |
| std        |         5.3534 |         5.2908 |         0.7769 |         0.1451 |
| min        |      -170.7315 |      -170.7315 |       -25.1031 |        -4.6892 |
| 25%        |        -0.2961 |        -0.2951 |      -1.56e-07 |      -2.91e-08 |
| 50%        |         0.4038 |         0.4001 |       5.57e-10 |       1.04e-10 |
| 75%        |         1.3891 |         1.3673 |       1.58e-07 |       2.94e-08 |
| max        |        83.8592 |        83.8592 |        35.2219 |         6.5793 |

**Regression Analysis** (Python ~ Stata):

- **Model**: python = 0.0064 + 0.9778 * stata
- **R-squared**: 0.9789
- **N observations**: 173,240

| Coefficient |     Estimate |    Std Error | t-statistic |   p-value |
|-------------|--------------|--------------|-------------|----------|
| Intercept   |       0.0064 |       0.0019 |      3.4395 |     0.001 |
| Slope       |       0.9778 |     3.45e-04 |   2837.9578 |     0.000 |

**Feedback**:
- Num observations with std_diff >= TOL_DIFF_1: 7512/173240 (4.336%)
- Stata standard deviation: 5.35e+00

**Most Recent Bad Observations**:
```
   permno  yyyymm    python     stata      diff
0   14033  202608  0.379405  0.192091  0.187314
1   14033  202607  0.379405  0.192091  0.187314
2   14033  202606  0.379405  0.192091  0.187314
3   14033  202605  0.379405  0.192091  0.187314
4   14245  202605  0.943359  0.997209 -0.053850
5   14432  202605  0.304188  0.448311 -0.144123
6   14668  202605  0.619375  0.359465  0.259910
7   15059  202605  0.805267 -4.663055  5.468322
8   16533  202605 -0.130891 -0.232203  0.101312
9   82670  202605  0.300767  0.394679 -0.093913
```

**Largest Differences**:
```
   permno  yyyymm     python      stata       diff
0   79283  200206 -24.396323 -59.618244  35.221921
1   79283  200207 -24.396323 -59.618244  35.221921
2   79283  200208 -24.396323 -59.618244  35.221921
3   79283  200209 -24.396323 -59.618244  35.221921
4   79283  200210 -24.396323 -59.618244  35.221921
5   79283  200211 -24.396323 -59.618244  35.221921
6   79283  200212 -24.396323 -59.618244  35.221921
7   79283  200301 -24.396323 -59.618244  35.221921
8   79283  200302 -24.396323 -59.618244  35.221921
9   79283  200303 -24.396323 -59.618244  35.221921
```

**Largest Differences Before 1950**:
```
No data before 1950
```

---

### RDS

**Status**: ❌ FAILED

**Test Results**:
- Test 1 - Superset check: ✅ PASSED
- Test 2 - NumRows check: ❌ FAILED (Python has +16.30% rows vs Stata)
- Test 3 - Precision1 check: ✅ PASSED
- Test 4 - Precision2 check: ✅ PASSED
- Test 5 - T-stat check: NA (Skipped for faster execution)

**Observations**:
- Stata:  2,725,375
- Python: 3,169,667
- Common: 2,725,375

**Precision1**: 0.000% obs with std_diff >= 1.00e-02 (tolerance: < 1%)

**Precision2**: 100th percentile diff = 8.65e-08 (tolerance: < 1.00e-01)

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

**Status**: ❌ FAILED

**Test Results**:
- Test 1 - Superset check: ✅ PASSED
- Test 2 - NumRows check: ❌ FAILED (Python has +62.31% rows vs Stata)
- Test 3 - Precision1 check: ✅ PASSED
- Test 4 - Precision2 check: ❌ FAILED
- Test 5 - T-stat check: NA (Skipped for faster execution)

**Observations**:
- Stata:  517,737
- Python: 840,337
- Common: 517,652

**Precision1**: 0.503% obs with std_diff >= 1.00e-02 (tolerance: < 1%)

**Precision2**: 100th percentile diff = 1.87e-01 (tolerance: < 1.00e-01)

**Summary Statistics** (Common Observations):

| Statistic  |          Stata |         Python |     Difference | Std Difference |
|------------|----------------|----------------|----------------|----------------|
| count      |    517652.0000 |    517652.0000 |    517652.0000 |    517652.0000 |
| mean       |         0.2067 |         0.2062 |      -4.55e-04 |      -6.52e-04 |
| std        |         0.6976 |         0.6972 |         0.0119 |         0.0170 |
| min        |        -0.0011 |        -0.0011 |        -3.1795 |        -4.5575 |
| 25%        |         0.0000 |         0.0000 |         0.0000 |         0.0000 |
| 50%        |         0.0000 |         0.0000 |         0.0000 |         0.0000 |
| 75%        |         0.1533 |         0.1526 |         0.0000 |         0.0000 |
| max        |        34.7810 |        34.7810 |       1.32e-06 |       1.90e-06 |

**Regression Analysis** (Python ~ Stata):

- **Model**: python = -0.0003 + 0.9993 * stata
- **R-squared**: 0.9997
- **N observations**: 517,652

| Coefficient |     Estimate |    Std Error | t-statistic |   p-value |
|-------------|--------------|--------------|-------------|----------|
| Intercept   |    -3.08e-04 |     1.72e-05 |    -17.9379 |     0.000 |
| Slope       |       0.9993 |     2.36e-05 |  42364.2386 |     0.000 |

**Feedback**:
- Num observations with std_diff >= TOL_DIFF_1: 2606/517652 (0.503%)
- Stata standard deviation: 6.98e-01

**Most Recent Bad Observations**:
```
   permno  yyyymm    python     stata      diff
0   12789  202310  1.533250  2.233868 -0.700618
1   15791  202309  0.523093  0.565146 -0.042053
2   15791  202302  0.305697  0.353305 -0.047608
3   15791  202301  0.305697  0.353305 -0.047608
4   15791  202212  0.305697  0.353305 -0.047608
5   15791  202211  0.305697  0.353305 -0.047608
6   15791  202210  0.305697  0.353305 -0.047608
7   15791  202209  0.305697  0.353305 -0.047608
8   91366  202209  0.450334  0.490646 -0.040312
9   91366  202208  0.450334  0.490646 -0.040312
```

**Largest Differences**:
```
   permno  yyyymm    python     stata      diff
0   15294  202105  4.068316  7.247835 -3.179518
1   33567  200306  0.595391  1.618097 -1.022706
2   33567  200307  0.595391  1.618097 -1.022706
3   33567  200308  0.595391  1.618097 -1.022706
4   33567  200309  0.595391  1.618097 -1.022706
5   33567  200310  0.595391  1.618097 -1.022706
6   33567  200311  0.595391  1.618097 -1.022706
7   33567  200401  0.595391  1.618097 -1.022706
8   33567  200402  0.595391  1.618097 -1.022706
9   82670  200706  5.749710  6.703712 -0.954003
```

**Largest Differences Before 1950**:
```
No data before 1950
```

---

### REV6

**Status**: ✅ PASSED

**Test Results**:
- Test 1 - Superset check: ✅ PASSED
- Test 2 - NumRows check: ✅ PASSED (Python has +0.05% rows vs Stata)
- Test 3 - Precision1 check: ✅ PASSED
- Test 4 - Precision2 check: ✅ PASSED
- Test 5 - T-stat check: NA (Skipped for faster execution)

**Observations**:
- Stata:  1,762,090
- Python: 1,762,915
- Common: 1,759,158

**Precision1**: 0.164% obs with std_diff >= 1.00e-02 (tolerance: < 1%)

**Precision2**: 100th percentile diff = 1.74e-02 (tolerance: < 1.00e-01)

**Summary Statistics** (Common Observations):

| Statistic  |          Stata |         Python |     Difference | Std Difference |
|------------|----------------|----------------|----------------|----------------|
| count      |       1.76e+06 |       1.76e+06 |       1.76e+06 |       1.76e+06 |
| mean       |        -0.0685 |        -0.0645 |         0.0040 |       6.18e-05 |
| std        |        64.8875 |        65.3849 |         8.3431 |         0.1286 |
| min        |    -58190.5590 |    -58190.5598 |     -3284.2074 |       -50.6138 |
| 25%        |        -0.0119 |        -0.0122 |      -9.71e-10 |      -1.50e-11 |
| 50%        |         0.0016 |         0.0017 |         0.0000 |         0.0000 |
| 75%        |         0.0124 |         0.0126 |       9.70e-10 |       1.49e-11 |
| max        |     32747.2600 |     32748.0882 |      8424.1383 |       129.8267 |

**Regression Analysis** (Python ~ Stata):

- **Model**: python = 0.0040 + 0.9994 * stata
- **R-squared**: 0.9837
- **N observations**: 1,759,158

| Coefficient |     Estimate |    Std Error | t-statistic |   p-value |
|-------------|--------------|--------------|-------------|----------|
| Intercept   |       0.0040 |       0.0063 |      0.6313 |     0.528 |
| Slope       |       0.9994 |     9.69e-05 |  10309.6465 |     0.000 |

**Feedback**:
- Num observations with std_diff >= TOL_DIFF_1: 2888/1759158 (0.164%)
- Stata standard deviation: 6.49e+01

---

### RIO_Disp

**Status**: ❌ FAILED

**Test Results**:
- Test 1 - Superset check: ✅ PASSED
- Test 2 - NumRows check: ✅ PASSED (Python has +0.07% rows vs Stata)
- Test 3 - Precision1 check: ✅ PASSED
- Test 4 - Precision2 check: ❌ FAILED
- Test 5 - T-stat check: NA (Skipped for faster execution)

**Observations**:
- Stata:  497,437
- Python: 497,766
- Common: 496,342

**Precision1**: 0.100% obs with std_diff >= 1.00e-02 (tolerance: < 1%)

**Precision2**: 100th percentile diff = 7.90e-01 (tolerance: < 1.00e-01)

**Summary Statistics** (Common Observations):

| Statistic  |          Stata |         Python |     Difference | Std Difference |
|------------|----------------|----------------|----------------|----------------|
| count      |    496342.0000 |    496342.0000 |    496342.0000 |    496342.0000 |
| mean       |         3.5900 |         3.5910 |       9.95e-04 |       7.86e-04 |
| std        |         1.2664 |         1.2665 |         0.0317 |         0.0250 |
| min        |         1.0000 |         1.0000 |        -1.0000 |        -0.7896 |
| 25%        |         3.0000 |         3.0000 |         0.0000 |         0.0000 |
| 50%        |         4.0000 |         4.0000 |         0.0000 |         0.0000 |
| 75%        |         5.0000 |         5.0000 |         0.0000 |         0.0000 |
| max        |         5.0000 |         5.0000 |         1.0000 |         0.7896 |

**Regression Analysis** (Python ~ Stata):

- **Model**: python = 0.0018 + 0.9998 * stata
- **R-squared**: 0.9994
- **N observations**: 496,342

| Coefficient |     Estimate |    Std Error | t-statistic |   p-value |
|-------------|--------------|--------------|-------------|----------|
| Intercept   |       0.0018 |     1.35e-04 |     13.0919 |     0.000 |
| Slope       |       0.9998 |     3.55e-05 |  28175.7412 |     0.000 |

**Feedback**:
- Num observations with std_diff >= TOL_DIFF_1: 498/496342 (0.100%)
- Stata standard deviation: 1.27e+00

**Most Recent Bad Observations**:
```
   permno  yyyymm  python  stata  diff
0   21563  202412     4.0      3   1.0
1   91910  202412     5.0      4   1.0
2   92597  202411     4.0      3   1.0
3   22758  202406     4.0      3   1.0
4   16630  202405     5.0      4   1.0
5   18937  202405     4.0      3   1.0
6   10382  202403     5.0      4   1.0
7   18572  202403     4.0      3   1.0
8   15291  202401     3.0      2   1.0
9   25590  202401     3.0      2   1.0
```

**Largest Differences**:
```
   permno  yyyymm  python  stata  diff
0   10026  199903     5.0      4   1.0
1   10026  201806     3.0      2   1.0
2   10035  199004     5.0      4   1.0
3   10083  198705     4.0      3   1.0
4   10091  198808     4.0      3   1.0
5   10180  200001     5.0      4   1.0
6   10182  201804     4.0      3   1.0
7   10192  199007     5.0      4   1.0
8   10258  199104     5.0      4   1.0
9   10258  201705     5.0      4   1.0
```

**Largest Differences Before 1950**:
```
No data before 1950
```

---

### RIO_MB

**Status**: ✅ PASSED

**Test Results**:
- Test 1 - Superset check: ✅ PASSED
- Test 2 - NumRows check: ✅ PASSED (Python has +0.09% rows vs Stata)
- Test 3 - Precision1 check: ✅ PASSED
- Test 4 - Precision2 check: ✅ PASSED
- Test 5 - T-stat check: NA (Skipped for faster execution)

**Observations**:
- Stata:  354,170
- Python: 354,474
- Common: 354,047

**Precision1**: 0.089% obs with std_diff >= 1.00e-02 (tolerance: < 1%)

**Precision2**: 100th percentile diff = 0.00e+00 (tolerance: < 1.00e-01)

**Summary Statistics** (Common Observations):

| Statistic  |          Stata |         Python |     Difference | Std Difference |
|------------|----------------|----------------|----------------|----------------|
| count      |    354047.0000 |    354047.0000 |    354047.0000 |    354047.0000 |
| mean       |         2.7904 |         2.7913 |       8.70e-04 |       6.41e-04 |
| std        |         1.3572 |         1.3576 |         0.0299 |         0.0220 |
| min        |         1.0000 |         1.0000 |        -1.0000 |        -0.7368 |
| 25%        |         2.0000 |         2.0000 |         0.0000 |         0.0000 |
| 50%        |         3.0000 |         3.0000 |         0.0000 |         0.0000 |
| 75%        |         4.0000 |         4.0000 |         0.0000 |         0.0000 |
| max        |         5.0000 |         5.0000 |         1.0000 |         0.7368 |

**Regression Analysis** (Python ~ Stata):

- **Model**: python = 0.0008 + 1.0000 * stata
- **R-squared**: 0.9995
- **N observations**: 354,047

| Coefficient |     Estimate |    Std Error | t-statistic |   p-value |
|-------------|--------------|--------------|-------------|----------|
| Intercept   |     7.91e-04 |     1.15e-04 |      6.8901 |     0.000 |
| Slope       |       1.0000 |     3.70e-05 |  27043.8615 |     0.000 |

**Feedback**:
- Num observations with std_diff >= TOL_DIFF_1: 316/354047 (0.089%)
- Stata standard deviation: 1.36e+00

---

### RIO_Turnover

**Status**: ❌ FAILED

**Test Results**:
- Test 1 - Superset check: ✅ PASSED
- Test 2 - NumRows check: ✅ PASSED (Python has +0.10% rows vs Stata)
- Test 3 - Precision1 check: ✅ PASSED
- Test 4 - Precision2 check: ❌ FAILED
- Test 5 - T-stat check: NA (Skipped for faster execution)

**Observations**:
- Stata:  445,546
- Python: 446,011
- Common: 445,391

**Precision1**: 0.132% obs with std_diff >= 1.00e-02 (tolerance: < 1%)

**Precision2**: 100th percentile diff = 7.42e-01 (tolerance: < 1.00e-01)

**Summary Statistics** (Common Observations):

| Statistic  |          Stata |         Python |     Difference | Std Difference |
|------------|----------------|----------------|----------------|----------------|
| count      |    445391.0000 |    445391.0000 |    445391.0000 |    445391.0000 |
| mean       |         3.2511 |         3.2524 |         0.0013 |       9.63e-04 |
| std        |         1.3475 |         1.3479 |         0.0362 |         0.0269 |
| min        |         1.0000 |         1.0000 |        -1.0000 |        -0.7421 |
| 25%        |         2.0000 |         2.0000 |         0.0000 |         0.0000 |
| 50%        |         3.0000 |         3.0000 |         0.0000 |         0.0000 |
| 75%        |         4.0000 |         4.0000 |         0.0000 |         0.0000 |
| max        |         5.0000 |         5.0000 |         1.0000 |         0.7421 |

**Regression Analysis** (Python ~ Stata):

- **Model**: python = 0.0015 + 0.9999 * stata
- **R-squared**: 0.9993
- **N observations**: 445,391

| Coefficient |     Estimate |    Std Error | t-statistic |   p-value |
|-------------|--------------|--------------|-------------|----------|
| Intercept   |       0.0015 |     1.42e-04 |     10.6257 |     0.000 |
| Slope       |       0.9999 |     4.03e-05 |  24807.3346 |     0.000 |

**Feedback**:
- Num observations with std_diff >= TOL_DIFF_1: 586/445391 (0.132%)
- Stata standard deviation: 1.35e+00

**Most Recent Bad Observations**:
```
   permno  yyyymm  python  stata  diff
0   21563  202412     4.0      3   1.0
1   18937  202405     4.0      3   1.0
2   18572  202403     4.0      3   1.0
3   15291  202401     3.0      2   1.0
4   16436  202311     4.0      3   1.0
5   78003  202309     4.0      3   1.0
6   91606  202307     4.0      3   1.0
7   18558  202301     3.0      2   1.0
8   18576  202207     2.0      1   1.0
9   21589  202207     4.0      3   1.0
```

**Largest Differences**:
```
   permno  yyyymm  python  stata  diff
0   10006  195909     4.0      3   1.0
1   10014  196902     5.0      4   1.0
2   10022  192809     5.0      4   1.0
3   10022  192901     5.0      4   1.0
4   10035  199004     5.0      4   1.0
5   10057  193607     5.0      4   1.0
6   10057  193609     5.0      4   1.0
7   10057  194101     4.0      3   1.0
8   10057  195009     5.0      4   1.0
9   10083  198705     4.0      3   1.0
```

**Largest Differences Before 1950**:
```
   permno  yyyymm  python  stata  diff
0   10022  192809     5.0      4   1.0
1   10022  192901     5.0      4   1.0
2   10057  193607     5.0      4   1.0
3   10057  193609     5.0      4   1.0
4   10057  194101     4.0      3   1.0
5   10137  194602     3.0      2   1.0
6   10137  194703     3.0      2   1.0
7   10233  193204     2.0      1   1.0
8   10559  194405     5.0      4   1.0
9   10671  192705     3.0      2   1.0
```

---

### RIO_Volatility

**Status**: ❌ FAILED

**Test Results**:
- Test 1 - Superset check: ❌ FAILED (Python missing 86206 Stata observations)
- Test 2 - NumRows check: ✅ PASSED (Python has -6.07% rows vs Stata)
- Test 3 - Precision1 check: ✅ PASSED
- Test 4 - Precision2 check: ❌ FAILED
- Test 5 - T-stat check: NA (Skipped for faster execution)

**Observations**:
- Stata:  470,062
- Python: 441,513
- Common: 383,856

**Precision1**: 0.144% obs with std_diff >= 1.00e-02 (tolerance: < 1%)

**Precision2**: 100th percentile diff = 7.66e-01 (tolerance: < 1.00e-01)

**Summary Statistics** (Common Observations):

| Statistic  |          Stata |         Python |     Difference | Std Difference |
|------------|----------------|----------------|----------------|----------------|
| count      |    383856.0000 |    383856.0000 |    383856.0000 |    383856.0000 |
| mean       |         3.3935 |         3.3949 |         0.0014 |         0.0011 |
| std        |         1.3056 |         1.3061 |         0.0379 |         0.0290 |
| min        |         1.0000 |         1.0000 |        -1.0000 |        -0.7659 |
| 25%        |         2.0000 |         2.0000 |         0.0000 |         0.0000 |
| 50%        |         4.0000 |         4.0000 |         0.0000 |         0.0000 |
| 75%        |         4.0000 |         4.0000 |         0.0000 |         0.0000 |
| max        |         5.0000 |         5.0000 |         1.0000 |         0.7659 |

**Regression Analysis** (Python ~ Stata):

- **Model**: python = 0.0016 + 1.0000 * stata
- **R-squared**: 0.9992
- **N observations**: 383,856

| Coefficient |     Estimate |    Std Error | t-statistic |   p-value |
|-------------|--------------|--------------|-------------|----------|
| Intercept   |       0.0016 |     1.70e-04 |      9.1372 |     0.000 |
| Slope       |       1.0000 |     4.68e-05 |  21344.5839 |     0.000 |

**Feedback**:
- Num observations with std_diff >= TOL_DIFF_1: 552/383856 (0.144%)
- Stata standard deviation: 1.31e+00

**Most Recent Bad Observations**:
```
   permno  yyyymm  python  stata  diff
0   21563  202412     4.0      3   1.0
1   14045  202410     5.0      4   1.0
2   22758  202406     4.0      3   1.0
3   18937  202405     4.0      3   1.0
4   18572  202403     4.0      3   1.0
5   88264  202401     5.0      4   1.0
6   78003  202309     4.0      3   1.0
7   17357  202305     3.0      2   1.0
8   18561  202305     5.0      4   1.0
9   18558  202301     3.0      2   1.0
```

**Largest Differences**:
```
   permno  yyyymm  python  stata  diff
0   10035  199004     5.0      4   1.0
1   10062  199006     5.0      4   1.0
2   10062  199403     4.0      3   1.0
3   10083  198705     4.0      3   1.0
4   10125  199008     4.0      3   1.0
5   10137  194308     4.0      3   1.0
6   10137  194602     3.0      2   1.0
7   10166  199002     5.0      4   1.0
8   10233  193204     2.0      1   1.0
9   10258  199104     5.0      4   1.0
```

**Largest Differences Before 1950**:
```
   permno  yyyymm  python  stata  diff
0   10137  194308     4.0      3   1.0
1   10137  194602     3.0      2   1.0
2   10233  193204     2.0      1   1.0
3   10284  192910     3.0      2   1.0
4   10559  194405     5.0      4   1.0
5   10591  193704     3.0      2   1.0
6   10671  192705     3.0      2   1.0
7   10698  194503     5.0      4   1.0
8   10823  194908     4.0      3   1.0
9   11148  193810     5.0      4   1.0
```

---

### RIVolSpread

**Status**: ✅ PASSED

**Test Results**:
- Test 1 - Superset check: ✅ PASSED
- Test 2 - NumRows check: ✅ PASSED (Python has -0.27% rows vs Stata)
- Test 3 - Precision1 check: ✅ PASSED
- Test 4 - Precision2 check: ✅ PASSED
- Test 5 - T-stat check: NA (Skipped for faster execution)

**Observations**:
- Stata:  750,937
- Python: 748,931
- Common: 745,589

**Precision1**: 0.051% obs with std_diff >= 1.00e-02 (tolerance: < 1%)

**Precision2**: 100th percentile diff = 8.07e-07 (tolerance: < 1.00e-01)

**Summary Statistics** (Common Observations):

| Statistic  |          Stata |         Python |     Difference | Std Difference |
|------------|----------------|----------------|----------------|----------------|
| count      |    745589.0000 |    745589.0000 |    745589.0000 |    745589.0000 |
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
- **N observations**: 745,589

| Coefficient |     Estimate |    Std Error | t-statistic |   p-value |
|-------------|--------------|--------------|-------------|----------|
| Intercept   |     1.56e-05 |     5.03e-06 |      3.1026 |     0.002 |
| Slope       |       0.9998 |     2.17e-05 |  46137.1191 |     0.000 |

**Feedback**:
- Num observations with std_diff >= TOL_DIFF_1: 381/745589 (0.051%)
- Stata standard deviation: 2.30e-01

---

### RealizedVol

**Status**: ✅ PASSED

**Test Results**:
- Test 1 - Superset check: ✅ PASSED
- Test 2 - NumRows check: ✅ PASSED (Python has -0.13% rows vs Stata)
- Test 3 - Precision1 check: ✅ PASSED
- Test 4 - Precision2 check: ✅ PASSED
- Test 5 - T-stat check: NA (Skipped for faster execution)

**Observations**:
- Stata:  4,987,397
- Python: 4,980,936
- Common: 4,980,936

**Precision1**: 0.000% obs with std_diff >= 1.00e-02 (tolerance: < 1%)

**Precision2**: 100th percentile diff = 2.68e-15 (tolerance: < 1.00e-01)

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

**Status**: ✅ PASSED (with override)

**Override Applied**:
- Reviewed on: 2025-08-20
- Reviewed by: ac
- Details: The do file was using asrol with stat(first) to fill in missing values. This method is not used anywhere else. Also, this method does not work properly. I really don't understand what it's doing See https://github.com/OpenSourceAP/CrossSection/issues/178. 

I wrote Recomm_ShortInterest.py from scratch to fill in the missing values properly. It results in far more observations than the do file. I checked a few of the Stata observations that are missing in Python and they all should be missing. They had ConsRecomm scores of around 3.0, which should not be an extreme quintile and therefore should be dropped.

**Test Results**:
- Test 1 - Superset check: ❌ FAILED (Python missing 21128 Stata observations)
- Test 2 - NumRows check: ❌ FAILED (Python has +39.71% rows vs Stata)
- Test 3 - Precision1 check: ✅ PASSED
- Test 4 - Precision2 check: ✅ PASSED
- Test 5 - T-stat check: NA (Skipped for faster execution)

**Observations**:
- Stata:  34,619
- Python: 48,367
- Common: 13,491

**Precision1**: 0.000% obs with std_diff >= 1.00e-02 (tolerance: < 1%)

**Precision2**: 100th percentile diff = 0.00e+00 (tolerance: < 1.00e-01)

**Summary Statistics** (Common Observations):

| Statistic  |          Stata |         Python |     Difference | Std Difference |
|------------|----------------|----------------|----------------|----------------|
| count      |     13491.0000 |     13491.0000 |     13491.0000 |     13491.0000 |
| mean       |         0.5014 |         0.5014 |         0.0000 |         0.0000 |
| std        |         0.5000 |         0.5000 |         0.0000 |         0.0000 |
| min        |         0.0000 |         0.0000 |         0.0000 |         0.0000 |
| 25%        |         0.0000 |         0.0000 |         0.0000 |         0.0000 |
| 50%        |         1.0000 |         1.0000 |         0.0000 |         0.0000 |
| 75%        |         1.0000 |         1.0000 |         0.0000 |         0.0000 |
| max        |         1.0000 |         1.0000 |         0.0000 |         0.0000 |

**Regression Analysis** (Python ~ Stata):

- **Model**: python = 0.0000 + 1.0000 * stata
- **R-squared**: 1.0000
- **N observations**: 13,491

| Coefficient |     Estimate |    Std Error | t-statistic |   p-value |
|-------------|--------------|--------------|-------------|----------|
| Intercept   |     2.12e-14 |     2.56e-16 |     82.8886 |     0.000 |
| Slope       |       1.0000 |     3.61e-16 |    2.77e+15 |     0.000 |

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
- Num observations with std_diff >= TOL_DIFF_1: 0/13491 (0.000%)
- Stata standard deviation: 5.00e-01

---

### ResidualMomentum

**Status**: ❌ FAILED

**Test Results**:
- Test 1 - Superset check: ✅ PASSED
- Test 2 - NumRows check: ✅ PASSED (Python has +1.72% rows vs Stata)
- Test 3 - Precision1 check: ❌ FAILED
- Test 4 - Precision2 check: ❌ FAILED
- Test 5 - T-stat check: NA (Skipped for faster execution)

**Observations**:
- Stata:  3,458,422
- Python: 3,517,891
- Common: 3,458,422

**Precision1**: 2.854% obs with std_diff >= 1.00e-02 (tolerance: < 1%)

**Precision2**: 100th percentile diff = 9.17e-01 (tolerance: < 1.00e-01)

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

**Most Recent Bad Observations**:
```
   permno  yyyymm    python     stata      diff
0   10028  202412  0.289036  0.283338  0.005699
1   10066  202412  0.502859  0.460886  0.041973
2   10107  202412 -0.795068 -0.786140 -0.008928
3   10252  202412  0.283345  0.277829  0.005516
4   10294  202412 -0.792843 -0.800530  0.007688
5   10308  202412  0.409725  0.405028  0.004697
6   10318  202412 -0.092833 -0.098400  0.005568
7   10397  202412 -0.336479 -0.339856  0.003377
8   10606  202412 -0.643135 -0.647104  0.003969
9   10629  202412  0.348657  0.343000  0.005657
```

**Largest Differences**:
```
   permno  yyyymm    python     stata      diff
0   43880  199301  1.350366 -0.471662  1.822028
1   79490  200801  0.170608 -1.534872  1.705480
2   79490  200712  0.183492 -1.389287  1.572779
3   85570  200801  0.073226  1.565069 -1.491844
4   77893  199012 -1.022008  0.420065 -1.442073
5   79490  200802 -0.083602 -1.520945  1.437344
6   79490  200803  0.000506 -1.406803  1.407309
7   43880  199303  0.941700 -0.449004  1.390704
8   84351  200603 -0.964103  0.425841 -1.389944
9   85570  200712  0.155851  1.525028 -1.369177
```

**Largest Differences Before 1950**:
```
   permno  yyyymm    python     stata      diff
0   13725  193509 -0.456978 -1.085686  0.628708
1   13725  193508 -0.570527 -1.109849  0.539321
2   13725  193506 -0.562432 -1.099878  0.537445
3   13725  193504 -0.451700 -0.988842  0.537142
4   13725  193505 -0.572521 -1.096676  0.524155
5   13725  193507 -0.594041 -1.081490  0.487448
6   13725  193503 -0.363179 -0.843710  0.480531
7   13725  193501 -0.504955 -0.972825  0.467870
8   13725  193502 -0.470708 -0.929486  0.458779
9   13725  193512 -0.732965 -1.179525  0.446559
```

---

### ReturnSkew

**Status**: ✅ PASSED

**Test Results**:
- Test 1 - Superset check: ✅ PASSED
- Test 2 - NumRows check: ✅ PASSED (Python has +0.00% rows vs Stata)
- Test 3 - Precision1 check: ✅ PASSED
- Test 4 - Precision2 check: ✅ PASSED
- Test 5 - T-stat check: NA (Skipped for faster execution)

**Observations**:
- Stata:  4,952,730
- Python: 4,952,730
- Common: 4,952,730

**Precision1**: 0.000% obs with std_diff >= 1.00e-02 (tolerance: < 1%)

**Precision2**: 100th percentile diff = 5.42e-15 (tolerance: < 1.00e-01)

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

**Status**: ❌ FAILED

**Test Results**:
- Test 1 - Superset check: ✅ PASSED
- Test 2 - NumRows check: ✅ PASSED (Python has +0.03% rows vs Stata)
- Test 3 - Precision1 check: ❌ FAILED
- Test 4 - Precision2 check: ❌ FAILED
- Test 5 - T-stat check: NA (Skipped for faster execution)

**Observations**:
- Stata:  4,978,948
- Python: 4,980,592
- Common: 4,978,741

**Precision1**: 2.575% obs with std_diff >= 1.00e-02 (tolerance: < 1%)

**Precision2**: 100th percentile diff = 1.40e+00 (tolerance: < 1.00e-01)

**Summary Statistics** (Common Observations):

| Statistic  |          Stata |         Python |     Difference | Std Difference |
|------------|----------------|----------------|----------------|----------------|
| count      |       4.98e+06 |       4.98e+06 |       4.98e+06 |       4.98e+06 |
| mean       |         0.1540 |         0.1536 |      -4.19e-04 |      -4.93e-04 |
| std        |         0.8499 |         0.8487 |         0.0940 |         0.1106 |
| min        |        -4.8206 |        -4.8206 |        -8.7287 |       -10.2706 |
| 25%        |        -0.2811 |        -0.2808 |      -2.22e-15 |      -2.61e-15 |
| 50%        |         0.1296 |         0.1295 |         0.0000 |         0.0000 |
| 75%        |         0.5701 |         0.5700 |       2.22e-15 |       2.61e-15 |
| max        |         4.7150 |         4.7150 |         5.1167 |         6.0205 |

**Regression Analysis** (Python ~ Stata):

- **Model**: python = 0.0007 + 0.9925 * stata
- **R-squared**: 0.9878
- **N observations**: 4,978,741

| Coefficient |     Estimate |    Std Error | t-statistic |   p-value |
|-------------|--------------|--------------|-------------|----------|
| Intercept   |     7.32e-04 |     4.27e-05 |     17.1416 |     0.000 |
| Slope       |       0.9925 |     4.95e-05 |  20063.9485 |     0.000 |

**Feedback**:
- Num observations with std_diff >= TOL_DIFF_1: 128182/4978741 (2.575%)
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

**Largest Differences Before 1950**:
```
   permno  yyyymm    python     stata      diff
0   10284  193108 -0.043656 -4.694855  4.651200
1   15632  192904 -0.366716 -4.800000  4.433284
2   15923  193809  0.684782  4.694855 -4.010073
3   20431  194502 -4.129483 -0.185154 -3.944329
4   11738  192802 -0.664669 -4.364358  3.699689
5   15923  194208  0.000000  3.175426 -3.175426
6   15632  192903 -1.812385 -4.587317  2.774932
7   21717  194307  1.559323 -1.205178  2.764501
8   10903  193303  0.000000  2.715344 -2.715344
9   13899  193303  0.000000  2.715344 -2.715344
```

---

### RevenueSurprise

**Status**: ✅ PASSED

**Test Results**:
- Test 1 - Superset check: ✅ PASSED
- Test 2 - NumRows check: ✅ PASSED (Python has +0.00% rows vs Stata)
- Test 3 - Precision1 check: ✅ PASSED
- Test 4 - Precision2 check: ✅ PASSED
- Test 5 - T-stat check: NA (Skipped for faster execution)

**Observations**:
- Stata:  2,107,489
- Python: 2,107,507
- Common: 2,107,434

**Precision1**: 0.009% obs with std_diff >= 1.00e-02 (tolerance: < 1%)

**Precision2**: 100th percentile diff = 2.28e-04 (tolerance: < 1.00e-01)

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
- Test 1 - Superset check: ✅ PASSED
- Test 2 - NumRows check: ✅ PASSED (Python has +0.03% rows vs Stata)
- Test 3 - Precision1 check: ✅ PASSED
- Test 4 - Precision2 check: ✅ PASSED
- Test 5 - T-stat check: NA (Skipped for faster execution)

**Observations**:
- Stata:  3,527,662
- Python: 3,528,790
- Common: 3,527,662

**Precision1**: 0.000% obs with std_diff >= 1.00e-02 (tolerance: < 1%)

**Precision2**: 100th percentile diff = 2.30e-08 (tolerance: < 1.00e-01)

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
- Test 1 - Superset check: ✅ PASSED
- Test 2 - NumRows check: ✅ PASSED (Python has +0.00% rows vs Stata)
- Test 3 - Precision1 check: ✅ PASSED
- Test 4 - Precision2 check: ✅ PASSED
- Test 5 - T-stat check: NA (Skipped for faster execution)

**Observations**:
- Stata:  3,030,926
- Python: 3,030,928
- Common: 3,030,926

**Precision1**: 0.000% obs with std_diff >= 1.00e-02 (tolerance: < 1%)

**Precision2**: 100th percentile diff = 2.63e-07 (tolerance: < 1.00e-01)

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
- Test 1 - Superset check: ✅ PASSED
- Test 2 - NumRows check: ✅ PASSED (Python has +0.00% rows vs Stata)
- Test 3 - Precision1 check: ✅ PASSED
- Test 4 - Precision2 check: ✅ PASSED
- Test 5 - T-stat check: NA (Skipped for faster execution)

**Observations**:
- Stata:  4,047,630
- Python: 4,047,630
- Common: 4,047,630

**Precision1**: 0.000% obs with std_diff >= 1.00e-02 (tolerance: < 1%)

**Precision2**: 100th percentile diff = 1.62e-07 (tolerance: < 1.00e-01)

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
- Test 1 - Superset check: ✅ PASSED
- Test 2 - NumRows check: ✅ PASSED (Python has +0.00% rows vs Stata)
- Test 3 - Precision1 check: ✅ PASSED
- Test 4 - Precision2 check: ✅ PASSED
- Test 5 - T-stat check: NA (Skipped for faster execution)

**Observations**:
- Stata:  3,517,326
- Python: 3,517,326
- Common: 3,517,326

**Precision1**: 0.000% obs with std_diff >= 1.00e-02 (tolerance: < 1%)

**Precision2**: 100th percentile diff = 7.53e-10 (tolerance: < 1.00e-01)

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
- Test 1 - Superset check: ✅ PASSED
- Test 2 - NumRows check: ✅ PASSED (Python has +0.00% rows vs Stata)
- Test 3 - Precision1 check: ✅ PASSED
- Test 4 - Precision2 check: ✅ PASSED
- Test 5 - T-stat check: NA (Skipped for faster execution)

**Observations**:
- Stata:  2,507,320
- Python: 2,507,320
- Common: 2,507,320

**Precision1**: 0.000% obs with std_diff >= 1.00e-02 (tolerance: < 1%)

**Precision2**: 100th percentile diff = 7.63e-10 (tolerance: < 1.00e-01)

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
- Test 1 - Superset check: ✅ PASSED
- Test 2 - NumRows check: ✅ PASSED (Python has +0.03% rows vs Stata)
- Test 3 - Precision1 check: ✅ PASSED
- Test 4 - Precision2 check: ✅ PASSED
- Test 5 - T-stat check: NA (Skipped for faster execution)

**Observations**:
- Stata:  3,624,363
- Python: 3,625,491
- Common: 3,624,363

**Precision1**: 0.002% obs with std_diff >= 1.00e-02 (tolerance: < 1%)

**Precision2**: 100th percentile diff = 0.00e+00 (tolerance: < 1.00e-01)

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
- Test 1 - Superset check: ✅ PASSED
- Test 2 - NumRows check: ✅ PASSED (Python has +0.06% rows vs Stata)
- Test 3 - Precision1 check: ✅ PASSED
- Test 4 - Precision2 check: ✅ PASSED
- Test 5 - T-stat check: NA (Skipped for faster execution)

**Observations**:
- Stata:  1,660,340
- Python: 1,661,295
- Common: 1,660,340

**Precision1**: 0.000% obs with std_diff >= 1.00e-02 (tolerance: < 1%)

**Precision2**: 100th percentile diff = 0.00e+00 (tolerance: < 1.00e-01)

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
- Test 1 - Superset check: ✅ PASSED
- Test 2 - NumRows check: ✅ PASSED (Python has +0.00% rows vs Stata)
- Test 3 - Precision1 check: ✅ PASSED
- Test 4 - Precision2 check: ✅ PASSED
- Test 5 - T-stat check: NA (Skipped for faster execution)

**Observations**:
- Stata:  873,175
- Python: 873,182
- Common: 873,175

**Precision1**: 0.000% obs with std_diff >= 1.00e-02 (tolerance: < 1%)

**Precision2**: 100th percentile diff = 8.99e-08 (tolerance: < 1.00e-01)

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
- Test 1 - Superset check: ✅ PASSED
- Test 2 - NumRows check: ✅ PASSED (Python has +0.00% rows vs Stata)
- Test 3 - Precision1 check: ✅ PASSED
- Test 4 - Precision2 check: ✅ PASSED
- Test 5 - T-stat check: NA (Skipped for faster execution)

**Observations**:
- Stata:  4,029,130
- Python: 4,029,130
- Common: 4,029,130

**Precision1**: 0.000% obs with std_diff >= 1.00e-02 (tolerance: < 1%)

**Precision2**: 100th percentile diff = 2.14e-07 (tolerance: < 1.00e-01)

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
- Test 1 - Superset check: ✅ PASSED
- Test 2 - NumRows check: ✅ PASSED (Python has -0.26% rows vs Stata)
- Test 3 - Precision1 check: ✅ PASSED
- Test 4 - Precision2 check: ✅ PASSED
- Test 5 - T-stat check: NA (Skipped for faster execution)

**Observations**:
- Stata:  862,230
- Python: 859,994
- Common: 856,084

**Precision1**: 0.038% obs with std_diff >= 1.00e-02 (tolerance: < 1%)

**Precision2**: 100th percentile diff = 4.20e-07 (tolerance: < 1.00e-01)

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
- Test 1 - Superset check: ✅ PASSED
- Test 2 - NumRows check: ✅ PASSED (Python has +0.00% rows vs Stata)
- Test 3 - Precision1 check: ✅ PASSED
- Test 4 - Precision2 check: ✅ PASSED
- Test 5 - T-stat check: NA (Skipped for faster execution)

**Observations**:
- Stata:  4,047,630
- Python: 4,047,630
- Common: 4,047,630

**Precision1**: 0.000% obs with std_diff >= 1.00e-02 (tolerance: < 1%)

**Precision2**: 100th percentile diff = 0.00e+00 (tolerance: < 1.00e-01)

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
- Test 1 - Superset check: ✅ PASSED
- Test 2 - NumRows check: ✅ PASSED (Python has +0.47% rows vs Stata)
- Test 3 - Precision1 check: ✅ PASSED
- Test 4 - Precision2 check: ✅ PASSED
- Test 5 - T-stat check: NA (Skipped for faster execution)

**Observations**:
- Stata:  1,545,193
- Python: 1,552,503
- Common: 1,545,193

**Precision1**: 0.005% obs with std_diff >= 1.00e-02 (tolerance: < 1%)

**Precision2**: 100th percentile diff = 0.00e+00 (tolerance: < 1.00e-01)

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
- Test 1 - Superset check: ✅ PASSED
- Test 2 - NumRows check: ✅ PASSED (Python has +0.05% rows vs Stata)
- Test 3 - Precision1 check: ✅ PASSED
- Test 4 - Precision2 check: ✅ PASSED
- Test 5 - T-stat check: NA (Skipped for faster execution)

**Observations**:
- Stata:  3,211,651
- Python: 3,213,292
- Common: 3,211,651

**Precision1**: 0.357% obs with std_diff >= 1.00e-02 (tolerance: < 1%)

**Precision2**: 100th percentile diff = 5.26e-02 (tolerance: < 1.00e-01)

**Summary Statistics** (Common Observations):

| Statistic  |          Stata |         Python |     Difference | Std Difference |
|------------|----------------|----------------|----------------|----------------|
| count      |       3.21e+06 |       3.21e+06 |       3.21e+06 |       3.21e+06 |
| mean       |         1.1689 |         1.1693 |       4.25e-04 |       2.23e-05 |
| std        |        19.0252 |        19.0298 |         0.4189 |         0.0220 |
| min        |     -2742.5000 |     -2742.5000 |        -1.0000 |        -0.0526 |
| 25%        |         0.0341 |         0.0303 |      -1.62e-08 |      -8.52e-10 |
| 50%        |         1.0000 |         1.0000 |         0.0000 |         0.0000 |
| 75%        |         1.4267 |         1.4286 |       3.68e-11 |       1.93e-12 |
| max        |      4463.7114 |      4463.7113 |       193.2381 |        10.1570 |

**Regression Analysis** (Python ~ Stata):

- **Model**: python = 0.0004 + 1.0000 * stata
- **R-squared**: 0.9995
- **N observations**: 3,211,651

| Coefficient |     Estimate |    Std Error | t-statistic |   p-value |
|-------------|--------------|--------------|-------------|----------|
| Intercept   |     4.25e-04 |     2.34e-04 |      1.8150 |     0.070 |
| Slope       |       1.0000 |     1.23e-05 |  81391.9534 |     0.000 |

**Feedback**:
- Num observations with std_diff >= TOL_DIFF_1: 11460/3211651 (0.357%)
- Stata standard deviation: 1.90e+01

---

### TotalAccruals

**Status**: ✅ PASSED

**Test Results**:
- Test 1 - Superset check: ✅ PASSED
- Test 2 - NumRows check: ✅ PASSED (Python has +0.51% rows vs Stata)
- Test 3 - Precision1 check: ✅ PASSED
- Test 4 - Precision2 check: ✅ PASSED
- Test 5 - T-stat check: NA (Skipped for faster execution)

**Observations**:
- Stata:  3,141,468
- Python: 3,157,365
- Common: 3,141,468

**Precision1**: 0.001% obs with std_diff >= 1.00e-02 (tolerance: < 1%)

**Precision2**: 100th percentile diff = 2.28e-07 (tolerance: < 1.00e-01)

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
- Test 1 - Superset check: ✅ PASSED
- Test 2 - NumRows check: ✅ PASSED (Python has +0.00% rows vs Stata)
- Test 3 - Precision1 check: ❌ FAILED
- Test 4 - Precision2 check: ❌ FAILED
- Test 5 - T-stat check: NA (Skipped for faster execution)

**Observations**:
- Stata:  2,058,231
- Python: 2,058,231
- Common: 2,058,231

**Precision1**: 25.129% obs with std_diff >= 1.00e-02 (tolerance: < 1%)

**Precision2**: 100th percentile diff = 9.08e-01 (tolerance: < 1.00e-01)

**Summary Statistics** (Common Observations):

| Statistic  |          Stata |         Python |     Difference | Std Difference |
|------------|----------------|----------------|----------------|----------------|
| count      |       2.06e+06 |       2.06e+06 |       2.06e+06 |       2.06e+06 |
| mean       |         0.2096 |         0.2089 |      -7.75e-04 |        -0.0050 |
| std        |         0.1540 |         0.1547 |         0.0237 |         0.1539 |
| min        |        -1.0711 |        -1.0711 |        -0.2349 |        -1.5251 |
| 25%        |         0.1242 |         0.1256 |      -4.61e-08 |      -2.99e-07 |
| 50%        |         0.2187 |         0.2184 |       1.35e-09 |       8.77e-09 |
| 75%        |         0.3000 |         0.2978 |       5.79e-08 |       3.76e-07 |
| max        |         3.2757 |         3.2757 |         0.3254 |         2.1131 |

**Regression Analysis** (Python ~ Stata):

- **Model**: python = 0.0007 + 0.9927 * stata
- **R-squared**: 0.9766
- **N observations**: 2,058,231

| Coefficient |     Estimate |    Std Error | t-statistic |   p-value |
|-------------|--------------|--------------|-------------|----------|
| Intercept   |     7.48e-04 |     2.79e-05 |     26.8560 |     0.000 |
| Slope       |       0.9927 |     1.07e-04 |   9267.5981 |     0.000 |

**Feedback**:
- Num observations with std_diff >= TOL_DIFF_1: 517211/2058231 (25.129%)
- Stata standard deviation: 1.54e-01

**Most Recent Bad Observations**:
```
   permno  yyyymm    python     stata      diff
0   10026  202412 -0.085958  0.032569 -0.118526
1   10032  202412 -0.081422  0.035968 -0.117390
2   10104  202412 -0.083346  0.034036 -0.117382
3   10107  202412 -0.082053  0.038111 -0.120163
4   10138  202412 -0.080283  0.037830 -0.118113
5   10145  202412 -0.082692  0.036421 -0.119112
6   10158  202412 -0.084249  0.032967 -0.117216
7   10200  202412 -0.082381  0.036853 -0.119233
8   10220  202412 -0.086329  0.030636 -0.116965
9   10252  202412 -0.083978  0.033475 -0.117454
```

**Largest Differences**:
```
   permno  yyyymm    python     stata      diff
0   90505  200811 -0.040092 -0.365492  0.325401
1   90505  200812  0.192350 -0.085925  0.278276
2   82775  200811 -0.058161 -0.301578  0.243417
3   14328  202407 -0.051984  0.182878 -0.234862
4   16280  193306  1.259595  1.030139  0.229456
5   82775  200810 -0.030812 -0.259940  0.229129
6   13442  193209  1.082268  0.867052  0.215216
7   75175  200807 -0.192257 -0.406882  0.214625
8   11236  193212  0.931366  0.723557  0.207809
9   51043  200808 -0.114697 -0.316233  0.201536
```

**Largest Differences Before 1950**:
```
   permno  yyyymm    python     stata      diff
0   16280  193306  1.259595  1.030139  0.229456
1   13442  193209  1.082268  0.867052  0.215216
2   11236  193212  0.931366  0.723557  0.207809
3   13864  193210  0.987406  0.790193  0.197213
4   11252  193210  0.853703  0.660276  0.193427
5   24512  193208  0.623597  0.430485  0.193113
6   13426  193304  0.887916  0.697897  0.190020
7   24512  193209  0.828814  0.641206  0.187608
8   13864  193212  0.814815  0.628115  0.186700
9   14509  193211  1.110083  0.929206  0.180877
```

---

### UpRecomm

**Status**: ✅ PASSED

**Test Results**:
- Test 1 - Superset check: ✅ PASSED
- Test 2 - NumRows check: ✅ PASSED (Python has +0.05% rows vs Stata)
- Test 3 - Precision1 check: ✅ PASSED
- Test 4 - Precision2 check: ✅ PASSED
- Test 5 - T-stat check: NA (Skipped for faster execution)

**Observations**:
- Stata:  463,983
- Python: 464,223
- Common: 462,936

**Precision1**: 0.023% obs with std_diff >= 1.00e-02 (tolerance: < 1%)

**Precision2**: 100th percentile diff = 0.00e+00 (tolerance: < 1.00e-01)

**Summary Statistics** (Common Observations):

| Statistic  |          Stata |         Python |     Difference | Std Difference |
|------------|----------------|----------------|----------------|----------------|
| count      |    462936.0000 |    462936.0000 |    462936.0000 |    462936.0000 |
| mean       |         0.3514 |         0.3514 |         0.0000 |         0.0000 |
| std        |         0.4774 |         0.4774 |         0.0151 |         0.0317 |
| min        |         0.0000 |         0.0000 |        -1.0000 |        -2.0946 |
| 25%        |         0.0000 |         0.0000 |         0.0000 |         0.0000 |
| 50%        |         0.0000 |         0.0000 |         0.0000 |         0.0000 |
| 75%        |         1.0000 |         1.0000 |         0.0000 |         0.0000 |
| max        |         1.0000 |         1.0000 |         1.0000 |         2.0946 |

**Regression Analysis** (Python ~ Stata):

- **Model**: python = 0.0002 + 0.9995 * stata
- **R-squared**: 0.9990
- **N observations**: 462,936

| Coefficient |     Estimate |    Std Error | t-statistic |   p-value |
|-------------|--------------|--------------|-------------|----------|
| Intercept   |     1.77e-04 |     2.76e-05 |      6.3929 |     0.000 |
| Slope       |       0.9995 |     4.66e-05 |  21458.7276 |     0.000 |

**Feedback**:
- Num observations with std_diff >= TOL_DIFF_1: 106/462936 (0.023%)
- Stata standard deviation: 4.77e-01

---

### VarCF

**Status**: ❌ FAILED

**Test Results**:
- Test 1 - Superset check: ❌ FAILED (Python missing 703349 Stata observations)
- Test 2 - NumRows check: ✅ PASSED (Python has -27.61% rows vs Stata)
- Test 3 - Precision1 check: ✅ PASSED
- Test 4 - Precision2 check: ✅ PASSED
- Test 5 - T-stat check: NA (Skipped for faster execution)

**Observations**:
- Stata:  2,547,003
- Python: 1,843,654
- Common: 1,843,654

**Precision1**: 0.000% obs with std_diff >= 1.00e-02 (tolerance: < 1%)

**Precision2**: 100th percentile diff = 4.00e-08 (tolerance: < 1.00e-01)

**Summary Statistics** (Common Observations):

| Statistic  |          Stata |         Python |     Difference | Std Difference |
|------------|----------------|----------------|----------------|----------------|
| count      |       1.84e+06 |       1.84e+06 |       1.84e+06 |       1.84e+06 |
| mean       |         0.8103 |         0.8103 |      -4.20e-09 |      -7.85e-11 |
| std        |        53.4588 |        53.4588 |       2.61e-05 |       4.88e-07 |
| min        |       1.04e-07 |       1.04e-07 |        -0.0179 |      -3.34e-04 |
| 25%        |       6.16e-04 |       6.16e-04 |      -5.67e-11 |      -1.06e-12 |
| 50%        |         0.0024 |         0.0024 |       1.68e-14 |       3.14e-16 |
| 75%        |         0.0122 |         0.0122 |       5.71e-11 |       1.07e-12 |
| max        |     19048.1760 |     19048.1751 |         0.0038 |       7.18e-05 |

**Regression Analysis** (Python ~ Stata):

- **Model**: python = 0.0000 + 1.0000 * stata
- **R-squared**: 1.0000
- **N observations**: 1,843,654

| Coefficient |     Estimate |    Std Error | t-statistic |   p-value |
|-------------|--------------|--------------|-------------|----------|
| Intercept   |     4.13e-08 |     1.91e-08 |      2.1665 |     0.030 |
| Slope       |       1.0000 |     3.57e-10 |    2.80e+09 |     0.000 |

**Feedback**:
- Num observations with std_diff >= TOL_DIFF_1: 0/1843654 (0.000%)
- Stata standard deviation: 5.35e+01

---

### VolMkt

**Status**: ✅ PASSED

**Test Results**:
- Test 1 - Superset check: ✅ PASSED
- Test 2 - NumRows check: ✅ PASSED (Python has -0.00% rows vs Stata)
- Test 3 - Precision1 check: ✅ PASSED
- Test 4 - Precision2 check: ✅ PASSED
- Test 5 - T-stat check: NA (Skipped for faster execution)

**Observations**:
- Stata:  4,359,237
- Python: 4,359,149
- Common: 4,358,313

**Precision1**: 0.008% obs with std_diff >= 1.00e-02 (tolerance: < 1%)

**Precision2**: 100th percentile diff = 2.22e-05 (tolerance: < 1.00e-01)

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
- Test 1 - Superset check: ✅ PASSED
- Test 2 - NumRows check: ✅ PASSED (Python has -0.00% rows vs Stata)
- Test 3 - Precision1 check: ✅ PASSED
- Test 4 - Precision2 check: ✅ PASSED
- Test 5 - T-stat check: NA (Skipped for faster execution)

**Observations**:
- Stata:  3,922,498
- Python: 3,922,399
- Common: 3,921,598

**Precision1**: 0.010% obs with std_diff >= 1.00e-02 (tolerance: < 1%)

**Precision2**: 100th percentile diff = 1.53e-04 (tolerance: < 1.00e-01)

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

**Status**: ❌ FAILED

**Test Results**:
- Test 1 - Superset check: ✅ PASSED
- Test 2 - NumRows check: ✅ PASSED (Python has +0.58% rows vs Stata)
- Test 3 - Precision1 check: ✅ PASSED
- Test 4 - Precision2 check: ❌ FAILED
- Test 5 - T-stat check: NA (Skipped for faster execution)

**Observations**:
- Stata:  3,655,889
- Python: 3,677,088
- Common: 3,654,259

**Precision1**: 0.963% obs with std_diff >= 1.00e-02 (tolerance: < 1%)

**Precision2**: 100th percentile diff = 1.54e+00 (tolerance: < 1.00e-01)

**Summary Statistics** (Common Observations):

| Statistic  |          Stata |         Python |     Difference | Std Difference |
|------------|----------------|----------------|----------------|----------------|
| count      |       3.65e+06 |       3.65e+06 |       3.65e+06 |       3.65e+06 |
| mean       |         0.0057 |         0.0057 |       3.66e-05 |         0.0018 |
| std        |         0.0207 |         0.0207 |         0.0018 |         0.0887 |
| min        |        -0.0566 |        -0.0565 |        -0.0651 |        -3.1500 |
| 25%        |        -0.0068 |        -0.0069 |      -2.24e-10 |      -1.09e-08 |
| 50%        |         0.0052 |         0.0052 |       1.42e-13 |       6.85e-12 |
| 75%        |         0.0184 |         0.0185 |       2.28e-10 |       1.10e-08 |
| max        |         0.0664 |         0.0670 |         0.1157 |         5.5949 |

**Regression Analysis** (Python ~ Stata):

- **Model**: python = 0.0000 + 0.9992 * stata
- **R-squared**: 0.9922
- **N observations**: 3,654,259

| Coefficient |     Estimate |    Std Error | t-statistic |   p-value |
|-------------|--------------|--------------|-------------|----------|
| Intercept   |     4.09e-05 |     9.95e-07 |     41.0827 |     0.000 |
| Slope       |       0.9992 |     4.64e-05 |  21542.2771 |     0.000 |

**Feedback**:
- Num observations with std_diff >= TOL_DIFF_1: 35207/3654259 (0.963%)
- Stata standard deviation: 2.07e-02

**Most Recent Bad Observations**:
```
   permno  yyyymm    python     stata      diff
0   10066  202412 -0.042738 -0.007268 -0.035470
1   11379  202412 -0.036342 -0.014016 -0.022326
2   13563  202412 -0.019177 -0.051617  0.032440
3   13878  202412 -0.002076 -0.044578  0.042502
4   14051  202412 -0.046306 -0.042498 -0.003808
5   15294  202412 -0.046056 -0.022408 -0.023648
6   15793  202412 -0.000766  0.004212 -0.004977
7   16086  202412 -0.048928 -0.015011 -0.033916
8   16376  202412 -0.012123 -0.005404 -0.006719
9   16787  202412 -0.037732 -0.028771 -0.008961
```

**Largest Differences**:
```
   permno  yyyymm    python     stata      diff
0   83622  201706  0.063452 -0.052244  0.115697
1   83622  201707  0.059125 -0.050653  0.109778
2   11161  200602  0.053628 -0.054415  0.108043
3   27204  201810  0.060988 -0.047022  0.108011
4   27204  201811  0.060954 -0.045956  0.106910
5   76188  199212  0.054548 -0.050417  0.104965
6   27204  201812  0.060880 -0.043556  0.104436
7   11236  193311  0.047995 -0.056055  0.104049
8   12221  200002  0.052244 -0.051749  0.103993
9   91893  201812  0.045865 -0.056252  0.102117
```

**Largest Differences Before 1950**:
```
   permno  yyyymm    python     stata      diff
0   11236  193311  0.047995 -0.056055  0.104049
1   12204  193601  0.034243 -0.043529  0.077773
2   12204  193602  0.038615 -0.035225  0.073840
3   11236  193402  0.043748 -0.029915  0.073663
4   11236  193405  0.038874 -0.033670  0.072544
5   11236  193406  0.035866 -0.035042  0.070907
6   11236  193403  0.038988 -0.030381  0.069369
7   12204  193512  0.015191 -0.051513  0.066704
8   11236  193404  0.034604 -0.030765  0.065369
9   11180  193309  0.009934 -0.054339  0.064272
```

---

### XFIN

**Status**: ✅ PASSED

**Test Results**:
- Test 1 - Superset check: ✅ PASSED
- Test 2 - NumRows check: ✅ PASSED (Python has +0.04% rows vs Stata)
- Test 3 - Precision1 check: ✅ PASSED
- Test 4 - Precision2 check: ✅ PASSED
- Test 5 - T-stat check: NA (Skipped for faster execution)

**Observations**:
- Stata:  3,022,290
- Python: 3,023,466
- Common: 3,022,290

**Precision1**: 0.002% obs with std_diff >= 1.00e-02 (tolerance: < 1%)

**Precision2**: 100th percentile diff = 1.62e-07 (tolerance: < 1.00e-01)

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
- Test 1 - Superset check: ✅ PASSED
- Test 2 - NumRows check: ✅ PASSED (Python has +1.22% rows vs Stata)
- Test 3 - Precision1 check: ✅ PASSED
- Test 4 - Precision2 check: ✅ PASSED
- Test 5 - T-stat check: NA (Skipped for faster execution)

**Observations**:
- Stata:  3,510,758
- Python: 3,553,481
- Common: 3,510,758

**Precision1**: 0.041% obs with std_diff >= 1.00e-02 (tolerance: < 1%)

**Precision2**: 100th percentile diff = 6.41e-03 (tolerance: < 1.00e-01)

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
- Test 1 - Superset check: ✅ PASSED
- Test 2 - NumRows check: ✅ PASSED (Python has +0.04% rows vs Stata)
- Test 3 - Precision1 check: ✅ PASSED
- Test 4 - Precision2 check: ✅ PASSED
- Test 5 - T-stat check: NA (Skipped for faster execution)

**Observations**:
- Stata:  2,613,997
- Python: 2,614,930
- Common: 2,613,997

**Precision1**: 0.000% obs with std_diff >= 1.00e-02 (tolerance: < 1%)

**Precision2**: 100th percentile diff = 1.83e-07 (tolerance: < 1.00e-01)

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
- Test 1 - Superset check: ✅ PASSED
- Test 2 - NumRows check: ✅ PASSED (Python has -0.08% rows vs Stata)
- Test 3 - Precision1 check: ✅ PASSED
- Test 4 - Precision2 check: ✅ PASSED
- Test 5 - T-stat check: NA (Skipped for faster execution)

**Observations**:
- Stata:  851,720
- Python: 851,001
- Common: 845,632

**Precision1**: 0.037% obs with std_diff >= 1.00e-02 (tolerance: < 1%)

**Precision2**: 100th percentile diff = 3.45e-07 (tolerance: < 1.00e-01)

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
- Test 1 - Superset check: ✅ PASSED
- Test 2 - NumRows check: ✅ PASSED (Python has +0.03% rows vs Stata)
- Test 3 - Precision1 check: ✅ PASSED
- Test 4 - Precision2 check: ✅ PASSED
- Test 5 - T-stat check: NA (Skipped for faster execution)

**Observations**:
- Stata:  3,194,445
- Python: 3,195,426
- Common: 3,194,445

**Precision1**: 0.005% obs with std_diff >= 1.00e-02 (tolerance: < 1%)

**Precision2**: 100th percentile diff = 2.53e-07 (tolerance: < 1.00e-01)

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
- Test 1 - Superset check: ✅ PASSED
- Test 2 - NumRows check: ✅ PASSED (Python has -0.08% rows vs Stata)
- Test 3 - Precision1 check: ✅ PASSED
- Test 4 - Precision2 check: ✅ PASSED
- Test 5 - T-stat check: NA (Skipped for faster execution)

**Observations**:
- Stata:  851,720
- Python: 851,001
- Common: 845,632

**Precision1**: 0.042% obs with std_diff >= 1.00e-02 (tolerance: < 1%)

**Precision2**: 100th percentile diff = 3.79e-07 (tolerance: < 1.00e-01)

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
- Test 1 - Superset check: ✅ PASSED
- Test 2 - NumRows check: ✅ PASSED (Python has -0.08% rows vs Stata)
- Test 3 - Precision1 check: ✅ PASSED
- Test 4 - Precision2 check: ✅ PASSED
- Test 5 - T-stat check: NA (Skipped for faster execution)

**Observations**:
- Stata:  851,720
- Python: 851,001
- Common: 845,632

**Precision1**: 0.042% obs with std_diff >= 1.00e-02 (tolerance: < 1%)

**Precision2**: 100th percentile diff = 3.75e-07 (tolerance: < 1.00e-01)

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
- Test 1 - Superset check: ✅ PASSED
- Test 2 - NumRows check: ✅ PASSED (Python has -0.02% rows vs Stata)
- Test 3 - Precision1 check: ✅ PASSED
- Test 4 - Precision2 check: ✅ PASSED
- Test 5 - T-stat check: NA (Skipped for faster execution)

**Observations**:
- Stata:  875,784
- Python: 875,652
- Common: 873,864

**Precision1**: 0.069% obs with std_diff >= 1.00e-02 (tolerance: < 1%)

**Precision2**: 100th percentile diff = 3.22e-07 (tolerance: < 1.00e-01)

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
- Test 1 - Superset check: ✅ PASSED
- Test 2 - NumRows check: ✅ PASSED (Python has +0.14% rows vs Stata)
- Test 3 - Precision1 check: ✅ PASSED
- Test 4 - Precision2 check: ✅ PASSED
- Test 5 - T-stat check: NA (Skipped for faster execution)

**Observations**:
- Stata:  2,425,711
- Python: 2,429,220
- Common: 2,407,796

**Precision1**: 0.042% obs with std_diff >= 1.00e-02 (tolerance: < 1%)

**Precision2**: 100th percentile diff = 2.73e-03 (tolerance: < 1.00e-01)

**Summary Statistics** (Common Observations):

| Statistic  |          Stata |         Python |     Difference | Std Difference |
|------------|----------------|----------------|----------------|----------------|
| count      |       2.41e+06 |       2.41e+06 |       2.41e+06 |       2.41e+06 |
| mean       |         3.7290 |         3.4938 |        -0.2352 |      -5.96e-04 |
| std        |       394.4922 |       367.2597 |       144.0547 |         0.3652 |
| min        |     -9061.0000 |     -9061.0000 |    -91202.9468 |      -231.1908 |
| 25%        |        -0.3587 |        -0.3588 |      -9.08e-09 |      -2.30e-11 |
| 50%        |         0.1307 |         0.1308 |         0.0000 |         0.0000 |
| 75%        |         0.8916 |         0.8918 |       9.27e-09 |       2.35e-11 |
| max        |    141782.2000 |    141782.2000 |      1490.2660 |         3.7777 |

**Regression Analysis** (Python ~ Stata):

- **Model**: python = 0.2619 + 0.8667 * stata
- **R-squared**: 0.8667
- **N observations**: 2,407,796

| Coefficient |     Estimate |    Std Error | t-statistic |   p-value |
|-------------|--------------|--------------|-------------|----------|
| Intercept   |       0.2619 |       0.0864 |      3.0306 |     0.002 |
| Slope       |       0.8667 |     2.19e-04 |   3955.8852 |     0.000 |

**Feedback**:
- Num observations with std_diff >= TOL_DIFF_1: 1014/2407796 (0.042%)
- Stata standard deviation: 3.94e+02

---

### grcapx3y

**Status**: ✅ PASSED

**Test Results**:
- Test 1 - Superset check: ✅ PASSED
- Test 2 - NumRows check: ✅ PASSED (Python has +0.91% rows vs Stata)
- Test 3 - Precision1 check: ✅ PASSED
- Test 4 - Precision2 check: ✅ PASSED
- Test 5 - T-stat check: NA (Skipped for faster execution)

**Observations**:
- Stata:  2,214,095
- Python: 2,234,287
- Common: 2,197,378

**Precision1**: 0.000% obs with std_diff >= 1.00e-02 (tolerance: < 1%)

**Precision2**: 100th percentile diff = 9.32e-20 (tolerance: < 1.00e-01)

**Summary Statistics** (Common Observations):

| Statistic  |          Stata |         Python |     Difference | Std Difference |
|------------|----------------|----------------|----------------|----------------|
| count      |       2.20e+06 |       2.20e+06 |       2.20e+06 |       2.20e+06 |
| mean       |      -4.24e+10 |      -4.24e+10 |      -553.6178 |      -1.23e-11 |
| std        |       4.50e+13 |       4.50e+13 |    248482.1794 |       5.52e-09 |
| min        |      -2.57e+16 |      -2.57e+16 |      -1.92e+08 |      -4.27e-06 |
| 25%        |         0.6523 |         0.6522 |      -1.95e-08 |      -4.32e-22 |
| 50%        |         1.0687 |         1.0686 |         0.0000 |         0.0000 |
| 75%        |         1.6003 |         1.6003 |       1.93e-08 |       4.28e-22 |
| max        |       1.44e+16 |       1.44e+16 |       1.50e+07 |       3.34e-07 |

**Regression Analysis** (Python ~ Stata):

- **Model**: python = -513.4838 + 1.0000 * stata
- **R-squared**: 1.0000
- **N observations**: 2,197,378

| Coefficient |     Estimate |    Std Error | t-statistic |   p-value |
|-------------|--------------|--------------|-------------|----------|
| Intercept   |    -513.4838 |     165.2024 |     -3.1082 |     0.002 |
| Slope       |       1.0000 |     3.67e-12 |    2.72e+11 |     0.000 |

**Feedback**:
- Num observations with std_diff >= TOL_DIFF_1: 0/2197378 (0.000%)
- Stata standard deviation: 4.50e+13

---

### hire

**Status**: ✅ PASSED

**Test Results**:
- Test 1 - Superset check: ✅ PASSED
- Test 2 - NumRows check: ✅ PASSED (Python has +0.03% rows vs Stata)
- Test 3 - Precision1 check: ✅ PASSED
- Test 4 - Precision2 check: ✅ PASSED
- Test 5 - T-stat check: NA (Skipped for faster execution)

**Observations**:
- Stata:  3,496,899
- Python: 3,498,027
- Common: 3,496,899

**Precision1**: 0.008% obs with std_diff >= 1.00e-02 (tolerance: < 1%)

**Precision2**: 100th percentile diff = 3.02e-07 (tolerance: < 1.00e-01)

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
- Test 1 - Superset check: ✅ PASSED
- Test 2 - NumRows check: ✅ PASSED (Python has +0.00% rows vs Stata)
- Test 3 - Precision1 check: ✅ PASSED
- Test 4 - Precision2 check: ✅ PASSED
- Test 5 - T-stat check: NA (Skipped for faster execution)

**Observations**:
- Stata:  1,637,670
- Python: 1,637,670
- Common: 1,637,670

**Precision1**: 0.034% obs with std_diff >= 1.00e-02 (tolerance: < 1%)

**Precision2**: 100th percentile diff = 5.03e-03 (tolerance: < 1.00e-01)

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
- Test 1 - Superset check: ✅ PASSED
- Test 2 - NumRows check: ✅ PASSED (Python has +0.00% rows vs Stata)
- Test 3 - Precision1 check: ✅ PASSED
- Test 4 - Precision2 check: ✅ PASSED
- Test 5 - T-stat check: NA (Skipped for faster execution)

**Observations**:
- Stata:  1,639,842
- Python: 1,639,842
- Common: 1,639,842

**Precision1**: 0.016% obs with std_diff >= 1.00e-02 (tolerance: < 1%)

**Precision2**: 100th percentile diff = 2.03e-03 (tolerance: < 1.00e-01)

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
- Test 1 - Superset check: ✅ PASSED
- Test 2 - NumRows check: ✅ PASSED (Python has +0.00% rows vs Stata)
- Test 3 - Precision1 check: ✅ PASSED
- Test 4 - Precision2 check: ✅ PASSED
- Test 5 - T-stat check: NA (Skipped for faster execution)

**Observations**:
- Stata:  1,448,154
- Python: 1,448,163
- Common: 1,448,154

**Precision1**: 0.040% obs with std_diff >= 1.00e-02 (tolerance: < 1%)

**Precision2**: 100th percentile diff = 1.74e-03 (tolerance: < 1.00e-01)

**Summary Statistics** (Common Observations):

| Statistic  |          Stata |         Python |     Difference | Std Difference |
|------------|----------------|----------------|----------------|----------------|
| count      |       1.45e+06 |       1.45e+06 |       1.45e+06 |       1.45e+06 |
| mean       |      -9.58e-12 |       2.30e-06 |       2.30e-06 |       9.29e-06 |
| std        |         0.2476 |         0.2476 |       8.33e-05 |       3.37e-04 |
| min        |        -1.6407 |        -1.6407 |      -2.22e-06 |      -8.96e-06 |
| 25%        |        -0.1188 |        -0.1188 |      -7.42e-09 |      -3.00e-08 |
| 50%        |        -0.0155 |        -0.0155 |       5.02e-12 |       2.03e-11 |
| 75%        |         0.0987 |         0.0987 |       7.52e-09 |       3.04e-08 |
| max        |        56.9154 |        56.9154 |         0.0043 |         0.0172 |

**Regression Analysis** (Python ~ Stata):

- **Model**: python = 0.0000 + 1.0000 * stata
- **R-squared**: 1.0000
- **N observations**: 1,448,154

| Coefficient |     Estimate |    Std Error | t-statistic |   p-value |
|-------------|--------------|--------------|-------------|----------|
| Intercept   |     2.30e-06 |     6.93e-08 |     33.2092 |     0.000 |
| Slope       |       1.0000 |     2.80e-07 |    3.57e+06 |     0.000 |

**Feedback**:
- Num observations with std_diff >= TOL_DIFF_1: 576/1448154 (0.040%)
- Stata standard deviation: 2.48e-01

---

### retConglomerate

**Status**: ✅ PASSED

**Test Results**:
- Test 1 - Superset check: ✅ PASSED
- Test 2 - NumRows check: ✅ PASSED (Python has +0.15% rows vs Stata)
- Test 3 - Precision1 check: ✅ PASSED
- Test 4 - Precision2 check: ✅ PASSED
- Test 5 - T-stat check: NA (Skipped for faster execution)

**Observations**:
- Stata:  758,394
- Python: 759,500
- Common: 758,382

**Precision1**: 0.886% obs with std_diff >= 1.00e-02 (tolerance: < 1%)

**Precision2**: 100th percentile diff = 7.59e-02 (tolerance: < 1.00e-01)

**Summary Statistics** (Common Observations):

| Statistic  |          Stata |         Python |     Difference | Std Difference |
|------------|----------------|----------------|----------------|----------------|
| count      |    758382.0000 |    758382.0000 |    758382.0000 |    758382.0000 |
| mean       |         0.0106 |         0.0106 |      -7.20e-06 |      -8.56e-05 |
| std        |         0.0841 |         0.0840 |       8.36e-04 |         0.0099 |
| min        |        -0.8000 |        -0.8000 |        -0.1242 |        -1.4774 |
| 25%        |        -0.0313 |        -0.0313 |      -2.78e-17 |      -3.30e-16 |
| 50%        |         0.0105 |         0.0105 |         0.0000 |         0.0000 |
| 75%        |         0.0495 |         0.0495 |       2.78e-17 |       3.30e-16 |
| max        |         4.3779 |         4.3779 |         0.1480 |         1.7604 |

**Regression Analysis** (Python ~ Stata):

- **Model**: python = -0.0000 + 0.9999 * stata
- **R-squared**: 0.9999
- **N observations**: 758,382

| Coefficient |     Estimate |    Std Error | t-statistic |   p-value |
|-------------|--------------|--------------|-------------|----------|
| Intercept   |    -6.07e-06 |     9.68e-07 |     -6.2667 |     0.000 |
| Slope       |       0.9999 |     1.14e-05 |  87522.5577 |     0.000 |

**Feedback**:
- Num observations with std_diff >= TOL_DIFF_1: 6723/758382 (0.886%)
- Stata standard deviation: 8.41e-02

---

### roaq

**Status**: ❌ FAILED

**Test Results**:
- Test 1 - Superset check: ✅ PASSED
- Test 2 - NumRows check: ❌ FAILED (Python has +8.99% rows vs Stata)
- Test 3 - Precision1 check: ✅ PASSED
- Test 4 - Precision2 check: ✅ PASSED
- Test 5 - T-stat check: NA (Skipped for faster execution)

**Observations**:
- Stata:  2,490,858
- Python: 2,714,774
- Common: 2,490,858

**Precision1**: 0.007% obs with std_diff >= 1.00e-02 (tolerance: < 1%)

**Precision2**: 100th percentile diff = 9.62e-08 (tolerance: < 1.00e-01)

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
- Test 1 - Superset check: ✅ PASSED
- Test 2 - NumRows check: ✅ PASSED (Python has +0.00% rows vs Stata)
- Test 3 - Precision1 check: ✅ PASSED
- Test 4 - Precision2 check: ✅ PASSED
- Test 5 - T-stat check: NA (Skipped for faster execution)

**Observations**:
- Stata:  611,076
- Python: 611,100
- Common: 609,876

**Precision1**: 0.022% obs with std_diff >= 1.00e-02 (tolerance: < 1%)

**Precision2**: 100th percentile diff = 4.38e-08 (tolerance: < 1.00e-01)

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
- Test 1 - Superset check: ✅ PASSED
- Test 2 - NumRows check: ✅ PASSED (Python has +0.21% rows vs Stata)
- Test 3 - Precision1 check: ✅ PASSED
- Test 4 - Precision2 check: ✅ PASSED
- Test 5 - T-stat check: NA (Skipped for faster execution)

**Observations**:
- Stata:  233,503
- Python: 233,996
- Common: 233,503

**Precision1**: 0.010% obs with std_diff >= 1.00e-02 (tolerance: < 1%)

**Precision2**: 100th percentile diff = 0.00e+00 (tolerance: < 1.00e-01)

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
- Test 1 - Superset check: ✅ PASSED
- Test 2 - NumRows check: ✅ PASSED (Python has -0.21% rows vs Stata)
- Test 3 - Precision1 check: ✅ PASSED
- Test 4 - Precision2 check: ✅ PASSED
- Test 5 - T-stat check: NA (Skipped for faster execution)

**Observations**:
- Stata:  473,447
- Python: 472,444
- Common: 470,063

**Precision1**: 0.043% obs with std_diff >= 1.00e-02 (tolerance: < 1%)

**Precision2**: 100th percentile diff = 3.63e-07 (tolerance: < 1.00e-01)

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
- Test 1 - Superset check: ✅ PASSED
- Test 2 - NumRows check: ✅ PASSED (Python has +1.58% rows vs Stata)
- Test 3 - Precision1 check: ✅ PASSED
- Test 4 - Precision2 check: ✅ PASSED
- Test 5 - T-stat check: NA (Skipped for faster execution)

**Observations**:
- Stata:  2,166,584
- Python: 2,200,763
- Common: 2,166,204

**Precision1**: 0.000% obs with std_diff >= 1.00e-02 (tolerance: < 1%)

**Precision2**: 100th percentile diff = 1.03e-07 (tolerance: < 1.00e-01)

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
- Test 1 - Superset check: ✅ PASSED
- Test 2 - NumRows check: ✅ PASSED (Python has +0.03% rows vs Stata)
- Test 3 - Precision1 check: ✅ PASSED
- Test 4 - Precision2 check: ✅ PASSED
- Test 5 - T-stat check: NA (Skipped for faster execution)

**Observations**:
- Stata:  1,517,431
- Python: 1,517,875
- Common: 1,517,107

**Precision1**: 0.002% obs with std_diff >= 1.00e-02 (tolerance: < 1%)

**Precision2**: 100th percentile diff = 4.82e-07 (tolerance: < 1.00e-01)

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
- Test 1 - Superset check: ✅ PASSED
- Test 2 - NumRows check: ✅ PASSED (Python has +0.05% rows vs Stata)
- Test 3 - Precision1 check: ✅ PASSED
- Test 4 - Precision2 check: ✅ PASSED
- Test 5 - T-stat check: NA (Skipped for faster execution)

**Observations**:
- Stata:  4,342,889
- Python: 4,345,044
- Common: 4,342,889

**Precision1**: 0.000% obs with std_diff >= 1.00e-02 (tolerance: < 1%)

**Precision2**: 100th percentile diff = 2.61e-07 (tolerance: < 1.00e-01)

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
- Test 1 - Superset check: ✅ PASSED
- Test 2 - NumRows check: ✅ PASSED (Python has +0.06% rows vs Stata)
- Test 3 - Precision1 check: ✅ PASSED
- Test 4 - Precision2 check: ✅ PASSED
- Test 5 - T-stat check: NA (Skipped for faster execution)

**Observations**:
- Stata:  4,680,231
- Python: 4,682,859
- Common: 4,680,231

**Precision1**: 0.000% obs with std_diff >= 1.00e-02 (tolerance: < 1%)

**Precision2**: 100th percentile diff = 2.83e-07 (tolerance: < 1.00e-01)

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
- Test 1 - Superset check: ✅ PASSED
- Test 2 - NumRows check: ✅ PASSED (Python has +0.05% rows vs Stata)
- Test 3 - Precision1 check: ✅ PASSED
- Test 4 - Precision2 check: ✅ PASSED
- Test 5 - T-stat check: NA (Skipped for faster execution)

**Observations**:
- Stata:  4,530,678
- Python: 4,533,091
- Common: 4,530,678

**Precision1**: 0.000% obs with std_diff >= 1.00e-02 (tolerance: < 1%)

**Precision2**: 100th percentile diff = 2.78e-07 (tolerance: < 1.00e-01)

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
- Test 1 - Superset check: ❌ FAILED (Python missing 0 Stata observations)
- Test 2 - NumRows check: ❌ FAILED
- Test 3 - Precision1 check: ❌ FAILED
- Test 4 - Precision2 check: ❌ FAILED
- Test 5 - T-stat check: NA

**Observations**:
- Stata:  0
- Python: 353,486
- Common: 0

---

### IndIPO

**Status**: ❌ FAILED

**Test Results**:
- Test 1 - Superset check: ❌ FAILED (Python missing 0 Stata observations)
- Test 2 - NumRows check: ❌ FAILED
- Test 3 - Precision1 check: ❌ FAILED
- Test 4 - Precision2 check: ❌ FAILED
- Test 5 - T-stat check: NA

**Observations**:
- Stata:  0
- Python: 4,047,630
- Common: 0

---

### RDIPO

**Status**: ❌ FAILED

**Test Results**:
- Test 1 - Superset check: ❌ FAILED (Python missing 0 Stata observations)
- Test 2 - NumRows check: ❌ FAILED
- Test 3 - Precision1 check: ❌ FAILED
- Test 4 - Precision2 check: ❌ FAILED
- Test 5 - T-stat check: NA

**Observations**:
- Stata:  0
- Python: 3,625,491
- Common: 0

---

