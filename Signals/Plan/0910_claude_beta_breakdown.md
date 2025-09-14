# ZZ1 Beta Files Line-by-Line Comparison - Section 5 Market Aggregation

## Overview
Detailed line-by-line breakdown of the Market Aggregation section (Preserve/Restore block):
- **Stata**: `Code/Placebos/ZZ1_betaRR_betaCC_betaRC_betaCR_betaNet.do` Lines 33-63
- **Python**: `pyCode/Placebos/ZZ1_betaRR_betaCC_betaRC_betaCR_betaNet.py` Lines 70-245

## 1. Preserve/Setup

### Stata
```stata
preserve
```

### Python  
```python
market_subset = df[
    (df['prc'].abs() > 5) & 
    (df['prc'].abs() < 1000) & 
    ((df['exchcd'] == 1) | (df['exchcd'] == 2)) &
    df['prc'].notna() & 
    df['exchcd'].notna()
].copy()
```

## 2. Data Filtering

### Stata
```stata
keep if abs(prc) > 5 & abs(prc) < 1000  
keep if exchcd == 1 | exchcd == 2
```

### Python
```python
# Filtering done in subset creation above
# (df['prc'].abs() > 5) & 
# (df['prc'].abs() < 1000) & 
# ((df['exchcd'] == 1) | (df['exchcd'] == 2))
```

## 3. Market Cap Calculation

### Stata
```stata
gen temp = shrout*abs(prc)
```

### Python
```python
market_subset['temp'] = market_subset['shrout'] * market_subset['prc'].abs()
```

## 4. Unnormalized Liquidity

### Stata
```stata
gen double temp2 = min(ill, (30-.25)/(.3*MarketCapitalization))
replace temp2 = . if mi(ill)
```

### Python
```python
market_subset['ill_float64'] = market_subset['ill'].astype('float64')
market_subset['temp2'] = np.minimum(
    market_subset['ill_float64'], 
    (30 - 0.25) / (0.3 * market_subset['MarketCapitalization'])
)
market_subset.loc[market_subset['ill_float64'].isna(), 'temp2'] = np.nan
```

## 5. Weighted Aggregation

### Stata
```stata
gcollapse (mean) MarketIlliquidity = temp2 rM = vwretd MarketCapitalization [aweight = temp], by(time_avail_m)
```

### Python
```python
market_agg = market_subset.groupby('time_avail_m').apply(
    lambda x: pd.Series({
        'MarketIlliquidity': (x['temp2'] * x['temp']).sum() / x['temp'].sum() if x['temp'].sum() > 0 else np.nan,
        'rM': (x['vwretd'] * x['temp']).sum() / x['temp'].sum() if x['temp'].sum() > 0 else np.nan,
        'MarketCapitalization': (x['MarketCapitalization'] * x['temp']).sum() / x['temp'].sum() if x['temp'].sum() > 0 else np.nan
    })
).reset_index()
```

## 6. Time Series Setup and Lags

### Stata
```stata
tsset time_avail_m
```

### Python
```python
market_agg = market_agg.sort_values('time_avail_m')
market_agg['l1_MarketCapitalization'] = market_agg['MarketCapitalization'].shift(1)
market_agg['l2_MarketCapitalization'] = market_agg['MarketCapitalization'].shift(2)
market_agg['l1_MarketIlliquidity'] = market_agg['MarketIlliquidity'].shift(1)
market_agg['l2_MarketIlliquidity'] = market_agg['MarketIlliquidity'].shift(2)
market_agg['l1_rM'] = market_agg['rM'].shift(1)
market_agg['l2_rM'] = market_agg['rM'].shift(2)
```

## 7. Market Model Variables

### Stata
```stata
gen double temp = .25 + MarketIlliquidity*l.MarketCapitalization
gen double templ1 = .25 + l.MarketIlliquidity*l.MarketCapitalization
gen double templ2 = .25 + l2.MarketIlliquidity*l.MarketCapitalization
```

### Python
```python
market_agg['temp'] = 0.25 + market_agg['MarketIlliquidity'] * market_agg['l1_MarketCapitalization']
market_agg['templ1'] = 0.25 + market_agg['l1_MarketIlliquidity'] * market_agg['l1_MarketCapitalization']
market_agg['templ2'] = 0.25 + market_agg['l2_MarketIlliquidity'] * market_agg['l1_MarketCapitalization']
```

## 8. Illiquidity Rolling Regression

### Stata
```stata
asreg temp templ1 templ2, window(time 60) min(48) fitted
rename _residuals eps_c_M
rename _b_cons APa0
rename _b_templ1 APa1
rename _b_templ2 APa2
drop _*
```

### Python
```python
def rolling_regression_illiquidity(group, window=60, min_periods=48):
    from sklearn.linear_model import LinearRegression
    
    group = group.sort_values('time_avail_m')
    group['eps_c_M'] = np.nan
    group['APa0'] = np.nan
    group['APa1'] = np.nan
    group['APa2'] = np.nan
    
    for i in range(len(group)):
        if i < min_periods - 1:
            continue
            
        start_idx = max(0, i - window + 1)
        window_data = group.iloc[start_idx:i+1]
        
        complete_mask = (
            window_data['temp'].notna() & 
            window_data['templ1'].notna() & 
            window_data['templ2'].notna()
        )
        
        if complete_mask.sum() < min_periods:
            continue
        
        y = window_data.loc[complete_mask, 'temp'].values
        X = window_data.loc[complete_mask, ['templ1', 'templ2']].values
        X_with_const = np.column_stack([np.ones(len(X)), X])
        
        if len(y) < min_periods:
            continue
            
        try:
            reg = LinearRegression(fit_intercept=False)
            reg.fit(X_with_const, y)
            
            group.iloc[i, group.columns.get_loc('APa0')] = reg.coef_[0]
            group.iloc[i, group.columns.get_loc('APa1')] = reg.coef_[1]
            group.iloc[i, group.columns.get_loc('APa2')] = reg.coef_[2]
            
            current_temp = group.iloc[i]['temp']
            current_templ1 = group.iloc[i]['templ1']
            current_templ2 = group.iloc[i]['templ2']
            
            if pd.notna(current_temp) and pd.notna(current_templ1) and pd.notna(current_templ2):
                fitted = reg.coef_[0] + reg.coef_[1] * current_templ1 + reg.coef_[2] * current_templ2
                group.iloc[i, group.columns.get_loc('eps_c_M')] = current_temp - fitted
                
        except:
            continue
            
    return group

market_agg = rolling_regression_illiquidity(market_agg)
```

## 9. Return Model Variables

### Stata
```stata
gen tempRlag1 = l.rM
gen tempRlag2 = l2.rM
```

### Python
```python
# Already created in step 6:
# market_agg['l1_rM'] = market_agg['rM'].shift(1)
# market_agg['l2_rM'] = market_agg['rM'].shift(2)
```

## 10. Return Rolling Regression

### Stata
```stata
asreg rM tempRlag1 tempRlag2, window(time 60) min(48) fitted
rename _residuals eps_r_M
```

### Python
```python
def rolling_regression_returns(group, window=60, min_periods=48):
    from sklearn.linear_model import LinearRegression
    
    group = group.sort_values('time_avail_m')
    group['eps_r_M'] = np.nan
    
    for i in range(len(group)):
        if i < min_periods - 1:
            continue
            
        start_idx = max(0, i - window + 1)
        window_data = group.iloc[start_idx:i+1]
        
        complete_mask = (
            window_data['rM'].notna() & 
            window_data['l1_rM'].notna() & 
            window_data['l2_rM'].notna()
        )
        
        if complete_mask.sum() < min_periods:
            continue
        
        y = window_data.loc[complete_mask, 'rM'].values
        X = window_data.loc[complete_mask, ['l1_rM', 'l2_rM']].values
        X_with_const = np.column_stack([np.ones(len(X)), X])
        
        if len(y) < min_periods:
            continue
            
        try:
            reg = LinearRegression(fit_intercept=False)
            reg.fit(X_with_const, y)
            
            current_rM = group.iloc[i]['rM']
            current_l1_rM = group.iloc[i]['l1_rM']
            current_l2_rM = group.iloc[i]['l2_rM']
            
            if pd.notna(current_rM) and pd.notna(current_l1_rM) and pd.notna(current_l2_rM):
                fitted = reg.coef_[0] + reg.coef_[1] * current_l1_rM + reg.coef_[2] * current_l2_rM
                group.iloc[i, group.columns.get_loc('eps_r_M')] = current_rM - fitted
                
        except:
            continue
            
    return group

market_agg = rolling_regression_returns(market_agg)
```

## 11. Save and Restore

### Stata
```stata
keep time_avail_m eps* AP*
save "$pathtemp/tempPlacebo", replace
restore
```

### Python
```python
temp_placebo = market_agg[['time_avail_m', 'eps_c_M', 'eps_r_M', 'APa0', 'APa1', 'APa2']].copy()
# No restore needed - using merge instead of preserve/restore pattern
```

## Key Differences and Potential Issues

1. **Weighted Aggregation Method**:
   - **Stata**: Uses built-in `gcollapse [aweight=temp]` for weighted means
   - **Python**: Manual implementation with `(x['temp2'] * x['temp']).sum() / x['temp'].sum()`
   - **Risk**: Mathematical differences in handling edge cases, missing values

2. **Rolling Regression Implementation**:
   - **Stata**: Uses `asreg window(time 60) min(48)` - built-in, optimized
   - **Python**: Custom implementation with sklearn LinearRegression
   - **Risk**: Different windowing logic, coefficient calculation, residual computation

3. **Lag Creation Timing**:
   - **Stata**: Creates lags implicitly after `tsset` on aggregated data
   - **Python**: Uses simple `shift()` on aggregated data (position-based)
   - **Risk**: If market data has gaps, position-based vs calendar-based differences

4. **Missing Value Propagation**:
   - **Stata**: Built-in missing value handling in aggregation and regression
   - **Python**: Explicit handling with multiple conditional checks
   - **Risk**: Different treatment of missing values in edge cases

5. **Precision and Numerical Stability**:
   - **Stata**: Uses native double precision throughout
   - **Python**: Explicit float64 conversion, potential pandas dtype issues
   - **Risk**: Floating point precision differences accumulating over calculations