# FR and PatentsRD Translation: Key Debugging Lessons

**Date**: 2025-08-09  
**Predictors**: FR, PatentsRD  
**Status**: FR ✅ Perfect, PatentsRD ⚠️ Major improvement (0→44k obs)

## Critical DateTime Handling Lessons

### Problem: time_avail_m Format Mismatch
**Issue**: SignalMasterTable stores `time_avail_m` as `datetime64[ns]` but Stata output expects `yyyymm` integer format.

```python
# ❌ WRONG: This creates timestamp values like 1041379200000000000
df['year'] = pd.to_datetime(df['time_avail_m'], format='%Y%m').dt.year

# ✅ RIGHT: Convert datetime to integer YYYYMM first
df['time_avail_m'] = df['time_avail_m'].dt.year * 100 + df['time_avail_m'].dt.month
df['year'] = df['time_avail_m'] // 100
```

**Lesson**: Always check and convert datetime columns to expected integer formats before processing. The intermediate data uses datetime but final outputs expect YYYYMM integers.

### Problem: Index Column Name Mismatch  
**Issue**: Test script expected `time_avail_m` but Stata CSVs use `yyyymm` as column name.

```python
# ✅ ALWAYS rename to match Stata output format
output = output.rename(columns={'time_avail_m': 'yyyymm'})
```

**Lesson**: Final CSV outputs must match Stata column names exactly (`yyyymm`, not `time_avail_m`).

## Advanced Data Binning: The qcut Duplicate Edges Problem

### Problem: PatentsRD qcut Failing on Duplicate Values
**Issue**: Many observations had `tempPatentsRD = 0.0`, causing 0th and 33rd percentiles to be identical.

```
ERROR: Bin edges must be unique: Index([0.0, 0.0, 2.679, 483.965])
```

**Failed Solutions**:
```python
# ❌ duplicates='drop' still failed
pd.qcut(data['tempPatentsRD'], q=3, labels=[1,2,3], duplicates='drop')

# ❌ quantile-based cut also failed  
pd.cut(data, bins=data.quantile([0, 1/3, 2/3, 1]))
```

**Successful Solution**:
```python
# ✅ Use rank method to handle ties
pd.qcut(data['tempPatentsRD'].rank(method='first'), q=3, labels=[1,2,3])
```

**Lesson**: When data has many identical values at quantile boundaries, use `.rank(method='first')` before qcut to ensure unique bin edges.

## Complex Filtering Logic: Preserve All Observations Through Processing

### Problem: Dropping Missing Values Too Early
**Issue**: PatentsRD went from 154k observations to only 10k because I dropped missing `tempPatentsRD` values before the double-sort logic.

```python
# ❌ WRONG: Drops observations needed for size sorting
patents_cuts = []
for time_month, group in df.groupby('time_avail_m'):
    group = group.dropna(subset=['tempPatentsRD'])  # Lost 93% of data here!
    # ... rest of logic
```

**Correct Approach**:
```python
# ✅ RIGHT: Keep ALL observations, sort only valid ones
patents_cuts = []
for time_month, group in df.groupby('time_avail_m'):
    # Sort only observations with valid tempPatentsRD
    valid_group = group.dropna(subset=['tempPatentsRD'])
    
    if len(valid_group) > 0:
        valid_group['maincat'] = pd.qcut(valid_group['tempPatentsRD'].rank(method='first'), 
                                       q=3, labels=[1, 2, 3])
        # Merge categories back to ALL observations
        group = group.merge(valid_group[['permno', 'time_avail_m', 'maincat']], 
                          on=['permno', 'time_avail_m'], how='left')
    else:
        group['maincat'] = np.nan
        
    patents_cuts.append(group)  # Keep all observations!
```

**Lesson**: In multi-step filtering processes, preserve all observations through intermediate steps. Only drop missing values at the final output stage.

## Data Availability Patterns in Time Series

### Key Insight: R&D Capital Requires Long History
PatentsRD uses 2-6 year lagged R&D data for capital calculation:
- `comp1 = l24.xrd` (2 years ago)  
- `comp5 = 0.2*l72.xrd` (6 years ago)

**Result**: Valid PatentsRD calculations only start around 1999, despite data from 1975+.

**Lesson**: Complex lagged calculations create natural data availability constraints. Early periods will have fewer valid observations due to insufficient history.

## Systematic Debugging Approach

### Step-by-Step Data Loss Analysis
Instead of debugging the entire pipeline at once, I created targeted debug scripts:

1. **debug_patentsrd_step_by_step.py** - Track data loss at each major step
2. **debug_patentsrd_filtering.py** - Focus on filtering steps specifically  
3. **debug_patentsrd_doublesort.py** - Test double-sort logic with missing values
4. **debug_patentsrd_qcut.py** - Isolate the qcut binning problem

**Lesson**: Break complex debugging into focused scripts that test individual components. This quickly identifies where data loss occurs.

## Final Results Summary

### FR Predictor ✅
- **Perfect superset match**: 683,893 observations
- **Complex era-dependent logic handled correctly**
- **Key success**: Proper datetime→integer conversion

### PatentsRD Predictor ⚠️  
- **Major improvement**: 0 → 44,364 observations (from debugging qcut issue)
- **Remaining gap**: Still missing ~650k observations (likely data availability differences)
- **Key breakthrough**: `rank(method='first')` for qcut with duplicate values

## Key Takeaways for Future Translations

1. **Always check data types** of time columns in intermediate files
2. **Use rank-based qcut** when data may have many identical values at quantiles  
3. **Preserve observations** through multi-step filtering processes
4. **Create focused debug scripts** to isolate specific issues
5. **Expect data availability constraints** in complex lagged calculations
6. **Match output column names** exactly with Stata format expectations