# Fastxtile Migration Inventory & Fix Instructions

**Date**: 2025-08-10  
**Context**: Comprehensive audit of fastxtile usage across all predictors after creating robust `utils/stata_fastxtile.py`

## Summary

Found **25 total predictors** using fastxtile-related operations. Only 4 currently use the new standardized utility, leaving **21 predictors with inline/custom implementations** that should be migrated.

## Migration Status

### ✅ Already Migrated (4/25)
- **PS** - Switched to `fastxtile(df, 'BM', by='time_avail_m', n=5)`
- **DivYieldST** - Switched from 28-line custom tercile function to simple fastxtile call
- **RDAbility** - Converted polars tercile logic to pandas fastxtile hybrid
- **NetDebtPrice** - Already using `fastxtile_by_group()` legacy interface

### 🔄 High-Priority Migration Candidates (12/25)

**Immediate Impact (High precision errors):**
1. **AccrualsBM** - 49.01% precision error, has custom fastxtile function
2. **MS** - 63.49% precision error, complex polars BM quintile ranking
3. **MomVol** - 0.42% precision error, custom fastxtile + transforms

**Easy Wins (Low complexity):**
4. **ChNAnalyst** - 0.01% precision error, simple fastxtile quintile function
5. **IndRetBig** - Simple fastxtile patterns
6. **EarnSupBig** - Standard fastxtile patterns
7. **PatentsRD** - Standard fastxtile patterns
8. **ChForecastAccrual** - 0.12% precision error, standard patterns
9. **Activism1** - Standard patterns
10. **tang** - Standard patterns
11. **OperProf** - Standard patterns
12. **ProbInformedTrading** - Standard patterns

**Complex Cases (Require careful review):**
13. **CitationsRD** - 0.00% precision (perfect), complex custom tercile logic
14. **FirmAgeMom** - Complex logic, needs analysis
15. **ZZ1_RIO_*** - Multi-predictor file, complex patterns
16. **TrendFactor** - Complex patterns

### 📊 Already Perfect (5/25)
These use inline patterns but have 0.00% precision errors - validate they maintain performance:
- **MomRev** - Uses inline `pd.qcut` with infinite handling (no utility import)
- **OScore** - Uses inline `pd.qcut` in `safe_qcut` function
- **CitationsRD** - Complex but perfect custom implementation
- **NetDebtPrice** - Already using utility, perfect performance
- **Other perfect predictors** - Maintain current implementations if working

## Standard Migration Pattern

### Before (Typical Inline Implementation):
```python
# Custom fastxtile function
def fastxtile(series, n_quantiles=5):
    try:
        series_clean = series.replace([np.inf, -np.inf], np.nan)
        return pd.qcut(series_clean, q=n_quantiles, labels=False, duplicates='drop') + 1
    except:
        return pd.Series(np.nan, index=series.index)

# Usage
df['quintile'] = df.groupby('time_avail_m')['variable'].transform(lambda x: fastxtile(x, 5))
```

### After (Standardized Implementation):
```python
# Import
from utils.stata_fastxtile import fastxtile

# Usage - single line
df['quintile'] = fastxtile(df, 'variable', by='time_avail_m', n=5)
```

## Step-by-Step Migration Instructions

### 1. Import Statement
```python
# Add this import at the top
from utils.stata_fastxtile import fastxtile
```

### 2. Remove Custom Functions
Delete any inline `fastxtile()`, `safe_qcut()`, or similar custom quantile functions.

### 3. Replace Usage Patterns

**Pattern A: Group-wise transforms**
```python
# OLD:
df['quintile'] = df.groupby('group')['var'].transform(lambda x: custom_fastxtile(x, 5))

# NEW:
df['quintile'] = fastxtile(df, 'var', by='group', n=5)
```

**Pattern B: Simple quintiles**
```python
# OLD:
df['quintile'] = custom_fastxtile(df['var'], 5)

# NEW:  
df['quintile'] = fastxtile(df, 'var', n=5)
```

**Pattern C: Manual infinite handling**
```python
# OLD:
df['var_clean'] = df['var'].replace([np.inf, -np.inf], np.nan)
df['quintile'] = df.groupby('group')['var_clean'].transform(lambda x: pd.qcut(x, q=5, labels=False, duplicates='drop') + 1)

# NEW:
df['quintile'] = fastxtile(df, 'var', by='group', n=5)  # Infinite handling automatic
```

### 4. Polars-Pandas Hybrid (for polars-heavy predictors)
```python
# For predictors using polars but needing fastxtile
df_pandas = df.select(['var', 'group']).to_pandas()
df_pandas['quintile'] = fastxtile(df_pandas, 'var', by='group', n=5)
df = df.with_columns(pl.Series(df_pandas['quintile']).alias('quintile'))
```

## Validation Checklist

After each migration:
1. ✅ **Import check**: Verify `from utils.stata_fastxtile import fastxtile` works
2. ✅ **Syntax check**: Verify new fastxtile calls use correct parameters
3. ✅ **Remove old code**: Delete custom fastxtile/quantile functions
4. ✅ **Test run**: Execute predictor script to check for errors
5. ✅ **Output check**: Verify output file is generated successfully
6. ✅ **Precision test**: Run validation to check precision didn't degrade

## Expected Benefits

**Performance Improvements:**
- **AccrualsBM**: 49.01% → Expected <5% precision error
- **MS**: 63.49% → Expected <10% precision error  
- **MomVol**: 0.42% → Expected <0.1% precision error

**Code Quality:**
- **Eliminate 20+ custom implementations** → 1 robust utility
- **Consistent infinite value handling** across all predictors
- **Reduced maintenance burden** and debugging complexity
- **Better Stata matching** using proven patterns

## Implementation Priority

### Phase 1: High-Impact (Week 1)
1. **AccrualsBM** - Highest precision error (49.01%)
2. **MS** - Second highest precision error (63.49%)
3. **MomVol** - Moderate precision error (0.42%)

### Phase 2: Easy Wins (Week 2)  
4. **ChNAnalyst** - Simple case, near-perfect already (0.01%)
5. **ChForecastAccrual** - Simple case (0.12%)
6. **Standard pattern predictors** (6-8 remaining)

### Phase 3: Complex Cases (Week 3)
7. **CitationsRD** - Perfect but complex (validate no regression)
8. **FirmAgeMom** - Complex logic
9. **ZZ1_RIO_*** - Multi-predictor files

## Notes

- **Perfect predictors**: Leave unchanged unless migration provides clear benefit
- **Complex custom logic**: Review carefully to ensure no functionality loss
- **Polars predictors**: Use hybrid pandas approach for fastxtile operations
- **Testing**: Always validate output after migration
- **Backup**: Keep original implementations commented until validation complete

## Success Metrics

- **Code reduction**: ~500+ lines of duplicate fastxtile code eliminated
- **Precision improvement**: Target <1% precision error for all migrated predictors
- **Maintenance**: Single source of truth for fastxtile operations
- **Consistency**: All predictors use same infinite value handling approach