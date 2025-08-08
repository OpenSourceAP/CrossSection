# Stata `asrol` Command Translation to Python

## Overview

The `asrol` command in Stata calculates rolling window statistics efficiently for panel data. It's widely used in finance for moving averages, standard deviations, and other rolling statistics that are essential for time series analysis and financial signal construction.

## Stata Syntax and Usage

### Basic Syntax
```stata
asrol varlist [if] [in], window(rangevar #) by(varlist) stat(statistic) [options]
```

### Key Options
- `window(rangevar #)`: Length of rolling window
- `by(varlist)`: Group variables
- `stat(statistic)`: Statistic to calculate (mean, sd, sum, count, etc.)
- `gen(newvar)`: Name for generated variable
- `minimum(#)`: Minimum observations required

### Available Statistics
- `mean`: Rolling average
- `sd`: Rolling standard deviation
- `sum`: Rolling sum
- `count`: Rolling count of non-missing values
- `min`: Rolling minimum
- `max`: Rolling maximum
- `median`: Rolling median

### Common Patterns from Our Codebase

**Example 1: Rolling Mean (Investment.do)**
```stata
asrol investment_asset, window(time_temp 36) min(6) by(permno) stat(mean) gen(mean36_investment)
```

**Example 2: Rolling Standard Deviation (std_turn.do)**
```stata
asrol turn, window(time_temp 36) min(6) by(permno) stat(sd) gen(std_turn)
```

**Example 3: Multiple Rolling Statistics (ZZ1_ResidualMomentum)**
```stata
asrol temp, window(time_temp 6) min(6) by(permno) stat(mean) gen(mean6_temp)
asrol temp, window(time_temp 6) min(6) by(permno) stat(sd) gen(sd6_temp)
```

**Example 4: Rolling Count (Herf.do)**
```stata
asrol herf_comp, window(time_temp 36) min(6) by(permno) stat(mean) gen(Herf)
```

## Python Translation Patterns

### Method 1: Simple Rolling Statistics with Pandas
```python
def asrol_translation(df, var_col, window, min_periods, group_col, stat='mean', gen_name=None):
    """
    Translate asrol functionality using pandas rolling
    
    Parameters:
    - df: DataFrame
    - var_col: Variable to calculate statistic on
    - window: Rolling window size
    - min_periods: Minimum observations required
    - group_col: Group variable (like by() option)
    - stat: Statistic to calculate ('mean', 'sd', 'sum', 'count', 'min', 'max')
    - gen_name: Name for new variable
    """
    
    if gen_name is None:
        gen_name = f'{stat}{window}_{var_col}'
    
    # Map statistics to pandas methods
    stat_map = {
        'mean': 'mean',
        'sd': 'std',
        'sum': 'sum',
        'count': 'count',
        'min': 'min',
        'max': 'max',
        'median': 'median'
    }
    
    if stat not in stat_map:
        raise ValueError(f"Unsupported statistic: {stat}")
    
    # Apply rolling statistic by group
    df[gen_name] = df.groupby(group_col)[var_col].transform(
        lambda x: getattr(x.rolling(window=window, min_periods=min_periods), stat_map[stat])()
    )
    
    return df

# Usage example
df = asrol_translation(df, 'turn', window=36, min_periods=6, 
                      group_col='permno', stat='sd', gen_name='std_turn')
```

### Method 2: Multiple Statistics at Once
```python
def multi_asrol_translation(df, var_col, window, min_periods, group_col, stats_dict):
    """
    Calculate multiple rolling statistics efficiently
    
    Parameters:
    - stats_dict: Dictionary mapping stat name to output variable name
                 e.g., {'mean': 'mean6_temp', 'sd': 'sd6_temp'}
    """
    
    for stat, gen_name in stats_dict.items():
        df = asrol_translation(df, var_col, window, min_periods, group_col, stat, gen_name)
    
    return df

# Usage example  
df = multi_asrol_translation(df, 'temp', window=6, min_periods=6, group_col='permno',
                            stats_dict={'mean': 'mean6_temp', 'sd': 'sd6_temp'})
```

### Method 3: Optimized Rolling Statistics Class
```python
class RollingStats:
    """Optimized rolling statistics class similar to asrol"""
    
    def __init__(self, window=36, min_periods=6):
        self.window = window
        self.min_periods = min_periods
    
    def calculate(self, df, var_col, group_col, stat='mean', gen_name=None, time_col=None):
        """
        Calculate rolling statistic
        
        Parameters:
        - df: DataFrame
        - var_col: Variable to calculate statistic on
        - group_col: Grouping variable
        - stat: Statistic type
        - gen_name: Name for output variable
        - time_col: Time variable for proper sorting
        """
        
        if gen_name is None:
            gen_name = f'{stat}{self.window}_{var_col}'
        
        # Ensure proper sorting within groups
        if time_col:
            df = df.sort_values([group_col, time_col])
        
        # Calculate rolling statistic
        if stat == 'mean':
            df[gen_name] = df.groupby(group_col)[var_col].transform(
                lambda x: x.rolling(window=self.window, min_periods=self.min_periods).mean()
            )
        elif stat == 'sd':
            df[gen_name] = df.groupby(group_col)[var_col].transform(
                lambda x: x.rolling(window=self.window, min_periods=self.min_periods).std()
            )
        elif stat == 'sum':
            df[gen_name] = df.groupby(group_col)[var_col].transform(
                lambda x: x.rolling(window=self.window, min_periods=self.min_periods).sum()
            )
        elif stat == 'count':
            df[gen_name] = df.groupby(group_col)[var_col].transform(
                lambda x: x.rolling(window=self.window, min_periods=self.min_periods).count()
            )
        elif stat == 'min':
            df[gen_name] = df.groupby(group_col)[var_col].transform(
                lambda x: x.rolling(window=self.window, min_periods=self.min_periods).min()
            )
        elif stat == 'max':
            df[gen_name] = df.groupby(group_col)[var_col].transform(
                lambda x: x.rolling(window=self.window, min_periods=self.min_periods).max()
            )
        else:
            raise ValueError(f"Unsupported statistic: {stat}")
        
        return df

# Usage
roller = RollingStats(window=36, min_periods=6)
df = roller.calculate(df, 'turn', 'permno', stat='sd', gen_name='std_turn', time_col='time_avail_m')
```

## Complete Translation Examples

### Example 1: Rolling Standard Deviation (std_turn.do)
**Stata:**
```stata
bys permno (time_avail_m): gen time_temp = _n
xtset permno time_temp
asrol turn, window(time_temp 36) min(6) by(permno) stat(sd) gen(std_turn)
```

**Python:**
```python
import pandas as pd
import numpy as np

def calculate_std_turn(df):
    """Calculate rolling standard deviation of turnover"""
    
    # Sort data properly (equivalent to bys permno (time_avail_m))
    df = df.sort_values(['permno', 'time_avail_m'])
    
    # Create time index within each group (equivalent to gen time_temp = _n)
    df['time_temp'] = df.groupby('permno').cumcount() + 1
    
    # Calculate rolling standard deviation (equivalent to asrol)
    df['std_turn'] = df.groupby('permno')['turn'].transform(
        lambda x: x.rolling(window=36, min_periods=6).std()
    )
    
    return df

# Usage
df = calculate_std_turn(df)
```

### Example 2: Rolling Mean (Investment.do)
**Stata:**
```stata
asrol investment_asset, window(time_temp 36) min(6) by(permno) stat(mean) gen(mean36_investment)
```

**Python:**
```python
def calculate_rolling_investment(df):
    """Calculate 36-month rolling mean of investment"""
    
    # Ensure proper sorting
    df = df.sort_values(['permno', 'time_avail_m'])
    
    # Calculate rolling mean
    df['mean36_investment'] = df.groupby('permno')['investment_asset'].transform(
        lambda x: x.rolling(window=36, min_periods=6).mean()
    )
    
    return df

# Usage
df = calculate_rolling_investment(df)
```

### Example 3: Multiple Rolling Statistics (ZZ1_ResidualMomentum)
**Stata:**
```stata
asrol temp, window(time_temp 6) min(6) by(permno) stat(mean) gen(mean6_temp)
asrol temp, window(time_temp 6) min(6) by(permno) stat(sd) gen(sd6_temp)
```

**Python:**
```python
def calculate_residual_momentum_stats(df):
    """Calculate rolling mean and standard deviation for residual momentum"""
    
    # Ensure proper sorting
    df = df.sort_values(['permno', 'time_avail_m'])
    
    # Calculate multiple rolling statistics
    grouped = df.groupby('permno')['temp']
    
    df['mean6_temp'] = grouped.transform(
        lambda x: x.rolling(window=6, min_periods=6).mean()
    )
    
    df['sd6_temp'] = grouped.transform(
        lambda x: x.rolling(window=6, min_periods=6).std()
    )
    
    return df

# Usage
df = calculate_residual_momentum_stats(df)
```

### Example 4: Herfindahl Index Rolling Mean (Herf.do)
**Stata:**
```stata
asrol herf_comp, window(time_temp 36) min(6) by(permno) stat(mean) gen(Herf)
```

**Python:**
```python
def calculate_herf_rolling(df):
    """Calculate 36-month rolling mean of Herfindahl index"""
    
    # Sort data
    df = df.sort_values(['permno', 'time_avail_m'])
    
    # Calculate rolling mean of Herfindahl index
    df['Herf'] = df.groupby('permno')['herf_comp'].transform(
        lambda x: x.rolling(window=36, min_periods=6).mean()
    )
    
    return df

# Usage
df = calculate_herf_rolling(df)
```

## Performance Optimization

### Using Polars for Better Performance
```python
import polars as pl

def polars_asrol_translation(df, var_col, window, min_periods, group_col, stat='mean', gen_name=None):
    """
    Fast asrol translation using polars
    """
    
    if gen_name is None:
        gen_name = f'{stat}{window}_{var_col}'
    
    # Convert to polars if needed
    if isinstance(df, pd.DataFrame):
        df_pl = pl.from_pandas(df)
    else:
        df_pl = df
    
    # Rolling statistics mapping
    if stat == 'mean':
        result = df_pl.with_columns(
            pl.col(var_col)
            .rolling_mean(window_size=window, min_periods=min_periods)
            .over(group_col)
            .alias(gen_name)
        )
    elif stat == 'sd':
        result = df_pl.with_columns(
            pl.col(var_col)
            .rolling_std(window_size=window, min_periods=min_periods)
            .over(group_col)
            .alias(gen_name)
        )
    elif stat == 'sum':
        result = df_pl.with_columns(
            pl.col(var_col)
            .rolling_sum(window_size=window, min_periods=min_periods)
            .over(group_col)
            .alias(gen_name)
        )
    else:
        raise ValueError(f"Statistic {stat} not yet implemented in polars version")
    
    return result.to_pandas() if isinstance(df, pd.DataFrame) else result

# Usage
df = polars_asrol_translation(df, 'turn', window=36, min_periods=6, 
                             group_col='permno', stat='sd', gen_name='std_turn')
```

### Vectorized Implementation for Large Datasets
```python
import numba as nb

@nb.jit(nopython=True)
def fast_rolling_mean(values, window, min_periods):
    """Fast rolling mean using numba"""
    n = len(values)
    result = np.full(n, np.nan)
    
    for i in range(window-1, n):
        start_idx = i - window + 1
        window_values = values[start_idx:i+1]
        
        # Count non-NaN values
        valid_count = np.sum(~np.isnan(window_values))
        
        if valid_count >= min_periods:
            result[i] = np.nanmean(window_values)
    
    return result

@nb.jit(nopython=True)
def fast_rolling_std(values, window, min_periods):
    """Fast rolling standard deviation using numba"""
    n = len(values)
    result = np.full(n, np.nan)
    
    for i in range(window-1, n):
        start_idx = i - window + 1
        window_values = values[start_idx:i+1]
        
        # Remove NaN values
        valid_values = window_values[~np.isnan(window_values)]
        
        if len(valid_values) >= min_periods:
            result[i] = np.std(valid_values)
    
    return result

def vectorized_asrol(df, var_col, window, min_periods, group_col, stat='mean', gen_name=None):
    """Vectorized asrol implementation for better performance"""
    
    if gen_name is None:
        gen_name = f'{stat}{window}_{var_col}'
    
    def process_group(group):
        values = group[var_col].values
        
        if stat == 'mean':
            rolling_result = fast_rolling_mean(values, window, min_periods)
        elif stat == 'sd':
            rolling_result = fast_rolling_std(values, window, min_periods)
        else:
            # Fallback to pandas for other statistics
            if stat == 'sum':
                rolling_result = group[var_col].rolling(window=window, min_periods=min_periods).sum().values
            elif stat == 'count':
                rolling_result = group[var_col].rolling(window=window, min_periods=min_periods).count().values
            elif stat == 'min':
                rolling_result = group[var_col].rolling(window=window, min_periods=min_periods).min().values
            elif stat == 'max':
                rolling_result = group[var_col].rolling(window=window, min_periods=min_periods).max().values
            else:
                raise ValueError(f"Unsupported statistic: {stat}")
        
        group[gen_name] = rolling_result
        return group
    
    return df.groupby(group_col).apply(process_group).reset_index(drop=True)
```

## Complete Translation Examples

### Example 1: Turnover Standard Deviation (std_turn.do)
**Stata:**
```stata
bys permno (time_avail_m): gen time_temp = _n
xtset permno time_temp
asrol turn, window(time_temp 36) min(6) by(permno) stat(sd) gen(std_turn)
```

**Python:**
```python
import pandas as pd
import numpy as np

def calculate_std_turn(df):
    """Calculate 36-month rolling standard deviation of turnover"""
    
    # Sort by permno and time (equivalent to bys permno (time_avail_m))
    df = df.sort_values(['permno', 'time_avail_m'])
    
    # Create time index within each group (equivalent to gen time_temp = _n)
    df['time_temp'] = df.groupby('permno').cumcount() + 1
    
    # Calculate rolling standard deviation (asrol translation)
    df['std_turn'] = df.groupby('permno')['turn'].transform(
        lambda x: x.rolling(window=36, min_periods=6).std()
    )
    
    return df

# Usage
df = calculate_std_turn(df)
```

### Example 2: Industry Concentration (Herf.do)
**Stata:**
```stata
asrol herf_comp, window(time_temp 36) min(6) by(permno) stat(mean) gen(Herf)
```

**Python:**
```python
def calculate_herf(df):
    """Calculate 36-month rolling mean of Herfindahl index"""
    
    # Ensure proper sorting
    df = df.sort_values(['permno', 'time_avail_m'])
    
    # Calculate rolling mean
    df['Herf'] = df.groupby('permno')['herf_comp'].transform(
        lambda x: x.rolling(window=36, min_periods=6).mean()
    )
    
    return df

# Usage
df = calculate_herf(df)
```

### Example 3: Investment Rolling Mean (Investment.do)
**Stata:**
```stata
asrol investment_asset, window(time_temp 36) min(6) by(permno) stat(mean) gen(mean36_investment)
```

**Python:**
```python
def calculate_investment_rolling(df):
    """Calculate 36-month rolling mean of investment"""
    
    # Sort data
    df = df.sort_values(['permno', 'time_avail_m'])
    
    # Calculate rolling mean
    df['mean36_investment'] = df.groupby('permno')['investment_asset'].transform(
        lambda x: x.rolling(window=36, min_periods=6).mean()
    )
    
    return df

# Usage
df = calculate_investment_rolling(df)
```

### Example 4: Dividend Statistics (DivYieldST.do)
**Stata:**
```stata
asrol dfy_rolling, window(time_temp 36) min(6) by(permno) stat(mean) gen(mean_dfy)
asrol dfy_rolling, window(time_temp 36) min(6) by(permno) stat(sd) gen(std_dfy)
```

**Python:**
```python
def calculate_dividend_stats(df):
    """Calculate rolling dividend yield statistics"""
    
    # Sort data
    df = df.sort_values(['permno', 'time_avail_m'])
    
    # Calculate multiple rolling statistics
    grouped = df.groupby('permno')['dfy_rolling']
    
    df['mean_dfy'] = grouped.transform(
        lambda x: x.rolling(window=36, min_periods=6).mean()
    )
    
    df['std_dfy'] = grouped.transform(
        lambda x: x.rolling(window=36, min_periods=6).std()
    )
    
    return df

# Usage
df = calculate_dividend_stats(df)
```

## Advanced Patterns

### Pattern 1: Custom Window Indexing
```python
def custom_window_asrol(df, var_col, window_col, window_size, min_periods, group_col, stat='mean'):
    """Handle custom window variables like time_temp"""
    
    def process_group(group):
        # Sort by window variable
        group = group.sort_values(window_col)
        
        # Reset window index
        group['_window_idx'] = range(len(group))
        
        # Calculate rolling statistic using window index
        if stat == 'mean':
            rolling_result = group[var_col].rolling(window=window_size, min_periods=min_periods).mean()
        elif stat == 'sd':
            rolling_result = group[var_col].rolling(window=window_size, min_periods=min_periods).std()
        else:
            raise ValueError(f"Statistic {stat} not implemented")
        
        return rolling_result
    
    return df.groupby(group_col).apply(process_group).reset_index(drop=True)
```

### Pattern 2: Conditional Rolling Statistics
```python
def conditional_asrol(df, var_col, condition_col, window, min_periods, group_col, stat='mean'):
    """Apply rolling statistics only when condition is met"""
    
    def process_group(group):
        # Apply condition filter
        filtered_group = group[group[condition_col] == True].copy()
        
        if len(filtered_group) == 0:
            return pd.Series([np.nan] * len(group), index=group.index)
        
        # Calculate rolling statistic on filtered data
        if stat == 'mean':
            rolling_result = filtered_group[var_col].rolling(window=window, min_periods=min_periods).mean()
        elif stat == 'sd':
            rolling_result = filtered_group[var_col].rolling(window=window, min_periods=min_periods).std()
        else:
            raise ValueError(f"Statistic {stat} not implemented")
        
        # Reindex to original group
        return rolling_result.reindex(group.index)
    
    return df.groupby(group_col).apply(process_group).reset_index(drop=True)
```

## Validation Checklist

After translating `asrol` commands:
1. ✅ Verify rolling window size matches Stata exactly
2. ✅ Check minimum observations requirement (`min_periods`)
3. ✅ Confirm statistic calculations (mean, sd, etc.)
4. ✅ Test group-wise operations preserve panel structure
5. ✅ Validate proper sorting within groups
6. ✅ Check edge cases (start/end of time series)
7. ✅ Test performance with large datasets

## Common Mistakes

### ❌ WRONG: Not sorting data within groups
```python
# Will produce incorrect rolling statistics
df['rolling_mean'] = df.groupby('permno')['variable'].transform(
    lambda x: x.rolling(36).mean()
)
```

### ❌ WRONG: Ignoring minimum periods requirement
```python
# May produce statistics with too few observations
df['rolling_mean'] = df.rolling(36).mean()
```

### ❌ WRONG: Using global rolling instead of group-wise
```python
# Rolls across different companies inappropriately
df['rolling_mean'] = df['variable'].rolling(36).mean()
```

### ❌ WRONG: Not handling missing values properly
```python
# Missing values may break rolling calculations
df['rolling_std'] = df.groupby('permno')['variable'].rolling(36).std()
```

### ✅ CORRECT: Proper asrol translation setup
```python
# Proper sorting, grouping, and parameters
df = df.sort_values(['permno', 'time_avail_m'])
df['rolling_stat'] = df.groupby('permno')['variable'].transform(
    lambda x: x.rolling(window=36, min_periods=6).mean()
)
```

## Key Differences from asreg

1. **Simplicity**: asrol only calculates statistics, not regressions
2. **Performance**: Generally faster than asreg equivalents
3. **Built-in support**: Pandas rolling methods map directly to most asrol functionality
4. **Less complex validation**: No coefficient or R-squared validation needed

## Files Using asrol in Our Codebase

1. **DivInit.do** - Dividend initiation rolling statistics
2. **DivOmit.do** - Dividend omission tracking
3. **DivSeason.do** - Seasonal dividend patterns  
4. **DivYieldST.do** - Short-term dividend yield rolling stats
5. **Herf.do** - Herfindahl index rolling mean
6. **HerfAsset.do** - Asset-based Herfindahl rolling mean
7. **HerfBE.do** - Book equity Herfindahl rolling mean
8. **std_turn.do** - Turnover standard deviation

## Translation Strategy Summary

### For asrol (Rolling Statistics):
1. **Simple statistics**: Use pandas `.rolling()` with appropriate window and `min_periods`
2. **Group operations**: Use `.groupby().transform()` pattern for `by()` option
3. **Custom statistics**: Implement using numba for performance if needed
4. **Window management**: Convert Stata's window syntax to pandas parameters
5. **Sorting**: Always ensure proper sorting within groups before rolling operations

### Performance Considerations:
1. **polars**: Use for very large datasets (6x speedup)
2. **numba**: Use for custom statistics not available in pandas
3. **vectorization**: Prefer vectorized operations over loop-based approaches
4. **memory**: Consider chunking for extremely large panels

## Notes

- asrol translations are generally simpler and more reliable than asreg
- Most validation issues stem from data alignment rather than statistical calculation differences
- Rolling statistics in pandas closely match Stata's asrol behavior
- Performance gains are substantial with modern libraries (polars, numba)