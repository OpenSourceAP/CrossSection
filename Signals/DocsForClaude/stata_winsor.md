# Stata `winsor` Commands Translation to Python

## Overview

Winsorization in Stata handles outliers by replacing extreme values with less extreme values (rather than removing them entirely). Multiple commands exist: `winsor`, `winsor2`, `winsor4`, and `gstats winsor`.

## Stata Syntax and Usage

### Most Common: winsor2
```stata
winsor2 varname, cuts(1 99)                    [1st and 99th percentiles]
winsor2 varname, cuts(5 95) by(group)          [by group]
winsor2 varname, suffix(_w) cuts(1 99)         [custom suffix]
winsor2 varname, replace cuts(1 99)            [replace original]
```

### Alternative: gstats winsor
```stata
gstats winsor varname, cuts(1 99)
gstats winsor varname, cuts(1 99) by(group)
gstats winsor varname, trim                    [trim instead of winsorize]
```

### Common Patterns from Finance Literature

**Example 1: Standard 1%/99% winsorization**
```stata
winsor2 roa, cuts(1 99) by(year)
```

**Example 2: Multiple variables**
```stata
winsor2 roa roe leverage, cuts(1 99) by(year)
```

**Example 3: Asymmetric winsorization**
```stata
winsor2 returns, cuts(5 99) by(year)  // More conservative on downside
```

**Example 4: Conservative winsorization**
```stata
winsor2 extreme_var, cuts(0.5 99.5) by(industry year)
```

## Python Translation Patterns

### Method 1: Simple Percentile-based Winsorization
```python
def winsorize_variable(df, var, lower_pct=1, upper_pct=99):
    """Basic winsorization function"""
    lower_bound = df[var].quantile(lower_pct / 100)
    upper_bound = df[var].quantile(upper_pct / 100)
    return df[var].clip(lower_bound, upper_bound)
```

### Method 2: Group-wise Winsorization
```python
def winsorize_by_group(df, var, group_cols, lower_pct=1, upper_pct=99):
    """Winsorize within groups"""
    def winsorize_group(group):
        lower_bound = group[var].quantile(lower_pct / 100)
        upper_bound = group[var].quantile(upper_pct / 100)
        return group[var].clip(lower_bound, upper_bound)
    
    return df.groupby(group_cols).apply(
        lambda x: x.assign(**{f"{var}_w": winsorize_group(x)})
    ).reset_index(drop=True)
```

### Method 3: Using scipy.stats.mstats
```python
from scipy.stats.mstats import winsorize
import numpy as np

def scipy_winsorize(df, var, lower_pct=1, upper_pct=99):
    """Using scipy's winsorize function"""
    # Convert percentiles to proportions
    limits = [(lower_pct/100), (upper_pct/100)]
    winsorized = winsorize(df[var].dropna(), limits=limits)
    
    # Handle missing values
    result = df[var].copy()
    result[df[var].notna()] = winsorized
    return result
```

## Complete Translation Examples

### Example 1: Standard 1%/99% Winsorization by Year
**Stata:**
```stata
winsor2 roa, cuts(1 99) by(year)
```

**Python:**
```python
def winsorize_by_year(df, var, lower_pct=1, upper_pct=99):
    def winsorize_group(group):
        if len(group) == 0 or group[var].isna().all():
            return group
        
        lower_bound = group[var].quantile(lower_pct / 100)
        upper_bound = group[var].quantile(upper_pct / 100)
        group[f"{var}_w"] = group[var].clip(lower_bound, upper_bound)
        return group
    
    return df.groupby('year').apply(winsorize_group).reset_index(drop=True)

# Usage
df = winsorize_by_year(df, 'roa', lower_pct=1, upper_pct=99)
```

### Example 2: Multiple Variables Winsorization
**Stata:**
```stata
winsor2 roa roe leverage, cuts(1 99) by(year)
```

**Python:**
```python
def winsorize_multiple_vars(df, vars, group_cols, lower_pct=1, upper_pct=99):
    def winsorize_group(group):
        for var in vars:
            if var in group.columns and not group[var].isna().all():
                lower_bound = group[var].quantile(lower_pct / 100)
                upper_bound = group[var].quantile(upper_pct / 100)
                group[f"{var}_w"] = group[var].clip(lower_bound, upper_bound)
        return group
    
    return df.groupby(group_cols).apply(winsorize_group).reset_index(drop=True)

# Usage
financial_vars = ['roa', 'roe', 'leverage']
df = winsorize_multiple_vars(df, financial_vars, ['year'], lower_pct=1, upper_pct=99)
```

### Example 3: Asymmetric Winsorization
**Stata:**
```stata
winsor2 returns, cuts(5 99) by(year)
```

**Python:**
```python
def asymmetric_winsorize(df, var, group_cols, lower_pct=5, upper_pct=99):
    def winsorize_group(group):
        if len(group) == 0 or group[var].isna().all():
            return group
            
        lower_bound = group[var].quantile(lower_pct / 100)
        upper_bound = group[var].quantile(upper_pct / 100)
        group[f"{var}_w"] = group[var].clip(lower_bound, upper_bound)
        return group
    
    return df.groupby(group_cols).apply(winsorize_group).reset_index(drop=True)

# Usage
df = asymmetric_winsorize(df, 'returns', ['year'], lower_pct=5, upper_pct=99)
```

### Example 4: Conservative Multi-group Winsorization
**Stata:**
```stata
winsor2 extreme_var, cuts(0.5 99.5) by(industry year)
```

**Python:**
```python
def conservative_winsorize(df, var, group_cols, lower_pct=0.5, upper_pct=99.5):
    def winsorize_group(group):
        if len(group) < 10:  # Skip small groups
            group[f"{var}_w"] = group[var]
            return group
            
        lower_bound = group[var].quantile(lower_pct / 100)
        upper_bound = group[var].quantile(upper_pct / 100)
        group[f"{var}_w"] = group[var].clip(lower_bound, upper_bound)
        return group
    
    return df.groupby(group_cols).apply(winsorize_group).reset_index(drop=True)

# Usage
df = conservative_winsorize(df, 'extreme_var', ['industry', 'year'], 
                           lower_pct=0.5, upper_pct=99.5)
```

## Advanced Winsorization Patterns

### Winsorization with Replacement
```python
def winsorize_replace(df, var, group_cols, lower_pct=1, upper_pct=99):
    """Replace original variable (like winsor2 replace option)"""
    def winsorize_group(group):
        if len(group) == 0 or group[var].isna().all():
            return group
            
        lower_bound = group[var].quantile(lower_pct / 100)
        upper_bound = group[var].quantile(upper_pct / 100)
        group[var] = group[var].clip(lower_bound, upper_bound)
        return group
    
    return df.groupby(group_cols).apply(winsorize_group).reset_index(drop=True)
```

### Trimming (Remove Outliers)
```python
def trim_outliers(df, var, group_cols, lower_pct=1, upper_pct=99):
    """Trim outliers (set to NaN) instead of winsorizing"""
    def trim_group(group):
        if len(group) == 0 or group[var].isna().all():
            return group
            
        lower_bound = group[var].quantile(lower_pct / 100)
        upper_bound = group[var].quantile(upper_pct / 100)
        
        # Set outliers to NaN
        group[f"{var}_trimmed"] = group[var].copy()
        group.loc[(group[var] < lower_bound) | (group[var] > upper_bound), 
                  f"{var}_trimmed"] = np.nan
        return group
    
    return df.groupby(group_cols).apply(trim_group).reset_index(drop=True)
```

### IQR-based Winsorization
```python
def winsorize_iqr(df, var, group_cols, multiplier=1.5):
    """Winsorize based on IQR (like winsor4)"""
    def winsorize_group(group):
        if len(group) == 0 or group[var].isna().all():
            return group
            
        Q1 = group[var].quantile(0.25)
        Q3 = group[var].quantile(0.75)
        IQR = Q3 - Q1
        
        lower_bound = Q1 - multiplier * IQR
        upper_bound = Q3 + multiplier * IQR
        
        group[f"{var}_w"] = group[var].clip(lower_bound, upper_bound)
        return group
    
    return df.groupby(group_cols).apply(winsorize_group).reset_index(drop=True)
```

## Comprehensive Winsorization Function

```python
def comprehensive_winsorize(df, variables, group_cols=None, method='percentile', 
                           lower_pct=1, upper_pct=99, iqr_multiplier=1.5, 
                           suffix='_w', replace=False, min_obs=10):
    """
    Comprehensive winsorization function supporting multiple methods
    
    Parameters:
    - df: DataFrame
    - variables: list of variables to winsorize
    - group_cols: list of grouping columns
    - method: 'percentile' or 'iqr'
    - lower_pct, upper_pct: percentile cutoffs
    - iqr_multiplier: multiplier for IQR method
    - suffix: suffix for new variables
    - replace: whether to replace original variables
    - min_obs: minimum observations per group
    """
    
    def winsorize_group(group):
        for var in variables:
            if var not in group.columns or group[var].isna().all():
                continue
                
            if len(group) < min_obs:
                if replace:
                    continue  # Skip small groups
                else:
                    group[f"{var}{suffix}"] = group[var]
                    continue
            
            if method == 'percentile':
                lower_bound = group[var].quantile(lower_pct / 100)
                upper_bound = group[var].quantile(upper_pct / 100)
            elif method == 'iqr':
                Q1 = group[var].quantile(0.25)
                Q3 = group[var].quantile(0.75)
                IQR = Q3 - Q1
                lower_bound = Q1 - iqr_multiplier * IQR
                upper_bound = Q3 + iqr_multiplier * IQR
            
            winsorized = group[var].clip(lower_bound, upper_bound)
            
            if replace:
                group[var] = winsorized
            else:
                group[f"{var}{suffix}"] = winsorized
        
        return group
    
    if group_cols:
        return df.groupby(group_cols).apply(winsorize_group).reset_index(drop=True)
    else:
        return winsorize_group(df)

# Usage examples
df = comprehensive_winsorize(df, ['roa', 'roe'], ['year'], method='percentile')
df = comprehensive_winsorize(df, ['leverage'], ['industry', 'year'], method='iqr')
```

## Performance Optimization

### Vectorized Winsorization
```python
def fast_winsorize(df, var, group_col, lower_pct=1, upper_pct=99):
    """Faster winsorization using vectorized operations"""
    # Calculate bounds by group
    bounds = df.groupby(group_col)[var].agg([
        ('lower', lambda x: x.quantile(lower_pct/100)),
        ('upper', lambda x: x.quantile(upper_pct/100))
    ]).reset_index()
    
    # Merge bounds back to main dataframe
    df = df.merge(bounds, on=group_col, how='left')
    
    # Apply winsorization
    df[f"{var}_w"] = df[var].clip(df['lower'], df['upper'])
    
    # Clean up
    df = df.drop(['lower', 'upper'], axis=1)
    return df
```

## Validation Checklist

After translating winsorization commands:
1. ✅ Check that percentile calculations match Stata exactly
2. ✅ Verify group-wise winsorization preserves group structure
3. ✅ Confirm handling of missing values matches Stata behavior
4. ✅ Test edge cases (small groups, all missing values)
5. ✅ Validate that extreme values are properly capped

## Common Mistakes

### ❌ WRONG: Not handling missing values
```python
df['var_w'] = df['var'].clip(df['var'].quantile(0.01), df['var'].quantile(0.99))
```

### ❌ WRONG: Ignoring group structure
```python
# Global winsorization instead of by-group
df['var_w'] = df['var'].clip(df['var'].quantile(0.01), df['var'].quantile(0.99))
```

### ❌ WRONG: Not handling small groups
```python
# May fail with small groups
df['var_w'] = df.groupby('group')['var'].transform(lambda x: x.clip(x.quantile(0.01), x.quantile(0.99)))
```

### ✅ CORRECT: Proper group-wise winsorization
```python
def safe_winsorize(group, var, lower_pct=1, upper_pct=99):
    if len(group) < 10 or group[var].isna().all():
        return group[var]
    return group[var].clip(
        group[var].quantile(lower_pct/100), 
        group[var].quantile(upper_pct/100)
    )

df['var_w'] = df.groupby('group').apply(lambda x: safe_winsorize(x, 'var')).reset_index(level=0, drop=True)
```