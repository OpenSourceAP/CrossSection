# asreg Utils Cleanup - Completed

## ✅ Consolidation Complete

Successfully consolidated all asreg functions into a single, organized `utils/stata_replication.py` file.

### What was done:

1. **Added `asreg_polars()` to `utils/stata_replication.py`**
   - Copied the fast polars-based asreg function from `utils/asreg.py`
   - Added comprehensive documentation explaining differences between implementations
   - Added polars imports with error handling

2. **Updated all 10 predictor files using polars asreg:**
   - ✅ Beta.py
   - ✅ BetaLiquidityPS.py  
   - ✅ BetaTailRisk.py
   - ✅ RDAbility.py
   - ✅ ZZ0_RealizedVol_IdioVol3F_ReturnSkew3F.py
   - ✅ ZZ1_AnalystValue_AOP_PredictedFE_IntrinsicValue.py
   - ✅ ZZ1_ResidualMomentum6m_ResidualMomentum.py
   - ✅ ZZ2_AbnormalAccruals_AbnormalAccrualsPercent.py
   - ✅ ZZ2_betaVIX.py (also fixed sys.path import)
   - ✅ ZZ2_IdioVolAHT.py (also fixed sys.path import)

3. **TrendFactor.py unchanged** - already uses `asreg_collinear()` correctly

4. **Cleaned up old files:**
   - ❌ Deleted `pyCode/utils/asreg.py`
   - ❌ Deleted `pyCode/Journal/0813h1-asreg-GPT5.py` (duplicate)

5. **All files tested successfully** - Each predictor script ran without errors after update

## Current Organization in `utils/stata_replication.py`:

- **`asreg_polars()`**: Fast polars-based implementation, no collinearity handling
- **`asreg_collinear()`**: Pandas-based with full Stata replication and collinearity handling  
- Comprehensive documentation explaining when to use each version

## Benefits:
- Single source of truth for asreg functionality
- Clear documentation of implementation differences  
- No duplicate code to maintain
- All predictor files continue to work exactly as before

# Other utils links

Here's the comprehensive list
  organized by utility module:

  utils/asrol.py (17 scripts):

  - CitationsRD.py
  - DivInit.py
  - DivOmit.py
  - DivSeason.py
  - Herf.py
  - HerfAsset.py
  - HerfBE.py
  - Investment.py
  - MomOffSeason06YrPlus.py
  - MomOffSeason11YrPlus.py
  - MomOffSeason16YrPlus.py
  - MomVol.py
  - RDAbility.py
  - Recomm_ShortInterest.py
  - TrendFactor.py
  - VarCF.py
  - ZZ1_RIO_MB_RIO_Disp_RIO_Turnover_RIO_Volatility.py

  utils/asrol_pedantic.py (0 scripts):

  - No scripts currently use this module

  utils/stata_fastxtile.py (25 scripts):

  - AccrualsBM.py
  - ChForecastAccrual.py
  - ChNAnalyst.py
  - CitationsRD.py
  - DivYieldST.py
  - FirmAgeMom.py
  - GrAdExp.py
  - MomRev.py
  - MomVol.py
  - MS.py
  - NetDebtPrice.py
  - OperProf.py
  - OScore.py
  - PatentsRD.py
  - ProbInformedTrading.py
  - PS.py
  - RDAbility.py
  - RDcap.py
  - Recomm_ShortInterest.py
  - sfe.py
  - std_turn.py
  - tang.py
  - ZZ1_Activism1_Activism2.py
  - ZZ1_AnalystValue_AOP_PredictedFE_IntrinsicValue.py
  - ZZ1_RIO_MB_RIO_Disp_RIO_Turnover_RIO_Volatility.py

  utils/stata_ineq.py (5 scripts):

  - DivSeason.py
  - MS.py
  - retConglomerate.py
  - ShareVol.py
  - TrendFactor.py

  utils/winsor2.py (5 scripts):

  - VolumeTrend.py
  - ZZ1_AnalystValue_AOP_PredictedFE_IntrinsicValue.py
  - ZZ1_IntanBM_IntanSP_IntanCFP_IntanEP.py
  - ZZ1_OrgCap_OrgCapNoAdj.py
  - ZZ2_AbnormalAccruals_AbnormalAccrualsPercent.py

  Summary:
  - Total unique scripts using these utilities: 34 scripts
  - Most used utility: stata_fastxtile.py (25 scripts)
  - Least used utility: asrol_pedantic.py (0 scripts)
