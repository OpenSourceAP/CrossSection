# Scripts That Failed Any Test

**Generated**: 2025-08-14 19:55:31

**Scripts that failed superset test** (Python missing Stata observations):

DownRecomm Mom6mJunk MomRev PatentsRD RDAbility Recomm_ShortInterest UpRecomm 

**Scripts that failed other tests** (but passed superset):

BetaTailRisk ChForecastAccrual CitationsRD CredRatDG DivSeason EarnSupBig Herf HerfAsset IndMom IndRetBig Investment MRreversal MS Mom12mOffSeason MomOffSeason MomOffSeason06YrPlus MomOffSeason11YrPlus MomOffSeason16YrPlus MomVol NumEarnIncrease PS Tax TrendFactor VolumeTrend realestate retConglomerate 

## Detailed Analysis

This section focuses on the 20 worst predictors by Superset and Precision1 metrics.

## Worst Superset

Predictors with highest superset failure rates (Python missing the most Stata observations):

- **Recomm_ShortInterest**
  - Script: Recomm_ShortInterest
  - Python CSV: yes
  - Superset: no (57.03%) ❌
  - Precision1: yes (0.00%)
  - Precision2: yes (99.900th diff 0.0E+00)

- **PatentsRD**
  - Script: PatentsRD
  - Python CSV: yes
  - Superset: no (21.05%) ❌
  - Precision1: yes (0.02%)
  - Precision2: yes (99.900th diff 0.0E+00)

- **Mom6mJunk**
  - Script: Mom6mJunk
  - Python CSV: yes
  - Superset: no (18.09%) ❌
  - Precision1: yes (0.28%)
  - Precision2: no (99.900th diff 5.8E-01) ❌

- **DownRecomm**
  - Script: DownRecomm
  - Python CSV: yes
  - Superset: no (3.19%) ❌
  - Precision1: yes (0.03%)
  - Precision2: yes (99.900th diff 0.0E+00)

- **UpRecomm**
  - Script: UpRecomm
  - Python CSV: yes
  - Superset: no (3.19%) ❌
  - Precision1: yes (0.02%)
  - Precision2: yes (99.900th diff 0.0E+00)

- **RDAbility**
  - Script: RDAbility
  - Python CSV: yes
  - Superset: no (1.43%) ❌
  - Precision1: no (10.38%) ❌
  - Precision2: no (99.900th diff 4.2E+00) ❌

- **MomRev**
  - Script: MomRev
  - Python CSV: yes
  - Superset: no (1.31%) ❌
  - Precision1: yes (0.00%)
  - Precision2: yes (99.900th diff 0.0E+00)

- **BetaTailRisk**
  - Script: BetaTailRisk
  - Python CSV: yes
  - Superset: yes (100%)
  - Precision1: no (4.15%) ❌
  - Precision2: yes (99.900th diff 4.8E-02)

- **ChForecastAccrual**
  - Script: ChForecastAccrual
  - Python CSV: yes
  - Superset: yes (100%)
  - Precision1: yes (0.12%)
  - Precision2: no (99.900th diff 2.0E+00) ❌

- **CitationsRD**
  - Script: CitationsRD
  - Python CSV: yes
  - Superset: yes (100%)
  - Precision1: no (21.54%) ❌
  - Precision2: no (99.900th diff 2.4E+00) ❌

- **CredRatDG**
  - Script: CredRatDG
  - Python CSV: yes
  - Superset: yes (100%)
  - Precision1: yes (0.94%)
  - Precision2: no (99.900th diff 6.6E+00) ❌

- **DivSeason**
  - Script: DivSeason
  - Python CSV: yes
  - Superset: yes (100%)
  - Precision1: no (5.21%) ❌
  - Precision2: no (99.900th diff 2.0E+00) ❌

- **EarnSupBig**
  - Script: EarnSupBig
  - Python CSV: yes
  - Superset: yes (100%)
  - Precision1: yes (0.15%)
  - Precision2: no (99.900th diff 1.5E+00) ❌

- **Herf**
  - Script: Herf
  - Python CSV: yes
  - Superset: yes (100%)
  - Precision1: yes (0.79%)
  - Precision2: no (99.900th diff 5.1E-01) ❌

- **HerfAsset**
  - Script: HerfAsset
  - Python CSV: yes
  - Superset: yes (100%)
  - Precision1: no (1.44%) ❌
  - Precision2: no (99.900th diff 5.1E-01) ❌

- **IndMom**
  - Script: IndMom
  - Python CSV: yes
  - Superset: yes (100%)
  - Precision1: no (3.28%) ❌
  - Precision2: no (99.900th diff 1.7E+00) ❌

- **IndRetBig**
  - Script: IndRetBig
  - Python CSV: yes
  - Superset: yes (100%)
  - Precision1: no (6.70%) ❌
  - Precision2: no (99.900th diff 3.8E-01) ❌

- **Investment**
  - Script: Investment
  - Python CSV: yes
  - Superset: yes (100%)
  - Precision1: yes (1.00%)
  - Precision2: no (99.900th diff 1.8E-01) ❌

- **MRreversal**
  - Script: MRreversal
  - Python CSV: yes
  - Superset: yes (100%)
  - Precision1: yes (0.15%)
  - Precision2: no (99.900th diff 2.5E-01) ❌

- **MS**
  - Script: MS
  - Python CSV: yes
  - Superset: yes (100%)
  - Precision1: no (32.97%) ❌
  - Precision2: no (99.900th diff 2.6E+00) ❌

## Worst Precision1

Predictors with highest precision1 failure rates (highest percentage of observations with significant differences):

- **TrendFactor**
  - Script: TrendFactor
  - Python CSV: yes
  - Superset: yes (100%)
  - Precision1: no (97.13%) ❌
  - Precision2: no (99.900th diff 2.0E+00) ❌

- **MS**
  - Script: MS
  - Python CSV: yes
  - Superset: yes (100%)
  - Precision1: no (32.97%) ❌
  - Precision2: no (99.900th diff 2.6E+00) ❌

- **CitationsRD**
  - Script: CitationsRD
  - Python CSV: yes
  - Superset: yes (100%)
  - Precision1: no (21.54%) ❌
  - Precision2: no (99.900th diff 2.4E+00) ❌

- **PS**
  - Script: PS
  - Python CSV: yes
  - Superset: yes (100%)
  - Precision1: no (17.93%) ❌
  - Precision2: no (99.900th diff 2.4E+00) ❌

- **RDAbility**
  - Script: RDAbility
  - Python CSV: yes
  - Superset: no (1.43%) ❌
  - Precision1: no (10.38%) ❌
  - Precision2: no (99.900th diff 4.2E+00) ❌

- **IndRetBig**
  - Script: IndRetBig
  - Python CSV: yes
  - Superset: yes (100%)
  - Precision1: no (6.70%) ❌
  - Precision2: no (99.900th diff 3.8E-01) ❌

- **DivSeason**
  - Script: DivSeason
  - Python CSV: yes
  - Superset: yes (100%)
  - Precision1: no (5.21%) ❌
  - Precision2: no (99.900th diff 2.0E+00) ❌

- **BetaTailRisk**
  - Script: BetaTailRisk
  - Python CSV: yes
  - Superset: yes (100%)
  - Precision1: no (4.15%) ❌
  - Precision2: yes (99.900th diff 4.8E-02)

- **IndMom**
  - Script: IndMom
  - Python CSV: yes
  - Superset: yes (100%)
  - Precision1: no (3.28%) ❌
  - Precision2: no (99.900th diff 1.7E+00) ❌

- **HerfAsset**
  - Script: HerfAsset
  - Python CSV: yes
  - Superset: yes (100%)
  - Precision1: no (1.44%) ❌
  - Precision2: no (99.900th diff 5.1E-01) ❌

- **VolumeTrend**
  - Script: VolumeTrend
  - Python CSV: yes
  - Superset: yes (100%)
  - Precision1: no (1.36%) ❌
  - Precision2: no (99.900th diff 1.8E+00) ❌

- **Tax**
  - Script: Tax
  - Python CSV: yes
  - Superset: yes (100%)
  - Precision1: no (1.24%) ❌
  - Precision2: no (99.900th diff 1.1E-01) ❌

- **MomOffSeason**
  - Script: MomOffSeason
  - Python CSV: yes
  - Superset: yes (100%)
  - Precision1: no (1.06%) ❌
  - Precision2: no (99.900th diff 2.1E+00) ❌

- **NumEarnIncrease**
  - Script: NumEarnIncrease
  - Python CSV: yes
  - Superset: yes (100%)
  - Precision1: no (1.01%) ❌
  - Precision2: no (99.900th diff 3.6E+00) ❌

- **Investment**
  - Script: Investment
  - Python CSV: yes
  - Superset: yes (100%)
  - Precision1: yes (1.00%)
  - Precision2: no (99.900th diff 1.8E-01) ❌

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
  - Precision1: yes (0.94%)
  - Precision2: no (99.900th diff 1.2E-01) ❌

- **MomOffSeason06YrPlus**
  - Script: MomOffSeason06YrPlus
  - Python CSV: yes
  - Superset: yes (100%)
  - Precision1: yes (0.92%)
  - Precision2: no (99.900th diff 1.9E+00) ❌

- **MomOffSeason11YrPlus**
  - Script: MomOffSeason11YrPlus
  - Python CSV: yes
  - Superset: yes (100%)
  - Precision1: yes (0.88%)
  - Precision2: no (99.900th diff 1.8E+00) ❌

- **Herf**
  - Script: Herf
  - Python CSV: yes
  - Superset: yes (100%)
  - Precision1: yes (0.79%)
  - Precision2: no (99.900th diff 5.1E-01) ❌

