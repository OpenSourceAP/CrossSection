# Stata `merge` Command Translation to Python

## Overview

Stata's `merge` command is fundamental for combining datasets and has specific behavior that must be replicated exactly in Python. **CRITICAL**: Incorrect merge translation can cause significant data loss (e.g., 40% in CompustatAnnual case).

## Stata Merge Types and Pandas Equivalents

### 1. Merge Type Specifications

| Stata | Description | Pandas Equivalent |
|-------|-------------|-------------------|
| `merge 1:1` | One-to-one merge | `pd.merge(..., validate='1:1')` |
| `merge 1:m` | One-to-many merge | `pd.merge(..., validate='1:m')` |
| `merge m:1` | Many-to-one merge | `pd.merge(..., validate='m:1')` |
| `merge m:m` | Many-to-many merge | **AVOID** - Use `joinby` instead |

### 2. Keep Options Translation

| Stata `keep()` | Description | Pandas `how=` |
|----------------|-------------|---------------|
| `keep(master)` | Keep only master dataset obs | `how='left'` + filter `_merge != 'both'` |
| `keep(using)` | Keep only using dataset obs | `how='right'` + filter `_merge != 'both'` |
| `keep(match)` | Keep only matched obs | `how='inner'` |
| `keep(master match)` | Keep master + matched | `how='left'` |
| `keep(using match)` | Keep using + matched | `how='right'` |
| No `keep()` (default) | Keep all observations | `how='outer'` |

## Critical Bug Example: BM.py

**WRONG** (current BM.py:20):
```python
df = pd.merge(m_compustat, signal_master, on=['permno', 'time_avail_m'], how='inner')
```

**CORRECT** translation of Stata line:
```stata
merge 1:1 permno time_avail_m using SignalMasterTable, keep(using match)
```

Should be:
```python
df = pd.merge(m_compustat, signal_master, on=['permno', 'time_avail_m'], how='right', validate='1:1')
```

## Complete Translation Pattern

### Stata:
```stata
use dataset1, clear
merge 1:1 id using dataset2, keep(using match) nogenerate keepusing(var1 var2)
```

### Python:
```python
# Load datasets
dataset1 = pd.read_parquet('dataset1.parquet')
dataset2 = pd.read_parquet('dataset2.parquet')[['id', 'var1', 'var2']]  # keepusing equivalent

# Merge with validation
df = pd.merge(dataset1, dataset2, on='id', how='right', validate='1:1')
# No need for nogenerate equivalent - pandas doesn't create _merge by default
```

## _merge Variable Behavior

Stata automatically creates `_merge` with values:
- `_merge == 1`: master only
- `_merge == 2`: using only  
- `_merge == 3`: matched

To replicate in Python (if needed):
```python
df = pd.merge(left_df, right_df, on='id', how='outer', indicator='_merge')
# _merge values: 'left_only', 'right_only', 'both'
```

## Common Translation Mistakes

### ❌ WRONG: Default to inner join
```python
df = pd.merge(df1, df2, on='id')  # Default how='inner'
```

### ❌ WRONG: Ignore validation
```python
df = pd.merge(df1, df2, on='id', how='left')  # No validate parameter
```

### ✅ CORRECT: Explicit translation
```python
df = pd.merge(df1, df2, on='id', how='right', validate='1:1')  # keep(using match) + 1:1 validation
```

## Key Translation Rules

1. **Always specify `how=`** - Never rely on pandas defaults
2. **Always add `validate=`** - Prevents silent data corruption
3. **Match `keep()` options exactly** - Each option has a specific pandas equivalent
4. **Preserve observation counts** - Validate that Python output has correct number of rows
5. **Handle `keepusing()`** - Filter columns before merge, not after

## Testing Merge Translations

After translating any merge:
1. **Count check**: Python observations should match expected Stata behavior
2. **Validation**: Use `validate=` parameter to catch unexpected cardinality
3. **Column check**: Ensure correct columns are kept/dropped
4. **Row check**: Verify which observations are retained vs. dropped

## Emergency Checklist for Merge Bugs

If you suspect a merge translation bug:
1. ✅ Check the Stata `keep()` option
2. ✅ Verify pandas `how=` parameter matches
3. ✅ Add `validate=` parameter
4. ✅ Count observations before/after merge
5. ✅ Run validation script to compare with Stata output