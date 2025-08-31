# Stata `use` Command Translation to Python

## Overview

The `use` command in Stata loads datasets into memory. It's the first command in virtually every .do file and determines which columns and observations are loaded for processing.

## Stata Syntax and Usage

### Basic Syntax
```stata
use [varlist] [if] [in] using "filename" [, options]
```

### Common Patterns from Our Codebase

**Example 1: Load specific columns (Size.do)**
```stata
use permno time_avail_m mve_c using "$pathDataIntermediate/SignalMasterTable", clear
```

**Example 2: Load with complex column selection (Accruals.do)**
```stata
use gvkey permno time_avail_m txp act che lct dlc at dp using "$pathDataIntermediate/m_aCompustat", clear
```

**Example 3: Load all columns (simple case)**
```stata
use "$pathDataIntermediate/monthlyCRSP", clear
```

## Python Translation Patterns

### Method 1: Direct Column Selection (Most Common)
```python
# Stata: use var1 var2 var3 using "file.dta", clear
df = pd.read_parquet('file.parquet')[['var1', 'var2', 'var3']]
```

### Method 2: Load All Columns
```python
# Stata: use "file.dta", clear
df = pd.read_parquet('file.parquet')
```

### Method 3: Load with Copy for Safety
```python
# Stata: use var1 var2 using "file.dta", clear
df = pd.read_parquet('file.parquet')[['var1', 'var2']].copy()
```

## Complete Translation Examples

### Example 1: Size.do Translation
**Stata:**
```stata
use permno time_avail_m mve_c using "$pathDataIntermediate/SignalMasterTable", clear
```

**Python:**
```python
df = pd.read_parquet('../pyData/Intermediate/SignalMasterTable.parquet')[['permno', 'time_avail_m', 'mve_c']]
```

### Example 2: Accruals.do Translation  
**Stata:**
```stata
use gvkey permno time_avail_m txp act che lct dlc at dp using "$pathDataIntermediate/m_aCompustat", clear
```

**Python:**
```python
df = pd.read_parquet('../pyData/Intermediate/m_aCompustat.parquet')[['gvkey', 'permno', 'time_avail_m', 'txp', 'act', 'che', 'lct', 'dlc', 'at', 'dp']]
```

## File Format Translation

| Stata Format | Python Equivalent | Notes |
|--------------|------------------|-------|
| `.dta` | `.parquet` | Our project standard |
| `$pathDataIntermediate/` | `../pyData/Intermediate/` | Path translation |
| `$pathDataPrep/` | `../pyData/Prep/` | Path translation |

## Key Translation Rules

### 1. **Always Use Column Selection**
- **Stata**: `use var1 var2 using file` loads only specified columns
- **Python**: **MUST** use `[['var1', 'var2']]` - don't load unnecessary columns

### 2. **Path Translation**
- **Stata**: `"$pathDataIntermediate/filename"`
- **Python**: `'../pyData/Intermediate/filename.parquet'`

### 3. **Memory Management**
- **Stata**: `clear` option overwrites data in memory
- **Python**: Each assignment creates new DataFrame (automatic memory management)

### 4. **Column Order Preservation**
```python
# Preserve exact column order from Stata
columns = ['permno', 'time_avail_m', 'mve_c']  # Same order as Stata
df = pd.read_parquet('file.parquet')[columns]
```

## Critical Translation Patterns

### ❌ WRONG: Loading unnecessary columns
```python
df = pd.read_parquet('SignalMasterTable.parquet')  # Loads all columns
df = df[['permno', 'time_avail_m', 'mve_c']]      # Inefficient
```

### ❌ WRONG: Wrong file format
```python
df = pd.read_csv('file.dta')  # Wrong - can't read .dta directly
```

### ✅ CORRECT: Direct column selection
```python
df = pd.read_parquet('../pyData/Intermediate/SignalMasterTable.parquet')[['permno', 'time_avail_m', 'mve_c']]
```

### ✅ CORRECT: Adding .copy() when needed
```python
# Use .copy() when DataFrame will be modified to avoid warnings
df = pd.read_parquet('file.parquet')[['var1', 'var2']].copy()
```

## Advanced Usage

### Conditional Loading (if/in equivalents)
**Stata:**
```stata
use var1 var2 if condition using "file.dta", clear
```

**Python:**
```python
df = pd.read_parquet('file.parquet')[['var1', 'var2']]
df = df[df['condition']]  # Apply filter after loading
```

### Large File Handling
```python
# For very large files, consider chunking
# But generally our parquet files load efficiently
df = pd.read_parquet('large_file.parquet', 
                     columns=['permno', 'time_avail_m', 'target_var'])
```

## File Path Best Practices

### Standard Project Paths
```python
# From pyCode/ directory (our working directory)
intermediate_data = '../pyData/Intermediate/'
prep_data = '../pyData/Prep/'

# Example usage
df = pd.read_parquet(f'{intermediate_data}SignalMasterTable.parquet')[required_columns]
```

## Validation Checklist

After translating `use` commands:
1. ✅ Check column names match exactly (case-sensitive)
2. ✅ Verify file path points to correct .parquet file
3. ✅ Ensure only necessary columns are loaded
4. ✅ Confirm DataFrame shape matches expectations
5. ✅ Test that file exists and is readable

## Common Mistakes

### Missing `.copy()`
```python
# Can cause SettingWithCopyWarning later
df = pd.read_parquet('file.parquet')[['col1', 'col2']]
df['new_col'] = 1  # Warning!

# Better:
df = pd.read_parquet('file.parquet')[['col1', 'col2']].copy()
df['new_col'] = 1  # No warning
```