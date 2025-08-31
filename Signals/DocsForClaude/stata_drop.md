# Stata `drop` Command Translation to Python

## Overview

The `drop` command in Stata removes variables (columns) or observations (rows) from datasets. It's the counterpart to `keep` and is commonly used for data cleaning and filtering.

## Stata Syntax and Usage

### Basic Syntax
```stata
drop varlist                   [removes specified variables]
drop if expression            [removes observations meeting condition]
```

### Common Patterns from Our Codebase

**Example 1: Drop unwanted variables (Accruals.do)**
```stata
drop temp*
```

**Example 2: Drop observations with missing key variables**
```stata
drop if mi(permno)
```

**Example 3: Drop by industry filter (tang.do)**
```stata
drop if sic < 2000 | sic > 3999
```

**Example 4: Drop intermediate calculations**
```stata
drop time_temp lag_variables
```

## Python Translation Patterns

### Method 1: Drop Variables (Column Removal)
```python
# Stata: drop var1 var2 var3
df = df.drop(['var1', 'var2', 'var3'], axis=1)
# OR
df = df.drop(columns=['var1', 'var2', 'var3'])
```

### Method 2: Drop Observations (Row Filtering)
```python
# Stata: drop if condition
df = df[~condition]  # Keep rows where condition is False
# OR
df = df.drop(df[condition].index)
```

### Method 3: In-place Operations
```python
# Modify DataFrame directly
df.drop(['var1', 'var2'], axis=1, inplace=True)
df.drop(df[condition].index, inplace=True)
```

## Complete Translation Examples

### Example 1: Drop Variables by Name
**Stata:**
```stata
drop temp*
```

**Python:**
```python
# Drop all columns starting with 'temp'
temp_cols = [col for col in df.columns if col.startswith('temp')]
df = df.drop(columns=temp_cols)

# OR using filter
df = df.loc[:, ~df.columns.str.startswith('temp')]
```

### Example 2: Drop Missing Observations
**Stata:**
```stata
drop if mi(permno)
```

**Python:**
```python
df = df[df['permno'].notna()]
# OR
df = df.dropna(subset=['permno'])
```

### Example 3: Conditional Row Dropping
**Stata:**
```stata
drop if sic < 2000 | sic > 3999
```

**Python:**
```python
# Method 1: Boolean indexing (recommended)
df = df[~((df['sic'] < 2000) | (df['sic'] > 3999))]

# Method 2: Keep the complement
df = df[(df['sic'] >= 2000) & (df['sic'] <= 3999)]
```

### Example 4: Drop Multiple Variables
**Stata:**
```stata
drop time_temp l1_var l2_var l3_var
```

**Python:**
```python
drop_vars = ['time_temp', 'l1_var', 'l2_var', 'l3_var']
df = df.drop(columns=drop_vars)
```

### Example 5: Complex Conditional Dropping
**Stata:**
```stata
drop if (variable <= 0) | mi(control_var) | (group_id > 100)
```

**Python:**
```python
condition = (
    (df['variable'] <= 0) | 
    (df['control_var'].isna()) | 
    (df['group_id'] > 100)
)
df = df[~condition]
```

## Variable Dropping Patterns

### Drop by Name Pattern
```python
# Single variable
df = df.drop('variable_name', axis=1)

# Multiple variables
df = df.drop(['var1', 'var2', 'var3'], axis=1)

# Using columns parameter (clearer)
df = df.drop(columns=['var1', 'var2', 'var3'])
```

### Drop with Wildcards (Stata-like)
```python
# Stata: drop var_*
drop_cols = [col for col in df.columns if col.startswith('var_')]
df = df.drop(columns=drop_cols)

# Using filter (more pandas-like)
df = df.loc[:, ~df.columns.str.startswith('var_')]

# Drop with regex pattern
df = df.loc[:, ~df.columns.str.match(r'^temp\d+$')]
```

### Drop by Data Type
```python
# Drop all string columns
df = df.select_dtypes(exclude=['object'])

# Drop all numeric columns
df = df.select_dtypes(exclude=[np.number])
```

## Observation Dropping Translation

### Basic Conditional Dropping
```python
# Stata: drop if var == value
df = df[df['var'] != value]

# Stata: drop if var > threshold  
df = df[df['var'] <= threshold]

# Stata: drop if var < min | var > max
df = df[(df['var'] >= min_val) & (df['var'] <= max_val)]
```

### Missing Value Dropping
```python
# Stata: drop if mi(var)
df = df[df['var'].notna()]

# Drop rows with any missing values
df = df.dropna()

# Drop rows missing specific variables
df = df.dropna(subset=['key_var1', 'key_var2'])
```

### Group-wise Dropping
```python
# Drop observations within groups
# Stata: bysort group: drop if _n > 5
df = df.groupby('group').head(5)

# Drop entire groups based on criteria
df = df.groupby('group').filter(lambda x: len(x) >= 10)
```

## Advanced Dropping Patterns

### Conditional Variable Dropping
```python
# Drop variables based on missing data percentage
missing_pct = df.isnull().mean()
cols_to_drop = missing_pct[missing_pct > 0.5].index
df = df.drop(columns=cols_to_drop)
```

### Drop Duplicates
```python
# Stata equivalent of keeping unique observations
df = df.drop_duplicates(subset=['key_var1', 'key_var2'])

# Drop all duplicates (keep none)
df = df[~df.duplicated(subset=['key_var1', 'key_var2'], keep=False)]
```

### Safe Dropping (Handle Non-existent Variables)
```python
# Stata: capture drop variable_name
drop_vars = ['var1', 'var2', 'var3']
existing_vars = [var for var in drop_vars if var in df.columns]
if existing_vars:
    df = df.drop(columns=existing_vars)
```

## Performance Considerations

### In-place vs Copy Operations
```python
# ✅ EFFICIENT: In-place operations (when safe)
df.drop(['var1', 'var2'], axis=1, inplace=True)

# ❌ LESS EFFICIENT: Creating copies repeatedly
df = df.drop('var1', axis=1)
df = df.drop('var2', axis=1)

# ✅ BETTER: Drop multiple at once
df = df.drop(['var1', 'var2'], axis=1)
```

### Boolean Indexing vs drop()
```python
# ✅ EFFICIENT: For conditional row dropping
df = df[~condition]

# ❌ LESS EFFICIENT: Using drop() for row filtering
df = df.drop(df[condition].index)
```

## Error Handling

### Handle Missing Variables Gracefully
```python
# Safe column dropping
def safe_drop_columns(dataframe, columns):
    existing_cols = [col for col in columns if col in dataframe.columns]
    return dataframe.drop(columns=existing_cols)

df = safe_drop_columns(df, ['var1', 'var2', 'nonexistent_var'])
```

### Validate Dropping Operations
```python
# Check before dropping
print(f"Before: {df.shape}")
df = df[~condition]
print(f"After: {df.shape}")
print(f"Dropped: {original_count - len(df)} observations")
```

## Validation Checklist

After translating `drop` commands:
1. ✅ Verify correct number of variables/observations removed
2. ✅ Check that remaining data matches expectations
3. ✅ Confirm no unintended data loss occurred
4. ✅ Test edge cases (empty results, non-existent variables)
5. ✅ Validate that index is properly managed

## Common Mistakes

### ❌ WRONG: Not using inversion for conditional dropping
```python
df = df.drop(df[condition].index)  # Inefficient
```

### ❌ WRONG: Dropping non-existent variables without checking
```python
df = df.drop('nonexistent_var', axis=1)  # KeyError!
```

### ❌ WRONG: Not handling missing values in conditions
```python
df = df[~(df['var'] > 0)]  # May not handle NaN correctly
```

### ✅ CORRECT: Proper conditional dropping
```python
df = df[~condition]  # Direct boolean indexing
```

### ✅ CORRECT: Safe variable dropping
```python
# Check existence first
if 'var_name' in df.columns:
    df = df.drop('var_name', axis=1)
```

### ✅ CORRECT: Handle missing values explicitly
```python
condition = (df['var'] > 0) & (df['var'].notna())
df = df[~condition]  # Explicitly handle NaN
```