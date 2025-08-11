# Plan: Systematic asreg Predictor Fixes - Step 1

## Context
Read 
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

## Priority Queue (Simple → Complex by Line Count)

### Phase 1: Start with Simple Files for Learning
**ZZ2_betaVIX.py** (30 lines) - 69.594% failure
   - Output: `betaVIX.csv`
   - Status: SIMPLE + SEVERE - systematic issue but easy to debug
   - Expected effort: 1 session

**ZZ2_IdioVolAHT.py** - 8.536% failure
    - Output: `IdioVolAHT.csv`

**ZZ2_BetaFP.py** - 5.980% failure, missing 0.54% obs
    - Output: `BetaFP.csv`    

### Phase 2: Complex Files After Learning
**Target: Apply lessons to harder cases**

**ZZ2_AbnormalAccruals_AbnormalAccrualsPercent.py** - 49.009% failure, missing 0.65% obs
   - Outputs: `AbnormalAccruals.csv`, `AbnormalAccrualsPercent.csv` (placebo)

**ZZ2_PriceDelaySlope_PriceDelayRsq_PriceDelayTstat.py** - 19.380% failure (PriceDelayTstat worst)
   - Outputs: `PriceDelaySlope.csv`, `PriceDelayRsq.csv`, `PriceDelayTstat.csv`


**TrendFactor.py** (104 lines) - 98.418% failure, missing 0.07% obs  
   - Output: `TrendFactor.csv`

**RDAbility.py** - 95.728% failure, missing 4.89% obs
   - Output: `RDAbility.csv`

### Phase 3: Remaining Moderate/Minor Fixes
**Target: Apply systematic approach after mastering simple cases**

**VolumeTrend.py** (13 lines in do file) - 1.001% failure
   - Output: `VolumeTrend.csv`
   - Status: SIMPLE + MINOR - ideal learning case
   - Expected effort: <1 session

**BetaLiquidityPS.py** (21 lines) - 0.309% failure  
   - Output: `BetaLiquidityPS.csv`
   - Status: SIMPLE + MINOR - good practice case
   - Expected effort: <1 session

**BetaTailRisk.py** (46 lines) - 4.149% failure
   - Output: `BetaTailRisk.csv`
   - Status: MODERATE + MODERATE - apply lessons learned
   - Expected effort: 1 session    

### Phase 4: Make sure these use the asreg helper
These are actually good enough. Skewness is difficult to match exactly. 

**ZZ0_RealizedVol_IdioVol3F_ReturnSkew3F.py** - 2.575% failure (ReturnSkew3F)
    - Outputs: `RealizedVol.csv`, `IdioVol3F.csv`, `ReturnSkew3F.csv`
**ZZ1_ResidualMomentum6m_ResidualMomentum.py** - 0.712% failure, missing 2.40% obs
    - Outputs: `ResidualMomentum.csv`, `ResidualMomentum6m.csv` (placebo)
14. **ZZ1_AnalystValue_AOP_PredictedFE_IntrinsicValue.py** - 0.263% failure, missing 0.22% obs
    - Outputs: `AnalystValue.csv`, `AOP.csv`, `PredictedFE.csv`, `IntrinsicValue.csv` (placebo)

### Save for Later
The do files don't actually use asreg, but are related to asreg.
**Coskewness.py** - 99.358% failure, missing 8.84% obs
   - Output: `Coskewness.csv`

## Step 1 Action Plan: Fix ZZ2_betaVIX.py

### Pre-Work Checklist  
- [ ] Activate venv: `source pyCode/.venv/bin/activate`
- [ ] Verify `utils/asreg.py` helper exists and works
- [ ] Review ZZ2_betaVIX.do Stata code line-by-line (DONE - 30 lines, very simple)
- [ ] Check current pyCode/Predictors/ZZ2_betaVIX.py implementation

### Implementation Strategy
1. **Read & Understand**
   - Read current `pyCode/Predictors/ZZ2_betaVIX.py` (check if exists)
   - Understand ZZ2_betaVIX.do logic: simple asreg with ret ~ mktrf + dVIX, window 20, min 15

2. **Apply Beta.do Lessons**
   - Replace any manual pandas/numpy regression logic with `utils/asreg.py` calls  
   - Ensure rolling operations use `order_by=pl.col(time_column)`
   - Add proper data sorting before regression: `lf.sort([*by, t])`
   - Use `time_temp = _n` pattern for observation windows
   - Set correct `min_samples=15` parameter (from min(15) in Stata)

3. **Technical Focus Areas**
   - 69.594% Precision1 failures suggest major systematic issue
   - Superset already passes (good sign - no missing obs)
   - Focus on coefficient extraction and missing value handling
   - Ensure proper VIX data merge and timing

4. **Validation Process**
   - Use inner join methodology (not left join)
   - Write Debug script to test specific problematic observations  
   - Target: <0.1% Precision1 failures
   - Check coefficient values match Stata exactly

### Success Criteria for Step 1
- [ ] Superset: ✅ PASSED (already achieved)
- [ ] Precision1: ✅ PASSED (<0.1% bad observations)
- [ ] Precision2: Target <1e-4 (microscopic differences acceptable)  
- [ ] Code: Clean, readable, line-by-line translation

### Next Steps After ZZ2_betaVIX Success
1. Move to VolumeTrend.py (simplest file - 13 lines, 1.001% failure)
2. Then BetaLiquidityPS.py (21 lines, 0.309% failure)
3. Document lessons learned for more complex cases

## Key Technical Reminders

### Must-Have Code Elements
```python
# Always sort data first
lf = lf.sort([*by, t])

# Use asreg helper with order_by
from utils.asreg import asreg
result = asreg(
    lf, 
    y_col="ret", 
    x_cols=["mkt", "smb", "hml"], 
    by=["permno"], 
    window=60, 
    min_samples=20,
    order_by=pl.col("time_column")  # CRITICAL - don't forget!
)

# Extract coefficients properly
lf = lf.with_columns([
    result["coef_mkt"].alias("beta"),
    result["coef_smb"].alias("beta_smb"),
    # etc.
])
```

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

## Progress Tracking
**Current Status**: Ready to start ZZ2_betaVIX.py fix  
**Expected Timeline**: 1-2 weeks for Phase 1 (4 simple files), 2-3 weeks for Phase 2 (3 complex files)
**Success Metric**: All 14 predictors achieve >99% Precision1 match

---
*Last Updated: 2025-08-10*  
*Next Claude: Start with ZZ2_betaVIX.py (30 lines, simple asreg case for learning)*