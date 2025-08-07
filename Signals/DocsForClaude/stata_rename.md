# Stata `rename` Command Translation to Python

## Overview

The `rename` command in Stata changes variable names. It supports individual variable renaming, bulk renaming with patterns, and case transformations.

## Stata Syntax and Usage

### Basic Syntax
```stata
rename old_varname new_varname                [single variable]
rename (old_list) (new_list)                 [multiple variables]
rename old_pattern new_pattern               [pattern-based]
```

### Advanced Options
```stata
rename varname, upper                        [uppercase]
rename varname, lower                        [lowercase]
rename varname, proper                       [proper case]
```

### Common Patterns from Our Codebase

**Example 1: Simple renaming (Beta.do)**
```stata
rename _b_ewmktrf Beta
```

**Example 2: Multiple variable renaming**
```stata
rename (old_var1 old_var2 old_var3) (new_var1 new_var2 new_var3)
```

**Example 3: Pattern-based renaming**
```stata
rename *_temp *_final
```

**Example 4: Adding prefixes/suffixes**
```stata
rename (*) (prefix_*)
rename (*) (*_suffix)
```

## Python Translation Patterns

### Method 1: Single Variable Renaming
```python
# Stata: rename old_var new_var
df = df.rename(columns={'old_var': 'new_var'})
```

### Method 2: Multiple Variable Renaming
```python
# Stata: rename (old1 old2 old3) (new1 new2 new3)
df = df.rename(columns={
    'old1': 'new1',
    'old2': 'new2', 
    'old3': 'new3'
})
```

### Method 3: Pattern-based Renaming
```python
# Stata: rename *_temp *_final
df.columns = df.columns.str.replace('_temp', '_final')
```

### Method 4: Case Transformations
```python
# Stata: rename varname, upper
df = df.rename(columns={'varname': 'varname'.upper()})

# Or for all columns
df.columns = df.columns.str.upper()
```

## Complete Translation Examples

### Example 1: Simple Variable Renaming
**Stata:**
```stata
rename _b_ewmktrf Beta
```

**Python:**
```python
df = df.rename(columns={'_b_ewmktrf': 'Beta'})
```

### Example 2: Multiple Variables
**Stata:**
```stata
rename (date symbol returns) (Date Symbol Returns)
```

**Python:**
```python
df = df.rename(columns={
    'date': 'Date',
    'symbol': 'Symbol',
    'returns': 'Returns'
})
```

### Example 3: Pattern-based Renaming
**Stata:**
```stata
rename *_temp *_final
```

**Python:**
```python
# Method 1: String replacement
df.columns = df.columns.str.replace('_temp', '_final')

# Method 2: Using dictionary comprehension
rename_dict = {col: col.replace('_temp', '_final') 
               for col in df.columns if '_temp' in col}
df = df.rename(columns=rename_dict)
```

### Example 4: Adding Prefixes
**Stata:**
```stata
rename (*) (prefix_*)
```

**Python:**
```python
# Add prefix to all columns
df.columns = 'prefix_' + df.columns

# Or using rename with dictionary comprehension
df = df.rename(columns={col: f'prefix_{col}' for col in df.columns})
```

### Example 5: Adding Suffixes
**Stata:**
```stata
rename (*) (*_suffix)
```

**Python:**
```python
# Add suffix to all columns
df.columns = df.columns + '_suffix'

# Or using rename
df = df.rename(columns={col: f'{col}_suffix' for col in df.columns})
```

## Advanced Renaming Patterns

### Case Transformations
```python
# Stata: rename varname, upper
df.columns = df.columns.str.upper()

# Stata: rename varname, lower
df.columns = df.columns.str.lower()

# Stata: rename varname, proper
df.columns = df.columns.str.title()
```

### Wildcard Pattern Matching
```python
# Stata: rename var* new_var*
import re

def rename_with_wildcards(df, old_pattern, new_pattern):
    """
    Rename columns using wildcard patterns
    old_pattern: 'var*' -> 'var(.*)'
    new_pattern: 'new_var*' -> 'new_var\\1'
    """
    # Convert Stata wildcards to regex
    old_regex = old_pattern.replace('*', '(.*)')
    new_template = new_pattern.replace('*', '\\1')
    
    rename_dict = {}
    for col in df.columns:
        match = re.match(old_regex, col)
        if match:
            new_name = re.sub(old_regex, new_template, col)
            rename_dict[col] = new_name
    
    return df.rename(columns=rename_dict)

# Usage
df = rename_with_wildcards(df, 'var*', 'new_var*')
```

### Sequential Numbering
```python
# Stata: rename (*) (var_#), addnumber
def add_sequential_numbers(df, prefix='var_'):
    """Add sequential numbers to column names"""
    new_columns = [f'{prefix}{i}' for i in range(1, len(df.columns) + 1)]
    return df.rename(columns=dict(zip(df.columns, new_columns)))

# Usage
df = add_sequential_numbers(df, 'var_')
```

### Conditional Renaming
```python
# Rename only specific columns based on condition
def conditional_rename(df, condition_func, rename_func):
    """
    Rename columns based on condition
    condition_func: function that returns True/False for each column name
    rename_func: function that transforms column name
    """
    rename_dict = {}
    for col in df.columns:
        if condition_func(col):
            rename_dict[col] = rename_func(col)
    
    return df.rename(columns=rename_dict)

# Example: Rename only columns containing 'temp'
df = conditional_rename(
    df, 
    lambda col: 'temp' in col,
    lambda col: col.replace('temp', 'final')
)
```

## Complex Renaming Functions

### Comprehensive Rename Function
```python
def stata_rename(df, old_names=None, new_names=None, pattern=None, 
                 case=None, prefix=None, suffix=None):
    """
    Comprehensive rename function mimicking Stata's rename command
    
    Parameters:
    - df: DataFrame
    - old_names: list of old column names
    - new_names: list of new column names
    - pattern: tuple of (old_pattern, new_pattern) for wildcards
    - case: 'upper', 'lower', or 'proper'
    - prefix: string to add as prefix
    - suffix: string to add as suffix
    """
    df_copy = df.copy()
    
    # Direct renaming
    if old_names and new_names:
        if len(old_names) != len(new_names):
            raise ValueError("old_names and new_names must have same length")
        rename_dict = dict(zip(old_names, new_names))
        df_copy = df_copy.rename(columns=rename_dict)
    
    # Pattern-based renaming
    if pattern:
        old_pattern, new_pattern = pattern
        df_copy = rename_with_wildcards(df_copy, old_pattern, new_pattern)
    
    # Case transformations
    if case == 'upper':
        df_copy.columns = df_copy.columns.str.upper()
    elif case == 'lower':
        df_copy.columns = df_copy.columns.str.lower()
    elif case == 'proper':
        df_copy.columns = df_copy.columns.str.title()
    
    # Add prefix
    if prefix:
        df_copy.columns = prefix + df_copy.columns
    
    # Add suffix
    if suffix:
        df_copy.columns = df_copy.columns + suffix
    
    return df_copy

# Usage examples
df = stata_rename(df, old_names=['var1', 'var2'], new_names=['new1', 'new2'])
df = stata_rename(df, pattern=('*_temp', '*_final'))
df = stata_rename(df, case='upper')
df = stata_rename(df, prefix='data_')
```

### Smart Column Cleaning
```python
def clean_column_names(df, remove_special=True, snake_case=True, 
                      remove_spaces=True, lowercase=True):
    """
    Clean column names following common conventions
    """
    columns = df.columns.tolist()
    
    for i, col in enumerate(columns):
        # Remove special characters
        if remove_special:
            col = re.sub(r'[^A-Za-z0-9_\s]', '', col)
        
        # Remove spaces
        if remove_spaces:
            col = col.replace(' ', '_')
        
        # Convert to snake_case
        if snake_case:
            col = re.sub(r'([A-Z])', r'_\1', col).lower()
            col = re.sub(r'^_', '', col)  # Remove leading underscore
            col = re.sub(r'_+', '_', col)  # Remove multiple underscores
        
        # Convert to lowercase
        if lowercase:
            col = col.lower()
        
        columns[i] = col
    
    return df.rename(columns=dict(zip(df.columns, columns)))

# Usage
df = clean_column_names(df)
```

## Validation and Safety

### Safe Renaming with Validation
```python
def safe_rename(df, rename_dict, check_duplicates=True, check_existence=True):
    """
    Safe renaming with validation
    """
    # Check if old columns exist
    if check_existence:
        missing_cols = set(rename_dict.keys()) - set(df.columns)
        if missing_cols:
            raise ValueError(f"Columns not found: {missing_cols}")
    
    # Check for duplicate new names
    if check_duplicates:
        new_names = list(rename_dict.values())
        if len(new_names) != len(set(new_names)):
            raise ValueError("Duplicate new column names detected")
    
    # Check for conflicts with existing columns
    existing_cols = set(df.columns) - set(rename_dict.keys())
    new_cols = set(rename_dict.values())
    conflicts = existing_cols & new_cols
    if conflicts:
        print(f"Warning: New names conflict with existing columns: {conflicts}")
    
    return df.rename(columns=rename_dict)

# Usage
df = safe_rename(df, {'old_name': 'new_name'})
```

### Batch Renaming with Logging
```python
def batch_rename_with_log(df, rename_operations, log_file=None):
    """
    Perform multiple rename operations with logging
    """
    log_entries = []
    df_result = df.copy()
    
    for operation in rename_operations:
        old_columns = df_result.columns.tolist()
        
        if operation['type'] == 'direct':
            df_result = df_result.rename(columns=operation['mapping'])
        elif operation['type'] == 'pattern':
            df_result = rename_with_wildcards(df_result, 
                                            operation['old_pattern'], 
                                            operation['new_pattern'])
        elif operation['type'] == 'case':
            if operation['case'] == 'upper':
                df_result.columns = df_result.columns.str.upper()
            elif operation['case'] == 'lower':
                df_result.columns = df_result.columns.str.lower()
        
        new_columns = df_result.columns.tolist()
        changes = [(old, new) for old, new in zip(old_columns, new_columns) if old != new]
        
        log_entry = {
            'operation': operation,
            'changes': changes,
            'timestamp': pd.Timestamp.now()
        }
        log_entries.append(log_entry)
    
    if log_file:
        pd.DataFrame(log_entries).to_csv(log_file, index=False)
    
    return df_result, log_entries

# Usage
operations = [
    {'type': 'direct', 'mapping': {'old1': 'new1', 'old2': 'new2'}},
    {'type': 'pattern', 'old_pattern': '*_temp', 'new_pattern': '*_final'},
    {'type': 'case', 'case': 'lower'}
]
df, log = batch_rename_with_log(df, operations, 'rename_log.csv')
```

## Validation Checklist

After translating `rename` commands:
1. ✅ Check that all intended columns were renamed
2. ✅ Verify no duplicate column names were created
3. ✅ Confirm column names follow project conventions
4. ✅ Test that downstream code still works with new names
5. ✅ Validate that data types and values are preserved

## Common Mistakes

### ❌ WRONG: Creating duplicate column names
```python
df.columns = ['name', 'name', 'value']  # Duplicate names!
```

### ❌ WRONG: Not checking if columns exist
```python
df = df.rename(columns={'nonexistent_col': 'new_name'})  # Silent failure
```

### ❌ WRONG: Overwriting existing columns
```python
df = df.rename(columns={'col1': 'col2'})  # May overwrite existing col2
```

### ✅ CORRECT: Safe renaming with validation
```python
# Check existence first
if 'old_name' in df.columns:
    df = df.rename(columns={'old_name': 'new_name'})

# Or use safe_rename function
df = safe_rename(df, {'old_name': 'new_name'})
```

### ✅ CORRECT: Pattern-based renaming
```python
# Use string methods for pattern replacement
df.columns = df.columns.str.replace('_temp$', '_final', regex=True)
```