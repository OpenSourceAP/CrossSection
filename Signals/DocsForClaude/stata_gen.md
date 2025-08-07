# Stata `gen` Command Translation to Python

## Overview

The `gen` (generate) command in Stata creates new variables. It's one of the most frequently used commands and has various patterns that require careful translation to pandas.

## Stata Syntax and Usage

### Basic Syntax
```stata
gen new_variable = expression [if condition]
```

### Common Patterns from Our Codebase

**Example 1: Simple calculations (Size.do)**
```stata
gen Size = log(mve_c)
```

**Example 2: Complex expressions with lags (Accruals.do)**
```stata
gen Accruals = ((act - l12.act) - (che - l12.che) - ((lct - l12.lct) - (dlc - l12.dlc) - (tempTXP - l12.tempTXP)) - dp) / ((at + l12.at)/2)
```

**Example 3: Conditional creation (tang.do)**
```stata
gen FC = 1 if tempFC <=3
```

**Example 4: Missing value initialization**
```stata
gen tempTXP = txp
```

**Example 5: Binary variables (Mom12m.do)**
```stata
gen Mom12m = ((1+l.ret)*(1+l2.ret)*(1+l3.ret)*(1+l4.ret)*(1+l5.ret)*(1+l6.ret)*(1+l7.ret)*(1+l8.ret)*(1+l9.ret)*(1+l10.ret)*(1+l11.ret)) - 1
```

## Python Translation Patterns

### Method 1: Direct Assignment (Most Common)
```python
# Stata: gen new_var = expression
df['new_var'] = expression
```

### Method 2: Conditional Assignment
```python
# Stata: gen new_var = value if condition
df['new_var'] = np.where(condition, value, np.nan)
# OR
df.loc[condition, 'new_var'] = value
```

### Method 3: Complex Mathematical Expressions
```python
# Stata: gen result = (var1 + var2) / (var3 - var4)
df['result'] = (df['var1'] + df['var2']) / (df['var3'] - df['var4'])
```

## Complete Translation Examples

### Example 1: Simple Log Transformation
**Stata:**
```stata
gen Size = log(mve_c)
```

**Python:**
```python
df['Size'] = np.log(df['mve_c'])
```

### Example 2: Complex Accruals Calculation
**Stata:**
```stata
gen tempTXP = txp
replace tempTXP = 0 if mi(txp)
gen Accruals = ((act - l12.act) - (che - l12.che) - ((lct - l12.lct) - (dlc - l12.dlc) - (tempTXP - l12.tempTXP)) - dp) / ((at + l12.at)/2)
```

**Python:**
```python
# Create temporary variable (equivalent to gen tempTXP = txp)
df['tempTXP'] = df['txp'].copy()
# Replace missing with 0 (equivalent to replace tempTXP = 0 if mi(txp))
df['tempTXP'] = df['tempTXP'].fillna(0)

# Calculate Accruals (assuming lag variables already created)
df['Accruals'] = (
    ((df['act'] - df['l12_act']) - (df['che'] - df['l12_che']) - 
     ((df['lct'] - df['l12_lct']) - (df['dlc'] - df['l12_dlc']) - 
      (df['tempTXP'] - df['l12_tempTXP'])) - df['dp']) / 
    ((df['at'] + df['l12_at']) / 2)
)
```

### Example 3: Conditional Variable Creation  
**Stata:**
```stata
gen FC = 1 if tempFC <=3
```

**Python:**
```python
# Method 1: Using np.where (creates NaN for unmatched)
df['FC'] = np.where(df['tempFC'] <= 3, 1, np.nan)

# Method 2: Using .loc (recommended for clear conditional assignment)
df['FC'] = np.nan  # Initialize with NaN
df.loc[df['tempFC'] <= 3, 'FC'] = 1
```

### Example 4: Momentum Calculation
**Stata:**
```stata
gen Mom12m = ((1+l.ret)*(1+l2.ret)*(1+l3.ret)*(1+l4.ret)*(1+l5.ret)*(1+l6.ret)*(1+l7.ret)*(1+l8.ret)*(1+l9.ret)*(1+l10.ret)*(1+l11.ret)) - 1
```

**Python:**
```python
# Assuming lag variables exist as l1_ret, l2_ret, etc.
momentum_product = 1
for i in range(1, 12):
    momentum_product *= (1 + df[f'l{i}_ret'])
df['Mom12m'] = momentum_product - 1
```

## Function Translation Table

| Stata Function | Python Equivalent | Notes |
|----------------|------------------|-------|
| `log()` | `np.log()` | Natural logarithm |
| `exp()` | `np.exp()` | Exponential |
| `sqrt()` | `np.sqrt()` | Square root |
| `abs()` | `np.abs()` or `df.abs()` | Absolute value |
| `max(a,b)` | `np.maximum(a,b)` | Element-wise maximum |
| `min(a,b)` | `np.minimum(a,b)` | Element-wise minimum |
| `round()` | `np.round()` | Rounding |

## Critical Translation Issues

### 1. **Missing Value Handling**
```python
# Stata automatically handles missing values in calculations
# Python may need explicit handling
df['result'] = np.where(df['var1'].notna() & df['var2'].notna(), 
                       df['var1'] + df['var2'], np.nan)
```

### 2. **Conditional Assignment Patterns**
```python
# ❌ WRONG: Overwrites existing values
df['new_var'] = condition_value

# ✅ CORRECT: Only assigns where condition is true
df.loc[condition, 'new_var'] = value
```

### 3. **Variable Initialization**
```python
# Stata: gen var = .  (creates missing)
df['var'] = np.nan

# Stata: gen var = 0  (creates zeros)
df['var'] = 0
```

## Advanced Patterns

### Creating Multiple Variables
```python
# Stata equivalent of multiple gen statements
df = df.assign(
    var1 = df['a'] + df['b'],
    var2 = np.log(df['c']),
    var3 = np.where(df['d'] > 0, 1, 0)
)
```

### Lag Variables in Calculations
```python
# Ensure lags are created first (see lag operators documentation)
df_sorted = df.sort_values(['permno', 'time_avail_m'])
df_sorted['l12_var'] = df_sorted.groupby('permno')['var'].shift(12)

# Then use in calculations
df_sorted['result'] = df_sorted['var'] - df_sorted['l12_var']
```

## Validation Checklist

After translating `gen` commands:
1. ✅ Check that new variable exists with correct name
2. ✅ Verify data types match expectations (float64 for numeric)
3. ✅ Confirm missing value handling is consistent with Stata
4. ✅ Test conditional assignments create correct number of non-missing values
5. ✅ Validate mathematical expressions produce expected results

## Common Mistakes

### ❌ WRONG: Using Python built-ins instead of numpy
```python
df['new_var'] = log(df['old_var'])  # NameError: 'log' not defined
```

### ❌ WRONG: Not handling missing values in conditions
```python
df['new_var'] = np.where(df['condition'], 1, 0)  # May not handle NaN correctly
```

### ✅ CORRECT: Proper function usage and missing value handling
```python
df['new_var'] = np.log(df['old_var'])  # Use np.log
df['new_var'] = np.where(df['condition'].fillna(False), 1, np.nan)  # Handle NaN
```