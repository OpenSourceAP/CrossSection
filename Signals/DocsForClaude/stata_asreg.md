# Stata `asreg` Command Translation to Python

## Overview

The `asreg` command in Stata performs rolling window regressions and by-group regressions efficiently. It's widely used in finance for calculating rolling betas, time-varying coefficients, and other moving statistics.

## Stata Syntax and Usage

### Basic Syntax
```stata
asreg depvar indepvars [if] [in], window([rangevar] #) [options]
```

### Key Options
- `window(rangevar #)`: Length of rolling window
- `by(varlist)`: Group variables
- `recursive`: Expanding window instead of rolling
- `minimum(#)`: Minimum observations required

### Common Patterns from Our Codebase

**Example 1: Rolling CAPM Beta (Beta.do)**
```stata
bys permno (time_avail_m): gen time_temp = _n
xtset permno time_temp
asreg retrf ewmktrf, window(time_temp 60) min(20) by(permno)
rename _b_ewmktrf Beta
```

**Example 2: Standard rolling regression**
```stata
asreg stock_return market_return, window(month 36) by(permno)
```

**Example 3: Multiple independent variables**
```stata
asreg returns factor1 factor2 factor3, window(date 60) by(firm_id)
```

## Python Translation Patterns

### Method 1: Using pandas rolling with apply
```python
def rolling_regression(df, y_col, x_cols, window, min_periods=None):
    """Basic rolling regression function"""
    from sklearn.linear_model import LinearRegression
    import numpy as np
    
    def fit_regression(data):
        if len(data) < (min_periods or window//2):
            return pd.Series([np.nan] * (len(x_cols) + 3), 
                           index=[f'_b_{col}' for col in x_cols] + ['_b_cons', '_R2', 'obs_N'])
        
        y = data[y_col].dropna()
        X = data[x_cols].dropna()
        
        # Align y and X
        common_idx = y.index.intersection(X.index)
        if len(common_idx) < (min_periods or window//2):
            return pd.Series([np.nan] * (len(x_cols) + 3), 
                           index=[f'_b_{col}' for col in x_cols] + ['_b_cons', '_R2', 'obs_N'])
        
        y_clean = y.loc[common_idx]
        X_clean = X.loc[common_idx]
        
        # Fit regression
        reg = LinearRegression()
        reg.fit(X_clean, y_clean)
        
        # Calculate R-squared
        y_pred = reg.predict(X_clean)
        ss_tot = np.sum((y_clean - y_clean.mean()) ** 2)
        ss_res = np.sum((y_clean - y_pred) ** 2)
        r_squared = 1 - (ss_res / ss_tot) if ss_tot > 0 else 0
        
        # Return results
        results = {}
        for i, col in enumerate(x_cols):
            results[f'_b_{col}'] = reg.coef_[i]
        results['_b_cons'] = reg.intercept_
        results['_R2'] = r_squared
        results['obs_N'] = len(y_clean)
        
        return pd.Series(results)
    
    return df.rolling(window=window, min_periods=min_periods).apply(fit_regression, raw=False)
```

### Method 2: Group-wise Rolling Regression
```python
def group_rolling_regression(df, group_cols, y_col, x_cols, window, min_periods=20):
    """Rolling regression by groups (like asreg by() option)"""
    def process_group(group):
        # Sort by time within group
        group = group.sort_index()
        
        # Apply rolling regression
        results = rolling_regression(group, y_col, x_cols, window, min_periods)
        
        # Combine with original data
        for col in results.columns:
            group[col] = results[col]
        
        return group
    
    return df.groupby(group_cols).apply(process_group).reset_index(drop=True)
```

## Complete Translation Examples

### Example 1: CAPM Beta Calculation
**Stata:**
```stata
bys permno (time_avail_m): gen time_temp = _n
xtset permno time_temp
asreg retrf ewmktrf, window(time_temp 60) min(20) by(permno)
rename _b_ewmktrf Beta
```

**Python:**
```python
import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression

def calculate_rolling_beta(df, window=60, min_periods=20):
    """Calculate rolling CAPM beta"""
    def rolling_beta(group):
        # Sort by time
        group = group.sort_values('time_avail_m')
        
        def fit_beta(data):
            if len(data) < min_periods:
                return pd.Series([np.nan, np.nan, np.nan], 
                               index=['_b_ewmktrf', '_b_cons', '_R2'])
            
            y = data['retrf'].dropna()
            x = data['ewmktrf'].dropna()
            
            # Align data
            common_idx = y.index.intersection(x.index)
            if len(common_idx) < min_periods:
                return pd.Series([np.nan, np.nan, np.nan], 
                               index=['_b_ewmktrf', '_b_cons', '_R2'])
            
            y_clean = y.loc[common_idx].values
            x_clean = x.loc[common_idx].values.reshape(-1, 1)
            
            # Fit regression
            reg = LinearRegression()
            reg.fit(x_clean, y_clean)
            
            # Calculate R-squared
            y_pred = reg.predict(x_clean)
            ss_tot = np.sum((y_clean - y_clean.mean()) ** 2)
            ss_res = np.sum((y_clean - y_pred) ** 2)
            r_squared = 1 - (ss_res / ss_tot) if ss_tot > 0 else 0
            
            return pd.Series([reg.coef_[0], reg.intercept_, r_squared], 
                           index=['_b_ewmktrf', '_b_cons', '_R2'])
        
        # Apply rolling regression
        rolling_results = group.rolling(window=window, min_periods=min_periods).apply(
            fit_beta, raw=False
        )
        
        # Add results to group
        for col in rolling_results.columns:
            group[col] = rolling_results[col]
        
        return group
    
    # Apply to each permno
    result = df.groupby('permno').apply(rolling_beta).reset_index(drop=True)
    
    # Rename beta coefficient (equivalent to rename _b_ewmktrf Beta)
    result['Beta'] = result['_b_ewmktrf']
    
    return result

# Usage
df = calculate_rolling_beta(df, window=60, min_periods=20)
```

### Example 2: Multi-factor Rolling Regression
**Stata:**
```stata
asreg returns factor1 factor2 factor3, window(date 60) by(firm_id)
```

**Python:**
```python
def multi_factor_rolling_regression(df, y_col, x_cols, group_col, window=60, min_periods=20):
    """Multi-factor rolling regression"""
    def process_group(group):
        group = group.sort_values('date')
        
        def fit_regression(data):
            if len(data) < min_periods:
                results = {f'_b_{col}': np.nan for col in x_cols}
                results.update({'_b_cons': np.nan, '_R2': np.nan, 'obs_N': np.nan})
                return pd.Series(results)
            
            y = data[y_col].dropna()
            X = data[x_cols].dropna()
            
            # Align data
            common_idx = y.index.intersection(X.index)
            if len(common_idx) < min_periods:
                results = {f'_b_{col}': np.nan for col in x_cols}
                results.update({'_b_cons': np.nan, '_R2': np.nan, 'obs_N': np.nan})
                return pd.Series(results)
            
            y_clean = y.loc[common_idx]
            X_clean = X.loc[common_idx]
            
            # Fit regression
            reg = LinearRegression()
            reg.fit(X_clean, y_clean)
            
            # Calculate R-squared
            y_pred = reg.predict(X_clean)
            ss_tot = np.sum((y_clean - y_clean.mean()) ** 2)
            ss_res = np.sum((y_clean - y_pred) ** 2)
            r_squared = 1 - (ss_res / ss_tot) if ss_tot > 0 else 0
            
            # Build results
            results = {}
            for i, col in enumerate(x_cols):
                results[f'_b_{col}'] = reg.coef_[i]
            results['_b_cons'] = reg.intercept_
            results['_R2'] = r_squared
            results['obs_N'] = len(y_clean)
            
            return pd.Series(results)
        
        # Apply rolling regression
        rolling_results = group.rolling(window=window, min_periods=min_periods).apply(
            fit_regression, raw=False
        )
        
        # Add results to group
        for col in rolling_results.columns:
            group[col] = rolling_results[col]
        
        return group
    
    return df.groupby(group_col).apply(process_group).reset_index(drop=True)

# Usage
factor_cols = ['factor1', 'factor2', 'factor3']
df = multi_factor_rolling_regression(df, 'returns', factor_cols, 'firm_id', window=60)
```

### Example 3: Optimized Rolling Regression Class
**Python:**
```python
class RollingRegression:
    """Optimized rolling regression class similar to asreg"""
    
    def __init__(self, window=60, min_periods=20):
        self.window = window
        self.min_periods = min_periods
    
    def fit(self, df, y_col, x_cols, group_col=None, time_col=None):
        """
        Fit rolling regression
        
        Parameters:
        - df: DataFrame
        - y_col: dependent variable
        - x_cols: list of independent variables
        - group_col: grouping variable (like by() option)
        - time_col: time variable for sorting
        """
        if group_col:
            return df.groupby(group_col).apply(
                lambda x: self._fit_group(x, y_col, x_cols, time_col)
            ).reset_index(drop=True)
        else:
            return self._fit_group(df, y_col, x_cols, time_col)
    
    def _fit_group(self, group, y_col, x_cols, time_col):
        """Fit rolling regression for a single group"""
        if time_col:
            group = group.sort_values(time_col)
        
        def fit_window(data):
            if len(data) < self.min_periods:
                return self._empty_results(x_cols)
            
            # Prepare data
            y = data[y_col].dropna()
            X = data[x_cols].dropna()
            
            # Find common observations
            common_idx = y.index.intersection(X.index)
            if len(common_idx) < self.min_periods:
                return self._empty_results(x_cols)
            
            y_clean = y.loc[common_idx]
            X_clean = X.loc[common_idx]
            
            # Fit regression
            try:
                reg = LinearRegression()
                reg.fit(X_clean, y_clean)
                
                # Calculate statistics
                y_pred = reg.predict(X_clean)
                ss_tot = np.sum((y_clean - y_clean.mean()) ** 2)
                ss_res = np.sum((y_clean - y_pred) ** 2)
                r_squared = 1 - (ss_res / ss_tot) if ss_tot > 0 else 0
                
                # Build results
                results = {}
                for i, col in enumerate(x_cols):
                    results[f'_b_{col}'] = reg.coef_[i]
                results['_b_cons'] = reg.intercept_
                results['_R2'] = r_squared
                results['obs_N'] = len(y_clean)
                
                return pd.Series(results)
            
            except:
                return self._empty_results(x_cols)
        
        # Apply rolling regression
        rolling_results = group.rolling(
            window=self.window, 
            min_periods=self.min_periods
        ).apply(fit_window, raw=False)
        
        # Add results to group
        for col in rolling_results.columns:
            group[col] = rolling_results[col]
        
        return group
    
    def _empty_results(self, x_cols):
        """Return empty results for insufficient data"""
        results = {f'_b_{col}': np.nan for col in x_cols}
        results.update({'_b_cons': np.nan, '_R2': np.nan, 'obs_N': np.nan})
        return pd.Series(results)

# Usage
reg = RollingRegression(window=60, min_periods=20)
df = reg.fit(df, 'retrf', ['ewmktrf'], group_col='permno', time_col='time_avail_m')
df['Beta'] = df['_b_ewmktrf']  # Rename coefficient
```

## Performance Optimization

### Using Numba for Speed
```python
import numba as nb

@nb.jit(nopython=True)
def fast_rolling_ols(y, x, window, min_periods):
    """Fast rolling OLS using numba"""
    n = len(y)
    betas = np.full(n, np.nan)
    r_squared = np.full(n, np.nan)
    
    for i in range(window-1, n):
        start_idx = i - window + 1
        
        # Extract window data
        y_window = y[start_idx:i+1]
        x_window = x[start_idx:i+1]
        
        # Remove NaN values
        mask = ~(np.isnan(y_window) | np.isnan(x_window))
        if np.sum(mask) < min_periods:
            continue
        
        y_clean = y_window[mask]
        x_clean = x_window[mask]
        
        # Calculate regression
        n_obs = len(y_clean)
        x_mean = np.mean(x_clean)
        y_mean = np.mean(y_clean)
        
        # Beta calculation
        numerator = np.sum((x_clean - x_mean) * (y_clean - y_mean))
        denominator = np.sum((x_clean - x_mean) ** 2)
        
        if denominator > 0:
            beta = numerator / denominator
            alpha = y_mean - beta * x_mean
            
            # R-squared
            y_pred = alpha + beta * x_clean
            ss_tot = np.sum((y_clean - y_mean) ** 2)
            ss_res = np.sum((y_clean - y_pred) ** 2)
            r2 = 1 - (ss_res / ss_tot) if ss_tot > 0 else 0
            
            betas[i] = beta
            r_squared[i] = r2
    
    return betas, r_squared
```

### Vectorized Implementation
```python
def vectorized_rolling_regression(df, y_col, x_col, group_col, window=60, min_periods=20):
    """Vectorized rolling regression for better performance"""
    def process_group(group):
        group = group.sort_values('date')
        
        y = group[y_col].values
        x = group[x_col].values
        
        betas, r_squared = fast_rolling_ols(y, x, window, min_periods)
        
        group[f'_b_{x_col}'] = betas
        group['_R2'] = r_squared
        
        return group
    
    return df.groupby(group_col).apply(process_group).reset_index(drop=True)
```

## Validation Checklist

After translating `asreg` commands:
1. ✅ Verify rolling window size matches Stata exactly
2. ✅ Check minimum observations requirement
3. ✅ Confirm coefficient and R-squared calculations
4. ✅ Test group-wise operations preserve panel structure
5. ✅ Validate performance with large datasets

## Common Mistakes

### ❌ WRONG: Not sorting data before rolling regression
```python
df['beta'] = df.groupby('permno')['return'].rolling(60).apply(regression_func)
```

### ❌ WRONG: Ignoring minimum observations requirement
```python
# May produce unstable results with few observations
df['beta'] = df.rolling(60).apply(regression_func)
```

### ❌ WRONG: Not handling missing values properly
```python
# May break with NaN values
reg = LinearRegression()
reg.fit(X_window, y_window)
```

### ✅ CORRECT: Proper rolling regression setup
```python
df = df.sort_values(['permno', 'date'])
df['beta'] = df.groupby('permno').apply(
    lambda x: rolling_regression(x, 'return', ['market'], window=60, min_periods=20)
).reset_index(drop=True)
```