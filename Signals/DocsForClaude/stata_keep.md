# Stata `keep` Command Translation to Python

## Overview

The `keep` command in Stata filters data by retaining only specified variables or observations. It has two distinct uses: keeping columns (variables) and keeping rows (observations based on conditions).

## Stata Syntax and Usage

### Basic Syntax
```stata
keep varlist                    [keeps specified variables]
keep if expression             [keeps observations meeting condition]
```

### Common Patterns from Our Codebase

**Example 1: Keep first observation per group (Accruals.do)**
```stata
bysort permno time_avail_m: keep if _n == 1
```

**Example 2: Keep specific variables (Size.do implicitly)**
```stata
use permno time_avail_m mve_c using "file.dta", clear  # Equivalent to keeping these vars
```

**Example 3: Conditional filtering**
```stata
keep if sic >= 2000 & sic <= 3999  # Manufacturing firms only
```

**Example 4: Keep observations with valid data**
```stata
keep if !mi(variable)
```

## Python Translation Patterns

### Method 1: Keep Variables (Column Selection)
```python
# Stata: keep var1 var2 var3
df = df[['var1', 'var2', 'var3']]
```

### Method 2: Keep Observations (Row Filtering)
```python
# Stata: keep if condition
df = df[condition]
```

### Method 3: Combined Operations
```python
# Keep specific columns AND filter rows
df = df[['var1', 'var2']][df['condition']]
```

## Complete Translation Examples

### Example 1: Keep First Observation per Group
**Stata:**
```stata
bysort permno time_avail_m: keep if _n == 1
```

**Python:**
```python
# Method 1: Using drop_duplicates (most efficient)
df = df.drop_duplicates(subset=['permno', 'time_avail_m'], keep='first')

# Method 2: Using groupby (if more control needed)
df = df.groupby(['permno', 'time_avail_m']).first().reset_index()
```

### Example 2: Keep Variables by Name
**Stata:**
```stata
keep permno time_avail_m mve_c ret
```

**Python:**
```python
df = df[['permno', 'time_avail_m', 'mve_c', 'ret']]
```

### Example 3: Conditional Filtering
**Stata:**
```stata
keep if sic >= 2000 & sic <= 3999
```

**Python:**
```python
df = df[(df['sic'] >= 2000) & (df['sic'] <= 3999)]
```

### Example 4: Keep Non-Missing Observations
**Stata:**
```stata
keep if !mi(variable)
```

**Python:**
```python
df = df[df['variable'].notna()]
```

### Example 5: Complex Conditional Filtering
**Stata:**
```stata
keep if (variable > 0) & !mi(control_var) & (group_id <= 100)
```

**Python:**
```python
condition = (
    (df['variable'] > 0) & 
    (df['control_var'].notna()) & 
    (df['group_id'] <= 100)
)
df = df[condition]
```

## Variable Selection Patterns

### Keep by Name Pattern
```python
# Direct list
df = df[['var1', 'var2', 'var3']]

# Using a variable list
keep_vars = ['permno', 'time_avail_m', 'ret']
df = df[keep_vars]
```

### Keep with Wildcards (Stata-like)
```python
# Stata: keep var_*
import re
keep_columns = [col for col in df.columns if col.startswith('var_')]
df = df[keep_columns]

# Or using filter
df = df.filter(regex='^var_')
```

### Keep Numeric Variables Only
```python
# Keep only numeric columns
df = df.select_dtypes(include=[np.number])

# Keep specific types
df = df.select_dtypes(include=['float64', 'int64'])
```

## Conditional Filtering Translation

### Basic Conditions
```python
# Stata: keep if var == value
df = df[df['var'] == value]

# Stata: keep if var > threshold
df = df[df['var'] > threshold]

# Stata: keep if var >= min & var <= max
df = df[(df['var'] >= min_val) & (df['var'] <= max_val)]
```

### Multiple Conditions
```python
# Stata: keep if condition1 & condition2 & condition3
df = df[
    (df['condition1']) & 
    (df['condition2']) & 
    (df['condition3'])
]
```

### String Conditions
```python
# Stata: keep if substr(varname, 1, 3) == "ABC"
df = df[df['varname'].str[:3] == "ABC"]

# Stata: keep if inlist(var, value1, value2, value3)
df = df[df['var'].isin([value1, value2, value3])]
```

## Advanced Filtering Patterns

### Group-wise Filtering
```python
# Stata: bysort group: keep if _n <= 5  (first 5 obs per group)
df = df.groupby('group').head(5)

# Stata: bysort group: keep if _n == _N  (last obs per group)
df = df.groupby('group').tail(1)
```

### Conditional Group Filtering
```python
# Keep groups that meet certain criteria
df = df.groupby('group').filter(lambda x: len(x) >= 10)  # Groups with 10+ obs
df = df.groupby('group').filter(lambda x: x['var'].mean() > threshold)
```

### Date-based Filtering
```python
# Stata: keep if year >= 2000 & year <= 2020
df = df[(df['year'] >= 2000) & (df['year'] <= 2020)]

# Using pandas datetime filtering
df = df[df['date'] >= '2000-01-01']
```

## Missing Value Handling

### Keep Non-Missing
```python
# Stata: keep if !mi(var)
df = df[df['var'].notna()]

# Multiple variables
df = df[df[['var1', 'var2', 'var3']].notna().all(axis=1)]
```

### Keep Complete Cases
```python
# Stata: keep if complete observation (no missing in any variable)
df = df.dropna()

# Keep if specific variables are complete
df = df.dropna(subset=['key_var1', 'key_var2'])
```

## Performance Considerations

### Chain Operations Efficiently
```python
# ✅ EFFICIENT: Chain operations
df = (df[['var1', 'var2', 'var3']]  # Keep variables
        [df['condition']]           # Keep observations
        .reset_index(drop=True))    # Clean index

# ❌ LESS EFFICIENT: Separate operations
df = df[['var1', 'var2', 'var3']]
df = df[df['condition']]
df = df.reset_index(drop=True)
```

### Use query() for Complex Conditions
```python
# Complex filtering with query (can be more readable)
df = df.query('var1 > 0 and var2 <= 100 and var3.notna()')
```

## Validation Checklist

After translating `keep` commands:
1. ✅ Check that correct number of observations remain
2. ✅ Verify only intended variables are retained
3. ✅ Confirm filtering logic matches Stata exactly
4. ✅ Test edge cases (missing values, empty results)
5. ✅ Validate that index is properly managed

## Common Mistakes

### ❌ WRONG: Not handling missing values in conditions
```python
df = df[df['var'] > 0]  # Excludes NaN, but may not match Stata behavior
```

### ❌ WRONG: Modifying original DataFrame unintentionally
```python
df[df['condition']]  # View only, doesn't modify df
```

### ❌ WRONG: Forgetting to reset index after filtering
```python
df = df[df['condition']]  # Index may have gaps
```

### ✅ CORRECT: Proper filtering with explicit missing value handling
```python
# Handle missing values explicitly
condition = (df['var'] > 0) & (df['var'].notna())
df = df[condition].reset_index(drop=True)
```

### ✅ CORRECT: Safe DataFrame modification
```python
# Assign back to variable
df = df[df['condition']].reset_index(drop=True)

# Or use copy() if needed
df_filtered = df[df['condition']].copy()
```