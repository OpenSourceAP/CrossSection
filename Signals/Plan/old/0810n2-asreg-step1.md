# Plan: Systematic asreg Predictor Fixes - Step 1

## Context
**Important: Before you start, read these docs**: 
- DocsForClaude/leg3-Predictors.md for the big picture
- DocsForClaude/asreg-implementation-milestone.md to understand the current goal

## Mission
Fix all 14 remaining asreg-related predictors using the proven Beta.do methodology. Target: >99% Precision1 match for all predictors.

## Strategy: Apply Beta.do Success Pattern
Beta.do succeeded by:
1. Using `utils/asreg.py` helper consistently
2. Always including `order_by` parameter in rolling operations  
3. Proper data sorting: `lf.sort([*by, t])`
4. Inner join validation methodology
5. Line-by-line translation without "improvements"

## Efficiency: Modify Code to output Work on only a subset of data
- Many of these scripts are computationally intensive, running thousands or millions of regressions.
- Modify the script so that it can filter the data to only 5 years (e.g. 1981-1985) before running the asreg helper.
- Compare the smaller subset of Python output with the Stata outputs using utils/test_predictor.py before running the full dataset.



### Debugging Methodology
- Focus on specific permno-yyyymm observations that fail
- Use bisection strategy before assuming "data differences"
- Write Debug/*.py scripts instead of long bash commands
- Never speculate about real data differences - keep investigating logic

### Validation Standards  
- Inner join comparison only (avoid timing artifact false positives)
- Fix structural issues (identifiers, formats) before data differences
- Achieve >99% precision before moving to next predictor
- Document any discoveries for future predictors



## Priority Queue (Simple → Complex by Line Count)

### Phase 1: Start with Simple Files for Learning
**ZZ2_betaVIX.py** (30 lines) - ✅ **COMPLETED** (0.041% failure - 99.94% improvement!)
   - Output: `betaVIX.csv`
   - Status: ✅ FIXED using utils/asreg.py helper
   - Actual effort: 1 session

**ZZ2_IdioVolAHT.py** - 8.536% failure
    - Output: `IdioVolAHT.csv`
    - Status: Skip for now based on user feedback. There may be a bug in the Stata code.

**ZZ2_BetaFP.py** - 5.980% failure, missing 0.54% obs
    - Output: `BetaFP.csv`    
    - Status: Skip for now based on user feedback. Computing correlation directly here is actually preferred to asreg and the deviations seem to be due to lag handling.

### Phase 2: Complex Files After Learning
**Target: Apply lessons to harder cases**

**ZZ2_AbnormalAccruals_AbnormalAccrualsPercent.py** - 49.009% failure, missing 0.65% obs
   - Outputs: `AbnormalAccruals.csv`, `AbnormalAccrualsPercent.csv` (placebo)
   - Status: tbc

**ZZ2_PriceDelaySlope_PriceDelayRsq_PriceDelayTstat.py** - 19.380% failure (PriceDelayTstat worst)
   - Outputs: `PriceDelaySlope.csv`, `PriceDelayRsq.csv`, `PriceDelayTstat.csv`
   - Status: tbc

**TrendFactor.py** (104 lines) - 98.418% failure, missing 0.07% obs  
   - Output: `TrendFactor.csv`
   - Status: tbc

**RDAbility.py** - 95.728% failure, missing 4.89% obs
   - Output: `RDAbility.csv`
   - Status: tbc

### Phase 3: Remaining Moderate/Minor Fixes
**Target: Apply systematic approach after mastering simple cases**

**VolumeTrend.py** (13 lines in do file) - 1.001% failure
   - Output: `VolumeTrend.csv`
   - Status: SIMPLE + MINOR - ideal learning case
   - Expected effort: <1 session
   - Status: tbc
**BetaLiquidityPS.py** (21 lines) - 0.309% failure  
   - Output: `BetaLiquidityPS.csv`
   - Status: SIMPLE + MINOR - good practice case
   - Expected effort: <1 session
   - Status: tbc
**BetaTailRisk.py** (46 lines) - 4.149% failure
   - Output: `BetaTailRisk.csv`
   - Status: MODERATE + MODERATE - apply lessons learned
   - Expected effort: 1 session    
   - Status: tbc
### Phase 4: Make sure these use the asreg helper
These are actually good enough. Skewness is difficult to match exactly. 

**ZZ0_RealizedVol_IdioVol3F_ReturnSkew3F.py** - 2.575% failure (ReturnSkew3F)
    - Outputs: `RealizedVol.csv`, `IdioVol3F.csv`, `ReturnSkew3F.csv`
    - Status: tbc
**ZZ1_ResidualMomentum6m_ResidualMomentum.py** - 0.712% failure, missing 2.40% obs
    - Outputs: `ResidualMomentum.csv`, `ResidualMomentum6m.csv` (placebo)
    - Status: tbc
**ZZ1_AnalystValue_AOP_PredictedFE_IntrinsicValue.py** - 0.263% failure, missing 0.22% obs
    - Outputs: `AnalystValue.csv`, `AOP.csv`, `PredictedFE.csv`, `IntrinsicValue.csv` (placebo)
    - Status: tbc

### Save for Later
The do files don't actually use asreg, but are related to asreg.
**Coskewness.py** - 99.358% failure, missing 8.84% obs
   - Output: `Coskewness.csv`

