# Stata `mi()` Function Translation to Python

## Overview

The `mi()` function (short for `missing()`) in Stata checks whether values are missing. It returns 1 if the value is missing, 0 if not missing. This function is essential for conditional operations and data cleaning.

## Stata Syntax and Usage

### Basic Syntax
```stata
mi(varname)                    [checks single variable]
missing(varname)               [equivalent to mi()]
mi(var1, var2, var3)          [checks if ANY variable is missing]
```

### Common Patterns from Our Codebase

**Example 1: Replace missing with default value (Accruals.do)**
```stata
replace tempTXP = 0 if mi(txp)
```

**Example 2: Conditional operations excluding missing (BM.do)**
```stata
replace me_datadate = . if l6.time_avail_m != mofd(datadate)
```

**Example 3: Keep non-missing observations**
```stata
keep if !mi(variable)
```

**Example 4: Complex conditions with missing checks (tang.do)**
```stata
replace FC = 0 if tempFC >=8 & !mi(tempFC)
```

**Example 5: Multiple variable missing check**
```stata
drop if mi(var1) | mi(var2) | mi(var3)
```

## Python Translation Patterns

### Method 1: Single Variable Missing Check
```python
# Stata: mi(var)
df['var'].isna()     # Returns Boolean Series
df['var'].isnull()   # Equivalent to isna()
```

### Method 2: Negation (Not Missing)
```python
# Stata: !mi(var)
df['var'].notna()    # Returns Boolean Series  
df['var'].notnull()  # Equivalent to notna()
```

### Method 3: Multiple Variable Missing Check
```python
# Stata: mi(var1, var2, var3) - ANY missing
df[['var1', 'var2', 'var3']].isna().any(axis=1)

# Stata: mi(var1) & mi(var2) & mi(var3) - ALL missing
df[['var1', 'var2', 'var3']].isna().all(axis=1)
```

## Complete Translation Examples

### Example 1: Replace Missing with Default
**Stata:**
```stata
replace tempTXP = 0 if mi(txp)
```

**Python:**
```python
df.loc[df['txp'].isna(), 'tempTXP'] = 0
# OR more concisely:
df['tempTXP'] = df['txp'].fillna(0)
```

### Example 2: Conditional with Missing Check
**Stata:**
```stata
replace FC = 0 if tempFC >=8 & !mi(tempFC)
```

**Python:**
```python
condition = (df['tempFC'] >= 8) & (df['tempFC'].notna())
df.loc[condition, 'FC'] = 0
```

### Example 3: Filter Non-Missing Observations
**Stata:**
```stata
keep if !mi(variable)
```

**Python:**
```python
df = df[df['variable'].notna()]
```

### Example 4: Drop Multiple Missing Variables
**Stata:**
```stata
drop if mi(var1) | mi(var2) | mi(var3)
```

**Python:**
```python
# Drop if ANY variable is missing
df = df[df[['var1', 'var2', 'var3']].notna().all(axis=1)]
# OR using dropna:
df = df.dropna(subset=['var1', 'var2', 'var3'])
```

### Example 5: Complex Missing Logic
**Stata:**
```stata
gen flag = 1 if !mi(var1) & mi(var2) & (var3 > 0)
```

**Python:**
```python
condition = (
    df['var1'].notna() & 
    df['var2'].isna() & 
    (df['var3'] > 0)
)
df['flag'] = np.where(condition, 1, np.nan)
```

## Missing Value Functions Translation

| Stata Function | Python Equivalent | Description |
|----------------|------------------|-------------|
| `mi(var)` | `df['var'].isna()` | Check if missing |
| `!mi(var)` | `df['var'].notna()` | Check if not missing |
| `mi(v1,v2,v3)` | `df[['v1','v2','v3']].isna().any(axis=1)` | Any variable missing |
| `missing(var)` | `df['var'].isna()` | Same as mi() |

## Advanced Missing Value Operations

### Count Missing Values
```python
# Stata: count if mi(var)
missing_count = df['var'].isna().sum()

# Missing by group
missing_by_group = df.groupby('group')['var'].apply(lambda x: x.isna().sum())
```

### Missing Value Patterns
```python
# Check missing patterns across multiple variables
missing_pattern = df[['var1', 'var2', 'var3']].isna()

# Count complete cases
complete_cases = (~missing_pattern.any(axis=1)).sum()
```

### Conditional Missing Assignment
```python
# Stata: replace var = . if condition
df.loc[condition, 'var'] = np.nan

# Multiple variables
df.loc[condition, ['var1', 'var2']] = np.nan
```

## Forward/Backward Fill with Missing Checks

### Forward Fill (Similar to Stata's Replace Pattern)
```python
# Stata: bys id (time): replace var = var[_n-1] if mi(var)
df['var'] = df.groupby('id')['var'].ffill()

# Conditional forward fill
mask = df['var'].isna()
df.loc[mask, 'var'] = df.groupby('id')['var'].ffill()[mask]
```

### Backward Fill
```python
df['var'] = df.groupby('id')['var'].bfill()
```

## Missing Value Creation and Handling

### Create Missing Values
```python
# Stata: replace var = . if condition
df.loc[condition, 'var'] = np.nan

# Create missing indicator
df['var_missing'] = df['var'].isna().astype(int)
```

### Handle Different Missing Types
```python
# Stata has different missing types (., .a, .b, etc.)
# Python uses np.nan for numeric, None for objects

# For categorical missing indicators:
df['var_missing_type'] = pd.Categorical(
    df['var'].isna().map({True: 'missing', False: 'present'})
)
```

## Performance Considerations

### Efficient Missing Checks
```python
# ✅ EFFICIENT: Direct pandas methods
is_missing = df['var'].isna()

# ❌ LESS EFFICIENT: Element-wise checking
is_missing = df['var'].apply(lambda x: pd.isna(x))
```

### Vectorized Operations
```python
# ✅ EFFICIENT: Vectorized missing handling
df['clean_var'] = df['var'].fillna(default_value)

# ❌ LESS EFFICIENT: Conditional assignment
df['clean_var'] = np.where(df['var'].isna(), default_value, df['var'])
```

## Data Type Considerations

### Numeric Variables
```python
# Missing values in numeric columns become np.nan
df['numeric_var'] = pd.to_numeric(df['string_var'], errors='coerce')
```

### String Variables
```python
# Missing values in string columns
df['string_var'] = df['string_var'].replace('', np.nan)  # Empty string to NaN
df['string_var'] = df['string_var'].fillna('Unknown')   # Fill missing strings
```

## Validation Checklist

After translating `mi()` functions:
1. ✅ Check that missing value logic matches Stata exactly
2. ✅ Verify boolean conditions handle NaN appropriately
3. ✅ Confirm data types preserved after missing value operations
4. ✅ Test edge cases (all missing, no missing values)
5. ✅ Validate group-wise missing value operations

## Common Mistakes

### ❌ WRONG: Using == or != with NaN
```python
df[df['var'] == np.nan]  # Always returns empty! NaN != NaN
df[df['var'] != np.nan]  # Always returns everything!
```

### ❌ WRONG: Not handling missing values in boolean conditions
```python
df[df['var'] > 0]  # Excludes NaN, but comparison returns False for NaN
```

### ❌ WRONG: Mixing None and np.nan
```python
df['var'] = None  # Can cause issues in numeric columns
```

### ✅ CORRECT: Proper missing value checking
```python
df[df['var'].isna()]      # Check for missing
df[df['var'].notna()]     # Check for not missing
```

### ✅ CORRECT: Handling missing in conditions
```python
# Explicit missing handling
condition = (df['var'] > 0) & (df['var'].notna())
df[condition]
```

### ✅ CORRECT: Consistent missing value types
```python
df['numeric_var'] = np.nan  # For numeric columns
df['object_var'] = pd.NA    # For nullable dtypes
```