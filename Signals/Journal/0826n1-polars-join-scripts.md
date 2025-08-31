# Polars Join Scripts in Predictors

## Scripts that use both `import polars` and `.join()`

26 out of 29 polars scripts use joins:

- ZZ1_Activism1_Activism2.py
- MS.py  
- ZZ2_PriceDelaySlope_PriceDelayRsq_PriceDelayTstat.py
- ZZ1_RIO_MB_RIO_Disp_RIO_Turnover_RIO_Volatility.py
- TrendFactor.py
- Recomm_ShortInterest.py
- RDAbility.py
- MomVol.py
- ShareVol.py
- ZZ1_AnalystValue_AOP_PredictedFE_IntrinsicValue.py
- ZZ2_IdioVolAHT.py
- ZZ2_betaVIX.py
- ZZ2_AbnormalAccruals_AbnormalAccrualsPercent.py
- ZZ1_ResidualMomentum6m_ResidualMomentum.py
- ZZ0_RealizedVol_IdioVol3F_ReturnSkew3F.py
- BetaTailRisk.py
- BetaLiquidityPS.py
- Beta.py
- ZZ2_BetaFP.py
- Coskewness.py
- ZZ1_EBM_BPEBM.py
- VolSD.py
- VolMkt.py
- STreversal.py
- ReturnSkew.py
- CoskewACX.py

## Scripts that import polars but don't use joins

3 scripts:
- VolumeTrend.py
- std_turn.py  
- OPLeverage.py

## Notes

Total: 29 polars scripts, 26 with joins, 3 without joins.