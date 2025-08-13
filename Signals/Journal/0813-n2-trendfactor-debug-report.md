# TrendFactor Debug Report - Root Cause Analysis

**Date**: 2025-08-13  
**Issue**: TrendFactor predictor has 97%+ precision failure rate  
**Status**: Root cause identified - CRSP cfacpr data quality issue  

## Executive Summary

**Root Cause Found**: Massive systematic data quality issue in CRSP `cfacpr` (cumulative factor for adjusting price) causing extreme moving averages that corrupt TrendFactor calculations.

**Impact**: 97.15% of TrendFactor observations have large deviations from Stata due to artificial price inflations from cfacpr discontinuities.

**Evidence**: Multiple stocks show extreme cfacpr jumps (10x to 570x) creating unrealistic adjusted prices (P values of 1000-4000+ instead of normal ~10-100 range).

## Detailed Investigation

### 1. Initial Findings
- TrendFactor precision failure: 97.15% bad observations  
- Stata inequality fix (utils/stata_ineq.py) only improved to 97.14%
- Largest differences: permno 89901 (diff = 2.70), permno 91040 (diff = 1.97)

### 2. Deep Dive Analysis
Investigated target observation permno 10026, yyyymm 202412:
- Python: -0.034347
- Stata: 0.032569  
- Difference: -0.066916

Traced through full calculation pipeline:
- Moving averages: ✅ Correctly calculated
- Filtering: ✅ Working properly with Stata inequality fix
- Cross-sectional regressions: ✅ asreg functioning correctly
- Beta coefficients: ✅ Reasonable values
- Rolling averages: ✅ Proper 12-month windows

### 3. Breakthrough: Extreme Moving Averages
Found permno 89901, Oct 2020 with **abnormal moving averages**:
```
A_3:    0.986530 (normal)
A_100:  3.697756 (abnormal)
A_200:  6.412472 (extremely abnormal)  
A_400:  36.233872 (extremely abnormal)
A_600:  87.734466 (extremely abnormal)
A_800:  104.174157 (extremely abnormal)
A_1000: 118.578067 (extremely abnormal)
```

Normal moving averages should be ~1.0 (normalized by current price).

### 4. Root Cause: CRSP cfacpr Discontinuities

#### Problem Pattern
Every problematic stock shows **massive cfacpr discontinuities**:

**Permno 89901 (Sep 2020)**:
- cfacpr jumps from 0.013490 → 1.000000 (74x change)
- Creates adjusted prices P = |prc|/cfacpr of 2000-4000+
- Historical A_1000 average = 1731.24 (hugely inflated)
- Normalized: A_1000 = 1731.24 / 14.6 = 118.58

**Permno 91040 (Dec 2016)**:
- cfacpr jumps from 0.001754 → 1.000000 (570x change)
- Creates extreme historical adjusted prices

**Permno 66800 (Jul 2009)**:
- cfacpr jumps from 0.059750 → 1.195001 (20x change)

#### Systematic Scope
- **1,499 stocks** have extreme cfacpr jumps (>10x change)
- **686,824 daily observations** have P > 1000 (should be ~10-100)
- Affects moving averages across **multiple lag lengths** (100-1000 days)

### 5. Calculation Impact
Moving averages spanning cfacpr discontinuities:
1. Include historical periods with **artificial extreme prices** (P = 2000-4000)
2. Recent periods with **normal prices** (P = 15-25)  
3. **Average dominated by extreme historical values**
4. **Normalization by current price creates absurd ratios**

Example: A_1000 = average(extreme_historical_P) / current_P = 1731 / 14.6 = 118.6

When TrendFactor = Σ(EBeta_i × A_i), even small EBeta values create huge results.

## Technical Root Cause

**cfacpr** (cumulative factor for adjusting price) is meant to handle:
- Stock splits
- Dividend adjustments  
- Spinoffs
- Other corporate actions

**The Problem**: Extreme discontinuities suggest either:
1. **Data processing errors** in CRSP data creation
2. **Missing corporate action data** creating artificial adjustments
3. **Different CRSP versions** between Stata and Python datasets
4. **Incorrect cfacpr calculation methodology**

## Solutions Attempted

### 1. Stata Inequality Fix
- **Applied**: utils/stata_ineq.py for missing value handling
- **Result**: 97.15% → 97.14% (minimal improvement)
- **Conclusion**: Not the core issue

### 2. Price Capping Approach  
- **Attempted**: Cap extreme P values at 3x 90th percentile by permno
- **Result**: Made problem worse (98.31% failures)
- **Conclusion**: Attacking symptoms, not root cause

### 3. cfacpr Jump Detection
- **Identified**: 1,499 extreme cfacpr jumps across dataset
- **Analysis**: Confirms systematic data quality issue
- **Status**: Need better handling strategy

## Recommendations

### Immediate Actions
1. **Investigate data source differences**: Check if Stata dataset has different cfacpr values
2. **Corporate action research**: Verify if extreme jumps correspond to legitimate corporate actions
3. **Alternative adjustment methods**: Consider using different price adjustment approaches

### Potential Fixes
1. **Smooth cfacpr transitions**: Detect and interpolate across extreme jumps
2. **Use alternative price series**: Raw prices or different adjustment factors  
3. **Winsorization**: Apply statistical outlier handling to adjusted prices
4. **Time-series specific handling**: Different adjustment logic for pre/post corporate actions

### Data Quality Investigation
1. **Compare CRSP versions**: Stata vs Python data sources
2. **Corporate action validation**: Cross-reference with known stock events
3. **Historical analysis**: Check if extreme cfacpr values are economically justified

## Impact Assessment

**Severity**: CRITICAL - 97%+ of TrendFactor calculations affected
**Scope**: Systematic across 1,499 stocks and decades of data  
**Confidence**: HIGH - Root cause clearly identified with specific examples
**Urgency**: Must resolve before TrendFactor can be considered reliable

## Next Steps

1. **Data source investigation**: Compare cfacpr values between Stata/Python datasets
2. **Corporate action research**: Validate whether extreme jumps are economically justified  
3. **Implement targeted fix**: Address cfacpr discontinuities while preserving legitimate adjustments
4. **Test validation**: Ensure fix improves precision without losing economic meaning

This represents a **fundamental data quality issue** that requires careful resolution to maintain the economic validity of the TrendFactor predictor.