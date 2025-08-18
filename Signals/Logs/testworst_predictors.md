# Scripts That Failed Any Test

**Generated**: 2025-08-17 13:03:40

**Scripts that failed superset test** (Python missing Stata observations):

CitationsRD Mom6mJunk Recomm_ShortInterest ZZ1_RIO_MB_RIO_Disp_RIO_Turnover_RIO_Volatility 

**Scripts that failed other tests** (but passed superset):

CredRatDG DivInit DivSeason EarnSupBig HerfAsset Investment MS PS RDAbility TrendFactor VolumeTrend ZZ0_RealizedVol_IdioVol3F_ReturnSkew3F ZZ1_OrgCap_OrgCapNoAdj ZZ1_RIO_MB_RIO_Disp_RIO_Turnover_RIO_Volatility ZZ1_ResidualMomentum6m_ResidualMomentum ZZ2_AbnormalAccruals_AbnormalAccrualsPercent ZZ2_BetaFP ZZ2_PriceDelaySlope_PriceDelayRsq_PriceDelayTstat 

## Detailed Analysis

This section focuses on the 20 worst predictors by Superset and Precision1 metrics.

## Worst Superset

Predictors with highest superset failure rates (Python missing the most Stata observations):

- **Recomm_ShortInterest**
  - Script: Recomm_ShortInterest
  - Python CSV: yes
  - Superset: no (47.99%) ❌
  - Precision1: yes (0.00%)
  - Precision2: yes (99.900th diff 0.0E+00)

- **Mom6mJunk**
  - Script: Mom6mJunk
  - Python CSV: yes
  - Superset: no (18.09%) ❌
  - Precision1: yes (0.28%)
  - Precision2: no (99.900th diff 5.8E-01) ❌

- **CitationsRD**
  - Script: CitationsRD
  - Python CSV: yes
  - Superset: no (4.69%) ❌
  - Precision1: no (6.16%) ❌
  - Precision2: no (99.900th diff 2.4E+00) ❌

- **RIO_Volatility**
  - Script: ZZ1_RIO_MB_RIO_Disp_RIO_Turnover_RIO_Volatility
  - Python CSV: yes
  - Superset: no (1.86%) ❌
  - Precision1: yes (0.14%)
  - Precision2: no (99.900th diff 7.5E-01) ❌

- **AM**
  - Script: AM
  - Python CSV: yes
  - Superset: yes (100%)
  - Precision1: yes (0.00%)
  - Precision2: yes (99.900th diff 1.5E-07)

- **AOP**
  - Script: ZZ1_AnalystValue_AOP_PredictedFE_IntrinsicValue
  - Python CSV: yes
  - Superset: yes (100%)
  - Precision1: yes (0.00%)
  - Precision2: yes (99.900th diff 8.0E-05)

- **AbnormalAccruals**
  - Script: ZZ2_AbnormalAccruals_AbnormalAccrualsPercent
  - Python CSV: yes
  - Superset: yes (100%)
  - Precision1: no (27.95%) ❌
  - Precision2: no (99.900th diff 1.0E+00) ❌

- **Accruals**
  - Script: Accruals
  - Python CSV: yes
  - Superset: yes (100%)
  - Precision1: yes (0.01%)
  - Precision2: yes (99.900th diff 2.4E-07)

- **AccrualsBM**
  - Script: AccrualsBM
  - Python CSV: yes
  - Superset: yes (100%)
  - Precision1: yes (0.00%)
  - Precision2: yes (99.900th diff 0.0E+00)

- **Activism1**
  - Script: ZZ1_Activism1_Activism2
  - Python CSV: yes
  - Superset: yes (100%)
  - Precision1: yes (0.00%)
  - Precision2: yes (99.900th diff 0.0E+00)

- **Activism2**
  - Script: ZZ1_Activism1_Activism2
  - Python CSV: yes
  - Superset: yes (100%)
  - Precision1: yes (0.00%)
  - Precision2: yes (99.900th diff 2.4E-07)

- **AdExp**
  - Script: AdExp
  - Python CSV: yes
  - Superset: yes (100%)
  - Precision1: yes (0.00%)
  - Precision2: yes (99.900th diff 2.7E-07)

- **AnalystRevision**
  - Script: AnalystRevision
  - Python CSV: yes
  - Superset: yes (100%)
  - Precision1: yes (0.04%)
  - Precision2: yes (99.900th diff 1.4E-07)

- **AnalystValue**
  - Script: ZZ1_AnalystValue_AOP_PredictedFE_IntrinsicValue
  - Python CSV: yes
  - Superset: yes (100%)
  - Precision1: yes (0.26%)
  - Precision2: yes (99.900th diff 3.1E-02)

- **AnnouncementReturn**
  - Script: ZZ2_AnnouncementReturn
  - Python CSV: yes
  - Superset: yes (100%)
  - Precision1: yes (0.00%)
  - Precision2: yes (99.900th diff 9.7E-04)

- **AssetGrowth**
  - Script: AssetGrowth
  - Python CSV: yes
  - Superset: yes (100%)
  - Precision1: yes (0.00%)
  - Precision2: yes (99.900th diff 1.3E-07)

- **BM**
  - Script: BM
  - Python CSV: yes
  - Superset: yes (100%)
  - Precision1: yes (0.03%)
  - Precision2: yes (99.900th diff 2.2E-07)

- **BMdec**
  - Script: BMdec
  - Python CSV: yes
  - Superset: yes (100%)
  - Precision1: yes (0.00%)
  - Precision2: yes (99.900th diff 3.1E-07)

- **BPEBM**
  - Script: ZZ1_EBM_BPEBM
  - Python CSV: yes
  - Superset: yes (100%)
  - Precision1: yes (0.00%)
  - Precision2: yes (99.900th diff 2.2E-06)

- **Beta**
  - Script: Beta
  - Python CSV: yes
  - Superset: yes (100%)
  - Precision1: yes (0.00%)
  - Precision2: yes (99.900th diff 1.9E-07)

## Worst Precision1

Predictors with highest precision1 failure rates (highest percentage of observations with significant differences):

- **TrendFactor**
  - Script: TrendFactor
  - Python CSV: yes
  - Superset: yes (100%)
  - Precision1: no (97.14%) ❌
  - Precision2: no (99.900th diff 2.9E+00) ❌

- **PredictedFE**
  - Script: ZZ1_AnalystValue_AOP_PredictedFE_IntrinsicValue
  - Python CSV: yes
  - Superset: yes (100%)
  - Precision1: no (85.27%) ❌
  - Precision2: no (99.900th diff 3.1E-01) ❌

- **AbnormalAccruals**
  - Script: ZZ2_AbnormalAccruals_AbnormalAccrualsPercent
  - Python CSV: yes
  - Superset: yes (100%)
  - Precision1: no (27.95%) ❌
  - Precision2: no (99.900th diff 1.0E+00) ❌

- **MS**
  - Script: MS
  - Python CSV: yes
  - Superset: yes (100%)
  - Precision1: no (19.57%) ❌
  - Precision2: no (99.900th diff 2.6E+00) ❌

- **PriceDelayTstat**
  - Script: ZZ2_PriceDelaySlope_PriceDelayRsq_PriceDelayTstat
  - Python CSV: yes
  - Superset: yes (100%)
  - Precision1: no (19.38%) ❌
  - Precision2: no (99.900th diff 5.7E+00) ❌

- **PS**
  - Script: PS
  - Python CSV: yes
  - Superset: yes (100%)
  - Precision1: no (17.93%) ❌
  - Precision2: no (99.900th diff 2.4E+00) ❌

- **RDAbility**
  - Script: RDAbility
  - Python CSV: yes
  - Superset: yes (100%)
  - Precision1: no (10.90%) ❌
  - Precision2: no (99.900th diff 4.2E+00) ❌

- **OrgCap**
  - Script: ZZ1_OrgCap_OrgCapNoAdj
  - Python CSV: yes
  - Superset: yes (100%)
  - Precision1: no (8.87%) ❌
  - Precision2: no (99.900th diff 3.6E-01) ❌

- **BetaFP**
  - Script: ZZ2_BetaFP
  - Python CSV: yes
  - Superset: yes (100%)
  - Precision1: no (6.26%) ❌
  - Precision2: no (99.900th diff 8.8E-01) ❌

- **CitationsRD**
  - Script: CitationsRD
  - Python CSV: yes
  - Superset: no (4.69%) ❌
  - Precision1: no (6.16%) ❌
  - Precision2: no (99.900th diff 2.4E+00) ❌

- **ResidualMomentum**
  - Script: ZZ1_ResidualMomentum6m_ResidualMomentum
  - Python CSV: yes
  - Superset: yes (100%)
  - Precision1: no (2.85%) ❌
  - Precision2: no (99.900th diff 9.2E-01) ❌

- **ReturnSkew3F**
  - Script: ZZ0_RealizedVol_IdioVol3F_ReturnSkew3F
  - Python CSV: yes
  - Superset: yes (100%)
  - Precision1: no (2.57%) ❌
  - Precision2: no (99.900th diff 1.4E+00) ❌

- **PriceDelayRsq**
  - Script: ZZ2_PriceDelaySlope_PriceDelayRsq_PriceDelayTstat
  - Python CSV: yes
  - Superset: yes (100%)
  - Precision1: no (1.21%) ❌
  - Precision2: no (99.900th diff 1.9E+00) ❌

- **DivSeason**
  - Script: DivSeason
  - Python CSV: yes
  - Superset: yes (100%)
  - Precision1: yes (0.99%)
  - Precision2: no (99.900th diff 2.0E+00) ❌

- **VolumeTrend**
  - Script: VolumeTrend
  - Python CSV: yes
  - Superset: yes (100%)
  - Precision1: yes (0.96%)
  - Precision2: no (99.900th diff 1.5E+00) ❌

- **CredRatDG**
  - Script: CredRatDG
  - Python CSV: yes
  - Superset: yes (100%)
  - Precision1: yes (0.94%)
  - Precision2: no (99.900th diff 6.6E+00) ❌

- **retConglomerate**
  - Script: retConglomerate
  - Python CSV: yes
  - Superset: yes (100%)
  - Precision1: yes (0.89%)
  - Precision2: yes (99.900th diff 7.6E-02)

- **HerfAsset**
  - Script: HerfAsset
  - Python CSV: yes
  - Superset: yes (100%)
  - Precision1: yes (0.66%)
  - Precision2: no (99.900th diff 2.3E-01) ❌

- **PriceDelaySlope**
  - Script: ZZ2_PriceDelaySlope_PriceDelayRsq_PriceDelayTstat
  - Python CSV: yes
  - Superset: yes (100%)
  - Precision1: yes (0.58%)
  - Precision2: yes (99.900th diff 7.0E-02)

- **Tax**
  - Script: Tax
  - Python CSV: yes
  - Superset: yes (100%)
  - Precision1: yes (0.36%)
  - Precision2: yes (99.900th diff 5.3E-02)

