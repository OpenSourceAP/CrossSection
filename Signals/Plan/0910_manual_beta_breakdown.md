# Potential Differences

## First Section

### Stata Lines 24-27: Market Cap Indexing
```stata
sum usdval if time_avail_m == ym(1962,7)
replace usdval = usdval/`r(mean)'
rename usdval MarketCapitalization
```

### Python Lines 45-53: Market Cap Indexing
```python
july_1962 = pd.to_datetime('1962-07-01')
july_1962_val = df.loc[df['time_avail_m'] == july_1962, 'usdval'].mean()
if pd.isna(july_1962_val):
    print("Warning: No July 1962 market cap data found, using first available value")
    july_1962_val = df['usdval'].dropna().iloc[0]
df['usdval'] = df['usdval'] / july_1962_val
df = df.rename(columns={'usdval': 'MarketCapitalization'})
```

**Key Differences**:
- Python has fallback logic for missing July 1962 data
- Stata uses `ym(1962,7)`, Python uses `pd.to_datetime('1962-07-01')`

--> *Does referring to 07-01 differ than referring to general 7 month?*
    - If so, ensure the python logic will take up the same obs in all cases. (If the obs is 7/1, 7/2, etc)

------------------------------------------------------------------------
------------------------------------------------------------------------
------------------------------------------------------------------------

## Market Aggregation (Preserve/Restore Block)

### Stata Lines 33-63: Market Aggregation
```stata
preserve
    keep if abs(prc) > 5 & abs(prc) < 1000  
    keep if exchcd == 1 | exchcd == 2
    gen temp = shrout*abs(prc)
    gen double temp2 = min(ill, (30-.25)/(.3*MarketCapitalization))
    replace temp2 = . if mi(ill)
    gcollapse (mean) MarketIlliquidity = temp2 rM = vwretd MarketCapitalization [aweight = temp], by(time_avail_m)
```

### Python Lines 70-245: Market Aggregation
```python
market_subset = df[
    (df['prc'].abs() > 5) & 
    (df['prc'].abs() < 1000) & 
    ((df['exchcd'] == 1) | (df['exchcd'] == 2)) &
    df['prc'].notna() & 
    df['exchcd'].notna()
].copy()

market_subset['temp'] = market_subset['shrout'] * market_subset['prc'].abs()
market_subset['ill_float64'] = market_subset['ill'].astype('float64')
market_subset['temp2'] = np.minimum(
    market_subset['ill_float64'], 
    (30 - 0.25) / (0.3 * market_subset['MarketCapitalization'])
)
market_subset.loc[market_subset['ill_float64'].isna(), 'temp2'] = np.nan

market_agg = market_subset.groupby('time_avail_m').apply(
    lambda x: pd.Series({
        'MarketIlliquidity': (x['temp2'] * x['temp']).sum() / x['temp'].sum() if x['temp'].sum() > 0 else np.nan,
        'rM': (x['vwretd'] * x['temp']).sum() / x['temp'].sum() if x['temp'].sum() > 0 else np.nan,
        'MarketCapitalization': (x['MarketCapitalization'] * x['temp']).sum() / x['temp'].sum() if x['temp'].sum() > 0 else np.nan
    })
).reset_index()
```

**Key Differences**:
--> *Is python's marketagg created with too many values dropping because of its conditioning to making x.temp.sum > 0?*
    - Ensure that the conditions put in the python market_agg are the same conditions found in stata.

------------------------------------------------------------------------
------------------------------------------------------------------------
------------------------------------------------------------------------

##  Time Series Setup and Lags

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

**Key Differences**:
--> *Are the .shift()'s lagging by actual date or just by row? What does stata's tsset do? Are these two matched?*
    - We already have stata_multi_lag function in our pyCode/utils to use.
    - Ensure that whatever lagging logic python uses matches the lagging logic stata uses.

------------------------------------------------------------------------
------------------------------------------------------------------------
------------------------------------------------------------------------

## Illiquidity Rolling Regression

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

**Key Differences**:
--> *We already have asreg python implementation in pyCode/utils/stata_regress.py which should be used instead*
    - Implement asreg from the above file into this file instead of writing your own.

------------------------------------------------------------------------
------------------------------------------------------------------------
------------------------------------------------------------------------

## Return Rolling Regression

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
**Key Differences**:
--> *We already have asreg python implementation in pyCode/utils/stata_regress.py which should be used instead*
    - Implement asreg from the above file into this file instead of writing your own.
