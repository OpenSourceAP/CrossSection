# Scripts That Failed Any Test

**Generated**: 2025-08-15 13:53:51

**Scripts that failed superset test** (Python missing Stata observations):

Recomm_ShortInterest ZZ1_RIO_MB_RIO_Disp_RIO_Turnover_RIO_Volatility 

**Scripts that failed other tests** (but passed superset):

DivSeason HerfAsset MomOffSeason MomOffSeason06YrPlus MomOffSeason11YrPlus MomOffSeason16YrPlus MomVol RDAbility TrendFactor ZZ1_RIO_MB_RIO_Disp_RIO_Turnover_RIO_Volatility 

## Detailed Analysis

This section focuses on the 20 worst predictors by Superset and Precision1 metrics.

## Worst Superset

Predictors with highest superset failure rates (Python missing the most Stata observations):

- **Recomm_ShortInterest**
  - Script: Recomm_ShortInterest
  - Python CSV: yes
  - Superset: no (47.17%) ❌
  - Precision1: yes (0.00%)
  - Precision2: yes (99.900th diff 0.0E+00)

- **RIO_Volatility**
  - Script: ZZ1_RIO_MB_RIO_Disp_RIO_Turnover_RIO_Volatility
  - Python CSV: yes
  - Superset: no (4.44%) ❌
  - Precision1: no (4.32%) ❌
  - Precision2: no (99.900th diff 7.5E-01) ❌

- **CitationsRD**
  - Script: CitationsRD
  - Python CSV: yes
  - Superset: yes (100%)
  - Precision1: yes (0.00%)
  - Precision2: yes (99.900th diff 0.0E+00)

- **DivInit**
  - Script: DivInit
  - Python CSV: yes
  - Superset: yes (100%)
  - Precision1: yes (0.01%)
  - Precision2: yes (99.900th diff 0.0E+00)

- **DivOmit**
  - Script: DivOmit
  - Python CSV: yes
  - Superset: yes (100%)
  - Precision1: yes (0.00%)
  - Precision2: yes (99.900th diff 0.0E+00)

- **DivSeason**
  - Script: DivSeason
  - Python CSV: yes
  - Superset: yes (100%)
  - Precision1: yes (0.99%)
  - Precision2: no (99.900th diff 2.0E+00) ❌

- **Herf**
  - Script: Herf
  - Python CSV: yes
  - Superset: yes (100%)
  - Precision1: yes (0.19%)
  - Precision2: yes (99.900th diff 6.2E-02)

- **HerfAsset**
  - Script: HerfAsset
  - Python CSV: yes
  - Superset: yes (100%)
  - Precision1: yes (0.66%)
  - Precision2: no (99.900th diff 2.3E-01) ❌

- **HerfBE**
  - Script: HerfBE
  - Python CSV: yes
  - Superset: yes (100%)
  - Precision1: yes (0.00%)
  - Precision2: yes (99.900th diff 1.5E-05)

- **Investment**
  - Script: Investment
  - Python CSV: yes
  - Superset: yes (100%)
  - Precision1: yes (0.18%)
  - Precision2: yes (99.900th diff 2.7E-02)

- **MomOffSeason**
  - Script: MomOffSeason
  - Python CSV: yes
  - Superset: yes (100%)
  - Precision1: no (1.06%) ❌
  - Precision2: no (99.900th diff 2.1E+00) ❌

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

- **MomOffSeason16YrPlus**
  - Script: MomOffSeason16YrPlus
  - Python CSV: yes
  - Superset: yes (100%)
  - Precision1: yes (0.51%)
  - Precision2: no (99.900th diff 6.1E-01) ❌

- **MomVol**
  - Script: MomVol
  - Python CSV: yes
  - Superset: yes (100%)
  - Precision1: yes (0.42%)
  - Precision2: no (99.900th diff 3.5E-01) ❌

- **RDAbility**
  - Script: RDAbility
  - Python CSV: yes
  - Superset: yes (100%)
  - Precision1: no (10.90%) ❌
  - Precision2: no (99.900th diff 4.2E+00) ❌

- **RIO_Disp**
  - Script: ZZ1_RIO_MB_RIO_Disp_RIO_Turnover_RIO_Volatility
  - Python CSV: yes
  - Superset: yes (100%)
  - Precision1: no (3.79%) ❌
  - Precision2: no (99.900th diff 7.9E-01) ❌

- **RIO_MB**
  - Script: ZZ1_RIO_MB_RIO_Disp_RIO_Turnover_RIO_Volatility
  - Python CSV: yes
  - Superset: yes (100%)
  - Precision1: no (3.45%) ❌
  - Precision2: no (99.900th diff 7.4E-01) ❌

- **RIO_Turnover**
  - Script: ZZ1_RIO_MB_RIO_Disp_RIO_Turnover_RIO_Volatility
  - Python CSV: yes
  - Superset: yes (100%)
  - Precision1: no (3.65%) ❌
  - Precision2: no (99.900th diff 7.4E-01) ❌

- **TrendFactor**
  - Script: TrendFactor
  - Python CSV: yes
  - Superset: yes (100%)
  - Precision1: no (97.14%) ❌
  - Precision2: no (99.900th diff 2.9E+00) ❌

## Worst Precision1

Predictors with highest precision1 failure rates (highest percentage of observations with significant differences):

- **TrendFactor**
  - Script: TrendFactor
  - Python CSV: yes
  - Superset: yes (100%)
  - Precision1: no (97.14%) ❌
  - Precision2: no (99.900th diff 2.9E+00) ❌

- **RDAbility**
  - Script: RDAbility
  - Python CSV: yes
  - Superset: yes (100%)
  - Precision1: no (10.90%) ❌
  - Precision2: no (99.900th diff 4.2E+00) ❌

- **RIO_Volatility**
  - Script: ZZ1_RIO_MB_RIO_Disp_RIO_Turnover_RIO_Volatility
  - Python CSV: yes
  - Superset: no (4.44%) ❌
  - Precision1: no (4.32%) ❌
  - Precision2: no (99.900th diff 7.5E-01) ❌

- **RIO_Disp**
  - Script: ZZ1_RIO_MB_RIO_Disp_RIO_Turnover_RIO_Volatility
  - Python CSV: yes
  - Superset: yes (100%)
  - Precision1: no (3.79%) ❌
  - Precision2: no (99.900th diff 7.9E-01) ❌

- **RIO_Turnover**
  - Script: ZZ1_RIO_MB_RIO_Disp_RIO_Turnover_RIO_Volatility
  - Python CSV: yes
  - Superset: yes (100%)
  - Precision1: no (3.65%) ❌
  - Precision2: no (99.900th diff 7.4E-01) ❌

- **RIO_MB**
  - Script: ZZ1_RIO_MB_RIO_Disp_RIO_Turnover_RIO_Volatility
  - Python CSV: yes
  - Superset: yes (100%)
  - Precision1: no (3.45%) ❌
  - Precision2: no (99.900th diff 7.4E-01) ❌

- **MomOffSeason**
  - Script: MomOffSeason
  - Python CSV: yes
  - Superset: yes (100%)
  - Precision1: no (1.06%) ❌
  - Precision2: no (99.900th diff 2.1E+00) ❌

- **DivSeason**
  - Script: DivSeason
  - Python CSV: yes
  - Superset: yes (100%)
  - Precision1: yes (0.99%)
  - Precision2: no (99.900th diff 2.0E+00) ❌

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

- **HerfAsset**
  - Script: HerfAsset
  - Python CSV: yes
  - Superset: yes (100%)
  - Precision1: yes (0.66%)
  - Precision2: no (99.900th diff 2.3E-01) ❌

- **MomOffSeason16YrPlus**
  - Script: MomOffSeason16YrPlus
  - Python CSV: yes
  - Superset: yes (100%)
  - Precision1: yes (0.51%)
  - Precision2: no (99.900th diff 6.1E-01) ❌

- **MomVol**
  - Script: MomVol
  - Python CSV: yes
  - Superset: yes (100%)
  - Precision1: yes (0.42%)
  - Precision2: no (99.900th diff 3.5E-01) ❌

- **Herf**
  - Script: Herf
  - Python CSV: yes
  - Superset: yes (100%)
  - Precision1: yes (0.19%)
  - Precision2: yes (99.900th diff 6.2E-02)

- **Investment**
  - Script: Investment
  - Python CSV: yes
  - Superset: yes (100%)
  - Precision1: yes (0.18%)
  - Precision2: yes (99.900th diff 2.7E-02)

- **DivInit**
  - Script: DivInit
  - Python CSV: yes
  - Superset: yes (100%)
  - Precision1: yes (0.01%)
  - Precision2: yes (99.900th diff 0.0E+00)

- **DivOmit**
  - Script: DivOmit
  - Python CSV: yes
  - Superset: yes (100%)
  - Precision1: yes (0.00%)
  - Precision2: yes (99.900th diff 0.0E+00)

- **HerfBE**
  - Script: HerfBE
  - Python CSV: yes
  - Superset: yes (100%)
  - Precision1: yes (0.00%)
  - Precision2: yes (99.900th diff 1.5E-05)

- **CitationsRD**
  - Script: CitationsRD
  - Python CSV: yes
  - Superset: yes (100%)
  - Precision1: yes (0.00%)
  - Precision2: yes (99.900th diff 0.0E+00)

- **Recomm_ShortInterest**
  - Script: Recomm_ShortInterest
  - Python CSV: yes
  - Superset: no (47.17%) ❌
  - Precision1: yes (0.00%)
  - Precision2: yes (99.900th diff 0.0E+00)

