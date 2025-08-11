# Plan: Continue Standardizing asreg translations

## Current Task: standardize the next Predictor py script that is marked as "tbc"
1. Find the next tbc script
  - Check "## Predictor py scripts" below
  - Find the first one with Status: tbc
2. Update the script to use `utils/asreg.py` instead of other regression implementations
  - See the example code snippet below

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

## Context: Before you start the task

Read these docs:
- DocsForClaude/leg3-Predictors.md for the big picture
- DocsForClaude/asreg-implementation-milestone.md to understand the current goal

Run the validation script on the predictors in question:
- Get predictor names by searching for the script in `pyCode/Predictors/00_map_predictors.yaml` 
- Run the validation script: `cd pyCode && python3 utils/test_predictor.py --predictors PREDICTOR1 PREDICTOR2 ...`

Think about the plan before writing code.

## Predictor py scripts

### Phase 1: Start with Curated Files for Learning
**ZZ2_betaVIX.py** (30 lines) - ✅ **COMPLETED** (0.041% failure - 99.94% improvement!)
   - Output: `betaVIX.csv`
   - Status: ✅ FIXED using utils/asreg.py helper
   - Actual effort: 1 session

**ZZ2_IdioVolAHT.py** - 8.536% failure
    - Output: `IdioVolAHT.csv`
    - Status: Skip
    - Note: There may be a bug in the Stata code 

**ZZ2_BetaFP.py** - 5.980% failure, missing 0.54% obs
    - Output: `BetaFP.csv`    
    - Status: Skip
    - Note: Computing correlation directly here is actually preferred to asreg and the deviations seem to be due to lag handling.

### Phase 2: Complex Files After Learning
**Target: Apply lessons to harder cases**

**ZZ2_AbnormalAccruals_AbnormalAccrualsPercent.py** - 49.009% failure, missing 0.65% obs
   - Outputs: `AbnormalAccruals.csv`, `AbnormalAccrualsPercent.csv` (placebo)
   - Status: UPDATED to use utils/asreg.py helper (precision unchanged)

**ZZ2_PriceDelaySlope_PriceDelayRsq_PriceDelayTstat.py** - 19.380% failure (PriceDelayTstat worst)
   - Outputs: `PriceDelaySlope.csv`, `PriceDelayRsq.csv`, `PriceDelayTstat.csv`
   - Status: UPDATED to use utils/asreg.py helper (precision unchanged)
   - Note: Seems like there's a bug in the Stata code. Github issue created.

**TrendFactor.py** (104 lines) - 97.153% failure (improved from 98.418%), missing 0.07% obs  
   - Output: `TrendFactor.csv`
   - Status: UPDATED to use utils/asreg.py helper (1.3% improvement achieved)
   - Note: Complex predictor with multiple issues beyond regression implementation. Asreg standardization provided modest improvement but significant precision issues remain.

**RDAbility.py** - 9.523% failure (improved from 95.728%), missing 4.95% obs
   - Output: `RDAbility.csv`
   - Status: UPDATED to use utils/asreg.py helper (86.2% improvement achieved!)
   - Key fix: Original had `add_intercept=False`, Stata asreg includes intercept by default

### Phase 3: Low priority files
The precision on these is likely good enough. But we still want to standardize `asreg.py` usage.

**VolumeTrend.py** (13 lines in do file) - 1.001% failure
   - Output: `VolumeTrend.csv`
   - Status: tbc
**BetaLiquidityPS.py** (21 lines) - 0.309% failure  
   - Output: `BetaLiquidityPS.csv`
   - Status: tbc
**BetaTailRisk.py** (46 lines) - 4.149% failure
   - Output: `BetaTailRisk.csv`
   - Expected effort: 1 session    
   - Status: tbc
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
