# Fastxtile Coding Standards

**Document Version**: 1.0  
**Created**: 2025-08-10  
**Purpose**: Comprehensive standards for fastxtile implementation to achieve >90% predictor success rate

## Executive Summary

This document establishes coding standards for fastxtile operations based on systematic analysis of predictor failures and successes. The enhanced `utils/stata_fastxtile.py` utility addresses the root cause of fastxtile issues: **infinite value handling**, which affected 6+ predictors including PS (17.88% precision1 error).

### Key Findings from Analysis
- **#1 Root Cause**: Infinite values from financial ratios (log of negative/zero values)  
- **Success Pattern**: Explicit infinite cleaning + pd.qcut approach (MomRev: 0.00% precision1)
- **Utility Enhancement**: Comprehensive edge case handling now supports all identified scenarios

## 1. When to Use utils/stata_fastxtile.py vs Inline

### ✅ Use Enhanced Utility (RECOMMENDED)
Use `from utils.stata_fastxtile import fastxtile` for:

- **All new predictors** (standardization and consistency)
- **Group-wise fastxtile operations** (`by='time_avail_m'` pattern)
- **Financial ratios with potential infinites** (BM, leverage, profitability ratios)
- **Predictors currently failing precision tests** (PS, MS, etc.)
- **Any predictor requiring >90% precision standards**

```python
# PREFERRED PATTERN - Enhanced utility
from utils.stata_fastxtile import fastxtile

# Simple case
df['quintile'] = fastxtile(df, 'variable', n=5)

# Group-wise (most common)
df['quintile'] = fastxtile(df, 'variable', by='time_avail_m', n=5)

# Multiple groups
df['quintile'] = fastxtile(df, 'variable', by=['time_avail_m', 'industry'], n=5)
```

### ⚠️ Keep Inline Only If
Keep existing inline implementations only if:

- **Already achieving 0.00% precision1** (MomRev, OScore patterns)
- **Simple, well-tested implementation** with proven success
- **No future changes expected** to the predictor logic

```python
# EXISTING SUCCESS PATTERN - Can keep if working
df['var_clean'] = df['var'].replace([np.inf, -np.inf], np.nan)
df['quintile'] = df.groupby('time_avail_m')['var_clean'].transform(
    lambda x: pd.qcut(x, q=5, labels=False, duplicates='drop') + 1
)
```

## 2. Mandatory Infinite Value Pre-processing

### Critical Rule: Always Handle Infinites First

**ALL financial ratio calculations MUST include infinite value handling:**

```python
# ❌ WRONG - Direct calculation without infinite handling
df['BM'] = np.log(df['ceq'] / df['mve_c'])
df['quintile'] = some_fastxtile_function(df['BM'])  # WILL FAIL

# ✅ RIGHT - Enhanced utility handles infinites automatically  
df['BM'] = np.log(df['ceq'] / df['mve_c'])  # May contain inf, -inf, NaN
df['quintile'] = fastxtile(df, 'BM', by='time_avail_m', n=5)  # Robust handling

# ✅ ALTERNATIVE - Explicit cleaning if using inline
df['BM'] = np.log(df['ceq'] / df['mve_c'])
df['BM_clean'] = df['BM'].replace([np.inf, -np.inf], np.nan)
df['quintile'] = df.groupby('time_avail_m')['BM_clean'].transform(
    lambda x: pd.qcut(x, q=5, labels=False, duplicates='drop') + 1
)
```

### Common Infinite-Generating Patterns

**1. Log of Division (BM calculation)**
```python
# Generates -inf when ceq/mve_c ≤ 0, NaN when ceq/mve_c < 0
df['BM'] = np.log(df['ceq'] / df['mve_c'])
```

**2. Division by Zero (Leverage ratios)**
```python
# Generates inf when denominator = 0
df['leverage'] = df['debt'] / df['assets']
```

**3. Percentage Changes**
```python
# Generates inf when denominator = 0
df['growth'] = (df['current'] - df['lagged']) / df['lagged']
```

**4. Safe Math Functions Pattern**
Following OScore success pattern:
```python
def safe_divide(a, b):
    return np.where((b == 0) | b.isna(), np.nan, a / b)

def safe_log(x):
    return np.where((x <= 0) | x.isna(), np.nan, np.log(x))

# Use these for complex calculations
df['ratio'] = safe_divide(df['numerator'], df['denominator'])
df['log_ratio'] = safe_log(df['ratio'])
```

## 3. Standard Group-wise Fastxtile Patterns

### Primary Pattern: Time-based Grouping
Most predictors use monthly time-based grouping:

```python
# STANDARD PATTERN - Monthly quintiles
df['quintile'] = fastxtile(df, 'variable', by='time_avail_m', n=5)

# Keep only specific quintiles (common pattern)
df.loc[df['quintile'] != 5, 'variable'] = np.nan  # Keep only highest quintile
```

### Multi-dimensional Grouping
For predictors requiring industry or size controls:

```python
# Industry and time-based
df['quintile'] = fastxtile(df, 'variable', by=['time_avail_m', 'industry'], n=5)

# Size-based sub-grouping
df['size_group'] = fastxtile(df, 'mve_c', by='time_avail_m', n=3)  # Size terciles
df['quintile'] = fastxtile(df, 'variable', by=['time_avail_m', 'size_group'], n=5)
```

### Conditional Quintiles Pattern
For predictors with universe restrictions:

```python
# BM-restricted universe (PS predictor pattern)
df['BM'] = np.log(df['ceq'] / df['mve_c'])
df['BM_quintile'] = fastxtile(df, 'BM', by='time_avail_m', n=5)

# Apply signal only to highest BM quintile
df['PS'] = calculate_piotroski_score(df)  # Your signal calculation
df.loc[df['BM_quintile'] != 5, 'PS'] = np.nan  # Restrict universe
```

## 4. Validation Checklist for Fastxtile Implementations

### Pre-Implementation Checklist

- [ ] **Data Review**: Identify potential infinite-generating calculations
- [ ] **Utility Decision**: Use enhanced utility vs proven inline approach
- [ ] **Variable Cleaning**: Handle negative values in log calculations
- [ ] **Group Structure**: Verify adequate observations per group
- [ ] **Edge Cases**: Test with empty/small groups

### Post-Implementation Checklist

- [ ] **Infinite Test**: Verify infinites become NaN in output
- [ ] **Distribution Test**: Check reasonable quintile distributions
- [ ] **Group Test**: Verify each time group has expected quintiles
- [ ] **Edge Case Test**: Test with problematic data (zeros, negatives, missing)
- [ ] **Precision Test**: Run against Stata output if available

### Standard Test Code Template

```python
# VALIDATION TEMPLATE - Include in every predictor
print("🧪 Fastxtile Validation:")
print(f"Variable stats: min={df['variable'].min():.3f}, max={df['variable'].max():.3f}")
print(f"Infinite values: +inf={np.isposinf(df['variable']).sum()}, -inf={np.isneginf(df['variable']).sum()}")
print(f"Quintile distribution:\n{df['quintile'].value_counts().sort_index()}")
print(f"Missing quintiles: {df['quintile'].isna().sum()}")
```

## 5. Common Pitfalls and Solutions

### Pitfall 1: Ignoring Infinite Values
**Problem**: Direct use of financial ratios without cleaning
```python
# ❌ WRONG
df['BM'] = np.log(df['ceq'] / df['mve_c'])
df['quintile'] = df.groupby('time_avail_m')['BM'].transform(lambda x: pd.qcut(x, q=5, labels=False) + 1)
# Fails with ValueError when BM contains inf
```

**Solution**: Use enhanced utility or explicit cleaning
```python
# ✅ RIGHT
df['quintile'] = fastxtile(df, 'BM', by='time_avail_m', n=5)  # Handles infinites
```

### Pitfall 2: Small Group Failures
**Problem**: qcut fails when insufficient observations
```python
# ❌ WRONG - Fails when groups have < n observations
df['quintile'] = df.groupby('time_avail_m')['variable'].transform(
    lambda x: pd.qcut(x, q=5, labels=False) + 1  # Crashes on small groups
)
```

**Solution**: Enhanced utility handles this automatically
```python
# ✅ RIGHT - Robust handling of small groups
df['quintile'] = fastxtile(df, 'variable', by='time_avail_m', n=5)
```

### Pitfall 3: Inconsistent Missing Data Handling
**Problem**: Different NaN handling across predictors
```python
# ❌ INCONSISTENT
# Some predictors drop NaN first, others don't
df_clean = df.dropna(subset=['variable'])  # Sometimes done, sometimes not
df['quintile'] = fastxtile_function(df_clean['variable'])
```

**Solution**: Standardized NaN handling in utility
```python
# ✅ CONSISTENT - Utility handles NaN consistently
df['quintile'] = fastxtile(df, 'variable', by='time_avail_m', n=5)
```

### Pitfall 4: Integer vs Float Indexing Issues
**Problem**: Inconsistent 0-based vs 1-based indexing
```python
# ❌ WRONG - pd.qcut returns 0-based, forgot to add 1
df['quintile'] = df.groupby('time_avail_m')['variable'].transform(
    lambda x: pd.qcut(x, q=5, labels=False)  # Returns 0,1,2,3,4
)
```

**Solution**: Utility ensures consistent 1-based indexing
```python
# ✅ RIGHT - Always 1,2,3,4,5 like Stata
df['quintile'] = fastxtile(df, 'variable', by='time_avail_m', n=5)
```

## 6. Migration Guidelines

### Priority Order for Migration to Enhanced Utility

**High Priority** (Immediate migration recommended):
1. **PS** (17.88% precision1) - BM quintile restriction
2. **MS** (63.49% precision1) - Market share calculation  
3. **Predictors using financial ratios** with known infinite issues
4. **Any predictor failing precision tests**

**Medium Priority** (Consider migration):
1. **Complex fastxtile operations** with multiple grouping variables
2. **Predictors with frequent edge case issues**
3. **New predictors under development**

**Low Priority** (Keep existing if working):
1. **Perfect performers** (MomRev 0.00%, OScore 0.00%)
2. **Simple inline implementations** with proven stability
3. **Predictors rarely modified**

### Migration Process

1. **Backup Current Implementation**
   ```python
   # Save copy of working version before changes
   cp Predictors/PS.py Predictors/PS_backup.py
   ```

2. **Replace Fastxtile Logic**
   ```python
   # OLD
   df['var_clean'] = df['var'].replace([np.inf, -np.inf], np.nan)
   df['quintile'] = df.groupby('time_avail_m')['var_clean'].transform(
       lambda x: pd.qcut(x, q=5, labels=False, duplicates='drop') + 1
   )
   
   # NEW
   from utils.stata_fastxtile import fastxtile
   df['quintile'] = fastxtile(df, 'var', by='time_avail_m', n=5)
   ```

3. **Test Migration**
   ```python
   # Validate output matches expected
   python3 Predictors/PS.py
   python3 utils/test_fastxtile_comprehensive.py
   ```

4. **Run Precision Test**
   ```python
   # Check improvement in precision scores
   # Target: <1% precision1 error after migration
   ```

## 7. Advanced Usage Patterns

### Multiple Quantile Calculations
When predictors need multiple quantile variables:

```python
# Efficient multiple quantile calculation
df['quintile_5'] = fastxtile(df, 'variable', by='time_avail_m', n=5)
df['decile_10'] = fastxtile(df, 'variable', by='time_avail_m', n=10)
df['tercile_3'] = fastxtile(df, 'variable', by='time_avail_m', n=3)
```

### Conditional Quantiles with Universe Restrictions
Following successful NetDebtPrice pattern:

```python
# Calculate BM quintiles for universe restriction
df['BM'] = np.log(df['ceq'] / df['mve_c'])
df['BM_quintile'] = fastxtile(df, 'BM', by='time_avail_m', n=5)

# Calculate signal
df['signal'] = calculate_signal(df)

# Apply universe restriction (keep only top 3 BM quintiles)
df.loc[df['BM_quintile'] <= 2, 'signal'] = np.nan
```

### Series Input for Non-DataFrame Cases
When working with Series directly:

```python
# Series input (no grouping)
quintiles = fastxtile(data_series, n=5)

# With DataFrame context for grouping
quintiles = fastxtile(df, 'variable', by='group_col', n=5)
```

## 8. Debugging and Troubleshooting

### Common Error Messages and Solutions

**Error**: `ValueError: Unable to select bins with quantiles`
```python
# Usually caused by insufficient unique values
# Enhanced utility handles this automatically
```

**Error**: `ValueError: Bin edges must be unique`
```python
# Caused by too many identical values
# Use duplicates='drop' or enhanced utility
```

**Error**: `All values are NaN`
```python
# Check data quality and infinite value handling
# Verify input data has finite values
```

### Debug Information Template
```python
def debug_fastxtile_input(df, variable, by=None):
    """Debug helper for fastxtile issues"""
    print(f"🔍 Debugging fastxtile input for '{variable}':")
    print(f"  Total observations: {len(df)}")
    print(f"  Non-null values: {df[variable].notna().sum()}")
    print(f"  Unique values: {df[variable].nunique()}")
    print(f"  Infinite values: {np.isinf(df[variable]).sum()}")
    print(f"  Min/Max: {df[variable].min():.3f} / {df[variable].max():.3f}")
    
    if by is not None:
        group_stats = df.groupby(by)[variable].agg(['count', 'nunique'])
        print(f"  Groups with < 5 observations: {(group_stats['count'] < 5).sum()}")
        print(f"  Groups with < 2 unique values: {(group_stats['nunique'] < 2).sum()}")
```

## 9. Performance Considerations

### Benchmarking Results
Based on comprehensive testing:

- **Large datasets**: 10,000 observations processed in ~0.07 seconds
- **Success rate**: 100% on well-formed data, robust error handling on problematic data
- **Memory usage**: Minimal overhead compared to inline implementations
- **Group-wise scalability**: Handles 100+ groups efficiently

### Optimization Tips

1. **Pre-filter data** if possible to reduce processing overhead
2. **Use appropriate n** - don't request 10 deciles for small groups
3. **Minimize grouping variables** - fewer groups = better performance
4. **Cache results** if reusing same quantile assignments

## 10. Future Enhancements

### Planned Improvements

1. **Stata tie-breaking exact matching** - Further refinement of tie-breaking rules
2. **Performance optimization** for very large datasets (>1M observations)
3. **Additional safe math functions** for specialized financial calculations
4. **Logging integration** for better debugging support

### Contributing Guidelines

When enhancing the utility:

1. **All changes must pass comprehensive test suite**
2. **Backward compatibility is mandatory**
3. **Add tests for new edge cases**
4. **Update documentation for new features**
5. **Benchmark performance impact**

---

## Summary

The enhanced `utils/stata_fastxtile.py` utility and these coding standards address the root cause of fastxtile failures across the predictor ecosystem. By following these standards, predictors should achieve >90% success rates and consistent behavior across all financial data scenarios.

**Key Success Factors**:
- Use enhanced utility for all new implementations
- Always handle infinite values properly
- Follow standard group-wise patterns
- Validate implementations thoroughly
- Migrate problematic predictors systematically

For questions or issues, refer to the comprehensive test suite and debug patterns provided in this document.