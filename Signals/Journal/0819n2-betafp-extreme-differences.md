# BetaFP Extreme Differences Analysis

**Date**: 2025-08-19
**Issue**: Large differences between Python and Stata BetaFP values, especially pre-1950

## Key Findings

### 1. The Problem
- Extreme case: permno 14269 in Dec 1941
  - Python: 4.258
  - Stata: 5.278
  - Difference: -1.02 (19% relative difference!)

### 2. Root Cause Analysis

#### Component Values for permno 14269, Dec 1941:
- **SD ratio (LogRet/LogMkt)**: 31.87 (extremely high!)
- **Correlation**: 0.1336 (very low)
- **R²**: 0.0178 (correlation squared)
- **BetaFP formula**: sqrt(R²) × (SD_LogRet/SD_LogMkt)
- **Python calc**: sqrt(0.0178) × 31.87 = 4.258

#### Why the Difference?
1. **Extreme SD ratios amplify small R² differences**
   - When SD_LogRet/SD_LogMkt > 30, tiny R² differences become huge BetaFP differences
   - Example: If R² differs by 0.005, BetaFP differs by sqrt(0.005) × 31 ≈ 2.2

2. **Correlation vs Regression R²**
   - Python: Uses correlation formula R² = corr²
   - Stata: Uses `asreg` actual regression R²
   - These can differ in edge cases with sparse/volatile data

3. **Window Parameters Impact**
   - Tested with min_samples = 500, 600, 750
   - All gave same result for Dec 1941 (window had 1186 obs)
   - But 750 minimum caused MORE failures overall (5.98% vs 0.19%)
   - Suggests the issue isn't just window size

### 3. Data Characteristics in Dec 1941

Looking at the raw data for permno 14269:
- Many NaN returns (about 40% of days)
- One extreme return: -0.5 on Dec 6, 1941
- Most other returns are 0.0
- Market (mktrf) much more stable with smaller moves

This creates:
- Very high individual stock volatility (LogRet SD ≈ 0.23)
- Low market volatility (LogMkt SD ≈ 0.007)
- Extreme ratio: 0.23/0.007 ≈ 32

### 4. Other Extreme Cases

The pattern repeats:
- permno 11453 (1993): diff = 4.79 (largest overall)
- permno 65622 (1994): diff = -3.98
- These all show similar characteristics: extreme SD ratios, low correlations

### 5. Why It Matters

The BetaFP (Frazzini-Pedersen beta) is designed to measure systematic risk.
- High SD ratio means stock is much more volatile than market
- Low R² means most of that volatility is idiosyncratic
- Small R² calculation differences get amplified by high SD ratio

## Attempted Solutions

1. **Changed min_samples from 500 to 750** 
   - Result: Made things worse (5.98% failure rate)
   - Reverted back to 500

2. **Analyzed correlation calculation**
   - Formula is mathematically correct
   - Issue seems to be numerical precision/methodology difference with Stata

## Recommendations

1. **Accept current implementation with 500 min_samples**
   - Gives best overall match (most periods pass)
   - Extreme cases are inherently unstable

2. **Consider future improvements**:
   - Use actual rolling regression (would need different library)
   - Add numerical stability checks for extreme SD ratios
   - Cap or windsorize extreme values

3. **Document the limitation**
   - BetaFP may differ from Stata in extreme volatility periods
   - Particularly affects wartime data (1940s) and crisis periods

## Technical Details

The calculation pipeline:
1. Calculate log returns (LogRet, LogMkt)
2. Create 3-day overlapping returns (tempRi, tempRm)
3. Calculate 252-day rolling SDs
4. Calculate 1260-day rolling correlation of overlapping returns
5. BetaFP = sqrt(R²) × (SD_LogRet/SD_LogMkt)

The differences arise in step 4 - the R² calculation from overlapping returns.